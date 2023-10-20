@echo off
set "currentDir=%~dp0"
set "myself=%~f0"

:: テキストファイルのパスを指定
set "filePath=%~dp0hierarchyCharaType.txt"

echo Current Directory: %currentDir%
echo File Path: %filePath%

:: 末尾のバックスラッシュを削除
set backCurrentDir=%currentDir:~0,-1%

:: 上の階層のディレクトリパスを取得
for %%i in (%backCurrentDir%) do set parentDir=%%~dpi


:: 末尾のバックスラッシュを削除
set parentDir=%parentDir:~0,-1%

:: 上の階層のディレクトリパスを取得
for %%i in (%parentDir%) do set parentParentDir=%%~dpi

:: 結果を表示
echo Parent Directory: %parentDir%
echo Parent Parent Directory: %parentParentDir%

set basePath=%parentParentDir%base\

:: テキストファイルからフォルダ階層を読み取り、フォルダまたはファイルを作成
for /f "usebackq delims=" %%A in ("%filePath%") do (
    :: Check if the line contains a file identifier (.)
    echo %%A | findstr /r ".*\..*" >nul
    if errorlevel 1 (
        :: Create folder
        if not exist "%currentDir%\%%A" (
            md "%%A"
            echo Created folder: %%A
        )
    ) else (
        :: Get the directory of the file
        for %%B in ("%%A") do (
            set "fileName=%%~nxB"
            set "fileDir=%%~dpB"
        )

        :: Create directory if it does not exist
        if not exist "%currentDir%\%fileDir%" (
            md "%fileDir%"
            echo Created folder: %fileDir%
        )

        :: Create file
        if not exist "%currentDir%\%%A" (
            echo. 2> "%%A"
            echo Created file: %%A
        )
    )
)

copy %basePath%buildCharaType.bat %currentDir%charaType\
copy %basePath%buildbase.xml %currentDir%charaType\
echo %currentDir%charaType\

:: 完了メッセージを表示
echo フォルダおよびファイルの作成が完了しました。
:: pause
