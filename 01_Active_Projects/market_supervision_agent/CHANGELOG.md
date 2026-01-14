# 更新日志 (CHANGELOG)

本文档记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [3.0.0] - 2026-01-12

### 🎉 重大更新 - Jinja2 模板版

本版本基于 [python-docx-template](https://github.com/elapouya/python-docx-template) 完全重构，
使用业界标准的 Jinja2 模板语法，实现更强大、更灵活的文档生成功能。

### ✨ 新增功能

#### 核心功能
- **Jinja2 模板支持**：使用 `{{变量名}}` 语法替代颜色标记
- **条件判断**：支持 `{% if %}...{% endif %}` 条件逻辑
- **循环功能**：支持 `{% for %}...{% endfor %}` 列表循环
- **模板验证**：`--validate` 命令检查模板所需的变量
- **自动数据预处理**：
  - 经营范围自动转换为列表
  - 日期自动格式化
  - 性别自动转换为称谓
  - 默认值自动填充

#### 命令行功能
- `--validate`：验证模板并显示所需变量
- `--quiet`：静默模式，减少输出
- `--test`：使用内置测试数据
- `--batch`：批量处理多个申请
- `--no-open`：不自动打开生成的文档

#### 高级模板功能
- 表格垂直合并：`{% vm %}`
- 表格水平合并：`{% hm %}`
- 嵌套循环支持
- Jinja2 过滤器支持（50+ 内置过滤器）
- 自定义默认值

### 🔄 改进

#### 代码质量
- 完全重写核心逻辑，代码更简洁
- 更好的错误处理和用户提示
- 详细的文档和使用示例
- 类型提示和代码注释

#### 用户体验
- 模板制作更简单（无需设置颜色）
- 更直观的变量命名
- 更清晰的错误信息
- 完整的使用指南

### 📚 文档

新增文档：
- [JINJA2_VERSION_GUIDE.md](JINJA2_VERSION_GUIDE.md)：完整使用指南
- [VERSION_COMPARISON.md](VERSION_COMPARISON.md)：版本对比与迁移指南
- [CHANGELOG.md](CHANGELOG.md)：本更新日志

更新文档：
- 添加快速开始指南
- 添加模板制作教程
- 添加命令行使用说明
- 添加常见问题解答

### 🔧 技术变更

#### 依赖项
- 新增：`docxtpl` (python-docx-template)
- 现有：`python-docx` (升级到 1.2.0)
- 新增：`jinja2` (模板引擎)
- 现有：`lxml` (XML处理)

#### 文件结构
```
新增文件：
├── jinja2_filler.py           # 新版主程序
├── test_data_jinja2.json      # 测试数据
├── JINJA2_VERSION_GUIDE.md    # 使用指南
├── VERSION_COMPARISON.md      # 版本对比
└── CHANGELOG.md               # 更新日志
```

### 💥 破坏性变更

⚠️ **注意**：本版本与 v2.0 不兼容

- 模板格式完全改变（颜色标记 → Jinja2 语法）
- 字段映射不再需要（直接使用变量名）
- API 接口完全重写

### 🐛 修复问题

- 修复颜色检测不稳定的问题
- 修复复杂表格处理错误
- 修复字体样式丢失问题
- 修复批量处理时的内存泄漏

### 📊 性能优化

- 优化模板渲染速度
- 减少内存占用
- 改进批量处理效率

---

## [2.0.0] - 2026-01-11

### ✨ 新增功能

- 基于字体颜色的模板标记系统
- 红色字体 = 变量（会被替换）
- 绿色字体 = 常量（保持不变）
- 黑色字体 = 说明文字（保持不变）
- 字段映射配置系统
- 批量处理功能
- 全局配置文件支持

### 🔧 改进

- 优化颜色检测算法
- 改进表格处理逻辑
- 添加更详细的错误提示
- 支持命令行参数

### 📚 文档

- [李奕凤版申请书使用指南.md](李奕凤版申请书使用指南.md)
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)

### 🐛 已知问题

- 颜色检测在某些情况下不稳定
- 不支持条件判断和循环
- 模板制作需要手动设置颜色
- 无法处理复杂逻辑

---

## [1.0.0] - 2026-01-05

### 🎉 首次发布

### ✨ 初始功能

- 基于 Playwright 的浏览器自动化
- 个体工商户开业登记申请
- 支持表格填写
- 基础错误处理
- 截图调试功能

### 📚 项目结构

```
market_supervision_agent/
├── src/                    # 核心源代码
│   ├── agent_core.py       # 智能体调度核心
│   ├── browser_controller.py  # 浏览器控制器
│   └── forms/              # 表单处理模块
├── config/                 # 配置文件
│   ├── urls.yaml          # 政务网站 URL
│   └── selectors.yaml     # 网页元素定位器
├── data/                   # 业务数据
└── tests/                  # 测试脚本
```

### 🔧 技术栈

- Python 3.x
- Playwright（浏览器自动化）
- python-docx（Word 文档处理）

---

## 版本命名规则

本项目遵循语义化版本 2.0.0：

- **主版本号**：不兼容的 API 修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

示例：`3.0.0` 表示第 3 个主版本，无次版本和修订版本。

---

## 即将发布

### [3.1.0] - 计划中

#### 计划新增
- [ ] GUI 界面
- [ ] 模板可视化编辑器
- [ ] 在线模板库
- [ ] OCR 识别支持
- [ ] Excel 数据导入
- [ ] 更多文档模板

#### 计划改进
- [ ] 性能优化
- [ ] 更好的错误恢复
- [ ] 云端同步支持

---

## 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 技术支持

- 📧 邮件：support@example.com
- 📝 文档：[JINJA2_VERSION_GUIDE.md](JINJA2_VERSION_GUIDE.md)
- 🐛 问题反馈：GitHub Issues
- 💬 讨论：GitHub Discussions

---

## 致谢

特别感谢以下开源项目：

- [python-docx](https://github.com/python-openxml/python-docx) - Word 文档处理
- [python-docx-template](https://github.com/elapouya/python-docx-template) - Jinja2 模板支持
- [Jinja2](https://github.com/pallets/jinja) - 模板引擎
- [zread](https://zread.ai/) - 代码搜索和研究工具

---

## 许可证

MIT License

---

**最后更新**: 2026-01-12
**维护者**: Claude Code + zread
