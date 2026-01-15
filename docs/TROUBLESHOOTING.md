# 🐛 问题排查指南

本文档提供常见问题的诊断步骤和解决方案。

---

## 🔍 快速诊断流程

```
遇到问题
    ↓
是否是错误信息？
    是 → 查看错误信息部分
    否 → 查看症状部分
    ↓
尝试该问题的解决方案
    ↓
问题解决？
    是 → 完成 ✅
    否 → 查看高级诊断或获取帮助
```

---

## ❌ 常见错误信息

### 中文乱码

**症状**:
- 终端输出中文显示为乱码
- 文件内容中文乱码
- Web界面中文显示异常

**诊断**:
```python
# 测试终端编码
import sys
print(sys.stdout.encoding)  # 应该输出 utf-8 或类似
```

**解决方案**:

1. **修复终端编码**
```python
# 在脚本开头添加
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
```

2. **文件读写指定编码**
```python
# ✅ 正确
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# ❌ 错误
with open('file.txt', 'r') as f:  # Windows可能使用GBK
    content = f.read()
```

3. **VSCode设置**
```json
{
    "files.encoding": "utf8withbom"
}
```

---

### Flask 启动失败

**症状**:
- `flask_app.py` 启动时报错
- 端口占用错误
- 模块导入错误

**诊断**:
```bash
# 检查端口占用
netstat -ano | findstr :5000

# 检查Flask版本
python -c "import flask; print(flask.__version__)"
```

**解决方案**:

1. **端口占用**
```python
# 修改 flask_app.py 中的端口
app.run(host='127.0.0.1', port=5001, debug=True)  # 改为5001
```

2. **模块缺失**
```bash
pip install flask python-docx jinja2
```

3. **路径问题**
```python
# 确保在正确的目录运行
cd 01_Active_Projects/market_supervision_agent
python ui/flask_app.py
```

---

### Playwright 浏览器未安装

**症状**:
```
Error: Executable doesn't exist at ...
```

**诊断**:
```bash
# 检查Playwright安装
python -c "import playwright; print(playwright.__version__)"
```

**解决方案**:

```bash
# 安装Playwright
pip install playwright

# 安装浏览器
playwright install chromium

# 验证安装
playwright install --help
```

---

### OCR 识别错误

**症状**:
- 识别结果不准确
- API调用失败
- 超时错误

**诊断**:
```bash
# 测试百度OCR
python 01_Active_Projects/market_supervision_agent/ocr/baidu_ocr.py --test

# 测试PaddleOCR
python 01_Active_Projects/market_supervision_agent/ocr/paddle_ocr.py --test
```

**解决方案**:

1. **百度OCR API问题**
```python
# 检查API密钥配置
# 确保config/baidu_ocr.yaml中有正确的API_KEY和SECRET_KEY
```

2. **PaddleOCR问题**
```bash
# 重新安装PaddleOCR
pip uninstall paddleocr paddlepaddle
pip install paddleocr paddlepaddle
```

3. **图片质量问题**
```python
# 添加图片预处理
from PIL import Image

image = Image.open('input.jpg')
image = image.convert('RGB')  # 转换格式
image = image.resize((2000, 2000))  # 提高分辨率
image.save('processed.jpg')
```

---

### 依赖安装失败

**症状**:
- `pip install` 报错
- 版本冲突
- 编译错误

**诊断**:
```bash
# 检查pip版本
pip --version

# 检查Python版本
python --version

# 检查已安装的包
pip list
```

**解决方案**:

1. **更新pip**
```bash
python -m pip install --upgrade pip
```

2. **使用虚拟环境**
```bash
# 创建新的虚拟环境
python -m venv venv
venv\Scripts\activate

# 重新安装依赖
pip install -r requirements.txt
```

3. **特定包的问题**
```bash
# 如果chromadb安装失败
pip install chromadb --no-cache-dir

# 如果sentence-transformers安装失败
pip install sentence-transformers --no-deps
pip install transformers torch
```

---

## 🩺 高级诊断

### 日志查看

```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
grep ERROR logs/app.log

# 查看最近的错误
tail -100 logs/app.log | grep ERROR
```

### 调试模式

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# Flask调试模式
app.run(debug=True)

# Streamlit调试
streamlit run app.py --logger.level=debug
```

### 性能分析

```python
import cProfile
import pstats

# 分析函数性能
def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()

    # 你的代码
    your_function()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

---

## 🔧 工具特定问题

### 市场监管智能体

**问题**: 申请书生成失败

**诊断步骤**:
1. 检查模板文件是否存在
2. 检查OCR识别结果
3. 检查YAML配置文件

```bash
# 测试完整流程
python 01_Active_Projects/market_supervision_agent/jinja2_filler.py --test
```

**解决方案**:
```python
# 检查模板路径
from pathlib import Path
template_path = Path("templates/个体工商户开业申请书（最终版）.docx")
print(template_path.exists())  # 应该为True
```

### 记忆助手

**问题**: ChromaDB连接失败

**诊断步骤**:
1. 检查数据库目录
2. 检查磁盘空间
3. 检查文件权限

```bash
# 测试ChromaDB
python -c "import chromadb; client = chromadb.Client(); print('OK')"
```

**解决方案**:
```python
# 重新初始化数据库
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="data/chroma"
))
```

### 文件整理工具

**问题**: 文件移动失败

**诊断步骤**:
1. 检查目标目录权限
2. 检查文件是否被占用
3. 检查路径长度

```bash
# 测试文件操作
python -c "from pathlib import Path; Path('test.txt').write_text('test'); print('OK')"
```

**解决方案**:
```python
# 添加错误处理
try:
    shutil.move(src, dst)
except PermissionError:
    print(f"权限不足: {dst}")
except FileNotFoundError:
    print(f"源文件不存在: {src}")
```

---

## 🆘 获取帮助

### 文档资源

1. **系统文档**
   - [完整系统指南](../COMPLETE_SYSTEM_GUIDE.md)
   - [架构设计](ARCHITECTURE.md)
   - [编码规范](CODING_STANDARDS.md)

2. **专题指南**
   - [扩展开发](guides/AGENT_DEVELOPMENT.md)
   - [技能系统](guides/SKILLS_SYSTEM.md)
   - [想法落地](guides/IDEA_WORKFLOW.md)

### 社区支持

- **超级管家**: 说"超级管家"获取即时帮助
- **技能系统**: 使用特定技能名称触发帮助

### 日志收集

在报告问题时，请提供:

1. **错误信息**: 完整的错误堆栈
2. **复现步骤**: 如何触发问题
3. **环境信息**:
```bash
python --version
pip list
systeminfo  # Windows
```

4. **日志文件**: `logs/app.log` 相关部分

---

## 📋 预防性维护

### 定期检查

```bash
# 每周运行
python workspace_scanner.py  # 扫描工作区
python workspace_cleaner.py  # 清理临时文件

# 每月运行
python workspace_report.py   # 生成报告
python create_snapshot.py    # 创建快照
```

### 健康检查

```python
# health_check.py
def check_system():
    """系统健康检查"""
    checks = {
        "Python版本": check_python_version(),
        "依赖包": check_dependencies(),
        "磁盘空间": check_disk_space(),
        "数据库": check_database(),
        "配置文件": check_config(),
    }

    for name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    return all(checks.values())
```

---

## 🎯 快速参考

### 常用命令

```bash
# 重置环境
deactivate  # 退出虚拟环境
rm -rf venv  # 删除虚拟环境
python -m venv venv  # 创建新虚拟环境
venv\Scripts\activate  # 激活
pip install -r requirements.txt  # 重新安装依赖

# 清理缓存
pip cache purge
python -m playwright install --force chromium  # 重新安装浏览器

# 测试环境
python --version
pip list
pytest  # 运行测试
```

### 重要文件位置

```
Office_Agent_Workspace/
├── logs/                    # 日志文件
├── 01_Active_Projects/
│   ├── market_supervision_agent/
│   │   ├── logs/           # 应用日志
│   │   ├── config/         # 配置文件
│   │   └── templates/      # Word模板
│   └── memory_agent/
│       └── data/           # 数据库文件
└── 06_Learning_Journal/    # 演进日志
```

---

**问题未解决?**
- 🤖 激活超级管家: "超级管家，帮我把这个问题..."
- 📚 查看完整文档: [docs/](.)
- 🔍 搜索类似问题: 查看历史日志
