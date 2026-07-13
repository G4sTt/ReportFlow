import os
import asyncio
import logging
from datetime import datetime

from app.pdf_generator import ReportGenerator
from app.database import update_task_status
from app.models import TaskStatus

logger = logging.getLogger(__name__)


async def process_file(task_id: str, input_file: str, output_file: str):
    """
    Фоновая задача обработки файла.
    Читает CSV/Excel, генерирует PDF, обновляет статус.
    """
    try:
        logger.info(f"Начало обработки задачи {task_id}")

        # Небольшая задержка для имитации обработки
        await asyncio.sleep(2)

        # Генерируем PDF отчёт
        generator = ReportGenerator()
        stats = generator.generate(input_file, output_file)

        # Обновляем статус на READY
        update_task_status(
            task_id=task_id,
            status=TaskStatus.READY,
            pdf_filename=os.path.basename(output_file)
        )

        logger.info(f"✅ Задача {task_id} успешно обработана. Статистика: {stats}")

    except Exception as e:
        logger.error(f"❌ Ошибка обработки задачи {task_id}: {e}", exc_info=True)

        # Обновляем статус на FAILED
        update_task_status(
            task_id=task_id,
            status=TaskStatus.FAILED,
            error_message=str(e)
        )