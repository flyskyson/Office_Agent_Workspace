"""
argparse 基础示例 4：限制参数值（choices）
"""

import argparse

parser = argparse.ArgumentParser(description='限制参数值示例')

# choices 参数限制用户只能选择指定的值
parser.add_argument(
    '-f', '--format',
    choices=['markdown', 'json', 'txt'],  # 只能选择这三个之一
    default='markdown',
    help='输出格式'
)

parser.add_argument(
    '-c', '--color',
    choices=['red', 'green', 'blue'],  # 只能选择这三个颜色
    help='喜欢的颜色'
)

args = parser.parse_args()

print(f"格式：{args.format}")
if args.color:
    print(f"颜色：{args.color}")

# ========================================
# 使用方法：
# 1. 使用默认值
# python argparse_demo4.py
# 输出：格式：markdown
#
# 2. 选择有效的值
# python argparse_demo4.py -f json -c red
# 输出：
# 格式：json
# 颜色：red
#
# 3. 选择无效的值（会报错）
# python argparse_demo4.py -f pdf
# 错误：error: argument -f/--format: invalid choice: 'pdf' (choose from 'markdown', 'json', 'txt')
# ========================================
