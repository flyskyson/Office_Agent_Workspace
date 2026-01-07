"""
argparse 基础示例 3：必需的可选参数
"""

import argparse

parser = argparse.ArgumentParser(description='必需参数示例')

# 使用 required=True 让可选参数变成必需的
parser.add_argument(
    '-i', '--input',
    type=str,
    required=True,  # 这个参数必须提供
    help='输入文件路径'
)

parser.add_argument(
    '-o', '--output',
    type=str,
    default='output.txt',  # 可选，有默认值
    help='输出文件路径'
)

args = parser.parse_args()

print(f"输入文件：{args.input}")
print(f"输出文件：{args.output}")

# ========================================
# 使用方法：
# 1. 正确使用（提供必需参数）
# python argparse_demo3.py -i "data.txt"
# 输出：
# 输入文件：data.txt
# 输出文件：output.txt（使用默认值）
#
# 2. 同时提供两个参数
# python argparse_demo3.py -i "data.txt" -o "result.txt"
# 输出：
# 输入文件：data.txt
# 输出文件：result.txt
#
# 3. 缺少必需参数（会报错）
# python argparse_demo3.py -o "result.txt"
# 错误：error: the following arguments are required: -i/--input
# ========================================
