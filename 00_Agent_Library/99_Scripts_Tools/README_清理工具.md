# 工作区清理工具使用说明

## 📋 功能概述

`workspace_cleaner.py` 是一个智能工作区清理工具，可以自动：

1. 🗑️ 清理 Python 缓存（`__pycache__` 和 `.pyc` 文件）
2. 📁 整理根目录的脚本文件到 `00_Agent_Library/99_Scripts_Tools/`
3. 📚 整理根目录的文档到 `00_Agent_Library/01_Documentation/`
4. 🗑️ 删除临时文件（如 `nul` 文件）
5. 📋 **自动归档超过 30 天的旧报告** ✨

---

## 🚀 使用方法

### 基本用法

```bash
# 演习模式（默认）- 查看会清理什么，但不实际执行
python workspace_cleaner.py

# 实际执行模式 - 真正清理文件
python workspace_cleaner.py --execute
```

### 自定义报告保留天数

```bash
# 只保留最近 7 天的报告
python workspace_cleaner.py --execute --retention 7

# 保留最近 60 天的报告
python workspace_cleaner.py --execute --retention 60

# 保留最近 90 天的报告
python workspace_cleaner.py --execute --retention 90
```

---

## 📋 旧报告自动归档功能

### 工作原理

1. **查找旧报告**: 扫描工作区根目录，查找以下模式的报告：
   - `清理报告_YYYYMMDD_HHMMSS.md`
   - `维护报告_YYYYMMDD_HHMMSS.md`
   - `工作区健康报告_YYYYMMDD_HHMMSS.md`

2. **计算日期**: 从文件名中提取日期，计算报告的年龄

3. **归档旧报告**: 将超过保留天数的报告移动到：
   ```
   06_Learning_Journal/workspace_memory/old_reports/
   ```

4. **保留新报告**: 最近的报告（默认 30 天内）保留在根目录

### 默认配置

- **保留天数**: 30 天
- **归档位置**: `06_Learning_Journal/workspace_memory/old_reports/`
- **支持的报告类型**: 清理报告、维护报告、健康报告

---

## 📊 执行效果

### 演习模式输出示例

```
============================================================
📋 清理旧报告 (超过 30 天)
============================================================

找到 3 个旧报告:
  • 清理报告_20251201_072943.md (37 天前, 2.15 KB)
  • 维护报告_20251205_082444.md (33 天前, 3.42 KB)
  • 清理报告_20251210_073100.md (28 天前, 1.98 KB)
  *... 还有 0 个*

总大小: 7.55 KB

🔍 [演习模式] 将归档/删除 3 个旧报告:
  → 移动到归档目录: 06_Learning_Journal\workspace_memory\old_reports\
```

### 实际执行模式输出

```
⚠️  正在归档旧报告...
✅ 已归档 3 个旧报告
```

---

## 📁 文件组织结构

### 清理前
```
Office_Agent_Workspace/
├── 清理报告_20251201_072943.md  ← 旧报告（37天前）
├── 清理报告_20260107_072943.md  ← 新报告（今天）
├── 清理报告_20260107_073100.md  ← 新报告（今天）
└── ...
```

### 清理后
```
Office_Agent_Workspace/
├── 清理报告_20260107_072943.md  ← 保留在根目录
├── 清理报告_20260107_073100.md  ← 保留在根目录
└── 06_Learning_Journal/
    └── workspace_memory/
        └── old_reports/         ← 旧报告归档到这里
            ├── 清理报告_20251201_072943.md
            ├── 维护报告_20251205_082444.md
            └── ...
```

---

## 💡 最佳实践

### 1. 定期清理建议

```bash
# 每周运行一次（演习模式查看）
python workspace_cleaner.py

# 每月运行一次（实际执行）
python workspace_cleaner.py --execute
```

### 2. 不同保留天数的选择

| 场景 | 保留天数 | 命令 |
|------|----------|------|
| **频繁清理，只保留最近的** | 7 天 | `--retention 7` |
| **标准使用（推荐）** | 30 天 | `--retention 30` (默认) |
| **长期保存历史记录** | 60-90 天 | `--retention 60` |
| **几乎不删除** | 180+ 天 | `--retention 180` |

### 3. 归档报告的管理

如果归档目录变得太大，可以手动清理：

```bash
# 删除整个归档目录（谨慎！）
rm -rf 06_Learning_Journal/workspace_memory/old_reports/

# 或者只删除超过 1 年的归档报告
# （可以添加到维护工具中）
```

---

## 🔧 高级用法

### 查看会归档哪些报告（不执行）

```bash
python workspace_cleaner.py
# 查看输出中的 "📋 清理旧报告" 部分
```

### 只清理缓存，不归档报告

如果想暂时禁用报告归档功能，可以：
- 注释掉代码中的 `self.cleanup_old_reports()` 调用
- 或者将保留天数设置得非常大（如 3650 天）

---

## ⚙️ 配置选项

### 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--execute` | 实际执行模式（默认是演习模式） | `python workspace_cleaner.py --execute` |
| `--retention N` | 设置报告保留天数（默认 30） | `--retention 7` |

### 代码配置

在 `workspace_cleaner.py` 中可以修改：

```python
# 第 41 行
self.report_retention_days = 30  # 默认保留天数

# 第 38 行
self.archive_dir = self.workspace_path / "06_Learning_Journal" / "workspace_memory" / "old_reports"  # 归档目录
```

---

## 📝 清理报告内容

每次运行后会生成一个清理报告，包含：

```markdown
## 📊 清理统计

- **删除的缓存目录**: 0
- **删除的 .pyc 文件**: 0
- **释放的空间**: 0.00 B
- **移动的文件**: 0
- **归档的旧报告**: 3 (超过 30 天)  ← 新增
```

---

## ❓ 常见问题

### Q: 会删除重要的新报告吗？
**A**: 不会。只归档超过保留天数的报告，最近 30 天（默认）的报告不会动。

### Q: 归档后的报告还能找回吗？
**A**: 可以。归档只是移动文件，不是删除。位置在 `06_Learning_Journal/workspace_memory/old_reports/`。

### Q: 如何彻底删除旧报告？
**A**: 如果确认不需要旧报告，可以手动删除归档目录，或修改代码将 `shutil.move` 改为 `os.remove`。

### Q: 可以分别设置不同报告类型的保留天数吗？
**A**: 当前版本不支持统一设置，但可以轻松修改代码实现。

### Q: 演习模式安全吗？
**A**: 非常安全。演习模式不会删除、移动或修改任何文件，只会显示将会做什么。

---

## 🎯 使用场景

### 场景 1: 日常维护

```bash
# 每周一次演习，查看工作区状态
python workspace_cleaner.py
```

### 场景 2: 月度大扫除

```bash
# 每月实际执行，清理缓存和归档旧报告
python workspace_cleaner.py --execute
```

### 场景 3: 项目完成后清理

```bash
# 项目完成后，只保留 7 天的报告
python workspace_cleaner.py --execute --retention 7
```

### 场景 4: 长期归档

```bash
# 保留 90 天的报告，方便追溯
python workspace_cleaner.py --execute --retention 90
```

---

## ✅ 更新日志

### 2026-01-07
- ✅ 新增自动归档旧报告功能
- ✅ 支持自定义保留天数（`--retention` 参数）
- ✅ 在清理报告中显示归档统计
- ✅ 演习模式也会显示将要归档的报告

---

**总结**: 现在清理工具会自动管理报告的生命周期，保持工作区整洁，同时保留历史记录供查阅！🎉
