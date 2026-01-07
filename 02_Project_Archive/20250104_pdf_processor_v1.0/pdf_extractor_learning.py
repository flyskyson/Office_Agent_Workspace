"""
PDF 文本提取器 - 学习版
========================
功能：批量提取文件夹中所有 PDF 文件的文本内容，并保存到 Markdown 或 JSON 文件中

适合：编程初学者学习 Python 基础知识
包含：详细的中文注释，解释每个函数、参数和逻辑的作用
"""

# ========================================
# 第一部分：导入需要的库
# ========================================
import os              # 操作系统相关功能，用于处理文件路径
import sys             # 系统相关功能，用于获取命令行参数和退出程序
import pdfplumber      # PDF 处理库，用于读取 PDF 文件内容
import argparse        # 命令行参数解析库，用于处理用户输入的参数
import json            # JSON 数据处理库，用于生成 JSON 格式的输出
from pathlib import Path   # 面向对象的路径处理库，让文件路径操作更简单
from typing import List, Tuple, Dict  # 类型提示，帮助代码更清晰
from datetime import datetime  # 日期时间库，用于获取当前时间

# ========================================
# 第二部分：Windows 控制台中文支持
# ========================================
# 检查是否在 Windows 系统上运行
if sys.platform == 'win32':
    import codecs  # 编码转换库
    # 设置标准输出使用 UTF-8 编码，避免中文乱码
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    # 设置标准错误输出使用 UTF-8 编码
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# ========================================
# 第三部分：核心功能函数
# ========================================

def get_pdf_files(folder_path: str) -> List[Path]:
    """
    获取指定文件夹中的所有 PDF 文件

    Args:
        folder_path: 文件夹路径，例如 "C:/Documents/PDFs"

    Returns:
        PDF 文件的 Path 对象列表，按文件名排序
        例如：[Path('file1.pdf'), Path('file2.pdf')]

    知识点：
        - Path 对象：表示文件路径，可以方便地进行路径操作
        - glob()：查找匹配特定模式的文件
        - set：集合，用于去重
        - sorted()：排序
    """
    # 创建 Path 对象
    folder = Path(folder_path)

    # 检查文件夹是否存在
    if not folder.exists():
        # 如果不存在，抛出异常并提示用户
        raise FileNotFoundError(f"文件夹不存在: {folder_path}")

    # 检查路径是否是文件夹
    if not folder.is_dir():
        # 如果不是文件夹，抛出异常
        raise NotADirectoryError(f"路径不是文件夹: {folder_path}")

    # 查找所有 .pdf 文件（小写）
    # glob("*.pdf") 返回所有匹配 *.pdf 的文件
    pdf_files_lower = folder.glob("*.pdf")

    # 查找所有 .PDF 文件（大写）
    # Windows 系统不区分大小写，但有些文件可能是 .PDF 扩展名
    pdf_files_upper = folder.glob("*.PDF")

    # 使用 set 合并两个列表并去重
    # | 运算符用于集合的合并
    pdf_files = set(pdf_files_lower) | set(pdf_files_upper)

    # 返回排序后的列表
    return sorted(pdf_files)


def extract_text_from_pdf(pdf_path: Path) -> Tuple[str, bool, str]:
    """
    从单个 PDF 文件中提取文本

    Args:
        pdf_path: PDF 文件的 Path 对象

    Returns:
        返回一个包含三个元素的元组：
        1. 提取的文本内容（字符串）
        2. 是否成功（布尔值：True/False）
        3. 错误信息（字符串，成功时为空）

        例如：("提取的文本内容...", True, "")
             或 ("", False, "PDF 文件已加密")

    知识点：
        - 元组：不可变的序列，用 () 表示
        - try-except：异常处理，捕获并处理错误
        - with 语句：自动管理资源（文件打开/关闭）
        - enumerate()：同时获取索引和值
        - 字符串方法：lower() 转小写，in 判断包含
    """
    try:
        # 使用 pdfplumber 打开 PDF 文件
        # with 语句会自动关闭文件，即使发生错误
        with pdfplumber.open(pdf_path) as pdf:
            # 创建一个列表，用于存储所有页面的文本
            all_text = []

            # 遍历 PDF 的每一页
            # enumerate() 返回 (页码, 页面对象) 的对
            # 参数 1 表示页码从 1 开始计数（而不是默认的 0）
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    # 提取当前页的文本
                    text = page.extract_text()

                    # 如果提取到了文本内容
                    if text:
                        # 添加页码标记和文本内容到列表
                        all_text.append(f"--- 第 {page_num} 页 ---\n{text}")
                    else:
                        # 如果没有文本内容，可能是图片或扫描件
                        all_text.append(f"--- 第 {page_num} 页 ---\n[此页无文本内容，可能是图片或扫描件]")

                except Exception as e:
                    # 如果处理某一页时出错，记录错误但继续处理其他页
                    all_text.append(f"--- 第 {page_num} 页 ---\n[提取失败: {str(e)}]")
                    continue  # 跳过当前页，继续下一页

            # 使用 "\n\n" 分隔符合并所有页面的文本
            # "\n\n" 表示两个换行符，即段落之间空一行
            full_text = "\n\n".join(all_text)

            # 返回成功结果：文本内容、成功标志、空错误信息
            return full_text, True, ""

    except Exception as e:
        # 如果打开 PDF 或处理过程中发生错误
        error_msg = str(e)

        # 判断错误类型，给出友好的提示
        # lower() 将字符串转换为小写，便于判断
        if "encrypted" in error_msg.lower() or "password" in error_msg.lower():
            # PDF 文件被加密保护
            return "", False, "PDF 文件已加密，需要密码"
        elif "damaged" in error_msg.lower() or "corrupt" in error_msg.lower():
            # PDF 文件已损坏
            return "", False, "PDF 文件已损坏"
        else:
            # 其他未知错误
            return "", False, f"读取失败: {error_msg}"


def save_to_markdown(results: List[Tuple[str, str, bool, str]], output_path: str) -> None:
    """
    将提取结果保存到 Markdown 文件

    Args:
        results: 提取结果列表，每个元素是一个包含四项的元组：
                (文件名, 提取内容, 是否成功, 错误信息)
        output_path: 输出文件的完整路径

    Returns:
        None（无返回值）

    知识点：
        - with open()：打开文件进行读写
        - encoding='utf-8'：指定文件编码，支持中文
        - sum()：求和函数
        - f-string：格式化字符串（Python 3.6+）
    """
    # 打开文件进行写入
    # 'w' 表示写入模式，如果文件已存在会被覆盖
    # encoding='utf-8' 确保中文能正确保存
    with open(output_path, 'w', encoding='utf-8') as f:
        # ==================== 写入文件标题 ====================
        # \n 表示换行符
        f.write("# PDF 文本提取结果\n\n")  # # 是 Markdown 的一级标题

        # 写入提取时间
        # f-string 中的 {} 会被替换成实际的值
        f.write(f"**提取时间**: {get_formatted_time()}\n\n")  # **文字** 表示加粗
        f.write("---\n\n")  # --- 是 Markdown 的分隔线

        # ==================== 写入统计信息 ====================
        # 计算成功和失败的数量
        # sum() 函数配合生成器表达式，统计 success 为 True 的数量
        success_count = sum(1 for _, _, success, _ in results if success)
        fail_count = len(results) - success_count

        # 写入统计部分
        f.write(f"## 提取统计\n\n")  # ## 是 Markdown 的二级标题
        f.write(f"- 总文件数: {len(results)}\n")  # - 表示列表项
        f.write(f"- 成功提取: {success_count}\n")
        f.write(f"- 提取失败: {fail_count}\n\n")
        f.write("---\n\n")

        # ==================== 写入每个文件的内容 ====================
        # 遍历所有文件的提取结果
        for filename, content, success, error_msg in results:
            # 写入文件名作为二级标题
            f.write(f"## {filename}\n\n")

            if success:
                # 如果提取成功，写入文本内容
                f.write(content)
            else:
                # 如果提取失败，写入错误信息
                # ⚠️ 是警告符号
                f.write(f"⚠️ **提取失败**: {error_msg}")

            # 用分隔线分开不同文件的内容
            f.write("\n\n---\n\n")


def save_to_json(results: List[Tuple[str, str, bool, str]], output_path: str) -> None:
    """
    将提取结果保存到 JSON 文件

    Args:
        results: 提取结果列表
        output_path: 输出文件的完整路径

    Returns:
        None

    知识点：
        - JSON：轻量级的数据交换格式
        - 字典：键值对的数据结构
        - 列表的 append() 方法：添加元素
        - json.dump()：将 Python 对象转换为 JSON 格式并保存到文件
        - ensure_ascii=False：允许 JSON 中包含非 ASCII 字符（如中文）
        - indent=2：格式化输出，使 JSON 易于阅读
    """
    # 计算统计信息
    success_count = sum(1 for _, _, success, _ in results if success)
    fail_count = len(results) - success_count

    # 构建要输出的数据结构（字典）
    output_data = {
        "提取时间": get_formatted_time(),
        "统计": {
            "总文件数": len(results),
            "成功提取": success_count,
            "提取失败": fail_count
        },
        "文件": []  # 空列表，稍后添加每个文件的信息
    }

    # 遍历所有文件，构建每个文件的信息
    for filename, content, success, error_msg in results:
        # 创建字典存储当前文件的信息
        file_data = {
            "文件名": filename,
            "状态": "成功" if success else "失败"
        }

        if success:
            # 如果成功，添加内容和字符数
            file_data["内容"] = content
            file_data["字符数"] = len(content)
        else:
            # 如果失败，添加错误信息
            file_data["错误信息"] = error_msg

        # 将当前文件的信息添加到"文件"列表中
        output_data["文件"].append(file_data)

    # 将字典保存为 JSON 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)


def get_formatted_time() -> str:
    """
    获取格式化的当前时间

    Returns:
        格式化的时间字符串，例如："2026-01-05 14:30:45"

    知识点：
        - datetime.now()：获取当前时间
        - strftime()：将时间格式化为字符串
        - 格式化符号：
            %Y：四位年份（2026）
            %m：两位月份（01-12）
            %d：两位日期（01-31）
            %H：24小时制小时（00-23）
            %M：分钟（00-59）
            %S：秒（00-59）
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def process_pdfs(input_dir: str, output_format: str = 'markdown', output_name: str = '提取结果') -> int:
    """
    处理 PDF 文件提取的主逻辑

    Args:
        input_dir: 输入文件夹路径
        output_format: 输出格式，可以是 'markdown' 或 'json'，默认为 'markdown'
        output_name: 输出文件名（不含扩展名），默认为 '提取结果'

    Returns:
        int: 0 表示成功，1 表示失败
             这称为"退出码"，用于告诉操作系统程序是否成功执行

    知识点：
        - 函数参数的默认值
        - 条件语句 if-else
        - 字符串的操作（strip, join）
        - 函数的返回值
        - print() 函数的 end 参数
    """
    # ==================== 打印欢迎信息 ====================
    print("=" * 60)  # 打印 60 个等号作为分隔线
    print("          PDF 文本批量提取工具")
    print("=" * 60)
    print()  # 打印空行

    # ==================== 处理输入路径 ====================
    # 去除路径两端可能存在的引号
    # strip() 方法可以删除字符串两端的指定字符
    input_dir = input_dir.strip('"').strip("'")

    # 打印正在扫描的文件夹
    print(f"📁 正在扫描文件夹: {input_dir}")

    # ==================== 获取所有 PDF 文件 ====================
    try:
        # 调用函数获取 PDF 文件列表
        pdf_files = get_pdf_files(input_dir)
    except Exception as e:
        # 如果获取失败，打印错误信息并返回退出码 1（表示失败）
        print(f"❌ 扫描文件夹失败: {e}")
        return 1

    # 检查是否找到了 PDF 文件
    if not pdf_files:
        print("⚠️  未找到任何 PDF 文件")
        return 0  # 虽然没找到文件，但这不算错误，返回 0

    # 显示找到的文件数量
    print(f"✅ 找到 {len(pdf_files)} 个 PDF 文件")
    print()

    # ==================== 提取每个 PDF 的文本 ====================
    # 创建一个空列表，用于存储所有文件的提取结果
    results = []

    # 遍历所有 PDF 文件
    # enumerate() 可以同时获得索引和值，用于显示进度
    for index, pdf_path in enumerate(pdf_files, 1):
        # 获取文件名
        filename = pdf_path.name

        # 显示正在处理的文件
        # end=" " 表示不换行，而是在末尾打印一个空格
        print(f"[{index}/{len(pdf_files)}] 正在处理: {filename}...", end=" ")

        # 调用函数提取文本
        content, success, error_msg = extract_text_from_pdf(pdf_path)

        # 将结果添加到列表中
        results.append((filename, content, success, error_msg))

        if success:
            # 如果成功，显示提取的字符数
            char_count = len(content)
            print(f"✅ 成功 ({char_count} 字符)")
        else:
            # 如果失败，显示错误信息
            print(f"❌ {error_msg}")

    # 所有文件处理完毕
    print()
    print("=" * 60)

    # ==================== 保存结果到文件 ====================
    # 根据输出格式确定文件扩展名
    if output_format == 'json':
        file_ext = '.json'  # JSON 格式
    else:
        file_ext = '.md'    # Markdown 格式（默认）

    # 构建完整的输出文件路径
    # os.path.join() 会根据操作系统自动使用正确的路径分隔符
    # Windows 用 \\，Mac/Linux 用 /
    output_path = os.path.join(input_dir, f"{output_name}{file_ext}")

    print(f"💾 正在保存结果到: {output_path}")

    # 根据格式调用不同的保存函数
    try:
        if output_format == 'json':
            # 保存为 JSON 格式
            save_to_json(results, output_path)
        else:
            # 保存为 Markdown 格式
            save_to_markdown(results, output_path)

        print("✅ 结果保存成功！")
    except Exception as e:
        # 如果保存失败，打印错误信息并返回退出码 1
        print(f"❌ 保存失败: {e}")
        return 1

    # ==================== 显示最终统计 ====================
    # 计算成功和失败的数量
    success_count = sum(1 for _, _, success, _ in results if success)
    fail_count = len(results) - success_count

    # 打印统计信息
    print()
    print("=" * 60)
    print("📊 提取完成统计")
    print("-" * 60)  # 打印 60 个短横线
    print(f"  总文件数: {len(results)}")
    print(f"  成功提取: {success_count}")
    print(f"  提取失败: {fail_count}")
    print("=" * 60)
    print(f"📄 结果文件: {output_path}")
    print()

    # 返回退出码 0 表示成功
    return 0


def parse_arguments() -> argparse.Namespace:
    """
    解析命令行参数

    Returns:
        解析后的参数对象，可以通过 .属性名 访问各个参数的值
        例如：args.input, args.format, args.output

    知识点：
        - argparse：Python 标准库，用于解析命令行参数
        - Namespace：一个简单的对象，用于存储属性
        - 必需参数 vs 可选参数
        - 参数的短选项和长选项
    """
    # 创建 ArgumentParser 对象
    # description：程序的描述信息
    # formatter_class：指定帮助信息的格式
    # epilog：帮助信息末尾显示的额外信息（示例）
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

    # ==================== 添加输入目录参数（必需） ====================
    parser.add_argument(
        '-i',                      # 短选项（简写）
        '--input',                 # 长选项（完整名称）
        type=str,                  # 参数类型为字符串
        required=True,             # 必需参数（必须提供）
        metavar='路径',            # 帮助信息中显示的参数名称占位符
        help='指定要处理的 PDF 文件夹路径（必需）'
    )

    # ==================== 添加输出格式参数（可选） ====================
    parser.add_argument(
        '-f',                      # 短选项
        '--format',                # 长选项
        type=str,                  # 参数类型为字符串
        choices=['markdown', 'json'],  # 限制参数值只能是这两个之一
        default='markdown',        # 默认值（如果不提供此参数）
        metavar='格式',            # 占位符
        help='指定输出格式：markdown 或 json（默认：markdown）'
    )

    # ==================== 添加输出文件名参数（可选） ====================
    parser.add_argument(
        '-o',                      # 短选项
        '--output',                # 长选项
        type=str,                  # 参数类型为字符串
        default='提取结果',         # 默认值
        metavar='文件名',          # 占位符
        help='指定输出文件名（不含扩展名）（默认：提取结果）'
    )

    # 解析命令行参数并返回
    return parser.parse_args()


def main():
    """
    主函数 - 程序的入口点

    这个函数负责：
    1. 解析命令行参数
    2. 调用核心处理逻辑
    3. 返回退出码

    知识点：
        - 程序的执行流程
        - 函数调用
        - 返回值
    """
    # ==================== 第一步：解析命令行参数 ====================
    # 调用 parse_arguments() 函数获取用户提供的参数
    args = parse_arguments()

    # ==================== 第二步：调用核心处理逻辑 ====================
    # 使用用户提供的参数调用处理函数
    # 并返回退出码（0 成功，1 失败）
    return process_pdfs(
        input_dir=args.input,        # 输入文件夹路径
        output_format=args.format,   # 输出格式
        output_name=args.output      # 输出文件名
    )


# ========================================
# 第四部分：程序入口
# ========================================
# 这个特殊的判断：if __name__ == "__main__"
# 作用：确保只有直接运行这个文件时，才会执行下面的代码
# 如果其他程序导入这个文件，下面的代码不会执行

if __name__ == "__main__":
    """
    程序入口 - 当你运行这个脚本时，这里的代码会首先执行

    知识点：
        - __name__：Python 的特殊变量
        - __main__：当文件被直接运行时，__name__ 的值就是 "__main__"
        - try-except-finally：完整的异常处理
        - sys.exit()：退出程序并返回状态码
        - traceback：打印详细的错误信息（用于调试）
    """
    try:
        # 尝试执行主函数
        # sys.exit() 会退出程序，并将返回值传递给操作系统
        # 0 表示成功，非 0 表示失败
        sys.exit(main())

    except KeyboardInterrupt:
        # 捕获用户按 Ctrl+C 的中断操作
        # KeyboardInterrupt 是 KeyboardInterrupt 异常类
        print("\n\n⚠️  用户中断操作")
        sys.exit(1)  # 返回 1 表示程序被中断（非正常退出）

    except Exception as e:
        # 捕获所有其他未预期的错误
        print(f"\n\n❌ 发生未预期的错误: {e}")

        # 导入 traceback 模块
        # traceback.print_exc() 会打印出完整的错误堆栈信息
        # 这对于调试程序非常有用
        import traceback
        traceback.print_exc()

        # 返回 1 表示程序出错退出
        sys.exit(1)


# ========================================
# 学习指南
# ========================================
"""
亲爱的初学者朋友：

如果你是第一次接触这个程序，建议按以下顺序学习：

1. 【理解程序结构】
   - 从 main() 函数开始，这是程序的入口
   - 理解程序的执行流程：解析参数 → 处理文件 → 保存结果

2. 【学习基础语法】
   - 变量和数据类型（字符串、列表、字典、元组）
   - 控制流（if/else、for/while 循环）
   - 函数定义和调用
   - 异常处理（try/except）

3. 【重点函数理解】
   - extract_text_from_pdf()：理解如何提取 PDF 内容
   - save_to_markdown()：理解如何写入文件
   - parse_arguments()：理解如何处理命令行参数

4. 【实践练习】
   - 修改输出格式，调整显示的统计信息
   - 添加新的功能，比如按文件名过滤
   - 修改错误处理，添加更多错误类型

5. 【运行测试】
   在命令行中运行：
   python pdf_extractor_learning.py -h

   查看帮助信息，然后尝试：
   python pdf_extractor_learning.py -i "你的PDF文件夹路径"

记住：编程最好的学习方式就是动手实践！
有问题可以随时查看这些注释，它们会帮助你理解每一行代码的作用。

祝你学习愉快！🎉
"""
