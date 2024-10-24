@echo off
chcp 65001

set WORK_PATH="C:\Program Files\Autodesk\Maya2024\bin"
set bin=""%WORK_PATH%\maya.exe""
set /P bin=设置Maya路径(留空使用以下路径：%bin%):

SET PYTHONPATH=;%~dp0

set "psCommand="(new-object -COM 'Shell.Application')^
.BrowseForFolder(0,'选择检测目录',0,0).self.path""

for /f "usebackq delims=" %%I in (`powershell %psCommand%`) do set "folder=%%I"

setlocal enabledelayedexpansion
echo Listing: !folder!
endlocal

set "regexPattern=^(?!.*_backup).*\.(ma|mb)$"
set findCommand="Get-ChildItem -Path '%folder%' -Recurse | Where-Object { $_.Name -match '%regexPattern%' } | ForEach-Object { Write-Output $_.FullName }"
set "pycmd=python("import wy_fix;wy_fix.main();")"
for /f "usebackq delims=" %%f in (`powershell %findCommand%`) do (
    echo Export: %%f
    %bin% -batch -file %%f -script %~dp0start.mel
)

pause