@echo off

setlocal

cd /d %~dp0

set TARGET_ROOT=%1
set EXPIRY_DATE=2023-12-31
set TIME_STAMP=%date:~0,4%%date:~5,2%%date:~8,2%
:: バッチと同じフォルダに出力する
set OUT_FOLDER=%CD%\cygames_%TIME_STAMP%

if not defined TARGET_ROOT (
    echo;
    echo 難読化したいフォルダをこの.batにドラッグ＆ドロップしてください
    echo;
    pause
    exit /b 1
)

:: .py以外のファイル(maya2022.batやreadme.txt)も外部協力会社へ渡したいので先に出力先に全部コピーしておく
robocopy %TARGET_ROOT% %OUT_FOLDER% /s /e /mir

:: 有効期限はつけなくてOK (2023/3 PM確認済み)
:: PyArmorはインストール時に環境変数のPATHに追加している前提
:: 難読化した.pyを出力
pyarmor-7 obfuscate --recursive --restrict 0 --exclude "pytransform,chara_utility\__init__.py,normal_editor\__init__.py,menu.py,userSetup.py" -O %OUT_FOLDER% %TARGET_ROOT%

endlocal

pause

exit /b