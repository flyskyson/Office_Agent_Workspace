# 项目名称

## 描述
这是一个智能文件整理助手项目，能够自动将文件夹中的文件按照类型分类整理到不同的子文件夹中。

## 功能特性

### 当前功能
- 自动识别并分类文件类型（PDF、图片、办公文档等）
- 自动创建分类文件夹
- 处理重复文件名（自动重命名）
- 详细的操作日志记录
- 用户确认机制

### 计划功能
- 支持更多文件类型
- 自定义分类规则
- 撤销操作功能

## 安装说明

### 环境要求
- Python 3.7+

### 安装步骤

1. 克隆项目到本地
```bash
git clone <项目地址>
cd my_first_agent
```

2. 创建虚拟环境（推荐）
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

1. 配置要整理的文件夹路径（编辑 `organizer.py` 中的 `folder_to_organize` 变量）

2. 运行程序
```bash
python organizer.py
```

3. 按照提示确认是否开始整理

### 配置说明

默认分类规则：
- PDF文件 → `PDF/` 文件夹
- 图片文件 (.jpg, .png) → `Images/` 文件夹
- 办公文档 (.docx, .xlsx, .doc) → `Documents/` 文件夹

可以在 `organizer.py` 中修改 `file_categories` 字典来自定义分类规则。

### 示例

```python
file_categories = {
    "PDF": [".pdf"],
    "Images": [".jpg", ".png"],
    "Documents": [".docx", ".xlsx", ".doc"]
}
```

## 文件结构

```
my_first_agent/
├── main.py                 # 主程序入口
├── organizer.py            # 核心整理逻辑
├── organizer_with_log.py   # 带日志版本的整理器
├── organizer01.py          # 备用版本
├── test_folder/            # 测试文件夹
├── organizer_log.txt       # 操作日志（自动生成）
├── requirements.txt        # 依赖列表
├── .gitignore             # Git忽略配置
└── README.md              # 项目说明文档
```

## 更新日志

### [待发布]
- 初始版本发布

### [1.0.0] - 2024-XX-XX
- 实现基础文件整理功能
- 添加日志记录功能
- 实现重复文件名处理
- 添加用户确认机制

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 作者

flyskyson

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件

## 致谢

感谢所有贡献者的支持！
