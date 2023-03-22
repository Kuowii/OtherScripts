@echo off
set bin=p4
set cl=1069
%bin% describe -s %cl% > temp.txt

for /f "tokens=2,4 delims=# " %%i in (temp.txt) do (
if %%j==edit (
rem echo %%j %%i 
%bin% revert %%i
%bin% delete -c %cl% %%i
)
)


pause