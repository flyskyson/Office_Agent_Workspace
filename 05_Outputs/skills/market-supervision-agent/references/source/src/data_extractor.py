"""
数据提取器 - 从OCR结果中提取结构化数据

功能：
- 提取身份证信息
- 提取营业执照信息
- 提取合同信息
- 数据验证
- 数据合并
"""

import re
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, validator, Field
from loguru import logger


class OperatorData(BaseModel):
    """经营户数据模型 - 使用Pydantic进行数据验证"""

    # 基本信息
    operator_name: str = Field(..., description="经营者姓名")
    id_card: str = Field(..., description="身份证号")

    # 联系信息
    phone: Optional[str] = Field(None, description="联系电话")
    email: Optional[str] = Field(None, description="电子邮箱")

    # 个人信息
    gender: Optional[str] = Field(None, description="性别")
    nation: Optional[str] = Field(None, description="民族")
    ethnicity: Optional[str] = Field(None, description="民族（别称）")
    address: Optional[str] = Field(None, description="地址")

    # 经营信息
    business_name: Optional[str] = Field(None, description="个体工商户名称")
    business_address: Optional[str] = Field(None, description="经营场所")
    business_scope: Optional[str] = Field(None, description="经营范围")
    credit_code: Optional[str] = Field(None, description="统一社会信用代码")

    # 场所信息
    property_owner: Optional[str] = Field(None, description="房产所有人/房东")
    landlord: Optional[str] = Field(None, description="房东（别称）")
    lease_start: Optional[str] = Field(None, description="租赁开始日期")
    lease_end: Optional[str] = Field(None, description="租赁结束日期")
    rent_amount: Optional[str] = Field(None, description="租金金额")

    # 文件路径
    id_card_front_path: Optional[str] = Field(None, description="身份证正面路径")
    id_card_back_path: Optional[str] = Field(None, description="身份证反面路径")
    business_license_path: Optional[str] = Field(None, description="营业执照路径")
    lease_contract_path: Optional[str] = Field(None, description="租赁合同路径")
    property_cert_path: Optional[str] = Field(None, description="产权证明路径")

    # 元数据
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="额外元数据")

    @validator('id_card')
    def validate_id_card(cls, v):
        """验证身份证号格式"""
        if not v:
            return v

        # 18位身份证号正则
        pattern = r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$'

        if not re.match(pattern, v):
            logger.warning(f'身份证号格式可能不正确: {v}')
            # 不抛出异常，允许OCR识别不完整的情况

        return v

    @validator('phone')
    def validate_phone(cls, v):
        """验证手机号格式"""
        if v and not re.match(r'^1[3-9]\d{9}$', v):
            logger.warning(f'手机号格式可能不正确: {v}')
        return v

    @validator('credit_code')
    def validate_credit_code(cls, v):
        """验证统一社会信用代码格式"""
        if v:
            # 18位统一社会信用代码
            if not re.match(r'^[A-Z0-9]{18}$', v):
                logger.warning(f'统一社会信用代码格式可能不正确: {v}')
        return v

    @validator('gender')
    def normalize_gender(cls, v):
        """标准化性别值"""
        if not v:
            return v

        v = v.strip()
        if v in ['男', 'M', 'Male', '男性']:
            return '男'
        elif v in ['女', 'F', 'Female', '女性']:
            return '女'
        return v

    @validator('nation', 'ethnicity', pre=True)
    def normalize_nation(cls, v):
        """统一民族字段"""
        # ethnicity 和 nation 都映射到 nation
        return v

    def to_dict(self) -> Dict:
        """转换为普通字典"""
        return self.dict(exclude_none=True)

    def get_missing_fields(self) -> List[str]:
        """获取缺失的必填字段"""
        missing = []
        if not self.operator_name:
            missing.append('operator_name')
        if not self.id_card:
            missing.append('id_card')
        return missing


class DataExtractor:
    """数据提取器 - 从OCR结果中提取结构化数据"""

    def __init__(self):
        """初始化提取器"""
        # 正则表达式模式
        self.patterns = {
            'phone': r'1[3-9]\d{9}',
            'id_card': r'[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]',
            'credit_code': r'[A-Z0-9]{18}',
            'date': r'\d{4}[-年]\d{1,2}[-月]\d{1,2}',
            'amount': r'\d+(?:\.\d+)?',
        }

    def extract_from_id_card(
        self,
        ocr_result: Dict,
        file_path: Optional[str] = None
    ) -> Dict:
        """从身份证OCR结果提取数据

        Args:
            ocr_result: OCR识别结果
            file_path: 文件路径（用于记录）

        Returns:
            提取的数据字典
        """
        data = {}

        # 提取姓名
        if 'name' in ocr_result:
            data['operator_name'] = ocr_result['name']

        # 提取身份证号
        if 'id_card' in ocr_result:
            data['id_card'] = ocr_result['id_card']

        # 提取性别
        if 'gender' in ocr_result:
            data['gender'] = ocr_result['gender']

        # 提取民族
        if 'ethnicity' in ocr_result:
            data['nation'] = ocr_result['ethnicity']

        # 提取地址（可作为经营场所候选）
        if 'address' in ocr_result:
            data['address'] = ocr_result['address']

        # 记录文件路径
        if file_path:
            # 根据文件名判断是正面还是反面
            if 'front' in file_path.lower() or '正面' in file_path:
                data['id_card_front_path'] = file_path
            elif 'back' in file_path.lower() or '反面' in file_path:
                data['id_card_back_path'] = file_path
            else:
                # 无法区分，默认当作正面
                if not data.get('id_card_front_path'):
                    data['id_card_front_path'] = file_path
                else:
                    data['id_card_back_path'] = file_path

        logger.debug(f"从身份证提取数据: {data}")
        return data

    def extract_from_business_license(
        self,
        ocr_result: Dict,
        file_path: Optional[str] = None
    ) -> Dict:
        """从营业执照OCR结果提取数据

        Args:
            ocr_result: OCR识别结果
            file_path: 文件路径

        Returns:
            提取的数据字典
        """
        data = {}

        # 提取公司/店名
        if 'company_name' in ocr_result:
            data['business_name'] = ocr_result['company_name']
            # 如果没有经营者姓名，可以用法人/经营者姓名
            if 'legal_person' in ocr_result:
                # 优先级：legal_person > operator_name
                if not data.get('operator_name'):
                    data['operator_name'] = ocr_result['legal_person']

        # 提取统一社会信用代码
        if 'credit_code' in ocr_result:
            data['credit_code'] = ocr_result['credit_code']

        # 提取地址（作为经营场所）
        if 'address' in ocr_result:
            data['business_address'] = ocr_result['address']

        # 提取经营范围
        if 'business_scope' in ocr_result:
            data['business_scope'] = ocr_result['business_scope']

        # 记录文件路径
        if file_path:
            data['business_license_path'] = file_path

        logger.debug(f"从营业执照提取数据: {data}")
        return data

    def extract_from_lease_contract(
        self,
        ocr_result: Dict,
        file_path: Optional[str] = None
    ) -> Dict:
        """从租赁合同OCR结果提取数据

        Args:
            ocr_result: OCR识别结果
            file_path: 文件路径

        Returns:
            提取的数据字典
        """
        data = {}

        # 提取房东/出租方
        if 'landlord' in ocr_result:
            data['property_owner'] = ocr_result['landlord']
        elif 'parties' in ocr_result and len(ocr_result['parties']) >= 1:
            # 使用第一个作为出租方
            data['property_owner'] = ocr_result['parties'][0]

        # 提取租赁期限
        if 'lease_start' in ocr_result:
            data['lease_start'] = ocr_result['lease_start']
        if 'lease_end' in ocr_result:
            data['lease_end'] = ocr_result['lease_end']

        # 提取租金
        if 'rent_amount' in ocr_result:
            data['rent_amount'] = ocr_result['rent_amount']

        # 记录文件路径
        if file_path:
            data['lease_contract_path'] = file_path

        logger.debug(f"从租赁合同提取数据: {data}")
        return data

    def extract_from_property_cert(
        self,
        ocr_result: Dict,
        file_path: Optional[str] = None
    ) -> Dict:
        """从产权证明OCR结果提取数据

        Args:
            ocr_result: OCR识别结果
            file_path: 文件路径

        Returns:
            提取的数据字典
        """
        data = {}

        # 从文本中提取房产所有人
        text = ocr_result.get('text', '')

        # 常见产权证明关键词
        owner_patterns = [
            r'房屋所有权人\s*[:：]\s*([\u4e00-\u9fa5]{2,4})',
            r'权利人\s*[:：]\s*([\u4e00-\u9fa5]{2,4})',
            r'所有人\s*[:：]\s*([\u4e00-\u9fa5]{2,4})',
        ]

        for pattern in owner_patterns:
            match = re.search(pattern, text)
            if match:
                data['property_owner'] = match.group(1).strip()
                break

        # 记录文件路径
        if file_path:
            data['property_cert_path'] = file_path

        logger.debug(f"从产权证明提取数据: {data}")
        return data

    def extract_from_general_document(
        self,
        ocr_result: Dict,
        file_path: Optional[str] = None
    ) -> Dict:
        """从通用文档中提取信息

        Args:
            ocr_result: OCR识别结果
            file_path: 文件路径

        Returns:
            提取的数据字典
        """
        data = {}
        text = ocr_result.get('text', '')

        # 提取手机号
        phone_match = re.search(self.patterns['phone'], text)
        if phone_match:
            data['phone'] = phone_match.group(0)

        # 提取身份证号
        id_match = re.search(self.patterns['id_card'], text)
        if id_match:
            data['id_card'] = id_match.group(0)

        # 提取日期
        dates = re.findall(self.patterns['date'], text)
        if dates and len(dates) >= 2:
            # 假设第一个是开始日期，第二个是结束日期
            data['lease_start'] = dates[0].replace('年', '-').replace('月', '-').replace('日', '')
            data['lease_end'] = dates[1].replace('年', '-').replace('月', '-').replace('日', '')

        return data

    def merge_data(
        self,
        *data_sources: Dict,
        validate: bool = True
    ) -> OperatorData:
        """合并多个数据源

        Args:
            *data_sources: 多个数据字典
            validate: 是否进行数据验证

        Returns:
            OperatorData对象

        Raises:
            ValidationError: 数据验证失败
        """
        # 定义字段优先级（值越大优先级越高）
        # 身份证字段优先级高，经营信息字段优先级高
        field_priority = {
            # 基本信息（来自身份证）
            'operator_name': 10,
            'id_card': 10,
            'gender': 10,
            'nation': 10,
            'ethnicity': 10,
            'address': 10,
            'birth_date': 10,

            # 经营信息（来自营业执照，优先级更高）
            'business_name': 20,
            'business_address': 20,
            'business_scope': 20,
            'credit_code': 20,
            'register_date': 20,
            'registered_capital': 20,
            'legal_person': 20,

            # 联系方式（中等优先级）
            'phone': 15,
            'email': 15,

            # 场所信息（来自合同等）
            'property_owner': 15,
            'landlord': 15,
            'lease_start': 15,
            'lease_end': 15,
            'rent_amount': 15,
        }

        # 合并所有数据源
        merged = {}
        source_priority = {}  # 记录每个字段当前值的来源优先级

        for source in data_sources:
            for key, value in source.items():
                if value:  # 只合并非空值
                    priority = field_priority.get(key, 5)  # 默认优先级
                    # 如果新数据优先级更高，或者字段为空，则更新
                    if key not in merged or source_priority.get(key, 0) < priority:
                        merged[key] = value
                        source_priority[key] = priority

        logger.info(f"合并后的数据: {merged}")

        # 创建数据对象
        if validate:
            try:
                return OperatorData(**merged)
            except Exception as e:
                logger.error(f"数据验证失败: {e}")
                # 尝试创建允许部分字段缺失的对象
                # 提取有效字段
                valid_data = {}
                for key, value in merged.items():
                    try:
                        # 逐个字段验证
                        temp = {key: value}
                        OperatorData(**valid_data, **temp)
                        valid_data[key] = value
                    except:
                        logger.warning(f"字段 {key} 验证失败，跳过")

                return OperatorData(**valid_data)
        else:
            return OperatorData(**merged)

    def extract_phone(self, text: str) -> Optional[str]:
        """从文本中提取手机号

        Args:
            text: 文本内容

        Returns:
            手机号或None
        """
        match = re.search(self.patterns['phone'], text)
        return match.group(0) if match else None

    def extract_id_card(self, text: str) -> Optional[str]:
        """从文本中提取身份证号

        Args:
            text: 文本内容

        Returns:
            身份证号或None
        """
        match = re.search(self.patterns['id_card'], text)
        return match.group(0) if match else None

    def infer_gender_from_id(self, id_card: str) -> str:
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
def extract_and_merge(
    ocr_results: Dict[str, Dict],
    file_categories: Dict[str, str]
) -> OperatorData:
    """便捷函数：从多个OCR结果中提取并合并数据

    Args:
        ocr_results: {文件路径: OCR结果}
        file_categories: {文件路径: 文件类别}

    Returns:
        合并后的OperatorData对象
    """
    extractor = DataExtractor()
    all_data = []

    for file_path, ocr_result in ocr_results.items():
        category = file_categories.get(file_path, 'unknown')

        if category == 'id_card':
            data = extractor.extract_from_id_card(ocr_result, file_path)
        elif category == 'business_license':
            data = extractor.extract_from_business_license(ocr_result, file_path)
        elif category == 'lease_contract':
            data = extractor.extract_from_lease_contract(ocr_result, file_path)
        elif category == 'property_cert':
            data = extractor.extract_from_property_cert(ocr_result, file_path)
        else:
            data = extractor.extract_from_general_document(ocr_result, file_path)

        all_data.append(data)

    return extractor.merge_data(*all_data)
