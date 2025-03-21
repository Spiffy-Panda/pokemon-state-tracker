from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class PaginatedResponse(APIResponse):
    total: int
    page: int
    per_page: int
    total_pages: int
