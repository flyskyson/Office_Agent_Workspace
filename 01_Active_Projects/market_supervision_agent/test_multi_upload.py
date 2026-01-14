#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试多文件上传
"""

import requests
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    print("=" * 60)
    print("测试多文件上传到 Flask 应用")
    print("=" * 60)

    url = "http://127.0.0.1:5000/upload"

    # 准备文件
    files = [
        ('files', open('C:/Users/flyskyson/Desktop/经营者身份证正面.jpg', 'rb')),
        ('files', open('C:/Users/flyskyson/Desktop/营业执照.jpg', 'rb'))
    ]

    # 准备表单数据
    data = {
        'skip_ocr': 'false',
        'auto_archive': 'true'
    }

    print(f"\n[1] 上传 {len(files)} 个文件到 {url}")
    for i, (key, _) in enumerate(files, 1):
        print(f"    文件 {i}: {key}")

    try:
        # 发送 POST 请求
        response = requests.post(
            url,
            files=files,
            data=data,
            timeout=60
        )

        print(f"\n[2] 响应状态: {response.status_code}")

        if response.status_code == 200:
            print("\n[OK] 上传成功！")
            print("\n响应内容预览:")
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        else:
            print(f"\n[FAIL] 上传失败: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"\n[ERROR] 请求失败: {e}")

    finally:
        # 关闭文件
        for _, f in files:
            f.close()

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
