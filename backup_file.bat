@echo off
::for���ŕ�����u�������邽�߂ɕK�v
setlocal EnableExtensions EnableDelayedExpansion

:: �J�����g�f�B���N�g�����擾
set CURRENTDIR=%~dp0

:: �����̃o�b�N�X���b�V�����폜
set BACKCURRENTDIR=%CURRENTDIR:~0,-1%

:: ��̊K�w�̃f�B���N�g���p�X���擾
for %%i in (%BACKCURRENTDIR%) do set PARENTCURRENTDIR=%%~dpi

::�����̓��t��ϐ��ɂ���
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set yyyy=%ldt:~0,4%
set mm=%ldt:~4,2%
set dd=%ldt:~6,2%
set tttt=%ldt:~8,4%

::
echo ���̎��ԂƓ��t %date% %time%
set /P CURRENTTIME="���t�Ǝ��Ԃ��w��(��:2023/11/12 18:29):"

::�o�b�N�A�b�v����t�H���_�̍쐬
set BACKUPDIR=%PARENTCURRENTDIR%backups\%yyyy%-%mm%-%dd%-%tttt%
md %BACKUPDIR%

::���̃o�b�`�t�@�C���̃f�B���N�g���K�w����X�V��(/D)�������̃t�@�C���������R�s�[����
::echo F |�͊m�F�������I�Ƀt�@�C��(F)�ŏ������邽�߂ɕt����
for /r %%a in ('forfiles /P %CURRENTDIR% /S /M *.* /D +0 /C "cmd /c echo @path"') do (
  set "MODITIME=%%~ta"
  set "SRC=%%~a"

  IF "!MODITIME!" GTR "%CURRENTTIME%" (
    set "modified=!SRC:%CURRENTDIR%=%BACKUPDIR%\!"
    echo �Ώۃt�@�C�� !SRC!
    echo �R�s�[��̃p�X !modified!
    echo F | xcopy !SRC! !modified! /D /S /R /Y /I /K /E
  ) ELSE (
    rem
  )
)

::zip���k
set folder=%BACKUPDIR%
set zipfile=%BACKUPDIR%.zip

if not exist "%folder%" (
    echo �w�肳�ꂽ�t�H���_�����݂��܂���B
    exit /b 1
)

if "%zipfile%"=="" (
    set zipfile=%folder%.zip
)

echo %folder% �� %zipfile% �Ɉ��k���Ă��܂�...
powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('%folder%', '%zipfile%'); }"

if %errorlevel%==0 (
    echo ���k���������܂����B
) else (
    echo ���k���ɃG���[���������܂����B
)

pause

::���̃t�H���_�̍폜
::rd /s /q %folder%
::echo Folder has been deleted successfully.
