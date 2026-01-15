# MCP 服务器配置日志

**更新时间**: 2026-01-14
**配置文件**: [.mcp.json](../../.mcp.json)

---

## 📡 当前已配置的 MCP 服务器

### 1. 🎭 Playwright MCP
- **包名**: `@playwright/mcp@latest`
- **开发商**: Microsoft
- **状态**: ✅ 活跃
- **配置日期**: 2026-01-14
- **功能**: 浏览器自动化、跨浏览器测试、网页截图

### 2. 🌐 Chrome DevTools MCP
- **包名**: `chrome-devtools-mcp@latest`
- **开发商**: Google
- **状态**: ✅ 已恢复 (2026-01-14)
- **功能**: 浏览器调试、性能分析、网络监控

### 3. 📁 Filesystem MCP
- **包名**: `@modelcontextprotocol/server-filesystem`
- **权限范围**: `c:\Users\flyskyson\Office_Agent_Workspace`
- **状态**: ✅ 活跃
- **功能**: 文件系统操作

---

## 📜 配置历史

| 日期 | 操作 | 服务器 | 说明 |
|------|------|--------|------|
| 2026-01-14 | ✅ 恢复 | chrome-devtools-mcp | 从历史配置恢复 |
| 2026-01-XX | ✅ 添加 | playwright-mcp | 微软官方 Playwright |
| 2026-01-XX | ✅ 添加 | filesystem-mcp | 文件系统访问 |

---

## 🔧 配置文件内容

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "c:\\Users\\flyskyson\\Office_Agent_Workspace"
      ]
    },
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp@latest"
      ]
    },
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@latest"
      ]
    }
  }
}
```

---

## 📚 相关文档

- [MCP服务器使用指南](../../04_Data_&_Resources/Learning_Materials/MCP服务器使用指南.md)
- [Chrome DevTools 指南](../../00_Agent_Library/CHROME_DEVTOOLS_GUIDE.md)
- [Chrome MCP Demo](../../00_Agent_Library/CHROME_MCP_DEMO.md)

---

## 💡 备注

- Chrome DevTools MCP 曾在早期版本中配置，后被移除，现已恢复
- 所有 MCP 服务器使用 `npx -y` 自动安装最新版本
- 重启 Claude Code 后生效
