@echo off
set "currentDir=%~dp0"
set "myself=%~f0"

:: �e�L�X�g�t�@�C���̃p�X���w��
set "filePath=%~dp0hierarchyCharaType.txt"

echo Current Directory: %currentDir%
echo File Path: %filePath%

:: �����̃o�b�N�X���b�V�����폜
set backCurrentDir=%currentDir:~0,-1%

:: ��̊K�w�̃f�B���N�g���p�X���擾
for %%i in (%backCurrentDir%) do set parentDir=%%~dpi


:: �����̃o�b�N�X���b�V�����폜
set parentDir=%parentDir:~0,-1%

:: ��̊K�w�̃f�B���N�g���p�X���擾
for %%i in (%parentDir%) do set parentParentDir=%%~dpi

:: ���ʂ�\��
echo Parent Directory: %parentDir%
echo Parent Parent Directory: %parentParentDir%

set basePath=%parentParentDir%base\

:: �e�L�X�g�t�@�C������t�H���_�K�w��ǂݎ��A�t�H���_�܂��̓t�@�C�����쐬
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

:: �������b�Z�[�W��\��
echo �t�H���_����уt�@�C���̍쐬���������܂����B
:: pause
