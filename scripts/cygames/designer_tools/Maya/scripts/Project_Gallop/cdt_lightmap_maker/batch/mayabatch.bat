@echo off

rem ------------------------------------
rem Env
rem ------------------------------------

set MAYA_FORCE_PANEL_FOCUS=0
set MAYA_INSTALL_PATH=C:\Program Files\Autodesk\Maya%MAYA_VER%\bin

rem ------------------------------------
rem Maya
rem ------------------------------------

set PYTHON_SCRIPT=python(\"import Project_Gallop.cdt_lightmap_maker.main as lightmap_maker;lightmap_maker.batch()\");

call "%MAYA_INSTALL_PATH%\mayabatch.exe" -noAutoloadPlugins -command "%PYTHON_SCRIPT%"

exit /b