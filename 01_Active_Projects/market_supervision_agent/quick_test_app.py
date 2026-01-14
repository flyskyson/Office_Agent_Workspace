#!/usr/bin/env python3
"""
快速测试申请表生成器 - 简化版
"""

import os
import json
from pathlib import Path

def test_basic_function():
    """测试基本功能"""

    print("快速测试申请表生成器")
    print("=" * 50)

    # 1. 检查模板目录
    template_dir = Path("templates")
    if not template_dir.exists():
        print("创建模板目录...")
        template_dir.mkdir(exist_ok=True)

    # 2. 创建简单的模板文件
    template_file = template_dir / "设立登记申请书.txt"
    simple_template = """个体工商户设立登记申请书

申请事项：个体工商户设立登记

一、基本信息
1. 个体工商户名称：{business_name}
2. 经营者姓名：{operator_name}
3. 身份证号码：{id_card}
4. 经营场所：{business_address}
5. 经营范围：{business_scope}
6. 资金数额：{registered_capital}元
7. 联系电话：{phone}

申请人（签字）：
申请日期：{application_date}
"""

    if not template_file.exists():
        template_file.write_text(simple_template, encoding='utf-8')
        print(f"创建模板文件: {template_file.name}")

    # 3. 准备测试数据
    test_data = {
        "business_name": "张三小吃店",
        "operator_name": "张三",
        "id_card": "110101199001011234",
        "business_address": "北京市东城区王府井大街1号",
        "business_scope": "餐饮服务；小吃店经营",
        "registered_capital": "50000",
        "phone": "13800138000",
        "application_date": "2026年01月11日"
    }

    print("\n测试数据:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")

    # 4. 生成申请表
    try:
        # 填充模板
        application_text = simple_template.format(**test_data)

        # 创建输出目录
        output_dir = Path("generated_applications")
        output_dir.mkdir(exist_ok=True)

        # 保存文件
        output_file = output_dir / f"{test_data['business_name']}_申请书.txt"
        output_file.write_text(application_text, encoding='utf-8')

        print(f"\n[成功] 申请表生成成功！")
        print(f"文件位置: {output_file}")

        # 显示文件内容预览
        print("\n文件内容预览:")
        print("-" * 40)
        print(application_text[:200] + "...")
        print("-" * 40)

        # 5. 保存JSON数据
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        data_file = data_dir / f"{test_data['business_name']}_data.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        print(f"\n[成功] 数据已保存: {data_file}")

        return True

    except Exception as e:
        print(f"\n[错误] 生成失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("开始快速测试")
    print("=" * 60)

    success = test_basic_function()

    print("\n" + "=" * 60)
    if success:
        print("[成功] 测试完成！")
        print("\n下一步:")
        print("1. 查看 generated_applications/ 目录中的文件")
        print("2. 查看 data/ 目录中的JSON数据文件")
        print("3. 运行 python application_generator.py 使用完整功能")
    else:
        print("[失败] 测试未完成")
        print("\n建议:")
        print("1. 检查文件权限")
        print("2. 检查磁盘空间")
        print("3. 手动运行程序测试")

if __name__ == "__main__":
    main()