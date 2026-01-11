# 🔄 项目恢复指南

## 项目状态
- **项目名称**: 市场监管智能体
- **当前状态**: ⏸️ 已暂停 (精简版)
- **完整版本**: 已归档到 `02_Project_Archive/20260111_market_supervision_agent_v1.0/`
- **归档日期**: 2026-01-11

## 当前目录内容
此目录包含项目的精简版本，已删除大文件以节省空间：
- ✅ 保留: 所有源代码、配置文件、文档
- 🗑️ 删除: `venv/` 虚拟环境 (约115MB)
- 🗑️ 删除: Python缓存文件

## 恢复选项

### 选项1: 使用精简版 (快速开始)
如果你只需要查看代码或文档，当前目录已足够。

### 选项2: 恢复完整版 (需要开发)
如果需要运行或开发项目，请恢复完整版本：

```bash
# 1. 删除当前精简版
rm -rf 01_Active_Projects/market_supervision_agent/*

# 2. 从归档复制完整版
cp -r 02_Project_Archive/20260111_market_supervision_agent_v1.0/* 01_Active_Projects/market_supervision_agent/

# 3. 重新创建虚拟环境
cd 01_Active_Projects/market_supervision_agent
python -m venv venv

# 4. 激活虚拟环境并安装依赖
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
playwright install chromium

# 5. 配置环境
cp .env.example .env
# 编辑 .env 文件配置实际参数
```

### 选项3: 仅恢复虚拟环境
如果只需要运行环境，不复制其他文件：

```bash
cd 01_Active_Projects/market_supervision_agent

# 创建虚拟环境
python -m venv venv

# 激活并安装
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
playwright install chromium
```

## 验证恢复
```bash
# 运行快速测试
python quick_test.py

# 检查核心模块
python -c "from src.agent_core import MarketSupervisionAgent; print('✅ 核心模块导入成功')"

# 检查Playwright
python -c "import playwright; print(f'✅ Playwright版本: {playwright.__version__}')"
```

## 项目功能验证
恢复后可以测试以下功能：
1. **浏览器控制**: `python src/browser_controller.py`
2. **智能体核心**: `python src/agent_core.py`
3. **表单处理**: 检查 `src/forms/` 目录
4. **配置文件**: 检查 `config/` 目录

## 注意事项
1. **选择器配置**: 恢复后需要检查 `config/selectors.yaml` 是否仍然有效
2. **网站变更**: 政务网站可能已更新，需要调整选择器
3. **依赖版本**: 恢复时可能需更新依赖版本
4. **环境变量**: 需要重新配置 `.env` 文件

## 联系信息
- **工作区**: Office_Agent_Workspace
- **归档版本**: v1.0
- **恢复支持**: 查看归档目录中的 `PAUSED.md` 获取完整信息

---
**提示**: 如需完全删除此项目，可删除整个 `01_Active_Projects/market_supervision_agent/` 目录，完整版本仍保存在归档中。