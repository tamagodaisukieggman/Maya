@echo off
set "currentDir=%~dp0"
set "myself=%~f0"

:: テキストファイルのパスを指定
set "filePath=%~dp0hierarchyProjectFolders.txt"

echo Current Directory: %currentDir%
echo File Path: %filePath%

set basePath=%currentDir:projects=base%
echo Base Path: %basePath%

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

copy %basePath%createCharaType.bat %currentDir%\projectName\
copy %basePath%hierarchyCharaType.txt %currentDir%\projectName\
call %currentDir%\projectName\createCharaType.bat

:: 完了メッセージを表示
echo フォルダおよびファイルの作成が完了しました。
:: pause
