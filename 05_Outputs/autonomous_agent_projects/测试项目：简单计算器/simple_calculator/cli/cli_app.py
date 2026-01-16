"""
命令行应用类
实现用户交互的命令行界面
"""

import sys
from typing import Optional

from simple_calculator.core.calculator import Calculator
from simple_calculator.utils.formatter import OutputFormatter
from simple_calculator.utils.validator import InputValidator


class CalculatorCLI:
    """命令行应用类"""

    VERSION = "1.0.0"
    NAME = "简单计算器"

    def __init__(self):
        """初始化CLI应用"""
        self.calculator = Calculator()
        self.validator = InputValidator()
        self.formatter = OutputFormatter()

    def run(self, args: list) -> int:
        """
        运行CLI应用

        Args:
            args: 命令行参数列表（不包括程序名）

        Returns:
            退出码 (0=成功, 1=参数错误, 2=运算错误, 3=其他错误)
        """
        if not args:
            print(self.formatter.format_help())
            return 0

        # 解析选项参数
        i = 0
        output_format = 'text'
        interactive = False
        positional_args = []

        while i < len(args):
            arg = args[i]

            if arg in ['-h', '--help']:
                print(self.formatter.format_help())
                return 0

            elif arg in ['-v', '--version']:
                print(f"{self.NAME} v{self.VERSION}")
                return 0

            elif arg in ['-i', '--interactive']:
                interactive = True
                i += 1

            elif arg in ['-o', '--output']:
                if i + 1 >= len(args):
                    print(self.formatter.format_error("--output 需要指定格式 (text/json)"))
                    return 1
                output_format = args[i + 1]
                if output_format not in ['text', 'json']:
                    print(self.formatter.format_error(f"不支持的输出格式 '{output_format}'，支持: text, json"))
                    return 1
                i += 2

            # 检查是否为选项（排除负数）
            elif arg.startswith('-') and not self._is_number(arg):
                print(self.formatter.format_error(f"未知选项 '{arg}'"))
                print("使用 --help 查看帮助信息")
                return 1

            else:
                # 收集位置参数（运算符和数字，包括负数）
                positional_args.append(arg)
                i += 1

        # 处理位置参数
        if interactive and positional_args:
            print(self.formatter.format_error("交互模式下不需要提供位置参数"))
            return 1
        elif interactive:
            return self.run_interactive()
        elif positional_args:
            return self.calculate_single(positional_args, output_format)
        else:
            print(self.formatter.format_help())
            return 0

    @staticmethod
    def _is_number(value: str) -> bool:
        """
        检查字符串是否为数字（包括负数和小数）

        Args:
            value: 待检查的字符串

        Returns:
            True 如果是数字，False 否则
        """
        try:
            float(value)
            return True
        except ValueError:
            return False

    def calculate_single(self, args: list, output_format: str = 'text') -> int:
        """
        执行单次计算

        Args:
            args: [operator, num1, num2]
            output_format: 输出格式

        Returns:
            退出码
        """
        try:
            # 验证参数
            operator, num1, num2 = self.validator.validate_arguments(args)

            # 执行计算
            result = self.calculator.calculate(operator, num1, num2)

            # 格式化输出
            output = self.formatter.format_result(
                result, operator, num1, num2, output_format
            )
            print(output)

            return 0

        except ValueError as e:
            print(self.formatter.format_error(str(e)))
            # 判断是参数错误还是运算错误
            error_msg = str(e)
            if "除数不能为零" in error_msg:
                return 2
            elif "不支持的运算符" in error_msg:
                return 1
            else:
                return 1
        except Exception as e:
            print(self.formatter.format_error(f"计算错误: {str(e)}"))
            return 3

    def run_interactive(self) -> int:
        """
        运行交互模式

        Returns:
            退出码
        """
        print(f"\n{self.NAME} v{self.VERSION} - 交互模式")
        print("输入 'quit' 或 'exit' 退出\n")

        while True:
            try:
                # 读取用户输入
                user_input = input("请输入运算表达式 (如: + 10 5): ").strip()

                # 检查退出命令
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("再见!")
                    return 0

                # 跳过空输入
                if not user_input:
                    continue

                # 解析输入
                parts = user_input.split()
                if len(parts) != 3:
                    print(self.formatter.format_error(
                        "输入格式错误，请使用: 运算符 数字1 数字2"
                    ))
                    continue

                # 执行计算
                exit_code = self.calculate_single(parts, 'text')

                # 如果是退出码3（严重错误），退出程序
                if exit_code == 3:
                    return 3

            except KeyboardInterrupt:
                print("\n\n检测到中断信号，退出程序")
                return 0
            except EOFError:
                print("\n\n再见!")
                return 0
            except Exception as e:
                print(self.formatter.format_error(f"未知错误: {str(e)}"))
                continue
