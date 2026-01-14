#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证工具 - 验证申请数据的完整性和正确性

功能:
1. 验证必填字段
2. 验证字段格式（如身份证、电话号码）
3. 检查数据一致性
4. 生成验证报告
5. 批量验证多个数据文件

作者: Claude Code
日期: 2026-01-12
"""

import json
import re
import sys
import os
from pathlib import Path
from datetime import datetime

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import locale
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


class DataValidator:
    """数据验证器"""

    def __init__(self, config_file="config.json"):
        self.config_file = Path(__file__).parent / config_file
        self.config = self.load_config()
        self.errors = []
        self.warnings = []

    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def validate(self, data, strict=False):
        """
        验证数据

        参数:
            data: 要验证的数据字典
            strict: 是否启用严格模式（更多检查）

        返回:
            (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        # 必填字段检查
        self._check_required_fields(data)

        # 字段格式检查
        self._check_formats(data)

        # 数据一致性检查
        self._check_consistency(data)

        # 业务规则检查
        self._check_business_rules(data)

        if strict:
            # 严格模式下的额外检查
            self._check_strict_rules(data)

        return len(self.errors) == 0, self.errors, self.warnings

    def _check_required_fields(self, data):
        """检查必填字段"""
        required_fields = [
            'business_name',
            'operator_name',
            'phone',
            'business_address',
            'id_card',
            'gender'
        ]

        for field in required_fields:
            if field not in data or not data[field] or str(data[field]).strip() == '':
                self.errors.append({
                    'field': field,
                    'message': f'缺少必填字段: {field}',
                    'severity': 'error'
                })

    def _check_formats(self, data):
        """检查字段格式"""
        # 检查手机号
        if 'phone' in data and data['phone']:
            phone = str(data['phone']).strip()
            if not re.match(r'^1[3-9]\d{9}$', phone):
                self.errors.append({
                    'field': 'phone',
                    'message': f'手机号格式不正确: {phone}',
                    'value': phone,
                    'severity': 'error'
                })

        # 检查身份证号
        if 'id_card' in data and data['id_card']:
            id_card = str(data['id_card']).strip()
            if not self._validate_id_card(id_card):
                self.errors.append({
                    'field': 'id_card',
                    'message': f'身份证号格式不正确: {id_card}',
                    'value': id_card,
                    'severity': 'error'
                })

        # 检查邮箱（如果提供）
        if 'email' in data and data['email']:
            email = str(data['email']).strip()
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                self.warnings.append({
                    'field': 'email',
                    'message': f'邮箱格式可能不正确: {email}',
                    'value': email,
                    'severity': 'warning'
                })

        # 检查邮编
        if 'postal_code' in data and data['postal_code']:
            postal_code = str(data['postal_code']).strip()
            if not re.match(r'^\d{6}$', postal_code):
                self.warnings.append({
                    'field': 'postal_code',
                    'message': f'邮政编码格式不正确: {postal_code}',
                    'value': postal_code,
                    'severity': 'warning'
                })

    def _check_consistency(self, data):
        """检查数据一致性"""
        # 检查性别字段
        if 'gender' in data and data['gender']:
            gender = str(data['gender']).strip()
            valid_genders = ['男', '女', '男性', '女性']
            if gender not in valid_genders:
                self.warnings.append({
                    'field': 'gender',
                    'message': f'性别值不常见: {gender}（建议使用: 男/女）',
                    'value': gender,
                    'severity': 'warning'
                })

        # 检查文化程度
        if 'education' in data and data['education']:
            education = str(data['education']).strip()
            valid_educations = ['小学', '初中', '高中', '中专', '大专', '本科', '硕士', '博士']
            if education not in valid_educations:
                self.warnings.append({
                    'field': 'education',
                    'message': f'文化程度值不常见: {education}',
                    'value': education,
                    'severity': 'warning'
                })

    def _check_business_rules(self, data):
        """检查业务规则"""
        # 检查注册资金是否为数字
        if 'registered_capital' in data and data['registered_capital']:
            capital = str(data['registered_capital']).strip()
            if not capital.isdigit():
                self.errors.append({
                    'field': 'registered_capital',
                    'message': f'注册资金必须为数字: {capital}',
                    'value': capital,
                    'severity': 'error'
                })

        # 检查从业人数是否为数字
        if 'employee_count' in data and data['employee_count']:
            count = str(data['employee_count']).strip()
            if not count.isdigit():
                self.errors.append({
                    'field': 'employee_count',
                    'message': f'从业人数必须为数字: {count}',
                    'value': count,
                    'severity': 'error'
                })

    def _check_strict_rules(self, data):
        """严格模式下的额外检查"""
        # 检查经营者姓名长度
        if 'operator_name' in data and data['operator_name']:
            name = str(data['operator_name']).strip()
            if len(name) < 2 or len(name) > 10:
                self.warnings.append({
                    'field': 'operator_name',
                    'message': f'经营者姓名长度异常: {name}（建议2-10个字符）',
                    'value': name,
                    'severity': 'warning'
                })

        # 检查经营场所地址
        if 'business_address' in data and data['business_address']:
            address = str(data['business_address']).strip()
            if len(address) < 10:
                self.warnings.append({
                    'field': 'business_address',
                    'message': f'经营场所地址过短: {address}',
                    'value': address,
                    'severity': 'warning'
                })

    def _validate_id_card(self, id_card):
        """验证身份证号格式和校验码"""
        # 基本格式检查
        if not re.match(r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$', id_card):
            return False

        # 校验码验证
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

        total = 0
        for i in range(17):
            total += int(id_card[i]) * weights[i]

        check_code = check_codes[total % 11]
        return id_card[-1].upper() == check_code

    def print_report(self, data, verbose=True):
        """打印验证报告"""
        print("\n" + "=" * 70)
        print("数据验证报告")
        print("=" * 70)

        # 显示基本信息
        print(f"\n个体工商户名称: {data.get('business_name', '未填写')}")
        print(f"经营者姓名: {data.get('operator_name', '未填写')}")

        # 显示错误
        if self.errors:
            print(f"\n[X] 发现 {len(self.errors)} 个错误:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. [{error['field']}] {error['message']}")
                if 'value' in error:
                    print(f"     值: {error['value']}")
        else:
            print("\n[OK] 没有发现错误")

        # 显示警告
        if self.warnings:
            print(f"\n[!] 发现 {len(self.warnings)} 个警告:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. [{warning['field']}] {warning['message']}")
                if 'value' in warning:
                    print(f"     值: {warning['value']}")
        else:
            print("\n[OK] 没有发现警告")

        # 总结
        print("\n" + "-" * 70)
        if not self.errors and not self.warnings:
            print("[OK] 数据验证通过！")
        elif not self.errors:
            print("[!] 数据存在警告，但仍可使用")
        else:
            print("[X] 数据验证失败，请修正错误后再试")

        print("=" * 70)

    def save_report(self, data, output_file):
        """保存验证报告到文件"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'errors': self.errors,
            'warnings': self.warnings,
            'summary': {
                'total_errors': len(self.errors),
                'total_warnings': len(self.warnings),
                'is_valid': len(self.errors) == 0
            }
        }

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"[成功] 验证报告已保存到: {output_file}")
            return True
        except Exception as e:
            print(f"[错误] 保存验证报告失败: {e}")
            return False


def validate_file(input_file, strict=False, save_report=False):
    """验证单个数据文件"""
    input_path = Path(input_file)

    if not input_path.is_absolute():
        input_path = Path(__file__).parent / input_file

    if not input_path.exists():
        print(f"[错误] 文件不存在: {input_path}")
        return False

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 如果是列表，取第一个元素
        if isinstance(data, list):
            if len(data) == 0:
                print("[错误] 数据文件为空")
                return False
            data = data[0]
            print(f"[提示] 检测到数据列表，只验证第一条数据")

        validator = DataValidator()
        is_valid, errors, warnings = validator.validate(data, strict=strict)
        validator.print_report(data)

        # 保存报告
        if save_report:
            report_file = input_path.stem + '_validation_report.json'
            validator.save_report(data, report_file)

        return is_valid

    except json.JSONDecodeError as e:
        print(f"[错误] JSON 格式错误: {e}")
        return False
    except Exception as e:
        print(f"[错误] 验证失败: {e}")
        return False


def validate_batch(input_file, strict=False):
    """批量验证数据文件"""
    input_path = Path(input_file)

    if not input_path.is_absolute():
        input_path = Path(__file__).parent / input_file

    if not input_path.exists():
        print(f"[错误] 文件不存在: {input_path}")
        return False

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data_list = json.load(f)

        if not isinstance(data_list, list):
            print("[提示] 数据不是列表格式，尝试作为单个数据验证")
            return validate_file(input_file, strict, True)

        print(f"\n批量验证 - 共 {len(data_list)} 条数据\n")
        print("=" * 70)

        validator = DataValidator()
        total_valid = 0
        total_errors = 0
        all_reports = []

        for idx, data in enumerate(data_list, 1):
            print(f"\n[第 {idx}/{len(data_list)} 条] {data.get('business_name', '未命名')}")

            is_valid, errors, warnings = validator.validate(data, strict=strict)

            if is_valid:
                print(f"  ✅ 通过")
                total_valid += 1
            else:
                print(f"  ❌ 失败 - {len(errors)} 个错误")
                total_errors += 1

            # 保存报告
            report = {
                'index': idx,
                'business_name': data.get('business_name', '未命名'),
                'is_valid': is_valid,
                'errors': errors,
                'warnings': warnings
            }
            all_reports.append(report)

        # 总结
        print("\n" + "=" * 70)
        print("批量验证总结")
        print("=" * 70)
        print(f"总计: {len(data_list)} 条")
        print(f"通过: {total_valid} 条")
        print(f"失败: {total_errors} 条")
        print("=" * 70)

        # 保存批量报告
        report_file = input_path.stem + '_batch_validation_report.json'
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'total': len(data_list),
                    'valid': total_valid,
                    'errors': total_errors,
                    'reports': all_reports
                }, f, ensure_ascii=False, indent=2)
            print(f"\n[成功] 批量验证报告已保存到: {report_file}")
        except Exception as e:
            print(f"[警告] 保存批量验证报告失败: {e}")

        return total_errors == 0

    except Exception as e:
        print(f"[错误] 批量验证失败: {e}")
        return False


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='数据验证工具 - 验证申请数据的完整性和正确性',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('file', nargs='?', help='要验证的JSON数据文件')
    parser.add_argument('--strict', action='store_true',
                        help='启用严格模式（更多检查）')
    parser.add_argument('--batch', action='store_true',
                        help='批量验证模式（数据文件包含多条数据）')
    parser.add_argument('--save-report', action='store_true',
                        help='保存验证报告到文件')

    args = parser.parse_args()

    if not args.file:
        print("数据验证工具 v1.0\n")
        print("使用方法:")
        print("  python data_validator.py data.json              # 验证单个数据文件")
        print("  python data_validator.py data.json --strict     # 严格模式")
        print("  python data_validator.py data.json --batch      # 批量验证")
        print("  python data_validator.py data.json --save-report # 保存验证报告")
        return

    if args.batch:
        success = validate_batch(args.file, args.strict)
    else:
        success = validate_file(args.file, args.strict, args.save_report)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[中断] 用户取消操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n[异常] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
