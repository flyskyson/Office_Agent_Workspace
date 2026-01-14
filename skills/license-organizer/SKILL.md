# 证照整理技能 (License Organizer)

**描述**: 智能证照文件整理工具，自动识别营业执照、身份证、许可证等文件类型，按日期/类别/关键词分类归档，自动重命名规范文件名。当用户需要"整理证照"、"归类文件"、"归档证件"、"管理证照材料"时触发。适用于日常证照管理、项目归档、文件整理。不支持破坏性操作（删除或覆盖原文件）。

---

## 概述

本技能自动化整理各类证照文件，核心功能：
1. **智能识别**: OCR识别文件类型（营业执照/身份证/许可证等）
2. **自动分类**: 按文件类型、日期、关键词分类
3. **规范命名**: 统一文件命名格式
4. **安全归档**: 复制而非移动，保护原文件

**关键优势**：
- 零手动分类，AI自动识别
- 统一命名规范，便于查找
- 安全归档，不破坏原文件
- 支持批量处理，高效省时

---

## 前置条件

### 必需文件
```
01_Active_Projects/file_organizer/
├── file_organizer.py           # 核心整理器
├── config.json                 # 配置文件
└── improved_identify.py        # 文件类型识别
```

### 环境依赖
```bash
pip install pillow paddleocr python-dateutil
```

### 支持的文件类型
- **图片**: JPG, PNG, JPEG
- **PDF**: 扫描件或电子版
- **其他**: 按扩展名分类

---

## 执行步骤

### 步骤 1: 确定整理范围

**询问用户**：
```
要整理哪个目录？
A. 整个 Downloads 文件夹
B. 特定项目文件夹
C. 指定文件列表
```

**默认路径建议**：
- 下载文件夹: `C:\Users\flyskyson\Downloads\`
- 桌面文件: `C:\Users\flyskyson\Desktop\`
- 自定义: 让用户指定

---

### 步骤 2: 扫描文件

**执行命令**：
```bash
cd 01_Active_Projects/file_organizer
python file_organizer.py scan <目标目录>
```

**扫描结果示例**：
```
发现 23 个待整理文件：
├── 图片文件: 15 个
├── PDF文件: 6 个
└── 其他文件: 2 个
```

---

### 步骤 3: 智能识别

**识别文件类型**：
```python
from improved_identify import FileTypeIdentifier

identifier = FileTypeIdentifier()

# 识别单个文件
file_type = identifier.identify("license.jpg")
# 输出: {"type": "营业执照", "confidence": 0.95}

# 识别批量
results = identifier.batch_identify(file_list)
```

**识别类别**：
| 文件类型 | 特征关键词 | 目标目录 |
|---------|-----------|---------|
| 营业执照 | "营业执照"、"统一社会信用代码" | `营业执照/` |
| 身份证 | "身份证"、"公民身份号码" | `身份证/` |
| 许可证 | "许可证"、"备案" | `许可证/` |
| 食品证 | "食品经营"、"许可证" | `食品经营许可证/` |
| 其他证照 | 其他关键词 | `其他证照/` |

---

### 步骤 4: 自动分类

**分类规则**：
```python
分类逻辑 = {
    "按类型": 文件类型（营业执照/身份证/许可证）,
    "按日期": 文件创建日期（YYYY-MM）,
    "按关键词": 经营者姓名/企业名称
}
```

**目标目录结构**：
```
organized_files/
├── 营业执照/
│   ├── 2026-01/
│   │   ├── 张三_个体工商户_20260113.jpg
│   │   └── XX公司_企业法人_20260112.jpg
│   └── 2025-12/
│       └── ...
├── 身份证/
│   ├── 正面/
│   └── 反面/
├── 食品经营许可证/
└── 其他证照/
```

---

### 步骤 5: 规范重命名

**命名规则**：
```
{类别}_{关键信息}_{日期}.{ext}
```

**示例**：
```
原始文件: IMG_20250113_123456.jpg
重命名后: 营业执照_张三_20260113.jpg

原始文件: 扫描件1.pdf
重命名后: 身份证_李四_正面_20260113.pdf
```

**重命名代码**：
```python
import re
from datetime import datetime

def generate_new_name(file_info):
    """生成规范文件名"""
    category = file_info['type']  # 营业执照
    keyword = file_info['name']   # 张三
    date = datetime.now().strftime("%Y%m%d")
    ext = file_info['extension']  # jpg

    return f"{category}_{keyword}_{date}.{ext}"
```

---

### 步骤 6: 安全归档

**归档策略**：**复制**而非移动，确保原文件安全

```python
import shutil
from pathlib import Path

def organize_file(source_path, target_dir):
    """安全归档文件"""
    source = Path(source_path)
    target = Path(target_dir) / source.name

    # 创建目标目录
    target.parent.mkdir(parents=True, exist_ok=True)

    # 复制文件（不删除原文件）
    shutil.copy2(source, target)

    print(f"✅ 已归档: {source} -> {target}")
```

**归档结果**：
```
归档完成！
├── 原文件保留: C:\Users\flyskyson\Downloads\
└── 整理副本: 01_Active_Projects/file_organizer/organized_files/
```

---

## 使用示例

### 示例 1: 整理下载文件夹

```
你: 帮我整理一下下载文件夹里的证照

我: 好的，开始扫描 C:\Users\flyskyson\Downloads\

    发现 18 个待整理文件：
    ├── 营业执照类: 8 个
    ├── 身份证类: 4 个
    └── 其他: 6 个

    正在识别和分类...
    [████████░░] 80% 14/18

    ✅ 整理完成！

    归档位置: 01_Active_Projects/file_organizer/organized_files/

    要查看整理结果吗？
```

---

### 示例 2: 处理特定类型

```
你: 只整理营业执照文件

我: 好的，只处理营业执照类型

    扫描中...
    找到 5 个营业执照文件：
    1. IMG_001.jpg → 张三_个体工商户
    2. 扫描.pdf → 李四_食品经营
    ...

    正在归档到 organized_files/营业执照/
    ✅ 完成！
```

---

### 示例 3: 按日期归档

```
你: 按月份整理这些证照

我: 好的，按月份分组归档

    organized_files/
    ├── 营业执照/
    │   ├── 2026-01/ (5个文件)
    │   ├── 2025-12/ (3个文件)
    │   └── 2025-11/ (2个文件)
    ...

    ✅ 已按月份归档！
```

---

## 配置说明

### 编辑配置文件

编辑 [config.json](../../01_Active_Projects/file_organizer/config.json)：

```json
{
  "target_directory": "organized_files",
  "organize_by": ["type", "date", "keyword"],
  "naming_rule": "{type}_{name}_{date}.{ext}",
  "copy_mode": true,
  "supported_formats": [".jpg", ".png", ".jpeg", ".pdf"],
  "ocr_confidence_threshold": 0.8
}
```

### 自定义分类规则

```python
# 在 file_organizer.py 中添加
custom_rules = {
    " urgent": "紧急/",
    " reviewed": "已审核/",
    " pending": "待处理/"
}
```

---

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `FileNotFoundError` | 源文件不存在 | 检查文件路径是否正确 |
| `PermissionError` | 无文件访问权限 | 检查文件是否被占用 |
| `OCRError` | OCR识别失败 | 检查图片清晰度或使用备用方法 |
| `DiskFullError` | 磁盘空间不足 | 清理磁盘空间或更改目标目录 |

### 跳过机制

```python
# 遇到错误时跳过，继续处理其他文件
try:
    organize_file(file)
except Exception as e:
    print(f"⚠️ 跳过文件 {file}: {e}")
    continue
```

---

## 局限说明

**本技能无法处理**：
- ❌ 加密或密码保护的文件
- ❌ 损坏或无法打开的文件
- ❌ 手写文字（OCR准确率低）
- ❌ 非证照类文件（需自定义规则）

**需要人工确认**：
- ⚠️ OCR识别置信度 < 80% 时
- ⚺ 文件名包含特殊字符
- ⚺ 同名文件冲突

---

## 安全机制

### 文件保护
- ✅ **复制模式**: 默认复制，不删除原文件
- ✅ **冲突处理**: 同名文件自动添加序号
- ✅ **权限检查**: 操作前验证读写权限

### 回滚支持
```bash
# 查看操作日志
cat file_organizer.log

# 手动恢复（如需要）
rm -rf organized_files/
```

---

## 扩展功能

### 添加新识别类型

```python
# 在 improved_identify.py 中添加
def identify_custom(self, file_path):
    """自定义识别逻辑"""
    if "关键词" in ocr_text:
        return {"type": "自定义类型", "confidence": 0.9}
```

### 集成其他工具

```python
# 整理后自动上传到云存储
def upload_to_cloud(file_path):
    """上传到云盘"""
    # 实现云存储上传逻辑
    pass
```

---

## 相关文件

- **核心代码**: [01_Active_Projects/file_organizer/file_organizer.py](../../01_Active_Projects/file_organizer/file_organizer.py)
- **识别模块**: [01_Active_Projects/file_organizer/improved_identify.py](../../01_Active_Projects/file_organizer/improved_identify.py)
- **配置文件**: [01_Active_Projects/file_organizer/config.json](../../01_Active_Projects/file_organizer/config.json)
- **输出目录**: [01_Active_Projects/file_organizer/organized_files/](../../01_Active_Projects/file_organizer/organized_files/)

---

## 版本历史

- **v1.0** (2026-01-13): 初始版本，支持智能识别和分类归档

---

**技能触发关键词**: `整理证照`、`归类文件`、`归档证件`、`管理证照`、`文件分类`、`批量整理`
