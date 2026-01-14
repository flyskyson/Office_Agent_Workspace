#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试营业执照 OCR 识别
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.baidu_ocr_engine import BaiduOCREngine
import json

def main():
    print("=" * 60)
    print("营业执照 OCR 识别测试")
    print("=" * 60)

    # 初始化 OCR 引擎
    print("\n[1] 初始化百度 OCR 引擎...")
    engine = BaiduOCREngine('', '', '', 'config/baidu_ocr.yaml')

    # 测试文件
    test_file = 'C:/Users/flyskyson/Desktop/营业执照.jpg'

    print(f"\n[2] 识别营业执照: {test_file}")
    print(f"    文件大小: {Path(test_file).stat().st_size / 1024 / 1024:.2f} MB")

    try:
        result = engine.recognize_business_license(test_file)

        print(f"\n[3] 识别结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

        if result:
            print(f"\n[OK] 识别成功，提取到 {len(result)} 个字段")
        else:
            print("\n[FAIL] 识别结果为空")

    except Exception as e:
        print(f"\n[ERROR] 识别失败: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
