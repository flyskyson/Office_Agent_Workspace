# 方法3: 最简单的方式 - 直接复制模块到项目（推荐用于生产环境）
# 或者使用下面的 importlib 方式：

import importlib.util

# 加载 file_organizer 模块
spec = importlib.util.spec_from_file_location(
    "file_organizer",
    r"C:\Users\flyskyson\Office_Agent_Workspace\00_Agent_Library\02_Code_Snippets\文件操作\file_organizer.py"
)
file_organizer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(file_organizer)

# 调用函数
organize_files = file_organizer.organize_files
organize_files(r"C:\Users\flyskyson\Desktop\临时工作")