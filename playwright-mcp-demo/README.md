# Playwright 自动化脚本示例

本项目包含多个实用的 Playwright 自动化脚本示例。

## 📦 安装

```bash
npm install
```

## 🌐 浏览器安装

首次使用需要安装浏览器(已配置国内镜像):

```bash
npx playwright install chromium
```

## 🚀 使用方法

### 1. 基础示例
```bash
npm run example
```
- 功能: 打开网页,获取标题和内容
- 文件: `example.js`

### 2. 网页截图
```bash
npm run screenshot
```
- 功能: 访问网站并截图
- 输出: `example-screenshot.png`
- 文件: `screenshot.js`

### 3. 数据抓取
```bash
npm run scrape
```
- 功能: 抓取 Bilibili 视频列表
- 输出: `bilibili-videos.json`
- 文件: `scrape-data.js`

### 4. 表单自动填写
```bash
npm run form
```
- 功能: 自动填写并提交表单
- 输出: `form-filled.png`
- 文件: `form-auto-fill.js`

## 🔧 配置说明

### 国内镜像
- npm 镜像: `https://registry.npmmirror.com`
- Playwright 浏览器镜像: `https://npmmirror.com/mirrors/playwright`

### MCP 配置
- 配置文件: `.vscode/mcp.json`
- 使用方法: 在 VSCode 中通过 Copilot Chat 启动

## 📝 脚本说明

### example.js
最基础的示例,演示如何:
- 启动浏览器
- 访问网页
- 获取页面信息
- 截图保存

### screenshot.js
网页全页截图工具,适用于:
- 网页存档
- 视觉验证
- 批量截图

### scrape-data.js
数据抓取示例,演示如何:
- 提取页面元素
- 获取链接和文本
- 保存 JSON 数据

### form-auto-fill.js
表单自动化示例,演示如何:
- 填写各种表单元素
- 选择下拉菜单
- 提交表单
- 验证结果

## 🎯 Playwright MCP 使用

1. 在 VSCode 中按 `Ctrl+Shift+P`
2. 输入 `Copilot Chat: Start MCP Server`
3. 选择 `playwright`
4. 在 Copilot Chat 中使用自然语言控制浏览器

示例指令:
```
使用 Playwright 打开 https://example.com 并告诉我页面标题
```

## 📚 学习资源

- [Playwright 官方文档](https://playwright.dev)
- [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)

## ⚠️ 注意事项

1. 首次运行需要下载 Chromium 浏览器(约 170MB)
2. 脚本默认使用 `headless: false` 模式,可以看到浏览器窗口
3. 修改 `headless: true` 可在后台运行
4. 确保网络连接正常

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!
