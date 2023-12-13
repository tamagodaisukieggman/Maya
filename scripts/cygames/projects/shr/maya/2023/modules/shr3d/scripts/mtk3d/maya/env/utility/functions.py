# -*- coding: cp932 -*-
#===============================================
#
# ���[�e�B���e�B
#
# Fujita Yukihiro
#
#===============================================

import os
import time
import mtk3d.maya.env.os.functions as envos

#===============================================
#
# �e�L�X�g �N���b�v�{�[�g
#
# @param      method : set,get
# @param      txt : �N���b�v�{�[�h�ɓn��������
# @return     �N���b�v�{�[�h�̕�����
#
#===============================================
def textClipboard(method, txt=""):
    """ �e�L�X�g���N���b�v�{�[�h�ɃR�s�[�A�N���b�v�{�[�h����擾 """

    # �R�s�[����txt �����������񂶂�Ȃ���ΏI��
    if method == "set" and not isinstance(txt, (str, unicode)):
        return False

    elif method != "set" and method != "get":
        return False

    # �ꎞ�t�@�C��
    tempFileName = os.path.join(os.getenv("TMP"), "fy_tempClipboard.txt") 
    
    # �N���b�v�{�[�h�ɃR�s�[�̏ꍇ�A�ꎞ�t�@�C���ɏ�������
    if method == "set":
        tempFile = open(tempFileName, "w")
        tempFile.write(txt)
        tempFile.close()
    
        # �ꎞ�t�@�C���̓��e���N���b�v�{�[�h�ɃR�s�[����R�}���h
        batCmd = "clip < " + tempFileName

    elif method == "get":
        # �N���b�v�{�[�h�̓��e���ꎞ�t�@�C���ɏ����o���R�}���h
        batCmd = 'mshta.exe "vbscript:Execute("str=window.clipboardData.getData(""text""):CreateObject(""Scripting.FileSystemObject"").GetStandardStream(1).Write(str^&""""):close")" > ' + tempFileName

    else:
        return False
        
    # �o�b�`�R�}���h���s
    envos.execBatchCmd(batCmd)

    # �N���b�v�{�[�h����擾�̏ꍇ
    if method == "get":
        #�E�F�C�g
        time.sleep(0.3)
        
        # �ꎞ�t�@�C������ǂݍ���
        tempFile = open(tempFileName, "r")
        txt = tempFile.read()
        tempFile.close()
    
        return txt
    else:
        return True
