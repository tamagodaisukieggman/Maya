@echo off

rem cd /d %~dp0
set CURRENT_DIR=%~dp0

echo CURRENT_DIR: %CURRENT_DIR%

:: �����̃o�b�N�X���b�V�����폜
set CURRENT_DIR=%CURRENT_DIR:~0,-1%

:: ��̊K�w�̃f�B���N�g���p�X���擾
for %%i in (%CURRENT_DIR%) do set PARENT_DIR=%%~dpi

:: ���ʂ�\��
echo Current Directory: %CURRENT_DIR%
echo Parent Directory: %PARENT_DIR%
pause

set SCRIPT_DIR=%CURRENT_DIR:\projects\wizard2=%

::Maya Settings
set MAYA_UI_LANGUAGE=en_US
set MAYA_CMD_FILE_OUTPUT=%SCRIPT_DIR%/maya_cmdFileOutput.log
set PYTHONPATH=%PYTHONPATH%;%SCRIPT_DIR%;
rem echo �ꎞ�I��PYTHONPATH���w��: %PYTHONPATH%

echo PYTHONPATH: %PYTHONPATH%
pause

echo -------------Build biped-------------

echo Maya�̃o�[�W�������w�肵�Ă��������B
set /P MAYA_VERSION="2018, 2019, 2020 :"
set MAYA_VERSION=%MAYA_VERSION:\=/%

::biped
set COMMAND="from tkgTools.tkgRig.scripts.build import rigbuild;rb=rigbuild.Build(types='biped', excactDir='wizard2_base_00_000');rb.main()"
call "C:\Program Files\Autodesk\Maya"%MAYA_VERSION%"\bin\mayabatch.exe" -command python(\"%COMMAND%\")"

::Folder Open
start "" "%SCRIPT_DIR%/types/biped/wizard2_base_00_000/000_data"
rem start "" "%SCRIPT_DIR%/types/biped/wizard2_base_00_000/data"
rem start "" "%SCRIPT_DIR%/types/biped/wizard2_base_00_000/data"

pause
