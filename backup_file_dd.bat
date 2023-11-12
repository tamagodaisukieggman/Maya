@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: �J�����g�f�B���N�g�����擾
set CURRENTDIR=%~dp0

::�����̓��t��ϐ��ɂ���
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set yyyy=%ldt:~0,4%
set mm=%ldt:~4,2%
set dd=%ldt:~6,2%
set tttt=%ldt:~8,4%

::
echo ���̎��ԂƓ��t %date% %time%
set /P CURRENTTIME="���t�Ǝ��Ԃ��w��(��:2023/11/12 18:29):"

:: �h���b�v���ꂽ�t�H���_
set ARGS=%*

::�o�b�N�A�b�v����t�H���_�̍쐬
set BACKUPDIR=%CURRENTDIR%backups\%yyyy%-%mm%-%dd%-%tttt%
md %BACKUPDIR%

for %%i in (%ARGS%) do (
  set "MODITIME=%%~ti"
  set "SRC=%%i"

  IF "!MODITIME!" GTR "%CURRENTTIME%" (
    set "modified=!SRC:%CURRENTDIR%=%BACKUPDIR%\!"
    xcopy !SRC! !modified! /D /S /R /Y /I /K /E
  ) ELSE (
    echo !MODITIME! %CURRENTTIME%
  )
)
