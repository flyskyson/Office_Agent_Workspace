"""
argparse 基础示例 1：最简单的参数解析
"""

import argparse

# 1. 创建解析器对象
parser = argparse.ArgumentParser(
    description='这是程序的描述信息'
)

# 2. 添加参数
# 这是一个位置参数（必需，不需要 - 前缀）
parser.add_argument('name', help='你的名字')

# 3. 解析参数
args = parser.parse_args()

# 4. 使用参数
print(f"你好，{args.name}!")

# ========================================
# 使用方法：
# python argparse_demo1.py 小明
# 输出：你好，小明!
#
# 如果不加参数运行：
# python argparse_demo1.py
# 会报错并显示帮助信息
# ========================================
