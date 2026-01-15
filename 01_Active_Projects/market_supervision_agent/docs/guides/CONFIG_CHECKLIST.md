# 配置检查清单 - 零基础学员版

## 📋 准备工作
- [ ] 1. 政务网站账号和密码
- [ ] 2. 浏览器（Chrome/Edge）已安装
- [ ] 3. Python环境已准备（已有项目）
- [ ] 4. 记事本或文本编辑器

## 🔧 第一步：学习开发者工具（30分钟）
- [ ] 打开政务网站：________________
- [ ] 按F12打开开发者工具
- [ ] 点击"选择元素"工具（Ctrl+Shift+C）
- [ ] 点击用户名输入框，观察变化
- [ ] 右键 → Copy → Copy selector

## 📝 第二步：配置登录选择器
打开 `config/selectors.yaml`，找到 `login:` 部分：

```yaml
login:
  username: "你复制的选择器"  # 例如: "#username" 或 "input[name='username']"
  password: "你复制的选择器"  # 例如: "#password" 或 "input[type='password']"
  submit: "你复制的选择器"    # 例如: "button[type='submit']" 或 "text=登录"
```

**获取方法**：
1. 在登录页面按F12
2. 点击用户名输入框 → 右键 → Copy → Copy selector
3. 粘贴到配置文件中
4. 重复获取密码框和登录按钮

## 🧪 第三步：测试登录配置
运行测试脚本：
```bash
python quick_test.py
```

**预期结果**：
- 浏览器自动打开
- 导航到政务网站
- 尝试填写用户名和密码
- 截图保存到 `logs/screenshots/`

**常见问题**：
1. **浏览器没打开** → 检查Playwright安装
2. **元素找不到** → 检查选择器是否正确
3. **页面没加载** → 检查网络连接

## 📊 第四步：配置业务表单
选择你要自动化的业务类型：

### 选项1：个体工商户设立登记
需要配置的表单字段：
- [ ] 个体工商户名称
- [ ] 经营者姓名
- [ ] 身份证号码
- [ ] 经营场所
- [ ] 经营范围
- [ ] 资金数额
- [ ] 提交按钮

### 选项2：个体工商户变更登记
需要配置的表单字段：
- [ ] 变更类型选择
- [ ] 新名称（如名称变更）
- [ ] 新经营者（如经营者变更）
- [ ] 新地址（如地址变更）
- [ ] 提交按钮

### 选项3：个体工商户年报
需要配置的表单字段：
- [ ] 统一社会信用代码
- [ ] 年度选择
- [ ] 经营情况
- [ ] 资产情况
- [ ] 提交按钮

## 🎯 第五步：创建测试数据
编辑 `data/sample_customers.json`：

```json
{
  "individual_businesses": [
    {
      "business_name": "张三小吃店",
      "operator_name": "张三",
      "id_card": "110101199001011234",
      "business_address": "北京市东城区王府井大街1号",
      "business_scope": "餐饮服务",
      "registered_capital": 50000,
      "phone": "13800138000",
      "email": "zhangsan@example.com"
    }
  ]
}
```

## ✅ 第六步：完整测试流程
1. [ ] 测试登录功能
2. [ ] 测试导航到业务页面
3. [ ] 测试表单填写
4. [ ] 测试提交功能
5. [ ] 验证结果

## 📚 学习资源
1. **CSS选择器教程**：https://www.w3schools.com/cssref/css_selectors.php
2. **Playwright文档**：https://playwright.dev/python/docs/intro
3. **开发者工具教程**：https://developer.chrome.com/docs/devtools/

## 🆘 故障排除
### 问题1：选择器找不到元素
**解决**：
1. 检查选择器是否正确
2. 使用更简单的选择器（如只用ID）
3. 等待页面完全加载

### 问题2：验证码无法处理
**解决**：
1. 暂时手动输入验证码
2. 后续可集成验证码识别服务

### 问题3：网站结构变化
**解决**：
1. 定期检查选择器是否有效
2. 使用更稳定的选择器（ID优先）
3. 建立选择器版本管理

## 📞 支持渠道
- 项目文档：`README.md`
- 选择器指南：`SELECTOR_GUIDE.md`
- 恢复指南：`RESTORE_GUIDE.md`

---

**重要提示**：每次修改配置文件后，记得运行 `python quick_test.py` 测试！

**进度跟踪**：完成一个复选框就打勾 ✅