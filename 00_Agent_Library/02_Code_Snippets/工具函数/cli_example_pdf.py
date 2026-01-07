import argparse
import sys


def parse_arguments() -> argparse.Namespace:
    """
    解析命令行参数

    Returns:
        解析后的参数对象
    """
    parser = argparse.ArgumentParser(
        description='PDF 文本批量提取工具 - 批量提取文件夹中所有 PDF 文件的文本内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s -i "C:\\Documents\\PDFs"                    # 使用默认设置（Markdown 格式）
  %(prog)s -i ./pdfs -f json                          # 输出为 JSON 格式
  %(prog)s -i "./my pdfs" -f markdown -o "我的提取结果"  # 自定义输出文件名
  %(prog)s --input ./documents --format json --output result  # 使用长参数名
        '''
    )

    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        metavar='路径',
        help='指定要处理的 PDF 文件夹路径（必需）'
    )

    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['markdown', 'json'],
        default='markdown',
        metavar='格式',
        help='指定输出格式：markdown 或 json（默认：markdown）'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='提取结果',
        metavar='文件名',
        help='指定输出文件名（不含扩展名）（默认：提取结果）'
    )

    return parser.parse_args()

def main():
    """主函数 - 使用 argparse 处理命令行参数"""
    # 解析命令行参数
    args = parse_arguments()

    # 调用核心处理逻辑
    return process_pdfs(
        input_dir=args.input,
        output_format=args.format,
        output_name=args.output
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

