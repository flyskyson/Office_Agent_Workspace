# Office Agent Workspace

> 个人开发工作区 - AI Agent 项目和资源管理中心

**更新时间**: 2026-01-07

---

## 📁 目录结构

```
Office_Agent_Workspace/
├── 00_Agent_Library/          # Agent 开发库和资源
│   ├── 01_Documentation/      # 📚 文档和指南
│   ├── 02_Code_Snippets/      # 💡 代码片段
│   └── 99_Scripts_Tools/      # 🔧 实用脚本工具
│
├── 01_Active_Projects/        # 🚀 活跃项目（当前开发中）
│   ├── my_first_agent/        # 我的第一个 Agent 项目
│   ├── pdf_processor/         # PDF 处理工具
│   └── web_monitor_agent/     # Web 监控 Agent
│
├── 02_Project_Archive/        # 📦 已归档项目
│
├── 03_Code_Templates/         # 📋 代码模板（待扩充）
│
├── 04_Data_&_Resources/       # 📊 数据和资源
│
├── 05_Outputs/                # 📤 输出文件（待使用）
│
├── 06_Learning_Journal/       # 📓 学习日志和成长记录
│   ├── AI_MEMORY.md           # 🧠 AI助手记忆文件（核心）
│   ├── daily_logs/            # 每日学习记录
│   ├── challenges_solved/     # 解决过的问题
│   ├── code_patterns/         # 积累的代码模式
│   └── progress_tracker/      # 技能进度追踪
│
├── workspace_report.py        # 🏥 工作区健康检查工具
├── workspace_cleaner.py       # 🧹 工作区清理工具
├── workspace_maintenance.py   # 🔧 定期维护脚本
└── README.md                  # 📖 本文件
```

---

## 📓 学习追踪系统

### 核心理念
记录学习历程,让AI助手更好地了解你的成长轨迹、技术偏好和编程风格。

### 核心文件: AI_MEMORY.md
位于 [06_Learning_Journal/AI_MEMORY.md](06_Learning_Journal/AI_MEMORY.md),包含:
- 👤 开发者档案和技术背景
- 🎯 学习目标和进度
- 💡 编码风格偏好
- 🐛 常见问题与解决方案
- 📁 项目经验总结
- 🎓 学习资源记录
- 🔧 工具和模板库

**使用建议**:
- ✅ 每次和新AI助手对话时,让它先读取此文件
- ✅ 每学会新技能时更新技能进度表
- ✅ 完成项目后记录心得和挑战

### 学习日志记录工具
交互式命令行工具,快速记录学习内容:

```bash
# 运行学习日志工具
python 06_Learning_Journal/learning_logger.py
```

**功能**:
1. 创建每日学习日志 (自动模板)
2. 记录遇到的问题和解决方案
3. 保存有用的代码模式
4. 更新技能进度
5. 查看学习统计

**输出位置**:
- 每日日志 → `06_Learning_Journal/daily_logs/YYYY-MM/DD.md`
- 问题记录 → `06_Learning_Journal/challenges_solved/`
- 代码模式 → `06_Learning_Journal/code_patterns/`
- 技能进度 → `06_Learning_Journal/progress_tracker/`

---

## 🛠️ 维护工具

### 1. 工作区健康报告
生成详细的工作区状态报告，包括：
- 主要文件夹统计（大小、项目数）
- 虚拟环境检测
- 缓存和临时文件识别
- 待归档项目标记

```bash
# 生成健康报告
python workspace_report.py
```

**输出**: `工作区健康报告_YYYYMMDD_HHMMSS.md`

---

### 2. 工作区清理工具
清理和整理工作区：
- 删除 Python 缓存（`__pycache__`、`.pyc`）
- 整理根目录文件到对应文件夹
- 删除临时文件

```bash
# 演习模式（预览效果）
python workspace_cleaner.py

# 实际执行清理
python workspace_cleaner.py --execute
```

**输出**: `清理报告_YYYYMMDD_HHMMSS.md`

**安全提示**:
- ✅ 默认为演习模式，不会实际删除文件
- ✅ 使用 `--execute` 参数才会真正执行
- ✅ 所有操作都有详细日志

---

### 3. 定期维护脚本
自动化维护任务：
- 清理 Python 缓存
- 检查不活跃项目
- 检查磁盘空间
- 查找大文件
- 验证工作区结构
- 可选：生成详细健康报告

```bash
# 基础维护
python workspace_maintenance.py

# 完整维护（含健康报告）
python workspace_maintenance.py --health-report
```

**输出**: `维护报告_YYYYMMDD_HHMMSS.md`

**建议频率**: 每周运行一次

---

## 📋 最佳实践

### 项目管理
1. **新项目** → 在 `01_Active_Projects/` 下创建
2. **完成项目** → 移动到 `02_Project_Archive/`
3. **代码片段** → 保存到 `00_Agent_Library/02_Code_Snippets/`
4. **文档** → 放到 `00_Agent_Library/01_Documentation/`

### 虚拟环境管理
- 每个项目独立维护自己的 `venv/`
- 删除不活跃项目的 venv 可节省空间
- 使用 `requirements.txt` 重建虚拟环境：
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Windows
  pip install -r requirements.txt
  ```

### 定期维护
- **每周**: 运行 `workspace_maintenance.py`
- **每月**: 运行 `workspace_report.py` 检查状态
- **需要时**: 运行 `workspace_cleaner.py` 清理缓存

### Git 仓库
在项目根目录创建 `.gitignore`：
```gitignore
__pycache__/
*.pyc
*.pyo
venv/
.venv/
*.log
temp_*.py
*.tmp
*.cache
工作区健康报告_*.md
清理报告_*.md
维护报告_*.md
```

---

## 🔍 快速统计

| 文件夹 | 用途 | 大小 | 项目数 |
|--------|------|------|--------|
| 00_Agent_Library | 资源库 | ~80 KB | 4 个子目录 |
| 01_Active_Projects | 活跃项目 | ~95 MB | 3 个项目 |
| 02_Project_Archive | 归档项目 | ~80 KB | 2 个项目 |

*数据更新于 2026-01-07，运行 `workspace_report.py` 获取最新数据*

---

## 🚀 快速开始

### 🌟 新对话快速开始（推荐）
当你重开对话时，使用以下方式快速恢复上下文：

**方式1: 一键启动（Windows）**
```bash
# 双击运行或在命令行执行
start_new_session.bat
```

**方式2: 标准开场白**
```
你好！我重开了一个新对话。

请先阅读我的开发者档案：
文件位置：06_Learning_Journal/AI_MEMORY.md

然后基于我的档案推荐适合的项目。
```

**详细指南**: [06_Learning_Journal/使用指南_新对话快速开始.md](06_Learning_Journal/使用指南_新对话快速开始.md)

---

### 📊 项目规划
需要项目建议？运行项目规划助手：

```bash
# 方式1: 运行Python脚本
python 06_Learning_Journal/project_planner.py

# 方式2: 使用快速启动菜单
start_new_session.bat
```

规划助手会：
- 分析你的技能水平（从AI_MEMORY.md）
- 推荐适合的办公自动化项目
- 生成学习路径和计划

**项目库**: [06_Learning_Journal/自动化项目库.md](06_Learning_Journal/自动化项目库.md)（18个项目示例）

---

### 📝 记录学习内容
完成学习后，记录到日志：

```bash
python 06_Learning_Journal/learning_logger.py
```

功能：
1. 创建每日学习日志
2. 记录问题和解决方案
3. 保存代码模式
4. 更新技能进度

---

### 传统方式：手动创建项目
```bash
cd 01_Active_Projects
mkdir my_new_project
cd my_new_project
python -m venv venv
venv\Scripts\activate
# 开始开发...
```

### 检查工作区健康
```bash
python workspace_report.py
```

### 清理缓存
```bash
python workspace_cleaner.py --execute
```

### 运行定期维护
```bash
python workspace_maintenance.py --health-report
```

---

## 📝 维护日志

### 2026-01-07
- ✅ 创建工作区维护工具集
- ✅ 清理 Python 缓存（释放 26.22 MB）
- ✅ 整理根目录文件（移动 13 个文件）
- ✅ 建立文件夹结构规范

---

## 📞 工具使用帮助

需要帮助？运行工具时查看详细输出，或查看生成的报告文件：
- `工作区健康报告_*.md` - 完整的状态分析
- `清理报告_*.md` - 清理操作记录
- `维护报告_*.md` - 定期维护结果

---

**Happy Coding! 🎉**
