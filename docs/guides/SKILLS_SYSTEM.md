# 🤖 技能系统详解

本指南详细说明 **Claude Code Skills 系统** 的工作原理和使用方法。

---

## 🎯 技能系统概览

### 核心概念

**技能 (Skill)** = **触发关键词** + **执行步骤** + **验证标准**

```
用户输入
    ↓
关键词检测
    ↓
技能匹配
    ↓
加载 SKILL.md
    ↓
执行步骤清单
    ↓
返回结果
```

### 与CLAUDE.md的关系

| 维度 | CLAUDE.md | Skills (SKILL.md) |
|------|-----------|------------------|
| **性质** | 项目百科全书 | 任务执行清单 |
| **加载时机** | 每次对话开始 | 检测到关键词时 |
| **内容范围** | 项目结构、规范、工具 | 具体任务流程 |
| **类比** | 建筑蓝图 | 施工手册 |

---

## 📂 技能目录结构

```
skills/
├── idea-to-product/         # 想法落地技能
│   └── SKILL.md
├── super-butler/            # 超级管家技能
│   └── SKILL.md
├── application-generator/   # 申请书生成技能
│   └── SKILL.md
├── license-organizer/       # 证照整理技能
│   └── SKILL.md
└── knowledge-indexer/       # 知识索引技能
    └── SKILL.md
```

---

## 🎭 技能工作流程

### 1. 触发阶段

```python
# 用户输入
user_input = "帮我生成个体工商户申请书"

# 关键词匹配
keywords = ["申请书", "申请表", "个体工商户开业"]
matched = any(kw in user_input for kw in keywords)
# → True，触发 application-generator 技能
```

### 2. 加载阶段

```python
# 加载技能文档
skill_path = "skills/application-generator/SKILL.md"
skill_content = read_file(skill_path)

# 解析步骤
steps = parse_skill_steps(skill_content)
```

### 3. 执行阶段

```python
# 按步骤执行
for step in steps:
    result = execute_step(step)
    if not result.success:
        return handle_error(result.error)
```

### 4. 验证阶段

```python
# 验证结果
validation = validate_result(result, skill.validation_criteria)
if validation.passed:
    return result
else:
    return retry_or_fail(validation.errors)
```

---

## 📝 SKILL.md 格式规范

### 基本结构

```markdown
# 技能名称 (简短描述)

**技能类型**: automation/development/guide
**触发关键词**: 关键词1, 关键词2, 关键词3
**执行时间**: 预估耗时

---

## 🎯 技能概述

详细描述技能的功能和适用场景

---

## 🔄 执行步骤

### 步骤1: 步骤名称

**目标**: 这一步要达成什么
**操作**:
1. 子操作1
2. 子操作2
**验证**: 如何确认这一步完成

### 步骤2: 步骤名称

...

---

## ✅ 成功标准

- [ ] 标准1
- [ ] 标准2

---

## 🐛 常见问题

### Q: 问题1?
A: 解决方案

---

## 📚 相关资源

- 相关文档链接
- 代码示例
```

### 示例: 申请书生成技能

```markdown
# 申请书生成技能

**技能类型**: automation
**触发关键词**: 生成申请书, 填写申请表, 个体工商户开业
**执行时间**: 2-5分钟

---

## 🎯 技能概述

使用OCR技术识别营业执照信息，自动填充Word模板生成申请书。

---

## 🔄 执行步骤

### 步骤1: 确认材料准备

**目标**: 确认所有必要文件已准备
**操作**:
1. 检查营业执照图片是否存在
2. 确认模板文件完整
**验证**: 文件存在且可访问

### 步骤2: 选择OCR工具

**目标**: 选择合适的OCR工具
**操作**:
1. 询问用户偏好（百度/PaddleOCR）
2. 检查API密钥（如果使用百度OCR）
**验证**: OCR工具可用

### 步骤3: 执行识别

**目标**: 提取营业执照信息
**操作**:
1. 调用OCR API
2. 解析返回结果
3. 验证关键字段
**验证**: 所有必要字段已提取

### 步骤4: 填充模板

**目标**: 生成Word文档
**操作**:
1. 加载YAML配置
2. 映射数据到模板变量
3. 使用Jinja2渲染
4. 生成最终文档
**验证**: 文档生成成功

### 步骤5: 质量检查

**目标**: 确保输出质量
**操作**:
1. 检查文档完整性
2. 验证关键信息正确性
3. 检查格式和排版
**验证**: 通过质量检查清单

---

## ✅ 成功标准

- [ ] OCR识别准确率 > 95%
- [ ] 所有必要字段已填充
- [ ] 文档格式正确
- [ ] 文件成功保存

---

## 🐛 常见问题

### Q: OCR识别不准确?
A: 尝试提高图片质量，或使用百度OCR（精度更高）

### Q: 模板填充失败?
A: 检查YAML配置文件，确保字段映射正确

---

## 📚 相关资源

- [市场监管智能体文档](../../01_Active_Projects/market_supervision_agent/)
- [Jinja2模板引擎](https://jinja.palletsprojects.com/)
```

---

## 🚀 创建新技能

### 步骤1: 确定技能范围

**问题**: 这个技能解决什么问题？

**示例**:
```
问题: 用户经常需要批量重命名文件
解决: 创建"批量重命名"技能
```

### 步骤2: 定义触发关键词

**原则**:
- 使用自然语言
- 覆盖常见表达
- 避免歧义

**示例**:
```python
# ✅ 好的关键词
["批量重命名", "文件重命名", "重命名文件"]

# ❌ 避免模糊关键词
["重命名"]  # 可能匹配到不相关的场景
```

### 步骤3: 编写SKILL.md

**模板**:
```markdown
# 技能名称

**技能类型**: automation
**触发关键词**: 关键词1, 关键词2
**执行时间**: 预估时间

---

## 🎯 技能概述

简要描述技能功能

---

## 🔄 执行步骤

### 步骤1: ...
...

---

## ✅ 成功标准
...
```

### 步骤4: 测试技能

```bash
# 测试技能触发
echo "批量重命名文件" | test_skill_trigger

# 测试技能执行
python skills/your_skill/test.py
```

### 步骤5: 注册技能

在 [CLAUDE.md](../../CLAUDE.md) 中添加:

```markdown
| **技能名称** | "关键词1", "关键词2" | [SKILL.md](skills/your-skill/SKILL.md) |
```

---

## 🎯 内置技能详解

### 1. 想法落地 (idea-to-product)

**功能**: 从模糊想法到可用产品

**触发关键词**:
- "我有个想法"
- "想添加功能"
- "能不能实现"

**执行流程**:
1. 理解与澄清 (10分钟)
2. 探索与分析 (5分钟)
3. 方案设计 (15分钟)
4. 快速原型 (20分钟)
5. 验证迭代 (10分钟)

**详细文档**: [IDEA_WORKFLOW.md](IDEA_WORKFLOW.md)

### 2. 超级管家 (super-butler)

**功能**: 统一工作区管理

**触发关键词**:
- "超级管家"
- "管家模式"
- "工作区状态"

**核心能力**:
- 🎯 工具启动
- 📊 状态监控
- 🔍 问题诊断
- 📚 知识检索
- 🛠️ 工作流编排

### 3. 申请书生成 (application-generator)

**功能**: OCR识别 + Word模板填充

**触发关键词**:
- "生成申请书"
- "填写申请表"
- "个体工商户开业"

**技术栈**:
- OCR: 百度OCR / PaddleOCR
- 模板: Jinja2
- 文档: python-docx

### 4. 证照整理 (license-organizer)

**功能**: 智能识别 + 自动分类归档

**触发关键词**:
- "整理证照"
- "归类文件"
- "归档证件"

**工作流程**:
1. 扫描目标目录
2. OCR识别文件内容
3. 根据规则分类
4. 移动到对应文件夹
5. 生成整理报告

### 5. 知识索引 (knowledge-indexer)

**功能**: 向量化索引 + 语义搜索

**触发关键词**:
- "索引笔记"
- "更新知识库"
- "构建索引"

**技术栈**:
- 向量化: sentence-transformers
- 存储: ChromaDB
- 检索: 语义相似度搜索

---

## 🔧 技能系统API

### 手动触发技能

```python
from skills.skill_manager import SkillManager

manager = SkillManager()

# 触发技能
result = manager.trigger_skill(
    skill_name="application-generator",
    params={
        "image_path": "license.jpg",
        "output_dir": "output/"
    }
)
```

### 列出可用技能

```python
skills = manager.list_skills()
for skill in skills:
    print(f"{skill.name}: {skill.description}")
```

### 注册新技能

```python
manager.register_skill(
    name="my-custom-skill",
    path="skills/my_custom_skill/SKILL.md",
    keywords=["custom", "my skill"]
)
```

---

## 💡 最佳实践

### 1. 技能设计原则

**单一职责**: 每个技能专注一个任务
**可组合**: 技能之间可以组合使用
**可测试**: 每个步骤都有验证标准
**可维护**: 清晰的文档和代码

### 2. 关键词选择

**自然语言**: 使用用户常用的表达
**避免冲突**: 不要与其他技能重叠
**覆盖全面**: 考虑多种表达方式

### 3. 错误处理

**友好提示**: 清晰的错误信息
**恢复建议**: 提供解决方案
**日志记录**: 详细的调试信息

---

## 🐛 故障排查

### 问题: 技能未触发

**诊断**:
```python
# 检查关键词匹配
from skills.skill_manager import SkillManager

manager = SkillManager()
matches = manager.find_matching_skills("用户输入")
print(matches)
```

**解决**:
- 检查关键词配置
- 确认技能文档格式正确
- 验证技能路径

### 问题: 执行失败

**诊断**:
```python
# 启用调试模式
manager.set_debug_mode(True)
result = manager.trigger_skill(...)
print(result.debug_info)
```

**解决**:
- 检查步骤依赖
- 验证输入参数
- 查看错误日志

---

## 📚 相关文档

- [完整系统指南](../../COMPLETE_SYSTEM_GUIDE.md)
- [架构设计](../ARCHITECTURE.md)
- [想法落地工作流](IDEA_WORKFLOW.md)
- [扩展开发](AGENT_DEVELOPMENT.md)

---

## 🚀 下一步

1. **使用技能**: 尝试触发内置技能
2. **创建技能**: 开发自定义技能
3. **扩展系统**: 增强技能功能
4. **分享经验**: 贡献技能到社区

**祝您使用愉快!** 🎉
