"""
最简单的网页抓取程序 - 第1版
功能：抓取一个网页，显示标题和内容长度
"""

import requests

def get_webpage(url):
    """获取网页内容"""
    print(f"正在访问: {url}")
    
    try:
        # 发送请求
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        
        print(f"✓ 成功获取网页!")
        print(f"状态码: {response.status_code}")
        print(f"网页大小: {len(response.text)} 字符")
        
        return response.text
        
    except Exception as e:
        print(f"✗ 获取失败: {e}")
        return None

def find_title(html):
    """从HTML中提取标题"""
    if not html:
        return "无标题"
    
    # 简单查找<title>标签
    if "<title>" in html and "</title>" in html:
        start = html.find("<title>") + 7
        end = html.find("</title>")
        title = html[start:end].strip()
        return title[:100]  # 只取前100个字符
    else:
        return "未找到标题"

# 主程序
if __name__ == "__main__":
    print("=== 简单网页抓取器 ===")
    print("正在测试...\n")
    
    # 测试网址（一个稳定的测试网站）
    test_url = "http://httpbin.org/html"
    
    # 获取网页
    html_content = get_webpage(test_url)
    
    if html_content:
        # 提取标题
        page_title = find_title(html_content)
        print(f"\n网页标题: {page_title}")
        
        # 显示前200个字符
        print(f"\n内容预览: {html_content[:200]}...")
        
        print("\n✓ 测试成功完成！")
    else:
        print("\n✗ 测试失败，请检查网络连接")