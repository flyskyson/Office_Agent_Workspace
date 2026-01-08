#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日文件自动整理器
智能混合模式：按项目分类 + 按文件类型细分

作者：Office Agent Workspace
创建日期：2026-01-08
运行频率：每天自动运行
"""

import os
import sys
import shutil
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# 设置控制台编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

class DailyFileOrganizer:
    """每日文件整理器 - 智能混合模式"""

    def __init__(self, workspace_root=None):
        """初始化整理器"""
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        self.workspace_root = Path(workspace_root)
        self.today = datetime.now().strftime("%Y%m%d")

        # 定义文件分类规则
        self.rules = self._init_rules()

        # 统计信息
        self.stats = {
            'moved': 0,
            'skipped': 0,
            'errors': 0,
            'details': []
        }

    def _init_rules(self):
        """初始化文件分类规则"""
        return {
            # 1. 核心工具脚本（保留在根目录）
            'keep_in_root': [
                r'^start_new_session\.bat$',
                r'^butler_mode\.bat$',
                r'^daily_launcher\.py$',
                r'^daily_file_organizer\.py$',  # 文件整理器
                r'^workspace_.*\.py$',
                r'^code_version_tracker\.py$',  # 版本追踪工具
                r'^create_snapshot\.py$',  # 快照工具
                r'^daily_snapshot\.py$',  # 每日快照
                r'^\.gitignore$',
                r'^README\.md$',
                r'^\.mcp\.json$',
            ],

            # 2. 输出报告文件（按日期归档）
            'reports': {
                'pattern': [r'.*报告.*\.md$', r'.*报告.*\.txt$', r'.*_report.*\.md$'],
                'target': '05_Outputs/Reports/{date}/',
                'description': '各类报告文件'
            },

            # 3. 日志文件（按日期归档）
            'logs': {
                'pattern': [r'.*_log.*\.txt$', r'.*_log.*\.log$'],
                'target': '06_Learning_Journal/daily_logs/{date}/',
                'description': '日志文件'
            },

            # 4. 配置和启动脚本
            'scripts': {
                'pattern': [r'.*\.bat$', r'.*\.ps1$'],
                'target': '00_Agent_Library/99_Scripts_Tools/',
                'exclude': [r'^start_new_session', r'^butler_mode'],
                'description': '脚本工具'
            },

            # 5. Python工具（非核心工具）
            'python_tools': {
                'pattern': [r'.*_test.*\.py$', r'demo.*\.py$', r'.*debug.*\.py$'],
                'target': '00_Agent_Library/02_Code_Snippets/测试和调试/',
                'description': '测试和演示脚本'
            },

            # 6. 文档文件
            'docs': {
                'pattern': [r'.*指南.*\.md$', r'.*说明.*\.md$', r'.*README.*\.md$'],
                'target': '04_Data_&_Resources/Learning_Materials/',
                'exclude': [r'^README\.md$'],
                'description': '学习资料和文档'
            },

            # 7. 临时文件
            'temp': {
                'pattern': [r'.*\.tmp$', r'.*\.cache$', r'.*~$'],
                'target': '00_Temp/{date}/',
                'description': '临时文件'
            },

            # 8. 测试输出
            'test_output': {
                'pattern': [r'test_.*\..*', r'.*_test\..*'],
                'target': '00_Temp/Tests/{date}/',
                'description': '测试输出文件'
            },
        }

    def should_keep_in_root(self, filename):
        """检查文件是否应该保留在根目录"""
        for pattern in self.rules['keep_in_root']:
            if re.match(pattern, filename, re.IGNORECASE):
                return True
        return False

    def classify_file(self, filepath):
        """分类单个文件"""
        filename = filepath.name

        # 检查是否应该保留在根目录
        if self.should_keep_in_root(filename):
            return None, 'keep_in_root'

        # 遍历所有分类规则
        for category, rule in self.rules.items():
            if category == 'keep_in_root':
                continue

            for pattern in rule.get('pattern', []):
                if re.match(pattern, filename, re.IGNORECASE):
                    # 检查排除规则
                    if 'exclude' in rule:
                        should_exclude = any(
                            re.match(exclude_pattern, filename, re.IGNORECASE)
                            for exclude_pattern in rule['exclude']
                        )
                        if should_exclude:
                            continue

                    # 替换日期占位符
                    target_path = rule['target'].format(date=self.today)
                    return category, target_path

        # 未分类的文件
        return None, 'uncategorized'

    def organize(self, dry_run=False):
        """执行文件整理"""
        print("=" * 70)
        print("📁 每日文件自动整理器 - 智能混合模式")
        print("=" * 70)
        print(f"📍 工作区: {self.workspace_root}")
        print(f"📅 日期: {self.today}")
        print(f"🔍 模式: {'模拟运行（不会移动文件）' if dry_run else '实际运行'}")
        print()

        # 获取根目录的所有文件
        files = [f for f in self.workspace_root.iterdir() if f.is_file()]

        if not files:
            print("✅ 根目录没有需要整理的文件")
            return self.stats

        print(f"📊 发现 {len(files)} 个文件，开始分类...")
        print()

        # 处理每个文件
        for filepath in files:
            category, target = self.classify_file(filepath)

            if target == 'keep_in_root':
                self.stats['skipped'] += 1
                print(f"⏭️  保留: {filepath.name} (核心文件)")
                continue

            if target == 'uncategorized':
                self.stats['skipped'] += 1
                print(f"❓ 跳过: {filepath.name} (未分类)")
                continue

            # 执行移动操作
            target_path = self.workspace_root / target / filepath.name

            if dry_run:
                print(f"📋 将移动: {filepath.name}")
                print(f"   → {target}")
                self.stats['moved'] += 1
                self.stats['details'].append({
                    'file': filepath.name,
                    'from': str(filepath),
                    'to': str(target_path),
                    'category': category
                })
            else:
                try:
                    # 创建目标目录
                    target_path.parent.mkdir(parents=True, exist_ok=True)

                    # 移动文件
                    shutil.move(str(filepath), str(target_path))
                    print(f"✅ 已移动: {filepath.name}")
                    print(f"   → {target}")
                    self.stats['moved'] += 1
                    self.stats['details'].append({
                        'file': filepath.name,
                        'from': str(filepath),
                        'to': str(target_path),
                        'category': category
                    })
                except Exception as e:
                    print(f"❌ 错误: {filepath.name} - {e}")
                    self.stats['errors'] += 1

        # 打印统计信息
        print()
        print("=" * 70)
        print("📊 整理完成统计")
        print("=" * 70)
        print(f"✅ 已移动: {self.stats['moved']} 个文件")
        print(f"⏭️  已跳过: {self.stats['skipped']} 个文件")
        print(f"❌ 错误: {self.stats['errors']} 个文件")
        print()

        return self.stats

    def generate_report(self):
        """生成整理报告"""
        report_path = self.workspace_root / f"05_Outputs/Reports/file_organize_report_{self.today}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 文件整理报告\n\n")
            f.write(f"**日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**工作区**: {self.workspace_root}\n\n")
            f.write("## 统计信息\n\n")
            f.write(f"- ✅ 已移动: {self.stats['moved']} 个文件\n")
            f.write(f"- ⏭️  已跳过: {self.stats['skipped']} 个文件\n")
            f.write(f"- ❌ 错误: {self.stats['errors']} 个文件\n\n")

            if self.stats['details']:
                f.write("## 文件移动详情\n\n")
                for detail in self.stats['details']:
                    f.write(f"### {detail['file']}\n")
                    f.write(f"- **分类**: {detail['category']}\n")
                    f.write(f"- **原位置**: `{detail['from']}`\n")
                    f.write(f"- **新位置**: `{detail['to']}`\n\n")

        print(f"📄 报告已生成: {report_path}")
        return report_path


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='每日文件自动整理器')
    parser.add_argument('--dry-run', action='store_true',
                       help='模拟运行，不实际移动文件')
    parser.add_argument('--workspace', type=str, default=None,
                       help='工作区路径（默认为当前目录）')

    args = parser.parse_args()

    # 创建整理器
    organizer = DailyFileOrganizer(args.workspace)

    # 执行整理
    stats = organizer.organize(dry_run=args.dry_run)

    # 生成报告
    if not args.dry_run and stats['moved'] > 0:
        organizer.generate_report()

    print()
    print("✨ 整理完成！")
    if args.dry_run:
        print("💡 这是模拟运行，使用 --no-dry-run 参数执行实际整理")


if __name__ == '__main__':
    main()
