# 市场监管智能体 - Market Supervision Agent

自动化处理市场监管业务，包括企业年报、设立登记、变更登记等。

## 项目特点

- 基于 Playwright 的浏览器自动化
- 模块化设计，易于扩展
- 配置文件驱动，适应不同政务平台
- 批量处理能力
- 完整的错误处理和日志记录

## 目录结构

```
market_supervision_agent/
├── src/                          # 核心源代码
│   ├── __init__.py
│   ├── agent_core.py             # 智能体调度核心
│   ├── browser_controller.py    # 浏览器控制器
│   └── forms/                    # 表单处理模块
│       ├── __init__.py
│       ├── annual_report.py      # 年报填写
│       ├── registration.py       # 设立登记
│       └── change.py             # 变更登记
├── config/                       # 配置文件
│   ├── urls.yaml                 # 政务网站 URL
│   └── selectors.yaml            # 网页元素定位器（核心！）
├── data/                         # 业务数据
│   ├── sample_customers.json    # 示例客户数据
│   ├── processed/                # 已处理文件
│   └── screenshots/              # 截图存储
├── tests/                        # 测试脚本
│   ├── test_agent_core.py
│   └── test_browser_controller.py
├── requirements.txt              # Python 依赖
├── .env.example                  # 环境变量模板
└── README.md                     # 本文件
```

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装 Python 包
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 2. 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入实际配置
```

### 3. 配置选择器

**这是最重要的步骤！**

使用浏览器开发者工具（F12）检查目标网站的表单元素，更新 [config/selectors.yaml](config/selectors.yaml) 中的选择器。

示例：
```yaml
login:
  username: "#username"      # CSS 选择器
  password: "#password"
  submit: "button[type='submit']"
```

### 4. 准备数据

编辑 [data/sample_customers.json](data/sample_customers.json)，填入实际企业数据。

### 5. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 测试浏览器控制器
python src/browser_controller.py

# 测试智能体核心
python src/agent_core.py
```

## 使用示例

### 单个企业年报

```python
from src.agent_core import MarketSupervisionAgent

agent = MarketSupervisionAgent()

company_data = {
    'company_name': '北京示例科技有限公司',
    'credit_code': '91110000XXXXXXXXXX',
    'password': 'your_password',
    'year': 2024,
    'financial_data': {
        'total_assets': 5000000,
        'total_revenue': 3000000,
        # ...更多数据
    }
}

success = agent.process_annual_report(company_data)
```

### 批量处理

```python
import json
from src.agent_core import MarketSupervisionAgent

# 读取客户数据
with open('data/sample_customers.json', 'r', encoding='utf-8') as f:
    customers = json.load(f)

# 构建任务列表
tasks = [
    {'type': 'annual_report', 'data': customer}
    for customer in customers
]

# 批量处理
agent = MarketSupervisionAgent()
results = agent.batch_process(tasks)

print(f"总计: {results['total']}")
print(f"成功: {results['success']}")
print(f"失败: {results['failed']}")
```

## 核心模块说明

### agent_core.py - 智能体核心

负责任务调度、流程编排、错误处理。

主要方法：
- `process_annual_report()` - 处理企业年报
- `process_registration()` - 处理设立登记
- `process_change()` - 处理变更登记
- `batch_process()` - 批量处理任务

### browser_controller.py - 浏览器控制器

封装 Playwright 功能，提供统一的浏览器操作接口。

主要方法：
- `start()` / `close()` - 启动/关闭浏览器
- `navigate()` - 导航到 URL
- `fill_form()` - 填写表单
- `click()` - 点击元素
- `screenshot()` - 截图
- `save_cookies()` / `load_cookies()` - Cookie 管理

### forms/ - 表单处理模块

针对不同业务的表单填写逻辑。

- `annual_report.py` - 企业年报表单
- `registration.py` - 设立登记表单
- `change.py` - 变更登记表单

## 配置文件说明

### config/urls.yaml

存储政务网站的 URL 地址。

```yaml
urls:
  login: "https://example.gov.cn/login"
  annual_report: "https://example.gov.cn/annual-report?year={year}"
```

### config/selectors.yaml

**最核心的配置文件！**

存储网页元素的 CSS 选择器，用于定位表单字段。

获取选择器的方法：
1. 打开目标网站
2. 按 F12 打开开发者工具
3. 点击"选择元素"工具
4. 点击要定位的表单字段
5. 在 Elements 面板右键 → Copy → Copy selector

## 注意事项

### 安全性

1. **不要将密码提交到版本控制**
   - 使用 `.env` 文件存储敏感信息
   - `.env` 已在 `.gitignore` 中

2. **选择器配置**
   - 定期检查选择器是否失效（网站更新后）
   - 使用稳定的选择器（ID > Class > Tag）

3. **错误处理**
   - 启用截图功能便于调试
   - 查看日志文件排查问题

### 法律合规

- 仅用于授权的自动化任务
- 遵守目标网站的服务条款
- 不要进行高频请求，避免被封禁

## 开发计划

- [ ] 添加验证码识别功能
- [ ] 支持更多业务类型
- [ ] 添加 GUI 界面
- [ ] 实现任务队列和调度
- [ ] 添加数据验证功能
- [ ] 支持多浏览器（Firefox, WebKit）

## 故障排除

### 浏览器启动失败

```bash
# 重新安装浏览器
playwright install chromium --force
```

### 元素定位失败

1. 检查 `config/selectors.yaml` 中的选择器是否正确
2. 打开浏览器开发者工具验证选择器
3. 查看截图确认页面是否正确加载

### 依赖安装问题

```bash
# 更新 pip
python -m pip install --upgrade pip

# 清理缓存重新安装
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 项目地址: [01_Active_Projects/market_supervision_agent](.)
- 工作区指南: [WORKSPACE_GUIDE.md](../../WORKSPACE_GUIDE.md)

---

**重要提示**: 使用前请确保已正确配置 `config/selectors.yaml` 文件，这是项目能否正常运行的关键！
