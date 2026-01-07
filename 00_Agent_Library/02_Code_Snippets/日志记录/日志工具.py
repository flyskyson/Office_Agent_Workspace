"""
日志记录工具
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class Logger:
    """简单的日志记录器"""

    def __init__(self, name: str = 'app', log_file: Optional[str] = None,
                 level: str = 'INFO'):
        """初始化日志记录器

        Args:
            name: 日志记录器名称
            log_file: 日志文件路径
            level: 日志级别
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # 避免重复添加处理器
        if not self.logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)

            # 设置格式
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # 文件处理器
            if log_file:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)

                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def debug(self, message: str):
        """调试日志"""
        self.logger.debug(message)

    def info(self, message: str):
        """信息日志"""
        self.logger.info(message)

    def warning(self, message: str):
        """警告日志"""
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """错误日志"""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: bool = False):
        """严重错误日志"""
        self.logger.critical(message, exc_info=exc_info)


# 使用示例
if __name__ == "__main__":
    # 创建日志记录器
    logger = Logger(
        name='my_app',
        log_file='logs/app.log',
        level='DEBUG'
    )

    # 记录不同级别的日志
    logger.debug("这是调试信息")
    logger.info("这是普通信息")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")

    # 带异常堆栈的错误日志
    try:
        1 / 0
    except Exception as e:
        logger.error("发生除零错误", exc_info=True)

    # 使用 Python 标准库 logging
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log', encoding='utf-8')
        ]
    )

    logger_std = logging.getLogger(__name__)
    logger_std.info("使用标准 logging 模块")
