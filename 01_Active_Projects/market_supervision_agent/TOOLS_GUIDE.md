# 工具使用指南

> **市场监管智能体项目 - 完整工具使用文档**
>
> 版本: v3.0 | 更新日期: 2026-01-12

---

## 📋 目录

1. [工具概览](#工具概览)
2. [主程序 - jinja2_filler.py](#主程序)
3. [配置管理 - config_manager.py](#配置管理)
4. [数据验证 - data_validator.py](#数据验证)
5. [快速启动菜单](#快速启动菜单)
6. [常见工作流程](#常见工作流程)
7. [故障排除](#故障排除)

---

## 🎯 工具概览

本项目提供以下工具：

| 工具 | 文件名 | 功能 |
|------|--------|------|
| **主程序** | `jinja2_filler.py` | 生成申请书 |
| **配置管理** | `config_manager.py` | 管理项目配置 |
| **数据验证** | `data_validator.py` | 验证数据完整性 |
| **快速启动** | `快速启动.bat` | 图形化菜单界面 |

---

## 🔧 主程序

### 基本用法

```bash
# 查看帮助
python jinja2_filler.py --help

# 测试模式（使用内置测试数据）
python jinja2_filler.py --test

# 从JSON文件生成
python jinja2_filler.py --data my_data.json

# 批量生成
python jinja2_filler.py --batch batch_data.json

# 验证模板
python jinja2_filler.py --validate template.docx
```

### 高级选项

```bash
# 指定模板文件
python jinja2_filler.py --template my_template.docx --data data.json

# 指定输出目录
python jinja2_filler.py --data data.json --output my_output

# 不自动打开文档
python jinja2_filler.py --data data.json --no-open

# 静默模式（减少输出）
python jinja2_filler.py --data data.json --quiet
```

### 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--data` | 指定JSON数据文件 | `--data data.json` |
| `--batch` | 批量处理模式 | `--batch list.json` |
| `--template` | 指定模板文件 | `--template tpl.docx` |
| `--output` | 指定输出目录 | `--output out` |
| `--test` | 使用测试数据 | `--test` |
| `--validate` | 验证模板 | `--validate tpl.docx` |
| `--no-open` | 不自动打开 | `--no-open` |
| `--quiet` | 静默模式 | `--quiet` |

---

## ⚙️ 配置管理

### 查看配置

```bash
python config_manager.py --show
```

显示内容：
- 常量配置（邮政编码、身份证件类型等）
- 默认值配置（经营范围、经营期限等）
- 数据模板示例

### 编辑配置

```bash
python config_manager.py --edit
```

交互式编辑流程：
1. 选择要编辑的配置部分
2. 逐项修改配置值
3. 确认保存

### 重置配置

```bash
python config_manager.py --reset
```

将配置恢复为默认值。

### 导出/导入配置

```bash
# 导出配置
python config_manager.py --export

# 导出到指定文件
python config_manager.py --export my_config.json

# 从文件导入
python config_manager.py --import my_config.json
```

### 验证配置

```bash
python config_manager.py --validate
```

检查配置文件格式是否正确。

### 创建新数据文件

```bash
python config_manager.py --new-data
```

根据配置模板创建新的数据文件。

### 配置文件结构

```json
{
  "_说明": "全局配置文件",
  "_版本": "v3.0",
  "constants": {
    "postal_code": "537820",
    "id_card_type": "身份证",
    "region": "广西壮族自治区玉林市兴业县蒲塘镇"
  },
  "defaults": {
    "business_scope_licensed": "小餐饮",
    "business_scope_general": "食品销售（仅销售预包装食品）",
    "operation_period": "长期"
  },
  "data_template": {
    "business_name": "示例：张三便利店",
    "operator_name": "示例：张三"
  }
}
```

---

## ✅ 数据验证

### 验证单个数据文件

```bash
python data_validator.py data.json
```

输出示例：
```
==================================================================
数据验证报告
==================================================================

个体工商户名称: 张三便利店
经营者姓名: 张三

✅ 没有发现错误
⚠️  发现 1 个警告:
  1. [email] 邮箱格式可能不正确: test@
     值: test@

------------------------------------------------------------------
⚠️  数据存在警告，但仍可使用
==================================================================
```

### 严格模式

```bash
python data_validator.py data.json --strict
```

启用更多检查项：
- 姓名长度检查
- 地址长度检查
- 更多业务规则

### 批量验证

```bash
python data_validator.py batch_data.json --batch
```

验证包含多条数据的文件。

输出总结：
```
批量验证总结
==================================================================
总计: 10 条
通过: 8 条
失败: 2 条
==================================================================
```

### 保存验证报告

```bash
python data_validator.py data.json --save-report
```

生成详细的验证报告JSON文件。

### 验证项目

**必填字段检查：**
- business_name（个体工商户名称）
- operator_name（经营者姓名）
- phone（联系电话）
- business_address（经营场所）
- id_card（身份证号）
- gender（性别）

**格式检查：**
- 手机号格式（1开头的11位数字）
- 身份证号格式（18位，含校验码）
- 邮箱格式（如果提供）
- 邮政编码格式（6位数字）

**一致性检查：**
- 性别值（男/女）
- 文化程度（常见学历）

**业务规则检查：**
- 注册资金必须为数字
- 从业人数必须为数字

---

## 🚀 快速启动菜单

双击运行 `快速启动.bat` 文件，进入图形化菜单界面：

```
╔════════════════════════════════════════════════════════════╗
║       个体工商户开业登记申请书填充工具 v3.0               ║
║            Jinja2 模板版 - 快速启动菜单                    ║
╚════════════════════════════════════════════════════════════╝

【主要功能】

  1. 生成申请书（使用测试数据）
  2. 生成申请书（从JSON文件）
  3. 批量生成申请书
  4. 验证数据文件

【工具功能】

  5. 查看当前配置
  6. 编辑配置
  7. 创建新数据文件
  8. 验证模板

【其他】

  9. 查看使用指南
  0. 退出
```

### 使用提示

1. **首次使用**：选择选项1（测试模式）了解工具
2. **快速生成**：选择选项2，直接拖放JSON文件
3. **批量处理**：选择选项3，批量生成多个申请书
4. **配置管理**：选择选项5或6管理配置

---

## 📚 常见工作流程

### 工作流1：首次使用

```bash
# 1. 测试运行
python jinja2_filler.py --test

# 2. 查看配置
python config_manager.py --show

# 3. 创建新数据文件
python config_manager.py --new-data

# 4. 生成申请书
python jinja2_filler.py --data new_data_20260112_120000.json
```

### 工作流2：批量处理

```bash
# 1. 准备批量数据文件
# 创建 batch_data.json，包含多条数据

# 2. 验证数据
python data_validator.py batch_data.json --batch

# 3. 批量生成
python jinja2_filler.py --batch batch_data.json
```

### 工作流3：自定义模板

```bash
# 1. 创建Word模板，添加变量
# 2. 验证模板
python jinja2_filler.py --validate my_template.docx

# 3. 使用新模板
python jinja2_filler.py --template my_template.docx --data data.json
```

### 工作流4：配置管理

```bash
# 1. 查看当前配置
python config_manager.py --show

# 2. 编辑配置
python config_manager.py --edit

# 3. 导出配置备份
python config_manager.py --export config_backup.json

# 4. 使用新配置
python jinja2_filler.py --test
```

---

## 🔧 故障排除

### 问题1：模块未找到

**错误信息**：
```
ModuleNotFoundError: No module named 'docxtpl'
```

**解决方案**：
```bash
pip install docxtpl
```

### 问题2：模板变量未替换

**可能原因**：
1. 变量名不匹配
2. 数据中缺少该字段

**解决方案**：
```bash
# 1. 验证模板需要的变量
python jinja2_filler.py --validate template.docx

# 2. 检查数据文件
python data_validator.py data.json
```

### 问题3：编码问题

**错误信息**：
```
UnicodeDecodeError: 'gbk' codec can't decode
```

**解决方案**：
- 确保JSON文件保存为UTF-8编码
- 在记事本中"另存为"，选择"UTF-8"编码

### 问题4：文档打开失败

**可能原因**：
- 输出目录不存在
- 文件被占用

**解决方案**：
```bash
# 指定输出目录
python jinja2_filler.py --data data.json --output output

# 不自动打开
python jinja2_filler.py --data data.json --no-open
```

### 问题5：数据验证失败

**解决方案**：
```bash
# 使用严格模式查看详细错误
python data_validator.py data.json --strict

# 保存验证报告
python data_validator.py data.json --save-report

# 查看报告文件
# 生成的 *_validation_report.json 文件包含详细错误信息
```

---

## 💡 最佳实践

### 1. 数据准备

- ✅ 使用UTF-8编码保存JSON文件
- ✅ 验证数据后再生成文档
- ✅ 使用配置管理工具创建数据模板

### 2. 模板制作

- ✅ 先用简单变量测试
- ✅ 使用 `--validate` 检查模板
- ✅ 保存多个版本的模板

### 3. 批量处理

- ✅ 先验证所有数据
- ✅ 使用 `--no-open` 避免打开过多文档
- ✅ 检查批量验证报告

### 4. 配置管理

- ✅ 定期导出配置备份
- ✅ 使用注释说明配置项
- ✅ 保持配置文件简洁

---

## 📞 技术支持

### 自助诊断

1. **查看日志**：程序输出包含详细的错误信息
2. **验证数据**：使用 `data_validator.py` 检查数据
3. **验证模板**：使用 `--validate` 检查模板
4. **查看配置**：使用 `config_manager.py --show`

### 获取帮助

```bash
# 查看主程序帮助
python jinja2_filler.py --help

# 查看配置管理帮助
python config_manager.py --help

# 查看数据验证帮助
python data_validator.py --help
```

### 文档资源

- [完整使用指南](JINJA2_VERSION_GUIDE.md)
- [版本对比](VERSION_COMPARISON.md)
- [更新日志](CHANGELOG.md)

---

**祝您使用愉快！** 🎉
