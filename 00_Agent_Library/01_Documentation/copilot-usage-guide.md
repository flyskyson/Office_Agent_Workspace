# GitHub Copilot Chat 使用指南

## 🎯 Copilot Chat 基础使用

### 1. 打开 Copilot Chat

有几种方式打开:
- **快捷键**: `Ctrl+Shift+I` (Windows/Linux) 或 `Cmd+Shift+I` (Mac)
- **菜单**: 点击 VSCode 右侧的 Copilot 图标
- **命令面板**: `Ctrl+Shift+P` → 输入 "Copilot Chat: Open Chat"

---

## 💬 基础对话功能

### 询问技术问题

在聊天框中输入问题,Copilot 会回答你:

```
什么是 React Hooks?
```

```
如何在 Python 中读取 JSON 文件?
```

```
解释这段代码的作用:[选中代码后询问]
```

### 代码生成

```
创建一个快速排序算法的 Python 实现
```

```
帮我写一个 JavaScript 函数来验证邮箱格式
```

### 代码解释

选中一段代码,然后:
```
解释这段代码
```

```
这段代码有什么问题?
```

---

## 🤖 使用 Agent 模式 (高级功能)

### 什么是 Agent 模式?

Agent 模式让 Copilot 可以:
- 📁 读取和编辑文件
- 🔍 搜索代码
- 💻 执行终端命令
- 🧰 使用 MCP 工具 (如 Playwright MCP)

### 启用 Agent 模式

1. 打开 Copilot Chat
2. 在输入框上方找到模式选择器
3. 从 **Ask** 模式切换到 **Agent** 模式

### Agent 模式示例

**示例 1: 创建文件**
```
在当前目录创建一个名为 hello.py 的文件,内容是打印 "Hello World"
```

**示例 2: 使用 Playwright MCP**
```
使用 Playwright 打开 https://example.com 并截图保存
```

**示例 3: 代码重构**
```
读取 app.js 文件,重构它使其更易读,并保存修改
```

---

## 🔧 选择不同的模型

### 查看可用模型

1. 打开 Copilot Chat
2. 点击顶部的模型选择器 (显示当前模型名称)
3. 点击 `Manage Models...`

### 切换模型

在模型列表中:
- **GitHub Copilot**: 官方模型 (GPT-4)
- **[OAI Compatible]**: 你配置的 DeepSeek 或 GLM-4.7

### 推荐使用场景

| 任务 | 推荐模型 |
|------|---------|
| 日常代码补全 | GitHub Copilot |
| 中文对话 | GLM-4.7 或 DeepSeek |
| 代码生成 | DeepSeek Coder / GLM-4.6 |
| 成本敏感 | DeepSeek (按量) 或 GLM 包月 |

---

## ⚡ 快捷命令

Copilot Chat 支持一些快捷命令 (以 `/` 开头):

### `/workspace`
```
/workspace
分析整个工作区的代码结构
```

### `/tests`
```
/tests
为当前文件生成单元测试
```

### `/explain`
```
/explain
解释选中的代码
```

### `/fix`
```
/fix
修复选中的代码中的错误
```

### `/clear`
```
/clear
清空对话历史
```

---

## 🎨 与代码交互

### 内联聊天 (Inline Chat)

1. 在编辑器中选中一段代码
2. 按 `Ctrl+I` (Windows/Linux) 或 `Cmd+I` (Mac)
3. 输入指令,例如:
   ```
   重构这段代码使其更简洁
   ```
   ```
   为这段函数添加注释
   ```
   ```
   将这段代码转换为 TypeScript
   ```

### 快速提问

1. 在代码中悬停或选中
2. 按 `Ctrl+Shift+I` 打开 Copilot Chat
3. 直接提问

---

## 📁 使用上下文

### 引用文件

在聊天中使用 `@` 符号引用文件:
```
@app.js 这个文件中的 main 函数是做什么的?
```

### 引用代码符号

```
@MyComponent 解释这个 React 组件
```

### 引用多个文件

```
@utils.js @config.js 这两个文件有什么关系?
```

---

## 🚀 实用技巧

### 1. 生成单元测试

```
为 calculator.js 创建完整的单元测试
```

### 2. 代码重构

```
重构这段代码,使用更现代的 JavaScript 语法
```

### 3. 添加文档注释

```
为这个函数添加 JSDoc 注释
```

### 4. 性能优化

```
分析这段代码的性能问题并提出优化建议
```

### 5. 代码转换

```
将这段 Python 代码转换为 JavaScript
```

### 6. 调试帮助

```
帮我找出这段代码为什么会报错
```

---

## 🎯 实战示例

### 示例 1: 创建新功能

```
创建一个用户登录表单,包含:
- 用户名输入框
- 密码输入框
- 登录按钮
- 表单验证
```

### 示例 2: 代码审查

```
审查当前文件的代码质量,指出潜在问题
```

### 示例 3: 学习新技术

```
教我如何使用 React Context API,并给出示例代码
```

### 示例 4: 修复 Bug

```
这个函数在处理空数组时会崩溃,帮我修复
```

### 示例 5: 文档生成

```
为这个项目生成 README.md 文档
```

---

## 💡 最佳实践

### 1. 明确的指令
❌ 不好的指令:
```
优化代码
```

✅ 好的指令:
```
优化这段代码的性能,减少循环次数,并添加注释说明改动
```

### 2. 提供上下文
❌ 不好的指令:
```
这个函数有问题
```

✅ 好的指令:
```
@app.js 中的 calculateTotal 函数在处理负数时返回 NaN,请修复这个问题
```

### 3. 逐步迭代
```
第一步:创建基础的 HTML 结构
第二步:添加 CSS 样式
第三步:添加 JavaScript 交互
```

### 4. 利用对话历史
Copilot Chat 记住对话上下文,你可以:
```
用户:创建一个待办事项列表
Copilot:[创建代码]

用户:添加删除功能
Copilot:[添加删除功能]

用户:现在添加本地存储
Copilot:[添加 localStorage]
```

---

## 🔌 与 MCP 工具结合 (高级)

如果你配置了 Playwright MCP,在 Agent 模式下可以:

```
使用 Playwright 打开百度并搜索"AI教程"
```

```
用 Playwright 测试登录表单,填写用户名和密码,然后截图
```

```
使用 Playwright 访问我的博客,提取所有文章链接
```

---

## ⚙️ 自定义设置

### 调整 Copilot 行为

1. 打开 VSCode 设置 (`Ctrl+,`)
2. 搜索 "Copilot"
3. 可以调整:
   - 代码建议样式
   - 自动完成触发条件
   - 语言偏好
   - 模型选择

### 键盘快捷键

在 VSCode 设置中搜索 "Copilot Chat Keybindings":
- `Ctrl+Shift+I`: 打开 Copilot Chat
- `Ctrl+I`: 内联聊天
- `Ctrl+Shift+Alt+I`: 快速操作

---

## 📊 对比: Ask 模式 vs Agent 模式

| 功能 | Ask 模式 | Agent 模式 |
|------|---------|-----------|
| 回答问题 | ✅ | ✅ |
| 生成代码 | ✅ | ✅ |
| 编辑文件 | ❌ | ✅ |
| 执行命令 | ❌ | ✅ |
| 使用 MCP 工具 | ❌ | ✅ |
| 读取文件 | ❌ | ✅ |

---

## ❓ 常见问题

### Q1: Copilot 没有响应?
**A**:
1. 检查网络连接
2. 确认已登录 GitHub 账号
3. 查看 Copilot 订阅状态

### Q2: 代码建议不准确?
**A**:
1. 提供更详细的上下文
2. 使用明确的指令
3. 尝试切换模型 (如 DeepSeek 或 GLM-4.7)

### Q3: 如何查看使用统计?
**A**: 访问 https://github.com/settings/copilot

### Q4: 可以在项目中禁用 Copilot?
**A**: 在 `.gitignore` 中添加或创建 `.copilot-instructions.md`

---

## 🎉 开始使用吧!

1. 按 `Ctrl+Shift+I` 打开 Copilot Chat
2. 输入你的第一个问题
3. 体验 AI 辅助编程的强大!

**提示**: 从简单的问题开始,逐步探索更多功能!
