@echo on
::======================================================================
::Maya
::======================================================================

cd /d %~dp0

setlocal

:: ----------------------------------------
:: MAYA VERSION
:: ----------------------------------------
set MAYA_VER=2018
::set MAYA_VER=2020
set MAYA_INSTALL_PATH=C:\Program Files\Autodesk\Maya%MAYA_VER%
set MAYA_ENABLE_LEGACY_VIEWPORT=1


:: ----------------------------------------
:: ENV VAR
:: ----------------------------------------
call setenv.bat

:: ----------------------------------------
:: LAUNCH
:: ----------------------------------------
cd /d %MAYA_INSTALL_PATH%\bin
echo ==================================================
echo MAYA VERSION %MAYA_VER%
if "%1" == "" (
	echo GUI MODE
    echo ==================================================
	start "" "%MAYA_INSTALL_PATH%\bin\maya.exe"
) else (
	echo BATCH MODE
	echo CMD: %*
    echo ==================================================
	call "%MAYA_INSTALL_PATH%\bin\mayabatch.exe" %*
)


endlocal
