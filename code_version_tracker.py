#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码版本追踪系统 - 智能管家的"历史档案"
记录每次代码变更，追踪脚本演进历史
让AI助手了解每个脚本的成长轨迹
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import hashlib


class CodeVersionTracker:
    """代码版本追踪器"""

    def __init__(self, workspace_root=None):
        """初始化追踪器

        Args:
            workspace_root: 工作区根目录
        """
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        else:
            workspace_root = Path(workspace_root)

        self.workspace_root = workspace_root
        self.memory_dir = workspace_root / "06_Learning_Journal" / "workspace_memory" / "code_versions"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.index_file = self.memory_dir / "version_index.json"

    def calculate_hash(self, filepath):
        """计算文件哈希值"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def load_index(self):
        """加载版本索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_index(self, index):
        """保存版本索引"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

    def track_file(self, filepath, reason="手动记录"):
        """追踪单个文件的版本

        Args:
            filepath: 文件路径
            reason: 记录原因
        """
        filepath = Path(filepath)
        if not filepath.exists():
            print(f"文件不存在: {filepath}")
            return

        # 计算哈希值
        file_hash = self.calculate_hash(filepath)
        if not file_hash:
            print(f"无法计算文件哈希: {filepath}")
            return

        # 加载索引
        index = self.load_index()

        # 文件的相对路径
        rel_path = str(filepath.relative_to(self.workspace_root))

        # 如果是新文件，创建记录
        if rel_path not in index:
            index[rel_path] = {
                'name': filepath.name,
                'path': rel_path,
                'versions': []
            }

        # 检查是否已有相同版本
        last_version = index[rel_path]['versions'][-1] if index[rel_path]['versions'] else None
        if last_version and last_version['hash'] == file_hash:
            print(f"文件未变更，无需记录新版本: {rel_path}")
            return

        # 读取文件内容（仅用于代码文件）
        content = None
        if filepath.suffix in ['.py', '.js', '.bat', '.ps1', '.md']:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                pass

        # 创建版本记录
        version_info = {
            'version': len(index[rel_path]['versions']) + 1,
            'hash': file_hash,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'size': filepath.stat().st_size,
            'reason': reason
        }

        # 保存文件内容快照
        version_dir = self.memory_dir / filepath.stem
        version_dir.mkdir(exist_ok=True)
        snapshot_file = version_dir / f"v{version_info['version']}_{filepath.suffix}"

        if content:
            with open(snapshot_file, 'w', encoding='utf-8') as f:
                f.write(content)
            version_info['snapshot'] = str(snapshot_file.relative_to(self.workspace_root))

        # 添加到索引
        index[rel_path]['versions'].append(version_info)

        # 保存索引
        self.save_index(index)

        print(f"[OK] 已记录版本: {rel_path} v{version_info['version']}")
        print(f"  哈希: {file_hash[:8]}...")
        print(f"  原因: {reason}")

        return version_info

    def get_file_history(self, filepath):
        """获取文件的历史版本

        Args:
            filepath: 文件路径

        Returns:
            list: 版本历史列表
        """
        filepath = Path(filepath)
        rel_path = str(filepath.relative_to(self.workspace_root))

        index = self.load_index()
        if rel_path not in index:
            return []

        return index[rel_path]['versions']

    def compare_versions(self, filepath, version1=None, version2=None):
        """比较两个版本的差异

        Args:
            filepath: 文件路径
            version1: 版本1（默认为最新版本）
            version2: 版本2（默认为上一个版本）
        """
        filepath = Path(filepath)
        rel_path = str(filepath.relative_to(self.workspace_root))

        index = self.load_index()
        if rel_path not in index:
            print(f"文件未被追踪: {rel_path}")
            return

        versions = index[rel_path]['versions']
        if len(versions) < 2:
            print("版本不足，无法比较")
            return

        # 默认比较最新两个版本
        if version1 is None:
            version1 = len(versions)
        if version2 is None:
            version2 = len(versions) - 1

        # 获取快照路径
        snapshot_dir = self.memory_dir / filepath.stem

        v1_file = snapshot_dir / f"v{version1}_{filepath.suffix}"
        v2_file = snapshot_dir / f"v{version2}_{filepath.suffix}"

        if not v1_file.exists() or not v2_file.exists():
            print("版本快照不存在")
            return

        # 读取内容
        with open(v1_file, 'r', encoding='utf-8') as f:
            content1 = f.readlines()
        with open(v2_file, 'r', encoding='utf-8') as f:
            content2 = f.readlines()

        # 简单的差异比较
        print(f"\n比较版本 {version2} -> {version1}:")
        print("="*70)

        import difflib
        diff = difflib.unified_diff(
            content2, content1,
            fromfile=f"v{version2}",
            tofile=f"v{version1}",
            lineterm=''
        )

        for line in diff:
            print(line)

    def auto_track_changed_files(self):
        """自动追踪工作区中变更的文件"""
        print("正在扫描变更的文件...")

        # 需要追踪的目录
        track_dirs = [
            self.workspace_root / "01_Active_Projects",
            self.workspace_root / "00_Agent_Library",
            self.workspace_root
        ]

        index = self.load_index()
        changed_count = 0

        for track_dir in track_dirs:
            if not track_dir.exists():
                continue

            # 扫描Python脚本和批处理文件
            for pattern in ['*.py', '*.bat', '*.ps1']:
                for filepath in track_dir.glob(pattern):
                    # 跳过特定目录
                    if 'venv' in str(filepath) or '__pycache__' in str(filepath):
                        continue

                    rel_path = str(filepath.relative_to(self.workspace_root))

                    # 计算当前哈希
                    current_hash = self.calculate_hash(filepath)
                    if not current_hash:
                        continue

                    # 检查是否需要记录
                    if rel_path in index and index[rel_path]['versions']:
                        last_hash = index[rel_path]['versions'][-1]['hash']
                        if current_hash == last_hash:
                            continue  # 未变更

                    # 记录新版本
                    self.track_file(filepath, reason="自动检测到变更")
                    changed_count += 1

        if changed_count == 0:
            print("未检测到文件变更")
        else:
            print(f"\n共记录 {changed_count} 个文件的变更")

    def generate_report(self):
        """生成版本追踪报告"""
        index = self.load_index()

        report = []
        report.append("# 代码版本追踪报告\n")
        report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**追踪文件数**: {len(index)}\n")
        report.append("\n---\n\n")

        # 统计信息
        total_versions = sum(len(file_info['versions']) for file_info in index.values())
        report.append(f"**总版本数**: {total_versions}\n\n")

        # 按最后修改时间排序
        sorted_files = sorted(
            index.items(),
            key=lambda x: x[1]['versions'][-1]['timestamp'] if x[1]['versions'] else '',
            reverse=True
        )

        # 最近变更
        report.append("## 最近变更\n\n")
        for rel_path, file_info in sorted_files[:10]:
            if file_info['versions']:
                latest = file_info['versions'][-1]
                report.append(f"### {file_info['name']}\n\n")
                report.append(f"- **路径**: `{rel_path}`\n")
                report.append(f"- **版本**: v{latest['version']}\n")
                report.append(f"- **时间**: {latest['timestamp']}\n")
                report.append(f"- **原因**: {latest['reason']}\n")
                report.append(f"- **大小**: {latest['size']} bytes\n\n")

        # 所有文件列表
        report.append("## 所有追踪文件\n\n")
        for rel_path, file_info in index.items():
            versions_count = len(file_info['versions'])
            if versions_count > 0:
                latest = file_info['versions'][-1]
                report.append(f"- **{file_info['name']}** ({versions_count} 个版本)")
                report.append(f" - 最后更新: {latest['timestamp']}\n")

        report_content = ''.join(report)

        # 保存报告
        report_file = self.memory_dir / f"version_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"\n[OK] 版本报告已保存: {report_file}")

        return report_content


def main():
    """主程序"""
    import sys
    import io

    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("="*70)
    print("代码版本追踪系统")
    print("="*70)

    tracker = CodeVersionTracker()

    while True:
        print("\n请选择操作:")
        print("1. 追踪单个文件")
        print("2. 自动扫描变更文件")
        print("3. 查看文件历史")
        print("4. 比较版本差异")
        print("5. 生成追踪报告")
        print("0. 退出")

        choice = input("\n请输入选项 (0-5): ").strip()

        if choice == '1':
            filepath = input("请输入文件路径 (相对或绝对): ").strip()
            reason = input("记录原因 (可选): ").strip() or "手动记录"
            tracker.track_file(filepath, reason)

        elif choice == '2':
            tracker.auto_track_changed_files()

        elif choice == '3':
            filepath = input("请输入文件路径: ").strip()
            history = tracker.get_file_history(filepath)
            if history:
                print(f"\n{filepath} 的版本历史:")
                for version in history:
                    print(f"  v{version['version']} - {version['timestamp']} - {version['reason']}")
            else:
                print("文件未被追踪")

        elif choice == '4':
            filepath = input("请输入文件路径: ").strip()
            tracker.compare_versions(filepath)

        elif choice == '5':
            report = tracker.generate_report()
            print("\n" + report)

        elif choice == '0':
            print("\n再见!")
            break

        else:
            print("无效选项")


if __name__ == "__main__":
    main()
