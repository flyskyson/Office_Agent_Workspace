# 已处理文件存储目录

此目录用于存放已成功处理的业务数据。

## 目录结构

```
processed/
├── 2024-01-15/
│   ├── annual_report_北京示例科技有限公司_success.json
│   └── annual_report_上海示例贸易有限公司_success.json
├── 2024-01-16/
└── success/
    └── summary.json  # 处理成功汇总
```

## 文件命名规范

- 年报: `annual_report_{公司名}_{状态}.json`
- 设立登记: `registration_{公司名}_{状态}.json`
- 变更登记: `change_{公司名}_{状态}.json`

状态包括:
- `success`: 处理成功
- `failed`: 处理失败
- `pending`: 待处理
