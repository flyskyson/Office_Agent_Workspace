#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习记忆助手 - Flask Web UI (Demo Mode)
演示版本 - 不需要加载模型
"""

import sys
import os
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 确保项目根目录在路径最前面
project_root = Path(__file__).parent.parent
project_root_str = str(project_root)
if project_root_str in sys.path:
    sys.path.remove(project_root_str)
sys.path.insert(0, project_root_str)

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime

# 创建 Flask 应用
app = Flask(__name__)
app.secret_key = 'memory-agent-2026-demo'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# ==================== 模拟数据（演示用） ====================

class DemoIndexer:
    """演示索引器"""
    def __init__(self):
        self.docs = [
            {'path': 'test1.py', 'content': 'Python file operation example', 'metadata': {'type': 'code'}},
            {'path': 'test2.md', 'content': 'Flask web development notes', 'metadata': {'type': 'note'}},
        ]

    def count(self):
        return len(self.docs)


class DemoScheduler:
    """演示调度器"""
    def __init__(self):
        self.reviews = []

    def get_due_reviews(self):
        return self.reviews

    def format_statistics(self):
        return "Demo mode - 0 reviews pending"


# 初始化演示组件
indexer = DemoIndexer()
scheduler = DemoScheduler()


# ==================== 模板过滤器 ====================

@app.template_filter('datetime')
def format_datetime(timestamp):
    """格式化时间戳"""
    if isinstance(timestamp, str):
        return timestamp
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return timestamp


@app.template_filter('truncate')
def truncate_text(text, length=200):
    """截断文本"""
    if not text:
        return ''
    if len(text) <= length:
        return text
    return text[:length] + '...'


# ==================== 路由 ====================

@app.route('/')
def index():
    """首页"""
    stats = {
        'total_docs': indexer.count(),
        'due_reviews': len(scheduler.get_due_reviews()),
        'last_index': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    return render_template('index.html', stats=stats)


@app.route('/search')
def search_page():
    """搜索页面"""
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'all')
    results = []

    if query:
        # 演示搜索结果
        results = [
            {
                'content': f'Demo result for "{query}" - This is a sample search result showing the UI layout...',
                'metadata': {'type': 'demo', 'path': 'demo/file.py'},
                'similarity': 0.85,
                'path': 'demo/file.py'
            }
        ]

    return render_template('search.html',
                          query=query,
                          search_type=search_type,
                          results=results)


@app.route('/similar')
def similar_page():
    """相似问题页面"""
    problem = request.args.get('problem', '')
    similar_problems = []

    if problem:
        similar_problems = [
            {
                'title': f'Similar to "{problem}"',
                'description': 'This is a demo result showing how similar problems would be displayed...',
                'similarity': 0.78,
                'solution': 'Try checking the file path and permissions'
            }
        ]

    return render_template('similar.html',
                          problem=problem,
                          similar_problems=similar_problems)


@app.route('/learning')
def learning_page():
    """学习路径页面"""
    topic = request.args.get('topic', '')
    learning_path = []

    if topic:
        learning_path = [
            {'title': f'Learn {topic} - Step 1', 'description': 'Get started with basics', 'source': 'demo'}
        ]

    return render_template('learning.html',
                          topic=topic,
                          learning_path=learning_path)


@app.route('/review')
def review_page():
    """复习页面"""
    return render_template('review.html',
                          due_reviews=[],
                          stats='Demo mode - No reviews scheduled')


@app.route('/manage')
def manage_page():
    """管理页面"""
    db_stats = {'total': indexer.count()}
    return render_template('manage.html',
                          db_stats=db_stats,
                          recent_docs=[])


@app.route('/manage/index', methods=['POST'])
def rebuild_index():
    """重建索引（演示版）"""
    flash('演示模式 - 索引重建功能不可用', 'info')
    return redirect(url_for('manage_page'))


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    """404 错误"""
    return render_template('error.html',
                          error_code=404,
                          error_message='页面不存在'), 404


@app.errorhandler(500)
def server_error(error):
    """500 错误"""
    return render_template('error.html',
                          error_code=500,
                          error_message='服务器内部错误'), 500


# ==================== 启动 ====================

def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("Memory Agent - Web UI (DEMO MODE)")
    print("=" * 70)
    print("\n[INFO] Starting server in demo mode (no models required)")
    print("[INFO] This is for UI testing only")
    print("\n[INFO] Server running at: http://127.0.0.1:5555")
    print("[INFO] Press Ctrl+C to stop\n")

    app.run(
        host='127.0.0.1',
        port=5555,
        debug=True
    )


if __name__ == '__main__':
    main()
