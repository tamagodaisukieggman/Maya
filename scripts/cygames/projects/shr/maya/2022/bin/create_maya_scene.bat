@echo off

cd /d %~dp0

setlocal
set PYTHONPATH=
set MAYAPY="C:\Program Files\Autodesk\Maya2022\bin\mayapy.exe"
set SCRIPT="%~dp0\create_maya_scene.py"

echo ==== create maya scene ====

call   %MAYAPY% %SCRIPT% %*

endlocal
