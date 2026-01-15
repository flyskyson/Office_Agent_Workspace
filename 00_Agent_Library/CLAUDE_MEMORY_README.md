# Claude Code 记忆持久化系统

## 🧠 概述

这是一个为Claude Code设计的跨会话记忆持久化系统，让AI助手能够记住历史对话、决策逻辑、用户偏好，并在未来的会话中复用这些经验。

## 🎯 核心功能

### 1. **上下文记忆 (Context Memory)**
记住每次对话的上下文信息：
- 对话主题
- 关键要点
- 使用的工具
- 做出的决策
- 最终结果

### 2. **决策记忆 (Decision Memory)**
记住工具选择和决策逻辑：
- 任务类型
- 选择的工具
- 备选方案
- 决策理由
- 成功与否
- 经验教训

### 3. **用户偏好 (User Preferences)**
学习和记住用户偏好：
- 编码风格
- 首选工具
- 沟通方式
- 常用命令

### 4. **对话历史 (Conversation History)**
记录完整的对话：
- 用户查询
- AI响应
- 工具使用
- 结果评估

### 5. **演进轨迹 (Evolution Timeline)**
追踪系统和项目的演进：
- 版本历史
- 能力变化
- 重要里程碑

## 📁 存储结构

```
06_Learning_Journal/claude_memory/
├── contexts.json       # 对话上下文
├── decisions.json      # 决策记录
├── preferences.json    # 用户偏好
├── projects.json       # 项目知识
├── evolution.json      # 演进轨迹
└── conversations.json  # 对话历史
```

## 🚀 使用方法

### 基础使用

```python
from 00_Agent_Library.claude_memory import ClaudeMemory

# 创建记忆系统
memory = ClaudeMemory()

# 记住决策
memory.remember_decision(
    task_type="read_file",
    tool_chosen="Read",
    alternatives=["Bash: cat", "Grep"],
    reasoning="Read工具更快更准确",
    success=True
)

# 记住上下文
memory.remember_context(
    topic="多Agent开发",
    summary="创建了演示系统",
    key_points=["4个Agent", "工作流编排"],
    tools_used=["Write", "Bash"],
    decisions_made=["使用workflow_engine"],
    outcomes="成功运行"
)

# 回忆相关经验
contexts = memory.recall("多Agent")

# 获取工具建议
tool = memory.suggest_tool("read_file")  # 返回 "Read"

# 学习用户偏好
memory.learn_preferences({
    'coding_style': {'language': 'Python'}
})

# 查看统计
stats = memory.get_memory_stats()
```

### 记忆增强Agent

```python
from 00_Agent_Library.claude_memory import MemoryEnhancedAgent

class MyAgent(MemoryEnhancedAgent):
    def process_task(self, task):
        # 行动前回忆
        past = self.recall_before_action(task.topic)

        # 获取建议
        tool = self.suggest_based_on_experience(task.type)

        # 执行任务
        result = execute(tool, task)

        # 从行动中学习
        self.learn_from_action(
            task_type=task.type,
            tool_used=tool,
            reasoning=f"基于历史选择了{tool}",
            success=result.success
        )
```

## 📊 记忆示例

### contexts.json
```json
{
  "total_contexts": 1,
  "contexts_by_topic": {
    "多Agent系统开发": 1
  },
  "contexts": [
    {
      "timestamp": "2026-01-15T13:17:57.744418",
      "session_id": "session_20260115_131757",
      "topic": "多Agent系统开发",
      "summary": "创建了基于WorkflowEngine的多Agent演示系统",
      "key_points": [
        "实现了4个专门Agent：Coordinator, Analyst, Processor, Reviewer",
        "使用WorkflowGraph进行工作流编排",
        "状态在Agent之间传递"
      ],
      "tools_used": ["Write", "Bash", "Read"],
      "decisions_made": ["使用workflow_engine而非LangGraph"],
      "outcomes": "成功运行演示，展示了Agent协作能力"
    }
  ]
}
```

### decisions.json
```json
{
  "total_decisions": 2,
  "tool_usage_stats": {
    "Read": 1,
    "Grep": 1
  },
  "decisions": [
    {
      "timestamp": "2026-01-15T13:17:57.744418",
      "task_type": "read_file",
      "tool_chosen": "Read",
      "alternatives": ["Bash: cat", "Grep"],
      "reasoning": "Read工具是专门为文件读取设计的，更快更准确",
      "success": true,
      "lesson_learned": "优先使用Read工具读取文件"
    }
  ]
}
```

## 🎯 实际应用场景

### 场景1: 工具选择优化

**问题**: 用户要求"读取文件"

**没有记忆**:
```
我 → 思考: 用什么工具？
    → 可能选择 Bash: cat (不理想)
```

**有记忆**:
```
我 → 查询记忆: suggest_tool("read_file")
    → 记忆返回: "Read" (历史上成功率100%)
    → 直接使用 Read 工具
```

### 场景2: 上下文延续

**问题**: 用户说"继续上次的任务"

**没有记忆**:
```
我 → 什么任务？不知道
    → 询问用户
```

**有记忆**:
```
我 → recall("上次的任务类型")
    → 找到: "多Agent系统开发"
    → 直接继续工作
```

### 场景3: 个性化建议

**问题**: 用户想"搜索代码"

**没有记忆**:
```
我 → 提供通用建议
```

**有记忆**:
```
我 → 查看用户偏好
    → 发现: 用户偏好精确搜索
    → 建议: 使用Grep而非Glob
```

## 🔄 与现有系统集成

### 与记忆助手 (memory_agent) 集成

```python
# memory_agent用于文档和笔记的语义搜索
# claude_memory用于对话上下文和决策记忆

from 01_Active_Projects.memory_agent import MemoryAgent
from 00_Agent_Library.claude_memory import ClaudeMemory

doc_memory = MemoryAgent()  # 文档记忆
conversation_memory = ClaudeMemory()  # 对话记忆

# 互补使用
doc_memory.search("关键词")  # 搜索文档
conversation_memory.recall("主题")  # 回忆对话
```

### 与WorkflowEngine集成

```python
from 00_Agent_Library.workflow_engine import Node
from 00_Agent_Library.claude_memory import MemoryEnhancedAgent

class SmartNode(Node, MemoryEnhancedAgent):
    """具有记忆能力的智能节点"""

    def execute(self, state):
        # 执行前回忆
        past = self.recall_before_action(state['task'])

        # 使用经验决策
        tool = self.suggest_based_on_experience(state['task_type'])

        # 执行并学习
        result = tool.execute(state)
        self.learn_from_action(state['task_type'], tool, "", result.success)

        return state
```

## 📈 进化路径

### 阶段1: 当前 (基础记忆)
- ✅ JSON存储
- ✅ 简单查询
- ✅ 工具统计

### 阶段2: 增强 (语义搜索)
- 🔄 向量嵌入
- 🔄 语义相似度
- 🔄 智能推荐

### 阶段3: 高级 (主动学习)
- ⏳ 自动模式识别
- ⏳ 预测性建议
- ⏳ 跨项目迁移

### 阶段4: 智能 (自我进化)
- ⏳ 元学习
- ⏳ 策略优化
- ⏳ 知识蒸馏

## 🛠️ 运行演示

```bash
cd 00_Agent_Library
python claude_memory.py
```

## 💡 设计原则

1. **轻量级**: 最小化存储和计算开销
2. **可扩展**: 易于添加新的记忆类型
3. **持久化**: 跨会话保持记忆
4. **隐私**: 所有数据存储在本地
5. **可解释**: 记忆结构清晰可读

## 🔐 隐私考虑

- 所有记忆存储在工作区本地
- 不上传到云端
- 用户可随时查看和删除
- 支持选择性遗忘

## 📝 未来改进

- [ ] 添加向量嵌入支持语义搜索
- [ ] 实现记忆重要性评分和自动清理
- [ ] 支持记忆导出和导入
- [ ] 添加可视化界面查看记忆
- [ ] 实现跨工作区的知识迁移
- [ ] 支持记忆版本控制

---

**作者**: Claude Code
**创建日期**: 2026-01-15
**版本**: 1.0.0
