# Skill Creator CLI - 使用指南

**工具**: `00_Agent_Library/skill_creator.py`
**版本**: 1.0
**创建日期**: 2026-01-13

---

## 🎯 快速开始

### 安装

无需安装，直接使用：

```bash
python 00_Agent_Library/skill_creator.py --help
```

### 基本用法

```bash
# 创建新技能
python 00_Agent_Library/skill_creator.py create \
  --name "my-skill" \
  --description "我的技能描述" \
  --category "automation" \
  --triggers "trigger1,trigger2"

# 验证技能
python 00_Agent_Library/skill_creator.py validate --path "skills/my-skill"

# 列出所有技能
python 00_Agent_Library/skill_creator.py list
```

---

## 📋 命令详解

### 1. create - 创建新技能

**语法**:
```bash
python skill_creator.py create [选项]
```

**必需参数**:
| 参数 | 说明 | 示例 |
|------|------|------|
| `--name` | 技能名称（kebab-case） | `--name "data-cleaner"` |
| `--description` | 技能描述 | `--description "数据清洗工具"` |

**可选参数**:
| 参数 | 说明 | 可选值 | 默认值 |
|------|------|--------|--------|
| `--category` | 技能分类 | automation/analysis/development/management/general | general |
| `--triggers` | 触发关键词（空格分隔） | 多个词 | 无 |
| `--author` | 作者名称 | 任意字符串 | 空 |
| `--no-layered` | 不创建分层文档 | 标志 | 创建分层文档 |

**示例**:

```bash
# 简单创建
python skill_creator.py create \
  --name "report-generator" \
  --description "自动生成报告"

# 完整创建
python skill_creator.py create \
  --name "market-analyzer" \
  --description "市场数据分析工具" \
  --category "analysis" \
  --triggers "分析市场 市场报告 数据分析" \
  --author "Your Name"
```

**输出**:
```
✅ 技能创建成功: skills/market-analyzer
   主文件: skills/market-analyzer/SKILL.md
   附加文档: EXAMPLES.md, CONFIG.md, TROUBLESHOOTING.md

💡 下一步:
   1. 编辑 skills/market-analyzer/SKILL.md
   2. 添加执行步骤和示例
   3. 运行: python skill_creator.py validate --path "skills/market-analyzer"
```

---

### 2. validate - 验证技能

**语法**:
```bash
python skill_creator.py validate [--path 路径]
```

**参数**:
| 参数 | 说明 | 示例 |
|------|------|------|
| `--path` | 技能路径（可选） | `--path "skills/my-skill"` |

**行为**:
- **指定路径**: 验证单个技能
- **不指定路径**: 验证所有技能

**示例**:

```bash
# 验证单个技能
python skill_creator.py validate --path "skills/market-analyzer"

# 验证所有技能
python skill_creator.py validate
```

**输出**:
```
📋 market-analyzer:
   ✅ 验证通过
   ℹ️  SKILL.md 大小: 1250 字符
   ℹ️  ✅ 找到附加文档: EXAMPLES.md
   ℹ️  ✅ 找到附加文档: CONFIG.md
   ℹ️  ✅ 找到附加文档: TROUBLESHOOTING.md
```

**验证项目**:
- ✅ SKILL.md 存在
- ✅ 包含必需章节（执行步骤、触发条件）
- ⚠️ 触发关键词定义
- ℹ️ 附加文档（EXAMPLES.md 等）

---

### 3. list - 列出所有技能

**语法**:
```bash
python skill_creator.py list
```

**输出**:
```
📚 找到 5 个技能:

📁 application-generator
   分类: general
   描述: 市场监管申请书自动生成工具...
   路径: skills/application-generator

📁 market-analyzer
   分类: analysis
   描述: 市场数据分析工具...
   路径: skills/market-analyzer
...
```

---

### 4. init - 初始化工作区

**语法**:
```bash
python skill_creator.py init
```

**功能**:
- 创建 `skills/` 目录（如不存在）
- 创建 `skills/.gitignore`

**输出**:
```
✅ 创建 skills/ 目录: /path/to/skills
✅ 创建 .gitignore

💡 工作区初始化完成
   技能目录: /path/to/skills
```

---

## 📁 生成的文件结构

```
skills/
└── your-skill/
    ├── SKILL.md               # 核心指令（精简）
    ├── EXAMPLES.md            # 详细案例
    ├── CONFIG.md              # 配置说明
    └── TROUBLESHOOTING.md     # 故障排查
```

### 文件说明

| 文件 | 用途 | 目标读者 |
|------|------|---------|
| **SKILL.md** | 执行步骤、触发条件、快速示例 | Claude（执行时） |
| **EXAMPLES.md** | 详细使用案例、对话示例 | Claude + 人类 |
| **CONFIG.md** | 环境变量、配置文件、参数说明 | 人类 |
| **TROUBLESHOOTING.md** | 常见问题、调试方法 | Claude + 人类 |

---

## 🎨 技能分类

| 分类 | 图标 | 适用场景 |
|------|------|---------|
| **automation** | ⚙️ | 自动化任务、批处理 |
| **analysis** | 🔍 | 数据分析、日志解析 |
| **development** | 💻 | 代码生成、重构 |
| **management** | 📊 | 项目管理、文件组织 |
| **general** | 🔧 | 通用工具、辅助功能 |

---

## 💡 最佳实践

### 1. 命名规范

**推荐**: kebab-case（小写 + 连字符）
```
✅ data-cleaner
✅ market-analyzer
✅ report-generator

❌ dataCleaner
❌ Market_Analyzer
❌ REPORTGENERATOR
```

### 2. 触发关键词

**原则**: 用户自然会说的短语
```
# 好的触发词
--triggers "生成报告 创建报告 report gen"

# 不好的触发词
--triggers "execute report generation protocol"  # 太正式
```

### 3. 描述撰写

**公式**: 功能 + 场景 + 限制

```
好的描述:
"数据清洗工具，自动去除重复数据、填充缺失值。当用户需要'清洗数据'、'整理表格'时触发。适用于CSV/Excel文件。不支持数据库操作。"

不好的描述:
"这是一个清洗数据的工具。"  # 太简单
```

### 4. 分层文档原则

**SKILL.md 只写**:
- ✅ 核心步骤（1-2-3-4）
- ✅ 快速示例（1个即可）
- ✅ 文件链接

**EXAMPLES.md 写**:
- ✅ 详细案例（多个）
- ✅ 完整对话示例
- ✅ 输入输出对比

**CONFIG.md 写**:
- ✅ 环境变量
- ✅ 配置文件结构
- ✅ 参数说明

**TROUBLESHOOTING.md 写**:
- ✅ 常见错误
- ✅ 解决方案
- ✅ 调试方法

---

## 🚀 高级用法

### 批量创建技能

```bash
# 创建脚本 create_skills.sh
#!/bin/bash
skills=(
  "data-cleaner:数据清洗工具:automation"
  "report-gen:报告生成器:automation"
  "log-analyzer:日志分析:analysis"
)

for skill in "${skills[@]}"; do
  IFS=':' read -r name desc category <<< "$skill"
  python skill_creator.py create \
    --name "$name" \
    --description "$desc" \
    --category "$category"
done
```

### 集成到项目

**在 `Makefile` 中添加**:
```makefile
.PHONY: skill-create skill-validate skill-list

skill-create:
	python 00_Agent_Library/skill_creator.py create $(ARGS)

skill-validate:
	python 00_Agent_Library/skill_creator.py validate

skill-list:
	python 00_Agent_Library/skill_creator.py list
```

**使用**:
```bash
make skill-create ARGS="--name 'new-skill' --description 'My skill'"
make skill-validate
```

### Git 钩子

**`.git/hooks/pre-commit`**:
```bash
#!/bin/bash
# 提交前验证技能
python 00_Agent_Library/skill_creator.py validate
if [ $? -ne 0 ]; then
  echo "技能验证失败，请修复后再提交"
  exit 1
fi
```

---

## 🔧 故障排查

### 问题: Python 路径错误

**症状**:
```
python: can't open file 'skill_creator.py'
```

**解决**:
```bash
# 使用完整路径
python "00_Agent_Library/skill_creator.py" --help

# 或添加到 PATH
export PATH="$PATH:$(pwd)/00_Agent_Library"
skill_creator.py --help
```

### 问题: 编码错误（Windows）

**症状**: 终端中文乱码

**解决**: 工具已内置编码修复，如仍有问题：
```bash
# 设置终端编码
chcp 65001
python "00_Agent_Library/skill_creator.py" --help
```

### 问题: 技能目录已存在

**症状**:
```
❌ 错误: 技能已存在: skills/my-skill
```

**解决**:
```bash
# 删除旧技能（谨慎！）
rm -rf skills/my-skill

# 或重新创建
python skill_creator.py create --name "my-skill-v2" ...
```

---

## 📊 对比手动创建

| 维度 | 手动创建 | Skill Creator |
|------|---------|---------------|
| **时间** | 5-10 分钟 | 10 秒 |
| **规范性** | ❌ 不统一 | ✅ 标准化 |
| **分层文档** | ❌ 经常忘记 | ✅ 自动创建 |
| **验证** | ❌ 手动检查 | ✅ 自动验证 |
| **维护性** | 🟡 中等 | 🟢 高 |

---

## 🤝 贡献

发现问题或建议改进？

**提交反馈**:
- 创建 Issue: [GitHub Issues](链接)
- 提交 PR: [GitHub PRs](链接)

---

## 📝 更新日志

### v1.0 (2026-01-13)
- ✅ 初始版本
- ✅ create/validate/list/init 命令
- ✅ 分层文档结构
- ✅ Windows 编码支持

---

**相关文档**:
- [CLAUDE.md](../CLAUDE.md) - 项目配置
- [skills/](../skills/) - 技能目录
- [00_Agent_Library/EVOLUTION_GUIDE.md](EVOLUTION_GUIDE.md) - 演进系统
