#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监管智能体 v4.0 - Flask Web UI

兼容 Python 3.14+ 的 Web 界面
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil
from datetime import datetime

# 确保项目根目录在路径最前面
project_root = Path(__file__).parent.parent
project_root_str = str(project_root)
if project_root_str in sys.path:
    sys.path.remove(project_root_str)
sys.path.insert(0, project_root_str)

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename

# 导入核心模块
from src.workflow import process_files
from src.database_manager import DatabaseManager
from src.application_generator import ApplicationGenerator
from src import create_ocr_engine

# 创建 Flask 应用
app = Flask(__name__)
app.secret_key = 'market-supervision-agent-2026'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB 最大文件上传
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'bmp', 'gif', 'webp'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== 路由 ====================

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    """文件上传页面"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """处理文件上传和 OCR 识别"""
    if 'files' not in request.files:
        flash('没有选择文件', 'error')
        return redirect(url_for('upload_page'))

    files = request.files.getlist('files')
    skip_ocr = request.form.get('skip_ocr') == 'true'
    auto_archive = request.form.get('auto_archive') != 'false'

    if not files or files[0].filename == '':
        flash('没有选择文件', 'error')
        return redirect(url_for('upload_page'))

    # 验证文件
    valid_files = []
    temp_paths = []

    try:
        for file in files:
            if file and allowed_file(file.filename):
                # 获取文件扩展名
                ext = os.path.splitext(file.filename)[1].lower()
                # 使用时间戳和扩展名创建临时文件名（避免中文文件名问题）
                temp_filename = f"temp_{int(datetime.now().timestamp() * 1000)}{ext}"
                temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
                file.save(temp_path)
                temp_paths.append(temp_path)
                valid_files.append(file)

        if not valid_files:
            flash('没有有效的文件（支持的格式：JPG, PNG, PDF）', 'error')
            return redirect(url_for('upload_page'))

        # 配置处理选项
        config = {
            "skip_ocr": skip_ocr,
            "skip_archiving": not auto_archive
        }

        # 处理文件
        import sys
        from pathlib import Path as Path2

        # 调试信息
        print(f"[DEBUG] 准备处理 {len(temp_paths)} 个文件", file=sys.stderr)
        for tp in temp_paths:
            print(f"[DEBUG] 临时文件: {tp}, 存在: {Path2(tp).exists()}", file=sys.stderr)

        result = process_files(temp_paths, config)

        # 调试结果
        print(f"[DEBUG] 处理结果: extracted_data={result.get('extracted_data')}", file=sys.stderr)
        print(f"[DEBUG] 消息: {result.get('messages', [])}", file=sys.stderr)

        # 清理临时文件
        for path in temp_paths:
            try:
                os.unlink(path)
            except:
                pass

        # 返回结果页面
        return render_template('upload_result.html',
                              files=valid_files,
                              result=result,
                              skip_ocr=skip_ocr)

    except Exception as e:
        # 清理临时文件
        for path in temp_paths:
            try:
                os.unlink(path)
            except:
                pass

        flash(f'处理失败: {str(e)}', 'error')
        return redirect(url_for('upload_page'))

@app.route('/database')
def database_page():
    """数据库管理页面"""
    db = DatabaseManager()
    keyword = request.args.get('keyword', '')
    limit = int(request.args.get('limit', 20))

    if keyword:
        operators = db.search_operators(keyword)
        search_term = keyword
    else:
        operators = db.list_operators(limit=limit)
        search_term = ''

    return render_template('database.html',
                          operators=operators,
                          search_term=search_term,
                          limit=limit)

@app.route('/generate')
def generate_page():
    """申请书生成页面"""
    db = DatabaseManager()
    operators = db.list_operators(limit=100)

    if not operators:
        flash('数据库中暂无记录，请先处理文件', 'warning')
        return redirect(url_for('upload_page'))

    return render_template('generate.html', operators=operators)

@app.route('/generate', methods=['POST'])
def generate_application():
    """生成申请书"""
    operator_id = request.form.get('operator_id')

    if not operator_id:
        flash('请选择经营户', 'error')
        return redirect(url_for('generate_page'))

    try:
        db = DatabaseManager()
        operator = db.get_operator_by_id(operator_id)

        if not operator:
            flash('找不到该经营户记录', 'error')
            return redirect(url_for('generate_page'))

        generator = ApplicationGenerator()
        # 使用绝对路径，因为 Flask 从 ui/ 目录运行
        output_dir = Path(__file__).parent.parent / "output"
        output_path = generator.generate_application(
            operator_data=operator,
            output_dir=str(output_dir)
        )

        flash(f'申请书已生成: {output_path}', 'success')

        # 如果文件存在，提供下载
        if os.path.exists(output_path):
            return send_file(output_path,
                           as_attachment=True,
                           download_name=Path(output_path).name)
        else:
            flash('文件生成失败', 'error')
            return redirect(url_for('generate_page'))

    except Exception as e:
        flash(f'生成失败: {str(e)}', 'error')
        return redirect(url_for('generate_page'))

@app.route('/edit/<int:operator_id>', methods=['GET', 'POST'])
def edit_page(operator_id):
    """编辑经营户信息页面"""
    import sys
    import os

    # 记录到文件
    log_file = 'debug_edit.log'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n[{datetime.now()}] edit_page called: ID={operator_id}, Method={request.method}\n")
        if request.method == 'POST':
            f.write(f"Form data: {dict(request.form)}\n")

    print(f"[DEBUG] edit_page 被调用: ID={operator_id}, Method={request.method}", file=sys.stderr)

    db = DatabaseManager()
    operator = db.get_operator_by_id(operator_id)

    if not operator:
        flash('找不到该经营户记录', 'error')
        return redirect(url_for('database_page'))

    if request.method == 'POST':
        # 处理表单提交
        updates = {}

        # 获取表单数据
        form_fields = [
            'operator_name', 'id_card', 'gender', 'nation', 'phone',
            'email', 'address', 'business_name', 'business_address',
            'business_scope', 'credit_code', 'property_owner',
            'lease_start', 'lease_end', 'rent_amount'
        ]

        # 必填字段列表（这些字段如果是空字符串，也要更新）
        required_fields = {'phone'}

        for field in form_fields:
            value = request.form.get(field, '').strip()
            # 必填字段或非空字段才更新
            if value or field in required_fields:
                updates[field] = value

        # 调试信息
        import sys
        print(f"[DEBUG] 收到表单数据: {dict(request.form)}", file=sys.stderr)
        print(f"[DEBUG] 准备更新: {updates}", file=sys.stderr)

        # 执行更新
        if updates:
            print(f"[DEBUG] 调用 db.update_operator({operator_id}, {updates})", file=sys.stderr)
            success = db.update_operator(operator_id, updates)
            print(f"[DEBUG] 更新结果: {success}", file=sys.stderr)
        else:
            print(f"[DEBUG] updates 为空，更新失败", file=sys.stderr)
            success = False

        print(f"[DEBUG] 最终 success = {success}", file=sys.stderr)

        if success:
            flash(f'✅ 更新成功！', 'success')
            return redirect(url_for('database_page'))
        else:
            flash('❌ 更新失败，请重试', 'error')
            return redirect(url_for('edit_page', operator_id=operator_id))

    # GET 请求，显示编辑表单
    return render_template('edit.html', operator=operator)

@app.route('/delete/<int:operator_id>', methods=['POST'])
def delete_operator(operator_id):
    """删除经营户记录"""
    db = DatabaseManager()
    operator = db.get_operator_by_id(operator_id)

    if not operator:
        flash('找不到该经营户记录', 'error')
        return redirect(url_for('database_page'))

    # 执行删除
    success = db.delete_operator(operator_id)

    if success:
        flash(f'✅ 已删除记录: {operator["operator_name"]}', 'success')
    else:
        flash('❌ 删除失败，请重试', 'error')

    return redirect(url_for('database_page'))

@app.route('/api/status')
def api_status():
    """API: 系统状态"""
    status = {
        "version": "4.0.0",
        "timestamp": datetime.now().isoformat(),
        "ocr_engine": None,
        "database_status": "unknown"
    }

    # 检查 OCR 引擎
    try:
        ocr = create_ocr_engine()
        status["ocr_engine"] = ocr.active_engine.upper()
        status["ocr_status"] = "ok"
    except Exception as e:
        status["ocr_status"] = f"error: {str(e)}"

    # 检查数据库
    try:
        db = DatabaseManager()
        count = len(db.list_operators(limit=1))
        status["database_status"] = "ok"
        status["record_count"] = db.get_record_count()
    except Exception as e:
        status["database_status"] = f"error: {str(e)}"

    return jsonify(status)

@app.route('/api/search')
def api_search():
    """API: 搜索经营户"""
    keyword = request.args.get('keyword', '')
    limit = int(request.args.get('limit', 20))

    if not keyword:
        return jsonify({"error": "请提供搜索关键词"}), 400

    try:
        db = DatabaseManager()
        operators = db.search_operators(keyword)
        return jsonify({"count": len(operators), "results": operators})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error_code=404, error_message="页面未找到"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500, error_message="服务器内部错误"), 500

@app.errorhandler(413)
def request_entity_too_large(e):
    flash('文件太大（最大50MB）', 'error')
    return redirect(url_for('upload_page'))

# ==================== 启动 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("[OK] 市场监管智能体 v4.0 - Flask Web UI")
    print("[OK] 版本: 4.0.0")
    print("[OK] 启动中...")
    print("=" * 60)

    # 检查 OCR 引擎
    try:
        ocr = create_ocr_engine()
        print(f"[OK] OCR 引擎: {ocr.active_engine.upper()}")
    except Exception as e:
        print(f"[FAIL] OCR 引擎加载失败: {e}")

    # 检查数据库
    try:
        db = DatabaseManager()
        count = db.get_record_count()
        print(f"[OK] 数据库: {count} 条记录")
    except Exception as e:
        print(f"[FAIL] 数据库检查失败: {e}")

    print("=" * 60)
    print("[INFO] 访问地址: http://localhost:5000")
    print("[INFO] 按 Ctrl+C 停止服务")
    print("=" * 60)
    print()

    # 启动 Flask 开发服务器
    app.run(host='0.0.0.0', port=5000, debug=True)
