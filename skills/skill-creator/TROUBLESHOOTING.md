# Skill Creator 故障排查

## 常见问题

### 问题 1: 技能目录已存在

**症状**:
```
❌ 错误: 技能已存在: skills/screenshot-organizer
```

**原因**:
- 之前创建过同名技能
- 目录已存在但不是技能目录

**解决方案**:

**方案 A: 删除旧技能**（谨慎！会丢失所有内容）
```bash
# Windows
rmdir /s /q skills\screenshot-organizer

# Linux/Mac
rm -rf skills/screenshot-organizer
```

**方案 B: 创建新版本**
```bash
# 使用版本号
python skill_creator.py create --name "screenshot-organizer-v2" ...
```

**方案 C: 查看现有技能**
```bash
# 先查看现有内容
ls skills/screenshot-organizer/

# 如果是误报，可以手动清理
```

---

### 问题 2: 验证失败 - 缺少必需章节

**症状**:
```
📋 my-skill:
   ⚠️  缺少推荐章节: ## 执行步骤
   ℹ️  SKILL.md 大小: 560 字符
```

**原因**:
- SKILL.md 不完整
- 手动编辑时删除了必需章节

**解决方案**:

**方案 A: 手动补充**
```markdown
# 添加到 SKILL.md

## 执行步骤

### 步骤 1: [步骤名称]

简短描述这一步做什么。

**关键文件/命令**:
```bash
# 示例命令
```

### 步骤 2: [步骤名称]
...
```

**方案 B: 参考完整示例**
```bash
# 查看完整技能示例
cat skills/super-butler/SKILL.md

# 复制相关章节到您的技能
```

**方案 C: 重新创建**
```bash
# 删除不完整的技能
rmdir /s /q skills\my-skill

# 重新创建
python skill_creator.py create --name "my-skill" ...
```

---

### 问题 3: 编码错误（Windows）

**症状**:
```
UnicodeEncodeError: 'utf-8' codec can't encode character...
```

**原因**:
- Windows 终端默认编码不是 UTF-8
- SKILL.md 包含中文字符

**解决方案**:

**方案 A: 设置终端编码**
```bash
# CMD
chcp 65001

# PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

**方案 B: 使用工具内置修复**
```bash
# skill_creator.py 已内置编码修复
# 如果仍有问题，检查文件编码
```

**方案 C: 保存为 UTF-8 with BOM**
```bash
# 使用支持 UTF-8 with BOM 的编辑器
# 如 VSCode、Notepad++
```

---

### 问题 4: Python 路径错误

**症状**:
```
python: can't open file 'skill_creator.py': [Errno 2] No such file or directory
```

**原因**:
- 不在项目根目录
- 路径不正确

**解决方案**:

**方案 A: 使用完整路径**
```bash
python "c:\Users\flyskyson\Office_Agent_Workspace\00_Agent_Library\skill_creator.py" list
```

**方案 B: 切换到项目根目录**
```bash
cd c:\Users\flyskyson\Office_Agent_Workspace
python 00_Agent_Library\skill_creator.py list
```

**方案 C: 使用启动脚本**
```bash
"00_Agent_Library/99_Scripts_Tools/skill_creator.bat" list
```

---

### 问题 5: 技能无法被 Claude 识别

**症状**:
- 创建了技能但 Claude 不响应触发词
- `list` 命令看不到新技能

**原因**:
- SKILL.md 描述不清晰
- 触发关键词不合理
- Claude 需要重启

**解决方案**:

**方案 A: 检查技能列表**
```bash
python skill_creator.py list

# 确认技能在列表中
```

**方案 B: 验证技能**
```bash
python skill_creator.py validate --path "skills/my-skill"
```

**方案 C: 优化触发关键词**
```markdown
# 好的触发词: 用户自然会说的
`整理截图` `截图分类` `清理桌面图片`

# 不好的触发词: 太正式
`execute screenshot organization protocol`
```

**方案 D: 重启 Claude Code**
```
完全退出 Claude Code 并重新启动
```

---

### 问题 6: 分层文档生成失败

**症状**:
```
✅ 技能创建成功: skills/my-skill
   主文件: skills/my-skill/SKILL.md
   # 缺少: EXAMPLES.md, CONFIG.md, TROUBLESHOOTING.md
```

**原因**:
- 使用了 `--no-layered` 参数
- 磁盘空间不足
- 权限问题

**解决方案**:

**方案 A: 不使用 `--no-layered`**
```bash
# 正确创建（会生成分层文档）
python skill_creator.py create --name "my-skill" --description "..."

# 错误创建（不会生成分层文档）
python skill_creator.py create --name "my-skill" --description "..." --no-layered
```

**方案 B: 手动创建分层文档**
```bash
# 复制模板
cp skills/super-butler/EXAMPLES.md skills/my-skill/
cp skills/super-butler/CONFIG.md skills/my-skill/
cp skills/super-butler/TROUBLESHOOTING.md skills/my-skill/
```

**方案 C: 检查磁盘空间**
```bash
# Windows
wmic logicaldisk get name,freespace

# 清理空间
python workspace_cleaner.py
```

---

### 问题 7: Git 追踪问题

**症状**:
```
$ git status
Untracked files:  (use "git add <file>..." to include in what will be committed)
        skills/my-skill/
```

**原因**:
- 新技能未被 Git 追踪

**解决方案**:

**方案 A: 添加到 Git**
```bash
git add skills/my-skill/
git commit -m "feat: 添加 my-skill 技能"
```

**方案 B: 检查 .gitignore**
```bash
# 确保 skills/ 不在 .gitignore 中
cat .gitignore

# 如果有，删除该行
```

**方案 C: 强制添加**
```bash
git add -f skills/my-skill/SKILL.md
```

---

## 调试模式

### 启用详细日志

虽然 skill_creator.py 没有专门的调试模式，但可以：

**方案 A: 使用 Python 详细输出**
```bash
python -v 00_Agent_Library/skill_creator.py create ...
```

**方案 B: 添加调试打印**
```python
# 编辑 skill_creator.py
def create(self, ...):
    print(f"DEBUG: Creating skill {name}")  # 添加调试信息
    ...
```

**方案 C: 使用 IDE 调试**
```bash
# 使用 VSCode 调试
code 00_Agent_Library/skill_creator.py
```

---

## 验证工具

### 完整验证流程

```bash
# 1. 验证所有技能
python skill_creator.py validate

# 2. 列出所有技能
python skill_creator.py list

# 3. 检查特定技能
python skill_creator.py validate --path "skills/my-skill"

# 4. 查看技能内容
cat skills/my-skill/SKILL.md

# 5. 检查文件结构
ls skills/my-skill/
```

---

## 获取帮助

### 文档资源

- **使用指南**: [00_Agent_Library/SKILL_CREATOR_GUIDE.md](../../00_Agent_Library/SKILL_CREATOR_GUIDE.md)
- **完整示例**: [skills/super-butler/SKILL.md](../super-butler/SKILL.md)
- **项目配置**: [CLAUDE.md](../../CLAUDE.md)

### 诊断信息收集

如果问题无法解决，收集以下信息：

```bash
# 1. Python 版本
python --version

# 2. 工作区状态
python skill_creator.py list

# 3. 错误详情
# 完整的错误堆栈信息

# 4. 操作系统
# Windows / Linux / Mac 版本

# 5. 复现步骤
# 详细描述如何触发问题
```

---

## 常见错误代码

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `FileExistsError` | 技能已存在 | 删除旧技能或使用新名称 |
| `UnicodeEncodeError` | 编码问题 | 设置终端为 UTF-8 |
| `FileNotFoundError` | 路径错误 | 使用完整路径 |
| `PermissionError` | 权限不足 | 以管理员身份运行 |
| `ValueError` | 参数无效 | 检查命令行参数 |

---

## 预防措施

### 1. 定期验证

```bash
# 每次创建后验证
python skill_creator.py create ... && python skill_creator.py validate
```

### 2. 使用版本控制

```bash
# 创建前提交
git commit -am "WIP: before creating new skill"

# 创建后提交
git add skills/ && git commit -m "feat: add new skill"
```

### 3. 备份重要技能

```bash
# 备份到归档目录
cp -r skills/my-skill 02_Project_Archive/skill_backups/
```

### 4. 遵循命名规范

```bash
# 使用 kebab-case
✅ my-skill
✅ file-backup
✅ screenshot-organizer

❌ mySkill
❌ file_backup
❌ ScreenshotOrganizer
```

---

## 常见使用错误

### 错误 1: 混淆 CLI 和 Skill

```
错误理解: 认为需要运行 skill_creator.py 才能使用技能

正确理解:
- skill_creator.py 是创建技能的工具
- 创建后的技能由 Claude Code 直接加载
- 不需要运行任何命令
```

### 错误 2: 忘记生成分层文档

```
错误做法: python skill_creator.py create ... --no-layered

正确做法: python skill_creator.py create ...
# 默认会生成分层文档，不需要 --no-layered
```

### 错误 3: 描述过于简单

```
错误描述: "这是一个工具。"

正确描述: "文件备份工具，自动备份指定目录。当用户需要'备份文件'、'自动备份'时触发。支持增量备份和压缩。"
```

---

## 性能问题

### 问题: 创建大量技能时很慢

**解决方案**:

```bash
# 批量创建脚本
import json
from skill_creator import SkillCreator

creator = SkillCreator()

# 批量创建（不验证）
for skill in skills:
    creator.create(...)

# 最后统一验证
creator.validate()
```

---

## 相关资源

- **核心工具**: [00_Agent_Library/skill_creator.py](../../00_Agent_Library/skill_creator.py)
- **使用指南**: [00_Agent_Library/SKILL_CREATOR_GUIDE.md](../../00_Agent_Library/SKILL_CREATOR_GUIDE.md)
- **完整示例**: [skills/super-butler/SKILL.md](../super-butler/SKILL.md)
- **项目配置**: [CLAUDE.md](../../CLAUDE.md)
