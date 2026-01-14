#!/usr/bin/env python3
"""测试 Flask POST 请求"""

from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        print(f"[DEBUG] 收到POST请求!")
        print(f"[DEBUG] Form数据: {dict(request.form)}")
        return "POST SUCCESS"
    return '''
    <form method="POST">
        <input name="test_field" value="test_value">
        <button type="submit">提交</button>
    </form>
    '''

if __name__ == '__main__':
    print("启动测试服务器...")
    app.run(port=5001, debug=True)
