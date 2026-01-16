# MCP 新闻服务器集成指南

**更新日期**: 2026-01-16
**状态**: 立即行动项目 ✅

---

## 📋 概述

本指南介绍如何将 MCP 新闻服务器集成到工作区，提供统一的多平台新闻聚合服务。

### 支持的 MCP 服务器

| 服务器 | 平台数 | 命令 | 状态 |
|--------|--------|------|------|
| mcp-hot-news | 13+ | `npx -y mcp-hot-news` | ✅ 推荐 |
| @wopal/mcp-server-hotnews | 9 | `npx -y @wopal/mcp-server-hotnews` | ✅ 可用 |

---

## 🚀 快速开始

### 方式 1: 使用统一客户端（推荐）

```bash
# 获取默认平台新闻
python 00_Agent_Library/mcp_news_client.py

# 获取技术新闻
python 00_Agent_Library/mcp_news_client.py --tech

# 指定平台
python 00_Agent_Library/mcp_news_client.py -p zhihu weibo github -n 30

# 保存报告
python 00_Agent_Library/mcp_news_client.py --tech -o 05_Outputs/news_report.md
```

### 方式 2: 使用现有工具

```bash
# 知乎、微博、B站
python 00_Agent_Library/news_reader.py

# 智能新闻助手（带兴趣匹配）
python 00_Agent_Library/smart_news_assistant.py
```

---

## 🔧 MCP 服务器配置

### 在 Claude Code 中配置 MCP 服务器

编辑 `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mcp-hot-news": {
      "command": "npx",
      "args": ["-y", "mcp-hot-news"]
    },
    "wopal-hotnews": {
      "command": "npx",
      "args": ["-y", "@wopal/mcp-server-hotnews"]
    }
  }
}
```

### Windows 用户注意事项

```json
{
  "mcpServers": {
    "mcp-hot-news": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "mcp-hot-news"]
    }
  }
}
```

---

## 📊 支持的平台

| 平台 | 代码 | 技术类 | 说明 |
|------|------|--------|------|
| 知乎 | zhihu | ✅ | 知乎热榜 |
| 微博 | weibo | ❌ | 微博热搜 |
| 百度 | baidu | ❌ | 百度热搜 |
| B站 | bilibili | ✅ | B站热门 |
| 抖音 | douyin | ❌ | 抖音热点 |
| 快手 | kuaishou | ❌ | 快手热榜 |
| 今日头条 | toutiao | ❌ | 头条热榜 |
| 36氪 | 36kr | ✅ | 36氪快讯 |
| CSDN | csdn | ✅ | CSDN头条 |
| GitHub | github | ✅ | GitHub趋势 |

---

## 🔌 集成到现有工具

### 1. 智能新闻助手升级

将 `00_Agent_Library/smart_news_assistant.py` 改为使用 MCP 客户端：

```python
from mcp_news_client import MCPNewsClient

async def get_matched_news():
    client = MCPNewsClient()
    results = await client.get_news(platforms=["zhihu", "github", "csdn"], limit=30)

    # 兴趣匹配逻辑...
    return matched_news
```

### 2. 超级管家技能

在 `skills/super-butler/SKILL.md` 中添加：

```markdown
## 步骤 6: 获取资讯

使用 MCP 新闻客户端获取最新资讯：

```bash
python 00_Agent_Library/mcp_news_client.py --tech
```
```

---

## 🛠️ 故障排查

### 问题 1: MCP 服务器无法启动

**症状**: `npx: command not found`

**解决方案**:
```bash
# 检查 Node.js 安装
node --version
npm --version

# 重新安装 Node.js
# 下载: https://nodejs.org/
```

### 问题 2: 网络请求失败

**症状**: 获取数据超时

**解决方案**:
- 使用本地 API 备份方案（已内置）
- 配置代理（如需要）

### 问题 3: 中文乱码

**解决方案**:
```python
# 在脚本开头添加
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
```

---

## 📈 性能优化

### 并发请求

```python
import asyncio

async def fetch_multiple():
    client = MCPNewsClient()

    # 并发获取多个平台
    tasks = [
        client.get_news(["zhihu"], 20),
        client.get_news(["github"], 20),
        client.get_news(["csdn"], 20)
    ]

    results = await asyncio.gather(*tasks)
    return results
```

### 缓存机制

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedMCPClient(MCPNewsClient):
    def __init__(self):
        super().__init__()
        self.cache = {}
        self.cache_time = {}

    async def get_news(self, platforms=None, limit=20, ttl=1800):
        cache_key = f"{','.join(platforms or [])}-{limit}"

        # 检查缓存
        if cache_key in self.cache:
            cache_age = (datetime.now() - self.cache_time[cache_key]).seconds
            if cache_age < ttl:
                return self.cache[cache_key]

        # 获取新数据
        results = await super().get_news(platforms, limit)
        self.cache[cache_key] = results
        self.cache_time[cache_key] = datetime.now()

        return results
```

---

## 📝 下一步计划

- [ ] 部署私有 MCP 新闻服务器（使用 DailyHotApi + Vercel）
- [ ] 添加更多平台支持
- [ ] 实现增量更新（只获取新新闻）
- [ ] 添加新闻分类和标签
- [ ] 集成到 Claude Code 技能系统

---

## 📚 相关资源

- [mcp-hot-news GitHub](https://github.com/wudalu/mcp-hot-news-server)
- [@wopal/mcp-server-hotnews](https://github.com/wopal-cn/mcp-hotnews-server)
- [MCP 官方文档](https://modelcontextprotocol.io/)
- [部署指南](DEPLOY_DAILYHOTAPI.md)

---

**生成者**: Claude Code (GLM-4.7)
**项目**: Office Agent Workspace
**路径**: [docs/guides/MCP_NEWS_SETUP.md](docs/guides/MCP_NEWS_SETUP.md)
