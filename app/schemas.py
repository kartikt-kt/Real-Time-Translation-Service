from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1)
    languages: List[str] = Field(..., min_items=1)
    
class TaskResponse(BaseModel):
    task_id: int
    
class TranslationStatus(BaseModel):
    task_id: int
    status: str
    translations: Dict[str, str] = Field(default_factory=dict)

    class Config:
        from_attributes = True