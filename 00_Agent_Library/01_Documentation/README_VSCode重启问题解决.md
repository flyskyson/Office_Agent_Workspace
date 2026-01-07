# DeepSeek 在 VSCode 重启后的环境变量问题

## 问题描述

每次重启 VSCode 后,DeepSeek API Key 环境变量不会自动加载到新的 PowerShell 会话中,导致无法使用 DeepSeek 模型。

## 原因

虽然 API Key 已永久保存到用户环境变量中,但 VSCode 的终端在启动时会创建新的 PowerShell 会话,这个新会话不会自动加载用户环境变量。

## 解决方案

我已经为你创建了以下解决方案:

### 方案一:VSCode 配置 (推荐) ✅

已创建 `.vscode/settings.json` 配置文件,自动在每次启动 PowerShell 终端时加载 API Key。

**优点:**
- 完全自动化
- 每次打开终端都自动加载
- 无需手动操作

**使用方法:**
正常启动 VSCode 即可,无需额外操作。

### 方案二:专用启动脚本

使用 `start-vscode-with-deepseek.bat` 启动 VSCode:

```cmd
start-vscode-with-deepseek.bat
```

**优点:**
- 确保环境变量在启动时加载
- 可以看到加载确认信息

### 方案三:手动加载 (备用)

如果上述方案失败,可以在 VSCode 终端中手动运行:

```powershell
# 加载 API Key 到当前会话
$env:DEEPSEEK_API_KEY = [System.Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', [System.EnvironmentVariableTarget]::User)

# 验证
$env:DEEPSEEK_API_KEY
```

## 验证配置

在任何时候,你可以运行验证脚本检查配置:

```powershell
.\check-deepseek.ps1
```

## 快速修复脚本

如果 DeepSeek 无法工作,运行修复脚本:

```powershell
.\fix-deepseek.ps1
```

该脚本会:
1. 验证永久 API Key
2. 加载到当前会话
3. 验证配置文件
4. 测试 API 连接

## 测试方法

重新加载 VSCode 窗口后,输入:

```
你好,请用一句话介绍你自己
```

如果收到 DeepSeek 的回复,说明配置成功!

## 文件清单

- `.vscode/settings.json` - VSCode 终端配置(自动加载 API Key)
- `.claude/load-env.ps1` - 环境变量加载脚本
- `start-vscode-with-deepseek.bat` - VSCode 启动脚本
- `check-deepseek.ps1` - 配置验证脚本
- `fix-deepseek.ps1` - 配置修复脚本

## 故障排除

### 问题: 重启后仍然无法使用 DeepSeek

**解决步骤:**

1. 运行验证脚本:
   ```powershell
   .\check-deepseek.ps1
   ```

2. 如果显示 "[WARN] API Key not loaded",运行修复脚本:
   ```powershell
   .\fix-deepseek.ps1
   ```

3. 重新加载 VSCode 窗口:
   - 按 `Ctrl+Shift+P`
   - 输入 "Developer: Reload Window"
   - 按回车

### 问题: 终端显示权限错误

**解决方案:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题: API Key 失效

**解决方案:**
1. 访问 https://platform.deepseek.com/
2. 检查账户余额
3. 重新获取 API Key
4. 更新环境变量:
   ```powershell
   [System.Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY', 'new-key-here', [System.EnvironmentVariableTarget]::User)
   ```

## 总结

现在你有多种方案确保 VSCode 重启后 DeepSeek 仍能正常工作:

1. ✅ **自动方案** (推荐) - .vscode/settings.json 已配置
2. ✅ **启动脚本** - start-vscode-with-deepseek.bat
3. ✅ **手动加载** - PowerShell 命令
4. ✅ **修复工具** - fix-deepseek.ps1

选择最适合你的方式即可!
