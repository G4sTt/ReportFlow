from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from enum import Enum
import os
import uuid
import shutil
import logging
from datetime import datetime
from typing import Optional

from app.config import settings
from app.models import TaskStatus, TaskResponse, TaskStatusResponse
from app.database import create_task, get_task
from app.tasks import process_file

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper()))
logger = logging.getLogger(__name__)


# ВРЕМЕННЫЕ МОДЕЛИ (без БД)
class TaskStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    READY = "Ready"
    FAILED = "Failed"


class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    message: str


class TaskStatusResponse(BaseModel):
    id: str
    status: TaskStatus
    pdf_filename: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# Хранилище задач в памяти (ВРЕМЕННО!)
tasks_storage = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Python API запускается (БЕЗ БД - тестовый режим)...")
    yield
    logger.info("👋 Приложение останавливается...")


app = FastAPI(
    title="ReportFlow Python API (TEST MODE)",
    description="Тестовый режим без БД",
    version="1.0.0-test",
    lifespan=lifespan
)


@app.post("/process")
async def process_file_endpoint(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        task_id: str = Form(...),
        user_id: str = Form(...)
):
    if not task_id or not user_id:
        raise HTTPException(status_code=400, detail="task_id и user_id обязательны")

    _, ext = os.path.splitext(file.filename.lower())
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимое расширение. Разрешены: {settings.ALLOWED_EXTENSIONS}"
        )

    # Сохраняем файл
    input_file = os.path.join(settings.UPLOAD_DIR, f"{task_id}_{file.filename}")
    with open(input_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_file = os.path.join(settings.RESULTS_DIR, f"{task_id}_report.pdf")

    # Сохраняем задачу в памяти
    tasks_storage[task_id] = {
        "id": task_id,
        "status": TaskStatus.PROCESSING,
        "pdf_filename": None,
        "error_message": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    # Запускаем обработку в фоне
    background_tasks.add_task(process_file, task_id, input_file, output_file)

    return TaskResponse(
        task_id=task_id,
        status=TaskStatus.PROCESSING,
        message="Файл загружен, обработка начата"
    )


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = tasks_storage.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return TaskStatusResponse(**task)


@app.get("/download/{task_id}")
async def download_pdf(task_id: str):
    task = tasks_storage.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if task["status"] != TaskStatus.READY:
        raise HTTPException(status_code=400, detail="PDF ещё не готов")

    pdf_path = os.path.join(settings.RESULTS_DIR, task["pdf_filename"])
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF файл не найден")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=task["pdf_filename"]
    )


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0-test",
        "mode": "TEST (no database)"
    }