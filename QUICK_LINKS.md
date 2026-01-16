# 🚀 快速链接索引 - Office Agent Workspace

**更新日期**: 2026-01-16

---

## 📖 核心文档

| 文档 | 描述 | 链接 |
|------|------|------|
| **CLAUDE.md** | 项目配置和导航 | [CLAUDE.md](CLAUDE.md) |
| **TODO.md** | 待办事项清单 | [TODO.md](TODO.md) |
| **README** | 完整系统指南 | [COMPLETE_SYSTEM_GUIDE.md](COMPLETE_SYSTEM_GUIDE.md) |

---

## 🏗️ 架构文档

| 文档 | 描述 | 链接 |
|------|------|------|
| **架构设计** | 系统架构说明 | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| **编码规范** | 代码风格指南 | [docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md) |
| **故障排查** | 问题解决指南 | [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) |

---

## 📚 专题指南

### 工作流模板
- **模板索引**: [docs/guides/TEMPLATES.md](docs/guides/TEMPLATES.md)
- **想法落地**: [docs/guides/IDEA_WORKFLOW.md](docs/guides/IDEA_WORKFLOW.md)
- **自主代理**: [docs/guides/AUTONOMOUS_AGENT_WORKFLOW.md](docs/guides/AUTONOMOUS_AGENT_WORKFLOW.md)

### 系统功能
- **v2.0核心功能**: [05_Outputs/core_features_detailed_guide_20260116.md](05_Outputs/core_features_detailed_guide_20260116.md)
- **记忆系统**: [docs/guides/SEMANTIC_MEMORY_GUIDE.md](docs/guides/SEMANTIC_MEMORY_GUIDE.md)
- **记忆监控**: [docs/guides/MEMORY_MONITOR.md](docs/guides/MEMORY_MONITOR.md)
- **自动会话**: [docs/guides/AUTO_SESSION_STARTER.md](docs/guides/AUTO_SESSION_STARTER.md)
- **MCP新闻**: [docs/guides/MCP_NEWS_SETUP.md](docs/guides/MCP_NEWS_SETUP.md)
- **Skill Seekers**: [docs/guides/SKILL_SEEKERS_INTEGRATION.md](docs/guides/SKILL_SEEKERS_INTEGRATION.md)

### 开发指南
- **智能体开发**: [docs/guides/AGENT_DEVELOPMENT.md](docs/guides/AGENT_DEVELOPMENT.md)
- **测试指南**: [docs/guides/TESTING_GUIDE.md](docs/guides/TESTING_GUIDE.md)
- **版本管理**: [docs/guides/VERSION_MANAGEMENT.md](docs/guides/VERSION_MANAGEMENT.md)

---

## 🤖 技能系统

| 技能 | 触发关键词 | 文档 |
|------|-----------|------|
| **想法落地** | "我有个想法"、"想添加功能" | [skills/idea-to-product/SKILL.md](skills/idea-to-product/SKILL.md) |
| **超级管家** | "超级管家"、"工作区状态" | [skills/super-butler/SKILL.md](skills/super-butler/SKILL.md) |
| **申请书生成** | "生成申请书"、"填写申请表" | [skills/application-generator/SKILL.md](skills/application-generator/SKILL.md) |
| **证照整理** | "整理证照"、"归类文件" | [skills/license-organizer/SKILL.md](skills/license-organizer/SKILL.md) |
| **知识索引** | "索引笔记"、"更新知识库" | [skills/knowledge-indexer/SKILL.md](skills/knowledge-indexer/SKILL.md) |
| **技能创建器** | "创建技能"、"开发新技能" | [skills/skill-creator/SKILL.md](skills/skill-creator/SKILL.md) |

---

## 🔧 核心框架

### 00_Agent_Library/

| 文件 | 功能 | 链接 |
|------|------|------|
| **claude_memory.py** | 记忆系统核心 | [00_Agent_Library/claude_memory.py](00_Agent_Library/claude_memory.py) |
| **semantic_memory.py** | 语义向量搜索 | [00_Agent_Library/semantic_memory.py](00_Agent_Library/semantic_memory.py) |
| **workflow_engine.py** | LangGraph工作流引擎 | [00_Agent_Library/workflow_engine.py](00_Aagent_Library/workflow_engine.py) |
| **agent_supervisor.py** | 智能体监督者 | [00_Agent_Library/agent_supervisor.py](00_Agent_Library/agent_supervisor.py) |
| **memory_monitor.py** | 记忆性能监控 | [00_Agent_Library/memory_monitor.py](00_Agent_Library/memory_monitor.py) |

### 工具脚本

| 脚本 | 功能 | 运行方式 |
|------|------|---------|
| **fix_ssl_issue.py** | SSL问题修复工具 | `python 00_Agent_Library/fix_ssl_issue.py` |
| **test_ssl_fix.py** | SSL修复验证测试 | `python 00_Agent_Library/test_ssl_fix.py` |
| **启动_Claude_v25会话.bat** | 快速启动脚本 | 双击运行 |

---

## 🚀 活跃项目

### 01_Active_Projects/

| 项目 | 描述 | 入口 |
|------|------|------|
| **market_supervision_agent** | 市场监管智能体 | `ui/flask_app.py` |
| **memory_agent** | 记忆助手 | `ui/app.py` (Streamlit) |
| **ai_agent_training_system** | AI智能体训练系统 | `ai_tutor_bot/app.py` |
| **langgraph_supervisor_experiment** | LangGraph监督者实验 | - |
| **smart_tools** | 智能工具集 | - |

### AI训练系统详情

| 组件 | 描述 | 链接 |
|------|------|------|
| **AI培训老师** | Streamlit学习界面 | [ai_tutor_bot/app.py](01_Active_Projects/ai_agent_training_system/ai_tutor_bot/app.py) |
| **自动化监督者** | 多Agent协作 | [automation_agents/supervisor.py](01_Active_Projects/ai_agent_training_system/automation_agents/supervisor.py) |
| **测试网站** | Flask测试服务器 | [test_site/server.py](01_Active_Projects/ai_agent_training_system/test_site/server.py) |

---

## 📤 输出报告

### 今日生成 (2026-01-16)

| 报告 | 描述 | 链接 |
|------|------|------|
| **会话总结** | 今日工作总结 | [05_Outputs/daily_session_summary_20260116.md](05_Outputs/daily_session_summary_20260116.md) |
| **更新总结** | 每日更新 | [05_Outputs/daily_update_summary_20260116.md](05_Outputs/daily_update_summary_20260116.md) |
| **SSL修复指南** | SSL问题解决 | [00_Agent_Library/fix_ssl_issue.py](00_Agent_Library/fix_ssl_issue.py) |
| **supervisor注释** | 代码注释文档 | [automation_agents/SUPERVISOR_ANNOTATED.md](01_Active_Projects/ai_agent_training_system/automation_agents/SUPERVISOR_ANNOTATED.md) |

### 其他重要报告

- [05_Outputs/semantic_memory_implementation_complete_20260116.md](05_Outputs/semantic_memory_implementation_complete_20260116.md)
- [05_Outputs/v25_integration_guide_20260116.md](05_Outputs/v25_integration_guide_20260116.md)
- [05_Outputs/skill_seekers_integration_report_20260116.md](05_Outputs/skill_seekers_integration_report_20260116.md)

---

## 🧩 学习资源

### 21天AI训练路径

**Week 1: 基础入门**
- Day 1-2: Playwright基础
- Day 3-4: Streamlit入门
- Day 5-7: 登录自动化

**Week 2: 核心技术**
- Day 8-10: LangGraph工作流
- Day 11-12: Agent设计模式
- Day 13-14: 表单自动化

**Week 3: 高级集成**
- Day 15-17: 多Agent协作
- Day 18-19: MCP工具集成
- Day 20-21: 完整系统部署

---

## 🔍 快速命令

### 启动命令

```bash
# AI培训老师（学习入口）
streamlit run 01_Active_Projects/ai_agent_training_system/ai_tutor_bot/app.py

# 市场监管智能体
python 01_Active_Projects/market_supervision_agent/ui/flask_app.py

# 记忆助手
streamlit run 01_Active_Projects/memory_agent/ui/app.py

# 工作区统一启动器
python office_agent_studio.py
```

### 测试命令

```bash
# SSL修复测试
python 00_Agent_Library/test_ssl_fix.py

# 记忆性能监控
python 00_Agent_Library/memory_monitor.py

# 市场监管智能体测试
python 01_Active_Projects/market_supervision_agent/jinja2_filler.py --test
```

---

## 📞 帮助与支持

- **问题排查**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **完整指南**: [COMPLETE_SYSTEM_GUIDE.md](COMPLETE_SYSTEM_GUIDE.md)
- **项目路线图**: [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)

---

**更新**: 2026-01-16
**版本**: v2.5.0
