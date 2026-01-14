#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监管智能体 v4.0 - 工作流测试

测试LangGraph工作流引擎的完整流程
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


def test_workflow_import():
    """测试工作流导入"""
    print_header("工作流导入测试")

    try:
        from src.workflow import (
            MarketSupervisionWorkflow,
            WorkflowState,
            process_files,
            quick_process
        )
        print_success("工作流模块导入成功")

        # 测试状态创建
        state = WorkflowState(
            detected_files=["test1.jpg", "test2.pdf"],
            current_step="testing"
        )
        print_success(f"状态创建成功: step={state['current_step']}, files={len(state['detected_files'])}")

        return True, MarketSupervisionWorkflow

    except Exception as e:
        print_error(f"工作流导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_workflow_initialization(WorkflowClass):
    """测试工作流初始化"""
    print_header("工作流初始化测试")

    try:
        workflow = WorkflowClass()
        print_success("工作流初始化成功")

        # 检查组件
        print_success(f"OCR引擎: {type(workflow.ocr_engine).__name__}")
        print_success(f"数据提取器: {type(workflow.data_extractor).__name__}")
        print_success(f"数据库管理器: {type(workflow.db_manager).__name__}")
        print_success(f"文件归档器: {type(workflow.file_archiver).__name__}")
        print_success(f"申请书生成器: {type(workflow.doc_generator).__name__}")

        return True, workflow

    except Exception as e:
        print_error(f"工作流初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_simple_workflow(workflow):
    """测试简化版工作流（不需要OCR）"""
    print_header("简化版工作流测试")

    try:
        # 模拟文件列表
        test_files = [
            "桌面/身份证_张三.jpg",
            "桌面/营业执照_张三便利店.jpg"
        ]

        # 配置：跳过OCR和归档
        config = {
            "skip_ocr": True,
            "skip_archiving": True,
            "skip_generation": True,
            "auto_clean_desktop": False
        }

        # 准备模拟的OCR结果
        from src.workflow import WorkflowState
        initial_state = WorkflowState(
            detected_files=test_files,
            config=config
        )

        # 手动设置OCR结果（模拟）
        initial_state["file_categories"] = {
            test_files[0]: "id_card",
            test_files[1]: "business_license"
        }
        initial_state["ocr_results"] = {
            test_files[0]: {
                "name": "王五",
                "id_card": "110101198008151234",
                "gender": "男",
                "ethnicity": "汉",
                "address": "北京市朝阳区XX路XX号"
            },
            test_files[1]: {
                "company_name": "王五小吃店",
                "credit_code": "91110000ZZZZZZZZZZ",
                "legal_person": "王五",
                "address": "北京市朝阳区XX路XX号",
                "business_scope": "小吃服务"
            }
        }

        # 执行工作流
        print_info("执行简化版工作流...")
        result = workflow._run_simple_workflow(initial_state)

        # 检查结果
        print_success(f"工作流完成: final_step={result['current_step']}")

        # 显示消息
        for msg in result.get("messages", []):
            print_info(f"  - {msg}")

        # 检查提取的数据
        if result.get("extracted_data"):
            data = result["extracted_data"]
            print_success(f"数据提取成功:")
            print_info(f"  - 姓名: {data.get('operator_name')}")
            print_info(f"  - 身份证: {data.get('id_card')}")
            print_info(f"  - 店名: {data.get('business_name')}")

        # 检查数据库
        if result.get("operator_id"):
            print_success(f"数据库记录ID: {result['operator_id']}")

            # 清理测试数据
            if data.get("id_card"):
                workflow.db_manager.delete_operator(data["id_card"])
                print_success("测试数据已清理")

        return True

    except Exception as e:
        print_error(f"简化版工作流测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_state_transitions():
    """测试状态转换"""
    print_header("状态转换测试")

    try:
        from src.workflow import WorkflowState

        # 测试初始状态
        state = WorkflowState()
        print_success(f"初始状态: {state['current_step']}")

        # 测试状态更新
        state["current_step"] = "processing"
        state["messages"].append("开始处理")
        print_success(f"状态更新: {state['current_step']}, 消息数: {len(state['messages'])}")

        # 测试错误状态
        state["error_message"] = "测试错误"
        state["retry_count"] = 1
        print_success(f"错误状态: {state['error_message']}, 重试次数: {state['retry_count']}")

        return True

    except Exception as e:
        print_error(f"状态转换测试失败: {e}")
        return False


def test_convenience_functions():
    """测试便捷函数"""
    print_header("便捷函数测试")

    try:
        from src.workflow import process_files, quick_process

        print_success("便捷函数导入成功")

        # 测试process_files签名
        import inspect
        sig = inspect.signature(process_files)
        print_success(f"process_files参数: {list(sig.parameters.keys())}")

        # 测试quick_process签名
        sig = inspect.signature(quick_process)
        print_success(f"quick_process参数: {list(sig.parameters.keys())}")

        return True

    except Exception as e:
        print_error(f"便捷函数测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print(f"\n{Colors.BOLD}市场监管智能体 v4.0 - 工作流测试{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.WARNING}注意: 测试使用模拟数据，跳过实际OCR识别{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}\n")

    results = {}

    # 1. 导入测试
    success, WorkflowClass = test_workflow_import()
    results["工作流导入"] = success

    if not success:
        print_error("无法继续测试，导入失败")
        return 1

    # 2. 初始化测试
    success, workflow = test_workflow_initialization(WorkflowClass)
    results["工作流初始化"] = success

    if not success:
        print_error("无法继续测试，初始化失败")
        return 1

    # 3. 状态转换测试
    results["状态转换"] = test_state_transitions()

    # 4. 便捷函数测试
    results["便捷函数"] = test_convenience_functions()

    # 5. 简化版工作流测试
    results["简化版工作流"] = test_simple_workflow(workflow)

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
        print(f"{Colors.OKGREEN}{Colors.BOLD}[SUCCESS] 工作流测试通过！{Colors.ENDC}\n")

        # 显示使用示例
        print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}使用示例:{Colors.ENDC}\n")
        print("# 方式1: 使用便捷函数")
        print("from src.workflow import process_files")
        print("result = process_files(['id.jpg', 'license.pdf'])")
        print("")
        print("# 方式2: 使用快速处理")
        print("from src.workflow import quick_process")
        print("result = quick_process('id.jpg', 'license.pdf')")
        print("")
        print("# 方式3: 使用工作流类")
        print("from src.workflow import MarketSupervisionWorkflow")
        print("workflow = MarketSupervisionWorkflow()")
        print("state = workflow.process(['id.jpg', 'license.pdf'])")
        print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}\n")

    else:
        print(f"{Colors.WARNING}[WARNING] 部分测试失败{Colors.ENDC}\n")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
