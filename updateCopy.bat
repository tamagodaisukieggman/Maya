@echo off
setlocal

:: 以下の変数を設定します。
:: SRC_FOLDER - ソースフォルダのパス
:: DEST_FOLDER - コピー先のフォルダのパス
:: MIN_DATE - ファイルが変更された最小日付 (形式: YYYYMMDD)
:: MIN_TIME - ファイルが変更された最小時間 (形式: HHMM)

:: 例:
set SRC_FOLDER=%~dp0
echo SRC_FOLDER %SRC_FOLDER%

set DEST_FOLDER=%SRC_FOLDER%destination
echo DEST_FOLDER %DEST_FOLDER%

set /P MIN_DATE="20231110"
set MIN_DATE=%MIN_DATE:\=/%
echo MIN_DATE %MIN_DATE%

set /P MIN_TIME="0800"
set MIN_TIME=%MIN_TIME:\=/%
echo MIN_TIME %MIN_TIME%

:: YYYYMMDDHHMM 形式で結合した日付と時間の文字列を作成します。
set MIN_DATETIME=%MIN_DATE%%MIN_TIME%
echo MIN_DATETIME %MIN_DATETIME%

:: robocopyコマンドを使用して、指定した日付と時間以降に更新されたファイルをコピーします。
robocopy %SRC_FOLDER% %DEST_FOLDER% /MAXAGE:%MIN_DATETIME% /E

endlocal
