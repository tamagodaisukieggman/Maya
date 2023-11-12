@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: カレントディレクトリを取得
set CURRENTDIR=%~dp0

::今日の日付を変数にする
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set yyyy=%ldt:~0,4%
set mm=%ldt:~4,2%
set dd=%ldt:~6,2%
set tttt=%ldt:~8,4%

::
echo 今の時間と日付 %date% %time%
set /P CURRENTTIME="日付と時間を指定(例:2023/11/12 18:29):"

:: ドロップされたフォルダ
set ARGS=%*

::バックアップするフォルダの作成
set BACKUPDIR=%CURRENTDIR%backups\%yyyy%-%mm%-%dd%-%tttt%
md %BACKUPDIR%

for %%i in (%ARGS%) do (
  set "MODITIME=%%~ti"
  set "SRC=%%i"

  IF "!MODITIME!" GTR "%CURRENTTIME%" (
    set "modified=!SRC:%CURRENTDIR%=%BACKUPDIR%\!"
    xcopy !SRC! !modified! /D /S /R /Y /I /K /E
  ) ELSE (
    echo !MODITIME! %CURRENTTIME%
  )
)
