"""
命令行工具通用模板

使用说明：
1. 复制此文件到新项目，并重命名为你的工具名（如 my_tool.py）
2. 修改所有标记有 【】 的部分
3. 在 main() 函数中实现你的核心逻辑
4. 删除所有【】标记和本说明，形成你的专属工具
"""

import argparse
import sys
# 如果需要，在此导入你的业务模块
# 【例如】 import pandas as pd


def parse_arguments() -> argparse.Namespace:
    """
    解析命令行参数。
    注意：这是一个模板，你需要修改以下部分以适应你的具体工具。
    """
    parser = argparse.ArgumentParser(
        description='【你的工具名称】 - 【工具功能简要描述】',  # 【修改点1】填写你的工具描述
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s --input data.txt --output result.txt    # 基本用法示例
  %(prog)s --verbose                               # 启用详细输出
  # 【你可以在此添加更多针对你工具的使用示例】
        '''
    )

    # ========== 参数定义区域 ==========
    # 以下是一些常见的参数类型示例，请根据你的需求修改、删除或添加
    
    # 1. 必需参数示例（输入文件/文件夹）
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,  # 必需参数
        metavar='路径',
        help='【输入文件或文件夹的路径描述】'  # 【修改点2】填写具体的帮助信息
    )

    # 2. 可选参数示例（输出文件）
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='output',  # 默认值
        metavar='文件名',
        help='【输出文件路径或名称，默认: output】'  # 【修改点3】
    )

    # 3. 选择项参数示例
    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['json', 'csv', 'txt'],  # 【修改点4】可选的值列表
        default='json',
        metavar='格式',
        help='【输出格式选择，默认: json】'
    )

    # 4. 开关标志示例
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',  # 出现此参数则值为 True，否则为 False
        help='【启用详细输出模式】'
    )

    # 5. 数值参数示例
    parser.add_argument(
        '-n', '--number',
        type=int,
        default=10,
        metavar='数量',
        help='【指定数量参数，默认: 10】'
    )

    # 【你可以根据需要添加更多参数】
    # parser.add_argument(...)
    
    return parser.parse_args()


def main():
    """主函数 - 命令行工具的入口点"""
    # 1. 解析命令行参数
    args = parse_arguments()
    
    # 2. 参数验证（可选但推荐）
    # 【例如：检查输入文件是否存在、参数是否有效等】
    # if not os.path.exists(args.input):
    #     print(f"错误: 输入路径不存在 {args.input}")
    #     return 1
    
    # 3. 核心业务逻辑
    try:
        # 【在这里调用你的核心处理函数】
        # 【示例结构】
        if args.verbose:
            print(f"开始处理，输入: {args.input}, 输出: {args.output}")
        
        # ========== 你的核心逻辑开始 ==========
        # 【调用你的业务函数】
        # result = your_core_function(
        #     input_path=args.input,
        #     output_path=args.output,
        #     format=args.format,
        #     verbose=args.verbose
        # )
        # ========== 你的核心逻辑结束 ==========
        
        # 4. 处理完成
        print("✅ 处理完成！")
        return 0  # 返回 0 表示成功
        
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
        return 1
    except ValueError as e:
        print(f"❌ 参数错误: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
        return 1
    except Exception as e:
        print(f"❌ 发生未预期的错误: {e}")
        if args.verbose:  # 只有在详细模式下才打印完整错误栈
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    # 调用主函数并退出
    sys.exit(main())