@echo off

set CURRENT_DIR=%~dp0

set ARGS=%*
set ARGS=%ARGS:\=/%

SET MAYA_UI_LANGUAGE=en_US
set PYTHONPATH=%PYTHONPATH%;%CURRENT_DIR%;

set COMMAND=import anmdescgenerator as adg;reload(adg);adg.main()

call "C:\Program Files\Autodesk\Maya2018\bin\mayabatch.exe" -command "python(\"%COMMAND%\")"

pause
