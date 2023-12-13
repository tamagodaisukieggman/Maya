@echo off

rem ------------------------------------
rem Env
rem ------------------------------------

set MAYA_FORCE_PANEL_FOCUS=0
set MAYA_INSTALL_PATH=C:\Program Files\Autodesk\Maya%MAYA_VER%\bin

rem ------------------------------------
rem Maya
rem ------------------------------------

set FIX_PYTHON_SCRIPT=%1
set FIX_PYTHON_SCRIPT=%FIX_PYTHON_SCRIPT:__space__= %
set FIX_PYTHON_SCRIPT=python(%FIX_PYTHON_SCRIPT%);

echo %FIX_PYTHON_SCRIPT%

call "%MAYA_INSTALL_PATH%\mayabatch.exe" -command "%FIX_PYTHON_SCRIPT%"

exit /b