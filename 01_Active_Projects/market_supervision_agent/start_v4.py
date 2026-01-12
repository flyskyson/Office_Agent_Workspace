#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监管智能体 v4.0 - 快速启动脚本

使用方法：
    python start_v4.py --help

示例：
    python start_v4.py test                    # 运行测试
    python start_v4.py ocr --image test.jpg   # OCR识别
    python start_v4.py generate --id 1        # 生成申请书
    python start_v4.py ui                     # 启动Web界面
"""

import sys
import argparse
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入核心模块
try:
    from src.ocr_adapter import OCREngineAdapter, create_ocr_engine
    from src.data_extractor import DataExtractor
    from src.database_manager import DatabaseManager
    from src.file_archiver import FileArchiver
    from src.application_generator import ApplicationGenerator
except ImportError as e:
    print(f"错误: 导入模块失败 - {e}")
    print("请先安装依赖: pip install -r requirements_v4.txt")
    sys.exit(1)


def cmd_test(args):
    """运行测试"""
    print("运行核心模块测试...")
    import subprocess
    result = subprocess.run([
        sys.executable,
        "tests/test_core_modules.py"
    ])
    return result.returncode


def cmd_ocr(args):
    """OCR识别"""
    print(f"OCR识别: {args.image}")

    # 使用 OCR 适配器（自动选择百度 OCR 或 PaddleOCR）
    engine = create_ocr_engine()

    if args.type == "id_card":
        result = engine.recognize_id_card(args.image)
        print(f"\n识别结果:")
        print(f"  姓名: {result.get('name', 'N/A')}")
        print(f"  身份证: {result.get('id_card', 'N/A')}")
        print(f"  性别: {result.get('gender', 'N/A')}")
        print(f"  民族: {result.get('nation', 'N/A')}")
        print(f"  地址: {result.get('address', 'N/A')}")

    elif args.type == "business_license":
        result = engine.recognize_business_license(args.image)
        print(f"\n识别结果:")
        print(f"  名称: {result.get('company_name', 'N/A')}")
        print(f"  信用代码: {result.get('credit_code', 'N/A')}")
        print(f"  法人: {result.get('legal_person', 'N/A')}")
        print(f"  地址: {result.get('address', 'N/A')}")

    else:
        result = engine.recognize_image(args.image)
        print(f"\n识别文本:\n{result.get('text', '')[:200]}...")

    return 0


def cmd_generate(args):
    """生成申请书"""
    db = DatabaseManager()

    if args.id:
        # 从数据库生成
        operator = db.get_operator_by_id(args.id)
        if not operator:
            print(f"错误: 找不到ID为 {args.id} 的记录")
            return 1

        print(f"生成申请书: {operator.get('business_name', 'N/A')}")

        generator = ApplicationGenerator()
        output = generator.generate_application(operator)
        print(f"生成成功: {output}")

    elif args.data:
        # 从JSON文件生成
        import json
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"生成申请书: {data.get('business_name', 'N/A')}")

        generator = ApplicationGenerator()
        output = generator.generate_application(data)
        print(f"生成成功: {output}")

    return 0


def cmd_db(args):
    """数据库操作"""
    db = DatabaseManager()

    if args.action == "list":
        operators = db.list_operators(limit=args.limit)
        print(f"\n共有 {len(operators)} 条记录:\n")
        for op in operators:
            print(f"  [{op['id']}] {op['operator_name']} - {op.get('business_name', 'N/A')}")

    elif args.action == "search":
        results = db.search_operators(args.keyword)
        print(f"\n找到 {len(results)} 条匹配记录:\n")
        for op in results:
            print(f"  [{op['id']}] {op['operator_name']} - {op.get('business_name', 'N/A')}")

    elif args.action == "stats":
        stats = db.get_statistics()
        print("\n数据库统计:")
        print(f"  总记录数: {stats['total_operators']}")
        print(f"  本月新增: {stats['this_month_new']}")
        print(f"  有营业执照: {stats['has_business_license']}")

    return 0


def cmd_archive(args):
    """文件归档"""
    archiver = FileArchiver()

    if args.action == "list":
        archives = archiver.list_archives()
        print(f"\n共有 {len(archives)} 个归档:\n")
        for arc in archives:
            print(f"  {arc['name']}: {arc['total_files']} 个文件")

    elif args.action == "stats":
        stats = archiver.get_storage_stats()
        print("\n归档存储统计:")
        print(f"  归档数: {stats['total_archives']}")
        print(f"  文件数: {stats['total_files']}")
        print(f"  总大小: {stats['total_size_mb']} MB")

    return 0


def cmd_ui(args):
    """启动Web界面"""
    ui_type = getattr(args, 'type', 'flask')

    if ui_type == 'flask':
        print("启动Flask界面...")
        print("[INFO] 按 Ctrl+C 停止服务")
        import subprocess
        subprocess.run([sys.executable, "ui/flask_app.py"])
    elif ui_type == 'streamlit':
        print("启动Streamlit界面...")
        print("[WARNING] Streamlit 可能与 Python 3.14+ 不兼容")
        import subprocess
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "ui/app_minimal.py"
        ])
    else:
        print(f"错误: 不支持的UI类型 '{ui_type}'")
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="市场监管智能体 v4.0 - 快速启动",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python start_v4.py test                    # 运行测试
  python start_v4.py ocr --image test.jpg   # OCR识别
  python start_v4.py generate --id 1        # 生成申请书
  python start_v4.py db list                # 列出所有记录
  python start_v4.py ui                     # 启动Web界面
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 测试命令
    subparsers.add_parser('test', help='运行测试')

    # OCR命令
    ocr_parser = subparsers.add_parser('ocr', help='OCR识别')
    ocr_parser.add_argument('--image', required=True, help='图片路径')
    ocr_parser.add_argument('--type', choices=['id_card', 'business_license', 'general'],
                           default='general', help='识别类型')
    ocr_parser.add_argument('--gpu', action='store_true', help='使用GPU')

    # 生成命令
    gen_parser = subparsers.add_parser('generate', help='生成申请书')
    gen_group = gen_parser.add_mutually_exclusive_group(required=True)
    gen_group.add_argument('--id', type=int, help='数据库记录ID')
    gen_group.add_argument('--data', help='JSON数据文件')

    # 数据库命令
    db_parser = subparsers.add_parser('db', help='数据库操作')
    db_parser.add_argument('action', choices=['list', 'search', 'stats'],
                          help='操作类型')
    db_parser.add_argument('--keyword', help='搜索关键词')
    db_parser.add_argument('--limit', type=int, default=20, help='列表限制')

    # 归档命令
    archive_parser = subparsers.add_parser('archive', help='文件归档')
    archive_parser.add_argument('action', choices=['list', 'stats'],
                              help='操作类型')

    # UI命令
    ui_parser = subparsers.add_parser('ui', help='启动Web界面')
    ui_parser.add_argument('--type', choices=['flask', 'streamlit'],
                          default='flask', help='UI类型 (默认: flask)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # 命令分发
    commands = {
        'test': cmd_test,
        'ocr': cmd_ocr,
        'generate': cmd_generate,
        'db': cmd_db,
        'archive': cmd_archive,
        'ui': cmd_ui
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        return cmd_func(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
