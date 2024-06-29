@echo off

set "launcherPath=%~dp0"
echo setenv %launcherPath%

set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;%launcherPath%modules
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;%launcherPath%plug-ins
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%launcherPath%scripts
set MAYA_PRESET_PATH=%MAYA_PRESET_PATH%;%launcherPath%presets
set XBMLANGPATH=%XBMLANGPATH%;%launcherPath%prefs\icons
set MAYA_PACKAGE_PATH=%MAYA_PACKAGE_PATH%;%launcherPath%ApplicationPlugins

set PYTHONPATH=%PYTHONPATH%;%launcherPath%python;%launcherPath%;

set PYTHONPATH=%PYTHONPATH%;%MAYA_SCRIPT_PATH%
set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;%PYTHONPATH%

:: CharcoalEditor
:: ----------------------------------------
:: 環境のルートパスをリストに追加
:: ----------------------------------------
:: set "list="
:: set "string1=2020"
:: set "string2=2022"
:: set "string3=2023"
:: set "string4=2024"

:: set "list=!list!%string1% "
:: set "list=!list!%string2% "
:: set "list=!list!%string3% "
:: set "list=!list!%string4% "

:: for %%i in (%list%) do (
:: 	echo set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;%launcherPath%plug-ins\CharcoalEditor\%%i
:: 	set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;%launcherPath%plug-ins\CharcoalEditor\%%i
:: )

set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;%launcherPath%plug-ins\CharcoalEditor\2020
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;%launcherPath%plug-ins\CharcoalEditor\2022
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;%launcherPath%plug-ins\CharcoalEditor\2023
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;%launcherPath%plug-ins\CharcoalEditor\2024

:: ----------------------------------------
:: ApplicationPluginsの追加
:: ----------------------------------------
set MAYA_PACKAGE_PATH=%MAYA_PACKAGE_PATH%;%launcherPath%ApplicationPlugins\MayaBonusTools-2020-2024
set MAYA_PACKAGE_PATH=%MAYA_PACKAGE_PATH%;%launcherPath%ApplicationPlugins\SIWeightEditor-master
set MAYA_PACKAGE_PATH=%MAYA_PACKAGE_PATH%;%launcherPath%ApplicationPlugins\ngskintools2

:: ----------------------------------------
:: site-packagesの追加
:: ----------------------------------------
set PYTHONPATH=%PYTHONPATH%;%launcherPath%site-packages

:: ----------------------------------------
:: Legacy View Portの有効化
:: ----------------------------------------
MAYA_ENABLE_DEPRECATED_VIEWPORT=1