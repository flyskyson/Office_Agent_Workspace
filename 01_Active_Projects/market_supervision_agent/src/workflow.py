"""
LangGraph工作流引擎 - 自动化申请处理流程

实现完整的自动化工作流：
文件监控 → OCR识别 → 数据提取 → 数据库存储
→ 文件归档 → 申请书生成 → UI表单补充
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Literal
from datetime import datetime
from loguru import logger

# 尝试导入 LangGraph
try:
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    logger.warning("LangGraph未安装，将使用简化版工作流")

# 导入核心模块
from .ocr_adapter import OCREngineAdapter, create_ocr_engine
from .data_extractor import DataExtractor, OperatorData
from .database_manager import DatabaseManager
from .file_archiver import FileArchiver
from .application_generator import ApplicationGenerator


# ============ 工作流状态定义 ============

class WorkflowState(Dict):
    """工作流状态

    继承自Dict，可以像字典一样访问，也可以使用点语法
    """

    def __init__(self, **kwargs):
        # 默认状态
        default_state = {
            # 当前步骤
            "current_step": "waiting",

            # 消息列表
            "messages": [],

            # 文件信息
            "detected_files": [],
            "file_categories": {},

            # OCR结果
            "ocr_results": {},

            # 提取的数据
            "extracted_data": {},

            # 数据库操作
            "operator_id": None,
            "database_status": "",

            # 归档信息
            "archive_path": None,

            # 生成结果
            "generated_document": None,

            # 错误处理
            "error_message": None,
            "retry_count": 0,
            "max_retries": 3,

            # 配置
            "config": {
                "skip_ocr": False,          # 跳过OCR（测试用）
                "skip_archiving": False,    # 跳过归档
                "skip_generation": False,   # 跳过申请书生成
                "auto_clean_desktop": True, # 自动清理桌面
                "desktop_path": "",         # 桌面路径
            }
        }

        # 合并用户输入
        default_state.update(kwargs)
        super().__init__(default_state)


# ============ LangGraph 工作流（完整版） ============

class MarketSupervisionWorkflow:
    """市场监管申请处理工作流"""

    def __init__(self, config: Optional[Dict] = None):
        """初始化工作流

        Args:
            config: 配置字典
        """
        self.config = config or {}

        # 初始化各个组件
        # 使用 OCR 适配器（自动选择百度 OCR 或 PaddleOCR）
        self.ocr_engine = create_ocr_engine()
        self.data_extractor = DataExtractor()
        self.db_manager = DatabaseManager()
        self.file_archiver = FileArchiver()
        self.doc_generator = ApplicationGenerator()

        # 构建工作流图
        self.workflow = None
        if HAS_LANGGRAPH:
            self.workflow = self._build_workflow()
            logger.info("LangGraph工作流构建成功")
        else:
            logger.info("使用简化版工作流")

    def _build_workflow(self):
        """构建LangGraph工作流图

        Returns:
            编译后的工作流
        """
        # 创建状态图
        workflow = StateGraph(WorkflowState)

        # 添加节点
        workflow.add_node("classify_files", self._classify_files_node)
        workflow.add_node("ocr_process", self._ocr_process_node)
        workflow.add_node("extract_data", self._extract_data_node)
        workflow.add_node("save_to_db", self._save_to_db_node)
        workflow.add_node("archive_files", self._archive_files_node)
        workflow.add_node("generate_document", self._generate_document_node)
        workflow.add_node("handle_error", self._handle_error_node)

        # 设置入口点
        workflow.set_entry_point("classify_files")

        # 添加边
        workflow.add_edge("classify_files", "ocr_process")
        workflow.add_edge("ocr_process", "extract_data")
        workflow.add_edge("extract_data", "save_to_db")

        # 条件边
        workflow.add_conditional_edges(
            "save_to_db",
            self._should_generate_document,
            {
                "generate": "generate_document",
                "archive": "archive_files",
                "error": "handle_error"
            }
        )

        workflow.add_edge("generate_document", "archive_files")
        workflow.add_edge("archive_files", END)
        workflow.add_edge("handle_error", END)

        # 编译工作流（使用内存检查点）
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory, interrupt_before=["handle_error"])

    # ============ 节点实现 ============

    def _classify_files_node(self, state: WorkflowState) -> WorkflowState:
        """文件分类节点

        根据文件名和扩展名对文件进行分类
        """
        state["current_step"] = "classifying"
        state["messages"].append(f"开始文件分类...")

        files = state.get("detected_files", [])
        categories = {}

        for file_path in files:
            category = self.file_archiver.categorize_file(file_path)
            categories[file_path] = category

        state["file_categories"] = categories
        state["messages"].append(f"已分类 {len(files)} 个文件")

        logger.info(f"文件分类完成: {categories}")
        return state

    def _ocr_process_node(self, state: WorkflowState) -> WorkflowState:
        """OCR处理节点

        对不同类型的文件执行OCR识别
        """
        state["current_step"] = "ocr_processing"
        state["messages"].append("开始OCR识别...")

        # 如果配置跳过OCR
        if state["config"].get("skip_ocr", False):
            state["messages"].append("跳过OCR识别（测试模式）")
            return state

        ocr_results = {}

        for file_path, category in state.get("file_categories", {}).items():
            try:
                if category == "id_card":
                    result = self.ocr_engine.recognize_id_card(file_path)
                elif category == "business_license":
                    result = self.ocr_engine.recognize_business_license(file_path)
                elif category == "lease_contract":
                    result = self.ocr_engine.recognize_contract(file_path)
                else:
                    result = self.ocr_engine.recognize_image(file_path)

                ocr_results[file_path] = result
                state["messages"].append(f"OCR识别成功: {Path(file_path).name}")

            except Exception as e:
                state["messages"].append(f"OCR识别失败 {file_path}: {str(e)}")
                logger.error(f"OCR识别失败: {file_path}, 错误: {e}")
                ocr_results[file_path] = {}

        state["ocr_results"] = ocr_results
        logger.info(f"OCR识别完成: {len(ocr_results)} 个文件")
        return state

    def _extract_data_node(self, state: WorkflowState) -> WorkflowState:
        """数据提取节点

        从OCR结果中提取结构化数据
        """
        state["current_step"] = "extracting"
        state["messages"].append("开始数据提取...")

        extracted = {}
        ocr_results = state.get("ocr_results", {})
        file_categories = state.get("file_categories", {})

        for file_path, ocr_result in ocr_results.items():
            category = file_categories.get(file_path, "unknown")

            # 调试信息
            logger.info(f"处理文件: {file_path}, 类别: {category}, OCR结果: {ocr_result}")

            try:
                if category == "id_card":
                    data = self.data_extractor.extract_from_id_card(ocr_result, file_path)
                elif category == "business_license":
                    data = self.data_extractor.extract_from_business_license(ocr_result, file_path)
                elif category == "lease_contract":
                    data = self.data_extractor.extract_from_lease_contract(ocr_result, file_path)
                elif category == "property_cert":
                    data = self.data_extractor.extract_from_property_cert(ocr_result, file_path)
                else:
                    data = self.data_extractor.extract_from_general_document(ocr_result, file_path)

                extracted.update(data)

            except Exception as e:
                state["messages"].append(f"数据提取失败 {file_path}: {str(e)}")
                logger.error(f"数据提取失败: {file_path}, 错误: {e}")

        # 验证并创建数据对象
        try:
            operator_data = self.data_extractor.merge_data(extracted)
            state["extracted_data"] = operator_data.to_dict()
            state["messages"].append(f"数据提取成功: {operator_data.operator_name}")
            logger.info(f"数据提取成功: {operator_data.operator_name}")
        except Exception as e:
            error_msg = str(e)
            # 提供更友好的错误提示
            if "operator_name" in error_msg and "id_card" in error_msg:
                friendly_error = "数据不完整：缺少经营者姓名或身份证号。请上传身份证照片。"
            elif "id_card" in error_msg:
                friendly_error = "数据不完整：缺少身份证号。请上传身份证照片。"
            elif "operator_name" in error_msg:
                friendly_error = "数据不完整：缺少经营者姓名。"
            else:
                friendly_error = f"数据验证失败: {error_msg}"

            state["error_message"] = friendly_error
            state["messages"].append(friendly_error)
            logger.error(f"数据验证失败: {e}")

        return state

    def _save_to_db_node(self, state: WorkflowState) -> WorkflowState:
        """保存到数据库节点

        将提取的数据保存到SQLite数据库
        """
        state["current_step"] = "saving_to_db"
        state["messages"].append("保存到数据库...")

        extracted_data = state.get("extracted_data", {})

        if not extracted_data.get("id_card"):
            state["error_message"] = "缺少身份证号，无法保存"
            state["database_status"] = "error"
            state["messages"].append(state["error_message"])
            return state

        try:
            # 检查是否已存在
            existing = self.db_manager.get_operator_by_id_card(extracted_data["id_card"])

            if existing:
                # 更新现有记录
                operator_id = existing["id"]

                # 如果记录是 deleted 状态，恢复为 active
                if existing.get("status") == "deleted":
                    extracted_data["status"] = "active"
                    state["messages"].append(f"恢复已删除的记录: ID={operator_id}")
                else:
                    state["messages"].append(f"更新现有记录: ID={operator_id}")

                self.db_manager.update_operator(
                    extracted_data["id_card"],
                    extracted_data
                )
                state["operator_id"] = operator_id
                state["database_status"] = "updated"
            else:
                # 插入新记录
                operator_id = self.db_manager.insert_operator(extracted_data)
                state["operator_id"] = operator_id
                state["database_status"] = "saved"
                state["messages"].append(f"保存新记录: ID={operator_id}")

            logger.info(f"数据库操作成功: ID={operator_id}, 状态={state['database_status']}")

        except Exception as e:
            state["error_message"] = f"数据库保存失败: {str(e)}"
            state["database_status"] = "error"
            state["messages"].append(state["error_message"])
            logger.error(f"数据库保存失败: {e}")

        return state

    def _archive_files_node(self, state: WorkflowState) -> WorkflowState:
        """文件归档节点

        将文件归档到指定目录
        """
        state["current_step"] = "archiving"
        state["messages"].append("归档文件...")

        if state["config"].get("skip_archiving", False):
            state["messages"].append("跳过文件归档（测试模式）")
            return state

        extracted_data = state.get("extracted_data", {})

        if not extracted_data.get("operator_name") or not extracted_data.get("id_card"):
            state["messages"].append("缺少必要信息，跳过归档")
            return state

        try:
            archive_path = self.file_archiver.archive_operator_files(
                operator_name=extracted_data["operator_name"],
                id_card=extracted_data["id_card"],
                files=state.get("file_categories", {})
            )
            state["archive_path"] = archive_path
            state["messages"].append(f"文件已归档到: {archive_path}")
            logger.info(f"文件归档成功: {archive_path}")

            # 清理桌面
            if state["config"].get("auto_clean_desktop", False):
                desktop_path = state["config"].get("desktop_path", "")
                if desktop_path:
                    cleaned = self.file_archiver.clean_desktop(
                        desktop_path,
                        list(state.get("detected_files", []))
                    )
                    state["messages"].append(f"清理桌面: {cleaned} 个文件")

        except Exception as e:
            state["messages"].append(f"归档失败: {str(e)}")
            logger.error(f"归档失败: {e}")

        return state

    def _generate_document_node(self, state: WorkflowState) -> WorkflowState:
        """生成申请书节点

        使用数据生成申请书文档
        """
        state["current_step"] = "generating"
        state["messages"].append("生成申请书...")

        if state["config"].get("skip_generation", False):
            state["messages"].append("跳过申请书生成（测试模式）")
            return state

        extracted_data = state.get("extracted_data", {})

        if not extracted_data.get("business_name"):
            state["messages"].append("缺少店名，跳过申请书生成")
            return state

        try:
            output_path = self.doc_generator.generate_application(
                operator_data=extracted_data,
                output_dir="output"
            )
            state["generated_document"] = output_path
            state["messages"].append(f"申请书已生成: {output_path}")
            logger.info(f"申请书生成成功: {output_path}")

        except Exception as e:
            state["messages"].append(f"生成失败: {str(e)}")
            logger.error(f"申请书生成失败: {e}")

        return state

    def _handle_error_node(self, state: WorkflowState) -> WorkflowState:
        """错误处理节点

        处理工作流中的错误
        """
        state["current_step"] = "error"
        state["messages"].append(f"处理出错: {state.get('error_message', '未知错误')}")
        logger.error(f"工作流错误: {state.get('error_message')}")
        return state

    # ============ 条件路由 ============

    def _should_generate_document(self, state: WorkflowState) -> str:
        """决定是否生成文档

        Returns:
            "generate" - 生成申请书
            "archive" - 直接归档
            "error" - 错误处理
        """
        if state.get("error_message"):
            return "error"

        # 如果有经营户名称，就生成申请书
        if state.get("extracted_data", {}).get("business_name"):
            return "generate"

        return "archive"

    # ============ 执行方法 ============

    def process(self, files: List[str], config: Optional[Dict] = None) -> WorkflowState:
        """处理一批文件

        Args:
            files: 文件路径列表
            config: 配置字典

        Returns:
            最终状态
        """
        # 合并配置
        merged_config = self.config.copy()
        if config:
            merged_config.update(config)

        # 初始状态
        initial_state = WorkflowState(
            detected_files=files,
            config=merged_config
        )

        # 执行工作流
        if self.workflow and HAS_LANGGRAPH:
            # 使用LangGraph
            thread_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            result = self.workflow.invoke(
                initial_state,
                config={"configurable": {"thread_id": thread_id}}
            )
        else:
            # 使用简化版工作流
            result = self._run_simple_workflow(initial_state)

        return result

    def _run_simple_workflow(self, state: WorkflowState) -> WorkflowState:
        """简化版工作流（不使用LangGraph）

        Args:
            state: 初始状态

        Returns:
            最终状态
        """
        try:
            # 1. 文件分类
            state = self._classify_files_node(state)

            # 2. OCR识别
            state = self._ocr_process_node(state)

            # 3. 数据提取
            state = self._extract_data_node(state)

            # 4. 保存到数据库
            state = self._save_to_db_node(state)

            # 5. 决定下一步
            if state.get("error_message"):
                state = self._handle_error_node(state)
            else:
                # 6. 生成申请书（如果有店名）
                if state.get("extracted_data", {}).get("business_name"):
                    state = self._generate_document_node(state)

                # 7. 文件归档
                state = self._archive_files_node(state)

        except Exception as e:
            state["error_message"] = f"工作流执行失败: {str(e)}"
            state = self._handle_error_node(state)
            logger.error(f"工作流执行失败: {e}")

        return state


# ============ 便捷函数 ============

def process_files(
    files: List[str],
    config: Optional[Dict] = None,
    desktop_path: str = ""
) -> WorkflowState:
    """便捷函数：处理一批文件

    Args:
        files: 文件路径列表
        config: 配置字典
        desktop_path: 桌面路径（用于清理）

    Returns:
        最终状态
    """
    workflow = MarketSupervisionWorkflow(config)

    if desktop_path:
        if config is None:
            config = {}
        config["desktop_path"] = desktop_path

    return workflow.process(files, config)


def quick_process(
    id_card_path: str,
    license_path: str,
    output_dir: str = "output"
) -> Dict:
    """快速处理：最常见的场景

    Args:
        id_card_path: 身份证图片路径
        license_path: 营业执照图片路径
        output_dir: 输出目录

    Returns:
        结果字典
    """
    files = [id_card_path, license_path]

    state = process_files(files, config={
        "skip_archiving": True,
        "auto_clean_desktop": False
    })

    return {
        "success": state.get("error_message") is None,
        "operator_data": state.get("extracted_data"),
        "operator_id": state.get("operator_id"),
        "messages": state.get("messages", []),
        "error": state.get("error_message")
    }
