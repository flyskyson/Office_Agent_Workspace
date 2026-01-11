# Claude Code + DeepSeek API 配置指南

## 📋 已完成的配置

已为你创建以下配置文件：

1. **~/.claude-deepseek-env** - DeepSeek API 环境变量配置
2. **~/.bashrc** - Bash 别名配置
3. **~/.bash_profile** - 自动加载 .bashrc（Git Bash 自动创建）

## 🔑 重要：配置你的 API 密钥

在使用前，你需要**设置你的 DeepSeek API 密钥**：

### 步骤 1: 获取 DeepSeek API 密钥

1. 访问 DeepSeek 平台: https://platform.deepseek.com/
2. 注册并登录账号
3. 在 API Keys 页面创建新的 API 密钥
4. 复制你的 API 密钥

### 步骤 2: 更新配置文件

编辑 `~/.claude-deepseek-env` 文件，将 `YOUR_DEEPSEEK_API_KEY_HERE` 替换为你的实际 API 密钥：

```bash
# 方法 1: 使用文本编辑器
notepad ~/.claude-deepseek-env

# 方法 2: 使用 sed 命令直接替换（推荐）
sed -i 's/YOUR_DEEPSEEK_API_KEY_HERE/你的实际API密钥/' ~/.claude-deepseek-env
```

## 🚀 使用方法

### 方法一：使用便捷别名（推荐）

```bash
# 启动使用 DeepSeek 模型的 Claude Code
claude-deepseek

# 仅加载 DeepSeek 环境变量（不启动 claude）
load-deepseek
```

### 方法二：手动加载环境变量

```bash
# 加载 DeepSeek 配置
source ~/.claude-deepseek-env

# 启动 Claude Code
claude
```

### 方法三：临时使用（一次性）

```bash
# 直接在命令行设置环境变量
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="你的API密钥"
export ANTHROPIC_MODEL="deepseek-chat"
claude
```

## 📝 配置详解

### 环境变量说明

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `ANTHROPIC_BASE_URL` | `https://api.deepseek.com/anthropic` | DeepSeek API 端点 |
| `ANTHROPIC_AUTH_TOKEN` | 你的 API 密钥 | DeepSeek API 认证令牌 |
| `API_TIMEOUT_MS` | `600000` | 超时时间（10分钟） |
| `ANTHROPIC_MODEL` | `deepseek-chat` | 主模型 |
| `ANTHROPIC_SMALL_FAST_MODEL` | `deepseek-chat` | 快速模型 |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | `1` | 禁用非必要流量 |

## ✅ 测试配置

运行以下命令测试配置是否正确：

```bash
# 1. 加载配置
source ~/.claude-deepseek-env

# 2. 检查环境变量
echo "Base URL: $ANTHROPIC_BASE_URL"
echo "Model: $ANTHROPIC_MODEL"

# 3. 测试 API 连接（需要先配置 API 密钥）
claude-deepseek
```

## 🔄 切换回 Anthropic Claude

如果你想切换回使用官方的 Anthropic Claude API：

```bash
# 取消 DeepSeek 环境变量
unset ANTHROPIC_BASE_URL
unset ANTHROPIC_AUTH_TOKEN
unset ANTHROPIC_MODEL
unset ANTHROPIC_SMALL_FAST_MODEL
unset CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC

# 然后正常使用 claude 命令
claude
```

或者**重启终端**，环境变量会自动清除。

## 💡 常见问题

### Q: 如何确认正在使用 DeepSeek 模型？

A: 加载配置后，终端会显示：
```
✓ DeepSeek API 配置已加载
  Base URL: https://api.deepseek.com/anthropic
  Model: deepseek-chat
```

### Q: 配置会影响其他终端窗口吗？

A: 不会。环境变量只在当前终端会话中有效。每次新开终端需要重新运行 `claude-deepseek` 或 `source ~/.claude-deepseek-env`。

### Q: 如何让配置自动加载？

A: 在 `~/.bashrc` 文件末尾添加：
```bash
# 自动加载 DeepSeek 配置（可选）
source ~/.claude-deepseek-env
```

**注意**：这会让每次打开终端都自动使用 DeepSeek，可能不是你想要的。

### Q: 如何在项目中使用？

A: 在项目目录中创建 `.env` 文件：
```bash
ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
ANTHROPIC_AUTH_TOKEN=你的API密钥
ANTHROPIC_MODEL=deepseek-chat
```

## 📚 参考资源

- [DeepSeek API 文档](https://api-docs.deepseek.com/guides/anthropic_api)
- [DeepSeek 平台](https://platform.deepseek.com/)
- [Claude Code 文档](https://docs.anthropic.com/claude/docs)

## 🔒 安全提示

- ⚠️ **不要将包含 API 密钥的文件提交到 Git**
- ⚠️ **不要在公共场合分享你的 API 密钥**
- ⚠️ **定期轮换你的 API 密钥**
- ⚠️ **设置适当的文件权限**: `chmod 600 ~/.claude-deepseek-env`

## ⏭️ 下一步

1. ✅ 获取 DeepSeek API 密钥
2. ✅ 更新 `~/.claude-deepseek-env` 文件中的密钥
3. ✅ 运行 `claude-deepseek` 测试
4. ✅ 开始使用！

---

**配置完成时间**: 2026-01-11
**配置位置**: `c:\Users\flyskyson\Office_Agent_Workspace`
