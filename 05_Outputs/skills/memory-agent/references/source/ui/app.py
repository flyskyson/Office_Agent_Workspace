#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习记忆助手 - Flask Web UI
提供现代化的 Web 界面进行语义搜索和知识管理
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

# 导入核心模块（延迟导入）
from indexer import DocumentIndexer
from search import SemanticSearch
from recommender import SmartRecommender
from review_scheduler import ReviewScheduler

# 创建 Flask 应用
app = Flask(__name__)
app.secret_key = 'memory-agent-2026-web-ui'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 延迟初始化核心组件（懒加载）
indexer = None
search_engine = None
recommender = None
scheduler = None


def get_components():
    """获取核心组件（延迟初始化）"""
    global indexer, search_engine, recommender, scheduler
    if indexer is None:
        print("[INIT] Initializing components...")
        try:
            indexer = DocumentIndexer()
            search_engine = SemanticSearch()
            recommender = SmartRecommender()
            scheduler = ReviewScheduler()
            print("[OK] Components initialized")
        except Exception as e:
            print(f"[ERROR] Failed to initialize: {e}")
            # 创建默认组件
            indexer = DocumentIndexer.__new__(DocumentIndexer)
            indexer.vector_store = type('obj', (object,), {'count': lambda: 0})()
            search_engine = SemanticSearch.__new__(SemanticSearch)
            recommender = SmartRecommender.__new__(SmartRecommender)
            scheduler = ReviewScheduler.__new__(ReviewScheduler)
    return indexer, search_engine, recommender, scheduler


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
    # 获取统计信息（延迟加载）
    indexer_local, _, scheduler_local, _ = get_components()
    stats = {
        'total_docs': indexer_local.vector_store.count(),
        'due_reviews': len(scheduler_local.get_due_reviews()) if hasattr(scheduler_local, 'get_due_reviews') else 0,
        'last_index': get_last_index_time()
    }
    return render_template('index.html', stats=stats)


@app.route('/search')
def search_page():
    """搜索页面"""
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'all')  # all, code, notes
    results = []

    if query:
        try:
            if search_type == 'code':
                results = search_engine.search_code(query)
            elif search_type == 'notes':
                results = search_engine.search_notes(query)
            else:
                results = search_engine.search(query)

            # 格式化结果
            formatted_results = []
            for r in results:
                formatted_results.append({
                    'content': r.get('content', '')[:500],
                    'metadata': r.get('metadata', {}),
                    'similarity': r.get('similarity', 0),
                    'path': r.get('metadata', {}).get('path', '')
                })
            results = formatted_results

        except Exception as e:
            flash(f'搜索出错: {str(e)}', 'error')

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
        try:
            similar_problems = recommender.find_similar_problems(problem)
        except Exception as e:
            flash(f'查找相似问题出错: {str(e)}', 'error')

    return render_template('similar.html',
                          problem=problem,
                          similar_problems=similar_problems)


@app.route('/learning')
def learning_page():
    """学习路径页面"""
    topic = request.args.get('topic', '')
    learning_path = []

    if topic:
        try:
            learning_path = recommender.get_learning_path(topic)
        except Exception as e:
            flash(f'生成学习路径出错: {str(e)}', 'error')

    return render_template('learning.html',
                          topic=topic,
                          learning_path=learning_path)


@app.route('/review')
def review_page():
    """复习页面"""
    due_reviews = scheduler.get_due_reviews()
    stats = scheduler.format_statistics()

    return render_template('review.html',
                          due_reviews=due_reviews,
                          stats=stats)


@app.route('/review/<int:review_id>/rate', methods=['POST'])
def rate_review(review_id):
    """评分复习"""
    try:
        rating = int(request.form.get('rating', 0))
        if 0 <= rating <= 5:
            scheduler.rate_review(review_id, rating)
            flash('评分成功！下次复习时间已更新', 'success')
        else:
            flash('评分必须在 0-5 之间', 'error')
    except Exception as e:
        flash(f'评分失败: {str(e)}', 'error')

    return redirect(url_for('review_page'))


@app.route('/manage')
def manage_page():
    """管理页面"""
    try:
        db_stats = {
            'total': indexer.vector_store.count(),
        }

        # 获取最近索引的文档
        recent_docs = get_recent_documents(limit=10)

    except Exception as e:
        flash(f'加载数据出错: {str(e)}', 'error')
        db_stats = {'total': 0}
        recent_docs = []

    return render_template('manage.html',
                          db_stats=db_stats,
                          recent_docs=recent_docs)


@app.route('/manage/index', methods=['POST'])
def rebuild_index():
    """重建索引"""
    try:
        flash('开始构建索引，这可能需要几分钟...', 'info')
        indexer.build_index()
        flash('索引构建完成！', 'success')
    except Exception as e:
        flash(f'构建索引失败: {str(e)}', 'error')

    return redirect(url_for('manage_page'))


@app.route('/api/search', methods=['POST'])
def api_search():
    """API: 搜索接口"""
    data = request.get_json()
    query = data.get('query', '')
    search_type = data.get('type', 'all')

    if not query:
        return jsonify({'error': '查询不能为空'}), 400

    try:
        if search_type == 'code':
            results = search_engine.search_code(query)
        elif search_type == 'notes':
            results = search_engine.search_notes(query)
        else:
            results = search_engine.search(query)

        return jsonify({
            'success': True,
            'results': results[:10]  # 限制返回10条
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/similar', methods=['POST'])
def api_similar():
    """API: 相似问题接口"""
    data = request.get_json()
    problem = data.get('problem', '')

    if not problem:
        return jsonify({'error': '问题描述不能为空'}), 400

    try:
        results = recommender.find_similar_problems(problem)
        return jsonify({
            'success': True,
            'results': results[:5]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== 辅助函数 ====================

def get_last_index_time():
    """获取最后索引时间"""
    try:
        import time
        db_path = project_root / '..' / '06_Learning_Journal' / 'workspace_memory' / 'chroma_db'
        if db_path.exists():
            # 获取目录最后修改时间
            timestamp = db_path.stat().st_mtime
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        return '从未索引'
    except:
        return '未知'


def get_recent_documents(limit=10):
    """获取最近索引的文档"""
    try:
        # 这里需要根据实际的向量存储实现来获取
        # 暂时返回空列表
        return []
    except:
        return []


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
    print("🧠 学习记忆助手 - Web UI")
    print("=" * 70)
    print("\n🚀 启动服务器...")
    print("📱 访问地址: http://127.0.0.1:5555")
    print("⏹️  按 Ctrl+C 停止服务器\n")

    app.run(
        host='127.0.0.1',
        port=5555,
        debug=True
    )


if __name__ == '__main__':
    main()
