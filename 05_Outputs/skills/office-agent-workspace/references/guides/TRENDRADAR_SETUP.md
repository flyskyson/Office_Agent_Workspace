# TrendRadar GitHub Actions 设置指南

## 📊 TrendRadar 简介

TrendRadar 是一个基于 GitHub Actions 的热点监控工具，可以监控 35+ 平台的热榜数据。

- **GitHub**: https://github.com/sansan0/TrendRadar
- **功能**: 热点监控、自动推送、AI 分析
- **成本**: 完全免费（使用 GitHub 免费额度）

---

## 🚀 部署步骤

### 步骤 1: Fork 项目

1. 访问 https://github.com/sansan0/TrendRadar
2. 点击右上角的 "Fork" 按钮
3. 选择 Fork 到你的 GitHub 账号

### 步骤 2: 启用 GitHub Actions

1. 进入你 Fork 的仓库
2. 点击 "Settings" 标签
3. 在左侧菜单找到 "Actions"
4. 点击 "General"
5. 滚动到 "Actions permissions" 部分
6. 选择 "Allow all actions and reusable workflows"
7. 点击 "Save" 保存

### 步骤 3: 配置 Secrets（可选）

如果需要配置通知服务（如 Telegram、钉钉等）：

1. 进入 "Settings" → "Secrets and variables" → "Actions"
2. 点击 "New repository secret"
3. 添加以下密钥（根据需要）：

```yaml
# Telegram 机器人（可选）
TELEGRAM_BOT_TOKEN: 你的 Telegram Bot Token
TELEGRAM_CHAT_ID: 你的 Telegram Chat ID

# 钉钉机器人（可选）
DINGTALK_WEBHOOK: 你的钉钉 Webhook URL

# 企业微信（可选）
WECHAT_WEBHOOK: 你的企业微信 Webhook URL
```

### 步骤 4: 运行 Workflow

1. 点击 "Actions" 标签
2. 在左侧选择可用的 workflow
3. 点击 "Run workflow" 按钮
4. 选择分支（通常是 main 或 master）
5. 点击绿色的 "Run workflow" 按钮

### 步骤 5: 查看结果

1. 等待 workflow 执行完成
2. 点击进入具体的 workflow run
3. 查看执行日志和输出结果
4. 结果会保存在仓库的相应位置

---

## 📋 支持的平台

TrendRadar 支持监控以下平台：

### 社交媒体
- 微博热搜
- 知乎热榜
- 抖音热点
- 快手热榜
- B站热门

### 新闻资讯
- 百度热搜
- 今日头条
- 36氪
- 虎扑热榜
- 豆瓣热榜

### 其他
- GitHub Trending
- IT之家
- 华尔街见闻
- 少数派
- 雪球

---

## ⚙️ 自定义配置

### 修改监控平台

编辑 `.github/workflows/` 目录下的 workflow 文件：

```yaml
name: TrendRadar Monitor

on:
  schedule:
    # 每天 8:00 和 20:00 运行
    - cron: '0 8,20 * * *'
  workflow_dispatch:  # 支持手动触发

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - name: Run TrendRadar
        run: |
          # 配置要监控的平台
          python main.py --platform zhihu,weibo,bilibili
```

### 修改运行频率

在 workflow 文件中修改 cron 表达式：

```yaml
schedule:
  # 每小时运行一次
  - cron: '0 * * * *'

  # 每天早上 8 点运行
  - cron: '0 8 * * *'

  # 每 6 小时运行一次
  - cron: '0 */6 * * *'
```

---

## 🔔 通知设置

### Telegram 通知

1. 创建 Telegram Bot：向 @BotFather 发送 `/newbot`
2. 获取 Bot Token
3. 获取你的 Chat ID：向 @userinfobot 发送消息
4. 在仓库 Secrets 中添加：
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

### 钉钉通知

1. 在钉钉群中添加自定义机器人
2. 获取 Webhook URL
3. 在仓库 Secrets 中添加：
   - `DINGTALK_WEBHOOK`

---

## 📖 使用示例

### 手动触发运行

1. 进入 "Actions" 标签
2. 选择对应的 workflow
3. 点击 "Run workflow"
4. 等待执行完成

### 查看历史数据

生成的数据文件会保存在仓库的指定目录中，可以直接查看。

---

## 💡 最佳实践

1. **定期检查**：建议每天或每半天运行一次
2. **数据备份**：定期导出重要数据
3. **通知配置**：配置及时的通知方式
4. **日志查看**：定期查看 workflow 运行日志
5. **版本更新**：关注上游更新，及时同步

---

## 🆘 常见问题

### Q: Workflow 运行失败怎么办？
**A**:
1. 查看运行日志，定位错误
2. 检查 Secrets 配置是否正确
3. 确认 GitHub Actions 已启用
4. 尝试重新运行 workflow

### Q: 如何修改监控的平台？
**A**: 编辑 workflow 文件中的平台配置列表

### Q: 数据保存在哪里？
**A**: 通常保存在仓库的特定目录或通过 Artifacts 保存

### Q: 可以同时监控多个平台吗？
**A**: 可以，在配置中添加多个平台即可

---

## 🔗 相关链接

- [TrendRadar GitHub](https://github.com/sansan0/TrendRadar)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Cron 表达式生成器](https://crontab.guru/)

---

**设置完成后，TrendRadar 将自动监控指定平台的热榜数据！**
