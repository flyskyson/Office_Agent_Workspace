"""
Office Agent Workspace - 统一错误处理

提供标准化的错误类型和错误处理工具
"""

import sys
import traceback
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Union
from pathlib import Path


# ================================
# 错误类型定义
# ================================

class ErrorCode(Enum):
    """错误代码枚举"""

    # 通用错误 (1000-1999)
    UNKNOWN_ERROR = 1000
    NOT_IMPLEMENTED = 1001
    INVALID_INPUT = 1002
    OPERATION_FAILED = 1003

    # 配置错误 (2000-2999)
    CONFIG_NOT_FOUND = 2000
    CONFIG_INVALID = 2001
    CONFIG_MISSING_REQUIRED = 2002
    CONFIG_VALIDATION_FAILED = 2003

    # 数据库错误 (3000-3999)
    DATABASE_CONNECTION_ERROR = 3000
    DATABASE_QUERY_ERROR = 3001
    DATABASE_NOT_FOUND = 3002
    DATABASE_CONSTRAINT_ERROR = 3003

    # 智能体错误 (4000-4999)
    AGENT_NOT_FOUND = 4000
    AGENT_EXECUTION_FAILED = 4001
    AGENT_DISABLED = 4002
    AGENT_TIMEOUT = 4003

    # 工作流错误 (5000-5999)
    WORKFLOW_INVALID = 5000
    WORKFLOW_EXECUTION_FAILED = 5001
    WORKFLOW_STEP_FAILED = 5002

    # 文件系统错误 (6000-6999)
    FILE_NOT_FOUND = 6000
    FILE_PERMISSION_ERROR = 6001
    FILE_INVALID_FORMAT = 6002

    # 网络错误 (7000-7999)
    NETWORK_ERROR = 7000
    NETWORK_TIMEOUT = 7001
    NETWORK_UNREACHABLE = 7002


class WorkspaceError(Exception):
    """
    工作区统一错误基类

    所有自定义错误都应该继承此类
    """

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        初始化错误

        参数:
            message: 错误消息
            code: 错误代码
            details: 额外详细信息
        """
        self.message = message
        self.code = code
        self.details = details or {}
        self.timestamp = datetime.now()

        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": False,
            "error": self.message,
            "code": self.code.value,
            "code_name": self.code.name,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "type": self.__class__.__name__
        }

    def __str__(self) -> str:
        return f"[{self.code.name}] {self.message}"


# ================================
# 具体错误类
# ================================

class ConfigError(WorkspaceError):
    """配置相关错误"""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.CONFIG_INVALID,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)


class DatabaseError(WorkspaceError):
    """数据库相关错误"""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.DATABASE_QUERY_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)


class AgentError(WorkspaceError):
    """智能体相关错误"""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.AGENT_EXECUTION_FAILED,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)


class WorkflowError(WorkspaceError):
    """工作流相关错误"""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.WORKFLOW_INVALID,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)


class FileSystemError(WorkspaceError):
    """文件系统相关错误"""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.FILE_NOT_FOUND,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)


class NetworkError(WorkspaceError):
    """网络相关错误"""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.NETWORK_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)


# ================================
# 错误处理工具
# ================================

class ErrorHandler:
    """
    错误处理器

    提供统一的错误处理接口
    """

    @staticmethod
    def handle_error(
        error: Exception,
        include_traceback: bool = False,
        log_file: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        处理错误并返回标准格式

        参数:
            error: 异常对象
            include_traceback: 是否包含堆栈跟踪
            log_file: 日志文件路径（可选）

        返回:
            标准错误响应字典
        """
        # 如果是 WorkspaceError，直接转换
        if isinstance(error, WorkspaceError):
            result = error.to_dict()
        else:
            # 其他异常，包装为 WorkspaceError
            workspace_error = WorkspaceError(
                message=str(error),
                details={"original_type": type(error).__name__}
            )
            result = workspace_error.to_dict()

        # 添加堆栈跟踪（如果需要）
        if include_traceback:
            result["traceback"] = traceback.format_exc()

        # 记录到日志文件
        if log_file:
            ErrorHandler._log_error(result, log_file)

        return result

    @staticmethod
    def _log_error(error_dict: Dict[str, Any], log_file: Path):
        """记录错误到日志文件"""
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{error_dict['timestamp']}] ")
                f.write(f"[{error_dict['code_name']}] ")
                f.write(f"{error_dict['error']}\n")

                if 'traceback' in error_dict:
                    f.write(f"\n{error_dict['traceback']}\n")

                f.write("\n" + "="*80 + "\n\n")
        except Exception as e:
            # 日志记录失败时不抛出异常
            print(f"警告: 无法写入错误日志 - {e}")

    @staticmethod
    def create_response(
        success: bool = True,
        data: Any = None,
        error: Optional[Union[str, Exception]] = None
    ) -> Dict[str, Any]:
        """
        创建标准响应

        参数:
            success: 是否成功
            data: 响应数据
            error: 错误信息（可选）

        返回:
            标准响应字典
        """
        if success:
            return {
                "success": True,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
        else:
            if isinstance(error, Exception):
                return ErrorHandler.handle_error(error)
            else:
                return {
                    "success": False,
                    "error": str(error) if error else "未知错误",
                    "timestamp": datetime.now().isoformat()
                }


# ================================
# 错误装饰器
# ================================

def handle_errors(
    default_return: Any = None,
    reraise: bool = False,
    error_class: type = WorkspaceError
):
    """
    错误处理装饰器

    参数:
        default_return: 发生错误时的默认返回值
        reraise: 是否重新抛出异常
        error_class: 要包装成的错误类

    示例:
        @handle_errors(default_return={"success": False})
        def my_function():
            # 可能抛出异常的代码
            pass
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # 如果已经是 WorkspaceError，直接使用
                if isinstance(e, WorkspaceError):
                    error = e
                else:
                    # 否则包装成指定错误类
                    error = error_class(
                        message=f"{func.__name__} 执行失败: {str(e)}",
                        details={"function": func.__name__}
                    )

                if reraise:
                    raise error
                else:
                    return default_return

        return wrapper
    return decorator


def safe_execute(
    func: callable,
    *args,
    default: Any = None,
    error_callback: Optional[callable] = None,
    **kwargs
) -> Any:
    """
    安全执行函数

    参数:
        func: 要执行的函数
        *args: 位置参数
        default: 默认返回值
        error_callback: 错误回调函数
        **kwargs: 关键字参数

    返回:
        函数执行结果或默认值
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if error_callback:
            error_callback(e)

        return default


# ================================
# 错误上下文管理器
# ================================

class ErrorContext:
    """
    错误上下文管理器

    用于捕获和处理代码块中的错误
    """

    def __init__(
        self,
        error_callback: Optional[callable] = None,
        suppress: bool = False,
        default_return: Any = None
    ):
        """
        初始化上下文管理器

        参数:
            error_callback: 错误回调函数
            suppress: 是否抑制异常
            default_return: 发生错误时的返回值
        """
        self.error_callback = error_callback
        self.suppress = suppress
        self.default_return = default_return
        self.error = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.error = exc_val

            if self.error_callback:
                self.error_callback(exc_val)

            # 抑制异常（如果配置）
            return self.suppress

        return False


# ================================
# 导出
# ================================

__all__ = [
    # 错误代码
    "ErrorCode",

    # 基础错误类
    "WorkspaceError",

    # 具体错误类
    "ConfigError",
    "DatabaseError",
    "AgentError",
    "WorkflowError",
    "FileSystemError",
    "NetworkError",

    # 错误处理工具
    "ErrorHandler",

    # 装饰器和工具函数
    "handle_errors",
    "safe_execute",
    "ErrorContext",
]
