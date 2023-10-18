@echo off

set "launcherPath=%~dp0"
echo setenv %launcherPath%

set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;%launcherPath%modules
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;%launcherPath%plug-ins
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%launcherPath%scripts
set MAYA_PRESET_PATH=%MAYA_PRESET_PATH%;%launcherPath%presets
set XBMLANGPATH=%XBMLANGPATH%;%launcherPath%prefs\icons

set PYTHONPATH=%PYTHONPATH%;%launcherPath%python;%launcherPath%;
