@echo off

rem cd /d %~dp0
set CURRENT_DIR=%~dp0

::set ARGS=%*
::set ARGS=%ARGS:\=/%

echo ビルドするタイプを入力してください
set /P USR_INPUT_STR=" biped fish :"
set USR_INPUT_STR=%USR_INPUT_STR:\=/%

echo フォルダを指定して実行する場合は名前を入力してください。
set /P USR_EXCACT_DIR=" mtk_base_00_000 mtk_base_01_000 mtk_base_02_000 simple_base_00_000 world_base_00_000 :"
set USR_EXCACT_DIR=%USR_EXCACT_DIR:\=/%

::mutsunokami
set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;Z:\mtk\tools\maya\modules;
set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;z:\cyllista\tools\maya\modules;
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;Z:\cyllista\tools\maya\modules\anm\plug-ins\2018;

::Maya Settings
set MAYA_UI_LANGUAGE=en_US
set MAYA_CMD_FILE_OUTPUT=%CURRENT_DIR%/maya_cmdFileOutput.log
set PYTHONPATH=%PYTHONPATH%;%CURRENT_DIR%;
rem echo 一時的にPYTHONPATHを指定: %PYTHONPATH%

set COMMAND="from tkgTools.tkgRig.scripts.build import rigbuild;rb=rigbuild.Build(types='%USR_INPUT_STR%', excactDir='%USR_EXCACT_DIR%');rb.main()"

rem call "C:\Program Files\Autodesk\Maya2018\bin\maya.exe" -command python(\"%COMMAND%\")"
echo Mayaのバージョンを指定してください。
set /P MAYA_VERSION="2018, 2019, 2020 :"
set MAYA_VERSION=%MAYA_VERSION:\=/%
call "C:\Program Files\Autodesk\Maya"%MAYA_VERSION%"\bin\mayabatch.exe" -command python(\"%COMMAND%\")"
