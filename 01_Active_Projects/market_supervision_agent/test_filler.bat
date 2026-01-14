@echo off
chcp 65001 > nul
echo 正在测试个体工商户申请书填充工具...
echo.

REM 检查模板文件是否存在
if not exist "个体工商户开业登记申请书（模板）.docx" (
    echo 错误: 模板文件不存在
    echo 请确保"个体工商户开业登记申请书（模板）.docx"在当前目录
    pause
    exit /b 1
)

echo 模板文件存在，开始测试...
echo.

REM 创建测试输入文件
echo 1> test_input.txt
echo 张三小吃店>> test_input.txt
echo 张三>> test_input.txt
echo 110101199001011234>> test_input.txt
echo 北京市东城区王府井大街1号>> test_input.txt
echo 餐饮服务；小吃店经营>> test_input.txt
echo 50000>> test_input.txt
echo 13800138000>> test_input.txt
echo>> test_input.txt
echo>> test_input.txt
echo>> test_input.txt
echo>> test_input.txt
echo>> test_input.txt
echo>> test_input.txt
echo>> test_input.txt
echo>> test_input.txt

echo 使用测试数据运行填充工具...
echo.

REM 运行填充工具，使用重定向输入
python 个体工商户申请书填充工具.py < test_input.txt

echo.
echo 测试完成！
echo.

REM 清理临时文件
if exist test_input.txt del test_input.txt

REM 检查生成的文件
if exist filled_applications\*.docx (
    echo 生成的文件:
    dir /b filled_applications\*.docx
    echo.
    echo 生成的文件位于 filled_applications\ 目录
) else (
    echo 未生成文件，可能出错了
)

pause