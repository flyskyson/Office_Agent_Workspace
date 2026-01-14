# Chrome DevTools MCP 使用指南

## 📋 概述

Chrome DevTools MCP 是 Chrome 官方和 Anthropic 合作开发的 **Model Context Protocol (MCP)** 服务器，允许 Claude Code 直接接管和控制 Chrome 浏览器。

## ✅ 配置状态

| 项目 | 状态 |
|------|------|
| ✅ MCP 配置文件 | `.mcp.json` 已配置 |
| ✅ 启动脚本 | `00_Agent_Library/99_Scripts_Tools/启动Chrome调试模式.bat` |
| ✅ Chrome DevTools 权限 | 已允许 |
| ⚠️ Chrome 远程调试 | 需要手动启动 |

---

## 🚀 使用步骤

### 1️⃣ 启动 Chrome 调试模式

**方式 A: 使用启动脚本（推荐）**
```bash
# 双击运行
00_Agent_Library\99_Scripts_Tools\启动Chrome调试模式.bat
```

**方式 B: 手动启动**
```bash
# 关闭所有 Chrome 窗口
taskkill /F /IM chrome.exe

# 启动 Chrome（调试端口 9222）
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

### 2️⃣ 验证连接

启动 Chrome 后，在浏览器中访问：
```
http://localhost:9222/json
```

应该看到 JSON 格式的页面信息。

### 3️⃣ 在 Claude Code 中使用

**查看可用的 MCP 服务器：**
```
/mcp
```

**可用工具列表：**
- `mcp__chrome-devtools__navigate_page` - 导航到 URL
- `mcp__chrome-devtools__take_snapshot` - 获取页面快照
- `mcp__chrome-devtools__click` - 点击元素
- `mcp__chrome-devtools__fill` - 填充表单
- `mcp__chrome-devtools__evaluate_script` - 执行 JavaScript
- `mcp__chrome-devtools__take_screenshot` - 截图
- `mcp__chrome-devtools__list_pages` - 列出打开的页面
- `mcp__chrome-devtools__list_console_messages` - 查看控制台消息
- `mcp__chrome-devtools__list_network_requests` - 查看网络请求
- `mcp__chrome-devtools__performance_start_trace` - 性能追踪
- 更多...

---

## 💡 使用示例

### 示例 1: 访问网站并截图
```
你: 帮我访问百度首页并截图

Claude 会：
1. mcp__chrome-devtools__new_page(url="https://www.baidu.com")
2. mcp__chrome-devtools__take_screenshot()
```

### 示例 2: 自动填写表单
```
你: 用浏览器打开这个网址并填写表单

Claude 会：
1. 导航到指定 URL
2. take_snapshot() 获取页面结构
3. 找到表单字段
4. fill() 填充数据
5. click() 提交
```

### 示例 3: 调试 Web 应用
```
你: 检查我的 Flask 应用有什么错误

Claude 会：
1. 访问 http://127.0.0.1:5000
2. list_console_messages() 查看控制台错误
3. list_network_requests() 检查失败的请求
4. 分析并提供解决方案
```

### 示例 4: 性能分析
```
你: 分析淘宝首页的性能

Claude 会：
1. performance_start_trace(reload=true, autoStop=true)
2. 等待追踪完成
3. 分析 Core Web Vitals (LCP, FID, CLS)
4. 提供优化建议
```

---

## 🛠️ 项目应用场景

### 市场监管智能体
- 自动登录政府网站
- 填写申请表单
- 查询企业信息

### 广西政务登录
- 替代 Playwright
- 更稳定的自动化
- 实时调试能力

### Web UI 测试
- 测试 Flask 应用
- 测试 Streamlit 界面
- 自动化回归测试

---

## 📚 相关资源

| 资源 | 链接 |
|------|------|
| **Claude Code 官方文档** | [code.claude.com/docs/en/chrome](https://code.claude.com/docs/en/chrome) |
| **Chrome 官方 GitHub** | [github.com/ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) |
| **Chrome 开发者博客** | [developer.chrome.com/blog/chrome-devtools-mcp](https://developer.chrome.com/blog/chrome-devtools-mcp) |
| **NPM 包** | [@chromecommand/chrome-devtools-mcp](https://www.npmjs.com/package/@chromecommand/chrome-devtools-mcp) |

---

## ⚠️ 注意事项

1. **端口冲突**: 确保 9222 端口未被占用
2. **Chrome 版本**: 建议使用最新版 Chrome
3. **权限**: MCP 服务器已在 `.mcp.json` 中配置
4. **调试**: 如果无法连接，检查 Chrome 是否以调试模式启动

---

## 🔄 与 Playwright 的对比

| 特性 | Chrome DevTools MCP | Playwright MCP |
|------|---------------------|----------------|
| **调试能力** | ⭐⭐⭐⭐⭐ 原生 DevTools | ⭐⭐⭐ 基础 |
| **性能分析** | ⭐⭐⭐⭐⭐ Core Web Vitals | ⭐⭐ 有限 |
| **网络调试** | ⭐⭐⭐⭐⭐ 详细请求信息 | ⭐⭐⭐ 基础 |
| **跨浏览器** | ❌ 仅 Chrome | ✅ Chrome/Firefox/WebKit |
| **速度** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **易用性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**建议**: 两者都保留，根据场景选择：
- **调试/分析** → Chrome DevTools MCP
- **跨浏览器测试** → Playwright MCP
- **爬虫/自动化** → 两者皆可

---

**创建时间**: 2026-01-14
**版本**: 1.0
**维护者**: Office Agent Workspace
