#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监管智能体 v5.0 - Flask Web UI
统一工作流 API

支持三输入源统一处理：
1. 文件上传 + OCR
2. 政务服务网表单
3. Flask Web 表单

作者: Claude Code
日期: 2026-01-14
"""

import sys
import os
import json
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# 确保项目根目录在路径最前面
project_root = Path(__file__).parent.parent
project_root_str = str(project_root)
if project_root_str in sys.path:
    sys.path.remove(project_root_str)
sys.path.insert(0, project_root_str)

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename

# 导入核心模块
from src.unified_workflow import (
    UnifiedWorkflowEngine,
    WorkflowConfig,
    WorkflowStage,
    create_workflow,
    quick_start_registration
)
from src.database_manager import DatabaseManager
from src.portal_automation import PortalAutomation, PortalConfig

# 创建 Flask 应用
app = Flask(__name__)
app.secret_key = 'market-supervision-agent-v5-2026'
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
    """首页 - 工作流仪表板"""
    return render_template('workflow_index.html')


@app.route('/workflow/new', methods=['GET', 'POST'])
def new_workflow():
    """创建新工作流"""
    if request.method == 'GET':
        return render_template('workflow_new.html')

    # POST: 创建新工作流
    scenario = request.form.get('scenario', 'registration')

    # 创建工作流
    workflow = create_workflow(scenario)
    progress = workflow.start_workflow()

    # 重定向到工作流页面
    return redirect(url_for('workflow_page', operator_id=progress.operator_id))


@app.route('/workflow/<int:operator_id>')
def workflow_page(operator_id: int):
    """工作流页面 - 显示进度和操作"""
    # 加载工作流进度
    workflow = create_workflow()
    progress_summary = workflow.get_progress_summary(operator_id)

    if not progress_summary:
        flash('工作流不存在', 'error')
        return redirect(url_for('index'))

    # 获取经营户数据
    db = DatabaseManager()
    operator = db.get_operator_by_id(operator_id)

    return render_template('workflow_detail.html',
                          operator_id=operator_id,
                          progress=progress_summary,
                          operator=operator)


@app.route('/api/workflow/<int:operator_id>/progress')
def api_workflow_progress(operator_id: int):
    """API: 获取工作流进度"""
    workflow = create_workflow()
    progress = workflow.get_progress_summary(operator_id)

    if not progress:
        return jsonify({'error': '工作流不存在'}), 404

    return jsonify(progress)


@app.route('/upload/ocr', methods=['POST'])
def upload_ocr():
    """文件上传 + OCR 输入"""
    if 'files' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400

    files = request.files.getlist('files')
    operator_id = request.form.get('operator_id', type=int)

    if not files or files[0].filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    # 验证文件
    valid_files = []
    temp_paths = []

    try:
        for file in files:
            if file and allowed_file(file.filename):
                # 保存临时文件
                ext = os.path.splitext(file.filename)[1].lower()
                temp_filename = f"temp_{int(datetime.now().timestamp() * 1000)}{ext}"
                temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
                file.save(temp_path)
                temp_paths.append(temp_path)
                valid_files.append(file)

        if not valid_files:
            return jsonify({'error': '没有有效的文件'}), 400

        # 创建或恢复工作流
        workflow = create_workflow()
        progress = workflow.start_workflow(operator_id=operator_id)

        # 处理OCR输入
        progress = workflow.process_ocr_input(temp_paths, progress)

        # 清理临时文件
        for path in temp_paths:
            try:
                os.unlink(path)
            except:
                pass

        return jsonify({
            'success': True,
            'operator_id': progress.operator_id,
            'input_sources': progress.input_sources,
            'data_completeness': progress.data_completeness,
            'messages': ['OCR处理完成'],
            'warnings': progress.warnings,
            'errors': progress.errors
        })

    except Exception as e:
        # 清理临时文件
        for path in temp_paths:
            try:
                os.unlink(path)
            except:
                pass

        return jsonify({'error': str(e)}), 500


@app.route('/portal/automation', methods=['POST'])
def portal_automation():
    """政务服务网表单自动化"""
    data = request.get_json()

    operator_id = data.get('operator_id')
    portal_config = data.get('portal_config', {})

    # 获取经营户数据
    db = DatabaseManager()
    operator = db.get_operator_by_id(operator_id)

    if not operator:
        return jsonify({'error': '经营户不存在'}), 404

    try:
        # 创建自动化实例
        config = PortalConfig(
            username=portal_config.get('username'),
            password=portal_config.get('password'),
            headless=False  # 建议非无头模式，方便观察
        )

        with PortalAutomation(config) as portal:
            result = portal.process_registration(
                business_name=operator.get('business_name', ''),
                operator_data=operator,
                business_scope=operator.get('business_scope', ''),
                auto_submit=False
            )

        # 更新工作流
        workflow = create_workflow()
        progress = workflow.start_workflow(operator_id=operator_id)
        progress = workflow.process_web_portal_input(result.get('extracted_data', {}), progress)

        return jsonify({
            'success': True,
            'operator_id': operator_id,
            'portal_result': result,
            'progress': workflow.get_progress_summary(operator_id)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/form/supplement', methods=['POST'])
def form_supplement():
    """Flask Web 表单补充数据"""
    operator_id = request.form.get('operator_id', type=int)

    if not operator_id:
        return jsonify({'error': '缺少 operator_id'}), 400

    # 获取表单数据
    form_data = {
        'operator_name': request.form.get('operator_name'),
        'id_card': request.form.get('id_card'),
        'phone': request.form.get('phone'),
        'email': request.form.get('email'),
        'gender': request.form.get('gender'),
        'nation': request.form.get('nation'),
        'address': request.form.get('address'),
        'business_name': request.form.get('business_name'),
        'business_address': request.form.get('business_address'),
        'business_scope': request.form.get('business_scope'),
    }

    # 过滤空值
    form_data = {k: v for k, v in form_data.items() if v}

    try:
        # 创建或恢复工作流
        workflow = create_workflow()
        progress = workflow.start_workflow(operator_id=operator_id)

        # 处理表单输入
        progress = workflow.process_web_form_input(form_data, progress)

        return jsonify({
            'success': True,
            'operator_id': progress.operator_id,
            'input_sources': progress.input_sources,
            'data_completeness': progress.data_completeness,
            'messages': ['表单数据已保存'],
            'warnings': progress.warnings,
            'errors': progress.errors
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/workflow/<int:operator_id>/fuse', methods=['POST'])
def fuse_data(operator_id: int):
    """数据融合"""
    try:
        workflow = create_workflow()
        progress = workflow.start_workflow(operator_id=operator_id)
        progress = workflow.fuse_data(progress)

        return jsonify({
            'success': True,
            'operator_id': operator_id,
            'current_stage': progress.current_stage.value,
            'data_completeness': progress.data_completeness
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/workflow/<int:operator_id>/validate', methods=['POST'])
def validate_materials(operator_id: int):
    """材料校验"""
    try:
        workflow = create_workflow()
        progress = workflow.start_workflow(operator_id=operator_id)
        progress = workflow.validate_materials(progress)

        return jsonify({
            'success': True,
            'operator_id': operator_id,
            'current_stage': progress.current_stage.value,
            'materials': {
                k: {
                    'name': v.name,
                    'status': v.status.value,
                    'required': v.required
                }
                for k, v in progress.materials.items()
            },
            'warnings': progress.warnings,
            'errors': progress.errors
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/workflow/<int:operator_id>/supplement', methods=['POST'])
def supplement_data(operator_id: int):
    """数据补充"""
    try:
        workflow = create_workflow()
        progress = workflow.start_workflow(operator_id=operator_id)
        progress = workflow.supplement_data(progress)

        return jsonify({
            'success': True,
            'operator_id': operator_id,
            'current_stage': progress.current_stage.value,
            'data_completeness': progress.data_completeness,
            'warnings': progress.warnings
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/workflow/<int:operator_id>/generate', methods=['POST'])
def generate_outputs(operator_id: int):
    """生成输出"""
    try:
        workflow = create_workflow()
        progress = workflow.start_workflow(operator_id=operator_id)
        progress = workflow.generate_outputs(progress)

        outputs = progress.metadata.get('outputs', {})

        return jsonify({
            'success': len(progress.errors) == 0,
            'operator_id': operator_id,
            'current_stage': progress.current_stage.value,
            'outputs': outputs,
            'warnings': progress.warnings,
            'errors': progress.errors
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/workflow/<int:operator_id>/complete', methods=['POST'])
def complete_workflow(operator_id: int):
    """完整工作流（一键完成）"""
    try:
        workflow = create_workflow()
        progress = workflow.start_workflow(operator_id=operator_id)

        # 执行完整流程
        if WorkflowStage.DATA_FUSION.value not in progress.completed_stages:
            progress = workflow.fuse_data(progress)

        if WorkflowStage.SUPPLEMENT.value not in progress.completed_stages:
            progress = workflow.supplement_data(progress)

        progress = workflow.validate_materials(progress)
        progress = workflow.generate_outputs(progress)

        outputs = progress.metadata.get('outputs', {})

        return jsonify({
            'success': len(progress.errors) == 0,
            'operator_id': operator_id,
            'current_stage': progress.current_stage.value,
            'outputs': outputs,
            'warnings': progress.warnings,
            'errors': progress.errors,
            'completeness': progress.data_completeness
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<path:filepath>')
def download_file(filepath):
    """下载文件"""
    try:
        # 安全检查：确保文件路径在允许的目录内
        safe_path = Path(filepath).resolve()
        allowed_dirs = [
            Path('generated_applications').resolve(),
            Path('archives').resolve(),
            Path('data/screenshots').resolve()
        ]

        if not any(str(safe_path).startswith(str(d)) for d in allowed_dirs):
            flash('文件路径不在允许范围内', 'error')
            return redirect(url_for('index'))

        if safe_path.exists():
            return send_file(str(safe_path), as_attachment=True)
        else:
            flash('文件不存在', 'error')
            return redirect(url_for('index'))

    except Exception as e:
        flash(f'下载失败: {e}', 'error')
        return redirect(url_for('index'))


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error_code=404, error_message="页面未找到"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500, error_message="服务器内部错误"), 500


# ==================== 启动 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("[OK] 市场监管智能体 v5.0 - 统一工作流 API")
    print("[OK] 版本: 5.0.0")
    print("[OK] 支持三输入源统一处理")
    print("=" * 60)
    print("[INFO] 访问地址: http://localhost:5000")
    print("[INFO] 按 Ctrl+C 停止服务")
    print("=" * 60)
    print()

    app.run(host='0.0.0.0', port=5000, debug=True)
