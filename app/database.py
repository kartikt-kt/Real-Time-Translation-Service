import os 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
logger.info(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

try:
    # Create engine without the check_same_thread parameter (it's only for SQLite)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Error creating database engine: {str(e)}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("SessionLocal created")

Base = declarative_base()

def get_db():
    logger.info("Getting database session")
    db = SessionLocal()
    try:
        logger.info("Database session created successfully")
        yield db
    finally:
        logger.info("Closing database session")
        db.close()