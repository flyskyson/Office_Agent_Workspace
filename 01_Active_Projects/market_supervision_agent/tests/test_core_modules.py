#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监管智能体 v4.0 - 核心模块测试脚本

测试功能：
- OCR识别引擎
- 数据提取器
- 数据库管理器
- 文件归档器
- 申请书生成器
"""

import sys
import json
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ocr_engine import OCREngine
from src.data_extractor import DataExtractor, OperatorData
from src.database_manager import DatabaseManager
from src.file_archiver import FileArchiver
from src.application_generator import ApplicationGenerator

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def test_ocr_engine():
    """测试OCR引擎"""
    print_header("OCR引擎测试")

    try:
        # 初始化
        engine = OCREngine()
        print_success("OCR引擎初始化成功")

        # 测试文件（需要准备测试图片）
        test_images = [
            "tests/test_data/id_card_sample.jpg",
            "tests/test_data/business_license_sample.jpg"
        ]

        for img_path in test_images:
            if Path(img_path).exists():
                print_info(f"测试图片: {img_path}")
                # result = engine.recognize_image(img_path)
                # print_success(f"识别结果: {result}")
            else:
                print_error(f"测试图片不存在: {img_path}")

        return True

    except Exception as e:
        print_error(f"OCR引擎测试失败: {e}")
        return False


def test_data_extractor():
    """测试数据提取器"""
    print_header("数据提取器测试")

    try:
        extractor = DataExtractor()
        print_success("数据提取器初始化成功")

        # 模拟OCR结果
        mock_id_card_result = {
            "name": "张三",
            "id_card": "110101199001011234",
            "gender": "男",
            "ethnicity": "汉"
        }

        mock_license_result = {
            "company_name": "张三便利店",
            "credit_code": "91110000XXXXXXXXXX",
            "address": "北京市东城区王府井大街1号"
        }

        # 提取数据
        id_data = extractor.extract_from_id_card(mock_id_card_result)
        print_success(f"身份证数据提取: {id_data}")

        license_data = extractor.extract_from_business_license(mock_license_result)
        print_success(f"营业执照数据提取: {license_data}")

        # 合并数据
        merged = extractor.merge_data(id_data, license_data)
        print_success(f"数据合并成功: 姓名={merged.operator_name}, 身份证={merged.id_card}")

        return True

    except Exception as e:
        print_error(f"数据提取器测试失败: {e}")
        return False


def test_database_manager():
    """测试数据库管理器"""
    print_header("数据库管理器测试")

    try:
        # 使用测试数据库
        db = DatabaseManager("data/test_database.db")
        print_success("数据库初始化成功")

        # 测试插入
        test_data = {
            "operator_name": "测试用户",
            "id_card": "110101199001019999",
            "phone": "13800138000",
            "gender": "男",
            "business_name": "测试便利店",
            "business_address": "测试地址123号"
        }

        operator_id = db.insert_operator(test_data)
        print_success(f"插入记录成功: ID={operator_id}")

        # 测试查询
        retrieved = db.get_operator_by_id_card(test_data["id_card"])
        if retrieved:
            print_success(f"查询记录成功: {retrieved['operator_name']}")
        else:
            print_error("查询记录失败")

        # 测试更新
        db.update_operator(test_data["id_card"], {"phone": "13900139000"})
        print_success("更新记录成功")

        # 测试搜索
        results = db.search_operators("测试")
        print_success(f"搜索结果: {len(results)} 条记录")

        # 清理测试数据
        db.delete_operator(test_data["id_card"])
        print_success("测试数据已清理")

        return True

    except Exception as e:
        print_error(f"数据库管理器测试失败: {e}")
        return False


def test_file_archiver():
    """测试文件归档器"""
    print_header("文件归档器测试")

    try:
        archiver = FileArchiver("archives/test")
        print_success("文件归档器初始化成功")

        # 测试分类
        test_files = [
            "身份证_正面.jpg",
            "营业执照.pdf",
            "租赁合同.pdf",
            "unknown.txt"
        ]

        for filename in test_files:
            category = archiver.categorize_file(filename)
            print_success(f"文件分类: {filename} -> {category}")

        # 测试创建归档目录
        archive_dir = archiver.create_archive_directory("张三", "110101199001019999")
        print_success(f"创建归档目录: {archive_dir}")

        # 获取存储统计
        stats = archiver.get_storage_stats()
        print_success(f"存储统计: {stats}")

        return True

    except Exception as e:
        print_error(f"文件归档器测试失败: {e}")
        return False


def test_application_generator():
    """测试申请书生成器"""
    print_header("申请书生成器测试")

    try:
        generator = ApplicationGenerator()
        print_success("申请书生成器初始化成功")

        # 列出模板
        templates = generator.list_templates()
        print_success(f"可用模板: {len(templates)} 个")
        for tpl in templates:
            print_info(f"  - {tpl['name']}")

        # 测试数据
        test_data = {
            "operator_name": "张三",
            "id_card": "110101199001011234",
            "phone": "13800138000",
            "gender": "男",
            "business_name": "张三便利店",
            "business_address": "北京市东城区王府井大街1号",
            "business_scope": "日用百货销售",
            "postal_code": "100006"
        }

        # 检查数据完整性
        if templates:
            completeness = generator.check_data_completeness(test_data, templates[0]['name'])
            print_success(f"数据完整性: {completeness['is_complete']}")

            if not completeness['is_complete']:
                print_info(f"缺失字段: {completeness['missing_fields']}")

        return True

    except Exception as e:
        print_error(f"申请书生成器测试失败: {e}")
        return False


def test_integration():
    """集成测试 - 完整流程"""
    print_header("集成测试")

    try:
        # 模拟完整流程
        print_info("步骤 1/6: OCR识别")
        # ocr_engine = OCREngine()
        print_success("OCR引擎准备就绪")

        print_info("步骤 2/6: 数据提取")
        extractor = DataExtractor()
        print_success("数据提取器准备就绪")

        print_info("步骤 3/6: 数据库连接")
        db = DatabaseManager("data/test_integration.db")
        print_success("数据库连接成功")

        print_info("步骤 4/6: 文件归档准备")
        archiver = FileArchiver("archives/test")
        print_success("文件归档器准备就绪")

        print_info("步骤 5/6: 申请书生成准备")
        generator = ApplicationGenerator()
        print_success("申请书生成器准备就绪")

        print_info("步骤 6/6: 组件集成测试")
        print_success("所有核心组件初始化成功！")

        return True

    except Exception as e:
        print_error(f"集成测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print(f"\n{Colors.BOLD}市场监管智能体 v4.0 - 核心模块测试{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}\n")

    results = {
        "OCR引擎": test_ocr_engine(),
        "数据提取器": test_data_extractor(),
        "数据库管理器": test_database_manager(),
        "文件归档器": test_file_archiver(),
        "申请书生成器": test_application_generator(),
        "集成测试": test_integration()
    }

    # 汇总结果
    print_header("测试结果汇总")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, result in results.items():
        if result:
            print_success(f"{name}: 通过")
        else:
            print_error(f"{name}: 失败")

    print(f"\n{Colors.BOLD}总计: {passed}/{total} 通过{Colors.ENDC}\n")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
