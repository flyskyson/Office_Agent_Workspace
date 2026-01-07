#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习日志记录工具
帮助快速记录每天的学习内容、遇到的问题和解决方案
"""

import os
from datetime import datetime
from pathlib import Path


class LearningLogger:
    """学习日志记录器"""

    def __init__(self, base_dir=None):
        """初始化日志记录器

        Args:
            base_dir: 学习日志目录，默认为 06_Learning_Journal/
        """
        if base_dir is None:
            # 获取脚本所在目录的父目录（工作区根目录）
            script_dir = Path(__file__).parent
            base_dir = script_dir

        self.base_dir = Path(base_dir)
        self.daily_logs_dir = self.base_dir / "daily_logs"

        # 确保目录存在
        self.daily_logs_dir.mkdir(parents=True, exist_ok=True)

    def get_today_log_path(self):
        """获取今日日志文件路径"""
        today = datetime.now()
        year_month = today.strftime("%Y-%m")
        filename = today.strftime("%Y-%m-%d.md")

        # 创建年月目录
        month_dir = self.daily_logs_dir / year_month
        month_dir.mkdir(exist_ok=True)

        return month_dir / filename

    def create_daily_log(self, content_type="auto"):
        """创建每日学习日志

        Args:
            content_type: 日志类型 (auto: 自动模板, custom: 自定义)
        """
        log_path = self.get_today_log_path()

        # 如果文件已存在，询问是否追加
        if log_path.exists():
            print(f"⚠️  今日日志已存在: {log_path}")
            choice = input("是否追加内容? (y/n): ").strip().lower()
            if choice != 'y':
                return None
            mode = 'a'
            print("\n--- 追加模式 ---")
        else:
            mode = 'w'

        if content_type == "auto":
            content = self._generate_auto_template()
        else:
            content = input("请输入日志内容:\n")

        # 写入文件
        with open(log_path, mode, encoding='utf-8') as f:
            if mode == 'w':
                f.write(content)
            else:
                f.write(f"\n\n{content}")

        print(f"\n✅ 日志已保存: {log_path}")
        return log_path

    def _generate_auto_template(self):
        """生成自动模板"""
        now = datetime.now()
        date_str = now.strftime("%Y年%m月%d日")
        weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]

        template = f"""# {date_str} {weekday}

**学习时间**: {now.strftime("%H:%M")}
**学习时长**: ___ 分钟
**心情指数**: ⭐⭐⭐⭐⭐

---

## 📚 今日学习内容

### 学习主题
- 主题:


### 学到的知识点
1.
2.
3.

---

## 🎯 完成任务

- [ ] 任务1
- [ ] 任务2
- [ ] 任务3

---

## 🐛 遇到的问题

### 问题1
**描述**:
**解决方案**:
**经验总结**:

---

## 💡 心得体会




---

## 🔗 相关资源

- 项目:
- 文档:
- 代码:

---

**AI助手备注**:

"""
        return template

    def record_challenge(self, title, problem, solution, category="bug"):
        """记录遇到的问题和解决方案

        Args:
            title: 问题标题
            problem: 问题描述
            solution: 解决方案
            category: 分类 (bug, concept, error, optimization)
        """
        challenges_dir = self.base_dir / "challenges_solved"
        challenges_dir.mkdir(exist_ok=True)

        # 根据分类选择文件
        category_files = {
            "bug": "bugs_fixed.md",
            "concept": "concepts_learned.md",
            "error": "errors_encountered.md",
            "optimization": "optimizations.md"
        }

        filename = category_files.get(category, "other_challenges.md")
        filepath = challenges_dir / filename

        # 生成条目
        now = datetime.now()
        entry = f"""
## {title}

**日期**: {now.strftime("%Y-%m-%d %H:%M")}
**分类**: {category}

### 📋 问题描述
{problem}

### ✅ 解决方案
{solution}

### 💡 经验总结



---

"""

        # 追加到文件
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(entry)

        print(f"✅ 问题已记录到: {filepath}")

    def record_code_pattern(self, title, description, code, use_case):
        """记录代码模式

        Args:
            title: 模式标题
            description: 描述
            code: 代码示例
            use_case: 使用场景
        """
        patterns_dir = self.base_dir / "code_patterns"
        patterns_dir.mkdir(exist_ok=True)

        # 根据语言分类
        if "python" in title.lower() or "def " in code:
            lang_dir = patterns_dir / "python"
        elif "javascript" in title.lower() or "function " in code:
            lang_dir = patterns_dir / "javascript"
        elif "powershell" in title.lower():
            lang_dir = patterns_dir / "powershell"
        else:
            lang_dir = patterns_dir / "general"

        lang_dir.mkdir(exist_ok=True)
        filepath = lang_dir / f"{title.replace(' ', '_')}.md"

        content = f"""# {title}

**描述**: {description}
**创建时间**: {datetime.now().strftime("%Y-%m-%d")}

## 使用场景
{use_case}

## 代码示例
```python
{code}
```

## 注意事项


---

"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 代码模式已保存: {filepath}")

    def update_skill_progress(self, skill_file, skill_name, new_level, notes=""):
        """更新技能进度

        Args:
            skill_file: 技能文件名 (如 python_skills.md)
            skill_name: 技能名称
            new_level: 新等级 (1-5星)
            notes: 备注
        """
        progress_dir = self.base_dir / "progress_tracker"
        progress_dir.mkdir(exist_ok=True)
        filepath = progress_dir / skill_file

        # 如果文件不存在，创建基础结构
        if not filepath.exists():
            initial_content = f"""# {skill_file.replace('_', ' ').replace('.md', '').title()}

**最后更新**: {datetime.now().strftime("%Y-%m-%d")}

---

## 技能进度表

| 技能 | 等级 | 更新日期 | 备注 |
|------|------|----------|------|

---

## 学习记录


"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(initial_content)

        # 读取文件并更新
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 简单追加记录（实际应用中可以用更复杂的表格更新逻辑）
        update_entry = f"""

### {datetime.now().strftime("%Y-%m-%d")}: {skill_name}
- **等级**: {"⭐" * new_level}{"☆" * (5 - new_level)}
- **备注**: {notes}

"""

        # 追加到学习记录部分
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(update_entry)

        print(f"✅ 技能进度已更新: {filepath}")

    def show_stats(self):
        """显示学习统计"""
        print("\n📊 学习日志统计\n")

        # 统计每日日志
        daily_count = len(list(self.daily_logs_dir.rglob("*.md")))
        print(f"📅 每日日志: {daily_count} 篇")

        # 统计解决的问题
        challenges_dir = self.base_dir / "challenges_solved"
        if challenges_dir.exists():
            for file in challenges_dir.glob("*.md"):
                # 统计问题数量（以##开头的标题）
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    count = content.count("## ")
                print(f"🐛 {file.name}: {count} 个问题")

        # 统计代码模式
        patterns_dir = self.base_dir / "code_patterns"
        if patterns_dir.exists():
            pattern_count = len(list(patterns_dir.rglob("*.md")))
            print(f"💡 代码模式: {pattern_count} 个")

        print()


def main():
    """命令行交互界面"""
    print("=" * 60)
    print("📝 学习日志记录工具")
    print("=" * 60)

    logger = LearningLogger()

    while True:
        print("\n请选择操作:")
        print("1. 创建今日学习日志")
        print("2. 记录遇到的问题")
        print("3. 保存代码模式")
        print("4. 更新技能进度")
        print("5. 查看学习统计")
        print("0. 退出")

        choice = input("\n请输入选项 (0-5): ").strip()

        if choice == '1':
            logger.create_daily_log()
        elif choice == '2':
            print("\n--- 记录问题 ---")
            title = input("问题标题: ").strip()
            category = input("分类 (bug/concept/error/optimization): ").strip() or "bug"
            print("\n问题描述:")
            problem = input().strip()
            print("\n解决方案:")
            solution = input().strip()
            logger.record_challenge(title, problem, solution, category)
        elif choice == '3':
            print("\n--- 保存代码模式 ---")
            title = input("模式标题: ").strip()
            description = input("描述: ").strip()
            use_case = input("使用场景: ").strip()
            print("\n代码示例:")
            code = input().strip()
            logger.record_code_pattern(title, description, code, use_case)
        elif choice == '4':
            print("\n--- 更新技能进度 ---")
            skill_file = input("技能文件 (如 python_skills.md): ").strip()
            skill_name = input("技能名称: ").strip()
            try:
                level = int(input("等级 (1-5): ").strip())
                notes = input("备注 (可选): ").strip()
                logger.update_skill_progress(skill_file, skill_name, level, notes)
            except ValueError:
                print("❌ 等级必须是数字")
        elif choice == '5':
            logger.show_stats()
        elif choice == '0':
            print("\n👋 继续加油，学习愉快!")
            break
        else:
            print("❌ 无效选项，请重新选择")


if __name__ == "__main__":
    main()
