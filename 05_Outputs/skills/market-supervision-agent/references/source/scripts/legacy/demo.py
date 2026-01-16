#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监管智能体 v4.0 - 完整功能演示

展示所有核心功能的使用方法
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()


def print_banner():
    """打印横幅"""
    console.print(Panel.fit(
        "[bold cyan]市场监管智能体 v4.0[/bold cyan]\n"
        "[yellow]自动化申请处理系统[/yellow]",
        border_style="bright_blue"
    ))
    console.print()


def demo_1_basic_import():
    """演示1: 基本导入"""
    console.print("[bold blue]演示 1: 基本模块导入[/bold blue]")

    # 导入核心模块
    from src import (
        OCREngine,
        DataExtractor,
        OperatorData,
        DatabaseManager,
        FileArchiver,
        ApplicationGenerator,
        process_files,
        quick_process
    )

    console.print("[green]✓[/green] 所有核心模块导入成功")

    # 显示可用模块
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("模块")
    table.add_column("功能")
    table.add_column("状态")

    modules = [
        ("OCREngine", "OCR文字识别", "✓"),
        ("DataExtractor", "数据提取验证", "✓"),
        ("DatabaseManager", "数据库管理", "✓"),
        ("FileArchiver", "文件归档", "✓"),
        ("ApplicationGenerator", "申请书生成", "✓"),
        ("process_files", "工作流处理", "✓"),
        ("quick_process", "快速处理", "✓"),
    ]

    for module, func, status in modules:
        table.add_row(module, func, f"[green]{status}[/green]")

    console.print(table)
    console.print()


def demo_2_database_operations():
    """演示2: 数据库操作"""
    console.print("[bold blue]演示 2: 数据库操作[/bold blue]")

    from src.database_manager import DatabaseManager

    # 初始化数据库
    db = DatabaseManager("data/demo_database.db")
    console.print("[green]✓[/green] 数据库初始化完成")

    # 插入示例数据
    console.print("\n[cyan]→ 插入示例数据...[/cyan]")

    demo_data = {
        "operator_name": "演示用户",
        "id_card": "110101199001011111",
        "phone": "13800138000",
        "gender": "男",
        "business_name": "演示便利店",
        "business_address": "演示地址123号",
        "business_scope": "日用百货销售"
    }

    operator_id = db.insert_operator(demo_data)
    console.print(f"[green]✓[/green] 插入成功，ID: {operator_id}")

    # 查询数据
    console.print("\n[cyan]→ 查询数据...[/cyan]")
    retrieved = db.get_operator_by_id_card(demo_data["id_card"])
    if retrieved:
        console.print(f"[green]✓[/green] 查询成功: {retrieved['operator_name']} - {retrieved['business_name']}")

    # 搜索
    console.print("\n[cyan]→ 搜索功能...[/cyan]")
    results = db.search_operators("演示")
    console.print(f"[green]✓[/green] 搜索到 {len(results)} 条记录")

    # 统计
    console.print("\n[cyan]→ 统计信息...[/cyan]")
    stats = db.get_statistics()
    console.print(f"[green]✓[/green] 总记录: {stats['total_operators']}, 本月新增: {stats['this_month_new']}")

    # 清理
    db.delete_operator(demo_data["id_card"])
    console.print("\n[yellow]→ 清理演示数据[/yellow]")

    console.print()


def demo_3_file_classification():
    """演示3: 文件分类"""
    console.print("[bold blue]演示 3: 智能文件分类[/bold blue]")

    from src.file_archiver import FileArchiver

    archiver = FileArchiver("archives/demo")

    # 测试文件
    test_files = [
        "身份证_正面.jpg",
        "营业执照.pdf",
        "租赁合同.pdf",
        "产权证明.jpg",
        "申请表.docx",
        "unknown.txt"
    ]

    console.print("[cyan]→ 文件分类测试:[/cyan]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("文件名")
    table.add_column("分类")
    table.add_column("结果")

    for filename in test_files:
        category = archiver.categorize_file(filename)
        expected_map = {
            "身份证_正面.jpg": "id_card",
            "营业执照.pdf": "business_license",
            "租赁合同.pdf": "lease_contract",
            "产权证明.jpg": "property_cert",
            "申请表.docx": "application",
            "unknown.txt": "other"
        }
        expected = expected_map.get(filename)
        status = "[green]✓[/green]" if category == expected else "[red]✗[/red]"

        table.add_row(filename, category, status)

    console.print(table)
    console.print()


def demo_4_data_extraction():
    """演示4: 数据提取和验证"""
    console.print("[bold blue]演示 4: 数据提取和验证[/bold blue]")

    from src.data_extractor import DataExtractor

    extractor = DataExtractor()

    # 模拟OCR结果
    mock_id_card = {
        "name": "张三",
        "id_card": "110101199001011234",
        "gender": "男",
        "ethnicity": "汉"
    }

    mock_license = {
        "company_name": "张三便利店",
        "credit_code": "91110000XXXXXXXXXX",
        "address": "北京市东城区王府井大街1号"
    }

    console.print("[cyan]→ 模拟OCR识别结果:[/cyan]")
    console.print(f"  身份证: {mock_id_card['name']} - {mock_id_card['id_card']}")
    console.print(f"  营业执照: {mock_license['company_name']}")

    console.print("\n[cyan]→ 数据提取:[/cyan]")
    id_data = extractor.extract_from_id_card(mock_id_card)
    console.print(f"[green]✓[/green] 身份证数据: {len(id_data)} 个字段")

    license_data = extractor.extract_from_business_license(mock_license)
    console.print(f"[green]✓[/green] 营业执照数据: {len(license_data)} 个字段")

    console.print("\n[cyan]→ 数据合并和验证:[/cyan]")
    merged = extractor.merge_data(id_data, license_data)
    console.print(f"[green]✓[/green] 合并成功")
    console.print(f"  - 姓名: {merged.operator_name}")
    console.print(f"  - 身份证: {merged.id_card}")
    console.print(f"  - 性别: {merged.gender}")
    console.print(f"  - 店名: {merged.business_name}")

    # 验证结果
    missing = merged.get_missing_fields()
    if not missing:
        console.print(f"[green]✓[/green] 数据完整，无缺失字段")
    else:
        console.print(f"[yellow]⚠[/yellow] 缺失字段: {missing}")

    console.print()


def demo_5_workflow():
    """演示5: 工作流处理"""
    console.print("[bold blue]演示 5: 工作流自动化[/bold blue]")

    from src.workflow import MarketSupervisionWorkflow, WorkflowState

    # 初始化工作流
    workflow = MarketSupervisionWorkflow()
    console.print("[green]✓[/green] 工作流初始化成功")

    # 模拟文件处理（跳过OCR）
    console.print("\n[cyan]→ 模拟文件处理（跳过OCR）:[/cyan]")

    mock_files = [
        "桌面/身份证_李四.jpg",
        "桌面/营业执照_李四小吃店.jpg"
    ]

    # 准备状态
    state = WorkflowState(
        detected_files=mock_files,
        config={"skip_ocr": True, "skip_archiving": True, "skip_generation": True}
    )

    # 设置模拟OCR结果
    state["file_categories"] = {
        mock_files[0]: "id_card",
        mock_files[1]: "business_license"
    }
    state["ocr_results"] = {
        mock_files[0]: {
            "name": "李四",
            "id_card": "110101198502021234",
            "gender": "女"
        },
        mock_files[1]: {
            "company_name": "李四小吃店",
            "credit_code": "91110000YYYYYYYYYY"
        }
    }

    console.print(f"  文件: {len(mock_files)} 个")
    console.print(f"  分类: {state['file_categories']}")
    console.print(f"  OCR: 已模拟")

    # 执行工作流
    console.print("\n[cyan]→ 执行工作流...[/cyan]")

    steps = [
        ("文件分类", "classify_files"),
        ("OCR识别", "ocr_process"),
        ("数据提取", "extract_data"),
        ("保存数据库", "save_to_db"),
    ]

    for step_name, step_func in steps:
        console.print(f"  [dim]→[/dim] {step_name}...")

    result = workflow._run_simple_workflow(state)

    console.print(f"\n[green]✓[/green] 工作流完成: {result['current_step']}")

    # 显示结果
    for msg in result.get("messages", []):
        console.print(f"  [dim]-[/dim] {msg}")

    if result.get("extracted_data"):
        data = result["extracted_data"]
        console.print(f"\n[cyan]→ 提取的数据:[/cyan]")
        console.print(f"  姓名: {data.get('operator_name')}")
        console.print(f"  身份证: {data.get('id_card')}")
        console.print(f"  店名: {data.get('business_name')}")

    # 清理
    if data.get("id_card"):
        workflow.db_manager.delete_operator(data["id_card"])
        console.print(f"\n[yellow]→ 清理演示数据[/yellow]")

    console.print()


def demo_6_usage_examples():
    """演示6: 使用示例"""
    console.print("[bold blue]演示 6: 使用示例[/bold blue]")

    examples = [
        ("快速处理", "quick_process('id.jpg', 'license.pdf')"),
        ("批量处理", "process_files(['f1.jpg', 'f2.pdf', 'f3.jpg'])"),
        ("OCR识别", "OCREngine().recognize_id_card('id.jpg')"),
        ("数据库查询", "DatabaseManager().search_operators('关键词')"),
        ("生成申请书", "ApplicationGenerator().generate_application(data)"),
    ]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("功能")
    table.add_column("代码示例")
    table.add_column("说明")

    for func, code, desc in examples:
        table.add_row(func, f"[cyan]{code}[/cyan]", desc)

    console.print(table)

    console.print("\n[dim]提示: 运行 'python start_v4.py --help' 查看更多命令[/dim]\n")
    console.print()


def main():
    """主函数"""
    print_banner()

    console.print("[bold yellow]市场监管智能体 v4.0 - 功能演示[/bold yellow]\n")

    # 运行各个演示
    demo_1_basic_import()
    demo_2_database_operations()
    demo_3_file_classification()
    demo_4_data_extraction()
    demo_5_workflow()
    demo_6_usage_examples()

    # 结束
    console.print(Panel.fit(
        "[bold green]演示完成！[/bold green]\n\n"
        "[cyan]Web界面:[/cyan] streamlit run ui/app.py\n"
        "[cyan]运行测试:[/cyan] python tests/test_basic.py\n"
        "[cyan]查看帮助:[/cyan] python start_v4.py --help",
        border_style="bright_green"
    ))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]演示已取消[/yellow]")
    except Exception as e:
        console.print(f"\n[red]错误: {e}[/red]")
        import traceback
        traceback.print_exc()
