@echo off
::for文で文字を置き換えるために必要
setlocal EnableExtensions EnableDelayedExpansion

:: カレントディレクトリを取得
set CURRENTDIR=%~dp0

::今日の日付を変数にする
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set yyyy=%ldt:~0,4%
set mm=%ldt:~4,2%
set dd=%ldt:~6,2%
set tttt=%ldt:~8,4%

::バックアップするフォルダの作成
set BACKUPDIR=%CURRENTDIR%backups\%yyyy%-%mm%-%dd%-%tttt%
md %BACKUPDIR%

::このバッチファイルのディレクトリ階層から更新日(/D)が今日のファイルを順次コピーする
::echo F |は確認を自動的にファイル(F)で処理するために付ける
for /f %%a in ('forfiles /S /M *.* /D +0 /C "cmd /c echo @path"') do (
  set "SRC=%%~a"
  set "modified=!SRC:%CURRENTDIR%=%BACKUPDIR%\!"
  echo !SRC! !modified! コピー！
  echo F | xcopy !SRC! !modified! /D /S /R /Y /I /K /E
)

::zip圧縮
set folder=%BACKUPDIR%
set zipfile=%BACKUPDIR%.zip

if not exist "%folder%" (
    echo 指定されたフォルダが存在しません。
    exit /b 1
)

if "%zipfile%"=="" (
    set zipfile=%folder%.zip
)

echo %folder% を %zipfile% に圧縮しています...
powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('%folder%', '%zipfile%'); }"

if %errorlevel%==0 (
    echo 圧縮が完了しました。
) else (
    echo 圧縮中にエラーが発生しました。
)

::元のフォルダの削除
::rd /s /q %folder%
::echo Folder has been deleted successfully.
