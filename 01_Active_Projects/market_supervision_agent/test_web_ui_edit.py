#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的 Web UI 编辑功能测试
模拟真实用户操作流程
"""

import requests
import time
from src.database_manager import DatabaseManager

def test_web_ui_edit():
    print("=" * 70)
    print("市场监管智能体 - Web UI 编辑功能完整测试")
    print("Python 3.12 虚拟环境")
    print("=" * 70)

    # 初始化
    db = DatabaseManager()
    session = requests.Session()

    # 1. 查看当前数据
    print("\n【步骤 1】查看当前数据库状态")
    operators = db.list_operators(limit=10)
    print(f"当前有 {len(operators)} 条记录：")
    for op in operators:
        print(f"  ID={op['id']}: {op['operator_name']} - 电话: {op.get('phone', '空')}")

    # 2. 选择一条记录进行编辑
    print("\n【步骤 2】选择编辑记录")
    test_id = 2
    operator = db.get_operator_by_id(test_id)
    print(f"选择记录: ID={test_id}, 姓名={operator['operator_name']}")
    print(f"当前电话: {operator.get('phone', '空')}")

    # 3. 访问编辑页面
    print("\n【步骤 3】访问编辑页面")
    edit_url = f'http://127.0.0.1:5000/edit/{test_id}'
    response = session.get(edit_url)
    print(f"GET {edit_url}")
    print(f"状态码: {response.status_code}")

    if response.status_code != 200:
        print("[FAIL] Page access failed")
        return False

    if operator['operator_name'] in response.text:
        print("[OK] Page loaded successfully")

    # 4. 填写表单并提交
    print("\n【步骤 4】填写并提交表单")
    new_phone = '13888888888'
    print(f"新电话号码: {new_phone}")

    form_data = {
        'operator_name': operator['operator_name'],
        'id_card': operator['id_card'],
        'gender': operator.get('gender', '男'),
        'nation': operator.get('nation', ''),
        'phone': new_phone,
        'political_status': operator.get('political_status', '群众'),
        'employee_count': str(operator.get('employee_count', 1)),
        'business_name': operator.get('business_name', ''),
        'business_address': operator.get('business_address', ''),
        'business_scope_general': operator.get('business_scope_general', ''),
        'business_scope_licensed': operator.get('business_scope_licensed', ''),
        'submit': 'save'
    }

    print(f"POST {edit_url}")
    post_response = session.post(edit_url, data=form_data, allow_redirects=False)
    print(f"状态码: {post_response.status_code}")

    # 5. 检查结果
    print("\n【步骤 5】检查操作结果")

    if post_response.status_code == 302:
        location = post_response.headers.get('Location', '')
        print(f"重定向到: {location}")

        if 'database' in location:
            print("[OK] Redirected to database page")
            success = True
        else:
            print(f"[FAIL] Wrong redirect (to {location})")
            success = False
    else:
        print(f"[FAIL] Wrong status code (got {post_response.status_code}, expected 302)")
        success = False

    # 6. 验证数据库更新
    print("\n【步骤 6】验证数据库更新")
    updated_operator = db.get_operator_by_id(test_id)
    actual_phone = updated_operator.get('phone', '')

    print(f"期望电话: {new_phone}")
    print(f"实际电话: {actual_phone}")

    if actual_phone == new_phone:
        print("[OK] Database updated successfully!")
    else:
        print("[FAIL] Database not updated")
        success = False

    # 7. 显示最终结果
    print("\n" + "=" * 70)
    if success:
        print("*** TEST PASSED! Web UI edit function works perfectly! ***")
    else:
        print("*** TEST FAILED ***")
    print("=" * 70)

    return success

if __name__ == '__main__':
    test_web_ui_edit()
