from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TranslationTask(Base):
    __tablename__ = "translation_tasks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    languages = Column(JSON)
    status = Column(String, default="pending")
    translations = Column(JSON, default={})
    audio_paths = Column(JSON, default={})  # Store paths to audio files for each translation

    def __repr__(self):
        return f"<TranslationTask(id={self.id}, text={self.text[:30]}..., languages={self.languages})>"