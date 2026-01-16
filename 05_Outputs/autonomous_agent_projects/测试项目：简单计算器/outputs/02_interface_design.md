# 简单计算器 - 接口设计文档

## 1. 命令行接口设计

### 1.1 基本语法

```bash
python calculator.py [选项] <运算符> <数字1> <数字2>
```

### 1.2 参数说明

#### 位置参数
| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| 运算符 | string | ✅ | 支持的运算符：+ - * / | `+`, `-`, `*`, `/` |
| 数字1 | number | ✅ | 第一个操作数 | `10`, `3.14`, `-5` |
| 数字2 | number | ✅ | 第二个操作数 | `5`, `2.5`, `-3` |

#### 可选参数
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| --help | -h | 显示帮助信息 | - |
| --interactive | -i | 进入交互模式 | False |
| --version | -v | 显示版本信息 | - |
| --output | -o | 指定输出格式（text/json） | text |

### 1.3 使用示例

#### 基本运算
```bash
# 加法
python calculator.py + 10 5
# 输出: 结果: 15

# 减法
python calculator.py - 10 5
# 输出: 结果: 5

# 乘法
python calculator.py * 10 5
# 输出: 结果: 50

# 除法
python calculator.py / 10 5
# 输出: 结果: 2.0

# 浮点数运算
python calculator.py + 10.5 5.3
# 输出: 结果: 15.8
```

#### JSON 输出格式
```bash
python calculator.py --output json + 10 5
# 输出: {"operator": "+", "operand1": 10, "operand2": 5, "result": 15}
```

#### 帮助信息
```bash
python calculator.py --help
# 输出完整的使用说明
```

#### 版本信息
```bash
python calculator.py --version
# 输出: 简单计算器 v1.0.0
```

### 1.4 交互式模式

```bash
# 进入交互模式
python calculator.py --interactive
# 或
python calculator.py -i

# 交互过程示例:
> 简单计算器 v1.0.0 - 交互模式
> 输入 'quit' 或 'exit' 退出
>
> 请输入运算表达式 (如: + 10 5): + 10 5
> 结果: 15
>
> 请输入运算表达式 (如: + 10 5): * 3 4
> 结果: 12
>
> 请输入运算表达式 (如: + 10 5): quit
> 再见!
```

### 1.5 错误处理

#### 参数错误
```bash
# 参数不足
python calculator.py + 10
# 输出: 错误: 需要提供3个参数（运算符 数字1 数字2）
#        用法: python calculator.py <运算符> <数字1> <数字2>

# 非法运算符
python calculator.py % 10 5
# 输出: 错误: 不支持的运算符 '%'
#        支持的运算符: +, -, *, /

# 非数字输入
python calculator.py + 10 abc
# 输出: 错误: 'abc' 不是有效的数字

# 除数为零
python calculator.py / 10 0
# 输出: 错误: 除数不能为零
```

### 1.6 退出码

| 退出码 | 说明 |
|--------|------|
| 0 | 成功执行 |
| 1 | 参数错误 |
| 2 | 运算错误（如除零） |
| 3 | 其他错误 |

## 2. Python API 接口设计

### 2.1 核心计算类

```python
class Calculator:
    """简单计算器核心类"""
    
    def add(self, a: float, b: float) -> float:
        """加法运算"""
        pass
    
    def subtract(self, a: float, b: float) -> float:
        """减法运算"""
        pass
    
    def multiply(self, a: float, b: float) -> float:
        """乘法运算"""
        pass
    
    def divide(self, a: float, b: float) -> float:
        """除法运算
        
        Raises:
            ValueError: 当除数为零时
        """
        pass
    
    def calculate(self, operator: str, a: float, b: float) -> float:
        """通用计算接口
        
        Args:
            operator: 运算符 (+, -, *, /)
            a: 第一个操作数
            b: 第二个操作数
            
        Returns:
            计算结果
            
        Raises:
            ValueError: 当运算符不支持或除数为零时
        """
        pass
```

### 2.2 输入验证器

```python
class InputValidator:
    """输入验证器"""
    
    @staticmethod
    def validate_operator(operator: str) -> bool:
        """验证运算符是否合法"""
        pass
    
    @staticmethod
    def validate_number(value: str) -> float:
        """验证并转换数字
        
        Raises:
            ValueError: 当不是有效数字时
        """
        pass
    
    @staticmethod
    def validate_arguments(args: list) -> tuple:
        """验证命令行参数
        
        Returns:
            (operator, num1, num2)
            
        Raises:
            ValueError: 当参数不合法时
        """
        pass
```

### 2.3 输出格式化器

```python
class OutputFormatter:
    """输出格式化器"""
    
    @staticmethod
    def format_result(result: float, format_type: str = 'text') -> str:
        """格式化输出结果
        
        Args:
            result: 计算结果
            format_type: 输出格式 (text/json)
            
        Returns:
            格式化后的字符串
        """
        pass
    
    @staticmethod
    def format_error(error_msg: str) -> str:
        """格式化错误信息"""
        pass
```

### 2.4 CLI 应用类

```python
class CalculatorCLI:
    """命令行应用类"""
    
    def __init__(self):
        self.calculator = Calculator()
        self.validator = InputValidator()
        self.formatter = OutputFormatter()
    
    def run(self, args: list):
        """运行CLI应用"""
        pass
    
    def run_interactive(self):
        """运行交互模式"""
        pass
```

## 3. 数据流设计

### 3.1 单次计算流程

```
用户输入 → 参数验证 → 运算符判断 → 执行计算 → 结果输出
   ↓           ↓           ↓           ↓           ↓
 args   InputValidator  Calculator   Calculator  OutputFormatter
```

### 3.2 交互模式流程

```
启动 → 显示欢迎信息 → 循环：
                          ├─ 读取输入
                          ├─ 验证输入
                          ├─ 执行计算
                          ├─ 显示结果
                          └─ 检查退出条件
                       ↓
                    退出程序
```

## 4. 配置文件设计（预留）

### 4.1 配置文件路径
- 位置: `~/.calculator/config.json`
- 默认配置: 自动生成

### 4.2 配置项
```json
{
  "default_format": "text",
  "precision": 2,
  "interactive_prompt": "> ",
  "history_file": "~/.calculator/history.json",
  "history_size": 100
}
```

## 5. 测试接口

### 5.1 单元测试接口
```python
# 测试计算功能
def test_calculator():
    calc = Calculator()
    assert calc.add(10, 5) == 15
    assert calc.subtract(10, 5) == 5
    assert calc.multiply(10, 5) == 50
    assert calc.divide(10, 5) == 2.0

# 测试验证器
def test_validator():
    validator = InputValidator()
    assert validator.validate_operator('+') == True
    assert validator.validate_number('10') == 10.0
```

### 5.2 集成测试接口
```bash
# 命令行测试
python calculator.py + 10 5
echo $?  # 检查退出码
```

---

**文档版本**: 1.0
**最后更新**: 2026-01-15
**状态**: ✅ 已完成
