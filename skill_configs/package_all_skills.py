#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能打包工具
将生成的技能打包成 ZIP 文件，可直接上传到 Claude
"""

import sys
import codecs
import zipfile
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

WORKSPACE_ROOT = Path(r"c:\Users\flyskyson\Office_Agent_Workspace")
SKILLS_DIR = WORKSPACE_ROOT / "05_Outputs" / "skills"
OUTPUT_DIR = SKILLS_DIR / "packages"


def package_skill(skill_name: str, skill_dir: Path) -> Path:
    """打包单个技能"""
    output_file = OUTPUT_DIR / f"{skill_name}.zip"

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in skill_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(skill_dir)
                zf.write(file, arcname)

    return output_file


def main():
    """主函数"""
    print("=" * 70)
    print("📦 技能打包工具")
    print("=" * 70)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 查找所有技能目录
    skill_dirs = [d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name == 'packages']

    if not skill_dirs:
        print("❌ 未找到技能目录")
        return 1

    print(f"\n📦 发现 {len(skill_dirs)} 个技能:")
    for skill_dir in skill_dirs:
        print(f"  - {skill_dir.name}")

    # 打包所有技能
    print("\n📦 打包技能:")
    packages = []

    for skill_dir in skill_dirs:
        try:
            output_file = package_skill(skill_dir.name, skill_dir)
            size_mb = output_file.stat().st_size / (1024 * 1024)
            packages.append({
                "name": skill_dir.name,
                "file": str(output_file),
                "size_mb": round(size_mb, 2)
            })
            print(f"  ✅ {skill_dir.name}.zip ({size_mb:.2f} MB)")
        except Exception as e:
            print(f"  ❌ {skill_dir.name}: {e}")

    # 创建安装说明
    readme = """# Office Agent Workspace - Claude 技能包

## 技能列表

"""
    for pkg in packages:
        readme += f"- **{pkg['name']}** - `{pkg['name']}.zip` ({pkg['size_mb']} MB)\n"

    readme += """

## 安装方式

### 方式A: Claude Code (推荐)

1. 将 ZIP 文件复制到 `~/.claude/skills/` 目录
2. 重启 Claude Code
3. 技能自动加载

### 方式B: Claude AI Web

1. 访问 https://claude.ai/skills
2. 点击 "Upload Skill"
3. 选择对应的 ZIP 文件
4. 点击 "Upload"

## 使用方式

安装后，在 Claude Code 或 Claude AI 中直接使用：

```
@office-agent-workspace 帮我创建一个新的智能体
@market-supervision-agent 填写申请书
@memory-agent 搜索关于Python的记忆
@workflow-engine 创建一个工作流
```

## 技能说明

- **office-agent-workspace**: 主技能，包含整个工作区概览
- **market-supervision-agent**: 市场监管智能体，用于填写申请书
- **memory-agent**: 记忆助手，语义记忆存储和检索
- **file-organizer**: 文件整理工具
- **smart-tools**: 智能工具集（新闻、工作流、导出）
- **workflow-engine**: 工作流引擎
- **agent-toolkit**: AgentTool 工具框架
- **claude-memory**: Claude 记忆系统

## 更新日期

2026-01-16

## 技术支持

- 项目地址: https://github.com/yourusername/Office_Agent_Workspace
- 文档: docs/
- 配置: CLAUDE.md
"""

    readme_file = OUTPUT_DIR / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme)

    print(f"\n📄 创建安装说明: {readme_file}")

    print("\n" + "=" * 70)
    print(f"✅ 打包完成! 共 {len(packages)} 个技能包")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print("=" * 70)

    print("\n📋 生成的技能包:")
    for pkg in packages:
        print(f"  📦 {pkg['file']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
