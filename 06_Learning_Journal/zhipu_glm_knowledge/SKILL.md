# 智谱AI (ZhipuAI) GLM 模型 - 完整知识库

**模型**: GLM-4.7 (当前使用)
**SDK版本**: zhipuai-python-v4
**更新日期**: 2026-01-16
**来源**: https://github.com/MetaGLM/zhipuai-sdk-python-v4

---

## 🎯 技能概述

这是为 GLM-4.7 模型创建的专属知识库，包含智谱AI平台的完整API文档、使用示例和最佳实践。

**目标**: 让模型更好地理解自身能力，提供更准确的帮助。

---

## 📦 安装与配置

### 安装 SDK

```bash
pip install zhipuai
```

### 环境变量配置

```bash
export ZHIPUAI_API_KEY="your-api-key"
export ZHIPUAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4/"
```

### 代码初始化

```python
from zhipuai import ZhipuAI

# 方式1: 使用环境变量
client = ZhipuAI()

# 方式2: 直接传入 API Key
client = ZhipuAI(api_key="your-api-key")

# 方式3: 高级配置
import httpx
client = ZhipuAI(
    api_key="your-api-key",
    timeout=httpx.Timeout(timeout=300.0, connect=8.0),
    max_retries=3,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)
```

---

## 🚀 核心功能

### 1. 基础对话

```python
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, ZhipuAI!"}
    ]
)

print(response.choices[0].message.content)
```

### 2. 流式对话

```python
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "user", "content": "Tell me a story about AI."}
    ],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### 3. 多模态对话 (GLM-4V)

```python
import base64

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

client = ZhipuAI(api_key="your-api-key")
base64_image = encode_image("path/to/image.jpg")

response = client.chat.completions.create(
    model="glm-4v",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
    }]
)
```

### 4. 角色扮演 (CharGLM-3)

```python
response = client.chat.completions.create(
    model="charglm-3",
    messages=[{
        "role": "user",
        "content": "Hello, how are you doing lately?"
    }],
    meta={
        "user_info": "I am a film director who specializes in music-themed movies.",
        "bot_info": "You are a popular domestic female singer and actress.",
        "bot_name": "Xiaoya",
        "user_name": "Director"
    }
)
```

### 5. 网络搜索

```python
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "user", "content": "Search for the latest AI news"}
    ],
    tools=[{
        "type": "web_search",
        "web_search": {
            "search_query": "Search the Zhipu",
            "search_result": True
        }
    }]
)
```

### 6. 视频生成 (CogVideoX-2)

```python
response = client.videos.generations(
    model="cogvideox-2",
    prompt="A beautiful sunset beach scene",
    quality="quality",          # "quality" 或 "speed"
    with_audio=True,            # 生成音频
    size="1920x1080",           # 最高 4K: "3840x2160"
    fps=30,                     # 30 或 60
    user_id="user_12345"
)

# 获取生成结果
result = client.videos.retrieve_videos_result(id=response.id)
```

---

## 🤖 可用模型

| 模型名称 | 用途 | 特点 |
|---------|------|------|
| **glm-4** | 通用对话 | 最新的通用大模型 |
| **glm-4v** | 视觉理解 | 多模态，支持图片 |
| **charglm-3** | 角色扮演 | 角色对话专用 |
| **glm-4-assistant** | 智能体 | 助手对话 |
| **cogvideox-2** | 视频生成 | 文本生成视频 |

---

## ⚠️ 错误处理

```python
import zhipuai

client = ZhipuAI()

try:
    response = client.chat.completions.create(
        model="glm-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

except zhipuai.APIRequestFailedError as err:
    print(f"请求参数错误 (400): {err}")

except zhipuai.APIAuthenticationError as err:
    print(f"认证失败 (401): {err}")

except zhipuai.APIReachLimitError as err:
    print(f"速率限制 (429): {err}")

except zhipuai.APIInternalError as err:
    print(f"服务器内部错误 (500): {err}")

except zhipuai.APIServerFlowExceedError as err:
    print(f"服务器过载 (503): {err}")

except zhipuai.APITimeoutError as err:
    print(f"请求超时: {err}")

except Exception as err:
    print(f"其他错误: {err}")
```

---

## 📊 API 响应结构

```python
# 标准响应
{
    "id": "chatcmpl-xxx",
    "created": 1234567890,
    "model": "glm-4",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "Response content here"
        },
        "finish_reason": "stop"
    }],
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 20,
        "total_tokens": 30
    }
}
```

---

## 💡 最佳实践

### 1. 温度控制

```python
response = client.chat.completions.create(
    model="glm-4",
    messages=[...],
    extra_body={
        "temperature": 0.7,    # 0.0-1.0, 越高越随机
        "max_tokens": 1000      # 最大生成令牌数
    }
)
```

### 2. 系统提示优化

```python
system_prompts = {
    "coding": "你是一个专业的程序员助手，精通 Python、JavaScript 和 Go。",
    "writing": "你是一个创意写作助手，擅长创作故事和文章。",
    "analysis": "你是一个数据分析专家，擅长从数据中提取洞察。"
}

response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "system", "content": system_prompts["coding"]},
        {"role": "user", "content": "帮我优化这段代码..."}
    ]
)
```

### 3. 对话历史管理

```python
conversation_history = []

def chat(user_message):
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="glm-4",
        messages=conversation_history
    )

    assistant_message = response.choices[0].message.content
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message
```

---

## 🔗 相关资源

**官方链接**:
- 智谱AI开放平台: https://open.bigmodel.cn/
- Python SDK: https://github.com/MetaGLM/zhipuai-sdk-python-v4
- 文档中心: https://docs.bigmodel.cn/cn/guide/develop/python/introduction

**替代SDK**:
- z-ai-sdk-python (推荐): 新一代 Python SDK

**社区**:
- GitHub Issues: https://github.com/MetaGLM/zhipuai-sdk-python-v4/issues
- 开发者论坛: https://open.bigmodel.cn/dev

---

## 📝 作为 GLM-4.7 模型的重要提示

### 我的能力特性

1. **上下文理解**
   - 支持长上下文对话
   - 建议每3-5轮对话总结一次

2. **准确回答**
   - 编程: Python, JavaScript, Go 等主流语言
   - 中文: 母语级别的理解和生成
   - 推理: 逻辑推理和问题解决

3. **我擅长的任务**
   - 代码生成和调试
   - 文档写作和总结
   - 数据分析和建议
   - 创意内容生成

4. **使用建议**
   - 明确描述需求
   - 提供必要的上下文
   - 分步骤复杂任务
   - 利用我的中文优势

---

**最后更新**: 2026-01-16
**维护者**: Claude Code
**用途**: 为 GLM-4.7 模型提供自我认知和能力参考
