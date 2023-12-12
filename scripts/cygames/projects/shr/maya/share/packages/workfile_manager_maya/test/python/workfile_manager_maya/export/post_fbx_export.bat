@echo ==================== Exporting... ====================
rem @echo off
set CYCLOPS_CONFIG_PATH=C:\cygames\shrdev\shr\tools\in\sta\cyclops\config
set BATCHPATH=%~dp0
set ENVUTILS_PATH=%1
set ENV_PATH=%2
set COMMAND=%3
set PACKAGE_VERSION=%4
set CYCLOPS_APP_NAME=%5
set CYCLOPS_APP_VERSION=%6
set P4TICKETS=%7
set WM_PROJECT=%8
set PYTHON_ARCHIVE_DIR=%9
shift
set SUBMIT_SERVER=%9
shift
set DEVELOP_LAUNCH=%9

if not %DEVELOP_LAUNCH% == 1 (
    c:
    cd %BATCHPATH%
    "C:\Program Files\Perforce\p4.exe" sync -s C:\cygames\shrdev\shr\tools\in\... C:\cygames\shrdev\shr\tools\tp\...
)

set MAYA_EXE="C:\Program Files\Autodesk\Maya%CYCLOPS_APP_VERSION%\bin\mayabatch.exe"

::バッチ処理で不要なプラグインのロードを回避するためのダミー
set MAYA_PLUG_IN_PATH=C:\cygames\shrshare\tools\maya\plugins\2023\test;%MAYA_PLUG_IN_PATH%

C:\cygames\shrdev\shr\tools\in\sta\cyclops\cyclops.exe export -p %WM_PROJECT% -a %CYCLOPS_APP_NAME% -v "%CYCLOPS_APP_VERSION%" --output "%ENV_PATH%"
"C:\cygames\shrshare\tools\workman\bin\envutils.exe" "%ENV_PATH%" %MAYA_EXE% -command "%COMMAND%"

