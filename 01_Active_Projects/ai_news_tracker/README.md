# AI 新闻追踪智能体

## 🎯 项目简介

**AI News Tracker** 是一个专门追踪 AI 行业动态的智能助手，帮助您及时了解：
- 🔥 最新 AI 工具发布
- 📦 版本更新和 MCP 服务器
- 🐙 GitHub 热门 AI 项目
- 📰 技术博客和新闻
- 🔌 Claude Code 插件和技能

---

## ✨ 核心功能

### 1. 多源新闻聚合
- ✅ GitHub Trending (AI/ML)
- ✅ Hacker News
- ✅ Reddit r/MachineLearning
- ✅ MCP 服务器更新
- ✅ Claude Code 官方博客

### 2. 智能分类
- 🛠️ **新工具** - 新发布的 AI 工具
- 📦 **版本更新** - MCP 服务器、插件更新
- 🐙 **GitHub 热门** - 上升趋势的项目
- 📝 **技术文章** - 深度技术分析
- 🎓 **教程资源** - 学习材料

### 3. 个性化推荐
- 根据您的兴趣过滤
- 关键词追踪（如 "MCP", "Claude Code", "Agent"）
- 每日/每周摘要

---

## 🚀 使用方式

### 方式 1: 使用 MCP 新闻服务器（推荐）

已集成的 MCP 服务器：

```json
{
  "mcpServers": {
    "news-aggregator": {
      "command": "npx",
      "args": ["-y", "mcp-hot-news-server"]
    }
  }
}
```

### 方式 2: 运行 Python 脚本

```bash
cd 01_Active_Projects/ai_news_tracker
python src/news_tracker.py
```

### 方式 3: 直接问 Claude

```
- "今天有什么 AI 新闻？"
- "最新的 MCP 服务器有哪些？"
- "GitHub 上有什么热门 AI 项目？"
- "Claude Code 有新版本吗？"
```

---

## 📊 推荐工具列表

### 新闻聚合工具

| 工具 | 类型 | 来源 |
|------|------|------|
| **TrendRadar** | MCP 集成 | [GitHub](https://github.com/sansan0/TrendRadar) |
| **MCP Hot News Server** | MCP 服务器 | [GitHub](https://github.com/wudalu/mcp-hot-news-server) |
| **News Agents** | MCP 实验 | [GitHub](https://github.com/eugeneyan/news-agents) |

### 追踪源

- 🔗 [MCP Pulse](https://www.pulsemcp.com) - MCP 服务器目录
- 🔗 [Claude Code Docs](https://code.claude.com) - 官方文档
- 🔗 [GitHub Trending](https://github.com/trending) - 热门项目
- 🔗 [Hacker News](https://news.ycombinator.com) - 技术新闻

---

## 🛠️ 项目结构

```
ai_news_tracker/
├── src/
│   ├── news_tracker.py      # 主程序
│   ├── sources/             # 新闻源配置
│   └── analyzers/           # 内容分析器
├── data/
│   ├── daily_news.json      # 每日新闻
│   └── tracked_tools.json   # 追踪的工具列表
├── config/
│   └── keywords.yaml        # 关键词配置
└── README.md
```

---

## 🎯 快速开始

### 1. 配置关键词追踪

编辑 `config/keywords.yaml`:
```yaml
keywords:
  - MCP
  - Claude Code
  - AI Agent
  - LLM
  - Browser Automation

sources:
  - github_trending
  - hacker_news
  - mcp_pulse
```

### 2. 获取今日新闻

```bash
python src/news_tracker.py --today
```

### 3. 生成周报

```bash
python src/news_tracker.py --week
```

---

## 📈 集成到工作区

添加到 `office_agent_studio.py` 菜单：

```
[6] AI 新闻追踪
    - 获取今日 AI 新闻
    - 查看最新 MCP 服务器
    - GitHub 热门 AI 项目
    - Claude Code 更新
```

---

## 🔄 自动化

### 每日自动更新

使用 Windows 任务计划程序：

```batch
schtasks /create /tn "AI News Daily" /tr "python /path/to/news_tracker.py --today" /sc daily /st 09:00
```

---

## 📚 相关资源

- [TrendRadar v3.0.0](https://github.com/sansan0/TrendRadar) - AI 舆情监控
- [Best MCP Servers 2026](https://www.builder.io/blog/best-mcp-servers-2026)
- [Top MCP Projects](https://www.nocobase.com/en/blog/github-open-source-mcp-projects)

---

**创建时间**: 2026-01-14
**版本**: 1.0.0
**维护者**: Office Agent Workspace
