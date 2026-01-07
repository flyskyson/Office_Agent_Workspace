"""
PDF 文本提取器
功能：批量提取文件夹中所有 PDF 文件的文本内容，并保存到 Markdown 或 JSON 文件中
"""

import os
import sys
import pdfplumber
import argparse
import json
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime

# Windows 控制台编码支持
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def get_pdf_files(folder_path: str) -> List[Path]:
    """
    获取指定文件夹中的所有 PDF 文件

    Args:
        folder_path: 文件夹路径

    Returns:
        PDF 文件的 Path 对象列表
    """
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"文件夹不存在: {folder_path}")

    if not folder.is_dir():
        raise NotADirectoryError(f"路径不是文件夹: {folder_path}")

    # 查找所有 .pdf 文件（不区分大小写）
    # 使用 set 去重，因为在 Windows 上 *.pdf 和 *.PDF 会匹配相同文件
    pdf_files = set(folder.glob("*.pdf")) | set(folder.glob("*.PDF"))
    return sorted(pdf_files)


def extract_text_from_pdf(pdf_path: Path) -> Tuple[str, bool, str]:
    """
    从单个 PDF 文件中提取文本

    Args:
        pdf_path: PDF 文件的 Path 对象

    Returns:
        (提取的文本内容, 是否成功, 错误信息)
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = []

            # 遍历每一页
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    # 提取当前页的文本
                    text = page.extract_text()
                    if text:
                        all_text.append(f"--- 第 {page_num} 页 ---\n{text}")
                    else:
                        all_text.append(f"--- 第 {page_num} 页 ---\n[此页无文本内容，可能是图片或扫描件]")
                except Exception as e:
                    all_text.append(f"--- 第 {page_num} 页 ---\n[提取失败: {str(e)}]")
                    continue

            # 合并所有页面的文本
            full_text = "\n\n".join(all_text)
            return full_text, True, ""

    except Exception as e:
        error_msg = str(e)
        # 判断常见错误类型
        if "encrypted" in error_msg.lower() or "password" in error_msg.lower():
            return "", False, "PDF 文件已加密，需要密码"
        elif "damaged" in error_msg.lower() or "corrupt" in error_msg.lower():
            return "", False, "PDF 文件已损坏"
        else:
            return "", False, f"读取失败: {error_msg}"


def save_to_markdown(results: List[Tuple[str, str, bool, str]], output_path: str) -> None:
    """
    将提取结果保存到 Markdown 文件

    Args:
        results: (文件名, 提取内容, 是否成功, 错误信息) 的列表
        output_path: 输出文件路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        # 写入文件头
        f.write("# PDF 文本提取结果\n\n")
        f.write(f"**提取时间**: {get_formatted_time()}\n\n")
        f.write("---\n\n")

        # 统计信息
        success_count = sum(1 for _, _, success, _ in results if success)
        fail_count = len(results) - success_count

        f.write(f"## 提取统计\n\n")
        f.write(f"- 总文件数: {len(results)}\n")
        f.write(f"- 成功提取: {success_count}\n")
        f.write(f"- 提取失败: {fail_count}\n\n")
        f.write("---\n\n")

        # 写入每个 PDF 的内容
        for filename, content, success, error_msg in results:
            f.write(f"## {filename}\n\n")

            if success:
                f.write(content)
            else:
                f.write(f"⚠️ **提取失败**: {error_msg}")

            f.write("\n\n---\n\n")


def save_to_json(results: List[Tuple[str, str, bool, str]], output_path: str) -> None:
    """
    将提取结果保存到 JSON 文件

    Args:
        results: (文件名, 提取内容, 是否成功, 错误信息) 的列表
        output_path: 输出文件路径
    """
    # 构建结果字典
    success_count = sum(1 for _, _, success, _ in results if success)
    fail_count = len(results) - success_count

    output_data = {
        "提取时间": get_formatted_time(),
        "统计": {
            "总文件数": len(results),
            "成功提取": success_count,
            "提取失败": fail_count
        },
        "文件": []
    }

    # 添加每个文件的结果
    for filename, content, success, error_msg in results:
        file_data = {
            "文件名": filename,
            "状态": "成功" if success else "失败"
        }

        if success:
            file_data["内容"] = content
            file_data["字符数"] = len(content)
        else:
            file_data["错误信息"] = error_msg

        output_data["文件"].append(file_data)

    # 保存到 JSON 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)


def get_formatted_time() -> str:
    """获取格式化的当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def process_pdfs(input_dir: str, output_format: str = 'markdown', output_name: str = '提取结果') -> int:
    """
    处理 PDF 文件提取的主逻辑

    Args:
        input_dir: 输入文件夹路径
        output_format: 输出格式 ('markdown' 或 'json')
        output_name: 输出文件名（不含扩展名）

    Returns:
        0 表示成功，1 表示失败
    """
    print("=" * 60)
    print("          PDF 文本批量提取工具")
    print("=" * 60)
    print()

    # 去除路径两端的引号
    input_dir = input_dir.strip('"').strip("'")

    print(f"📁 正在扫描文件夹: {input_dir}")

    # 获取所有 PDF 文件
    try:
        pdf_files = get_pdf_files(input_dir)
    except Exception as e:
        print(f"❌ 扫描文件夹失败: {e}")
        return 1

    if not pdf_files:
        print("⚠️  未找到任何 PDF 文件")
        return 0

    print(f"✅ 找到 {len(pdf_files)} 个 PDF 文件")
    print()

    # 提取每个 PDF 的文本
    results = []
    for index, pdf_path in enumerate(pdf_files, 1):
        filename = pdf_path.name
        print(f"[{index}/{len(pdf_files)}] 正在处理: {filename}...", end=" ")

        content, success, error_msg = extract_text_from_pdf(pdf_path)
        results.append((filename, content, success, error_msg))

        if success:
            # 显示提取的字符数
            char_count = len(content)
            print(f"✅ 成功 ({char_count} 字符)")
        else:
            print(f"❌ {error_msg}")

    print()
    print("=" * 60)

    # 确定输出文件扩展名
    if output_format == 'json':
        file_ext = '.json'
    else:
        file_ext = '.md'

    # 构建完整输出路径
    output_path = os.path.join(input_dir, f"{output_name}{file_ext}")
    print(f"💾 正在保存结果到: {output_path}")

    # 根据格式保存结果
    try:
        if output_format == 'json':
            save_to_json(results, output_path)
        else:
            save_to_markdown(results, output_path)
        print("✅ 结果保存成功！")
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return 1

    # 显示最终统计
    success_count = sum(1 for _, _, success, _ in results if success)
    fail_count = len(results) - success_count

    print()
    print("=" * 60)
    print("📊 提取完成统计")
    print("-" * 60)
    print(f"  总文件数: {len(results)}")
    print(f"  成功提取: {success_count}")
    print(f"  提取失败: {fail_count}")
    print("=" * 60)
    print(f"📄 结果文件: {output_path}")
    print()

    return 0


def parse_arguments() -> argparse.Namespace:
    """
    解析命令行参数

    Returns:
        解析后的参数对象
    """
    parser = argparse.ArgumentParser(
        description='PDF 文本批量提取工具 - 批量提取文件夹中所有 PDF 文件的文本内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s -i "C:\\Documents\\PDFs"                    # 使用默认设置（Markdown 格式）
  %(prog)s -i ./pdfs -f json                          # 输出为 JSON 格式
  %(prog)s -i "./my pdfs" -f markdown -o "我的提取结果"  # 自定义输出文件名
  %(prog)s --input ./documents --format json --output result  # 使用长参数名
        '''
    )

    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        metavar='路径',
        help='指定要处理的 PDF 文件夹路径（必需）'
    )

    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['markdown', 'json'],
        default='markdown',
        metavar='格式',
        help='指定输出格式：markdown 或 json（默认：markdown）'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='提取结果',
        metavar='文件名',
        help='指定输出文件名（不含扩展名）（默认：提取结果）'
    )

    return parser.parse_args()


def main():
    """主函数 - 使用 argparse 处理命令行参数"""
    # 解析命令行参数
    args = parse_arguments()

    # 调用核心处理逻辑
    return process_pdfs(
        input_dir=args.input,
        output_format=args.format,
        output_name=args.output
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
