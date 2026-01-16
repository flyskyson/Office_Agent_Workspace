# 市场监管智能体

**类型**: 智能体项目
**技术栈**: Flask, Jinja2, 百度OCR, PaddleOCR
**位置**: `01_Active_Projects/market_supervision_agent`

## 技能概述

个体工商户开业申请书自动填写系统，支持OCR识别和Jinja2模板生成

## 核心功能
- **OCR识别营业执照**
- **自动填写申请书**
- **PDF生成**
- **模板管理**

## 快速开始

### 启动服务
```bash
cd 01_Active_Projects/market_supervision_agent
python ui/flask_app.py
```

## 项目结构
- `application_generator.py` - 文件
- `archives/` - 目录
- `BAIDU_OCR_GUIDE.md` - 文件
- `CHANGELOG.md` - 文件
- `config/` - 目录
- `config.json` - 文件
- `data/` - 目录
- `docs/` - 目录
- `jinja2_filler.py` - 文件
- `logs/` - 目录
- `output/` - 目录
- `README.md` - 文件
- `README_PY312.md` - 文件
- `RESTORE_GUIDE.md` - 文件
- `scripts/` - 目录
- `SELECTOR_GUIDE.md` - 文件
- `simple_template_analyzer.py` - 文件
- `simple_word_filler.py` - 文件
- `src/` - 目录
- `src__init__.py` - 文件
- `TECH_DESIGN_V4.md` - 文件
- `temp_scripts/` - 目录
- `template_analyzer.py` - 文件
- `templates/` - 目录
- `test_baidu_api_raw.py` - 文件
- `test_certi/` - 目录
- `test_data.json` - 文件
- `test_data_jinja2.json` - 文件
- `test_database.py` - 文件
- `test_generate_doc.py` - 文件
- `test_multi_file.py` - 文件
- `test_ocr_desktop.py` - 文件
- `test_ocr_direct.py` - 文件
- `test_workflow_integration.py` - 文件
- `tests/` - 目录
- `TOOLS_GUIDE.md` - 文件
- `TROUBLESHOOTING.md` - 文件
- `ui/` - 目录
- `UPDATE_v2.0_README.md` - 文件
- `venv_py312/` - 目录
- `VERSION_COMPARISON.md` - 文件
- `word_application_generator.py` - 文件
- `WORD_TEMPLATE_GUIDE.md` - 文件
- `zero_basics_test.py` - 文件
- `个体工商户申请书填充工具.py` - 文件
- `新版申请书填充工具.py` - 文件
- `李奕凤版申请书使用指南.md` - 文件
- `李奕凤版申请书填充工具.py` - 文件
- `李奕凤版申请书填充工具_v2.py` - 文件

## 技术细节

### 技术栈
- **Flask**
- **Jinja2**
- **百度OCR**
- **PaddleOCR**

### 配置文件
- `config.json` - 配置文件
- `test_data.json` - 配置文件
- `test_data_jinja2.json` - 配置文件


## 使用场景

- 填写个体工商户开业申请书
- OCR识别营业执照信息
- 批量生成申请文档

## 相关链接

- [主技能](../office-agent-workspace/)
- [项目文档](../../../../docs/)
- [CLAUDE.md](../../../../CLAUDE.md)
