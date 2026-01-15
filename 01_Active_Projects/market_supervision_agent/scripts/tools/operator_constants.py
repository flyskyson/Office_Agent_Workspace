#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经营户数据区管理工具
管理固定的经营户信息（邮政编码、身份证件类型等）
"""

import json
from pathlib import Path

# 配置文件路径
CONFIG_FILE = Path(__file__).parent / "config.json"

def load_operator_constants():
    """加载经营户常量数据"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('constants', {})
    except Exception as e:
        print(f"[错误] 无法加载配置文件: {e}")
        return {}

def save_operator_constants(constants):
    """保存经营户常量数据"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)

        config['constants'] = constants

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"[错误] 无法保存配置文件: {e}")
        return False

def show_operator_constants():
    """显示当前经营户常量"""
    print("=" * 70)
    print("经营户数据区常量")
    print("=" * 70)

    constants = load_operator_constants()

    if not constants:
        print("\n暂无经营户常量数据")
        return

    print("\n当前常量配置:\n")

    # 过滤掉说明字段
    display_data = {k: v for k, v in constants.items() if not k.endswith('_说明')}

    for key, value in display_data.items():
        print(f"  {key:20} : {value}")

    print("\n" + "=" * 70)

def update_operator_constants():
    """更新经营户常量"""
    print("=" * 70)
    print("更新经营户数据区常量")
    print("=" * 70)

    constants = load_operator_constants()

    print("\n当前值:")
    show_operator_constants()

    print("\n请输入新的常量值 (直接回车保持原值):\n")

    # 邮政编码
    current_postal = constants.get('postal_code', '537820')
    new_postal = input(f"邮政编码 [{current_postal}]: ").strip()
    if new_postal:
        constants['postal_code'] = new_postal

    # 身份证件类型
    current_id_type = constants.get('id_card_type', '身份证')
    new_id_type = input(f"身份证件类型 [{current_id_type}]: ").strip()
    if new_id_type:
        constants['id_card_type'] = new_id_type

    # 所属区域
    current_region = constants.get('region', '')
    new_region = input(f"所属区域 [{current_region}]: ").strip()
    if new_region:
        constants['region'] = new_region

    # 保存
    if save_operator_constants(constants):
        print("\n[成功] 经营户常量已更新!")
        show_operator_constants()
    else:
        print("\n[错误] 保存失败!")

def main():
    """主程序"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "show":
            show_operator_constants()
        elif command == "update":
            update_operator_constants()
        elif command == "reset":
            # 重置为默认值
            default_constants = {
                "_说明": "经营户数据区常量",
                "postal_code": "537820",
                "id_card_type": "身份证",
                "region": "广西壮族自治区玉林市兴业县蒲塘镇"
            }
            if save_operator_constants(default_constants):
                print("[成功] 已重置为默认值")
                show_operator_constants()
        else:
            print(f"未知命令: {command}")
            print("可用命令: show, update, reset")
    else:
        # 默认显示当前常量
        show_operator_constants()

if __name__ == "__main__":
    main()
