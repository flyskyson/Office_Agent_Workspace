# DeepSeek 模型接入 Claude Code 使用说明

## 已创建的配置文件

已为你创建了两个 DeepSeek 模型的配置文件:

- **`.claude/config-deepseek.json`** - DeepSeek Chat (通用对话,高性价比)
- **`.claude/config-deepseek-reasoner.json`** - DeepSeek Reasoner (强化推理能力)

## 📋 接入前准备

### 1. 获取 DeepSeek API Key

如果还没有 API Key,请访问 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册并获取。

### 2. 设置环境变量 (重要)

在 PowerShell 中设置环境变量:

**临时设置 (仅当前会话有效):**
```powershell
$env:DEEPSEEK_API_KEY="your-actual-api-key-here"
```

**永久设置 (推荐):**
```powershell
# 用户级别环境变量
[System.Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY', 'sk-8fbe6563bb9c46b7856aaa4d4781c497', [System.EnvironmentVariableTarget]::User)

# 系统级别环境变量 (需要管理员权限)
[System.Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY', 'your-actual-api-key-here', [System.EnvironmentVariableTarget]::Machine)
```

**验证环境变量:**
```powershell
$env:DEEPSEEK_API_KEY
```

## 🚀 切换到 DeepSeek 模型

### 方法一:使用 PowerShell 脚本 (推荐)

在项目根目录下运行:

```powershell
# 切换到 DeepSeek Chat (推荐日常使用)
.\switch-model.ps1 deepseek

# 切换到 DeepSeek Reasoner (复杂推理任务)
.\switch-model.ps1 deepseek-reasoner
```

### 方法二:手动复制配置文件

1. 打开 `.claude` 文件夹
2. 选择你想要的配置文件:
   - `config-deepseek.json`
   - `config-deepseek-reasoner.json`
3. 复制内容到 `.claude/settings.local.json`
4. 重启 VSCode 或重新加载 Claude Code 窗口

## 🔧 配置详情

### DeepSeek Chat (deepseek-chat)

```json
{
  "model": "deepseek-chat",
  "api": {
    "base_url": "https://api.deepseek.com/v1",
    "api_key_env_var": "DEEPSEEK_API_KEY"
  }
}
```

**特点:**
- 通用对话模型
- 高性能价格比
- 适合日常开发任务

### DeepSeek Reasoner (deepseek-reasoner)

```json
{
  "model": "deepseek-reasoner",
  "api": {
    "base_url": "https://api.deepseek.com/v1",
    "api_key_env_var": "DEEPSEEK_API_KEY"
  }
}
```

**特点:**
- 强化推理能力
- 适合复杂逻辑推理
- 适合架构设计和算法问题

## 📊 模型对比

| 模型 | 类型 | 优势 | 成本 | 适用场景 |
|------|------|------|------|----------|
| **DeepSeek Chat** | 通用对话 | 高性价比 | 💰 低 | 日常开发、代码编写、问题解答 |
| **DeepSeek Reasoner** | 强化推理 | 深度推理 | 💰💰 中 | 算法设计、复杂bug、架构决策 |
| **Claude Sonnet** | 平衡型 | 综合能力强 | 💰💰💰 高 | 复杂任务、多步骤操作 |
| **Claude Opus** | 顶级 | 最强能力 | 💰💰💰💰 最高 | 极具挑战性的任务 |

## ⚠️ 常见问题

### 1. 环境变量未生效

**症状:** 切换后无法使用 DeepSeek

**解决方案:**
```powershell
# 检查环境变量
$env:DEEPSEEK_API_KEY

# 如果为空,重新设置
$env:DEEPSEEK_API_KEY="your-api-key"

# 然后重新切换模型
.\switch-model.ps1 deepseek
```

### 2. API Key 无效

**症状:** 提示认证失败

**解决方案:**
- 检查 API Key 是否正确
- 确认 API Key 已激活
- 检查账户余额是否充足

### 3. 配置文件格式错误

**症状:** 切换脚本报错

**解决方案:**
```powershell
# 查看备份配置
Get-Content .claude\settings.backup.*.json

# 恢复备份
Copy-Item .claude\settings.backup.最新时间戳.json .claude\settings.local.json
```

## 💡 使用建议

### 日常开发工作流

```powershell
# 简单任务使用 DeepSeek Chat (省钱)
.\switch-model.ps1 deepseek

# 复杂推理使用 DeepSeek Reasoner
.\switch-model.ps1 deepseek-reasoner

# 需要最强能力时切换回 Claude
.\switch-model.ps1 sonnet  # 或 opus
```

### 成本优化策略

1. **简单问答** → DeepSeek Chat
2. **代码补全** → DeepSeek Chat
3. **文档编写** → DeepSeek Chat
4. **Bug 调试** → DeepSeek Reasoner
5. **架构设计** → Claude Sonnet/Opus
6. **复杂重构** → Claude Opus

## 🔗 相关链接

- [DeepSeek API 文档](https://api-docs.deepseek.com/zh-cn/)
- [DeepSeek 开放平台](https://platform.deepseek.com/)
- [模型定价](https://platform.deepseek.com/pricing)

## 📝 快速参考

```powershell
# 设置环境变量
$env:DEEPSEEK_API_KEY="sk-xxx"

# 切换到 DeepSeek Chat
.\switch-model.ps1 deepseek

# 切换到 DeepSeek Reasoner
.\switch-model.ps1 deepseek-reasoner

# 验证当前配置
Get-Content .claude\settings.local.json
```
