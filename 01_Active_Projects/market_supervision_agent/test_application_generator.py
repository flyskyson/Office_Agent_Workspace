#!/usr/bin/env python3
"""
测试申请表生成器
"""

import subprocess
import sys
import time
from pathlib import Path

def test_application_generator():
    """测试申请表生成器"""

    print("测试申请表生成器")
    print("=" * 50)

    # 检查模板目录
    template_dir = Path("templates")
    if not template_dir.exists():
        print("模板目录不存在，程序会自动创建")

    # 准备测试输入
    test_inputs = [
        "1",  # 选择设立登记申请书
        "张三小吃店",  # 个体工商户名称
        "张三",  # 经营者姓名
        "男",  # 性别
        "110101199001011234",  # 身份证号码
        "北京市东城区王府井大街1号",  # 经营场所
        "餐饮服务；小吃店经营",  # 经营范围
        "50000",  # 资金数额
        "13800138000",  # 联系电话
        "6"  # 退出系统
    ]

    input_text = "\n".join(test_inputs)

    print("测试输入:")
    for i, inp in enumerate(test_inputs, 1):
        print(f"  {i}. {inp}")

    try:
        # 运行程序
        process = subprocess.Popen(
            [sys.executable, "application_generator.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        # 发送输入
        stdout, stderr = process.communicate(input=input_text, timeout=30)

        print("\n程序输出:")
        print("-" * 50)
        print(stdout[:500])  # 只打印前500个字符

        if stderr:
            print("\n错误信息:")
            print(stderr)

        # 检查是否生成文件
        output_dir = Path("generated_applications")
        if output_dir.exists():
            files = list(output_dir.glob("*.txt"))
            if files:
                print(f"\n[OK] 成功生成文件:")
                for file in files:
                    print(f"  - {file.name}")
                    # 显示文件内容
                    try:
                        content = file.read_text(encoding='utf-8')
                        print(f"    内容预览: {content[:100]}...")
                    except:
                        print(f"    无法读取文件内容")
                return True
            else:
                print("\n[错误] 未生成文本文件")
        else:
            print("\n[错误] 输出目录不存在")

        return False

    except subprocess.TimeoutExpired:
        print("\n[错误] 程序超时")
        return False
    except Exception as e:
        print(f"\n[错误] 测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("开始测试申请表生成器")
    print("=" * 60)

    success = test_application_generator()

    print("\n" + "=" * 60)
    if success:
        print("[OK] 测试成功！")
        print("生成的文件在 generated_applications/ 目录中")
    else:
        print("[错误] 测试失败")
        print("可能的原因:")
        print("1. 程序有编码问题")
        print("2. 输入格式不正确")
        print("3. 文件权限问题")

    print("\n建议:")
    print("1. 直接运行 python application_generator.py 手动测试")
    print("2. 输入 '1' 选择设立登记申请书")
    print("3. 按照提示输入信息")

if __name__ == "__main__":
    main()