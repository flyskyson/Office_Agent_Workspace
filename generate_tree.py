#!/usr/bin/env python3
"""
工作区目录树生成器
生成易读的目录结构文档，方便 AI 快速了解工作区布局
"""

import os
from pathlib import Path
from datetime import datetime

# 需要忽略的目录和文件
IGNORE_DIRS = {
    '__pycache__', '.git', 'node_modules', '.vscode',
    'venv', 'env', '.pytest_cache', '.mypy_cache',
    '__MACOSX', '.DS_Store'
}

IGNORE_FILES = {
    '.gitignore', '.npmrc', 'package-lock.json',
    'poetry.lock', 'yarn.lock', '.env'
}

def generate_tree(directory, prefix="", max_depth=3, current_depth=0, show_files=True):
    """生成目录树结构"""
    if current_depth >= max_depth:
        return []

    lines = []
    path = Path(directory)

    try:
        items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        items = [item for item in items if item.name not in IGNORE_DIRS and item.name not in IGNORE_FILES]
    except PermissionError:
        return lines

    for index, item in enumerate(items):
        is_last = index == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        next_prefix = "    " if is_last else "│   "

        if item.is_dir():
            # 目录
            lines.append(f"{prefix}{current_prefix}{item.name}/")
            # 递归处理子目录
            lines.extend(generate_tree(
                item,
                prefix + next_prefix,
                max_depth,
                current_depth + 1,
                show_files
            ))
        elif show_files and current_depth < max_depth - 1:
            # 文件（只在非最深层显示）
            size = item.stat().st_size
            size_str = format_size(size)
            lines.append(f"{prefix}{current_prefix}{item.name} ({size_str})")

    return lines

def format_size(size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}TB"

def get_project_summary(project_path):
    """获取项目简要信息"""
    readme_path = project_path / "README.md"
    if readme_path.exists():
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # 尝试获取第一行标题
                for line in lines:
                    line = line.strip()
                    if line.startswith('#'):
                        return line.lstrip('#').strip()
        except:
            pass
    return None

def main():
    workspace_root = Path(__file__).parent
    output_file = workspace_root / "DIRECTORY_TREE.md"

    print("正在生成工作区目录树...")

    lines = [
        "# Office Agent Workspace - 目录树",
        "",
        f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 完整目录结构",
        "",
        "```",
        f"{workspace_root.name}/",
    ]

    # 生成树形结构（3层深度）
    tree_lines = generate_tree(workspace_root, max_depth=3, show_files=False)
    lines.extend(tree_lines)
    lines.append("```")
    lines.append("")

    # 添加关键项目详情
    lines.append("## 关键项目详情")
    lines.append("")

    # 活跃项目
    active_projects_path = workspace_root / "01_Active_Projects"
    if active_projects_path.exists():
        lines.append("### 活跃项目 (01_Active_Projects)")
        lines.append("")
        for project in sorted(active_projects_path.iterdir()):
            if project.is_dir() and project.name not in IGNORE_DIRS:
                summary = get_project_summary(project)
                if summary:
                    lines.append(f"- **{project.name}**: {summary}")
                else:
                    lines.append(f"- **{project.name}**")
        lines.append("")

    # Playwright demo
    playwright_path = workspace_root / "playwright-mcp-demo"
    if playwright_path.exists():
        lines.append("### Playwright 自动化示例")
        lines.append("")
        lines.append("```")
        lines.append("playwright-mcp-demo/")
        tree_lines = generate_tree(playwright_path, "  ", max_depth=2, show_files=True)
        lines.extend(tree_lines)
        lines.append("```")
        lines.append("")

    # 工具脚本
    lines.append("## 工作区管理工具")
    lines.append("")
    lines.append("位于根目录的 Python 工具:")
    lines.append("")
    for file in sorted(workspace_root.glob("*.py")):
        if file.is_file():
            lines.append(f"- `{file.name}`")
    lines.append("")

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"[OK] 目录树已生成: {output_file}")
    print(f"    包含 {len(lines)} 行")

    # 也输出到控制台（前50行）
    print("\n" + "="*60)
    print("预览 (前50行):")
    print("="*60)
    for line in lines[:50]:
        print(line)
    if len(lines) > 50:
        print(f"\n... 还有 {len(lines)-50} 行 ...")

if __name__ == "__main__":
    main()
