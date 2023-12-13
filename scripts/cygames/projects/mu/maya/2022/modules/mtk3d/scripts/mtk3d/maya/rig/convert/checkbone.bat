@echo off

rem cd /d %~dp0
set CURRENT_DIR=%~dp0

set ARGS=%*
set ARGS=%ARGS:\=/%

set MAYA_UI_LANGUAGE=en_US
set MAYA_CMD_FILE_OUTPUT=%CURRENT_DIR%/maya_cmdFileOutput.log
set PYTHONPATH=%PYTHONPATH%;%CURRENT_DIR%;
rem echo 一時的にPYTHONPATHを指定: %PYTHONPATH%

set /P USR_INPUT_STR="保存するパスを入力してEnterを押してください:"
set USR_INPUT_STR=%USR_INPUT_STR:\=/%

set ROOT_JNT=rootBindJt
set CHECK_JOINTS=False
set EXPORT_FBX=True
set PLY00_999_SPECIAL=True

set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;Z:\mtk\tools\maya\modules;

set COMMAND="import checkbone;reload(checkbone);rb=checkbone.RunBones(round_value=3);rb.run_files('%ARGS%', '%USR_INPUT_STR%', '%ROOT_JNT%', '%CHECK_JOINTS%', '%EXPORT_FBX%', '%PLY00_999_SPECIAL%')"

rem call "C:\Program Files\Autodesk\Maya2018\bin\maya.exe" -command python(\"%COMMAND%\")"
call "C:\Program Files\Autodesk\Maya2018\bin\mayabatch.exe" -command python(\"%COMMAND%\")"
pause
