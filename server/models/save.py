from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class SaveFile(BaseModel):
    id: str
    name: str
    game_version: str = "Black2White2"
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    data: Dict[str, Any]

class SaveFileCreate(BaseModel):
    name: str
    game_version: str = "Black2White2"

class SaveFileResponse(BaseModel):
    id: str
    name: str
    game_version: str
    created_at: datetime
    last_updated: datetime

class SaveFileList(BaseModel):
    saves: List[SaveFileResponse]
