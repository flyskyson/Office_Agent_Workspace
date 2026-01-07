# Playwright 安装指南

## ✅ 已完成的配置

### 1. npm 镜像配置
- ✅ 全局 npm 镜像: `https://registry.npmmirror.com`
- ✅ 项目镜像: `.npmrc` 已配置

### 2. Playwright 浏览器镜像
- ✅ 用户环境变量: `PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright`

### 3. 已安装的包
- ✅ playwright: v1.57.0
- ✅ @playwright/test: v1.57.0

## 🔄 当前状态

### 正在下载 Chromium 浏览器
- **文件大小**: ~170MB
- **镜像源**: https://npmmirror.com/mirrors/playwright (国内)
- **状态**: 🔄 下载中...

### 等待下载完成

下载完成后,你将看到类似这样的输出:
```
Chromium 143.0.7499.4 downloaded to C:\Users\flyskyson\AppData\Local\ms-playwright\chromium-1200
```

## 🚀 下载完成后如何使用

### 方法 1: 运行测试脚本

```bash
# 进入项目目录
cd playwright-mcp-demo

# 运行基础示例
npm run example

# 或运行其他脚本
npm run screenshot
npm run scrape
npm run form
```

### 方法 2: 使用 Playwright MCP

1. 在 VSCode 中打开 [mcp.json](.vscode/mcp.json)
2. 按 `Ctrl+Shift+P` 打开命令面板
3. 输入 `Copilot Chat: Start MCP Server`
4. 选择 `playwright` 并启动
5. 在 Copilot Chat 的 Agent 模式下使用自然语言

示例指令:
```
使用 Playwright 打开 https://example.com 并告诉我页面标题
```

## 📊 可用的脚本

| 脚本文件 | 功能 | 运行命令 |
|---------|------|---------|
| example.js | 基础示例 | `npm run example` |
| screenshot.js | 网页截图 | `npm run screenshot` |
| scrape-data.js | 数据抓取 | `npm run scrape` |
| form-auto-fill.js | 表单填写 | `npm run form` |
| test-simple.js | 简单测试 | `node test-simple.js` |
| test-headless.js | 无头模式 | `node test-headless.js` |

## ⏱️ 预计下载时间

根据网络速度:
- 🟢 快速网络 (>10MB/s): ~20 秒
- 🟡 普通网络 (2-10MB/s): ~1-2 分钟
- 🔴 较慢网络 (<2MB/s): ~3-5 分钟

## 🛠️ 手动检查下载进度

### 方式 1: 检查目录
```powershell
dir C:\Users\flyskyson\AppData\Local\ms-playwright
```

### 方式 2: 检查网络活动
打开任务管理器查看网络使用情况

### 方式 3: 查看临时文件
```powershell
dir C:\Users\flyskyson\AppData\Local\Temp\playwright* /s
```

## ❓ 常见问题

### Q: 下载失败怎么办?
A: 重新运行安装命令:
```bash
cd playwright-mcp-demo
npx playwright install chromium
```

### Q: 想取消下载?
A: 按 `Ctrl+C` 终止进程

### Q: 如何验证安装成功?
A: 运行测试脚本:
```bash
npm run example
```

### Q: 可以使用其他浏览器吗?
A: 可以!安装其他浏览器:
```bash
npx playwright install firefox  # Firefox
npx playwright install webkit   # WebKit (Safari)
```

## 📚 下一步

下载完成后:
1. ✅ 运行示例脚本测试
2. ✅ 查看 [README.md](README.md) 了解详细用法
3. ✅ 配置 Playwright MCP
4. ✅ 开始编写自己的自动化脚本

## 🎯 快速命令参考

```bash
# 安装浏览器
npx playwright install chromium

# 查看已安装的浏览器
npx playwright show-browsers

# 运行所有示例
npm run example
npm run screenshot
npm run scrape
npm run form

# 开发模式
npx playwright codegen https://example.com  # 录制脚本
```

---

**提示**: 下载过程使用国内镜像,速度会很快。请耐心等待几分钟! 🚀
