from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

# ============================================
# SQLAlchemy Base (для БД)
# ============================================
Base = declarative_base()


# ============================================
# SQLAlchemy модель (для PostgreSQL)
# ============================================

class Task(Base):
    """Модель задачи в PostgreSQL"""
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    input_file_path = Column(String(500), nullable=False)
    pdf_file_path = Column(String(500), nullable=True)
    chart_file_path = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default="Pending")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ============================================
# Pydantic модели (для API)
# ============================================

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