"""
argparse 基础示例 5：布尔值参数（开关）
"""

import argparse

parser = argparse.ArgumentParser(description='布尔开关参数示例')

# action='store_true'：如果提供这个参数，值为 True，否则为 False
parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    help='显示详细信息'
)

# action='store_false'：如果提供这个参数，值为 False，否则为 True
parser.add_argument(
    '-q', '--quiet',
    action='store_false',
    dest='verbose',  # 存储到 args.verbose
    help='静默模式'
)

parser.add_argument(
    '--debug',
    action='store_true',
    help='启用调试模式'
)

args = parser.parse_args()

print(f"详细模式：{args.verbose}")
print(f"调试模式：{args.debug}")

if args.verbose:
    print("✅ 已启用详细输出模式")
else:
    print("普通模式")

if args.debug:
    print("🐛 调试模式已开启")

# ========================================
# 使用方法：
# 1. 不加任何开关
# python argparse_demo5.py
# 输出：
# 详细模式：False
# 调试模式：False
# 普通模式
#
# 2. 启用详细模式
# python argparse_demo5.py -v
# 输出：
# 详细模式：True
# 调试模式：False
# ✅ 已启用详细输出模式
#
# 3. 同时启用多个开关
# python argparse_demo5.py -v --debug
# 输出：
# 详细模式：True
# 调试模式：True
# ✅ 已启用详细输出模式
# 🐛 调试模式已开启
#
# 4. 使用冲突的开关（后面的会覆盖前面的）
# python argparse_demo5.py -v -q
# 输出：
# 详细模式：False
# 调试模式：False
# 普通模式
# ========================================
