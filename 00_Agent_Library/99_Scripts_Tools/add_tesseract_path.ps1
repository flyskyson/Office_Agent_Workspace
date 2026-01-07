# 添加 Tesseract-OCR 到系统环境变量
$currentPath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
$tesseractPath = 'C:\Program Files\Tesseract-OCR'

if ($currentPath -notlike "*$tesseractPath*") {
    $newPath = "$currentPath;$tesseractPath"
    [Environment]::SetEnvironmentVariable('Path', $newPath, 'Machine')
    Write-Host "成功添加 Tesseract-OCR 到系统环境变量" -ForegroundColor Green
    Write-Host "路径: $tesseractPath" -ForegroundColor Green
} else {
    Write-Host "Tesseract-OCR 路径已存在于环境变量中" -ForegroundColor Yellow
}

Write-Host "`n请关闭并重新打开终端以使环境变量生效" -ForegroundColor Cyan
