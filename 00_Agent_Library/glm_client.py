#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-4.7 API 客户端工具类
简化 GLM-4.7 的调用，支持流式和非流式输出
"""

import os
from typing import List, Dict, Any, Optional, Generator
from dataclasses import dataclass


@dataclass
class Message:
    """消息类"""
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


class GLMClient:
    """
    GLM-4.7 客户端

    使用方式:
    1. 安装 SDK: pip install zai-sdk==0.2.0
    2. 设置环境变量: export GLM_API_KEY="your-api-key"
    3. 或者直接传入 api_key
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "glm-4.7"):
        """
        初始化客户端

        Args:
            api_key: API密钥，如果不提供则从环境变量 GLM_API_KEY 读取
            model: 模型名称，默认为 glm-4.7
        """
        self.api_key = api_key or os.getenv("GLM_API_KEY")
        if not self.api_key:
            raise ValueError("请提供 API Key 或设置环境变量 GLM_API_KEY")

        self.model = model

        # 动态导入 SDK（避免未安装时启动失败）
        try:
            from zai import ZhipuAiClient
            self.client = ZhipuAiClient(api_key=self.api_key)
            self.sdk_available = True
        except ImportError:
            print("警告: 未安装 zai-sdk，请运行: pip install zai-sdk==0.2.0")
            self.client = None
            self.sdk_available = False

    def chat(
        self,
        messages: List[Message],
        temperature: float = 1.0,
        max_tokens: int = 65536,
        thinking_enabled: bool = True,
        stream: bool = False
    ) -> str:
        """
        非流式对话

        Args:
            messages: 消息列表
            temperature: 温度参数 (0.0-2.0)
            max_tokens: 最大输出 tokens
            thinking_enabled: 是否启用深度思考
            stream: 是否使用流式输出

        Returns:
            AI 回复内容
        """
        if not self.sdk_available:
            raise RuntimeError("SDK 未安装，请运行: pip install zai-sdk==0.2.0")

        # 转换消息格式
        msg_dicts = [msg.to_dict() for msg in messages]

        # 构建请求参数
        params = {
            "model": self.model,
            "messages": msg_dicts,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        if thinking_enabled:
            params["thinking"] = {"type": "enabled"}

        if stream:
            params["stream"] = True

        response = self.client.chat.completions.create(**params)

        if stream:
            # 流式处理
            result = ""
            for chunk in response:
                if hasattr(chunk.choices[0].delta, "reasoning_content"):
                    result += chunk.choices[0].delta.reasoning_content or ""
                if hasattr(chunk.choices[0].delta, "content"):
                    result += chunk.choices[0].delta.content or ""
            return result
        else:
            # 非流式
            return response.choices[0].message.content or ""

    def chat_stream(
        self,
        messages: List[Message],
        temperature: float = 1.0,
        max_tokens: int = 65536,
        thinking_enabled: bool = True
    ) -> Generator[str, None, None]:
        """
        流式对话（生成器）

        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大输出 tokens
            thinking_enabled: 是否启用深度思考

        Yields:
            每次生成的文本片段
        """
        if not self.sdk_available:
            raise RuntimeError("SDK 未安装，请运行: pip install zai-sdk==0.2.0")

        msg_dicts = [msg.to_dict() for msg in messages]

        params = {
            "model": self.model,
            "messages": msg_dicts,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True
        }

        if thinking_enabled:
            params["thinking"] = {"type": "enabled"}

        response = self.client.chat.completions.create(**params)

        for chunk in response:
            if hasattr(chunk.choices[0].delta, "reasoning_content"):
                content = chunk.choices[0].delta.reasoning_content or ""
                if content:
                    yield content
            if hasattr(chunk.choices[0].delta, "content"):
                content = chunk.choices[0].delta.content or ""
                if content:
                    yield content


# 便捷函数
def quick_chat(user_message: str, api_key: Optional[str] = None) -> str:
    """
    快速对话（单轮）

    Args:
        user_message: 用户消息
        api_key: API密钥

    Returns:
        AI 回复
    """
    client = GLMClient(api_key=api_key)
    messages = [Message(role="user", content=user_message)]
    return client.chat(messages)


def quick_chat_stream(user_message: str, api_key: Optional[str] = None) -> Generator[str, None, None]:
    """
    快速流式对话

    Args:
        user_message: 用户消息
        api_key: API密钥

    Yields:
        每次生成的文本片段
    """
    client = GLMClient(api_key=api_key)
    messages = [Message(role="user", content=user_message)]
    yield from client.chat_stream(messages)


# 示例代码
if __name__ == "__main__":
    # 示例1: 基础对话
    print("=== 示例1: 基础对话 ===")
    try:
        response = quick_chat("你好，请介绍一下 GLM-4.7")
        print(f"回复: {response}")
    except Exception as e:
        print(f"错误: {e}")

    print()

    # 示例2: 多轮对话
    print("=== 示例2: 多轮对话 ===")
    try:
        client = GLMClient()
        messages = [
            Message(role="user", content="什么是 Python？"),
            Message(role="assistant", content="Python 是一种高级编程语言..."),
            Message(role="user", content="它有哪些特点？")
        ]
        response = client.chat(messages)
        print(f"回复: {response}")
    except Exception as e:
        print(f"错误: {e}")

    print()

    # 示例3: 流式输出
    print("=== 示例3: 流式输出 ===")
    try:
        for chunk in quick_chat_stream("写一首关于春天的诗"):
            print(chunk, end="", flush=True)
        print()  # 换行
    except Exception as e:
        print(f"错误: {e}")
