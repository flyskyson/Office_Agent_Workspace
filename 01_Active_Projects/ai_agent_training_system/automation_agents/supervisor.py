#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化监督者 - 多Agent协作架构
协调登录、表单、文件、验证等Agent完成网上业务自动化

作者: Claude Code
日期: 2026-01-16
版本: 1.0.0
基于: agent_supervisor.py
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

# 添加库路径
LIB_PATH = Path(__file__).parent.parent.parent / "00_Agent_Library"
sys.path.insert(0, str(LIB_PATH))

# 尝试导入workflow_engine，如果失败则使用简化版本
try:
    from workflow_engine import WorkflowGraph, WorkflowStatus
except ImportError:
    # 简化版本：仅用于演示
    class WorkflowGraph:
        pass
    class WorkflowStatus:
        pass


# ============================================================================
# Agent类型定义
# ============================================================================

class AutomationAgentType(Enum):
    """自动化Agent类型"""
    LOGIN = "login"           # 登录Agent
    FORM = "form"             # 表单Agent
    FILE = "file"             # 文件Agent
    VALIDATION = "validation" # 验证Agent
    SUPERVISOR = "supervisor" # 监督者


# ============================================================================
# Agent响应
# ============================================================================

class AgentResponse:
    """Agent执行响应"""

    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: str = None,
        next_agent: str = None,
        message: str = ""
    ):
        self.success = success
        self.data = data
        self.error = error
        self.next_agent = next_agent
        self.message = message
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "next_agent": self.next_agent,
            "message": self.message,
            "timestamp": self.timestamp.isoformat()
        }


# ============================================================================
# 基础Agent类
# ============================================================================

class BaseAutomationAgent:
    """自动化Agent基类"""

    def __init__(self, name: str, agent_type: AutomationAgentType):
        self.name = name
        self.agent_type = agent_type
        self.enabled = True
        self.state = {}

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        执行Agent任务（抽象方法，子类必须实现）

        参数:
            input_data: 输入数据字典，可能包含:
                - page: Playwright页面对象，用于浏览器操作
                - browser: Playwright浏览器对象，用于浏览器控制
                - context: 上下文信息，如会话状态、用户信息等
                - config: 配置信息，如超时时间、选择器等
                - workflow_state: 工作流状态，跨Agent共享的状态数据

        返回:
            AgentResponse: 包含执行结果的对象
                - success: 是否成功
                - data: 返回的数据
                - error: 错误信息（如果失败）
                - next_agent: 下一个执行的Agent名称
                - message: 执行消息描述
        """
        raise NotImplementedError("子类必须实现execute方法")

    def reset(self):
        """重置Agent状态"""
        self.state = {}


# ============================================================================
# 登录Agent
# ============================================================================

class LoginAgent(BaseAutomationAgent):
    """登录Agent - 处理网站登录"""

    def __init__(self):
        super().__init__("LoginAgent", AutomationAgentType.LOGIN)

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        执行登录操作

        工作流程:
            1. 访问登录页面
            2. 填写用户名和密码
            3. 点击登录按钮
            4. 验证登录是否成功（通过URL变化判断）
            5. 返回执行结果

        输入数据:
            - url: 登录页面URL (如: http://127.0.0.1:5555/login)
            - username: 登录用户名
            - password: 登录密码
            - page: Playwright页面对象（已创建的页面）

        返回结果:
            - 成功时: success=True, next_agent="form_agent"
            - 失败时: success=False, error包含失败原因
        """
        try:
            # 获取必要参数
            page = input_data.get("page")
            url = input_data.get("url")
            username = input_data.get("username")
            password = input_data.get("password")

            # 参数校验：确保所有必要参数都存在
            if not all([page, url, username, password]):
                return AgentResponse(
                    success=False,
                    error="缺少必要参数: page, url, username, password"
                )

            # 步骤1: 访问登录页面
            await page.goto(url)
            # 等待页面网络空闲（所有资源加载完成）
            await page.wait_for_load_state("networkidle")

            # 步骤2: 填写登录表单
            # 使用CSS选择器定位用户名输入框（ID为username）
            await page.fill("#username", username)
            # 使用CSS选择器定位密码输入框（ID为password）
            await page.fill("#password", password)

            # 步骤3: 点击登录按钮（CSS类选择器）
            await page.click(".btn-login")
            # 等待登录请求完成
            await page.wait_for_load_state("networkidle")

            # 步骤4: 验证登录是否成功
            # 通过判断URL是否变化来确认登录状态
            current_url = page.url
            if "login" not in current_url:
                # 登录成功：URL不再包含"login"
                return AgentResponse(
                    success=True,
                    message="登录成功",
                    next_agent="form_agent",  # 指定下一个执行的Agent
                    data={"current_url": current_url}
                )
            else:
                # 登录失败：仍在登录页面
                return AgentResponse(
                    success=False,
                    error="登录失败，仍在登录页面"
                )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"登录过程中出错: {str(e)}"
            )


# ============================================================================
# 表单Agent
# ============================================================================

class FormAgent(BaseAutomationAgent):
    """表单Agent - 处理表单填写"""

    def __init__(self):
        super().__init__("FormAgent", AutomationAgentType.FORM)

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        执行表单填写

        工作流程:
            1. 等待表单元素加载完成
            2. 遍历表单数据字典
            3. 智能识别元素类型（下拉框/输入框）
            4. 使用多种选择器策略（ID/name属性）
            5. 截图保存填写结果
            6. 返回执行统计

        输入数据:
            - page: Playwright页面对象
            - form_data: 表单数据字典，格式: {"字段名": "字段值"}
                例如: {"businessName": "测试商店", "phone": "13800138000"}

        选择器策略:
            优先级1: #字段名 (ID选择器)
            优先级2: select#字段名 (下拉框专用)
            优先级3: [name='字段名'] (name属性选择器)
        """
        try:
            # 获取页面对象和表单数据
            page = input_data.get("page")
            form_data = input_data.get("form_data", {})

            if not page:
                return AgentResponse(
                    success=False,
                    error="缺少page对象"
                )

            # 步骤1: 等待表单元素出现（最多等待5秒）
            await page.wait_for_selector("form", timeout=5000)

            # 步骤2: 遍历表单数据，逐个填写字段
            filled_count = 0  # 成功填写的字段计数器

            for field_name, value in form_data.items():
                # 构造ID选择器
                selector = f"#{field_name}"

                try:
                    # 策略1: 检查是否是下拉框（<select>元素）
                    select_element = await page.query_selector(f"select#{field_name}")
                    if select_element:
                        # 使用 select_option 方法处理下拉框
                        await page.select_option(selector, value)
                        filled_count += 1
                    else:
                        # 策略2: 普通输入框，直接填充
                        await page.fill(selector, value)
                        filled_count += 1
                except:
                    # 策略3: ID选择器失败，尝试使用name属性
                    try:
                        await page.fill(f"[name='{field_name}']", value)
                        filled_count += 1
                    except:
                        # 所有策略都失败，跳过该字段
                        # 注: 实际项目中应该记录失败的字段
                        pass

            # 步骤3: 截图保存（用于调试和验证）
            screenshot_path = input_data.get("screenshot_path", "form_filled.png")
            await page.screenshot(path=screenshot_path)

            return AgentResponse(
                success=True,
                message=f"表单填写完成，共填写{filled_count}个字段",
                next_agent="file_agent",  # 指定下一个执行的Agent
                data={"fields_filled": filled_count}
            )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"表单填写过程中出错: {str(e)}"
            )


# ============================================================================
# 文件Agent
# ============================================================================

class FileAgent(BaseAutomationAgent):
    """文件Agent - 处理文件上传下载"""

    def __init__(self):
        super().__init__("FileAgent", AutomationAgentType.FILE)

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        执行文件操作（上传/下载/保存）

        支持的操作类型:
            - upload: 上传文件到网页
            - save: 保存/提交表单（点击提交按钮）
            - download: 从网页下载文件

        工作流程:
            upload模式:
                1. 定位文件输入框（<input type='file'>）
                2. 设置文件路径
                3. 触发上传

            save模式:
                1. 点击提交按钮（.btn-primary）
                2. 等待页面响应

            download模式:
                1. 监听下载事件
                2. 点击下载按钮
                3. 保存文件到指定路径

        输入数据:
            - page: Playwright页面对象
            - action: 操作类型 (upload/download/save)，默认"save"
            - file_path: 文件路径（upload时必填）
            - save_path: 保存路径（download时可选）
        """
        try:
            # 获取参数
            page = input_data.get("page")
            action = input_data.get("action", "save")  # 默认为save操作

            if not page:
                return AgentResponse(
                    success=False,
                    error="缺少page对象"
                )

            # 分支1: 文件上传操作
            if action == "upload":
                file_path = input_data.get("file_path")
                if not file_path:
                    return AgentResponse(
                        success=False,
                        error="缺少file_path参数"
                    )

                # 定位文件输入框
                file_input = await page.query_selector("input[type='file']")
                # 设置要上传的文件路径
                await file_input.set_input_files(file_path)

                return AgentResponse(
                    success=True,
                    message=f"文件上传成功: {file_path}"
                )

            # 分支2: 保存/提交表单操作
            elif action == "save":
                # 点击提交按钮（CSS类选择器 .btn-primary）
                await page.click(".btn-primary")
                # 等待页面响应（网络请求完成）
                await page.wait_for_load_state("networkidle")

                return AgentResponse(
                    success=True,
                    message="表单提交成功",
                    next_agent="validation_agent"  # 指定下一个执行的Agent
                )

            # 分支3: 文件下载操作
            elif action == "download":
                # 创建下载监听器（上下文管理器）
                async with page.expect_download() as download_info:
                    # 点击下载按钮
                    await page.click(".btn-download")
                # 获取下载对象
                download = await download_info.value

                # 保存下载文件到指定路径
                save_path = input_data.get("save_path", "downloaded_file.pdf")
                await download.save_as(save_path)

                return AgentResponse(
                    success=True,
                    message=f"文件下载成功: {save_path}"
                )

            # 分支4: 未知操作类型
            else:
                return AgentResponse(
                    success=False,
                    error=f"未知的操作类型: {action}，支持的类型: upload/save/download"
                )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"文件操作过程中出错: {str(e)}"
            )


# ============================================================================
# 验证Agent
# ============================================================================

class ValidationAgent(BaseAutomationAgent):
    """验证Agent - 验证操作结果"""

    def __init__(self):
        super().__init__("ValidationAgent", AutomationAgentType.VALIDATION)

    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        执行结果验证

        验证项目:
            1. URL验证: 检查当前URL是否包含期望的字符串
            2. 文本验证: 检查页面是否包含期望的文本内容
            3. 错误检测: 检查页面是否有错误提示元素

        验证逻辑:
            - URL验证成功 → 显示 ✅
            - URL验证失败 → 显示 ❌
            - 文本验证成功 → 显示 ✅
            - 文本验证失败 → 显示 ❌
            - 发现错误元素 → 显示 ⚠️
            - 最终成功条件: 没有 ❌ 标记的验证项

        输入数据:
            - page: Playwright页面对象
            - expected_url: 期望的URL字符串（可选）
                例如: "success" 表示期望URL包含"success"
            - expected_text: 期望的页面文本（可选）
                例如: "提交成功" 表示期望页面包含"提交成功"

        返回结果:
            - success: 所有验证是否通过（无 ❌ 标记）
            - message: 详细验证结果列表
            - data.validation_results: 验证结果数组
        """
        try:
            # 获取参数
            page = input_data.get("page")
            expected_url = input_data.get("expected_url")
            expected_text = input_data.get("expected_text")

            # 验证结果列表
            validation_results = []

            # 验证项1: URL验证
            if expected_url:
                current_url = page.url
                if expected_url in current_url:
                    validation_results.append(f"✅ URL验证通过: {current_url}")
                else:
                    validation_results.append(f"❌ URL验证失败: 期望包含'{expected_url}', 实际'{current_url}'")

            # 验证项2: 页面文本验证
            if expected_text:
                # 获取<body>元素的文本内容
                page_text = await page.text_content("body")
                if expected_text in page_text:
                    validation_results.append(f"✅ 文本验证通过: 包含'{expected_text}'")
                else:
                    validation_results.append(f"❌ 文本验证失败: 未包含'{expected_text}'")

            # 验证项3: 错误消息检测
            # 查找页面上所有错误提示元素（.error 或 .alert-danger）
            error_elements = await page.query_selector_all(".error, .alert-danger")
            if error_elements:
                validation_results.append("⚠️ 页面存在错误消息")

            # 计算最终验证结果
            # 成功条件: 没有任何带 ❌ 标记的验证项
            has_failures = len([r for r in validation_results if "❌" in r]) > 0

            return AgentResponse(
                success=not has_failures,
                message="\n".join(validation_results),
                data={"validation_results": validation_results}
            )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"验证过程中出错: {str(e)}"
            )


# ============================================================================
# 监督者Agent
# ============================================================================

class AutomationSupervisor:
    """
    自动化监督者 - 协调多个Agent协作

    使用LangGraph风格的workflow来协调Agent执行
    """

    def __init__(self):
        """初始化监督者"""
        self.agents = {
            "login_agent": LoginAgent(),
            "form_agent": FormAgent(),
            "file_agent": FileAgent(),
            "validation_agent": ValidationAgent()
        }
        self.workflow_state = {}
        self.execution_log = []

    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.execution_log.append(log_entry)
        print(log_entry)

    async def execute_workflow(
        self,
        workflow_config: Dict[str, Any]
    ) -> AgentResponse:
        """
        执行完整的自动化工作流（核心协调方法）

        工作流模式: 链式Agent协作
            LoginAgent → FormAgent → FileAgent → ValidationAgent

        执行流程:
            1. 创建浏览器页面
            2. 从login_agent开始执行
            3. 每个Agent返回后，检查是否成功
            4. 根据next_agent字段决定下一个执行的Agent
            5. 重复步骤3-4，直到没有下一个Agent
            6. 返回最终执行结果

        参数:
            workflow_config: 工作流配置字典
                - start_url: 起始URL（已废弃，统一使用url）
                - url: 登录页面URL
                - username: 登录用户名
                - password: 登录密码
                - form_data: 表单数据字典
                - file_actions: 文件操作列表（可选）
                - browser: Playwright浏览器对象（必填）
                - screenshot_path: 截图保存路径（可选）

        安全机制:
            - 最大迭代次数: 10次（防止无限循环）
            - 异常捕获: 任何Agent失败都会终止工作流
            - 详细日志: 记录每步执行结果
        """
        try:
            # 打印工作流开始标记
            self.log("="*60)
            self.log("🚀 启动自动化工作流")
            self.log("="*60)

            # 步骤1: 获取浏览器对象并创建新页面
            browser = workflow_config.get("browser")
            if not browser:
                return AgentResponse(
                    success=False,
                    error="缺少browser对象，无法创建页面"
                )

            # 创建新的浏览器页面（独立上下文）
            page = await browser.new_page()

            # 准备输入数据：合并工作流配置和页面对象
            input_data = {**workflow_config, "page": page}

            # 步骤2: 初始化工作流执行状态
            current_agent = "login_agent"  # 从登录Agent开始
            max_iterations = 10  # 防止无限循环的安全限制
            iteration = 0

            # 步骤3: 主循环 - 依次执行各个Agent
            while current_agent and iteration < max_iterations:
                iteration += 1
                self.log(f"\n📋 步骤{iteration}: 执行 {current_agent}")

                # 获取当前要执行的Agent
                agent = self.agents.get(current_agent)
                if not agent:
                    # Agent不存在，终止工作流
                    self.log(f"❌ Agent不存在: {current_agent}")
                    break

                # 执行Agent的execute方法
                response = await agent.execute(input_data)

                # 记录Agent返回的消息
                self.log(f"   {response.message}")

                # 检查Agent执行是否成功
                if not response.success:
                    # Agent执行失败，终止工作流并返回错误
                    self.log(f"❌ Agent执行失败: {response.error}")
                    return AgentResponse(
                        success=False,
                        error=f"工作流在{current_agent}阶段失败: {response.error}",
                        data={"execution_log": self.execution_log}
                    )

                # 步骤4: 更新输入数据（传递给下一个Agent）
                # 将Agent返回的数据合并到input_data中
                input_data.update(response.data or {})

                # 步骤5: 获取下一个要执行的Agent
                current_agent = response.next_agent

                # 步骤6: 短暂暂停（便于观察执行过程）
                await asyncio.sleep(1)

            # 工作流执行完成
            self.log("\n" + "="*60)
            self.log("✅ 工作流执行完成")
            self.log("="*60)

            return AgentResponse(
                success=True,
                message="工作流执行成功",
                data={
                    "execution_log": self.execution_log,  # 执行日志
                    "final_state": input_data  # 最终状态
                }
            )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"工作流执行异常: {str(e)}",
                data={"execution_log": self.execution_log}
            )


# ============================================================================
# 测试入口
# ============================================================================

async def main():
    """
    测试入口函数（演示完整工作流）

    测试场景:
        在本地测试网站 (http://127.0.0.1:5555) 上执行完整的登录-填表-提交流程

    前置条件:
        1. 需要先启动测试网站: python test_site/server.py
        2. 测试网站应该在 http://127.0.0.1:5555 监听

    执行流程:
        1. 启动Playwright浏览器（非无头模式，便于观察）
        2. 创建AutomationSupervisor实例
        3. 配置工作流参数
        4. 执行工作流
        5. 打印执行结果
        6. 关闭浏览器

    浏览器参数:
        - headless=False: 显示浏览器窗口（便于调试）
        - slow_mo=500: 操作间隔500ms（放慢速度，便于观察）
    """
    from playwright.async_api import async_playwright

    # 打印测试开始标记
    print("\n" + "="*60)
    print("🤖 自动化监督者测试")
    print("="*60 + "\n")

    # 创建Playwright异步上下文
    async with async_playwright() as p:
        # 启动Chromium浏览器
        # headless=False: 显示浏览器窗口
        # slow_mo=500: 每个操作之间延迟500毫秒（便于观察）
        browser = await p.chromium.launch(headless=False, slow_mo=500)

        try:
            # 步骤1: 创建监督者实例
            supervisor = AutomationSupervisor()

            # 步骤2: 配置工作流参数
            workflow_config = {
                # 浏览器对象
                "browser": browser,

                # 登录配置
                "url": "http://127.0.0.1:5555/login",  # 登录页面URL
                "username": "test_user",              # 测试用户名
                "password": "test123",                # 测试密码

                # 表单数据（登录后要填写的表单）
                "form_data": {
                    "businessName": "测试商店",    # 商店名称
                    "ownerName": "张三",          # 经营者姓名
                    "phone": "13800138000"         # 联系电话
                },

                # 截图保存路径（用于调试）
                "screenshot_path": "test_outputs/supervisor_test.png"
            }

            # 步骤3: 执行工作流
            # 这将依次执行: LoginAgent → FormAgent → FileAgent → ValidationAgent
            result = await supervisor.execute_workflow(workflow_config)

            # 步骤4: 打印执行结果
            print("\n" + "="*60)
            print("执行结果:")
            print("="*60)
            print(f"成功: {result.success}")
            print(f"消息: {result.message}")
            if result.error:
                print(f"错误: {result.error}")
            print("="*60 + "\n")

        finally:
            # 步骤5: 确保浏览器被关闭（释放资源）
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
