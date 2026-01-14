#!/usr/bin/env python3
"""
测试新版申请书填充工具
"""

import subprocess
import sys
from pathlib import Path
import json

def test_new_filler():
    """测试新版填充工具"""

    print("测试新版申请书填充工具")
    print("=" * 60)

    # 检查模板和测试数据
    template_file = "个体工商户开业登记申请书_新版.docx"
    test_data_file = "test_data.json"

    if not Path(template_file).exists():
        print(f"错误: 模板文件 {template_file} 不存在")
        return False

    if not Path(test_data_file).exists():
        print(f"错误: 测试数据文件 {test_data_file} 不存在")
        return False

    print(f"模板文件: {template_file}")
    print(f"测试数据: {test_data_file}")

    # 读取测试数据
    with open(test_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("\n测试数据:")
    print(f"  个体工商户名称: {data['business_name']}")
    print(f"  经营者姓名: {data['operator_name']}")
    print(f"  经营场所: {data['business_address']}")

    # 准备输入
    test_input = "2\n" + test_data_file + "\n"

    try:
        # 运行填充工具
        print("\n正在运行填充工具...")

        process = subprocess.Popen(
            [sys.executable, "新版申请书填充工具.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        stdout, stderr = process.communicate(input=test_input, timeout=30)

        print("\n程序输出:")
        print(stdout)

        if stderr:
            print("\n错误信息:")
            print(stderr)

        # 检查生成的文件
        output_dir = Path("output")
        if output_dir.exists():
            files = list(output_dir.glob("*.docx"))
            if files:
                print(f"\n[成功] 生成文件:")
                for file in files:
                    file_size = file.stat().st_size / 1024
                    print(f"  - {file.name} ({file_size:.1f} KB)")

                # 检查JSON数据文件
                json_files = list(output_dir.glob("*.json"))
                if json_files:
                    print(f"\n[数据文件]:")
                    for file in json_files:
                        print(f"  - {file.name}")

                return True
            else:
                print("\n[失败] 未生成Word文件")
        else:
            print("\n[失败] 输出目录不存在")

        return False

    except subprocess.TimeoutExpired:
        print("\n[错误] 程序超时")
        return False
    except Exception as e:
        print(f"\n[错误] 测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("开始测试新版Word模板填充工具")
    print("=" * 60)

    success = test_new_filler()

    print("\n" + "=" * 60)
    if success:
        print("[成功] 测试通过！")
        print("\n使用说明:")
        print("1. 打开 output/ 目录查看生成的Word文件")
        print("2. 使用示例数据: test_data.json")
        print("3. 或运行: python 新版申请书填充工具.py")
        print("4. 选择交互式填写或从JSON加载")
    else:
        print("[失败] 测试失败")
        print("\n可能的原因:")
        print("1. 模板文件格式有问题")
        print("2. python-docx库版本不兼容")
        print("3. 文件权限问题")

    print("=" * 60)

if __name__ == "__main__":
    main()