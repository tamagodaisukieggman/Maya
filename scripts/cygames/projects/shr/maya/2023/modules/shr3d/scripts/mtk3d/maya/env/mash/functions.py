# -*- coding: cp932 -*-
#===============================================
#
# MASH�֘A
#
# Fujita Yukihiro
#
#===============================================

import maya.cmds as cmds
import MASH.api as mapi

#===============================================
#
# �R���C�_�[��ǉ�
#
# @param      mashNetworkName : MASH �l�b�g���[�N��
# @param      colliderName : �R���C�_�[�m�[�h��
#
#===============================================
def addCollider(mashNetworkName, colliderName):
    """ �R���C�_�[��ǉ� """

    # �m�[�h�����݂��Ȃ���ΏI��
    if cmds.objExists(mashNetworkName) == False:
        print ("// " + mashNetworkName + u" ��������܂���B")
        return ""

    if cmds.objExists(colliderName) == False:
        print ("// " + colliderName + u" ��������܂���B")
        return ""

    # MASH �l�b�g���[�N���擾
    mashNetwork = mapi.Network(mashNetworkName)

    # �R���C�_�[��ǉ�
    mashNetwork.addCollider(colliderName)
