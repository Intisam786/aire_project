from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LogEvent(BaseModel):
    timestamp: datetime
    user: str
    action: Optional[str] = None
    ip: Optional[str] = None
    resource: Optional[str] = None
