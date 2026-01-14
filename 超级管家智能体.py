#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超级管家智能体 - 工作区总管
一个对话式智能体，由AI扮演管家角色，与用户进行自然对话

作者: 工作区超级管家
版本: v2.0
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import time

# Windows UTF-8 修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class SuperButlerAgent:
    """超级管家智能体 - 你的工作区总管"""

    def __init__(self, workspace_root=None):
        """初始化管家"""
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        else:
            workspace_root = Path(workspace_root)

        self.workspace_root = workspace_root
        self.memory_dir = workspace_root / "06_Learning_Journal" / "workspace_memory"
        self.projects_dir = workspace_root / "01_Active_Projects"

        # 管家的问候语
        self.greetings = {
            'morning': ['早上好！新的一天开始了！', '早安！今天准备做点什么？', '早上好，主人！'],
            'afternoon': ['下午好！需要我帮忙吗？', '午安！工作还顺利吗？', '下午好，有什么可以为您效劳的？'],
            'evening': ['晚上好！今天辛苦了', '晚上好！要总结一下今天的工作吗？', '晚上好，主人！']
        }

        # 加载工作区数据
        self.workspace_data = self.load_workspace_data()

    def load_workspace_data(self):
        """加载工作区数据"""
        index_file = self.memory_dir / "workspace_index_latest.json"

        if not index_file.exists():
            return None

        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[管家] 加载数据时出错: {e}")
            return None

    def get_time_greeting(self):
        """根据时间获取问候语"""
        hour = datetime.now().hour

        if 5 <= hour < 12:
            return self.greetings['morning']
        elif 12 <= hour < 18:
            return self.greetings['afternoon']
        else:
            return self.greetings['evening']

    def introduce(self):
        """管家自我介绍"""
        greeting = self.get_time_greeting()
        import random
        chosen_greeting = random.choice(greeting)

        print("\n" + "=" * 70)
        print(f"[管家] {chosen_greeting}")
        print("=" * 70)
        print()
        print("  我是您的超级管家，工作区的总管。")
        print("  我可以帮您：")
        print("    - 查看工作区状态")
        print("    - 管理项目和文件")
        print("    - 启动其他工具")
        print("    - 提供建议和帮助")
        print()
        print("  您可以随时用自然语言和我对话，或者输入 'help' 查看我能做的事。")
        print()
        print("  输入 'quit' 或 'exit' 退出，输入 'ai' 来与AI对话")
        print()

    def show_menu(self):
        """显示管家菜单"""
        print("\n" + "-" * 70)
        print("[管家] 我能为您做些什么？")
        print("-" * 70)
        print("  1. status    - 查看工作区状态")
        print("  2. projects  - 查看项目列表")
        print("  3. tools     - 查看可用工具")
        print("  4. launch    - 启动工具")
        print("  5. organize  - 整理文件")
        print("  6. snapshot  - 创建快照")
        print("  7. report    - 生成报告")
        print("  8. ai        - 与AI对话")
        print("  9. help      - 显示帮助")
        print("  0. quit/exit - 退出")
        print("-" * 70)

    def get_workspace_status(self):
        """获取工作区状态"""
        if self.workspace_data is None:
            return "[管家] 抱歉，我暂时无法加载工作区数据。请先运行工作区扫描。"

        # 解析工作区数据
        data = self.workspace_data

        status = "\n"
        status += "=" * 70 + "\n"
        status += "[管家] 工作区状态报告\n"
        status += "=" * 70 + "\n\n"

        # 扫描时间
        scan_time = data.get('scan_time', '未知')
        status += f"[扫描时间] {scan_time}\n\n"

        # 项目统计
        projects = data.get('active_projects', {})
        status += f"[活跃项目] 共 {len(projects)} 个\n"

        for name, info in projects.items():
            file_count = info.get('python_files', 0)
            status += f"  - {name} ({file_count} 个文件)\n"

        status += "\n"

        # 工具统计
        tools = data.get('python_tools', {})
        status += f"[可用工具] 共 {len(tools)} 个\n"

        # 数据新鲜度
        if 'data_freshness' in data:
            freshness = data['data_freshness']
            status += f"\n[数据状态] {freshness.get('status', '未知')}\n"

        status += "\n" + "=" * 70

        return status

    def get_projects_list(self):
        """获取项目列表"""
        if self.workspace_data is None:
            return "[管家] 暂无数据"

        projects = self.workspace_data.get('active_projects', {})

        result = "\n"
        result += "=" * 70 + "\n"
        result += "[管家] 活跃项目列表\n"
        result += "=" * 70 + "\n\n"

        for name, info in projects.items():
            path = info.get('path', '未知')
            file_count = info.get('python_files', 0)
            modified = info.get('last_modified', '未知')

            result += f"[项目] {name}\n"
            result += f"  路径: {path}\n"
            result += f"  文件: {file_count} 个\n"
            result += f"  修改: {modified}\n\n"

        result += "=" * 70

        return result

    def get_tools_list(self):
        """获取工具列表"""
        if self.workspace_data is None:
            return "[管家] 暂无数据"

        tools = self.workspace_data.get('python_tools', {})

        result = "\n"
        result += "=" * 70 + "\n"
        result += "[管家] 可用工具列表\n"
        result += "=" * 70 + "\n\n"

        # 显示前20个工具
        count = 0
        for name, info in tools.items():
            if count >= 20:
                result += f"\n... 还有 {len(tools) - 20} 个工具\n"
                break

            modified = info.get('last_modified', '未知')
            result += f"  - {name} ({modified})\n"
            count += 1

        result += "\n" + "=" * 70

        return result

    def launch_tool(self, tool_name=None):
        """启动工具"""
        if tool_name is None:
            print("\n[管家] 请选择要启动的工具：")
            print("  1. daily_launcher  - 今日启动器")
            print("  2. file_manager   - 文件管理中心")
            print("  3. market_supervision - 市场监管智能体")
            print("  0. 取消")
            print()

            choice = input("[管家] 请输入编号: ").strip()

            tools = {
                '1': ('daily_launcher', 'python daily_launcher.py'),
                '2': ('file_manager', 'python file_manager_center.py'),
                '3': ('market_supervision', 'python 01_Active_Projects/market_supervision_agent/新版申请书填充工具.py')
            }

            if choice in tools:
                name, cmd = tools[choice]
                print(f"\n[管家] 正在启动 {name}...")
                self.run_command(cmd)
            else:
                print("[管家] 已取消")
        else:
            # 直接启动指定工具
            tool_map = {
                'launcher': 'python daily_launcher.py',
                'file': 'python file_manager_center.py',
                'market': 'python 01_Active_Projects/market_supervision_agent/新版申请书填充工具.py'
            }

            cmd = tool_map.get(tool_name)
            if cmd:
                print(f"\n[管家] 正在启动工具...")
                self.run_command(cmd)
            else:
                print(f"[管家] 未找到工具: {tool_name}")

    def run_command(self, cmd):
        """运行命令"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=self.workspace_root,
                capture_output=False
            )
            print(f"\n[管家] 命令执行完成，返回码: {result.returncode}")
        except Exception as e:
            print(f"[管家] 执行命令时出错: {e}")

    def organize_files(self):
        """整理文件"""
        print("\n[管家] 正在为您整理文件...")
        self.run_command("python file_manager_center.py organize")

    def create_snapshot(self):
        """创建快照"""
        print("\n[管家] 正在创建工作区快照...")
        self.run_command("python file_manager_center.py snapshot")

    def generate_report(self):
        """生成报告"""
        print("\n[管家] 正在生成工作区报告...")
        self.run_command("python 超级管家.py --export")

    def ai_dialogue(self):
        """与AI对话"""
        print("\n" + "=" * 70)
        print("[管家] AI对话模式")
        print("=" * 70)
        print()
        print("  现在您可以与AI助手直接对话了！")
        print("  AI助手可以帮助您：")
        print("    - 分析工作区状态")
        print("    - 提供编程建议")
        print("    - 解答技术问题")
        print("    - 协助开发工作")
        print()
        print("  输入 'back' 返回管家模式")
        print()

        while True:
            user_input = input("\n[AI对话] 请输入您的问题: ").strip()

            if user_input.lower() in ['back', 'return', '退出', '返回']:
                print("[AI对话] 返回管家模式...")
                break

            if not user_input:
                continue

            # 这里可以集成AI对话功能
            print("[AI对话] 我理解您的问题是：")
            print(f"  {user_input}")
            print()
            print("[AI对话] 要使用完整的AI对话功能，请启动Claude Code或其他AI助手。")
            print("[AI对话] 您可以通过以下方式获得帮助：")
            print("  1. 查看工作区文档")
            print("  2. 运行相关工具")
            print("  3. 查看项目README")

    def handle_command(self, user_input):
        """处理用户命令"""
        cmd = user_input.lower().strip()

        # 退出命令
        if cmd in ['quit', 'exit', 'q', '退出', '再见']:
            print("\n[管家] 再见！有任何需要随时找我。")
            return False

        # 帮助命令
        elif cmd in ['help', 'h', '帮助', '?']:
            self.show_help()

        # 状态命令
        elif cmd in ['status', 's', '状态', 'state']:
            print(self.get_workspace_status())

        # 项目命令
        elif cmd in ['projects', 'p', '项目', 'project']:
            print(self.get_projects_list())

        # 工具命令
        elif cmd in ['tools', 't', '工具', 'tool']:
            print(self.get_tools_list())

        # 启动命令
        elif cmd in ['launch', 'l', '启动', 'start', 'run']:
            self.launch_tool()

        # 整理命令
        elif cmd in ['organize', 'o', '整理', 'clean']:
            self.organize_files()

        # 快照命令
        elif cmd in ['snapshot', 'snap', '快照', 'backup']:
            self.create_snapshot()

        # 报告命令
        elif cmd in ['report', 'r', '报告', 'generate']:
            self.generate_report()

        # AI对话命令
        elif cmd in ['ai', 'AI', 'ai对话', 'AI对话']:
            self.ai_dialogue()

        # 菜单命令
        elif cmd in ['menu', 'm', '菜单']:
            self.show_menu()

        # 自然语言处理
        else:
            self.natural_language_process(user_input)

        return True

    def natural_language_process(self, user_input):
        """自然语言处理"""
        input_lower = user_input.lower()

        # 关键词匹配
        if any(word in input_lower for word in ['怎么样', '如何', '状态', '怎样']):
            print(self.get_workspace_status())

        elif any(word in input_lower for word in ['项目', '工程']):
            print(self.get_projects_list())

        elif any(word in input_lower for word in ['工具', '脚本']):
            print(self.get_tools_list())

        elif any(word in input_lower for word in ['整理', '清理', 'clean']):
            print("[管家] 明白了，我来帮您整理文件...")
            self.organize_files()

        elif any(word in input_lower for word in ['快照', '备份', 'snapshot', 'backup']):
            print("[管家] 好的，我来创建快照...")
            self.create_snapshot()

        elif any(word in input_lower for word in ['启动', '打开', 'launch', 'open']):
            print("[管家] 请选择要启动的工具：")
            self.launch_tool()

        elif any(word in input_lower for word in ['报告', 'report']):
            print("[管家] 正在生成报告...")
            self.generate_report()

        else:
            print(f"[管家] 我理解您说的是：{user_input}")
            print("[管家] 抱歉，我还在学习中。您可以：")
            print("  1. 输入 'help' 查看我能做的事")
            print("  2. 输入 'ai' 与AI对话获取更详细的帮助")
            print("  3. 使用简洁的命令，如 'status'、'projects'")

    def show_help(self):
        """显示帮助"""
        print("\n" + "=" * 70)
        print("[管家] 帮助信息")
        print("=" * 70)
        print()
        print("命令方式：")
        print("  status    - 查看工作区状态")
        print("  projects  - 查看项目列表")
        print("  tools     - 查看可用工具")
        print("  launch    - 启动工具")
        print("  organize  - 整理文件")
        print("  snapshot  - 创建快照")
        print("  report    - 生成报告")
        print("  ai        - 与AI对话")
        print()
        print("自然语言方式：")
        print("  '工作区怎么样了？'  - 查看状态")
        print("  '有哪些项目？'      - 查看项目")
        print("  '帮我整理文件'      - 整理文件")
        print("  '创建快照'          - 创建快照")
        print()
        print("其他：")
        print("  help      - 显示帮助")
        print("  menu      - 显示菜单")
        print("  quit      - 退出")
        print()

    def run(self):
        """运行管家"""
        self.introduce()

        while True:
            try:
                user_input = input("\n[管家] 请告诉我您需要什么帮助: ").strip()

                if not user_input:
                    continue

                keep_running = self.handle_command(user_input)

                if not keep_running:
                    break

            except KeyboardInterrupt:
                print("\n\n[管家] 检测到中断信号...")
                choice = input("[管家] 确定要退出吗？(y/n): ").strip().lower()
                if choice in ['y', 'yes', '是']:
                    print("\n[管家] 再见！")
                    break
                else:
                    print("[管家] 继续为您服务...")

            except Exception as e:
                print(f"\n[管家] 发生错误: {e}")
                print("[管家] 请稍后重试或联系开发者")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='超级管家智能体 - 工作区总管')
    parser.add_argument('--workspace', '-w', help='工作区路径')
    parser.add_argument('--version', '-v', action='version', version='超级管家 v2.0')

    args = parser.parse_args()

    # 创建并运行管家
    butler = SuperButlerAgent(workspace_root=args.workspace)
    butler.run()


if __name__ == '__main__':
    main()
