# VS Code 扩展版 Claude Code + DeepSeek API 配置指南

## 📋 配置概述

VS Code 扩展版的 Claude Code 通过两种方式配置 DeepSeek API：

1. **VS Code 用户设置** (`settings.json`) - 推荐方式
2. **Claude 配置文件** (`~/.claude/config.json`) - 备用方式

## ✅ 已完成的配置

### 1. Claude Code 配置文件

位置: `C:\Users\flyskyson\.claude\config.json`

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_DEEPSEEK_API_KEY_HERE"
  }
}
```

### 2. VS Code 用户设置

位置: `C:\Users\flyskyson\AppData\Roaming\Code\User\settings.json`

已添加以下环境变量配置：

```json
{
  "claudeCode.environmentVariables": [
    {
      "name": "ANTHROPIC_BASE_URL",
      "value": "https://api.deepseek.com/anthropic"
    },
    {
      "name": "ANTHROPIC_AUTH_TOKEN",
      "value": "YOUR_DEEPSEEK_API_KEY_HERE"
    },
    {
      "name": "ANTHROPIC_MODEL",
      "value": "deepseek-chat"
    },
    {
      "name": "ANTHROPIC_SMALL_FAST_MODEL",
      "value": "deepseek-chat"
    },
    {
      "name": "API_TIMEOUT_MS",
      "value": "600000"
    },
    {
      "name": "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC",
      "value": "1"
    }
  ],
  "claudeCode.disableLoginPrompt": true
}
```

## 🔑 配置 API 密钥

### 步骤 1: 获取 DeepSeek API 密钥

1. 访问 DeepSeek 平台: https://platform.deepseek.com/
2. 注册并登录账号
3. 在 **API Keys** 页面创建新密钥
4. 复制你的 API 密钥（格式类似 `sk-xxx...`）

### 步骤 2: 更新配置文件

你需要在**两个文件**中替换 `YOUR_DEEPSEEK_API_KEY_HERE`：

#### 方法 A: 通过 VS Code 界面（推荐）

1. 打开 VS Code
2. 按 `Ctrl + ,` 打开设置
3. 点击右上角的 **打开设置 (JSON)** 按钮
4. 找到 `ANTHROPIC_AUTH_TOKEN` 那一行
5. 将 `YOUR_DEEPSEEK_API_KEY_HERE` 替换为你的实际 API 密钥
6. 保存文件（`Ctrl + S`）

#### 方法 B: 直接编辑文件

**编辑 VS Code 设置:**
```bash
notepad "$APPDATA\Code\User\settings.json"
```

**编辑 Claude 配置:**
```bash
notepad ~/.claude/config.json
```

在两个文件中都将 `YOUR_DEEPSEEK_API_KEY_HERE` 替换为你的实际 API 密钥。

## 🚀 使用方法

### 启动 Claude Code

配置完成后，在 VS Code 中使用 Claude Code 扩展：

1. **方法 1：点击编辑器右上角的 ✱ 图标**
   - 在打开任何文件时，编辑器右上角会显示 Spark (✱) 图标
   - 点击即可打开 Claude Code 面板

2. **方法 2：使用命令面板**
   - 按 `Ctrl + Shift + P` 打开命令面板
   - 输入 "Claude Code"
   - 选择 "Claude Code: Open in Side Bar" 或其他选项

3. **方法 3：使用快捷键**
   - `Ctrl + Esc` - 聚焦到 Claude Code 输入框
   - `Ctrl + Shift + Esc` - 在新标签页打开 Claude Code

4. **方法 4：点击状态栏**
   - 点击 VS Code 底部状态栏右下角的 "✱ Claude Code"

### 验证配置

打开 Claude Code 面板后：

1. 如果配置正确，面板会直接显示对话输入框
2. 输入一个简单的问题测试，如 "你好"
3. 如果收到回复，说明配置成功！

如果出现错误：
- 检查 API 密钥是否正确
- 确保网络可以访问 DeepSeek API
- 重启 VS Code 后再试

## 🎯 常用功能

### 1. 斜杠命令

在 Claude Code 输入框中输入 `/` 可以看到所有可用命令：

- `/model` - 切换模型
- `/new` - 开始新对话
- `/files` - 管理文件引用
- `/help` - 查看帮助

### 2. @ 引用文件

- 输入 `@` 可以引用项目中的文件
- 选中代码后按 `Alt + K` 快速插入文件引用（包含行号）

### 3. 多对话管理

- `Ctrl + N` - 新建对话
- `Ctrl + Shift + Esc` - 在新标签页打开对话
- 点击面板上的箭头图标查看历史对话

### 4. 布局调整

可以拖动 Claude Code 面板到：
- **右侧边栏**（默认）
- **左侧边栏**
- **编辑器区域**（作为标签页）

## ⚙️ 高级设置

在 VS Code 设置中搜索 "Claude Code" 可以找到更多选项：

| 设置项 | 说明 |
|--------|------|
| **Selected Model** | 默认模型（可通过 `/model` 命令临时切换） |
| **Use Terminal** | 使用终端模式而非图形面板 |
| **Initial Permission Mode** | 权限模式（`default` 每次询问，`auto` 自动执行） |
| **Preferred Location** | 默认位置（sidebar 或 panel） |
| **Autosave** | 自动保存文件 |
| **Respect Git Ignore** | 遵守 .gitignore 规则 |

## 🔄 切换回官方 Claude API

如果想切换回使用 Anthropic 官方 API：

### 方法 1: 修改环境变量

在 VS Code 设置中将 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 改为：

```json
{
  "name": "ANTHROPIC_BASE_URL",
  "value": "https://api.anthropic.com/v1"
},
{
  "name": "ANTHROPIC_AUTH_TOKEN",
  "value": "你的_ANTHROPIC_API_KEY"
}
```

### 方法 2: 删除环境变量配置

删除 `claudeCode.environmentVariables` 整个配置块，然后：
- 将 `claudeCode.disableLoginPrompt` 设为 `false`
- 重启 VS Code 后登录 Anthropic 账号

## 📊 环境变量说明

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `ANTHROPIC_BASE_URL` | `https://api.deepseek.com/anthropic` | DeepSeek API 端点 |
| `ANTHROPIC_AUTH_TOKEN` | 你的 API 密钥 | DeepSeek 认证令牌 |
| `ANTHROPIC_MODEL` | `deepseek-chat` | 主模型 |
| `ANTHROPIC_SMALL_FAST_MODEL` | `deepseek-chat` | 快速模型 |
| `API_TIMEOUT_MS` | `600000` | 超时时间（10分钟） |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | `1` | 禁用非必要流量 |

## 🔒 安全提示

- ⚠️ **settings.json 包含敏感信息，不要分享或提交到 Git**
- ⚠️ 如果项目使用 Git，确保 `.vscode/settings.json` 在 `.gitignore` 中
- ⚠️ 定期轮换你的 API 密钥
- ⚠️ 不要在公共场合展示包含 API 密钥的配置

## 💡 故障排除

### 问题 1: Spark (✱) 图标不显示

**原因**: 需要打开一个文件才能看到图标

**解决方案**:
1. 打开任意项目文件
2. 或点击状态栏的 "✱ Claude Code"
3. 或使用命令面板 (`Ctrl + Shift + P`)

### 问题 2: Claude Code 没有响应

**检查步骤**:
1. 确认 API 密钥已正确配置
2. 检查网络连接
3. 查看 VS Code 输出面板的错误信息
4. 重启 VS Code

### 问题 3: 提示登录 Anthropic

**原因**: `disableLoginPrompt` 设置未生效

**解决方案**:
确保 settings.json 中有：
```json
"claudeCode.disableLoginPrompt": true
```

### 问题 4: 显示 API 错误

**常见原因**:
- API 密钥无效或过期
- DeepSeek 账户余额不足
- 网络无法访问 DeepSeek API

**解决方案**:
1. 检查 API 密钥是否正确
2. 登录 DeepSeek 平台检查账户状态
3. 测试网络连接: `curl https://api.deepseek.com/anthropic`

## 📂 配置文件位置汇总

| 文件 | 路径 |
|------|------|
| VS Code 用户设置 | `C:\Users\flyskyson\AppData\Roaming\Code\User\settings.json` |
| Claude 配置文件 | `C:\Users\flyskyson\.claude\config.json` |

## 🔧 推荐的 VS Code 扩展配置

```json
{
  "claudeCode.preferredLocation": "panel",
  "claudeCode.disableLoginPrompt": true,
  "claudeCode.autosave": true,
  "claudeCode.respectGitIgnore": true,
  "claudeCode.initialPermissionMode": "default"
}
```

## 📚 相关资源

- [DeepSeek API 文档](https://api-docs.deepseek.com/guides/anthropic_api)
- [Claude Code 官方文档](https://code.claude.com/docs/en/vs-code)
- [DeepSeek 平台](https://platform.deepseek.com/)

## ⏭️ 下一步

1. ✅ 获取 DeepSeek API 密钥
2. ✅ 在两个配置文件中更新密钥
3. ✅ 重启 VS Code
4. ✅ 打开 Claude Code 面板测试
5. ✅ 开始使用！

---

**配置完成时间**: 2026-01-11
**配置位置**: `c:\Users\flyskyson\Office_Agent_Workspace`
