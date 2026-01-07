"""
常用 HTTP 请求操作
"""

import requests
from typing import Dict, Any, Optional
import json


def get_request(url: str, params: Dict = None, headers: Dict = None) -> Dict:
    """发送 GET 请求"""
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def post_request(url: str, data: Dict = None, json_data: Dict = None,
                 headers: Dict = None) -> Dict:
    """发送 POST 请求"""
    response = requests.post(url, data=data, json=json_data, headers=headers)
    response.raise_for_status()
    return response.json()


def put_request(url: str, data: Dict = None, json_data: Dict = None,
                headers: Dict = None) -> Dict:
    """发送 PUT 请求"""
    response = requests.put(url, data=data, json=json_data, headers=headers)
    response.raise_for_status()
    return response.json()


def delete_request(url: str, headers: Dict = None) -> Dict:
    """发送 DELETE 请求"""
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.json()


def download_file(url: str, save_path: str):
    """下载文件"""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


# API 客户端类
class APIClient:
    """简单的 API 客户端"""

    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()

    def _get_headers(self) -> Dict:
        """获取请求头"""
        headers = {
            'Content-Type': 'application/json'
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def get(self, endpoint: str, params: Dict = None) -> Dict:
        """GET 请求"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Dict = None) -> Dict:
        """POST 请求"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=data, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: Dict = None) -> Dict:
        """PUT 请求"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(url, json=data, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> Dict:
        """DELETE 请求"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.delete(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()


# 使用示例
if __name__ == "__main__":
    # 简单 GET 请求
    try:
        data = get_request("https://api.github.com/users/python")
        print(f"用户信息: {data}")
    except Exception as e:
        print(f"请求失败: {e}")

    # 使用 API 客户端
    # client = APIClient("https://api.example.com", api_key="your_key")
    # result = client.get("/users/1")
    # print(result)
