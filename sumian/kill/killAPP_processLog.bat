@echo off&setlocal enabledelayedexpansion
set ff1=killAPP.log
echo ����ͳ��&echo;
set str=�ν���  �ܿ� ʧ��  �Ƚ���  ̫��
set fileName=killAPP_Result.txt
echo %date% %time% >%fileName%
echo.>>%fileName%
echo ���������>>%fileName%
echo ---------------------------------------------->>%fileName%
(for %%a in (%str%)do (
  set n%%a=0&set/p=   %%a : <nul>con
  for /f "delims=" %%b in ('findstr "%%a" "%ff1%"')do (
    set h=%%b
    call :yky %%a)
  echo !n%%a!>con
  echo �ؼ��� %%a  ���� !n%%a! ��
))>>%fileName%
echo.>>%fileName%
findstr "%str%" "%ff1%">>%fileName%
echo/&pause&exit
:yky
set/a n%1+=1
set h=!h:*%1=!
if defined h if not "!h:*%1=!"=="!h!" goto :yky