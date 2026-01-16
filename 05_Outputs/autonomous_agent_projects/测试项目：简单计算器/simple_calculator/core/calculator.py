"""
计算器核心类
提供基本的四则运算功能
"""

from typing import Union


Number = Union[int, float]


class Calculator:
    """简单计算器核心类"""

    SUPPORTED_OPERATORS = ['+', '-', '*', '/']

    def __init__(self):
        """初始化计算器"""
        pass

    def add(self, a: Number, b: Number) -> float:
        """
        加法运算

        Args:
            a: 第一个操作数
            b: 第二个操作数

        Returns:
            两数之和

        Examples:
            >>> calc = Calculator()
            >>> calc.add(10, 5)
            15.0
            >>> calc.add(-10, 5)
            -5.0
        """
        return float(a + b)

    def subtract(self, a: Number, b: Number) -> float:
        """
        减法运算

        Args:
            a: 被减数
            b: 减数

        Returns:
            两数之差

        Examples:
            >>> calc = Calculator()
            >>> calc.subtract(10, 5)
            5.0
            >>> calc.subtract(5, 10)
            -5.0
        """
        return float(a - b)

    def multiply(self, a: Number, b: Number) -> float:
        """
        乘法运算

        Args:
            a: 第一个因数
            b: 第二个因数

        Returns:
            两数之积

        Examples:
            >>> calc = Calculator()
            >>> calc.multiply(10, 5)
            50.0
            >>> calc.multiply(-10, 5)
            -50.0
        """
        return float(a * b)

    def divide(self, a: Number, b: Number) -> float:
        """
        除法运算

        Args:
            a: 被除数
            b: 除数

        Returns:
            两数之商

        Raises:
            ValueError: 当除数为零时

        Examples:
            >>> calc = Calculator()
            >>> calc.divide(10, 5)
            2.0
            >>> calc.divide(10, 2.5)
            4.0

        """
        if b == 0:
            raise ValueError("除数不能为零")
        return float(a / b)

    def calculate(self, operator: str, a: Number, b: Number) -> float:
        """
        通用计算接口

        Args:
            operator: 运算符 (+, -, *, /)
            a: 第一个操作数
            b: 第二个操作数

        Returns:
            计算结果

        Raises:
            ValueError: 当运算符不支持或除数为零时

        Examples:
            >>> calc = Calculator()
            >>> calc.calculate('+', 10, 5)
            15.0
            >>> calc.calculate('*', 3, 4)
            12.0
        """
        if operator == '+':
            return self.add(a, b)
        elif operator == '-':
            return self.subtract(a, b)
        elif operator == '*':
            return self.multiply(a, b)
        elif operator == '/':
            return self.divide(a, b)
        else:
            raise ValueError(f"不支持的运算符: {operator}. 支持的运算符: {', '.join(self.SUPPORTED_OPERATORS)}")
