# ================================
# 智能文件整理助手
# 功能：自动整理文件夹中的文件到不同分类
# 作者：flyskyson
# ================================

# ========== 导入必要的工具箱 ==========
import os        # 操作系统工具箱：用于创建文件夹、检查文件存在等
import shutil    # 文件操作工具箱：用于移动文件
import sys       # 系统工具箱：用于退出程序
from datetime import datetime  # 时间工具箱：用于获取当前时间

# ========== 配置区域 ==========
# 设置要整理的文件夹路径（可以修改成你想要整理的任何文件夹）
folder_to_organize = "test_folder"

# ========== 人工确认环节 ==========
# 打印将要整理的文件夹信息
print(f"将要整理的文件夹: {folder_to_organize}")

# 显示整理规则，让用户了解如何分类
print("整理规则：")
print("  - PDF文件 -> PDF文件夹")
print("  - 图片文件 -> Images文件夹")
print("  - 办公文档 -> Documents文件夹")
print("  - 其他文件保持不变")

# 询问用户是否开始整理
# input() 函数会暂停程序，等待用户输入内容并按回车
user_confirm = input("是否开始整理？: ")

# 检查用户输入是否为 'y' 或 'Y'
# .lower() 把输入转为小写，所以 'Y' 和 'y' 都会被识别为确认
if user_confirm.lower() != 'y':
    print("取消整理。")
    sys.exit()  # 退出程序，不执行后续操作

# ========== 日志函数定义 ==========
def log_message(message):
    """
    记录消息到日志文件和屏幕

    参数:
        message (str): 要记录的消息内容

    功能:
        1. 在屏幕上打印消息
        2. 将消息追加写入到 organizer_log.txt 文件，并带上时间戳
    """
    # 获取当前日期和时间
    now = datetime.now()

    # 格式化时间为字符串：年-月-日 时:分:秒
    # 例如：2024-01-15 14:30:25
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")

    # 组合最终的日志行：[时间] 消息内容
    log_line = f"[{time_string}] {message}\n"

    # 在屏幕上打印消息（让用户实时看到）
    print(message)

    # 将日志写入文件
    # 'a' 表示追加模式（append），不会覆盖之前的日志
    # encoding='utf-8' 确保能正确处理中文字符
    with open("organizer_log.txt", 'a', encoding='utf-8') as log_file:
        log_file.write(log_line)

# ========== 文件分类规则 ==========
# 使用字典（dict）定义分类规则
# 格式：{"目标文件夹名": [文件扩展名列表]}
file_categories = {
    "PDF": [".pdf"],                      # PDF文件夹存放所有.pdf文件
    "Images": [".jpg", ".png"],           # Images文件夹存放.jpg和.png图片
    "Documents": [".docx", ".xlsx", ".doc"]  # Documents文件夹存放办公文档
}

# ========== 开始整理 ==========
# 初始化计数器，记录移动了多少个文件
moved_count = 0

# 遍历要整理的文件夹中的所有文件和子文件夹
# os.listdir() 返回文件夹中所有项目的名称列表
for filename in os.listdir(folder_to_organize):

    # 拼接完整的文件路径（文件夹路径 + 文件名）
    # 例如："test_folder" + "报告.pdf" = "test_folder/报告.pdf"
    file_path = os.path.join(folder_to_organize, filename)

    # 检查这个路径是否是一个文件（而不是文件夹）
    # os.path.isfile() 返回 True 如果是文件，False 如果是文件夹
    if os.path.isfile(file_path):

        # 提取文件的扩展名
        # os.path.splitext() 会将文件名拆分成（名称, 扩展名）两部分
        # 例如："报告.pdf" -> ("报告", ".pdf")
        # 用 _ 表示我们不需要文件名部分，只需要扩展名
        _, extension = os.path.splitext(filename)

        # 标记变量：记录是否找到了匹配的分类
        matched = False

        # 遍历所有分类规则，检查当前文件属于哪一类
        # .items() 会同时返回字典的键和值
        for category_name, extensions in file_categories.items():

            # 检查当前文件的扩展名是否在当前分类的扩展名列表中
            if extension in extensions:

                # 确定目标文件夹的完整路径
                # 例如："test_folder" + "PDF" = "test_folder/PDF"
                target_folder = os.path.join(folder_to_organize, category_name)

                # 检查目标文件夹是否存在
                if not os.path.exists(target_folder):
                    # 如果不存在，创建它
                    # os.makedirs() 可以创建多级文件夹
                    os.makedirs(target_folder)

                    # 记录到日志
                    log_message(f"创建文件夹: {category_name}")

                # ========== 处理重复文件名 ==========
                # 确定最终的目标文件完整路径
                target_file_path = os.path.join(target_folder, filename)

                # 检查目标位置是否已经存在同名文件
                if os.path.exists(target_file_path):

                    # 拆分文件名和扩展名
                    name, ext = os.path.splitext(filename)

                    # 尝试添加 "_副本" 后缀
                    # 例如："报告.pdf" -> "报告_副本.pdf"
                    new_filename = f"{name}_副本{ext}"
                    target_file_path = os.path.join(target_folder, new_filename)

                    # 如果 "_副本" 也存在，就添加数字 (1), (2), (3)...
                    copy_num = 1
                    # while循环：只要文件存在，就继续尝试新的名字
                    while os.path.exists(target_file_path):
                        new_filename = f"{name}_副本({copy_num}){ext}"
                        target_file_path = os.path.join(target_folder, new_filename)
                        copy_num += 1  # 数字递增

                    # 记录重命名信息到日志
                    log_message(f"检测到重复文件，重命名为: {new_filename}")

                # ========== 移动文件 ==========
                # 使用 shutil.move() 将文件从原位置移动到目标位置
                shutil.move(file_path, target_file_path)

                # 记录移动信息到日志
                log_message(f"移动: {filename} -> {category_name}/")

                # 计数器加1
                moved_count += 1

                # 标记已找到匹配的分类
                matched = True

                # 跳出内层循环（不需要再检查其他分类）
                break

        # 如果遍历完所有分类都没找到匹配
        if not matched:
            # 记录跳过信息（比如.txt文件不在分类规则中）
            log_message(f"跳过: {filename}（不在分类规则中）")

# ========== 整理完成摘要 ==========
# 打印分隔线（40个等号）
print("\n" + "="*40)

# 显示整理统计信息
print(f"整理完成：共移动了 {moved_count} 个文件")

# 打印结束分隔线
print("="*40)

# 将整理摘要记录到日志
log_message(f"整理完成：共移动了 {moved_count} 个文件")

# 提示用户可以整理其他文件夹
print('下次想整理那个文件夹？')

# ========== 程序结束 ==========
# 程序执行完毕，自动退出
