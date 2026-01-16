"""
输入验证器
负责验证用户输入的合法性
"""

from typing import Tuple, Union


Number = Union[int, float]


class InputValidator:
    """输入验证器"""

    SUPPORTED_OPERATORS = ['+', '-', '*', '/']
    OPERATOR_ALIASES = {
        'add': '+',
        'plus': '+',
        'subtract': '-',
        'minus': '-',
        'multiply': '*',
        'times': '*',
        'divide': '/',
        'div': '/'
    }

    @staticmethod
    def validate_operator(operator: str) -> bool:
        """
        验证运算符是否合法

        Args:
            operator: 待验证的运算符

        Returns:
            True 如果合法，False 否则

        Examples:
            >>> InputValidator.validate_operator('+')
            True
            >>> InputValidator.validate_operator('%')
            False
        """
        # 检查是否为符号运算符
        if operator in InputValidator.SUPPORTED_OPERATORS:
            return True
        # 检查是否为别名运算符
        if operator.lower() in InputValidator.OPERATOR_ALIASES:
            return True
        return False

    @staticmethod
    def normalize_operator(operator: str) -> str:
        """
        标准化运算符

        Args:
            operator: 运算符或别名

        Returns:
            标准化的运算符符号
        """
        if operator in InputValidator.SUPPORTED_OPERATORS:
            return operator
        return InputValidator.OPERATOR_ALIASES.get(operator.lower(), operator)

    @staticmethod
    def validate_number(value: str) -> float:
        """
        验证并转换数字

        Args:
            value: 待验证的数字字符串

        Returns:
            转换后的浮点数

        Raises:
            ValueError: 当不是有效数字时

        Examples:
            >>> InputValidator.validate_number('10')
            10.0
            >>> InputValidator.validate_number('3.14')
            3.14
            >>> InputValidator.validate_number('-5')
            -5.0
        """
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"'{value}' 不是有效的数字")

    @staticmethod
    def validate_arguments(args: list) -> Tuple[str, float, float]:
        """
        验证命令行参数

        Args:
            args: 参数列表 [operator, num1, num2]

        Returns:
            (operator, num1, num2) 元组

        Raises:
            ValueError: 当参数不合法时

        Examples:
            >>> InputValidator.validate_arguments(['+', '10', '5'])
            ('+', 10.0, 5.0)
            >>> InputValidator.validate_arguments(['add', '10', '5'])
            ('+', 10.0, 5.0)
        """
        if len(args) != 3:
            raise ValueError(
                f"需要提供3个参数（运算符 数字1 数字2），实际提供 {len(args)} 个"
            )

        operator_raw, num1_str, num2_str = args

        if not InputValidator.validate_operator(operator_raw):
            raise ValueError(
                f"不支持的运算符 '{operator_raw}'。"
                f"支持的运算符: {', '.join(InputValidator.SUPPORTED_OPERATORS)}"
            )

        # 标准化运算符
        operator = InputValidator.normalize_operator(operator_raw)

        try:
            num1 = InputValidator.validate_number(num1_str)
            num2 = InputValidator.validate_number(num2_str)
        except ValueError as e:
            raise ValueError(f"参数错误: {str(e)}")

        return operator, num1, num2
