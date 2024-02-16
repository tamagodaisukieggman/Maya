@echo off
::======================================================================
::Maya2022
::======================================================================

cd /d %~dp0

setlocal
:: -----------------------------------------------------------
set MAYA_UI_LANGUAGE=en_US

set MAYA_VER=2022
set MAYA_INSTALL_PATH=C:\Program Files\Autodesk\Maya%MAYA_VER%

set PYTHONDONTWRITEBYTECODE=1
set PYTHONPATH=%CD%;%CD%\chara_utility;%CD%\normal_editor;%PYTHONPATH%

if "%1" == "" (
	echo ==================================================
	echo GUI MODE
	echo MAYA VERSION %MAYA_VER%
	echo ==================================================
	start "" "%MAYA_INSTALL_PATH%\bin\maya.exe"
) else (
	echo ==================================================
	echo BATCH MODE
	echo MAYA VERSION %MAYA_VER%
	echo ==================================================
	call "%MAYA_INSTALL_PATH%\bin\mayabatch.exe" %*
)

endlocal