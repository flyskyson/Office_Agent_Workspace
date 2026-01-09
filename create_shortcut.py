#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建工作区管家桌面快捷方式
"""

import os
import sys
from pathlib import Path

# 设置控制台编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_shortcut():
    """创建桌面快捷方式"""
    try:
        import win32com.client

        workspace_root = Path(__file__).parent
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        target = str(workspace_root / '00_Agent_Library' / '99_Scripts_Tools' / '启动管家模式.bat')
        shortcut_path = os.path.join(desktop, 'Workspace Butler.lnk')

        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)

        shortcut.Targetpath = target
        shortcut.WorkingDirectory = str(workspace_root)
        shortcut.Description = 'Workspace Butler - Daily Start'
        shortcut.save()

        print("✅ 成功创建桌面快捷方式!")
        print(f"位置: {shortcut_path}")
        print()
        print("现在可以在桌面上看到 'Workspace Butler.lnk' 图标")
        print("双击即可启动工作区管家")

        return True

    except ImportError:
        print("❌ 需要安装 pywin32 库")
        print()
        print("请运行:")
        print("  pip install pywin32")
        print()
        print("或者直接双击运行:")
        print("  00_Agent_Library\\99_Scripts_Tools\\创建管家快捷方式.bat")
        return False

    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False

if __name__ == '__main__':
    print("=" * 70)
    print("创建工作区管家桌面快捷方式")
    print("=" * 70)
    print()

    success = create_shortcut()

    print()
    if success:
        input("按回车键退出...")
