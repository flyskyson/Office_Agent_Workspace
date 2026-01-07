"""
日志模块
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = 'app', debug: bool = False, verbose: bool = False,
                 log_file: str = None) -> logging.Logger:
    """设置日志记录器

    Args:
        name: 日志记录器名称
        debug: 是否启用调试模式
        verbose: 是否显示详细日志
        log_file: 日志文件路径

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)

    # 如果已经配置过，直接返回
    if logger.handlers:
        return logger

    # 设置日志级别
    level = logging.DEBUG if debug else (logging.INFO if verbose else logging.WARNING)
    logger.setLevel(level)

    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件处理器
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # 文件始终记录 DEBUG 级别
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = 'app') -> logging.Logger:
    """获取日志记录器"""
    return logging.getLogger(name)
