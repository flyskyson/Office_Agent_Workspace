# 简单计算器 - 快速使用指南

## 基本用法

### 单次计算
```bash
# 使用别名（推荐）
python main.py add 10 5          # 加法: 15
python main.py subtract 20 8     # 减法: 12
python main.py multiply 3 4      # 乘法: 12
python main.py divide 15 3       # 除法: 5

# 使用符号
python main.py + 10 5            # 加法
python main.py - 10 5            # 减法
python main.py * 10 5            # 乘法
python main.py / 10 5            # 除法
```

### JSON输出
```bash
python main.py --output json add 10 5
# 输出: {"result": 15.0, "operator": "+", "operand1": 10.0, "operand2": 5.0}
```

### 交互模式
```bash
python main.py --interactive
# 或
python main.py -i

# 交互中输入:
add 10 5
subtract 20 8
quit
```

### 帮助和版本
```bash
python main.py --help            # 查看帮助
python main.py --version         # 查看版本
python main.py -v                # 简短版本信息
```

## 支持的运算符

| 符号 | 别名 | 说明 |
|------|------|------|
| + | add, plus | 加法 |
| - | subtract, minus | 减法 |
| * | multiply, times | 乘法 |
| / | divide, div | 除法 |

## 退出码

| 代码 | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 参数错误 |
| 2 | 运算错误（如除零） |
| 3 | 其他错误 |

## 示例

### 基本运算
```bash
# 整数运算
python main.py add 10 5          # 15

# 小数运算
python main.py add 10.5 5.3      # 15.8

# 负数运算
python main.py add -10 5         # -5
python main.py multiply -5 -3    # 15
```

### 错误处理
```bash
# 参数不足
python main.py add 10
# 错误: 需要提供3个参数（运算符 数字1 数字2），实际提供 2 个

# 非法运算符
python main.py modulo 10 5
# 错误: 不支持的运算符 'modulo'。支持的运算符: +, -, *, /

# 除数为零
python main.py divide 10 0
# 错误: 除数不能为零
```

## Windows批处理

### 使用bat脚本
```batch
REM 双击运行或命令行执行
calculator.bat add 10 5
```

## Python API

```python
from simple_calculator.cli.cli_app import CalculatorCLI

# 创建CLI应用
cli = CalculatorCLI()

# 运行单次计算
exit_code = cli.run(['add', '10', '5'])

# 运行交互模式
exit_code = cli.run_interactive()
```

## 测试

```bash
# 测试交互模式
python test_interactive_mode.py

# 运行测试脚本
test_interactive.bat
```

## 故障排除

### Windows编码问题
如果中文显示乱码，确保在脚本开头添加：
```python
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
```

### 符号运算符问题
在Windows Git Bash中，建议使用别名运算符：
```bash
# 推荐
python main.py add 10 5

# 而不是
python main.py + 10 5
```

## 更多信息

- 详细文档: `docs/`
- 接口设计: `outputs/02_interface_design.md`
- 实现报告: `outputs/03_cli_implementation.md`
