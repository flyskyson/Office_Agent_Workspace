#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新管家快捷方式为增强版"""

import os
import sys
from pathlib import Path

# 设置控制台编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def update_shortcut():
    """更新快捷方式"""
    try:
        import win32com.client

        workspace_root = Path(__file__).parent
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        # 使用简单版
        target = str(workspace_root / '00_Agent_Library' / '99_Scripts_Tools' / '启动管家_简单版.bat')
        shortcut_path = os.path.join(desktop, 'Workspace Butler.lnk')

        # 删除旧快捷方式
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)

        # 创建新快捷方式
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)

        shortcut.Targetpath = target
        shortcut.WorkingDirectory = str(workspace_root)
        shortcut.Description = 'Workspace Butler - Enhanced Daily Start'
        shortcut.save()

        print("✅ 快捷方式已更新为简单版!")
        print(f"位置: {shortcut_path}")
        print()
        print("功能:")
        print("  - 话术自动复制到剪贴板")
        print("  - 自动打开VS Code")
        print("  - 简洁清晰的显示")

        return True

    except Exception as e:
        print(f"❌ 更新失败: {e}")
        return False

if __name__ == '__main__':
    print("=" * 70)
    print("更新工作区管家快捷方式")
    print("=" * 70)
    print()

    success = update_shortcut()

    print()
    if success:
        input("按回车键退出...")
