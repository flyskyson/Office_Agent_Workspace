#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
名称工具 - 名称验证和生成

功能：
- 本地名称格式验证
- 智能名称生成
- 名称合规性检查
- 批量名称建议

作者: Claude Code
日期: 2026-01-15
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from loguru import logger


# ============ 数据类定义 ============

@dataclass
class NameSuggestion:
    """名称建议"""
    full_name: str                    # 完整名称
    district: str                     # 行政区划
    trade_name: str                   # 字号
    industry: str                     # 行业
    organization: str                 # 组织形式
    score: int = 0                   # 可用性评分 (0-100)
    reasons: List[str] = field(default_factory=list)  # 评分理由


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool                    # 是否有效
    format_correct: bool              # 格式是否正确
    warnings: List[str] = field(default_factory=list)  # 警告信息
    suggestions: List[str] = field(default_factory=list)  # 改进建议
    confidence: float = 0.0           # 可信度 (0-1)


# ============ 名称工具类 ============

class NameTools:
    """名称工具类"""

    # 广西行政区划
    DISTRICTS = {
        "南宁市": {
            "青秀区": "450103",
            "兴宁区": "450102",
            "江南区": "450105",
            "西乡塘区": "450107",
            "良庆区": "450108",
            "邕宁区": "450109",
            "武鸣区": "450110",
        },
        "柳州市": {
            "城中区": "450202",
            "鱼峰区": "450203",
            "柳南区": "450204",
            "柳北区": "450205",
            "柳江区": "450206",
        },
        "桂林市": {
            "秀峰区": "450302",
            "叠彩区": "450303",
            "象山区": "450304",
            "七星区": "450305",
        },
        "玉林市": {
            "玉州区": "450902",
            "福绵区": "450903",
            "兴业县": "450924",
            "容县": "450921",
            "陆川县": "450922",
            "博白县": "450923",
        }
    }

    # 常用行业
    INDUSTRIES = [
        "便利店", "超市", "餐饮", "服装店", "美容美发",
        "汽车维修", "五金店", "建材", "花店", "水果店",
        "早餐店", "奶茶店", "文具店", "药店", "理发店",
        "家政服务", "保洁服务", "搬家服务", "快递代理", "物流",
        "小吃店", "烧烤", "火锅", "米粉店", "面馆",
        "建材经营", "装饰材料", "门窗", "电器销售", "电子产品",
    ]

    # 组织形式
    ORGANIZATIONS = [
        "（个体工商户）",
        "（个体工商户）",
        "店", "馆", "社", "部", "中心"
    ]

    # 敏感词（不能在字号中使用）
    SENSITIVE_WORDS = [
        "中国", "国际", "全国", "国家", "中华",
        "中央", "政府",
        "集团", "公司", "企业", "股份", "有限",
        "银行", "证券", "保险"
    ]

    # 行政区划关键词（这些是合法的，不应被标记为敏感词）
    DISTRICT_KEYWORDS = ["省", "市", "区", "县", "镇", "乡", "街道"]

    # 名称格式正则
    NAME_PATTERN = r'^(.+?)(（个体工商户）)$'

    def __init__(self, config_path: Optional[str] = None):
        """初始化名称工具

        Args:
            config_path: 配置文件路径（可选）
        """
        self.local_db_path = Path("data/local_names.json")
        self.local_db = self._load_local_db()

        logger.info("名称工具初始化完成")

    def _load_local_db(self) -> Dict:
        """加载本地名称数据库"""
        if self.local_db_path.exists():
            try:
                with open(self.local_db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"加载本地名称数据库失败: {e}")

        # 返回默认结构
        return {
            "used_names": [],          # 已使用的名称
            "reserved_names": [],      # 预留名称
            "blacklist": [],           # 黑名单
            "statistics": {
                "total_checked": 0,
                "total_generated": 0
            }
        }

    def _save_local_db(self):
        """保存本地名称数据库"""
        try:
            self.local_db_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.local_db_path, 'w', encoding='utf-8') as f:
                json.dump(self.local_db, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存本地名称数据库失败: {e}")

    def validate_name(self, business_name: str) -> ValidationResult:
        """验证名称格式和合规性

        Args:
            business_name: 个体工商户名称

        Returns:
            验证结果
        """
        result = ValidationResult(
            is_valid=True,
            format_correct=False,
            confidence=0.0
        )

        # 1. 格式检查
        match = re.match(self.NAME_PATTERN, business_name)
        if not match:
            result.format_correct = False
            result.warnings.append("名称格式不符合规范")
            result.suggestions.append("名称格式应为：行政区划 + 字号 + 行业 + （个体工商户）")
            result.is_valid = False
            return result

        result.format_correct = True

        # 解析名称
        prefix = match.group(1)  # 行政区划 + 字号 + 行业
        organization = match.group(2)  # 组织形式

        # 2. 长度检查
        if len(business_name) < 10:
            result.warnings.append("名称过短（建议10-50字符）")
            result.confidence -= 0.2
        elif len(business_name) > 50:
            result.warnings.append("名称过长（建议10-50字符）")
            result.confidence -= 0.2

        # 3. 敏感词检查（只检查字号部分，不包括行政区划和行业）
        # 尝试提取字号：去掉已知的行政区划和行业词汇
        trade_name_candidate = prefix
        for district in self.DISTRICT_KEYWORDS:
            if district in prefix:
                parts = prefix.split(district, 1)
                if len(parts) > 1:
                    trade_name_candidate = parts[1]
                break

        # 检查字号中是否包含敏感词
        for word in self.SENSITIVE_WORDS:
            if word in trade_name_candidate:
                result.warnings.append(f"字号包含敏感词: {word}")
                result.is_valid = False
                result.confidence -= 0.5

        # 4. 本地查重
        if business_name in self.local_db.get("used_names", []):
            result.warnings.append("本地数据库中已存在此名称")
            result.is_valid = False
            result.confidence -= 0.8

        if business_name in self.local_db.get("blacklist", []):
            result.warnings.append("名称在黑名单中")
            result.is_valid = False
            result.confidence = 0.0

        # 5. 检查组织形式
        if organization not in self.ORGANIZATIONS:
            result.warnings.append(f"组织形式不规范: {organization}")
            result.suggestions.append("建议使用：（个体工商户）")
            result.confidence -= 0.1

        # 计算最终可信度
        if result.is_valid and result.format_correct:
            base_confidence = 0.8
            result.confidence = max(0.0, min(1.0, base_confidence + result.confidence))

        # 更新统计
        self.local_db["statistics"]["total_checked"] += 1
        self._save_local_db()

        return result

    def generate_names(
        self,
        operator_name: str,
        industry: str,
        district: str = "玉林市兴业县",
        count: int = 10
    ) -> List[NameSuggestion]:
        """生成名称建议

        Args:
            operator_name: 经营者姓名
            industry: 行业类型
            district: 行政区划
            count: 生成数量

        Returns:
            名称建议列表
        """
        suggestions = []

        # 尝试不同的字号组合
        trade_names = []

        # 1. 使用经营者姓名
        trade_names.append(operator_name)

        # 2. 姓名谐音/变体
        if len(operator_name) >= 2:
            trade_names.append(operator_name[:2] + "氏")
            trade_names.append(operator_name[-2:] + "记")

        # 3. 常用字号
        common_prefixes = ["鑫", "瑞", "祥", "顺", "通", "达", "美", "佳", "优", "新"]
        for prefix in common_prefixes[:5]:
            trade_names.append(prefix + operator_name[-1:])
            trade_names.append(prefix + industry.replace("店", "").replace("经营", ""))

        # 4. 组合生成
        for i, trade_name in enumerate(trade_names):
            if i >= count:
                break

            full_name = f"{district}{trade_name}{industry}（个体工商户）"

            # 验证名称
            validation = self.validate_name(full_name)

            suggestion = NameSuggestion(
                full_name=full_name,
                district=district,
                trade_name=trade_name,
                industry=industry,
                organization="（个体工商户）",
                score=int(validation.confidence * 100),
                reasons=[f"可信度: {validation.confidence:.2f}"] + validation.warnings
            )

            suggestions.append(suggestion)

        # 按评分排序
        suggestions.sort(key=lambda x: x.score, reverse=True)

        # 更新统计
        self.local_db["statistics"]["total_generated"] += len(suggestions)
        self._save_local_db()

        logger.info(f"生成 {len(suggestions)} 个名称建议")
        return suggestions

    def reserve_name(self, business_name: str) -> bool:
        """预留名称

        Args:
            business_name: 个体工商户名称

        Returns:
            是否成功
        """
        if business_name not in self.local_db.get("reserved_names", []):
            self.local_db.setdefault("reserved_names", []).append(business_name)
            self._save_local_db()
            logger.info(f"预留名称: {business_name}")
            return True
        return False

    def mark_name_used(self, business_name: str) -> bool:
        """标记名称为已使用

        Args:
            business_name: 个体工商户名称

        Returns:
            是否成功
        """
        if business_name not in self.local_db.get("used_names", []):
            self.local_db.setdefault("used_names", []).append(business_name)

            # 从预留列表中移除
            if business_name in self.local_db.get("reserved_names", []):
                self.local_db["reserved_names"].remove(business_name)

            self._save_local_db()
            logger.info(f"标记名称已使用: {business_name}")
            return True
        return False

    def get_industry_list(self) -> List[str]:
        """获取行业列表"""
        return self.INDUSTRIES.copy()

    def get_district_list(self) -> Dict[str, Dict[str, str]]:
        """获取行政区划列表"""
        return self.DISTRICTS.copy()

    def batch_validate(self, names: List[str]) -> List[ValidationResult]:
        """批量验证名称

        Args:
            names: 名称列表

        Returns:
            验证结果列表
        """
        results = []
        for name in names:
            result = self.validate_name(name)
            results.append(result)
        return results

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return self.local_db.get("statistics", {})

    def parse_name(self, business_name: str) -> Optional[Dict[str, str]]:
        """解析名称结构

        Args:
            business_name: 个体工商户名称

        Returns:
            解析结果字典，失败返回None
        """
        match = re.match(self.NAME_PATTERN, business_name)
        if not match:
            return None

        prefix = match.group(1)
        organization = match.group(2)

        # 尝试解析行政区划、字号、行业
        # 这是一个简化版本，实际可能需要更复杂的逻辑

        return {
            "full_name": business_name,
            "prefix": prefix,
            "organization": organization,
            "parsed": True
        }


# ============ 便捷函数 ============

def create_name_tools(config_path: Optional[str] = None) -> NameTools:
    """创建名称工具实例

    Args:
        config_path: 配置文件路径

    Returns:
        NameTools实例
    """
    return NameTools(config_path)


def quick_validate(business_name: str) -> ValidationResult:
    """快速验证名称

    Args:
        business_name: 个体工商户名称

    Returns:
        验证结果
    """
    tools = NameTools()
    return tools.validate_name(business_name)


def quick_generate(
    operator_name: str,
    industry: str,
    district: str = "玉林市兴业县",
    count: int = 10
) -> List[str]:
    """快速生成名称

    Args:
        operator_name: 经营者姓名
        industry: 行业类型
        district: 行政区划
        count: 生成数量

    Returns:
        名称列表
    """
    tools = NameTools()
    suggestions = tools.generate_names(operator_name, industry, district, count)
    return [s.full_name for s in suggestions]


# ============ 测试代码 ============

if __name__ == "__main__":
    # 测试
    tools = NameTools()

    # 验证测试
    test_names = [
        "玉林市兴业县张三便利店（个体工商户）",
        "南宁市青秀区李四餐饮店（个体工商户）",
        "中国贸易公司（个体工商户）",
    ]

    print("=" * 60)
    print("名称验证测试")
    print("=" * 60)

    for name in test_names:
        result = tools.validate_name(name)
        print(f"\n名称: {name}")
        print(f"  有效: {result.is_valid}")
        print(f"  格式正确: {result.format_correct}")
        print(f"  可信度: {result.confidence:.2f}")
        if result.warnings:
            print(f"  警告: {', '.join(result.warnings)}")
        if result.suggestions:
            print(f"  建议: {', '.join(result.suggestions)}")

    # 生成测试
    print("\n" + "=" * 60)
    print("名称生成测试")
    print("=" * 60)

    suggestions = tools.generate_names("张三", "便利店", "玉林市兴业县", 5)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n建议 {i}:")
        print(f"  名称: {suggestion.full_name}")
        print(f"  评分: {suggestion.score}")
        print(f"  理由: {', '.join(suggestion.reasons)}")
