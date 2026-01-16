"""
运算实现模块
预留用于添加更多运算类型
"""

from typing import Union
from abc import ABC, abstractmethod


Number = Union[int, float]


class Operation(ABC):
    """运算基类"""

    @abstractmethod
    def execute(self, a: Number, b: Number) -> float:
        """执行运算"""
        raise NotImplementedError("子类必须实现 execute 方法")


class AddOperation(Operation):
    """加法运算"""

    def execute(self, a: Number, b: Number) -> float:
        """
        执行加法运算

        Args:
            a: 第一个操作数
            b: 第二个操作数

        Returns:
            两数之和
        """
        return float(a + b)


class SubtractOperation(Operation):
    """减法运算"""

    def execute(self, a: Number, b: Number) -> float:
        """
        执行减法运算

        Args:
            a: 被减数
            b: 减数

        Returns:
            两数之差
        """
        return float(a - b)


class MultiplyOperation(Operation):
    """乘法运算"""

    def execute(self, a: Number, b: Number) -> float:
        """
        执行乘法运算

        Args:
            a: 第一个因数
            b: 第二个因数

        Returns:
            两数之积
        """
        return float(a * b)


class DivideOperation(Operation):
    """除法运算"""

    def execute(self, a: Number, b: Number) -> float:
        """
        执行除法运算

        Args:
            a: 被除数
            b: 除数

        Returns:
            两数之商

        Raises:
            ValueError: 当除数为零时
        """
        if b == 0:
            raise ValueError("除数不能为零")
        return float(a / b)
