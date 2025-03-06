from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import logging
import sys
import traceback
import time
import os
import json
from typing import List, Dict, Optional
import asyncio
import uuid

# Local imports
from app.utily import perform_translation
from app import schemas
from app import crud
from app import models
from app.database import get_db, engine, SessionLocal
from app.tts import text_to_speech

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ping")
def ping():
    logger.info("Ping endpoint called")
    return {"message": "pong"}

@app.post("/translate", response_model=schemas.TaskResponse)
async def translate(request: schemas.TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received translation request: {request.dict()}")
        task = crud.create_translation_task(db, request.text, request.languages)
        logger.info(f"Created task with ID: {task.id}")
        
        background_tasks.add_task(
            perform_translation,
            task.id,
            request.text,
            request.languages,
            db
        )
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)
        
        return {"task_id": task.id}
    except Exception as e:
        logger.error(f"Error in translate endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/translate/{task_id}")
async def get_translation_status(task_id: int, db: Session = Depends(get_db)):
    try:
        task = crud.get_translation_task(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {
            "task_id": task.id,
            "status": task.status,
            "translations": task.translations,
            "audio_paths": task.audio_paths
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting translation status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI application...")
    logger.info("=== Application Starting ===")
    uvicorn.run(app, host="127.0.0.1", port=8001)  # Changed to port 8001
