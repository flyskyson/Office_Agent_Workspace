"""
OCR 适配器 - 支持 PaddleOCR 和百度 OCR 自动切换

优先级：
1. 如果配置了百度 OCR，优先使用百度 OCR（云端识别，准确率高）
2. 否则使用 PaddleOCR（本地识别，无需联网）
"""

from pathlib import Path
from typing import Dict, Optional
from loguru import logger

# 检查可用的 OCR 引擎
try:
    from paddleocr import PaddleOCR
    HAS_PADDLEOCR = True
except ImportError:
    HAS_PADDLEOCR = False
    logger.warning("PaddleOCR 未安装")

try:
    from .baidu_ocr_engine import BaiduOCREngine, HAS_BAIDU_OCR
except (ImportError, SyntaxError):
    HAS_BAIDU_OCR = False
    BaiduOCREngine = None
    logger.warning("百度 OCR 引擎未找到")


class OCREngineAdapter:
    """OCR 引擎适配器 - 自动选择可用的 OCR 引擎"""

    def __init__(
        self,
        engine: str = "auto",
        baidu_config: str = "config/baidu_ocr.yaml",
        use_angle_cls: bool = True,
        lang: str = "ch"
    ):
        """初始化 OCR 适配器

        Args:
            engine: OCR 引擎类型 ("auto", "paddle", "baidu")
            baidu_config: 百度 OCR 配置文件路径
            use_angle_cls: PaddleOCR 是否使用方向分类器
            lang: PaddleOCR 语言设置
        """
        self.engine_type = engine
        self.baidu_config = baidu_config
        self.use_angle_cls = use_angle_cls
        self.lang = lang

        self._paddle_engine = None
        self._baidu_engine = None
        self._active_engine = None

        # 初始化引擎
        self._initialize()

    def _initialize(self):
        """初始化 OCR 引擎"""
        if self.engine_type == "auto":
            # 自动选择：优先百度 OCR
            if self._try_baidu():
                logger.info("使用百度 OCR 引擎")
                self._active_engine = "baidu"
            elif self._try_paddle():
                logger.info("使用 PaddleOCR 引擎")
                self._active_engine = "paddle"
            else:
                raise RuntimeError(
                    "没有可用的 OCR 引擎！请安装以下任一：\n"
                    "1. 百度 OCR: pip install baidu-aip\n"
                    "2. PaddleOCR: pip install paddleocr paddlepaddle"
                )
        elif self.engine_type == "baidu":
            if not self._try_baidu():
                raise RuntimeError("百度 OCR 不可用，请安装: pip install baidu-aip")
            self._active_engine = "baidu"
        elif self.engine_type == "paddle":
            if not self._try_paddle():
                raise RuntimeError("PaddleOCR 不可用，请安装: pip install paddleocr")
            self._active_engine = "paddle"
        else:
            raise ValueError(f"不支持的引擎类型: {self.engine_type}")

    def _try_baidu(self) -> bool:
        """尝试初始化百度 OCR"""
        if not HAS_BAIDU_OCR:
            return False

        try:
            self._baidu_engine = BaiduOCREngine(config_file=self.baidu_config)
            # 测试一下是否配置了凭证
            self._baidu_engine._initialize()
            return True
        except Exception as e:
            logger.debug(f"百度 OCR 不可用: {e}")
            return False

    def _try_paddle(self) -> bool:
        """尝试初始化 PaddleOCR"""
        if not HAS_PADDLEOCR:
            return False

        try:
            self._paddle_engine = PaddleOCR(
                use_angle_cls=self.use_angle_cls,
                lang=self.lang
            )
            return True
        except Exception as e:
            logger.debug(f"PaddleOCR 初始化失败: {e}")
            return False

    def recognize_id_card(self, image_path: str) -> Dict:
        """识别身份证

        Args:
            image_path: 身份证图片路径

        Returns:
            身份证信息字典
        """
        if self._active_engine == "baidu":
            return self._baidu_engine.recognize_id_card(image_path)
        else:
            return self._paddle_recognize_id_card(image_path)

    def recognize_business_license(self, image_path: str) -> Dict:
        """识别营业执照

        Args:
            image_path: 营业执照图片路径

        Returns:
            营业执照信息字典
        """
        if self._active_engine == "baidu":
            return self._baidu_engine.recognize_business_license(image_path)
        else:
            return self._paddle_recognize_business_license(image_path)

    def recognize_image(self, image_path: str) -> Dict:
        """通用文字识别

        Args:
            image_path: 图片路径

        Returns:
            识别结果字典
        """
        if self._active_engine == "baidu":
            return self._baidu_engine.recognize_image(image_path)
        else:
            return self._paddle_recognize_image(image_path)

    def recognize_contract(self, image_path: str) -> Dict:
        """识别租赁合同等文档

        Args:
            image_path: 合同图片路径

        Returns:
            合同信息字典
        """
        if self._active_engine == "baidu":
            return self._baidu_engine.recognize_contract(image_path)
        else:
            return self._paddle_recognize_image(image_path)

    # ========== PaddleOCR 后备方法 ==========

    def _paddle_recognize_id_card(self, image_path: str) -> Dict:
        """PaddleOCR 识别身份证"""
        result = self._paddle_engine.ocr(image_path, cls=True)

        if not result or not result[0]:
            return {}

        # 提取文本
        lines = [line[1][0] for line in result[0]]
        text = "\n".join(lines)

        # 解析身份证信息
        info = self._parse_id_card_text(text)
        return info

    def _paddle_recognize_business_license(self, image_path: str) -> Dict:
        """PaddleOCR 识别营业执照"""
        result = self._paddle_engine.ocr(image_path, cls=True)

        if not result or not result[0]:
            return {}

        lines = [line[1][0] for line in result[0]]
        text = "\n".join(lines)

        # 解析营业执照信息
        return self._parse_business_license_text(text)

    def _paddle_recognize_image(self, image_path: str) -> Dict:
        """PaddleOCR 通用识别"""
        # 移除cls参数以兼容新版PaddleOCR
        result = self._paddle_engine.ocr(image_path)

        if not result or not result[0]:
            return {"text": "", "words_result": []}

        lines = [line[1][0] for line in result[0]]
        text = "\n".join(lines)

        return {
            "text": text,
            "words_result": [{"words": line} for line in lines]
        }

    def _parse_id_card_text(self, text: str) -> Dict:
        """从 OCR 文本解析身份证信息"""
        import re

        info = {}

        # 姓名
        name_match = re.search(r'姓名[：:]\s*([\u4e00-\u9fa5]{2,4})', text)
        if name_match:
            info["name"] = name_match.group(1)

        # 身份证号
        id_match = re.search(
            r'[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]',
            text
        )
        if id_match:
            info["id_card"] = id_match.group(0)

        # 性别
        gender_match = re.search(r'性别[：:]\s*([男女])', text)
        if gender_match:
            info["gender"] = gender_match.group(1)

        # 民族
        nation_match = re.search(r'民族[：:]\s*([\u4e00-\u9fa5]{2,4})', text)
        if nation_match:
            info["nation"] = nation_match.group(1)
            info["ethnicity"] = nation_match.group(1)

        # 从身份证号推断性别
        if "id_card" in info and "gender" not in info:
            gender_code = int(info["id_card"][16])
            info["gender"] = "女" if gender_code % 2 == 0 else "男"

        return info

    def _parse_business_license_text(self, text: str) -> Dict:
        """从 OCR 文本解析营业执照信息"""
        import re

        info = {}

        # 名称
        patterns = [
            r'名称[：:]\s*([^\n]+)',
            r'经营者名称[：:]\s*([^\n]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                info["company_name"] = match.group(1).strip()
                break

        # 统一社会信用代码
        credit_match = re.search(r'统一社会信用代码[：:]\s*([A-Z0-9]{18})', text)
        if credit_match:
            info["credit_code"] = credit_match.group(1)

        # 经营者/法定代表人
        patterns = [
            r'经营者[：:]\s*([\u4e00-\u9fa5]{2,4})',
            r'法定代表人[：:]\s*([\u4e00-\u9fa5]{2,4})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                info["legal_person"] = match.group(1).strip()
                break

        # 地址
        patterns = [
            r'经营场所[：:]\s*([^\n]+?)(?:\n|电话|经营范围)',
            r'住所[：:]\s*([^\n]+?)(?:\n|电话|经营范围)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                info["address"] = match.group(1).strip()
                break

        # 经营范围
        scope_match = re.search(
            r'经营范围[：:]\s*([^\n]+?)(?:\n|成立日期|经营期限)',
            text,
            re.DOTALL
        )
        if scope_match:
            info["business_scope"] = scope_match.group(1).strip()

        return info

    @property
    def active_engine(self) -> str:
        """获取当前激活的 OCR 引擎"""
        return self._active_engine


# ============ 便捷函数 ============

def create_ocr_engine(engine: str = "auto", baidu_config: str = "config/baidu_ocr.yaml"):
    """创建 OCR 引擎的便捷函数

    Args:
        engine: OCR 引擎类型 ("auto", "paddle", "baidu")
        baidu_config: 百度 OCR 配置文件路径

    Returns:
        OCREngineAdapter 实例
    """
    return OCREngineAdapter(engine=engine, baidu_config=baidu_config)
