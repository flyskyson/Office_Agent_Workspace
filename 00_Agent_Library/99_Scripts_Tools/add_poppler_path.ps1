# 添加 Poppler 到用户环境变量
$currentPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$popplerPath = 'C:\Users\flyskyson\poppler\Library\bin'

if ($currentPath -notlike "*$popplerPath*") {
    $newPath = "$currentPath;$popplerPath"
    [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
    Write-Host "成功添加 Poppler 到用户环境变量" -ForegroundColor Green
    Write-Host "路径: $popplerPath" -ForegroundColor Green
} else {
    Write-Host "Poppler 路径已存在于环境变量中" -ForegroundColor Yellow
}

Write-Host "`n请关闭并重新打开终端以使环境变量生效" -ForegroundColor Cyan
