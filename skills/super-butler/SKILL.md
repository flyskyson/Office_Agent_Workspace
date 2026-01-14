# 超级管家技能 (Super Butler)

**描述**: 工作区智能管家，提供全方位的项目管理、工具启动、问题解决服务。当用户说"超级管家"、"管家模式"、"帮我管理"、"工作区状态"时触发。作为整个工作区的统一入口，协调所有智能体和工具的使用。

**🆕 技能热重载测试**: 此技能支持 Claude Code 2.1+ 的热重载功能，修改后无需重启即可生效。（测试时间戳: 2026-01-14）

---

## 概述

超级管家是您的**AI工作区助理**，核心能力：
- 🎯 **智能推荐**: 基于上下文自动推荐相关工具 (v2.0新增)
- 🚀 **工具启动**: 一键启动任何智能体或工具
- 📊 **状态监控**: 实时掌握工作区健康状态
- 🔍 **问题诊断**: 快速定位和解决技术问题
- 📚 **知识检索**: 利用 Memory Agent 搜索代码和解决方案
- 🛠️ **工作流编排**: 多工具协作完成复杂任务
- 🧠 **学习偏好**: 记住您的使用习惯，优化推荐 (v2.0新增)

**核心理念**: "一个入口，全知全能"

**v2.0 升级** (2026-01-14):
- ✨ 集成智能推荐引擎，自动匹配相关工具
- ✨ 支持同义词扩展和语义理解
- ✨ 用户偏好学习机制

---

## 工作区资产清单

### 🤖 核心智能体 (4个)

| 智能体 | 状态 | 端口 | 用途 | 启动命令 |
|--------|------|------|------|----------|
| 🏢 市场监管智能体 | ✅ 生产就绪 | 5000 | 营业执照OCR + 申请书生成 | `python market_supervision_agent/ui/flask_app.py` |
| 🧠 学习记忆助手 | ✅ Web UI完成 | 5555 | 知识管理 + 语义搜索 | `python memory_agent/ui/app.py` |
| 📁 证照整理工具 | 🔄 MVP | - | 智能文件分类 | `python file_organizer/file_organizer.py` |
| 🔐 广西政务登录 | ✅ 可用 | - | 自动登录脚本 | `python 00_Agent_Library/99_Scripts_Tools/广西政务自动登录.py` |

### 🛠️ 实用工具 (39个)

**统一启动器**:
- [office_agent_studio.py](../../office_agent_studio.py) - CLI菜单式启动器

**工作区维护**:
- workspace_scanner.py - 扫描并索引工作区
- workspace_cleaner.py - 清理缓存和临时文件
- workspace_report.py - 生成健康报告
- workspace_maintenance.py - 定期维护

**脚本工具**:
- 启动_OA_Studio.bat - 快速启动
- 创建桌面快捷方式脚本
- 版本管理工具

---

## 执行步骤

### 步骤 1: 激活管家模式

**检测触发词**：
```
用户说: "超级管家"、"管家模式"、"工作区状态"、"帮我管理"
    ↓
自动激活超级管家技能
    ↓
调用智能推荐引擎分析意图
    ↓
显示工作区概览 + 推荐工具 + 可用操作
```

**响应模板 (v2.0 增强)**：
```
# 🤖 超级管家模式已激活

您好！我是您的智能工作区管家。

## 📊 工作区状态
- 活跃项目: X个
- 可用工具: XX个
- Python版本: 3.12.9

## 🎯 智能推荐
[根据上下文自动推荐相关工具]

## 💡 我还能帮您
[列出其他常见操作选项]
```

**集成智能推荐引擎**：
```python
# 在超级管家中调用推荐引擎
from smart_recommender import SmartRecommender

recommender = SmartRecommender()
recommendations = recommender.recommend_tools(user_input)

# 显示推荐结果
for rec in recommendations:
    print(f"- {rec['name']}: {rec['reason']}")
```

---

### 步骤 2: 智能需求评估 (v2.0)

**使用推荐引擎自动识别意图**：
```python
# 用户输入分析
from smart_recommender import recommend

# 示例场景
user_inputs = [
    "我要生成个体工商户申请书",
    "帮我整理桌面文件",
    "查看最近的AI新闻",
    "搜索之前的笔记"
]

for input_text in user_inputs:
    print(f"用户: {input_text}")
    print(recommend(input_text))
    print("-" * 50)
```

**自动需求分类**：

| 需求类型 | 示例问题 | 自动推荐 | 对应操作 |
|---------|---------|---------|---------|
| **工具启动** | "启动市场监管" | 市场监管智能体 🔥80% | 调用对应智能体 |
| **代码搜索** | "找文件读取代码" | 学习记忆助手 ✨60% | 使用 Memory Agent 搜索 |
| **问题解决** | "为什么报错" | 知识索引器 💡50% | 查找历史解决方案 |
| **工作区管理** | "清理缓存" | 文件整理工具 💡40% | 运行维护工具 |
| **开发协助** | "创建新工具" | 超级管家 | 引导开发流程 |

---

### 步骤 3: 执行任务

#### 3.1 启动工具

**使用统一启动器**：
```bash
python office_agent_studio.py
# 或双击: 启动_OA_Studio.bat
```

**直接启动特定工具**：
```bash
# 市场监管智能体
python 01_Active_Projects/market_supervision_agent/ui/flask_app.py

# 学习记忆助手
python 01_Active_Projects/memory_agent/ui/app.py
```

#### 3.2 搜索代码/知识

**使用 Memory Agent Web UI**：
```bash
cd 01_Active_Projects/memory_agent
python ui/app.py
# 访问 http://127.0.0.1:5555
```

**命令行搜索**：
```bash
python memory_agent.py search "查询内容"
python memory_agent.py code "代码功能"
python memory_agent.py similar "问题描述"
```

#### 3.3 问题诊断

**诊断流程**：
```
1. 确认问题类型
   - 代码错误 → 搜索历史解决方案
   - 环境问题 → 检查依赖和配置
   - 工具故障 → 查看错误日志

2. 查找解决方案
   - Memory Agent 搜索类似问题
   - 查看 CLAUDE.md 文档
   - 检查 Skills 文档

3. 提供解决方案
   - 步骤化指导
   - 代码示例
   - 预防措施
```

#### 3.4 工作区维护

**日常维护**：
```bash
# 扫描工作区
python workspace_scanner.py

# 清理缓存
python workspace_cleaner.py

# 生成报告
python workspace_report.py
```

---

### 步骤 4: 跟进和反馈

**任务完成后**：
```
✅ 任务已完成

[详细说明结果]

💡 建议:
- [相关建议]
- [优化方向]

需要其他帮助吗？
```

---

## 使用场景

### 场景 1: 智能工具推荐 (v2.0 新增)

```
你: 我要生成个体工商户开业申请书

我: 💡 **为您推荐以下工具:**

    1. **申请书生成器** 🔥 匹配度: 80%
       └─ OCR识别 + Word模板填充
       └─ 检测到关键词: 申请书, 生成
       └─ 技能: application-generator

    2. **市场监管智能体** 💡 匹配度: 32%
       └─ 营业执照 OCR + 申请书自动生成
       └─ 检测到关键词: 申请书, 个体工商户
       └─ 启动: `python .../flask_app.py`
       └─ 访问: http://127.0.0.1:5000

    💬 需要我帮您启动吗？说"启动"即可
```

---

### 场景 2: 同义词智能匹配 (v2.0 新增)

```
你: 我要填个表格

我: 💡 **为您推荐以下工具:**

    1. **申请书生成器** 💡 匹配度: 40%
       └─ OCR识别 + Word模板填充
       └─ 检测到关键词: 表格
       └─ 技能: application-generator

    💬 需要我帮您启动吗？
```

---

### 场景 3: 日常工具使用

```
你: 超级管家，启动市场监管智能体

我: 好的，正在启动市场监管智能体...

    ✅ 服务启动成功！
    📱 访问地址: http://127.0.0.1:5000
    💡 提示: 浏览器已自动打开

    需要帮助使用吗？我可以：
    - 解释功能
    - 排查问题
    - 生成测试数据
```

---

### 场景 4: 代码检索

```
你: 管家，找一下批量重命名文件的代码

我: 好的，正在搜索您的代码库...

    🔍 在 file_organizer.py 中找到相关代码：
    📄 函数: batch_rename_files()
    📍 位置: 第45-67行

    [显示代码片段]

    需要详细说明或修改建议吗？
```

---

### 场景 5: 问题解决

```
你: 为什么我的 Flask 应用启动失败？

我: 让我帮您诊断...

    🔍 问题分析：
    - 检查端口占用... ✅ 端口5000可用
    - 检查依赖... ❌ 缺少 flask 模块
    - 检查配置... ✅ 配置正常

    💡 解决方案：
    1. 安装依赖: pip install flask
    2. 重新启动应用

    [提供详细命令]

    要我帮您执行吗？
```

---

### 场景 6: 工作区优化

```
你: 管家，帮我优化工作区

我: 好的，正在生成优化建议...

    📊 工作区健康报告：
    - 项目数量: 5个
    - 代码行数: ~50,000行
    - 缓存大小: 256MB (建议清理)

    🎯 优化建议：
    1. 清理 Python 缓存 (节省空间)
    2. 更新依赖版本 (提升性能)
    3. 统一编码规范 (提高兼容性)

    要我执行优化吗？
```

---

## 常见操作

### 启动任何工具

**命令格式**：
```
"启动 [工具名]"
"打开 [智能体]"
"运行 [工具]"
```

**示例**：
```
"启动市场监管"
"打开记忆助手"
"运行清理工具"
```

---

### 搜索代码

**命令格式**：
```
"找 [代码功能]"
"搜索 [关键词]"
"查一下 [问题描述]"
```

**示例**：
```
"找文件读取代码"
"搜索 OCR识别"
"查一下数据库连接"
```

---

### 管理工作区

**命令格式**：
```
"清理缓存"
"生成报告"
"检查状态"
```

---

## 错误处理

### 工具启动失败

**诊断步骤**：
```
1. 检查 Python 版本 (需要 3.12)
   py -3.12 --version

2. 检查依赖安装
   pip list | grep [模块名]

3. 检查端口占用
   netstat -an | findstr [端口号]

4. 查看错误日志
   [工具目录]/logs/
```

---

### 搜索无结果

**建议**：
```
1. 尝试不同的关键词
2. 检查是否已构建索引
3. 确认搜索范围（代码/笔记/全部）
```

---

## 工作流编排

### 复杂任务：处理营业执照到生成申请书

```
你: 管家，处理这批营业执照，生成所有申请书

我: 好的，这是多步骤任务，我来编排：

    📋 执行计划：
    1. ✅ 整理上传的图片
    2. ✅ 批量 OCR 识别
    3. ✅ 验证识别结果
    4. ✅ 生成申请书
    5. ✅ 质量检查
    6. ✅ 打包输出

    开始执行...
    [进度显示]

    ✅ 全部完成！
    📦 输出位置: generated_applications/batch_20260113.zip

    需要我发送邮件或归档吗？
```

---

## 配置和自定义

### 个性化设置

创建 `skills/super-butler/config.json`:
```json
{
  "preferred_tools": {
    "code_editor": "vscode",
    "browser": "chrome",
    "python": "3.12"
  },
  "auto_actions": {
    "clean_cache": "weekly",
    "backup": "daily",
    "index": "on_change"
  },
  "notifications": {
    "errors": true,
    "updates": true,
    "tips": true
  }
}
```

---

## 最佳实践

### 1. 定期维护
```bash
# 每周运行
python workspace_cleaner.py

# 每月运行
python workspace_report.py
python workspace_scanner.py
```

### 2. 保持索引更新
```bash
# 代码变更后
python memory_agent/memory_agent.py index
```

### 3. 版本控制
```bash
# 重要更新后
git add .
git commit -m "feat: 更新描述"
```

---

## 局限说明

**本技能无法处理**：
- ❌ 超出工作区范围的任务
- ❌ 需要外部API的付费服务
- ❌ 违反法律法规的操作

**需要人工介入**：
- ⚠️ 复杂的架构决策
- ⚠️ 安全性敏感的操作
- ⚠️ 大规模数据处理

---

## 相关技能

- **[application-generator](../application-generator/SKILL.md)** - 申请书生成
- **[license-organizer](../license-organizer/SKILL.md)** - 证照整理
- **[knowledge-indexer](../knowledge-indexer/SKILL.md)** - 知识索引

---

## 相关文件

- **[CLAUDE.md](../../CLAUDE.md)** - 项目配置
- **[office_agent_studio.py](../../office_agent_studio.py)** - 统一启动器
- **[workspace_memory/](../../06_Learning_Journal/workspace_memory/)** - 工作区记忆

---

## 版本历史

- **v2.0** (2026-01-14): 集成智能推荐引擎，支持自动工具推荐和同义词匹配
- **v1.0** (2026-01-13): 初始版本，统一工作区管理

---

**技能触发关键词**: `超级管家`、`管家模式`、`工作区状态`、`帮我管理`、`工作区概览`

**推荐引擎集成**: [00_Agent_Library/smart_recommender.py](../../00_Agent_Library/smart_recommender.py)
