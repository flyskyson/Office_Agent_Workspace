"""
常用文件读写操作
"""

from pathlib import Path
import json
import csv
from typing import Any, List, Dict


def read_text(file_path: str) -> str:
    """读取文本文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_text(file_path: str, content: str):
    """写入文本文件"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def read_json(file_path: str) -> Any:
    """读取 JSON 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(file_path: str, data: Any, indent: int = 2):
    """写入 JSON 文件"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def read_csv(file_path: str) -> List[Dict]:
    """读取 CSV 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(file_path: str, data: List[Dict], fieldnames: List[str] = None):
    """写入 CSV 文件"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    if not fieldnames and data:
        fieldnames = list(data[0].keys())

    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def list_files(directory: str, pattern: str = "*") -> List[Path]:
    """列出目录中的文件"""
    return list(Path(directory).glob(pattern))


def create_directory(directory: str):
    """创建目录"""
    Path(directory).mkdir(parents=True, exist_ok=True)


def file_exists(file_path: str) -> bool:
    """检查文件是否存在"""
    return Path(file_path).exists()


def get_file_size(file_path: str) -> int:
    """获取文件大小（字节）"""
    return Path(file_path).stat().st_size


def delete_file(file_path: str):
    """删除文件"""
    Path(file_path).unlink(missing_ok=True)


# 使用示例
if __name__ == "__main__":
    # 文本文件示例
    write_text("test.txt", "Hello, World!")
    content = read_text("test.txt")
    print(f"文本内容: {content}")

    # JSON 文件示例
    data = {"name": "张三", "age": 25}
    write_json("data.json", data)
    loaded_data = read_json("data.json")
    print(f"JSON 数据: {loaded_data}")

    # CSV 文件示例
    csv_data = [
        {"name": "张三", "age": "25"},
        {"name": "李四", "age": "30"}
    ]
    write_csv("data.csv", csv_data)
    loaded_csv = read_csv("data.csv")
    print(f"CSV 数据: {loaded_csv}")
