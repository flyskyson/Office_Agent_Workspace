# PDF 文本提取器 - 项目说明

## 📋 项目概述

**PDF 文本提取器** 是一个基于 Python 开发的命令行工具，专门用于批量提取 PDF 文件的文本内容。

### 核心价值

- 🚀 **高效批量处理** - 一次性处理整个文件夹中的所有 PDF 文件
- 📊 **多格式输出** - 支持 Markdown 和 JSON 两种主流格式
- 🛡️ **智能容错** - 自动识别并处理加密、损坏等异常情况
- 📈 **实时进度** - 显示详细的处理进度和统计信息
- 🌏 **完美中文支持** - 原生支持中文文件名和内容

---

## 🎯 适用场景

| 场景 | 说明 |
|------|------|
| **文档归档** | 将纸质文档扫描后的 PDF 整理为可搜索的文本 |
| **数据分析** | 提取报告数据，进行文本分析和挖掘 |
| **内容检索** | 建立文档索引，便于快速查找 |
| **格式转换** | 将 PDF 转换为更易读的 Markdown 或 JSON 格式 |
| **批量处理** | 处理大量 PDF 文件，自动化办公流程 |

---

## 📂 项目结构

```
pdf_processor/
├── pdf_extractor.py              # 主程序（命令行工具）
├── pdf_extractor_learning.py     # 学习版（带详细注释）
├── requirements.txt              # 依赖包列表
├── README.md                     # 用户手册
├── PROJECT.md                    # 项目说明（本文件）
├── AI_WORKFLOW.md                # AI 助手使用指南
└── argparse_demo*.py             # argparse 学习示例
```

---

## 🔧 技术栈

### 核心依赖

| 库名 | 版本 | 用途 |
|------|------|------|
| **pdfplumber** | 0.11.8+ | PDF 文本提取核心库 |
| **argparse** | - | 命令行参数解析（Python 标准库） |
| **json** | - | JSON 格式输出（Python 标准库） |

### 系统要求

- **Python**: 3.7 或更高版本
- **操作系统**: Windows / macOS / Linux（跨平台）
- **内存**: 建议 2GB 以上（处理大型 PDF 时）

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install pdfplumber
```

### 2. 基本使用

```bash
# 查看帮助信息
python pdf_extractor.py -h

# 基本用法（Markdown 格式）
python pdf_extractor.py -i "C:\Documents\PDFs"

# 输出为 JSON 格式
python pdf_extractor.py -i "./pdfs" -f json

# 自定义输出文件名
python pdf_extractor.py -i "./pdfs" -o "2024年度报告"
```

### 3. 查看结果

提取完成后，在输入文件夹中会生成：

- **Markdown 格式**: `提取结果.md`
- **JSON 格式**: `提取结果.json`

---

## 💡 命令行参数

| 参数 | 短选项 | 长选项 | 必需/可选 | 说明 |
|------|--------|--------|-----------|------|
| **输入路径** | `-i` | `--input` | ✅ 必需 | PDF 文件夹路径 |
| **输出格式** | `-f` | `--format` | ⚪ 可选 | markdown 或 json（默认：markdown） |
| **输出文件名** | `-o` | `--output` | ⚪ 可选 | 输出文件名，不含扩展名（默认：提取结果） |
| **帮助** | `-h` | `--help` | - | 显示帮助信息 |

---

## 📖 核心功能说明

### 1. 批量文件处理

**功能**: 自动扫描并处理指定文件夹中的所有 PDF 文件

**特性**:
- 支持 `.pdf` 和 `.PDF` 扩展名（不区分大小写）
- 自动排序文件处理顺序
- 跳过子文件夹，只处理 PDF 文件

### 2. 多页文本提取

**功能**: 逐页提取 PDF 文本内容

**特性**:
- 保留页码信息
- 标记空页面
- 记录每页提取失败的情况

### 3. 智能错误处理

**功能**: 识别并处理常见的 PDF 问题

| 错误类型 | 识别方式 | 处理方式 |
|---------|---------|---------|
| **加密 PDF** | 检测 "encrypted" 或 "password" 关键字 | 标记失败，继续处理其他文件 |
| **损坏 PDF** | 检测 "damaged" 或 "corrupt" 关键字 | 标记失败，继续处理其他文件 |
| **扫描件** | 提取结果为空 | 标记为"无文本内容" |
| **单页错误** | 页面处理异常 | 记录错误，继续处理其他页 |

### 4. 双格式输出

#### Markdown 格式（`.md`）

**适用**: 需要人工阅读和编辑的场景

**结构**:
```markdown
# PDF 文本提取结果

**提取时间**: 2026-01-05 14:30:45

---

## 提取统计

- 总文件数: 5
- 成功提取: 4
- 提取失败: 1

---

## 文件1.pdf

--- 第 1 页 ---
文本内容...

---
```

**特点**:
- 📖 易读性强
- 🎨 支持 Markdown 语法高亮
- 📊 包含统计信息

#### JSON 格式（`.json`）

**适用**: 需要程序处理和数据分析的场景

**结构**:
```json
{
  "提取时间": "2026-01-05 14:30:45",
  "统计": {
    "总文件数": 5,
    "成功提取": 4,
    "提取失败": 1
  },
  "文件": [
    {
      "文件名": "文件1.pdf",
      "状态": "成功",
      "内容": "...",
      "字符数": 1234
    }
  ]
}
```

**特点**:
- 💻 结构化数据
- 🔗 便于程序解析
- 📈 适合数据分析

---

## 🏗️ 代码架构

### 模块划分

```
┌─────────────────────────────────────┐
│         main()                      │  程序入口
│   └─> parse_arguments()            │  参数解析
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│      process_pdfs()                 │  主处理逻辑
│   ├─> get_pdf_files()              │  获取文件列表
│   ├─> extract_text_from_pdf()      │  提取文本
│   ├─> save_to_markdown()           │  保存 MD
│   └─> save_to_json()               │  保存 JSON
└─────────────────────────────────────┘
```

### 核心函数说明

| 函数 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **parse_arguments()** | 解析命令行参数 | 命令行参数 | 参数对象 |
| **get_pdf_files()** | 获取 PDF 文件列表 | 文件夹路径 | 文件列表 |
| **extract_text_from_pdf()** | 提取单个 PDF 文本 | PDF 文件路径 | (文本, 成功标志, 错误信息) |
| **save_to_markdown()** | 保存为 Markdown | 结果列表, 输出路径 | - |
| **save_to_json()** | 保存为 JSON | 结果列表, 输出路径 | - |
| **process_pdfs()** | 主处理流程 | 输入路径, 格式, 文件名 | 退出码 |

---

## 📝 使用示例

### 示例 1：处理下载文件夹

```bash
# 场景：整理下载文件夹中的 PDF 文档
python pdf_extractor.py -i "C:\Users\YourName\Downloads"
```

**输出**:
```
============================================================
          PDF 文本批量提取工具
============================================================

📁 正在扫描文件夹: C:\Users\YourName\Downloads
✅ 找到 15 个 PDF 文件

[1/15] 正在处理: report1.pdf... ✅ 成功 (12345 字符)
[2/15] 正在处理: manual.pdf... ✅ 成功 (8765 字符)
...

============================================================
💾 正在保存结果到: C:\Users\YourName\Downloads\提取结果.md
✅ 结果保存成功！
```

### 示例 2：提取财务报告（JSON 格式）

```bash
# 场景：提取财务报告，便于后续数据分析
python pdf_extractor.py -i "./财务报告" -f json -o "Q4财务数据"
```

**用途**:
- 导入 Excel 进行分析
- 使用 pandas 处理数据
- 建立数据库索引

### 示例 3：批量处理学术论文

```bash
# 场景：提取学术论文全文
python pdf_extractor.py -i "D:\论文集" -o "论文全文"
```

**用途**:
- 建立文献检索系统
- 进行文本相似度分析
- 提取关键信息

---

## ⚠️ 注意事项与限制

### 支持的文件类型

✅ **支持**:
- 包含可提取文本的 PDF（文字型 PDF）
- 各种编码的 PDF（UTF-8, GBK 等）
- 加密的 PDF（会跳过并标记）

❌ **不支持**:
- 纯图片扫描件（OCR 功能需额外开发）
- 需要密码的 PDF（会提示失败）
- 严重损坏的 PDF（无法打开）

### 性能考虑

| 文件大小 | 建议操作 |
|---------|---------|
| < 10MB | 正常处理 |
| 10MB - 100MB | 可能需要较长时间 |
| > 100MB | 建议单独处理 |

### 使用限制

1. **输出文件覆盖**
   - 如果同名文件已存在，会被覆盖
   - 建议处理前备份重要文件

2. **编码问题**
   - Windows 控制台已优化中文显示
   - 输出文件使用 UTF-8 编码
   - 某些特殊字符可能无法正确显示

3. **内存占用**
   - 处理大型 PDF 或批量文件时，内存占用较高
   - 建议关闭其他程序以释放内存

---

## 🐛 常见问题

### Q1: 提示"未找到任何 PDF 文件"

**可能原因**:
- 文件夹路径不正确
- 文件夹中没有 `.pdf` 或 `.PDF` 文件
- 没有读取权限

**解决方法**:
```bash
# 检查文件夹路径是否正确
# 确保路径用引号括起来
python pdf_extractor.py -i "正确的路径"

# 检查文件扩展名
# Windows: 查看 .pdf 或 .PDF
dir "你的文件夹\*.pdf"
```

### Q2: 某些 PDF 提取失败或内容为空

**可能原因**:
- PDF 是扫描件（图片格式）
- PDF 已加密
- PDF 文件损坏
- PDF 使用特殊编码

**解决方法**:
```bash
# 检查输出文件中的错误信息
# Markdown: 查找 "⚠️ 提取失败"
# JSON: 查看 "状态": "失败" 的文件
```

### Q3: 中文显示乱码

**解决方法**:
```bash
# Windows 用户，程序已内置编码支持
# 如仍有问题，设置控制台编码：
chcp 65001

# 然后重新运行
python pdf_extractor.py -i "路径"
```

### Q4: 处理速度慢

**优化建议**:
- 处理大文件时，关闭其他程序
- 分批处理文件（不要一次性处理几百个）
- 使用 SSD 硬盘提升 I/O 速度

### Q5: 如何处理加密 PDF

**说明**:
- 当前版本不支持解密
- 需要使用 PDF 解密工具预先处理
- 或使用 PDF 编辑器移除密码保护

---

## 🔮 未来扩展方向

### 短期计划

- [ ] 支持 OCR（光学字符识别）
- [ ] 添加图片提取功能
- [ ] 支持多线程处理
- [ ] 添加进度条显示

### 长期计划

- [ ] 支持批量加密 PDF 解密
- [ ] 添加 GUI 图形界面
- [ ] 支持更多输出格式（XML, Excel）
- [ ] 开发 Web API 接口
- [ ] 添加 PDF 元数据提取

---

## 📚 相关资源

### 学习资料

- **pdfplumber 官方文档**: https://github.com/jsvine/pdfplumber
- **argparse 教程**: https://docs.python.org/3/library/argparse.html
- **Python 文件操作**: https://docs.python.org/3/library/filesys.html

### 项目文档

- [README.md](README.md) - 用户手册
- [AI_WORKFLOW.md](AI_WORKFLOW.md) - AI 助手使用指南
- [pdf_extractor_learning.py](pdf_extractor_learning.py) - 学习版代码

### 工具推荐

- **PDF 编辑**: PDF-XChange Editor, Adobe Acrobat
- **PDF 转换**: pandoc, calibre
- **文本编辑**: VS Code, Sublime Text

---

## 🤝 贡献指南

### 如何贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 添加详细的注释和文档字符串
- 编写单元测试
- 更新相关文档

---

## 📄 许可证

MIT License

---

## 👨‍💻 作者

**flyskyson**

- GitHub: [@flyskyson](https://github.com/flyskyson)
- 项目地址: [PDF Processor](https://github.com/flyskyson/pdf_processor)

---

## 🌟 致谢

感谢以下开源项目：

- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF 文本提取核心
- [Python](https://www.python.org/) - 编程语言
- [argparse](https://docs.python.org/3/library/argparse.html) - 命令行参数解析

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 提交 GitHub Issue
- 💬 发起 GitHub Discussion
- 📖 查看项目文档

---

<div align="center">

**如有帮助，请给个 ⭐Star 支持一下！**

Made with ❤️ by flyskyson

</div>
