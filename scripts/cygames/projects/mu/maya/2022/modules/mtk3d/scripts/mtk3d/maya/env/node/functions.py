# -*- coding: cp932 -*-
#===============================================
#
# �m�[�h�֘A
#
# Fujita Yukihiro
#
#===============================================

import maya.cmds as cmds

#===============================================
#
# �ŏ�ʃm�[�h���擾
#
# @param      nodeName : �m�[�h��
# @return     �ŏ�ʃm�[�h��
#
#===============================================
def getRootNodeName(nodeName):
    """ �ŏ�ʂ̃m�[�h�����擾 """

    # �m�[�h�l�[������Ȃ�I��
    if nodeName == "":
        return ""

    # �m�[�h�����݂��Ȃ���ΏI��
    if cmds.objExists(nodeName) == False:
        print ("// " + nodeName + u" ��������܂���B")
        return ""

    # �m�[�h���g�����X�t�H�[���m�[�h����Ȃ���ΏI��
    if cmds.objectType( nodeName, isType='transform' ) == False:
        print ("// " + nodeName + u" �̓g�����X�t�H�[���m�[�h�ł͂���܂���B")
        return ""
    
    # �m�[�h�̃t���p�X�����擾
    fullPathName = cmds.ls( nodeName, long=True)
    
    # �t���p�X���𕪊�
    tokens = fullPathName[0].split("|")
    
    # ���[���h�̎q�̏ꍇ
    if nodeName == tokens[1]:
        return nodeName
    else:
        # ���X�g�̂Q�Ԗڂ�Ԃ��B��Ԗڂ͋󔒂�����̂ŁB
        return tokens[1]


#===============================================
#
# �w�肵���m�[�h�K�w�̒�����A�w�肵����������܂ރm�[�h���擾
#
# @param      targetNode : �Ώۃm�[�h�K�w
# @param      searchStrs : ���������񃊃X�g
# @return     �}�b�`�����m�[�h���X�g
#
#===============================================
def searchNodesContains(targetNode, searchStrs):
    """ �w�肵���m�[�h�K�w�̒�����A�w�肵���������S�Ċ܂ރm�[�h���擾 """
    
    # �m�[�h�����݂��Ȃ���ΏI��
    if cmds.objExists(targetNode) == False:
        print ("// " + targetNode + u" ��������܂���B")
        return []
    
    if len(searchStrs) == 0:
        print (u"// ���������񂪎w�肳��Ă��܂���B")
        return []

    # �S�Ă̎q�m�[�h�Ƒ��m�[�h���擾
    allDescendents = cmds.listRelatives(targetNode, allDescendents=True, path=True, type="transform", noIntermediate=True)

    if allDescendents is None:
        return []

    # �}�b�`�����m�[�h���X�g
    matchedNodes = []

    for elm in allDescendents:
        
        # �m�[�h���𕪊�
        tokens = elm.split("|")
        
        counts = 0
        
        for str in searchStrs:
            
            # ���������񂪃m�[�h���Ɋ܂܂�Ă��邩
            if str in tokens[-1]:
                counts += 1
                
        # ���������񂪑S�ăm�[�h���Ɋ܂܂�Ă�����
        if len(searchStrs) == counts:
            matchedNodes.append(elm)

    return matchedNodes



