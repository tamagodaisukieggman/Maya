#!/bin/zsh
# Turn off echoing each command
set +v

# Capture the current directory based on the location of this script
currentDir=$(dirname "$0")
cd "$currentDir"

# Extract the Maya version from the script's filename
filename=$(basename "$0")
noExtFile="${filename%.*}"
replacement="maya"
MAYA_VER=${noExtFile/$replacement/}

echo "Maya Version: $MAYA_VER"

# Specify the Maya install path
MAYA_INSTALL_PATH="/Applications/Autodesk/maya$MAYA_VER"

# Set basic environment variables
export PYTHONDONTWRITEBYTECODE=1
export MAYA_UI_LANGUAGE="en_US"
export MAYA_ENABLE_LEGACY_VIEWPORT=1

# Append paths to the list
list=()
string1="$currentDir/tkgTools"
string2="$currentDir/thirdparty"
string3="$currentDir/inhouse"

list+=("$string1")
list+=("$string2")
list+=("$string3")

# Set environment variables from each path
for i in "${list[@]}"; do
  source "$i/setenv.sh" # Assuming setenv.sh is the equivalent of setenv.bat
done

# Launch Maya
cd "$MAYA_INSTALL_PATH/bin"
echo "=================================================="
echo "MAYA VERSION $MAYA_VER"
if [[ -z "$1" ]]; then
    echo "GUI MODE"
    echo "=================================================="
    open -a "$MAYA_INSTALL_PATH/Maya.app/Contents/bin/maya" # Assumes Maya.app is the correct application bundle
else
    echo "BATCH MODE"
    echo "CMD: $@"
    echo "=================================================="
    "$MAYA_INSTALL_PATH/bin/mayabatch" "$@" # Run mayabatch with arguments
fi
