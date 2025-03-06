from sqlalchemy.orm import Session
from app import models
from datetime import datetime

def write_log(message):
    with open('app.log', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n{timestamp} - {message}")

def create_translation_task(db: Session, text: str, languages: list):
    try:
        write_log(f"Creating translation task for text: {text[:50]}...")
        write_log(f"Languages requested: {languages}")
        
        # Validate input
        if not isinstance(languages, list):
            raise ValueError("Languages must be a list")
        
        task = models.TranslationTask(
            text=text,
            languages=languages,
            translations={},
            audio_paths={},
            status="pending"
        )
        
        write_log("Translation task object created")
        
        try:
            db.add(task)
            write_log("Task added to session")
            
            db.commit()
            write_log("Session committed")
            
            db.refresh(task)
            write_log(f"Task refreshed, ID: {task.id}")
            
            return task
            
        except Exception as e:
            write_log(f"Database operation failed: {str(e)}")
            db.rollback()
            raise Exception(f"Database error: {str(e)}")
            
    except Exception as e:
        write_log(f"Error in create_translation_task: {str(e)}")
        if 'db' in locals():
            db.rollback()
        raise

def get_translation_task(db: Session, task_id: int):
    try:
        write_log(f"Fetching task with ID: {task_id}")
        task = db.query(models.TranslationTask).filter(models.TranslationTask.id == task_id).first()
        if task:
            write_log("Task found")
        else:
            write_log("Task not found")
        return task
    except Exception as e:
        write_log(f"Error fetching task: {str(e)}")
        raise

def update_translation_task(db: Session, task_id: int, translations: dict, status: str = "completed", audio_paths: dict = None):
    try:
        write_log(f"Updating task {task_id} with status {status}")
        task = db.query(models.TranslationTask).filter(models.TranslationTask.id == task_id).first()
        if task:
            task.translations = translations
            task.status = status
            if audio_paths is not None:
                task.audio_paths = audio_paths
            db.commit()
            db.refresh(task)
            write_log(f"Successfully updated task {task_id}")
            return task
        else:
            write_log(f"Task {task_id} not found for update")
            return None
    except Exception as e:
        write_log(f"Error updating translation task: {str(e)}")
        db.rollback()
        raise
