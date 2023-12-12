# -*- coding: cp932 -*-
#===============================================
#
# ���[�e�B���e�B
#
# Fujita Yukihiro
#
#===============================================

import maya.cmds as cmds
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
    if method == "set" and not isinstance(txt, str):
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


#===============================================
#
# �X���[�Y�o�C���h���ăE�F�C�g���R�s�[
#
# @param      msource_mesh: �R�s�[���̃��b�V��
# @param      forward_mesh:  �R�s�[��̃��b�V��
#
#===============================================
def bind_and_copy_weights(source_mesh, forward_mesh):
    """ �X���[�Y�o�C���h���ăE�F�C�g���R�s�[ """

    # �R�s�[���̃��b�V������W���C���g�A�X�L���N���X�^���擾
    root_joint = get_root_joint(source_mesh)

    skin_cluster = get_skin_cluster(source_mesh)

    # skinning mesh�ł͂Ȃ��ꍇ�A�������ďI��
    if not skin_cluster:
        return

    # �X�L���N���X�^�̍ő�C���t���G���X���̎擾
    max_influence = cmds.getAttr('{}.maxInfluences'.format(skin_cluster))

    # �R�s�[��̃��b�V�����X���[�Y�o�C���h�A�E�F�C�g�R�s�[
    cmds.skinCluster(forward_mesh, root_joint, omi=True, bm=1, mi=max_influence)

    # �E�F�C�g�R�s�[
    cmds.select([source_mesh, forward_mesh])
    cmds.copySkinWeights(sa='closestPoint', ia='closestJoint', nm=True)


#===============================================
#
# ���[�g�W���C���g�̎擾
#
# @param      mesh: ���b�V��
# @return     ���[�g�W���C���g
#
#===============================================
def get_root_joint(mesh):
    """ ���[�g�W���C���g�̎擾 """

    skin_cluster = get_skin_cluster(mesh)
    if not skin_cluster:
        return

    joints = cmds.ls(cmds.skinCluster(skin_cluster, q=True, influence=True), long=True)

    if not joints:
        return

    root_joint = None

    for _node in joints[0].split("|"):
        if _node and cmds.objectType(_node) == "joint":
            root_joint = _node
            break

    return root_joint


#===============================================
#
# skinCluster�̎擾
#
# @param      mesh: ���b�V��
# @return     skinCluster
#
#===============================================
def get_skin_cluster(mesh):
    """ skinCluster�̎擾 """

    skin_clusters = cmds.ls(cmds.listHistory(mesh), typ='skinCluster')
    if skin_clusters:
        return skin_clusters[0]
    else:
        return []


