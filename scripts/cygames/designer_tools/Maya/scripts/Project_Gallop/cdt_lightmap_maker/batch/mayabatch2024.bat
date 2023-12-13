@echo off
rem ======================================================================
rem Maya2022
rem ======================================================================

setlocal enabledelayedexpansion

set MAYA_VER=2024

call %~dp0\mayabatch.bat %1

endlocal

exit /b