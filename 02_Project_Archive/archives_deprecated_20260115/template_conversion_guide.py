#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板转换助手 - 生成转换对照表
"""

from docx import Document
import json

def analyze_template():
    """分析原模板，生成转换指南"""

    print("=" * 70)
    print("模板转换助手")
    print("=" * 70)

    # 读取原模板
    src = Document(r'c:\Users\flyskyson\Desktop\（李奕凤）个体工商户开业登记申请书（模板-待修改）.docx')

    # 字段映射
    field_mappings = {
        "个体工商户名称": "business_name",
        "经营者姓名": "operator_name",
        "经营者": "operator_name",
        "联系电话": "phone",
        "电话": "phone",
        "电子邮箱": "email",
        "邮箱": "email",
        "经营场所": "business_address",
        "住所": "business_address",
        "地址": "business_address",
        "邮政编码": "postal_code",
        "邮编": "postal_code",
        "从业人数": "employee_count",
        "人数": "employee_count",
        "注册资金": "registered_capital",
        "资金": "registered_capital",
        "身份证号码": "id_card",
        "身份证": "id_card",
        "性别": "gender",
        "民族": "nation",
        "政治面貌": "political_status",
        "政治": "political_status",
        "文化程度": "education",
        "学历": "education",
        "经营范围": "business_scope",
        "经营期限": "operation_period",
        "期限": "operation_period"
    }

    # 示例数据
    sample_data = {
        "business_name": "兴业县蒲塘镇源兴快餐店",
        "operator_name": "李奕凤",
        "phone": "18207759518",
        "business_address": "广西壮族自治区玉林市兴业县蒲塘镇蒲安路238号",
        "postal_code": "537820",
        "id_card": "452501196705095123",
        "gender": "女",
        "nation": "汉",
        "political_status": "群众",
        "education": "初中",
        "employee_count": "2",
        "registered_capital": "10000"
    }

    print("\n转换对照表:")
    print("-" * 70)
    print(f"{'查找内容':<30} {'替换为':<25} {'说明'}")
    print("-" * 70)

    # 生成对照表
    conversion_list = []

    for cn_name, var_name in field_mappings.items():
        sample = sample_data.get(var_name, "")
        conversion_list.append({
            'find': sample,
            'replace': "{{" + var_name + "}}",
            'field': cn_name
        })

    # 去重并排序
    seen = set()
    unique_list = []
    for item in conversion_list:
        if item['find'] and item['find'] not in seen:
            seen.add(item['find'])
            unique_list.append(item)

    for item in unique_list:
        print(f"{item['find']:<30} {item['replace']:<25} {item['field']}")

    print("-" * 70)
    print(f"\n共 {len(unique_list)} 处需要转换")

    # 保存为JSON文件
    output_file = r'c:\Users\flyskyson\Desktop\conversion_guide.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(unique_list),
            'conversions': unique_list
        }, f, ensure_ascii=False, indent=2)

    print(f"\n转换指南已保存到: {output_file}")

    print("\n" + "=" * 70)
    print("操作步骤:")
    print("=" * 70)
    print("1. 在WPS中打开原模板:")
    print("   （李奕凤）个体工商户开业登记申请书（模板-待修改）.docx")
    print("\n2. 另存为新模板:")
    print("   文件名：Jinja2模板.docx")
    print("\n3. 查找并替换（使用上面的对照表）:")
    print("   - 按Ctrl+H打开查找替换")
    print("   - 查找上面的'查找内容'")
    print("   - 替换为上面的'替换为'")
    print("\n4. 保存后使用以下命令测试:")
    print("   python jinja2_filler.py --template \"Jinja2模板.docx\" --test")
    print("=" * 70)

if __name__ == "__main__":
    analyze_template()
