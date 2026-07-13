import json
import os
from datetime import datetime
from typing import Optional

from app.models import TaskStatus

# Путь к JSON файлу (создастся в корне проекта python-api/)
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tasks.json")


def _read_db() -> dict:
    """Читает базу данных из JSON файла"""
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_db(data: dict):
    """Записывает базу данных в JSON файл"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        # default=str нужен, чтобы datetime автоматически превращался в строку
        json.dump(data, f, indent=4, ensure_ascii=False, default=str)


def create_task(task_id: str, user_id: str, filename: str):
    """Создаёт новую задачу в JSON"""
    db = _read_db()
    db[task_id] = {
        "id": task_id,
        "user_id": user_id,
        "filename": filename,
        "status": TaskStatus.PROCESSING.value,  # Сохраняем как строку
        "pdf_filename": None,
        "error_message": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    _write_db(db)


def update_task_status(
    task_id: str,
    status: TaskStatus,
    pdf_filename: str = None,
    error_message: str = None
):
    """Обновляет статус задачи в JSON"""
    db = _read_db()
    if task_id in db:
        db[task_id].update({
            "status": status.value,
            "pdf_filename": pdf_filename,
            "error_message": error_message,
            "updated_at": datetime.utcnow()
        })
        _write_db(db)


def get_task(task_id: str) -> Optional[dict]:
    """Получает задачу по ID"""
    db = _read_db()
    return db.get(task_id)