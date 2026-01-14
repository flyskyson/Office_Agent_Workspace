#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试表单提交功能"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database_manager import DatabaseManager

def main():
    print("=" * 60)
    print("数据编辑功能测试")
    print("=" * 60)

    db = DatabaseManager()

    # 列出所有记录
    operators = db.list_operators(limit=10)
    print(f"\n当前数据库有 {len(operators)} 条记录:\n")

    for op in operators:
        print(f"ID={op['id']}: {op['operator_name']} - 电话: {op.get('phone', '空')}")

    # 交互式更新
    print("\n" + "=" * 60)
    operator_id = input("请输入要编辑的记录ID: ").strip()

    if not operator_id.isdigit():
        print("❌ 无效的ID")
        return

    operator_id = int(operator_id)
    operator = db.get_operator_by_id(operator_id)

    if not operator:
        print(f"❌ 找不到ID={operator_id}的记录")
        return

    print(f"\n当前记录: {operator['operator_name']}")
    print(f"电话: {operator.get('phone', '空')}")

    # 输入新电话
    new_phone = input("\n请输入新的联系电话: ").strip()

    if not new_phone:
        print("❌ 电话号码不能为空")
        return

    # 执行更新
    print(f"\n正在更新ID={operator_id}的电话为 {new_phone}...")
    success = db.update_operator(operator_id, {'phone': new_phone})

    if success:
        print("✅ 更新成功!")

        # 验证
        updated = db.get_operator_by_id(operator_id)
        print(f"验证: {updated['operator_name']} 的电话现在是 {updated.get('phone', '空')}")
    else:
        print("❌ 更新失败")

if __name__ == '__main__':
    main()
