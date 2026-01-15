# Office Agent Workspace - 项目配置

**项目类型**: Python 办公自动化工具集
**主要框架**: Streamlit, Flask, Playwright, AutoGen AgentTool
**Python版本**: 3.9+ (推荐 3.12)
**更新日期**: 2026-01-14

---

## 🎯 30秒快速导航

| 我想... | 查看文档 |
|---------|---------|
| 🚀 **快速上手** | [GETTING_STARTED.md](docs/GETTING_STARTED.md) |
| 🏗️ **了解架构** | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 📝 **查看编码规范** | [CODING_STANDARDS.md](docs/CODING_STANDARDS.md) |
| 🔧 **开发新功能** | [guides/AGENT_DEVELOPMENT.md](docs/guides/AGENT_DEVELOPMENT.md) |
| 🤖 **使用技能系统** | [guides/SKILLS_SYSTEM.md](docs/guides/SKILLS_SYSTEM.md) |
| 💡 **想法落地工作流** | [guides/IDEA_WORKFLOW.md](docs/guides/IDEA_WORKFLOW.md) |
| 🐛 **排查问题** | [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) |

---

## 📂 核心目录结构

```
Office_Agent_Workspace/
├── office_agent_studio.py          # 🎯 统一启动器 (CLI菜单)
├── CLAUDE.md                        # 📖 本文件 - 项目核心配置
├── COMPLETE_SYSTEM_GUIDE.md         # 📚 完整系统指南
├── PROJECT_ROADMAP.md               # 🗺️ 项目路线图
│
├── docs/                            # 📚 详细文档目录 ⭐ NEW
│   ├── GETTING_STARTED.md           #    入门指南
│   ├── ARCHITECTURE.md              #    架构设计
│   ├── CODING_STANDARDS.md          #    编码规范
│   ├── TROUBLESHOOTING.md           #    问题排查
│   └── guides/                      #    专题指南
│       ├── IDEA_WORKFLOW.md         #       想法落地详细指南
│       ├── SKILLS_SYSTEM.md         #       技能系统说明
│       ├── VERSION_MANAGEMENT.md    #       版本管理
│       └── AGENT_DEVELOPMENT.md     #       智能体开发
│
├── skills/                          # 🤖 Claude Code 技能
│   ├── idea-to-product/SKILL.md     #    想法落地技能
│   ├── super-butler/SKILL.md        #    超级管家技能
│   ├── application-generator/       #    申请书生成技能
│   ├── license-organizer/           #    证照整理技能
│   └── knowledge-indexer/           #    知识索引技能
│
├── 00_Agent_Library/                # 🔧 核心框架库
│   ├── agent_toolkit.py             #    AgentTool 工具框架
│   ├── workflow_engine.py           #    LangGraph 工作流引擎
│   ├── idea_workflow_engine.py      #    想法落地工作流引擎
│   ├── version_manager.py           #    版本管理器
│   └── EVOLUTION_GUIDE.md           #    演进系统说明
│
├── 01_Active_Projects/              # 🚀 活跃项目
│   ├── market_supervision_agent/    #    市场监管智能体
│   ├── memory_agent/                #    记忆助手
│   └── file_organizer/              #    文件整理工具
│
├── 02_Project_Archive/              # 📦 归档项目
├── 04_Data_&_Resources/             # 📊 数据和资源
├── 05_Outputs/                      # 📤 输出文件
└── 06_Learning_Journal/             # 📝 学习日志和演进记录
```

---

## 🚀 快速启动

### 方式A: 统一启动器 (推荐)

```bash
python office_agent_studio.py
# 或双击: 启动_OA_Studio.bat
```

### 方式B: 直接启动各工具

```bash
# 市场监管智能体 (Flask Web)
python 01_Active_Projects/market_supervision_agent/ui/flask_app.py
# 访问 http://127.0.0.1:5000

# 记忆助手 (Streamlit)
streamlit run 01_Active_Projects/memory_agent/ui/app.py
# 访问 http://localhost:8501

# 文件整理工具 (CLI)
python 01_Active_Projects/file_organizer/file_organizer.py
```

### 测试环境

```bash
# 测试市场监管智能体
python 01_Active_Projects/market_supervision_agent/jinja2_filler.py --test

# 测试记忆助手
python 01_Active_Projects/memory_agent/memory_agent.py --test
```

---

## 📋 核心规范速览

### 代码风格
✅ **Python版本**: 3.9+ (推荐 3.12)
✅ **编码**: UTF-8 with BOM (Windows兼容)
✅ **缩进**: 4空格
✅ **行长**: 100字符 (软限制120)

### 命名约定
✅ **文件名**: `snake_case.py` (如 `file_organizer.py`)
✅ **类名**: `PascalCase` (如 `FileOrganizer`)
✅ **函数名**: `snake_case` (如 `execute_task`)
✅ **常量**: `UPPER_SNAKE_CASE` (如 `MAX_RETRIES`)

### Windows 兼容性
```python
# 路径处理使用 pathlib
from pathlib import Path
WORKSPACE_ROOT = Path(__file__).parent

# 终端编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
```

---

## 🤖 可用技能速查

| 技能 | 触发关键词 | 详细文档 |
|-----|-----------|---------|
| 💡 **想法落地** | "我有个想法"、"想添加功能"、"能不能实现" | [SKILL.md](skills/idea-to-product/SKILL.md) |
| 🏠 **超级管家** | "超级管家"、"管家模式"、"工作区状态" | [SKILL.md](skills/super-butler/SKILL.md) |
| 📄 **申请书生成** | "生成申请书"、"填写申请表"、"个体工商户开业" | [SKILL.md](skills/application-generator/SKILL.md) |
| 📁 **证照整理** | "整理证照"、"归类文件"、"归档证件" | [SKILL.md](skills/license-organizer/SKILL.md) |
| 🔍 **知识索引** | "索引笔记"、"更新知识库"、"构建索引" | [SKILL.md](skills/knowledge-indexer/SKILL.md) |

> 💡 **提示**: 技能系统会在检测到关键词时自动激活，无需手动调用。

---

## 🔗 重要文档索引

### 系统文档
- 📖 [完整系统指南](COMPLETE_SYSTEM_GUIDE.md)
- 🔄 [演进系统说明](00_Agent_Library/EVOLUTION_GUIDE.md)
- 🗂️ [工作区索引](06_Learning_Journal/workspace_memory/workspace_index_latest.md)

### 快速链接
- 🚀 [想法落地工作流](docs/guides/IDEA_WORKFLOW.md) - 从模糊想法到可用产品
- 🤖 [超级管家模式](skills/super-butler/SKILL.md) - 统一工作区管理
- 🛠️ [扩展开发指南](docs/guides/AGENT_DEVELOPMENT.md) - 开发新智能体

---

## 💡 常见问题

### Q: 中文显示乱码?
**A**: 在代码中添加：
```python
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
```

### Q: Flask 启动失败?
**A**: 检查端口占用，默认 5000，可在 `flask_app.py` 中修改

### Q: Playwright 浏览器未安装?
**A**: 运行 `playwright install chromium`

### Q: 旧版本代码在哪?
**A**: 查看 `02_Project_Archive/version_backups/` 或保留在原目录的 `_v{版本}.py` 文件

---

## 📦 核心依赖

```
streamlit>=1.28.0        # Web界面
flask>=2.3.0             # Web服务
playwright>=1.40.0       # 浏览器自动化
python-docx>=1.0.0       # Word操作
pypdf2>=3.0.0            # PDF处理
jieba>=0.42.0            # 中文分词
chromadb>=0.4.0          # 向量数据库
sentence-transformers    # 嵌入模型
paddleocr>=2.7.0         # OCR (备用)
```

安装命令:
```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 🛠️ 常用维护命令

### 工作区维护
```bash
# 扫描并索引工作区
python workspace_scanner.py

# 清理缓存和临时文件
python workspace_cleaner.py

# 生成工作区报告
python workspace_report.py

# 创建快照
python create_snapshot.py
```

### 版本管理
```bash
# 生成版本报告
python 00_Agent_Library/version_manager.py

# 查看演进日志
cat 06_Learning_Journal/evolution_log.json

# 查看版本历史
cat 06_Learning_Journal/version_registry.json
```

---

## 🎯 核心智能体

### 市场监管智能体 (market_supervision_agent)
- **入口**: `ui/flask_app.py`
- **核心**: `jinja2_filler.py` (Jinja2模板引擎)
- **配置**: `config/database_schema.yaml`
- **模板**: `templates/个体工商户开业申请书（最终版）.docx`
- **OCR**: 支持百度OCR和PaddleOCR
- **输出**: `generated_applications/`

### 记忆助手 (memory_agent)
- **入口**: `ui/app.py`
- **核心**: `memory_agent.py`
- **存储**: ChromaDB 向量数据库
- **嵌入**: sentence-transformers
- **功能**: 添加笔记、语义搜索、间隔复习

### 文件整理工具 (file_organizer)
- **入口**: `file_organizer.py`
- **配置**: `config.json`
- **功能**: 按类型/日期/关键词整理文件

---

## ⚠️ 重要提醒

### 不兼容的操作
❌ 不要直接删除 `_v{版本}.py` 文件（历史版本）
❌ 不要修改 `06_Learning_Journal/` 中的 JSON 文件（自动生成）
❌ 不要移动 `02_Project_Archive/` 中的备份文件

### 推荐做法
✅ 使用 `workspace_scanner.py` 定期扫描工作区
✅ 升级前查看 `evolution_log.json` 了解变更
✅ 遇到问题查看 `COMPLETE_SYSTEM_GUIDE.md` 或 `docs/TROUBLESHOOTING.md`
✅ 使用版本管理器追踪变化

---

## 🚀 想法落地工作流 (Idea to Product) ⭐

当您有**新想法、改进需求或项目构想**时，系统提供5阶段流程：

```
模糊想法 → 澄清 → 探索 → 设计 → 原型 → 验证 → 可用产品
   (1分钟)  (10分)  (5分)  (15分)  (20分)  (10分)   总计<1小时
```

**快速启动**:
```python
# 运行工作流引擎
python 00_Agent_Library/idea_workflow_engine.py

# 或在Python中使用
from 00_Agent_Library.idea_workflow_engine import quick_start
session = quick_start("我想添加智能推荐功能")
```

**详细文档**: [docs/guides/IDEA_WORKFLOW.md](docs/guides/IDEA_WORKFLOW.md)

---

## 📚 文档系统说明

### 文档组织结构

本项目采用**分层文档系统**：

1. **CLAUDE.md** (本文件) - 核心配置和快速导航
2. **docs/** 目录 - 详细专题文档
3. **skills/** 目录 - 技能执行清单
4. **项目内文档** - 各项目的 README 和指南

### 文档使用原则

- ✅ **快速查询**: 先看 CLAUDE.md 的导航表
- ✅ **深入学习**: 查阅 docs/ 目录的专题文档
- ✅ **执行任务**: 参考 skills/ 目录的 SKILL.md
- ✅ **系统理解**: 阅读 COMPLETE_SYSTEM_GUIDE.md

---

**项目维护**: 使用 Claude Code (GLM-4.7) + VSCode 插件
**更新策略**: 增量升级，向后兼容
**版本追踪**: 自动化演进管理系统
**技能系统**: 自动化任务执行

**需要详细信息?** 查看 [docs/](docs/) 目录 📚
