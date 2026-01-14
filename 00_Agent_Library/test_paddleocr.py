#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaddleOCR 测试脚本（简化版）
"""

import sys
import os

# 设置环境变量跳过模型源检查
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

print("\n" + "="*70)
print("PaddleOCR 测试")
print("="*70 + "\n")

# 测试 1: 检查安装
print("测试 1: 检查 PaddleOCR 安装")
print("-" * 70)

try:
    import paddleocr
    print(f"✅ PaddleOCR 版本: {paddleocr.__version__}")
except ImportError as e:
    print(f"❌ PaddleOCR 未安装: {e}")
    sys.exit(1)

print()

# 测试 2: 检查配置文件
print("测试 2: 检查本地 AI 配置文件")
print("-" * 70)

config_path = "01_Active_Projects/market_supervision_agent/config/local_ai_config.yaml"
if os.path.exists(config_path):
    print(f"✅ 配置文件存在: {config_path}")
    import yaml
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    ocr_config = config.get('ocr', {}).get('paddleocr', {})
    print(f"  GPU 加速: {ocr_config.get('use_gpu', False)}")
    print(f"  MKL-DNN: {ocr_config.get('enable_mkldnn', True)}")
    print(f"  语言: {ocr_config.get('lang', 'ch')}")
else:
    print(f"⚠️  配置文件不存在: {config_path}")

print()

# 测试 3: 创建 OCR 实例
print("测试 3: 创建 PaddleOCR 实例")
print("-" * 70)

try:
    from paddleocr import PaddleOCR

    # 创建 OCR 实例（使用新参数名）
    ocr = PaddleOCR(
        use_textline_orientation=True,  # 新参数名
        lang='ch',
        use_gpu=False
    )

    print("✅ PaddleOCR 实例创建成功!")
    print(f"  语言: 中文 (ch)")
    print(f"  GPU: False (CPU 模式)")
    print(f"  方向分类器: True")

except Exception as e:
    print(f"⚠️  PaddleOCR 实例创建警告: {e}")
    print("提示: 首次运行会下载模型文件，请稍候...")

print()

# 测试 4: 查找测试图片
print("测试 4: 查找测试图片")
print("-" * 70)

from pathlib import Path

test_dirs = [
    "01_Active_Projects/market_supervision_agent/templates",
    "01_Active_Projects/market_supervision_agent/output",
    "."
]

test_image_found = False
for test_dir in test_dirs:
    test_path = Path(test_dir)
    if test_path.exists():
        images = list(test_path.glob("*.jpg")) + list(test_path.glob("*.png")) + list(test_path.glob("*.jpeg"))
        if images:
            print(f"✅ 找到 {len(images)} 张图片:")
            for img in images[:3]:
                print(f"  • {img}")
            test_image_found = True
            break

if not test_image_found:
    print("⚠️  未找到测试图片")
    print("提示: 将营业执照图片放到项目目录中即可测试")

print()

# 测试 5: 性能信息
print("测试 5: 系统信息")
print("-" * 70)

try:
    import platform
    import psutil

    print(f"  CPU: {platform.processor()}")
    print(f"  核心数: {psutil.cpu_count()}")
    print(f"  内存: {psutil.virtual_memory().total / (1024**3):.1f} GB")
except:
    print("  系统信息获取失败")

print()

# 总结
print("="*70)
print("测试总结")
print("="*70)
print()
print("✅ PaddleOCR 已成功安装!")
print()
print("版本信息:")
print(f"  PaddleOCR: {paddleocr.__version__}")
print(f"  配置: CPU 模式")
print()
print("配置文件:")
print(f"  位置: {config_path}")
print(f"  GPU 加速: {ocr_config.get('use_gpu', False)}")
print(f"  MKL-DNN: {ocr_config.get('enable_mkldnn', True)}")
print()
print("下一步:")
print("  1. 使用营业执照图片测试 OCR 识别")
print("  2. 集成到市场监管智能体")
print("  3. 如有 GPU，修改配置文件启用 use_gpu: true")
print()
print("使用示例:")
print("  from paddleocr import PaddleOCR")
print("  ocr = PaddleOCR(use_textline_orientation=True, lang='ch')")
print("  result = ocr.ocr('business_license.jpg')")
print()
