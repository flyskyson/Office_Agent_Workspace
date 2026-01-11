# Office Agent Workspace - 工作区指南

> 最后更新: 2026-01-11 17:30

## 目录结构概览

```
Office_Agent_Workspace/
├── 00_Agent_Library/        # AI 助手资源库
│   ├── 01_Prompt_Library/   # 提示词模板
│   ├── 02_Code_Snippets/    # 代码片段
│   └── 99_Scripts_Tools/    # 工具脚本集合
├── 01_Active_Projects/      # 活跃开发项目
├── 02_Project_Archive/      # 历史项目归档
├── 06_Learning_Journal/     # 学习笔记与工作区记忆
└── playwright-mcp-demo/     # Playwright 自动化示例
```

## 核心项目

### 活跃项目 (01_Active_Projects)

1. **file_organizer** - 证照材料智能整理工具
   - 语言: Python
   - 状态: 活跃开发
   - 文档: [README](01_Active_Projects/file_organizer/README.md)

2. **market_supervision_agent** - 市场监管智能体
   - 语言: Python
   - 功能: 自动化处理企业年报、设立登记、变更登记等市场监管业务
   - 技术: Playwright 浏览器自动化
   - 状态: 新建项目，活跃开发
   - 文档: [README](01_Active_Projects/market_supervision_agent/README.md)
   - 项目结构: [PROJECT_STRUCTURE.md](01_Active_Projects/market_supervision_agent/PROJECT_STRUCTURE.md)

3. **memory_agent** - 学习记忆助手
   - 语言: Python
   - 功能: 智能知识管理、语义搜索、间隔重复复习系统
   - 技术: ChromaDB向量数据库、sentence-transformers
   - 状态: MVP版本已完成
   - 文档: [README](01_Active_Projects/memory_agent/README.md)

4. **pdf_processor** - PDF 处理工具集
   - 语言: Python
   - 功能: PDF 提取、转换
   - 文档: [README](01_Active_Projects/pdf_processor/README.md)

5. **my_first_agent** - 文件整理 Agent
   - 语言: Python
   - 说明: 第一个 AI Agent 项目
   - 文档: [README](01_Active_Projects/my_first_agent/README.md)

### 演示项目

6. **playwright-mcp-demo** - Playwright 自动化脚本示例
   - 语言: JavaScript (Node.js)
   - 技术: Playwright 1.57.0
   - 文档: [README](playwright-mcp-demo/README.md)
   - 用途: 浏览器自动化、网页抓取、表单填写

## 工作区管理工具

位于工作区根目录的 Python 脚本：

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `workspace_scanner.py` | 扫描并建立工作区索引 | 更新项目结构视图 |
| `workspace_cleaner.py` | 清理缓存、临时文件 | 释放磁盘空间 |
| `workspace_report.py` | 生成健康报告 | 定期检查工作区状态 |
| `workspace_maintenance.py` | 自动维护任务 | 定期清理与优化 |
| `workspace_butler_unified.py` | 统一管家系统 | 一键启动所有管理功能 |

## 快速启动

### 新建项目时
1. 在 `01_Active_Projects/` 创建项目文件夹
2. 添加 README.md 说明文档
3. 运行 `python workspace_scanner.py` 更新索引

### 查看工作区状态
```bash
python workspace_report.py
```

### 清理工作区
```bash
python workspace_cleaner.py
```

### 使用 Playwright 自动化
```bash
cd playwright-mcp-demo
npm run example    # 基础示例
npm run screenshot # 网页截图
npm run scrape     # 数据抓取
npm run form       # 表单自动填写
```

## AI 助手使用指南

### 代码片段库
- 位置: `00_Agent_Library/02_Code_Snippets/`
- 分类: API调用、文件操作、数据处理、日志记录、工具函数

### 提示词模板
- 位置: `00_Agent_Library/01_Prompt_Library/`
- 分类: 角色设定、项目管理

### 工具脚本
- 位置: `00_Agent_Library/99_Scripts_Tools/`
- 内容: 38+ 实用脚本（清理、维护、启动器等）

## 工作区索引

详细的项目信息请查看自动生成的索引文件：
- JSON 格式: [workspace_index_latest.json](06_Learning_Journal/workspace_memory/)
- Markdown 格式: [workspace_index_latest.md](06_Learning_Journal/workspace_memory/)

## 项目归档规则

完成或暂停的项目移至 `02_Project_Archive/`，使用命名格式：
```
YYYYMMDD_项目名_版本号/
```

## 技术栈

- **Python**: 主要开发语言
- **Node.js**: Playwright 自动化
- **PowerShell/Batch**: 系统工具脚本

## Git 管理

- 主分支: `master`
- 自动忽略: Python缓存、Node模块、临时文件
- 提交前运行: `workspace_cleaner.py`

## 资源链接

- 工作区管理工具文档: [00_Agent_Library/99_Scripts_Tools/](00_Agent_Library/99_Scripts_Tools/)
- Playwright 文档: [playwright-mcp-demo/README.md](playwright-mcp-demo/README.md)

---

**提示**: 让 AI 助手先阅读此文档，可快速了解工作区结构和可用资源。
