# Python 语法高亮修复指南

## 问题原因
1. JSON配置文件包含中文注释，导致解析失败
2. VSCode无法正确加载Python语言服务器配置

## 已完成的修复
- [x] 清理了 `.vscode/settings.json` 中的所有注释
- [x] 验证了JSON配置的有效性
- [x] 确认了Pylance语言服务器配置正确
- [x] 创建了 `.vscode/languages.json` 强制语言模式

## 立即执行步骤

### 步骤 1: 重新加载VSCode窗口（必须）
1. 按 `Ctrl+Shift+P`
2. 输入 `Developer: Reload Window`
3. 按 `Enter`

### 步骤 2: 选择Python解释器
1. 按 `Ctrl+Shift+P`
2. 输入 `Python: Select Interpreter`
3. 选择 `Python 3.12.0`

### 步骤 3: 重启Pylance语言服务器
1. 按 `Ctrl+Shift+P`
2. 输入 `Pylance: Restart Server`
3. 按 `Enter`

### 步骤 4: 验证语法高亮
打开 `simple_test.py`，应该看到：
- 彩色的语法高亮（紫色、蓝色、橙色、黄色等）
- 输入 `.` 时显示代码提示
- 函数参数提示

## 如果仍然没有高亮

### 检查文件语言模式
1. 打开任意 `.py` 文件
2. 查看右下角状态栏
3. 确认显示 `Python`
4. 如果不是，点击它并选择 `Python`

### 检查VSCode输出
1. 按 `Ctrl+Shift+U` 打开输出面板
2. 在下拉菜单中选择 `Pylance`
3. 查看是否有错误信息

### 检查扩展状态
1. 按 `Ctrl+Shift+X` 打开扩展面板
2. 搜索 `Python`
3. 确认 `ms-python.python` 已启用
4. 搜索 `Pylance`
5. 确认 `ms-python.vscode-pylance` 已启用

## 最终方案
如果以上都不行，尝试：
1. 完全关闭VSCode
2. 删除工作区下的 `.vscode` 文件夹
3. 重新打开VSCode
4. 重新配置Python解释器
