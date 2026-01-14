# GLM-4.7 开发参考文档

## 📚 官方资源

- **智谱AI开放平台**: https://open.bigmodel.cn/
- **官方文档**: https://docs.bigmodel.cn/
- **GLM-4.7 专项文档**: https://docs.bigmodel.cn/cn/guide/models/text/glm-4.7
- **快速开始**: https://docs.bigmodel.cn/cn/guide/start/quick-start
- **HTTP API文档**: https://docs.bigmodel.cn/cn/guide/develop/http/introduction
- **对话补全API**: https://docs.bigmodel.cn/api-reference/模型-api/对话补全

## 🌟 GLM-4.7 核心特性

### 模型定位
GLM-4.7 是智谱最新旗舰模型，**面向 Agentic Coding 场景强化**：
- ✨ 增强的编码能力
- 🎯 长程任务规划与工具协同
- 📊 多个公开基准榜单中取得开源模型领先表现
- 💬 回复更简洁自然
- ✍️ 写作更具沉浸感
- 🔧 工具调用时指令遵循更强
- 🎨 Artifacts 前端美感与长程任务完成效率提升

### 技术规格
- **上下文窗口**: 200K 输入 + 128K 输出
- **深度思考模式**: 支持 `thinking` 参数
- **结构化输出**: 支持 JSON 等格式化输出
- **工具调用**: 强化的 Function Calling 能力

## 🔧 API 调用示例

### 1. 基础调用（cURL）

```bash
curl -X POST "https://open.bigmodel.cn/api/paas/v4/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your-api-key" \
    -d '{
        "model": "glm-4.7",
        "messages": [
            {
                "role": "user",
                "content": "作为一名营销专家，请为我的产品创作一个吸引人的口号"
            }
        ],
        "thinking": {
            "type": "enabled"
        },
        "max_tokens": 65536,
        "temperature": 1.0
    }'
```

### 2. Python SDK 调用（新版）

**安装**:
```bash
pip install zai-sdk
# 或指定版本
pip install zai-sdk==0.2.0
```

**代码示例**:
```python
from zai import ZhipuAiClient

client = ZhipuAiClient(api_key="your-api-key")

response = client.chat.completions.create(
    model="glm-4.7",
    messages=[
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的口号"},
        {"role": "assistant", "content": "当然，要创作一个吸引人的口号，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"}
    ],
    thinking={
        "type": "enabled",    # 启用深度思考模式
    },
    max_tokens=65536,          # 最大输出 tokens
    temperature=1.0           # 控制输出的随机性
)

# 获取完整回复
print(response.choices[0].message)
```

**流式调用**:
```python
from zai import ZhipuAiClient

client = ZhipuAiClient(api_key="your-api-key")

response = client.chat.completions.create(
    model="glm-4.7",
    messages=[...],
    thinking={"type": "enabled"},
    stream=True,              # 启用流式输出
    max_tokens=65536,
    temperature=1.0
)

# 流式获取回复
for chunk in response:
    if chunk.choices[0].delta.reasoning_content:
        print(chunk.choices[0].delta.reasoning_content, end='', flush=True)
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

### 3. Python SDK 调用（旧版）

**安装**:
```bash
pip install zhipuai==2.1.5.20250726
```

**代码示例**:
```python
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your-api-key")

response = client.chat.completions.create(
  model="glm-4.7",
  messages=[
      {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的口号"}
  ],
  thinking={
    "type": "enabled",
  },
  max_tokens=65536,
  temperature=1.0
)

print(response.choices[0].message)
```

### 4. Java SDK 调用

**Maven 依赖**:
```xml
<dependency>
    <groupId>ai.z.openapi</groupId>
    <artifactId>zai-sdk</artifactId>
    <version>0.3.0</version>
</dependency>
```

**Gradle 依赖**:
```groovy
implementation 'ai.z.openapi:zai-sdk:0.3.0'
```

**代码示例**:
```java
import ai.z.openapi.ZhipuAiClient;
import ai.z.openapi.service.model.ChatCompletionCreateParams;
import ai.z.openapi.service.model.ChatMessage;
import ai.z.openapi.service.model.ChatMessageRole;
import ai.z.openapi.service.model.ChatThinking;
import java.util.Arrays;

public class BasicChat {
    public static void main(String[] args) {
        // 初始化客户端
        ZhipuAiClient client = ZhipuAiClient.builder()
            .apiKey("your-api-key")
            .build();

        // 创建聊天完成请求
        ChatCompletionCreateParams request = ChatCompletionCreateParams.builder()
            .model("glm-4.7")
            .messages(Arrays.asList(
                ChatMessage.builder()
                    .role(ChatMessageRole.USER.value())
                    .content("作为一名营销专家，请为我的产品创作一个吸引人的口号")
                    .build()
            ))
            .thinking(ChatThinking.builder().type("enabled").build())
            .maxTokens(65536)
            .temperature(1.0f)
            .build();

        // 发送请求
        ChatCompletionResponse response = client.chat().createChatCompletion(request);

        // 获取回复
        if (response.isSuccess()) {
            System.out.println("AI 回复: " + response.getData().getChoices().get(0).getMessage());
        } else {
            System.err.println("错误: " + response.getMsg());
        }
    }
}
```

## 📋 重要参数说明

### 核心参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `model` | string | 模型名称，必须为 `"glm-4.7"` | - |
| `messages` | array | 对话消息列表 | - |
| `thinking` | object | 深度思考模式配置 | - |
| `thinking.type` | string | 思考模式：`"enabled"` 启用，`"disabled"` 禁用 | `"disabled"` |
| `max_tokens` | integer | 最大输出 tokens 数 | 65536 |
| `temperature` | float | 控制输出随机性 (0.0-2.0) | 1.0 |
| `top_p` | float | nucleus sampling (0.01-1.0) | 0.95 |
| `stream` | boolean | 是否使用流式输出 | false |

### Messages 格式

```json
[
    {
        "role": "user",
        "content": "用户输入内容"
    },
    {
        "role": "assistant",
        "content": "助手回复内容"
    },
    {
        "role": "user",
        "content": "用户后续输入"
    }
]
```

### 深度思考模式 (Thinking Mode)

GLM-4.7 支持深度思考模式，适合复杂推理任务：

```python
thinking={
    "type": "enabled",  # 启用深度思考
    "tokens": 10000      # 可选：分配给思考的 token 数
}
```

## 💡 最佳实践

### 1. Agentic Coding 场景
GLM-4.7 针对编程场景优化，适合：
- 代码生成与审查
- 复杂任务拆解
- 工具调用与协同
- 长程任务规划

### 2. 思考模式使用
对于复杂推理任务，启用 `thinking` 参数：
```python
thinking={"type": "enabled"}
```

### 3. 温度参数建议
- **创意写作**: `temperature=1.0-1.5`
- **代码生成**: `temperature=0.2-0.5`
- **逻辑推理**: `temperature=0.1-0.3`

### 4. Token 估算
使用官方 Tokenizer 工具估算上下文长度，避免超出限制。

## 🔗 相关资源

### 开发工具
- **体验中心**: https://open.bigmodel.cn/dev/api# 在线测试模型
- **Tokenizer 工具**: 官方文档提供的 token 计算工具

### 社区资源
- **GitHub**: 搜索 GLM-4 相关项目
- **CSDN/掘金**: 大量实战案例和教程

### SDK 版本
- **Python (新版)**: `zai-sdk==0.2.0`
- **Python (旧版)**: `zhipuai==2.1.5.20250726`
- **Java**: `zai-sdk:0.3.0`

## 📝 更新日志

根据官方文档，GLM-4.7 是最新旗舰模型，持续更新中。建议定期查看官方文档获取最新功能。

---

**最后更新**: 2026-01-13
**文档来源**: 智谱AI官方文档
