#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试网站服务器 - 模拟网上办事平台
用于测试自动化Agent

作者: Claude Code
日期: 2026-01-16
版本: 1.0.0
"""

import sys
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from flask import Flask, render_template, request, redirect, url_for, session, send_file
from datetime import datetime

# 创建Flask应用
app = Flask(__name__)
app.secret_key = 'test_secret_key_for_ai_training_2026'

# 测试用户数据
TEST_USERS = {
    "test_user": "test123",
    "admin": "admin123"
}

# 存储提交的表单数据（内存存储，重启后清空）
submitted_forms = {}


# ============================================================================
# 路由定义
# ============================================================================

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 验证用户
        if username in TEST_USERS and TEST_USERS[username] == password:
            session['user'] = username
            session['login_time'] = datetime.now().isoformat()
            return redirect(url_for('application_form'))
        else:
            return render_template('login.html', error='用户名或密码错误')

    return render_template('login.html')


@app.route('/individual-business', methods=['GET', 'POST'])
def application_form():
    """个体工商户申请表单"""
    # 检查登录状态
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # 保存表单数据
        form_id = f"FORM_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        form_data = {
            'form_id': form_id,
            'submit_time': datetime.now().isoformat(),
            'user': session.get('user'),
            'businessName': request.form.get('businessName'),
            'ownerName': request.form.get('ownerName'),
            'idCard': request.form.get('idCard'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'address': request.form.get('address'),
            'businessScope': request.form.get('businessScope'),
            'businessType': request.form.get('businessType'),
        }

        submitted_forms[form_id] = form_data
        session['last_form_id'] = form_id

        return redirect(url_for('success'))

    return render_template('application_form.html')


@app.route('/success')
def success():
    """成功页面"""
    if 'user' not in session:
        return redirect(url_for('login'))

    form_id = session.get('last_form_id')
    form_data = submitted_forms.get(form_id, {})

    return render_template('success.html', form_data=form_data)


@app.route('/logout')
def logout():
    """登出"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/form/<form_id>')
def get_form(form_id):
    """API: 获取表单数据"""
    if 'user' not in session:
        return {'error': '未登录'}, 401

    form_data = submitted_forms.get(form_id)
    if form_data:
        return form_data
    else:
        return {'error': '表单不存在'}, 404


@app.route('/api/forms')
def list_forms():
    """API: 列出所有表单"""
    if 'user' not in session:
        return {'error': '未登录'}, 401

    return {
        'total': len(submitted_forms),
        'forms': list(submitted_forms.values())
    }


# ============================================================================
# 启动服务器
# ============================================================================

def main():
    """启动测试服务器"""
    print("\n" + "="*60)
    print("🌐 测试网站服务器".center(50))
    print("="*60)
    print()
    print("服务器信息:")
    print(f"  地址: http://127.0.0.1:5555")
    print(f"  登录页面: http://127.0.0.1:5555/login")
    print(f"  测试账号: test_user / test123")
    print()
    print("可用页面:")
    print(f"  - 首页: /")
    print(f"  - 登录: /login")
    print(f"  - 申请表单: /individual-business")
    print(f"  - 成功页面: /success")
    print(f"  - 登出: /logout")
    print()
    print("API接口:")
    print(f"  - GET /api/form/<form_id>  获取表单数据")
    print(f"  - GET /api/forms          列出所有表单")
    print()
    print("="*60)
    print("服务器启动中... (按 Ctrl+C 停止)")
    print("="*60 + "\n")

    # 启动服务器
    app.run(
        host='127.0.0.1',
        port=5555,
        debug=True
    )


if __name__ == "__main__":
    main()
