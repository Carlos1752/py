@echo off&setlocal enabledelayedexpansion
set ff=*.log
echo 正在统计&echo;
set str=开始进行OTA压测 升级成功  升级失败
set fileName=OTA_Result.txt
echo %date% %time% >%fileName%
echo.>>%fileName%
echo 分析结果：>>%fileName%
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
echo 崩溃日志：>>%fileName%
findstr "%str%" "%ff%">>%fileName%
echo/&pause&exit
:yky
set/a n%1+=1
set h=!h:*%1=!
if defined h if not "!h:*%1=!"=="!h!" goto :yky