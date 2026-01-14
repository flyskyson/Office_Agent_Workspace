#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个体工商户开业登记申请书填充工具 v3.0 - Jinja2 模板版
- 基于 python-docx-template（docxtpl）
- 使用 Jinja2 模板语法
- 支持条件判断、循环等高级功能
- 模板制作更简单直观

作者: Claude Code + zread 协助
日期: 2026-01-12
"""

import json
import datetime
import sys
import argparse
from pathlib import Path
from docxtpl import DocxTemplate
from jinja2 import Environment, BaseLoader

# ============ 配置加载 ============

def load_config(config_file="config.json"):
    """加载全局配置文件"""
    config_path = Path(__file__).parent / config_file
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # 如果配置文件不存在，返回默认配置
        return {
            'constants': {
                'postal_code_default': '537820',
                'operation_period_default': '长期'
            },
            'defaults': {},
            'field_mappings': {}
        }

# ============ 模板验证 ============

def validate_template(template_file):
    """
    验证模板文件并获取所需的变量列表

    参数:
        template_file: 模板文件路径

    返回:
        所需变量集合
    """
    try:
        tpl = DocxTemplate(template_file)
        undeclared_variables = tpl.get_undeclared_template_variables()
        return undeclared_variables
    except Exception as e:
        print(f"[警告] 模板验证失败: {e}")
        return set()

# ============ 数据预处理 ============

def preprocess_data(data, config):
    """
    预处理数据，添加默认值和格式化

    参数:
        data: 原始数据字典
        config: 配置字典

    返回:
        处理后的数据字典
    """
    result = data.copy()

    # 应用常量
    constants = config.get('constants', {})
    if 'postal_code' not in result or not result['postal_code']:
        result['postal_code'] = constants.get('postal_code_default', '537820')
    if 'operation_period' not in result or not result['operation_period']:
        result['operation_period'] = constants.get('operation_period_default', '长期')

    # 处理经营范围 - 分为许可项目和一般项目
    if 'business_scope' in result and isinstance(result['business_scope'], str):
        scope_text = result['business_scope']

        # 默认值（如果数据中没有区分）
        result['business_scope_licensed'] = scope_text
        result['business_scope_general'] = scope_text

        # 尝试从分号分隔的内容中提取
        if '；' in scope_text or ';' in scope_text:
            parts = [s.strip() for s in scope_text.replace('；', ';').split(';')]
            if len(parts) >= 2:
                # 第一个作为许可项目，其余作为一般项目
                result['business_scope_licensed'] = parts[0]
                result['business_scope_general'] = '；'.join(parts[1:])

    # 如果没有这些字段，使用默认值
    if 'business_scope_licensed' not in result:
        result['business_scope_licensed'] = config.get('defaults', {}).get('business_scope_licensed', '小餐饮')
    if 'business_scope_general' not in result:
        result['business_scope_general'] = config.get('defaults', {}).get('business_scope_general', '食品销售（仅销售预包装食品）')

    # 处理经营范围列表（支持字符串或列表）
    if 'business_scope' in result and isinstance(result['business_scope'], str):
        # 将分号、逗号分隔的字符串转换为列表
        scope_text = result['business_scope']
        for sep in ['；', ';', '，', ',']:
            if sep in scope_text:
                result['business_scope_list'] = [s.strip() for s in scope_text.split(sep)]
                break
        else:
            result['business_scope_list'] = [scope_text]
    elif 'business_scope' not in result and 'business_scope_list' not in result:
        result['business_scope_list'] = []

    # 添加日期格式化
    today = datetime.datetime.now()
    result['today'] = today.strftime('%Y年%m月%d日')
    result['today_year'] = today.year
    result['today_month'] = today.month
    result['today_day'] = today.day

    # 性别到称谓的映射
    gender_map = {
        '男': '先生',
        '男性': '先生',
        '女': '女士',
        '女性': '女士'
    }
    if 'gender' in result:
        result['gender_title'] = gender_map.get(result['gender'], '')

    return result

# ============ 核心填充功能 ============

def fill_template(data, template_file="个体工商户开业登记申请书（Jinja2模板）.docx",
                  output_dir="output", auto_open=True, config=None, verbose=True):
    """
    使用 Jinja2 模板填充申请书

    参数:
        data: 包含申请信息的字典
        template_file: 模板文件路径
        output_dir: 输出目录
        auto_open: 是否自动打开文档
        config: 全局配置
        verbose: 是否显示详细信息

    返回:
        生成的文件路径，失败返回None
    """
    try:
        if config is None:
            config = load_config()

        # 检查模板文件
        template_path = Path(template_file)
        if not template_path.is_absolute():
            template_path = Path(__file__).parent / template_file

        if not template_path.exists():
            print(f"[错误] 模板文件不存在: {template_path}")
            return None

        if verbose:
            print(f"正在读取模板: {template_path}")

        # 验证模板并获取所需变量
        if verbose:
            print("正在验证模板...")
            required_vars = validate_template(str(template_path))
            if required_vars:
                print(f"  模板需要 {len(required_vars)} 个变量: {', '.join(sorted(required_vars))}")

        # 预处理数据
        context = preprocess_data(data, config)

        # 检查缺失的必需变量
        missing_vars = required_vars - set(context.keys()) if 'required_vars' in locals() else set()
        if missing_vars and verbose:
            print(f"  [警告] 缺少 {len(missing_vars)} 个变量: {', '.join(sorted(missing_vars))}")

        if verbose:
            print("正在渲染模板...")

        # 加载模板并渲染
        tpl = DocxTemplate(str(template_path))
        tpl.render(context)

        # 创建输出目录
        business_name = context.get("business_name", "未知")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        output_file = output_path / f"{business_name}_开业登记_{timestamp}.docx"

        # 保存文档
        tpl.save(str(output_file))

        # 保存数据（用于调试和记录）
        data_file = output_file.with_suffix('.json')
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(context, f, ensure_ascii=False, indent=2)

        if verbose:
            print(f"\n[成功] 申请书生成成功！")
            print(f"[文件] {output_file}")
            print(f"[数据] {data_file}")
            print(f"[统计] 渲染变量 {len(context)} 个")

        # 自动打开
        if auto_open:
            import subprocess
            subprocess.Popen(['cmd', '/c', 'start', '', str(output_file)], shell=True)
            if verbose:
                print("\n正在用WPS打开文档...")

        return output_file

    except Exception as e:
        print(f"\n[错误] 填充失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# ============ 批量处理 ============

def batch_fill(data_list, template_file, output_dir="output", config=None):
    """
    批量填充多个申请

    参数:
        data_list: 数据列表
        template_file: 模板文件路径
        output_dir: 输出目录
        config: 全局配置

    返回:
        成功生成的文件列表
    """
    results = []
    print(f"\n[批量处理] 共 {len(data_list)} 条数据\n")

    for idx, data in enumerate(data_list, 1):
        print(f"处理第 {idx}/{len(data_list)} 条:")
        result = fill_template(data, template_file, output_dir, auto_open=False, config=config)
        if result:
            results.append(result)
            print(f"  ✓ 完成")
        else:
            print(f"  ✗ 失败")

    return results

# ============ 主程序 ============

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='个体工商户开业登记申请书填充工具 v3.0 - Jinja2模板版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 使用测试数据
  python jinja2_filler.py --test

  # 从JSON文件加载数据
  python jinja2_filler.py --data test_data.json

  # 批量处理
  python jinja2_filler.py --batch data_list.json

  # 验证模板
  python jinja2_filler.py --validate 模板.docx

模板制作指南:
  1. 在Word文档中，使用 {{变量名}} 表示要替换的内容
  2. 使用 {% if 条件 %}...{% endif %} 进行条件判断
  3. 使用 {% for item in list %}...{% endfor %} 进行循环
  4. 保存为 .docx 文件即可作为模板
        """
    )

    parser.add_argument('--data', type=str, help='JSON数据文件路径')
    parser.add_argument('--batch', type=str, help='批量处理的JSON文件路径')
    parser.add_argument('--template', type=str,
                        default='（李奕凤）个体工商户开业登记申请书（Jinja2模板）.docx',
                        help='模板文件路径')
    parser.add_argument('--output', type=str, default='output', help='输出目录')
    parser.add_argument('--test', action='store_true', help='使用测试数据')
    parser.add_argument('--validate', type=str, metavar='模板文件',
                        help='验证模板并显示所需变量')
    parser.add_argument('--no-open', action='store_true', help='不自动打开文档')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式，减少输出')

    args = parser.parse_args()

    print("=" * 70)
    print("个体工商户开业登记申请书填充工具 v3.0")
    print("基于 Jinja2 模板 - 支持条件判断和循环")
    print("=" * 70)

    verbose = not args.quiet

    # 加载配置
    config = load_config()

    # 验证模板
    if args.validate:
        template_path = Path(args.validate)
        if not template_path.is_absolute():
            template_path = Path(__file__).parent / args.validate

        if not template_path.exists():
            print(f"\n[错误] 模板文件不存在: {template_path}")
            return 1

        print(f"\n正在验证模板: {template_path}")
        required_vars = validate_template(str(template_path))

        if required_vars:
            print(f"\n模板需要以下 {len(required_vars)} 个变量:\n")
            for var in sorted(required_vars):
                print(f"  - {var}")
        else:
            print("\n未找到任何模板变量")
        return 0

    # 检查模板文件
    template_path = Path(args.template)
    if not template_path.is_absolute():
        template_path = Path(__file__).parent / args.template

    if not template_path.exists():
        print(f"\n[错误] 模板文件不存在: {template_path}")
        print("\n提示:")
        print("  1. 请将模板文件放在当前目录")
        print("  2. 或使用 --template 参数指定模板文件")
        print("  3. 使用 --validate 检查现有模板")
        return 1

    auto_open = not args.no_open

    # 根据参数执行不同操作
    if args.test:
        # 使用测试数据
        test_data = {
            'business_name': '测试便利店',
            'operator_name': '张三',
            'phone': '13800138000',
            'email': 'zhangsan@example.com',
            'business_address': '广西玉林市兴业县蒲塘镇测试路123号',
            'postal_code': '537820',
            'employee_count': '2',
            'registered_capital': '30000',
            'id_card': '450101199001011234',
            'gender': '男',
            'nation': '汉族',
            'political_status': '群众',
            'education': '高中',
            'business_scope': '食品销售；日用百货；烟草制品零售',  # 支持分号分隔
            'operation_period': '长期'
        }

        if verbose:
            print("\n[测试模式] 使用预设测试数据\n")
        result = fill_template(test_data, str(template_path), args.output, auto_open, config, verbose)

    elif args.batch:
        # 批量处理
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                data_list = json.load(f)

            if isinstance(data_list, dict):
                data_list = [data_list]

            results = batch_fill(data_list, str(template_path), args.output, config)

            # 全部处理完后，打开最后一个文件
            if auto_open and results:
                import subprocess
                subprocess.Popen(['cmd', '/c', 'start', '', str(results[-1])], shell=True)

            print(f"\n[完成] 共生成 {len(results)} 个文档")
            if len(results) == 0:
                return 1

        except Exception as e:
            print(f"\n[错误] 批量处理失败: {e}")
            return 1

    elif args.data:
        # 从文件加载
        try:
            with open(args.data, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if verbose:
                print(f"\n[加载数据] 从文件: {args.data}\n")
            result = fill_template(data, str(template_path), args.output, auto_open, config, verbose)

            if not result:
                return 1

        except Exception as e:
            print(f"\n[错误] 加载数据失败: {e}")
            return 1

    else:
        # 显示帮助
        parser.print_help()
        print("\n快速开始:")
        print("  1. python jinja2_filler.py --test          # 使用测试数据")
        print("  2. python jinja2_filler.py --validate xxx.docx  # 验证模板")
        print("\n模板制作示例:")
        print("  在Word文档中输入: {{business_name}}")
        print("  保存为 .docx 文件即可作为模板")
        return 0

    if verbose:
        print("\n" + "=" * 70)
        print("处理完成！")
        print("=" * 70)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[中断] 用户取消操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n[异常] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
