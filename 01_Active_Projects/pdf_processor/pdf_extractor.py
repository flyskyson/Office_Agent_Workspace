"""
PDF 文本提取器 (增强版)
功能：批量提取文件夹中所有 PDF 文件的文本内容，支持文本型和扫描件
新增：智能OCR降级功能，自动处理扫描件PDF
"""

import os
import sys
import pdfplumber
import argparse
import json
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from datetime import datetime

# OCR相关库（选择性导入，避免未安装时崩溃）
try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("[WARNING] OCR功能不可用：未安装 pdf2image 或 pytesseract")
    print("   请运行: pip install pdf2image pytesseract pillow")

# Windows 控制台编码支持
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def get_pdf_files(folder_path: str) -> List[Path]:
    """获取指定文件夹中的所有 PDF 文件"""
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"文件夹不存在: {folder_path}")

    if not folder.is_dir():
        raise NotADirectoryError(f"路径不是文件夹: {folder_path}")

    pdf_files = set(folder.glob("*.pdf")) | set(folder.glob("*.PDF"))
    return sorted(pdf_files)


def extract_text_with_ocr(pdf_path: Path, lang: str = 'chi_sim+eng') -> Tuple[str, bool, str]:
    """
    使用OCR技术提取扫描件PDF的文本

    Args:
        pdf_path: PDF文件路径
        lang: OCR语言设置，'chi_sim+eng'支持中英文混合识别

    Returns:
        (提取的文本内容, 是否成功, 错误信息)
    """
    if not OCR_AVAILABLE:
        return "", False, "OCR功能未安装"

    try:
        # 指定 poppler 路径 (Windows)
        import platform
        poppler_path = None
        if platform.system() == 'Windows':
            poppler_path = r'C:\Users\flyskyson\poppler\Library\bin'
            # 指定 tesseract 路径 (Windows)
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            # 设置 TESSDATA_PREFIX 环境变量指向语言包目录
            os.environ['TESSDATA_PREFIX'] = r'C:\Users\flyskyson\Downloads'

        # 将PDF转换为图片列表
        images = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)  # dpi越高识别越准，但越慢
        
        if not images:
            return "", False, "PDF转换为图片失败"
        
        all_text = []
        print(f"   正在OCR识别 {len(images)} 页...", end="", flush=True)
        
        for i, image in enumerate(images, 1):
            try:
                # 进行OCR识别
                text = pytesseract.image_to_string(image, lang=lang)
                if text.strip():
                    all_text.append(f"--- 第 {i} 页 (OCR识别) ---\n{text.strip()}")
                else:
                    all_text.append(f"--- 第 {i} 页 (OCR识别) ---\n[OCR未识别到文字]")
            except Exception as e:
                all_text.append(f"--- 第 {i} 页 (OCR识别) ---\n[OCR识别失败: {str(e)}]")
                continue
        
        print("[OK]")  # OCR进度完成
        
        if not all_text:
            return "", False, "OCR未识别到任何文字"
        
        return "\n\n".join(all_text), True, "(通过OCR识别)"
        
    except Exception as e:
        error_msg = str(e)
        if "tesseract is not installed" in error_msg.lower():
            return "", False, "Tesseract-OCR引擎未安装或路径未配置"
        elif "Unable to locate poppler" in error_msg:
            return "", False, "未找到poppler工具（pdf2image依赖）"
        else:
            return "", False, f"OCR处理失败: {error_msg}"


def extract_text_from_pdf(pdf_path: Path, 
                         use_ocr_threshold: int = 50,
                         force_ocr: bool = False) -> Tuple[str, bool, str]:
    """
    智能PDF文本提取：优先文本提取，失败则自动降级为OCR
    
    Args:
        pdf_path: PDF文件路径
        use_ocr_threshold: 文本长度阈值，低于此值则尝试OCR（默认50字符）
        force_ocr: 强制使用OCR，跳过文本提取尝试
    
    Returns:
        (提取的文本内容, 是否成功, 提取方式说明)
    """
    # 如果强制使用OCR或用户明确要求OCR
    if force_ocr:
        if not OCR_AVAILABLE:
            return "", False, "强制OCR但OCR功能不可用"
        return extract_text_with_ocr(pdf_path)
    
    # 1. 首先尝试标准文本提取
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = []
            total_chars = 0
            
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    text = page.extract_text()
                    if text and text.strip():
                        page_text = f"--- 第 {page_num} 页 ---\n{text.strip()}"
                        all_text.append(page_text)
                        total_chars += len(text.strip())
                    else:
                        all_text.append(f"--- 第 {page_num} 页 ---\n[此页无文本内容]")
                except Exception as e:
                    all_text.append(f"--- 第 {page_num} 页 ---\n[页面提取失败: {str(e)}]")
                    continue
            
            full_text = "\n\n".join(all_text)
            
            # 2. 智能判断：是否需要降级到OCR？
            # 条件：总字符数很少，或者超过一半的页面没有文本
            empty_pages = sum(1 for t in all_text if "[此页无文本内容]" in t or "[页面提取失败]" in t)
            total_pages = len(pdf.pages)
            
            need_ocr = (total_chars < use_ocr_threshold) or (empty_pages / total_pages > 0.5)
            
            if need_ocr and OCR_AVAILABLE and total_pages > 0:
                print(f"  文本过少({total_chars}字符)，尝试OCR...", end="", flush=True)
                ocr_text, ocr_success, ocr_msg = extract_text_with_ocr(pdf_path)
                if ocr_success and len(ocr_text.strip()) > total_chars:
                    # 只有当OCR识别到更多文字时才使用OCR结果
                    print("[OK] (使用OCR结果)")
                    return ocr_text, True, f"(智能降级OCR: {ocr_msg})"
                else:
                    print("[WARNING] (OCR未获得更好结果，保留原提取)")
            
            if total_chars > 0:
                return full_text, True, f"(文本提取, {total_chars}字符)"
            else:
                return full_text, False, "未提取到有效文本"
                
    except Exception as e:
        error_msg = str(e)
        
        # 3. 如果文本提取完全失败，尝试OCR
        if OCR_AVAILABLE:
            print(f"  文本提取失败，尝试OCR...", end="", flush=True)
            ocr_text, ocr_success, ocr_msg = extract_text_with_ocr(pdf_path)
            if ocr_success:
                print("[OK]")
                return ocr_text, True, f"(降级OCR: {ocr_msg})"
            else:
                print("[FAILED]")
        
        # 错误类型判断
        if "encrypted" in error_msg.lower():
            return "", False, "PDF文件已加密"
        elif "damaged" in error_msg.lower():
            return "", False, "PDF文件损坏"
        else:
            return "", False, f"读取失败: {error_msg}"


def save_to_markdown(results: List[Tuple[str, str, bool, str]], output_path: str) -> None:
    """将提取结果保存到Markdown文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# PDF 文本提取结果（增强版）\n\n")
        f.write(f"**提取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 统计信息
        success_count = sum(1 for _, _, success, _ in results if success)
        ocr_count = sum(1 for _, _, _, method in results if "OCR" in method)
        
        f.write("## 提取统计\n\n")
        f.write(f"- 总文件数: {len(results)}\n")
        f.write(f"- 成功提取: {success_count}\n")
        f.write(f"- 使用OCR: {ocr_count} 个文件\n")
        f.write(f"- 提取失败: {len(results) - success_count}\n\n")
        f.write("---\n\n")
        
        # 每个文件的结果
        for filename, content, success, method in results:
            f.write(f"## {filename}\n\n")
            f.write(f"**提取方式**: {method}\n\n")
            
            if success:
                f.write(content)
            else:
                f.write(f"[WARNING] **提取失败**: {content if content else method}")
            
            f.write("\n\n---\n\n")


def save_to_json(results: List[Tuple[str, str, bool, str]], output_path: str) -> None:
    """将提取结果保存到JSON文件"""
    success_count = sum(1 for _, _, success, _ in results if success)
    ocr_count = sum(1 for _, _, _, method in results if "OCR" in method)
    
    output_data = {
        "提取时间": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "统计": {
            "总文件数": len(results),
            "成功提取": success_count,
            "使用OCR的文件数": ocr_count,
            "提取失败": len(results) - success_count
        },
        "文件": []
    }
    
    for filename, content, success, method in results:
        file_data = {
            "文件名": filename,
            "提取方式": method,
            "状态": "成功" if success else "失败"
        }
        
        if success:
            file_data["内容"] = content
            file_data["字符数"] = len(content)
            file_data["是否OCR"] = "OCR" in method
        else:
            file_data["错误信息"] = content if content else method
        
        output_data["文件"].append(file_data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2, separators=(',', ': '))


def process_pdfs(input_dir: str, 
                output_format: str = 'markdown', 
                output_name: str = '提取结果',
                ocr_threshold: int = 50,
                force_ocr: bool = False) -> int:
    """处理PDF文件提取的主逻辑"""
    
    print("=" * 60)
    print("       PDF 文本批量提取工具 (增强OCR版)")
    print("=" * 60)
    print(f"[FOLDER] 扫描文件夹: {input_dir}")
    
    if force_ocr:
        print("[MODE] 模式: 强制使用OCR")
    elif ocr_threshold > 0:
        print(f"[MODE] 模式: 智能降级 (阈值: {ocr_threshold}字符)")

    if not OCR_AVAILABLE and (force_ocr or ocr_threshold > 0):
        print("[WARNING] 警告: OCR功能不可用，将仅使用文本提取")
    
    try:
        pdf_files = get_pdf_files(input_dir)
    except Exception as e:
        print(f"[ERROR] 扫描失败: {e}")
        return 1
    
    if not pdf_files:
        print("[WARNING] 未找到PDF文件")
        return 0
    
    print(f"[OK] 找到 {len(pdf_files)} 个PDF文件")
    print()
    
    # 处理每个PDF
    results = []
    for index, pdf_path in enumerate(pdf_files, 1):
        filename = pdf_path.name
        print(f"[{index}/{len(pdf_files)}] {filename}", end=" ")
        
        content, success, method = extract_text_from_pdf(
            pdf_path, 
            use_ocr_threshold=ocr_threshold,
            force_ocr=force_ocr
        )
        
        results.append((filename, content, success, method))
        
        if success:
            char_count = len(content)
            print(f"[OK] {method}")
        else:
            print(f"[FAILED] {method}")
    
    print("\n" + "=" * 60)
    
    # 保存结果
    file_ext = '.json' if output_format == 'json' else '.md'
    output_path = os.path.join(input_dir, f"{output_name}{file_ext}")
    
    print(f"[SAVE] 保存到: {output_path}")
    
    try:
        if output_format == 'json':
            save_to_json(results, output_path)
        else:
            save_to_markdown(results, output_path)
        print("[OK] 保存成功")
    except Exception as e:
        print(f"[ERROR] 保存失败: {e}")
        return 1
    
    # 最终统计
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
    
    return 0


def parse_arguments() -> argparse.Namespace:
    """解析命令行参数"""
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
    
    # 必需参数
    parser.add_argument('-i', '--input', required=True, 
                       help='PDF文件夹路径 (必需)')
    
    # 输出参数
    parser.add_argument('-f', '--format', choices=['markdown', 'json'], 
                       default='markdown', help='输出格式 (默认: markdown)')
    parser.add_argument('-o', '--output', default='提取结果',
                       help='输出文件名，不含扩展名 (默认: 提取结果)')
    
    # OCR相关参数
    parser.add_argument('--ocr-threshold', type=int, default=50,
                       help='OCR触发阈值(字符数)，低于此值则尝试OCR (默认: 50，0=禁用OCR)')
    parser.add_argument('--force-ocr', action='store_true',
                       help='强制使用OCR，跳过文本提取尝试')
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()
    
    input_dir = args.input.strip('"').strip("'")
    
    return process_pdfs(
        input_dir=input_dir,
        output_format=args.format,
        output_name=args.output,
        ocr_threshold=args.ocr_threshold,
        force_ocr=args.force_ocr
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[WARNING] 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)