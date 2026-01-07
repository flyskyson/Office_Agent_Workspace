# ================================
# 智能文件整理助手
# 功能：自动整理文件夹中的文件到不同分类
# 作者：flyskyson
# ================================

# ========== 导入必要的工具箱 ==========
import os        # 操作系统工具箱：用于创建文件夹、检查文件存在等
                # 常用功能：os.listdir（列出文件）、os.path.join（拼接路径）
import shutil    # 文件操作工具箱：用于移动文件
                # 常用功能：shutil.move（移动文件）
import sys       # 系统工具箱：用于退出程序
                # 常用功能：sys.exit（退出程序）
from datetime import datetime  # 时间工具箱：用于获取当前时间
                               # 常用功能：datetime.now（获取现在的时间）

# ========== 配置区域 ==========
# 设置要整理的文件夹路径（可以修改成你想要整理的任何文件夹）
# 例如：folder_to_organize = "C:/Users/你的用户名/Downloads"
folder_to_organize = "test_folder"

# ========== 人工确认环节 ==========
# 打印将要整理的文件夹信息
# f"" 叫做 f-string（格式化字符串），{} 中的变量会被替换成实际值
# 例如：如果 folder_to_organize = "test_folder"，就会显示 "将要整理的文件夹: test_folder"
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
# 例如：用户输入 "y"，那么 user_confirm 的值就是 "y"
user_confirm = input("是否开始整理？: ")

# 检查用户输入是否为 'y' 或 'Y'
# .lower() 是字符串方法，把输入转为小写
# 所以无论用户输入 'Y' 还是 'y'，都会变成 'y'，方便判断
# != 是"不等于"的意思
# 整句的意思是：如果用户输入的不是 'y'，就执行下面缩进的代码
if user_confirm.lower() != 'y':
    print("取消整理。")
    # sys.exit() 会立即结束程序，不执行后面的代码
    sys.exit()  # 退出程序，不执行后续操作

# ========== 日志函数定义 ==========
# def 关键字用于定义函数（自定义功能）
# log_message 是函数名，后面括号里的 message 是参数（输入数据）
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
    """
    # 获取当前日期和时间
    # datetime.now() 返回一个包含当前时间的对象
    now = datetime.now()

    # 格式化时间为字符串：年-月-日 时:分:秒
    # strftime() 是"格式化时间"的函数
    # %Y = 4位年份（2024），%m = 2位月份（01），%d = 2位日期（15）
    # %H = 24小时制小时（14），%M = 分钟（30），%S = 秒（25）
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
    # encoding='utf-8' 确保能正确处理中文字符
    # with open() as 语句会自动处理文件的打开和关闭，即使出错也会关闭
    with open("organizer_log.txt", 'a', encoding='utf-8') as log_file:
        log_file.write(log_line)  # 将日志行写入文件

# ========== 文件分类规则 ==========
# 使用字典（dict）定义分类规则
# 字典格式：{"键": "值"}
# 这里：{"目标文件夹名": [文件扩展名列表]}
# [] 表示列表（list），可以存放多个数据
file_categories = {
    "PDF": [".pdf"],                      # PDF文件夹存放所有.pdf文件
    "Images": [".jpg", ".png"],           # Images文件夹存放.jpg和.png图片
    "Documents": [".docx", ".xlsx", ".doc"]  # Documents文件夹存放办公文档
}
# 解释：
# - "PDF" 是键（文件夹名称）
# - [".pdf"] 是值（该文件夹接收的文件扩展名列表）
# - 你可以根据需要添加更多分类，例如：
#   "Videos": [".mp4", ".avi", ".mkv"],
#   "Music": [".mp3", ".wav"]

# ========== 开始整理 ==========
# 初始化计数器变量，记录移动了多少个文件
# = 是赋值符号，把 0 赋值给变量 moved_count
moved_count = 0

# for 循环：遍历（逐个处理）要整理的文件夹中的所有文件和子文件夹
# os.listdir() 返回文件夹中所有项目的名称列表（类似 ["文件1.pdf", "图片.jpg", "文件夹A"]）
# for filename in ... 表示依次把每个文件名赋值给变量 filename
for filename in os.listdir(folder_to_organize):

    # 拼接完整的文件路径（文件夹路径 + 文件名）
    # os.path.join() 会根据操作系统自动选择正确的路径分隔符
    # Windows 用 "\"，Mac/Linux 用 "/"
    # 例如："test_folder" + "报告.pdf" = "test_folder\报告.pdf"（Windows）
    file_path = os.path.join(folder_to_organize, filename)

    # 检查这个路径是否是一个文件（而不是文件夹）
    # os.path.isfile() 返回 True（是文件）或 False（不是文件，是文件夹）
    # 这一步很重要，因为我们只想处理文件，不想处理文件夹
    if os.path.isfile(file_path):

        # 提取文件的扩展名
        # os.path.splitext() 会将文件名拆分成（名称, 扩展名）两部分
        # 例如："报告.pdf" -> ("报告", ".pdf")
        # 例如："照片.jpg" -> ("照片", ".jpg")
        # 用 _ 表示我们不需要文件名部分，只需要扩展名
        # 这叫"解包赋值"，_ 是一个特殊的变量名，表示"这个值我不需要"
        _, extension = os.path.splitext(filename)

        # 标记变量：记录是否找到了匹配的分类
        # 初始值设为 False（表示还没有找到匹配）
        matched = False

        # 内层 for 循环：遍历所有分类规则，检查当前文件属于哪一类
        # .items() 方法会同时返回字典的键和值
        # 例如：第一次循环：category_name="PDF", extensions=[".pdf"]
        #      第二次循环：category_name="Images", extensions=[".jpg", ".png"]
        for category_name, extensions in file_categories.items():

            # 检查当前文件的扩展名是否在当前分类的扩展名列表中
            # in 是"包含"的意思
            # 例如：".pdf" in [".pdf"] → True
            #       ".jpg" in [".pdf"] → False
            if extension in extensions:

                # 确定目标文件夹的完整路径
                # 例如："test_folder" + "PDF" = "test_folder\PDF"
                target_folder = os.path.join(folder_to_organize, category_name)

                # 检查目标文件夹是否存在
                # not 是"非"的意思，not True = False, not False = True
                if not os.path.exists(target_folder):
                    # 如果不存在，创建它
                    # os.makedirs() 可以创建多级文件夹
                    # exist_ok=True 表示如果文件夹已存在，不会报错
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
                    # f-string 可以组合多个变量
                    new_filename = f"{name}_副本{ext}"
                    target_file_path = os.path.join(target_folder, new_filename)

                    # 如果 "_副本" 也存在，就添加数字 (1), (2), (3)...
                    copy_num = 1  # 初始数字为 1
                    # while 循环：只要条件为 True，就一直执行
                    # 这里：只要文件存在，就继续尝试新的名字
                    while os.path.exists(target_file_path):
                        # 生成新名字，例如："报告_副本(1).pdf"
                        new_filename = f"{name}_副本({copy_num}){ext}"
                        target_file_path = os.path.join(target_folder, new_filename)
                        copy_num += 1  # copy_num = copy_num + 1，数字递增

                    # 记录重命名信息到日志
                    log_message(f"检测到重复文件，重命名为: {new_filename}")

                # ========== 移动文件 ==========
                # 使用 shutil.move() 将文件从原位置移动到目标位置
                # 参数1：源文件路径，参数2：目标文件路径
                shutil.move(file_path, target_file_path)

                # 记录移动信息到日志
                log_message(f"移动: {filename} -> {category_name}/")

                # 计数器加1
                # moved_count = moved_count + 1 的简写
                moved_count += 1

                # 标记已找到匹配的分类
                matched = True

                # break 跳出当前循环
                # 跳出内层循环（不需要再检查其他分类）
                # 因为一个文件只能属于一个分类
                break

        # 如果遍历完所有分类都没找到匹配
        # not matched = not True = False
        # 如果 matched 还是 False，说明没有找到匹配
        if not matched:
            # 记录跳过信息（比如.txt文件不在分类规则中）
            log_message(f"跳过: {filename}（不在分类规则中）")

# ========== 整理完成摘要 ==========
# 打印分隔线（40个等号）
# * 号用于重复字符串，"="*40 = "========================================"
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
