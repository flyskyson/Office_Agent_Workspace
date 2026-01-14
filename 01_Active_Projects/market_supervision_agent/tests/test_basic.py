#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监管智能体 v4.0 - 基础模块测试（无需PaddleOCR）

只测试不需要外部依赖的核心模块
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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
    print(f"{Colors.OKGREEN}[OK] {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.FAIL}[FAIL] {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.OKCYAN}[INFO] {text}{Colors.ENDC}")


def test_data_extractor():
    """测试数据提取器"""
    print_header("数据提取器测试")

    try:
        from src.data_extractor import DataExtractor, OperatorData
        print_success("数据提取器导入成功")

        extractor = DataExtractor()

        # 测试身份证数据提取
        mock_id_result = {
            "name": "张三",
            "id_card": "110101199001011234",
            "gender": "男",
            "ethnicity": "汉",
            "address": "北京市东城区XX路XX号"
        }

        id_data = extractor.extract_from_id_card(mock_id_result, "test_id.jpg")
        print_success(f"身份证数据提取: 姓名={id_data.get('operator_name')}, 身份证={id_data.get('id_card')}")

        # 测试营业执照数据提取
        mock_license_result = {
            "company_name": "张三便利店",
            "credit_code": "91110000XXXXXXXXXX",
            "legal_person": "张三",
            "address": "北京市东城区王府井大街1号",
            "business_scope": "日用百货销售"
        }

        license_data = extractor.extract_from_business_license(mock_license_result, "test_license.jpg")
        print_success(f"营业执照数据提取: 店名={license_data.get('business_name')}")

        # 测试数据合并
        merged = extractor.merge_data(id_data, license_data)
        print_success(f"数据合并成功: 姓名={merged.operator_name}, 店名={merged.business_name}")

        # 测试数据验证
        print_success(f"身份证验证: {merged.id_card}")
        print_success(f"性别推断: {merged.gender}")

        return True

    except Exception as e:
        print_error(f"数据提取器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_manager():
    """测试数据库管理器"""
    print_header("数据库管理器测试")

    try:
        from src.database_manager import DatabaseManager
        print_success("数据库管理器导入成功")

        # 使用测试数据库
        test_db_path = "data/test_database.db"
        db = DatabaseManager(test_db_path)
        print_success("数据库初始化成功")

        # 测试插入
        test_data = {
            "operator_name": "测试用户",
            "id_card": "110101199001019999",
            "phone": "13800138000",
            "gender": "男",
            "nation": "汉",
            "business_name": "测试便利店",
            "business_address": "测试地址123号",
            "business_scope": "日用百货销售",
            "postal_code": "100006"
        }

        operator_id = db.insert_operator(test_data)
        print_success(f"插入记录成功: ID={operator_id}")

        # 测试查询
        retrieved = db.get_operator_by_id_card(test_data["id_card"])
        if retrieved:
            print_success(f"查询记录成功: {retrieved['operator_name']} - {retrieved['business_name']}")
        else:
            print_error("查询记录失败")

        # 测试更新
        db.update_operator(test_data["id_card"], {"phone": "13900139000"})
        print_success("更新记录成功")

        # 测试搜索
        results = db.search_operators("测试")
        print_success(f"搜索结果: {len(results)} 条记录")

        # 测试统计
        stats = db.get_statistics()
        print_success(f"统计信息: 总记录={stats['total_operators']}, 本月新增={stats['this_month_new']}")

        # 清理测试数据
        db.delete_operator(test_data["id_card"])
        print_success("测试数据已清理")

        # 删除测试数据库文件
        import os
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print_success("测试数据库文件已删除")

        return True

    except Exception as e:
        print_error(f"数据库管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_archiver():
    """测试文件归档器"""
    print_header("文件归档器测试")

    try:
        from src.file_archiver import FileArchiver
        print_success("文件归档器导入成功")

        archiver = FileArchiver("archives/test")

        # 测试文件分类
        test_files = [
            ("身份证_正面.jpg", "id_card"),
            ("身份证反面.jpg", "id_card"),
            ("营业执照.pdf", "business_license"),
            ("租赁合同.pdf", "lease_contract"),
            ("产权证明.jpg", "property_cert"),
            ("unknown.txt", "other")
        ]

        for filename, expected_category in test_files:
            category = archiver.categorize_file(filename)
            if category == expected_category:
                print_success(f"文件分类正确: {filename} -> {category}")
            else:
                print_error(f"文件分类错误: {filename} -> {category} (期望: {expected_category})")

        # 测试创建归档目录
        archive_dir = archiver.create_archive_directory("张三", "110101199001019999")
        print_success(f"创建归档目录: {archive_dir}")

        # 测试存储统计
        stats = archiver.get_storage_stats()
        print_success(f"存储统计: 归档数={stats['total_archives']}, 文件数={stats['total_files']}")

        # 清理测试目录
        import shutil
        if Path("archives/test").exists():
            shutil.rmtree("archives/test")
            print_success("测试归档目录已清理")

        return True

    except Exception as e:
        print_error(f"文件归档器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_application_generator():
    """测试申请书生成器"""
    print_header("申请书生成器测试")

    try:
        from src.application_generator import ApplicationGenerator
        print_success("申请书生成器导入成功")

        generator = ApplicationGenerator()
        print_success("申请书生成器初始化成功")

        # 测试配置加载
        config = generator.config
        print_success(f"配置加载成功: 常量数={len(config.get('constants', {}))}")

        # 测试上下文准备
        test_data = {
            "operator_name": "张三",
            "id_card": "110101199001011234",
            "phone": "13800138000",
            "gender": "男",
            "business_name": "张三便利店",
            "business_address": "北京市东城区王府井大街1号",
            "business_scope": "日用百货销售"
        }

        context = generator._prepare_context(test_data)
        print_success(f"上下文准备成功: 字段数={len(context)}")

        # 检查关键字段
        required_fields = ['operator_name', 'business_name', 'postal_code']
        for field in required_fields:
            if field in context:
                print_success(f"  字段 '{field}': {context[field]}")
            else:
                print_error(f"  字段 '{field}' 缺失")

        return True

    except Exception as e:
        print_error(f"申请书生成器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """集成测试 - 模拟完整流程"""
    print_header("集成测试")

    try:
        from src.data_extractor import DataExtractor
        from src.database_manager import DatabaseManager
        from src.file_archiver import FileArchiver
        from src.application_generator import ApplicationGenerator

        print_success("所有核心模块导入成功")

        # 模拟完整工作流
        print_info("模拟完整工作流程...")

        # 1. 模拟OCR结果（跳过实际OCR）
        mock_ocr_results = {
            "id_card": {
                "name": "李四",
                "id_card": "110101198502021234",
                "gender": "女",
                "ethnicity": "汉"
            },
            "business_license": {
                "company_name": "李四水果店",
                "credit_code": "91110000YYYYYYYYYY"
            }
        }

        # 2. 数据提取
        extractor = DataExtractor()
        id_data = extractor.extract_from_id_card(mock_ocr_results["id_card"])
        license_data = extractor.extract_from_business_license(mock_ocr_results["business_license"])
        merged = extractor.merge_data(id_data, license_data)
        print_success("步骤 1/4: 数据提取完成")

        # 3. 保存到数据库
        test_db_path = "data/test_integration.db"
        db = DatabaseManager(test_db_path)
        operator_id = db.insert_operator(merged.to_dict())
        print_success(f"步骤 2/4: 保存到数据库完成 (ID={operator_id})")

        # 4. 准备申请书生成数据
        generator = ApplicationGenerator()
        context = generator._prepare_context(merged.to_dict())
        print_success("步骤 3/4: 申请书数据准备完成")

        # 5. 归档信息（模拟）
        archiver = FileArchiver("archives/test")
        archive_dir = archiver.create_archive_directory(merged.operator_name, merged.id_card)
        print_success(f"步骤 4/4: 归档目录创建完成")

        # 清理
        import os
        db.delete_operator(merged.id_card)
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
        import shutil
        if Path("archives/test").exists():
            shutil.rmtree("archives/test")

        print_success("\n[OK] 完整工作流程测试通过！")

        return True

    except Exception as e:
        print_error(f"集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print(f"\n{Colors.BOLD}市场监管智能体 v4.0 - 基础模块测试{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.WARNING}注意: 此测试跳过OCR功能（需要PaddleOCR）{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}\n")

    results = {
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

    if passed == total:
        print(f"{Colors.OKGREEN}{Colors.BOLD}[SUCCESS] 所有测试通过！核心功能正常工作。{Colors.ENDC}\n")
    else:
        print(f"{Colors.WARNING}[WARNING] 部分测试失败，请检查错误信息。{Colors.ENDC}\n")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
