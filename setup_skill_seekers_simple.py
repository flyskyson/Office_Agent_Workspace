#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Seekers 快速部署脚本
一键安装和配置
"""
import sys
import subprocess
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def main():
    workspace_root = Path(__file__).parent
    external_dir = workspace_root / "external"
    skill_seekers_path = external_dir / "skill_seekers"

    print("=" * 60)
    print("Skill Seekers 快速部署")
    print("=" * 60)

    # 1. 创建目录
    print("\n[1/4] 创建目录...")
    external_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ external 目录: {external_dir}")

    # 2. 克隆仓库
    print("\n[2/4] 克隆 Skill Seekers...")
    if skill_seekers_path.exists():
        print("⚠️ 已存在,跳过克隆")
    else:
        try:
            subprocess.run(
                ["git", "clone", "https://github.com/yusufkaraaslan/Skill_Seekers.git"],
                cwd=external_dir,
                check=True
            )
            print(f"✅ 已克隆到: {skill_seekers_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ 克隆失败: {e}")
            print("\n手动克隆命令:")
            print(f"  cd {external_dir}")
            print(f"  git clone https://github.com/yusufkaraaslan/Skill_Seekers.git")
            return

    # 3. 安装依赖
    print("\n[3/4] 安装依赖...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=skill_seekers_path,
            check=True
        )
        print("✅ 依赖已安装")
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        return

    # 4. 创建输出目录
    print("\n[4/4] 创建输出目录...")
    output_dir = workspace_root / "skills" / "auto_generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ 输出目录: {output_dir}")

    # 完成
    print("\n" + "=" * 60)
    print("部署完成!")
    print("=" * 60)
    print(f"\nSkill Seekers: {skill_seekers_path}")
    print(f"输出目录: {output_dir}")
    print("\n下一步:")
    print("  1. 运行测试: python -m 00_Agent_Library.skill_builder_facade")
    print("  2. 查看示例: python 00_Agent_Library/examples/skill_builder_examples.py")

if __name__ == "__main__":
    main()
