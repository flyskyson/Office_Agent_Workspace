"""
简单计算器 - 主入口文件
提供命令行界面进行四则运算
"""

import sys
import codecs
from pathlib import Path

# 修复Windows终端编码问题
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from simple_calculator.cli.cli_app import CalculatorCLI


def main():
    """
    主函数

    使用示例:
        python main.py + 10 5
        python main.py --interactive
        python main.py --help
    """
    # 创建CLI应用
    cli = CalculatorCLI()

    # 获取命令行参数（排除程序名）
    args = sys.argv[1:]

    # 运行CLI应用并返回退出码
    exit_code = cli.run(args)

    # 退出程序
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
