@echo off
cd /d %~dp0
:: ----------------------------------------
:: Maya VERSION
:: ---------------------------------------- 
set MAYA_VER=2019
set MAYA_INSTALL_PATH=C:\Program Files\Autodesk\Maya%MAYA_VER%
:: ----------------------------------------
:: ENV VAR
:: ----------------------------------------
cd /d %~dp0
cd /d ..\..\..\..\2019\bat
echo %cd%
echo setenv.bat
call setenv.bat
call %cd%\..\..\share\bat\setenv.bat

cd /d %~dp0
set PYTYHON_FILE=%CD%\bat_command.py
:: ----------------------------------------
:: LAUNCH
:: ----------------------------------------
cd /d %MAYA_INSTALL_PATH%\bin
echo ==================================================
echo Maya VERSION %MAYA_VER%
echo BATCH MODE
echo ==================================================

echo Retarget: Start
"%MAYA_INSTALL_PATH%\bin\mayapy.exe" "%PYTYHON_FILE%" "%~1"

echo Retarget: End
echo;

pause

exit /b
