# 市场监管智能体 v4.0 - 使用指南

> **版本**: v4.0
> **发布日期**: 2026-01-12
> **核心功能**: OCR识别 → 数据提取 → 自动归档 → 申请书生成

---

## 📋 快速开始

### 1. 安装依赖

```bash
# 进入项目目录
cd 01_Active_Projects/market_supervision_agent

# 安装依赖
pip install -r requirements_v4.txt
```

### 2. 运行测试

```bash
python start_v4.py test
```

### 3. 启动 Web 界面

```bash
# 启动 Streamlit Web 界面
streamlit run ui/app.py

# 或指定端口
streamlit run ui/app.py --server.port 8501
```

Web 界面包含 4 个页面：
- **文件处理** - 上传文件进行 OCR 识别
- **数据库管理** - 查看/搜索/管理经营户记录
- **申请书生成** - 选择记录生成 Word 文档
- **归档管理** - 查看文件归档状态

### 4. 使用快速启动脚本

```bash
# 查看帮助
python start_v4.py --help

# OCR识别
python start_v4.py ocr --image test.jpg --type id_card

# 生成申请书（从数据库ID）
python start_v4.py generate --id 1

# 数据库操作
python start_v4.py db list
python start_v4.py db search --keyword "张三"
python start_v4.py db stats

# 文件归档
python start_v4.py archive list
python start_v4.py archive stats

# 启动Web界面
python start_v4.py ui
```

---

## 🏗️ 项目结构

```
market_supervision_agent/
├── src/                           # 源代码
│   ├── __init__.py               # 包导出
│   ├── ocr_engine.py             # OCR识别引擎
│   ├── data_extractor.py         # 数据提取器
│   ├── database_manager.py       # 数据库管理器
│   ├── file_archiver.py          # 文件归档器
│   ├── application_generator.py  # 申请书生成器
│   └── workflow.py               # LangGraph工作流
├── ui/                           # Web界面
│   ├── __init__.py
│   └── app.py                    # Streamlit应用
├── config/                       # 配置文件
│   ├── ocr_config.yaml           # OCR配置
│   └── database_schema.yaml      # 数据库结构定义
├── data/                         # 数据目录
│   └── operators_database.db     # SQLite数据库
├── archives/                     # 归档目录
├── templates/                    # Word模板
├── output/                       # 生成文档输出
├── tests/                        # 测试脚本
│   ├── test_basic.py             # 基础测试
│   └── test_workflow.py          # 工作流测试
├── start_v4.py                   # 快速启动脚本
├── requirements_v4.txt           # 依赖清单
├── TECH_DESIGN_V4.md             # 技术设计文档
└── README_V4.md                  # 本文档
```

---

## 🎯 核心功能

### 1. OCR识别引擎 (OCREngine)

**功能**: 从图片/PDF中识别文字

```python
from src.ocr_engine import OCREngine

engine = OCREngine()

# 识别身份证
result = engine.recognize_id_card("id_card.jpg")
# {'name': '张三', 'id_card': '110101199001011234', ...}

# 识别营业执照
result = engine.recognize_business_license("license.jpg")
# {'company_name': 'XX公司', 'credit_code': '91110000XXXXXXXXXX', ...}

# 通用识别
result = engine.recognize_image("document.jpg")
# {'text': '完整文本', 'regions': [...]}
```

### 2. 数据提取器 (DataExtractor)

**功能**: 从OCR结果提取结构化数据

```python
from src.data_extractor import DataExtractor

extractor = DataExtractor()

# 从身份证提取
data = extractor.extract_from_id_card(ocr_result)
# {'operator_name': '张三', 'id_card': '...', 'gender': '男'}

# 从营业执照提取
data = extractor.extract_from_business_license(ocr_result)
# {'business_name': 'XX便利店', 'credit_code': '...'}

# 合并多个数据源
merged = extractor.merge_data(id_data, license_data)
# OperatorData 对象
```

### 3. 数据库管理器 (DatabaseManager)

**功能**: 管理经营户档案

```python
from src.database_manager import DatabaseManager

db = DatabaseManager()

# 插入记录
operator_id = db.insert_operator({
    "operator_name": "张三",
    "id_card": "110101199001011234",
    "business_name": "张三便利店"
})

# 查询记录
operator = db.get_operator_by_id_card("110101199001011234")

# 搜索
results = db.search_operators("张三")

# 统计
stats = db.get_statistics()
```

### 4. 文件归档器 (FileArchiver)

**功能**: 自动分类和归档文档

```python
from src.file_archiver import FileArchiver

archiver = FileArchiver("archives")

# 文件分类
category = archiver.categorize_file("身份证.jpg")
# 'id_card'

# 归档经营者的所有文件
archive_path = archiver.archive_operator_files(
    operator_name="张三",
    id_card="110101199001011234",
    files={
        'id_card': 'path/to/id_card.jpg',
        'business_license': 'path/to/license.jpg'
    }
)

# 清理桌面
cleaned = archiver.clean_desktop(
    desktop_path="~/Desktop",
    processed_files=["file1.jpg", "file2.pdf"]
)
```

### 5. 申请书生成器 (ApplicationGenerator)

**功能**: 使用Word模板生成申请书

```python
from src.application_generator import ApplicationGenerator

generator = ApplicationGenerator()

# 生成申请书
output = generator.generate_application(
    operator_data={
        "operator_name": "张三",
        "business_name": "张三便利店",
        ...
    },
    template_name="个体工商户开业登记申请书.docx",
    output_dir="output"
)

# 检查数据完整性
completeness = generator.check_data_completeness(
    operator_data,
    "个体工商户开业登记申请书.docx"
)
```

---

## 🔄 完整工作流示例

```python
from src import OCREngine, DataExtractor, DatabaseManager, FileArchiver, ApplicationGenerator

# 1. OCR识别
engine = OCREngine()
id_result = engine.recognize_id_card("桌面/身份证.jpg")
license_result = engine.recognize_business_license("桌面/营业执照.jpg")

# 2. 数据提取
extractor = DataExtractor()
id_data = extractor.extract_from_id_card(id_result, "桌面/身份证.jpg")
license_data = extractor.extract_from_business_license(license_result, "桌面/营业执照.jpg")

# 3. 合并数据
operator_data = extractor.merge_data(id_data, license_data)

# 4. 保存到数据库
db = DatabaseManager()
operator_id = db.insert_operator(operator_data.to_dict())

# 5. 归档文件
archiver = FileArchiver()
archive_path = archiver.archive_operator_files(
    operator_name=operator_data.operator_name,
    id_card=operator_data.id_card,
    files={
        'id_card': '桌面/身份证.jpg',
        'business_license': '桌面/营业执照.jpg'
    }
)

# 6. 清理桌面
archiver.clean_desktop("桌面", ["桌面/身份证.jpg", "桌面/营业执照.jpg"])

# 7. 生成申请书
generator = ApplicationGenerator()
output_doc = generator.generate_application(
    operator_data.to_dict(),
    output_dir="output"
)

print(f"处理完成！申请书: {output_doc}")
```

### 更简单的方式 - 使用工作流

```python
from src.workflow import process_files, quick_process

# 方式1: 处理文件列表
result = process_files(['身份证.jpg', '营业执照.pdf'])

# 方式2: 快速处理（最常用）
result = quick_process('身份证.jpg', '营业执照.pdf')

# 查看结果
print(result['operator_data'])  # 提取的数据
print(result['operator_id'])    # 数据库ID
print(result['messages'])       # 处理消息
```

---

## 📊 数据库表结构

### operators 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键ID |
| operator_name | TEXT | 经营者姓名 |
| id_card | TEXT | 身份证号（唯一） |
| phone | TEXT | 联系电话 |
| business_name | TEXT | 个体工商户名称 |
| business_address | TEXT | 经营场所 |
| ... | ... | 更多字段见设计文档 |

---

## ⚙️ 配置说明

### OCR配置 (config/ocr_config.yaml)

```yaml
paddleocr:
  use_gpu: false        # 是否使用GPU
  lang: ch              # 语言
  use_angle_cls: true   # 启用方向分类

file_classification:
  id_card:
    keywords: ["身份证", "id_card"]
    extensions: [".jpg", ".png"]
  # ... 更多配置
```

### 数据库配置 (config/database_schema.yaml)

定义了表结构、索引、验证规则等。

---

## 🚧 待开发功能

- [ ] LangGraph工作流引擎集成（可选）
- [ ] 批量处理模式
- [ ] 导出功能增强
- [ ] 数据备份和恢复
- [ ] 桌面文件监控（自动触发处理）

---

## 📝 技术设计文档

详细的技术设计请参阅: [TECH_DESIGN_V4.md](TECH_DESIGN_V4.md)

---

## 🔧 故障排除

### OCR识别失败

```bash
# 重新安装PaddleOCR
pip uninstall paddleocr paddlepaddle -y
pip install paddleocr paddlepaddle
```

### 数据库错误

```bash
# 删除数据库重新初始化
rm data/operators_database.db
python start_v4.py test
```

### 依赖冲突

```bash
# 使用虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements_v4.txt
```

---

**版本**: v4.0.0 | **更新日期**: 2026-01-12
