#!/usr/bin/env python3
"""
工作区文档更新器
一键更新所有工作区结构文档
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_script(script_name):
    """运行 Python 脚本"""
    print(f"\n{'='*60}")
    print(f"运行: {script_name}")
    print('='*60)

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=Path(__file__).parent,
            check=True,
            capture_output=False,
            text=True
        )
        print(f"[OK] {script_name} 执行成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {script_name} 执行失败: {e}")
        return False

def main():
    print(f"""
╔══════════════════════════════════════════════════════════╗
║        工作区文档更新器 - Workspace Doc Updater         ║
╚══════════════════════════════════════════════════════════╝

更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

将更新以下文档:
1. 工作区索引 (JSON + MD)
2. 可视化目录树
3. 工作区报告

""")

    workspace_root = Path(__file__).parent

    # 要运行的脚本列表
    scripts = [
        'workspace_scanner.py',      # 生成 JSON 索引
        'generate_tree.py',          # 生成目录树
        # 'workspace_report.py',     # 可选：生成健康报告
    ]

    success_count = 0

    for script in scripts:
        script_path = workspace_root / script
        if script_path.exists():
            if run_script(script_path):
                success_count += 1
        else:
            print(f"[WARN] 脚本不存在: {script}")

    print(f"\n{'='*60}")
    print(f"完成! {success_count}/{len(scripts)} 个脚本执行成功")
    print('='*60)

    print(f"""
生成的文档:
- WORKSPACE_GUIDE.md      # 总览指南 (手动维护)
- DIRECTORY_TREE.md       # 目录树 (自动生成)
- workspace_index_*.json  # 详细索引 (自动生成)
- workspace_index_*.md    # 索引摘要 (自动生成)

建议:
- 新建项目后运行此脚本
- 每周定期更新一次
- Git 提交前更新文档
""")

if __name__ == "__main__":
    main()
