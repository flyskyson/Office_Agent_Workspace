# 市场监管智能体 v4.0 - Python 3.12 稳定版

## 🚀 快速启动

### 方式 1：双击启动（推荐）
```
双击 "启动项目.bat"
```

### 方式 2：使用虚拟环境（最稳定）
```bash
# 启动 Web UI
venv_py312\Scripts\python.exe ui/flask_app.py

# 访问 http://localhost:5000
```

## 📋 Python 版本说明

### ✅ 推荐版本
- **Python 3.12** - 完全兼容，无问题
- 虚拟环境位置: `venv_py312/`

### ⚠️ 不推荐
- Python 3.14 - 存在兼容性问题
- Python 3.13 - 未充分测试

## 🔧 常用功能

### 1. 数据编辑
```bash
# 交互式编辑
venv_py312\Scripts\python.exe test_form_submit.py

# 或使用启动脚本
启动编辑工具.bat
```

### 2. 查看数据库
```bash
venv_py312\Scripts\python.exe -c "from src.database_manager import DatabaseManager; db = DatabaseManager(); ops = db.list_operators(); [print(f'ID={o[\"id\"]}: {o[\"operator_name\"]}') for o in ops]"
```

### 3. 生成申请书
```bash
venv_py312\Scripts\python.exe start_v4.py generate --id 2
```

### 4. OCR 识别
```bash
venv_py312\Scripts\python.exe start_v4.py ocr --image test.jpg
```

## 📦 虚拟环境

虚拟环境已预装所有依赖：
- Flask 3.1.2
- Werkzeug 3.1.5
- Jinja2 3.1.6
- python-docx
- Pydantic
- Loguru
- baidu-aip（可选）

## 🎯 Web UI 功能

1. **文件处理** - 上传身份证/营业执照进行 OCR 识别
2. **数据库管理** - 查看和搜索记录
3. **数据编辑** - 补录联系电话等信息
4. **申请书生成** - 一键生成 Word 文档

访问地址: http://localhost:5000

## 📝 测试脚本

- `test_web_ui_edit.py` - 完整的 Web UI 编辑功能测试
- `test_form_submit.py` - 交互式命令行编辑工具
- `tests/test_core_modules.py` - 核心模块单元测试

## 🐛 问题排查

### 如果 Flask 无法启动
```bash
# 检查端口占用
netstat -ano | findstr :5000

# 使用虚拟环境启动
venv_py312\Scripts\python.exe ui/flask_app.py
```

### 如果缺少依赖
```bash
# 在虚拟环境中安装
venv_py312\Scripts\pip.exe install -r requirements_v4.txt
```

### 如果数据库出错
```bash
# 备份数据库
copy data\operators_database.db data\backup_%date:~0,4%.db

# 重新初始化
del data\operators_database.db
venv_py312\Scripts\python.exe -c "from src.database_manager import DatabaseManager; DatabaseManager()"
```

## 📊 项目状态

- **核心功能**: 100% 完成
- **Web UI**: 100% 完成（Python 3.12）
- **测试覆盖**: 基本完成
- **文档**: 完善

## 🔗 相关文件

- `启动项目.bat` - 主启动器
- `启动编辑工具.bat` - 数据编辑工具
- `切换Python版本.bat` - Python 版本管理
- `start_v4.py` - 命令行工具
- `ui/flask_app.py` - Flask Web 应用

---

**最后更新**: 2026-01-13
**Python 版本**: 3.12.9
**状态**: ✅ 稳定可用
