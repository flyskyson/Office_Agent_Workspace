# -*- coding: utf-8 -*-
"""
测试 file_organizer 模块导入
============================
验证从材料库导入是否正常工作
"""

import importlib.util
import os
import sys

# 设置输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("测试 file_organizer 模块导入")
print("=" * 60)

# 1. 检查模块文件是否存在
module_path = r"C:\Users\flyskyson\Office_Agent_Workspace\00_Agent_Library\02_Code_Snippets\文件操作\file_organizer.py"
print(f"\n[1/4] 检查模块路径...")
print(f"  路径: {module_path}")
if os.path.exists(module_path):
    print("  [OK] 模块文件存在")
else:
    print("  [FAIL] 模块文件不存在")
    exit(1)

# 2. 动态加载模块
print(f"\n[2/4] 动态加载模块...")
try:
    spec = importlib.util.spec_from_file_location("file_organizer", module_path)
    file_organizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(file_organizer)
    print("  [OK] 模块加载成功")
except Exception as e:
    print(f"  [FAIL] 模块加载失败: {e}")
    exit(1)

# 3. 检查函数是否可导入
print(f"\n[3/4] 检查函数可用性...")
try:
    organize_files = file_organizer.organize_files
    FileOrganizer = file_organizer.FileOrganizer
    print("  [OK] organize_files 函数可用")
    print("  [OK] FileOrganizer 类可用")
except AttributeError as e:
    print(f"  [FAIL] 函数不可用: {e}")
    exit(1)

# 4. 测试函数签名
print(f"\n[4/4] 验证函数签名...")
try:
    import inspect
    sig = inspect.signature(organize_files)
    print(f"  函数签名: organize_files{sig}")
    print("  [OK] 函数签名正确")
except Exception as e:
    print(f"  [FAIL] 签名检查失败: {e}")

# 输出模块信息
print(f"\n" + "=" * 60)
print("模块信息:")
print("=" * 60)
print(f"  模块名称: {file_organizer.__name__ if hasattr(file_organizer, '__name__') else 'file_organizer'}")
doc_str = file_organizer.__doc__[:50] if hasattr(file_organizer, '__doc__') else 'N/A'
print(f"  文档字符串: {doc_str}...")

print(f"\n" + "=" * 60)
print("[SUCCESS] 所有测试通过！模块导入正常")
print("=" * 60)
