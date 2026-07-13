"""
ReportFlow Python API
Микросервис для обработки CSV/Excel файлов и генерации PDF отчётов
"""

__version__ = "1.0.0-test"

from .main import app

__all__ = ["app", "__version__"]