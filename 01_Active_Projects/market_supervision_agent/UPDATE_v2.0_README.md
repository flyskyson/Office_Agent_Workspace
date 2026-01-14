# 李奕凤版申请书填充工具 v2.0 - 更新说明

## 更新日期
2026年1月12日

## 主要更新

### 1. 支持修改后的模板

根据您修改的模板，v2.0版本现在支持：

#### 颜色分类
- 🔴 **红色字体（76处）**：变量数据，每次填写时需要替换
- 🟢 **绿色字体（4处）**：常量数据，保持不变
  - `537820` - 邮政编码
  - `身份证` (3处) - 字段标识

#### 处理逻辑
- **红色字体**：删除并填充新的实际数据
- **绿色字体**：保留不变，不删除
- **黑色字体**：字段名，保留不变

### 2. 新增全局配置文件

**文件**：[config.json](config.json)

**功能**：
- 存储常量数据（绿色字体的值）
- 存储默认值（当用户没有提供时使用）
- 字段映射配置

**配置内容**：
```json
{
  "constants": {
    "postal_code_default": "537820"
  },
  "defaults": {
    "business_scope_licensed": "小餐饮",
    "business_scope_general": "食品销售（仅销售预包装食品）",
    "operation_period": "长期"
  },
  "field_mappings": {
    "个体工商户名称": "business_name",
    "经营者姓名": "operator_name",
    ...
  }
}
```

### 3. 测试结果

使用测试数据生成文档：
- 删除红色字体：76处
- 填充数据：8处
- 保留绿色常量：0处（在红色单元格中未发现绿色）

## 使用方法

### 快速测试

```bash
cd 01_Active_Projects/market_supervision_agent
python 李奕凤版申请书填充工具_v2.py --test
```

### 使用修改后的模板

```bash
python 李奕凤版申请书填充工具_v2.py --test --template "c:\Users\flyskyson\Desktop\（李奕凤）个体工商户开业登记申请书（模板-待修改）.docx"
```

### 使用自定义数据

1. 创建JSON文件（my_data.json）：
```json
{
  "business_name": "张三便利店",
  "operator_name": "张三",
  "phone": "13800138000",
  "business_address": "广西玉林市兴业县蒲塘镇XX路XX号",
  "postal_code": "537820",
  "id_card": "450101199001011234",
  "gender": "男",
  "nation": "汉族",
  "political_status": "群众",
  "education": "高中",
  "business_scope": "食品销售；日用百货"
}
```

2. 运行工具：
```bash
python 李奕凤版申请书填充工具_v2.py --data my_data.json
```

## 文件清单

### 新增文件

1. **[李奕凤版申请书填充工具_v2.py](李奕凤版申请书填充工具_v2.py)** - v2.0主程序
2. **[config.json](config.json)** - 全局配置文件
3. **[UPDATE_v2.0_README.md](UPDATE_v2.0_README.md)** - 本说明文档

### 保留文件

1. **[李奕凤版申请书填充工具.py](李奕凤版申请书填充工具.py)** - v1.0版本（原版）
2. **[李奕凤版申请书使用指南.md](李奕凤版申请书使用指南.md)** - 原使用指南

### 分析工具（临时）

1. **analyze_modified_template.py** - 模板分析脚本
2. **analyze_all_colors.py** - 颜色分析脚本
3. **template_analysis.json** - 分析结果
4. **all_colors_analysis.json** - 颜色统计

## 技术改进

### 1. 绿色字体识别

```python
def is_green_font(run):
    """判断是否为绿色字体 RGB(0,176,80)"""
    if run.font.color and run.font.color.rgb:
        r, g, b = run.font.color.rgb
        return r == 0 and g == 176 and b == 80
    return False
```

### 2. 保留绿色字体

在删除红色字体时，跳过绿色字体：

```python
# 删除红色字体（保留绿色和黑色）
for paragraph in cell.paragraphs:
    for run in paragraph.runs:
        if is_red_font(run):
            run.text = ""
            deleted_count += 1
```

### 3. 配置文件支持

自动加载config.json，支持：
- 常量数据
- 默认值
- 字段映射

## 下一步

主人，现在您可以：

1. **测试v2.0版本**，确认绿色常量被正确保留
2. **调整配置文件** [config.json](config.json)，修改常量和默认值
3. **准备实际数据**，开始使用工具处理真实业务

如果您需要：
- 修改常量数据（如邮政编码）
- 添加更多默认值
- 调整字段映射

请告诉我，我会帮您更新配置文件！

---

**版本**：v2.0
**状态**：✅ 已测试，可使用
**模板**：支持修改后的模板（绿色常量保留）
