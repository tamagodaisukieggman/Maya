@echo off

setlocal enabledelayedexpansion

rem ------------------------------------
rem Env
rem ------------------------------------

set MAYA_VER=%1
set MAYA_FORCE_PANEL_FOCUS=0
set MAYA_INSTALL_PATH=C:\Program Files\Autodesk\Maya%MAYA_VER%\bin

echo %MAYA_INSTALL_PATH%

rem ------------------------------------
rem Maya
rem ------------------------------------

set FIX_PYTHON_SCRIPT=%2
set FIX_PYTHON_SCRIPT=%FIX_PYTHON_SCRIPT:__space__= %
set FIX_PYTHON_SCRIPT=python(%FIX_PYTHON_SCRIPT%);

echo %FIX_PYTHON_SCRIPT%

rem ------------------------------------
rem Batch
rem ------------------------------------

call "%MAYA_INSTALL_PATH%\mayabatch.exe" -noAutoloadPlugins -command "%FIX_PYTHON_SCRIPT%"
echo;
echo âΩÇ©ÉLÅ[ÇâüÇ∑Ç∆Ç±ÇÃâÊñ ÇÕï¬Ç∂Ç‹Ç∑
echo;
pause

endlocal

exit /b
