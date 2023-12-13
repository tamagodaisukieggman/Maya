@echo off
rem ======================================================================
rem Maya2022
rem ======================================================================

setlocal enabledelayedexpansion

set MAYA_VER=2022

echo %1

call %~dp0\mayabatch.bat %1

endlocal

exit /b