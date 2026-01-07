@echo off
chcp 65001 >nul
echo ========================================================================
echo 🏠 工作区管家模式 - 智能助手启动
echo ========================================================================
echo.
echo 正在启动智能管家系统...
echo.

echo [步骤 1/3] 扫描工作区全貌...
python workspace_scanner.py
echo.

echo [步骤 2/3] 读取工作区索引...
echo 工作区索引位置: 06_Learning_Journal\workspace_memory\workspace_index_latest.json
echo.

echo [步骤 3/3] 加载管家记忆...
echo 开发者档案: 06_Learning_Journal\AI_MEMORY.md
echo 管家记忆: 06_Learning_Journal\WORKSPACE_MEMORY.md
echo.

echo ========================================================================
echo ✅ 工作区管家模式已激活！
echo ========================================================================
echo.
echo 现在告诉AI助手：
echo "请以工作区管家模式为我服务"
echo.
echo 管家可以：
echo 1. 查询任何文件、项目、代码的位置和用途
echo 2. 追踪代码版本历史和变更
echo 3. 推荐相关项目和代码示例
echo 4. 分析工作区状态和项目进展
echo 5. 提供上下文感知的智能建议
echo.
echo ========================================================================
echo.
pause
