import os
import shutil
import sys
from datetime import datetime

# 设置要整理的文件夹路径
folder_to_organize = "test_folder"

# 人工确认
print(f"将要整理的文件夹: {folder_to_organize}")
print("整理规则：")
print("  - PDF文件 -> PDF文件夹")
print("  - 图片文件 -> Images文件夹")
print("  - 办公文档 -> Documents文件夹")
print("  - 其他文件保持不变")

user_confirm = input("是否开始整理？: ")

if user_confirm.lower() != 'y':
    print("取消整理。")
    sys.exit()

# 日志函数
def log_message(message):
    """记录消息到日志文件和屏幕"""
    now = datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{time_string}] {message}\n"
    
    print(message)
    
    with open("organizer_log.txt", 'a', encoding='utf-8') as log_file:
        log_file.write(log_line)

# 定义文件分类规则
file_categories = {
    "PDF": [".pdf"],
    "Images": [".jpg", ".png"],
    "Documents": [".docx", ".xlsx", ".doc"]
}

# 计数器
moved_count = 0

# 遍历文件夹
for filename in os.listdir(folder_to_organize):
    file_path = os.path.join(folder_to_organize, filename)
    
    if os.path.isfile(file_path):
        _, extension = os.path.splitext(filename)
        matched = False
        
        for category_name, extensions in file_categories.items():
            if extension in extensions:
                target_folder = os.path.join(folder_to_organize, category_name)
                
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                    log_message(f"创建文件夹: {category_name}")
                
                # 处理重复文件名
                target_file_path = os.path.join(target_folder, filename)
                
                if os.path.exists(target_file_path):
                    name, ext = os.path.splitext(filename)
                    new_filename = f"{name}_副本{ext}"
                    target_file_path = os.path.join(target_folder, new_filename)
                    
                    copy_num = 1
                    while os.path.exists(target_file_path):
                        new_filename = f"{name}_副本({copy_num}){ext}"
                        target_file_path = os.path.join(target_folder, new_filename)
                        copy_num += 1
                    
                    log_message(f"检测到重复文件，重命名为: {new_filename}")
                
                # 移动文件
                shutil.move(file_path, target_file_path)
                log_message(f"移动: {filename} -> {category_name}/")
                
                moved_count += 1
                matched = True
                break
        
        if not matched:
            log_message(f"跳过: {filename}（不在分类规则中）")

# 整理摘要
print("\n" + "="*40)
print(f"整理完成：共移动了 {moved_count} 个文件")
print("="*40)
log_message(f"整理完成：共移动了 {moved_count} 个文件")
log_message('下次想整理那个文件夹？')  # ← 新增这一行
print('下次想整理那个文件夹？')
