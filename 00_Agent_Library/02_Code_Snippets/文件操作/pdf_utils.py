"""
PDF 文本提取工具模块

本模块提供从 PDF 文件中提取文本内容的函数。

依赖:
    - pdfplumber: pip install pdfplumber

主要功能:
    - extract_text_from_pdf(): 提取单个 PDF 文件的文本内容

示例:
    >>> from pathlib import Path
    >>> from pdf_utils import extract_text_from_pdf
    >>>
    >>> pdf_path = Path("example.pdf")
    >>> text, success, error = extract_text_from_pdf(pdf_path)
    >>>
    >>> if success:
    ...     print(f"提取成功！共 {len(text)} 个字符")
    ... else:
    ...     print(f"提取失败: {error}")
"""

from pathlib import Path
from typing import Tuple, Optional
import pdfplumber


def extract_text_from_pdf(
    pdf_path: Path,
    keep_page_markers: bool = True,
    extract_empty_pages: bool = True
) -> Tuple[str, bool, str]:
    """
    从单个 PDF 文件中提取所有页面的文本内容

    本函数会逐页提取 PDF 文本，保留页码信息，并自动处理常见错误。

    Args:
        pdf_path (Path): PDF 文件的路径对象
            - 支持绝对路径和相对路径
            - 例如: Path("C:/Documents/file.pdf") 或 Path("./file.pdf")

        keep_page_markers (bool): 是否在文本中保留页码标记，默认为 True
            - True: 每页文本前添加 "--- 第 N 页 ---" 标记
            - False: 只返回纯文本，不添加页码标记

        extract_empty_pages (bool): 是否为空页面添加占位文本，默认为 True
            - True: 空页面显示 "[此页无文本内容，可能是图片或扫描件]"
            - False: 空页面返回空字符串

    Returns:
        Tuple[str, bool, str]: 返回一个包含三个元素的元组

        - 元素 0 (str): 提取的文本内容
            * 成功时: 包含所有页面的文本，页面之间用 "\\n\\n" 分隔
            * 失败时: 空字符串 ""

        - 元素 1 (bool): 提取是否成功
            * True: 文本提取成功
            * False: 提取失败（加密、损坏等）

        - 元素 2 (str): 错误信息
            * 成功时: 空字符串 ""
            * 失败时: 具体的错误描述

    返回值示例:
        成功: ("完整的文本内容...", True, "")
        失败: ("", False, "PDF 文件已加密，需要密码")

    错误类型:
        - "PDF 文件已加密，需要密码": 文件有密码保护
        - "PDF 文件已损坏": 文件结构损坏
        - "读取失败: <具体错误>": 其他读取错误

    Raises:
        无异常抛出，所有错误都通过返回值传递

    使用示例:
        >>> # 基本用法
        >>> pdf_path = Path("report.pdf")
        >>> text, success, error = extract_text_from_pdf(pdf_path)
        >>>
        >>> if success:
        ...     print(text)
        ...     print(f"字符数: {len(text)}")
        ... else:
        ...     print(f"错误: {error}")

        >>> # 不保留页码标记
        >>> text, success, error = extract_text_from_pdf(
        ...     pdf_path,
        ...     keep_page_markers=False
        ... )

        >>> # 批量处理
        >>> from pathlib import Path
        >>>
        >>> results = []
        >>> for pdf_file in Path("pdfs").glob("*.pdf"):
        ...     text, success, error = extract_text_from_pdf(pdf_file)
        ...     if success:
        ...         results.append((pdf_file.name, text))
        ...     else:
        ...         print(f"⚠️ {pdf_file.name}: {error}")

    注意事项:
        1. 此函数无法提取扫描件或图片型 PDF 的文本
        2. 加密 PDF 需要先解密才能提取
        3. 大型 PDF 文件可能需要较长的处理时间
        4. 确保已安装 pdfplumber: pip install pdfplumber

    相关函数:
        - 如需批量提取，建议配合 Path.glob() 使用
        - 如需保存结果，可使用 save_to_markdown() 或 save_to_json()
    """
    try:
        # 使用 pdfplumber 打开 PDF 文件
        with pdfplumber.open(pdf_path) as pdf:
            all_text = []

            # 逐页提取文本
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    # 提取当前页的文本
                    text = page.extract_text()

                    # 处理提取的文本
                    if text:
                        # 有文本内容
                        if keep_page_markers:
                            all_text.append(f"--- 第 {page_num} 页 ---\n{text}")
                        else:
                            all_text.append(text)
                    else:
                        # 无文本内容（可能是图片或扫描件）
                        if extract_empty_pages:
                            if keep_page_markers:
                                all_text.append(
                                    f"--- 第 {page_num} 页 ---\n"
                                    f"[此页无文本内容，可能是图片或扫描件]"
                                )
                            else:
                                all_text.append("[此页无文本内容，可能是图片或扫描件]")
                        # 如果 extract_empty_pages=False，不添加任何内容

                except Exception as e:
                    # 单页提取失败，记录错误但继续处理其他页
                    error_msg = f"[第 {page_num} 页提取失败: {str(e)}]"
                    if keep_page_markers:
                        all_text.append(f"--- 第 {page_num} 页 ---\n{error_msg}")
                    else:
                        all_text.append(error_msg)
                    continue

            # 合并所有页面文本，用两个换行符分隔
            full_text = "\n\n".join(all_text)
            return full_text, True, ""

    except Exception as e:
        # PDF 文件级别的错误处理
        error_msg = str(e)

        # 识别常见错误类型并返回友好提示
        error_lower = error_msg.lower()

        if "encrypted" in error_lower or "password" in error_lower:
            return "", False, "PDF 文件已加密，需要密码"

        elif "damaged" in error_lower or "corrupt" in error_lower:
            return "", False, "PDF 文件已损坏"

        elif "not found" in error_lower or "no such file" in error_lower:
            return "", False, f"文件不存在: {pdf_path}"

        elif "permission" in error_lower:
            return "", False, f"没有文件读取权限: {pdf_path}"

        else:
            # 其他未知错误，返回原始错误信息
            return "", False, f"读取失败: {error_msg}"


# 为了方便使用，提供一个简单的别名
extract_pdf = extract_text_from_pdf


# 如果直接运行此模块，执行示例代码
if __name__ == "__main__":
    """
    模块测试代码

    运行此模块时会执行简单的功能测试
    """
    from pathlib import Path

    print("=" * 60)
    print("PDF 文本提取模块测试")
    print("=" * 60)
    print()

    # 测试 1: 检查依赖
    print("检查依赖...")
    try:
        import pdfplumber
        print("✅ pdfplumber 已安装")
    except ImportError:
        print("❌ 请先安装 pdfplumber: pip install pdfplumber")
        exit(1)

    print()

    # 测试 2: 提示用户输入文件路径
    print("请输入要测试的 PDF 文件路径（留空跳过测试）")
    user_input = input("PDF 文件路径: ").strip()

    if not user_input:
        print("\n⚠️ 未提供文件，跳过测试")
        print("\n使用示例:")
        print("  from pdf_utils import extract_text_from_pdf")
        print('  text, success, error = extract_text_from_pdf(Path("file.pdf"))')
        exit(0)

    # 测试 3: 尝试提取文本
    pdf_path = Path(user_input)

    if not pdf_path.exists():
        print(f"\n❌ 文件不存在: {pdf_path}")
        exit(1)

    print(f"\n正在提取文本: {pdf_path.name}")
    print("-" * 60)

    text, success, error = extract_text_from_pdf(pdf_path)

    if success:
        print(f"✅ 提取成功！")
        print(f"   总字符数: {len(text)}")
        print(f"   总页数估算: {text.count('--- 第')}")
        print()
        print("前 200 个字符预览:")
        print("-" * 60)
        print(text[:200])
        if len(text) > 200:
            print("...")
        print("-" * 60)
    else:
        print(f"❌ 提取失败: {error}")

    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)
