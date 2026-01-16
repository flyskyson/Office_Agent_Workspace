"""
文件归档器 - 自动分类和归档文档

功能：
- 根据文件名/内容自动分类
- 创建归档目录结构
- 复制/移动文件到归档目录
- 清理桌面已处理文件
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from loguru import logger


class FileArchiver:
    """文件归档器 - 自动分类和归档文档"""

    # 文件类别定义
    FILE_CATEGORIES = {
        'id_card': {
            'keywords': ['身份证', 'id_card', 'idcard', 'sfz'],
            'extensions': ['.jpg', '.jpeg', '.png', '.bmp'],
            'description': '身份证'
        },
        'business_license': {
            'keywords': ['营业执照', 'license', 'yyzz', 'yyzz'],
            'extensions': ['.jpg', '.jpeg', '.png', '.pdf', '.bmp'],
            'description': '营业执照'
        },
        'lease_contract': {
            'keywords': ['租赁', '合同', 'lease', 'contract', 'zlht', 'zu'],
            'extensions': ['.pdf', '.jpg', '.png', '.docx'],
            'description': '租赁合同'
        },
        'property_cert': {
            'keywords': ['产权', '房产', 'property', 'cqzm', 'fang'],
            'extensions': ['.pdf', '.jpg', '.png', '.docx'],
            'description': '产权证明'
        },
        'application': {
            'keywords': ['申请', 'application', 'sq'],
            'extensions': ['.docx', '.pdf'],
            'description': '申请书'
        },
        'other': {
            'keywords': [],
            'extensions': [],
            'description': '其他'
        }
    }

    def __init__(self, base_archive_path: str = "archives"):
        """初始化归档器

        Args:
            base_archive_path: 归档基础路径
        """
        self.base_path = Path(base_archive_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"文件归档器初始化: {self.base_path}")

    def categorize_file(self, file_path: str) -> str:
        """根据文件名/路径确定文件类别

        Args:
            file_path: 文件路径

        Returns:
            文件类别
        """
        path = Path(file_path)
        filename = path.stem.lower()
        ext = path.suffix.lower()

        # 检查每个类别
        for category, config in self.FILE_CATEGORIES.items():
            if category == 'other':
                continue

            # 检查关键词
            for keyword in config['keywords']:
                if keyword.lower() in filename:
                    logger.debug(f"文件 '{file_path}' 分类为 '{category}' (关键词匹配)")
                    return category

            # 检查扩展名
            if ext in config['extensions']:
                # 对于仅靠扩展名判断的，需要更谨慎
                # 优先使用关键词匹配
                pass

        # 根据扩展名做最后判断
        for category, config in self.FILE_CATEGORIES.items():
            if category == 'other':
                continue
            if ext in config['extensions']:
                logger.debug(f"文件 '{file_path}' 分类为 '{category}' (扩展名匹配)")
                return category

        # 默认为other
        logger.debug(f"文件 '{file_path}' 分类为 'other' (默认)")
        return 'other'

    def create_archive_directory(
        self,
        operator_name: str,
        id_card: str
    ) -> Path:
        """创建归档目录

        Args:
            operator_name: 经营者姓名
            id_card: 身份证号

        Returns:
            归档目录路径
        """
        from datetime import datetime
        import hashlib

        # 使用身份证后4位 + 时间戳生成安全的目录名
        # 避免中文文件名导致的文件系统问题
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_hash = hashlib.md5(f"{operator_name}_{id_card}".encode('utf-8')).hexdigest()[:8]
        dir_name = f"operator_{id_card[-4:]}_{timestamp}_{dir_hash}"

        archive_dir = self.base_path / dir_name
        archive_dir.mkdir(parents=True, exist_ok=True)

        # 创建元数据文件，保存原始姓名
        metadata_file = archive_dir / ".metadata.json"
        if not metadata_file.exists():
            import json
            metadata = {
                "operator_name": operator_name,
                "id_card": id_card,
                "created_at": datetime.now().isoformat()
            }
            metadata_file.write_text(json.dumps(metadata, ensure_ascii=False), encoding='utf-8')

        # 创建子目录
        for category in self.FILE_CATEGORIES.keys():
            if category != 'other':
                (archive_dir / category).mkdir(exist_ok=True)

        logger.info(f"创建归档目录: {archive_dir} (经营者: {operator_name})")
        return archive_dir

    def archive_file(
        self,
        file_path: str,
        archive_dir: Path,
        category: str,
        operator_name: str = ""
    ) -> Optional[str]:
        """归档单个文件

        Args:
            file_path: 源文件路径
            archive_dir: 归档目录
            category: 文件类别
            operator_name: 经营者姓名（用于重命名）

        Returns:
            归档后的文件路径，失败返回None
        """
        src = Path(file_path)

        if not src.exists():
            logger.warning(f"源文件不存在: {src}")
            return None

        # 目标子目录
        target_dir = archive_dir / category
        target_dir.mkdir(exist_ok=True)

        # 目标文件名 - 使用 UUID 避免中文文件名问题
        import uuid
        ext = src.suffix.lower()
        unique_id = str(uuid.uuid4())[:8]

        if operator_name:
            # 使用格式: operator_分类_UUID.扩展名
            target_name = f"operator_{category}_{unique_id}{ext}"
        else:
            target_name = f"{category}_{unique_id}{ext}"

        dst = target_dir / target_name

        # 如果目标文件已存在，添加时间戳
        if dst.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            target_name = f"operator_{category}_{timestamp}_{unique_id}{ext}"
            dst = target_dir / target_name

        try:
            # 复制文件（保留原文件）
            shutil.copy2(src, dst)
            logger.info(f"归档文件: {src} -> {dst}")
            return str(dst)

        except Exception as e:
            logger.error(f"归档文件失败: {src} -> {dst}, 错误: {e}")
            return None

    def archive_operator_files(
        self,
        operator_name: str,
        id_card: str,
        files: Dict[str, str],
        move: bool = False
    ) -> str:
        """归档单个经营者的所有文件

        Args:
            operator_name: 经营者姓名
            id_card: 身份证号
            files: 文件字典 {'category': 'file_path'}
            move: 是否移动而非复制

        Returns:
            归档目录路径
        """
        # 创建归档目录
        archive_dir = self.create_archive_directory(operator_name, id_card)

        # 归档文件
        archived_paths = {}
        for category, file_path in files.items():
            if not file_path:
                continue

            # 确保类别有效
            if category not in self.FILE_CATEGORIES:
                category = self.categorize_file(file_path)

            archived_path = self.archive_file(
                file_path,
                archive_dir,
                category,
                operator_name
            )

            if archived_path:
                archived_paths[f"{category}_path"] = archived_path

                # 如果需要移动
                if move:
                    try:
                        Path(file_path).unlink()
                        logger.info(f"删除原文件: {file_path}")
                    except Exception as e:
                        logger.error(f"删除原文件失败: {file_path}, 错误: {e}")

        return str(archive_dir)

    def clean_desktop(
        self,
        desktop_path: str,
        processed_files: List[str],
        move_to_trash: bool = True
    ) -> int:
        """清理桌面已处理的文件

        Args:
            desktop_path: 桌面路径
            processed_files: 已处理的文件列表
            move_to_trash: 是否移到回收站而非直接删除

        Returns:
            清理的文件数量
        """
        desktop = Path(desktop_path)

        if not desktop.exists():
            logger.warning(f"桌面路径不存在: {desktop_path}")
            return 0

        cleaned_count = 0

        for file_path in processed_files:
            file = Path(file_path)

            # 只清理桌面上的文件
            if file.parent != desktop:
                continue

            if not file.exists():
                continue

            try:
                if move_to_trash:
                    # 移到回收站（桌面上的回收站文件夹）
                    trash_dir = desktop / "已处理文件"
                    trash_dir.mkdir(exist_ok=True)

                    # 重命名避免冲突
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_name = f"{file.stem}_{timestamp}{file.suffix}"
                    new_path = trash_dir / new_name

                    shutil.move(str(file), str(new_path))
                    logger.info(f"移动到回收站: {file} -> {new_path}")
                else:
                    # 直接删除
                    file.unlink()
                    logger.info(f"删除文件: {file}")

                cleaned_count += 1

            except Exception as e:
                logger.error(f"清理文件失败: {file}, 错误: {e}")

        logger.info(f"清理完成，共处理 {cleaned_count} 个文件")
        return cleaned_count

    def get_archive_info(self, operator_name: str, id_card: str) -> Optional[Dict]:
        """获取归档信息

        Args:
            operator_name: 经营者姓名
            id_card: 身份证号

        Returns:
            归档信息字典
        """
        dir_name = f"{operator_name}_{id_card[-4:]}"
        archive_dir = self.base_path / dir_name

        if not archive_dir.exists():
            return None

        # 统计各类文件
        files_info = {}
        total_files = 0
        total_size = 0

        for category in self.FILE_CATEGORIES.keys():
            if category == 'other':
                continue

            category_dir = archive_dir / category
            if category_dir.exists():
                files = list(category_dir.glob('*'))
                files_info[category] = {
                    'count': len(files),
                    'files': [str(f) for f in files]
                }
                total_files += len(files)
                for f in files:
                    total_size += f.stat().st_size

        return {
            'archive_path': str(archive_dir),
            'total_files': total_files,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'categories': files_info
        }

    def list_archives(self) -> List[Dict]:
        """列出所有归档

        Returns:
            归档列表
        """
        archives = []

        for item in self.base_path.iterdir():
            if not item.is_dir():
                continue

            # 统计文件
            total_files = 0
            categories = {}

            for sub_item in item.iterdir():
                if sub_item.is_dir():
                    files = list(sub_item.glob('*'))
                    categories[sub_item.name] = len(files)
                    total_files += len(files)

            archives.append({
                'name': item.name,
                'path': str(item),
                'total_files': total_files,
                'categories': categories
            })

        return sorted(archives, key=lambda x: x['name'])

    def cleanup_empty_archives(self) -> int:
        """清理空的归档目录

        Returns:
            清理的目录数量
        """
        cleaned = 0

        for item in self.base_path.iterdir():
            if not item.is_dir():
                continue

            # 检查是否为空
            files = list(item.rglob('*'))
            files = [f for f in files if f.is_file()]

            if not files:
                try:
                    shutil.rmtree(item)
                    logger.info(f"删除空归档目录: {item}")
                    cleaned += 1
                except Exception as e:
                    logger.error(f"删除目录失败: {item}, 错误: {e}")

        return cleaned

    def get_storage_stats(self) -> Dict:
        """获取存储统计信息

        Returns:
            统计信息字典
        """
        total_archives = 0
        total_files = 0
        total_size = 0

        for item in self.base_path.rglob('*'):
            if item.is_file():
                total_files += 1
                total_size += item.stat().st_size

        # 统计归档目录数
        for item in self.base_path.iterdir():
            if item.is_dir():
                total_archives += 1

        return {
            'total_archives': total_archives,
            'total_files': total_files,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'archive_path': str(self.base_path)
        }


# 便捷函数
def archive_files(
    operator_name: str,
    id_card: str,
    files: Dict[str, str],
    archive_path: str = "archives"
) -> str:
    """便捷函数：归档文件

    Args:
        operator_name: 经营者姓名
        id_card: 身份证号
        files: 文件字典
        archive_path: 归档基础路径

    Returns:
        归档目录路径
    """
    archiver = FileArchiver(archive_path)
    return archiver.archive_operator_files(operator_name, id_card, files)
