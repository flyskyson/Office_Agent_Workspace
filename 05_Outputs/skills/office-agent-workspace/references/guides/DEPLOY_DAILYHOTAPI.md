# DailyHotApi 部署指南

## 📦 DailyHotApi - Vercel 部署

### 🚀 快速部署步骤

#### 1. Fork 项目
访问 [imsyy/DailyHotApi](https://github.com/imsyy/DailyHotApi) 并 Fork 到你的 GitHub

#### 2. 部署到 Vercel

**方式 A - 使用 Vercel 专用版本（推荐）**:
- 访问 [DailyHotApi-Vercel](https://github.com/imsyy/DailyHotApi-Vercel)
- Fork 这个版本
- 在 Vercel 中导入并部署

**方式 B - 使用原版本**:
⚠️ 注意：不要更新到 v2.0.0，使用 v1.x 版本

#### 3. Vercel 部署流程
```
1. 登录 https://vercel.com (使用 GitHub 账号)
2. 点击 "Add New" → "Project"
3. 选择你 Fork 的仓库
4. 点击 "Import"
5. 等待部署完成
6. 获得 *.vercel.app 域名
```

#### 4. 使用 API
```bash
# 获取知乎热榜
curl https://你的域名.vercel.app/api/zhihu

# 获取微博热搜
curl https://你的域名.vercel.app/api/weibo

# 获取 B站热门
curl https://你的域名.vercel.app/api/bilibili
```

---

## 📊 TrendRadar - GitHub Actions 设置

### 项目地址
[sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)

### 功能特点
- 监控 35+ 平台热榜
- 基于 GitHub Actions（免费）
- 自动推送和 AI 分析
- 无需自己维护服务器

### 部署步骤

#### 1. Fork 项目
```bash
https://github.com/sansan0/TrendRadar
```

#### 2. 启用 GitHub Actions
1. 进入你的 Fork 仓库
2. 点击 "Settings" → "Actions" → "General"
3. 选择 "Allow all actions and reusable workflows"
4. 保存

#### 3. 配置 Secrets（可选）
如果有需要配置的密钥，在 "Settings" → "Secrets and variables" → "Actions" 中添加

#### 4. 运行 Workflow
1. 进入 "Actions" 标签
2. 选择可用的 workflow
3. 点击 "Run workflow"

---

## 🕷️ Playwright 爬虫优化

### 已验证可用
- ✅ 微博热搜：真实数据
- ⏳ 知乎热榜：需要登录（使用 API 方式）
- ⏳ 百度热搜：需要处理动态加载

### 使用方式
```bash
python 00_Agent_Library/news_scraper.py
```

### 支持的平台
- 微博热搜（已验证）
- 知乎热榜
- 百度热搜

---

## 🎯 推荐方案对比

| 方案 | 优点 | 缺点 | 推荐指数 |
|------|------|------|----------|
| **DailyHotApi + Vercel** | 完全免费，一键部署，多平台 | 需要账号 | ⭐⭐⭐⭐⭐ |
| **TrendRadar + GitHub Actions** | 免费，自动化，AI 分析 | 需要 GitHub 账号 | ⭐⭐⭐⭐⭐ |
| **Playwright 爬虫** | 完全自主，实时数据 | 需要维护，可能被封 | ⭐⭐⭐ |
| **MCP 服务器** | 集成方便，标准化 | 依赖网络 | ⭐⭐⭐⭐ |

---

## 📝 快速开始

### 最简单的方式（推荐新手）

1. **Fork DailyHotApi-Vercel**
2. **在 Vercel 导入**
3. **获得 API 域名**
4. **在代码中使用**

### 示例代码
```python
import httpx

async def get_hot_news(platform="zhihu"):
    url = f"https://你的域名.vercel.app/api/{platform}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# 使用
news = await get_hot_news("weibo")
print(news)
```

---

## 🔗 相关链接

- [DailyHotApi GitHub](https://github.com/imsyy/DailyHotApi)
- [DailyHotApi-Vercel](https://github.com/imsyy/DailyHotApi-Vercel)
- [TrendRadar GitHub](https://github.com/sansan0/TrendRadar)
- [Vercel 官网](https://vercel.com)

---

**部署完成后，将 API 域名添加到工作区配置中即可使用！**
