"""
argparse 综合实战示例：一个完整的文件处理程序
"""

import argparse
import sys
from pathlib import Path

def process_files(input_path, output_path, format_type, verbose, dry_run):
    """
    处理文件的主函数
    """
    # 检查输入文件是否存在
    if not Path(input_path).exists():
        print(f"❌ 错误：输入文件不存在：{input_path}")
        return 1

    if verbose:
        print("=" * 60)
        print("📋 处理配置")
        print("-" * 60)
        print(f"输入文件：{input_path}")
        print(f"输出文件：{output_path}")
        print(f"输出格式：{format_type}")
        print(f"详细模式：开启")
        print(f"模拟运行：{'是' if dry_run else '否'}")
        print("=" * 60)
        print()

    # 模拟运行
    if dry_run:
        print("🔍 [模拟运行] 将执行以下操作：")
        print(f"  1. 读取文件：{input_path}")
        print(f"  2. 转换为 {format_type} 格式")
        print(f"  3. 保存到：{output_path}")
        print()
        print("✅ 模拟运行完成（未实际修改文件）")
        return 0

    # 实际处理（这里只是示例）
    print(f"⏳ 正在处理：{input_path}")
    print(f"✅ 处理完成！结果已保存到：{output_path}")

    return 0


def main():
    """
    主函数：使用 argparse 解析参数
    """
    # 创建解析器
    parser = argparse.ArgumentParser(
        description='文件格式转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s input.txt output.json                    # 基本用法
  %(prog)s -i data.txt -o result.json -f json -v    # 完整参数
  %(prog)s input.txt output.txt --dry-run           # 模拟运行
  %(prog)s --list                                  # 查看支持的格式
        '''
    )

    # ==================== 必需参数 ====================
    parser.add_argument(
        'input_file',
        nargs='?',  # 可选的位置参数（配合 default 使用）
        default=None,
        metavar='输入文件',
        help='要处理的输入文件路径'
    )

    parser.add_argument(
        'output_file',
        nargs='?',
        default=None,
        metavar='输出文件',
        help='输出文件路径'
    )

    # ==================== 可选参数 ====================
    parser.add_argument(
        '-i', '--input',
        dest='input_file',  # 存储到 input_file 变量
        help='输入文件路径（可选，也可以作为位置参数提供）'
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        help='输出文件路径（可选，也可以作为位置参数提供）'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['json', 'csv', 'txt', 'xml'],
        default='json',
        metavar='格式',
        help='输出格式（默认：json）'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细的处理信息'
    )

    parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='模拟运行，不实际修改文件'
    )

    parser.add_argument(
        '--list-formats',
        action='store_true',
        help='列出所有支持的输出格式'
    )

    # 解析参数
    args = parser.parse_args()

    # 处理特殊命令：列出格式
    if args.list_formats:
        print("支持的输出格式：")
        print("  - json  : JSON 格式")
        print("  - csv   : CSV 格式")
        print("  - txt   : 纯文本格式")
        print("  - xml   : XML 格式")
        return 0

    # 检查必需参数
    if not args.input_file or not args.output_file:
        parser.error("需要提供输入文件和输出文件路径")
        return 1

    # 调用处理函数
    return process_files(
        input_path=args.input_file,
        output_path=args.output_file,
        format_type=args.format,
        verbose=args.verbose,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 错误：{e}")
        sys.exit(1)


# ========================================
# 使用示例：
#
# 1. 查看帮助信息
# python argparse_demo7.py -h
#
# 2. 基本用法（位置参数）
# python argparse_demo7.py input.txt output.json
#
# 3. 使用选项参数
# python argparse_demo7.py -i input.txt -o output.json -f json
#
# 4. 启用详细模式
# python argparse_demo7.py input.txt output.json -v
#
# 5. 模拟运行（不实际修改文件）
# python argparse_demo7.py input.txt output.json --dry-run
#
# 6. 查看支持的格式
# python argparse_demo7.py --list-formats
#
# 7. 综合使用
# python argparse_demo7.py -i data.txt -o result.csv -f csv -v -d
# ========================================
