# 📊 版本管理指南

本指南说明 Office Agent Workspace 的版本管理系统和演进追踪。

---

## 🎯 版本管理概览

### 核心理念

**增量升级，向后兼容，自动追踪**

```
版本变更
    ↓
1. 自动备份旧版本
    ↓
2. 保留兼容代码
    ↓
3. 记录变更日志
    ↓
4. 生成演进报告
```

### 版本命名规则

```
v{主版本}.{次版本}.{修订版本}

示例:
- v1.0.0  - 首次稳定发布
- v1.1.0  - 新增功能
- v1.1.1  - Bug修复
- v2.0.0  - 重大更新（可能不兼容）
```

---

## 📂 版本管理结构

### 目录组织

```
Office_Agent_Workspace/
├── 02_Project_Archive/
│   └── version_backups/          # 版本备份
│       ├── market_supervision_agent_v1.0/
│       ├── market_supervision_agent_v1.1/
│       └── ...
│
├── 06_Learning_Journal/
│   ├── evolution_log.json        # 演进日志
│   ├── version_registry.json     # 版本注册表
│   ├── version_report_*.md       # 版本报告
│   └── evolution_report_*.md     # 演进报告
│
└── [项目目录]/
    ├── module.py                 # 当前版本
    ├── module_v1.py              # 保留的旧版本
    └── module_v2.py              # 保留的旧版本
```

### 版本注册表

**位置**: [06_Learning_Journal/version_registry.json](../../06_Learning_Journal/version_registry.json)

```json
{
  "current_version": "v4.0",
  "versions": [
    {
      "version": "v1.0",
      "date": "2024-12-01",
      "description": "市场监管智能体初始版本",
      "changes": ["OCR识别", "模板填充", "文档生成"]
    },
    {
      "version": "v2.0",
      "date": "2024-12-15",
      "description": "添加Web界面",
      "changes": ["Flask UI", "文件上传", "实时预览"]
    }
  ]
}
```

---

## 🔄 版本升级流程

### 标准升级流程

```python
# 1. 备份当前版本
backup_current_version()

# 2. 创建新版本
create_new_version()

# 3. 保留旧版本
rename_old_version()

# 4. 更新导入
update_imports()

# 5. 更新配置
update_config()

# 6. 记录变更
log_changes()

# 7. 生成报告
generate_reports()
```

### 示例: 升级市场监管智能体

**步骤1: 备份**
```bash
# 自动备份到归档目录
python 00_Agent_Library/version_manager.py --backup
```

**步骤2: 保留旧代码**
```python
# jinja2_filler_v3.py (旧版本)
# 保留但不删除
```

**步骤3: 创建新版本**
```python
# jinja2_filler.py (新版本)
# 添加新功能
```

**步骤4: 更新演进日志**
```json
{
  "date": "2025-01-14",
  "version": "v4.0",
  "changes": [
    "添加Flask Web界面",
    "集成百度OCR",
    "优化模板引擎"
  ]
}
```

---

## 🛠️ 版本管理工具

### 版本管理器

**位置**: [00_Agent_Library/version_manager.py](../../00_Agent_Library/version_manager.py)

**使用方法**:

```bash
# 生成版本报告
python 00_Agent_Library/version_manager.py

# 备份当前版本
python 00_Agent_Library/version_manager.py --backup

# 查看版本历史
python 00_Agent_Library/version_manager.py --history

# 比较版本差异
python 00_Agent_Library/version_manager.py --diff v1.0 v2.0
```

### 版本管理API

```python
from 00_Agent_Library.version_manager import VersionManager

vm = VersionManager()

# 创建新版本
vm.create_version(
    version="v1.1.0",
    description="添加新功能",
    changes=["功能1", "功能2"]
)

# 获取版本信息
info = vm.get_version_info("v1.0.0")

# 列出所有版本
versions = vm.list_versions()

# 比较版本
diff = vm.compare_versions("v1.0.0", "v1.1.0")
```

---

## 📊 演进追踪

### 演进日志

**位置**: [06_Learning_Journal/evolution_log.json](../../06_Learning_Journal/evolution_log.json)

```json
{
  "project": "Office Agent Workspace",
  "start_date": "2024-12-01",
  "current_version": "v4.0",
  "evolution_history": [
    {
      "date": "2024-12-01",
      "version": "v1.0",
      "milestone": "市场监管智能体初始版本",
      "impact": "high",
      "metrics": {
        "features": 5,
        "test_coverage": "60%",
        "performance": "2s"
      }
    },
    {
      "date": "2025-01-14",
      "version": "v4.0",
      "milestone": "Flask Web UI和百度OCR集成",
      "impact": "high",
      "metrics": {
        "features": 15,
        "test_coverage": "85%",
        "performance": "0.5s"
      }
    }
  ]
}
```

### 生成演进报告

```bash
# 生成演进报告
python 00_Agent_Library/version_manager.py --evolution-report

# 报告保存到
06_Learning_Journal/evolution_report_20250114.md
```

**报告内容**:
- 版本历史
- 功能演进
- 性能变化
- 技术债务
- 改进建议

---

## 🎯 版本兼容性

### 向后兼容策略

```python
# 保留旧版本接口
def old_function():
    """旧版本接口 - 保留兼容"""
    warnings.warn("建议使用new_function", DeprecationWarning)
    return new_function()

def new_function():
    """新版本接口"""
    # 实现逻辑
    pass
```

### 迁移指南

**v3 → v4 迁移**

1. **配置文件格式变更**
```yaml
# v3 格式
ocr_engine: "paddle"

# v4 格式
ocr:
  engine: "baidu"
  api_key: "xxx"
```

2. **API接口变更**
```python
# v3
result = agent.process(file_path)

# v4
result = agent.execute(file_path=file_path, ocr_engine="baidu")
```

---

## 📋 版本发布清单

### 发布前检查

- [ ] 所有测试通过
- [ ] 代码符合规范
- [ ] 文档已更新
- [ ] 向后兼容
- [ ] 性能测试
- [ ] 安全审查

### 发布步骤

1. **创建版本标签**
```bash
git tag -a v4.0 -m "版本v4.0发布"
git push origin v4.0
```

2. **生成版本报告**
```bash
python 00_Agent_Library/version_manager.py --version-report
```

3. **更新文档**
- 更新 CLAUDE.md
- 更新 CHANGELOG.md
- 更新版本号

4. **发布通知**
- 发送发布说明
- 更新工作区索引

---

## 🔍 版本诊断

### 查看版本信息

```bash
# 查看当前版本
python --version
pip show office-agent-workspace

# 查看所有版本
python 00_Agent_Library/version_manager.py --list-versions

# 查看版本详情
python 00_Agent_Library/version_manager.py --version-info v4.0
```

### 版本回滚

```bash
# 回滚到指定版本
python 00_Agent_Library/version_manager.py --rollback v3.0

# 或手动恢复
cp 02_Project_Archive/version_backups/v3.0/* 01_Active_Projects/
```

---

## 💡 最佳实践

### 1. 版本命名

```
✅ 好的版本号
- v1.0.0 (首次发布)
- v1.1.0 (新增功能)
- v1.1.1 (Bug修复)

❌ 避免
- v1 (不完整)
- v1.0 (缺少修订号)
- latest (不明确)
```

### 2. 变更记录

```
✅ 好的变更记录
- "添加Flask Web界面"
- "集成百度OCR API"
- "优化响应时间从2s到0.5s"

❌ 避免
- "更新代码"
- "修复bug"
- "改进"
```

### 3. 备份策略

```
✅ 推荐
- 每次发布前自动备份
- 保留最近5个版本
- 重要版本单独归档

❌ 避免
- 覆盖旧备份
- 删除历史版本
```

---

## 📚 相关文档

- [演进系统说明](../../00_Agent_Library/EVOLUTION_GUIDE.md)
- [完整系统指南](../../COMPLETE_SYSTEM_GUIDE.md)
- [问题排查](../TROUBLESHOOTING.md)

---

**最后更新**: 2026-01-14
