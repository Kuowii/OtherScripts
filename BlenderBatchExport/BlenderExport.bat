@ECHO off

:setbl
set bl="blender.exe"
set root=%~dp0
set /p bl=设置Blender路径(直接回车取当前目录):
set /p root=设置遍历根目录路径(直接回车取当前目录):
set sf="C:\Users\Administrator\Desktop\doris_armchairshetlandmoss\scene.gltf"

setlocal enabledelayedexpansion
 
for /r %root% %%a in (*) do ( 
::echo a is %%a
set EXISTS_FLAG=false
echo %%~nxa|find ".gltf">nul&&set EXISTS_FLAG=true
if "!EXISTS_FLAG!"=="true" (
::echo GET
%bl% -b -P fbx.py -- -s %%a
)
)
endlocal

::%bl% -b -P fbx.py -- -s %sf%

echo 转换完毕！

pause