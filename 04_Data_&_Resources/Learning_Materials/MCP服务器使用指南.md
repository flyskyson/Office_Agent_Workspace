# MCP 服务器配置说明

## 📦 已安装的 MCP 服务器

你的工作区现在配置了 4 个 MCP 服务器：

### 1. 🎭 Playwright MCP (微软官方)

**包名**: `@playwright/mcp@latest`
**版本**: 0.0.54
**开发商**: Microsoft
**功能**: 强大的浏览器自动化和测试

**能力**:
- ✅ 跨浏览器自动化（Chrome、Firefox、Safari、Edge）
- ✅ 网页截图和PDF生成
- ✅ 表单自动填写
- ✅ 点击、输入、导航等用户操作
- ✅ 网络拦截和Mock
- ✅ 移动端模拟
- ✅ API 测试

**使用示例**:
```
"用 Playwright 自动登录这个网站"
"截取整个网页的截图"
"测试这个表单提交功能"
"批量爬取这个网站的列表数据"
```

**优势**:
- 🎯 微软官方维护，质量保证
- 🌐 支持所有主流浏览器
- 📱 移动端模拟
- 🔄 自动等待元素，稳定性高

---

### 2. 🌐 Chrome DevTools MCP

**包名**: `chrome-devtools-mcp@latest`
**版本**: 0.12.1
**功能**: 浏览器调试、性能分析、网络监控

**能力**:
- ✅ 检查网页元素和样式
- ✅ 监控网络请求
- ✅ 分析 JavaScript 错误
- ✅ 性能追踪（LCP、FCP等）
- ✅ 自动化浏览器操作

**使用示例**:
```
"检查 localhost:8080 页面的性能"
"为什么这个按钮点击没反应？"
"分析这个网页的加载速度"
```

---

### 3. 📁 Filesystem MCP

**包名**: `@modelcontextprotocol/server-filesystem`
**路径**: `c:\Users\flyskyson\Office_Agent_Workspace`
**功能**: 安全的文件系统访问

**能力**:
- ✅ 读取文件
- ✅ 写入文件
- ✅ 创建目录
- ✅ 搜索文件
- ✅ 批量文件操作

**安全限制**:
- 只能访问配置的目录（你的工作区）
- 不能访问系统文件

**使用示例**:
```
"读取工作区所有 Python 文件"
"在工作区创建测试目录"
"批量重命名文件"
```

---

### 4. 🐙 GitHub Repos Manager MCP

**包名**: `github-repos-manager-mcp`
**功能**: GitHub 仓库管理

**能力**:
- ✅ 查看仓库信息
- ✅ 管理 Issues
- ✅ 管理 Pull Requests
- ✅ 查看提交历史
- ✅ 仓库文件操作

**⚠️ 需要配置**:
使用前需要设置 GitHub Token：

1. 生成 GitHub Personal Access Token:
   - 访问: https://github.com/settings/tokens
   - 权限: repo (完整仓库访问权限)

2. 设置环境变量:
   ```bash
   # Windows PowerShell
   $env:GH_TOKEN = "你的GitHub Token"

   # 或添加到系统环境变量（永久）
   ```

3. 重启 Claude Code 使配置生效

**使用示例**:
```
"查看我的 GitHub 仓库列表"
"创建一个新的 Issue"
"查看最近的提交记录"
```

---

## 🚀 快速开始

### 使用 Playwright MCP

直接告诉我浏览器自动化需求:
```
"用 Playwright 打开这个网页并截图"
"自动填写表单并提交"
"测试登录功能是否正常"
```

### 使用 Chrome DevTools MCP

1. 在浏览器中打开网页
2. 告诉我:
   ```
   "用 Chrome DevTools 检查这个页面的错误"
   ```

### 使用 Filesystem MCP

直接告诉我文件操作需求:
```
"列出工作区所有 Markdown 文件"
"在工作区创建今天的学习日志"
```

### 使用 GitHub MCP

1. 先设置 `GH_TOKEN` 环境变量
2. 然后告诉我:
   ```
   "查看我的 GitHub 仓库状态"
   ```

---

## 🔧 配置文件

MCP 配置文件位置: `.mcp.json`

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "工作区路径"]
    },
    "github-repos-manager": {
      "command": "npx",
      "args": ["-y", "github-repos-manager-mcp"]
    }
  }
}
```

---

## 📚 其他可用的 MCP 服务器

根据 [awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) 列表，还有 300+ 个 MCP 服务器可用：

### 🔥 热门服务器

| 名称 | 功能 | 安装命令 |
|------|------|----------|
| **Docker** | 容器管理 | `npx @modelcontextprotocol/server-docker` |
| **Slack** | 消息发送 | `npx @modelcontextprotocol/server-slack` |
| **PostgreSQL** | 数据库操作 | `npx @modelcontextprotocol/server-postgres` |
| **Puppeteer** | 浏览器自动化 | `npx @modelcontextprotocol/server-puppeteer` |
| **Git** | 版本控制 | `npx mcp-server-git` |
| **Notion** | 笔记管理 | `npx notion-mcp-server` |

### 🎯 推荐安装

如果你需要其他 MCP 服务器，告诉我：
```
"我想安装 Slack MCP"
"我想连接 PostgreSQL 数据库"
```

我会帮你配置！

---

## 🐛 故障排除

### Chrome DevTools MCP 不工作?

**问题**: 无法连接到浏览器

**解决**:
1. 确保 Chrome 浏览器正在运行
2. 检查端口是否被占用
3. 重启 Claude Code

### Filesystem MCP 权限错误?

**问题**: 无法访问文件

**解决**:
1. 检查 `.mcp.json` 中的路径是否正确
2. 确保使用绝对路径
3. 检查文件权限

### GitHub MCP 提示缺少 Token?

**问题**: `GH_TOKEN environment variable is not set`

**解决**:
1. 生成 GitHub Token: https://github.com/settings/tokens
2. 设置环境变量:
   ```bash
   # PowerShell (临时)
   $env:GH_TOKEN = "ghp_xxxxxxxxxxxxxx"

   # CMD (临时)
   set GH_TOKEN=ghp_xxxxxxxxxxxxxx

   # 永久设置（系统环境变量）
   # Windows 设置 → 添加环境变量
   ```
3. 重启 Claude Code

---

## 📖 相关资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)
- [Chrome DevTools MCP 博客](https://developer.chrome.com/blog/chrome-devtools-mcp)

---

## 🎊 总结

你现在拥有 4 个强大的 MCP 服务器：

1. **Playwright** - 微软官方浏览器自动化（跨浏览器、测试、爬虫）
2. **Chrome DevTools** - 浏览器调试和性能分析
3. **Filesystem** - 文件系统操作
4. **GitHub** - 仓库管理（需配置 Token）

开始使用吧！🚀

---

**Sources**:
- [Awesome MCP Servers - GitHub](https://github.com/wong2/awesome-mcp-servers)
- [Microsoft Playwright MCP - GitHub](https://github.com/microsoft/playwright-mcp)
- [Chrome DevTools MCP - Chrome for Developers](https://developer.chrome.com/blog/chrome-devtools-mcp)
- [Top 7 MCP Servers Every Developer Needs in 2026](https://medium.com/@reactjsbd/the-top-7-mcp-servers-every-developer-needs-in-2026-d7d7e0a1b1da)
- [MCP Server Filesystem：AI工程师必备的本地交互深度指南](https://skywork.ai/skypage/zh/MCP-Server-Filesystem%EF%BC%9AAI%E5%B7%A5%E7%A8%8B%E5%B8%88%E5%BF%85%E5%A4%87%E7%9A%84%E6%9C%AC%E5%9C%B0%E4%BA%A4%E4%BA%92%E6%B7%B1%E5%BA%A6%E6%8C%87%E5%8D%97/1971090856160063488)
- [Playwright MCP完全指南：AI驱动的浏览器自动化工具【2025】](https://www.cursor-ide.com/blog/playwright-mcp-ai-tools-2025)
- [How to Install Microsoft Playwright MCP Server in VS Code?](https://medium.com/@testerstalk/how-to-install-microsoft-playwright-mcp-server-in-vs-code-9e65513e23e5)
