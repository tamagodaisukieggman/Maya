@echo off

setlocal

cd /d %~dp0

set TARGET_ROOT=%1
set EXPIRY_DATE=2023-12-31
set TIME_STAMP=%date:~0,4%%date:~5,2%%date:~8,2%
:: �o�b�`�Ɠ����t�H���_�ɏo�͂���
set OUT_FOLDER=%CD%\tkgpublic_%TIME_STAMP%

if not defined TARGET_ROOT (
    echo;
    echo ��ǉ��������t�H���_������.bat�Ƀh���b�O���h���b�v���Ă�������
    echo;
    pause
    exit /b 1
)

:: .py�ȊO�̃t�@�C��(maya2022.bat��readme.txt)���O�����͉�Ђ֓n�������̂Ő�ɏo�͐�ɑS���R�s�[���Ă���
robocopy %TARGET_ROOT% %OUT_FOLDER% /s /e /mir

:: �L�������͂��Ȃ���OK (2023/3 PM�m�F�ς�)
:: PyArmor�̓C���X�g�[�����Ɋ��ϐ���PATH�ɒǉ����Ă���O��
:: ��ǉ�����.py���o��
pyarmor-7 obfuscate --recursive --restrict 0 --exclude "pytransform,chara_utility\__init__.py,normal_editor\__init__.py,menu.py,userSetup.py" -O %OUT_FOLDER% %TARGET_ROOT%

endlocal

pause

exit /b