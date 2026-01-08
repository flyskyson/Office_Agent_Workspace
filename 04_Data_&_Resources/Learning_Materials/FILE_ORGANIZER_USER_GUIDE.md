# 每日文件整理器 - 使用指南

> **智能混合模式：按项目分类 + 按文件类型细分**

作者：Office Agent Workspace
创建日期：2026-01-08
最后更新：2026-01-08

---

## 🎯 为什么需要这个工具？

**问题**：每天工作都会产生大量文件散落在工作区根目录：
- 报告文件（健康报告、清理报告、维护报告...）
- 临时脚本（test_*.py, demo_*.html）
- 文档资料（各种指南、README）
- 这些文件堆积如山，难以管理！

**解决方案**：智能文件整理器自动帮你：
1. **分类文件**：按规则自动识别文件类型
2. **归档整理**：移动到正确的目录
3. **保留核心**：重要文件保留在根目录
4. **生成报告**：记录每次整理的详细信息

---

## 🚀 快速开始

### 方式1：使用菜单（最简单）

双击运行：
```
run_organizer.bat
```

然后选择：
- 选项1：模拟运行（安全查看效果）
- 选项2：执行整理

### 方式2：命令行运行

**模拟运行（推荐先试这个）**：
```bash
python daily_file_organizer.py --dry-run
```

**执行实际整理**：
```bash
python daily_file_organizer.py
```

---

## 📁 文件分类规则

### 📍 保留在根目录（核心文件）

这些文件**不会移动**，因为常用且重要：

| 文件类型 | 示例 |
|---------|------|
| 快速启动脚本 | `start_new_session.bat`, `butler_mode.bat` |
| 核心工具 | `workspace_*.py`, `daily_launcher.py` |
| 配置文件 | `.gitignore`, `.mcp.json`, `README.md` |

### 📂 自动归档的文件

| 分类 | 规则 | 目标位置 |
|------|------|----------|
| **报告文件** | `*报告*.md` | `05_Outputs/Reports/日期/` |
| **脚本工具** | `*.bat`, `*.ps1` | `00_Agent_Library/99_Scripts_Tools/` |
| **学习资料** | `*指南*.md`, `*说明*.md` | `04_Data_&_Resources/Learning_Materials/` |
| **测试文件** | `test_*.*`, `*_test.*` | `00_Temp/Tests/日期/` |
| **临时文件** | `*.tmp`, `*.cache` | `00_Temp/日期/` |

---

## 💡 使用场景

### 场景1：每天下班前整理

```bash
# 1. 下班前运行一次
python daily_file_organizer.py

# 2. 查看报告
# 报告自动保存在 05_Outputs/Reports/
```

### 场景2：定期自动整理

创建Windows计划任务，每天自动运行（见下文"定时任务设置"）

### 场景3：查看整理历史

```bash
# 方式1：使用菜单
run_organizer.bat
# 选择"查看最近的整理报告"

# 方式2：直接打开报告目录
# 05_Outputs/Reports/
```

---

## ⚙️ 高级用法

### 自定义整理规则

编辑 `daily_file_organizer.py` 文件中的 `rules` 字典：

```python
self.rules = {
    'keep_in_root': [
        r'^your_file\.ext$',  # 添加要保留的文件
    ],

    'custom_category': {
        'pattern': [r'your_pattern.*\.ext$'],
        'target': 'your/target/path/',
        'description': '你的自定义分类'
    },
}
```

### 整理其他目录

```bash
python daily_file_organizer.py --workspace "D:\MyOtherWorkspace"
```

### 模拟运行（预览效果）

```bash
python daily_file_organizer.py --dry-run
```

**优点**：
- ✅ 不会实际移动文件
- ✅ 查看哪些文件会被分类
- ✅ 确认规则是否正确

---

## 📅 设置定时任务（自动运行）

### 方法1：使用PowerShell脚本（推荐）

运行已有的定时任务设置脚本：
```bash
setup_scheduled_maintenance.bat
```

然后修改计划任务，添加 `daily_file_organizer.py`

### 方法2：手动创建计划任务

1. 打开"任务计划程序"（Win + R 输入 `taskschd.msc`）
2. 创建基本任务
3. 触发器：每天运行（建议下班时间，如18:00）
4. 操作：启动程序
   - 程序：`python`
   - 参数：`daily_file_organizer.py`
   - 起始于：`C:\Users\flyskyson\Office_Agent_Workspace`

---

## 📊 整理报告说明

每次整理后会生成报告：
```
05_Outputs/Reports/file_organize_report_20260108.md
```

**报告内容**：
- 整理时间
- 统计信息（移动了多少文件）
- 文件移动详情（原位置 → 新位置）
- 错误日志（如果有）

---

## ⚠️ 注意事项

### ❌ 不要移动的文件

如果你不想移动某个重要文件：

**方法1：添加到保留规则**
```python
'keep_in_root': [
    r'^important_file\.txt$',  # 添加这一行
]
```

**方法2：移动到项目目录**
- 把文件放到 `01_Active_Projects/你的项目/` 下
- 整理器只处理根目录的文件

### 🔒 安全性

- ✅ 默认模拟运行模式，不会误操作
- ✅ 生成详细报告，可追溯
- ✅ 只处理根目录，不影响项目目录
- ⚠️ 建议先 `--dry-run` 查看效果

### 💾 备份建议

虽然整理器很安全，但重要文件建议：
1. 定期备份整个工作区
2. 使用Git版本控制
3. 检查整理报告确认无误

---

## 🎓 自定义规则示例

### 示例1：保留所有项目配置文件

```python
'keep_in_root': [
    r'^.*_config\.yaml$',
    r'^.*_config\.json$',
    r'^settings\.py$',
]
```

### 示例2：按项目分类

```python
'project_files': {
    'pattern': [r'^projectA_.*\..*'],
    'target': '01_Active_Projects/projectA/',
    'description': 'ProjectA相关文件'
}
```

### 示例3：归档旧报告

```python
'old_reports': {
    'pattern': [r'.*_2024.*报告.*\.md$'],
    'target': '02_Project_Archive/OldReports/',
    'description': '2024年的旧报告'
}
```

---

## 🐛 常见问题

### Q1: 整理后文件找不到了？

**A**: 检查整理报告，查看文件被移动到哪里：
```
05_Outputs/Reports/file_organize_report_YYYYMMDD.md
```

### Q2: 某个文件不想被移动？

**A**: 添加到 `keep_in_root` 规则中（见"自定义规则"）

### Q3: 如何撤销整理？

**A**: 查看整理报告中的"原位置"，手动移回。或者使用Git恢复：
```bash
git checkout -- .
```

### Q4: 报告文件太多了？

**A**: 可以定期删除旧报告，或者修改规则只保留最近N天的报告

### Q5: 如何整理子目录的文件？

**A**: 当前版本只整理根目录。如需整理子目录：
1. 修改脚本中的 `files = [f for f in self.workspace_root.rglob('*') if f.is_file()]`
2. 注意递归整理可能会影响项目文件，建议先备份

---

## 🔄 工作流建议

### 推荐的每日工作流

```
1️⃣ 开始工作
   ↓
2️⃣ 产生文件（报告、脚本等）
   ↓
3️⃣ 下班前运行整理
   python daily_file_organizer.py
   ↓
4️⃣ 查看报告确认
   type 05_Outputs\Reports\file_organize_report_*.md
   ↓
5️⃣ 提交Git（可选）
   git add . && git commit -m "daily organize"
```

### 推荐的每周工作流

```
周一到周五：每天自动整理
    ↓
周末：回顾和清理
    ↓
1. 查看一周的整理报告
2. 删除不需要的临时文件
3. 归档旧项目
4. 更新分类规则
```

---

## 📚 相关工具

配合其他工作区工具使用：

- **workspace_cleaner.py** - 清理缓存和临时文件
- **workspace_scanner.py** - 扫描工作区全貌
- **workspace_report.py** - 生成健康报告
- **daily_launcher.py** - 每日启动器

---

## 🎉 效果对比

### 整理前
```
工作区根目录/
├── 报告_20260101.md ❌
├── 报告_20260102.md ❌
├── 报告_20260103.md ❌
├── test_script.py ❌
├── demo.html ❌
├── tool.bat ❌
└── ...（46个文件堆积）
```

### 整理后
```
工作区根目录/
├── start_new_session.bat ✅ （核心文件保留）
├── daily_launcher.py ✅ （核心文件保留）
├── workspace_scanner.py ✅ （核心文件保留）
└── ...（只有18个核心文件）

05_Outputs/Reports/20260108/
├── 工作区健康报告_*.md ✅
├── 清理报告_*.md ✅
└── 维护报告_*.md ✅

00_Agent_Library/99_Scripts_Tools/
├── check_scheduled_task.bat ✅
├── setup_scheduled_maintenance.ps1 ✅
└── ...（工具脚本归档）

00_Temp/Tests/20260108/
└── test_login.py ✅
```

---

## 📝 更新日志

### v1.0 (2026-01-08)
- ✅ 创建智能文件整理器
- ✅ 支持智能混合模式分类
- ✅ 生成详细整理报告
- ✅ 模拟运行功能
- ✅ 快捷启动菜单
- ✅ UTF-8编码支持

---

## 🚀 下一步计划

- [ ] 支持自定义配置文件（YAML/JSON）
- [ ] 添加图形界面
- [ ] 支持撤销操作
- [ ] 智能识别重复文件
- [ ] 自动压缩归档旧文件

---

**开始享受整洁的工作区吧！** 🎉

有问题？查看整理报告或编辑规则自定义！
