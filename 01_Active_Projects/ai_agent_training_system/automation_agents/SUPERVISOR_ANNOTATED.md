# 自动化监督者 (AutomationSupervisor) - 详细学习文档

> **目标**: 通过详细注释和示例，深入理解 LangGraph 风格的多智能体协作架构

---

## 📚 目录

1. [架构概览](#架构概览)
2. [核心概念](#核心概念)
3. [类关系图](#类关系图)
4. [执行流程](#执行流程)
5. [代码详解](#代码详解)
6. [扩展指南](#扩展指南)
7. [常见问题](#常见问题)

---

## 架构概览

### 什么是监督者模式？

**监督者模式 (Supervisor Pattern)** 是一种多智能体协作模式，其中一个中心化的"监督者"负责协调多个专业化的"工作 Agent"。

```
┌─────────────────────────────────────────────────────────┐
│                  AutomationSupervisor                   │
│                   (监督者 - 协调器)                       │
│                                                         │
│  职责:                                                   │
│  1. 管理所有 Agent                                       │
│  2. 决定执行顺序                                         │
│  3. 传递数据                                            │
│  4. 处理错误                                            │
└─────────────┬───────────────────────────────────────────┘
              │
    ┌─────────┴─────────┬──────────────┬──────────────┐
    │                   │              │              │
    ▼                   ▼              ▼              ▼
┌────────┐      ┌──────────┐   ┌──────────┐   ┌──────────────┐
│ Login  │  →   │  Form    │ → │  File    │ → │  Validation  │
│ Agent  │      │  Agent   │   │  Agent   │   │    Agent     │
└────────┘      └──────────┘   └──────────┘   └──────────────┘
  登录处理         表单填写        文件操作         结果验证
```

### 与 LangGraph 的关系

本实现借鉴了 **LangGraph** 的核心思想：

| LangGraph 概念 | 本实现对应 | 说明 |
|---------------|----------|------|
| Node (节点) | Agent | 每个函数/类是一个处理单元 |
| Edge (边) | next_agent | 决定下一个执行的节点 |
| State (状态) | workflow_state | 跨节点共享的数据 |
| Graph (图) | execute_workflow | 执行流程控制 |

---

## 核心概念

### 1. Agent (智能体/代理)

**Agent** 是一个独立的执行单元，负责完成特定任务。

```python
# Agent 的标准接口
class Agent:
    async def execute(self, input_data: Dict) -> Response:
        """
        输入: input_data (字典)
        输出: Response (包含 success, data, next_agent)
        """
        pass
```

**Agent 的职责**:
- ✅ 单一职责：每个 Agent 只做一件事
- ✅ 独立性：Agent 之间不直接调用
- ✅ 可组合：通过 next_agent 链接

### 2. Response (响应)

**AgentResponse** 是 Agent 之间的通信协议。

```python
class AgentResponse:
    success: bool      # 是否成功
    data: Any          # 返回数据
    error: str         # 错误信息
    next_agent: str    # 下一个 Agent 名称
    message: str       # 执行描述
```

### 3. Workflow (工作流)

**Workflow** 是多个 Agent 按顺序执行的流程。

```
典型工作流:
Login → Form → File → Validation → 完成
```

---

## 类关系图

```
┌───────────────────────────────────────────────────────────────┐
│                         类继承关系                              │
└───────────────────────────────────────────────────────────────┘

                    BaseAutomationAgent
                            ↑
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   LoginAgent          FormAgent          FileAgent   ValidationAgent
   (登录)              (填表)              (文件)          (验证)


┌───────────────────────────────────────────────────────────────┐
│                         组合关系                                │
└───────────────────────────────────────────────────────────────┘

    AutomationSupervisor
         │
         ├─── agents: Dict[str, Agent]
         │    ├─── "login_agent" → LoginAgent
         │    ├─── "form_agent" → FormAgent
         │    ├─── "file_agent" → FileAgent
         │    └─── "validation_agent" → ValidationAgent
         │
         ├─── workflow_state: Dict (共享状态)
         │
         └─── execution_log: List (执行日志)
```

---

## 执行流程

### 完整执行时序图

```
用户                    Supervisor           LoginAgent          FormAgent
 │                          │                    │                  │
 │  execute_workflow()      │                    │                  │
 ├─────────────────────────>│                    │                  │
 │                          │                    │                  │
 │                          │  execute(input)    │                  │
 │                          ├───────────────────>│                  │
 │                          │                    │  填写表单         │
 │                          │                    │                  │
 │                          │  Response(         │                  │
 │                          │    next_agent=     │                  │
 │                          │    "form_agent")   │                  │
 │                          │<───────────────────┤                  │
 │                          │                    │                  │
 │                          │  execute(input)    │                  │
 │                          ├─────────────────────────────────────>│
 │                          │                    │                  │
 │                          │  Response(         │                  │
 │                          │    next_agent=     │                  │
 │                          │    "file_agent")   │                  │
 │                          │<─────────────────────────────────────┤
 │                          │                    │                  │
 │                          │  ...继续...        │                  │
 │                          │                    │                  │
 │  最终结果                 │                    │                  │
 │<─────────────────────────┤                    │                  │
```

### 关键决策点

1. **Agent 选择**: 根据 `next_agent` 字段决定
2. **数据传递**: 通过 `input_data` 累积传递
3. **错误处理**: 任何 Agent 失败立即终止
4. **循环防护**: 最多执行 10 次 Agent

---

## 代码详解

### 1. AgentResponse - 通信协议

**位置**: [supervisor.py:52-78](supervisor.py#L52-L78)

```python
class AgentResponse:
    """
    Agent 之间传递信息的标准格式

    设计思路:
    - 统一返回格式，便于监督者处理
    - next_agent 实现动态工作流
    - timestamp 便于调试和追踪
    """
    def __init__(
        self,
        success: bool,        # 执行是否成功 (必填)
        data: Any = None,     # 返回的数据 (可选)
        error: str = None,    # 错误信息 (失败时必填)
        next_agent: str = None,  # 下一个执行的Agent (可选)
        message: str = ""     # 执行描述 (推荐填写)
    ):
        self.success = success
        self.data = data
        self.error = error
        self.next_agent = next_agent
        self.message = message
        self.timestamp = datetime.now()  # 自动记录时间戳
```

**使用示例**:

```python
# 成功情况
return AgentResponse(
    success=True,
    message="登录成功",
    next_agent="form_agent",
    data={"user_id": 12345}
)

# 失败情况
return AgentResponse(
    success=False,
    error="密码错误",
    message="登录失败"
)
```

---

### 2. BaseAutomationAgent - Agent 基类

**位置**: [supervisor.py:85-118](supervisor.py#L85-L118)

```python
class BaseAutomationAgent:
    """
    所有 Agent 的基类

    设计模式: 模板方法模式 (Template Method)
    - 定义统一的接口 (execute)
    - 子类实现具体行为
    """
    def __init__(self, name: str, agent_type: AutomationAgentType):
        self.name = name              # Agent 名称
        self.agent_type = agent_type   # Agent 类型
        self.enabled = True            # 是否启用
        self.state = {}                # Agent 内部状态

    async def execute(self, input_data: Dict) -> AgentResponse:
        """
        抽象方法，子类必须实现

        参数说明:
            input_data 可能包含:
            - page: Playwright 页面对象 (用于浏览器操作)
            - browser: Playwright 浏览器对象
            - context: 上下文信息
            - config: 配置参数
            - workflow_state: 工作流共享状态

        返回说明:
            必须返回 AgentResponse 对象
        """
        raise NotImplementedError("子类必须实现")
```

---

### 3. LoginAgent - 登录处理

**位置**: [supervisor.py:125-204](supervisor.py#L125-L204)

```python
class LoginAgent(BaseAutomationAgent):
    """
    登录 Agent - 处理网站登录流程

    职责:
    1. 访问登录页面
    2. 填写用户名和密码
    3. 点击登录按钮
    4. 验证登录状态

    输入要求:
    - url: 登录页面URL
    - username: 用户名
    - password: 密码
    - page: Playwright页面对象

    输出:
    - 成功: next_agent="form_agent"
    - 失败: success=False
    """

    async def execute(self, input_data: Dict) -> AgentResponse:
        # 步骤1: 参数提取和验证
        page = input_data.get("page")
        url = input_data.get("url")
        username = input_data.get("username")
        password = input_data.get("password")

        if not all([page, url, username, password]):
            return AgentResponse(
                success=False,
                error="缺少必要参数"
            )

        # 步骤2: 访问登录页面
        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        # 步骤3: 填写表单
        await page.fill("#username", username)
        await page.fill("#password", password)

        # 步骤4: 点击登录
        await page.click(".btn-login")
        await page.wait_for_load_state("networkidle")

        # 步骤5: 验证登录状态
        if "login" not in page.url:
            return AgentResponse(
                success=True,
                message="登录成功",
                next_agent="form_agent"  # ← 关键：指定下一个Agent
            )

        return AgentResponse(
            success=False,
            error="登录失败"
        )
```

**关键技术点**:

| Playwright 方法 | 说明 | 示例 |
|---------------|------|------|
| `page.goto(url)` | 访问URL | `goto("https://example.com")` |
| `page.wait_for_load_state("networkidle")` | 等待网络空闲 | 确保页面加载完成 |
| `page.fill(selector, value)` | 填写输入框 | `fill("#username", "admin")` |
| `page.click(selector)` | 点击元素 | `click(".btn-login")` |
| `page.url` | 获取当前URL | 判断登录状态 |

---

### 4. FormAgent - 表单填写

**位置**: [supervisor.py:211-296](supervisor.py#L211-L296)

```python
class FormAgent(BaseAutomationAgent):
    """
    表单 Agent - 智能填写表单

    特性:
    1. 多选择器策略 (ID → name属性)
    2. 自动识别下拉框
    3. 容错处理
    4. 截图保存
    """

    async def execute(self, input_data: Dict) -> AgentResponse:
        page = input_data.get("page")
        form_data = input_data.get("form_data", {})

        # 等待表单出现
        await page.wait_for_selector("form", timeout=5000)

        filled_count = 0

        for field_name, value in form_data.items():
            # 策略1: 尝试作为下拉框处理
            try:
                select = await page.query_selector(f"select#{field_name}")
                if select:
                    await page.select_option(f"#{field_name}", value)
                    filled_count += 1
                    continue
            except:
                pass

            # 策略2: 尝试作为输入框处理 (ID选择器)
            try:
                await page.fill(f"#{field_name}", value)
                filled_count += 1
            except:
                # 策略3: 尝试 name 属性选择器
                try:
                    await page.fill(f"[name='{field_name}']", value)
                    filled_count += 1
                except:
                    pass  # 跳过无法填写的字段

        # 截图保存
        screenshot_path = input_data.get("screenshot_path", "form_filled.png")
        await page.screenshot(path=screenshot_path)

        return AgentResponse(
            success=True,
            message=f"填写了 {filled_count} 个字段",
            next_agent="file_agent",
            data={"fields_filled": filled_count}
        )
```

**选择器策略**:

```
1. ID选择器 (最优先)
   #username

2. 下拉框专用选择器
   select#username

3. name属性选择器 (备用)
   [name='username']
```

---

### 5. FileAgent - 文件操作

**位置**: [supervisor.py:303-411](supervisor.py#L303-L411)

```python
class FileAgent(BaseAutomationAgent):
    """
    文件 Agent - 处理文件上传/下载/保存

    支持的操作:
    - upload: 上传文件
    - save: 提交表单
    - download: 下载文件
    """

    async def execute(self, input_data: Dict) -> AgentResponse:
        page = input_data.get("page")
        action = input_data.get("action", "save")

        if action == "upload":
            # 文件上传
            file_path = input_data.get("file_path")
            file_input = await page.query_selector("input[type='file']")
            await file_input.set_input_files(file_path)

            return AgentResponse(success=True, message="上传成功")

        elif action == "save":
            # 提交表单
            await page.click(".btn-primary")
            await page.wait_for_load_state("networkidle")

            return AgentResponse(
                success=True,
                message="提交成功",
                next_agent="validation_agent"
            )

        elif action == "download":
            # 文件下载
            async with page.expect_download() as download_info:
                await page.click(".btn-download")
            download = await download_info.value

            save_path = input_data.get("save_path", "file.pdf")
            await download.save_as(save_path)

            return AgentResponse(success=True, message="下载成功")
```

---

### 6. ValidationAgent - 结果验证

**位置**: [supervisor.py:418-499](supervisor.py#L418-L499)

```python
class ValidationAgent(BaseAutomationAgent):
    """
    验证 Agent - 检查操作结果

    验证维度:
    1. URL验证
    2. 页面文本验证
    3. 错误消息检测
    """

    async def execute(self, input_data: Dict) -> AgentResponse:
        page = input_data.get("page")
        expected_url = input_data.get("expected_url")
        expected_text = input_data.get("expected_text")

        results = []

        # 验证1: URL
        if expected_url and expected_url in page.url:
            results.append(f"✅ URL验证通过: {page.url}")
        elif expected_url:
            results.append(f"❌ URL验证失败")

        # 验证2: 文本
        if expected_text:
            page_text = await page.text_content("body")
            if expected_text in page_text:
                results.append(f"✅ 文本验证通过")
            else:
                results.append(f"❌ 文本验证失败")

        # 验证3: 错误检测
        errors = await page.query_selector_all(".error, .alert-danger")
        if errors:
            results.append("⚠️ 发现错误消息")

        # 判断总体是否成功
        has_failures = any("❌" in r for r in results)

        return AgentResponse(
            success=not has_failures,
            message="\n".join(results),
            data={"validation_results": results}
        )
```

---

### 7. AutomationSupervisor - 监督者核心

**位置**: [supervisor.py:506-647](supervisor.py#L506-L647)

```python
class AutomationSupervisor:
    """
    自动化监督者 - 多Agent协调器

    核心职责:
    1. 管理所有 Agent
    2. 决定执行顺序
    3. 传递数据
    4. 处理错误
    """

    def __init__(self):
        # 初始化所有 Agent
        self.agents = {
            "login_agent": LoginAgent(),
            "form_agent": FormAgent(),
            "file_agent": FileAgent(),
            "validation_agent": ValidationAgent()
        }
        self.workflow_state = {}
        self.execution_log = []

    async def execute_workflow(self, workflow_config: Dict) -> AgentResponse:
        """
        执行完整工作流的核心方法

        流程:
        1. 创建浏览器页面
        2. 从 login_agent 开始
        3. 循环执行 Agent
        4. 根据 next_agent 决定下一步
        5. 直到没有下一个 Agent
        """

        # 步骤1: 创建页面
        browser = workflow_config.get("browser")
        page = await browser.new_page()
        input_data = {**workflow_config, "page": page}

        # 步骤2: 初始化执行状态
        current_agent = "login_agent"
        max_iterations = 10  # 防止无限循环
        iteration = 0

        # 步骤3: 主循环
        while current_agent and iteration < max_iterations:
            iteration += 1

            # 获取 Agent
            agent = self.agents.get(current_agent)
            if not agent:
                break

            # 执行 Agent
            response = await agent.execute(input_data)

            # 检查结果
            if not response.success:
                return AgentResponse(
                    success=False,
                    error=f"Agent失败: {response.error}"
                )

            # 更新数据
            input_data.update(response.data or {})

            # 决定下一个 Agent
            current_agent = response.next_agent

            await asyncio.sleep(1)

        return AgentResponse(
            success=True,
            message="工作流完成",
            data={"final_state": input_data}
        )
```

**执行流程图**:

```
┌─────────────────────────────────────────────────────────────┐
│                    execute_workflow()                        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  创建浏览器页面         │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  current_agent =       │
              │  "login_agent"         │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  while current_agent   │◄────────┐
              │  and < 10次:           │         │
              └────────────────────────┘         │
                           │                    │
                           ▼                    │
              ┌────────────────────────┐         │
              │  agent =               │         │
              │  agents[current_agent] │         │
              └────────────────────────┘         │
                           │                    │
                           ▼                    │
              ┌────────────────────────┐         │
              │  response =            │         │
              │  await agent.execute() │         │
              └────────────────────────┘         │
                           │                    │
                           ▼                    │
              ┌────────────────────────┐         │
              │  if not success:       │         │
              │    return error        │         │
              └────────────────────────┘         │
                           │                    │
                           ▼                    │
              ┌────────────────────────┐         │
              │  input_data.update(    │         │
              │    response.data)      │         │
              └────────────────────────┘         │
                           │                    │
                           ▼                    │
              ┌────────────────────────┐         │
              │  current_agent =        │         │
              │  response.next_agent    │         │
              └────────────────────────┘         │
                           │                    │
                           └────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  return success        │
              └────────────────────────┘
```

---

## 扩展指南

### 如何添加新的 Agent？

**步骤1**: 创建 Agent 类

```python
class NewAgent(BaseAutomationAgent):
    """新的Agent - 描述功能"""

    def __init__(self):
        super().__init__("NewAgent", AutomationAgentType.OTHER)

    async def execute(self, input_data: Dict) -> AgentResponse:
        # 实现你的逻辑
        try:
            # ... 处理逻辑 ...

            return AgentResponse(
                success=True,
                message="操作成功",
                next_agent="下一个agent名称"  # 如果需要继续
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"操作失败: {str(e)}"
            )
```python

**步骤2**: 注册到监督者

```python
class AutomationSupervisor:
    def __init__(self):
        self.agents = {
            # ... 现有agents ...
            "new_agent": NewAgent()  # ← 添加新Agent
        }
```

**步骤3**: 在工作流中连接

```python
# 在某个Agent的返回中指定next_agent
return AgentResponse(
    success=True,
    next_agent="new_agent"  # ← 指向新Agent
)
```

### 常见扩展场景

| 场景 | 实现 |
|-----|------|
| **条件分支** | 根据 input_data 返回不同的 next_agent |
| **并行执行** | 使用 asyncio.gather() 同时执行多个Agent |
| **重试机制** | 在 execute_workflow 中添加重试逻辑 |
| **数据持久化** | 在 workflow_state 中保存中间结果 |
| **人工干预** | 添加 input() 等待用户输入 |

### 示例：条件分支

```python
class DecisionAgent(BaseAutomationAgent):
    """决策Agent - 根据数据决定下一步"""

    async def execute(self, input_data: Dict) -> AgentResponse:
        data_type = input_data.get("data_type")

        if data_type == "image":
            return AgentResponse(
                success=True,
                next_agent="image_processor_agent"
            )
        elif data_type == "text":
            return AgentResponse(
                success=True,
                next_agent="text_processor_agent"
            )
        else:
            return AgentResponse(
                success=False,
                error="未知的数据类型"
            )
```

---

## 学习总结

### 关键要点

1. **单一职责**: 每个 Agent 只做一件事
2. **松耦合**: Agent 之间通过 Response 通信，不直接调用
3. **可组合**: 通过 next_agent 灵活组合工作流
4. **容错性**: 统一的错误处理机制

### 设计模式

| 模式 | 应用 |
|-----|------|
| **模板方法** | BaseAutomationAgent 定义执行框架 |
| **策略模式** | 不同 Agent 实现不同策略 |
| **责任链** | Agent 通过 next_agent 传递责任 |
| **门面** | Supervisor 提供统一接口 |

### 与 LangGraph 对比

| 特性 | LangGraph | 本实现 |
|-----|-----------|--------|
| 节点定义 | @node 装饰器 | 类方法 |
| 状态管理 | StateGraph 类 | workflow_state 字典 |
| 类型检查 | TypedDict | 类型注解 |
| 可视化 | 生成 PNG 图 | 执行日志 |

---

## 常见问题

### Q1: 如何调试单个 Agent？

```python
# 直接实例化并执行
agent = LoginAgent()
result = await agent.execute({
    "page": page,
    "url": "http://example.com/login",
    "username": "test",
    "password": "test123"
})
print(result.message)
```

### Q2: 如何添加日志？

```
# 在 Supervisor 中添加
self.log(f"执行 {agent.name}: {response.message}")
```

### Q3: 如何处理异步操作？

```python
# 使用 asyncio.gather 并行执行
results = await asyncio.gather(
    agent1.execute(input_data),
    agent2.execute(input_data)
)
```

### Q4: 如何持久化状态？

```python
# 保存到文件
import json
with open("state.json", "w") as f:
    json.dump(workflow_state, f)
```

---

## 快速测试

```bash
# 1. 启动测试网站
cd test_site
python server.py

# 2. 运行监督者（新终端）
cd ..
python automation_agents/supervisor.py
```

---

**文档版本**: 2.0.0
**最后更新**: 2026-01-16
**作者**: Claude Code
**相关文件**: [supervisor.py](supervisor.py)
