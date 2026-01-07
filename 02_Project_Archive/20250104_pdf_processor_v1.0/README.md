# PDF 文本批量提取工具

<div align="center">

**一个强大、易用的 PDF 文本批量提取工具**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[功能特性](#功能特性) • [快速开始](#快速开始) • [使用说明](#使用说明) • [输出格式](#输出格式) • [注意事项](#注意事项)

</div>

---

## 📖 项目简介

PDF 文本批量提取工具是一个基于 Python 开发的命令行工具，旨在帮助用户快速、高效地从批量 PDF 文件中提取文本内容。该工具支持多种输出格式，并提供友好的命令行界面，适用于文档处理、数据分析、内容归档等多种场景。

### ✨ 核心优势

- 🚀 **高效批量处理** - 一次性处理整个文件夹中的所有 PDF 文件
- 📊 **多种输出格式** - 支持 Markdown 和 JSON 两种主流格式
- 🛡️ **智能错误处理** - 自动识别加密文件、损坏文件等异常情况
- 📈 **详细进度显示** - 实时显示处理进度和统计信息
- 🔧 **灵活的命令行接口** - 丰富的参数选项，满足各种使用需求
- 🌏 **完美中文支持** - 原生支持中文文件名和内容，无乱码问题

---

## 🎯 功能特性

### 核心功能

| 功能 | 说明 |
|------|------|
| **批量提取** | 自动扫描并处理指定文件夹中的所有 PDF 文件（支持 `.pdf` 和 `.PDF`） |
| **多页提取** | 逐页提取 PDF 文本内容，保留页码信息 |
| **格式支持** | 支持 Markdown (`.md`) 和 JSON (`.json`) 两种输出格式 |
| **错误检测** | 自动识别加密文件、损坏文件、扫描件等 |
| **统计报告** | 提供详细的提取统计信息（成功/失败数量、字符数等） |
| **自定义输出** | 支持自定义输出文件名 |

### 错误处理

- ✅ 自动识别加密 PDF 文件
- ✅ 自动检测损坏的 PDF 文件
- ✅ 友好的错误提示信息
- ✅ 单个文件失败不影响整体处理

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.7 或更高版本
- **操作系统**: Windows / macOS / Linux

### 安装步骤

#### 1. 克隆或下载项目

```bash
# 如果使用 Git
git clone <repository-url>
cd pdf_processor

# 或直接下载并解压项目文件夹
```

#### 2. 安装依赖

```bash
# 使用 pip 安装依赖
pip install -r requirements.txt
```

**依赖包说明：**

| 依赖包 | 版本 | 用途 |
|--------|------|------|
| pdfplumber | 0.11.8 | PDF 文本提取核心库 |
| cryptography | 46.0.3 | 加密支持 |
| Pillow | 12.1.0 | 图像处理支持 |

#### 3. 验证安装

```bash
# 查看帮助信息
python pdf_extractor.py -h
```

如果看到帮助信息，说明安装成功！

---

## 📚 使用说明

### 基本语法

```bash
python pdf_extractor.py -i <PDF文件夹路径> [选项]
```

### 命令行参数

| 参数 | 短选项 | 长选项 | 必需/可选 | 说明 | 示例 |
|------|--------|--------|-----------|------|------|
| **输入路径** | `-i` | `--input` | ✅ 必需 | 指定包含 PDF 文件的文件夹路径 | `-i "C:\Documents\PDFs"` |
| **输出格式** | `-f` | `--format` | ⚪ 可选 | 指定输出格式：`markdown` 或 `json`（默认：markdown） | `-f json` |
| **输出文件名** | `-o` | `--output` | ⚪ 可选 | 指定输出文件名（不含扩展名，默认：提取结果） | `-o "我的提取结果"` |
| **帮助信息** | `-h` | `--help` | - | 显示帮助信息并退出 | `-h` |

### 使用示例

#### 示例 1：基本使用（Markdown 格式）

```bash
python pdf_extractor.py -i "C:\Documents\PDFs"
```

**说明：** 使用默认设置，将 PDF 文本提取为 Markdown 格式，输出到 `C:\Documents\PDFs\提取结果.md`

#### 示例 2：输出为 JSON 格式

```bash
python pdf_extractor.py -i "./pdfs" -f json
```

**说明：** 提取文本并保存为 JSON 格式，输出到 `./pdfs/提取结果.json`

#### 示例 3：自定义输出文件名

```bash
python pdf_extractor.py -i "./my pdfs" -o "2024年度报告"
```

**说明：** 提取结果将保存为 `./my pdfs/2024年度报告.md`

#### 示例 4：完整参数示例

```bash
python pdf_extractor.py --input "./documents" --format json --output "analysis_result"
```

**说明：** 使用长选项形式，功能与短选项相同

#### 示例 5：查看帮助信息

```bash
python pdf_extractor.py -h
```

**输出：**
```
usage: pdf_extractor.py [-h] -i INPUT [-f {markdown,json}] [-o OUTPUT]

PDF 文本批量提取工具 - 批量提取文件夹中所有 PDF 文件的文本内容

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        指定要处理的 PDF 文件夹路径（必需）
  -f {markdown,json}, --format {markdown,json}
                        指定输出格式：markdown 或 json（默认：markdown）
  -o OUTPUT, --output OUTPUT
                        指定输出文件名（不含扩展名）（默认：提取结果）
```

---

## 📄 输出格式说明

### 1. Markdown 格式（`.md`）

默认输出格式，适合阅读和编辑。

**文件结构：**

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
这是第一页的文本内容...

--- 第 2 页 ---
这是第二页的文本内容...

---

## 文件2.pdf

--- 第 1 页 ---
[此页无文本内容，可能是图片或扫描件]

---

## 文件3.pdf

⚠️ **提取失败**: PDF 文件已加密，需要密码

---
```

**特点：**
- 📖 易读性强，适合人工查看
- 🎨 支持 Markdown 语法高亮
- 📊 包含统计信息
- 🔍 保留原始文本格式

### 2. JSON 格式（`.json`）

结构化数据格式，适合程序处理和数据分析。

**文件结构：**

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
      "内容": "--- 第 1 页 ---\n这是第一页的文本内容...",
      "字符数": 1234
    },
    {
      "文件名": "文件2.pdf",
      "状态": "失败",
      "错误信息": "PDF 文件已加密，需要密码"
    }
  ]
}
```

**特点：**
- 💻 结构化数据，易于程序解析
- 📊 便于数据分析和处理
- 🔗 支持与其他工具集成
- 📈 包含详细的统计信息

---

## ⚠️ 注意事项

### 文件要求

1. **支持的文件格式**
   - ✅ PDF 文件（`.pdf` 或 `.PDF` 扩展名）
   - ✅ 包含可提取文本的 PDF（非扫描件）
   - ❌ 不支持扫描件或图片型 PDF（将显示为"无文本内容"）

2. **文件路径**
   - 路径可以是绝对路径或相对路径
   - 路径中的空格会被自动处理
   - Windows 路径示例：
     - `C:\Documents\PDFs`
     - `"C:\My Documents\PDF Files"`
     - `./pdfs`（相对路径）

3. **特殊文件处理**
   - 🔒 **加密 PDF**：需要密码的 PDF 无法提取，会标记为失败
   - ❌ **损坏 PDF**：损坏的文件无法处理，会显示相应错误信息
   - 🖼️ **扫描件/图片 PDF**：无法提取文本，会标记为"无文本内容"

### 使用限制

1. **性能考虑**
   - 大型 PDF 文件（>100MB）可能需要较长的处理时间
   - 同时处理大量文件（>100个）时，请确保有足够的系统资源

2. **编码问题**
   - ✅ 工具已针对 Windows 控制台进行优化，支持中文显示
   - ✅ 输出文件统一使用 UTF-8 编码
   - ⚠️ 在某些非 UTF-8 环境中可能需要额外的编码转换

3. **输出文件**
   - 输出文件默认保存在输入文件夹中
   - 如果同名文件已存在，会被覆盖
   - 建议在处理前备份重要文件

### 常见问题

#### Q1: 提示"未找到任何 PDF 文件"？

**A:** 请检查：
- 文件夹路径是否正确
- 文件夹中是否确实包含 `.pdf` 或 `.PDF` 文件
- 是否有读取该文件夹的权限

#### Q2: 某些 PDF 提取失败或内容为空？

**A:** 可能的原因：
- PDF 是扫描件或图片格式（非文本 PDF）
- PDF 已加密或密码保护
- PDF 文件已损坏
- PDF 使用了特殊的编码格式

#### Q3: 如何处理包含大量文件的文件夹？

**A:**
- 工具会逐个处理文件并显示进度
- 建议先测试小批量文件，确认结果后再批量处理
- 处理大量文件时请确保有足够的磁盘空间

#### Q4: 可以在 Linux 或 macOS 上使用吗？

**A:** 可以！工具是跨平台的：
- Windows: `python pdf_extractor.py -i "path/to/pdfs"`
- Linux/macOS: `python3 pdf_extractor.py -i "path/to/pdfs"`

#### Q5: 如何处理中文文件名的 PDF？

**A:** 工具完全支持中文文件名和路径：
```bash
python pdf_extractor.py -i "C:\文档\PDF文件"
```

---

## 🛠️ 高级用法

### 批处理脚本（Windows）

创建一个批处理文件 `batch_extract.bat`：

```batch
@echo off
echo 正在提取 PDF 文本...
python pdf_extractor.py -i "C:\Documents\PDFs" -f json -o "result"
echo 处理完成！
pause
```

### Shell 脚本（Linux/macOS）

创建一个 shell 脚本 `batch_extract.sh`：

```bash
#!/bin/bash
echo "正在提取 PDF 文本..."
python3 pdf_extractor.py -i "/path/to/pdfs" -f markdown -o "result"
echo "处理完成！"
```

---

## 📂 项目文件说明

```
pdf_processor/
├── pdf_extractor.py              # 主程序（推荐使用）
├── pdf_extractor_learning.py     # 学习版（带详细注释）
├── requirements.txt              # 依赖包列表
├── README.md                     # 项目说明文档（本文件）
└── argparse_demo*.py             # argparse 学习示例
```

---

## 🤝 技术支持

如有问题或建议，欢迎通过以下方式联系：

- 📧 提交 Issue
- 💬 讨论
- 📖 查看代码注释

---

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🌟 致谢

本项目使用了以下优秀的开源库：

- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF 文本提取
- [argparse](https://docs.python.org/3/library/argparse.html) - 命令行参数解析

---

<div align="center">

**如有帮助，请给个 ⭐Star 支持一下！**

Made with ❤️ by PDF Extractor Team

</div>
