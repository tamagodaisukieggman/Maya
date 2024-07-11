@echo off

rem ------------------------------------
rem Env
rem ------------------------------------

set MAYA_VER=%1
set MAYA_FORCE_PANEL_FOCUS=0
set MAYA_INSTALL_PATH=C:\Program Files\Autodesk\Maya%MAYA_VER%\bin

echo %MAYA_INSTALL_PATH%

rem ------------------------------------
rem Maya
rem ------------------------------------

set FIX_PYTHON_SCRIPT=%2
set FIX_PYTHON_SCRIPT=%FIX_PYTHON_SCRIPT:__space__= %
set FIX_PYTHON_SCRIPT=python(%FIX_PYTHON_SCRIPT%);

echo %FIX_PYTHON_SCRIPT%

@REM TA�p ���g��mayaLegacy�p�X�ɏ��������ăR�����g�A�E�g���Ďg�p
@REM set MAYA_SCRIPT_PATH=D:\tech-designer\Maya\scripts
@REM set PYTHONPATH=D:\tech-designer\Maya\scripts;%localPythonSitepackagePath%;
@REM set XBMLANGPATH=C:\tkgpublic\designer_tools\Maya\icons
@REM set MAYA_UI_LANGUAGE=en_US

call "%MAYA_INSTALL_PATH%\mayabatch.exe" -noAutoloadPlugins -command "%FIX_PYTHON_SCRIPT%"

echo;
echo �����L�[�������Ƃ��̉�ʂ͕��܂�
echo;
pause
exit /b