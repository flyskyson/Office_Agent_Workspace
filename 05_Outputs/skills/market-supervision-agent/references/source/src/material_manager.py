#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
材料文件夹管理器

管理个体工商户申请材料的本地存储，支持：
1. 自动创建经营者专属材料文件夹
2. 材料分类存储（身份证、产权证明等）
3. 与政务服务网上传对接
4. 材料状态追踪

作者: Claude Code
日期: 2026-01-14
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from loguru import logger


@dataclass
class MaterialFile:
    """材料文件信息"""
    name: str              # 材料名称（中文）
    key: str               # 材料键值（英文，用于数据库）
    file_path: str         # 文件路径
    category: str          # 分类: id_card, property_cert, license, contract, other
    required: bool = True  # 是否必需
    status: str = "pending" # pending, uploaded, verified
    upload_time: Optional[str] = None
    portal_uploaded: bool = False  # 是否已在政务网上传
    portal_upload_time: Optional[str] = None


class MaterialFolderManager:
    """材料文件夹管理器"""

    # 默认材料文件夹位置（桌面）
    DEFAULT_DESKTOP_FOLDER = Path("Desktop/市场监管申请材料")

    # 材料分类
    CATEGORIES = {
        "id_card": "身份证",
        "property_cert": "经营场所证明",
        "license": "证照",
        "contract": "合同",
        "other": "其他材料"
    }

    # 标准材料键值
    STANDARD_MATERIALS = {
        # 身份证
        "id_card_front": MaterialFile(
            name="身份证正面",
            key="id_card_front",
            file_path="",
            category="id_card",
            required=True
        ),
        "id_card_back": MaterialFile(
            name="身份证反面",
            key="id_card_back",
            file_path="",
            category="id_card",
            required=True
        ),
        # 经营场所证明（三选一）
        "property_cert": MaterialFile(
            name="产权证明",
            key="property_cert",
            file_path="",
            category="property_cert",
            required=True
        ),
        "lease_contract": MaterialFile(
            name="租赁合同",
            key="lease_contract",
            file_path="",
            category="contract",
            required=False
        ),
        "declaration_form": MaterialFile(
            name="经营场所申报表",
            key="declaration_form",
            file_path="",
            category="other",
            required=False
        ),
        # 营业执照（变更/注销时需要）
        "business_license": MaterialFile(
            name="营业执照",
            key="business_license",
            file_path="",
            category="license",
            required=False
        ),
        # 其他材料
        "other_materials": MaterialFile(
            name="其他材料",
            key="other_materials",
            file_path="",
            category="other",
            required=False
        )
    }

    def __init__(
        self,
        base_folder: Optional[Path] = None,
        auto_create: bool = True
    ):
        """
        初始化材料管理器

        Args:
            base_folder: 基础文件夹路径，默认为桌面/市场监管申请材料
            auto_create: 是否自动创建文件夹
        """
        # 获取桌面路径
        if base_folder is None:
            desktop = Path.home() / "Desktop"
            # 尝试中文桌面
            if not desktop.exists():
                desktop = Path.home() / "桌面"
            self.base_folder = desktop / "市场监管申请材料"
        else:
            self.base_folder = Path(base_folder)

        # 创建基础文件夹
        if auto_create:
            self.base_folder.mkdir(parents=True, exist_ok=True)
            logger.info(f"材料文件夹: {self.base_folder}")

        # 材料索引
        self.materials: Dict[str, MaterialFile] = {}

    def create_operator_folder(
        self,
        operator_name: str,
        business_name: Optional[str] = None,
        operator_id: Optional[int] = None
    ) -> Path:
        """
        为经营者创建专属材料文件夹

        Args:
            operator_name: 经营者姓名
            business_name: 个体工商户名称（可选）
            operator_id: 经营者ID（可选）

        Returns:
            文件夹路径
        """
        # 生成文件夹名
        if operator_id:
            folder_name = f"{operator_id}_{operator_name}"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = f"{timestamp}_{operator_name}"

        # 创建文件夹
        operator_folder = self.base_folder / folder_name
        operator_folder.mkdir(parents=True, exist_ok=True)

        # 创建子文件夹（按材料分类）
        for category_key, category_name in self.CATEGORIES.items():
            category_folder = operator_folder / category_name
            category_folder.mkdir(exist_ok=True)

        logger.info(f"创建经营者材料文件夹: {operator_folder}")

        # 保存元数据
        metadata = {
            "operator_id": operator_id,
            "operator_name": operator_name,
            "business_name": business_name,
            "created_at": datetime.now().isoformat(),
            "folder_path": str(operator_folder)
        }

        metadata_file = operator_folder / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        return operator_folder

    def add_material(
        self,
        operator_folder: Path,
        key: str,
        file_path: str,
        copy: bool = True
    ) -> MaterialFile:
        """
        添加材料文件

        Args:
            operator_folder: 经营者文件夹路径
            key: 材料键值
            file_path: 源文件路径
            copy: 是否复制文件（True）还是移动（False）

        Returns:
            材料文件对象
        """
        # 获取标准材料定义
        if key not in self.STANDARD_MATERIALS:
            logger.warning(f"未知的材料键值: {key}，将作为其他材料处理")
            material = MaterialFile(
                name=key,
                key=key,
                file_path="",
                category="other",
                required=False
            )
        else:
            material = self.STANDARD_MATERIALS[key]

        # 确定目标文件夹
        category_folder = operator_folder / self.CATEGORIES[material.category]
        category_folder.mkdir(exist_ok=True)

        # 复制/移动文件
        source_path = Path(file_path)
        if not source_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        # 目标文件名（使用材料名称 + 原扩展名）
        target_name = f"{material.name}{source_path.suffix}"
        target_path = category_folder / target_name

        # 执行复制或移动
        if copy:
            shutil.copy2(source_path, target_path)
            logger.debug(f"复制文件: {source_path} -> {target_path}")
        else:
            shutil.move(str(source_path), str(target_path))
            logger.debug(f"移动文件: {source_path} -> {target_path}")

        # 更新材料信息
        material.file_path = str(target_path)
        material.status = "uploaded"
        material.upload_time = datetime.now().isoformat()

        # 保存到索引
        self.materials[key] = material

        # 更新元数据文件
        self._update_metadata(operator_folder, material)

        logger.info(f"添加材料: {material.name} -> {target_path}")

        return material

    def get_material(self, key: str) -> Optional[MaterialFile]:
        """
        获取材料信息

        Args:
            key: 材料键值

        Returns:
            材料文件对象
        """
        return self.materials.get(key)

    def get_materials_by_category(self, category: str) -> List[MaterialFile]:
        """
        按分类获取材料

        Args:
            category: 分类名称

        Returns:
            材料列表
        """
        return [
            m for m in self.materials.values()
            if m.category == category
        ]

    def mark_portal_uploaded(
        self,
        operator_folder: Path,
        key: str
    ) -> bool:
        """
        标记材料已在政务网上传

        Args:
            operator_folder: 经营者文件夹路径
            key: 材料键值

        Returns:
            是否成功
        """
        if key not in self.materials:
            logger.warning(f"材料不存在: {key}")
            return False

        material = self.materials[key]
        material.portal_uploaded = True
        material.portal_upload_time = datetime.now().isoformat()

        # 更新元数据
        self._update_metadata(operator_folder, material)

        logger.info(f"标记政务网上传: {material.name}")
        return True

    def get_missing_materials(self, scenario: str = "registration") -> List[MaterialFile]:
        """
        获取缺失的必需材料

        Args:
            scenario: 场景（registration, change, cancellation, annual_report）

        Returns:
            缺失材料列表
        """
        # 定义各场景必需的材料
        required_by_scenario = {
            "registration": ["id_card_front", "id_card_back", "property_cert"],
            "change": ["id_card_front", "id_card_back", "business_license"],
            "cancellation": ["id_card_front", "id_card_back", "business_license"],
            "annual_report": ["business_license"]
        }

        required_keys = required_by_scenario.get(scenario, [])

        missing = []
        for key in required_keys:
            if key not in self.materials or self.materials[key].status != "uploaded":
                # 获取标准材料定义
                if key in self.STANDARD_MATERIALS:
                    missing.append(self.STANDARD_MATERIALS[key])

        return missing

    def get_materials_for_portal(
        self,
        operator_folder: Path
    ) -> List[MaterialFile]:
        """
        获取需要在政务网上传的材料

        Args:
            operator_folder: 经营者文件夹路径

        Returns:
            需要上传的材料列表
        """
        return [
            m for m in self.materials.values()
            if m.status == "uploaded" and not m.portal_uploaded
        ]

    def export_materials_list(
        self,
        operator_folder: Path,
        output_file: Optional[Path] = None
    ) -> Path:
        """
        导出材料清单

        Args:
            operator_folder: 经营者文件夹路径
            output_file: 输出文件路径（可选）

        Returns:
            清单文件路径
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = operator_folder / f"材料清单_{timestamp}.json"

        # 准备清单数据
        materials_data = {
            "generated_at": datetime.now().isoformat(),
            "total_materials": len(self.materials),
            "uploaded_count": sum(1 for m in self.materials.values() if m.status == "uploaded"),
            "portal_uploaded_count": sum(1 for m in self.materials.values() if m.portal_uploaded),
            "materials": {
                key: {
                    "name": m.name,
                    "key": m.key,
                    "file_path": m.file_path,
                    "category": m.category,
                    "required": m.required,
                    "status": m.status,
                    "upload_time": m.upload_time,
                    "portal_uploaded": m.portal_uploaded,
                    "portal_upload_time": m.portal_upload_time
                }
                for key, m in self.materials.items()
            }
        }

        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(materials_data, f, ensure_ascii=False, indent=2)

        logger.info(f"导出材料清单: {output_file}")
        return output_file

    def _update_metadata(
        self,
        operator_folder: Path,
        material: MaterialFile
    ):
        """
        更新材料元数据

        Args:
            operator_folder: 经营者文件夹路径
            material: 材料对象
        """
        metadata_file = operator_folder / "metadata.json"

        # 读取现有元数据
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            metadata = {}

        # 更新材料信息
        if "materials" not in metadata:
            metadata["materials"] = {}

        metadata["materials"][material.key] = {
            "name": material.name,
            "file_path": material.file_path,
            "category": material.category,
            "status": material.status,
            "upload_time": material.upload_time,
            "portal_uploaded": material.portal_uploaded,
            "portal_upload_time": material.portal_upload_time
        }

        # 保存元数据
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)


# ==================== 便捷函数 ====================

def create_materials_folder(
    operator_name: str,
    business_name: Optional[str] = None,
    operator_id: Optional[int] = None
) -> MaterialFolderManager:
    """
    快速创建材料文件夹并返回管理器

    Args:
        operator_name: 经营者姓名
        business_name: 个体工商户名称
        operator_id: 经营者ID

    Returns:
        材料管理器实例
    """
    manager = MaterialFolderManager()
    operator_folder = manager.create_operator_folder(
        operator_name=operator_name,
        business_name=business_name,
        operator_id=operator_id
    )

    logger.info(f"材料文件夹已创建: {operator_folder}")
    logger.info(f"请将材料文件放入对应的子文件夹中")

    return manager


def add_material_from_file(
    manager: MaterialFolderManager,
    operator_folder: Path,
    key: str,
    file_path: str
) -> MaterialFile:
    """
    快速添加材料文件

    Args:
        manager: 材料管理器
        operator_folder: 经营者文件夹
        key: 材料键值
        file_path: 文件路径

    Returns:
        材料对象
    """
    return manager.add_material(
        operator_folder=operator_folder,
        key=key,
        file_path=file_path,
        copy=True
    )


if __name__ == "__main__":
    # 测试代码
    logger.info("=" * 60)
    logger.info("材料文件夹管理器测试")
    logger.info("=" * 60)

    # 创建管理器
    manager = MaterialFolderManager()

    # 创建测试文件夹
    operator_folder = manager.create_operator_folder(
        operator_name="张三",
        business_name="张三便利店",
        operator_id=1
    )

    logger.info(f"\n测试文件夹: {operator_folder}")
    logger.info("子文件夹结构:")
    for category in manager.CATEGORIES.values():
        logger.info(f"  - {category}")

    logger.info("\n请将材料文件放入对应文件夹，然后运行测试程序添加材料")
