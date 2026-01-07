"""
文件整理模块
===========

智能文件整理助手 - 自动将文件夹中的文件按类型分类整理

依赖:
    - Python 标准库（无需额外安装）

主要功能:
    - FileOrganizer 类: 提供完整的文件整理功能
    - organize_files 函数: 便捷的简化接口

特性:
    - 自定义分类规则
    - 自动处理重复文件名
    - 支持日志记录
    - 提供预演模式（dry_run）
    - 详细的统计信息

使用示例:
    >>> # 方式 1: 使用便捷函数（简单场景）
    >>> from file_organizer import organize_files
    >>>
    >>> stats = organize_files("/path/to/messy_folder", confirm=False)
    >>> print(f"移动了 {stats['moved']} 个文件")
    >>>
    >>> # 方式 2: 使用类接口（高级场景）
    >>> from file_organizer import FileOrganizer
    >>>
    >>> organizer = FileOrganizer(log_file="organizer.log", verbose=True)
    >>> stats = organizer.organize_files(
    ...     "/path/to/folder",
    ...     categories={"Images": [".jpg", ".png"]},
    ...     dry_run=True  # 预演模式，不实际移动
    ... )

作者: flyskyson
创建时间: 2024-01-03
版本: 2.0
"""

import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class FileOrganizer:
    """
    文件整理器类 - 智能文件分类整理工具

    这个类提供了完整的文件整理功能，支持自定义分类规则、重复文件处理、
    日志记录等高级功能。

    属性:
        DEFAULT_CATEGORIES (dict): 默认的文件分类规则
        log_file (str): 日志文件路径
        verbose (bool): 是否输出详细信息
        stats (dict): 整理统计信息

    使用示例:
        >>> # 基本使用
        >>> organizer = FileOrganizer(log_file="organizer.log")
        >>> stats = organizer.organize_files("/path/to/folder", confirm=False)
        >>>
        >>> # 自定义分类规则
        >>> custom_rules = {
        ...     "Photos": [".jpg", ".jpeg", ".png"],
        ...     "Documents": [".pdf", ".doc", ".docx"]
        ... }
        >>> stats = organizer.organize_files(
        ...     "/path/to/folder",
        ...     categories=custom_rules
        ... )
        >>>
        >>> # 预演模式（不实际移动文件）
        >>> stats = organizer.organize_files(
        ...     "/path/to/folder",
        ...     dry_run=True  # 只显示将要执行的操作
        ... )
    """

    # 默认分类规则 - 扩展名列表（不区分大小写）
    DEFAULT_CATEGORIES = {
        "PDF": [".pdf"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
        "Documents": [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".json", ".xml"],
        "Data": [".csv", ".xlsx", ".xls", ".json", ".xml", ".sql", ".db"]
    }

    def __init__(self, log_file: Optional[str] = None, verbose: bool = True):
        """
        初始化文件整理器

        Args:
            log_file (str, optional): 日志文件路径
                - 如果提供，所有操作都会记录到这个文件
                - 日志格式: [时间戳] 消息内容
                - 例如: "organizer.log" 或 "/path/to/logs/organizer.log"
                - 如果为 None，则不记录日志

            verbose (bool): 是否在控制台输出详细信息，默认为 True
                - True: 打印每个操作（移动文件、创建文件夹等）
                - False: 静默模式，只输出关键信息

        示例:
            >>> # 带日志和详细输出
            >>> organizer = FileOrganizer(log_file="organizer.log", verbose=True)
            >>>
            >>> # 静默模式，不记录日志
            >>> organizer = FileOrganizer(verbose=False)
        """
        self.log_file = log_file
        self.verbose = verbose
        self.stats = {
            'moved': 0,           # 移动的文件数量
            'skipped': 0,         # 跳过的文件数量
            'created_folders': 0, # 创建的文件夹数量
            'renamed': 0          # 重命名的文件数量
        }

    def _log(self, message: str) -> None:
        """
        记录日志信息到控制台和/或日志文件

        Args:
            message (str): 要记录的消息内容

        行为:
            - 如果 verbose=True，打印到控制台
            - 如果 log_file 已设置，追加到日志文件
            - 日志文件包含时间戳: [YYYY-MM-DD HH:MM:SS] 消息

        注意:
            - 日志文件使用 UTF-8 编码
            - 如果日志文件目录不存在，会自动创建
            - 日志文件以追加模式写入，不会覆盖之前的内容
        """
        # 输出到控制台
        if self.verbose:
            print(message)

        # 写入日志文件
        if self.log_file:
            now = datetime.now()
            time_string = now.strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"[{time_string}] {message}\n"

            # 确保日志文件目录存在
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            # 追加写入日志文件
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_line)

    def _handle_duplicate(self, target_folder: str, filename: str) -> str:
        """
        处理重复文件名，生成新的唯一文件名

        Args:
            target_folder (str): 目标文件夹路径
            filename (str): 原始文件名

        Returns:
            str: 处理后的新文件名（确保不重复）

        命名规则:
            - 第一次重复: "文件名_副本.扩展名"
            - 第二次重复: "文件名_副本(1).扩展名"
            - 第三次重复: "文件名_副本(2).扩展名"
            - 以此类推...

        示例:
            >>> _handle_duplicate("/folder", "test.txt")
            "test_副本.txt"
            >>> _handle_duplicate("/folder", "test_副本.txt")
            "test_副本(1).txt"
        """
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_副本{ext}"
        target_path = os.path.join(target_folder, new_filename)

        # 如果重复，添加序号
        copy_num = 1
        while os.path.exists(target_path):
            new_filename = f"{name}_副本({copy_num}){ext}"
            target_path = os.path.join(target_folder, new_filename)
            copy_num += 1

        self.stats['renamed'] += 1
        return new_filename

    def organize_files(
        self,
        source_dir: str,
        categories: Optional[Dict[str, List[str]]] = None,
        confirm: bool = True,
        dry_run: bool = False
    ) -> Dict[str, int]:
        """
        整理指定文件夹中的文件，按扩展名分类到不同文件夹

        这是核心方法，会扫描源文件夹中的所有文件，根据扩展名将它们
        移动到对应的分类文件夹中。

        Args:
            source_dir (str): 要整理的源文件夹路径
                - 支持绝对路径和相对路径
                - 例如: "C:/Users/Name/Downloads" 或 "./messy_folder"
                - 必须是已存在的文件夹路径

            categories (dict, optional): 自定义分类规则
                - 格式: {文件夹名: [扩展名列表]}
                - 扩展名必须包含点号（如 ".jpg"）
                - 扩展名不区分大小写
                - 如果为 None，使用 DEFAULT_CATEGORIES
                - 示例: {"Images": [".jpg", ".png"], "Docs": [".pdf"]}

            confirm (bool): 是否在执行前需要用户确认，默认为 True
                - True: 显示整理计划，等待用户输入 y/n
                - False: 直接开始整理，无需确认

            dry_run (bool): 是否为预演模式，默认为 False
                - False: 正常模式，实际移动文件
                - True: 预演模式，只显示将要执行的操作，不实际移动

        Returns:
            dict: 统计信息字典，包含以下键:
                - 'moved': 成功移动的文件数量
                - 'skipped': 跳过的文件数量（未匹配分类规则）
                - 'created_folders': 创建的分类文件夹数量
                - 'renamed': 重命名的文件数量（处理重复）

        Raises:
            FileNotFoundError: 源文件夹不存在
            NotADirectoryError: 源路径不是文件夹

        使用示例:
            >>> # 基本使用
            >>> organizer = FileOrganizer()
            >>> stats = organizer.organize_files(
            ...     "/path/to/downloads",
            ...     confirm=False
            ... )
            >>> print(f"移动了 {stats['moved']} 个文件")

            >>> # 自定义分类规则
            >>> custom_rules = {
            ...     "Photos": [".jpg", ".jpeg", ".png"],
            ...     "Work": [".pdf", ".docx", ".xlsx"]
            ... }
            >>> stats = organizer.organize_files(
            ...     "/path/to/folder",
            ...     categories=custom_rules
            ... )

            >>> # 预演模式（不实际移动）
            >>> stats = organizer.organize_files(
            ...     "/path/to/folder",
            ...     dry_run=True
            ... )
            >>> # 检查 stats，满意后设置 dry_run=False 再执行

        注意事项:
            1. 文件移动操作不可逆，建议先用 dry_run=True 测试
            2. 如果目标文件夹中已存在同名文件，会自动重命名
            3. 不会移动子文件夹，只处理文件
            4. 不在分类规则中的文件会被跳过（留在原位置）
            5. 分类文件夹会自动创建（如果不存在）
        """
        # 使用默认分类规则（如果未提供）
        if categories is None:
            categories = self.DEFAULT_CATEGORIES

        # 重置统计信息
        self.stats = {
            'moved': 0,
            'skipped': 0,
            'created_folders': 0,
            'renamed': 0
        }

        # 验证源文件夹
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"源文件夹不存在: {source_dir}")

        if not os.path.isdir(source_dir):
            raise NotADirectoryError(f"路径不是文件夹: {source_dir}")

        # 显示整理信息
        self._log("=" * 50)
        self._log(f"📁 文件整理任务")
        self._log(f"源文件夹: {source_dir}")
        self._log(f"分类规则: {len(categories)} 个分类")
        self._log(f"预演模式: {'是' if dry_run else '否'}")

        # 显示分类详情
        for folder, extensions in categories.items():
            ext_str = ", ".join(extensions) if len(extensions) <= 5 else f"{len(extensions)} 种类型"
            self._log(f"  📂 {folder}: {ext_str}")

        # 用户确认
        if confirm:
            self._log("")
            response = input("是否开始整理？ [y/N]: ")
            if response.lower() not in ['y', 'yes', '是']:
                self._log("❌ 取消整理")
                return self.stats

        self._log("-" * 50)

        # 开始整理
        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)

            # 跳过文件夹
            if not os.path.isfile(file_path):
                continue

            # 提取文件扩展名（转为小写）
            _, extension = os.path.splitext(filename)
            extension = extension.lower()

            # 查找匹配的分类
            matched = False
            for category_name, extensions in categories.items():
                # 将扩展名列表转为小写进行比较
                extensions_lower = [ext.lower() for ext in extensions]

                if extension in extensions_lower:
                    # 目标文件夹路径
                    target_folder = os.path.join(source_dir, category_name)

                    # 创建目标文件夹（如果不存在）
                    if not os.path.exists(target_folder):
                        if not dry_run:
                            os.makedirs(target_folder, exist_ok=True)
                        self.stats['created_folders'] += 1
                        self._log(f"📁 创建文件夹: {category_name}")

                    # 处理重复文件名
                    target_file_path = os.path.join(target_folder, filename)
                    final_filename = filename

                    if os.path.exists(target_file_path):
                        final_filename = self._handle_duplicate(target_folder, filename)
                        target_file_path = os.path.join(target_folder, final_filename)
                        self._log(f"⚠️  重复文件: {filename} -> {final_filename}")

                    # 移动文件
                    action = "预演" if dry_run else "移动"
                    if not dry_run:
                        shutil.move(file_path, target_file_path)

                    self._log(f"✓ {action}: {filename} -> {category_name}/{final_filename}")
                    self.stats['moved'] += 1
                    matched = True
                    break

            # 未匹配的文件
            if not matched:
                self._log(f"⊘ 跳过: {filename} (不在分类规则中)")
                self.stats['skipped'] += 1

        # 输出统计信息
        self._log("-" * 50)
        self._log(f"✅ 整理完成！")
        self._log(f"  📦 移动文件: {self.stats['moved']} 个")
        self._log(f"  ⊘ 跳过文件: {self.stats['skipped']} 个")
        self._log(f"  📁 创建文件夹: {self.stats['created_folders']} 个")
        self._log(f"  ✏️  重命名文件: {self.stats['renamed']} 个")
        self._log("=" * 50)

        return self.stats


# ========== 便捷函数 ==========

def organize_files(
    source_dir: str,
    rule_dict: Optional[Dict[str, List[str]]] = None,
    confirm: bool = True,
    log_file: Optional[str] = None
) -> Dict[str, int]:
    """
    便捷函数：快速整理文件（简化接口）

    这是一个向后兼容的简化接口，适合快速使用。如果需要更多功能
    （如预演模式），请使用 FileOrganizer 类。

    Args:
        source_dir (str): 要整理的源文件夹路径

        rule_dict (dict, optional): 分类规则字典
            - 格式: {文件夹名: [扩展名列表]}
            - 例如: {"Images": [".jpg", ".png"], "Docs": [".pdf"]}
            - 如果为 None，使用默认分类规则

        confirm (bool): 是否在执行前需要用户确认，默认为 True
            - True: 显示整理计划，等待用户确认
            - False: 直接开始整理

        log_file (str, optional): 日志文件路径
            - 如果提供，操作会记录到日志文件
            - 例如: "organizer.log"

    Returns:
        dict: 统计信息字典
            - 'moved': 移动的文件数量
            - 'skipped': 跳过的文件数量
            - 'created_folders': 创建的文件夹数量
            - 'renamed': 重命名的文件数量

    使用示例:
        >>> # 使用默认规则（最简单）
        >>> stats = organize_files("/path/to/downloads", confirm=False)
        >>> print(f"整理了 {stats['moved']} 个文件")

        >>> # 自定义规则
        >>> custom_rules = {
        ...     "Photos": [".jpg", ".jpeg", ".png"],
        ...     "Documents": [".pdf", ".docx"]
        ... }
        >>> stats = organize_files(
        ...     "/path/to/folder",
        ...     rule_dict=custom_rules,
        ...     confirm=False,
        ...     log_file="organizer.log"
        ... )

    注意事项:
        - 此函数不支持预演模式（dry_run）
        - 如需预演，请使用 FileOrganizer 类
        - 文件移动操作不可逆，建议先备份重要文件

    另见:
        FileOrganizer 类提供更多功能，包括预演模式
    """
    organizer = FileOrganizer(log_file=log_file)
    return organizer.organize_files(source_dir, rule_dict, confirm)


# ========== 测试接口 ==========

if __name__ == '__main__':
    """
    模块测试代码

    运行此模块会执行测试示例，展示基本用法
    """
    print("=" * 70)
    print("文件整理模块 - 测试示例")
    print("=" * 70)
    print()

    # 示例 1: 基本使用（带确认）
    print("【示例 1】基本使用 - 整理文件夹（带确认）")
    print("-" * 70)
    print("说明: 使用默认分类规则整理 test_folder 文件夹")
    print()

    try:
        stats = organize_files(
            source_dir="test_folder",
            log_file="organizer_log.txt",
            confirm=True
        )
        print(f"\n统计结果: {stats}")
    except FileNotFoundError as e:
        print(f"⚠️  错误: {e}")
        print("提示: 请先创建 test_folder 文件夹并放入一些测试文件")
    except Exception as e:
        print(f"❌ 错误: {e}")

    # 示例 2: 自定义规则（无确认）
    print("\n" + "=" * 70)
    print("【示例 2】自定义规则 - 仅整理图片文件")
    print("-" * 70)
    print("说明: 只整理 .jpg 和 .png 文件，不需要确认")
    print()

    custom_rules = {
        "Photos": [".jpg", ".jpeg", ".png"],
        "Screenshots": [".png"]
    }

    try:
        stats = organize_files(
            source_dir="test_folder",
            rule_dict=custom_rules,
            confirm=False,
            log_file="organizer_log.txt"
        )
        print(f"\n统计结果: {stats}")
    except FileNotFoundError as e:
        print(f"⚠️  错误: {e}")
    except Exception as e:
        print(f"❌ 错误: {e}")

    # 示例 3: 使用类接口（预演模式）
    print("\n" + "=" * 70)
    print("【示例 3】使用 FileOrganizer 类 - 预演模式")
    print("-" * 70)
    print("说明: 预演模式不会实际移动文件，只显示将要执行的操作")
    print()

    try:
        organizer = FileOrganizer(log_file="organizer_log.txt", verbose=True)
        stats = organizer.organize_files(
            source_dir="test_folder",
            categories={"PDF": [".pdf"]},
            confirm=False,
            dry_run=True  # 预演模式，不实际移动
        )
        print(f"\n预演统计: {stats}")
        print("提示: 如果满意结果，请设置 dry_run=False 再执行")
    except FileNotFoundError as e:
        print(f"⚠️  错误: {e}")
    except Exception as e:
        print(f"❌ 错误: {e}")

    # 使用提示
    print("\n" + "=" * 70)
    print("💡 使用建议")
    print("-" * 70)
    print("""
1. 在实际使用前，建议先使用预演模式 (dry_run=True) 测试
2. 对于重要的文件夹，建议先备份再整理
3. 可以通过修改 rule_dict 参数来自定义分类规则
4. 日志文件会记录所有操作，便于追踪和审计
5. 如需更详细的信息，设置 verbose=True

快速开始:
    from file_organizer import organize_files

    stats = organize_files("/your/folder/path", confirm=False)
    print(f"整理完成！移动了 {stats['moved']} 个文件")
    """)

    print("=" * 70)
    print("测试完成")
    print("=" * 70)
