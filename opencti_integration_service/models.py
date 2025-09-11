from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProcessingRequest(BaseModel):
    dump_id: UUID
    s3_url: str


class TaskStatus(BaseModel):
    task_id: UUID
    status: str  # "pending", "processing", "completed", "error"
    progress: float = 0.0
    logs: Optional[str] = None
