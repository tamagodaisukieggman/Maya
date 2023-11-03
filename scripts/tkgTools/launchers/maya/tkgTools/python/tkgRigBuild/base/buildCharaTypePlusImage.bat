@echo off

rem cd /d %~dp0
set CURRENT_DIR=%~dp0

echo TYPE: %CURRENT_DIR%

:: 末尾のバックスラッシュを削除
set BACK_CURRENT_DIR=%CURRENT_DIR:~0,-1%

:: 上の階層のディレクトリパスを取得
for %%i in (%BACK_CURRENT_DIR%) do set PARENT_DIR=%%~dpi

:: 末尾のバックスラッシュを削除
set PARENT_DIR=%PARENT_DIR:~0,-1%

:: 上の階層のディレクトリパスを取得
for %%i in (%PARENT_DIR%) do set PARENT_PARENT_DIR=%%~dpi

:: set SCRIPT_DIR=%CURRENT_DIR:\projects\wizard2=%
set BAT_SCRIPT_DIR=%PARENT_PARENT_DIR:\projects=\bat%
set BUILD_SCRIPT_DIR=%PARENT_PARENT_DIR:\projects=%


:: 末尾のバックスラッシュを削除
set _BACK_CURRENT_DIR=%BUILD_SCRIPT_DIR:~0,-1%

:: 上の階層のディレクトリパスを取得
for %%i in (%_BACK_CURRENT_DIR%) do set BUILD_SCRIPT_DIR=%%~dpi


::Maya Settings
set MAYA_UI_LANGUAGE=en_US
set MAYA_CMD_FILE_OUTPUT=%BAT_SCRIPT_DIR%/maya_cmdFileOutput.log
set PYTHONPATH=%PYTHONPATH%;%BAT_SCRIPT_DIR%;
set PYTHONPATH=%PYTHONPATH%;%BUILD_SCRIPT_DIR%;
echo 一時的にPYTHONPATHを指定: %PYTHONPATH%

for %%i in ("%CD%") do set TYPE=%%~ni
echo TYPE: %TYPE%

set CURRENT_DIR=%CURRENT_DIR:\=/%
set LOG_FOLDER=%CURRENT_DIR%\log

echo -------------Build biped-------------

echo Mayaのバージョンを指定してください。
set /P MAYA_VERSION="2018, 2019, 2020 :"
set MAYA_VERSION=%MAYA_VERSION:\=/%
set CLOSE_MAYA=import maya.cmds as cmds;cmds.evalDeferred('cmds.quit(force=True)')

::biped
set COMMAND="import rigbuild;rb=rigbuild.Build(buildPath='%CURRENT_DIR%', logFolder='%LOG_FOLDER%', plus_image=True);rb.main();%CLOSE_MAYA%"
call "C:\Program Files\Autodesk\Maya"%MAYA_VERSION%"\bin\maya.exe" -command python(\"%COMMAND%\")"

::Folder Open
start "" "%CURRENT_DIR%/000_data"
rem start "" "%CURRENT_DIR%/data"
rem start "" "%CURRENT_DIR%/data"
