@echo off

rem cd /d %~dp0
set CURRENT_DIR=%~dp0

echo CURRENT_DIR: %CURRENT_DIR%

:: 末尾のバックスラッシュを削除
set CURRENT_DIR=%CURRENT_DIR:~0,-1%

:: 上の階層のディレクトリパスを取得
for %%i in (%CURRENT_DIR%) do set PARENT_DIR=%%~dpi

:: 結果を表示
echo Current Directory: %CURRENT_DIR%
echo Parent Directory: %PARENT_DIR%
pause

set SCRIPT_DIR=%CURRENT_DIR:\projects\wizard2=%

::Maya Settings
set MAYA_UI_LANGUAGE=en_US
set MAYA_CMD_FILE_OUTPUT=%SCRIPT_DIR%/maya_cmdFileOutput.log
set PYTHONPATH=%PYTHONPATH%;%SCRIPT_DIR%;
rem echo 一時的にPYTHONPATHを指定: %PYTHONPATH%

echo PYTHONPATH: %PYTHONPATH%
pause

echo -------------Build biped-------------

echo Mayaのバージョンを指定してください。
set /P MAYA_VERSION="2018, 2019, 2020 :"
set MAYA_VERSION=%MAYA_VERSION:\=/%

::biped
set COMMAND="from tkgTools.tkgRig.scripts.build import rigbuild;rb=rigbuild.Build(types='biped', excactDir='wizard2_base_00_000');rb.main()"
call "C:\Program Files\Autodesk\Maya"%MAYA_VERSION%"\bin\mayabatch.exe" -command python(\"%COMMAND%\")"

::Folder Open
start "" "%SCRIPT_DIR%/types/biped/wizard2_base_00_000/000_data"
rem start "" "%SCRIPT_DIR%/types/biped/wizard2_base_00_000/data"
rem start "" "%SCRIPT_DIR%/types/biped/wizard2_base_00_000/data"

pause
