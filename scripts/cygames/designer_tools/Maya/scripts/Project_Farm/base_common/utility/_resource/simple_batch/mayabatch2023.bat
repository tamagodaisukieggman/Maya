@echo off
rem ======================================================================
rem Maya2023
rem ======================================================================

setlocal enabledelayedexpansion

set MAYA_VER=2023

echo %1

call %~dp0\mayabatch.bat %1

endlocal

exit /b