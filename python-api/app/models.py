from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    READY = "Ready"
    FAILED = "Failed"

class ProcessRequest(BaseModel):
    task_id: UUID
    user_id: UUID

class TaskResponse(BaseModel):
    task_id: UUID
    status: TaskStatus
    message: str
    pdf_filename: Optional[str] = None

class TaskStatusResponse(BaseModel):
    id: UUID
    status: TaskStatus
    pdf_filename: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime