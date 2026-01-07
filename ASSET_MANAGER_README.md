# 资产盘点工具快速开始指南

##  使用方法

### 方式1: 交互式模式 (推荐)

```bash
python asset_manager.py
```

然后输入命令:
- `dashboard` - 查看资产总览
- `projects` - 查看活跃项目
- `archived` - 查看归档项目
- `tools` - 查看工具脚本
- `recent [天数]` - 查看最近更新
- `health` - 健康检查
- `refresh` - 刷新索引
- `help` - 查看帮助
- `quit` - 退出

### 方式2: 快捷启动

双击运行: `查看我的资产.bat`

### 方式3: 命令行模式

```bash
python asset_manager.py --dashboard      # 查看总览
python asset_manager.py --projects       # 查看项目
python asset_manager.py --tools          # 查看工具
python asset_manager.py --health         # 健康检查
python asset_manager.py --refresh        # 刷新索引
```

---

## 常见使用场景

### 场景1: 每天开始工作

```bash
python asset_manager.py
> dashboard      # 查看总览
> recent 7       # 本周更新
```

### 场景2: 找遗忘的代码

```bash
python asset_manager.py
> projects       # 查看项目列表
> tools          # 查看工具
```

### 场景3: 每周盘点

```bash
python asset_manager.py
> dashboard      # 总览
> health         # 健康检查
> refresh        # 刷新数据
```

---

## 注意事项

1. 如果数据不准确,运行 `refresh` 刷新索引
2. 首次使用前确保运行过 `workspace_scanner.py`
3. 建议每周至少刷新一次索引

---

**详细文档**: 请查看 `资产盘点完全指南.md`
