# Office Agent Studio - 统一启动器使用说明

**版本**: v1.0
**日期**: 2026-01-12
**作者**: Claude Code

---

## 快速开始

### 方式1: 一键启动 (推荐)

双击运行 `启动_OA_Studio.bat`

### 方式2: 命令行启动

```bash
streamlit run office_agent_studio.py
```

浏览器会自动打开 http://localhost:8501

---

## 功能特性

### 1. 首页

- 欢迎界面和系统概览
- 核心功能介绍
- 最新动态展示
- 快速统计信息

### 2. 工具启动

统一的工具启动界面：

| 工具 | 状态 | 功能 |
|------|------|------|
| 文件整理 | 就绪 | 智能整理证照材料 |
| 申请书生成 | 就绪 | 自动生成申请书 |
| 记忆助手 | MVP | 智能知识管理 |
| 工作区管理 | 就绪 | 工作区维护工具 |

每个工具支持：
- 一键启动
- 查看文档
- 打开位置

### 3. 工作流

预设的自动化流程：

**申请书生成完整流程**
1. 验证数据
2. 选择模板
3. 生成文档
4. 审查文档

**文件整理并索引**
1. 整理文件
2. 索引知识

### 4. 系统状态

- 工作区状态监控
- 系统信息展示
- 最近活动记录

---

## 依赖安装

```bash
pip install streamlit streamlit-option-menu
```

---

## 技术架构

### 实现的开源模式

1. **AutoGen AgentTool 模式**
   - 工具互操作框架
   - 代码: [agent_toolkit.py](00_Agent_Library/agent_toolkit.py)

2. **LangGraph 状态管理**
   - 工作流引擎
   - 代码: [workflow_engine.py](00_Agent_Library/workflow_engine.py)

3. **AutoGen Studio 设计理念**
   - 统一图形界面
   - 工具状态监控

---

## 目录结构

```
Office_Agent_Workspace/
├── office_agent_studio.py      # 主程序
├── 启动_OA_Studio.bat          # 启动脚本
├── 00_Agent_Library/
│   ├── agent_toolkit.py        # 工具框架
│   └── workflow_engine.py      # 工作流引擎
└── 01_Active_Projects/
    ├── file_organizer/         # 文件整理工具
    ├── market_supervision_agent/  # 申请书生成工具
    └── memory_agent/           # 记忆助手
```

---

## 使用场景

### 场景1: 生成申请书

1. 打开 Studio
2. 点击 "工具启动"
3. 找到 "申请书生成"
4. 点击 "启动"
5. 填写数据，生成文档

### 场景2: 整理文件

1. 打开 Studio
2. 点击 "工具启动"
3. 找到 "文件整理"
4. 点击 "启动"
5. 自动整理和归档

### 场景3: 搜索知识

1. 打开 Studio
2. 点击 "工具启动"
3. 找到 "记忆助手"
4. 点击 "启动"
5. 语义搜索你的笔记

---

## 常见问题

### Q: 启动失败？

A: 检查 Python 是否安装，依赖是否完整：
```bash
pip install -r requirements.txt
```

### Q: 端口被占用？

A: 修改启动脚本中的端口号：
```bash
streamlit run office_agent_studio.py --server.port 8502
```

### Q: 工具启动后没反应？

A: 检查工具路径是否正确，查看控制台错误信息

---

## 更新日志

### v1.0 (2026-01-12)

- ✅ 创建统一 Streamlit 界面
- ✅ 实现 AgentTool 工具框架
- ✅ 实现 LangGraph 工作流引擎
- ✅ 集成所有办公工具
- ✅ 工具状态监控
- ✅ 系统状态展示

---

## 下一步计划

- [ ] 添加更多工作流模板
- [ ] 实现工具间数据传递
- [ ] 添加自定义工作流编辑器
- [ ] 支持插件系统
- [ ] Web API 接口

---

**祝你使用愉快！🎉**
