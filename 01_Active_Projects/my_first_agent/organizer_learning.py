# ================================
# 智能文件整理助手 - 学习版
# 功能：自动整理文件夹中的文件到不同分类
# 作者：flyskyson
#
# 本版本特点：
# - 详细注释每行代码的作用
# - 解释Python核心概念
# - 适合编程新手学习
# ================================

# ========== 导入必要的工具箱 ==========
# 在Python中，import 用于导入外部模块（别人写好的代码库）
# 模块就像工具箱，里面有很多现成的工具（函数）可以使用

import os        # 操作系统工具箱：用于创建文件夹、检查文件存在等
                # 常用功能：
                #   - os.listdir()       列出文件夹中的所有文件
                #   - os.path.join()     拼接文件路径
                #   - os.path.exists()   检查文件或文件夹是否存在
                #   - os.path.isfile()   检查是否是文件
                #   - os.makedirs()      创建文件夹

import shutil    # 文件操作工具箱：用于移动文件
                # 常用功能：
                #   - shutil.move()      移动文件到新位置
                #   - shutil.copy()      复制文件
                #   - shutil.rmtree()    删除整个文件夹

import sys       # 系统工具箱：用于退出程序
                # 常用功能：
                #   - sys.exit()         立即退出程序
                #   - sys.path           显示Python搜索路径

from datetime import datetime  # 时间工具箱：用于获取当前时间
                               # 常用功能：
                               #   - datetime.now()     获取当前时间
                               #   - .strftime()        格式化时间显示

# ========== 配置区域 ==========
# 变量：用于存储数据的容器
# folder_to_organize 是变量名，"test_folder" 是变量的值
# 设置要整理的文件夹路径（可以修改成你想要整理的任何文件夹）
# 例如：folder_to_organize = "C:/Users/你的用户名/Downloads"
folder_to_organize = "test_folder"


# ========== 人工确认环节 ==========
# 打印将要整理的文件夹信息
# f"" 叫做 f-string（格式化字符串），是Python 3.6+的特性
# {} 中的变量会被替换成实际值
# 例如：如果 folder_to_organize = "test_folder"
#       就会显示 "将要整理的文件夹: test_folder"
print(f"将要整理的文件夹: {folder_to_organize}")

# 显示整理规则，让用户了解如何分类
# print() 函数用于在屏幕上显示文字
print("整理规则：")
print("  - PDF文件 -> PDF文件夹")
print("  - 图片文件 -> Images文件夹")
print("  - 办公文档 -> Documents文件夹")
print("  - 其他文件保持不变")

# 询问用户是否开始整理
# input() 函数会暂停程序，等待用户输入内容并按回车键
# 用户输入的内容会被保存到变量 user_confirm 中
# 例如：用户输入 "y"，那么 user_confirm 的值就是字符串 "y"
user_confirm = input("是否开始整理？: ")

# 检查用户输入是否为 'y' 或 'Y'
# .lower() 是字符串方法，把输入转为小写
# 所以无论用户输入 'Y'、'y'、'Yy' 等，都会变成 'y'，方便判断
# != 是"不等于"的比较运算符
# 整句的意思是：如果用户输入的不是 'y'，就执行下面缩进的代码
if user_confirm.lower() != 'y':
    print("取消整理。")
    # sys.exit() 会立即结束程序，不执行后面的代码
    sys.exit()  # 退出程序，不执行后续操作


# ========== 日志函数定义 ==========
# def 关键字用于定义函数（自定义功能）
# 函数是一段可以重复使用的代码
# log_message 是函数名，后面括号里的 message 是参数（输入数据）
# 定义函数后，可以通过 log_message("消息内容") 来调用它
def log_message(message):
    """
    记录消息到日志文件和屏幕

    参数:
        message (str): 要记录的消息内容

    功能:
        1. 在屏幕上打印消息
        2. 将消息追加写入到 organizer_log.txt 文件，并带上时间戳

    返回:
        无（None）

    使用示例:
        log_message("创建文件夹: PDF")
        会显示: [2024-01-15 14:30:25] 创建文件夹: PDF
    """
    # 获取当前日期和时间
    # datetime.now() 返回一个包含当前时间的对象
    now = datetime.now()

    # 格式化时间为字符串：年-月-日 时:分:秒
    # strftime() 是"格式化时间"的函数
    # 格式化代码说明：
    #   %Y = 4位年份（2024）
    #   %m = 2位月份（01-12）
    #   %d = 2位日期（01-31）
    #   %H = 24小时制小时（00-23）
    #   %M = 分钟（00-59）
    #   %S = 秒（00-59）
    # 例如：2024-01-15 14:30:25
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")

    # 组合最终的日志行：[时间] 消息内容
    # \n 表示换行符，让每条日志占一行
    log_line = f"[{time_string}] {message}\n"

    # 在屏幕上打印消息（让用户实时看到）
    print(message)

    # 将日志写入文件
    # "organizer_log.txt" 是日志文件名
    # 'a' 表示追加模式（append），不会覆盖之前的日志，而是添加到末尾
    # 其他模式：
    #   'w' = 写入模式（会覆盖原文件）
    #   'r' = 只读模式
    # encoding='utf-8' 确保能正确处理中文字符
    # with open() as 语句会自动处理文件的打开和关闭，即使出错也会关闭
    # 这叫做"上下文管理器"，是Python的最佳实践
    with open("organizer_log.txt", 'a', encoding='utf-8') as log_file:
        log_file.write(log_line)  # 将日志行写入文件


# ========== 文件分类规则 ==========
# 使用字典（dict）定义分类规则
# 字典是Python中的一种数据结构，格式：{"键": "值"}
# 这里：{"目标文件夹名": [文件扩展名列表]}
# [] 表示列表（list），可以存放多个数据
file_categories = {
    "PDF": [".pdf"],                      # PDF文件夹存放所有.pdf文件
    "Images": [".jpg", ".png"],           # Images文件夹存放.jpg和.png图片
    "Documents": [".docx", ".xlsx", ".doc"]  # Documents文件夹存放办公文档
}
# 解释：
# - "PDF" 是键（key），也就是文件夹名称
# - [".pdf"] 是值（value），该文件夹接收的文件扩展名列表
# - 字典的查找速度很快，可以根据键快速找到对应的值
# - 你可以根据需要添加更多分类，例如：
#   "Videos": [".mp4", ".avi", ".mkv"],
#   "Music": [".mp3", ".wav"],
#   "Archives": [".zip", ".rar", ".7z"]


# ========== 开始整理 ==========
# 初始化计数器变量，记录移动了多少个文件
# = 是赋值符号，把右边的值 0 赋值给左边的变量 moved_count
# 在Python中，变量不需要声明类型，可以直接赋值
moved_count = 0

# for 循环：遍历（逐个处理）要整理的文件夹中的所有文件和子文件夹
# 循环是编程中非常重要的概念，用于重复执行相同的操作
# os.listdir() 返回文件夹中所有项目的名称列表
# 类似：["文件1.pdf", "图片.jpg", "文件夹A", "报告.docx"]
# for filename in ... 表示依次把每个文件名赋值给变量 filename
# 第一次循环：filename = "文件1.pdf"
# 第二次循环：filename = "图片.jpg"
# 以此类推...
for filename in os.listdir(folder_to_organize):

    # 拼接完整的文件路径（文件夹路径 + 文件名）
    # os.path.join() 会根据操作系统自动选择正确的路径分隔符
    # Windows 使用 "\"，Mac/Linux 使用 "/"
    # 这样可以确保代码在不同操作系统上都能正常工作
    # 例如："test_folder" + "报告.pdf" = "test_folder\报告.pdf"（Windows）
    file_path = os.path.join(folder_to_organize, filename)

    # 检查这个路径是否是一个文件（而不是文件夹）
    # os.path.isfile() 返回 True（是文件）或 False（不是文件，是文件夹）
    # 这一步很重要，因为我们只想处理文件，不想处理文件夹
    # if 语句用于条件判断，如果条件为 True，就执行缩进的代码
    if os.path.isfile(file_path):

        # 提取文件的扩展名
        # os.path.splitext() 会将文件名拆分成（名称, 扩展名）两部分
        # 返回的是一个元组（tuple），类似列表，但不可修改
        # 例如："报告.pdf" -> ("报告", ".pdf")
        # 例如："照片.jpg" -> ("照片", ".jpg")
        # 用 _ 表示我们不需要文件名部分，只需要扩展名
        # 这叫"解包赋值"，_ 是一个特殊的变量名，表示"这个值我不需要"
        _, extension = os.path.splitext(filename)

        # 标记变量：记录是否找到了匹配的分类
        # 初始值设为 False（表示还没有找到匹配）
        # 布尔值（boolean）只有两个值：True（真）或 False（假）
        matched = False

        # 内层 for 循环：遍历所有分类规则，检查当前文件属于哪一类
        # .items() 方法会同时返回字典的键和值
        # 第一次循环：category_name="PDF", extensions=[".pdf"]
        # 第二次循环：category_name="Images", extensions=[".jpg", ".png"]
        # 第三次循环：category_name="Documents", extensions=[".docx", ".xlsx", ".doc"]
        for category_name, extensions in file_categories.items():

            # 检查当前文件的扩展名是否在当前分类的扩展名列表中
            # in 是"包含"的意思，用于判断某个元素是否在列表中
            # 例如：".pdf" in [".pdf"] → True（在列表中）
            #       ".jpg" in [".pdf"] → False（不在列表中）
            #       ".png" in [".jpg", ".png"] → True（在列表中）
            if extension in extensions:

                # 确定目标文件夹的完整路径
                # 例如："test_folder" + "PDF" = "test_folder\PDF"
                target_folder = os.path.join(folder_to_organize, category_name)

                # 检查目标文件夹是否存在
                # not 是"非"的意思，也叫逻辑非运算符
                # not True = False, not False = True
                # 整句的意思：如果目标文件夹不存在
                if not os.path.exists(target_folder):

                    # 如果不存在，创建它
                    # os.makedirs() 可以创建多级文件夹
                    # 例如：创建 "a/b/c" 这样的嵌套文件夹
                    os.makedirs(target_folder)

                    # 记录到日志（调用我们之前定义的函数）
                    log_message(f"创建文件夹: {category_name}")

                # ========== 处理重复文件名 ==========
                # 确定最终的目标文件完整路径
                target_file_path = os.path.join(target_folder, filename)

                # 检查目标位置是否已经存在同名文件
                if os.path.exists(target_file_path):

                    # 拆分文件名和扩展名
                    # 这次两个值都需要，所以用 name 和 ext 两个变量接收
                    name, ext = os.path.splitext(filename)

                    # 尝试添加 "_副本" 后缀
                    # 例如："报告.pdf" -> "报告_副本.pdf"
                    # f-string 可以组合多个变量，非常方便
                    new_filename = f"{name}_副本{ext}"
                    target_file_path = os.path.join(target_folder, new_filename)

                    # 如果 "_副本" 也存在，就添加数字 (1), (2), (3)...
                    copy_num = 1  # 初始数字为 1

                    # while 循环：只要条件为 True，就一直执行循环体
                    # 这里：只要文件存在，就继续尝试新的名字
                    # 这种循环方式叫做"当循环"，和 for 循环不同
                    # for 循环用于已知次数的循环，while 循环用于未知次数
                    while os.path.exists(target_file_path):
                        # 生成新名字，例如："报告_副本(1).pdf"
                        new_filename = f"{name}_副本({copy_num}){ext}"
                        target_file_path = os.path.join(target_folder, new_filename)
                        copy_num += 1  # copy_num = copy_num + 1，数字递增
                        # += 是加法赋值运算符，先加后赋值

                    # 记录重命名信息到日志
                    log_message(f"检测到重复文件，重命名为: {new_filename}")

                # ========== 移动文件 ==========
                # 使用 shutil.move() 将文件从原位置移动到目标位置
                # 参数1：源文件路径（file_path）
                # 参数2：目标文件路径（target_file_path）
                # 移动操作会改变文件的位置，但不会创建副本
                shutil.move(file_path, target_file_path)

                # 记录移动信息到日志
                log_message(f"移动: {filename} -> {category_name}/")

                # 计数器加1
                # moved_count = moved_count + 1 的简写
                # 这种写法更简洁，是Python的常见写法
                moved_count += 1

                # 标记已找到匹配的分类
                matched = True

                # break 跳出当前循环
                # 跳出内层循环（不需要再检查其他分类）
                # 因为一个文件只能属于一个分类，找到匹配后就可以停止了
                # 如果不break，程序会继续检查其他分类，浪费性能
                break

        # 如果遍历完所有分类都没找到匹配
        # not matched = not True = False
        # 如果 matched 还是 False，说明没有找到匹配
        if not matched:
            # 记录跳过信息（比如.txt文件不在分类规则中）
            log_message(f"跳过: {filename}（不在分类规则中）")


# ========== 整理完成摘要 ==========
# 打印分隔线（40个等号）
# * 号用于重复字符串
# "="*40 = "========================================"
# "\n" 是换行符，在分隔线前加一个空行
print("\n" + "="*40)

# 显示整理统计信息
# f-string 会将变量 moved_count 的值插入到字符串中
# 例如：moved_count = 5，显示为 "整理完成：共移动了 5 个文件"
print(f"整理完成：共移动了 {moved_count} 个文件")

# 打印结束分隔线
print("="*40)

# 将整理摘要记录到日志
# 再次调用 log_message 函数，把统计信息写入日志文件
log_message(f"整理完成：共移动了 {moved_count} 个文件")

# 提示用户可以整理其他文件夹
print('下次想整理那个文件夹？')

# ========== 程序结束 ==========
# 程序执行到这里就结束了，会自动退出
# 不需要写 return 或 exit()，Python 会自动处理
# 在脚本的末尾，程序会自然结束


# ========== 学习要点总结 ==========
"""
本脚本涵盖的Python核心概念：

1. 变量和数据类型
   - 字符串 (str)：文本数据，如 "hello"
   - 整数 (int)：数字，如 42
   - 布尔值 (bool)：True 或 False
   - 列表 (list)：[1, 2, 3]
   - 字典 (dict)：{"key": "value"}
   - 元组 (tuple)：(1, 2)

2. 运算符
   - 赋值：=
   - 比较：==, !=, <, >, <=, >=
   - 逻辑：and, or, not
   - 成员：in, not in
   - 算术：+, -, *, /, %, **
   - 赋值简写：+=, -=, *=, /=

3. 控制流
   - if 语句：条件判断
   - for 循环：遍历序列
   - while 循环：条件循环
   - break：跳出循环
   - continue：跳过本次循环

4. 函数
   - def 定义函数
   - 参数传递
   - 返回值 (return)
   - 函数调用

5. 文件操作
   - open() 打开文件
   - read() 读取
   - write() 写入
   - close() 关闭（with自动处理）
   - 文件模式：'r', 'w', 'a'

6. 字符串操作
   - f-string：格式化字符串
   - .lower()：转小写
   - .upper()：转大写
   - .split()：分割字符串
   - .strip()：去除两端空白

7. 模块导入
   - import module
   - from module import something
   - import module as alias

8. 代码风格
   - 缩进：Python使用4个空格缩进
   - 注释：# 单行注释，""" """ 多行注释
   - 变量命名：snake_case（小写+下划线）
   - 函数命名：snake_case

9. 最佳实践
   - 使用 with 语句管理文件
   - 函数要有文档字符串
   - 代码要有注释
   - 变量名要有意义
   - 避免硬编码，使用变量

10. 错误处理（本脚本未展示）
    - try-except：捕获异常
    - raise：抛出异常

继续学习建议：
1. 修改分类规则，添加新的文件类型
2. 尝试整理不同的文件夹
3. 添加更多的日志信息
4. 学习异常处理，让程序更健壮
5. 尝试添加命令行参数支持
"""
