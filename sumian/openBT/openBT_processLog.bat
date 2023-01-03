@echo off&setlocal enabledelayedexpansion
set ff=openBT1212.log
echo 正在统计&echo;
set str=次结束  很快 失败  比较慢  太慢了
set fileName=openBT_Result.txt
echo %date% %time% >%fileName%
echo.>>%fileName%
echo 数据统计：>>%fileName%
echo ---------------------------------------------->>%fileName%
(for %%a in (%str%)do (
  set n%%a=0&set/p=   %%a : <nul>con
  for /f "delims=" %%b in ('findstr "%%a" "%ff%"')do (
    set h=%%b
    call :yky %%a)
  echo !n%%a!>con
  echo 关键字 %%a  共有 !n%%a! 处
))>>%fileName%
echo.>>%fileName%
findstr "%str%" "%ff%">>%fileName%
echo/&pause&exit
:yky
set/a n%1+=1
set h=!h:*%1=!
if defined h if not "!h:*%1=!"=="!h!" goto :yky