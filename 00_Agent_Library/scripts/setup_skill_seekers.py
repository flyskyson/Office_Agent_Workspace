#!/usr/bin/env python3
"""
Skill Seekers 集成设置脚本

自动下载和配置 Skill Seekers 集成。

版本: v1.0.0
日期: 2026-01-16
"""

import sys
import subprocess
import shutil
from pathlib import Path


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_step(step, description):
    """打印步骤"""
    print(f"\n[{step}] {description}")


def run_command(cmd, cwd=None, check=True):
    """运行命令并显示输出"""
    print(f"  运行: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(f"  输出: {result.stdout.strip()}")

    return result


def setup_skill_seekers():
    """设置 Skill Seekers 集成"""
    print_header("Skill Seekers 集成设置")

    # 获取工作区根目录
    workspace_root = Path(__file__).parent.parent.parent
    external_dir = workspace_root / "external"
    skill_seekers_path = external_dir / "skill_seekers"

    # 步骤 1: 检查现有安装
    print_step("1/5", "检查现有安装")

    if skill_seekers_path.exists():
        print(f"  ⚠️ 发现现有安装: {skill_seekers_path}")
        response = input("  是否删除并重新安装? (y/N): ").strip().lower()

        if response == 'y':
            print(f"  删除现有安装...")
            shutil.rmtree(skill_seekers_path)
        else:
            print("  跳过安装")
            return

    # 步骤 2: 创建目录
    print_step("2/5", "创建目录结构")
    external_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✅ 目录已创建: {external_dir}")

    # 步骤 3: 克隆仓库
    print_step("3/5", "克隆 Skill Seekers 仓库")

    try:
        run_command([
            "git", "clone",
            "https://github.com/yusufkaraaslan/Skill_Seekers.git",
            str(skill_seekers_path)
        ], cwd=external_dir)
        print(f"  ✅ 仓库已克隆")
    except subprocess.CalledProcessError as e:
        print(f"  ❌ 克隆失败: {e}")
        print(f"  请手动克隆: git clone https://github.com/yusufkaraaslan/Skill_Seekers.git")
        return

    # 步骤 4: 安装依赖
    print_step("4/5", "安装 Python 依赖")

    try:
        # 检查是否使用虚拟环境
        in_venv = hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )

        if in_venm:
            print("  检测到虚拟环境")
        else:
            print("  ⚠️ 建议在虚拟环境中安装")
            response = input("  是否继续? (y/N): ").strip().lower()
            if response != 'y':
                return

        # 安装 Skill Seekers
        run_command([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], cwd=skill_seekers_path)

        print(f"  ✅ 依赖已安装")

    except subprocess.CalledProcessError as e:
        print(f"  ❌ 安装失败: {e}")
        return

    # 步骤 5: 验证安装
    print_step("5/5", "验证安装")

    try:
        # 测试导入
        sys.path.insert(0, str(skill_seekers_path))
        import src.skill_seekers as ss
        print(f"  ✅ 模块导入成功")

        # 检查版本
        version_file = skill_seekers_path / "pyproject.toml"
        if version_file.exists():
            import toml
            config = toml.load(version_file)
            version = config.get("project", {}).get("version", "unknown")
            print(f"  ✅ Skill Seekers 版本: {version}")

    except ImportError as e:
        print(f"  ❌ 导入失败: {e}")
        return
    except Exception as e:
        print(f"  ⚠️ 版本检查失败: {e}")

    # 完成
    print_header("安装完成")
    print(f"\nSkill Seekers 已安装到:")
    print(f"  {skill_seekers_path}")
    print(f"\n集成文件已创建:")
    print(f"  - 00_Agent_Library/skill_builder_facade.py")
    print(f"  - 00_Agent_Library/skill_seekers_adapter.py")
    print(f"  - docs/guides/SKILL_SEEKERS_INTEGRATION.md")
    print(f"\n下一步:")
    print(f"  1. 查看集成指南: docs/guides/SKILL_SEEKERS_INTEGRATION.md")
    print(f"  2. 运行示例: python 00_Agent_Library/examples/skill_builder_examples.py")
    print(f"  3. 运行测试: pytest tests/integration/test_skill_builder_integration.py")
    print()


def create_directories():
    """创建必要的目录"""
    workspace_root = Path(__file__).parent.parent.parent

    # 创建输出目录
    output_dir = workspace_root / "skills" / "auto_generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"  ✅ 输出目录: {output_dir}")


def create_config():
    """创建配置文件"""
    workspace_root = Path(__file__).parent.parent.parent
    config_dir = workspace_root / "04_Data_&_Resources" / "config"

    config_dir.mkdir(parents=True, exist_ok=True)

    # 创建示例配置
    import json
    config_file = config_dir / "skill_builder_config.json"

    example_config = {
        "default_output_dir": "skills/auto_generated",
        "default_options": {
            "enhance_with_ai": True,
            "include_issues": True,
            "include_prs": False,
            "max_pages": 100
        },
        "quality_threshold": 70.0,
        "auto_package": False
    }

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(example_config, f, indent=2, ensure_ascii=False)

    print(f"  ✅ 配置文件: {config_file}")


if __name__ == "__main__":
    print("\n🚀 Skill Seekers 集成设置向导")
    print("这个脚本将:")
    print("  1. 下载 Skill Seekers 到 external/skill_seekers/")
    print("  2. 安装所需的 Python 依赖")
    print("  3. 验证安装")
    print("  4. 创建必要的目录和配置")

    print("\n⚠️ 注意:")
    print("  - 需要网络连接")
    print("  - 需要安装 Git")
    print("  - 建议在虚拟环境中运行")

    response = input("\n是否继续? (y/N): ").strip().lower()

    if response == 'y':
        setup_skill_seekers()
        create_directories()
        create_config()
    else:
        print("\n已取消")
