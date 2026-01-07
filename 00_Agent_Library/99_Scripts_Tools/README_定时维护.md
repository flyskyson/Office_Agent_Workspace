# 工作区自动化维护设置指南

## 📋 已创建的文件

1. **[setup_scheduled_maintenance.ps1](../../setup_scheduled_maintenance.ps1)** - 计划任务设置脚本
2. **[run_maintenance.bat](../../run_maintenance.bat)** - 快速手动维护批处理文件

---

## 🚀 设置方法

### 方法一：使用设置脚本（推荐）

1. **右键点击** `setup_scheduled_maintenance.ps1`
2. **选择** "以管理员身份运行 PowerShell"
3. **如果提示权限**，输入 `Y` 自动提权
4. **完成** - 任务已创建

### 方法二：手动设置

1. 按 `Win + R`，输入 `taskschd.msc` 打开任务计划程序
2. 点击 "创建任务"
3. 设置：
   - **名称**: `Office_Workspace_Weekly_Maintenance`
   - **触发器**: 每周日凌晨 2:00
   - **操作**: 运行 `python workspace_maintenance.py --health-report`
   - **起始位置**: 你的工作区路径
   - **用户**: SYSTEM

---

## 📅 定时任务说明

### 默认配置
- **执行频率**: 每周一次
- **执行时间**: 周日凌晨 2:00
- **权限级别**: SYSTEM（最高权限）
- **任务内容**:
  - 清理 Python 缓存
  - 检查不活跃项目
  - 检查磁盘空间
  - 查找大文件
  - 生成详细健康报告

### 自定义时间
如需修改执行时间，编辑 `setup_scheduled_maintenance.ps1` 第 60 行：
```powershell
# 修改为其他时间，如每周五晚 10 点
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At 10pm
```

---

## 🛠️ 使用工具

### 手动运行维护
#### 方式 1：双击批处理文件
双击 [run_maintenance.bat](../../run_maintenance.bat)

#### 方式 2：命令行
```bash
# 基础维护
python workspace_maintenance.py

# 完整维护（含健康报告）
python workspace_maintenance.py --health-report
```

#### 方式 3：任务计划程序
1. 打开 `taskschd.msc`
2. 找到 `Office_Workspace_Weekly_Maintenance`
3. 右键 → "运行"

---

## 🔧 管理计划任务

### 打开任务计划程序
```powershell
taskschd.msc
```

### PowerShell 命令
```powershell
# 查看任务
Get-ScheduledTask -TaskName "Office_Workspace_Weekly_Maintenance"

# 立即运行
Start-ScheduledTask -TaskName "Office_Workspace_Weekly_Maintenance"

# 禁用任务
Disable-ScheduledTask -TaskName "Office_Workspace_Weekly_Maintenance"

# 启用任务
Enable-ScheduledTask -TaskName "Office_Workspace_Weekly_Maintenance"

# 删除任务
Unregister-ScheduledTask -TaskName "Office_Workspace_Weekly_Maintenance" -Confirm:$false

# 查看任务历史
Get-ScheduledTaskInfo -TaskName "Office_Workspace_Weekly_Maintenance"
```

---

## 📊 维护报告

每次运行后会生成报告：
- **基础维护**: `维护报告_YYYYMMDD_HHMMSS.md`
- **完整维护**:
  - `维护报告_YYYYMMDD_HHMMSS.md`
  - `工作区健康报告_YYYYMMDD_HHMMSS.md`

报告保存在工作区根目录。

---

## 💡 最佳实践

1. **每周检查**: 查看维护报告，了解工作区状态
2. **每月健康检查**: 运行 `workspace_report.py` 获取详细分析
3. **需要时清理**: 如果缓存堆积，运行 `workspace_cleaner.py --execute`
4. **项目归档**: 将不活跃项目移到 `02_Project_Archive/`

---

## ❓ 常见问题

### Q: 任务没有运行？
A: 检查任务计划程序中的历史记录，确认：
- 计算机是否在设定时间开机
- Python 路径是否正确
- 工作区路径是否存在

### Q: 如何修改执行频率？
A: 编辑 `setup_scheduled_maintenance.ps1` 第 60 行，重新运行脚本

### Q: 想每天运行？
A: 将第 60 行改为：
```powershell
$Trigger = New-ScheduledTaskTrigger -Daily -At 2am
```

### Q: 不想使用计划任务？
A: 直接双击 `run_maintenance.bat` 手动运行

---

## 🎯 总结

现在你有三种维护方式：

| 方式 | 适用场景 | 操作 |
|------|----------|------|
| **自动定时** | 设置后无需操心 | 运行 `setup_scheduled_maintenance.ps1` |
| **手动批处理** | 需要时快速运行 | 双击 `run_maintenance.bat` |
| **命令行** | 灵活控制 | `python workspace_maintenance.py` |

---

**提示**: 第一次运行建议手动执行，确认无问题后再设置自动化。
