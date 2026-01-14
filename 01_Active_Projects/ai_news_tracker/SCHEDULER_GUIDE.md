# AI 新闻追踪器 - 自动运行配置指南

## 🎯 配置目标

设置 Windows 任务计划程序，每天自动运行 AI 新闻追踪器。

---

## 🚀 方法一：使用配置脚本（推荐）

### 步骤 1: 以管理员身份运行 PowerShell

右键点击 PowerShell 图标 → "以管理员身份运行"

### 步骤 2: 运行配置命令

```powershell
# 进入工作区目录
cd C:\Users\flyskyson\Office_Agent_Workspace

# 运行配置脚本
.\00_Agent_Library\99_Scripts_Tools\setup_scheduler.ps1
```

如果提示执行策略错误，先运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

---

## 🔧 方法二：手动创建任务

### 创建每日任务

```powershell
# 创建任务操作
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\Users\flyskyson\Office_Agent_Workspace\01_Active_Projects\ai_news_tracker\src\news_tracker.py"

# 创建触发器（每天 09:00）
$trigger = New-ScheduledTaskTrigger -Daily -At "09:00"

# 注册任务
Register-ScheduledTask -TaskName "AI_News_Daily" -Action $action -Trigger $trigger -Description "AI 新闻追踪器 - 每日运行"
```

### 创建每周任务

```powershell
# 创建触发器（每周一 09:00）
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "09:00"

# 注册任务
Register-ScheduledTask -TaskName "AI_News_Weekly" -Action $action -Trigger $trigger -Description "AI 新闻追踪器 - 周报"
```

---

## ✅ 验证任务是否创建成功

```powershell
# 查看已创建的任务
Get-ScheduledTask -TaskName "AI_News_Daily"
Get-ScheduledTask -TaskName "AI_News_Weekly"

# 或查看所有任务
schtasks /query | findstr "AI_News"
```

---

## 🧪 测试任务

```powershell
# 手动运行任务（测试）
Start-ScheduledTask -TaskName "AI_News_Daily"

# 查看任务历史
Get-ScheduledTaskInfo -TaskName "AI_News_Daily"
```

---

## 🗑️ 删除任务

```powershell
# 删除每日任务
Unregister-ScheduledTask -TaskName "AI_News_Daily" -Confirm:$false

# 删除每周任务
Unregister-ScheduledTask -TaskName "AI_News_Weekly" -Confirm:$false

# 或使用 schtasks
schtasks /delete /tn "AI_News_Daily" /f
schtasks /delete /tn "AI_News_Weekly" /f
```

---

## 📁 手动运行

如果不想配置自动任务，可以手动运行：

### 方式 1: 双击批处理文件
```
00_Agent_Library\99_Scripts_Tools\运行AI新闻追踪.bat
```

### 方式 2: 命令行
```bash
python 01_Active_Projects\ai_news_tracker\src\news_tracker.py
```

### 方式 3: 直接问我
```
- "获取今天的 AI 新闻"
- "运行新闻追踪器"
```

---

## 📊 配置状态

| 任务 | 频率 | 时间 | 状态 |
|------|------|------|------|
| AI_News_Daily | 每日 | 09:00 | ⏳ 待配置 |
| AI_News_Weekly | 每周一 | 09:00 | ⏳ 待配置 |

---

## 💡 提示

1. **首次配置**: 需要管理员权限
2. **修改时间**: 删除任务后重新创建
3. **查看日志**: 报告保存在 `data/daily_news_*.md`
4. **Python 路径**: 如果提示找不到 python，使用完整路径：
   ```
   C:\Users\flyskyson\AppData\Local\Programs\Python\Python312\python.exe
   ```

---

**文件位置**: `01_Active_Projects/ai_news_tracker/SCHEDULER_GUIDE.md`
