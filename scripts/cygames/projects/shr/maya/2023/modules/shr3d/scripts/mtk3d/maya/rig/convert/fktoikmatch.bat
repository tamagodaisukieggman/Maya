@echo off

rem cd /d %~dp0
set CURRENT_DIR=%~dp0

set ARGS=%*
set ARGS=%ARGS:\=/%

set /P USR_INPUT_STR="保存するパスを入力してEnterを押してください:"
set USR_INPUT_STR=%USR_INPUT_STR:\=/%

echo 強制的に切り替えるIKFKスイッチを指定してください。ex) arms_l_fk,legs_r_ik
echo ※キーがある場合は指定してもスキップされます。
echo 指定できるワード  arms_l_fk,arms_r_fk,arms_l_ik,arms_r_ik,legs_l_fk,legs_r_fk,legs_l_ik,legs_r_ik
set /P IKFK_SWITCHES=" arms_l_fk,legs_r_ik と指定すると「左手はFK」「右足はIK」に強制的に切り替えます。:"
set IKFK_SWITCHES=%IKFK_SWITCHES:\=/%

set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;Z:\mtk\tools\maya\modules;
set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;z:\cyllista\tools\maya\modules
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;Z:\cyllista\tools\maya\modules\anm\plug-ins\2018

set MAYA_UI_LANGUAGE=en_US
set MAYA_CMD_FILE_OUTPUT=%CURRENT_DIR%/maya_cmdFileOutput.log
set PYTHONPATH=%PYTHONPATH%;%CURRENT_DIR%;
rem echo 一時的にPYTHONPATHを指定: %PYTHONPATH%

set COMMAND="import runfiles;reload(runfiles);rr=runfiles.RunFiles(fktoikmatch=True);rr.fktoikmatch_set_switch='%IKFK_SWITCHES%';rr.main('%ARGS%', '%USR_INPUT_STR%')"

rem call "C:\Program Files\Autodesk\Maya2018\bin\maya.exe" -command python(\"%COMMAND%\")"
call "C:\Program Files\Autodesk\Maya2018\bin\mayabatch.exe" -command python(\"%COMMAND%\")"

pause
