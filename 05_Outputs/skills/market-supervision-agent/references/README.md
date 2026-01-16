# 市场监管智能体 - Market Supervision Agent v4.0

> **状态**: ✅ 开发完成 (100%)
> **版本**: v4.0.0
> **更新日期**: 2026-01-15

自动化处理市场监管业务，包括 OCR 识别、数据提取、申请书生成等。

## 📋 项目状态
- **开发状态**: ✅ 完成并可用
- **当前版本**: v4.0.0
- **核心功能**: 100% 完成
- **Flask Web UI**: ✅ 已实现
- **百度 OCR 集成**: ✅ 已集成
- **申请书生成**: ✅ 已完成

## 项目特点

- **OCR 识别**: 支持身份证、营业执照自动识别
- **Flask Web UI**: 友好的 Web 界面，支持文件上传和数据处理
- **Jinja2 模板**: 灵活的申请书生成系统
- **数据库管理**: SQLite 本地数据库，支持增删改查
- **批量处理**: 支持多文件同时上传和数据处理
- **完整的错误处理**: 友好的错误提示和日志记录

## 目录结构

```
market_supervision_agent/
├── src/                          # 核心源代码
│   ├── __init__.py
│   ├── workflow.py               # 工作流引擎
│   ├── database_manager.py       # 数据库管理
│   ├── application_generator.py  # 申请书生成器
│   ├── baidu_ocr_engine.py       # 百度 OCR 引擎
│   ├── data_extractor.py         # 数据提取器
│   ├── file_archiver.py          # 文件归档器
│   └── ocr_engine.py             # OCR 引擎基类
├── ui/                           # Flask Web UI
│   ├── flask_app.py              # Flask 应用入口
│   └── templates/                # HTML 模板
│       ├── index.html
│       ├── upload.html
│       ├── database.html
│       ├── generate.html
│       └── edit.html
├── templates/                    # Word 模板
│   └── 个体工商户开业登记申请书.docx
├── config/                       # 配置文件
│   ├── database_schema.yaml      # 数据库结构
│   └── baidu_ocr.yaml            # 百度 OCR 配置
├── data/                         # 数据目录
│   └── database.db               # SQLite 数据库
├── output/                       # 输出目录
│   └── application_*.docx        # 生成的申请书
├── jinja2_filler.py              # 命令行填充工具
├── requirements_v4.txt            # Python 依赖
├── .env.example                  # 环境变量模板
└── README.md                     # 本文件
```

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 包
pip install -r requirements_v4.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入百度 OCR API 密钥
```

### 2. 启动 Flask Web UI (推荐)

```bash
# 启动 Web 服务
python ui/flask_app.py

# 访问 http://localhost:5000
```

### 3. 使用命令行工具

```bash
# 使用测试数据生成申请书
python jinja2_filler.py --test

# 验证模板
python jinja2_filler.py --validate templates/个体工商户开业登记申请书.docx
```

### 4. Web UI 功能说明

**文件上传页面** (`/upload`)
- 上传身份证/营业执照图片
- 自动 OCR 识别
- 数据提取和保存

**数据库管理页面** (`/database`)
- 查看所有经营户记录
- 搜索和筛选
- 编辑和删除记录

**申请书生成页面** (`/generate`)
- 选择经营户记录
- 一键生成申请书
- 下载 Word 文档

## 使用示例

### 生成申请书

```python
from src.application_generator import ApplicationGenerator

# 准备数据
operator_data = {
    'operator_name': '张三',
    'id_card': '450101199001011234',
    'gender': '男',
    'nation': '汉族',
    'phone': '13800138000',
    'business_name': '张三便利店',
    'business_address': '广西玉林市兴业县蒲塘镇测试路123号',
    'business_scope': '食品销售；日用百货',
    'employee_count': '2',
    'political_status': '群众'
}

# 生成申请书
generator = ApplicationGenerator(template_path='templates')
output_path = generator.generate_application(operator_data, output_dir='output')
print(f'申请书已生成: {output_path}')
```

### 批量生成

```python
from src.application_generator import ApplicationGenerator

# 批量数据
operators_list = [
    {
        'operator_name': '张三',
        'id_card': '450101199001011234',
        'business_name': '张三便利店',
        # ... 更多字段
    },
    {
        'operator_name': '李四',
        'id_card': '450101199001011235',
        'business_name': '李四水果店',
        # ... 更多字段
    }
]

# 批量生成
generator = ApplicationGenerator(template_path='templates')
results = generator.batch_generate(operators_list, output_dir='output')

for r in results:
    if r['success']:
        print(f"✓ {r['operator_name']}: {r['output']}")
    else:
        print(f"✗ {r['operator_name']}: {r['error']}")
```

## 核心模块说明

### workflow.py - 工作流引擎

负责任务调度、流程编排、错误处理。

主要方法：
- `process_files()` - 处理上传的文件
- `extract_data()` - 提取 OCR 数据
- `save_to_database()` - 保存到数据库

### database_manager.py - 数据库管理

SQLite 数据库的增删改查操作。

主要方法：
- `add_operator()` - 添加经营户记录
- `get_operator_by_id()` - 根据 ID 查询
- `search_operators()` - 搜索记录
- `update_operator()` - 更新记录
- `delete_operator()` - 删除记录

### application_generator.py - 申请书生成器

使用 Jinja2 模板生成 Word 文档。

主要方法：
- `generate_application()` - 生成申请书
- `batch_generate()` - 批量生成
- `validate_template()` - 验证模板
- `check_data_completeness()` - 检查数据完整性

### baidu_ocr_engine.py - 百度 OCR 引擎

百度 OCR API 集成，支持身份证和营业执照识别。

主要方法：
- `recognize_id_card()` - 识别身份证
- `recognize_business_license()` - 识别营业执照

## 配置文件说明

### config/baidu_ocr.yaml

百度 OCR API 配置。

```yaml
api_key: "${BAIDU_OCR_API_KEY}"
secret_key: "${BAIDU_OCR_SECRET_KEY}"
```

### config/database_schema.yaml

数据库结构和字段定义。

## 模板系统

### Jinja2 模板变量

申请书模板支持以下变量：

- `operator_name` - 经营者姓名
- `id_card` - 身份证号
- `gender` - 性别
- `nation` - 民族
- `phone` - 联系电话
- `business_name` - 个体工商户名称
- `business_address` - 经营场所
- `business_scope_licensed` - 许可项目
- `business_scope_general` - 一般项目
- `employee_count` - 从业人数
- `political_status` - 政治面貌

### 模板制作

在 Word 文档中使用 `{{变量名}}` 语法：

```
经营者姓名：{{operator_name}}
身份证号：{{id_card}}
个体工商户名称：{{business_name}}
```

## 测试

```bash
# 测试 OCR 引擎
python -c "from src import create_ocr_engine; ocr = create_ocr_engine(); print('OCR引擎:', ocr.active_engine)"

# 测试数据库
python -c "from src.database_manager import DatabaseManager; db = DatabaseManager(); print('记录数:', db.get_record_count())"

# 测试申请书生成
python jinja2_filler.py --test

# 测试 Flask 应用
python ui/flask_app.py
```

## 常见问题

### OCR 识别失败

1. 检查 API 密钥配置
2. 确认图片格式支持（JPG、PNG、PDF）
3. 查看错误日志了解详情

### 数据库错误

```bash
# 重置数据库
rm data/database.db
python -c "from src.database_manager import DatabaseManager; DatabaseManager()"
```

### 模板渲染失败

```bash
# 验证模板变量
python jinja2_filler.py --validate templates/个体工商户开业登记申请书.docx
```

## 版本历史

### v4.0.0 (2026-01-15)
- ✅ Flask Web UI 完整实现
- ✅ 百度 OCR API 集成
- ✅ Jinja2 模板系统
- ✅ 数据库管理功能
- ✅ 申请书自动生成
- ✅ 多文件上传支持

### v3.0.0 (2026-01-12)
- Jinja2 模板系统
- 命令行填充工具

### v1.0.0 (2026-01-11)
- 基础 OCR 功能
- 浏览器自动化

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 项目地址: [01_Active_Projects/market_supervision_agent](.)
- 工作区指南: [../../CLAUDE.md](../../CLAUDE.md)

---

**项目完成时间**: 2026-01-15
**维护状态**: ✅ 活跃维护

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 项目地址: [01_Active_Projects/market_supervision_agent](.)
- 工作区指南: [WORKSPACE_GUIDE.md](../../WORKSPACE_GUIDE.md)

---

**重要提示**: 使用前请确保已正确配置 `config/selectors.yaml` 文件，这是项目能否正常运行的关键！
