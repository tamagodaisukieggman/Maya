@echo off
rem ======================================================================
rem Maya2015
rem ======================================================================

setlocal enabledelayedexpansion

set MAYA_VER=2017

call %~dp0\mayabatch.bat %1

endlocal

exit /b