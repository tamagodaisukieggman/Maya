@echo off

rem cd /d %~dp0
set CURRENT_DIR=%~dp0

set ARGS=%*
set ARGS=%ARGS:\=/%

set /P USR_INPUT_STR="�ۑ�����p�X����͂���Enter�������Ă�������:"
set USR_INPUT_STR=%USR_INPUT_STR:\=/%

echo �����I�ɐ؂�ւ���IKFK�X�C�b�`���w�肵�Ă��������Bex) arms_l_fk,legs_r_ik
echo ���L�[������ꍇ�͎w�肵�Ă��X�L�b�v����܂��B
echo �w��ł��郏�[�h  arms_l_fk,arms_r_fk,arms_l_ik,arms_r_ik,legs_l_fk,legs_r_fk,legs_l_ik,legs_r_ik
set /P IKFK_SWITCHES=" arms_l_fk,legs_r_ik �Ǝw�肷��Ɓu�����FK�v�u�E����IK�v�ɋ����I�ɐ؂�ւ��܂��B:"
set IKFK_SWITCHES=%IKFK_SWITCHES:\=/%

set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;Z:\mtk\tools\maya\modules;
set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;z:\cyllista\tools\maya\modules
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;Z:\cyllista\tools\maya\modules\anm\plug-ins\2018

set MAYA_UI_LANGUAGE=en_US
set MAYA_CMD_FILE_OUTPUT=%CURRENT_DIR%/maya_cmdFileOutput.log
set PYTHONPATH=%PYTHONPATH%;%CURRENT_DIR%;
rem echo �ꎞ�I��PYTHONPATH���w��: %PYTHONPATH%

set COMMAND="import runfiles;reload(runfiles);rr=runfiles.RunFiles(fktoikmatch=True);rr.fktoikmatch_set_switch='%IKFK_SWITCHES%';rr.main('%ARGS%', '%USR_INPUT_STR%')"

rem call "C:\Program Files\Autodesk\Maya2018\bin\maya.exe" -command python(\"%COMMAND%\")"
call "C:\Program Files\Autodesk\Maya2018\bin\mayabatch.exe" -command python(\"%COMMAND%\")"

pause
