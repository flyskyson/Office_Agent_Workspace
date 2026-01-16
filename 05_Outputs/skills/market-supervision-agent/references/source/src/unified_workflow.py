#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监管智能体 - 统一工作流引擎 v5.0

支持三输入源统一处理：
1. 文件上传 + OCR → 数据库
2. 政务服务网 Web 表单 → 数据库
3. Flask Web 表单 → 数据库

核心功能：
- 数据融合与校验
- 流程进度追踪（断点续传）
- 智能表单填写
- 材料智能校验
- 电子档案打包
- 多场景模板支持

作者: Claude Code
日期: 2026-01-14
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any, Literal, Callable
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum
from loguru import logger

# 导入核心模块
from .database_manager import DatabaseManager
from .application_generator import ApplicationGenerator
from .file_archiver import FileArchiver
from .ocr_adapter import create_ocr_engine
from .data_extractor import DataExtractor


# ============ 枚举定义 ============

class InputSource(Enum):
    """输入源类型"""
    OCR_UPLOAD = "ocr_upload"           # 文件上传+OCR
    WEB_PORTAL = "web_portal"           # 政务服务网
    WEB_FORM = "web_form"               # Flask Web表单


class WorkflowStage(Enum):
    """工作流阶段"""
    INIT = "init"                       # 初始化
    DATA_INPUT = "data_input"           # 数据输入
    DATA_FUSION = "data_fusion"         # 数据融合
    VALIDATION = "validation"           # 数据校验
    SUPPLEMENT = "supplement"           # 数据补充
    GENERATION = "generation"           # 文档生成
    ARCHIVING = "archiving"             # 档案归档
    COMPLETE = "complete"               # 完成


class MaterialStatus(Enum):
    """材料状态"""
    PENDING = "pending"                 # 待提交
    UPLOADED = "uploaded"               # 已上传
    VERIFIED = "verified"               # 已验证
    MISSING = "missing"                 # 缺失
    INVALID = "invalid"                 # 无效


# ============ 数据类定义 ============

@dataclass
class MaterialItem:
    """材料项"""
    name: str                           # 材料名称
    type: str                           # 材料类型 (id_card, business_license, etc.)
    required: bool = True              # 是否必需
    status: MaterialStatus = MaterialStatus.PENDING
    file_path: Optional[str] = None     # 文件路径
    ocr_result: Optional[Dict] = None   # OCR结果
    upload_time: Optional[str] = None   # 上传时间


@dataclass
class WorkflowProgress:
    """工作流进度"""
    operator_id: Optional[int] = None   # 经营户ID
    current_stage: WorkflowStage = WorkflowStage.INIT
    completed_stages: List[str] = field(default_factory=list)
    input_sources: List[str] = field(default_factory=list)

    # 数据完整性
    data_completeness: Dict[str, bool] = field(default_factory=dict)

    # 材料清单
    materials: Dict[str, MaterialItem] = field(default_factory=dict)

    # 时间戳
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # 错误信息
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowConfig:
    """工作流配置"""
    # 场景类型
    scenario: Literal["registration", "change", "cancellation", "annual_report"] = "registration"

    # 输入源配置
    enable_ocr: bool = True
    enable_web_portal: bool = True
    enable_web_form: bool = True

    # 输出配置
    auto_generate_document: bool = True
    auto_create_archive: bool = True
    generate_report: bool = True

    # 数据校验配置
    strict_validation: bool = False    # 严格模式：缺少必需材料时暂停
    auto_supplement: bool = True       # 自动补充默认值

    # 模板配置
    template_name: str = "个体工商户开业登记申请书（最终版）.docx"
    output_dir: str = "generated_applications"

    # 归档配置
    archive_base_dir: str = "archives"

    # 政务服务网配置
    portal_url: str = "https://zwfw.gxzf.gov.cn/yct/"
    portal_username: Optional[str] = None
    portal_password: Optional[str] = None


# ============ 统一工作流引擎 ============

class UnifiedWorkflowEngine:
    """统一工作流引擎 - 三输入源统一处理"""

    # 必需字段清单
    REQUIRED_FIELDS = {
        "registration": [
            "operator_name", "id_card", "phone",
            "business_name", "business_address", "business_scope"
        ],
        "change": [
            "operator_name", "id_card", "credit_code",
            "change_items"
        ],
        "cancellation": [
            "operator_name", "id_card", "credit_code"
        ],
        "annual_report": [
            "operator_name", "id_card", "credit_code",
            "annual_year"
        ]
    }

    # 材料清单
    MATERIAL_REQUIREMENTS = {
        "registration": [
            MaterialItem("身份证正面", "id_card_front", True),
            MaterialItem("身份证反面", "id_card_back", True),
            MaterialItem("经营场所证明", "property_cert", True),
            MaterialItem("租赁合同", "lease_contract", False),
        ],
        "change": [
            MaterialItem("身份证正面", "id_card_front", True),
            MaterialItem("营业执照", "business_license", True),
            MaterialItem("变更证明文件", "change_proof", True),
        ],
        "cancellation": [
            MaterialItem("身份证正面", "id_card_front", True),
            MaterialItem("营业执照", "business_license", True),
            MaterialItem("清税证明", "tax_proof", False),
        ],
        "annual_report": [
            MaterialItem("营业执照", "business_license", True),
        ]
    }

    def __init__(self, config: Optional[WorkflowConfig] = None):
        """初始化工作流引擎

        Args:
            config: 工作流配置
        """
        self.config = config or WorkflowConfig()

        # 初始化核心组件
        self.db_manager = DatabaseManager()
        self.doc_generator = ApplicationGenerator()
        self.file_archiver = FileArchiver()
        self.ocr_engine = create_ocr_engine()
        self.data_extractor = DataExtractor()

        # 工作流进度存储
        self.progress_db_path = Path("data/workflow_progress.db")
        self._init_progress_db()

        logger.info(f"统一工作流引擎初始化完成: scenario={self.config.scenario}")

    def _init_progress_db(self):
        """初始化进度数据库"""
        self.progress_db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(str(self.progress_db_path)) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS workflow_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operator_id INTEGER,
                    scenario TEXT,
                    current_stage TEXT,
                    completed_stages TEXT,
                    input_sources TEXT,
                    data_completeness TEXT,
                    materials TEXT,
                    errors TEXT,
                    warnings TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    metadata TEXT
                )
            ''')

            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_operator_id
                ON workflow_progress(operator_id)
            ''')

            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_scenario
                ON workflow_progress(scenario)
            ''')

        logger.info("进度数据库初始化完成")

    # ============ 核心工作流方法 ============

    def start_workflow(
        self,
        operator_data: Optional[Dict] = None,
        operator_id: Optional[int] = None
    ) -> WorkflowProgress:
        """启动或恢复工作流

        Args:
            operator_data: 经营户数据（可选）
            operator_id: 经营户ID（可选，用于恢复工作流）

        Returns:
            工作流进度对象
        """
        # 如果提供了 operator_id，尝试恢复现有工作流
        if operator_id:
            progress = self._load_progress(operator_id)
            if progress:
                logger.info(f"恢复工作流: operator_id={operator_id}, stage={progress.current_stage}")
                return progress

        # 创建新工作流
        progress = WorkflowProgress(
            current_stage=WorkflowStage.DATA_INPUT,
            input_sources=[],
            materials=self._init_materials()
        )

        # 保存初始数据
        if operator_data:
            progress.metadata['initial_data'] = operator_data
            progress.data_completeness = self._check_completeness(operator_data)

        self._save_progress(progress, operator_id)
        logger.info(f"创建新工作流: scenario={self.config.scenario}")

        return progress

    def process_ocr_input(
        self,
        files: List[str],
        progress: WorkflowProgress
    ) -> WorkflowProgress:
        """处理OCR输入（输入源①）

        Args:
            files: 文件路径列表
            progress: 工作流进度

        Returns:
            更新后的工作流进度
        """
        logger.info(f"处理OCR输入: {len(files)} 个文件")

        # 记录输入源
        if InputSource.OCR_UPLOAD.value not in progress.input_sources:
            progress.input_sources.append(InputSource.OCR_UPLOAD.value)

        try:
            # 1. 文件分类和OCR识别
            ocr_results = {}
            for file_path in files:
                category = self._classify_file(file_path)
                if category == "id_card":
                    result = self.ocr_engine.recognize_id_card(file_path)
                elif category == "business_license":
                    result = self.ocr_engine.recognize_business_license(file_path)
                else:
                    result = self.ocr_engine.recognize_image(file_path)

                ocr_results[file_path] = result

                # 更新材料状态
                if category in progress.materials:
                    progress.materials[category].status = MaterialStatus.UPLOADED
                    progress.materials[category].file_path = file_path
                    progress.materials[category].ocr_result = result
                    progress.materials[category].upload_time = datetime.now().isoformat()

            # 2. 数据提取
            extracted_data = self._extract_data_from_ocr(ocr_results, files)

            # 3. 保存到数据库
            if extracted_data.get('id_card'):
                existing = self.db_manager.get_operator_by_id_card(extracted_data['id_card'])
                if existing:
                    operator_id = existing['id']
                    self.db_manager.update_operator(existing['id'], extracted_data)
                else:
                    operator_id = self.db_manager.insert_operator(extracted_data)

                progress.operator_id = operator_id

            # 4. 更新进度
            progress.metadata['ocr_data'] = extracted_data
            progress.data_completeness.update(self._check_completeness(extracted_data))
            progress.updated_at = datetime.now().isoformat()

            self._save_progress(progress)
            logger.info(f"OCR输入处理完成: operator_id={progress.operator_id}")

        except Exception as e:
            error_msg = f"OCR处理失败: {str(e)}"
            progress.errors.append(error_msg)
            logger.error(error_msg)

        return progress

    def process_web_portal_input(
        self,
        portal_data: Dict,
        progress: WorkflowProgress
    ) -> WorkflowProgress:
        """处理政务服务网输入（输入源②）

        Args:
            portal_data: 从政务服务网获取的数据
            progress: 工作流进度

        Returns:
            更新后的工作流进度
        """
        logger.info("处理政务服务网输入")

        # 记录输入源
        if InputSource.WEB_PORTAL.value not in progress.input_sources:
            progress.input_sources.append(InputSource.WEB_PORTAL.value)

        try:
            # 1. 数据校验和清洗
            cleaned_data = self._clean_portal_data(portal_data)

            # 2. 保存/更新到数据库
            if cleaned_data.get('id_card'):
                existing = self.db_manager.get_operator_by_id_card(cleaned_data['id_card'])
                if existing:
                    operator_id = existing['id']
                    self.db_manager.update_operator(operator_id, cleaned_data)
                else:
                    operator_id = self.db_manager.insert_operator(cleaned_data)

                progress.operator_id = operator_id

            # 3. 更新进度
            progress.metadata['portal_data'] = cleaned_data
            progress.data_completeness.update(self._check_completeness(cleaned_data))
            progress.updated_at = datetime.now().isoformat()

            self._save_progress(progress)
            logger.info(f"政务服务网输入处理完成: operator_id={progress.operator_id}")

        except Exception as e:
            error_msg = f"政务服务网数据处理失败: {str(e)}"
            progress.errors.append(error_msg)
            logger.error(error_msg)

        return progress

    def process_web_form_input(
        self,
        form_data: Dict,
        progress: WorkflowProgress
    ) -> WorkflowProgress:
        """处理Flask Web表单输入（输入源③）

        Args:
            form_data: 表单数据
            progress: 工作流进度

        Returns:
            更新后的工作流进度
        """
        logger.info("处理Web表单输入")

        # 记录输入源
        if InputSource.WEB_FORM.value not in progress.input_sources:
            progress.input_sources.append(InputSource.WEB_FORM.value)

        try:
            # 1. 数据校验
            validated_data = self._validate_form_data(form_data)

            # 2. 保存/更新到数据库
            if validated_data.get('id_card'):
                existing = self.db_manager.get_operator_by_id_card(validated_data['id_card'])
                if existing:
                    operator_id = existing['id']
                    self.db_manager.update_operator(operator_id, validated_data)
                else:
                    operator_id = self.db_manager.insert_operator(validated_data)

                progress.operator_id = operator_id

            # 2. 更新进度
            progress.metadata['form_data'] = validated_data
            progress.data_completeness.update(self._check_completeness(validated_data))
            progress.updated_at = datetime.now().isoformat()

            self._save_progress(progress)
            logger.info(f"Web表单输入处理完成: operator_id={progress.operator_id}")

        except Exception as e:
            error_msg = f"Web表单处理失败: {str(e)}"
            progress.errors.append(error_msg)
            logger.error(error_msg)

        return progress

    def fuse_data(self, progress: WorkflowProgress) -> WorkflowProgress:
        """数据融合 - 合并多输入源数据

        Args:
            progress: 工作流进度

        Returns:
            更新后的工作流进度
        """
        logger.info("开始数据融合")

        progress.current_stage = WorkflowStage.DATA_FUSION

        # 收集所有数据源
        all_data = {}
        for source in [InputSource.OCR_UPLOAD.value, InputSource.WEB_PORTAL.value, InputSource.WEB_FORM.value]:
            if source in progress.metadata:
                source_key = f"{source}_data"
                if source_key in progress.metadata:
                    all_data.update(progress.metadata[source_key])

        # 数据融合策略：后面的覆盖前面的
        # 优先级: Web Form > Web Portal > OCR
        fusion_order = [
            f"{InputSource.OCR_UPLOAD.value}_data",
            f"{InputSource.WEB_PORTAL.value}_data",
            f"{InputSource.WEB_FORM.value}_data"
        ]

        fused_data = {}
        for source_key in fusion_order:
            if source_key in progress.metadata:
                fused_data.update(progress.metadata[source_key])

        # 保存融合后的数据
        progress.metadata['fused_data'] = fused_data
        progress.data_completeness = self._check_completeness(fused_data)

        self._save_progress(progress)
        logger.info(f"数据融合完成: {len(fused_data)} 个字段")

        return progress

    def validate_materials(self, progress: WorkflowProgress) -> WorkflowProgress:
        """材料智能校验

        Args:
            progress: 工作流进度

        Returns:
            更新后的工作流进度
        """
        logger.info("开始材料校验")

        progress.current_stage = WorkflowStage.VALIDATION

        required_materials = self.MATERIAL_REQUIREMENTS.get(self.config.scenario, [])

        for material in required_materials:
            material_key = material.type

            if material_key in progress.materials:
                item = progress.materials[material_key]

                # 检查材料状态
                if item.status == MaterialStatus.UPLOADED:
                    # 验证文件
                    if item.file_path and Path(item.file_path).exists():
                        item.status = MaterialStatus.VERIFIED
                    else:
                        item.status = MaterialStatus.INVALID
                        progress.warnings.append(f"材料文件不存在: {item.name}")

                # 检查必需材料
                if item.required and item.status == MaterialStatus.PENDING:
                    item.status = MaterialStatus.MISSING
                    if self.config.strict_validation:
                        progress.errors.append(f"缺少必需材料: {item.name}")

        self._save_progress(progress)
        logger.info("材料校验完成")

        return progress

    def supplement_data(self, progress: WorkflowProgress) -> WorkflowProgress:
        """智能数据补充

        Args:
            progress: 工作流进度

        Returns:
            更新后的工作流进度
        """
        logger.info("开始数据补充")

        progress.current_stage = WorkflowStage.SUPPLEMENT

        fused_data = progress.metadata.get('fused_data', {})

        # 应用默认值
        if self.config.auto_supplement:
            defaults = self.doc_generator.config.get('defaults', {})
            constants = self.doc_generator.config.get('constants', {})

            for key, value in {**defaults, **constants}.items():
                if key not in fused_data or not fused_data[key]:
                    fused_data[key] = value
                    progress.warnings.append(f"使用默认值: {key} = {value}")

        progress.metadata['supplemented_data'] = fused_data
        progress.data_completeness = self._check_completeness(fused_data)

        self._save_progress(progress)
        logger.info("数据补充完成")

        return progress

    def generate_outputs(self, progress: WorkflowProgress) -> WorkflowProgress:
        """生成所有输出

        Args:
            progress: 工作流进度

        Returns:
            更新后的工作流进度
        """
        logger.info("开始生成输出")

        progress.current_stage = WorkflowStage.GENERATION

        # 获取最终数据
        final_data = progress.metadata.get('supplemented_data') or progress.metadata.get('fused_data', {})

        if not final_data:
            progress.errors.append("没有可用的数据")
            return progress

        outputs = {}

        try:
            # 1. 生成Word申请书
            if self.config.auto_generate_document:
                doc_path = self.doc_generator.generate_application(
                    operator_data=final_data,
                    template_name=self.config.template_name,
                    output_dir=self.config.output_dir
                )
                outputs['document'] = doc_path
                logger.info(f"申请书生成: {doc_path}")

            # 2. 数据库记录已存在（在输入处理阶段已保存）
            outputs['database_id'] = progress.operator_id

            # 3. 生成流程报告
            if self.config.generate_report:
                report_path = self._generate_report(progress, final_data)
                outputs['report'] = report_path
                logger.info(f"流程报告生成: {report_path}")

            # 4. 电子档案打包
            if self.config.auto_create_archive:
                archive_path = self._create_electronic_archive(progress, final_data)
                outputs['archive'] = archive_path
                logger.info(f"电子档案创建: {archive_path}")

            progress.metadata['outputs'] = outputs
            progress.current_stage = WorkflowStage.COMPLETE

            # 标记完成的阶段
            if WorkflowStage.GENERATION.value not in progress.completed_stages:
                progress.completed_stages.append(WorkflowStage.GENERATION.value)

            self._save_progress(progress)
            logger.info("输出生成完成")

        except Exception as e:
            error_msg = f"生成输出失败: {str(e)}"
            progress.errors.append(error_msg)
            logger.error(error_msg)

        return progress

    # ============ 辅助方法 ============

    def _classify_file(self, file_path: str) -> str:
        """分类文件类型"""
        file_name = Path(file_path).name.lower()

        if 'id' in file_name or '身份证' in file_name:
            return 'id_card'
        elif 'license' in file_name or '营业执照' in file_name:
            return 'business_license'
        elif 'lease' in file_name or '租赁' in file_name:
            return 'lease_contract'
        elif 'property' in file_name or '产权' in file_name:
            return 'property_cert'
        else:
            return 'unknown'

    def _extract_data_from_ocr(self, ocr_results: Dict, files: List[str]) -> Dict:
        """从OCR结果提取数据"""
        extracted = {}

        for file_path, ocr_result in ocr_results.items():
            category = self._classify_file(file_path)

            try:
                if category == 'id_card':
                    data = self.data_extractor.extract_from_id_card(ocr_result, file_path)
                elif category == 'business_license':
                    data = self.data_extractor.extract_from_business_license(ocr_result, file_path)
                else:
                    data = self.data_extractor.extract_from_general_document(ocr_result, file_path)

                extracted.update(data)

            except Exception as e:
                logger.warning(f"数据提取失败: {file_path}, {e}")

        return extracted

    def _clean_portal_data(self, portal_data: Dict) -> Dict:
        """清洗政务服务网数据"""
        cleaned = {}

        # 字段映射（根据实际页面结构调整）
        field_mapping = {
            'operatorName': 'operator_name',
            'idCard': 'id_card',
            'phone': 'phone',
            'businessName': 'business_name',
            'businessAddress': 'business_address',
            'businessScope': 'business_scope',
            # 添加更多映射...
        }

        for portal_field, standard_field in field_mapping.items():
            if portal_field in portal_data:
                cleaned[standard_field] = portal_data[portal_field]

        return cleaned

    def _validate_form_data(self, form_data: Dict) -> Dict:
        """验证表单数据"""
        validated = {}

        # 只保留有效字段
        valid_fields = {
            'operator_name', 'id_card', 'phone', 'email',
            'business_name', 'business_address', 'business_scope',
            'gender', 'nation', 'address'
        }

        for key, value in form_data.items():
            if key in valid_fields and value:
                validated[key] = value

        return validated

    def _check_completeness(self, data: Dict) -> Dict[str, bool]:
        """检查数据完整性"""
        required = self.REQUIRED_FIELDS.get(self.config.scenario, [])
        completeness = {}

        for field in required:
            completeness[field] = bool(data.get(field))

        return completeness

    def _init_materials(self) -> Dict[str, MaterialItem]:
        """初始化材料清单"""
        materials = {}
        required_materials = self.MATERIAL_REQUIREMENTS.get(self.config.scenario, [])

        for material in required_materials:
            materials[material.type] = material

        return materials

    def _generate_report(self, progress: WorkflowProgress, data: Dict) -> str:
        """生成流程报告"""
        report_dir = Path(self.config.output_dir) / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        id_suffix = data.get('id_card', '')[-4:]
        report_file = report_dir / f"report_{id_suffix}_{timestamp}.json"

        report = {
            "workflow_info": {
                "scenario": self.config.scenario,
                "operator_id": progress.operator_id,
                "created_at": progress.created_at,
                "updated_at": progress.updated_at,
                "completed_stages": progress.completed_stages,
                "input_sources": progress.input_sources
            },
            "data": data,
            "data_completeness": progress.data_completeness,
            "materials": {
                k: {
                    "name": v.name,
                    "status": v.status.value,
                    "required": v.required
                }
                for k, v in progress.materials.items()
            },
            "outputs": progress.metadata.get('outputs', {}),
            "errors": progress.errors,
            "warnings": progress.warnings
        }

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return str(report_file)

    def _create_electronic_archive(self, progress: WorkflowProgress, data: Dict) -> str:
        """创建电子档案"""
        archive_base = Path(self.config.archive_base_dir)

        # 创建归档目录
        operator_name = data.get('operator_name', 'unknown')
        id_card = data.get('id_card', '')
        timestamp = datetime.now().strftime("%Y%m%d")

        archive_dir = archive_base / f"{operator_name}_{id_card[-4:]}_{timestamp}"
        archive_dir.mkdir(parents=True, exist_ok=True)

        # 复制材料文件
        files_copied = []
        for material_key, material in progress.materials.items():
            if material.file_path and Path(material.file_path).exists():
                dest_file = archive_dir / f"{material.name}_{Path(material.file_path).suffix}"
                import shutil
                shutil.copy2(material.file_path, dest_file)
                files_copied.append(str(dest_file))

        # 复制生成的文档
        outputs = progress.metadata.get('outputs', {})
        if 'document' in outputs:
            doc_path = Path(outputs['document'])
            if doc_path.exists():
                shutil.copy2(doc_path, archive_dir / "申请书.docx")
                files_copied.append(str(archive_dir / "申请书.docx"))

        # 复制流程报告
        if 'report' in outputs:
            report_path = Path(outputs['report'])
            if report_path.exists():
                shutil.copy2(report_path, archive_dir / "流程报告.json")

        # 保存数据JSON
        data_file = archive_dir / "经营户数据.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return str(archive_dir)

    def _save_progress(self, progress: WorkflowProgress, operator_id: Optional[int] = None):
        """保存工作流进度"""
        id_to_save = operator_id or progress.operator_id

        with sqlite3.connect(str(self.progress_db_path)) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO workflow_progress (
                    id, operator_id, scenario, current_stage,
                    completed_stages, input_sources, data_completeness,
                    materials, errors, warnings, created_at, updated_at, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                id_to_save,  # 使用 operator_id 作为主键
                progress.operator_id,
                self.config.scenario,
                progress.current_stage.value,
                json.dumps(progress.completed_stages, ensure_ascii=False),
                json.dumps(progress.input_sources, ensure_ascii=False),
                json.dumps(progress.data_completeness, ensure_ascii=False),
                json.dumps({k: {
                    'name': v.name,
                    'type': v.type,
                    'required': v.required,
                    'status': v.status.value,
                    'file_path': v.file_path,
                    'upload_time': v.upload_time
                } for k, v in progress.materials.items()}, ensure_ascii=False),
                json.dumps(progress.errors, ensure_ascii=False),
                json.dumps(progress.warnings, ensure_ascii=False),
                progress.created_at,
                progress.updated_at,
                json.dumps(progress.metadata, ensure_ascii=False)
            ))

    def _load_progress(self, operator_id: int) -> Optional[WorkflowProgress]:
        """加载工作流进度"""
        with sqlite3.connect(str(self.progress_db_path)) as conn:
            cursor = conn.execute(
                'SELECT * FROM workflow_progress WHERE operator_id = ?',
                (operator_id,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            # 解析数据
            columns = [
                'id', 'operator_id', 'scenario', 'current_stage',
                'completed_stages', 'input_sources', 'data_completeness',
                'materials', 'errors', 'warnings', 'created_at', 'updated_at', 'metadata'
            ]
            data = dict(zip(columns, row))

            # 重建进度对象
            materials_dict = json.loads(data['materials']) if data['materials'] else {}
            materials = {}
            for key, value in materials_dict.items():
                materials[key] = MaterialItem(
                    name=value['name'],
                    type=value['type'],
                    required=value['required'],
                    status=MaterialStatus(value['status']),
                    file_path=value.get('file_path'),
                    upload_time=value.get('upload_time')
                )

            progress = WorkflowProgress(
                operator_id=data['operator_id'],
                current_stage=WorkflowStage(data['current_stage']),
                completed_stages=json.loads(data['completed_stages']),
                input_sources=json.loads(data['input_sources']),
                data_completeness=json.loads(data['data_completeness']),
                materials=materials,
                errors=json.loads(data['errors']),
                warnings=json.loads(data['warnings']),
                created_at=data['created_at'],
                updated_at=data['updated_at'],
                metadata=json.loads(data['metadata'])
            )

            return progress

    def get_progress_summary(self, operator_id: int) -> Optional[Dict]:
        """获取工作流进度摘要"""
        progress = self._load_progress(operator_id)
        if not progress:
            return None

        return {
            "operator_id": progress.operator_id,
            "current_stage": progress.current_stage.value,
            "completed_stages": progress.completed_stages,
            "input_sources": progress.input_sources,
            "data_completeness": progress.data_completeness,
            "materials_status": {
                k: v.status.value for k, v in progress.materials.items()
            },
            "has_errors": len(progress.errors) > 0,
            "error_count": len(progress.errors),
            "warning_count": len(progress.warnings),
            "created_at": progress.created_at,
            "updated_at": progress.updated_at
        }


# ============ 便捷函数 ============

def create_workflow(
    scenario: Literal["registration", "change", "cancellation", "annual_report"] = "registration",
    config: Optional[Dict] = None
) -> UnifiedWorkflowEngine:
    """创建工作流引擎

    Args:
        scenario: 场景类型
        config: 配置字典

    Returns:
        工作流引擎实例
    """
    workflow_config = WorkflowConfig(scenario=scenario)

    if config:
        for key, value in config.items():
            if hasattr(workflow_config, key):
                setattr(workflow_config, key, value)

    return UnifiedWorkflowEngine(workflow_config)


def quick_start_registration(operator_data: Dict) -> Dict:
    """快速启动个体工商户设立流程

    Args:
        operator_data: 经营户数据

    Returns:
        结果字典
    """
    workflow = create_workflow("registration")
    progress = workflow.start_workflow(operator_data=operator_data)

    # 处理数据
    progress = workflow.fuse_data(progress)
    progress = workflow.supplement_data(progress)
    progress = workflow.validate_materials(progress)
    progress = workflow.generate_outputs(progress)

    return {
        "success": len(progress.errors) == 0,
        "operator_id": progress.operator_id,
        "outputs": progress.metadata.get('outputs', {}),
        "errors": progress.errors,
        "warnings": progress.warnings,
        "completeness": progress.data_completeness
    }
