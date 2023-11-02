@echo off
setlocal enabledelayedexpansion

:: ----------------------------------------
:: batをたたいたらMayaのバージョンを取得する
:: ----------------------------------------
cd /d %~dp0
set "currentDir=%~dp0"

set "filename=%~n0"
set "replacement=maya"
set "MAYA_VER=!filename:%replacement%=!"

echo Maya Version:%MAYA_VER%

:: ----------------------------------------
:: Mayaからインストールパスを指定
:: ----------------------------------------
set MAYA_INSTALL_PATH=C:\Program Files\Autodesk\Maya%MAYA_VER%

:: ----------------------------------------
:: 基本環境変数の設定
:: ----------------------------------------
set PYTHONDONTWRITEBYTECODE=1
set MAYA_UI_LANGUAGE=en_US
set MAYA_ENABLE_LEGACY_VIEWPORT=1

:: ----------------------------------------
:: 環境のルートパスをリストに追加
:: ----------------------------------------
set "list="
set "string1=%currentDir%tkgTools"
set "string2=%currentDir%thirdparty"
set "string3=%currentDir%inhouse"

set "list=!list!%string1% "
set "list=!list!%string2% "
set "list=!list!%string3% "

:: ----------------------------------------
:: ルートパスのリストからそれぞれの環境変数を設定
:: ----------------------------------------
for %%i in (%list%) do (
  call %%i\setenv.bat
)

:: ----------------------------------------
:: LAUNCH
:: ----------------------------------------
cd /d %MAYA_INSTALL_PATH%\bin
echo ==================================================
echo MAYA VERSION %MAYA_VER%
if "%1" == "" (
	echo GUI MODE
    echo ==================================================
	start "" "%MAYA_INSTALL_PATH%\bin\maya.exe"
) else (
	echo BATCH MODE
	echo CMD: %*
    echo ==================================================
	call "%MAYA_INSTALL_PATH%\bin\mayabatch.exe" %*
)

pause
