@echo off
set "source_folder=%~dp0\maya\scripts\tkgTools"
set "destination_folder=C:\Users\%USERNAME%\Documents\maya\scripts\tkgTools"

if not exist "%source_folder%" (
    echo Source folder not found.
    exit /b 1
)

if not exist "%destination_folder%" (
    echo Destination folder not found.
    exit /b 1
)

echo Copying folders from "%source_folder%" to "%destination_folder%"
xcopy "%source_folder%\*" "%destination_folder%" /E /I /Y

echo Folders copied successfully.

pause
