@echo off
cd /d "Z:\"

::======================================================================
set PIVOT_FRAME=None
set TO_FPS=59.94
set CHECKOUT=1
::======================================================================

set CURRENT_DIR=%~dp0

echo ###################################################################
echo FPS コンバート処理を実行します。
set /P OUTPUT_DIR= "出力ディレクトリを指定して下さい。 >>> "
if not exist %OUTPUT_DIR% (mkdir %OUTPUT_DIR%)

set OUTPUT_DIR=%OUTPUT_DIR:\=/%

set ARGS=%*
set ARGS=%ARGS:\=/%

set LOG_FILE=%OUTPUT_DIR%\convert_log.log

set PYTHONPATH=%PYTHONPATH%;%CURRENT_DIR%\scripts;
set COMMAND="import convert_fps;convert_fps.convert_scenes(u'%OUTPUT_DIR%', u'%ARGS%', scale_pivot_frame=%PIVOT_FRAME%, to_fps='%TO_FPS%', checkout=%CHECKOUT%)"

call  T:\tools\projects\mutsunokami\inhouse\win\extension\maya\share\packages\mtku\v1.0\modules\bat\setenv.bat 2018
call "%MAYA_INSTALL_PATH%\bin\mayabatch.exe" -command "python("%COMMAND%")"
:: call "%MAYA_INSTALL_PATH%\bin\mayabatch.exe" -command "python("%COMMAND%")" -log %LOG_FILE%

pause

exit /b 0
