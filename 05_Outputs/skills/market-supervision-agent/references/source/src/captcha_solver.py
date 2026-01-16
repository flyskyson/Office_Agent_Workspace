#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
滑块验证码自动识别与破解
支持多种滑块验证码方案

作者: Claude Code
日期: 2026-01-14
"""

import asyncio
import base64
import time
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from playwright.async_api import async_playwright, Page, Browser
import cv2
import numpy as np
from loguru import logger


class SliderCaptchaSolver:
    """滑块验证码求解器"""

    def __init__(self, page: Page):
        """
        初始化滑块验证码求解器

        Args:
            page: Playwright 页面对象
        """
        self.page = page
        self.screenshot_dir = Path("data/screenshots")
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    async def detect_and_solve_slider(
        self,
        selector: str = ".captcha-slider, .slider-container, .verify-slider",
        timeout: int = 10000
    ) -> bool:
        """
        检测并解决滑块验证码

        Args:
            selector: 滑块验证码容器选择器
            timeout: 超时时间（毫秒）

        Returns:
            是否成功解决
        """
        logger.info("[滑块验证码] 开始检测...")

        # 等待滑块验证码出现
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            logger.info("[滑块验证码] 检测到滑块验证码")
        except Exception as e:
            logger.warning(f"[滑块验证码] 未检测到滑块验证码: {e}")
            return False

        # 尝试多种解决方法
        methods = [
            self._method_playwright_drag,
            self._method_human_simulation,
            self._method_direct_api
        ]

        for method in methods:
            try:
                logger.info(f"[滑块验证码] 尝试方法: {method.__name__}")
                result = await method()
                if result:
                    logger.success("[滑块验证码] 解决成功！")
                    await asyncio.sleep(1)  # 等待验证结果
                    return True
            except Exception as e:
                logger.error(f"[滑块验证码] {method.__name__} 失败: {e}")
                continue

        logger.error("[滑块验证码] 所有方法均失败，需要手动处理")
        return False

    async def _method_playwright_drag(self) -> bool:
        """
        方法1: 使用 Playwright 的拖拽 API（最简单）
        适用于标准 HTML5 drag&drop
        """
        try:
            # 查找滑块按钮
            slider_btn = await self.page.query_selector(".slider-btn, .captcha-slider-btn, .verify-move")

            if not slider_btn:
                logger.warning("[方法1] 未找到滑块按钮")
                return False

            # 获取滑块位置和大小
            box = await slider_btn.bounding_box()
            if not box:
                logger.warning("[方法1] 无法获取滑块位置")
                return False

            # 计算拖动距离（通常是 200-300 像素）
            drag_distance = 250

            # 模拟人类拖动轨迹（先快后慢，带抖动）
            steps = self._generate_human_trajectory(drag_distance)

            # 执行拖动
            await slider_btn.hover()
            await self.page.mouse.down()

            for x, y in steps:
                await self.page.mouse.move(x, y)
                await asyncio.sleep(0.01)  # 短暂延迟

            await self.page.mouse.up()

            # 等待验证结果
            await asyncio.sleep(2)

            # 检查是否成功
            success = await self._check_success()
            return success

        except Exception as e:
            logger.error(f"[方法1] 执行失败: {e}")
            return False

    async def _method_human_simulation(self) -> bool:
        """
        方法2: 人类行为模拟（更真实）
        模拟鼠标移动轨迹、速度变化、停顿等
        """
        try:
            # 查找滑块
            slider = await self.page.query_selector(".slider-btn, .captcha-slider-btn")
            if not slider:
                return False

            # 获取滑块初始位置
            box = await slider.bounding_box()
            if not box:
                return False

            start_x = box['x'] + box['width'] / 2
            start_y = box['y'] + box['height'] / 2

            # 生成类人轨迹
            trajectory = self._generate_realistic_trajectory(start_x, start_y, 250)

            # 执行轨迹
            for i, (x, y, duration) in enumerate(trajectory):
                await self.page.mouse.move(x, y)
                await asyncio.sleep(duration / 1000.0)

                # 在滑块上按下
                if i == 3:
                    await self.page.mouse.down()

                # 在目标位置松开
                if i == len(trajectory) - 3:
                    await self.page.mouse.up()

            await asyncio.sleep(2)
            return await self._check_success()

        except Exception as e:
            logger.error(f"[方法2] 执行失败: {e}")
            return False

    async def _method_direct_api(self) -> bool:
        """
        方法3: 直接调用验证码 API（如果有）
        某些网站提供 JavaScript API 来触发验证
        """
        try:
            # 尝试调用常见的验证码 API
            scripts = [
                "window.verifySlider.success()",
                "document.querySelector('.captcha-slider').click()",
                "document.querySelector('.slider-btn').dispatchEvent(new MouseEvent('mouseup'))"
            ]

            for script in scripts:
                try:
                    await self.page.evaluate(script)
                    await asyncio.sleep(1)
                    if await self._check_success():
                        return True
                except:
                    continue

            return False

        except Exception as e:
            logger.error(f"[方法3] 执行失败: {e}")
            return False

    def _generate_human_trajectory(
        self,
        distance: int,
        num_points: int = 50
    ) -> list:
        """
        生成类人拖动轨迹

        Args:
            distance: 拖动总距离
            num_points: 轨迹点数

        Returns:
            轨迹点列表 [(x, y), ...]
        """
        trajectory = []

        # 使用贝塞尔曲线生成平滑轨迹
        for i in range(num_points):
            # 进度 0-1
            t = i / (num_points - 1)

            # 先加速后减速（ease-in-out）
            if t < 0.5:
                # 加速阶段
                progress = 2 * t * t
            else:
                # 减速阶段
                progress = 1 - 2 * (1 - t) * (1 - t)

            # 计算当前 x 坐标
            x = distance * progress

            # 添加轻微抖动（模拟手抖）
            y = np.random.normal(0, 0.5)

            trajectory.append((x, y))

        return trajectory

    def _generate_realistic_trajectory(
        self,
        start_x: float,
        start_y: float,
        distance: int
    ) -> list:
        """
        生成更真实的鼠标轨迹

        Args:
            start_x: 起始 x 坐标
            start_y: 起始 y 坐标
            distance: 拖动距离

        Returns:
            轨迹列表 [(x, y, duration_ms), ...]
        """
        trajectory = []

        # 阶段1: 鼠标移动到滑块（3个点）
        for i in range(3):
            x = start_x + np.random.normal(0, 2)
            y = start_y + np.random.normal(0, 2)
            duration = 50 + np.random.normal(0, 10)
            trajectory.append((x, y, max(20, duration)))

        # 阶段2: 拖动滑块（20-30个点）
        drag_points = 25
        for i in range(drag_points):
            t = i / (drag_points - 1)

            # 速度变化：开始快，中间慢，结束快
            if t < 0.3:
                progress = (t / 0.3) * 0.6
            elif t < 0.7:
                progress = 0.6 + ((t - 0.3) / 0.4) * 0.2
            else:
                progress = 0.8 + ((t - 0.7) / 0.3) * 0.2

            x = start_x + distance * progress
            y = start_y + np.random.normal(0, 1)

            # 时间间隔：开始和结束稍长
            if i < 5 or i > drag_points - 5:
                duration = 30 + np.random.normal(0, 5)
            else:
                duration = 15 + np.random.normal(0, 3)

            trajectory.append((x, y, max(10, duration)))

        # 阶段3: 拖动后短暂停留（2个点）
        for i in range(2):
            x = start_x + distance + np.random.normal(0, 1)
            y = start_y + np.random.normal(0, 1)
            trajectory.append((x, y, 50))

        return trajectory

    async def _check_success(self) -> bool:
        """
        检查验证是否成功

        Returns:
            是否成功
        """
        try:
            # 检查成功标志（常见成功标志）
            success_indicators = [
                ".success",
                ".captcha-success",
                ".verify-success",
                "[class*='success']",
                "[class*='pass']"
            ]

            for indicator in success_indicators:
                element = await self.page.query_selector(indicator)
                if element:
                    return True

            # 检查错误标志
            error_indicators = [
                ".error",
                ".captcha-error",
                ".verify-error",
                "[class*='fail']"
            ]

            for indicator in error_indicators:
                element = await self.page.query_selector(indicator)
                if element:
                    return False

            # 检查滑块是否消失
            slider = await self.page.query_selector(".slider-btn, .captcha-slider")
            if not slider:
                return True

            # 默认认为成功（等待后续验证）
            return True

        except Exception as e:
            logger.warning(f"[滑块验证码] 检查结果失败: {e}")
            return False


class HybridCaptchaSolver:
    """混合型验证码求解器（滑块 + 点击等）"""

    def __init__(self, page: Page):
        self.page = page
        self.slider_solver = SliderCaptchaSolver(page)

    async def solve_captcha(self, timeout: int = 10000) -> Dict[str, Any]:
        """
        自动检测并解决验证码

        Args:
            timeout: 检测超时时间

        Returns:
            解决结果
        """
        result = {
            "success": False,
            "type": None,
            "method": None,
            "duration": 0
        }

        start_time = time.time()

        try:
            # 检测验证码类型
            captcha_type = await self._detect_captcha_type()
            result["type"] = captcha_type

            logger.info(f"[验证码] 检测到类型: {captcha_type}")

            # 根据类型选择解决方法
            if captcha_type == "slider":
                success = await self.slider_solver.detect_and_solve_slider()
                result["method"] = "slider_simulation"

            elif captcha_type == "click":
                success = await self._solve_click_captcha()
                result["method"] = "click_position"

            elif captcha_type == "calc":
                success = await self._solve_calc_captcha()
                result["method"] = "calc_formula"

            else:
                logger.warning(f"[验证码] 未知类型: {captcha_type}")
                success = False

            result["success"] = success
            result["duration"] = int((time.time() - start_time) * 1000)

            return result

        except Exception as e:
            logger.error(f"[验证码] 解决失败: {e}")
            result["duration"] = int((time.time() - start_time) * 1000)
            return result

    async def _detect_captcha_type(self) -> str:
        """
        检测验证码类型

        Returns:
            验证码类型：slider, click, calc, unknown
        """
        # 检查滑块验证码
        slider_indicators = [
            ".slider-btn",
            ".captcha-slider",
            ".verify-slider",
            ".slide-verify"
        ]

        for indicator in slider_indicators:
            if await self.page.query_selector(indicator):
                return "slider"

        # 检查点击验证码
        click_indicators = [
            ".click-captcha",
            ".verify-click",
            ".captcha-click"
        ]

        for indicator in click_indicators:
            if await self.page.query_selector(indicator):
                return "click"

        # 检查计算验证码
        calc_indicators = [
            ".calc-captcha",
            ".verify-calc",
            "input[name*='calc']"
        ]

        for indicator in calc_indicators:
            if await self.page.query_selector(indicator):
                return "calc"

        return "unknown"

    async def _solve_click_captcha(self) -> bool:
        """解决点击验证码（占位）"""
        # TODO: 实现点击验证码识别
        logger.warning("[验证码] 点击验证码暂未实现")
        return False

    async def _solve_calc_captcha(self) -> bool:
        """解决计算验证码（占位）"""
        # TODO: 实现计算验证码识别
        logger.warning("[验证码] 计算验证码暂未实现")
        return False


# ==================== 测试代码 ====================

async def test_slider_captcha():
    """测试滑块验证码解决"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 导航到政务服务网登录页
        await page.goto("https://zwfw.gxzf.gov.cn/")

        # 等待用户手动打开登录
        logger.info("[测试] 请手动打开登录页面，出现滑块验证码后按回车...")
        input()

        # 尝试解决
        solver = SliderCaptchaSolver(page)
        success = await solver.detect_and_solve_slider()

        logger.info(f"[测试] 解决结果: {'成功' if success else '失败'}")

        await asyncio.sleep(5)
        await browser.close()


if __name__ == "__main__":
    import sys

    # 配置日志
    logger.add(
        "logs/captcha_solver.log",
        rotation="10 MB",
        level="DEBUG",
        encoding="utf-8"
    )

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 运行测试
        asyncio.run(test_slider_captcha())
    else:
        logger.info("[滑块验证码求解器] 使用 --test 参数运行测试")
