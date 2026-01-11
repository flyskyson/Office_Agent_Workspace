# 配置选择器实用指南

基于 playwright-mcp-demo 的实战经验

## 📚 从 gxpf-auto-login.js 学到的经验

### 1. 查找输入框的多种方法

```javascript
// 方法 1: 通过 type 属性
const usernameInput = await page.locator('input[type="text"]').first();
const passwordInput = await page.locator('input[type="password"]').first();

// 方法 2: 通过 placeholder
await page.locator('input[placeholder="请输入用户名"]')

// 方法 3: 通过 ID
await page.locator('#username')

// 方法 4: 通过 name 属性
await page.locator('input[name="username"]')
```

### 2. 查找按钮的方法

```javascript
// 方法 1: 通过文本内容
await page.locator('text=用户登录')
await page.locator('text=提交')

// 方法 2: 通过 button 标签
await page.locator('button[type="submit"]')

// 方法 3: 通过类名
await page.locator('.login-button')
```

### 3. 处理表格数据

```javascript
// 查找所有表格
const tables = await page.locator('table, .el-table').all();

// 遍历行
const rows = await table.locator('tr, .el-table__row').all();

// 提取单元格
const cells = await row.locator('td, th, .el-table__cell').all();
```

### 4. 实用技巧

```javascript
// 等待元素可见
await page.waitForSelector('.loading', { state: 'hidden' })

// 等待网络空闲
await page.goto(url, { waitUntil: 'networkidle' })

// 截图调试
await page.screenshot({ path: 'debug.png', fullPage: true })

// 保存页面HTML
const html = await page.content();
fs.writeFileSync('page.html', html, 'utf-8')

// 保存Cookie
const cookies = await context.cookies();
fs.writeFileSync('cookies.json', JSON.stringify(cookies, null, 2))
```

## 🔍 如何获取选择器（开发者工具方法）

### 步骤 1: 打开开发者工具
1. 访问目标网站
2. 按 F12 打开开发者工具
3. 点击"选择元素"工具（或按 Ctrl+Shift+C）

### 步骤 2: 选择元素
1. 点击页面上的表单字段
2. 在 Elements 面板会高亮显示对应的 HTML
3. 右键 → Copy → Copy selector

### 步骤 3: 优化选择器
```yaml
# ❌ 不好的选择器（太长、太具体）
username: "#app > div > div.login-container > form > div:nth-child(1) > div > input"

# ✅ 好的选择器（简洁、稳定）
username: "#username"
# 或
username: "input[name='username']"
# 或
username: "input[placeholder='用户名']"
```

### 优先级建议
1. **ID 选择器** (最稳定): `#username`
2. **Name 属性**: `input[name="username"]`
3. **Placeholder**: `input[placeholder="请输入用户名"]`
4. **Type + 位置**: `input[type="text"]` (配合 .first() 或 .nth(0))
5. **类名**: `.username-input` (可能会变)
6. **文本内容**: `text=登录` (适合按钮)

## 🎯 实战：配置年报表单选择器

假设你要填写企业年报表单：

### 1. 打开浏览器查看表单
```bash
# 使用 Playwright 的 codegen 工具
python -m playwright codegen https://your-target-website.com
```

这会打开一个浏览器，你的操作会自动生成代码！

### 2. 手动点击和填写
- 点击用户名输入框
- 填写用户名
- 点击密码输入框
- 填写密码
- 点击登录按钮

### 3. 复制生成的代码
Playwright Inspector 会自动生成类似这样的代码：

```javascript
await page.locator('#username').fill('your_username');
await page.locator('#password').fill('your_password');
await page.locator('button:has-text("登录")').click();
```

### 4. 转换为 YAML 配置
```yaml
login:
  username: "#username"
  password: "#password"
  submit: "button:has-text('登录')"
  success_indicator: ".user-info"
```

## 🧪 测试选择器

创建一个简单的测试脚本：

```python
# test_selectors.py
from src.browser_controller import BrowserController

with BrowserController(headless=False) as browser:
    browser.navigate("https://your-target-website.com")

    # 测试能否找到元素
    try:
        browser.wait_for_selector("#username", timeout=5000)
        print("✅ 找到用户名输入框")
    except:
        print("❌ 未找到用户名输入框，检查选择器！")

    # 测试填写
    browser.fill_form("#username", "test_user")
    browser.screenshot("test.png")
```

## 📋 常见表单元素映射

| 元素类型 | HTML 示例 | 选择器 |
|---------|----------|--------|
| 文本输入 | `<input type="text" id="company">` | `#company` |
| 密码输入 | `<input type="password" name="pwd">` | `input[name="pwd"]` |
| 下拉菜单 | `<select id="type">` | `#type` |
| 单选按钮 | `<input type="radio" name="gender" value="M">` | `input[name="gender"][value="M"]` |
| 复选框 | `<input type="checkbox" id="agree">` | `#agree` |
| 文本域 | `<textarea id="description">` | `#description` |
| 按钮 | `<button type="submit">提交</button>` | `button[type="submit"]` |
| 链接 | `<a href="/logout">退出</a>` | `a[href="/logout"]` |

## 🚀 快速开始：配置你的项目

1. **使用 codegen 录制操作**
   ```bash
   cd 01_Active_Projects/market_supervision_agent
   python -m playwright codegen https://your-target-site.com
   ```

2. **复制生成的选择器到 config/selectors.yaml**

3. **运行测试验证**
   ```bash
   python src/browser_controller.py
   ```

4. **调整和优化选择器**

## 💡 提示

- 如果网站使用动态内容（Vue/React），选择器可能包含 `.el-`, `.ant-` 等前缀
- 优先使用稳定的属性（id, name）而不是动态生成的类名
- 使用 `page.waitForSelector()` 确保元素已加载
- 遇到验证码时，预留等待时间（如示例中的 30 秒）
- 保存 Cookie 可以避免重复登录

---

**下一步**: 使用 `playwright codegen` 工具录制你的目标网站操作！
