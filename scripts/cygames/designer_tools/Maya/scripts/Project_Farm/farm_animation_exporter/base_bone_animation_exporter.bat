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
set PYTYHON_FILE=%CD%\bat_command.pyc
:: ----------------------------------------
:: LAUNCH
:: ----------------------------------------
cd /d %MAYA_INSTALL_PATH%\bin
echo ==================================================
echo Maya VERSION %MAYA_VER%
echo BATCH MODE
echo ==================================================
:LOOP
if not "%~1"=="" (
    :: echo %~1
    if defined EXPORT_FILES (
        set EXPORT_FILES=%EXPORT_FILES%;%~1
    ) else (
        set EXPORT_FILES=%~1
    )
    shift
    goto LOOP
)

set EXPORT_FILES=%EXPORT_FILES%
set EX_EXCLUDE="True"
echo Export: Start
"%MAYA_INSTALL_PATH%\bin\mayapy.exe" %PYTYHON_FILE%

echo Export: End
echo;

pause

exit /b