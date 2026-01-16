# Office Agent Workspace

**版本**: 1.0.0
**更新**: 2026-01-16
**类型**: Python 办公自动化工具集

## 技能概述

Office Agent Workspace 是一个集成的 Python 办公自动化工具集，包含多个智能体和工具框架。

## 核心组件

### 1. 市场监管智能体 (market_supervision_agent)
- **位置**: `01_Active_Projects/market_supervision_agent/`
- **功能**: 个体工商户开业申请书自动填写
- **技术**: Flask + Jinja2 + OCR (百度/Paddle)
- **入口**: `ui/flask_app.py`

### 2. 记忆助手 (memory_agent)
- **位置**: `01_Active_Projects/memory_agent/`
- **功能**: 语义记忆存储和检索
- **技术**: Streamlit + ChromaDB + sentence-transformers
- **入口**: `ui/app.py`

### 3. 工作流引擎 (workflow_engine)
- **位置**: `00_Agent_Library/workflow_engine.py`
- **功能**: LangGraph 工作流编排
- **技术**: LangGraph + 状态管理
- **API**: WorkflowEngine 类

### 4. AgentTool 工具框架 (agent_toolkit)
- **位置**: `00_Agent_Library/agent_toolkit.py`
- **功能**: 智能体工具抽象层
- **技术**: Python + 装饰器模式
- **API**: AgentTool, tool装饰器

## 项目结构

```
Office_Agent_Workspace/
├── 00_Agent_Library/          # 核心框架库
├── 01_Active_Projects/        # 活跃项目
├── 02_Project_Archive/        # 归档项目
├── 04_Data_&_Resources/       # 数据和资源
├── 05_Outputs/                # 输出文件
├── 06_Learning_Journal/       # 学习日志
├── docs/                      # 详细文档
├── skills/                    # Claude Code 技能
└── CLAUDE.md                  # 项目配置
```

## 快速开始

### 启动市场监管智能体
```bash
python 01_Active_Projects/market_supervision_agent/ui/flask_app.py
# 访问 http://127.0.0.1:5000
```

### 启动记忆助手
```bash
streamlit run 01_Active_Projects/memory_agent/ui/app.py
# 访问 http://localhost:8501
```

### 使用工作流引擎
```python
from 00_Agent_Library.workflow_engine import WorkflowEngine

engine = WorkflowEngine()
result = engine.run_workflow("my_workflow", input_data)
```

## 技能用法

### 添加新智能体
1. 在 `01_Active_Projects/` 创建项目目录
2. 实现核心功能类
3. 创建 UI (Flask/Streamlit/CLI)
4. 更新 CLAUDE.md

### 使用技能系统
- 见 `skills/idea-to-product/` - 想法落地技能
- 见 `skills/super-butler/` - 超级管家技能

### 记忆系统
```python
from 00_Agent_Library.claude_memory import ClaudeMemory

memory = ClaudeMemory()
memory.remember("context", "用户偏好使用中文")
contexts = memory.recall("用户偏好")
```

## 常见任务

### 生成申请书
使用市场监管智能体的 Jinja2 模板引擎

### 语义搜索
使用记忆助手的 ChromaDB 向量搜索

### 工作流编排
使用 WorkflowEngine 的状态图功能

### 版本管理
运行 `python 00_Agent_Library/version_manager.py`

## 编码规范

- **Python版本**: 3.9+ (推荐 3.12)
- **编码**: UTF-8 with BOM
- **命名**: snake_case 文件, PascalCase 类
- **行长**: 100字符 (软限制120)
- **路径**: 使用 pathlib.Path

## Windows 兼容性

所有脚本包含终端编码修复：
```python
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
```

## 扩展阅读

- [完整系统指南](COMPLETE_SYSTEM_GUIDE.md)
- [架构设计](docs/ARCHITECTURE.md)
- [编码规范](docs/CODING_STANDARDS.md)
- [智能体开发](docs/guides/AGENT_DEVELOPMENT.md)

## 技能触发关键词

- "市场监管" → market_supervision_agent
- "记忆" → memory_agent
- "工作流" → workflow_engine
- "智能体" → AgentTool
- "想法" → idea-to-product 技能
- "管家" → super-butler 技能
