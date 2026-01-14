#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Office Agent Studio - 统一启动器 v2.0
集成所有办公自动化工具，提供统一的访问入口
"""

import sys
import os
from pathlib import Path
import subprocess
import webbrowser
from datetime import datetime

# 添加工作区根目录到路径
WORKSPACE_ROOT = Path(__file__).parent
sys.path.insert(0, str(WORKSPACE_ROOT))

# ANSI 颜色代码
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(title):
    """打印标题"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{title:^70}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 70}{Colors.END}\n")


def print_menu_item(number, icon, name, description, status=""):
    """打印菜单项"""
    status_text = f" {Colors.GREEN}✓{Colors.END}" if status == "✓" else f" {Colors.YELLOW}○{Colors.END}"
    print(f"  {Colors.BOLD}[{number}]{Colors.END} {icon} {Colors.BOLD}{name}{Colors.END}{status_text}")
    print(f"      {description}\n")


def print_separator():
    """打印分隔线"""
    print(f"{Colors.CYAN}{'─' * 70}{Colors.END}\n")


class ToolLauncher:
    """工具启动器"""

    def __init__(self):
        """初始化启动器"""
        self.tools = {
            '1': {
                'name': '市场监管智能体',
                'icon': '🏢',
                'description': '营业执照OCR识别 + 申请书自动生成',
                'path': WORKSPACE_ROOT / '01_Active_Projects' / 'market_supervision_agent' / 'ui' / 'flask_app.py',
                'url': 'http://127.0.0.1:5000',
                'type': 'flask',
                'status': '✓'
            },
            '2': {
                'name': '学习记忆助手',
                'icon': '🧠',
                'description': '智能知识管理 + 语义搜索 + 间隔复习',
                'path': WORKSPACE_ROOT / '01_Active_Projects' / 'memory_agent' / 'ui' / 'app.py',
                'url': 'http://127.0.0.1:5555',
                'type': 'flask',
                'status': '✓'
            },
            '3': {
                'name': '证照整理工具',
                'icon': '📁',
                'description': '智能识别并整理证照材料',
                'path': WORKSPACE_ROOT / '01_Active_Projects' / 'file_organizer' / 'file_organizer.py',
                'type': 'cli',
                'status': '○'
            },
            '4': {
                'name': '广西政务自动登录',
                'icon': '🔐',
                'description': '自动登录广西政务服务平台',
                'path': WORKSPACE_ROOT / '00_Agent_Library' / '99_Scripts_Tools' / '广西政务自动登录.py',
                'type': 'playwright',
                'status': '✓'
            },
            '5': {
                'name': '工作区扫描器',
                'icon': '🔍',
                'description': '扫描并索引整个工作区',
                'path': WORKSPACE_ROOT / 'workspace_scanner.py',
                'type': 'cli',
                'status': '○'
            },
            '6': {
                'name': '工作区清理工具',
                'icon': '🧹',
                'description': '清理缓存和临时文件',
                'path': WORKSPACE_ROOT / 'workspace_cleaner.py',
                'type': 'cli',
                'status': '○'
            },
            '7': {
                'name': '工作区健康报告',
                'icon': '📊',
                'description': '生成工作区健康状态报告',
                'path': WORKSPACE_ROOT / 'workspace_report.py',
                'type': 'cli',
                'status': '○'
            }
        }

    def show_menu(self):
        """显示主菜单"""
        os.system('cls' if os.name == 'nt' else 'clear')

        print_header("🚀 Office Agent Studio v2.0")

        print(f"{Colors.BOLD}{Colors.UNDERLINE}核心智能体{Colors.END}\n")

        print_menu_item('1', '🏢', '市场监管智能体',
                       '营业执照OCR识别 + 申请书自动生成',
                       self.tools['1']['status'])
        print_menu_item('2', '🧠', '学习记忆助手',
                       '智能知识管理 + 语义搜索 + 间隔复习',
                       self.tools['2']['status'])

        print_separator()

        print(f"{Colors.BOLD}{Colors.UNDERLINE}实用工具{Colors.END}\n")

        print_menu_item('3', '📁', '证照整理工具',
                       '智能识别并整理证照材料',
                       self.tools['3']['status'])
        print_menu_item('4', '🔐', '广西政务自动登录',
                       '自动登录广西政务服务平台',
                       self.tools['4']['status'])

        print_separator()

        print(f"{Colors.BOLD}{Colors.UNDERLINE}工作区管理{Colors.END}\n")

        print_menu_item('5', '🔍', '工作区扫描器',
                       '扫描并索引整个工作区',
                       self.tools['5']['status'])
        print_menu_item('6', '🧹', '工作区清理工具',
                       '清理缓存和临时文件',
                       self.tools['6']['status'])
        print_menu_item('7', '📊', '工作区健康报告',
                       '生成工作区健康状态报告',
                       self.tools['7']['status'])

        print_separator()

        print(f"  {Colors.BOLD}[0]{Colors.END} 🚪 退出")
        print(f"  {Colors.BOLD}[H]{Colors.END} ℹ️  查看帮助")
        print(f"  {Colors.BOLD}[I]{Colors.END} 📋 查看项目信息\n")

        print(f"{Colors.CYAN}{'=' * 70}{Colors.END}\n")

    def launch_flask_app(self, tool_key):
        """启动 Flask 应用"""
        tool = self.tools[tool_key]
        path = tool['path']
        url = tool['url']

        print(f"{Colors.YELLOW}正在启动 {tool['name']}...{Colors.END}\n")

        if not path.exists():
            print(f"{Colors.RED}错误: 找不到文件 {path}{Colors.END}")
            input(f"\n{Colors.CYAN}按回车返回...{Colors.END}")
            return

        print(f"{Colors.GREEN}✓{Colors.END} 服务启动成功!")
        print(f"{Colors.CYAN}  访问地址: {url}{Colors.END}")
        print(f"{Colors.YELLOW}  提示: 按 Ctrl+C 停止服务{Colors.END}\n")

        # 打开浏览器
        try:
            webbrowser.open(url)
        except:
            pass

        # 启动服务
        try:
            subprocess.run([sys.executable, str(path)], check=True)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}服务已停止{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}启动失败: {e}{Colors.END}")

        input(f"\n{Colors.CYAN}按回车返回...{Colors.END}")

    def launch_cli_tool(self, tool_key):
        """启动命令行工具"""
        tool = self.tools[tool_key]
        path = tool['path']

        print(f"{Colors.YELLOW}正在启动 {tool['name']}...{Colors.END}\n")

        if not path.exists():
            print(f"{Colors.RED}错误: 找不到文件 {path}{Colors.END}")
            input(f"\n{Colors.CYAN}按回车返回...{Colors.END}")
            return

        try:
            subprocess.run([sys.executable, str(path)], check=True)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}已中断{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}运行失败: {e}{Colors.END}")

        input(f"\n{Colors.CYAN}按回车返回...{Colors.END}")

    def show_help(self):
        """显示帮助信息"""
        print_header("📚 帮助信息")

        help_text = f"""
{Colors.BOLD}核心智能体:{Colors.END}

  {Colors.GREEN}1. 市场监管智能体{Colors.END}
     - 功能: 上传营业执照图片，自动OCR识别并生成申请书
     - 输入: 营业执照、身份证照片（支持 JPG、PNG、PDF）
     - 输出: Word 格式申请书
     - 技术栈: Flask + 百度 OCR + Python-docx

  {Colors.GREEN}2. 学习记忆助手{Colors.END}
     - 功能: 语义搜索代码和笔记，智能复习提醒
     - 特点: 向量数据库 + 间隔重复算法
     - 用途: 快速找到之前的代码和解决方案
     - 技术栈: Flask + ChromaDB + Sentence Transformers

{Colors.BOLD}实用工具:{Colors.END}

  {Colors.YELLOW}3. 证照整理工具{Colors.END}
     - 自动识别证照类型并分类整理
     - 支持批量处理

  {Colors.YELLOW}4. 广西政务自动登录{Colors.END}
     - 自动填写账号密码
     - 需要手动完成滑块验证

{Colors.BOLD}工作区管理:{Colors.END}

  {Colors.CYAN}5. 工作区扫描器{Colors.END}
     - 扫描所有项目并建立索引
     - 生成工作区记忆文件

  {Colors.CYAN}6. 工作区清理工具{Colors.END}
     - 清理 Python 缓存 (__pycache__)
     - 删除临时文件

  {Colors.CYAN}7. 工作区健康报告{Colors.END}
     - 分析项目状态
     - 统计代码行数
     - 检查大文件
"""
        print(help_text)
        input(f"\n{Colors.CYAN}按回车返回...{Colors.END}")

    def show_info(self):
        """显示项目信息"""
        print_header("📋 项目信息")

        # 统计信息
        active_projects = len(list((WORKSPACE_ROOT / '01_Active_Projects').glob('*')))
        archived_projects = len(list((WORKSPACE_ROOT / '02_Project_Archive').glob('*'))) if (WORKSPACE_ROOT / '02_Project_Archive').exists() else 0

        info = f"""
{Colors.BOLD}工作区信息{Colors.END}

  路径: {WORKSPACE_ROOT}
  活跃项目: {active_projects} 个
  归档项目: {archived_projects} 个
  Python 版本: {sys.version.split()[0]}

{Colors.BOLD}最近更新{Colors.END}

  v2.0 (2026-01-13)
  - 新增: 学习记忆助手 Web UI
  - 新增: 统一启动器
  - 优化: 市场监管智能体 v4.0

{Colors.BOLD}技术栈{Colors.END}

  - Python 3.12
  - Flask (Web UI)
  - ChromaDB (向量数据库)
  - 百度 OCR (文字识别)
  - Playwright (浏览器自动化)
  - Sentence Transformers (语义搜索)

{Colors.BOLD}快捷方式{Colors.END}

  - 双击 {Colors.CYAN}启动_OA_Studio.bat{Colors.END} 快速启动
  - 添加桌面快捷方式方便访问
"""
        print(info)
        input(f"\n{Colors.CYAN}按回车返回...{Colors.END}")

    def run(self):
        """运行主循环"""
        while True:
            self.show_menu()

            try:
                choice = input(f"{Colors.BOLD}请选择操作 (0-7, H, I):{Colors.END} ").strip().upper()

                if choice == '0':
                    print(f"\n{Colors.GREEN}再见！祝工作愉快！👋{Colors.END}\n")
                    break

                elif choice == '1':
                    self.launch_flask_app('1')
                elif choice == '2':
                    self.launch_flask_app('2')
                elif choice == '3':
                    self.launch_cli_tool('3')
                elif choice == '4':
                    self.launch_cli_tool('4')
                elif choice == '5':
                    self.launch_cli_tool('5')
                elif choice == '6':
                    self.launch_cli_tool('6')
                elif choice == '7':
                    self.launch_cli_tool('7')

                elif choice == 'H':
                    self.show_help()
                elif choice == 'I':
                    self.show_info()

                else:
                    print(f"{Colors.RED}无效选项，请重试{Colors.END}")
                    input(f"\n{Colors.CYAN}按回车继续...{Colors.END}")

            except KeyboardInterrupt:
                print(f"\n\n{Colors.GREEN}再见！👋{Colors.END}\n")
                break
            except Exception as e:
                print(f"\n{Colors.RED}错误: {e}{Colors.END}")
                input(f"\n{Colors.CYAN}按回车继续...{Colors.END}")


def main():
    """主函数"""
    launcher = ToolLauncher()
    launcher.run()


if __name__ == '__main__':
    main()
