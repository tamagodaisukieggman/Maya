@echo off
setlocal
title %~n0
cd /d %~dp0

if "%1"=="" goto WARNING
goto EXECUTE

:WARNING
echo drag and drop the folder.
goto END

:EXECUTE
@REM cd ..\..\maya\2022\modules\mtk\scripts\mtk\file\new_checker
set PYTHON="C:\Program Files\Autodesk\Maya2022\bin\mayapy.exe"

set SCRIPT="C:\cygames\shrdev\shr\tools\in\ext\maya\2022\modules\shr\scripts\shr\file\maya_scene_checker\no_gui.py"
@REM %PYTHON% no_gui.py main %1
%PYTHON% %SCRIPT% main %1

:END
endlocal
pause