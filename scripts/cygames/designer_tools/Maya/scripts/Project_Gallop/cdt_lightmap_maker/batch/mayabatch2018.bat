@echo off
rem ======================================================================
rem Maya2018
rem ======================================================================

setlocal enabledelayedexpansion

set MAYA_VER=2018

call %~dp0\mayabatch.bat %1

endlocal

exit /b