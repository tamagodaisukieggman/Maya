@echo off

REM for /f "delims=" %%a in ('dir /b /ad-h /od "C:\Users\%USERNAME%\Documents\maya\scripts\tkgTools*"') do set "latestDir=%%~a"
REM echo %latestDir%

setlocal EnableExtensions EnableDelayedExpansion

for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set yyyy=%ldt:~0,4%
set mm=%ldt:~4,2%
set dd=%ldt:~6,2%
set tttt=%ldt:~8,4%

set ARGS=%*
REM set ARGS=%ARGS:\=/%

set "REPLACE=%USERNAME%\Desktop\backup-%yyyy%-%mm%-%dd%-%tttt%"

for %%i in (%ARGS%) do (
  set "SRC=%%i"
  set "modified=!SRC:%USERNAME%\Documents=%REPLACE%!"
  echo !SRC!
  echo !modified!
  xcopy !SRC! !modified! /D /S /R /Y /I /K /E

)

set COPYTKGBAT=%~dp0copy_tkg.bat
set PASTEPATH=C:\Users\%REPLACE%
copy %COPYTKGBAT% %PASTEPATH%
