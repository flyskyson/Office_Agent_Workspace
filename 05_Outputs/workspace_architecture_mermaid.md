# Office Agent Workspace - 完整架构图

**生成日期**: 2026-01-16
**版本**: v2.0 Mermaid 可视化版

---

## 🎨 系统整体架构

### 三层架构模型

```mermaid
graph TB
    subgraph UI["用户交互层"]
        A1[Flask Web UI]
        A2[Streamlit UI]
        A3[CLI 菜单启动器]
    end

    subgraph Business["业务逻辑层"]
        B1[AgentTool 框架]
        B2[Workflow Engine]
        B3[Skill System]

        C1[市场监管智能体]
        C2[记忆助手]
        C3[文件整理工具]
    end

    subgraph Data["数据存储层"]
        D1[文件系统]
        D2[ChromaDB 向量数据库]
        D3[YAML 配置]
    end

    A1 --> B1
    A2 --> B2
    A3 --> B3

    B1 --> C1
    B2 --> C2
    B3 --> C3

    C1 --> D1
    C1 --> D3
    C2 --> D2
    C3 --> D1

    style A1 fill:#e1f5ff
    style A2 fill:#e8f5e9
    style A3 fill:#fff4e6
    style B1 fill:#e3f2fd
    style B2 fill:#e0f2f1
    style B3 fill:#fce4ec
    style C1 fill:#f3e5f5
    style C2 fill:#e8f6f3
    style C3 fill:#fff3e0
    style D1 fill:#e1bee7
    style D2 fill:#c8e6c9
    style D3 fill:#ffe0b2
```

---

## 🧩 核心组件架构

### AgentTool 框架

```mermaid
graph LR
    A[BaseTool 基类] --> B[OCRTool]
    A --> C[TemplateFillerTool]
    A --> D[FileOrganizerTool]

    B --> E[百度OCR]
    B --> F[PaddleOCR]

    C --> G[Jinja2 渲染]
    C --> H[文档生成]

    D --> I[文件扫描]
    D --> J[规则匹配]

    style A fill:#e3f2fd
    style B fill:#fff4e6
    style C fill:#e8f5e9
    style D fill:#fce4ec
    style E fill:#e0f2f1
    style F fill:#f3e5f5
    style G fill:#e8f6f3
    style H fill:#fff3e0
    style I fill:#e1bee7
    style J fill:#c8e6c9
```

### Workflow Engine

```mermaid
graph TD
    A[StateGraph] --> B[添加节点]
    A --> C[添加边]
    A --> D[条件分支]

    B --> E[工作流节点]
    C --> F[节点连接]
    D --> G[路由决策]

    E --> H[执行工作流]
    F --> H
    G --> H

    H --> I[返回结果]

    style A fill:#e3f2fd
    style B fill:#fff4e6
    style C fill:#e8f5e9
    style D fill:#fce4ec
    style E fill:#e0f2f1
    style F fill:#f3e5f5
    style G fill:#e8f6f3
    style H fill:#fff3e0
    style I fill:#c8e6c9
```

### Skill System

```mermaid
graph LR
    A[用户输入] --> B[关键词检测]
    B --> C[技能匹配]
    C --> D[加载 SKILL.md]
    D --> E[执行步骤清单]
    E --> F[返回结果]

    style A fill:#e1f5ff
    style B fill:#fff4e6
    style C fill:#e8f5e9
    style D fill:#e3f2fd
    style E fill:#e0f2f1
    style F fill:#e8f6f3
```

---

## 🤖 智能体详细架构

### 市场监管智能体

```mermaid
graph TD
    A[flask_app.py<br/>Web界面] --> B[jinja2_filler.py<br/>核心逻辑]

    B --> C[OCR模块<br/>百度/PaddleOCR]
    B --> D[模板引擎<br/>Jinja2]
    B --> E[文档生成<br/>python-docx]

    C --> F[database_schema.yaml<br/>数据映射]
    D --> F
    E --> F

    F --> G[templates/*.docx<br/>Word模板]

    style A fill:#e1f5fe
    style B fill:#e8f5e9
    style C fill:#fff4e6
    style D fill:#e3f2fd
    style E fill:#e0f2f1
    style F fill:#fce4ec
    style G fill:#f3e5f5
```

### 记忆助手

```mermaid
graph TD
    A[app.py<br/>Streamlit界面] --> B[memory_agent.py<br/>核心逻辑]

    B --> C[笔记添加]
    B --> D[语义搜索]
    B --> E[间隔复习]

    C --> F[ChromaDB<br/>向量数据库]
    D --> F
    E --> F

    F --> G[sentence-transformers<br/>嵌入模型]

    style A fill:#f3e5f5
    style B fill:#e8f5e9
    style C fill:#fff4e6
    style D fill:#e3f2fd
    style E fill:#e0f2f1
    style F fill:#fce4ec
    style G fill:#f3e5f5
```

### 文件整理工具

```mermaid
graph TD
    A[file_organizer.py<br/>核心逻辑] --> B[文件扫描]
    A --> C[规则匹配]
    A --> D[自动移动]

    B --> E[config.json<br/>整理规则]
    C --> E
    D --> E

    style A fill:#e8f5e9
    style B fill:#fff4e6
    style C fill:#e3f2fd
    style D fill:#e0f2f1
    style E fill:#fce4ec
```

---

## 🔄 数据流设计

### 申请书生成流程

```mermaid
graph TD
    A[用户上传图片] --> B[Flask 接收请求]
    B --> C[OCR 识别营业执照]
    C --> D[提取结构化数据]
    D --> E[加载 YAML 配置]
    E --> F[映射到模板变量]
    F --> G[Jinja2 渲染模板]
    G --> H[生成 Word 文档]
    H --> I[返回下载链接]

    style A fill:#64b5f6
    style B fill:#81c784
    style C fill:#ffb74d
    style D fill:#81c784
    style E fill:#81c784
    style F fill:#81c784
    style G fill:#ffb74d
    style H fill:#81c784
    style I fill:#4caf50
```

### 知识管理流程

```mermaid
graph TD
    A[用户添加笔记] --> B[Streamlit 接收输入]
    B --> C[文本预处理]
    C --> D[sentence-transformers 向量化]
    D --> E[存储到 ChromaDB]
    E --> F[用户搜索]
    F --> G[查询向量化]
    G --> H[ChromaDB 相似度检索]
    H --> I[返回相关笔记]

    style A fill:#64b5f6
    style B fill:#81c784
    style C fill:#81c784
    style D fill:#ffb74d
    style E fill:#81c784
    style F fill:#64b5f6
    style G fill:#ffb74d
    style H fill:#81c784
    style I fill:#4caf50
```

---

## 🎯 技能系统工作流

### 技能触发与执行

```mermaid
graph LR
    A[用户输入] --> B{触发关键词检测}

    B -->|匹配| C[激活技能]
    B -->|不匹配| D[继续检测]

    C --> E[加载 SKILL.md]
    E --> F[解析执行步骤]

    F --> G[执行步骤 1]
    G --> H[执行步骤 2]
    H --> I[执行步骤 N]

    I --> J{验证结果}
    J -->|成功| K[返回结果]
    J -->|失败| L[错误处理]

    L --> M[记录错误]
    M --> N[提供解决方案]

    style A fill:#e1f5ff
    style C fill:#e8f5e9
    style E fill:#fff4e6
    style F fill:#e3f2fd
    style G fill:#e0f2f1
    style H fill:#fce4ec
    style I fill:#f3e5f5
    style K fill:#c8e6c9
    style L fill:#ffccbc
    style M fill:#ffccbc
    style N fill:#fff9c4
```

---

## 📊 技术栈关系图

```mermaid
graph TB
    subgraph WebFrameworks[Web框架]
        A1[Flask]
        A2[Streamlit]
    end

    subgraph Automation[自动化工具]
        B1[Playwright]
    end

    subgraph AIML[AI/ML]
        C1[百度OCR]
        C2[PaddleOCR]
        C3[ChromaDB]
        C4[sentence-transformers]
    end

    subgraph Docs[文档处理]
        D1[python-docx]
        D2[Jinja2]
    end

    A1 --> D1
    A1 --> D2
    A2 --> C3

    B1 --> C1

    C1 --> A1
    C2 --> A1
    C3 --> A2
    C4 --> C3

    style A1 fill:#e1f5fe
    style A2 fill:#f3e5f5
    style B1 fill:#fff4e6
    style C1 fill:#e8f5e9
    style C2 fill:#c8e6c9
    style C3 fill:#fff9c4
    style C4 fill:#ffccbc
    style D1 fill:#e0f2f1
    style D2 fill:#fce4ec
```

---

## 🎨 颜色主题说明

本架构图使用统一的配色方案：

| 颜色 | 色值 | 用途 |
|------|------|------|
| 🔵 蓝色 | #e1f5ff | 输入/开始 |
| 🟢 绿色 | #e8f5e9 | 成功/完成 |
| 🟡 黄色 | #fff4e6 | 处理中 |
| 🟠 橙色 | #fce4ec | 检查/验证 |
| 🟣 紫色 | #f3e5f5 | 特殊操作 |
| 🔴 红色 | #ffccbc | 错误/警告 |

---

## 📝 使用说明

### 在 VSCode 中查看

1. 安装扩展: "Mermaid Chart Preview"
2. 打开本文件
3. 查看实时渲染的流程图

### 在线查看

访问 https://mermaid.live
将 Mermaid 代码块粘贴到编辑器中

### 导出为图片

```bash
# 安装工具
npm install -g @mermaid-js/mermaid-cli

# 导出图片
mmdc -i workspace_architecture_mermaid.md -o architecture.png
```

---

**文档版本**: v2.0
**最后更新**: 2026-01-16
**维护者**: Claude Code (GLM-4.7)
