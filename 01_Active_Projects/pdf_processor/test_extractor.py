"""
测试 pdf_extractor.py 的脚本
"""

import os
import sys
from pathlib import Path

# 检查是否安装了依赖
try:
    import pdfplumber
    print("✅ pdfplumber 已安装")
except ImportError:
    print("❌ pdfplumber 未安装，请先运行: pip install pdfplumber")
    sys.exit(1)


def test_with_current_directory():
    """使用当前目录进行测试"""
    print("\n" + "="*60)
    print("测试方案 1: 使用当前项目目录")
    print("="*60)

    current_dir = str(Path(__file__).parent.absolute())
    print(f"当前目录: {current_dir}")

    # 检查是否有 PDF 文件
    pdf_files = list(Path(current_dir).glob("*.pdf")) + list(Path(current_dir).glob("*.PDF"))

    if not pdf_files:
        print("\n⚠️  当前目录没有 PDF 文件")
        print("建议：")
        print("  1. 将一些 PDF 文件复制到项目目录")
        print("  2. 或者使用方案 2 指定其他文件夹")
        return False

    print(f"找到 {len(pdf_files)} 个 PDF 文件:")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")

    print("\n开始运行 pdf_extractor.py...")
    print("提示: 请输入当前目录路径\n")

    # 导入并运行主程序
    from pdf_extractor import main
    main()
    return True


def test_with_custom_folder():
    """使用自定义文件夹进行测试"""
    print("\n" + "="*60)
    print("测试方案 2: 指定包含 PDF 的文件夹")
    print("="*60)

    print("\n请提供以下信息之一：")
    print("  1. 一个包含 PDF 文件的文件夹路径")
    print("  2. 按 Enter 直接运行 pdf_extractor.py（程序会提示输入路径）")

    user_input = input("\n是否现在运行 pdf_extractor.py? (Y/n): ").strip()

    if user_input.lower() in ['n', 'no']:
        print("测试取消")
        return False

    print("\n开始运行 pdf_extractor.py...\n")
    from pdf_extractor import main
    main()
    return True


def create_sample_test():
    """创建示例测试说明"""
    print("\n" + "="*60)
    print("测试建议")
    print("="*60)
    print("""
由于当前目录没有 PDF 文件，你可以：

1️⃣  **准备测试 PDF 文件**
    - 将一些 PDF 文件复制到项目目录
    - 或者记下某个包含 PDF 的文件夹路径

2️⃣  **运行测试**
    python pdf_extractor.py

3️⃣  **输入文件夹路径**
    - 程序会提示输入路径
    - 直接粘贴或输入包含 PDF 文件的文件夹路径

4️⃣  **查看结果**
    - 程序会在该文件夹下生成 "提取结果.md"
    - 打开该文件查看提取的内容

推荐测试场景：
  ✅ 包含多个 PDF 的文件夹
  ✅ 包含加密 PDF 的文件夹（测试错误处理）
  ✅ 包含扫描件/图片 PDF 的文件夹（测试空文本处理）
    """)


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("       PDF Extractor 测试程序")
    print("="*60)

    # 检查当前目录是否有 PDF
    current_dir = Path(__file__).parent
    pdf_files = list(current_dir.glob("*.pdf")) + list(current_dir.glob("*.PDF"))

    if pdf_files:
        # 有 PDF 文件，直接测试
        print(f"\n✅ 发现 {len(pdf_files)} 个 PDF 文件在当前目录")
        for pdf in pdf_files:
            print(f"   - {pdf.name}")

        response = input("\n是否使用当前目录进行测试? (Y/n): ").strip()

        if response.lower() not in ['n', 'no']:
            test_with_current_directory()
        else:
            test_with_custom_folder()
    else:
        # 没有 PDF 文件，提供选择
        create_sample_test()

        print("\n选择下一步操作:")
        print("  1. 直接运行 pdf_extractor.py（手动输入路径）")
        print("  2. 退出测试")

        choice = input("\n请选择 (1/2): ").strip()

        if choice == '1':
            from pdf_extractor import main
            print()
            main()
        else:
            print("\n测试结束。准备好 PDF 文件后可以随时运行:")
            print("  python pdf_extractor.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  测试中断")
    except Exception as e:
        print(f"\n\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
