#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作区快照工具
在重要时刻创建工作区状态快照
"""

import sys
import io
from pathlib import Path
from datetime import datetime
import shutil
import json

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def create_snapshot(workspace_root=None, description=""):
    """创建工作区快照

    Args:
        workspace_root: 工作区根目录
        description: 快照描述
    """
    if workspace_root is None:
        workspace_root = Path.cwd()
    else:
        workspace_root = Path(workspace_root)

    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 快照目录
    snapshot_dir = workspace_root / "06_Learning_Journal" / "snapshots" / timestamp
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("📸 创建工作区快照")
    print("=" * 70)
    print(f"\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"快照目录: {snapshot_dir.relative_to(workspace_root)}")

    if description:
        print(f"描述: {description}")

    # 1. 复制工作区索引
    print("\n[1/5] 保存工作区索引...")
    latest_index = workspace_root / "06_Learning_Journal" / "workspace_memory" / "workspace_index_latest.json"
    if latest_index.exists():
        shutil.copy2(latest_index, snapshot_dir / "workspace_index.json")
        print("  ✅ 工作区索引已保存")
    else:
        print("  ⚠️  未找到工作区索引，请先运行 workspace_scanner.py")

    # 2. 保存开发者档案
    print("\n[2/5] 保存开发者档案...")
    ai_memory = workspace_root / "06_Learning_Journal" / "AI_MEMORY.md"
    if ai_memory.exists():
        shutil.copy2(ai_memory, snapshot_dir / "AI_MEMORY.md")
        print("  ✅ 开发者档案已保存")

    # 3. 保存项目列表
    print("\n[3/5] 保存项目信息...")
    active_projects = workspace_root / "01_Active_Projects"
    if active_projects.exists():
        projects = []
        for project_dir in active_projects.iterdir():
            if project_dir.is_dir():
                readme = project_dir / "README.md"
                projects.append({
                    "name": project_dir.name,
                    "has_readme": readme.exists(),
                    "modified": datetime.fromtimestamp(project_dir.stat().st_mtime()).strftime('%Y-%m-%d %H:%M:%S')
                })

        with open(snapshot_dir / "projects.json", 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)
        print(f"  ✅ 项目列表已保存 ({len(projects)} 个活跃项目)")

    # 4. 保存工具列表
    print("\n[4/5] 保存工具列表...")
    tools = []
    for tool_file in workspace_root.glob("*.py"):
        if tool_file.name not in ["create_snapshot.py"]:
            tools.append({
                "name": tool_file.name,
                "size": tool_file.stat().st_size,
                "modified": datetime.fromtimestamp(tool_file.stat().st_mtime()).strftime('%Y-%m-%d %H:%M:%S')
            })

    with open(snapshot_dir / "tools.json", 'w', encoding='utf-8') as f:
        json.dump(tools, f, indent=2, ensure_ascii=False)
    print(f"  ✅ 工具列表已保存 ({len(tools)} 个工具)")

    # 5. 生成快照说明
    print("\n[5/5] 生成快照说明...")
    snapshot_readme = snapshot_dir / "README.md"
    with open(snapshot_readme, 'w', encoding='utf-8') as f:
        f.write(f"""# 工作区快照

**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**快照ID**: {timestamp}

---

## 📋 快照内容

### 工作区索引
- `workspace_index.json` - 完整的工作区文件索引

### 开发者档案
- `AI_MEMORY.md` - 开发者学习档案

### 项目信息
- `projects.json` - 活跃项目列表

### 工具列表
- `tools.json` - 工作区工具清单

---

## 📝 快照描述

{description if description else "（无描述）"}

---

## 💡 恢复快照

如需查看快照时的状态：

1. 查看工作区索引：`workspace_index.json`
2. 对比当前状态：运行 `python workspace_scanner.py`
3. 查看开发者档案：`AI_MEMORY.md`

---

*快照由 create_snapshot.py 自动生成*
""")

    print("  ✅ 快照说明已生成")

    # 统计信息
    print("\n" + "=" * 70)
    print("✅ 快照创建完成！")
    print("=" * 70)
    print(f"\n快照位置: {snapshot_dir}")
    print(f"包含文件: {len(list(snapshot_dir.glob('*')))} 个")

    # 保存快照记录到索引
    snapshot_index = workspace_root / "06_Learning_Journal" / "snapshots" / "snapshot_index.json"

    snapshot_record = {
        "id": timestamp,
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "description": description,
        "path": str(snapshot_dir.relative_to(workspace_root))
    }

    # 读取现有索引
    if snapshot_index.exists():
        with open(snapshot_index, 'r', encoding='utf-8') as f:
            snapshots = json.load(f)
    else:
        snapshots = []

    # 添加新快照
    snapshots.insert(0, snapshot_record)

    # 保存索引
    with open(snapshot_index, 'w', encoding='utf-8') as f:
        json.dump(snapshots, f, indent=2, ensure_ascii=False)

    print(f"\n历史快照: {len(snapshots)} 个")
    print(f"索引文件: {snapshot_index.relative_to(workspace_root)}")


def list_snapshots(workspace_root=None):
    """列出所有快照"""
    if workspace_root is None:
        workspace_root = Path.cwd()
    else:
        workspace_root = Path(workspace_root)

    snapshot_index = workspace_root / "06_Learning_Journal" / "snapshots" / "snapshot_index.json"

    if not snapshot_index.exists():
        print("\n❌ 未找到快照记录")
        return

    with open(snapshot_index, 'r', encoding='utf-8') as f:
        snapshots = json.load(f)

    print("\n" + "=" * 70)
    print("📸 工作区快照列表")
    print("=" * 70)

    if not snapshots:
        print("\n暂无快照")
        return

    for i, snapshot in enumerate(snapshots[:10], 1):  # 只显示最近10个
        print(f"\n{i}. {snapshot['id']}")
        print(f"   时间: {snapshot['time']}")
        print(f"   描述: {snapshot.get('description', '（无）')}")
        print(f"   路径: {snapshot['path']}")

    if len(snapshots) > 10:
        print(f"\n... 还有 {len(snapshots) - 10} 个快照")

    print(f"\n总计: {len(snapshots)} 个快照")


def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("""
工作区快照工具

用法：
  python create_snapshot.py list                    # 列出所有快照
  python create_snapshot.py create [描述]          # 创建快照
  python create_snapshot.py create "项目完成"       # 创建带描述的快照

示例：
  python create_snapshot.py list
  python create_snapshot.py create "完成my_first_agent"
  python create_snapshot.py create "2026年1月里程碑"
        """)
        return

    command = sys.argv[1]

    if command == "list":
        list_snapshots()

    elif command == "create":
        description = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        create_snapshot(description=description)

    else:
        print(f"❌ 未知命令: {command}")
        print("可用命令: list, create")


if __name__ == "__main__":
    main()
