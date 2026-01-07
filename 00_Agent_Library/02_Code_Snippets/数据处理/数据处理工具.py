"""
常用数据处理工具
"""

import re
from datetime import datetime
from typing import List, Dict, Any
import hashlib


def clean_text(text: str) -> str:
    """清理文本（去除多余空格、换行等）"""
    return ' '.join(text.split())


def extract_emails(text: str) -> List[str]:
    """提取文本中的所有邮箱地址"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text, re.IGNORECASE)


def extract_urls(text: str) -> List[str]:
    """提取文本中的所有 URL"""
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(pattern, text)


def remove_special_chars(text: str, keep_chars: str = " .,!?,;:") -> str:
    """移除特殊字符"""
    return ''.join(c for c in text if c.isalnum() or c in keep_chars or c.isspace())


def chunk_list(items: List, chunk_size: int) -> List[List]:
    """将列表分块"""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """展平嵌套列表"""
    return [item for sublist in nested_list for item in sublist]


def unique_list(items: List[Any]) -> List[Any]:
    """去重并保持顺序"""
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]


def sort_dict_by_value(d: Dict, reverse: bool = False) -> Dict:
    """按值排序字典"""
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=reverse))


def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期"""
    return date.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """解析日期字符串"""
    return datetime.strptime(date_str, format_str)


def calculate_hash(text: str, algorithm: str = "md5") -> str:
    """计算文本哈希值"""
    hash_func = hashlib.new(algorithm)
    hash_func.update(text.encode('utf-8'))
    return hash_func.hexdigest()


def merge_dicts(*dicts: Dict) -> Dict:
    """合并多个字典"""
    result = {}
    for d in dicts:
        result.update(d)
    return result


def filter_dict(d: Dict, keys: List[str]) -> Dict:
    """过滤字典，只保留指定的键"""
    return {k: v for k, v in d.items() if k in keys}


def rename_keys(d: Dict, key_map: Dict[str, str]) -> Dict:
    """重命名字典的键"""
    return {key_map.get(k, k): v for k, v in d.items()}


# 数据验证
def is_valid_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """验证 URL 格式"""
    pattern = r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'
    return bool(re.match(pattern, url))


# 使用示例
if __name__ == "__main__":
    # 文本处理
    text = "  Hello   World!  "
    print(f"清理后: '{clean_text(text)}'")

    # 数据提取
    text_with_email = "联系邮箱: test@example.com 和 admin@site.com"
    print(f"提取的邮箱: {extract_emails(text_with_email)}")

    # 列表操作
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"分块后: {chunk_list(numbers, 3)}")

    # 字典操作
    data = {"apple": 3, "banana": 1, "orange": 2}
    print(f"排序后: {sort_dict_by_value(data, reverse=True)}")

    # 数据验证
    print(f"邮箱有效: {is_valid_email('test@example.com')}")
    print(f"URL 有效: {is_valid_url('https://www.example.com')}")
