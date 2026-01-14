# 智能翻译助手 - Smart Translator

## 🎯 项目简介

**Smart Translator** 是一个多引擎翻译助手，集成多种翻译服务，解决 Google 翻译在中国无法使用的问题。

---

## ✨ 核心功能

### 1. 多翻译引擎支持
- ✅ **DeepL** - 翻译质量最高
- ✅ **微软必应** - 稳定可用
- ✅ **百度翻译** - 国内优化
- ✅ **腾讯翻译** - 日常可用
- ✅ **火山翻译** - 字节跳动

### 2. 多种使用方式
- 📝 **命令行翻译**
- 🌐 **网页翻译**
- 📄 **文档翻译**
- 🔧 **Chrome 集成**
- 🤖 **AI 智能翻译**

### 3. 特色功能
- 🔄 自动翻译检测
- 💾 翻译历史缓存
- 📊 多引擎对比
- 🚀 快捷键支持
- 📱 批量翻译

---

## 🚀 使用方式

### 方式 1: 命令行翻译

```bash
# 翻译文本
python 01_Active_Projects/smart_translator/src/translator.py "Hello World"

# 指定引擎
python 01_Active_Projects/smart_translator/src/translator.py "Hello World" --engine deepl

# 翻译文件
python 01_Active_Projects/smart_translator/src/translator.py --file document.txt
```

### 方式 2: Python 脚本

```python
from smart_translator import Translator

# 创建翻译器
translator = Translator(engine='deepl')

# 翻译文本
result = translator.translate("Hello World", target='zh')
print(result)  # 你好，世界

# 批量翻译
texts = ["Hello", "World", "AI"]
results = translator.translate_batch(texts, target='zh')
```

### 方式 3: 浏览器书签

在浏览器中添加以下书签，点击即可翻译当前页面：

```javascript
javascript:(function(){var s=document.createElement('script');s.src='https://cdn.jsdelivr.net/gh/fss95/smart-translator@main/translator.js';document.body.appendChild(s);})();
```

### 方式 4: Chrome DevTools 集成

使用 Chrome DevTools MCP 自动翻译网页：

```
"用 Chrome 打开这个网页并翻译成中文"
```

---

## 📊 支持的翻译引擎

| 引擎 | 质量 | 速度 | 稳定性 | 推荐度 |
|------|------|------|--------|--------|
| **DeepL** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ 最推荐 |
| **微软必应** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ 稳定 |
| **百度翻译** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ 国内 |
| **腾讯翻译** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ 快速 |
| **火山翻译** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ AI |

---

## 🛠️ 配置

### API 密钥配置（可选）

部分引擎支持 API 调用（更稳定）：

```yaml
# config/api_keys.yaml
deepl:
  api_key: "your-deepl-api-key"

microsoft:
  api_key: "your-microsoft-api-key"
  region: "china"

baidu:
  app_id: "your-baidu-app-id"
  secret_key: "your-baidu-secret-key"
```

### 默认引擎配置

```yaml
# config/settings.yaml
default_engine: "deepl"
fallback_engine: "microsoft"
target_language: "zh"
source_language: "auto"
cache_enabled: true
cache_duration: 86400  # 24小时
```

---

## 📁 项目结构

```
smart_translator/
├── src/
│   ├── translator.py       # 主翻译器
│   ├── engines/            # 翻译引擎
│   │   ├── deepl.py
│   │   ├── microsoft.py
│   │   ├── baidu.py
│   │   └── tencent.py
│   └── utils.py            # 工具函数
├── config/
│   ├── api_keys.yaml       # API 密钥
│   └── settings.yaml       # 设置
├── data/
│   └── cache.json          # 翻译缓存
└── README.md
```

---

## 🌐 浏览器扩展推荐

### Immersive Translate（强烈推荐）

**安装**：
1. 访问 [Chrome 网上应用店](https://chromewebstore.google.com/detail/immersive-translate-trans/bpoadfkcbjbfhfodiogcnhhhpibjhbnh)
2. 添加到 Chrome
3. 配置使用 DeepL 引擎

**特点**：
- 双语对照显示
- 支持 PDF 翻译
- 自动检测语言
- 快捷键 `Alt + T`

### DeepL for Chrome

**安装**：
1. 访问 [Chrome 网上应用店](https://chromewebstore.google.com/detail/deepl-for-chrome/clneakkikoojmpfofhlppjmbmfeodoje)
2. 添加到 Chrome

**特点**：
- 最高翻译质量
- 快速翻译
- 支持文档

---

## 💡 使用示例

### 示例 1: 翻译网页

```
你: "帮我打开这个网页并翻译成中文"
   https://example.com

Claude: 使用 Chrome DevTools:
   1. 打开网页
   2. 提取文本
   3. 使用 DeepL 翻译
   4. 显示双语对照
```

### 示例 2: 翻译文档

```
你: "翻译这个 PDF 文档"

Claude: 使用智能翻译助手:
   1. 读取 PDF 内容
   2. 分段翻译
   3. 保持格式
   4. 保存翻译后的文档
```

### 示例 3: 实时翻译

```
你: "创建一个实时翻译工具，监控剪贴板"

Claude: 创建脚本:
   1. 监控剪贴板变化
   2. 自动复制文本
   3. 翻译后显示
   4. 保存到历史记录
```

---

## 🔧 高级功能

### 1. 批量翻译

```bash
python -m smart_translator batch --input texts.txt --output translated.txt
```

### 2. 翻译对比

```bash
python -m smart_translator compare --text "Hello World" --engines deepl,microsoft,baidu
```

### 3. 语言检测

```bash
python -m smart_translator detect --text "Bonjour le monde"
```

---

## 📚 相关资源

- [DeepL 翻译](https://www.deepl.com/translator)
- [微软必应翻译](https://www.bing.com/translator)
- [Immersive Translate](https://immersivetranslate.com/)
- [最佳翻译扩展对比](https://www.swifdoo.com/blog/chrome-translation-extension/)

---

**创建时间**: 2026-01-14
**版本**: 1.0.0
**维护者**: Office Agent Workspace
