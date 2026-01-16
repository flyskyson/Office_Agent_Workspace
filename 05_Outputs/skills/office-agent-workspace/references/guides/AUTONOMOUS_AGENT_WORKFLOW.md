# 自主代理工作流模板

> **核心理念**: "有多大责任，就有多大权利"

---

## 📋 模板元信息

| 属性 | 值 |
|------|-----|
| **模板名称** | 自主代理工作流 |
| **英文名称** | Autonomous Agent Workflow |
| **版本** | v1.0 |
| **创建日期** | 2026-01-15 |
| **最后更新** | 2026-01-15 |
| **状态** | 稳定 |
| **创建方式** | 用户 + AI 共同讨论设计 |

---

## 🎯 适用场景

### ✅ 最适合

- 复杂的多步骤项目（如开发一个完整功能）
- 目标明确、实现路径灵活的任务
- 需要多次迭代优化的工作
- 用户时间有限，希望 AI 自主完成的项目

### ⚠️ 谨慎使用

- 简单任务（杀鸡用牛刀）
- 高风险、不可逆的操作（建议用想法落地工作流）
- 需要频繁人工反馈的创意工作

### ❌ 不适合

- 紧急且需要精确控制的任务
- 对过程可追溯性要求极高的场景（如审计）

---

## 🏗️ 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────┐
│              用户（使用者+监督方）                │
│  - 提出项目需求                                  │
│  - 参与暂停点确认                                │
│  - 参与重大决策（目标变更、模板修改）            │
│  - 验收最终结果                                  │
└─────────────────────────────────────────────────┘
                       ↕
┌─────────────────────────────────────────────────┐
│              总代理（AI）                        │
│  - 项目整体管控                                  │
│  - 进度跟踪                                      │
│  - 协调子代理                                    │
│  - 节点验收                                      │
│  - 工具库管理                                    │
│  - 失败处理                                      │
│  - 记录复盘                                      │
└─────────────────────────────────────────────────┘
         ↕         ↕         ↕
    ┌─────┐    ┌─────┐    ┌─────┐
    │子代理│    │子代理│    │子代理│ ...
    │节点1│    │节点2│    │节点3│
    └─────┘    └─────┘    └─────┘
```

---

## 🎭 角色定义

### 用户（使用者+监督方）

**职责**：
- 提出项目需求
- 参与暂停点确认
- 参与重大决策（目标变更、模板修改）
- 验收最终结果

**权限**：
- 项目启动前的最终确认
- 暂停点的状态确认
- 目标变更的决定权
- 模板修改的批准权

---

### 总代理（AI）

**职责**：
- 项目整体管控
- 进度跟踪和报告
- 协调子代理工作
- 节点验收（两级验收的第二级）
- 工具库管理
- 失败处理和恢复
- 记录和复盘

**权限**：
- 节点划分和分配
- 工作指南修改（步骤级）
- 工具底线判断
- 暂停点触发的判断
- 预算底线的执行
- 子代理能力档案管理

**约束**：
- 不能修改项目总目标（需与用户协商）
- 不能违反编码规范和架构底线
- 必须遵守预算底线
- 必须记录所有重要决策

---

### 子代理（AI）

**职责**：
- 理解节点工作指南（角色、目的、任务、步骤、要求）
- 自主完成节点任务
- 调用现有工具或创造新工具
- 自评验收（两级验收的第一级）
- 记录经验和教训
- 参与其他子代理的评估（自愿）

**权限**：
- 充分自主选择实现路径
- 创造新工具（在不违反底线的前提下）
- 调整具体实现步骤
- 申请工作指南修改（向总代理）

**约束**：
- 必须完成节点目标
- 不能违反编码规范和架构底线
- 必须通过两级验收
- 必须记录工作过程

**能力档案**（每个子代理都有）：
- 历史任务记录
- 成功率统计
- 擅长的任务类型
- 避免的任务类型
- 平均完成时间
- 工具创造记录
- 个性特征（如：保守 vs 激进、详细 vs 简洁）

---

## ⚙️ 核心机制

### 1. 节点定义

**粒度**：模块级别

**原则**：有多大的责任，就有多大的权利

**配置内容**：
```yaml
node:
  id: "node_1"
  name: "数据库设计"
  agent: "sub_agent_1"

  # 工作指南
  role: "数据库架构师"
  purpose: "为项目设计合理的数据库结构"
  tasks:
    - "分析数据需求"
    - "设计表结构"
    - "定义关系和约束"
  steps:
    - "1. 理解项目数据需求..."
    - "2. 设计初始schema..."
    - "3. 验证和优化..."
  requirements:
    - "不违反编码规范"
    - "考虑扩展性"
    - "符合项目架构"

  # 约束
  constraints:
    - "不违反编码规范"
    - "不破坏整体架构"
```

---

### 2. 目标层次结构

```
不可修改（需与用户协商）：
├── 项目总目标
│   示例："开发一个文档管理系统"

可以调整（总代理判断）：
├── 阶段目标
│   示例："完成数据存储模块"
│   操作：拆分、合并、重排、修改
└── 节点目标
    示例："设计数据库schema"
    操作：调整、优化、重写

所有变更必须记录：
- 变更时间
- 变更内容
- 变更原因
- 影响分析
```

---

### 3. 失败处理机制

```
子代理失败
    ↓
【第一步】总代理审查
  - 审查目标是否清晰
  - 审查步骤是否合理
  - 分析失败原因
  - 给出诊断意见
    ↓
【第二步】多代理评估（总代理判断触发）
  - 其他子代理自愿参与
  - 进行可行性评估
  - 形成评估报告
  - 给出建议的新工作指南
    ↓
【第三步】修改工作指南（总代理权限）
  - ✅ 可改：步骤
  - ❌ 不可改：目标
  - ⚠️ 涉及模板：与用户探讨后决定是否改目标
  - 记录修改内容
    ↓
【第四步】总代理接管
  - 如果还不行，总代理亲自完成
```

---

### 4. 验收机制

**两级验收**：

| 级别 | 方式 | 执行者 | 通过条件 |
|------|------|--------|----------|
| **第一级** | 自动判断 | 子代理自评 | 完成节点目标、符合要求 |
| **第二级** | 人工验收 | 总代理复验 | 目标达成、质量合格、无底线违反 |

只有通过两级验收，节点才算完成。

---

### 5. 暂停点机制（宽松）

**暂停点设置**：
```yaml
milestones:
  - point: "start"
    description: "启动后、执行前"
    require_confirmation: true
    trigger_condition: "明显不符合条件才停止"

  - point: "30%"
    description: "30%进度时"
    require_confirmation: false  # 宽松：默认不阻塞
    trigger_condition: "明显偏离目标才停止"

  - point: "70%"
    description: "70%进度时"
    require_confirmation: false
    trigger_condition: "明显无法达成目标才停止"

  - point: "pre_final"
    description: "最终验收前"
    require_confirmation: true
    trigger_condition: "明显未完成目标才停止"
```

**宽松触发逻辑**：
- 总代理向您汇报状态
- 如果明显不符合条件 → 果断停止
- 如果基本符合 → 继续执行
- 您可以主动干预，但默认不阻塞

---

### 6. 预算机制（充分资源 + 底线）

**预算配置**：
```yaml
budget:
  # 资源：给予充分（不设严格上限）
  resources:
    max_retries: "unlimited"
    max_tools: "unlimited"
    max_duration: "flexible"

  # 底线：设置最低限度
  limits:
    min_success_rate: 0.3      # 成功率低于30%果断停
    broken_tools_limit: 5      # 超过5个工具损坏果断停
    consecutive_failures: 3     # 连续3次节点失败果断停
```

**触发逻辑**：
- 正常情况：给予充分资源，不设硬限制
- 触发底线：果断停止，向您汇报
- 底线调整：需要与您协商

---

### 7. 工具管理

#### 工具注册表

**位置**：`00_Agent_Library/workflow_templates/autonomous_agent/tools_registry.json`

**结构**：
```json
{
  "tools": [
    {
      "name": "database_connector",
      "version": "1.0.0",
      "creator": "sub_agent_1",
      "created_at": "2026-01-15T10:00:00Z",
      "status": "stable",
      "purpose": "连接数据库并执行查询",
      "usage_count": 15,
      "success_rate": 0.95,
      "file_path": "00_Agent_Library/tools/database_connector.py",
      "dependencies": ["sqlalchemy", "psycopg2"]
    }
  ]
}
```

#### 工具生命周期

```
1. 创建阶段：status = "experimental"
   - 只有创建者可以使用
   - 其他代理可见但需谨慎
   - 持续时间：首次使用后

2. 试用阶段：status = "testing"
   - 需要至少2个其他代理使用过
   - 收集使用反馈
   - 持续时间：直到有足够数据

3. 稳定阶段：status = "stable"
   - 工具注册表标记为稳定
   - 推荐其他代理优先使用
   - 条件：成功率高、使用广泛

4. 废弃阶段：status = "deprecated"
   - 长期未使用或发现问题
   - 标记但不删除（可能有项目依赖）
   - 条件：30天未使用或有严重问题
```

#### 工具创造流程

```
子代理需要工具
    ↓
查询工具注册表
    ↓
┌─ 找到合适工具 ─┐
│                ↓
│          使用现有工具
│
└─ 未找到 ────────┐
                  ↓
            创建新工具
                  ↓
            检查底线约束
                  ↓
            ✅ 通过：创建并注册
            ❌ 不通过：调整方案或向总代理汇报
```

---

### 8. 信息同步

**同步方式**：

| 类型 | 方式 | 频率 | 内容 |
|------|------|------|------|
| **进度广播** | 定期广播 | 完成节点后 | 节点ID、状态、结果 |
| **状态查询** | 按需查询 | 主动询问 | 代理询问"谁在做X相关的事" |
| **大图景同步** | 渐进式 + 事件触发 | 项目开始 + 目标变更时 | 项目概要、目标、架构 |

**信息透明度**：
- 每个子代理需要：记住自己的历史、知道其他代理在做什么、理解项目大图景
- 总代理需要：掌握全局状态、监控所有节点、协调资源分配

---

### 9. 记录与复盘

**记录内容**：

| 内容 | 负责人 | 存储 |
|------|--------|------|
| **工具注册** | 总代理 | `tools_registry.json` |
| **工作指南修改记录** | 总代理 | `project/logs/guideline_changes.json` |
| **节点完成记录** | 总代理 | `project/logs/nodes_complete.json` |
| **失败处理记录** | 总代理 | `project/logs/failures_handled.json` |
| **暂停点记录** | 总代理 | `project/logs/milestones.json` |
| **预算使用记录** | 总代理 | `project/logs/budget_usage.json` |
| **子代理能力档案更新** | 总代理 | `project/agent_profiles/` |

**复盘报告**（项目结束后）：
```markdown
# 项目复盘报告

## 项目概要
- 项目名称
- 执行时间
- 总目标

## 执行统计
- 总节点数
- 成功节点数
- 失败节点数
- 平均完成时间

## 工具统计
- 创建工具数
- 复用工具数
- 工具成功率

## 子代理表现
- 各子代理的任务完成情况
- 能力档案更新

## 经验教训
- 做得好的地方
- 遇到的问题
- 改进建议

## 附录
- 完整日志
- 所有记录文件
```

---

### 10. 日志体系

**日志级别**：

```python
CRITICAL：总代理接管、目标变更、触发底线
ERROR：节点失败、工具错误、严重偏离
WARNING：工作指南修改、预算告警、暂停点触发
INFO：节点完成、工具创建、进度报告
DEBUG：子代理思考过程、详细决策路径
```

**日志内容**：
```json
{
  "timestamp": "2026-01-15T10:30:00Z",
  "level": "INFO",
  "agent": "sub_agent_1",
  "event_type": "node_complete",
  "node_id": "node_1",
  "message": "节点 node_1 完成",
  "data": {
    "duration_seconds": 1800,
    "tools_created": 2,
    "tools_used": 5
  }
}
```

**输出方式**：
- 实时流式：输出到控制台（用户看到进度）
- 结构化存储：保存到 `project/logs/`（便于分析）

---

## 📖 使用指南

### 项目生命周期

```
【启动阶段】
  ↓
  1. 用户提出需求
  2. 总代理与用户澄清需求、确定总目标
  3. 总代理设计节点、分配任务
  4. 总代理生成项目配置文件
  5. 总代理生成项目概要，同步给所有子代理
  6. 【暂停点1】用户确认：工作指南、节点划分
    ↓
【执行阶段】
  ↓
  对每个节点：
    1. 总代理激活子代理，传递工作指南
    2. 子代理执行任务（调用/创造工具）
    3. 子代理自评验收
    4. 总代理复验
       - 通过 → 5
       - 失败 → 触发失败处理机制
    5. 记录完成、广播进度
    6. 检查是否到达暂停点
    ↓
【收尾阶段】
  ↓
  1. 【暂停点4】总代理汇报最终状态
  2. 总代理生成复盘报告
  3. 用户验收最终成果
  4. 工具归档
  5. 项目结束
```

---

### 快速开始

**1. 创建项目配置文件**：

```yaml
# project_config.yaml
project:
  name: "文档管理系统开发"
  version: "1.0"
  goal: "开发一个基础的文档管理系统"
  description: "支持文档的上传、存储、检索和下载"

milestones:
  - point: "start"
    require_confirmation: true
    trigger_condition: "明显不符合条件才停止"
  - point: "30%"
    require_confirmation: false
  - point: "70%"
    require_confirmation: false
  - point: "pre_final"
    require_confirmation: true

budget:
  resources:
    max_retries: "unlimited"
    max_tools: "unlimited"
  limits:
    min_success_rate: 0.3
    broken_tools_limit: 5
    consecutive_failures: 3

nodes:
  - id: "node_1"
    name: "数据库设计"
    role: "数据库架构师"
    purpose: "设计文档管理系统的数据库结构"
    tasks:
      - "分析数据需求"
      - "设计表结构"
      - "定义关系和约束"
    requirements:
      - "不违反编码规范"
      - "考虑扩展性"

tools_registry:
  path: "00_Agent_Library/tools/"
  registry_file: "tools_registry.json"

logging:
  level: "INFO"
  output: "project/logs/"
```

**2. 启动项目**：

```python
from 00_Agent_Library.workflow_templates.autonomous_agent.template import AutonomousAgentWorkflow

# 创建工作流实例
workflow = AutonomousAgentWorkflow(config_path="project_config.yaml")

# 启动项目
workflow.start()
```

**3. 监控进度**：

```bash
# 查看实时日志
tail -f project/logs/project.log

# 查看当前状态
python -m workflow_templates.autonomous_agent.status --project project_name
```

---

### 最佳实践

#### 对于用户

1. **明确目标**：项目开始前，确保总目标清晰明确
2. **信任但验证**：信任 AI 自主执行，但在暂停点认真检查
3. **及时反馈**：发现问题及时沟通，不要等到验收
4. **积累经验**：每个项目后查看复盘报告，总结经验

#### 对于总代理

1. **合理划分节点**：粒度适中，既不过细也不过粗
2. **匹配能力**：根据子代理能力档案分配任务
3. **及时记录**：所有重要决策都要记录
4. **果断止损**：触发底线时果断停止，不要拖延
5. **定期汇报**：在暂停点主动向用户汇报状态

#### 对于子代理

1. **理解目标**：充分理解节点目标和项目大图景
2. **复用优先**：优先使用现有工具，避免重复创造
3. **记录过程**：详细记录工作过程和决策
4. **主动求助**：遇到困难主动向总代理汇报
5. **总结经验**：任务完成后总结经验教训

---

## 📝 示例

### 完整示例：开发一个简单的待办事项应用

**项目配置**：`todo_app_config.yaml`

```yaml
project:
  name: "待办事项应用开发"
  version: "1.0"
  goal: "开发一个简单的待办事项Web应用"
  description: "支持添加、完成、删除待办事项"

milestones:
  - point: "start"
    require_confirmation: true
  - point: "30%"
    require_confirmation: false
  - point: "70%"
    require_confirmation: false
  - point: "pre_final"
    require_confirmation: true

budget:
  resources:
    max_retries: "unlimited"
  limits:
    min_success_rate: 0.3
    consecutive_failures: 3

nodes:
  - id: "node_1"
    name: "需求分析和设计"
    role: "产品设计师"
    purpose: "分析需求并设计应用结构"
    tasks:
      - "明确功能需求"
      - "设计数据模型"
      - "规划API接口"
    requirements:
      - "简单易用"
      - "可扩展"

  - id: "node_2"
    name: "后端开发"
    role: "后端工程师"
    purpose: "实现后端API和数据库"
    tasks:
      - "搭建Flask框架"
      - "实现数据库模型"
      - "实现API接口"
    requirements:
      - "RESTful设计"
      - "数据持久化"

  - id: "node_3"
    name: "前端开发"
    role: "前端工程师"
    purpose: "实现用户界面"
    tasks:
      - "设计界面布局"
      - "实现交互逻辑"
      - "对接后端API"
    requirements:
      - "响应式设计"
      - "用户体验良好"

  - id: "node_4"
    name: "测试和部署"
    role: "测试工程师"
    purpose: "测试应用并准备部署"
    tasks:
      - "编写测试用例"
      - "执行测试"
      - "准备部署配置"
    requirements:
      - "核心功能测试覆盖"
      - "部署文档完整"

tools_registry:
  path: "00_Agent_Library/tools/"
  registry_file: "tools_registry.json"

logging:
  level: "INFO"
  output: "todo_app/logs/"
```

**执行流程**：

```
启动阶段：
├─ 用户提出需求
├─ 总代理澄清需求
├─ 总代理设计节点（如上）
├─ 总代理生成配置文件
├─ 【暂停点1】用户确认
└─ 开始执行

执行阶段：
├─ 节点1：需求分析和设计
│  ├─ 子代理A执行
│  ├─ 创建工具：data_model_designer.py
│  ├─ 自评验收：通过
│  └─ 总代理复验：通过
│
├─ 节点2：后端开发
│  ├─ 子代理B执行
│  ├─ 使用工具：data_model_designer.py
│  ├─ 创建工具：flask_starter.py
│  ├─ 自评验收：通过
│  └─ 总代理复验：通过
│
├─ 节点3：前端开发
│  ├─ 子代理C执行
│  ├─ 使用工具：flask_starter.py
│  ├─ 创建工具：responsive_ui_builder.py
│  ├─ 自评验收：通过
│  └─ 总代理复验：通过
│
└─ 节点4：测试和部署
   ├─ 子代理D执行
   ├─ 使用工具：flask_starter.py
   ├─ 自评验收：通过
   └─ 总代理复验：通过

收尾阶段：
├─ 【暂停点4】总代理汇报最终状态
├─ 总代理生成复盘报告
├─ 用户验收
└─ 项目结束
```

**预期输出**：

```
todo_app/
├── app.py                 # Flask应用主文件
├── models.py              # 数据模型
├── routes.py              # API路由
├── templates/             # HTML模板
├── static/                # 静态资源
├── tests/                 # 测试文件
├── requirements.txt       # 依赖清单
├── README.md              # 使用文档
└── deployment_guide.md    # 部署指南

tools/
├── data_model_designer.py
├── flask_starter.py
└── responsive_ui_builder.py

logs/
├── project.log            # 完整日志
├── nodes_complete.json    # 节点完成记录
├── tools_created.json     # 工具创建记录
└── final_report.md        # 复盘报告
```

---

## 🔄 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0 | 2026-01-15 | 初始版本<br>- 核心框架设计<br>- 角色定义和权限<br>- 失败处理机制<br>- 工具管理和共享<br>- 暂停点和预算机制<br>- 日志和复盘系统 |

---

## 🔮 未来规划

### v1.1 计划
- [ ] 回滚机制（状态快照和恢复）
- [ ] 工具质量评分系统
- [ ] 进度通知机制
- [ ] 性能监控面板

### v2.0 愿景
- [ ] 并行节点执行
- [ ] 自学习能力（从历史项目中学习）
- [ ] 跨项目知识迁移
- [ ] 智能节点调度

---

## 📚 相关文档

- [想法落地工作流](IDEA_WORKFLOW.md) - 适用于需求澄清和探索
- [模板索引](TEMPLATES.md) - 所有工作流模板的快速导航
- [CLAUDE.md](../../CLAUDE.md) - 项目核心配置

---

**模板维护**: 总代理（AI）
**更新策略**: 增量升级，向后兼容
**反馈渠道**: 项目复盘中的改进建议
