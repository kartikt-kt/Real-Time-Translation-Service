from gtts import gTTS
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def create_audio_directory():
    """Create a directory to store audio files if it doesn't exist."""
    audio_dir = Path("static/audio")
    audio_dir.mkdir(parents=True, exist_ok=True)
    return audio_dir

def text_to_speech(text: str, language: str, task_id: int) -> str:
    """
    Convert text to speech and save it as an MP3 file.
    
    Args:
        text (str): The text to convert to speech
        language (str): The language code (e.g., 'en', 'es', 'fr')
        task_id (int): The task ID to use in the filename
        
    Returns:
        str: The relative path to the generated audio file
    """
    try:
        # Create audio directory if it doesn't exist
        audio_dir = create_audio_directory()
        
        # Generate a unique filename
        filename = f"task_{task_id}_{language}.mp3"
        filepath = audio_dir / filename
        
        # Convert text to speech
        tts = gTTS(text=text, lang=language)
        
        # Save the audio file
        tts.save(str(filepath))
        
        # Return the relative path for storage in the database
        relative_path = f"/static/audio/{filename}"
        logger.info(f"Generated audio file: {relative_path}")
        
        return relative_path
        
    except Exception as e:
        logger.error(f"Error in text_to_speech: {str(e)}")
        raise 