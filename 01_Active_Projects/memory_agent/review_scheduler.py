#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复习调度器
使用间隔重复算法（Spaced Repetition）智能提醒复习
"""

import yaml
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from vector_store import VectorStore


class ReviewScheduler:
    """复习调度系统 - 基于间隔重复算法"""

    def __init__(self, config_path="config.yaml"):
        """初始化复习调度器"""
        # 加载配置
        config_path = Path(__file__).parent / config_path
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.workspace_root = Path(__file__).parent.parent.parent
        self.vector_store = VectorStore(config_path)

        # 复习间隔配置（天）
        self.intervals = self.config['review']['intervals']
        self.daily_limit = self.config['review']['daily_limit']

        # 复习记录文件
        self.review_db_path = self.workspace_root / "06_Learning_Journal" / "workspace_memory" / "review_schedule.json"

        # 加载复习记录
        self.review_records = self._load_review_records()

    def _load_review_records(self) -> Dict:
        """加载复习记录"""
        if self.review_db_path.exists():
            try:
                with open(self.review_db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  加载复习记录失败: {e}")

        return {
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'records': {}
        }

    def _save_review_records(self):
        """保存复习记录"""
        self.review_db_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.review_db_path, 'w', encoding='utf-8') as f:
            json.dump(self.review_records, f, ensure_ascii=False, indent=2)

    def add_to_review(self, doc_id: str, initial_interval: int = 0):
        """
        添加文档到复习队列

        Args:
            doc_id: 文档ID
            initial_interval: 初始间隔（天数）
        """
        if doc_id in self.review_records['records']:
            print(f"⚠️  文档已在复习队列中")
            return

        now = datetime.now()
        next_review = now + timedelta(days=initial_interval)

        self.review_records['records'][doc_id] = {
            'interval_index': 0,
            'review_count': 0,
            'last_review': now.strftime("%Y-%m-%d %H:%M:%S"),
            'next_review': next_review.strftime("%Y-%m-%d %H:%M:%S"),
            'ease_factor': 2.5,  # SM-2算法的易度因子
            'created_at': now.strftime("%Y-%m-%d %H:%M:%S")
        }

        self._save_review_records()
        print(f"✅ 已添加到复习队列")

    def mark_reviewed(self, doc_id: str, quality: int = 4):
        """
        标记文档已复习

        Args:
            doc_id: 文档ID
            quality: 复习质量评分（0-5）
                    5: 完美记忆
                    4: 正确但犹豫
                    3: 回忆起但困难
                    2: 错误但有印象
                    1: 错误且无印象
                    0: 完全忘记
        """
        if doc_id not in self.review_records['records']:
            print(f"❌ 文档不在复习队列中")
            return

        record = self.review_records['records'][doc_id]

        # 使用SM-2算法计算下次复习时间
        # 简化版：根据质量评分调整间隔
        if quality >= 3:
            # 答对了，推进到下一个间隔
            record['interval_index'] = min(
                record['interval_index'] + 1,
                len(self.intervals) - 1
            )
            record['ease_factor'] = max(1.3, record['ease_factor'] + 0.1)
        else:
            # 答错了，重置间隔
            record['interval_index'] = 0
            record['ease_factor'] = max(1.3, record['ease_factor'] - 0.2)

        # 计算下次复习时间
        interval_days = self.intervals[record['interval_index']]
        next_review = datetime.now() + timedelta(days=interval_days)

        record['review_count'] += 1
        record['last_review'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record['next_review'] = next_review.strftime("%Y-%m-%d %H:%M:%S")

        self._save_review_records()
        print(f"✅ 复习完成，{interval_days}天后再次复习")

    def get_due_reviews(self) -> List[Dict]:
        """
        获取到期需要复习的文档

        Returns:
            待复习文档列表
        """
        now = datetime.now()
        due_docs = []

        for doc_id, record in self.review_records['records'].items():
            next_review = datetime.strptime(record['next_review'], "%Y-%m-%d %H:%M:%S")

            if next_review <= now:
                # 获取文档详情
                doc = self.vector_store.get_document(doc_id)
                if doc:
                    due_docs.append({
                        'id': doc_id,
                        'metadata': doc['metadata'],
                        'content': doc['document'],
                        'review_info': record
                    })

        # 按优先级排序（ overdue 最长优先）
        due_docs.sort(
            key=lambda x: datetime.strptime(x['review_info']['last_review'], "%Y-%m-%d %H:%M:%S")
        )

        return due_docs[:self.daily_limit]

    def get_all_reviews(self) -> List[Dict]:
        """获取所有复习记录"""
        all_reviews = []

        for doc_id, record in self.review_records['records'].items():
            doc = self.vector_store.get_document(doc_id)
            if doc:
                all_reviews.append({
                    'id': doc_id,
                    'metadata': doc['metadata'],
                    'review_info': record
                })

        return all_reviews

    def get_statistics(self) -> Dict:
        """获取复习统计信息"""
        now = datetime.now()
        total = len(self.review_records['records'])
        due_count = 0
        overdue_count = 0

        for record in self.review_records['records'].values():
            next_review = datetime.strptime(record['next_review'], "%Y-%m-%d %H:%M:%S")

            if next_review <= now:
                due_count += 1

            if next_review < now:
                overdue_count += 1

        return {
            'total_items': total,
            'due_today': due_count,
            'overdue': overdue_count,
            'intervals': self.intervals
        }

    def format_due_reviews(self, due_docs: List[Dict]) -> str:
        """格式化待复习文档"""
        if not due_docs:
            return "✅ 今天没有需要复习的内容！"

        output = []
        output.append("=" * 70)
        output.append(f"📖 待复习内容 ({len(due_docs)}项)")
        output.append("=" * 70)

        for i, doc in enumerate(due_docs, 1):
            metadata = doc['metadata']
            review_info = doc['review_info']

            output.append(f"\n{i}. {metadata.get('title', 'N/A')}")
            output.append(f"   📁 {metadata.get('path', 'N/A')}")
            output.append(f"   🔄 复习次数: {review_info['review_count']}")
            output.append(f"   ⏰ 上次复习: {review_info['last_review']}")

            # 内容预览
            content = doc['content']
            preview = content[:100] + "..." if len(content) > 100 else content
            output.append(f"   📝 {preview}")

        return '\n'.join(output)

    def format_statistics(self) -> str:
        """格式化统计信息"""
        stats = self.get_statistics()

        output = []
        output.append("=" * 70)
        output.append("📊 复习统计")
        output.append("=" * 70)
        output.append(f"总条目: {stats['total_items']}")
        output.append(f"今日待复习: {stats['due_today']}")
        output.append(f"已逾期: {stats['overdue']}")
        output.append(f"\n复习间隔: {stats['intervals']} 天")

        return '\n'.join(output)

    def interactive_review(self):
        """交互式复习模式"""
        print("\n" + "=" * 70)
        print("📖 学习记忆助手 - 复习模式")
        print("=" * 70)

        # 显示统计
        print(self.format_statistics())
        print()

        # 获取待复习内容
        due_docs = self.get_due_reviews()
        print(self.format_due_reviews(due_docs))
        print()

        if not due_docs:
            return

        print("提示:")
        print("  - 输入文档编号进行复习")
        print("  - 输入 'all' 复习所有")
        print("  - 输入 'quit' 退出")
        print()

        while True:
            try:
                choice = input("🔖 选择: ").strip()

                if not choice:
                    continue

                if choice.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 复习结束！")
                    break

                elif choice.lower() == 'all':
                    # 复习所有
                    for doc in due_docs:
                        self._review_single(doc)

                elif choice.isdigit():
                    # 复习单个
                    index = int(choice) - 1
                    if 0 <= index < len(due_docs):
                        self._review_single(due_docs[index])
                    else:
                        print("❌ 无效编号")

                else:
                    print("❌ 无效输入")

            except KeyboardInterrupt:
                print("\n\n👋 复习结束！")
                break

    def _review_single(self, doc: Dict):
        """复习单个文档"""
        metadata = doc['metadata']
        content = doc['content']
        doc_id = doc['id']

        print("\n" + "=" * 70)
        print(f"📄 {metadata.get('title', 'N/A')}")
        print("=" * 70)
        print(f"📁 {metadata.get('path', 'N/A')}")
        print(f"\n{content}")
        print("\n" + "=" * 70)

        print("\n评分你的记忆质量:")
        print("  5 - 完美记忆")
        print("  4 - 正确但犹豫")
        print("  3 - 回忆起但困难")
        print("  2 - 错误但有印象")
        print("  1 - 错误且无印象")
        print("  0 - 完全忘记")

        while True:
            try:
                quality = input("\n评分 (0-5): ").strip()
                if quality.lower() in ['skip', 's']:
                    print("⏭️  已跳过")
                    return

                quality = int(quality)
                if 0 <= quality <= 5:
                    self.mark_reviewed(doc_id, quality)
                    break
                else:
                    print("❌ 请输入0-5之间的数字")
            except ValueError:
                print("❌ 请输入数字")


def main():
    """主函数"""
    import sys

    scheduler = ReviewScheduler()

    if len(sys.argv) < 2:
        # 默认：交互式复习
        scheduler.interactive_review()

    else:
        command = sys.argv[1]

        if command == "due":
            # 查看待复习
            due = scheduler.get_due_reviews()
            print(scheduler.format_due_reviews(due))

        elif command == "stats":
            # 统计信息
            print(scheduler.format_statistics())

        elif command == "list":
            # 列出所有复习记录
            all_reviews = scheduler.get_all_reviews()
            print(f"\n共有 {len(all_reviews)} 个复习条目:\n")
            for i, item in enumerate(all_reviews, 1):
                metadata = item['metadata']
                review = item['review_info']
                print(f"{i}. {metadata.get('title', 'N/A')}")
                print(f"   下次复习: {review['next_review']}")
                print(f"   复习次数: {review['review_count']}")
                print()

        elif command == "add" and len(sys.argv) > 2:
            # 添加到复习队列
            doc_id = sys.argv[2]
            scheduler.add_to_review(doc_id)

        elif command == "interactive":
            # 交互式复习
            scheduler.interactive_review()

        else:
            print("用法:")
            print("  python review_scheduler.py                    # 交互式复习")
            print("  python review_scheduler.py due               # 查看待复习")
            print("  python review_scheduler.py stats             # 统计信息")
            print("  python review_scheduler.py list              # 列出所有")
            print("  python review_scheduler.py add <doc_id>      # 添加到复习")


if __name__ == "__main__":
    main()
