"""
====================================
  argparse 速查表
====================================

目录：
1. 基本结构
2. 常用参数
3. 参数类型
4. 特殊参数
5. 完整示例
====================================
"""

# =====================================
# 1. 基本结构
# =====================================

import argparse

# 第一步：创建解析器
parser = argparse.ArgumentParser(
    description='程序描述信息',      # 程序的说明
    epilog='额外信息'               # 帮助信息末尾的内容
)

# 第二步：添加参数
parser.add_argument('参数名', help='参数说明')

# 第三步：解析参数
args = parser.parse_args()

# 第四步：使用参数
print(args.参数名)


# =====================================
# 2. 常用参数
# =====================================

parser.add_argument(
    'name',              # 参数名（位置参数不需要 - 前缀）
    type=str,            # 参数类型：str, int, float, bool 等
    default='默认值',     # 默认值（可选参数才有默认值）
    required=True,       # 是否必需（仅可选参数可用）
    help='参数说明',      # 帮助信息中显示的文本
    metavar='占位符',     # 在帮助信息中显示的参数名称占位符
    choices=['A', 'B'],   # 限制参数值的范围
    nargs=1              # 参数的数量（见下文详细说明）
)

# =====================================
# 3. 参数类型
# =====================================

# 【位置参数】必需，按顺序提供
parser.add_argument('filename', help='文件名')
# 使用：python script.py data.txt

# 【可选参数】可选，使用 - 或 -- 前缀
parser.add_argument('-f', '--format', help='格式')
# 使用：python script.py -f json 或 python script.py --format json

# 【必需的可选参数】加上 required=True
parser.add_argument('-i', '--input', required=True, help='输入文件')
# 使用：python script.py -i data.txt（必须提供）

# =====================================
# 4. 特殊参数
# =====================================

# 【布尔开关】action='store_true'
parser.add_argument('-v', '--verbose', action='store_true', help='详细模式')
# 使用：python script.py -v（有参数时为 True，否则为 False）

# 【布尔开关】action='store_false'
parser.add_argument('-q', '--quiet', action='store_false', help='静默模式')
# 使用：python script.py -q（有参数时为 False，否则为 True）

# 【多个值】nargs='+' 或 nargs='*'
parser.add_argument('files', nargs='+', help='文件列表')
# nargs='+'  至少一个值
# nargs='*'  零个或多个值
# nargs=3    恰好 3 个值
# 使用：python script.py file1.txt file2.txt file3.txt

# 【互斥参数】只能选择其中一个
group = parser.add_mutually_exclusive_group()
group.add_argument('--fast', action='store_true', help='快速模式')
group.add_argument('--slow', action='store_true', help='慢速模式')
# 使用：python script.py --fast 或 python script.py --slow（不能同时使用）

# =====================================
# 5. add_argument 完整参数列表
# =====================================

"""
parser.add_argument(
    name or flags...      # 参数名或选项（如 'foo' 或 '-f', '--foo'）
    action='store',       # 动作：store, store_true, store_false 等
    nargs=None,           # 参数数量：整数, '?', '*', '+'
    const=None,           # 常量值（配合某些 action 使用）
    default=None,         # 默认值
    type=None,            # 类型转换函数
    choices=None,         # 限制值的选择范围
    required=False,       # 是否必需
    help=None,            # 帮助信息
    metavar=None,         # 帮助信息中的占位符
    dest=None,            # 存储到 args 的属性名
)
"""

# =====================================
# 6. 实用示例
# =====================================

# 【示例 1】简单参数
parser.add_argument('-o', '--output', help='输出文件')
# 使用：python script.py -o result.txt

# 【示例 2】限制选择
parser.add_argument('-f', '--format', choices=['json', 'csv'], help='格式')
# 使用：python script.py -f json（只能是 json 或 csv）

# 【示例 3】指定类型
parser.add_argument('-n', '--number', type=int, help='数字')
# 使用：python script.py -n 42（自动转换为整数）

# 【示例 4】带默认值
parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
# 使用：python script.py -v（启用）或 python script.py（不启用，为 False）

# 【示例 5】多个文件
parser.add_argument('files', nargs='+', help='文件列表')
# 使用：python script.py file1.txt file2.txt file3.txt

# 【示例 6】坐标（恰好 3 个值）
parser.add_argument('--coord', nargs=3, type=float, help='坐标 X Y Z')
# 使用：python script.py --coord 1.5 2.3 3.7

# =====================================
# 7. 常用 action 值
# =====================================

"""
action='store'          # 保存参数值（默认）
action='store_true'     # 存储为 True（不需要值）
action='store_false'    # 存储为 False（不需要值）
action='append'         # 追加到列表（可多次使用）
action='append_const'   # 追加常量到列表
action='count'          # 统计参数出现的次数
action='help'           # 显示帮助信息
action='version'        # 显示版本信息
"""

# 【append 示例】
parser.add_argument('-t', '--tag', action='append', help='标签')
# 使用：python script.py -t python -t cli -t demo
# 结果：args.tags = ['python', 'cli', 'demo']

# 【count 示例】
parser.add_argument('-v', '--verbose', action='count', help='详细程度')
# 使用：python script.py -v     -> args.verbose = 1
#       python script.py -vv    -> args.verbose = 2
#       python script.py -vvv   -> args.verbose = 3

# =====================================
# 8. 高级功能
# =====================================

# 【参数组】将相关参数分组
parser = argparse.ArgumentParser()

# 必需参数组
required_group = parser.add_argument_group('必需参数')
required_group.add_argument('-i', '--input', required=True, help='输入文件')

# 可选参数组
optional_group = parser.add_argument_group('可选参数')
optional_group.add_argument('-o', '--output', help='输出文件')
optional_group.add_argument('-v', '--verbose', action='store_true')

# 【互斥参数组】只能选择其中一个
mutex_group = parser.add_mutually_exclusive_group()
mutex_group.add_argument('--fast', action='store_true', help='快速模式')
mutex_group.add_argument('--slow', action='store_true', help='慢速模式')

# 【子命令】类似 git 的命令（git add, git commit）
subparsers = parser.add_subparsers(dest='command', help='可用命令')

# add 子命令
parser_add = subparsers.add_parser('add', help='添加文件')
parser_add.add_argument('filename', help='文件名')

# commit 子命令
parser_commit = subparsers.add_parser('commit', help='提交更改')
parser_commit.add_argument('-m', '--message', required=True, help='提交信息')

# 使用：
# python script.py add file.txt
# python script.py commit -m "Initial commit"

# =====================================
# 9. 常见模式
# =====================================

# 【模式 1】简单的文件处理工具
parser = argparse.ArgumentParser(description='文件处理工具')
parser.add_argument('input', help='输入文件')
parser.add_argument('-o', '--output', help='输出文件（可选）')
parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json')
parser.add_argument('-v', '--verbose', action='store_true')

# 【模式 2】配置工具
parser = argparse.ArgumentParser(description='配置工具')
parser.add_argument('-c', '--config', help='配置文件路径')
parser.add_argument('-p', '--port', type=int, default=8080, help='端口号')
parser.add_argument('-d', '--debug', action='store_true', help='调试模式')

# 【模式 3】批量处理工具
parser = argparse.ArgumentParser(description='批量处理工具')
parser.add_argument('files', nargs='+', help='要处理的文件列表')
parser.add_argument('-o', '--output-dir', help='输出目录')
parser.add_argument('--dry-run', action='store_true', help='模拟运行')

# 【模式 4】带子命令的工具
parser = argparse.ArgumentParser(description='多功能工具')
subparsers = parser.add_subparsers(dest='command', help='子命令')

# 不同的子命令
parser_download = subparsers.add_parser('download', help='下载文件')
parser_download.add_argument('url', help='下载地址')

parser_upload = subparsers.add_parser('upload', help='上传文件')
parser_upload.add_argument('file', help='要上传的文件')

# =====================================
# 10. 实用技巧
# =====================================

# 【技巧 1】使用 formatter_class 美化帮助信息
from argparse import RawDescriptionHelpFormatter, ArgumentDefaultsHelpFormatter

parser = argparse.ArgumentParser(
    description='程序描述',
    formatter_class=RawDescriptionHelpFormatter  # 保留格式
)

# 【技巧 2】在帮助信息中显示默认值
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-p', '--port', default=8080, help='端口号')
# 帮助信息会显示：端口 (默认: 8080)

# 【技巧 3】使用 epilog 添加使用示例
parser = argparse.ArgumentParser(
    description='文件处理工具',
    epilog='''
使用示例:
  %(prog)s input.txt                    # 基本用法
  %(prog)s input.txt -o output.txt      # 指定输出
  %(prog)s input.txt -f json -v         # JSON 格式，详细模式
    '''
)

# 【技巧 4】使用 parents 共享参数
# 创建父解析器
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('-v', '--verbose', action='store_true')
parent_parser.add_argument('-q', '--quiet', action='store_true')

# 创建子解析器并继承父解析器的参数
parser = argparse.ArgumentParser(parents=[parent_parser])
parser.add_argument('-i', '--input', help='输入文件')

# =====================================
# 11. 调试技巧
# =====================================

# 【查看解析后的参数】
args = parser.parse_args()
print(args)        # 打印所有参数
print(args.input)  # 打印单个参数
print(vars(args))  # 以字典形式打印所有参数

# 【从字符串解析（用于测试）】
args = parser.parse_args(['-i', 'input.txt', '-v'])
# 相当于在命令行运行：python script.py -i input.txt -v

# =====================================
# 12. 完整示例
# =====================================

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description='文件转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s input.txt output.json
  %(prog)s -i data.txt -o result.json -f json -v
        '''
    )

    # 必需参数
    parser.add_argument('-i', '--input', required=True, help='输入文件')
    parser.add_argument('-o', '--output', required=True, help='输出文件')

    # 可选参数
    parser.add_argument('-f', '--format', choices=['json', 'csv', 'txt'],
                        default='json', help='输出格式')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='详细输出')
    parser.add_argument('--dry-run', action='store_true',
                        help='模拟运行')

    args = parser.parse_args()

    if args.verbose:
        print(f"输入：{args.input}")
        print(f"输出：{args.output}")
        print(f"格式：{args.format}")

    if args.dry_run:
        print("模拟运行模式")
        return 0

    # 实际处理逻辑...
    print("处理中...")
    return 0

if __name__ == "__main__":
    sys.exit(main())

# =====================================
# 总结
# =====================================

"""
argparse 的核心步骤：
1. 创建 ArgumentParser 对象
2. 使用 add_argument() 添加参数
3. 使用 parse_args() 解析参数
4. 通过 args.参数名 使用参数

常用参数类型：
- 位置参数：必须提供，按顺序
- 可选参数：用 - 或 -- 标记
- 布尔开关：action='store_true/false'
- 多值参数：nargs='+', '*', 数字

记住：
- 短选项用 -（如 -h）
- 长选项用 --（如 --help）
- 默认行为是存储值
- type 参数可以自动转换类型
"""
