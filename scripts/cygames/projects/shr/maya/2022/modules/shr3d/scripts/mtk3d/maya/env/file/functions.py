# -*- coding: cp932 -*-
#===============================================
#
# �t�@�C�� �֘A
#
# Fujita Yukihiro
#
#===============================================
import os
import datetime
import math
import sys

#===============================================
# �w�肵���p�X�ɂ���f�B���N�g�����̃��X�g���擾
#
# @param vPath �w��p�X
#
# @return vDirs ���������f�B���N�g�����X�g
#===============================================
def getDirs(vPath, **kwargs):
    """ �w�肵���p�X�ɂ���f�B���N�g�����̃��X�g���擾 """

    vDirs = []

    for i in os.listdir(vPath):
        # �w��t�H���_�̃t�H���_���X�g���擾
        if os.path.isdir(os.path.join(vPath, i)):

            # ���X�g�ɒǉ�
            vDirs.append(i)

    return vDirs

#===============================================
# �w�肵���p�X�ɂ���t�@�C�����̃��X�g���擾
#
# @param vPath �w��p�X
#
# @keyward ext �g���q�̗L��
#
# @return vFiles ���������t�@�C�����X�g
#===============================================
def getFiles(vPath, **kwargs):
    """ �w�肵���p�X�ɂ���t�@�C�����̃��X�g���擾 """

    # �L�[���[�h�����擾�E�f�t�H���g�w��
    withExtention = kwargs.get("ext", True)

    vFiles = []

    for i in os.listdir(vPath):
        # �w��t�H���_�̃t�@�C�������擾
        if os.path.isfile(os.path.join(vPath, i)):

            # �g���q�Ȃ��w��̏ꍇ
            if withExtention == False:
                i = os.path.splitext(i)[0]

            # ���X�g�ɒǉ�
            vFiles.append(i)

    return vFiles

#===============================================
#
# �t�@�C�� �^�C���X�^���v�擾
#
# @param targetFile �Ώۃt�@�C��
# @return result �^�C���X�^���v
#
#===============================================
def getTimeStampStr(targetFile):

    # �Ώۃt�@�C���̃^�C���X�^���v���擾
    mTime_s = datetime.datetime.fromtimestamp(os.stat(targetFile).st_mtime);

    # �}�C�N���b��0�Ɂi�^�[�Q�b�g�����}�C�N���b���擾�ł��Ȃ��̂Łj
    # mTime_s = mTime_s.replace(microsecond = 0);

    # �Ώۃt�@�C���̍X�V����
    result = mTime_s.strftime('%Y/%m/%d %H:%M:%S');

    return result

#===============================================
#
# �t�@�C�� �^�C���X�^���v��r
#
# @param sourceFile ��r���t�@�C��
# @param targetFile ��r��t�@�C��
# @return result ��r����
#
#===============================================
def compareTimeStamp(sourceFile, targetFile):

    # �\�[�X�t�@�C���̃^�C���X�^���v���擾
    mTime_s = datetime.datetime.fromtimestamp(os.stat(sourceFile).st_mtime);

    # �}�C�N���b��0�Ɂi�^�[�Q�b�g�����}�C�N���b���擾�ł��Ȃ��̂Łj
    mTime_s = mTime_s.replace(microsecond = 0);

    #�\�[�X�t�@�C���̍X�V����
    key = mTime_s.strftime('%Y/%m/%d %H:%M:%S');

    # �^�[�Q�b�g�t�@�C�������݂��Ȃ��ꍇ
    if not os.path.isfile(targetFile):
        result = 'new';

    else:
        # �^�[�Q�b�g�t�@�C���̃^�C���X�^���v���擾
        mTime_t = datetime.datetime.fromtimestamp(os.stat(targetFile).st_mtime);

        # �}�C�N���b��0�Ɂi�^�[�Q�b�g�����}�C�N���b���擾�ł��Ȃ��̂Łj
        mTime_t = mTime_t.replace(microsecond = 0);

        # �\�[�X�t�@�C�����V�����ꍇ
        if mTime_s > mTime_t:
            result = 'update';

        # �����ꍇ
        elif mTime_s == mTime_t:
            result = 'equal';

        # �^�[�Q�b�g�t�@�C�����V�����ꍇ
        elif mTime_s < mTime_t:
            result = 'old';

    return result, key;


#===============================================
#
# �t�@�C���E�t�H���_�̃T�C�Y�𐮌`����������ŕԂ�
#
# @param    filePath    �t�@�C���E�t�H���_�̃t���p�X
# @keyward  unit        �P��:KB, MB, GB, Opt
# @keyward  pre         �����_����
# @keyward  cmm         �J���}��؂�̗L��
# @return   �t�@�C���T�C�Y�i���`���ꂽ������j
#
#===============================================
def getSizeStr(filePath, **options):

    # �p�X�̃t�@�C�����t�H���_�����݂��邩
    isFile = os.path.isfile(filePath)
    isFolder = os.path.isdir(filePath)

    # �t�@�C���E�t�H���_�����݂��Ȃ���ΏI��
    if isFile == isFolder == False:
        sys.stderr.write("File or Folder not found.\n")
        return False

    # �f�t�H���g�l
    unit = options.get("unit", "Opt")
    pre = options.get("pre", 3)
    cmm = options.get("cmm", True)

    #
    unitDict = {
        "KB" : 1024.0,
        "MB" : 1024.0 ** 2,
        "GB" : 1024.0 ** 3
    }

    # �t�@�C���T�C�Y���擾
    if isFile:
        fileSize = os.path.getsize(filePath)
    elif isFolder:
        fileSize = getFolderSize(filePath)

    # �P�ʎw�肪 opt �̏ꍇ�A�T�C�Y�𔻒肵�ĒP�ʂ����߂�
    if unit == "Opt":
        if fileSize < 1024:
            unit = "Bytes"
        elif fileSize < 1024 ** 2:
            unit = "KB"
        elif fileSize < 1024 ** 3:
            unit = "MB"
        elif fileSize < 1024 ** 4:
            unit = "GB"

    # �l��P�ʂɍ��킹��
    if unit in unitDict:
        fileSize = round(fileSize / unitDict[unit], pre)
    else:
        unit = "Bytes"

    # �����_�Ȃ��w��Ȃ琮����
    if pre == 0:
        fileSize = int(fileSize)

    # �R���}��؂�
    if cmm:
        fileSize = "{:,}".format(fileSize)

    # ������𐮌`���ĕԂ�
    return "%s %s" % (fileSize, unit)


#===============================================
#
# �t�H���_�̃T�C�Y��Ԃ�
#
# @param    path        �t�H���_�̃t���p�X
# @return   �T�C�Y
#
#===============================================
def getFolderSize(path):

    # �t�H���_�̃T�C�Y
    folderSize = 0

    # �t�H���_�����݂��Ȃ���ΏI��
    if os.path.isdir(path) == False:

        return folderSize

    for fileFolderName in os.listdir(path):
        fullPath = os.path.join(path, fileFolderName)

        # �t�@�C���̏ꍇ�A�T�C�Y�����v
        if os.path.isfile(fullPath):
            folderSize += os.path.getsize(fullPath)
        # �t�H���_�̏ꍇ�A�ċA�Ăяo��
        elif os.path.isdir(fullPath):
            folderSize += getFolderSize(fullPath)

    return folderSize


#===============================================
#
# �t�@�C���T�C�Y��r
#
# @param sourceFile ��r���t�@�C��
# @param targetFile ��r��t�@�C��
# @return result ��r����
#
#===============================================
def compareSize(sourceFile, targetFile):

    # �\�[�X�t�@�C�����Ȃ���ΏI��
    if os.path.isfile(sourceFile) == False:
        sys.stderr.write("File not found.\n")
        return False

    # �^�[�Q�b�g�t�@�C�����Ȃ��ꍇ
    if os.path.isfile(targetFile) == False:
        return "big"

    # �e�t�@�C���̃T�C�Y���擾
    size_s = os.path.getsize(sourceFile)
    size_t = os.path.getsize(targetFile)

    result = "equal"

    # �\�[�X�t�@�C�����傫���ꍇ
    if size_s > size_t:
        result = 'big'

    # �^�[�Q�b�g�t�@�C�����傫���ꍇ
    elif size_s < size_t:
        result = 'small'

    return result;


#===============================================
# �w�肵���p�X�ȉ��̃T�u�f�B���N�g�����܂ނ��ׂẴt�@�C���ƃf�B���N�g�����t���p�X�Ԃ�
#
# @param path �w��p�X
# @keyword    recursion �ċA�񐔁i��������K�w�̐[���j
#
# @return  ���������f�B���N�g���ƃt�@�C���̃t���p�X���X�g
#===============================================
def getDirsFiles(path, **options):

    # �f�t�H���g�l
    recursion  = options.get("recursion", 100)

    # �߂�l
    result = []

    # �w��p�X�����݂��Ȃ��A�������̓t�@�C���̏ꍇ�͏I��
    if not os.path.exists(path) or os.path.isfile(path):
        return False

    # �w��p�X�̃f�B���N�g���ƃt�@�C���̃��X�g���擾
    dirsFiles = os.listdir(path)

    tempDirs = []
    tempFiles = []

    # ���X�g����בւ� �F �f�B���N�g���A�t�@�C�� �̏�
    for i in dirsFiles:
        fullPath = os.path.join(path, i)

        if os.path.isdir(fullPath):
            tempDirs.append(i)
        else:
            tempFiles.append(i)

    # ���X�g�𖼑O���i�啶���A�������̋�ʂȂ��j�Ƀ\�[�g
    dirsFiles = sorted(tempDirs, key=str.lower) + sorted(tempFiles, key=str.lower)

    # �߂�l���X�g�ɗv�f��ǉ�
    for i in dirsFiles:
        fullPath = os.path.join(path, i)

        result.append(fullPath.replace(os.sep, "/"))

        # �f�B���N�g����������֐����ċA�Ăяo��
        if os.path.isdir(fullPath):

            if recursion != 0:
                result += getDirsFiles(fullPath, recursion = recursion-1)

    return result
