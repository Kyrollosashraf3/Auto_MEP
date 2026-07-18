# =============================================================================
# REQUEST SCHEMAS
# =============================================================================

from pydantic import BaseModel, Field
from typing import Optional , List


class MessageItem(BaseModel):
    role: str
    content: str
    
class ChatRequest(BaseModel):
    model: str
    messages: List[MessageItem]
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    max_tokens: Optional[int] = 1024
    
    web_search_mode: Optional[str] = None
    web_search_max_tokens: Optional[int] = None
    web_search_temperature: Optional[float] = None
    web_search_top_p: Optional[float] = None
    stream: Optional[bool] = False

