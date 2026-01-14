@echo off
REM 快速上下文生成器 - 给 Claude AI 的工作区状态摘要

echo =====================================================================
echo   Office Agent Workspace - Claude AI 上下文信息
echo =====================================================================
echo.
echo 将以下内容复制粘贴给 Claude，让他快速了解工作区状态
echo.
echo =====================================================================
echo.

echo ## 工作区状态摘要
echo.
echo ### 核心工具
echo   - file_organizer (v1.0.0) - 文件整理
echo   - market_supervision_agent (v3.0.0) - 申请书生成
echo   - memory_agent (v1.0.0) - 记忆助手
echo.
echo ### 新增框架
echo   - agent_toolkit - AgentTool 工具框架
echo   - workflow_engine - 工作流引擎
echo   - office_agent_studio - 统一GUI
echo   - version_manager - 版本管理系统
echo.
echo ### 最近升级 (2026-01-12)
echo   基于 zread 开源项目调研，实施了：
echo   1. AutoGen AgentTool 模式 - 工具互操作
echo   2. LangGraph 状态管理 - 工作流引擎
echo   3. AutoGen Studio GUI - 统一界面
echo.
echo ### 关键特性
echo   - 向后兼容：旧代码继续可用
echo   - 自动备份：升级前自动备份
echo   - 版本追踪：完整的历史记录
echo   - 可回滚：随时恢复旧版本
echo.
echo ### 快速命令
echo   启动GUI: streamlit run office_agent_studio.py
echo   查看状态: python 00_Agent_Library/version_manager.py
echo   文件整理: python 01_Active_Projects/file_organizer/file_organizer.py
echo   申请书: python 01_Active_Projects/market_supervision_agent/jinja2_filler.py --test
echo.
echo ### 关键文件
echo   - COMPLETE_SYSTEM_GUIDE.md - 完整系统指南
echo   - EVOLUTION_GUIDE.md - 演进系统说明
echo   - version_registry.json - 版本注册表
echo   - evolution_log.json - 演进日志
echo.
echo =====================================================================
echo.

pause
