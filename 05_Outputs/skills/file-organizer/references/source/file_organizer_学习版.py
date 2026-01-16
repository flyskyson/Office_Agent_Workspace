"""
证照材料智能整理工具 - 学习版
================================
这个版本包含详细的中文注释，帮助您理解每一行代码的作用

作者: flyskyson
日期: 2025-01-08
"""

# ========== 1. 导入需要的库 ==========
import os           # 操作系统相关：文件路径、文件夹操作
import shutil       # 文件操作：移动、复制文件
import json         # JSON配置文件：读取和写入配置
from datetime import datetime  # 日期时间：获取当前日期

# ========== 2. 定义FileOrganizer类 ==========
class FileOrganizer:
    """
    证照材料智能整理工具

    这个类包含所有整理功能：
    - 加载配置
    - 扫描文件
    - 识别文件
    - 移动文件
    - 生成报告
    """

    def __init__(self, config_path='config.json'):
        """
        初始化函数（创建对象时自动执行）

        参数:
            config_path: 配置文件的路径，默认是'config.json'
        """
        # 加载配置文件，保存到self.config变量
        # self.config 现在可以在类的其他方法中使用
        self.config = self.load_config(config_path)

        # 初始化统计信息字典，用于记录整理情况
        self.stats = {
            '总文件数': 0,         # 一共处理了多少文件
            '成功移动': 0,         # 成功移动了多少文件
            '申请人统计': {},      # 每个申请人有多少文件 {姓名: 数量}
            '材料类型统计': {}     # 每种材料类型有多少 {类型: 数量}
        }

    def load_config(self, config_path):
        """
        加载配置文件

        为什么要用配置文件？
        - 因为改配置比改代码简单！
        - 加新材料类型？改配置就行
        - 改档案位置？改配置就行

        参数:
            config_path: 配置文件路径

        返回:
            配置字典（Python字典格式）
        """
        try:
            # 打开配置文件（用utf-8编码支持中文）
            # 'r' 表示读取模式
            with open(config_path, 'r', encoding='utf-8') as f:
                # json.load() 把JSON文本转换成Python字典
                config = json.load(f)
                return config

        except FileNotFoundError:
            # 如果文件不存在，显示错误信息
            print(f"[错误] 配置文件不存在: {config_path}")
            return None

    def scan_folder(self, folder_path):
        """
        扫描文件夹，找出所有需要整理的文件

        工作流程：
        1. 列出文件夹中的所有项目
        2. 检查每个项目是否是文件（不是文件夹）
        3. 检查文件扩展名是否在白名单中
        4. 返回符合条件的文件列表

        参数:
            folder_path: 要扫描的文件夹路径

        返回:
            文件路径列表
        """
        files = []  # 创建空列表，用于存放找到的文件路径

        try:
            # os.listdir() 列出文件夹中的所有项目（文件和文件夹）
            for item in os.listdir(folder_path):
                # os.path.join() 拼接路径，自动处理斜杠
                # 例如: os.path.join('C:/Desktop', 'file.txt')
                # 返回: 'C:/Desktop/file.txt' (Windows自动用反斜杠)
                item_path = os.path.join(folder_path, item)

                # os.path.isfile() 检查是否是文件（不是文件夹）
                if os.path.isfile(item_path):
                    # os.path.splitext() 分离文件名和扩展名
                    # 返回: (文件名, 扩展名)
                    # 例如: os.path.splitext('文件.txt') 返回 ('文件', '.txt')
                    # [1] 取扩展名部分
                    ext = os.path.splitext(item)[1].lower()  # .lower()转为小写

                    # 检查扩展名是否在配置文件的白名单中
                    if ext in self.config['allowed_extensions']:
                        # 如果是允许的文件类型，添加到列表
                        files.append(item_path)

        except PermissionError:
            # 如果没有权限访问这个文件夹
            print(f"[警告] 无权限访问: {folder_path}")
        except Exception as e:
            # 其他错误
            print(f"[错误] 扫描错误 {folder_path}: {e}")

        # 返回找到的文件列表
        return files

    def identify_file(self, filename):
        """
        智能识别文件，提取申请人名字和材料类型

        识别规则：
        1. 按分隔符（_ 或 -）提取申请人名字
        2. 按关键词识别材料类型

        参数:
            filename: 文件名（不含路径）

        返回:
            (申请人名字, 材料类型) 元组
        """
        # 去掉扩展名，只保留文件名
        # 例如: '张三_身份证.jpg' -> '张三_身份证'
        name_without_ext = os.path.splitext(filename)[0]

        # 初始化变量
        applicant = None   # 申请人名字（未知）
        materials = []     # 匹配到的材料类型列表

        # ========== 提取申请人名字 ==========
        # 格式1: 张三_身份证.jpg (下划线分隔)
        if '_' in filename:
            # split('_') 按下划线分割字符串
            # '张三_身份证.jpg'.split('_') -> ['张三', '身份证.jpg']
            parts = filename.split('_')
            applicant = parts[0]  # 第一部分是申请人名字
            remaining = '_'.join(parts[1:])  # 剩余部分用于识别材料类型

        # 格式2: 张三-身份证.jpg (横杠分隔)
        elif '-' in filename:
            parts = filename.split('-')
            applicant = parts[0]
            remaining = '-'.join(parts[1:])

        # 格式3: 张三身份证.jpg (无分隔符)
        else:
            applicant = None  # 无法提取申请人
            remaining = filename

        # ========== 识别材料类型 ==========
        # 遍历配置文件中定义的所有材料类型
        for material_type, keywords in self.config['file_patterns'].items():
            # 遍历该材料类型的关键词
            for keyword in keywords:
                # 检查关键词是否出现在文件名中
                # .lower() 转为小写，实现不区分大小写的匹配
                if keyword in remaining.lower():
                    # 如果找到匹配，添加到材料列表
                    materials.append(material_type)
                    break  # 找到一个就跳出，避免重复

        # 如果找到匹配的材料类型，取第一个；否则标记为"其他材料"
        material = materials[0] if materials else "其他材料"

        # 返回申请人和材料类型
        return applicant, material

    def get_archive_path(self, applicant, date_str):
        """
        生成归档路径

        根据配置决定是否按日期和申请人分类

        参数:
            applicant: 申请人名字
            date_str: 日期字符串（如 '2025-01-08'）

        返回:
            完整的归档路径
        """
        # 从配置文件获取基础路径
        # 例如: 'C:/工作文档/证照档案'
        base_path = self.config['archive_root']

        # 如果配置要求按日期分类
        if self.config['organize_by_date']:
            # os.path.join() 拼接路径
            # 例如: 'C:/工作文档/证照档案' + '2025-01-08'
            # 结果: 'C:/工作文档/证照档案/2025-01-08'
            base_path = os.path.join(base_path, date_str)

        # 如果配置要求按申请人分类，并且有申请人信息
        if self.config['organize_by_applicant'] and applicant:
            base_path = os.path.join(base_path, applicant)

        # 返回最终路径
        return base_path

    def move_file(self, src_path, dest_folder):
        """
        移动文件到目标文件夹

        参数:
            src_path: 源文件路径（要移动的文件）
            dest_folder: 目标文件夹路径（要移动到哪里）

        返回:
            True表示成功，False表示失败
        """
        try:
            # 创建目标文件夹（如果不存在）
            # exist_ok=True 表示文件夹存在也不报错
            os.makedirs(dest_folder, exist_ok=True)

            # 获取文件名（不含路径）
            # os.path.basename() 从路径中提取文件名
            # 例如: 'C:/Desktop/测试/文件.txt' -> '文件.txt'
            filename = os.path.basename(src_path)

            # 拼接完整的目标路径
            dest_path = os.path.join(dest_folder, filename)

            # shutil.move() 移动文件
            # 从源路径移动到目标路径
            shutil.move(src_path, dest_path)

            # 移动成功，返回True
            return True

        except Exception as e:
            # 如果移动失败，显示错误信息
            print(f"[错误] 移动失败 {src_path}: {e}")
            return False

    def organize(self):
        """
        执行整理：主功能

        这是整个工具的核心函数！

        工作流程：
        1. 获取今天的日期
        2. 扫描所有源文件夹
        3. 对每个文件：
           - 识别申请人和材料类型
           - 生成归档路径
           - 移动文件
        4. 生成统计报告
        """
        # ========== 显示标题 ==========
        print("=" * 70)
        print("证照材料智能整理工具")
        print("=" * 70)
        print()

        # ========== 获取今天的日期 ==========
        # datetime.now() 获取当前时间
        # .strftime() 格式化日期
        # '%Y-%m-%d' 格式: 2025-01-08
        today = datetime.now().strftime(self.config['date_format'])

        # ========== 扫描所有源文件夹 ==========
        all_files = []  # 用于存放所有找到的文件

        # 遍历配置文件中定义的所有源文件夹
        for folder in self.config['source_folders']:
            print(f"[扫描] {folder}")

            # 调用scan_folder()方法扫描这个文件夹
            files = self.scan_folder(folder)

            # 把找到的文件添加到总列表
            all_files.extend(files)

            # 显示找到了多少文件
            print(f"   找到 {len(files)} 个文件")

        print()
        print(f"[统计] 总共找到 {len(all_files)} 个文件")
        print()

        # 如果没有找到文件，直接结束
        if len(all_files) == 0:
            print("[完成] 没有需要整理的文件")
            return

        # ========== 处理每个文件 ==========
        print("开始整理...")
        print("-" * 70)

        # 遍历所有文件
        for file_path in all_files:
            # 提取文件名（不含路径）
            filename = os.path.basename(file_path)

            # 调用identify_file()识别文件
            applicant, material = self.identify_file(filename)

            # 调用get_archive_path()生成归档路径
            archive_path = self.get_archive_path(applicant, today)

            # 调用move_file()移动文件
            success = self.move_file(file_path, archive_path)

            # 如果移动成功
            if success:
                # 显示文件信息
                print(f"[OK] {filename}")
                print(f"   申请人: {applicant if applicant else '未知'}")
                print(f"   类型: {material}")
                print(f"   归档到: {archive_path}")
                print()

                # ========== 统计信息 ==========
                # 成功移动计数加1
                self.stats['成功移动'] += 1

                # 统计每个申请人的文件数
                if applicant:
                    # 如果申请人在字典中，数量+1；否则初始化为1
                    self.stats['申请人统计'][applicant] = \
                        self.stats['申请人统计'].get(applicant, 0) + 1

                # 统计每种材料类型的数量
                self.stats['材料类型统计'][material] = \
                    self.stats['材料类型统计'].get(material, 0) + 1

        # 记录总文件数
        self.stats['总文件数'] = len(all_files)

        # ========== 生成报告 ==========
        # 调用generate_report()方法显示统计报告
        self.generate_report(today)

    def generate_report(self, date_str):
        """
        生成整理报告

        参数:
            date_str: 日期字符串
        """
        print()
        print("=" * 70)
        print("整理报告")
        print("=" * 70)

        # 显示整理时间
        print(f"整理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 显示归档位置
        print(f"归档位置: {self.config['archive_root']}/{date_str}/")
        print()

        # 显示处理统计
        print("处理统计:")
        print(f"  - 总文件数: {self.stats['总文件数']}")
        print(f"  - 成功移动: {self.stats['成功移动']}")
        print()

        # 显示申请人统计
        print("申请人统计:")
        # 遍历申请人统计字典
        for applicant, count in self.stats['申请人统计'].items():
            print(f"  - {applicant}: {count}个文件")
        print()

        # 显示材料类型统计
        print("材料类型统计:")
        for material, count in self.stats['材料类型统计'].items():
            print(f"  - {material}: {count}个")
        print()

        print("=" * 70)
        print("[完成] 整理完成！")
        print("=" * 70)


# ========== 3. 主函数 ==========
def main():
    """
    程序入口

    当你运行这个脚本时，Python会先执行这个函数
    """
    # 创建FileOrganizer对象
    # 这会自动调用__init__()方法
    organizer = FileOrganizer('config.json')

    # 调用organize()方法开始整理
    organizer.organize()


# ========== 4. 程序入口 ==========
if __name__ == '__main__':
    """
    这是什么意思？

    - 如果直接运行这个脚本（python file_organizer_学习版.py）
      则 __name__ == '__main__' 为True
      会执行 main() 函数

    - 如果被其他脚本import导入
      则 __name__ != '__main__'
      不会自动执行 main() 函数
    """
    main()
