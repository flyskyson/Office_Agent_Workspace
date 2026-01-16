# 简单计算器 - 代码结构设计

## 1. 项目目录结构

```
simple_calculator/
├── calculator.py              # 🎯 主入口文件（CLI应用）
├── core/                      # 🔧 核心功能模块
│   ├── __init__.py
│   ├── calculator.py          #    计算器核心类
│   └── operations.py          #    运算实现
├── utils/                     # 🛠️ 工具模块
│   ├── __init__.py
│   ├── validator.py           #    输入验证器
│   └── formatter.py           #    输出格式化器
├── cli/                       # 💻 命令行界面
│   ├── __init__.py
│   └── app.py                 #    CLI应用类
├── tests/                     # 🧪 测试模块
│   ├── __init__.py
│   ├── test_calculator.py     #    核心功能测试
│   ├── test_validator.py      #    验证器测试
│   └── test_cli.py            #    CLI测试
├── config/                    # ⚙️ 配置文件
│   └── default_config.json    #    默认配置
├── docs/                      # 📚 文档
│   ├── requirements.md        #    需求文档
│   ├── interface_design.md    #    接口设计
│   └── code_structure.md      #    代码结构（本文件）
├── .env.example               #    环境变量示例
├── requirements.txt           #    依赖列表
├── README.md                  #    项目说明
└── setup.py                   #    安装脚本
```

## 2. 模块设计

### 2.1 核心模块 (core/)

#### calculator.py - 计算器核心类
```python
"""
计算器核心类
提供基本的四则运算功能
"""

class Calculator:
    """简单计算器核心类"""
    
    SUPPORTED_OPERATORS = ['+', '-', '*', '/']
    
    def __init__(self):
        """初始化计算器"""
        pass
    
    def add(self, a: float, b: float) -> float:
        """
        加法运算
        
        Args:
            a: 第一个操作数
            b: 第二个操作数
            
        Returns:
            两数之和
        """
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """
        减法运算
        
        Args:
            a: 被减数
            b: 减数
            
        Returns:
            两数之差
        """
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """
        乘法运算
        
        Args:
            a: 第一个因数
            b: 第二个因数
            
        Returns:
            两数之积
        """
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """
        除法运算
        
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
        return a / b
    
    def calculate(self, operator: str, a: float, b: float) -> float:
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
            raise ValueError(f"不支持的运算符: {operator}")
```

#### operations.py - 运算实现（预留扩展）
```python
"""
运算实现模块
预留用于添加更多运算类型
"""

class Operation:
    """运算基类"""
    
    def execute(self, a: float, b: float) -> float:
        """执行运算"""
        raise NotImplementedError


class AddOperation(Operation):
    """加法运算"""
    
    def execute(self, a: float, b: float) -> float:
        return a + b


class SubtractOperation(Operation):
    """减法运算"""
    
    def execute(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation(Operation):
    """乘法运算"""
    
    def execute(self, a: float, b: float) -> float:
        return a * b


class DivideOperation(Operation):
    """除法运算"""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b
```

### 2.2 工具模块 (utils/)

#### validator.py - 输入验证器
```python
"""
输入验证器
负责验证用户输入的合法性
"""

from typing import Tuple


class InputValidator:
    """输入验证器"""
    
    SUPPORTED_OPERATORS = ['+', '-', '*', '/']
    
    @staticmethod
    def validate_operator(operator: str) -> bool:
        """
        验证运算符是否合法
        
        Args:
            operator: 待验证的运算符
            
        Returns:
            True 如果合法，False 否则
        """
        return operator in InputValidator.SUPPORTED_OPERATORS
    
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
        """
        if len(args) != 3:
            raise ValueError(
                f"需要提供3个参数（运算符 数字1 数字2），实际提供 {len(args)} 个"
            )
        
        operator, num1_str, num2_str = args
        
        if not InputValidator.validate_operator(operator):
            raise ValueError(
                f"不支持的运算符 '{operator}'。"
                f"支持的运算符: {', '.join(InputValidator.SUPPORTED_OPERATORS)}"
            )
        
        try:
            num1 = InputValidator.validate_number(num1_str)
            num2 = InputValidator.validate_number(num2_str)
        except ValueError as e:
            raise ValueError(f"参数错误: {str(e)}")
        
        return operator, num1, num2
```

#### formatter.py - 输出格式化器
```python
"""
输出格式化器
负责格式化输出结果和错误信息
"""

import json
from typing import Any


class OutputFormatter:
    """输出格式化器"""
    
    @staticmethod
    def format_result(
        result: float,
        operator: str = None,
        operand1: float = None,
        operand2: float = None,
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
        """
        if format_type == 'json':
            data = {
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
```

### 2.3 CLI模块 (cli/)

#### app.py - CLI应用类
```python
"""
CLI应用类
负责处理命令行界面和用户交互
"""

import sys
from typing import List

from core.calculator import Calculator
from utils.validator import InputValidator
from utils.formatter import OutputFormatter


class CalculatorCLI:
    """命令行应用类"""
    
    def __init__(self):
        """初始化CLI应用"""
        self.calculator = Calculator()
        self.validator = InputValidator()
        self.formatter = OutputFormatter()
    
    def run(self, args: List[str]) -> int:
        """
        运行CLI应用
        
        Args:
            args: 命令行参数列表
            
        Returns:
            退出码
        """
        try:
            # 处理选项参数
            if self._handle_options(args):
                return 0
            
            # 验证参数
            operator, num1, num2 = self.validator.validate_arguments(args)
            
            # 执行计算
            result = self.calculator.calculate(operator, num1, num2)
            
            # 输出结果
            output = self.formatter.format_result(result, operator, num1, num2)
            print(output)
            
            return 0
            
        except ValueError as e:
            print(self.formatter.format_error(str(e)))
            return 1
        except Exception as e:
            print(self.formatter.format_error(f"发生错误: {str(e)}"))
            return 3
    
    def run_interactive(self) -> int:
        """
        运行交互模式
        
        Returns:
            退出码
        """
        print("简单计算器 v1.0.0 - 交互模式")
        print("输入 'quit' 或 'exit' 退出")
        print()
        
        while True:
            try:
                # 读取用户输入
                user_input = input("请输入运算表达式 (如: + 10 5): ").strip()
                
                # 检查退出条件
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("再见!")
                    return 0
                
                # 解析输入
                args = user_input.split()
                if len(args) != 3:
                    print("错误: 请输入3个参数（运算符 数字1 数字2）")
                    continue
                
                # 验证和计算
                operator, num1, num2 = self.validator.validate_arguments(args)
                result = self.calculator.calculate(operator, num1, num2)
                
                # 输出结果
                output = self.formatter.format_result(result)
                print(output)
                print()
                
            except ValueError as e:
                print(self.formatter.format_error(str(e)))
                print()
            except KeyboardInterrupt:
                print("\n\n再见!")
                return 0
            except Exception as e:
                print(self.formatter.format_error(f"发生错误: {str(e)}"))
                print()
    
    def _handle_options(self, args: List[str]) -> bool:
        """
        处理选项参数
        
        Args:
            args: 参数列表
            
        Returns:
            True 如果是选项参数（已处理），False 否则
        """
        if not args:
            return False
        
        if args[0] in ['-h', '--help']:
            print(self.formatter.format_help())
            return True
        
        if args[0] in ['-v', '--version']:
            print("简单计算器 v1.0.0")
            return True
        
        return False


def main():
    """主入口函数"""
    cli = CalculatorCLI()
    args = sys.argv[1:]
    
    # 检查交互模式
    if '-i' in args or '--interactive' in args:
        # 移除交互模式标志
        args = [a for a in args if a not in ['-i', '--interactive']]
        if not args:  # 纯交互模式
            sys.exit(cli.run_interactive())
    
    # 运行单次计算
    sys.exit(cli.run(args))


if __name__ == '__main__':
    main()
```

### 2.4 主入口文件 (calculator.py)

```python
#!/usr/bin/env python3
"""
简单计算器 - 主入口文件
"""

from cli.app import main

if __name__ == '__main__':
    main()
```

## 3. 模块依赖关系

```
calculator.py (主入口)
    ↓
cli/app.py (CLI应用)
    ↓
├── core/calculator.py (核心计算)
│   └── core/operations.py (运算实现)
├── utils/validator.py (输入验证)
└── utils/formatter.py (输出格式化)
```

## 4. 测试模块设计

### 4.1 test_calculator.py
```python
"""
核心功能测试
"""

import pytest
from core.calculator import Calculator


def test_calculator_add():
    """测试加法"""
    calc = Calculator()
    assert calc.add(10, 5) == 15
    assert calc.add(-10, 5) == -5
    assert calc.add(0, 0) == 0


def test_calculator_subtract():
    """测试减法"""
    calc = Calculator()
    assert calc.subtract(10, 5) == 5
    assert calc.subtract(5, 10) == -5


def test_calculator_multiply():
    """测试乘法"""
    calc = Calculator()
    assert calc.multiply(10, 5) == 50
    assert calc.multiply(-10, 5) == -50


def test_calculator_divide():
    """测试除法"""
    calc = Calculator()
    assert calc.divide(10, 5) == 2.0
    assert calc.divide(10, 2.5) == 4.0


def test_calculator_divide_by_zero():
    """测试除以零"""
    calc = Calculator()
    with pytest.raises(ValueError, match="除数不能为零"):
        calc.divide(10, 0)
```

### 4.2 test_validator.py
```python
"""
验证器测试
"""

import pytest
from utils.validator import InputValidator


def test_validate_operator():
    """测试运算符验证"""
    assert InputValidator.validate_operator('+') == True
    assert InputValidator.validate_operator('-') == True
    assert InputValidator.validate_operator('*') == True
    assert InputValidator.validate_operator('/') == True
    assert InputValidator.validate_operator('%') == False


def test_validate_number():
    """测试数字验证"""
    assert InputValidator.validate_number('10') == 10.0
    assert InputValidator.validate_number('3.14') == 3.14
    assert InputValidator.validate_number('-5') == -5.0
    
    with pytest.raises(ValueError):
        InputValidator.validate_number('abc')


def test_validate_arguments():
    """测试参数验证"""
    # 正常参数
    op, n1, n2 = InputValidator.validate_arguments(['+', '10', '5'])
    assert op == '+'
    assert n1 == 10.0
    assert n2 == 5.0
    
    # 参数不足
    with pytest.raises(ValueError):
        InputValidator.validate_arguments(['+', '10'])
    
    # 非法运算符
    with pytest.raises(ValueError):
        InputValidator.validate_arguments(['%', '10', '5'])
```

## 5. 扩展性设计

### 5.1 运算扩展点
- 使用 `Operation` 基类，方便添加新运算
- 运算符映射表，易于注册新运算符

### 5.2 输入扩展点
- 支持更多输入格式（如表达式字符串）
- 支持配置文件自定义

### 5.3 输出扩展点
- 支持更多输出格式（XML、CSV等）
- 支持自定义输出模板

### 5.4 功能扩展点
- 历史记录功能
- 变量存储功能
- 链式计算功能

## 6. 代码规范

### 6.1 命名规范
- 类名: `PascalCase` (如 `Calculator`)
- 函数名: `snake_case` (如 `calculate`)
- 常量: `UPPER_SNAKE_CASE` (如 `SUPPORTED_OPERATORS`)
- 私有方法: `_leading_underscore` (如 `_handle_options`)

### 6.2 文档规范
- 所有模块、类、函数都有文档字符串
- 使用 Google 风格的文档字符串
- 复杂逻辑添加行内注释

### 6.3 类型注解
- 所有函数都有类型注解
- 使用 `typing` 模块的类型

### 6.4 错误处理
- 使用明确的异常类型
- 错误信息清晰具体
- 适当的错误日志记录

## 7. 性能优化

### 7.1 计算优化
- 使用基本的算术运算，无需优化
- 大数运算可使用 `decimal` 模块

### 7.2 内存优化
- 避免不必要的对象创建
- 及时释放资源

### 7.3 响应优化
- 输入验证快速失败
- 错误处理简洁高效

---

**文档版本**: 1.0
**最后更新**: 2026-01-15
**状态**: ✅ 已完成
