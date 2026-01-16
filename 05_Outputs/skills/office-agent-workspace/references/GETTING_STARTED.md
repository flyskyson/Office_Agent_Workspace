# 🚀 快速入门指南

欢迎来到 **Office Agent Workspace**！这是一个智能办公自动化工具集，帮助您高效处理市场监管、文档管理、知识整理等任务。

---

## 📋 系统要求

### 必需环境
- **Python**: 3.9 或更高版本（推荐 3.12）
- **操作系统**: Windows 10/11
- **内存**: 至少 4GB RAM（推荐 8GB+）
- **磁盘空间**: 至少 2GB 可用空间

### 可选工具
- **Git**: 用于版本控制
- **VSCode**: 推荐的代码编辑器
- **Chrome/Edge**: 浏览器（用于 Playwright）

---

## 🔄 安装步骤

### 1️⃣ 克隆或下载项目

```bash
# 如果使用 Git
git clone <repository-url>
cd Office_Agent_Workspace

# 或直接下载并解压 ZIP 文件
```

### 2️⃣ 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate  # Windows
```

### 3️⃣ 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 4️⃣ 验证安装

```bash
# 测试市场监管智能体
python 01_Active_Projects/market_supervision_agent/jinja2_filler.py --test

# 测试记忆助手
python 01_Active_Projects/memory_agent/memory_agent.py --test
```

---

## 🎯 首次使用

### 方式A: 使用统一启动器（推荐）

1. 双击 `启动_OA_Studio.bat` 文件
2. 或在命令行运行:
   ```bash
   python office_agent_studio.py
   ```
3. 按照菜单提示选择工具

### 方式B: 直接启动各工具

#### 市场监管智能体

```bash
python 01_Active_Projects/market_supervision_agent/ui/flask_app.py
```

然后在浏览器访问: **http://127.0.0.1:5000**

**功能**:
- 上传营业执照图片
- 自动识别信息
- 生成申请书
- 下载 Word 文档

#### 记忆助手

```bash
streamlit run 01_Active_Projects/memory_agent/ui/app.py
```

然后在浏览器访问: **http://localhost:8501**

**功能**:
- 添加学习笔记
- 语义搜索
- 间隔复习提醒

#### 文件整理工具

```bash
python 01_Active_Projects/file_organizer/file_organizer.py
```

**功能**:
- 按类型整理文件
- 按日期归档
- 关键词分类

---

## 📚 核心概念

### 智能体 (Agent)

智能体是**封装好的自动化工具**，每个智能体负责特定任务：

| 智能体 | 主要功能 | 适用场景 |
|--------|---------|---------|
| **市场监管智能体** | 营业执照 OCR + 申请书生成 | 个体工商户开业登记 |
| **记忆助手** | 知识管理 + 语义搜索 | 学习笔记整理 |
| **文件整理工具** | 智能文件分类 | 证照材料归档 |

### 技能 (Skill)

**技能系统**让您通过自然语言触发特定任务：

```bash
# 示例对话
您: "帮我生成个体工商户申请书"
Claude: 自动激活申请书生成技能
```

可用技能:
- 💡 **想法落地**: 从模糊想法到可用产品
- 🏠 **超级管家**: 统一工作区管理
- 📄 **申请书生成**: OCR识别 + 模板填充
- 📁 **证照整理**: 智能分类归档
- 🔍 **知识索引**: 向量化笔记搜索

---

## 🎓 学习路径

### 初级（5分钟）

1. ✅ 阅读 [CLAUDE.md](../CLAUDE.md) - 了解项目结构
2. ✅ 运行 `office_agent_studio.py` - 熟悉统一界面
3. ✅ 尝试启动市场监管智能体 - 体验核心功能

### 中级（30分钟）

1. ✅ 阅读 [ARCHITECTURE.md](ARCHITECTURE.md) - 理解系统架构
2. ✅ 查看 [CODING_STANDARDS.md](CODING_STANDARDS.md) - 学习编码规范
3. ✅ 尝试修改配置文件 - 自定义工具行为

### 高级（2小时）

1. ✅ 学习 [guides/AGENT_DEVELOPMENT.md](guides/AGENT_DEVELOPMENT.md) - 开发新智能体
2. ✅ 阅读 [guides/SKILLS_SYSTEM.md](guides/SKILLS_SYSTEM.md) - 理解技能系统
3. ✅ 实践 [guides/IDEA_WORKFLOW.md](guides/IDEA_WORKFLOW.md) - 从想法到产品

---

## 💡 常用操作

### 启动工具

```bash
# 统一启动器
python office_agent_studio.py

# 市场监管智能体
python 01_Active_Projects/market_supervision_agent/ui/flask_app.py

# 记忆助手
streamlit run 01_Active_Projects/memory_agent/ui/app.py

# 文件整理工具
python 01_Active_Projects/file_organizer/file_organizer.py
```

### 测试功能

```bash
# 测试市场监管智能体
python 01_Active_Projects/market_supervision_agent/jinja2_filler.py --test

# 测试记忆助手
python 01_Active_Projects/memory_agent/memory_agent.py --test

# 测试想法落地工作流
python 00_Agent_Library/idea_workflow_engine.py
```

### 工作区维护

```bash
# 扫描并索引工作区
python workspace_scanner.py

# 清理缓存和临时文件
python workspace_cleaner.py

# 生成工作区报告
python workspace_report.py

# 创建快照
python create_snapshot.py
```

---

## 🐛 遇到问题?

### 快速诊断

1. **中文乱码** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md#中文乱码)
2. **Flask 启动失败** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md#flask-启动失败)
3. **OCR 识别错误** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md#ocr-识别错误)
4. **依赖安装失败** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md#依赖安装失败)

### 获取帮助

- 📖 查看 [完整系统指南](../COMPLETE_SYSTEM_GUIDE.md)
- 🤖 使用超级管家: 说"超级管家"获取帮助
- 📚 查阅专题文档: [docs/](.)

---

## 🎯 下一步

现在您已经完成了基础设置，可以:

1. **使用工具**: 开始使用各智能体处理实际任务
2. **定制配置**: 根据需求修改配置文件
3. **扩展功能**: 开发新的智能体或技能
4. **深入学习**: 阅读详细文档了解系统原理

---

## 📞 联系方式

- **项目维护**: 使用 Claude Code (GLM-4.7) + VSCode 插件
- **更新策略**: 增量升级，向后兼容
- **版本追踪**: 自动化演进管理系统

**祝您使用愉快！** 🎉
