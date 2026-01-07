"""
创建简单的测试 PDF 文件
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path


def create_test_pdf_1():
    """创建测试 PDF 1 - 简单的英文文档"""
    filename = Path("test_pdfs/test_document_1.pdf")
    filename.parent.mkdir(exist_ok=True)

    c = canvas.Canvas(str(filename), pagesize=letter)

    # 第一页
    c.drawString(100, 750, "Test Document 1")
    c.drawString(100, 730, "This is a test PDF file for extraction.")
    c.drawString(100, 710, "")
    c.drawString(100, 690, "Features:")
    c.drawString(120, 670, "- Simple text content")
    c.drawString(120, 650, "- Multiple pages")
    c.drawString(120, 630, "- Easy to extract")

    c.showPage()

    # 第二页
    c.drawString(100, 750, "Page 2 of Test Document 1")
    c.drawString(100, 730, "This demonstrates multi-page extraction.")
    c.drawString(100, 710, "The extractor should capture all pages.")
    c.drawString(100, 690, "")

    c.showPage()

    # 第三页
    c.drawString(100, 750, "Page 3 - Final Page")
    c.drawString(100, 730, "End of test document 1.")

    c.save()
    print(f"[OK] Created: {filename}")
    return filename


def create_test_pdf_2():
    """创建测试 PDF 2 - 中文文档"""
    filename = Path("test_pdfs/test_document_2.pdf")
    filename.parent.mkdir(exist_ok=True)

    c = canvas.Canvas(str(filename), pagesize=letter)

    # 第一页
    c.drawString(100, 750, "测试文档 2")
    c.drawString(100, 730, "这是一个中文测试 PDF 文件。")
    c.drawString(100, 710, "")
    c.drawString(100, 690, "功能特点：")
    c.drawString(120, 670, "- 支持中文内容")
    c.drawString(120, 650, "- 文本提取测试")
    c.drawString(120, 630, "- 批量处理演示")

    c.showPage()

    # 第二页
    c.drawString(100, 750, "第二页 - 测试文档 2")
    c.drawString(100, 730, "展示多页文档的提取功能。")
    c.drawString(100, 710, "提取器应该能捕获所有页面内容。")

    c.save()
    print(f"[OK] Created: {filename}")
    return filename


def create_test_pdf_3():
    """创建测试 PDF 3 - 简短文档"""
    filename = Path("test_pdfs/test_document_3.pdf")
    filename.parent.mkdir(exist_ok=True)

    c = canvas.Canvas(str(filename), pagesize=letter)

    c.drawString(100, 750, "Test Document 3 - Short Document")
    c.drawString(100, 730, "This is a single-page document for testing.")
    c.drawString(100, 710, "It has fewer pages but should work the same way.")

    c.save()
    print(f"[OK] Created: {filename}")
    return filename


def main():
    print("="*60)
    print("Creating Test PDF Files")
    print("="*60)
    print()

    try:
        create_test_pdf_1()
        create_test_pdf_2()
        create_test_pdf_3()

        print()
        print("="*60)
        print("[SUCCESS] Test PDFs created successfully!")
        print("="*60)
        print()
        print("Created test_pdfs folder with 3 test PDF files:")
        print("  1. test_document_1.pdf (3 pages, English)")
        print("  2. test_document_2.pdf (2 pages, Chinese)")
        print("  3. test_document_3.pdf (1 page, English)")
        print()
        print("Now you can run:")
        print("  python pdf_extractor.py")
        print()
        print("And enter the path: test_pdfs")
        print()

    except ImportError:
        print("[ERROR] reportlab not installed. Installing...")
        import subprocess
        subprocess.run(["pip", "install", "reportlab"], check=True)
        print("[OK] reportlab installed. Please run this script again.")
    except Exception as e:
        print(f"[ERROR] Error creating test PDFs: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
