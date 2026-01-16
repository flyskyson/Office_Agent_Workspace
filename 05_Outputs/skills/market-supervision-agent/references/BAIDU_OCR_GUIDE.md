# 百度 OCR API 集成指南

## 概述

市场监管智能体 v4.0 现已集成百度 OCR API 支持。当 PaddleOCR（本地 OCR）不可用时，系统可以自动切换到百度 OCR API（云端 OCR）。

## 对比：PaddleOCR vs 百度 OCR

| 特性 | PaddleOCR | 百度 OCR API |
|------|-----------|-------------|
| 安装难度 | 需要 Python 3.9-3.11 | 任何 Python 版本 |
| 识别准确率 | 中等 | 高（云端服务） |
| 识别速度 | 受本地硬件影响 | 网络延迟影响 |
| 使用成本 | 完全免费 | 500次/天（免费额度） |
| 网络要求 | 无需联网 | 需要联网 |
| 配置复杂度 | 简单 | 需要注册账号 |

## 快速开始

### 1. 安装依赖

```bash
pip install baidu-aip
```

### 2. 获取百度 OCR 凭证

1. 访问 [百度智能云](https://cloud.baidu.com/)
2. 注册/登录账号
3. 进入管理控制台 -> 人工智能 -> 文字识别
4. 创建应用，获取：
   - AppID
   - API Key
   - Secret Key

### 3. 配置凭证

编辑 `config/baidu_ocr.yaml`：

```yaml
app_id: "your_app_id_here"
api_key: "your_api_key_here"
secret_key: "your_secret_key_here"
```

### 4. 使用方式

#### 方式一：自动选择（推荐）

```python
from src import create_ocr_engine

# 自动选择可用的 OCR 引擎（优先百度 OCR）
ocr = create_ocr_engine()

# 识别身份证
result = ocr.recognize_id_card("id_card.jpg")
print(result["name"], result["id_card"])
```

#### 方式二：强制使用百度 OCR

```python
from src import OCREngineAdapter

# 指定使用百度 OCR
ocr = OCREngineAdapter(engine="baidu")

result = ocr.recognize_business_license("license.jpg")
```

#### 方式三：直接使用百度 OCR 引擎

```python
from src.baidu_ocr_engine import BaiduOCREngine

engine = BaiduOCREngine(
    app_id="your_app_id",
    api_key="your_api_key",
    secret_key="your_secret_key"
)

result = engine.recognize_id_card("id_card.jpg")
```

## API 参考

### OCREngineAdapter

```python
class OCREngineAdapter:
    def __init__(
        self,
        engine: str = "auto",        # "auto", "paddle", "baidu"
        baidu_config: str = "config/baidu_ocr.yaml",
        use_angle_cls: bool = True,
        lang: str = "ch"
    )
```

**方法：**

- `recognize_id_card(image_path)` - 识别身份证
  - 返回：`{"name", "id_card", "gender", "nation", "address"}`

- `recognize_business_license(image_path)` - 识别营业执照
  - 返回：`{"company_name", "credit_code", "legal_person", "address", "business_scope"}`

- `recognize_contract(image_path)` - 识别租赁合同
  - 返回：`{"text", "landlord", "lease_start", "lease_end"}`

- `recognize_image(image_path)` - 通用文字识别
  - 返回：`{"text", "words_result"}`

### BaiduOCREngine

```python
class BaiduOCREngine:
    def __init__(
        self,
        app_id: str = "",
        api_key: str = "",
        secret_key: str = "",
        config_file: str = "config/baidu_ocr.yaml"
    )
```

方法同 `OCREngineAdapter`，但只使用百度 OCR API。

## 免费额度说明

百度 OCR API 免费额度（每个应用）：

| API | 免费额度 |
|-----|---------|
| 通用文字识别 | 500次/天 |
| 通用文字识别（高精度） | 50次/天 |
| 身份证识别 | 500次/天 |
| 营业执照识别 | 500次/天 |

## 故障排除

### 问题：RuntimeError: 百度 OCR 凭证缺失！

**解决方案：**
1. 确认已注册百度智能云账号并创建 OCR 应用
2. 确认 `config/baidu_ocr.yaml` 中的凭证已正确填写
3. 检查 YAML 文件格式是否正确（注意缩进）

### 问题：No matching distribution found for paddlepaddle

**解决方案：**
使用百度 OCR API 替代，无需安装 PaddlePaddle：

```python
# 强制使用百度 OCR
ocr = OCREngineAdapter(engine="baidu")
```

### 问题：API 错误 18 - Open api qps request limit reached

**解决方案：**
已超过 QPS 限制，请：
1. 降低并发请求频率
2. 升级到付费版本
3. 使用多个应用轮询

## 工作流集成

在工作流中使用百度 OCR：

```python
from src.workflow import process_files

config = {
    "ocr_engine": "baidu",           # 指定使用百度 OCR
    "baidu_config": "config/baidu_ocr.yaml"
}

result = process_files(
    ["id_card.jpg", "license.pdf"],
    config=config
)
```

## 安全提示

1. **不要提交凭证到版本控制系统**
   ```bash
   # 将配置文件添加到 .gitignore
   echo "config/baidu_ocr.yaml" >> .gitignore
   ```

2. **为不同环境使用不同的应用**
   - 开发环境：使用测试应用
   - 生产环境：使用正式应用

3. **定期轮换 API Key**
   - 建议每 90 天更换一次

## 迁移指南

### 从 PaddleOCR 迁移到百度 OCR

**之前（PaddleOCR）：**

```python
from src import OCREngine

ocr = OCREngine()
result = ocr.recognize_id_card("id.jpg")
```

**之后（百度 OCR）：**

```python
from src import OCREngineAdapter

# 方式一：自动选择（推荐）
ocr = OCREngineAdapter()
result = ocr.recognize_id_card("id.jpg")

# 方式二：指定使用百度 OCR
ocr = OCREngineAdapter(engine="baidu")
result = ocr.recognize_id_card("id.jpg")
```

API 完全兼容，无需修改业务代码！
