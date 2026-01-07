"""
============================================================
PDF 文本提取器 (增强版) - 详细注释学习版
============================================================
功能：批量提取文件夹中所有 PDF 文件的文本内容
作者：Assistant
日期：2026-01-06

支持类型：
1. 文本型 PDF（直接提取文字）
2. 扫描件 PDF（使用 OCR 识别图片中的文字）

核心特性：
- 智能判断：自动识别 PDF 类型并选择最佳提取方式
- OCR 降级：文本提取失败时自动使用 OCR
- 批量处理：一次处理整个文件夹
- 多种输出：Markdown 和 JSON 格式
"""

# ============================================================
# 第一部分：导入必要的库
# ============================================================

# os, sys: Python 标准库，用于操作系统相关功能
import os          # 操作系统接口，用于文件路径操作
import sys         # 系统相关的参数和函数，例如获取平台信息

# pdfplumber: 第三方库，用于从 PDF 中提取文本
import pdfplumber

# argparse: Python 标准库，用于解析命令行参数
import argparse

# json: Python 标准库，用于 JSON 数据处理
import json

# pathlib: Python 标准库，用于面向对象的文件路径操作
from pathlib import Path

# typing: Python 标准库，用于类型提示（让代码更清晰）
from typing import List, Tuple, Dict, Optional

# datetime: Python 标准库，用于日期和时间处理
from datetime import datetime

# ============================================================
# 第二部分：OCR 相关库的导入（选择性导入）
# ============================================================

"""
为什么要用 try-except？
因为 OCR 库可能没有安装，如果直接导入会报错。
使用 try-exatch 可以让程序在没有 OCR 的情况下也能运行（只是没有 OCR 功能）。
"""

try:
    # pdf2image: 将 PDF 转换为图片（OCR 前的必要步骤）
    from pdf2image import convert_from_path

    # pytesseract: Python 的 Tesseract OCR 接口，用于图片文字识别
    import pytesseract

    # 如果导入成功，设置 OCR 可用标志为 True
    OCR_AVAILABLE = True

except ImportError:
    # 如果导入失败（库未安装），设置标志为 False
    OCR_AVAILABLE = False

    # 提示用户安装缺失的库
    print("[WARNING] OCR功能不可用：未安装 pdf2image 或 pytesseract")
    print("   请运行: pip install pdf2image pytesseract pillow")

# ============================================================
# 第三部分：Windows 控制台编码修复
# ============================================================

"""
为什么要设置编码？
Windows 的命令行默认使用 GBK 编码，不支持中文和一些特殊字符。
这里强制使用 UTF-8 编码输出，避免乱码。
"""

# sys.platform 返回操作系统类型
# 'win32' 表示 Windows 系统
if sys.platform == 'win32':
    import codecs  # 编码转换库

    # 将标准输出（stdout）设置为 UTF-8 编码
    # sys.stdout.buffer: 原始的输出流（二进制）
    # codecs.getwriter('utf-8'): 创建一个 UTF-8 编码写入器
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

    # 将标准错误输出（stderr）也设置为 UTF-8 编码
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# ============================================================
# 第四部分：辅助函数 - 获取 PDF 文件列表
# ============================================================

def get_pdf_files(folder_path: str) -> List[Path]:
    """
    获取指定文件夹中的所有 PDF 文件

    参数:
        folder_path (str): 文件夹路径，例如 "C:\\Documents\\PDFs"

    返回:
        List[Path]: PDF 文件路径对象的排序列表

    抛出异常:
        FileNotFoundError: 文件夹不存在
        NotADirectoryError: 路径不是文件夹
    """
    # 将字符串路径转换为 Path 对象（Path 提供更方便的路径操作方法）
    folder = Path(folder_path)

    # 检查文件夹是否存在
    if not folder.exists():
        raise FileNotFoundError(f"文件夹不存在: {folder_path}")

    # 检查路径是否真的是文件夹（而不是文件）
    if not folder.is_dir():
        raise NotADirectoryError(f"路径不是文件夹: {folder_path}")

    """
    Path.glob(pattern): 查找匹配模式的所有文件
    "*.pdf": 匹配所有小写的 .pdf 文件
    "*.PDF": 匹配所有大写的 .PDF 文件
    set(): 转换为集合（自动去重）
    |: 集合的并集操作（合并两组结果）
    sorted(): 排序，让文件按字母顺序排列
    """
    pdf_files = set(folder.glob("*.pdf")) | set(folder.glob("*.PDF"))

    # 返回排序后的 PDF 文件列表
    return sorted(pdf_files)


# ============================================================
# 第五部分：核心函数 - OCR 文本提取
# ============================================================

def extract_text_with_ocr(pdf_path: Path, lang: str = 'chi_sim+eng') -> Tuple[str, bool, str]:
    """
    使用 OCR 技术提取扫描件 PDF 的文本

    工作流程：
    1. 将 PDF 转换为图片
    2. 对每一页图片进行 OCR 识别
    3. 提取识别出的文字

    参数:
        pdf_path (Path): PDF 文件的路径对象
        lang (str): OCR 语言设置
            - 'chi_sim+eng': 中英文混合（默认）
            - 'chi_sim': 仅中文
            - 'eng': 仅英文

    返回:
        Tuple[str, bool, str]: 包含三个元素的元组
            - [0] 提取的文本内容
            - [1] 是否成功 (True/False)
            - [2] 提取方式说明或错误信息
    """

    # 检查 OCR 功能是否可用
    if not OCR_AVAILABLE:
        return "", False, "OCR功能未安装"

    try:
        """
        ========================================
        步骤 1: 配置工具路径（Windows 系统）
        ========================================
        """
        import platform  # 用于获取操作系统信息

        poppler_path = None  # 默认为空（非 Windows 系统）

        # 判断是否为 Windows 系统
        if platform.system() == 'Windows':
            # 设置 Poppler 路径（PDF 转图片工具）
            poppler_path = r'C:\Users\flyskyson\poppler\Library\bin'

            # 设置 Tesseract 可执行文件路径（OCR 引擎）
            # pytesseract 需要知道 tesseract.exe 在哪里
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

            # 设置 Tesseract 语言包路径
            # Tesseract 需要知道 .traineddata 语言文件在哪里
            # os.environ: 访问和修改环境变量
            os.environ['TESSDATA_PREFIX'] = r'C:\Users\flyskyson\Downloads'

        """
        ========================================
        步骤 2: 将 PDF 转换为图片
        ========================================
        convert_from_path 参数说明：
        - pdf_path: PDF 文件路径
        - dpi=200: 分辨率（每英寸点数）
            * 200: 平衡速度和精度（推荐）
            * 300: 更高精度，速度较慢
            * 150: 更快速度，精度略低
        - poppler_path: Poppler 工具的路径
        """
        images = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)

        # 检查是否成功转换为图片
        if not images:
            return "", False, "PDF转换为图片失败"

        """
        ========================================
        步骤 3: 对每一页图片进行 OCR 识别
        ========================================
        """
        all_text = []  # 存储所有页面的文字

        # 显示进度信息
        # end="": 不换行
        # flush=True: 立即输出（不缓冲）
        print(f"   正在OCR识别 {len(images)} 页...", end="", flush=True)

        # enumerate(images, 1): 遍历图片列表，从 1 开始计数
        # i: 页码（1, 2, 3...）
        # image: 图片对象
        for i, image in enumerate(images, 1):
            try:
                """
                pytesseract.image_to_string 参数说明：
                - image: PIL 图片对象
                - lang: 识别语言
                    * 'chi_sim+eng': 同时识别中文和英文
                """
                text = pytesseract.image_to_string(image, lang=lang)

                # 检查是否识别到文字
                # text.strip(): 去除首尾空白字符
                if text.strip():
                    # 识别成功，添加到列表
                    all_text.append(f"--- 第 {i} 页 (OCR识别) ---\n{text.strip()}")
                else:
                    # 这一页是空白页或识别失败
                    all_text.append(f"--- 第 {i} 页 (OCR识别) ---\n[OCR未识别到文字]")

            except Exception as e:
                # 某一页识别失败，记录错误但继续处理其他页
                all_text.append(f"--- 第 {i} 页 (OCR识别) ---\n[OCR识别失败: {str(e)}]")
                continue

        # OCR 完成，显示成功提示
        print("[OK]")

        # 检查是否提取到任何文字
        if not all_text:
            return "", False, "OCR未识别到任何文字"

        """
        ========================================
        步骤 4: 合并所有页面的文字
        ========================================
        "\n\n".join(all_text): 用两个换行符连接所有页面
        结果格式：
            第1页内容

            第2页内容

            第3页内容
        """
        return "\n\n".join(all_text), True, "(通过OCR识别)"

    except Exception as e:
        """
        ========================================
        步骤 5: 错误处理
        ========================================
        """
        error_msg = str(e)

        # 根据错误信息判断具体问题
        if "tesseract is not installed" in error_msg.lower():
            return "", False, "Tesseract-OCR引擎未安装或路径未配置"
        elif "Unable to locate poppler" in error_msg:
            return "", False, "未找到poppler工具（pdf2image依赖）"
        else:
            return "", False, f"OCR处理失败: {error_msg}"


# ============================================================
# 第六部分：核心函数 - 智能文本提取（含 OCR 降级）
# ============================================================

def extract_text_from_pdf(pdf_path: Path,
                         use_ocr_threshold: int = 50,
                         force_ocr: bool = False) -> Tuple[str, bool, str]:
    """
    智能 PDF 文本提取：优先文本提取，失败则自动降级为 OCR

    工作流程：
    1. 如果强制 OCR 模式 → 直接使用 OCR
    2. 否则，先尝试文本提取（快速）
    3. 如果文本太少 → 使用 OCR 重新识别
    4. 如果文本提取失败 → 使用 OCR 降级

    参数:
        pdf_path (Path): PDF 文件路径
        use_ocr_threshold (int): OCR 触发阈值（字符数）
            - 默认 50：如果提取的文本少于 50 字符，尝试 OCR
            - 设置为 0：禁用自动 OCR
        force_ocr (bool): 是否强制使用 OCR
            - True: 跳过文本提取，直接用 OCR
            - False: 先尝试文本提取（默认）

    返回:
        Tuple[str, bool, str]: (文本内容, 是否成功, 提取方式说明)
    """

    """
    ========================================
    场景 1: 强制 OCR 模式
    ========================================
    如果用户指定 --force-ocr 参数，直接使用 OCR，跳过文本提取
    适用场景：纯扫描件 PDF
    """
    if force_ocr:
        if not OCR_AVAILABLE:
            return "", False, "强制OCR但OCR功能不可用"
        return extract_text_with_ocr(pdf_path)

    """
    ========================================
    场景 2: 标准文本提取（优先尝试）
    ========================================
    pdfplumber: 可以直接从 PDF 中提取文本（不需要 OCR）
    优点：速度快，准确率高
    缺点：对扫描件无效（扫描件是图片，没有文本层）
    """
    try:
        # 打开 PDF 文件
        # with 语句会自动关闭文件（即使出错）
        with pdfplumber.open(pdf_path) as pdf:

            all_text = []     # 存储所有页面的文本
            total_chars = 0   # 统计总字符数

            # 遍历 PDF 的每一页
            # enumerate(pdf.pages, 1): 从第 1 页开始计数
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    # 提取当前页的文本
                    text = page.extract_text()

                    # 检查是否提取到文本
                    if text and text.strip():
                        # 有文本，保存并统计字符数
                        page_text = f"--- 第 {page_num} 页 ---\n{text.strip()}"
                        all_text.append(page_text)
                        total_chars += len(text.strip())
                    else:
                        # 这一页是空白页（可能是扫描件）
                        all_text.append(f"--- 第 {page_num} 页 ---\n[此页无文本内容]")

                except Exception as e:
                    # 某一页提取失败，记录错误
                    all_text.append(f"--- 第 {page_num} 页 ---\n[页面提取失败: {str(e)}]")
                    continue

            # 合并所有页面的文本
            full_text = "\n\n".join(all_text)

            """
            ========================================
            场景 3: 智能判断 - 是否需要 OCR？
            ========================================
            判断条件（满足任一即触发 OCR）：
            1. 总字符数 < 阈值（默认 50）
            2. 超过一半的页面是空白页

            示例：
            - 5 页 PDF，提取了 10 个字符 → 触发 OCR（太少）
            - 5 页 PDF，3 页是空白 → 触发 OCR（60% 空白）
            """
            # 统计空白页数量
            empty_pages = sum(1 for t in all_text if "[此页无文本内容]" in t or "[页面提取失败]" in t)
            total_pages = len(pdf.pages)

            # 判断是否需要 OCR
            need_ocr = (total_chars < use_ocr_threshold) or (empty_pages / total_pages > 0.5)

            # 如果需要 OCR 且 OCR 功能可用
            if need_ocr and OCR_AVAILABLE and total_pages > 0:
                print(f"  文本过少({total_chars}字符)，尝试OCR...", end="", flush=True)

                # 使用 OCR 重新识别
                ocr_text, ocr_success, ocr_msg = extract_text_with_ocr(pdf_path)

                # 比较：OCR 结果是否更好？
                if ocr_success and len(ocr_text.strip()) > total_chars:
                    # OCR 识别到更多文字，使用 OCR 结果
                    print("[OK] (使用OCR结果)")
                    return ocr_text, True, f"(智能降级OCR: {ocr_msg})"
                else:
                    # OCR 没有更好，保留原文本提取结果
                    print("[WARNING] (OCR未获得更好结果，保留原提取)")

            # 返回文本提取结果
            if total_chars > 0:
                return full_text, True, f"(文本提取, {total_chars}字符)"
            else:
                return full_text, False, "未提取到有效文本"

    except Exception as e:
        """
        ========================================
        场景 4: 文本提取完全失败，OCR 降级
        ========================================
        """
        error_msg = str(e)

        # 尝试使用 OCR 作为最后的手段
        if OCR_AVAILABLE:
            print(f"  文本提取失败，尝试OCR...", end="", flush=True)
            ocr_text, ocr_success, ocr_msg = extract_text_with_ocr(pdf_path)

            if ocr_success:
                print("[OK]")
                return ocr_text, True, f"(降级OCR: {ocr_msg})"
            else:
                print("[FAILED]")

        # 根据错误信息判断问题类型
        if "encrypted" in error_msg.lower():
            return "", False, "PDF文件已加密"
        elif "damaged" in error_msg.lower():
            return "", False, "PDF文件损坏"
        else:
            return "", False, f"读取失败: {error_msg}"


# ============================================================
# 第七部分：保存函数 - Markdown 格式
# ============================================================

def save_to_markdown(results: List[Tuple[str, str, bool, str]], output_path: str) -> None:
    """
    将提取结果保存到 Markdown 文件

    参数:
        results: 提取结果列表
            每个元素是一个元组: (文件名, 内容, 是否成功, 提取方式)
        output_path: 输出文件路径

    返回:
        None（直接写入文件）
    """
    # 打开文件（自动创建，如果存在则覆盖）
    # encoding='utf-8': 使用 UTF-8 编码（支持中文）
    with open(output_path, 'w', encoding='utf-8') as f:
        # 写入文件标题
        f.write("# PDF 文本提取结果（增强版）\n\n")

        # 写入提取时间
        # datetime.now(): 获取当前时间
        # strftime(): 格式化时间为字符串
        f.write(f"**提取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        """
        ========================================
        统计信息
        ========================================
        """
        # 统计成功提取的文件数量
        # results 是一个列表，每个元素是 (文件名, 内容, 是否成功, 提取方式)
        # success 是元组的第 3 个元素（索引 2）
        success_count = sum(1 for _, _, success, _ in results if success)

        # 统计使用 OCR 的文件数量
        # method 是元组的第 4 个元素（索引 3）
        # "OCR" in method: 检查提取方式说明中是否包含 "OCR"
        ocr_count = sum(1 for _, _, _, method in results if "OCR" in method)

        # 写入统计信息
        f.write("## 提取统计\n\n")
        f.write(f"- 总文件数: {len(results)}\n")
        f.write(f"- 成功提取: {success_count}\n")
        f.write(f"- 使用OCR: {ocr_count} 个文件\n")
        f.write(f"- 提取失败: {len(results) - success_count}\n\n")
        f.write("---\n\n")

        """
        ========================================
        每个文件的详细结果
        ========================================
        """
        for filename, content, success, method in results:
            # 写入文件名作为二级标题
            f.write(f"## {filename}\n\n")

            # 写入提取方式
            f.write(f"**提取方式**: {method}\n\n")

            if success:
                # 提取成功，写入内容
                f.write(content)
            else:
                # 提取失败，写入错误信息
                f.write(f"[WARNING] **提取失败**: {content if content else method}")

            # 写入分隔线（区分不同文件）
            f.write("\n\n---\n\n")


# ============================================================
# 第八部分：保存函数 - JSON 格式
# ============================================================

def save_to_json(results: List[Tuple[str, str, bool, str]], output_path: str) -> None:
    """
    将提取结果保存到 JSON 文件

    JSON 格式优点：
    - 结构化数据，便于程序处理
    - 可以直接用 Python、JavaScript 等语言读取
    - 支持嵌套数据结构

    参数:
        results: 提取结果列表
        output_path: 输出文件路径
    """
    # 统计信息（与 Markdown 版本相同）
    success_count = sum(1 for _, _, success, _ in results if success)
    ocr_count = sum(1 for _, _, _, method in results if "OCR" in method)

    # 构建输出数据结构（字典）
    output_data = {
        "提取时间": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "统计": {
            "总文件数": len(results),
            "成功提取": success_count,
            "使用OCR的文件数": ocr_count,
            "提取失败": len(results) - success_count
        },
        "文件": []  # 空列表，稍后填充
    }

    # 遍历每个文件的结果，添加到 "文件" 列表中
    for filename, content, success, method in results:
        # 构建单个文件的数据
        file_data = {
            "文件名": filename,
            "提取方式": method,
            "状态": "成功" if success else "失败"
        }

        if success:
            # 提取成功，添加内容和统计信息
            file_data["内容"] = content
            file_data["字符数"] = len(content)
            file_data["是否OCR"] = "OCR" in method
        else:
            # 提取失败，记录错误信息
            file_data["错误信息"] = content if content else method

        # 将当前文件数据添加到总列表中
        output_data["文件"].append(file_data)

    # 写入 JSON 文件
    # json.dump(): 将 Python 对象转换为 JSON 格式并写入文件
    # ensure_ascii=False: 支持中文（不转义为 Unicode）
    # indent=2: 缩进 2 个空格（美化格式）
    # separators=(',', ': '): 使用紧凑的分隔符
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2, separators=(',', ': '))


# ============================================================
# 第九部分：主处理函数
# ============================================================

def process_pdfs(input_dir: str,
                output_format: str = 'markdown',
                output_name: str = '提取结果',
                ocr_threshold: int = 50,
                force_ocr: bool = False) -> int:
    """
    处理 PDF 文件提取的主逻辑

    这是整个程序的核心函数，协调所有其他函数完成以下任务：
    1. 扫描文件夹找到所有 PDF
    2. 逐个处理 PDF 文件
    3. 保存提取结果
    4. 显示统计信息

    参数:
        input_dir (str): 输入文件夹路径
        output_format (str): 输出格式 ('markdown' 或 'json')
        output_name (str): 输出文件名（不含扩展名）
        ocr_threshold (int): OCR 触发阈值
        force_ocr (bool): 是否强制使用 OCR

    返回:
        int: 退出码
            - 0: 成功
            - 1: 失败
    """

    """
    ========================================
    步骤 1: 显示欢迎信息和配置
    ========================================
    """
    print("=" * 60)
    print("       PDF 文本批量提取工具 (增强OCR版)")
    print("=" * 60)
    print(f"[FOLDER] 扫描文件夹: {input_dir}")

    # 显示当前运行模式
    if force_ocr:
        print("[MODE] 模式: 强制使用OCR")
    elif ocr_threshold > 0:
        print(f"[MODE] 模式: 智能降级 (阈值: {ocr_threshold}字符)")

    # 检查 OCR 功能是否可用
    if not OCR_AVAILABLE and (force_ocr or ocr_threshold > 0):
        print("[WARNING] 警告: OCR功能不可用，将仅使用文本提取")

    """
    ========================================
    步骤 2: 扫描文件夹，查找 PDF 文件
    ========================================
    """
    try:
        pdf_files = get_pdf_files(input_dir)
    except Exception as e:
        print(f"[ERROR] 扫描失败: {e}")
        return 1  # 返回错误码

    # 检查是否找到 PDF 文件
    if not pdf_files:
        print("[WARNING] 未找到PDF文件")
        return 0  # 不是错误，只是没有文件

    print(f"[OK] 找到 {len(pdf_files)} 个PDF文件")
    print()

    """
    ========================================
    步骤 3: 逐个处理 PDF 文件
    ========================================
    """
    results = []  # 存储所有文件的提取结果

    # enumerate(pdf_files, 1): 从 1 开始计数
    # index: 当前处理第几个文件（1, 2, 3...）
    # pdf_path: PDF 文件的路径对象
    for index, pdf_path in enumerate(pdf_files, 1):
        filename = pdf_path.name  # 获取文件名（不含路径）

        # 显示当前进度
        # end="": 不换行（后续会追加结果）
        print(f"[{index}/{len(pdf_files)}] {filename}", end=" ")

        # 调用提取函数
        content, success, method = extract_text_from_pdf(
            pdf_path,
            use_ocr_threshold=ocr_threshold,
            force_ocr=force_ocr
        )

        # 保存结果到列表
        results.append((filename, content, success, method))

        # 显示处理结果
        if success:
            char_count = len(content)
            print(f"[OK] {method}")
        else:
            print(f"[FAILED] {method}")

    print("\n" + "=" * 60)

    """
    ========================================
    步骤 4: 保存结果到文件
    ========================================
    """
    # 确定文件扩展名
    file_ext = '.json' if output_format == 'json' else '.md'

    # 构建完整输出路径
    # os.path.join(): 拼接路径（自动处理分隔符）
    output_path = os.path.join(input_dir, f"{output_name}{file_ext}")

    print(f"[SAVE] 保存到: {output_path}")

    try:
        # 根据格式选择保存函数
        if output_format == 'json':
            save_to_json(results, output_path)
        else:
            save_to_markdown(results, output_path)

        print("[OK] 保存成功")
    except Exception as e:
        print(f"[ERROR] 保存失败: {e}")
        return 1  # 返回错误码

    """
    ========================================
    步骤 5: 显示最终统计
    ========================================
    """
    success_count = sum(1 for _, _, success, _ in results if success)
    ocr_count = sum(1 for _, _, _, method in results if "OCR" in method)

    print("\n" + "=" * 60)
    print("[STATS] 最终统计")
    print("-" * 60)
    print(f"  总文件数: {len(results)}")
    print(f"  成功提取: {success_count}")
    print(f"  使用OCR: {ocr_count}")
    print(f"  提取失败: {len(results) - success_count}")
    print("=" * 60)

    # 返回成功码
    return 0


# ============================================================
# 第十部分：命令行参数解析
# ============================================================

def parse_arguments() -> argparse.Namespace:
    """
    解析命令行参数

    argparse 是 Python 标准库，用于处理命令行参数

    返回:
        argparse.Namespace: 包含所有参数的对象
    """
    # 创建参数解析器
    parser = argparse.ArgumentParser(
        description='PDF文本批量提取工具 (增强OCR版) - 支持文本型和扫描件PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s -i "C:\\PDF文件夹"                    # 智能模式(默认)
  %(prog)s -i ./pdfs --ocr-threshold 30         # 调低OCR触发阈值
  %(prog)s -i ./pdfs --force-ocr                # 强制使用OCR(处理纯扫描件)
  %(prog)s -i "./我的PDF" -f json -o 结果       # 输出JSON格式
  %(prog)s --input ./扫描件 --force-ocr --format markdown

OCR配置说明:
  • 智能模式: 文本<阈值字符时自动使用OCR (默认阈值:50)
  • 强制OCR: 跳过文本提取，直接使用OCR
  • 如OCR失败，请确保已安装 Tesseract-OCR 和中文语言包
        '''
    )

    """
    ========================================
    必需参数
    ========================================
    """
    parser.add_argument('-i', '--input', required=True,
                       help='PDF文件夹路径 (必需)')

    """
    ========================================
    输出参数（可选）
    ========================================
    """
    # choices: 限定选项只能是 'markdown' 或 'json'
    parser.add_argument('-f', '--format', choices=['markdown', 'json'],
                       default='markdown', help='输出格式 (默认: markdown)')

    parser.add_argument('-o', '--output', default='提取结果',
                       help='输出文件名，不含扩展名 (默认: 提取结果)')

    """
    ========================================
    OCR 相关参数（可选）
    ========================================
    """
    # type=int: 参数类型为整数
    parser.add_argument('--ocr-threshold', type=int, default=50,
                       help='OCR触发阈值(字符数)，低于此值则尝试OCR (默认: 50，0=禁用OCR)')

    # action='store_true': 布尔开关，存在即为 True，不存在为 False
    parser.add_argument('--force-ocr', action='store_true',
                       help='强制使用OCR，跳过文本提取尝试')

    # 解析参数并返回
    return parser.parse_args()


# ============================================================
# 第十一部分：主函数入口
# ============================================================

def main():
    """
    主函数 - 程序的入口点

    工作流程：
    1. 解析命令行参数
    2. 调用主处理函数
    3. 返回退出码
    """
    # 解析命令行参数
    args = parse_arguments()

    # 清理输入路径（去除首尾的引号）
    input_dir = args.input.strip('"').strip("'")

    # 调用主处理函数
    return process_pdfs(
        input_dir=input_dir,
        output_format=args.format,
        output_name=args.output,
        ocr_threshold=args.ocr_threshold,
        force_ocr=args.force_ocr
    )


# ============================================================
# 第十二部分：程序入口
# ============================================================

if __name__ == "__main__":
    """
    Python 程序的标准入口写法

    __name__: Python 的特殊变量
    - 如果直接运行此脚本（python script.py），__name__ == "__main__"
    - 如果被其他脚本导入（import script），__name__ == "script"

    这样设计的好处：
    - 脚本可以独立运行
    - 也可以被其他脚本导入使用（不会自动运行）
    """
    try:
        # 运行主函数，并返回退出码
        # sys.exit(0): 正常退出
        # sys.exit(1): 错误退出
        sys.exit(main())

    except KeyboardInterrupt:
        # 用户按 Ctrl+C 中断程序
        print("\n\n[WARNING] 用户中断操作")
        sys.exit(1)

    except Exception as e:
        # 程序运行出错
        print(f"\n\n[ERROR] 错误: {e}")

        # 打印详细的错误堆栈（用于调试）
        import traceback
        traceback.print_exc()

        sys.exit(1)


# ============================================================
# 学习提示
# ============================================================

"""
初学者学习路径建议：

第一阶段：理解基本概念
1. 学习 Python 基础语法（变量、函数、循环、条件）
2. 学习文件操作（open, read, write）
3. 学习异常处理（try-except）

第二阶段：理解模块化
1. 理解函数的定义和调用
2. 理解参数传递（位置参数、关键字参数、默认值）
3. 理解返回值（return）

第三阶段：理解库的使用
1. 学习 pathlib（路径操作）
2. 学习 argparse（命令行参数）
3. 学习 pdfplumber 和 pdf2image（PDF 处理）

第四阶段：实践项目
1. 修改脚本，添加新功能（例如：进度条）
2. 优化错误处理（更友好的错误提示）
3. 添加日志记录（记录处理过程）

推荐资源：
- Python 官方文档: https://docs.python.org/zh-cn/3/
- 廖雪峰 Python 教程: https://www.liaoxuefeng.com/wiki/1016959663602400
- 菜鸟教程 Python: https://www.runoob.com/python
"""
