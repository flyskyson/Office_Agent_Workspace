# 市场监管智能体 v4.0 技术设计文档

> **版本**: v4.0
> **创建日期**: 2026-01-12
> **基于开源项目调研结果**
> **核心目标**: 桌面材料OCR识别 → 经营户数据库 → 申请书自动生成

---

## 📋 目录

1. [项目概述](#项目概述)
2. [技术选型](#技术选型)
3. [系统架构](#系统架构)
4. [核心模块设计](#核心模块设计)
5. [数据流程](#数据流程)
6. [数据库设计](#数据库设计)
7. [工作流设计](#工作流设计)
8. [错误处理](#错误处理)
9. [实施计划](#实施计划)

---

## 项目概述

### 业务场景

```
用户操作流程：
1. 将经营者资料放在桌面
   ├── 身份证（正反面）
   ├── 产权证明
   ├── 营业执照电子档
   └── 租赁合同

2. 自动OCR识别
   ├── 提取结构化数据
   └── 录入经营户档案数据库

3. 清理桌面并归档
   ├── 按经营者分类
   └── 归档到指定目录

4. 生成申请书
   ├── 从数据库读取数据
   ├── 填充Word模板
   └── 缺失数据通过UI表单补充
```

### 核心价值

- **自动化**: 80%的数据自动提取，减少手动录入
- **准确性**: OCR识别 + 人工校对双重保障
- **可追溯**: 完整的档案管理和版本控制
- **易扩展**: 模块化设计，便于添加新功能

---

## 技术选型

### 基于开源调研的决策

| 技术领域 | 选择方案 | 替代方案 | 选择理由 |
|---------|---------|---------|---------|
| **OCR识别** | PaddleOCR | Tesseract | 中文准确度高，支持表格识别 |
| **图像处理** | Pillow + OpenCV | - | 成熟稳定，功能完整 |
| **Word操作** | python-docx | docxtpl | 与现有v3.0兼容 |
| **工作流引擎** | LangGraph | Prefect | 状态管理优秀，适合智能体 |
| **文档分类** | Scikit-learn | - | 轻量级，满足需求 |
| **数据库** | SQLite | JSON/TinyDB | 事务支持，适合桌面应用 |
| **PDF处理** | PyPDF | pdfplumber | 表单填充支持好 |

### 依赖清单

```txt
# 核心依赖
paddleocr>=2.7.0          # OCR识别
paddlepaddle>=2.5.0       # PaddlePaddle框架
pillow>=10.0.0            # 图像处理
opencv-python>=4.8.0      # 图像处理增强
python-docx>=1.0.0        # Word文档操作
pypdf>=3.17.0             # PDF表单处理

# 工作流
langgraph>=0.0.20         # 工作流引擎
langchain>=0.1.0          # LangChain生态

# 机器学习
scikit-learn>=1.3.0       # 文档分类

# 数据库
# SQLite - Python内置

# 工具库
pydantic>=2.0.0           # 数据验证
pyyaml>=6.0.0             # 配置文件
loguru>=0.7.0             # 日志记录
rich>=13.0.0              # 终端美化
tqdm>=4.65.0              # 进度条
```

---

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                      市场监管智能体 v4.0                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  文件监控层   │───→│   OCR识别层  │───→│  数据提取层  │      │
│  │ FileWatcher  │    │  OCREngine   │    │DataExtractor │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         ↓                   ↓                   ↓               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  文件归档层   │    │  工作流引擎  │    │  数据库层    │      │
│  │FileArchiver  │    │ LangGraph    │    │  SQLite DB   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         ↓                   ↓                   ↓               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  UI界面层    │←───│  申请书生成  │←───│  模板管理层  │      │
│  │   Streamlit  │    │DocGenerator  │    │TemplateMgr   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 模块职责

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| **FileWatcher** | 监控桌面文件变化 | 文件路径 | 文件事件 |
| **OCREngine** | 识别文档文字 | 图片/PDF | 结构化文本 |
| **DataExtractor** | 提取关键信息 | OCR文本 | 字段字典 |
| **FileArchiver** | 文件分类归档 | 文件+元数据 | 归档路径 |
| **LangGraph** | 工作流编排 | 触发事件 | 执行状态 |
| **SQLiteDB** | 数据持久化 | 数据对象 | 存储结果 |
| **DocGenerator** | 生成申请书 | 模板+数据 | Word文档 |
| **TemplateMgr** | 模板版本管理 | 模板文件 | 模板对象 |
| **StreamlitUI** | 用户交互界面 | 用户输入 | 系统命令 |

---

## 核心模块设计

### 1. OCR识别引擎 (OCREngine)

**功能**: 从图片/PDF中识别文字，提取结构化数据

```python
"""
src/ocr_engine.py
"""
from paddleocr import PaddleOCR
from typing import Dict, List, Optional
import cv2
from pathlib import Path

class OCREngine:
    """OCR识别引擎"""

    def __init__(self, use_gpu: bool = False):
        """初始化OCR引擎

        Args:
            use_gpu: 是否使用GPU加速
        """
        self.ocr = PaddleOCR(
            use_angle_cls=True,  # 启用文字方向分类
            lang='ch',           # 中文识别
            use_gpu=use_gpu,
            show_log=False
        )

    def recognize_image(self, image_path: str) -> Dict:
        """识别图片中的文字

        Args:
            image_path: 图片路径

        Returns:
            识别结果字典
            {
                "text": "识别的完整文本",
                "regions": [
                    {"box": [x1,y1,x2,y2], "text": "区域文字", "confidence": 0.95}
                ],
                "tables": [...]  # 如果有表格
            }
        """
        result = self.ocr.ocr(image_path, cls=True)
        return self._parse_result(result)

    def recognize_id_card(self, image_path: str) -> Dict:
        """专门识别身份证

        Args:
            image_path: 身份证图片路径

        Returns:
            {
                "name": "张三",
                "id_card": "110101199001011234",
                "address": "北京市...",
                "ethnicity": "汉"
            }
        """
        # 预处理身份证图片
        img = cv2.imread(image_path)
        img = self._preprocess_id_card(img)

        # 识别并提取信息
        result = self.ocr.ocr(img, cls=True)

        # 解析身份证特定格式
        return self._parse_id_card(result)

    def recognize_business_license(self, image_path: str) -> Dict:
        """识别营业执照

        Returns:
            {
                "company_name": "XX公司",
                "credit_code": "91110000XXXXXXXXXX",
                "address": "...",
                "legal_person": "..."
            }
        """
        result = self.ocr.ocr(image_path, cls=True)
        return self._parse_business_license(result)

    def _preprocess_id_card(self, img):
        """身份证图片预处理"""
        # 灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 去噪
        denoised = cv2.fastNlMeansDenoising(gray)
        # 二值化
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def _parse_id_card(self, result) -> Dict:
        """解析身份证识别结果"""
        info = {}
        for line in result:
            text = line[1][0]
            # 姓名: 姓名 张三
            if "姓名" in text:
                info["name"] = text.split("姓名")[1].strip()
            # 身份证号: 身份证号码 110101199001011234
            elif "身份证号码" in text:
                info["id_card"] = text.split("身份证号码")[1].strip()
            # 地址
            elif "住址" in text:
                info["address"] = text.split("住址")[1].strip()
        return info

    def _parse_business_license(self, result) -> Dict:
        """解析营业执照识别结果"""
        info = {}
        for line in result:
            text = line[1][0]
            if "名称" in text and "名称" == text[:2]:
                info["company_name"] = text.split("名称")[1].strip()
            elif "统一社会信用代码" in text:
                info["credit_code"] = text.split("统一社会信用代码")[1].strip()
        return info
```

### 2. 数据提取器 (DataExtractor)

**功能**: 从OCR结果中提取结构化字段

```python
"""
src/data_extractor.py
"""
import re
from typing import Dict, Any
from pydantic import BaseModel, validator

class OperatorData(BaseModel):
    """经营户数据模型"""
    # 基本信息
    operator_name: str
    id_card: str
    phone: Optional[str] = None
    gender: Optional[str] = None
    nation: Optional[str] = None

    # 经营信息
    business_name: Optional[str] = None
    business_address: Optional[str] = None
    business_scope: Optional[str] = None

    # 场所信息
    property_owner: Optional[str] = None
    lease_start: Optional[str] = None
    lease_end: Optional[str] = None

    @validator('id_card')
    def validate_id_card(cls, v):
        """验证身份证号格式"""
        pattern = r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$'
        if not re.match(pattern, v):
            raise ValueError(f'身份证号格式错误: {v}')
        return v

    @validator('phone')
    def validate_phone(cls, v):
        """验证手机号格式"""
        if v and not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError(f'手机号格式错误: {v}')
        return v


class DataExtractor:
    """数据提取器 - 从OCR结果中提取结构化数据"""

    def __init__(self):
        """初始化提取规则"""
        self.patterns = {
            'phone': r'1[3-9]\d{9}',
            'id_card': r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$',
            'date': r'\d{4}年\d{1,2}月\d{1,2}日',
        }

    def extract_from_id_card(self, ocr_result: Dict) -> Dict:
        """从身份证OCR结果提取数据"""
        data = {}

        # 提取姓名
        if 'name' in ocr_result:
            data['operator_name'] = ocr_result['name']

        # 提取身份证号
        if 'id_card' in ocr_result:
            data['id_card'] = ocr_result['id_card']
            # 从身份证号推断性别
            data['gender'] = self._infer_gender(ocr_result['id_card'])

        # 提取地址（作为经营场所候选）
        if 'address' in ocr_result:
            data['address'] = ocr_result['address']

        return data

    def extract_from_business_license(self, ocr_result: Dict) -> Dict:
        """从营业执照OCR结果提取数据"""
        data = {}

        if 'company_name' in ocr_result:
            data['business_name'] = ocr_result['company_name']

        if 'credit_code' in ocr_result:
            data['credit_code'] = ocr_result['credit_code']

        return data

    def extract_from_lease_contract(self, ocr_result: Dict) -> Dict:
        """从租赁合同OCR结果提取数据"""
        data = {}

        text = ocr_result.get('text', '')

        # 提取房东姓名
        owner_match = re.search(r'出租人[：:]\s*([\u4e00-\u9fa5]{2,4})', text)
        if owner_match:
            data['property_owner'] = owner_match.group(1)

        # 提取租赁期限
        date_matches = re.findall(r'(\d{4})年(\d{1,2})月(\d{1,2})日', text)
        if len(date_matches) >= 2:
            data['lease_start'] = f"{date_matches[0][0]}-{date_matches[0][1]}-{date_matches[0][2]}"
            data['lease_end'] = f"{date_matches[1][0]}-{date_matches[1][1]}-{date_matches[1][2]}"

        return data

    def merge_data(self, *data_sources: Dict) -> OperatorData:
        """合并多个数据源，返回验证后的数据对象"""
        merged = {}
        for source in data_sources:
            merged.update(source)

        return OperatorData(**merged)

    def _infer_gender(self, id_card: str) -> str:
        """从身份证号推断性别"""
        if len(id_card) >= 17:
            gender_code = int(id_card[16])
            return '女' if gender_code % 2 == 0 else '男'
        return '未知'
```

### 3. 数据库管理器 (DatabaseManager)

**功能**: 管理经营户档案数据库

```python
"""
src/database_manager.py
"""
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from contextlib import contextmanager

class DatabaseManager:
    """数据库管理器 - 使用SQLite存储经营户档案"""

    def __init__(self, db_path: str = "data/operators_database.db"):
        """初始化数据库

        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self._init_database()

    @contextmanager
    def _get_connection(self):
        """获取数据库连接（上下文管理器）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 返回字典格式
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _init_database(self):
        """初始化数据库表结构"""
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS operators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    -- 基本信息
                    operator_name TEXT NOT NULL,
                    id_card TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    gender TEXT,
                    nation TEXT,

                    -- 经营信息
                    business_name TEXT,
                    business_address TEXT,
                    business_scope TEXT,

                    -- 场所信息
                    property_owner TEXT,
                    lease_start DATE,
                    lease_end DATE,

                    -- 文件路径
                    id_card_front_path TEXT,
                    id_card_back_path TEXT,
                    business_license_path TEXT,
                    lease_contract_path TEXT,
                    property_cert_path TEXT,

                    -- 归档信息
                    archive_path TEXT,

                    -- 状态
                    status TEXT DEFAULT 'active',

                    -- 元数据
                    metadata TEXT  -- JSON格式的额外信息
                )
            ''')

            # 创建索引
            conn.execute('CREATE INDEX IF NOT EXISTS idx_id_card ON operators(id_card)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_business_name ON operators(business_name)')

    def insert_operator(self, data: Dict) -> int:
        """插入经营户数据

        Args:
            data: 经营户数据字典

        Returns:
            插入记录的ID
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO operators (
                    operator_name, id_card, phone, gender, nation,
                    business_name, business_address, business_scope,
                    property_owner, lease_start, lease_end,
                    id_card_front_path, id_card_back_path,
                    business_license_path, lease_contract_path,
                    property_cert_path, archive_path, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('operator_name'),
                data.get('id_card'),
                data.get('phone'),
                data.get('gender'),
                data.get('nation'),
                data.get('business_name'),
                data.get('business_address'),
                data.get('business_scope'),
                data.get('property_owner'),
                data.get('lease_start'),
                data.get('lease_end'),
                data.get('id_card_front_path'),
                data.get('id_card_back_path'),
                data.get('business_license_path'),
                data.get('lease_contract_path'),
                data.get('property_cert_path'),
                data.get('archive_path'),
                json.dumps(data.get('metadata', {}))
            ))
            return cursor.lastrowid

    def get_operator_by_id_card(self, id_card: str) -> Optional[Dict]:
        """根据身份证号查询经营户

        Args:
            id_card: 身份证号

        Returns:
            经营户数据字典，不存在返回None
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM operators WHERE id_card = ?',
                (id_card,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update_operator(self, id_card: str, updates: Dict):
        """更新经营户数据

        Args:
            id_card: 身份证号
            updates: 要更新的字段字典
        """
        set_clause = ', '.join(f'{k} = ?' for k in updates.keys())
        values = list(updates.values()) + [datetime.now(), id_card]

        with self._get_connection() as conn:
            conn.execute(
                f'UPDATE operators SET {set_clause}, updated_at = ? WHERE id_card = ?',
                values
            )

    def list_operators(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """列出所有经营户

        Args:
            limit: 返回数量限制
            offset: 偏移量

        Returns:
            经营户列表
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM operators
                WHERE status = 'active'
                ORDER BY updated_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))

            return [dict(row) for row in cursor.fetchall()]

    def search_operators(self, keyword: str) -> List[Dict]:
        """搜索经营户

        Args:
            keyword: 搜索关键词（匹配姓名、店名、身份证号）

        Returns:
            匹配的经营户列表
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM operators
                WHERE status = 'active'
                AND (
                    operator_name LIKE ?
                    OR business_name LIKE ?
                    OR id_card LIKE ?
                )
                ORDER BY updated_at DESC
            ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))

            return [dict(row) for row in cursor.fetchall()]
```

### 4. 文件归档器 (FileArchiver)

**功能**: 整理和归档桌面文件

```python
"""
src/file_archiver.py
"""
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class FileArchiver:
    """文件归档器 - 自动分类和归档文档"""

    def __init__(self, base_archive_path: str = "archives"):
        """初始化归档器

        Args:
            base_archive_path: 归档基础路径
        """
        self.base_path = Path(base_archive_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

        # 定义文件类型分类
        self.file_categories = {
            'id_card': ['身份证', 'id_card', 'idcard'],
            'business_license': ['营业执照', 'license', 'yyzz'],
            'lease_contract': ['租赁', '合同', 'lease', 'contract', 'zlht'],
            'property_cert': ['产权', '房产', 'property', 'cqzm'],
            'other': []
        }

    def categorize_file(self, file_path: str) -> str:
        """根据文件名/路径确定文件类别

        Args:
            file_path: 文件路径

        Returns:
            文件类别
        """
        path = Path(file_path)
        filename = path.stem.lower()

        for category, keywords in self.file_categories.items():
            if category == 'other':
                continue
            if any(keyword in filename for keyword in keywords):
                return category

        # 根据扩展名判断
        if path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            return 'id_card'  # 图片默认当作身份证处理

        return 'other'

    def archive_operator_files(
        self,
        operator_name: str,
        id_card: str,
        files: Dict[str, str]
    ) -> str:
        """归档单个经营者的所有文件

        Args:
            operator_name: 经营者姓名
            id_card: 身份证号
            files: 文件字典 {'category': 'file_path'}

        Returns:
            归档目录路径
        """
        # 创建归档目录: archives/姓名_身份证后4位/
        archive_dir = self.base_path / f"{operator_name}_{id_card[-4:]}"
        archive_dir.mkdir(parents=True, exist_ok=True)

        # 创建子目录
        for category in self.file_categories.keys():
            (archive_dir / category).mkdir(exist_ok=True)

        # 复制文件到对应目录
        archived_paths = {}
        for category, file_path in files.items():
            if not file_path:
                continue

            src = Path(file_path)
            if not src.exists():
                continue

            # 目标文件名: 原文件名
            dst = archive_dir / category / src.name

            try:
                shutil.copy2(src, dst)
                archived_paths[f"{category}_path"] = str(dst)
            except Exception as e:
                print(f"复制文件失败: {src} -> {dst}, 错误: {e}")

        return str(archive_dir)

    def clean_desktop(self, desktop_path: str, processed_files: List[str]):
        """清理桌面已处理的文件

        Args:
            desktop_path: 桌面路径
            processed_files: 已处理的文件列表
        """
        desktop = Path(desktop_path)

        for file_path in processed_files:
            file = Path(file_path)

            # 只删除桌面上的文件
            if file.parent != desktop:
                continue

            try:
                if file.is_file():
                    # 移到回收站而不是直接删除
                    trash_dir = desktop / "回收站"
                    trash_dir.mkdir(exist_ok=True)

                    # 重命名避免冲突
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_name = f"{file.stem}_{timestamp}{file.suffix}"
                    shutil.move(str(file), trash_dir / new_name)

            except Exception as e:
                print(f"清理文件失败: {file}, 错误: {e}")
```

### 5. 申请书生成器 (ApplicationGenerator)

**功能**: 复用v3.0的Jinja2模板生成能力

```python
"""
src/application_generator.py
"""
from pathlib import Path
from typing import Dict, Optional
from docxtpl import DocxTemplate
import json

class ApplicationGenerator:
    """申请书生成器 - 复用v3.0模板系统"""

    def __init__(self, template_path: str = "templates"):
        """初始化生成器

        Args:
            template_path: 模板目录路径
        """
        self.template_path = Path(template_path)

    def generate_application(
        self,
        operator_data: Dict,
        template_name: str = "个体工商户开业登记申请书.docx",
        output_dir: str = "output"
    ) -> str:
        """生成申请书

        Args:
            operator_data: 经营户数据
            template_name: 模板文件名
            output_dir: 输出目录

        Returns:
            生成文件路径
        """
        # 加载模板
        template_file = self.template_path / template_name
        if not template_file.exists():
            raise FileNotFoundError(f"模板文件不存在: {template_file}")

        doc = DocxTemplate(str(template_file))

        # 准备上下文数据
        context = self._prepare_context(operator_data)

        # 渲染模板
        doc.render(context)

        # 保存文件
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        business_name = operator_data.get('business_name', '未命名')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_path / f"{business_name}_申请书_{timestamp}.docx"

        doc.save(str(output_file))

        return str(output_file)

    def _prepare_context(self, operator_data: Dict) -> Dict:
        """准备模板渲染上下文

        Args:
            operator_data: 原始数据

        Returns:
            模板上下文字典
        """
        # 读取全局配置
        config = self._load_global_config()

        # 合并数据
        context = {
            **config.get('constants', {}),
            **config.get('defaults', {}),
            **operator_data
        }

        # 字段映射
        field_mappings = config.get('field_mappings', {})

        return {
            key: context.get(value, '')
            for key, value in field_mappings.items()
        }

    def _load_global_config(self) -> Dict:
        """加载全局配置"""
        config_file = Path("config.json")
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
```

---

## 数据流程

### 完整数据流图

```
┌─────────────────────────────────────────────────────────────────┐
│                        数据流程图                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 文件监控                                                     │
│     ├── 监听桌面文件夹                                             │
│     └── 检测新文件                                               │
│         ↓                                                       │
│  2. 文件分类                                                     │
│     ├── 身份证 → id_card                                        │
│     ├── 营业执照 → business_license                             │
│     ├── 租赁合同 → lease_contract                               │
│     └── 产权证明 → property_cert                                │
│         ↓                                                       │
│  3. OCR识别                                                     │
│     ├── 身份证 → 姓名+身份证号+性别+地址                           │
│     ├── 营业执照 → 店名+信用代码                                   │
│     └── 合同 → 房东+租赁期限                                       │
│         ↓                                                       │
│  4. 数据提取                                                     │
│     ├── 提取结构化字段                                            │
│     ├── 数据验证                                                 │
│     └── 数据合并                                                 │
│         ↓                                                       │
│  5. 数据入库                                                     │
│     ├── 查询是否已存在                                            │
│     ├── 插入新记录                                                │
│     └── 返回记录ID                                               │
│         ↓                                                       │
│  6. 文件归档                                                     │
│     ├── 创建归档目录                                              │
│     ├── 复制文件到归档目录                                         │
│     └── 清理桌面                                                 │
│         ↓                                                       │
│  7. 申请书生成                                                   │
│     ├── 从数据库读取数据                                          │
│     ├── 加载Word模板                                              │
│     └── 渲染并保存                                               │
│         ↓                                                       │
│  8. UI表单补充                                                   │
│     ├── 显示缺失字段                                              │
│     ├── 用户输入补充                                              │
│     └── 更新数据库                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 工作流状态定义

```python
from typing import TypedDict, Literal
from langgraph.graph.message import add_messages

class WorkflowState(TypedDict):
    """工作流状态定义"""
    # 消息列表
    messages: list

    # 当前步骤
    current_step: Literal[
        'waiting',
        'file_detected',
        'classifying',
        'ocr_processing',
        'extracting',
        'saving_to_db',
        'archiving',
        'generating',
        'completed',
        'error'
    ]

    # 文件信息
    detected_files: list[str]
    file_categories: dict[str, str]

    # OCR结果
    ocr_results: dict[str, dict]

    # 提取的数据
    extracted_data: dict

    # 数据库操作
    operator_id: int | None
    database_status: str

    # 归档信息
    archive_path: str | None

    # 生成结果
    generated_document: str | None

    # 错误处理
    error_message: str | None
    retry_count: int
```

---

## 工作流设计

### LangGraph工作流定义

```python
"""
src/workflow.py
"""
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import Any

class MarketSupervisionWorkflow:
    """市场监管申请处理工作流"""

    def __init__(self):
        """初始化工作流"""
        # 初始化各个组件
        self.ocr_engine = OCREngine()
        self.data_extractor = DataExtractor()
        self.db_manager = DatabaseManager()
        self.file_archiver = FileArchiver()
        self.doc_generator = ApplicationGenerator()

        # 构建工作流图
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """构建工作流图

        Returns:
            编译后的工作流
        """
        # 创建状态图
        workflow = StateGraph(WorkflowState)

        # 添加节点
        workflow.add_node("classify_files", self._classify_files_node)
        workflow.add_node("ocr_process", self._ocr_process_node)
        workflow.add_node("extract_data", self._extract_data_node)
        workflow.add_node("save_to_db", self._save_to_db_node)
        workflow.add_node("archive_files", self._archive_files_node)
        workflow.add_node("generate_document", self._generate_document_node)
        workflow.add_node("handle_error", self._handle_error_node)

        # 设置入口点
        workflow.set_entry_point("classify_files")

        # 添加边
        workflow.add_edge("classify_files", "ocr_process")
        workflow.add_edge("ocr_process", "extract_data")
        workflow.add_edge("extract_data", "save_to_db")

        # 条件边
        workflow.add_conditional_edges(
            "save_to_db",
            self._should_generate_document,
            {
                "generate": "generate_document",
                "archive": "archive_files",
                "error": "handle_error"
            }
        )

        workflow.add_edge("generate_document", "archive_files")
        workflow.add_edge("archive_files", END)
        workflow.add_edge("handle_error", END)

        return workflow.compile()

    def _classify_files_node(self, state: WorkflowState) -> WorkflowState:
        """文件分类节点"""
        files = state['detected_files']
        categories = {}

        archiver = FileArchiver()
        for file_path in files:
            category = archiver.categorize_file(file_path)
            categories[file_path] = category

        state['file_categories'] = categories
        state['current_step'] = 'classifying'
        state['messages'].append(f"已分类 {len(files)} 个文件")

        return state

    def _ocr_process_node(self, state: WorkflowState) -> WorkflowState:
        """OCR处理节点"""
        ocr_results = {}

        for file_path, category in state['file_categories'].items():
            try:
                if category == 'id_card':
                    result = self.ocr_engine.recognize_id_card(file_path)
                elif category == 'business_license':
                    result = self.ocr_engine.recognize_business_license(file_path)
                else:
                    result = self.ocr_engine.recognize_image(file_path)

                ocr_results[file_path] = result

            except Exception as e:
                state['messages'].append(f"OCR识别失败 {file_path}: {str(e)}")
                ocr_results[file_path] = {}

        state['ocr_results'] = ocr_results
        state['current_step'] = 'ocr_processing'

        return state

    def _extract_data_node(self, state: WorkflowState) -> WorkflowState:
        """数据提取节点"""
        extracted = {}

        for file_path, ocr_result in state['ocr_results'].items():
            category = state['file_categories'][file_path]

            try:
                if category == 'id_card':
                    data = self.data_extractor.extract_from_id_card(ocr_result)
                elif category == 'business_license':
                    data = self.data_extractor.extract_from_business_license(ocr_result)
                elif category == 'lease_contract':
                    data = self.data_extractor.extract_from_lease_contract(ocr_result)
                else:
                    data = {}

                extracted.update(data)

            except Exception as e:
                state['messages'].append(f"数据提取失败 {file_path}: {str(e)}")

        # 验证并创建数据对象
        try:
            operator_data = self.data_extractor.merge_data(extracted)
            state['extracted_data'] = operator_data.dict()
            state['messages'].append("数据提取成功")
        except Exception as e:
            state['error_message'] = f"数据验证失败: {str(e)}"
            state['current_step'] = 'error'

        state['current_step'] = 'extracting'

        return state

    def _save_to_db_node(self, state: WorkflowState) -> WorkflowState:
        """保存到数据库节点"""
        try:
            operator_id = self.db_manager.insert_operator(
                state['extracted_data']
            )
            state['operator_id'] = operator_id
            state['database_status'] = 'saved'
            state['messages'].append(f"已保存到数据库，ID: {operator_id}")
        except Exception as e:
            state['error_message'] = f"数据库保存失败: {str(e)}"
            state['database_status'] = 'error'

        state['current_step'] = 'saving_to_db'

        return state

    def _archive_files_node(self, state: WorkflowState) -> WorkflowState:
        """文件归档节点"""
        try:
            archive_path = self.file_archiver.archive_operator_files(
                operator_name=state['extracted_data'].get('operator_name', '未知'),
                id_card=state['extracted_data'].get('id_card', ''),
                files=state['file_categories']
            )
            state['archive_path'] = archive_path
            state['messages'].append(f"文件已归档到: {archive_path}")
        except Exception as e:
            state['messages'].append(f"归档失败: {str(e)}")

        state['current_step'] = 'archiving'

        return state

    def _generate_document_node(self, state: WorkflowState) -> WorkflowState:
        """生成申请书节点"""
        try:
            doc_path = self.doc_generator.generate_application(
                operator_data=state['extracted_data']
            )
            state['generated_document'] = doc_path
            state['messages'].append(f"申请书已生成: {doc_path}")
        except Exception as e:
            state['messages'].append(f"生成失败: {str(e)}")

        state['current_step'] = 'generating'

        return state

    def _handle_error_node(self, state: WorkflowState) -> WorkflowState:
        """错误处理节点"""
        state['messages'].append(f"处理出错: {state['error_message']}")
        state['current_step'] = 'error'

        return state

    def _should_generate_document(self, state: WorkflowState) -> str:
        """决定是否生成文档"""
        if state.get('error_message'):
            return 'error'

        # 如果有经营户名称，就生成申请书
        if state['extracted_data'].get('business_name'):
            return 'generate'

        return 'archive'

    def process(self, files: list[str]) -> WorkflowState:
        """处理一批文件

        Args:
            files: 文件路径列表

        Returns:
            最终状态
        """
        initial_state: WorkflowState = {
            'messages': [],
            'current_step': 'waiting',
            'detected_files': files,
            'file_categories': {},
            'ocr_results': {},
            'extracted_data': {},
            'operator_id': None,
            'database_status': '',
            'archive_path': None,
            'generated_document': None,
            'error_message': None,
            'retry_count': 0
        }

        # 执行工作流
        result = self.workflow.invoke(initial_state)

        return result
```

---

## 错误处理

### 错误分类和处理策略

| 错误类型 | 处理策略 | 重试次数 | 降级方案 |
|---------|---------|---------|---------|
| **文件读取失败** | 跳过该文件 | 0 | 记录日志，继续处理 |
| **OCR识别失败** | 重试 | 3 | 使用手动输入 |
| **数据验证失败** | 人工校对 | 0 | 通过UI表单修正 |
| **数据库冲突** | 更新现有记录 | 0 | 合并数据 |
| **模板缺失** | 使用默认模板 | 0 | 生成简化版文档 |
| **归档失败** | 保留原位置 | 0 | 手动归档 |

### 错误恢复机制

```python
class ErrorHandler:
    """错误处理器"""

    def __init__(self):
        self.max_retries = {
            'ocr': 3,
            'database': 1,
            'file_operation': 0
        }

    def handle_ocr_error(self, file_path: str, error: Exception, retry_count: int) -> dict:
        """处理OCR错误"""
        if retry_count >= self.max_retries['ocr']:
            return {
                'action': 'skip',
                'message': f"OCR识别失败，已达最大重试次数: {file_path}",
                'fallback': 'manual_input'
            }

        return {
            'action': 'retry',
            'delay': 2 ** retry_count  # 指数退避
        }

    def handle_validation_error(self, data: dict, errors: list) -> dict:
        """处理数据验证错误"""
        return {
            'action': 'require_manual_fix',
            'fields': errors,
            'ui_prompt': True
        }
```

---

## 实施计划

### 开发阶段

| 阶段 | 任务 | 预计工作量 | 优先级 |
|------|------|-----------|-------|
| **第一阶段** | 核心功能开发 | | |
| 1.1 | 搭建项目结构 | 2小时 | P0 |
| 1.2 | 实现OCR引擎 | 4小时 | P0 |
| 1.3 | 实现数据提取器 | 3小时 | P0 |
| 1.4 | 实现数据库管理器 | 2小时 | P0 |
| 1.5 | 实现文件归档器 | 2小时 | P0 |
| **第二阶段** | 工作流集成 | | |
| 2.1 | 设计LangGraph工作流 | 3小时 | P0 |
| 2.2 | 实现各处理节点 | 4小时 | P0 |
| 2.3 | 错误处理和重试 | 2小时 | P1 |
| **第三阶段** | UI和优化 | | |
| 3.1 | Streamlit界面 | 4小时 | P1 |
| 3.2 | 性能优化 | 2小时 | P2 |
| 3.3 | 测试和调试 | 4小时 | P0 |
| **第四阶段** | 文档和部署 | | |
| 4.1 | 编写使用文档 | 2小时 | P1 |
| 4.2 | 打包和分发 | 2小时 | P2 |

### 里程碑

- **里程碑1**: 核心功能可用（第1阶段结束）
- **里程碑2**: 工作流跑通（第2阶段结束）
- **里程碑3**: UI界面完成（第3阶段结束）
- **里程碑4**: 发布v4.0（第4阶段结束）

---

## 附录

### A. 项目目录结构

```
market_supervision_agent/
├── src/                           # 源代码
│   ├── __init__.py
│   ├── ocr_engine.py             # OCR引擎
│   ├── data_extractor.py         # 数据提取器
│   ├── database_manager.py       # 数据库管理
│   ├── file_archiver.py          # 文件归档器
│   ├── application_generator.py  # 申请书生成器
│   └── workflow.py               # LangGraph工作流
├── ui/                           # 用户界面
│   ├── __init__.py
│   └── app.py                    # Streamlit应用
├── data/                         # 数据目录
│   ├── operators_database.db     # SQLite数据库
│   └── sample_customers.json     # 示例数据
├── templates/                    # Word模板
│   └── 个体工商户开业登记申请书.docx
├── config/                       # 配置文件
│   ├── ocr_config.yaml           # OCR配置
│   └── database_schema.yaml      # 数据库结构
├── archives/                     # 归档目录
│   └── 张三_1234/
│       ├── id_card/
│       ├── business_license/
│       └── lease_contract/
├── output/                       # 生成文档输出
├── tests/                        # 测试
│   ├── test_ocr.py
│   ├── test_workflow.py
│   └── test_data/
├── requirements.txt              # 依赖
├── README.md                     # 说明文档
└── TECH_DESIGN_V4.md             # 本文档
```

### B. 配置文件示例

**config/ocr_config.yaml**
```yaml
# OCR配置
paddleocr:
  use_gpu: false
  lang: ch
  use_angle_cls: true

# 文件分类规则
file_classification:
  id_card:
    keywords: ["身份证", "id_card", "idcard"]
    extensions: [".jpg", ".jpeg", ".png"]
  business_license:
    keywords: ["营业执照", "license"]
    extensions: [".jpg", ".jpeg", ".png", ".pdf"]
  lease_contract:
    keywords: ["租赁", "合同", "lease"]
    extensions: [".pdf", ".jpg", ".png"]

# 提取规则
extraction:
  id_card:
    - name
    - id_card
    - gender
    - address
  business_license:
    - company_name
    - credit_code
  lease_contract:
    - property_owner
    - lease_start
    - lease_end
```

### C. 数据库ER图

```
┌─────────────────────────────────────────┐
│             operators                   │
├─────────────────────────────────────────┤
│ PK │ id                INTEGER          │
│    │ created_at        TIMESTAMP       │
│    │ updated_at        TIMESTAMP       │
│    │                                   │
│    │ operator_name     TEXT     NOT NULL│
│    │ id_card           TEXT     UNIQUE │
│    │ phone             TEXT            │
│    │ gender            TEXT            │
│    │ business_name     TEXT            │
│    │ business_address  TEXT            │
│    │ business_scope   TEXT            │
│    │ property_owner   TEXT            │
│    │ lease_start      DATE            │
│    │ lease_end        DATE            │
│    │                                   │
│    │ id_card_front_path    TEXT       │
│    │ id_card_back_path     TEXT       │
│    │ business_license_path TEXT       │
│    │ lease_contract_path   TEXT       │
│    │ archive_path          TEXT       │
│    │ metadata               JSON      │
└─────────────────────────────────────────┘
```

---

**文档结束**

> 本文档基于开源项目调研结果编写，为市场监管智能体 v4.0 的开发提供完整的技术指导。
