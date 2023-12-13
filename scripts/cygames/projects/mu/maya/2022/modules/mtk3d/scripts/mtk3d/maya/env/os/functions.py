# -*- coding: cp932 -*-
#===============================================
#
# OS / �V�X�e�� �֘A
#
# Fujita Yukihiro
#
#===============================================

import os
import subprocess

#===============================================
#
# �o�b�`�R�}���h���E�B���h�E�Ȃ��Ŏ��s
#
# @param      commandStr : �R�}���h
# @return
#
#===============================================
def execBatchCmd(commandStr):
    """ �o�b�`�R�}���h���E�B���h�E�����Ŏ��s """

    # �����������񂶂�Ȃ���ΏI��
    if not isinstance(commandStr, str):
        return False

    # �ꎞ�t�@�C��
    tempBatFileName = os.path.join(os.getenv("TMP"), "fy_temp.bat")
    tempVbsFileName = os.path.join(os.getenv("TMP"), "fy_temp.vbs")

    # �o�b�`�t�@�C���쐬
    tempBatFile = open(tempBatFileName, "w")
    tempBatFile.write(commandStr)
    tempBatFile.close()

    # vbs �t�@�C���쐬�i�o�b�`���s���ɃE�B���h�E��\�������Ȃ��p�Ɂj
    tempVbsFile = open(tempVbsFileName, "w")
    tempVbsFile.write('CreateObject("WScript.Shell").Run "' + tempBatFileName + '",0')
    tempVbsFile.close()

    # vbs �t�@�C�����s
    subprocess.call(tempVbsFileName, shell=True)

    return True
