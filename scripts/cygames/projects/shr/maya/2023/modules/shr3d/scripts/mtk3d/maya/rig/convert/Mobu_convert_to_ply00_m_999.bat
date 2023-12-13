@echo off

rem cd /d %~dp0
set CURRENT_DIR=%~dp0

set ARGS=%*
set ARGS=%ARGS:\=/%

set MAYA_UI_LANGUAGE=en_US
set MAYA_CMD_FILE_OUTPUT=%CURRENT_DIR%/maya_cmdFileOutput.log
set PYTHONPATH=%PYTHONPATH%;%CURRENT_DIR%;
rem echo �ꎞ�I��PYTHONPATH���w��: %PYTHONPATH%

set /P USR_INPUT_STR="�ۑ�����p�X����͂���Enter�������Ă�������:"
set USR_INPUT_STR=%USR_INPUT_STR:\=/%

::set /P USR_INPUT_STR_TYPE="�R���o�[�g����^�C�v����͂���Enter�������Ă��������B bossBattleJD or mcjt or bindJoints or sotai or bindJoints_HIK or bossBattleJD_HIK or MB_sotai :"
::set USR_INPUT_STR_TYPE=%USR_INPUT_STR_TYPE:\=/%
set USR_INPUT_STR_TYPE=bindJoints

set /P TO_FPS="�ۑ�����f�[�^��FPS����͂���Enter�������Ă��������B:"
set TO_FPS=%TO_FPS:\=/%

set /P MAIN_HIP_AXIS="main_ctrl�����ɒǏ]������BYes or No :"
set MAIN_HIP_AXIS=%MAIN_HIP_AXIS:\=/%

::set /P ANIM_BASE="�A�j���[�V�����𗬂�����Maya�f�[�^���w�肵�Ă��������B:"
::set ANIM_BASE=%ANIM_BASE:\=/%
set ANIM_BASE=Z:/mtk/work/resources/animations/clips/player/workscenes/anm_ply00_m_999_anim.ma

set COMMAND="import convert;reload(convert);convert.main('%ARGS%', '%USR_INPUT_STR%', '%USR_INPUT_STR_TYPE%', %TO_FPS%, '%MAIN_HIP_AXIS%', '%ANIM_BASE%')"

rem call "C:\Program Files\Autodesk\Maya2018\bin\maya.exe" -command python(\"%COMMAND%\")"
call "C:\Program Files\Autodesk\Maya2018\bin\mayabatch.exe" -command python(\"%COMMAND%\")"
pause
