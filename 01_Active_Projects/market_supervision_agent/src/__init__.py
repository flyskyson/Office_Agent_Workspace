"""
市场监管智能体 v4.0 - 源代码包

核心功能：
- OCR文档识别
- 数据提取和验证
- 文件自动归档
- 申请书自动生成
- 工作流自动化
"""

__version__ = "4.0.0"
__author__ = "Office Agent Workspace"

from .ocr_adapter import OCREngineAdapter, create_ocr_engine
from .data_extractor import DataExtractor, OperatorData
from .database_manager import DatabaseManager
from .file_archiver import FileArchiver
from .application_generator import ApplicationGenerator
from .workflow import (
    MarketSupervisionWorkflow,
    WorkflowState,
    process_files,
    quick_process
)

__all__ = [
    "OCREngineAdapter",
    "create_ocr_engine",
    "DataExtractor",
    "OperatorData",
    "DatabaseManager",
    "FileArchiver",
    "ApplicationGenerator",
    "MarketSupervisionWorkflow",
    "WorkflowState",
    "process_files",
    "quick_process",
]
