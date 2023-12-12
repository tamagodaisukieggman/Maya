@echo off

set CURRENT_DIR=%~dp0

set ARGS=%*
set ARGS=%ARGS:\=/%

SET MAYA_UI_LANGUAGE=en_US
set PYTHONPATH=%PYTHONPATH%;%CURRENT_DIR%;

set /P USR_INPUT_STR="保存するパスを入力してEnterを押してください:"
set bs=\
if not "%USR_INPUT_STR:~-1%"=="\" set USR_INPUT_STR=%USR_INPUT_STR%%bs%
set USR_INPUT_STR=%USR_INPUT_STR:\=/%


set /P CONVERT_SCENE="アニメーションを流し込むMayaデータを指定してください。:"
set CONVERT_SCENE=%CONVERT_SCENE:\=/%

set /P NAME_SPACE="namespaceを指定してください。bos00_000_000/bos02_000_000/cre00_000_000/cre01_000_000/ply00_m_000_000/mob00_m_000_000 :"
set NAME_SPACE=%NAME_SPACE:\=/%

set COMMAND=import convert;import importlib;importlib.reload(convert);convert.main('%ARGS%','%USR_INPUT_STR%','%CONVERT_SCENE%','%NAME_SPACE%')

set PRJ_MAYA_TOOL_PATH=Z:\cyllista\tools\maya\modules
set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;%PRJ_MAYA_TOOL_PATH%

call "C:\Program Files\Autodesk\Maya2022\bin\mayabatch.exe" -command "python(\"%COMMAND%\")"

pause