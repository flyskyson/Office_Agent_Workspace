# 🤖 AI 新闻追踪智能体 - 使用指南

## ✅ 已创建完成

您的 **AI 新闻追踪智能体** 已成功配置！

---

## 📊 今日新闻摘要（2026-01-14）

### 🔥 GitHub 热门 AI 项目

| 项目 | 描述 | 标签 |
|------|------|------|
| [TrendRadar](https://github.com/sansan0/TrendRadar) | AI 舆情监控工具，支持 MCP 集成 | MCP, AI, News |
| [mcp-hot-news-server](https://github.com/wudalu/mcp-hot-news-server) | 多平台热点新闻聚合 MCP 服务器 | MCP, News, FastAPI |

### 📦 最新 MCP 服务器

| 服务器 | 状态 | 描述 |
|--------|------|------|
| chrome-devtools-mcp | ✅ 已配置 | Chrome 官方 DevTools MCP |
| playwright-mcp | ✅ 已配置 | Playwright 浏览器自动化 |
| hot-news | 🆕 新增 | 热点新闻聚合 |

### 🛠️ 新发布的 AI 工具

| 工具 | 发布日期 | 分类 |
|------|---------|------|
| **Claude Cowork** | 2026-01-12 | 通用 AI 工作助手 |
| **Claude Code 2.1** | 2026-01-07 | 开发工具（109 项优化） |
| **TrendRadar v3.0** | 2026-01-11 | 新闻聚合器 |

---

## 🚀 使用方式

### 方式 1: 直接问我

在 Claude Code 中直接问：

```
- "今天有什么 AI 新闻？"
- "最新的 MCP 服务器有哪些？"
- "GitHub 上有什么热门 AI 项目？"
- "有什么新的 AI 工具发布？"
```

### 方式 2: 运行新闻追踪器

```bash
# 生成今日新闻报告
python 01_Active_Projects/ai_news_tracker/src/news_tracker.py

# 查看保存的报告
cat 01_Active_Projects/ai_news_tracker/data/daily_news_20260114.md
```

### 方式 3: 使用 MCP 热点新闻服务器

在 MCP 连接后，可以使用：
- `mcp__hot-news__get_trending` - 获取热点新闻
- `mcp__hot-news__search` - 搜索特定主题

---

## 📚 推荐的新闻源

### 官方资源

| 资源 | 链接 | 说明 |
|------|------|------|
| **Claude Code 文档** | [code.claude.com](https://code.claude.com) | 官方文档和更新 |
| **MCP Pulse** | [pulsemcp.com](https://www.pulsemcp.com) | MCP 服务器目录 |
| **GitHub Trending** | [github.com/trending](https://github.com/trending) | 热门项目 |

### 社区资源

| 资源 | 链接 | 说明 |
|------|------|------|
| **Hacker News** | [news.ycombinator.com](https://news.ycombinator.com) | 技术新闻 |
| **Reddit ML** | [r/MachineLearning](https://reddit.com/r/MachineLearning) | ML 社区 |
| **Best MCP 2026** | [Builder.io](https://www.builder.io/blog/best-mcp-servers-2026) | MCP 服务器推荐 |

---

## 🎯 项目文件

| 文件 | 说明 |
|------|------|
| [README.md](01_Active_Projects/ai_news_tracker/README.md) | 项目说明 |
| [src/news_tracker.py](01_Active_Projects/ai_news_tracker/src/news_tracker.py) | 主程序 |
| [config/keywords.yaml](01_Active_Projects/ai_news_tracker/config/keywords.yaml) | 关键词配置 |
| [data/daily_news_*.md](01_Active_Projects/ai_news_tracker/data/) | 每日新闻存档 |

---

## 🔧 自定义配置

编辑 `config/keywords.yaml` 添加您感兴趣的关键词：

```yaml
keywords:
  - MCP
  - Claude Code
  - 您的关键词

sources:
  github:
    enabled: true
  hacker_news:
    enabled: true
```

---

## 📅 每日自动更新

使用 Windows 任务计划程序自动运行：

```batch
schtasks /create /tn "AI News Daily" /tr "python C:\Users\flyskyson\Office_Agent_Workspace\01_Active_Projects\ai_news_tracker\src\news_tracker.py" /sc daily /st 09:00
```

---

## 🌟 相关工具推荐

### 1. TrendRadar
- **GitHub**: [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)
- **功能**: AI 舆情监控，支持 MCP 集成
- **特色**: 自然语言交互分析新闻

### 2. News Agents
- **GitHub**: [eugeneyan/news-agents](https://github.com/eugeneyan/news-agents)
- **功能**: 基于 MCP 的终端新闻聚合
- **特色**: Amazon Q + MCP + tmux

### 3. MCP Hot News Server
- **GitHub**: [wudalu/mcp-hot-news-server](https://github.com/wudalu/mcp-hot-news-server)
- **功能**: 多平台热点新闻
- **特色**: FastMCP 框架

---

**创建时间**: 2026-01-14
**版本**: 1.0.0
**状态**: ✅ 运行正常
