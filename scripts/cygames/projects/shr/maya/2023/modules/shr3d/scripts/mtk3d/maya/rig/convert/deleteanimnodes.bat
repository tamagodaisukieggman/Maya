@echo off

rem cd /d %~dp0
set CURRENT_DIR=%~dp0

set ARGS=%*
set ARGS=%ARGS:\=/%

set /P USR_INPUT_STR="�ۑ�����p�X����͂���Enter�������Ă�������:"
set USR_INPUT_STR=%USR_INPUT_STR:\=/%

set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;Z:\mtk\tools\maya\modules;
set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;z:\cyllista\tools\maya\modules
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;Z:\cyllista\tools\maya\modules\anm\plug-ins\2018

set MAYA_UI_LANGUAGE=en_US
set MAYA_CMD_FILE_OUTPUT=%CURRENT_DIR%/maya_cmdFileOutput.log
set PYTHONPATH=%PYTHONPATH%;%CURRENT_DIR%;
rem echo �ꎞ�I��PYTHONPATH���w��: %PYTHONPATH%

set COMMAND="import runfiles;reload(runfiles);rr=runfiles.RunFiles(deleteAnimNode=True);rr.main('%ARGS%', '%USR_INPUT_STR%')"

rem call "C:\Program Files\Autodesk\Maya2018\bin\maya.exe" -command python(\"%COMMAND%\")"
call "C:\Program Files\Autodesk\Maya2018\bin\mayabatch.exe" -command python(\"%COMMAND%\")"

pause
