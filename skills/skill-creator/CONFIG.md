# Skill Creator 配置说明

## 概述

Skill Creator 本身不需要配置文件，但它创建的技能可能需要配置。本文档说明：

1. **Skill Creator CLI** 的命令行参数
2. **被创建技能** 的配置文件模板
3. **工作区级别** 的技能相关配置

---

## Skill Creator CLI 参数

### create 命令参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--name` | string | ✅ | - | 技能名称（kebab-case） |
| `--description` | string | ✅ | - | 技能描述 |
| `--category` | string | ❌ | general | 技能分类 |
| `--triggers` | list | ❌ | [] | 触发关键词列表 |
| `--author` | string | ❌ | "" | 作者名称 |
| `--no-layered` | flag | ❌ | false | 不创建分层文档 |

**示例**:
```bash
python skill_creator.py create \
  --name "my-skill" \
  --description "我的技能" \
  --category "automation" \
  --triggers "关键词1 关键词2" \
  --author "Your Name"
```

---

### validate 命令参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--path` | string | ❌ | null | 技能路径（默认验证所有） |

**示例**:
```bash
# 验证所有技能
python skill_creator.py validate

# 验证单个技能
python skill_creator.py validate --path "skills/my-skill"
```

---

### list 命令参数

无参数。

**示例**:
```bash
python skill_creator.py list
```

---

### init 命令参数

无参数。

**示例**:
```bash
python skill_creator.py init
```

---

## 技能分类系统

Skill Creator 使用以下分类系统：

| 分类 | 图标 | 适用场景 | 示例 |
|------|------|---------|------|
| **automation** | ⚙️ | 自动化任务、批处理 | 文件备份、批量重命名 |
| **analysis** | 🔍 | 数据分析、日志解析 | 日志分析、数据统计 |
| **development** | 💻 | 代码生成、重构 | 代码生成、测试工具 |
| **management** | 📊 | 项目管理、文件组织 | 项目管理、文件整理 |
| **general** | 🔧 | 通用工具、辅助功能 | 超级管家、帮助系统 |

**配置方式**:
```bash
--category "automation"
```

---

## 被创建技能的配置模板

### 技能配置文件（可选）

如果技能需要配置，可以在技能目录下创建 `config.json`:

```json
{
  "skill_name": "my-skill",
  "version": "1.0",
  "settings": {
    "enabled": true,
    "auto_trigger": true,
    "priority": 50
  },
  "parameters": {
    "param1": "value1",
    "param2": 42
  }
}
```

**示例** (file-backup 技能):
```json
{
  "skill_name": "file-backup",
  "version": "1.0",
  "settings": {
    "default_source": "~/Documents",
    "default_target": "~/Backups",
    "compression": true,
    "incremental": true
  }
}
```

---

### 技能环境变量（可选）

如果技能需要环境变量，可以在 `CONFIG.md` 中说明：

```markdown
## 环境变量

创建 `.env` 文件：

```bash
# 备份目标路径
BACKUP_TARGET=D:/Backups

# 压缩级别 (0-9)
COMPRESSION_LEVEL=6

# 是否增量备份
INCREMENTAL_BACKUP=true
```
```

---

## 工作区级别配置

### skills/.gitignore

Skill Creator 的 `init` 命令会创建此文件：

```bash
# 忽略临时文件
*.tmp
*.bak

# 忽略测试技能
test-*/
```

---

### CLAUDE.md 配置

在项目根目录的 `CLAUDE.md` 中，Skill Creator 相关配置：

```markdown
## Claude Code Skills

工作区配置了 **Claude Code Skills** 系统。

### 可用技能

| 技能名称 | 触发关键词 | 核心功能 |
|---------|-----------|---------|
| **skill-creator** | `创建技能` `新建技能` | 创建和管理 Skills |
| **super-butler** | `超级管家` `管家模式` | 工作区统一管理 |

### Skills 工作原理

[说明技能如何被加载和执行]
```

---

## 技能元信息

### 从 SKILL.md 提取元信息

Skill Creator 会自动从 SKILL.md 提取以下信息：

```markdown
# 技能名称

📝 **描述**: 技能描述
👤 **作者**: 作者名称
```

**提取结果**:
```json
{
  "name": "技能名称",
  "description": "技能描述",
  "author": "作者名称",
  "category": "general"
}
```

---

## 验证配置

### 验证规则

Skill Creator 的 `validate` 命令检查：

| 检查项 | 说明 | 严重级别 |
|--------|------|---------|
| SKILL.md 存在 | 主文件必须存在 | ❌ 错误 |
| 执行步骤章节 | 必须包含"执行步骤" | ⚠️ 警告 |
| 触发条件 | 必须定义触发条件 | ⚠️ 警告 |
| 附加文档 | EXAMPLES.md 等 | ℹ️ 信息 |

**输出示例**:
```
📋 my-skill:
   ✅ 验证通过
   ℹ️  SKILL.md 大小: 1250 字符
   ℹ️  ✅ 找到附加文档: EXAMPLES.md
   ℹ️  ✅ 找到附加文档: CONFIG.md
   ℹ️  ✅ 找到附加文档: TROUBLESHOOTING.md
```

---

## 高级配置

### 自定义模板

虽然 Skill Creator 不支持自定义模板，但您可以：

1. **修改 `skill_creator.py`**: 编辑 `_generate_skill_md()` 方法
2. **创建后修改**: 生成后手动调整 SKILL.md
3. **使用示例**: 复制现有技能作为模板

---

### 批量配置

创建 `skills_config.json`:

```json
{
  "skills": [
    {
      "name": "skill-1",
      "description": "描述1",
      "category": "automation",
      "triggers": ["触发词1", "触发词2"]
    },
    {
      "name": "skill-2",
      "description": "描述2",
      "category": "automation",
      "triggers": ["触发词3"]
    }
  ]
}
```

**批量创建脚本**:
```python
import json
from skill_creator import SkillCreator

# 加载配置
with open("skills_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 批量创建
creator = SkillCreator()
for skill_config in config["skills"]:
    creator.create(**skill_config)
```

---

## 配置最佳实践

### 1. 描述配置

```
好的描述: 功能 + 场景 + 限制
"截图整理工具，自动按日期/应用分类桌面截图。当用户需要'整理截图'时触发。仅支持 PNG/JPG 格式。"

不好的描述: 太简单
"这是一个整理截图的工具。"
```

### 2. 触发词配置

```
好的触发词: 用户自然会说的短语
`整理截图` `截图分类` `清理桌面图片`

不好的触发词: 太正式
`execute screenshot organization protocol`
```

### 3. 分类配置

```
选择最匹配的分类:
- automation: 自动化任务（如备份、压缩）
- analysis: 分析工具（如日志分析、数据统计）
- development: 开发工具（如代码生成、测试）
- management: 管理工具（如项目管理、文件整理）
- general: 通用工具（如超级管家）
```

---

## 常见配置问题

### Q: 如何修改已创建技能的配置？

A: 直接编辑 SKILL.md 文件，不需要重新创建。

### Q: 配置文件放在哪里？

A: 技能配置可以放在：
- 技能目录内: `skills/my-skill/config.json`
- 工作区根目录: `.env` 或 `config.yaml`

### Q: 如何共享配置？

A: 使用 CONFIG.md 说明配置格式，用户可以根据说明创建自己的配置文件。

---

## 配置示例

### 完整技能配置示例

**技能**: file-backup

**SKILL.md**:
```markdown
# File Backup Skill

📝 **描述**: 自动备份文件工具...

## 配置

编辑 `skills/file-backup/config.json`:

```json
{
  "default_source": "~/Documents",
  "default_target": "~/Backups",
  "compression": true,
  "incremental": true
}
```

## 执行步骤
...
```

**config.json**:
```json
{
  "default_source": "~/Documents",
  "default_target": "~/Backups",
  "compression": true,
  "incremental": true,
  "exclude_patterns": ["*.tmp", "*.bak"]
}
```

**CONFIG.md**:
```markdown
## 配置说明

### 基本配置

编辑 `config.json`:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| default_source | string | ~/Documents | 源目录 |
| default_target | string | ~/Backups | 目标目录 |
| compression | boolean | true | 是否压缩 |
| incremental | boolean | true | 是否增量备份 |
...
```

---

## 相关资源

- **CLI 工具**: [00_Agent_Library/skill_creator.py](../../00_Agent_Library/skill_creator.py)
- **使用指南**: [00_Agent_Library/SKILL_CREATOR_GUIDE.md](../../00_Agent_Library/SKILL_CREATOR_GUIDE.md)
- **主配置**: [CLAUDE.md](../../CLAUDE.md)
