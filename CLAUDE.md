# Office Agent Workspace - 项目配置

**项目类型**: Python 办公自动化工具集
**主要框架**: Streamlit, Flask, Playwright, AutoGen AgentTool, LangGraph, MCP
**Python版本**: 3.9+ (推荐 3.12)
**更新日期**: 2026-01-16
**当前版本**: v2.5.0

---

## 🎯 30秒快速导航

| 我想... | 查看文档 |
|---------|---------|
| 🚀 **快速上手** | [GETTING_STARTED.md](docs/GETTING_STARTED.md) |
| 🔗 **快速链接** | [QUICK_LINKS.md](QUICK_LINKS.md) |
| 🏗️ **了解架构** | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 📝 **查看编码规范** | [CODING_STANDARDS.md](docs/CODING_STANDARDS.md) |
| 🔧 **开发新功能** | [guides/AGENT_DEVELOPMENT.md](docs/guides/AGENT_DEVELOPMENT.md) |
| 🤖 **使用技能系统** | [guides/SKILLS_SYSTEM.md](docs/guides/SKILLS_SYSTEM.md) |
| 📋 **选择工作流模板** | [guides/TEMPLATES.md](docs/guides/TEMPLATES.md) |
| 💡 **想法落地工作流** | [guides/IDEA_WORKFLOW.md](docs/guides/IDEA_WORKFLOW.md) |
| 🤖 **自主代理工作流** | [guides/AUTONOMOUS_AGENT_WORKFLOW.md](docs/guides/AUTONOMOUS_AGENT_WORKFLOW.md) |
| 🐛 **排查问题** | [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) |
| 🧪 **测试与验证** | [guides/TESTING_GUIDE.md](docs/guides/TESTING_GUIDE.md) |
| 🌐 **MCP 新闻设置** | [guides/MCP_NEWS_SETUP.md](docs/guides/MCP_NEWS_SETUP.md) |
| 🎯 **Skill Seekers** | [guides/SKILL_SEEKERS_INTEGRATION.md](docs/guides/SKILL_SEEKERS_INTEGRATION.md) |
| ⭐ **v2.5 核心功能** | [05_Outputs/core_features_detailed_guide_20260116.md](05_Outputs/core_features_detailed_guide_20260116.md) |

---

## 🆕 v2.5 核心功能

2026-01-16 更新 - 语义记忆系统与AI训练系统

### 🔧 v2.5 核心升级

| 组件 | 功能 | 位置 | 状态 |
|------|------|------|------|
| **语义记忆 v2.5** | 向量语义搜索 | [claude_memory.py](00_Agent_Library/claude_memory.py) | ✅ SSL修复完成 |
| **AI训练系统** | 21天学习路径 | [ai_agent_training_system/](01_Active_Projects/ai_agent_training_system/) | ✅ supervisor注释 |
| **快速链接索引** | 工作区快速导航 | [QUICK_LINKS.md](QUICK_LINKS.md) | ✅ 已创建 |
| **会话总结** | 每日会话记录 | [daily_session_summary.py](00_Agent_Library/daily_session_summary.py) | ✅ 自动化 |

### 🔧 v2.0 四大核心组件

| 组件 | 功能 | 位置 | 状态 |
|------|------|------|------|
| **SQLite MCP** | 统一数据访问层 | [mcp_sqlite_wrapper.py](00_Agent_Library/mcp_sqlite_wrapper.py) | ✅ 测试通过 |
| **ConfigCenter** | 分层配置系统 | [config_center.py](00_Agent_Library/config_center.py) | ✅ 测试通过 |
| **AgentSupervisor** | 智能体协作编排 | [agent_supervisor.py](00_Agent_Library/agent_supervisor.py) | ✅ 测试通过 |
| **Workflow Templates** | 可复用工作流 | [workflow_templates.py](00_Agent_Library/workflow_templates.py) | ✅ 测试通过 |

### 📊 架构升级

**Before (v1.x)**: 独立智能体，分散配置，异构数据库
**After (v2.0)**: 统一监督者，分层配置，MCP统一接口

### 🚀 快速使用

```bash
# 初始化配置中心
python 00_Agent_Library/config_center.py init

# 使用智能体监督者
python 00_Agent_Library/agent_supervisor.py

# 查看工作流模板
python 00_Agent_Library/workflow_templates.py
```

详细文档: [core_features_detailed_guide_20260116.md](05_Outputs/core_features_detailed_guide_20260116.md)

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
│       ├── TEMPLATES.md             #       工作流模板索引
│       ├── IDEA_WORKFLOW.md         #       想法落地工作流
│       ├── AUTONOMOUS_AGENT_WORKFLOW.md  # 自主代理工作流
│       ├── SKILLS_SYSTEM.md         #       技能系统说明
│       ├── VERSION_MANAGEMENT.md    #       版本管理
│       └── AGENT_DEVELOPMENT.md     #       智能体开发
│
├── skills/                          # 🤖 Claude Code 技能
│   ├── idea-to-product/SKILL.md     #    想法落地技能
│   ├── super-butler/SKILL.md        #    超级管家技能
│   ├── application-generator/       #    申请书生成技能
│   ├── license-organizer/           #    证照整理技能
│   ├── knowledge-indexer/           #    知识索引技能
│   └── skill-creator/SKILL.md       #    技能创建器 ⭐ NEW
│
├── 00_Agent_Library/                # 🔧 核心框架库
│   ├── agent_toolkit.py             #    AgentTool 工具框架
│   ├── workflow_engine.py           #    LangGraph 工作流引擎
│   ├── idea_workflow_engine.py      #    想法落地工作流引擎
│   ├── version_manager.py           #    版本管理器
│   ├── agent_supervisor.py          #    ⭐ 智能体监督者 (v2.0)
│   ├── config_center.py             #    ⭐ 统一配置中心 (v2.0)
│   ├── mcp_sqlite_wrapper.py        #    ⭐ MCP SQLite 服务器 (v2.0)
│   ├── workflow_templates.py        #    ⭐ 工作流模板系统 (v2.0)
│   ├── workflow_templates/          #    工作流模板目录
│   ├── claude_memory.py             #    ⭐ Claude 记忆模块 (v2.0/v2.5)
│   ├── exceptions.py                #    ⭐ 异常处理系统 (v2.0)
│   ├── semantic_memory.py           #    ⭐ 语义向量搜索 (v2.5)
│   ├── fix_ssl_issue.py             #    SSL修复工具 (v2.5)
│   ├── test_ssl_fix.py              #    SSL修复测试 (v2.5)
│   ├── diagram_generator.py         #    图表生成器
│   ├── workspace_diagram_generator.py #    工作区图表生成器
│   ├── glm_knowledge_accessor.py    #    GLM 知识访问器
│   ├── mcp_news_client.py           #    MCP 新闻客户端
│   ├── memory_monitor.py            #    记忆监控
│   ├── memory_trigger.py            #    记忆触发器
│   ├── session_initializer.py       #    会话初始化器
│   ├── skill_seekers_adapter.py     #    Skill Seekers 适配器
│   ├── skill_builder_facade.py      #    技能构建器门面
│   ├── smart_news_monitor.py        #    智能新闻监控
│   ├── news_reader.py               #    新闻读取器
│   ├── news_scraper.py              #    新闻爬虫
│   ├── auto_session_starter.py      #    自动会话启动器
│   └── EVOLUTION_GUIDE.md           #    演进系统说明
│
├── 01_Active_Projects/              # 🚀 活跃项目
│   ├── market_supervision_agent/    #    市场监管智能体
│   ├── memory_agent/                #    记忆助手
│   ├── file_organizer/              #    文件整理工具
│   ├── pdf_processor/               #    PDF 处理工具
│   ├── smart_translator/            #    智能翻译工具
│   ├── smart_tools/                 #    智能工具集 ⭐ NEW
│   ├── langgraph_supervisor_experiment/  #    LangGraph 监督者实验 ⭐ NEW
│   ├── ai_agent_training_system/    #    AI智能体训练系统 ⭐ NEW
│   ├── ai_news_tracker/             #    AI 新闻追踪器
│   └── 06_Learning_Journal/         #    学习日志软链接
│
├── 02_Project_Archive/              # 📦 归档项目
├── 04_Data_&_Resources/             # 📊 数据和资源
│   └── config/                      # ⭐ 统一配置目录 (v2.0)
├── 05_Outputs/                      # 📤 输出文件
│   └── core_features_detailed_guide_20260116.md  # v2.0 功能详解
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
| 🛠️ **技能创建器** | "创建技能"、"开发新技能"、"技能生成" | [SKILL.md](skills/skill-creator/SKILL.md) |
| 📰 **新闻资讯** | "今日新闻"、"热点新闻"、"有什么新闻" | 见下方「📰 新闻资讯工具」 |

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

### PDF 处理工具 (pdf_processor)
- **入口**: `main.py`
- **核心**: `pdf_extractor.py`
- **功能**: PDF 内容提取、文本分析、批量处理

### 智能翻译工具 (smart_translator)
- **功能**: 多语言智能翻译
- **特点**: 上下文感知翻译

### 智能工具集 (smart_tools)
- **功能**: 常用办公工具集合
- **特点**: 模块化设计

### LangGraph 监督者实验 (langgraph_supervisor_experiment)
- **功能**: LangGraph 智能体协作实验
- **特点**: 多智能体监督模式

### AI智能体训练系统 (ai_agent_training_system) ⭐ NEW
- **入口**: `automation_agents/supervisor.py`
- **AI培训老师**: Streamlit学习界面（21天学习路径）
- **自动化监督者**: 多Agent协作工作流
- **测试网站**: Flask测试服务器
- **文档**: [SUPERVISOR_ANNOTATED.md](01_Active_Projects/ai_agent_training_system/automation_agents/SUPERVISOR_ANNOTATED.md) - 详细注释
- **特点**:
  - 7个核心类完整中文注释
  - SSL证书问题修复
  - 语义记忆系统集成
  - 自动化测试流程

---

## 📰 新闻资讯工具 ⭐ NEW

### 🏠 新闻中心（统一入口）
- **入口**: `news_center.py`
- **功能**: 整合多种新闻获取方式，提供交互式菜单
- **使用方式**:
```bash
python news_center.py
```

**支持的获取方式**:
1. 🕷️ **Playwright 爬虫** - 微博真实数据
2. 📦 **模拟数据** - 多平台演示
3. 🌐 **MCP 服务器** - 标准化接口
4. 📖 **部署教程** - DailyHotApi + Vercel
5. 🔧 **TrendRadar** - GitHub Actions 自动化

### 🕷️ Playwright 爬虫
- **入口**: `00_Agent_Library/news_scraper.py`
- **功能**: 直接爬取平台真实数据
- **支持**: 微博（已验证）、知乎、百度
- **使用方式**:
```bash
python 00_Agent_Library/news_scraper.py
```

### 📦 统一新闻读取器
- **入口**: `00_Agent_Library/news_reader.py`
- **功能**: 整合多个新闻源，提供一致的接口
- **支持平台**: 知乎、微博、百度、B站、抖音、今日头条、36氪
- **使用方式**:
```bash
# 获取默认平台（知乎、微博、B站）
python 00_Agent_Library/news_reader.py

# 指定平台
python 00_Agent_Library/news_reader.py -p zhihu weibo bilibili

# 指定数量
python 00_Agent_Library/news_reader.py -n 15
```

### 🧠 智能新闻监控助手
- **入口**: `00_Agent_Library/smart_news_monitor.py`
- **功能**: 记住用户兴趣，智能匹配相关新闻
- **支持平台**: 知乎、微博、B站、抖音、快手
- **特点**: 长期/短期兴趣管理，自动学习关键词

### 🤖 AI 新闻追踪器
- **入口**: `01_Active_Projects/ai_news_tracker/`
- **功能**: 追踪 GitHub AI 项目、MCP 服务器、AI 工具更新
- **报告**: 自动生成每日新闻报告

### 🌐 MCP 新闻服务器（已安装）
| 服务器 | 平台数 | 启动命令 |
|--------|--------|----------|
| mcp-hot-news | 13+ | `mcp-hot-news` |
| @wopal/mcp-server-hotnews | 9 | `npx @wopal/mcp-server-hotnews` |

### 📖 部署指南
- **文档**: [docs/guides/DEPLOY_DAILYHOTAPI.md](docs/guides/DEPLOY_DAILYHOTAPI.md)
- **内容**: DailyHotApi Vercel 部署、TrendRadar 设置、爬虫优化

### 📚 相关指南
- **MCP 新闻设置**: [docs/guides/MCP_NEWS_SETUP.md](docs/guides/MCP_NEWS_SETUP.md)
- **TrendRadar 设置**: [docs/guides/TRENDRADAR_SETUP.md](docs/guides/TRENDRADAR_SETUP.md)

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

## 🧪 测试与质量保证

### 测试指南
- **文档**: [docs/guides/TESTING_GUIDE.md](docs/guides/TESTING_GUIDE.md)
- **内容**: 单元测试、集成测试、端到端测试

### 自动会话启动器
- **入口**: `00_Agent_Library/auto_session_starter.py`
- **文档**: [docs/guides/AUTO_SESSION_STARTER.md](docs/guides/AUTO_SESSION_STARTER.md)
- **功能**: 自动化会话初始化和工作区准备

### 记忆监控
- **入口**: `00_Agent_Library/memory_monitor.py`
- **文档**: [docs/guides/MEMORY_MONITOR.md](docs/guides/MEMORY_MONITOR.md)
- **功能**: 监控记忆系统性能和状态

---

## 🎯 Skill Seekers 集成

### 概述
Skill Seekers 是一个技能发现和集成平台，支持自动化技能管理和部署。

### 核心组件
- **适配器**: [skill_seekers_adapter.py](00_Agent_Library/skill_seekers_adapter.py)
- **构建器**: [skill_builder_facade.py](00_Agent_Library/skill_builder_facade.py)

### 详细文档
- **集成指南**: [docs/guides/SKILL_SEEKERS_INTEGRATION.md](docs/guides/SKILL_SEEKERS_INTEGRATION.md)

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
**记忆系统**: Claude 记忆增强 (v2.5)
**质量保证**: 测试框架和错误处理系统

**需要详细信息?** 查看 [docs/](docs/) 目录 📚
