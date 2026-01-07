# Claude Code 模型切换使用说明

## 已创建的配置文件

已为你创建了三个模型的配置文件:

- **`.claude/config-sonnet.json`** - Sonnet 4.5 (平衡性能,推荐日常使用)
- **`.claude/config-haiku.json`** - Haiku 4.5 (快速响应,适合简单任务)
- **`.claude/config-opus.json`** - Opus 4.5 (最强性能,适合复杂任务)

## 切换模型的方法

### 方法一:使用 PowerShell 脚本 (推荐)

在项目根目录下运行:

```powershell
# 切换到 Sonnet 4.5 (平衡)
.\switch-model.ps1 sonnet

# 切换到 Haiku 4.5 (快速)
.\switch-model.ps1 haiku

# 切换到 Opus 4.5 (最强)
.\switch-model.ps1 opus
```

脚本会自动:
1. 备份当前配置(带时间戳)
2. 应用新模型配置
3. 显示切换结果

### 方法二:手动切换配置文件

1. 打开 `.claude` 文件夹
2. 选择你想要的配置文件(如 `config-sonnet.json`)
3. 复制其内容到 `.claude/settings.local.json`
4. 重启 VSCode 或重新加载 Claude Code 窗口

### 方法三:直接修改 settings.local.json

打开 [`.claude/settings.local.json`](.claude/settings.local.json),修改 `"model"` 字段:

```json
{
  "model": "claude-sonnet-4-5-20250929",  // Sonnet 4.5
  "model": "claude-haiku-4-5-20250929",   // Haiku 4.5
  "model": "claude-opus-4-5-20251101"     // Opus 4.5
}
```

## 模型特性对比

| 模型 | 速度 | 成本 | 适用场景 |
|------|------|------|----------|
| **Haiku 4.5** | ⚡⚡⚡ 最快 | 💰 最低 | 简单问答、代码补全、快速迭代 |
| **Sonnet 4.5** | ⚡⚡ 中等 | 💰💰 中等 | 日常开发、复杂任务、平衡选择 |
| **Opus 4.5** | ⚡ 较慢 | 💰💰💰 最高 | 复杂推理、架构设计、困难bug |

## 注意事项

1. **需要重启**: 切换配置后需要重启 VSCode 或重新加载 Claude Code 窗口才能生效
2. **自动备份**: 使用切换脚本会自动备份当前配置,可以在 `.claude` 文件夹找到备份文件
3. **权限继承**: 所有配置文件都继承了你当前的权限设置

## 查看当前使用的模型

在 Claude Code 对话中输入:
```
你使用的是什么模型?
```

或者在 VSCode 中查看当前活动模型的信息。

## 快速切换示例

```powershell
# 日常开发使用 Sonnet (推荐)
.\switch-model.ps1 sonnet

# 遇到简单任务需要快速响应时切换到 Haiku
.\switch-model.ps1 haiku

# 遇到复杂问题需要最强推理时切换到 Opus
.\switch-model.ps1 opus
```
