# 🛠️ 智能体开发指南

本指南详细说明如何开发新的智能体 (Agent) 并集成到工作区。

---

## 🎯 智能体架构概述

### 什么是智能体?

**智能体 (Agent)** = **自动化工具** + **接口层** + **配置系统**

```
┌─────────────────────────────────────┐
│         用户交互层 (UI)              │
│  Flask Web / Streamlit / CLI        │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│         业务逻辑层 (Core)            │
│  AgentTool基类 + 自定义逻辑          │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│         数据存储层 (Storage)         │
│  文件系统 / 数据库 / 配置文件        │
└─────────────────────────────────────┘
```

---

## 📋 开发流程

### 阶段1: 需求分析

**明确问题**:
```
❌ 模糊: "做一个发票管理工具"
✅ 明确: "自动识别发票信息并生成Excel报表"
```

**定义范围**:
1. **输入**: 发票图片/PDF
2. **处理**: OCR识别 + 数据提取
3. **输出**: Excel报表

**估算工作量**:
- 简单工具: 1-2天
- 中等工具: 3-5天
- 复杂工具: 1-2周

### 阶段2: 架构设计

**选择技术栈**:

| 组件 | 推荐技术 | 备选方案 |
|------|---------|---------|
| **Web界面** | Flask | Streamlit / FastAPI |
| **OCR** | 百度OCR / PaddleOCR | Tesseract |
| **数据处理** | pandas | openpyxl |
| **文档生成** | python-docx | reportlab |

**设计目录结构**:
```
invoice_agent/
├── ui/
│   └── flask_app.py           # Web界面
├── core/
│   ├── __init__.py
│   ├── invoice_agent.py       # 核心逻辑
│   ├── ocr_processor.py       # OCR处理
│   └── excel_generator.py     # Excel生成
├── config/
│   ├── schema.yaml            # 数据模式
│   └── settings.yaml          # 配置文件
├── templates/                 # 模板文件
├── tests/
│   ├── test_invoice_agent.py
│   └── test_data/
├── README.md
└── requirements.txt
```

### 阶段3: 核心开发

**步骤1: 创建AgentTool基类**

```python
# core/invoice_agent.py
from 00_Agent_Library.agent_toolkit import BaseTool
from typing import Dict, Optional

class InvoiceAgent(BaseTool):
    """发票管理智能体"""

    def __init__(self):
        super().__init__(
            name="invoice_agent",
            description="自动识别发票信息并生成Excel报表"
        )

    def validate_input(self, **kwargs) -> tuple[bool, str]:
        """验证输入参数"""
        if 'file_path' not in kwargs:
            return False, "缺少file_path参数"

        file_path = Path(kwargs['file_path'])
        if not file_path.exists():
            return False, f"文件不存在: {file_path}"

        return True, ""

    def execute(self, **kwargs) -> Dict:
        """执行核心逻辑"""
        # 验证输入
        is_valid, error_msg = self.validate_input(**kwargs)
        if not is_valid:
            return {'success': False, 'error': error_msg}

        try:
            # 处理发票
            result = self.process_invoice(kwargs['file_path'])
            return {
                'success': True,
                'result': result,
                'message': '处理完成'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def process_invoice(self, file_path: str) -> Dict:
        """处理发票文件"""
        # 1. OCR识别
        ocr_result = self.ocr_recognize(file_path)

        # 2. 数据提取
        data = self.extract_data(ocr_result)

        # 3. 生成报表
        report = self.generate_report(data)

        return report

    def ocr_recognize(self, file_path: str) -> Dict:
        """OCR识别"""
        # 实现OCR逻辑
        pass

    def extract_data(self, ocr_result: Dict) -> Dict:
        """提取数据"""
        # 实现数据提取逻辑
        pass

    def generate_report(self, data: Dict) -> str:
        """生成报表"""
        # 实现报表生成逻辑
        pass
```

**步骤2: 实现OCR处理**

```python
# core/ocr_processor.py
from paddleocr import PaddleOCR
from pathlib import Path

class OCRProcessor:
    """OCR处理器"""

    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')

    def recognize(self, image_path: str) -> list:
        """识别图片文字"""
        result = self.ocr.ocr(image_path, cls=True)
        return result

    def parse_invoice(self, ocr_result: list) -> dict:
        """解析发票信息"""
        # 实现发票信息提取逻辑
        invoice_data = {
            'invoice_number': '',
            'date': '',
            'amount': '',
            'seller': '',
            'buyer': ''
        }

        # 解析OCR结果
        for line in ocr_result:
            text = line[1][0]
            # 提取关键字段
            if '发票号码' in text:
                invoice_data['invoice_number'] = text.split(':')[-1]
            # ... 其他字段

        return invoice_data
```

**步骤3: 创建Web界面**

```python
# ui/flask_app.py
from flask import Flask, request, jsonify, send_file
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.invoice_agent import InvoiceAgent

app = Flask(__name__)
agent = InvoiceAgent()

@app.route('/')
def index():
    """首页"""
    return '''
    <h1>发票管理智能体</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".jpg,.png,.pdf">
        <button type="submit">上传发票</button>
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    """上传并处理发票"""
    if 'file' not in request.files:
        return jsonify({'error': '未上传文件'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    # 保存临时文件
    temp_path = f'/tmp/{file.filename}'
    file.save(temp_path)

    # 处理发票
    result = agent.execute(file_path=temp_path)

    # 返回结果
    if result['success']:
        return send_file(result['result'], as_attachment=True)
    else:
        return jsonify({'error': result['error']}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
```

### 阶段4: 测试

**单元测试**:
```python
# tests/test_invoice_agent.py
import pytest
from core.invoice_agent import InvoiceAgent

def test_validate_input():
    """测试输入验证"""
    agent = InvoiceAgent()

    # 测试缺少参数
    is_valid, error = agent.validate_input()
    assert not is_valid
    assert "缺少file_path参数" in error

    # 测试文件不存在
    is_valid, error = agent.validate_input(file_path="nonexistent.jpg")
    assert not is_valid
    assert "文件不存在" in error

def test_process_invoice():
    """测试发票处理"""
    agent = InvoiceAgent()
    # 添加测试逻辑
```

**集成测试**:
```bash
# 运行测试
pytest tests/

# 测试覆盖率
pytest --cov=core tests/
```

### 阶段5: 集成

**注册到统一启动器**:

```python
# 在 office_agent_studio.py 中添加
TOOLS = {
    # ... 现有工具
    'invoice_agent': {
        'name': '发票管理智能体',
        'description': '自动识别发票信息并生成Excel报表',
        'script': '01_Active_Projects/invoice_agent/ui/flask_app.py',
        'type': 'web'
    }
}
```

**创建技能文档**:

```markdown
# skills/invoice-processor/SKILL.md

# 发票处理技能

**技能类型**: automation
**触发关键词**: 发票识别, 发票管理, 生成报表
**执行时间**: 2-3分钟

---

## 🎯 技能概述

自动识别发票信息并生成Excel报表

---

## 🔄 执行步骤

### 步骤1: 上传发票
...

### 步骤2: OCR识别
...

### 步骤3: 生成报表
...
```

---

## 🎨 UI设计模式

### Flask Web界面

**适用场景**: 需要复杂交互、文件上传

**模板**:
```python
from flask import Flask, render_template, request, send_file
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # 处理逻辑
    pass
```

### Streamlit界面

**适用场景**: 快速原型、数据展示

**模板**:
```python
import streamlit as st

st.title("发票管理智能体")

# 文件上传
uploaded_file = st.file_uploader("上传发票", type=['jpg', 'png'])

if uploaded_file:
    # 处理文件
    result = process_invoice(uploaded_file)

    # 显示结果
    st.dataframe(result)
```

### CLI界面

**适用场景**: 批量处理、自动化脚本

**模板**:
```python
import argparse

def main():
    parser = argparse.ArgumentParser(description='发票管理智能体')
    parser.add_argument('file', help='发票文件路径')
    parser.add_argument('--output', default='output.xlsx', help='输出文件')

    args = parser.parse_args()

    # 处理文件
    result = process_invoice(args.file)

    # 保存结果
    save_result(result, args.output)

if __name__ == '__main__':
    main()
```

---

## 📦 配置管理

### YAML配置

```yaml
# config/settings.yaml
ocr:
  engine: paddle  # paddle 或 baidu
  api_key: ""
  secret_key: ""

output:
  format: xlsx
  template: "templates/invoice_template.xlsx"

logging:
  level: INFO
  file: logs/invoice_agent.log
```

**加载配置**:
```python
import yaml

def load_config(config_path: str) -> dict:
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

config = load_config('config/settings.yaml')
ocr_engine = config['ocr']['engine']
```

---

## 🔒 错误处理

### 统一错误处理

```python
class AgentError(Exception):
    """智能体错误基类"""
    pass

class OCRError(AgentError):
    """OCR错误"""
    pass

class ValidationError(AgentError):
    """验证错误"""
    pass

# 使用
try:
    result = agent.execute(file_path=file_path)
except OCRError as e:
    logger.error(f"OCR识别失败: {e}")
except ValidationError as e:
    logger.error(f"输入验证失败: {e}")
except Exception as e:
    logger.error(f"未知错误: {e}")
```

---

## 📊 性能优化

### 异步处理

```python
from concurrent.futures import ThreadPoolExecutor

def batch_process(files: list) -> list:
    """批量处理文件"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(process_invoice, files)
    return list(results)
```

### 缓存

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def load_template(template_path: str):
    """加载模板（带缓存）"""
    # 加载逻辑
    pass
```

---

## ✅ 部署清单

开发完成后，检查以下项目:

- [ ] 代码符合[编码规范](../CODING_STANDARDS.md)
- [ ] 所有函数有文档字符串
- [ ] 单元测试覆盖率 > 80%
- [ ] 错误处理完整
- [ ] 配置文件独立
- [ ] 日志记录完整
- [ ] README文档完整
- [ ] 已集成到统一启动器
- [ ] 创建了技能文档
- [ ] Windows兼容性测试通过

---

## 📚 参考示例

**学习现有智能体**:
- [市场监管智能体](../../01_Active_Projects/market_supervision_agent/) - Flask Web + OCR + Word生成
- [记忆助手](../../01_Active_Projects/memory_agent/) - Streamlit + 向量数据库
- [文件整理工具](../../01_Active_Projects/file_organizer/) - CLI + 文件操作

---

## 🚀 下一步

1. **开始开发**: 基于本指南创建新智能体
2. **参考示例**: 学习现有智能体的实现
3. **测试部署**: 完成测试和集成
4. **文档完善**: 编写README和技能文档

**祝开发顺利!** 🎉
