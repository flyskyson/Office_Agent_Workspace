"""
证照材料智能整理工具
作者: flyskyson
创建日期: 2025-01-08
功能: 自动识别、分类、归档证照材料
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path


class FileOrganizer:
    """证照材料智能整理工具"""

    def __init__(self, config_path='config.json'):
        """
        初始化配置
        :param config_path: 配置文件路径
        """
        self.config = self.load_config(config_path)
        self.stats = {
            '总文件数': 0,
            '成功移动': 0,
            '申请人统计': {},
            '材料类型统计': {}
        }

    def load_config(self, config_path):
        """
        加载配置文件
        为什么用配置文件？因为这样改规则不需要改代码！
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[错误] 配置文件不存在: {config_path}")
            return None

    def scan_folder(self, folder_path):
        """
        扫描文件夹，返回所有文件列表
        :param folder_path: 要扫描的文件夹路径
        :return: 文件路径列表
        """
        files = []
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)

                # 只处理文件，不处理文件夹
                if os.path.isfile(item_path):
                    # 检查扩展名是否在白名单中
                    ext = os.path.splitext(item)[1].lower()  # 修复: 应该是[1]不是[0]
                    if ext in self.config['allowed_extensions']:
                        files.append(item_path)
        except PermissionError:
            print(f"[警告] 无权限访问: {folder_path}")
        except Exception as e:
            print(f"[错误] 扫描错误 {folder_path}: {e}")

        return files

    def identify_file(self, filename):
        """
        智能识别文件
        :param filename: 文件名（不含路径）
        :return: (申请人名字, 材料类型)
        """
        # 去掉扩展名
        name_without_ext = os.path.splitext(filename)[0]

        # 尝试提取申请人名字（按常见格式）
        applicant = None
        materials = []

        # 格式1: 张三_身份证.jpg
        if '_' in filename:
            parts = filename.split('_')
            applicant = parts[0]
            remaining = '_'.join(parts[1:])
        # 格式2: 张三-身份证.jpg
        elif '-' in filename:
            parts = filename.split('-')
            applicant = parts[0]
            remaining = '-'.join(parts[1:])
        # 格式3: 张三身份证.jpg (无分隔符)
        else:
            applicant = None
            remaining = filename

        # 识别材料类型
        for material_type, keywords in self.config['file_patterns'].items():
            for keyword in keywords:
                if keyword in remaining.lower():
                    materials.append(material_type)
                    break

        material = materials[0] if materials else "其他材料"

        return applicant, material

    def get_archive_path(self, applicant, date_str):
        """
        生成归档路径
        :param applicant: 申请人名字
        :param date_str: 日期字符串
        :return: 完整的归档路径
        """
        base_path = self.config['archive_root']

        # 按日期分类
        if self.config['organize_by_date']:
            base_path = os.path.join(base_path, date_str)

        # 按申请人分类
        if self.config['organize_by_applicant'] and applicant:
            base_path = os.path.join(base_path, applicant)

        return base_path

    def move_file(self, src_path, dest_folder):
        """
        移动文件到目标文件夹
        :param src_path: 源文件路径
        :param dest_folder: 目标文件夹
        :return: 是否成功
        """
        try:
            # 创建目标文件夹（如果不存在）
            os.makedirs(dest_folder, exist_ok=True)

            # 移动文件
            filename = os.path.basename(src_path)
            dest_path = os.path.join(dest_folder, filename)

            shutil.move(src_path, dest_path)
            return True

        except Exception as e:
            print(f"[错误] 移动失败 {src_path}: {e}")
            return False

    def organize(self):
        """
        执行整理：主功能
        1. 扫描源文件夹
        2. 识别每个文件
        3. 移动到归档位置
        4. 生成报告
        """
        print("=" * 70)
        print("证照材料智能整理工具")
        print("=" * 70)
        print()

        # 获取今天的日期
        today = datetime.now().strftime(self.config['date_format'])

        # 扫描所有源文件夹
        all_files = []
        for folder in self.config['source_folders']:
            print(f"[扫描] {folder}")
            files = self.scan_folder(folder)
            all_files.extend(files)
            print(f"   找到 {len(files)} 个文件")

        print()
        print(f"[统计] 总共找到 {len(all_files)} 个文件")
        print()

        if len(all_files) == 0:
            print("[完成] 没有需要整理的文件")
            return

        # 处理每个文件
        print("开始整理...")
        print("-" * 70)

        for file_path in all_files:
            filename = os.path.basename(file_path)

            # 识别文件
            applicant, material = self.identify_file(filename)

            # 生成归档路径
            archive_path = self.get_archive_path(applicant, today)

            # 移动文件
            success = self.move_file(file_path, archive_path)

            if success:
                print(f"[OK] {filename}")
                print(f"   申请人: {applicant if applicant else '未知'}")
                print(f"   类型: {material}")
                print(f"   归档到: {archive_path}")
                print()

                # 统计
                self.stats['成功移动'] += 1

                if applicant:
                    self.stats['申请人统计'][applicant] = \
                        self.stats['申请人统计'].get(applicant, 0) + 1

                self.stats['材料类型统计'][material] = \
                    self.stats['材料类型统计'].get(material, 0) + 1

        self.stats['总文件数'] = len(all_files)

        # 生成报告
        self.generate_report(today)

    def generate_report(self, date_str):
        """
        生成整理报告
        :param date_str: 日期字符串
        """
        print()
        print("=" * 70)
        print("整理报告")
        print("=" * 70)
        print(f"整理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"归档位置: {self.config['archive_root']}/{date_str}/")
        print()
        print("处理统计:")
        print(f"  - 总文件数: {self.stats['总文件数']}")
        print(f"  - 成功移动: {self.stats['成功移动']}")
        print()
        print("申请人统计:")
        for applicant, count in self.stats['申请人统计'].items():
            print(f"  - {applicant}: {count}个文件")
        print()
        print("材料类型统计:")
        for material, count in self.stats['材料类型统计'].items():
            print(f"  - {material}: {count}个")
        print()
        print("=" * 70)
        print("[完成] 整理完成！")
        print("=" * 70)


def main():
    """主函数"""
    organizer = FileOrganizer('config.json')
    organizer.organize()


if __name__ == '__main__':
    main()
