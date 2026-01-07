"""
argparse 基础示例 2：可选参数
"""

import argparse

# 创建解析器
parser = argparse.ArgumentParser(description='可选参数示例')

# 添加可选参数
# --age 是长选项，-a 是短选项
# type=int 指定参数类型为整数
# default=18 设置默认值
parser.add_argument('-a', '--age', type=int, default=18, help='你的年龄')

# 解析参数
args = parser.parse_args()

# 使用参数
print(f"年龄：{args.age}")

# ========================================
# 使用方法：
# 1. 使用默认值
# python argparse_demo2.py
# 输出：年龄：18
#
# 2. 使用短选项
# python argparse_demo2.py -a 25
# 输出：年龄：25
#
# 3. 使用长选项
# python argparse_demo2.py --age 30
# 输出：年龄：30
# ========================================
