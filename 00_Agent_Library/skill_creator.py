"""
Skill Creator CLI - Claude Code 技能创建工具

用法:
    python skill_creator.py create --name "my-skill" --category "automation"
    python skill_creator.py validate --path "skills/my-skill"
    python skill_creator.py init --workspace "."
    python skill_creator.py template --type "basic"
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Windows 终端编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class SkillCreator:
    """Claude Code 技能创建器"""

    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.skills_dir = self.workspace_root / "skills"

    def create(
        self,
        name: str,
        description: str,
        category: str = "general",
        triggers: List[str] = None,
        author: str = "",
        layered: bool = True
    ) -> Path:
        """
        创建新技能

        Args:
            name: 技能名称（kebab-case）
            description: 技能描述
            category: 技能分类 (automation/analysis/development/management/general)
            triggers: 触发关键词列表
            author: 作者
            layered: 是否创建分层文档结构

        Returns:
            技能目录路径
        """
        skill_dir = self.skills_dir / name
        if skill_dir.exists():
            raise FileExistsError(f"技能已存在: {skill_dir}")

        skill_dir.mkdir(parents=True, exist_ok=True)

        # 生成 SKILL.md
        skill_md = self._generate_skill_md(
            name=name,
            description=description,
            category=category,
            triggers=triggers or [],
            author=author
        )

        (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

        # 生成分层文档
        if layered:
            self._create_layered_docs(skill_dir, name)

        print(f"✅ 技能创建成功: {skill_dir}")
        print(f"   主文件: {skill_dir / 'SKILL.md'}")
        if layered:
            print(f"   附加文档: EXAMPLES.md, CONFIG.md, TROUBLESHOOTING.md")

        return skill_dir

    def _generate_skill_md(
        self,
        name: str,
        description: str,
        category: str,
        triggers: List[str],
        author: str
    ) -> str:
        """生成 SKILL.md 内容"""

        category_emoji = {
            "automation": "⚙️",
            "analysis": "🔍",
            "development": "💻",
            "management": "📊",
            "general": "🔧"
        }.get(category, "🔧")

        triggers_str = ", ".join([f"`{t}`" for t in triggers])

        return f"""# {name.replace("-", " ").title()} Skill

{category_emoji} **分类**: {category}
📝 **描述**: {description}
{'👤 **作者**: ' + author if author else ''}

---

## 概述

简要描述这个技能的核心功能（1-2句话）。

**核心价值**:
- 价值点 1
- 价值点 2

---

## 触发条件

当用户提到以下内容时激活此技能：
{triggers_str if triggers else '`待填写`'}

**适用场景**:
- 场景 1
- 场景 2

**不适用场景**:
- ❌ 不支持的功能

---

## 执行步骤

### 步骤 1: [步骤名称]

简短描述这一步做什么。

**关键文件/命令**:
```bash
# 示例命令
```

### 步骤 2: [步骤名称]

...

### 步骤 3: [步骤名称]

...

---

## 快速示例

```
用户: [用户输入]

AI: [预期的AI响应]
```

---

## 详细文档

- 📖 **[使用案例](EXAMPLES.md)** - 详细的使用示例
- ⚙️ **[配置说明](CONFIG.md)** - 配置文件和参数
- 🔧 **[故障排查](TROUBLESHOOTING.md)** - 常见问题解决

---

## 相关资源

- **核心代码**: `path/to/code.py`
- **配置文件**: `path/to/config.yaml`
- **文档**: `path/to/docs.md`

---

**技能版本**: 1.0
**创建日期**: {datetime.now().strftime("%Y-%m-%d")}
**最后更新**: {datetime.now().strftime("%Y-%m-%d")}
"""

    def _create_layered_docs(self, skill_dir: Path, name: str):
        """创建分层文档结构"""

        # EXAMPLES.md
        examples_md = f"""# {name.replace('-', ' ').title()} - 使用案例

## 案例 1: [案例标题]

### 场景
描述这个案例的使用场景。

### 操作步骤

1. **步骤 1**
   ```bash
   # 命令示例
   ```

2. **步骤 2**
   - 操作说明
   - 注意事项

### 预期结果

```
[输出示例]
```

---

## 案例 2: [案例标题]

...

---

## 更多案例

持续添加真实的使用案例...
"""

        # CONFIG.md
        config_md = """# 配置说明

## 环境变量

创建 `.env` 文件：

```bash
# 配置项
CONFIG_KEY=value
```

## 配置文件

编辑 `config/config.yaml`：

```yaml
key: value
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| param1 | string | "default" | 参数说明 |
"""

        # TROUBLESHOOTING.md
        troubleshooting_md = """# 故障排查

## 常见问题

### 问题 1: [问题标题]

**症状**:
```
错误信息
```

**原因**:
- 原因 1
- 原因 2

**解决方案**:
```bash
# 解决命令
```

---

## 调试模式

启用详细日志：
```bash
# 添加 --debug 或 --verbose 参数
```

---

## 获取帮助

- 查看文档: [链接]
- 提交问题: [链接]
"""

        (skill_dir / "EXAMPLES.md").write_text(examples_md, encoding="utf-8")
        (skill_dir / "CONFIG.md").write_text(config_md, encoding="utf-8")
        (skill_dir / "TROUBLESHOOTING.md").write_text(troubleshooting_md, encoding="utf-8")

    def validate(self, skill_path: Path = None) -> Dict:
        """
        验证技能结构

        Returns:
            验证结果字典
        """
        if skill_path is None:
            skill_path = self.skills_dir

        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": []
        }

        if not skill_path.exists():
            results["valid"] = False
            results["errors"].append(f"技能目录不存在: {skill_path}")
            return results

        # 检查 SKILL.md
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            results["valid"] = False
            results["errors"].append(f"缺少 SKILL.md: {skill_md}")
        else:
            content = skill_md.read_text(encoding="utf-8")

            # 检查必需章节
            required_sections = ["## 执行步骤", "## 触发条件"]
            for section in required_sections:
                if section not in content:
                    results["warnings"].append(f"缺少推荐章节: {section}")

            # 检查触发关键词
            if "**触发关键词**" not in content and "**触发条件**" not in content:
                results["warnings"].append("未找到触发关键词定义")

            results["info"].append(f"SKILL.md 大小: {len(content)} 字符")

        # 检查分层文档
        for doc in ["EXAMPLES.md", "CONFIG.md", "TROUBLESHOOTING.md"]:
            doc_path = skill_path / doc
            if doc_path.exists():
                results["info"].append(f"✅ 找到附加文档: {doc}")

        return results

    def list_skills(self) -> List[Dict]:
        """列出所有技能"""
        skills = []

        if not self.skills_dir.exists():
            return skills

        for skill_dir in sorted(self.skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            # 提取元信息
            content = skill_md.read_text(encoding="utf-8")
            name = skill_dir.name
            description = self._extract_description(content)
            category = self._extract_category(content)

            skills.append({
                "name": name,
                "path": str(skill_dir),
                "description": description,
                "category": category
            })

        return skills

    def _extract_description(self, content: str) -> str:
        """从 SKILL.md 提取描述"""
        for line in content.split("\n"):
            if "📝 **描述**:" in line or "**描述**:" in line:
                return line.split(":")[-1].strip()
        return "无描述"

    def _extract_category(self, content: str) -> str:
        """从 SKILL.md 提取分类"""
        for line in content.split("\n"):
            if "⚙️ **分类**:" in line or "**分类**:" in line:
                return line.split(":")[-1].strip()
        return "general"


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Claude Code 技能创建工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 创建新技能
  python skill_creator.py create --name "my-skill" --description "我的技能" --triggers "trigger1,trigger2"

  # 验证技能
  python skill_creator.py validate --path "skills/my-skill"

  # 列出所有技能
  python skill_creator.py list

  # 初始化工作区
  python skill_creator.py init
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新技能")
    create_parser.add_argument("--name", required=True, help="技能名称 (kebab-case)")
    create_parser.add_argument("--description", required=True, help="技能描述")
    create_parser.add_argument("--category", default="general", choices=["automation", "analysis", "development", "management", "general"], help="技能分类")
    create_parser.add_argument("--triggers", nargs="+", help="触发关键词列表")
    create_parser.add_argument("--author", default="", help="作者")
    create_parser.add_argument("--no-layered", action="store_true", help="不创建分层文档")

    # validate 命令
    validate_parser = subparsers.add_parser("validate", help="验证技能结构")
    validate_parser.add_argument("--path", help="技能路径 (默认验证所有)")

    # list 命令
    subparsers.add_parser("list", help="列出所有技能")

    # init 命令
    subparsers.add_parser("init", help="初始化工作区")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    creator = SkillCreator()

    if args.command == "create":
        try:
            skill_dir = creator.create(
                name=args.name,
                description=args.description,
                category=args.category,
                triggers=args.triggers,
                author=args.author,
                layered=not args.no_layered
            )
            print(f"\n💡 下一步:")
            print(f"   1. 编辑 {skill_dir / 'SKILL.md'}")
            print(f"   2. 添加执行步骤和示例")
            print(f"   3. 运行: python skill_creator.py validate --path \"{skill_dir}\"")
        except FileExistsError as e:
            print(f"❌ 错误: {e}")

    elif args.command == "validate":
        if args.path:
            skill_path = Path(args.path)
            result = creator.validate(skill_path)
        else:
            # 验证所有技能
            all_valid = True
            for skill in creator.list_skills():
                skill_path = Path(skill["path"])
                result = creator.validate(skill_path)

                print(f"\n📋 {skill['name']}:")
                if not result["valid"]:
                    all_valid = False
                    for error in result["errors"]:
                        print(f"   ❌ {error}")
                for warning in result["warnings"]:
                    print(f"   ⚠️  {warning}")
                for info in result["info"]:
                    print(f"   ℹ️  {info}")

            if all_valid:
                print("\n✅ 所有技能验证通过")
            return

        # 单个技能验证结果
        if result["valid"]:
            print("✅ 验证通过")
        else:
            print("❌ 验证失败")

        for error in result["errors"]:
            print(f"   ❌ {error}")
        for warning in result["warnings"]:
            print(f"   ⚠️  {warning}")
        for info in result["info"]:
            print(f"   ℹ️  {info}")

    elif args.command == "list":
        skills = creator.list_skills()

        if not skills:
            print("📭 未找到技能")
            return

        print(f"📚 找到 {len(skills)} 个技能:\n")
        for skill in skills:
            print(f"📁 {skill['name']}")
            print(f"   分类: {skill['category']}")
            print(f"   描述: {skill['description']}")
            print(f"   路径: {skill['path']}")
            print()

    elif args.command == "init":
        skills_dir = creator.skills_dir
        if skills_dir.exists():
            print(f"⚠️  skills/ 目录已存在: {skills_dir}")
        else:
            skills_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建 skills/ 目录: {skills_dir}")

        # 创建 .gitignore
        gitignore = skills_dir / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text("# 忽略临时文件\n*.tmp\n*.bak\n")
            print(f"✅ 创建 .gitignore")

        print("\n💡 工作区初始化完成")
        print(f"   技能目录: {skills_dir}")


if __name__ == "__main__":
    main()
