# Idea to Product Skill - 想法落地技能 🚀

**版本**: v3.0 - Mermaid 可视化版
**更新**: 2026-01-16
**升级**: 新增 Mermaid 流程图可视化

---

## 触发关键词

当用户提到以下内容时,自动激活本技能:
- "我有个想法"
- "想添加一个功能"
- "能不能实现..."
- "有个改进建议"
- "新建项目"
- "从零开始做..."
- 任何**模糊的、未结构化的想法表达**

---

## 技能描述

本技能实现从**模糊想法**到**可用产品**的完整落地流程,通过结构化的5阶段方法论,确保想法能够快速、系统地转化为实际可用的代码和功能。

## 🎨 可视化工作流程

### 整体流程图

```mermaid
graph TD
    A[用户输入: 我有个想法] --> B{想法类型判断}

    B -->|新功能| C[Phase 1: 理解与澄清]
    B -->|Bug修复| D[Phase 2: 探索与分析]
    B -->|重构| E[Phase 3: 方案设计]
    B -->|新项目| F[Phase 4: 快速原型]
    B -->|未定| G[Phase 5: 验证与迭代]

    C --> H{目标明确?}
    D --> I{找到解决方案?}
    E --> J{方案确定?}
    F --> K{原型可用?}
    G --> L{测试通过?}

    H -->|否| M[继续澄清]
    H -->|是| N[进入下一阶段]
    I -->|否| N[深入探索]
    I -->|是| N
    J -->|否| N[生成方案]
    J -->|是| N
    K -->|否| N[调整优化]
    K -->|是| N
    L -->|否| M[继续测试]
    L -->|是| O[交付产品]

    M --> N
    N --> O

    style A fill:#e1f5ff
    style C fill:#e8f5e9
    style D fill:#fff3e0
    style E fill:#ffe0b2
    style F fill:#f3e5f5
    style G fill:#e3f2fd
    style O fill:#4caf50

    classDef phase fill:#fff9c4,stroke:#f57c00
    classDef success fill:#4caf50,stroke:#2e7d32
    classDef info fill:#2196f3,stroke:#0d47a1

    class C,D,E,F,G info
    class A,B,O success
```

### Phase 1: 理解与澄清 (Clarification) 🎯

```mermaid
graph TD
    A[Phase 1: 理解与澄清] --> B[引导式对话]

    B --> C["📋 问题1: 场景描述"]
    C --> D[用户描述使用场景]

    B --> E["📋 问题2: 核心需求"]
    E --> F[明确核心功能]

    B --> G["📋 问题3: 约束条件"]
    G --> H[了解技术约束]

    B --> I["📋 问题4: 成功标准"]
    I --> J[定义验收标准]

    D --> K[生成需求文档]
    F --> K
    H --> K
    J --> K

    K --> L{需求明确?}
    L -->|否| M[继续澄清]
    L -->|是| N[进入Phase 2]

    style A fill:#e8f5e9
    style K fill:#e1f5ff

    classDef phase fill:#e8f5e9,stroke:#2e7d32
    classDef success fill:#4caf50,stroke:#2e7d32
```

### Phase 2: 探索与分析 (Exploration) 🔍

```mermaid
graph TD
    A[Phase 2: 探索与分析] --> B[Grep搜索相关代码]
    B --> C[分析现有实现]

    B --> D[搜索可用工具]
    C --> E[识别集成点]

    D --> F{找到解决方案?}
    E --> F

    F -->|是| G[提取实现方案]
    F -->|否| H[技术调研]

    G --> I[生成探索报告]
    H --> I

    I --> J{可行性评估}
    J --> K{高/中/低}

    K --> L[进入Phase 3]
    J --> L

    style A fill:#fff3e0
    style I fill:#f3f5f5
    style L fill:#e0f2f1

    classDef phase fill:#fff3e0,stroke:#f57c00
    classDef success fill:#4caf50,stroke:#2e7d32
    classDef info fill:#2196f3,stroke:#0d47a1

    class A,B,C,D,E,F,G,H,I,J,K info
```

### Phase 3: 方案设计 (Design) 📐

```mermaid
graph TD
    A[Phase 3: 方案设计] --> B[生成3个方案]

    B --> C[MVP方案]
    B --> D[推荐方案]
    B --> E[完整方案]

    C --> F[特点: 快速实现]
    D --> F[特点: 平衡方案]
    E --> F[特点: 功能全面]

    F --> G[对比优缺点]
    G --> H[评估实现难度]

    H --> I[推荐最佳方案]
    I --> J[生成实现计划]

    J --> K[进入Phase 4]

    style A fill:#ffe0b2
    style B fill:#e8f5e9
    style C fill:#e1f5ff
    style D fill:#e3f2fd
    style E fill:#f3e5f5
    style F fill:#fff4e6
    style I fill:#4caf50

    classDef phase fill:#ffe0b2,stroke:#f57c00
    classDef success fill:#4caf50,stroke:#2e7d32
    classDef info fill:#2196f3,stroke:#0d47a1

    class A,B,G,I info
```

### Phase 4: 快速原型 (Prototyping) ⚡

```mermaid
graph TD
    A[Phase 4: 快速原型] --> B[创建项目结构]

    B --> C[实现核心功能]
    C --> D[创建用户界面]

    D --> E[编写测试代码]
    E --> F[生成测试数据]

    F --> G[运行测试套件]
    G --> H{测试通过?}

    H -->|否| I[修复错误]
    H -->|是| J[进入Phase 5]

    I --> J[重新测试]
    J --> H

    style A fill:#f3e5f5
    style B fill:#e0f2f1
    style C fill:#fce4ec
    style D fill:#fff4e6
    style E fill:#e3f2fd
    style F fill:#e1f5ff
    style J fill:#4caf50

    classDef phase fill:#f3e5f5,stroke:#2e7d32
    classDef success fill:#4caf50,stroke:#2e7d32
    classDef info fill:#2196f3,stroke:#0d47a1

    class A,B,C,D,E,F,G,H,J info
```

### Phase 5: 验证与迭代 (Validation) ✅

```mermaid
graph TD
    A[Phase 5: 验证与迭代] --> B[运行测试套件]

    B --> C[功能测试]
    B --> D[性能测试]

    C --> E{测试通过?}
    D --> F{性能达标?}

    E -->|否| G[快速修复]
    F -->|否| H[优化调整]

    G --> H
    H --> I[重新测试]

    E -->|是| J[收集用户反馈]
    F -->|是| J

    J --> K{满意?}
    K -->|是| L[交付产品]
    K -->|否| M[进入Phase 3]

    L --> M[版本发布]
    M --> N[记录到知识库]

    style A fill:#e8f6f3
    style L fill:#4caf50
    style M fill:#4caf50,stroke:#2e7d32

    classDef phase fill:#e8f6f3,stroke:#2e7d32
    classDef success fill:#4caf50,stroke:#2e7d32
    classDef info fill:#2196f3,stroke:#0d47a1

    class A,B,C,D,E,F,G,H,I,J,K,L,M,N info
```

---

## 🎯 使用场景示例

### 场景1: 新功能开发

```
输入: "我有个想法，想添加智能推荐功能"
    ↓
Phase 1: 澄清需求
    ├── 目标: 基于用户历史的内容推荐
    ├── 输入: 用户浏览记录
    └── 输出: Top-5推荐列表
    ↓
Phase 2: 探索代码库
    ├── 找到 memory_agent (向量搜索)
    ├── 发现 ChromaDB (向量数据库)
    └── 发现 sentence-transformers (嵌入模型)
    ↓
Phase 3: 方案设计
    ├── MVP: 关键词匹配
    ├── 推荐: 向量相似度
    └── 完整: 深度学习
    ↓
Phase 4: 快速原型
    ├── 创建 recommender/
    ├── 实现 RecommenderEngine
    ├── 编写 API 接口
    └── 编写测试
    ↓
Phase 5: 验证交付
    ├── 运行 pytest (15个测试通过)
    ├── 性能测试 (0.8s < 1s ✅)
    └── 准确率测试 (75% > 70% ✅)
    ↓
时间: < 1.5小时 → 可用原型
```

---

## 🚀 下一步

### 立即体验

1. **在 VSCode 中安装 Mermaid Chart 扩展**
   - 搜索 "Mermaid Chart Preview"
   - 点击安装

2. **查看升级后的流程图**
   - 打开 [skills/super-butler/SKILL.md](skills/super-butler/SKILL.md)
   - 查看实时渲染的 Mermaid 流程图

3. **升级其他技能文档**
   - [skills/application-generator/SKILL.md](skills/application-generator/SKILL.md)
   - [skills/knowledge-indexer/SkILL.md](skills/knowledge-indexer/SKILL.md)
   - [skills/license-organizer/SKILL.md](skills/license-organizer/SKILL.md)

---

**技能版本**: v3.0 - Mermaid 可视化版
**更新日期**: 2026-01-16
