@echo off
rem ======================================================================
rem Maya2019
rem ======================================================================

setlocal enabledelayedexpansion

set MAYA_VER=2019

call %~dp0\mayabatch.bat %1

endlocal

exit /b