# 市场监管智能体 - 故障排查指南

最后更新: 2026-01-13

---

## 🔥 常见问题

### 问题 1: OCR 引擎初始化失败

**错误信息**:
```
[FAIL] OCR 引擎初始化失败: 没有可用的 OCR 引擎！请安装以下任一：
1. 百度 OCR: pip install baidu-aip
2. PaddleOCR: pip install paddleocr paddlepaddle
```

**原因**: `baidu-aip` SDK 缺少 `chardet` 依赖

**解决方案**:
```bash
cd 01_Active_Projects/market_supervision_agent
venv_py312\Scripts\pip.exe install chardet
```

**验证**:
```bash
venv_py312\Scripts\python.exe -c "from aip import AipOcr; print('OK')"
```

---

### 问题 2: 使用全局 Python 启动导致依赖缺失

**症状**:
- Flask 启动成功但 OCR 不可用
- 日志显示 "百度 OCR SDK 未安装"

**原因**: 使用了全局 Python 而非虚拟环境

**解决方案**:
```bash
# 错误方式
python ui/flask_app.py

# 正确方式
venv_py312\Scripts\python.exe ui/flask_app.py
```

---

### 问题 3: 依赖清单与虚拟环境不同步

**症状**: requirements_v4.txt 中列出的依赖未安装

**预防措施**:
```bash
# 每次更新后同步依赖
venv_py312\Scripts\pip.exe install -r requirements_v4.txt

# 检查已安装依赖
venv_py312\Scripts\pip.exe list
```

---

## 📋 完整依赖检查清单

### 启动前检查

运行以下命令确保所有依赖已安装:

```bash
cd 01_Active_Projects/market_supervision_agent

# 1. 同步依赖
venv_py312\Scripts\pip.exe install -r requirements_v4.txt

# 2. 验证关键模块
venv_py312\Scripts\python.exe -c "from aip import AipOcr; print('✓ baidu-aip')"
venv_py312\Scripts\python.exe -c "from loguru import logger; print('✓ loguru')"
venv_py312\Scripts\python.exe -c "from flask import Flask; print('✓ flask')"

# 3. 启动服务
venv_py312\Scripts\python.exe ui\flask_app.py
```

---

## 🚀 推荐启动流程

### 方式 1: 手动启动

```bash
cd 01_Active_Projects/market_supervision_agent
venv_py312\Scripts\python.exe ui\flask_app.py
```

### 方式 2: 使用启动脚本

创建 `start_flask.bat`:
```bat
@echo off
cd /d "%~dp0"
venv_py312\Scripts\python.exe ui\flask_app.py
pause
```

### 方式 3: 使用统一启动器

```bash
python office_agent_studio.py
# 选择: 1. 市场监管智能体
```

---

## 📊 启动成功日志

正常启动应看到:

```
============================================================
[OK] 市场监管智能体 v4.0 - Flask Web UI
[OK] 版本: 4.0.0
[OK] 正在启动...
============================================================
[OK] OCR 引擎: BAIDU          ← 重要！
[OK] 数据库: 2 条记录
============================================================
[INFO] 访问地址: http://localhost:5000
```

如果看到 `[FAIL] OCR 引擎初始化失败`，参考问题 1。

---

## 🔍 故障排查步骤

### 步骤 1: 检查 Python 环境

```bash
# 确认使用虚拟环境
venv_py312\Scripts\python.exe --version
# 应输出: Python 3.12.x
```

### 步骤 2: 检查依赖

```bash
venv_py312\Scripts\pip.exe list | findstr "baidu-aip chardet"
# 应输出:
# baidu-aip       4.16.13
# chardet         5.2.0
```

### 步骤 3: 测试导入

```bash
venv_py312\Scripts\python.exe -c "from aip import AipOcr; print('OK')"
# 如果报错: ModuleNotFoundError: No module named 'chardet'
# 运行: venv_py312\Scripts\pip.exe install chardet
```

### 步骤 4: 查看详细日志

启动时的详细日志会指出问题:
- `[WARNING] 百度 OCR SDK 未安装` → 安装 baidu-aip 和 chardet
- `[INFO] 使用百度 OCR 引擎` → 成功！

---

## 💡 最佳实践

### ✅ DO

1. **始终使用虚拟环境**
   ```bash
   venv_py312\Scripts\python.exe ui\flask_app.py
   ```

2. **定期同步依赖**
   ```bash
   venv_py312\Scripts\pip.exe install -r requirements_v4.txt
   ```

3. **使用启动脚本**
   - 双击 `.bat` 文件自动使用虚拟环境

### ❌ DON'T

1. **不要使用全局 Python**
   ```bash
   # 错误
   python ui/flask_app.py
   ```

2. **不要忽略 WARNING 日志**
   - `[WARNING]` 通常预示后续问题

3. **不要手动修改虚拟环境**
   - 始终通过 pip 管理依赖

---

## 📞 获取帮助

如果以上方法无法解决问题:

1. **查看完整日志**: `logs/ocr.log`
2. **检查配置文件**: `config/baidu_ocr.yaml`
3. **参考文档**: `BAIDU_OCR_GUIDE.md`
4. **超级管家**: 说 "超级管家" 获取帮助

---

**维护者**: Office Agent Workspace
**版本**: 1.0
**更新日期**: 2026-01-13
