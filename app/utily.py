import requests
from sqlalchemy.orm import Session
from app.crud import update_translation_task
import logging
import os
import json
import time
from app.tts import text_to_speech

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Using MyMemory Translation API (free, no authentication needed)
TRANSLATE_ENDPOINT = "https://api.mymemory.translated.net/get"

# Language code mapping
LANGUAGE_CODES = {
    'english': 'en',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'italian': 'it',
    'portuguese': 'pt',
    'russian': 'ru',
    'japanese': 'ja',
    'korean': 'ko',
    'chinese': 'zh',
    # Add common variations
    'en': 'en',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    'it': 'it',
    'pt': 'pt',
    'ru': 'ru',
    'ja': 'ja',
    'ko': 'ko',
    'zh': 'zh',
    # Add full names
    'english': 'en',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'italian': 'it',
    'portuguese': 'pt',
    'russian': 'ru',
    'japanese': 'ja',
    'korean': 'ko',
    'chinese': 'zh'
}

def get_language_code(lang: str) -> str:
    """Convert language name or code to proper ISO code."""
    lang = lang.lower().strip()
    return LANGUAGE_CODES.get(lang, lang)

def perform_translation(task_id: int, text: str, languages: list, db: Session):
    logger.info(f"Starting translation for task {task_id}")
    logger.info(f"Text to translate: {text}")
    logger.info(f"Target languages: {languages}")
    
    translations = {}
    audio_paths = {}
    
    try:
        for lang in languages:
            try:
                logger.info(f"Translating to {lang}...")
                
                # Get proper language code
                lang_code = get_language_code(lang)
                logger.info(f"Using language code: {lang_code}")
                
                # Prepare the request parameters
                params = {
                    "q": text,
                    "langpair": f"en|{lang_code}"
                }
                
                # Make the request with a timeout
                response = requests.get(
                    TRANSLATE_ENDPOINT, 
                    params=params,
                    timeout=10
                )
                response.raise_for_status()
                
                # Parse the response
                result = response.json()
                translated_text = result['responseData']['translatedText']
                
                logger.info(f"Successfully translated to {lang}")
                translations[lang] = translated_text
                
                # Generate audio for the translated text
                try:
                    audio_path = text_to_speech(translated_text, lang_code, task_id)
                    audio_paths[lang] = audio_path
                    logger.info(f"Generated audio file for {lang}: {audio_path}")
                except Exception as e:
                    logger.error(f"Error generating audio for {lang}: {str(e)}")
                    audio_paths[lang] = None
                
                # Update the task status after each successful translation
                current_translations = translations.copy()
                current_audio_paths = audio_paths.copy()
                update_translation_task(db, task_id, current_translations, status="in_progress", audio_paths=current_audio_paths)
                
                # Add a small delay to avoid rate limiting
                time.sleep(1)
                
            except requests.Timeout:
                error_msg = "Translation request timed out"
                logger.error(error_msg)
                translations[lang] = f"Error: {error_msg}"
            except requests.RequestException as e:
                logger.error(f"Error translating to {lang}: {str(e)}")
                translations[lang] = f"Error: {str(e)}"
            except Exception as e:
                logger.error(f"Unexpected error translating to {lang}: {str(e)}")
                translations[lang] = f"Error: {str(e)}"
        
        # All translations completed
        logger.info("All translations completed")
        update_translation_task(db, task_id, translations, status="completed", audio_paths=audio_paths)
        
    except Exception as e:
        error_msg = f"Unexpected error in perform_translation: {str(e)}"
        logger.error(error_msg)
        update_translation_task(db, task_id, {"error": str(e)}, status="failed")
        raise