#!/usr/bin/env python3
"""
创建桌面快捷方式
"""

import os
import sys
from pathlib import Path

def create_batch_files():
    """创建批处理文件"""

    workspace = Path("C:/Users/flyskyson/Office_Agent_Workspace")

    # 1. 今日启动器
    launcher_content = """@echo off
chcp 65001 > nul
cd /d C:\\Users\\flyskyson\\Office_Agent_Workspace
python daily_launcher.py
pause
"""

    launcher_file = workspace / "启动今日启动器.bat"
    with open(launcher_file, 'w', encoding='gbk') as f:
        f.write(launcher_content)
    print(f"✓ 创建: {launcher_file.name}")

    # 2. 文件管理中心
    file_manager_content = """@echo off
chcp 65001 > nul
cd /d C:\\Users\\flyskyson\\Office_Agent_Workspace
python file_manager_center.py
pause
"""

    file_manager_file = workspace / "启动文件管理中心.bat"
    with open(file_manager_file, 'w', encoding='gbk') as f:
        f.write(file_manager_content)
    print(f"✓ 创建: {file_manager_file.name}")

    # 3. 市场监管智能体
    market_agent_content = """@echo off
chcp 65001 > nul
cd /d C:\\Users\\flyskyson\\Office_Agent_Workspace\\01_Active_Projects\\market_supervision_agent
python 新版申请书填充工具.py
pause
"""

    market_agent_file = workspace / "启动市场监管智能体.bat"
    with open(market_agent_file, 'w', encoding='gbk') as f:
        f.write(market_agent_content)
    print(f"✓ 创建: {market_agent_file.name}")

    return launcher_file, file_manager_file, market_agent_file

def create_shortcuts():
    """创建桌面快捷方式"""

    try:
        from win32com.client import Dispatch

        desktop = Path(os.path.expanduser("~/Desktop"))
        workspace = Path("C:/Users/flyskyson/Office_Agent_Workspace")

        print("\n创建桌面快捷方式...")
        print("=" * 50)

        # 创建批处理文件
        launcher, file_manager, market_agent = create_batch_files()

        # 创建快捷方式函数
        def create_shortcut(target_path, shortcut_name, description):
            shortcut_path = desktop / f"{shortcut_name}.lnk"
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(target_path)
            shortcut.WorkingDirectory = str(workspace)
            shortcut.Description = description
            shortcut.save()
            print(f"✓ 桌面快捷方式: {shortcut_name}.lnk")

        # 创建快捷方式
        create_shortcut(launcher, "今日启动器", "每天开始工作的第一站")
        create_shortcut(file_manager, "文件管理中心", "统一管理所有文件")
        create_shortcut(market_agent, "市场监管智能体", "个体工商户证照办理自动化")
        create_shortcut(workspace, "工作区文件夹", "访问工作区所有文件")
        create_shortcut(workspace / "三大工具快速指南.md", "工具使用指南", "工作区工具使用说明")

        print("\n" + "=" * 50)
        print("✓ 所有快捷方式创建完成！")
        print(f"\n桌面快捷方式已创建:")
        print("  1. 今日启动器.lnk")
        print("  2. 文件管理中心.lnk")
        print("  3. 市场监管智能体.lnk")
        print("  4. 工作区文件夹.lnk")
        print("  5. 工具使用指南.lnk")
        print(f"\n位置: {desktop}")

        return True

    except ImportError:
        print("\n需要 pywin32 库")
        print("安装命令: pip install pywin32")
        return False
    except Exception as e:
        print(f"\n创建快捷方式失败: {e}")
        return False

def create_desktop_guide():
    """创建桌面指南文件"""

    workspace = Path("C:/Users/flyskyson/Office_Agent_Workspace")
    desktop = Path(os.path.expanduser("~/Desktop"))

    # 复制指南到桌面
    import shutil
    guide_src = workspace / "三大工具快速指南.md"
    guide_dst = desktop / "工作区工具使用指南.md"

    if guide_src.exists():
        shutil.copy(guide_src, guide_dst)
        print(f"✓ 桌面指南: {guide_dst.name}")

def main():
    """主函数"""

    print("=" * 60)
    print("  创建桌面快捷方式和指南")
    print("=" * 60)

    # 创建批处理文件
    print("\n步骤1: 创建批处理启动文件")
    create_batch_files()

    # 创建桌面快捷方式
    print("\n步骤2: 创建桌面快捷方式")
    success = create_shortcuts()

    # 创建桌面指南
    print("\n步骤3: 复制使用指南到桌面")
    try:
        create_desktop_guide()
    except Exception as e:
        print(f"  跳过: {e}")

    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

    if success:
        print("\n使用说明:")
        print("1. 桌面上现在有5个快捷方式")
        print("2. 双击即可使用对应功能")
        print("3. 查看'工具使用指南'了解详细用法")
    else:
        print("\n批处理文件已创建在:")
        print("  C:\\Users\\flyskyson\\Office_Agent_Workspace")
        print("\n可以手动双击这些.bat文件使用:")
        print("  - 启动今日启动器.bat")
        print("  - 启动文件管理中心.bat")
        print("  - 启动市场监管智能体.bat")

    print("\n按回车键退出...")
    input()

if __name__ == "__main__":
    main()