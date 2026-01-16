# 🧪 Office Agent Workspace - 测试与开发指南

**版本**: 2.0.0
**更新日期**: 2026-01-16

---

## 📋 目录

1. [快速开始](#快速开始)
2. [依赖管理](#依赖管理)
3. [测试框架](#测试框架)
4. [错误处理](#错误处理)
5. [开发工作流](#开发工作流)
6. [CI/CD](#cicd)

---

## 🚀 快速开始

### 安装 Poetry

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# 验证安装
poetry --version
```

### 安装依赖

```bash
# 安装所有依赖（包括开发依赖）
poetry install

# 只安装核心依赖
poetry install --no-dev

# 激活虚拟环境
poetry shell
```

### 运行测试

```bash
# 运行所有测试
poetry run pytest

# 运行单元测试
poetry run pytest tests/unit/

# 运行测试并生成覆盖率报告
poetry run pytest --cov=00_Agent_Library --cov-report=html

# 查看覆盖率报告
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## 📦 依赖管理

### Poetry 依赖组

**核心依赖** (`dependencies`):
- Web框架: Streamlit, Flask
- 浏览器自动化: Playwright
- AI/ML: ChromaDB, sentence-transformers
- LangGraph: langgraph, langchain

**开发依赖** (`dev.dependencies`):
- **测试框架**: pytest, pytest-cov, pytest-mock
- **代码质量**: black, isort, flake8, mypy
- **文档**: sphinx, sphinx-rtd-theme
- **安全**: pip-audit, bandit
- **性能**: py-spy, memory-profiler

### 添加新依赖

```bash
# 添加核心依赖
poetry add package-name

# 添加开发依赖
poetry add --group dev package-name

# 更新依赖
poetry update

# 导出 requirements.txt
poetry export -f requirements.txt --output requirements.txt
```

### 依赖安全检查

```bash
# 安全审计
poetry run pip-audit

# 安全扫描（Bandit）
poetry run bandit -r 00_Agent_Library/
```

---

## 🧪 测试框架

### 测试结构

```
tests/
├── __init__.py           # 测试包初始化
├── conftest.py           # pytest 配置和共享夹具
├── unit/                 # 单元测试
│   ├── test_config_center.py
│   ├── test_agent_supervisor.py
│   └── ...
├── integration/          # 集成测试
│   ├── test_mcp_integration.py
│   └── ...
├── e2e/                  # 端到端测试
│   └── test_full_workflow.py
├── fixtures/             # 测试数据
│   ├── configs/
│   └── data/
└── mocks/                # Mock 对象
    └── mock_agents.py
```

### 测试标记

```bash
# 只运行单元测试
pytest -m unit

# 排除慢速测试
pytest -m "not slow"

# 运行需要网络的测试
pytest -m requires_network --run-network
```

### 编写测试

#### 单元测试示例

```python
import pytest
from 00_Agent_Library.config_center import ConfigCenter

class TestConfigCenter:
    """ConfigCenter 测试"""

    @pytest.mark.unit
    def test_init(self):
        """测试初始化"""
        config = ConfigCenter()
        assert config is not None

    @pytest.mark.unit
    def test_get_config(self, sample_config):
        """测试读取配置"""
        config = ConfigCenter()
        value = config.get("database.default_type")
        assert value == "sqlite"
```

#### 参数化测试

```python
@pytest.mark.parametrize("input,expected", [
    ("test1", "result1"),
    ("test2", "result2"),
    ("test3", "result3"),
])
def test_multiple_cases(input, expected):
    """参数化测试"""
    result = process(input)
    assert result == expected
```

#### 使用夹具

```python
def test_with_fixture(temp_dir, sample_config):
    """使用测试夹具"""
    # temp_dir 和 sample_config 由 conftest.py 提供
    config_path = temp_dir / "config.yaml"
    assert config_path.parent == temp_dir
```

### 测试最佳实践

1. **命名约定**:
   - 测试文件: `test_*.py` 或 `*_test.py`
   - 测试类: `Test*`
   - 测试函数: `test_*`

2. **AAA 模式** (Arrange-Act-Assert):
```python
def test_something():
    # Arrange (准备)
    config = ConfigCenter()
    config.set("test", "value")

    # Act (执行)
    result = config.get("test")

    # Assert (断言)
    assert result == "value"
```

3. **测试独立性**:
   - 每个测试应该独立运行
   - 使用夹具创建测试数据
   - 清理副作用

---

## ⚠️ 错误处理

### 统一错误类

```python
from 00_Agent_Library.exceptions import (
    WorkspaceError,
    ConfigError,
    DatabaseError,
    AgentError,
    ErrorHandler
)

# 抛出标准错误
def my_function():
    if not config:
        raise ConfigError(
            "配置文件未找到",
            code=ErrorCode.CONFIG_NOT_FOUND,
            details={"expected_path": "/path/to/config"}
        )
```

### 错误处理装饰器

```python
from 00_Agent_Library.exceptions import handle_errors

@handle_errors(default_return={"success": False})
def risky_function():
    # 可能抛出异常的代码
    pass
```

### 错误上下文管理器

```python
from 00_Agent_Library.exceptions import ErrorContext

with ErrorContext(error_callback=lambda e: print(f"错误: {e}")):
    # 可能抛出异常的代码
    risky_operation()
```

### 标准错误响应

```python
from 00_Agent_Library.exceptions import ErrorHandler

try:
    result = risky_operation()
except Exception as e:
    error_response = ErrorHandler.handle_error(e, include_traceback=True)
    # error_response 格式:
    # {
    #     "success": False,
    #     "error": "错误消息",
    #     "code": 1001,
    #     "code_name": "NOT_IMPLEMENTED",
    #     "details": {...},
    #     "timestamp": "2026-01-16T10:00:00",
    #     "traceback": "..."
    # }
```

---

## 🔧 开发工作流

### 代码格式化

```bash
# 使用 Black 格式化代码
poetry run black 00_Agent_Library/ tests/

# 使用 isort 排序导入
poetry run isort 00_Agent_Library/ tests/

# 同时运行两者
poetry run black 00_Agent_Library/ tests/ && poetry run isort 00_Agent_Library/ tests/
```

### 代码检查

```bash
# 使用 flake8 检查代码风格
poetry run flake8 00_Agent_Library/

# 使用 mypy 进行类型检查
poetry run mypy 00_Agent_Library/

# 生成类型存根
poetry run mypy --stub 00_Agent_Library/
```

### 提交前检查

```bash
# 完整检查流程
poetry run black 00_Agent_Library/ tests/
poetry run isort 00_Agent_Library/ tests/
poetry run flake8 00_Agent_Library/
poetry run mypy 00_Agent_Library/
poetry run pytest
poetry run pytest --cov=00_Agent_Library
```

### 创建预提交钩子

创建 `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# 提交前自动运行检查

echo "运行代码格式化..."
poetry run black 00_Agent_Library/ tests/
poetry run isort 00_Agent_Library/ tests/

echo "运行代码检查..."
poetry run flake8 00_Agent_Library/
poetry run mypy 00_Agent_Library/

echo "运行测试..."
poetry run pytest

if [ $? -ne 0 ]; then
    echo "测试失败，提交被拒绝"
    exit 1
fi
```

---

## 🚀 CI/CD

### GitHub Actions 示例

创建 `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ master, main ]
  pull_request:
    branches: [ master, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Install dependencies
      run: poetry install --with dev

    - name: Run linters
      run: |
        poetry run black --check 00_Agent_Library/ tests/
        poetry run isort --check 00_Agent_Library/ tests/
        poetry run flake8 00_Agent_Library/

    - name: Run tests
      run: poetry run pytest --cov=00_Agent_Library

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 📊 性能分析

### CPU 性能分析

```bash
# 使用 py-spy 分析 CPU 性能
poetry run py-spy record --output profile.svg -- python your_script.py

# 查看结果
start profile.svg  # Windows
```

### 内存分析

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    # 你的代码
    pass

if __name__ == "__main__":
    memory_intensive_function()
```

```bash
# 运行内存分析
poetry run python -m memory_profiler your_script.py
```

---

## 📚 相关文档

- [编码规范](CODING_STANDARDS.md)
- [架构设计](ARCHITECTURE.md)
- [Agent开发指南](guides/AGENT_DEVELOPMENT.md)
- [故障排查](TROUBLESHOOTING.md)

---

**文档版本**: 1.0.0
**最后更新**: 2026-01-16
