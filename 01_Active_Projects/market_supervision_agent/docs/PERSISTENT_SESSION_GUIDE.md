# 持久化会话使用指南

## 🎯 功能说明

使用持久化浏览器会话，实现**一次登录，长期有效**。

### 优点
- ✅ **一次登录，长期有效**：登录后会话自动保存
- ✅ **无需重复登录**：下次启动自动使用保存的会话
- ✅ **完整保存**：自动保存Cookie、LocalStorage、Session Storage
- ✅ **简单易用**：一键启动脚本

---

## 📋 使用步骤

### 第一次使用（需要登录）

1. **运行启动脚本**
   ```bash
   cd 01_Active_Projects/market_supervision_agent
   python start_persistent_session.py
   ```

2. **浏览器自动打开**
   - 自动导航到：https://zwfw.gxzf.gov.cn/yct/
   - 检测到未登录状态

3. **手动登录**
   - 在浏览器中点击"登录"按钮
   - 输入账号密码
   - 完成登录

4. **会话自动保存**
   - 登录成功后，会话自动保存到 `data/browser_profile/`
   - Cookie自动保存到 `data/portal_cookies.json`

5. **关闭浏览器**
   - 按 Ctrl+C 关闭脚本
   - 或直接关闭浏览器窗口

### 后续使用（无需登录）

1. **再次运行启动脚本**
   ```bash
   python start_persistent_session.py
   ```

2. **自动登录**
   - 自动加载保存的会话
   - 无需重复登录
   - 可以直接进行自动化操作

---

## 🚀 高级用法

### 使用Python代码

```python
from src.session_manager import PersistentSessionManager

# 创建会话
session = PersistentSessionManager(
    user_data_dir="data/browser_profile",
    headless=False  # 设为True启用无头模式
)

# 启动（自动检查登录状态）
session.start(auto_login=True)

# 导航到指定页面
session.navigate_to("https://zwfw.gxzf.gov.cn/yct/")

# 截图
session.take_screenshot("test.png")

# 获取Cookie
cookies = session.get_cookies()

# 关闭会话
session.close()
```

### 使用上下文管理器

```python
from src.session_manager import PersistentSessionManager

with PersistentSessionManager() as session:
    # 自动启动和关闭
    session.navigate_to("https://zwfw.gxzf.gov.cn/yct/")
    session.take_screenshot()
    # ... 其他操作
```

### 政务服务网自动化

```python
from src.portal_automation_persistent import PersistentPortalAutomation

with PersistentPortalAutomation() as portal:
    # 导航到企业开办页面
    portal.navigate_to_enterprise_setup()

    # 检测页面元素
    elements = portal.detect_page_elements()
```

---

## 📁 文件说明

### 核心文件

| 文件 | 说明 |
|------|------|
| `src/session_manager.py` | 持久化会话管理器 |
| `start_persistent_session.py` | 一键启动脚本 |
| `src/portal_automation_persistent.py` | 政务网自动化（持久化版本） |

### 数据文件

| 文件/目录 | 说明 |
|----------|------|
| `data/browser_profile/` | 浏览器配置文件（会话数据） |
| `data/portal_cookies.json` | 导出的Cookie |
| `data/screenshots/` | 截图保存目录 |

---

## ⚙️ 配置选项

### 会话管理器配置

```python
PersistentSessionManager(
    user_data_dir=Path("data/browser_profile"),  # 用户数据目录
    headless=False,                               # 是否无头模式
    slow_mo=500                                   # 操作延迟（毫秒）
)
```

### 启动选项

```python
session.start(
    auto_login=True,                              # 是否自动打开登录页
    login_url="https://zwfw.gxzf.gov.cn/yct/"    # 登录页面URL
)
```

---

## 🔧 常见问题

### Q: 会话有效期多久？
A: 理论上永久有效，除非：
- 手动清除 `data/browser_profile/` 目录
- 服务端Session过期（通常30分钟无操作后）
- 修改密码或重新登录

### Q: 如何重新登录？
A: 删除 `data/browser_profile/` 目录，重新运行启动脚本：
```bash
rm -rf data/browser_profile/
python start_persistent_session.py
```

### Q: 如何使用无头模式？
A: 在创建会话时设置 `headless=True`：
```python
session = PersistentSessionManager(headless=True)
```

### Q: 多个账号如何管理？
A: 使用不同的 `user_data_dir`：
```python
# 账号1
session1 = PersistentSessionManager(user_data_dir="data/account1")

# 账号2
session2 = PersistentSessionManager(user_data_dir="data/account2")
```

### Q: 会话数据在哪里？
A: 存储在 `data/browser_profile/` 目录：
- Cookie: `Default/Network/Cookies`
- LocalStorage: `Default/Local Storage/leveldb/`
- Session Storage: `Default/Session Storage/`

---

## 📊 测试脚本

运行测试脚本验证功能：

```bash
# 测试会话管理
python start_persistent_session.py

# 测试政务服务网自动化
python src/portal_automation_persistent.py
```

---

## 🎯 下一步

会话建立后，可以：

1. **开发自动化脚本**
   - 自动填写表单
   - 自动提交申请
   - 自动查询状态

2. **集成到工作流**
   - 作为统一工作流的输入源
   - 自动提取政务服务网数据

3. **批量操作**
   - 批量名称查重
   - 批量申请提交

---

## 📞 技术支持

如有问题，请查看：
- 日志文件：`logs/session_*.log`
- 截图文件：`data/screenshots/`
- 页面元素：`data/page_elements.json`
