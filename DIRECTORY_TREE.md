# Office Agent Workspace - 目录树

> 生成时间: 2026-01-11 16:04:08

## 完整目录结构

```
Office_Agent_Workspace/
├── .claude/
├── 00_Agent_Library/
│   ├── 01_Documentation/
│   ├── 01_Prompt_Library/
│   │   ├── 任务拆解/
│   │   ├── 格式规范/
│   │   ├── 角色设定/
│   │   └── 项目管理/
│   ├── 02_Code_Snippets/
│   │   ├── API调用/
│   │   ├── 工具函数/
│   │   ├── 数据处理/
│   │   ├── 文件操作/
│   │   ├── 日志记录/
│   │   └── 网络请求/
│   ├── 03_MCP_Prototypes/
│   │   ├── 办公工具/
│   │   └── 网络工具/
│   ├── 04_Project_Templates/
│   │   ├── 带MCP的智能体/
│   │   └── 标准智能体/
│   ├── 99_Scripts_Tools/
├── 00_Temp/
│   └── Tests/
│       └── 20260108/
├── 01_Active_Projects/
│   ├── file_organizer/
│   │   ├── tests/
│   ├── market_supervision_agent/
│   │   ├── config/
│   │   ├── data/
│   │   ├── logs/
│   │   ├── src/
│   │   ├── tests/
│   ├── memory_agent/
│   ├── my_first_agent/
│   │   ├── .claude/
│   │   ├── test_folder/
│   ├── pdf_processor/
│   │   ├── .claude/
│   │   ├── test_pdfs/
├── 02_Project_Archive/
│   ├── 20250104_pdf_processor_v1.0/
│   │   ├── test_pdfs/
│   └── my_first_agent_历史版本/
├── 03_Code_Templates/
│   └── agent_project_template/
│       ├── data/
│       ├── utils/
├── 04_Data_&_Resources/
│   ├── Learning_Materials/
│   ├── Personal_Config/
│   └── Public_Data/
├── 05_Outputs/
│   └── Reports/
│       ├── 20260108/
├── 06_Learning_Journal/
│   ├── challenges_solved/
│   ├── code_patterns/
│   ├── daily_logs/
│   │   └── 2026-01/
│   ├── progress_tracker/
│   ├── snapshots/
│   │   ├── 20260107_151418/
│   │   ├── 20260107_152003/
│   ├── workspace_memory/
│   │   ├── code_versions/
├── playwright-mcp-demo/
├── playwright-mcp-demo.vscode/
```

## 关键项目详情

### 活跃项目 (01_Active_Projects)

- **file_organizer**: 证照材料智能整理工具
- **market_supervision_agent**: 市场监管智能体 - Market Supervision Agent
- **memory_agent**: 🧠 学习记忆助手 - Memory Agent
- **my_first_agent**: 项目名称
- **pdf_processor**: PDF 文本批量提取工具

### Playwright 自动化示例

```
playwright-mcp-demo/
  ├── exam-final-info.json (159.0B)
  ├── exam-info.json (163.0B)
  ├── exam-scores-summary.md (1.2KB)
  ├── example-chrome.js (1.1KB)
  ├── example.js (1007.0B)
  ├── form-auto-fill.js (2.0KB)
  ├── gxpf-after-login.png (1.5MB)
  ├── gxpf-auto-login.js (9.7KB)
  ├── gxpf-before-login.png (1.5MB)
  ├── gxpf-cookies.json (1011.0B)
  ├── gxpf-detailed-scores.html (16.3KB)
  ├── gxpf-detailed-scores.js (8.1KB)
  ├── gxpf-detailed-scores.png (1.6MB)
  ├── gxpf-exam-login-page.png (1.5MB)
  ├── gxpf-exam-login.js (3.4KB)
  ├── gxpf-exam-result.png (194.1KB)
  ├── gxpf-exam-scraper-helper.js (5.2KB)
  ├── gxpf-extract-scores-now.js (6.0KB)
  ├── gxpf-final-page.html (17.8KB)
  ├── gxpf-page-content.html (19.6KB)
  ├── INSTALL_GUIDE.md (3.4KB)
  ├── laptop-buying-guide.js (3.3KB)
  ├── laptop-recommendations.md (5.7KB)
  ├── package.json (492.0B)
  ├── README.md (2.4KB)
  ├── scrape-data.js (1.4KB)
  ├── screenshot.js (563.0B)
  ├── screenshot.png (13.1KB)
  ├── taobao-homepage.png (2.3MB)
  ├── taobao-laptop-search.js (5.9KB)
  ├── taobao-laptop-search.png (2.2MB)
  ├── taobao-scraper.js (2.2KB)
  ├── taobao-search-filled.png (611.0KB)
  ├── test-headless.js (1.3KB)
  ├── test-simple.js (1.6KB)
  ├── yingdao-courses.png (312.3KB)
  ├── yingdao-homepage.png (348.2KB)
  └── yingdao-rpa.js (2.9KB)
```

## 工作区管理工具

位于根目录的 Python 工具:

- `asset_manager.py`
- `code_version_tracker.py`
- `create_shortcut.py`
- `create_snapshot.py`
- `daily_file_organizer.py`
- `daily_launcher.py`
- `daily_snapshot.py`
- `file_manager_center.py`
- `generate_tree.py`
- `project_tracker.py`
- `update_shortcut.py`
- `update_workspace_docs.py`
- `workspace_butler_unified.py`
- `workspace_cleaner.py`
- `workspace_maintenance.py`
- `workspace_report.py`
- `workspace_scanner.py`
- `智能管家项目查询.py`
- `超级管家.py`
