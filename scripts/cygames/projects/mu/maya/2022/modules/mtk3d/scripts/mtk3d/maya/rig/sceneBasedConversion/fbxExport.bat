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

set /P NAME_SPACE="namespaceを指定してください。bos00_000_000/bos02_000_000/cre00_000_000/cre01_000_000/ply00_m_000_000/mob00_m_000_000 etc...:"
set NAME_SPACE=%NAME_SPACE:\=/%

set COMMAND=import fbxExport;import importlib;importlib.reload(fbxExport);fbxExport.main('%ARGS%','%USR_INPUT_STR%','%NAME_SPACE%')

call "C:\Program Files\Autodesk\Maya2022\bin\mayabatch.exe" -command "python(\"%COMMAND%\")"

pause