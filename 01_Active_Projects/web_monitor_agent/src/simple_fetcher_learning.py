"""
=====================================================
网页抓取程序 - 学习详解版
=====================================================
本程序适合Python初学者，包含详细的注释说明
每一步都有解释，帮助你理解网页抓取的基本原理

功能：
    1. 访问一个网址
    2. 获取网页的HTML内容
    3. 从HTML中提取有用的信息（标题、链接等）
"""

# ============================================
# 第一步：导入需要的库
# ============================================
import requests  # 这是一个用来发送HTTP请求的库（就像浏览器访问网站一样）

# ============================================
# 第二步：定义功能函数
# ============================================

def get_webpage(url):
    """
    获取网页内容的核心函数

    参数:
        url (str): 要访问的网址，例如 "https://www.baidu.com"

    返回:
        str: 网页的HTML内容（文本格式），如果失败则返回None
    """

    # ========== 1. 打印提示信息 ==========
    print(f"🌐 正在访问: {url}")
    print("-" * 50)  # 打印一条分隔线让输出更清晰

    # ========== 2. 使用try-except处理错误 ==========
    # try: 尝试执行代码
    # except: 如果发生错误，执行这里的代码
    try:

        # ---------- 发送HTTP请求 ----------
        # requests.get() 就像你在浏览器地址栏输入网址并按回车
        # timeout=10 表示最多等待10秒，防止一直卡住
        response = requests.get(url, timeout=10)

        # ---------- 设置编码 ----------
        # encoding='utf-8' 告诉程序如何正确显示中文等字符
        response.encoding = 'utf-8'

        # ---------- 检查请求是否成功 ----------
        # status_code 是HTTP状态码
        # 200 = 成功
        # 404 = 页面不存在
        # 500 = 服务器错误
        if response.status_code == 200:
            print(f"✅ 请求成功！状态码: {response.status_code}")
        else:
            print(f"⚠️  请求完成但状态码异常: {response.status_code}")

        # ---------- 显示网页信息 ----------
        # len(response.text) 计算网页内容的字符数
        print(f"📄 网页大小: {len(response.text)} 字符")

        # ---------- 返回网页内容 ----------
        # response.text 是网页的HTML代码（文本形式）
        return response.text

    # ========== 3. 捕获可能出现的错误 ==========
    except requests.exceptions.Timeout:
        # 超时错误：网络太慢或服务器无响应
        print("❌ 超时错误：网站响应时间过长")
        return None

    except requests.exceptions.ConnectionError:
        # 连接错误：网址不存在、网络断开等
        print("❌ 连接错误：无法连接到该网站")
        return None

    except Exception as e:
        # 其他未知错误
        print(f"❌ 发生错误: {e}")
        return None


def find_title(html):
    """
    从HTML代码中提取网页标题

    参数:
        html (str): 网页的HTML代码

    返回:
        str: 网页标题文字

    HTML标题格式: <title>网页标题</title>
    """

    # ========== 1. 检查HTML是否为空 ==========
    if not html:
        return "❌ 无内容"

    # ========== 2. 查找<title>标签 ==========
    # HTML中标题是这样写的：<title>百度一下，你就知道</title>

    # 先检查是否包含<title>标签
    if "<title>" in html and "</title>" in html:

        # ---------- find() 方法说明 ----------
        # html.find("<title>") 返回 "<title>" 在文本中的起始位置
        # +7 是因为 "<title>" 这个标签有7个字符，我们要跳过它
        start = html.find("<title>") + 7

        # 找到结束标签 </title> 的位置
        end = html.find("</title>")

        # ---------- 切片提取标题 ----------
        # html[start:end] 提取从start到end之间的文字
        title = html[start:end].strip()  # strip() 去掉首尾的空格和换行

        # 只取前100个字符，防止标题太长
        return title[:100]

    else:
        return "❌ 未找到标题标签"


def find_links(html):
    """
    从HTML中提取所有链接（进阶功能）

    参数:
        html (str): 网页的HTML代码

    返回:
        list: 包含所有链接地址的列表

    HTML链接格式: <a href="https://www.example.com">链接文字</a>
    """

    if not html:
        return []

    links = []

    # ========== 简单的链接提取 ==========
    # 查找所有 href=" 的位置
    start_pos = 0
    while True:
        # 查找 href="
        pos = html.find('href="', start_pos)
        if pos == -1:  # 找不到了，结束循环
            break

        # 提取链接地址（从 href=" 后面开始）
        link_start = pos + 6  # href=" 有6个字符
        link_end = html.find('"', link_start)  # 找下一个引号

        if link_end != -1:
            link = html[link_start:link_end]
            # 只保留http开头的链接（过滤掉JavaScript、锚点等）
            if link.startswith('http'):
                links.append(link)

        # 继续往后查找
        start_pos = link_end

    return links


# ============================================
# 第三步：主程序（程序入口）
# ============================================

if __name__ == "__main__":
    """
    __name__ == "__main__" 的解释：
    - 当你直接运行这个文件时，__name__ 的值是 "__main__"
    - 当你从其他文件导入这个文件时，__name__ 的值是文件名
    - 这样可以确保只有在直接运行时才执行下面的代码
    """

    print("=" * 60)
    print("🌟 网页抓取器 - 学习版")
    print("=" * 60)
    print()

    # ========== 1. 设置测试网址 ==========
    # httpbin.org 是一个专门用于测试的网站
    test_url = "http://httpbin.org/html"
    print(f"📍 目标网址: {test_url}")
    print()

    # ========== 2. 获取网页内容 ==========
    print("【第1步】正在获取网页...")
    html_content = get_webpage(test_url)
    print()

    # ========== 3. 处理网页内容 ==========
    if html_content:  # 如果成功获取到内容

        # ---------- 提取标题 ----------
        print("【第2步】提取网页标题...")
        page_title = find_title(html_content)
        print(f"📌 标题: {page_title}")
        print()

        # ---------- 提取链接（可选）----------
        print("【第3步】查找网页中的链接...")
        all_links = find_links(html_content)
        print(f"🔗 找到 {len(all_links)} 个链接")
        if all_links:
            for i, link in enumerate(all_links[:5], 1):  # 只显示前5个
                print(f"   {i}. {link}")
            if len(all_links) > 5:
                print(f"   ... 还有 {len(all_links) - 5} 个链接")
        print()

        # ---------- 显示内容预览 ----------
        print("【第4步】内容预览（前300个字符）...")
        print("-" * 50)
        print(html_content[:300])
        print("...")
        print("-" * 50)
        print()

        # ========== 4. 成功提示 ==========
        print("✅ 程序执行成功！")
        print()
        print("💡 学习提示：")
        print("   - HTML是网页的源代码")
        print("   - response.text 获取完整的HTML")
        print("   - 我们可以用字符串方法查找和提取信息")
        print("   - 进阶学习：可以使用BeautifulSoup库更方便地解析HTML")

    else:
        # ========== 5. 失败提示 ==========
        print("❌ 程序执行失败")
        print()
        print("💡 可能的原因：")
        print("   - 网络连接断开")
        print("   - 网址不正确")
        print("   - 网站服务器故障")
        print("   - 防火墙阻止了连接")

    print()
    print("=" * 60)
    print("程序结束")
    print("=" * 60)
