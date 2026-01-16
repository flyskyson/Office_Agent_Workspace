# 📝 编码规范

本文档定义了 Office Agent Workspace 项目的编码标准和最佳实践。

---

## 🎯 核心原则

1. **可读性优先**: 代码应该像文档一样易读
2. **一致性**: 全项目保持统一的风格
3. **简单性**: 避免过度设计和复杂化
4. **可维护性**: 便于后续修改和扩展
5. **Windows兼容性**: 确保在Windows环境下正常运行

---

## 🐍 Python规范

### 版本要求

- **最低版本**: Python 3.9
- **推荐版本**: Python 3.12
- **目标版本**: Python 3.9 - 3.12

### 文件编码

```python
# -*- coding: utf-8 -*-
"""
模块文档字符串
"""
```

**要求**:
- ✅ 使用 UTF-8 with BOM 编码（Windows兼容）
- ✅ 所有文件包含编码声明
- ✅ 模块级别文档字符串

### 命名约定

#### 文件命名

```python
# ✅ 正确
file_organizer.py
workflow_engine.py
market_supervision_agent.py

# ❌ 错误
FileOrganizer.py
file-organizer.py
fileOrganizer.py
```

**规则**: 使用 `snake_case`，全小写，单词间用下划线分隔

#### 类命名

```python
# ✅ 正确
class FileOrganizer:
    pass

class WorkflowEngine:
    pass

# ❌ 错误
class file_organizer:
    pass

class FileOrganizer:
    pass
```

**规则**: 使用 `PascalCase`，每个单词首字母大写

#### 函数命名

```python
# ✅ 正确
def execute_task():
    pass

def validate_input():
    pass

# ❌ 错误
def ExecuteTask():
    pass

def executeTask():
    pass
```

**规则**: 使用 `snake_case`，全小写，单词间用下划线分隔

#### 变量命名

```python
# ✅ 正确
user_name = "John"
max_retries = 3
is_valid = True

# ❌ 错误
userName = "John"
MAX_RETRIES = 3  # 除非是真正的常量
```

**规则**: 使用 `snake_case`，全小写，单词间用下划线分隔

#### 常量命名

```python
# ✅ 正确
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
API_KEY = "your_api_key"

# ❌ 错误
max_retries = 3
default_timeout = 30
```

**规则**: 使用 `UPPER_SNAKE_CASE`，全大写，单词间用下划线分隔

#### 私有成员命名

```python
# ✅ 正确
class MyClass:
    def __init__(self):
        self._private_var = 10

    def _private_method(self):
        pass

# ❌ 错误
class MyClass:
    def __init__(self):
        self.private_var = 10  # 应该有前缀
```

**规则**: 使用 `_leading_underscore` 表示私有成员

---

## 📐 代码格式化

### 缩进

```python
# ✅ 正确 - 4空格
def my_function():
    if condition:
        do_something()

# ❌ 错误 - 2空格
def my_function():
  if condition:
    do_something()

# ❌ 错误 - Tab
def my_function():
	if condition:
		do_something()
```

**规则**: 使用 **4个空格**缩进，不使用Tab

### 行长度

```python
# ✅ 正确 - 100字符以内
result = some_function_with_long_name(
    parameter1, parameter2, parameter3
)

# ✅ 可接受 - 软限制120字符
long_variable_name = some_function_with_very_long_name(parameter1, parameter2)

# ❌ 避免 - 超过120字符
result = some_function_with_long_name(parameter1, parameter2, parameter3, parameter4, parameter5)
```

**规则**:
- **硬限制**: 120字符
- **软限制**: 100字符
- **建议**: 80-90字符最佳

### 空行

```python
# ✅ 正确
def function_one():
    pass


def function_two():
    pass


class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass

# ❌ 错误 - 缺少空行
def function_one():
    pass
def function_two():
    pass
```

**规则**:
- 函数之间: **2个空行**
- 类之间: **2个空行**
- 方法之间: **1个空行**
- 逻辑块之间: **1个空行**

### 导入顺序

```python
# ✅ 正确
import sys
import os
from pathlib import Path

import flask
import streamlit
from playwright.sync_api import sync_playwright

from local_module import LocalClass
from local_package import local_function
```

**规则** (按顺序):
1. 标准库导入
2. 第三方库导入
3. 本地模块导入

**要求**:
- 每组之间用 **1个空行** 分隔
- 按字母顺序排列
- 每行最多导入 **1个模块**

---

## 💬 注释规范

### 文档字符串

```python
# ✅ 正确 - Google风格
def process_file(file_path: str, output_dir: str) -> bool:
    """处理文件并保存到输出目录。

    Args:
        file_path: 输入文件路径
        output_dir: 输出目录路径

    Returns:
        处理成功返回True，失败返回False

    Raises:
        FileNotFoundError: 如果输入文件不存在
        PermissionError: 如果没有写入权限
    """
    pass


# ✅ 正确 - 简短版本
def calculate_sum(a: int, b: int) -> int:
    """计算两个数的和。"""
    return a + b


# ❌ 错误 - 过于简单
def process_file(file_path, output_dir):
    # 处理文件
    pass
```

**要求**:
- 所有公共函数必须有文档字符串
- 使用 Google 风格或 NumPy 风格
- 简单函数可以一行描述

### 行内注释

```python
# ✅ 正确 - 解释为什么
# 使用Windows路径分隔符
file_path = os.path.join("dir", "file.txt")

# ✅ 正确 - 解释复杂逻辑
# 使用FNV哈希算法减少冲突概率
hash_value = fnv_hash(data)

# ❌ 错误 - 重复代码
# 设置变量x为10
x = 10

# ❌ 错误 - 过时的注释
# 这个函数已被弃用 - 请使用new_function()  ← 但代码仍在使用
def old_function():
    pass
```

**原则**:
- 解释 **为什么** 而不是 **是什么**
- 保持注释与代码同步
- 删除过时的注释

### TODO注释

```python
# ✅ 正确
# TODO(flyskyson): 添加输入验证
# FIXME: 这里的性能可以优化
# HACK: 临时解决方案，待重构
def my_function():
    pass
```

**格式**: `PREFIX(作者): 描述`

---

## 🛠️ Windows兼容性

### 路径处理

```python
# ✅ 正确 - 使用pathlib
from pathlib import Path

# 构建路径
file_path = Path("data") / "file.txt"
output_dir = Path(__file__).parent / "output"

# 路径操作
if file_path.exists():
    content = file_path.read_text(encoding="utf-8")


# ✅ 正确 - 使用os.path
import os

file_path = os.path.join("data", "file.txt")
output_dir = os.path.dirname(__file__)


# ❌ 错误 - 硬编码路径分隔符
file_path = "data/file.txt"  # Windows使用反斜杠
```

**原则**:
- 优先使用 `pathlib.Path`
- 避免硬编码路径分隔符
- 使用相对路径而非绝对路径

### 终端编码

```python
# ✅ 正确 - Windows编码修复
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# ✅ 正确 - 文件编码
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()


# ❌ 错误 - 不指定编码
with open('file.txt', 'r') as f:  # Windows可能使用GBK
    content = f.read()
```

### 进程和线程

```python
# ✅ 正确 - Windows兼容的多进程
if __name__ == '__main__':
    # 多进程代码
    pass


# ✅ 正确 - 使用multiprocessing
from multiprocessing import Pool

def process_task(item):
    return item * 2

if __name__ == '__main__':
    with Pool() as pool:
        results = pool.map(process_task, items)
```

---

## 🎯 类型提示

### 基本用法

```python
# ✅ 正确 - 使用类型提示
from typing import List, Dict, Optional, Union

def process_items(items: List[str]) -> Dict[str, int]:
    """处理项目列表。"""
    result = {}
    for item in items:
        result[item] = len(item)
    return result

def find_user(user_id: int) -> Optional[Dict]:
    """查找用户，找不到返回None。"""
    if user_id == 1:
        return {"name": "John"}
    return None

def parse_value(value: Union[str, int]) -> str:
    """解析值为字符串。"""
    return str(value)
```

### 复杂类型

```python
# ✅ 正确 - 使用Type别名
from typing import TypeAlias, Tuple

UserData: TypeAlias = Dict[str, Union[str, int, List[str]]]

def process_user(user: UserData) -> Tuple[bool, str]:
    """处理用户数据。"""
    return True, "success"


# ✅ 正确 - 使用泛型
from typing import TypeVar, Generic

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, value: T):
        self.value = value
```

---

## ⚡ 性能最佳实践

### 列表和生成器

```python
# ✅ 正确 - 使用生成器处理大数据
def process_large_file(file_path: str):
    with open(file_path) as f:
        for line in f:  # 逐行处理，不加载全部
            yield process_line(line)


# ✅ 正确 - 列表推导式
squares = [x**2 for x in range(1000)]


# ❌ 避免 - 不必要的列表创建
def get_all_lines(file_path: str) -> list:
    with open(file_path) as f:
        return [line for line in f]  # 加载全部到内存
```

### 字符串操作

```python
# ✅ 正确 - 使用join连接字符串
parts = ['Hello', 'World', '!']
result = ' '.join(parts)


# ❌ 避免 - 重复拼接
result = ''
for part in parts:
    result += part  # 每次创建新字符串
```

### 缓存和记忆化

```python
# ✅ 正确 - 使用缓存
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n: int) -> int:
    """计算密集型函数。"""
    return sum(range(n))
```

---

## 🔒 错误处理

### 异常捕获

```python
# ✅ 正确 - 具体异常
try:
    result = process_file(file_path)
except FileNotFoundError as e:
    logger.error(f"文件不存在: {e}")
except PermissionError as e:
    logger.error(f"权限不足: {e}")
except Exception as e:
    logger.error(f"未知错误: {e}")
    raise


# ✅ 正确 - 资源清理
try:
    f = open('file.txt', 'r')
    content = f.read()
finally:
    f.close()


# ✅ 最佳 - 使用with语句
with open('file.txt', 'r') as f:
    content = f.read()


# ❌ 避免 - 捕获所有异常
try:
    result = process_file(file_path)
except:
    pass  # 吞掉所有错误
```

### 自定义异常

```python
# ✅ 正确 - 自定义异常
class ProcessingError(Exception):
    """处理错误基类。"""
    pass


class FileValidationError(ProcessingError):
    """文件验证错误。"""
    pass


def validate_file(file_path: str) -> None:
    """验证文件。"""
    if not Path(file_path).exists():
        raise FileValidationError(f"文件不存在: {file_path}")
```

---

## 🧪 测试规范

### 单元测试

```python
# ✅ 正确 - 使用pytest
import pytest

def test_addition():
    """测试加法。"""
    assert add(2, 3) == 5


def test_file_not_found():
    """测试文件不存在的情况。"""
    with pytest.raises(FileNotFoundError):
        process_file("nonexistent.txt")


@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    """测试平方函数。"""
    assert square(input) == expected
```

### 测试文件结构

```
project/
├── module.py
└── tests/
    ├── __init__.py
    └── test_module.py
```

---

## 📋 代码审查清单

在提交代码前，请检查:

- [ ] 代码符合PEP 8规范
- [ ] 所有函数都有文档字符串
- [ ] 使用了类型提示
- [ ] 添加了必要的注释
- [ ] 处理了所有异常情况
- [ ] 使用了pathlib处理路径
- [ ] Windows兼容性已测试
- [ ] 添加了单元测试
- [ ] 测试全部通过
- [ ] 更新了相关文档

---

**参考文档**:
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Type Hints in Python](https://docs.python.org/3/library/typing.html)
