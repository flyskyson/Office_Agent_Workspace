"""
argparse 基础示例 6：多个值的参数
"""

import argparse

parser = argparse.ArgumentParser(description='多个值参数示例')

# nargs='+' 表示至少提供一个值，可以有多个
# nargs='*' 表示可以提供 0 个或多个值
# nargs=3 表示必须提供恰好 3 个值

# 示例 1：接受多个文件名
parser.add_argument(
    'files',
    nargs='+',  # 至少一个文件
    help='要处理的文件列表'
)

# 示例 2：接受多个数字
parser.add_argument(
    '--numbers',
    nargs='*',  # 可以 0 个或多个
    type=int,
    help='数字列表'
)

# 示例 3：恰好接受 3 个值
parser.add_argument(
    '--coord',
    nargs=3,  # 必须恰好 3 个值
    type=float,
    metavar=('X', 'Y', 'Z'),  # 在帮助信息中显示的占位符
    help='坐标 (X Y Z)'
)

args = parser.parse_args()

print("=" * 50)
print(f"文件列表：{args.files}")
print(f"文件数量：{len(args.files)}")

if args.numbers:
    print(f"数字列表：{args.numbers}")
    print(f"数字总和：{sum(args.numbers)}")
else:
    print("未提供数字")

if args.coord:
    x, y, z = args.coord
    print(f"坐标：X={x}, Y={y}, Z={z}")

print("=" * 50)

# ========================================
# 使用方法：
# 1. 提供多个文件
# python argparse_demo6.py file1.txt file2.txt file3.txt
# 输出：
# ==================================================
# 文件列表：['file1.txt', 'file2.txt', 'file3.txt']
# 文件数量：3
# 未提供数字
# ==================================================
#
# 2. 提供文件和数字
# python argparse_demo6.py a.txt b.txt --numbers 1 2 3 4 5
# 输出：
# ==================================================
# 文件列表：['a.txt', 'b.txt']
# 文件数量：2
# 数字列表：[1, 2, 3, 4, 5]
# 数字总和：15
# ==================================================
#
# 3. 提供坐标
# python argparse_demo6.py file.txt --coord 1.5 2.3 3.7
# 输出：
# ==================================================
# 文件列表：['file.txt']
# 文件数量：1
# 未提供数字
# 坐标：X=1.5, Y=2.3, Z=3.7
# ==================================================
# ========================================
