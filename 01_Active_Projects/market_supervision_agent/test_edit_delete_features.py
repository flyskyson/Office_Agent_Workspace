#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试编辑和删除功能
"""

import sys
from pathlib import Path

# 确保项目根目录在路径中
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database_manager import DatabaseManager

def test_edit_functionality():
    """测试编辑功能"""
    print("=" * 60)
    print("测试 1: 编辑功能")
    print("=" * 60)

    db = DatabaseManager()

    # 获取一条记录进行测试
    operators = db.list_operators(limit=1)
    if not operators:
        print("[ERROR] 数据库中没有记录")
        return False

    operator = operators[0]
    operator_id = operator['id']
    original_phone = operator.get('phone', '')

    print(f"[INFO] 测试记录 ID={operator_id}")
    print(f"  姓名: {operator['operator_name']}")
    print(f"  原电话: {original_phone}")

    # 测试更新电话号码
    new_phone = "13999999999"
    print(f"\n[TEST] 更新电话号码为: {new_phone}")

    success = db.update_operator(operator_id, {'phone': new_phone})
    print(f"  更新结果: {'成功' if success else '失败'}")

    # 验证更新
    updated_op = db.get_operator_by_id(operator_id)
    updated_phone = updated_op.get('phone', '')
    print(f"  验证电话: {updated_phone}")

    if updated_phone == new_phone:
        print("[OK] 编辑功能测试通过!")
        return True
    else:
        print("[FAIL] 编辑功能测试失败!")
        return False

def test_delete_functionality():
    """测试删除功能"""
    print("\n" + "=" * 60)
    print("测试 2: 删除功能")
    print("=" * 60)

    db = DatabaseManager()

    # 创建一个测试记录
    import random
    test_id_card = f'{random.randint(100000, 999999)}{random.randint(100000, 999999)}{random.randint(10, 99)}'
    test_data = {
        'operator_name': '测试用户',
        'id_card': test_id_card,
        'phone': '11111111111',
        'business_name': '测试店铺'
    }

    print("[INFO] 创建测试记录...")
    try:
        new_id = db.insert_operator(test_data)
        print(f"  新记录 ID: {new_id}")
    except Exception as e:
        print(f"  创建失败: {e}")
        return False

    # 验证记录存在
    test_op = db.get_operator_by_id(new_id)
    if not test_op:
        print("[ERROR] 记录创建失败")
        return False
    print(f"  记录姓名: {test_op['operator_name']}")

    # 测试删除
    print(f"\n[TEST] 删除记录 ID={new_id}")
    success = db.delete_operator(new_id)
    print(f"  删除结果: {'成功' if success else '失败'}")

    # 验证软删除
    deleted_op = db.get_operator_by_id(new_id)
    if deleted_op and deleted_op.get('status') == 'deleted':
        print(f"  记录状态: {deleted_op['status']}")
        print("[OK] 删除功能测试通过!")
        return True
    else:
        print("[FAIL] 删除功能测试失败!")
        return False

def test_update_multiple_fields():
    """测试更新多个字段"""
    print("\n" + "=" * 60)
    print("测试 3: 更新多个字段")
    print("=" * 60)

    db = DatabaseManager()

    # 获取一条记录
    operators = db.list_operators(limit=1)
    if not operators:
        print("[ERROR] 数据库中没有记录")
        return False

    operator = operators[0]
    operator_id = operator['id']

    print(f"[INFO] 测试记录 ID={operator_id}")

    # 更新多个字段（使用数据库实际存在的字段）
    updates = {
        'phone': '13800138000',
        'business_name': '更新后的店铺名称',
        'email': 'test@example.com'
    }

    print(f"[TEST] 更新多个字段:")
    for k, v in updates.items():
        print(f"  {k}: {v}")

    success = db.update_operator(operator_id, updates)
    print(f"  更新结果: {'成功' if success else '失败'}")

    # 验证更新
    updated_op = db.get_operator_by_id(operator_id)
    all_match = True
    for k, v in updates.items():
        actual = updated_op.get(k)
        match = actual == v
        all_match = all_match and match
        print(f"  {k}: {actual} {'[OK]' if match else '[FAIL]'}")

    if all_match:
        print("[OK] 多字段更新测试通过!")
        return True
    else:
        print("[FAIL] 多字段更新测试失败!")
        return False

def main():
    print("\n市场监管智能体 v4.0 - 功能测试")
    print("=" * 60)
    print()

    results = []

    # 运行测试
    results.append(("编辑功能", test_edit_functionality()))
    results.append(("删除功能", test_delete_functionality()))
    results.append(("多字段更新", test_update_multiple_fields()))

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[OK]" if result else "[FAIL]"
        print(f"  {status} {name}")

    print()
    print(f"总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n所有测试通过!")
        return 0
    else:
        print(f"\n{total - passed} 个测试失败")
        return 1

if __name__ == '__main__':
    sys.exit(main())
