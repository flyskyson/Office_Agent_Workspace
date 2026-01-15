# 编码最佳实践指南

## 问题背景

中文文件名和中文内容在脚本开发中容易引发各种问题：
- **文件系统兼容性**: Windows/Linux/macOS 对中文文件名支持不一致
- **编码问题**: GBK vs UTF-8 编码冲突
- **URL 编码**: Web 应用上传文件时的编码转换
- **日志输出**: 控制台乱码

## 已修复的问题

### ✅ 1. Flask 文件上传 (ui/flask_app.py)

**问题**: `secure_filename()` 会删除中文字符

```python
# ❌ 修复前
filename = secure_filename(file.filename)  # "经营者身份证.jpg" → ".jpg"

# ✅ 修复后
ext = os.path.splitext(file.filename)[1].lower()
temp_filename = f"temp_{int(datetime.now().timestamp() * 1000)}{ext}"
```

### ✅ 2. 文件归档目录 (src/file_archiver.py)

**问题**: 使用中文姓名作为目录名

```python
# ❌ 修复前
dir_name = f"{operator_name}_{id_card[-4:]}"  # "黎林_1018"

# ✅ 修复后
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
dir_hash = hashlib.md5(f"{operator_name}_{id_card}".encode('utf-8')).hexdigest()[:8]
dir_name = f"operator_{id_card[-4:]}_{timestamp}_{dir_hash}"

# 同时创建 .metadata.json 保存原始信息
metadata = {
    "operator_name": operator_name,
    "id_card": id_card,
    "created_at": datetime.now().isoformat()
}
```

### ✅ 3. 归档文件重命名 (src/file_archiver.py)

**问题**: 使用中文姓名 + 原文件名

```python
# ❌ 修复前
target_name = f"{operator_name}_{src.name}"  # "黎林_身份证.jpg"

# ✅ 修复后
unique_id = str(uuid.uuid4())[:8]
target_name = f"operator_{category}_{unique_id}{ext}"
```

### ✅ 4. 申请书生成 (src/application_generator.py)

**问题**: 使用中文店名作为文件名

```python
# ❌ 修复前
output_file = output_path / f"{business_name}_申请书_{timestamp}.docx"

# ✅ 修复后
id_suffix = id_card[-4:] if id_card else '0000'
safe_filename = f"application_{id_suffix}_{timestamp}.docx"

# 创建元数据文件保存原始信息
metadata = {
    "original_filename": f"{business_name}_申请书_{timestamp}.docx",
    "operator_name": operator_name,
    "business_name": business_name
}
```

## 最佳实践

### 1. 文件命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 临时文件 | `temp_时间戳.扩展名` | `temp_1768229730295.jpg` |
| 归档目录 | `operator_身份证后4位_时间戳_hash` | `operator_1018_20260112_224500_a3b4c5d6` |
| 归档文件 | `operator_分类_UUID.扩展名` | `operator_id_card_a3b4c5d6.jpg` |
| 申请书 | `application_身份证后4位_时间戳.docx` | `application_1018_20260112_224500.docx` |

### 2. 元数据管理

使用 `.metadata.json` 文件保存原始信息：

```json
{
  "operator_name": "黎林",
  "id_card": "450305197801041018",
  "business_name": "某某小吃店",
  "created_at": "2026-01-12T22:45:00",
  "original_filename": "黎林_申请书_20260112.docx"
}
```

### 3. 编码配置

#### Python 脚本
```python
import sys
import io

# 强制 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 文件读写
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```

#### 数据库
```python
conn = sqlite3.connect('database.db')
conn.execute("PRAGMA encoding = 'UTF-8'")
```

#### JSON
```python
import json

# 保存（确保中文正常显示）
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### 4. 路径处理

```python
from pathlib import Path

# ✅ 推荐
archive_dir = Path("archives") / "operators" / f"{operator_id}"
file_path = archive_dir / "file.jpg"

# ❌ 避免
archive_dir = "archives/operators/" + operator_name  # 字符串拼接
```

### 5. URL 和 Web 处理

```python
from urllib.parse import quote, unquote

# URL 编码（用于文件下载）
filename = "申请书.docx"
encoded_filename = quote(filename.encode('utf-8'))

# HTTP 响应头
response.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{encoded_filename}"
```

## 检查清单

开发新功能时，请检查：

- [ ] 文件名是否包含中文？ → 使用 UUID/时间戳 + 元数据
- [ ] 路径拼接是否使用 `pathlib.Path`？
- [ ] 文件读写是否指定 `encoding='utf-8'`？
- [ ] JSON 是否使用 `ensure_ascii=False`？
- [ ] 是否创建 `.metadata.json` 保存原始信息？
- [ ] 日志输出中是否正确显示中文？

## 测试验证

```bash
# 测试中文文件名处理
python -c "
from pathlib import Path
import uuid

# 生成安全文件名
ext = '.jpg'
safe_name = f'temp_{uuid.uuid4().hex[:8]}{ext}'
print(f'安全文件名: {safe_name}')
"

# 测试编码
python -c "
import json
data = {'name': '张三'}
print(json.dumps(data, ensure_ascii=False))
"
```

## 参考资源

- [Python Unicode HOWTO](https://docs.python.org/3/howto/unicode.html)
- [PEP 597 - 增加编码可选功能](https://peps.python.org/pep-0597/)
- [Filesystem encoding in Python](https://docs.python.org/3/library/os.html#os.fsencode)
