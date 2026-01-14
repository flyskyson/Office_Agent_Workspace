"""
OCR识别引擎 - 使用PaddleOCR识别文档

支持的文档类型：
- 身份证（正反面）
- 营业执照
- 租赁合同
- 产权证明
- 通用文档
"""

import cv2
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from loguru import logger


class OCREngine:
    """OCR识别引擎"""

    def __init__(self, use_gpu: bool = False):
        """初始化OCR引擎

        Args:
            use_gpu: 是否使用GPU加速
        """
        self.use_gpu = use_gpu
        self.ocr = None
        self._initialized = False

    def _initialize(self):
        """延迟初始化PaddleOCR（避免导入时立即加载）"""
        if self._initialized:
            return

        try:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(
                use_angle_cls=True,  # 启用文字方向分类
                lang='ch',           # 中文识别
                use_gpu=self.use_gpu,
                show_log=False
            )
            self._initialized = True
            logger.info("PaddleOCR初始化成功")
        except ImportError:
            logger.error("PaddleOCR未安装，请运行: pip install paddleocr")
            raise
        except Exception as e:
            logger.error(f"PaddleOCR初始化失败: {e}")
            raise

    def recognize_image(self, image_path: str) -> Dict:
        """识别图片中的文字

        Args:
            image_path: 图片路径

        Returns:
            识别结果字典
            {
                "text": "识别的完整文本",
                "regions": [
                    {"box": [x1,y1,x2,y2], "text": "区域文字", "confidence": 0.95}
                ]
            }
        """
        self._initialize()

        if not Path(image_path).exists():
            raise FileNotFoundError(f"文件不存在: {image_path}")

        try:
            result = self.ocr.ocr(image_path, cls=True)
            return self._parse_result(result)
        except Exception as e:
            logger.error(f"OCR识别失败: {image_path}, 错误: {e}")
            return {"text": "", "regions": []}

    def recognize_id_card(self, image_path: str) -> Dict:
        """专门识别身份证

        Args:
            image_path: 身份证图片路径

        Returns:
            {
                "name": "张三",
                "id_card": "110101199001011234",
                "address": "北京市...",
                "ethnicity": "汉",
                "gender": "男"
            }
        """
        self._initialize()

        try:
            # 预处理身份证图片
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"无法读取图片: {image_path}")

            img_processed = self._preprocess_id_card(img)

            # 识别
            result = self.ocr.ocr(img_processed, cls=True)

            # 解析身份证特定格式
            info = self._parse_id_card(result)

            logger.info(f"身份证识别成功: {image_path}")
            return info

        except Exception as e:
            logger.error(f"身份证识别失败: {image_path}, 错误: {e}")
            return {}

    def recognize_business_license(self, image_path: str) -> Dict:
        """识别营业执照

        Args:
            image_path: 营业执照图片路径

        Returns:
            {
                "company_name": "XX公司",
                "credit_code": "91110000XXXXXXXXXX",
                "address": "...",
                "legal_person": "...",
                "business_scope": "..."
            }
        """
        self._initialize()

        try:
            result = self.ocr.ocr(image_path, cls=True)
            info = self._parse_business_license(result)

            logger.info(f"营业执照识别成功: {image_path}")
            return info

        except Exception as e:
            logger.error(f"营业执照识别失败: {image_path}, 错误: {e}")
            return {}

    def recognize_contract(self, image_path: str) -> Dict:
        """识别租赁合同等文档

        Args:
            image_path: 合同图片路径

        Returns:
            {
                "text": "完整文本",
                "parties": ["甲方", "乙方"],
                "dates": ["开始日期", "结束日期"],
                "amount": "金额（如有）"
            }
        """
        self._initialize()

        try:
            result = self.ocr.ocr(image_path, cls=True)
            parsed = self._parse_result(result)

            # 提取合同特有信息
            contract_info = self._parse_contract_info(parsed.get("text", ""))

            logger.info(f"合同识别成功: {image_path}")
            return contract_info

        except Exception as e:
            logger.error(f"合同识别失败: {image_path}, 错误: {e}")
            return {}

    def _preprocess_id_card(self, img):
        """身份证图片预处理

        Args:
            img: OpenCV图片对象

        Returns:
            处理后的图片
        """
        # 灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 去噪
        denoised = cv2.fastNlMeansDenoising(gray)

        # 二值化
        _, binary = cv2.threshold(
            denoised, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        return binary

    def _parse_result(self, result) -> Dict:
        """解析通用OCR结果

        Args:
            result: PaddleOCR原始结果

        Returns:
            解析后的字典
        """
        if not result or not result[0]:
            return {"text": "", "regions": []}

        regions = []
        full_text = []

        for line in result[0]:
            if not line:
                continue

            box = line[0]
            text_info = line[1]

            if text_info:
                text = text_info[0]
                confidence = text_info[1]

                regions.append({
                    "box": box,
                    "text": text,
                    "confidence": confidence
                })

                full_text.append(text)

        return {
            "text": "\n".join(full_text),
            "regions": regions
        }

    def _parse_id_card(self, result) -> Dict:
        """解析身份证识别结果

        Args:
            result: OCR原始结果

        Returns:
            身份证信息字典
        """
        info = {}

        if not result or not result[0]:
            return info

        for line in result[0]:
            if not line or not line[1]:
                continue

            text = line[1][0]

            # 姓名识别
            if "姓名" in text:
                name_match = re.search(r'姓名\s*(\S+)', text)
                if name_match:
                    info["name"] = name_match.group(1)

            # 身份证号识别
            id_match = re.search(r'(\d{17}[\dXx])', text)
            if id_match:
                info["id_card"] = id_match.group(1)
                # 推断性别
                info["gender"] = self._infer_gender(info["id_card"])

            # 民族识别
            if "民族" in text:
                nation_match = re.search(r'民族\s*(\S+)', text)
                if nation_match:
                    info["ethnicity"] = nation_match.group(1)

            # 地址识别
            if "住址" in text:
                address_match = re.search(r'住址\s*(.+)', text)
                if address_match:
                    info["address"] = address_match.group(1).strip()

        return info

    def _parse_business_license(self, result) -> Dict:
        """解析营业执照识别结果

        Args:
            result: OCR原始结果

        Returns:
            营业执照信息字典
        """
        info = {}
        text_lines = []

        # 收集所有文本
        if result and result[0]:
            for line in result[0]:
                if line and line[1]:
                    text_lines.append(line[1][0])

        full_text = "\n".join(text_lines)

        # 名称识别
        name_patterns = [
            r'名称\s*[:：]\s*(.+?)(?:\n|$)',
            r'经营者名称\s*[:：]\s*(.+?)(?:\n|$)',
            r'个体工商户名称\s*[:：]\s*(.+?)(?:\n|$)',
        ]
        for pattern in name_patterns:
            match = re.search(pattern, full_text)
            if match:
                info["company_name"] = match.group(1).strip()
                break

        # 统一社会信用代码
        credit_match = re.search(
            r'统一社会信用代码\s*[:：]\s*([A-Z0-9]{18})',
            full_text
        )
        if credit_match:
            info["credit_code"] = credit_match.group(1)

        # 法定代表人/经营者
        person_patterns = [
            r'法定代表人\s*[:：]\s*(\S+)',
            r'经营者\s*[:：]\s*(\S+)',
            r'经营者姓名\s*[:：]\s*(\S+)',
        ]
        for pattern in person_patterns:
            match = re.search(pattern, full_text)
            if match:
                info["legal_person"] = match.group(1).strip()
                break

        # 地址
        address_patterns = [
            r'经营场所\s*[:：]\s*(.+?)(?:\n|电话|$)',
            r'住所\s*[:：]\s*(.+?)(?:\n|电话|$)',
            r'地址\s*[:：]\s*(.+?)(?:\n|电话|$)',
        ]
        for pattern in address_patterns:
            match = re.search(pattern, full_text)
            if match:
                info["address"] = match.group(1).strip()
                break

        # 经营范围
        scope_match = re.search(
            r'经营范围\s*[:：]\s*(.+?)(?:\n|成立日期|$)',
            full_text,
            re.DOTALL
        )
        if scope_match:
            info["business_scope"] = scope_match.group(1).strip()

        return info

    def _parse_contract_info(self, text: str) -> Dict:
        """解析合同信息

        Args:
            text: OCR识别的完整文本

        Returns:
            合同信息字典
        """
        info = {"text": text}

        # 提取日期
        date_patterns = [
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{4})/(\d{1,2})/(\d{1,2})',
        ]

        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                date_str = f"{match[0]}-{match[1].zfill(2)}-{match[2].zfill(2)}"
                dates.append(date_str)

        if dates:
            info["dates"] = dates
            if len(dates) >= 2:
                info["lease_start"] = dates[0]
                info["lease_end"] = dates[1]

        # 提取甲方（出租方）
        landlord_patterns = [
            r'出租方\s*[:：]\s*([\u4e00-\u9fa5]{2,4})',
            r'甲方\s*[:：]\s*([\u4e00-\u9fa5]{2,4})',
            r'房主\s*[:：]\s*([\u4e00-\u9fa5]{2,4})',
        ]
        for pattern in landlord_patterns:
            match = re.search(pattern, text)
            if match:
                info["landlord"] = match.group(1).strip()
                break

        # 提取乙方（承租方）
        tenant_patterns = [
            r'承租方\s*[:：]\s*([\u4e00-\u9fa5]{2,4})',
            r'乙方\s*[:：]\s*([\u4e00-\u9fa5]{2,4})',
        ]
        for pattern in tenant_patterns:
            match = re.search(pattern, text)
            if match:
                info["tenant"] = match.group(1).strip()
                break

        # 提取金额
        amount_match = re.search(
            r'租金\s*[:：]?\s*(\d+(?:\.\d+)?)\s*元',
            text
        )
        if amount_match:
            info["rent_amount"] = amount_match.group(1)

        return info

    def _infer_gender(self, id_card: str) -> str:
        """从身份证号推断性别

        Args:
            id_card: 身份证号

        Returns:
            性别：男/女
        """
        if len(id_card) >= 17:
            gender_code = int(id_card[16])
            return '女' if gender_code % 2 == 0 else '男'
        return '未知'


# 便捷函数
def recognize_image(image_path: str, use_gpu: bool = False) -> Dict:
    """便捷函数：识别图片

    Args:
        image_path: 图片路径
        use_gpu: 是否使用GPU

    Returns:
        识别结果
    """
    engine = OCREngine(use_gpu=use_gpu)
    return engine.recognize_image(image_path)


def recognize_id_card(image_path: str, use_gpu: bool = False) -> Dict:
    """便捷函数：识别身份证

    Args:
        image_path: 身份证图片路径
        use_gpu: 是否使用GPU

    Returns:
        身份证信息
    """
    engine = OCREngine(use_gpu=use_gpu)
    return engine.recognize_id_card(image_path)
