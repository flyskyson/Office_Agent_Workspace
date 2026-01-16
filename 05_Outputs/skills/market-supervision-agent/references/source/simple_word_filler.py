#!/usr/bin/env python3
"""
简单的Word模板填充工具
只处理基本字段，避免编码问题
"""

import sys
from pathlib import Path
import json
import datetime

try:
    from docx import Document
except ImportError:
    print("需要安装 python-docx 库")
    print("请运行: pip install python-docx")
    sys.exit(1)

def clean_text(text):
    """清理文本，移除无效字符"""
    if not text:
        return ""
    # 移除控制字符和无效Unicode
    cleaned = ''.join(char for char in text if ord(char) >= 32 and ord(char) != 65533)
    return cleaned

def main():
    print("个体工商户开业登记申请书填充工具")
    print("=" * 50)

    # 检查模板
    template_file = "个体工商户开业登记申请书（模板）.docx"
    if not Path(template_file).exists():
        print(f"错误: 模板文件 '{template_file}' 不存在")
        return

    print(f"找到模板文件: {template_file}")
    print("\n请填写以下信息:")

    # 收集基本信息
    data = {}
    data["business_name"] = input("个体工商户名称: ").strip()
    data["operator_name"] = input("经营者姓名: ").strip()
    data["id_card"] = input("身份证号码: ").strip()
    data["business_address"] = input("经营场所: ").strip()
    data["business_scope"] = input("经营范围: ").strip()
    data["registered_capital"] = input("资金数额（元）: ").strip()
    data["phone"] = input("联系电话: ").strip()
    data["application_date"] = datetime.datetime.now().strftime("%Y年%m月%d日")

    print("\n正在处理...")

    try:
        # 读取模板
        doc = Document(template_file)

        # 只替换几个关键字段，避免编码问题
        replacements = {
            "个体工商户名称": clean_text(data["business_name"]),
            "经营者姓名": clean_text(data["operator_name"]),
            "身份证号码": clean_text(data["id_card"]),
            "经营场所": clean_text(data["business_address"]),
            "经营范围": clean_text(data["business_scope"]),
            "资金数额": clean_text(data["registered_capital"]),
            "联系电话": clean_text(data["phone"]),
            "申请日期": clean_text(data["application_date"])
        }

        # 简单替换：只在段落中替换
        for paragraph in doc.paragraphs:
            text = paragraph.text
            for old_text, new_text in replacements.items():
                if old_text in text and new_text:
                    paragraph.text = text.replace(old_text, new_text)
                    break  # 只替换一次

        # 创建输出目录
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        # 生成文件名
        filename = f"{data['business_name']}_申请书_{datetime.datetime.now().strftime('%Y%m%d')}.docx"
        output_file = output_dir / filename

        # 保存文件
        doc.save(str(output_file))

        print(f"\n成功生成文件: {output_file}")

        # 保存数据
        data_file = output_file.with_suffix('.json')
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据文件: {data_file}")

    except Exception as e:
        print(f"\n处理失败: {str(e)}")
        print("可能的原因:")
        print("1. 模板文件损坏")
        print("2. 包含特殊字符")
        print("3. 权限问题")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已取消")
    except Exception as e:
        print(f"\n程序错误: {str(e)}")