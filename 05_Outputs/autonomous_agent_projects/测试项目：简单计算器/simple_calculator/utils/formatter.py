"""
输出格式化器
负责格式化输出结果和错误信息
"""

import json
from typing import Any, Optional


class OutputFormatter:
    """输出格式化器"""

    @staticmethod
    def format_result(
        result: float,
        operator: Optional[str] = None,
        operand1: Optional[float] = None,
        operand2: Optional[float] = None,
        format_type: str = 'text'
    ) -> str:
        """
        格式化输出结果

        Args:
            result: 计算结果
            operator: 运算符（可选）
            operand1: 第一个操作数（可选）
            operand2: 第二个操作数（可选）
            format_type: 输出格式 (text/json)

        Returns:
            格式化后的字符串

        Examples:
            >>> OutputFormatter.format_result(15.0, '+', 10, 5)
            '结果: 15'
            >>> OutputFormatter.format_result(3.14, format_type='json')
            '{"result": 3.14}'
        """
        if format_type == 'json':
            data: dict[str, Any] = {
                "result": result
            }
            if operator:
                data["operator"] = operator
            if operand1 is not None:
                data["operand1"] = operand1
            if operand2 is not None:
                data["operand2"] = operand2
            return json.dumps(data, ensure_ascii=False)
        else:
            # 文本格式
            if result.is_integer():
                return f"结果: {int(result)}"
            else:
                return f"结果: {result}"

    @staticmethod
    def format_error(error_msg: str) -> str:
        """
        格式化错误信息

        Args:
            error_msg: 错误信息

        Returns:
            格式化后的错误信息

        Examples:
            >>> OutputFormatter.format_error("除数不能为零")
            '错误: 除数不能为零'
        """
        return f"错误: {error_msg}"

    @staticmethod
    def format_help() -> str:
        """
        格式化帮助信息

        Returns:
            帮助信息字符串
        """
        return """
简单计算器 v1.0.0

用法:
  python calculator.py [选项] <运算符> <数字1> <数字2>

参数:
  运算符         支持的运算符: +, -, *, /
  数字1         第一个操作数
  数字2         第二个操作数

选项:
  -h, --help     显示此帮助信息
  -v, --version  显示版本信息
  -i, --interactive  进入交互模式
  -o, --output FORMAT  输出格式 (text/json)

示例:
  python calculator.py + 10 5
  python calculator.py --output json * 3 4
  python calculator.py --interactive

退出码:
  0 - 成功
  1 - 参数错误
  2 - 运算错误
  3 - 其他错误
        """.strip()
