"""
百度 OCR API 引擎 - 基于百度智能云 OCR 服务

支持的文档类型：
- 身份证识别
- 通用文字识别
- 营业执照识别（通用）

配置：
1. 注册百度智能云账号：https://cloud.baidu.com/
2. 创建 OCR 应用，获取 API Key 和 Secret Key
3. 安装依赖：pip install baidu-aip

免费额度：
- 通用文字识别：500次/天
- 身份证识别：500次/天
- 营业执照：500次/天
"""

import base64
from pathlib import Path
from typing import Dict, Optional
from loguru import logger

try:
    from aip import AipOcr
    HAS_BAIDU_OCR = True
except (ImportError, SyntaxError):
    HAS_BAIDU_OCR = False
    AipOcr = None
    logger.warning("百度 OCR SDK 未安装，请运行: pip install baidu-aip")


class BaiduOCREngine:
    """百度 OCR API 引擎"""

    def __init__(
        self,
        app_id: str = "",
        api_key: str = "",
        secret_key: str = "",
        config_file: str = "config/baidu_ocr.yaml"
    ):
        """初始化百度 OCR 引擎

        Args:
            app_id: 百度 OCR AppID
            api_key: 百度 OCR API Key
            secret_key: 百度 OCR Secret Key
            config_file: 配置文件路径（YAML格式）
        """
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.config_file = config_file

        # 尝试从配置文件加载
        if not all([app_id, api_key, secret_key]) and Path(config_file).exists():
            self._load_config()

        self.client = None
        self._initialized = False

    def _load_config(self):
        """从 YAML 配置文件加载"""
        try:
            import yaml
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.app_id = config.get('app_id', '')
                self.api_key = config.get('api_key', '')
                self.secret_key = config.get('secret_key', '')
                logger.info(f"从配置文件加载: {self.config_file}")
        except Exception as e:
            logger.warning(f"加载配置文件失败: {e}")

    def _initialize(self):
        """延迟初始化百度 OCR 客户端"""
        if self._initialized:
            return

        if not HAS_BAIDU_OCR:
            raise RuntimeError("百度 OCR SDK 未安装，请运行: pip install baidu-aip")

        if not all([self.app_id, self.api_key, self.secret_key]):
            raise ValueError(
                "百度 OCR 凭证缺失！请配置 app_id、api_key 和 secret_key\n"
                "1. 访问 https://cloud.baidu.com/ 注册账号\n"
                "2. 创建 OCR 应用获取凭证\n"
                "3. 在 config/baidu_ocr.yaml 中配置凭证"
            )

        self.client = AipOcr(self.app_id, self.api_key, self.secret_key)
        self._initialized = True
        logger.info("百度 OCR 客户端初始化成功")

    def recognize_image(self, image_path: str) -> Dict:
        """通用文字识别

        Args:
            image_path: 图片路径

        Returns:
            识别结果字典
        """
        self._initialize()

        if not Path(image_path).exists():
            raise FileNotFoundError(f"文件不存在: {image_path}")

        try:
            # 读取图片并转换为 base64
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # 调用百度 OCR API
            result = self.client.basicGeneral(image_data)

            # 解析结果
            return self._parse_general_result(result)

        except Exception as e:
            logger.error(f"OCR识别失败: {image_path}, 错误: {e}")
            return {"text": "", "words_result": [], "error": str(e)}

    def recognize_id_card(self, image_path: str) -> Dict:
        """身份证识别

        Args:
            image_path: 身份证图片路径

        Returns:
            {
                "name": "张三",
                "id_card": "110101199001011234",
                "gender": "男",
                "nation": "汉",
                "address": "..."
            }
        """
        self._initialize()

        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # 调用身份证识别 API
            # 百度 API 参数: idCardSide (front=正面, back=背面)
            result = self.client.idcard(image_data, "front")

            # 解析结果
            return self._parse_id_card_result(result)

        except Exception as e:
            logger.error(f"身份证识别失败: {image_path}, 错误: {e}")
            return {}

    def recognize_business_license(self, image_path: str) -> Dict:
        """营业执照识别

        Args:
            image_path: 营业执照图片路径

        Returns:
            {
                "company_name": "XX公司",
                "credit_code": "91110000XXXXXXXXXX",
                "legal_person": "...",
                "address": "...",
                "business_scope": "..."
            }
        """
        self._initialize()

        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # 优先使用专门的营业执照识别 API
            try:
                result = self.client.businessLicense(image_data)
                return self._parse_business_license_result(result)
            except Exception as e:
                logger.warning(f"营业执照专用 API 调用失败，尝试通用识别: {e}")

                # 降级到通用文字识别（高精度版）
                result = self.client.basicAccurate(image_data)
                parsed = self._parse_general_result(result)
                return self._extract_business_info(parsed.get("text", ""))

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
                "landlord": "房东姓名",
                "lease_start": "开始日期",
                "lease_end": "结束日期"
            }
        """
        self._initialize()

        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # 使用通用文字识别
            result = self.client.general(image_data)

            parsed = self._parse_general_result(result)
            contract_info = self._extract_contract_info(parsed.get("text", ""))

            return contract_info

        except Exception as e:
            logger.error(f"合同识别失败: {image_path}, 错误: {e}")
            return {}

    def _parse_general_result(self, result: Dict) -> Dict:
        """解析通用文字识别结果

        Args:
            result: 百度 OCR API 返回结果

        Returns:
            解析后的字典
        """
        # 检查错误
        if 'error_code' in result:
            error_msg = result.get('error_msg', '未知错误')
            logger.error(f"百度 OCR API 错误: {result['error_code']} - {error_msg}")
            return {"text": "", "words_result": [], "error": error_msg}

        # 提取文字
        words_result = result.get('words_result', [])
        text_lines = [item.get('words', '') for item in words_result]
        full_text = '\n'.join(text_lines)

        return {
            "text": full_text,
            "words_result": words_result,
            "log_id": result.get('log_id', ''),
        }

    def _parse_id_card_result(self, result: Dict) -> Dict:
        """解析身份证识别结果

        Args:
            result: 百度身份证识别 API 返回结果

        Returns:
            身份证信息字典
        """
        # 百度身份证识别返回结构：
        # {
        #   "words_result": {
        #     "姓名": {"words": "张三"},
        #     "民族": {"words": "汉"},
        #     "住址": {"words": "..."},
        #     "公民身份号码": {"words": "..."},
        #     "性别": {"words": "男"}
        #   }
        # }

        # 检查错误
        if isinstance(result, dict) and 'error_code' in result:
            logger.error(f"百度身份证识别 API 错误: {result.get('error_msg', result['error_code'])}")
            return {}

        # 确保 result 是字典类型
        if not isinstance(result, dict):
            logger.error(f"返回结果类型错误: {type(result)}")
            return {}

        info = {}

        # 获取 words_result
        words_result = result.get('words_result', {})
        if not words_result:
            logger.warning("身份证识别结果为空")
            return {}

        # 百度身份证识别返回的结构化字段
        field_mapping = {
            '姓名': 'name',
            '公民身份号码': 'id_card',
            '性别': 'gender',
            '民族': 'nation',
            '住址': 'address',
            '出生': 'birth_date'
        }

        for cn_field, en_field in field_mapping.items():
            if cn_field in words_result:
                field_data = words_result[cn_field]
                if isinstance(field_data, dict):
                    info[en_field] = field_data.get('words', '').strip()
                elif isinstance(field_data, str):
                    info[en_field] = field_data.strip()

        # 添加 ethnicity 别名
        if 'nation' in info:
            info['ethnicity'] = info['nation']

        # 从身份证号推断性别（如果没有）
        if 'id_card' in info and 'gender' not in info:
            info['gender'] = self._infer_gender(info['id_card'])

        return info

    def _extract_business_info(self, text: str) -> Dict:
        """从文本中提取营业执照信息

        Args:
            text: OCR 识别的文本

        Returns:
            营业执照信息字典
        """
        import re

        info = {}

        # 名称识别
        patterns = [
            r'名称[：:]\s*([^\n]+)',
            r'经营者名称[：:]\s*([^\n]+)',
            r'个体工商户名称[：:]\s*([^\n]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                info['company_name'] = match.group(1).strip()
                break

        # 统一社会信用代码
        credit_match = re.search(r'统一社会信用代码[：:]\s*([A-Z0-9]{18})', text)
        if credit_match:
            info['credit_code'] = credit_match.group(1)

        # 法定代表人/经营者
        patterns = [
            r'法定代表人[：:]\s*([\u4e00-\u9fa5]{2,4})',
            r'经营者[：:]\s*([\u4e00-\u9fa5]{2,4})',
            r'经营者姓名[：:]\s*([\u4e00-\u9fa5]{2,4})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                info['legal_person'] = match.group(1).strip()
                break

        # 地址
        patterns = [
            r'经营场所[：:]\s*([^\n]+?)(?:\n|电话|经营范围)',
            r'住所[：:]\s*([^\n]+?)(?:\n|电话|经营范围)',
            r'地址[：:]\s*([^\n]+?)(?:\n|电话|经营范围)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                info['address'] = match.group(1).strip()
                break

        # 经营范围
        scope_match = re.search(
            r'经营范围[：:]\s*([^\n]+?)(?:\n|成立日期|经营期限)',
            text,
            re.DOTALL
        )
        if scope_match:
            info['business_scope'] = scope_match.group(1).strip()

        return info

    def _parse_business_license_result(self, result: Dict) -> Dict:
        """解析百度营业执照识别 API 返回结果

        Args:
            result: 百度营业执照识别 API 返回结果

        Returns:
            营业执照信息字典
        """
        # 检查错误
        if isinstance(result, dict) and 'error_code' in result:
            logger.error(f"百度营业执照识别 API 错误: {result.get('error_msg', result['error_code'])}")
            raise Exception(f"API Error: {result.get('error_msg')}")

        # 确保结果是字典类型
        if not isinstance(result, dict):
            logger.error(f"返回结果类型错误: {type(result)}")
            return {}

        info = {}

        # 获取 words_result
        words_result = result.get('words_result', {})
        if not words_result:
            logger.warning("营业执照识别结果为空")
            return {}

        # 百度营业执照识别返回的结构化字段
        # 单位名称
        if '单位名称' in words_result:
            info['company_name'] = words_result['单位名称'].get('words', '').strip()

        # 法定代表人
        if '法定代表人' in words_result:
            info['legal_person'] = words_result['法定代表人'].get('words', '').strip()

        # 统一社会信用代码
        if '统一社会信用代码' in words_result:
            info['credit_code'] = words_result['统一社会信用代码'].get('words', '').strip()

        # 地址
        if '地址' in words_result:
            info['address'] = words_result['地址'].get('words', '').strip()

        # 经营范围
        if '经营范围' in words_result:
            info['business_scope'] = words_result['经营范围'].get('words', '').strip()

        # 成立日期
        if '成立日期' in words_result:
            info['register_date'] = words_result['成立日期'].get('words', '').strip()

        # 注册资本
        if '注册资本' in words_result:
            info['registered_capital'] = words_result['注册资本'].get('words', '').strip()

        return info

    def _extract_contract_info(self, text: str) -> Dict:
        """从文本中提取合同信息

        Args:
            text: OCR 识别的文本

        Returns:
            合同信息字典
        """
        import re

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
            r'出租方[：:]\s*([\u4e00-\u9fa5]{2,4})',
            r'甲方[：:]\s*([\u4e00-\u9fa5]{2,4})',
            r'房主[：:]\s*([\u4e00-\u9fa5]{2,4})',
        ]
        for pattern in landlord_patterns:
            match = re.search(pattern, text)
            if match:
                info["landlord"] = match.group(1).strip()
                break

        # 提取乙方（承租方）
        tenant_patterns = [
            r'承租方[：:]\s*([\u4e00-\u9fa5]{2,4})',
            r'乙方[：:]\s*([\u4e00-\u9fa5]{2,4})',
        ]
        for pattern in tenant_patterns:
            match = re.search(pattern, text)
            if match:
                info["tenant"] = match.group(1).strip()
                break

        # 提取金额
        amount_match = re.search(
            r'租金[：:]?\s*(\d+(?:\.\d+)?)\s*元',
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
def recognize_image(image_path: str, app_id: str, api_key: str, secret_key: str) -> Dict:
    """便捷函数：通用文字识别

    Args:
        image_path: 图片路径
        app_id: 百度 OCR AppID
        api_key: 百度 OCR API Key
        secret_key: 百度 OCR Secret Key

    Returns:
        识别结果
    """
    engine = BaiduOCREngine(app_id, api_key, secret_key)
    return engine.recognize_image(image_path)


def recognize_id_card(image_path: str, app_id: str, api_key: str, secret_key: str) -> Dict:
    """便捷函数：身份证识别

    Args:
        image_path: 身份证图片路径
        app_id: 百度 OCR AppID
        api_key: 百度 OCR API Key
        secret_key: 百度 OCR Secret Key

    Returns:
        身份证信息
    """
    engine = BaiduOCREngine(app_id, api_key, secret_key)
    return engine.recognize_id_card(image_path)
