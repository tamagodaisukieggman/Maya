@echo ==================== Exporting... ====================
rem @echo off

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


set PYTHON_VERSION=2.7.17
set MAYA_EXE="C:\Program Files\Autodesk\Maya%CYCLOPS_APP_VERSION%\bin\mayabatch.exe"
set PYTHON_EXE="c:\cygames\wiz2\tools\python\%PYTHON_VERSION%\python.exe"

set TOOL_ROOT=c:\cygames\wiz2\tools

if %SUBMIT_SERVER% == 1 (
    rem net use P: \\cydrive01\100_projects\051_world

    set APPDATA=%LOCALAPPDATA%
    set PYTHONPATH=%PYTHONPATH%;%ENVUTILS_PATH%
    call %TOOL_ROOT%\projects\world\inhouse\win\standalone\cyclops_world\launch\write_env.bat %WM_PROJECT% %CYCLOPS_APP_NAME% "%CYCLOPS_APP_VERSION%" "Default" "%ENV_PATH%" %PACKAGE_VERSION% %DEVELOP_LAUNCH%
)

%PYTHON_EXE% %ENVUTILS_PATH%\envutils.py "%ENV_PATH%" %MAYA_EXE% -command "%COMMAND%"
