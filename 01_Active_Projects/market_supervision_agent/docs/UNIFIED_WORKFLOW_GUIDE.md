# 市场监管智能体 v5.0 - 统一工作流使用指南

**版本**: 5.0.0
**更新日期**: 2026-01-14
**作者**: Claude Code

---

## 📖 目录

1. [系统概述](#系统概述)
2. [核心功能](#核心功能)
3. [快速开始](#快速开始)
4. [三输入源详解](#三输入源详解)
5. [工作流API](#工作流api)
6. [政务服务网自动化](#政务服务网自动化)
7. [Web界面使用](#web界面使用)
8. [多场景支持](#多场景支持)
9. [故障排查](#故障排查)

---

## 系统概述

### 什么是统一工作流？

市场监管智能体 v5.0 引入了**统一工作流引擎**，支持从多个输入源收集数据，自动融合、校验，并生成完整的申请材料。

### 核心特性

✅ **三输入源统一处理**
- 文件上传 + OCR 自动识别
- 政务服务网表单自动填写
- Flask Web 表单补充

✅ **智能数据融合**
- 自动合并多源数据
- 优先级：Web 表单 > 政务服务网 > OCR

✅ **流程进度追踪**
- 断点续传
- 随时恢复处理

✅ **材料智能校验**
- 自动检查必需材料
- 标记缺失和无效材料

✅ **完整输出生成**
- Word 申请书
- 数据库记录
- 流程报告
- 电子档案包

---

## 核心功能

### 工作流阶段

```
┌─────────────────────────────────────────────────────────────┐
│                      统一工作流引擎                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 数据输入 (Data Input)                                   │
│     ├─ 输入源①: 文件上传 + OCR                             │
│     ├─ 输入源②: 政务服务网                                 │
│     └─ 输入源③: Flask Web 表单                             │
│                                                             │
│  2. 数据融合 (Data Fusion)                                  │
│     └─ 合并多源数据，智能补全                               │
│                                                             │
│  3. 数据校验 (Validation)                                   │
│     ├─ 数据完整性检查                                       │
│     └─ 材料状态验证                                         │
│                                                             │
│  4. 数据补充 (Supplement)                                   │
│     └─ 应用默认值和智能推断                                 │
│                                                             │
│  5. 输出生成 (Generation)                                   │
│     ├─ Word 申请书                                          │
│     ├─ 流程报告                                             │
│     ├─ 数据库记录                                           │
│     └─ 电子档案包                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 快速开始

### 方式1: Python 脚本快速处理

```python
from src.unified_workflow import quick_start_registration

# 准备数据
operator_data = {
    'operator_name': '张三',
    'id_card': '450101199001011234',
    'phone': '13800138000',
    'business_name': '张三便利店',
    'business_address': '广西玉林市兴业县蒲塘镇和平路123号',
    'business_scope': '食品销售；日用百货',
    'gender': '男',
    'nation': '汉族'
}

# 一键处理
result = quick_start_registration(operator_data)

print(f"成功: {result['success']}")
print(f"经营户ID: {result['operator_id']}")
print(f"申请书: {result['outputs']['document']}")
```

### 方式2: 分步处理（更灵活）

```python
from src.unified_workflow import create_workflow

# 创建工作流
workflow = create_workflow("registration")
progress = workflow.start_workflow()

# 1. 处理OCR输入
files = ['id_card.jpg', 'property_cert.pdf']
progress = workflow.process_ocr_input(files, progress)

# 2. 处理Web表单输入
form_data = {'business_name': '张三便利店', ...}
progress = workflow.process_web_form_input(form_data, progress)

# 3. 数据融合
progress = workflow.fuse_data(progress)

# 4. 数据补充
progress = workflow.supplement_data(progress)

# 5. 材料校验
progress = workflow.validate_materials(progress)

# 6. 生成输出
progress = workflow.generate_outputs(progress)

# 获取结果
outputs = progress.metadata.get('outputs', {})
```

### 方式3: Flask Web 界面

```bash
# 启动 Web 服务
python ui/flask_app_workflow.py

# 访问 http://localhost:5000
```

---

## 三输入源详解

### 输入源①: 文件上传 + OCR

**用途**: 从证件照片中自动提取信息

**支持文件类型**:
- 身份证（正面/反面）
- 营业执照
- 租赁合同
- 产权证明
- 其他证件

**使用示例**:

```python
# 方式1: Python API
workflow = create_workflow()
progress = workflow.start_workflow()

files = [
    'id_card_front.jpg',
    'id_card_back.jpg',
    'property_cert.pdf'
]
progress = workflow.process_ocr_input(files, progress)
```

```bash
# 方式2: Web API
curl -X POST http://localhost:5000/upload/ocr \
  -F "files=@id_card.jpg" \
  -F "files=@property_cert.pdf" \
  -F "operator_id=1"
```

### 输入源②: 政务服务网

**用途**: 从广西数字政务一体化平台自动填写并提取数据

**平台**: https://zwfw.gxzf.gov.cn/yct/

**功能**:
- 自动登录（保存 Cookies）
- 拟定个体工商户名称
- 填写经营户信息
- 填写经营范围
- 提取已填写数据

**使用示例**:

```python
from src.portal_automation import PortalAutomation, PortalConfig

# 配置
config = PortalConfig(
    username='your_username',
    password='your_password',
    headless=False  # 建议非无头模式
)

# 执行自动化
with PortalAutomation(config) as portal:
    result = portal.process_registration(
        business_name='张三便利店',
        operator_data={
            'operator_name': '张三',
            'id_card': '450101199001011234',
            'phone': '13800138000'
        },
        business_scope='食品销售；日用百货',
        auto_submit=False  # 不自动提交
    )

# 提取的数据
extracted_data = result['extracted_data']
```

```bash
# 方式2: Web API
curl -X POST http://localhost:5000/portal/automation \
  -H "Content-Type: application/json" \
  -d '{
    "operator_id": 1,
    "portal_config": {
      "username": "your_username",
      "password": "your_password"
    }
  }'
```

### 输入源③: Flask Web 表单

**用途**: 通过 Web 表单补充缺失信息

**使用示例**:

```bash
# Web API
curl -X POST http://localhost:5000/form/supplement \
  -F "operator_id=1" \
  -F "business_name=张三便利店" \
  -F "business_address=广西玉林市兴业县蒲塘镇和平路123号" \
  -F "business_scope=食品销售；日用百货"
```

---

## 工作流API

### 核心类: UnifiedWorkflowEngine

```python
from src.unified_workflow import UnifiedWorkflowEngine, WorkflowConfig

# 创建工作流
config = WorkflowConfig(
    scenario="registration",           # 场景
    auto_generate_document=True,       # 自动生成文档
    auto_create_archive=True,          # 自动创建档案
    strict_validation=False            # 严格验证模式
)
workflow = UnifiedWorkflowEngine(config)
```

### 主要方法

#### 1. start_workflow()

启动或恢复工作流

```python
# 新建工作流
progress = workflow.start_workflow(
    operator_data={'operator_name': '张三', ...}
)

# 恢复工作流
progress = workflow.start_workflow(operator_id=123)
```

#### 2. process_ocr_input()

处理 OCR 输入

```python
progress = workflow.process_ocr_input(
    files=['id_card.jpg', 'license.jpg'],
    progress=progress
)
```

#### 3. process_web_portal_input()

处理政务服务网输入

```python
progress = workflow.process_web_portal_input(
    portal_data={'business_name': '...', ...},
    progress=progress
)
```

#### 4. process_web_form_input()

处理 Web 表单输入

```python
progress = workflow.process_web_form_input(
    form_data={'business_name': '...', ...},
    progress=progress
)
```

#### 5. fuse_data()

数据融合

```python
progress = workflow.fuse_data(progress)
```

#### 6. validate_materials()

材料校验

```python
progress = workflow.validate_materials(progress)
```

#### 7. supplement_data()

数据补充

```python
progress = workflow.supplement_data(progress)
```

#### 8. generate_outputs()

生成输出

```python
progress = workflow.generate_outputs(progress)
```

### 便捷函数

```python
from src.unified_workflow import create_workflow

# 快速创建工作流
workflow = create_workflow("registration")

# 快速启动设立流程
result = quick_start_registration(operator_data)
```

---

## 政务服务网自动化

### 配置

```python
from src.portal_automation import PortalConfig

config = PortalConfig(
    username='your_username',       # 政务服务网用户名
    password='your_password',       # 政务服务网密码
    headless=False,                 # 是否无头模式（建议False）
    slow_mo=500,                    # 操作延迟（毫秒）
    cookies_path='data/portal_cookies.json',  # Cookie保存路径
    screenshot_dir='data/screenshots'         # 截图保存路径
)
```

### 完整流程

```python
from src.portal_automation import PortalAutomation

with PortalAutomation(config) as portal:
    # 1. 登录
    portal.login()

    # 2. 导航到设立登记页面
    portal.navigate_to_registration()

    # 3. 拟定名称
    portal.fill_business_name('张三便利店')

    # 4. 填写经营户信息
    portal.fill_operator_info({
        'operator_name': '张三',
        'id_card': '450101199001011234',
        'phone': '13800138000',
        'address': '广西玉林市兴业县蒲塘镇...'
    })

    # 5. 填写经营范围
    portal.fill_business_scope('食品销售；日用百货')

    # 6. 保存表单
    portal.save_form()

    # 7. 提取数据
    extracted = portal.extract_form_data()
```

### 注意事项

⚠️ **验证码处理**: 如果遇到验证码，需要手动输入

⚠️ **页面变化**: 政务服务网页面可能更新，选择器需要相应调整

⚠️ **Cookie 保存**: 首次登录后，Cookie 会保存，后续可免密登录

⚠️ **推荐模式**: 使用非无头模式（`headless=False`），方便观察和调试

---

## Web界面使用

### 启动服务

```bash
python ui/flask_app_workflow.py
```

访问 http://localhost:5000

### API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/workflow/new` | POST | 创建新工作流 |
| `/workflow/<id>` | GET | 查看工作流详情 |
| `/upload/ocr` | POST | 上传文件进行 OCR |
| `/portal/automation` | POST | 政务服务网自动化 |
| `/form/supplement` | POST | Web 表单补充 |
| `/workflow/<id>/fuse` | POST | 数据融合 |
| `/workflow/<id>/validate` | POST | 材料校验 |
| `/workflow/<id>/supplement` | POST | 数据补充 |
| `/workflow/<id>/generate` | POST | 生成输出 |
| `/workflow/<id>/complete` | POST | 一键完成 |

### 使用示例

```bash
# 1. 创建工作流
curl -X POST http://localhost:5000/workflow/new \
  -F "scenario=registration"

# 2. 上传OCR文件
curl -X POST http://localhost:5000/upload/ocr \
  -F "files=@id_card.jpg" \
  -F "operator_id=1"

# 3. 补充表单数据
curl -X POST http://localhost:5000/form/supplement \
  -F "operator_id=1" \
  -F "business_name=张三便利店" \
  -F "business_address=..."

# 4. 一键完成
curl -X POST http://localhost:5000/workflow/1/complete
```

---

## 多场景支持

### 支持的场景

| 场景 | 说明 | 必需字段 | 材料要求 |
|------|------|----------|----------|
| `registration` | 个体工商户设立 | operator_name, id_card, phone, business_name, business_address, business_scope | 身份证、产权证明 |
| `change` | 变更登记 | operator_name, id_card, credit_code, change_items | 身份证、营业执照、变更证明 |
| `cancellation` | 注销登记 | operator_name, id_card, credit_code | 身份证、营业执照、清税证明 |
| `annual_report` | 年报 | operator_name, id_card, credit_code, annual_year | 营业执照 |

### 使用不同场景

```python
from src.unified_workflow import create_workflow

# 设立登记
workflow = create_workflow("registration")

# 变更登记
workflow = create_workflow("change")

# 注销登记
workflow = create_workflow("cancellation")

# 年报
workflow = create_workflow("annual_report")
```

---

## 故障排查

### 常见问题

#### 1. OCR 识别失败

**问题**: OCR 识别返回空结果或错误

**解决方法**:
- 检查图片质量，确保清晰
- 尝试使用百度 OCR（需要 API Key）
- 检查文件路径是否正确

#### 2. 数据库保存失败

**问题**: 保存到数据库时出错

**解决方法**:
- 检查身份证号格式（18位）
- 检查必填字段是否完整
- 查看错误日志获取详细信息

#### 3. 政务服务网自动化失败

**问题**: 无法登录或表单填写失败

**解决方法**:
- 检查用户名密码是否正确
- 手动处理验证码
- 使用非无头模式观察页面
- 检查页面结构是否变化

#### 4. 进度无法恢复

**问题**: operator_id 找不到对应进度

**解决方法**:
- 确认 operator_id 正确
- 检查进度数据库文件是否存在
- 查看日志获取详细错误信息

### 日志调试

```python
from loguru import logger

# 设置日志级别
logger.add("workflow_debug.log", level="DEBUG")

# 工作流会自动记录详细日志
```

---

## 技术支持

- **项目地址**: [01_Active_Projects/market_supervision_agent/](../)
- **核心代码**: [src/unified_workflow.py](src/unified_workflow.py)
- **政务服务网**: [src/portal_automation.py](src/portal_automation.py)
- **Flask API**: [ui/flask_app_workflow.py](ui/flask_app_workflow.py)
- **测试脚本**: [test_unified_workflow.py](test_unified_workflow.py)

---

**版本历史**:
- v5.0.0 (2026-01-14): 初始版本，统一工作流引擎
- v4.0.0: Flask Web UI
- v3.0.0: Jinja2 模板系统

---

**祝使用愉快！** 🎉
