@echo off
cd /d %~dp0

setlocal

call preprocess.bat
start "" "C:\Program Files\Autodesk\Maya2022\bin\maya.exe"

endlocal