#!/usr/bin/env python3
"""
测试简化版Word填充工具
"""

import subprocess
import sys
from pathlib import Path

def test_simple_filler():
    """测试简化版填充工具"""

    # 检查模板文件
    template_file = "个体工商户开业登记申请书（模板）.docx"
    if not Path(template_file).exists():
        print(f"模板文件不存在: {template_file}")
        return False

    print("测试简化版Word填充工具")
    print("=" * 50)

    # 准备测试数据
    test_input = """张三小吃店
张三
110101199001011234
北京市东城区王府井大街1号
餐饮服务；小吃店经营
50000
13800138000
"""

    print("测试数据:")
    print(test_input)

    try:
        # 运行程序并传递输入
        process = subprocess.Popen(
            [sys.executable, "simple_word_filler.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        stdout, stderr = process.communicate(input=test_input, timeout=30)

        print("\n程序输出:")
        print(stdout)

        if stderr:
            print("\n错误信息:")
            print(stderr)

        # 检查是否生成文件
        output_dir = Path("output")
        if output_dir.exists():
            files = list(output_dir.glob("*.docx"))
            if files:
                print(f"\n✅ 成功生成文件:")
                for file in files:
                    print(f"  - {file.name}")
                return True
            else:
                print("\n❌ 未生成Word文件")
        else:
            print("\n❌ 输出目录不存在")

        return False

    except subprocess.TimeoutExpired:
        print("\n❌ 程序超时")
        return False
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("开始测试Word模板填充工具")
    print("=" * 60)

    success = test_simple_filler()

    print("\n" + "=" * 60)
    if success:
        print("✅ 测试成功！")
        print("生成的文件在 output/ 目录中")
    else:
        print("❌ 测试失败")
        print("可能的原因:")
        print("1. 模板文件有特殊字符")
        print("2. python-docx库有问题")
        print("3. 编码问题")

    print("\n建议:")
    print("1. 尝试清理Word模板中的特殊字符")
    print("2. 使用 application_generator.py 生成文本格式申请表")
    print("3. 或者手动填写Word模板")

if __name__ == "__main__":
    main()