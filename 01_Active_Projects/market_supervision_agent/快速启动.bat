@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:menu
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║       个体工商户开业登记申请书填充工具 v3.0               ║
echo ║            Jinja2 模板版 - 快速启动菜单                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 【主要功能】
echo.
echo   1. 生成申请书（使用测试数据）
echo   2. 生成申请书（从JSON文件）
echo   3. 批量生成申请书
echo   4. 验证数据文件
echo.
echo 【工具功能】
echo.
echo   5. 查看当前配置
echo   6. 编辑配置
echo   7. 创建新数据文件
echo   8. 验证模板
echo.
echo 【其他】
echo.
echo   9. 查看使用指南
echo   0. 退出
echo.
echo ════════════════════════════════════════════════════════════
echo.

set /p choice="请选择功能 (0-9): "

if "%choice%"=="1" goto test_mode
if "%choice%"=="2" goto single_file
if "%choice%"=="3" goto batch_mode
if "%choice%"=="4" goto validate_data
if "%choice%"=="5" goto show_config
if "%choice%"=="6" goto edit_config
if "%choice%"=="7" goto new_data
if "%choice%"=="8" goto validate_template
if "%choice%"=="9" goto show_guide
if "%choice%"=="0" goto exit
goto menu

:test_mode
cls
echo.
echo [测试模式] 使用内置测试数据生成申请书
echo.
python jinja2_filler.py --test
echo.
pause
goto menu

:single_file
cls
echo.
set /p jsonfile="请输入JSON数据文件路径（或直接拖放文件到此处）: "
if "%jsonfile%"=="" goto menu

cls
echo.
echo [生成申请书] 从文件: %jsonfile%
echo.
python jinja2_filler.py --data "%jsonfile%"
echo.
pause
goto menu

:batch_mode
cls
echo.
set /p jsonfile="请输入批量数据文件路径（或直接拖放文件到此处）: "
if "%jsonfile%"=="" goto menu

cls
echo.
echo [批量生成] 从文件: %jsonfile%
echo.
python jinja2_filler.py --batch "%jsonfile%"
echo.
pause
goto menu

:validate_data
cls
echo.
set /p jsonfile="请输入要验证的数据文件路径: "
if "%jsonfile%"=="" goto menu

cls
echo.
echo [验证数据] 文件: %jsonfile%
echo.
python data_validator.py "%jsonfile%"
echo.
pause
goto menu

:show_config
cls
echo.
echo [查看配置]
echo.
python config_manager.py --show
echo.
pause
goto menu

:edit_config
cls
echo.
echo [编辑配置]
echo.
python config_manager.py --edit
echo.
pause
goto menu

:new_data
cls
echo.
echo [创建新数据文件]
echo.
python config_manager.py --new-data
echo.
pause
goto menu

:validate_template
cls
echo.
set /p templatefile="请输入模板文件路径: "
if "%templatefile%"=="" goto menu

cls
echo.
echo [验证模板] 文件: %templatefile%
echo.
python jinja2_filler.py --validate "%templatefile%"
echo.
pause
goto menu

:show_guide
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    快速使用指南                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 【模板制作】
echo.
echo   1. 在Word文档中输入变量，格式: {{变量名}}
echo   2. 示例:
echo      个体工商户名称：{{business_name}}
echo      经营者姓名：{{operator_name}}
echo      联系电话：{{phone}}
echo.
echo   3. 保存为 .docx 文件
echo.
echo 【数据准备】
echo.
echo   创建JSON文件，例如 data.json:
echo   {
echo     "business_name": "张三便利店",
echo     "operator_name": "张三",
echo     "phone": "13800138000",
echo     "business_address": "广西玉林市兴业县蒲塘镇商业街88号",
echo     "id_card": "450101199001011234",
echo     "gender": "男"
echo   }
echo.
echo 【常用变量】
echo.
echo   business_name      - 个体工商户名称
echo   operator_name      - 经营者姓名
echo   phone              - 联系电话
echo   email              - 电子邮箱
echo   business_address   - 经营场所
echo   postal_code        - 邮政编码（默认537820）
echo   id_card            - 身份证号码
echo   gender             - 性别
echo   nation             - 民族
echo   education          - 文化程度
echo   business_scope     - 经营范围
echo   operation_period   - 经营期限
echo.
echo 【高级功能】
echo.
echo   条件判断:
echo   {%% if operation_period == '长期' %%}
echo     经营期限：长期
echo   {%% else %%}
echo     经营期限：{{operation_period}}
echo   {%% endif %%}
echo.
echo   列表循环:
echo   {%% for item in business_scope_list %%}
echo   - {{item}}
echo   {%% endfor %%}
echo.
echo 【命令行使用】
echo.
echo   python jinja2_filler.py --test              # 测试模式
echo   python jinja2_filler.py --data data.json    # 从文件生成
echo   python jinja2_filler.py --batch batch.json  # 批量生成
echo   python jinja2_filler.py --validate x.docx   # 验证模板
echo.
echo ════════════════════════════════════════════════════════════
echo.
pause
goto menu

:exit
cls
echo.
echo 感谢使用！再见！
echo.
timeout /t 2 >nul
exit
