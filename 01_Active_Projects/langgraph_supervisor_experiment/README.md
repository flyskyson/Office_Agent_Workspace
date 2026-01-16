# LangGraph Supervisor 对比实验

**实验目标**: 对比 WorkflowEngine Coordinator 与 LangGraph Supervisor

**实验日期**: 2026-01-15

---

## 📊 实验设计

### 对比维度

| 维度 | WorkflowEngine | LangGraph |
|------|----------------|-----------|
| 代码量 | 待测试 | 待测试 |
| 开发时间 | 待测试 | 待测试 |
| 执行效率 | 待测试 | 待测试 |
| 可维护性 | 待测试 | 待测试 |
| 检查点 | ✅ 已实现 | ✅ 原生支持 |
| 可视化 | ✅ 已实现 | ✅ Studio |

### 任务场景

**文档处理团队**:
- Supervisor: 协调任务分配
- Researcher: 研究文档内容
- Writer: 撰写文档
- Reviewer: 审查文档

---

## 📁 项目结构

```
langraph_supervisor_experiment/
├── README.md                    # 本文件
├── version_a_workflow.py       # 版本A: WorkflowEngine
├── version_b_langgraph.py      # 版本B: LangGraph
├── comparison_report.md        # 对比报告
└── test_data/                  # 测试数据
    └── sample_document.txt
```

---

## 🚀 运行实验

```bash
# 运行版本A (WorkflowEngine)
python version_a_workflow.py

# 运行版本B (LangGraph)
python version_b_langgraph.py

# 查看对比报告
cat comparison_report.md
```

---

## 📈 预期结果

### 假设

1. **代码量**: LangGraph 更少（预构建组件）
2. **开发时间**: LangGraph 更快（开箱即用）
3. **执行效率**: 相近（相同逻辑）
4. **可维护性**: LangGraph 更好（标准化）
5. **功能完整性**: LangGraph 更强（Studio、生态）

---

## 🎯 下一步

1. ✅ 安装 LangGraph
2. 🔄 实现版本A
3. ⏳ 实现版本B
4. ⏳ 运行对比测试
5. ⏳ 生成分析报告
