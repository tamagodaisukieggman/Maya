#!/bin/zsh

# Disable command echo
set +v

# Get the directory where the script is located
launcherPath="$(dirname "$0")"
echo "setenv $launcherPath"

# Append paths to the respective environment variables
export MAYA_MODULE_PATH="$MAYA_MODULE_PATH:$launcherPath/modules"
export MAYA_PLUG_IN_PATH="$MAYA_PLUG_IN_PATH:$launcherPath/plug-ins"
export MAYA_SCRIPT_PATH="$MAYA_SCRIPT_PATH:$launcherPath/scripts"
export MAYA_PRESET_PATH="$MAYA_PRESET_PATH:$launcherPath/presets"
export XBMLANGPATH="$XBMLANGPATH:$launcherPath/prefs/icons"
export MAYA_PACKAGE_PATH="$MAYA_PACKAGE_PATH:$launcherPath/ApplicationPlugins"

# Python paths
export PYTHONPATH="$PYTHONPATH:$launcherPath/python:$launcherPath"

# Append to PYTHONPATH for Maya scripts
export PYTHONPATH="$PYTHONPATH:$MAYA_SCRIPT_PATH"
export MAYA_SCRIPT_PATH="$MAYA_SCRIPT_PATH:$PYTHONPATH"

# CharcoalEditor plugin paths
export MAYA_PLUG_IN_PATH="$MAYA_PLUG_IN_PATH:$launcherPath/plug-ins/CharcoalEditor/2020"
export MAYA_PLUG_IN_PATH="$MAYA_PLUG_IN_PATH:$launcherPath/plug-ins/CharcoalEditor/2022"
export MAYA_PLUG_IN_PATH="$MAYA_PLUG_IN_PATH:$launcherPath/plug-ins/CharcoalEditor/2023"
export MAYA_PLUG_IN_PATH="$MAYA_PLUG_IN_PATH:$launcherPath/plug-ins/CharcoalEditor/2024"

# ApplicationPlugins additions
export MAYA_PACKAGE_PATH="$MAYA_PACKAGE_PATH:$launcherPath/ApplicationPlugins/MayaBonusTools-2020-2024"
export MAYA_PACKAGE_PATH="$MAYA_PACKAGE_PATH:$launcherPath/ApplicationPlugins/SIWeightEditor-master"
export MAYA_PACKAGE_PATH="$MAYA_PACKAGE_PATH:$launcherPath/ApplicationPlugins/ngskintools2"

# Additional site-packages
export PYTHONPATH="$PYTHONPATH:$launcherPath/site-packages"

