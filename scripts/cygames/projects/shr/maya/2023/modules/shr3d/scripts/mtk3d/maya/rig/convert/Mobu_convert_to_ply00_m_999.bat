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

::set /P USR_INPUT_STR_TYPE="コンバートするタイプを入力してEnterを押してください。 bossBattleJD or mcjt or bindJoints or sotai or bindJoints_HIK or bossBattleJD_HIK or MB_sotai :"
::set USR_INPUT_STR_TYPE=%USR_INPUT_STR_TYPE:\=/%
set USR_INPUT_STR_TYPE=bindJoints

set /P TO_FPS="保存するデータのFPSを入力してEnterを押してください。:"
set TO_FPS=%TO_FPS:\=/%

set /P MAIN_HIP_AXIS="main_ctrlを腰に追従させる。Yes or No :"
set MAIN_HIP_AXIS=%MAIN_HIP_AXIS:\=/%

::set /P ANIM_BASE="アニメーションを流し込むMayaデータを指定してください。:"
::set ANIM_BASE=%ANIM_BASE:\=/%
set ANIM_BASE=Z:/mtk/work/resources/animations/clips/player/workscenes/anm_ply00_m_999_anim.ma

set COMMAND="import convert;reload(convert);convert.main('%ARGS%', '%USR_INPUT_STR%', '%USR_INPUT_STR_TYPE%', %TO_FPS%, '%MAIN_HIP_AXIS%', '%ANIM_BASE%')"

rem call "C:\Program Files\Autodesk\Maya2018\bin\maya.exe" -command python(\"%COMMAND%\")"
call "C:\Program Files\Autodesk\Maya2018\bin\mayabatch.exe" -command python(\"%COMMAND%\")"
pause
