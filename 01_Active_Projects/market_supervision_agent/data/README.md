# 数据目录说明

## 目录结构

```
data/
├── sample_customers.json    # 客户数据示例（年报）
├── processed/               # 已处理文件存储
│   ├── YYYY-MM-DD/         # 按日期组织
│   └── success/            # 成功处理的记录
└── screenshots/             # 截图保存目录
```

## 数据格式说明

### 企业年报数据格式 (sample_customers.json)

```json
{
  "company_name": "企业名称",
  "credit_code": "统一社会信用代码",
  "password": "登录密码",
  "year": 2024,
  "company_type": "企业类型",
  "registered_capital": 1000000,
  "business_address": "经营地址",
  "postal_code": "邮政编码",
  "phone": "联系电话",
  "email": "电子邮箱",
  "financial_data": {
    "total_assets": 5000000,
    "total_liabilities": 2000000,
    "total_revenue": 3000000,
    "net_profit": 500000,
    "tax_paid": 150000
  }
}
```

### 企业设立登记数据格式

```json
{
  "company_name": "企业名称",
  "company_type": "企业类型",
  "registered_capital": 1000000,
  "business_scope": "经营范围",
  "legal_representative": {
    "name": "法定代表人姓名",
    "id_card": "身份证号"
  },
  "shareholders": [
    {
      "name": "股东姓名",
      "id_card": "身份证号",
      "investment": 600000,
      "ratio": 60
    }
  ],
  "documents": {
    "application_form": "path/to/application.pdf",
    "id_card_copy": "path/to/id_card.pdf"
  }
}
```

### 企业变更登记数据格式

```json
{
  "company_name": "企业名称",
  "credit_code": "统一社会信用代码",
  "change_type": "name_change",
  "change_data": {
    "new_name": "新企业名称",
    "reason": "变更原因"
  },
  "documents": {
    "change_application": "path/to/change_app.pdf",
    "board_resolution": "path/to/resolution.pdf"
  }
}
```

## 注意事项

1. **敏感信息**:
   - 示例文件中的密码需要替换为实际密码
   - 不要将包含真实密码的文件提交到版本控制

2. **数据验证**:
   - 运行前请确保所有必填字段已填写
   - 金额单位为元（人民币）

3. **文件路径**:
   - 文档路径支持相对路径和绝对路径
   - 建议使用绝对路径避免错误

4. **已处理文件**:
   - 成功处理后会自动移动到 `processed/` 目录
   - 按日期归档便于追溯
