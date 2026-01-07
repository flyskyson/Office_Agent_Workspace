# GitHub Copilot Chat 接入 DeepSeek 和 GLM-4.7 指南

## 📋 前置条件

✅ 已安装:
- GitHub Copilot
- GitHub Copilot Chat

## 🔧 方法一:通过 OAI Compatible Provider 插件 (推荐)

这是最简单的方法,支持任何 OpenAI 兼容的 API。

### 步骤 1:安装 OAI Compatible Provider 插件

1. 在 VSCode 中按 `Ctrl+Shift+X` 打开扩展市场
2. 搜索 "OAI Compatible Provider for Copilot" 或简搜 "oai"
3. 点击安装

### 步骤 2:配置 DeepSeek

#### 2.1 获取 DeepSeek API Key

1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册/登录账号
3. 点击右上角头像 → `API Keys` → `创建新的 API Key`
4. 复制生成的 API Key (格式类似: `sk-xxxxxxxx`)

#### 2.2 配置 OAI Compatible 插件

1. 在 VSCode 中按 `Ctrl+,` 打开设置
2. 搜索 "oai"
3. 找到 "OAI Compatible Provider: Base Url"
4. 填入 DeepSeek 的 API 地址:
   ```
   https://api.deepseek.com
   ```

#### 2.3 在 Copilot Chat 中启用 DeepSeek

1. 打开 Copilot Chat (`Ctrl+Shift+I`)
2. 点击模型选择器
3. 点击 `Manage Models...`
4. 选择 `[OAI Compatible]` 右侧的小齿轮图标
5. 填入你的 DeepSeek API Key
6. 选择模型:
   - `deepseek-chat` (通用对话)
   - `deepseek-coder` (代码专用)
7. 点击 OK 保存

### 步骤 3:配置 GLM-4.7

#### 3.1 获取智谱 API Key

1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册/登录账号
3. 点击右上角头像 → `API Keys` → `创建新的 API Key`
4. 复制生成的 API Key

#### 3.2 配置 GLM-4.7

**方案 A:包月计划用户 (GLM Coding Plan)**

1. 打开 OAI Compatible Provider 设置
2. 修改 Base URL 为:
   ```
   https://open.bigmodel.cn/api/coding/paas/v4
   ```

**方案 B:按量付费用户**

1. 打开 OAI Compatible Provider 设置
2. 修改 Base URL 为:
   ```
   https://open.bigmodel.cn/api/paas/v4
   ```

#### 3.3 在 Copilot Chat 中启用 GLM-4.7

1. 打开 Copilot Chat
2. 点击 `Manage Models...`
3. 选择 `[OAI Compatible]` 右侧的齿轮图标
4. 填入你的智谱 API Key
5. 选择模型:
   - `GLM-4.7` (最新旗舰模型)
   - `GLM-4.6` (编程专用)
   - `GLM-4.5-air` (轻量快速)
6. 点击 OK 保存

### 步骤 4:使用配置的模型

1. 在 Copilot Chat 中点击模型选择器
2. 从列表中选择你配置的模型 (DeepSeek 或 GLM-4.7)
3. 开始对话!

---

## 🎯 API 地址汇总

| 提供商 | Base URL (按量付费) | Base URL (包月) |
|--------|-------------------|----------------|
| **DeepSeek** | `https://api.deepseek.com` | - |
| **智谱 GLM** | `https://open.bigmodel.cn/api/paas/v4` | `https://open.bigmodel.cn/api/coding/paas/v4` |

## 🤖 模型名称对照表

### DeepSeek
- `deepseek-chat` - 通用对话模型
- `deepseek-coder` - 代码生成模型

### 智谱 GLM
- `GLM-4.7` - 最新旗舰模型 (推荐)
- `GLM-4.6` - 编程专用模型
- `GLM-4.5-air` - 轻量快速模型

---

## 💰 费用对比

### DeepSeek
- 新用户赠送 500万 tokens
- 按量计费,价格低廉
- 适合:个人开发者、小团队

### 智谱 GLM
- **包月计划** (GLM Coding Plan):
  - 每月 20 元起
  - 适合高频使用
- **按量付费**:
  - 新用户赠送一定额度
  - 用多少付多少

---

## 🔧 多模型切换使用

你可以同时配置 DeepSeek 和 GLM-4.7,在不同场景切换使用:

### 使用场景建议

| 场景 | 推荐模型 | 原因 |
|------|---------|------|
| **代码生成** | DeepSeek Coder / GLM-4.6 | 专门针对代码优化 |
| **通用问答** | GLM-4.7 | 综合能力强 |
| **快速响应** | GLM-4.5-air | 速度快,成本低 |
| **复杂推理** | GLM-4.7 | 推理能力强 |

### 切换方法

1. 在 Copilot Chat 界面
2. 点击模型选择器 (通常在顶部)
3. 从下拉列表中选择想要的模型
4. 开始对话

---

## ❓ 常见问题

### Q1: 配置后无法使用?
**A**: 检查以下几点:
1. API Key 是否正确复制
2. Base URL 是否填写正确
3. 网络是否能访问 API 地址
4. 账户是否有足够的额度

### Q2: 可以同时使用多个模型吗?
**A**: 可以!OAI Compatible Provider 支持多个配置,你可以随时切换。

### Q3: 哪个模型更适合编程?
**A**:
- **DeepSeek Coder**: 代码生成质量高,价格便宜
- **GLM-4.6**: 中文编程场景优秀,有包月计划
- **GitHub Copilot 官方**: 英文代码场景更好

### Q4: 如何查看剩余额度?
**A**:
- **DeepSeek**: 登录 https://platform.deepseek.com/usage
- **智谱 GLM**: 登录 https://open.bigmodel.cn/ 查看控制台

### Q5: 可以取消订阅吗?
**A**: 可以随时取消,按需使用。

---

## 🚀 快速开始

### 推荐配置方案

**方案 A: 预算友好型**
- 代码补全: GitHub Copilot (官方)
- 对话问答: DeepSeek (按量付费)
- 月成本: ~$10-20

**方案 B: 高性价比型**
- 代码补全: GLM-4.6 包月计划
- 对话问答: GLM-4.7 包月计划
- 月成本: ~20-40 元

**方案 C: 免费试用型**
- 代码补全: DeepSeek (新用户 500万 tokens)
- 对话问答: DeepSeek
- 月成本: 免费 (用完额度后再付费)

---

## 📚 参考资源

- [DeepSeek 官方文档](https://platform.deepseek.com/docs)
- [智谱AI 开放平台](https://open.bigmodel.cn/)
- [OAI Compatible Provider GitHub](https://github.com/JohnnyZ93/oai-compatible-copilot)

---

**开始配置吧! 🎉**
