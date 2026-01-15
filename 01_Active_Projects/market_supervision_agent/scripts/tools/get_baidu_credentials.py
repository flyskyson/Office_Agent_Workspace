#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度 OCR 凭证配置助手

帮助用户快速配置百度 OCR API 凭证
"""

import yaml
from pathlib import Path


def get_baidu_credentials():
    """获取百度 OCR 凭证并保存到配置文件"""

    print("=" * 60)
    print("百度 OCR API 凭证配置助手")
    print("=" * 60)
    print()

    # 说明
    print("请按以下步骤操作：")
    print("1. 访问百度智能云控制台：https://console.bce.baidu.com/ai/#/ai/ocr/overview/index")
    print("2. 如果没有应用，点击'创建应用'")
    print("3. 填写应用名称（如：市场监管智能体）")
    print("4. 选择文字识别服务")
    print("5. 提交后，在应用列表中查看以下信息：")
    print()
    print("   - AppID")
    print("   - API Key")
    print("   - Secret Key")
    print()
    print("-" * 60)

    # 输入凭证
    app_id = input("\n请输入 AppID: ").strip()
    api_key = input("请输入 API Key: ").strip()
    secret_key = input("请输入 Secret Key: ").strip()

    if not all([app_id, api_key, secret_key]):
        print("\n[ERROR] 凭证不完整，请重新填写！")
        return False

    # 配置内容
    config_content = f"""# 百度智能云 OCR API 配置
# 配置说明：https://cloud.baidu.com/doc/OCR/index.html

# ============ API 凭证 ============
app_id: "{app_id}"
api_key: "{api_key}"
secret_key: "{secret_key}"

# ============ 免费额度 ============
# 通用文字识别：500次/天
# 身份证识别：500次/天
# 营业执照识别：500次/天
"""

    # 保存配置文件
    config_file = Path("config/baidu_ocr.yaml")
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)

    print(f"\n[SUCCESS] 配置已保存到: {config_file}")

    # 验证配置
    print("\n[INFO] 正在验证配置...")

    try:
        from src.baidu_ocr_engine import BaiduOCREngine

        engine = BaiduOCREngine(config_file=str(config_file))
        engine._initialize()

        print("[SUCCESS] 百度 OCR API 连接成功！")
        print()
        print("=" * 60)
        print("配置完成！您现在可以使用以下功能：")
        print("- 身份证识别")
        print("- 营业执照识别")
        print("- 租赁合同识别")
        print("- 通用文字识别")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"[WARNING] 配置已保存，但验证失败: {e}")
        print()
        print("可能的原因：")
        print("1. AppID / API Key / Secret Key 填写错误")
        print("2. 网络连接问题")
        print("3. 百度 OCR 服务异常")
        print()
        print("请检查配置文件:", config_file)
        return False


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))

    try:
        success = get_baidu_credentials()
        if success:
            print("\n运行 'python start_v4.py ocr' 测试 OCR 功能")
        else:
            print("\n请重新运行此脚本配置凭证")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n配置已取消")
        sys.exit(0)
