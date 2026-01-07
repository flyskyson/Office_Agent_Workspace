#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目规划助手 - 专为办公自动化和网页自动化设计
帮助用户根据技能水平和需求规划合适的项目
"""

import os
from datetime import datetime
from pathlib import Path
import json


class ProjectPlanner:
    """项目规划助手"""

    def __init__(self, workspace_root=None):
        """初始化规划助手

        Args:
            workspace_root: 工作区根目录
        """
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent
        else:
            workspace_root = Path(workspace_root)

        self.workspace_root = workspace_root
        self.ai_memory_path = workspace_root / "06_Learning_Journal" / "AI_MEMORY.md"
        self.projects_dir = workspace_root / "01_Active_Projects"
        self.archive_dir = workspace_root / "02_Project_Archive"

        # 项目难度等级
        self.levels = {
            1: "入门级 - 适合初学者",
            2: "初级 - 需要基础知识",
            3: "中级 - 需要一些经验",
            4: "进阶级 - 需要较多经验",
            5: "高级 - 需要深入理解"
        }

    def read_ai_memory(self):
        """读取AI记忆文件"""
        if not self.ai_memory_path.exists():
            print(f"⚠️  未找到 AI_MEMORY.md: {self.ai_memory_path}")
            return None

        with open(self.ai_memory_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print("✅ 已读取开发者档案")
        return content

    def analyze_user_profile(self, memory_content):
        """分析用户档案

        Args:
            memory_content: AI_MEMORY.md 的内容

        Returns:
            dict: 用户画像信息
        """
        profile = {
            "identity": "编程学习者",
            "current_level": 1,
            "skills": [],
            "completed_projects": [],
            "learning_goals": [],
            "preferences": []
        }

        if not memory_content:
            return profile

        # 简单的关键词提取（实际可用更复杂的解析）
        if "Python基础" in memory_content:
            if "⭐⭐⭐" in memory_content:
                profile["current_level"] = 3
            elif "⭐⭐" in memory_content:
                profile["current_level"] = 2

        if "公务员" in memory_content or "办公自动化" in memory_content:
            profile["identity"] = "公务员 - 办公自动化方向"
            profile["preferences"].extend(["办公自动化", "文档处理", "数据整理"])

        if "AI Agent" in memory_content:
            profile["skills"].append("AI_Agent_Development")

        if "web_monitor_agent" in memory_content or "my_first_agent" in memory_content:
            profile["completed_projects"] = ["Agent开发基础"]

        if "pdf_processor" in memory_content:
            profile["completed_projects"].append("PDF处理")

        return profile

    def get_recommended_projects(self, user_profile):
        """根据用户画像推荐项目

        Args:
            user_profile: 用户画像信息

        Returns:
            list: 推荐项目列表
        """
        recommendations = []

        # 办公自动化项目库
        office_projects = [
            {
                "name": "Excel自动化报表生成器",
                "description": "自动读取多个Excel文件，汇总数据，生成报表和图表",
                "level": 2,
                "skills": ["pandas", "openpyxl", "数据可视化"],
                "duration": "3-5天",
                "value": "★★★★★",
                "category": "办公自动化"
            },
            {
                "name": "Word文档批量处理工具",
                "description": "批量替换Word文档内容，统一格式，生成报告",
                "level": 2,
                "skills": ["python-docx", "字符串处理", "文件操作"],
                "duration": "2-3天",
                "value": "★★★★☆",
                "category": "办公自动化"
            },
            {
                "name": "PPT自动生成器",
                "description": "根据模板和数据自动生成PowerPoint演示文稿",
                "level": 2,
                "skills": ["python-pptx", "模板设计", "数据映射"],
                "duration": "3-4天",
                "value": "★★★★★",
                "category": "办公自动化"
            },
            {
                "name": "邮件自动分类和回复助手",
                "description": "自动分类邮件，识别重要信息，生成回复草稿",
                "level": 3,
                "skills": ["IMAP/SMTP", "邮件处理", "文本分析"],
                "duration": "5-7天",
                "value": "★★★★★",
                "category": "办公自动化"
            },
            {
                "name": "文件智能整理工具",
                "description": "自动分类下载文件夹的文件，按类型/日期整理",
                "level": 2,
                "skills": ["文件操作", "路径处理", "规则引擎"],
                "duration": "2-3天",
                "value": "★★★★☆",
                "category": "办公自动化"
            }
        ]

        # 网页自动化项目库
        web_projects = [
            {
                "name": "网页表单自动填写助手",
                "description": "自动填写和提交重复性网页表单",
                "level": 2,
                "skills": ["Playwright/Selenium", "表单操作", "数据填充"],
                "duration": "3-4天",
                "value": "★★★★★",
                "category": "网页自动化"
            },
            {
                "name": "网站数据监控Agent",
                "description": "定期监控指定网站，检测变化并发送通知",
                "level": 3,
                "skills": ["网页抓取", "定时任务", "变化检测"],
                "duration": "4-5天",
                "value": "★★★★☆",
                "category": "网页自动化"
            },
            {
                "name": "多网站信息聚合工具",
                "description": "从多个网站抓取信息，整合生成日报",
                "level": 3,
                "skills": ["数据抓取", "数据清洗", "报告生成"],
                "duration": "5-7天",
                "value": "★★★★★",
                "category": "网页自动化"
            },
            {
                "name": "网页截图和PDF归档工具",
                "description": "批量截图网页并保存为PDF，自动归档",
                "level": 2,
                "skills": ["浏览器自动化", "PDF生成", "文件管理"],
                "duration": "2-3天",
                "value": "★★★★☆",
                "category": "网页自动化"
            }
        ]

        # AI Agent项目库
        agent_projects = [
            {
                "name": "智能会议助手Agent",
                "description": "记录会议内容，提取行动项，生成会议纪要",
                "level": 3,
                "skills": ["语音识别", "文本摘要", "Agent设计"],
                "duration": "7-10天",
                "value": "★★★★★",
                "category": "AI_Agent"
            },
            {
                "name": "文档问答助手",
                "description": "基于文档内容进行智能问答和检索",
                "level": 4,
                "skills": ["向量数据库", "文本嵌入", "RAG架构"],
                "duration": "10-14天",
                "value": "★★★★★",
                "category": "AI_Agent"
            },
            {
                "name": "工作流自动化Agent",
                "description": "理解复杂工作流，自动协调多个任务",
                "level": 4,
                "skills": ["Agent编排", "任务调度", "状态管理"],
                "duration": "10-15天",
                "value": "★★★★★",
                "category": "AI_Agent"
            }
        ]

        # 根据用户偏好和等级筛选
        all_projects = office_projects + web_projects + agent_projects

        # 过滤符合用户等级的项目（不超过当前等级+1）
        suitable_level = user_profile.get("current_level", 1) + 1
        recommendations = [p for p in all_projects if p["level"] <= suitable_level]

        # 根据偏好排序
        preferences = user_profile.get("preferences", [])
        if preferences:
            for pref in preferences:
                for project in recommendations:
                    if pref.lower() in project["category"].lower():
                        project["match_score"] = project.get("match_score", 0) + 2

        # 按匹配度和价值排序
        recommendations.sort(key=lambda x: (x.get("match_score", 0), x["value"]), reverse=True)

        return recommendations[:10]  # 返回前10个推荐

    def generate_learning_path(self, project):
        """生成项目的学习路径

        Args:
            project: 项目信息字典

        Returns:
            str: 学习路径描述
        """
        path = f"""
## 📚 学习路径：{project['name']}

### 阶段1：准备工作 (0.5天)
- [ ] 安装必要的依赖包
- [ ] 学习基础概念
- [ ] 搭建开发环境

### 阶段2：核心功能学习 (1-2天)
- [ ] 学习主要技能：{', '.join(project['skills'][:2])}
- [ ] 完成小练习
- [ ] 理解关键API

### 阶段3：项目开发 ({project['duration']})
- [ ] 设计项目结构
- [ ] 实现基础功能
- [ ] 添加错误处理
- [ ] 测试和优化

### 阶段4：总结和扩展 (0.5天)
- [ ] 编写文档
- [ ] 记录遇到的问题
- [ ] 思考扩展功能

### 推荐学习资源
- 官方文档
- 00_Agent_Library/02_Code_Snippets/ 中的相关代码片段
- AI助手结对编程
"""
        return path

    def create_project_plan(self, user_needs):
        """创建项目计划

        Args:
            user_needs: 用户需求描述

        Returns:
            dict: 项目计划
        """
        # 读取用户档案
        memory_content = self.read_ai_memory()
        user_profile = self.analyze_user_profile(memory_content)

        # 获取推荐项目
        recommendations = self.get_recommended_projects(user_profile)

        # 生成计划
        plan = {
            "user_profile": user_profile,
            "recommendations": recommendations,
            "next_steps": self._generate_next_steps(user_profile, recommendations),
            "quick_start": self._generate_quick_start()
        }

        return plan

    def _generate_next_steps(self, user_profile, recommendations):
        """生成下一步建议"""
        level = user_profile.get("current_level", 1)

        if level == 1:
            return """
### 🎯 建议的起步项目

作为初学者，建议从以下项目开始：

1. **Excel自动化报表生成器** (入门级)
   - 为什么推荐：实用性高，容易上手，立竿见影
   - 学到的技能：数据处理、文件操作、自动化思维

2. **文件智能整理工具** (入门级)
   - 为什么推荐：贴近日常，逻辑清晰
   - 学到的技能：路径处理、规则引擎、文件管理

**学习建议**：
- 一次只做一个项目
- 遇到问题及时记录到 06_Learning_Journal/
- 完成后更新 AI_MEMORY.md 中的技能进度
"""
        else:
            top_3 = recommendations[:3]
            projects_desc = "\n".join([
                f"{i+1}. **{p['name']}** ({p['category']}, 等级{p['level']})\n"
                f"   - {p['description']}\n"
                f"   - 预计用时：{p['duration']}\n"
                for i, p in enumerate(top_3)
            ])

            return f"""
### 🎯 为您推荐的项目

基于您的技能水平和偏好，推荐以下项目：

{projects_desc}

**选择建议**：
- 优先选择价值★★★★★的项目
- 考虑与工作相关的项目
- 挑战稍高于当前水平的项目
"""

    def _generate_quick_start(self):
        """生成快速开始指南"""
        return """
## 🚀 快速开始新项目

### 步骤1: 选择项目
从上面的推荐中选择一个感兴趣的项目

### 步骤2: 创建项目目录
```bash
cd 01_Active_Projects
mkdir your_project_name
cd your_project_name
python -m venv venv
venv\\Scripts\\activate  # Windows
```

### 步骤3: 初始化项目
```bash
# 创建基础结构
mkdir src tests data docs

# 创建 README.md
echo "# Your Project Name" > README.md

# 创建 requirements.txt
echo "your-dependencies-here" > requirements.txt
```

### 步骤4: 开始开发
- 告诉AI助手你选择的项目
- AI会帮助你一步步实现
- 记得记录学习日志！

### 步骤5: 记录和总结
完成后，运行：
```bash
python 06_Learning_Journal/learning_logger.py
```
记录你的学习心得
"""

    def print_plan(self, plan):
        """打印项目计划"""
        print("\n" + "="*70)
        print("项目规划报告")
        print("="*70)

        # 用户画像
        profile = plan["user_profile"]
        print(f"\n开发者画像")
        print(f"身份：{profile['identity']}")
        print(f"当前水平：{self.levels.get(profile['current_level'], '未知')}")
        if profile.get("skills"):
            print(f"已掌握技能：{', '.join(profile['skills'])}")
        if profile.get("completed_projects"):
            print(f"已完成项目：{', '.join(profile['completed_projects'])}")

        # 下一步建议
        print(plan["next_steps"])

        # 快速开始
        print(plan["quick_start"])

        print("\n" + "="*70)
        print("提示：告诉AI助手你想做哪个项目，我会帮助你开始！")
        print("="*70 + "\n")

    def save_plan_to_file(self, plan, filename=None):
        """保存计划到文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"项目计划_{timestamp}.md"

        output_path = self.workspace_root / "05_Outputs" / filename
        output_path.parent.mkdir(exist_ok=True)

        # 生成Markdown内容
        content = f"""# 项目规划报告

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 👤 开发者画像

**身份**: {plan['user_profile']['identity']}
**当前水平**: {self.levels.get(plan['user_profile']['current_level'], '未知')}
**已掌握技能**: {', '.join(plan['user_profile'].get('skills', ['待补充']))}
**已完成项目**: {', '.join(plan['user_profile'].get('completed_projects', ['暂无']))}

---

{plan['next_steps']}

{plan['quick_start']}

---

## 📊 推荐项目详情

"""

        # 添加项目详情
        for i, project in enumerate(plan['recommendations'][:5], 1):
            content += f"""
### {i}. {project['name']}

**分类**: {project['category']}
**难度**: 等级 {project['level']} - {self.levels[project['level']]}
**预计用时**: {project['duration']}
**实用价值**: {project['value']}

**项目描述**:
{project['description']}

**涉及技能**:
{chr(10).join([f"- {skill}" for skill in project['skills']])}

{self.generate_learning_path(project)}

---

"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] 项目计划已保存到: {output_path}")
        return output_path


def main():
    """交互式命令行界面"""
    import sys
    import io

    # 设置UTF-8编码输出
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("="*70)
    print("项目规划助手")
    print("专为办公自动化和网页自动化设计")
    print("="*70)

    planner = ProjectPlanner()

    print("\n正在分析您的档案和需求...")
    plan = planner.create_project_plan("办公自动化和网页自动化")

    # 打印计划
    planner.print_plan(plan)

    # 询问是否保存
    save_choice = input("\n是否保存项目计划到文件? (y/n): ").strip().lower()
    if save_choice == 'y':
        planner.save_plan_to_file(plan)

    print("\n现在告诉AI助手你想做哪个项目吧！")


if __name__ == "__main__":
    main()
