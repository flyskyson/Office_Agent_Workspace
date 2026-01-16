#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习记忆助手 - 主程序
统一入口点，整合所有功能
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from indexer import DocumentIndexer
from search import SemanticSearch
from recommender import SmartRecommender
from review_scheduler import ReviewScheduler


class MemoryAgent:
    """学习记忆助手 - 你的第二大脑"""

    def __init__(self):
        """初始化助手"""
        self.indexer = DocumentIndexer()
        self.search_engine = SemanticSearch()
        self.recommender = SmartRecommender()
        self.scheduler = ReviewScheduler()

    def build_index(self):
        """构建/更新索引"""
        print("\n" + "=" * 70)
        print("🚀 学习记忆助手 - 构建索引")
        print("=" * 70)
        self.indexer.build_index()

    def search(self, query: str):
        """语义搜索"""
        print(f"\n🔍 搜索: '{query}'")
        results = self.search_engine.search(query)
        print(self.search_engine.format_results(results))

    def search_code(self, query: str):
        """搜索代码"""
        print(f"\n💻 搜索代码: '{query}'")
        results = self.search_engine.search_code(query)
        print(self.search_engine.format_results(results))

    def search_notes(self, query: str):
        """搜索笔记"""
        print(f"\n📓 搜索笔记: '{query}'")
        results = self.search_engine.search_notes(query)
        print(self.search_engine.format_results(results))

    def find_similar(self, problem: str):
        """查找相似问题"""
        print(f"\n💭 查找相似问题: '{problem}'")
        results = self.recommender.find_similar_problems(problem)
        print(self.recommender.format_similar_problems(results))

    def get_learning_path(self, topic: str):
        """获取学习路径"""
        print(f"\n📚 学习路径: '{topic}'")
        path = self.recommender.get_learning_path(topic)
        print(self.recommender.format_learning_path(path))

    def review_today(self):
        """今日复习"""
        print("\n" + "=" * 70)
        print("📖 今日复习")
        print("=" * 70)
        print(self.scheduler.format_statistics())

        due = self.scheduler.get_due_reviews()
        print(self.scheduler.format_due_reviews(due))

    def interactive_review(self):
        """交互式复习"""
        self.scheduler.interactive_review()

    def show_menu(self):
        """显示主菜单"""
        menu = """
╔════════════════════════════════════════════════════════════════════╗
║          🧠 学习记忆助手 - 你的第二大脑                          ║
╚════════════════════════════════════════════════════════════════════╝

📚 核心功能:
  1. 🔍 语义搜索      - 智能搜索你的笔记和代码
  2. 💻 搜索代码      - 只搜索项目代码
  3. 📓 搜索笔记      - 只搜索学习笔记
  4. 💭 相似问题      - 查找历史相似问题

📖 学习助手:
  5. 🎯 学习路径      - 获取主题学习路径推荐
  6. 📅 今日复习      - 查看待复习内容
  7. 🔄 交互复习      - 交互式复习模式

🛠️  维护:
  8. 🚀 构建索引      - 扫描并索引学习资料
  9. 📊 统计信息      - 查看数据库统计

  0. 退出
"""
        print(menu)

    def run(self):
        """交互式运行"""
        while True:
            self.show_menu()

            try:
                choice = input("\n请选择操作 (0-9): ").strip()

                if choice == '0':
                    print("\n👋 再见！祝学习愉快！")
                    break

                elif choice == '1':
                    query = input("🔍 搜索: ").strip()
                    if query:
                        self.search(query)

                elif choice == '2':
                    query = input("💻 搜索代码: ").strip()
                    if query:
                        self.search_code(query)

                elif choice == '3':
                    query = input("📓 搜索笔记: ").strip()
                    if query:
                        self.search_notes(query)

                elif choice == '4':
                    problem = input("💭 问题描述: ").strip()
                    if problem:
                        self.find_similar(problem)

                elif choice == '5':
                    topic = input("🎯 学习主题: ").strip()
                    if topic:
                        self.get_learning_path(topic)

                elif choice == '6':
                    self.review_today()

                elif choice == '7':
                    self.interactive_review()

                elif choice == '8':
                    confirm = input("⚠️  确定要重新构建索引吗？(yes/no): ").strip().lower()
                    if confirm == 'yes':
                        self.build_index()
                    else:
                        print("❌ 已取消")

                elif choice == '9':
                    stats = self.scheduler.format_statistics()
                    print(f"\n{stats}")
                    print(f"\n📚 数据库文档数: {self.indexer.vector_store.count()}")

                else:
                    print("\n❌ 无效选项")

                input("\n按回车继续...")

            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 出错: {e}")
                input("\n按回车继续...")


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║     🧠  学习记忆助手  -  Memory Agent                            ║
║                                                                    ║
║              你的第二大脑 · 智能知识管理助手                      ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main():
    """主函数"""
    # 切换到脚本目录
    import os
    os.chdir(Path(__file__).parent)

    print_banner()

    agent = MemoryAgent()

    # 命令行模式
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "index":
            agent.build_index()

        elif command == "search" and len(sys.argv) > 2:
            query = ' '.join(sys.argv[2:])
            agent.search(query)

        elif command == "code" and len(sys.argv) > 2:
            query = ' '.join(sys.argv[2:])
            agent.search_code(query)

        elif command == "note" and len(sys.argv) > 2:
            query = ' '.join(sys.argv[2:])
            agent.search_notes(query)

        elif command == "similar" and len(sys.argv) > 2:
            problem = ' '.join(sys.argv[2:])
            agent.find_similar(problem)

        elif command == "path" and len(sys.argv) > 2:
            topic = ' '.join(sys.argv[2:])
            agent.get_learning_path(topic)

        elif command == "review":
            agent.review_today()

        elif command == "interactive":
            agent.interactive_review()

        else:
            print("用法:")
            print("  交互模式: python memory_agent.py")
            print("  构建索引: python memory_agent.py index")
            print("  语义搜索: python memory_agent.py search <查询>")
            print("  搜索代码: python memory_agent.py code <查询>")
            print("  搜索笔记: python memory_agent.py note <查询>")
            print("  相似问题: python memory_agent.py similar <问题>")
            print("  学习路径: python memory_agent.py path <主题>")
            print("  今日复习: python memory_agent.py review")
            print("  交互复习: python memory_agent.py interactive")

    else:
        # 交互模式
        agent.run()


if __name__ == "__main__":
    main()
