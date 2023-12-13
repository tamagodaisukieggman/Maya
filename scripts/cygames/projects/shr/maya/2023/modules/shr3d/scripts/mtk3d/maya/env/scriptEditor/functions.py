# -*- coding: cp932 -*-
#===============================================
#
# �X�N���v�g�֘A
#
# Fujita Yukihiro
#
#===============================================
import maya.cmds as cmds
#import maya.mel as mel
#import pymel.core as pm

#-----------------------------------------------
# �J�����g�^�u�̃v���V�[�W�����X�g���擾
#-----------------------------------------------
def getProcedures(gLastFocusedCommandControl):
    
    # �R�[�h�S�̂��擾
    wholeCode = cmds.cmdScrollFieldExecuter(gLastFocusedCommandControl, q=True, text=True)

    # �e�s���擾
    lines = wholeCode.split("\n")
    
    # �s�ԍ�
    lineNumber = 1
    
    # �R�����g�u���b�N�t���O
    isComment = False

    procedureName = "notFound"

    # ���������v���V�[�W�����X�g
    procedures = []

    # �s���Ƃ̏���
    for line in lines:
        # �R�����g����
        commentStartIndex = line.find("//")
        
        # // ������������R�����g�폜
        if commentStartIndex != -1:
            line = line[:commentStartIndex]

        # ������u���b�N����
        stringStartIndex = line.find('"')
        stringEndIndex = line.rfind('"')
        
        # ������u���b�N������Ε�����u���b�N�����폜
        if stringStartIndex != -1:
            line = line[:stringStartIndex] + line[stringEndIndex+2:]
            
        # �R�����g�u���b�N�̊J�n������
        commentStartIndex = line.find("/*")
        
        # �R�����g�u���b�N�̏I��������
        commentEndIndex = line.find("*/")
        
        # /* �� */ ������������
        if commentStartIndex != -1 and commentEndIndex != -1:

            # /* �̌�� */ ������ꍇ�A�R�����g�������폜
            if commentStartIndex < commentEndIndex:
                
                # �R�����g�u���b�N������Ȃ��Ȃ�
                if not isComment:
                    line = line[:commentStartIndex] + line[commentEndIndex+2:]
                # �R�����g�u���b�N���Ȃ�
                else:
                    line = line[commentEndIndex+2:]
                
                isComment = False
                
                # �v���V�[�W���錾�`�F�b�N
                procedureName = checkProcedure(line)
            
            # /* �̑O�� */ ������ꍇ�A�R�����g�������폜
            else:
                line = line[commentEndIndex+2:commentStartIndex]
                
                # �R�����g�u���b�N������Ȃ��Ȃ�v���V�[�W���錾�`�F�b�N
                if not isComment:
                    procedureName = checkProcedure(line)
                
                isComment = True
                
        # /* �̂݌��������ꍇ�A�R�����g�������폜
        elif commentStartIndex != -1:
            line = line[:commentStartIndex]

            # �R�����g�u���b�N������Ȃ��Ȃ�v���V�[�W���錾�`�F�b�N
            if not isComment:
                procedureName = checkProcedure(line)

            isComment = True
    
        # */ �̂݌��������ꍇ�A�R�����g�������폜
        elif commentEndIndex != -1:
            line = line[commentEndIndex+2:]
            
            isComment = False
            
            # �v���V�[�W���錾�`�F�b�N
            procedureName = checkProcedure(line)
            
        else:
            # �R�����g�u���b�N������Ȃ��Ȃ�v���V�[�W���錾�`�F�b�N
            if not isComment:
                procedureName = checkProcedure(line)

        if procedureName == "notFound":
            pass
        elif procedureName is None:
            pass
        else:
            if procedureName.find("(") != -1:
                procedureName = procedureName[:procedureName.index("(")]
            
            # �v���V�[�W���� �s�ԍ� �̌`��
            procedures.append(procedureName + " " + str(lineNumber))
            #procedures.append(lineNumber)
            
        lineNumber = lineNumber + 1

    return procedures
    
#-----------------------------------------------
# �v���V�[�W��������
#-----------------------------------------------
def checkProcedure(line):

    if len(line) == 0:
        return

    # �s�̊e�P����擾
    words = line.split()
    
    if len(words) == 0:
        return
    
    # �ϐ��^���X�g
    variableTypes = ["int", "int[]", "float", "float[]", "string", "string[]", "vector", "vector[]", "matrix"]
    
    procedureName = "notFound"
    
    if "proc" in words:
        procIndex = words.index("proc")
        
        # �s���v���V�[�W���錾�݂̂ŏI����Ă��Ȃ��ꍇ
        if len(words)-1 > procIndex:

            # �v���V�[�W�����߂�l���w�肵�Ă���ꍇ
            if words[procIndex + 1] in variableTypes:

                # �s���߂�l�̎w��ŏI����Ă��Ȃ��ꍇ
                if len(words)-2 > procIndex:
                    procedureName = words[procIndex + 2]

            # �v���V�[�W�����߂�l���w�肵�Ă��Ȃ��ꍇ
            else:
                procedureName = words[procIndex + 1]

    return procedureName

#-----------------------------------------------
# �J�����g�^�u�̊֐����X�g���擾
#-----------------------------------------------
def getFunctions(gLastFocusedCommandControl):
    
    # �R�[�h�S�̂��擾
    wholeCode = cmds.cmdScrollFieldExecuter(gLastFocusedCommandControl, q=True, text=True)

    # �e�s���擾
    lines = wholeCode.split("\n")
    
    # �s�ԍ�
    lineNumber = 1
    
    functionName = "notFound"

    # ���������֐����X�g
    functions = []
    

    # �s���Ƃ̏���
    for line in lines:
        # �R�����g����
        commentStartIndex = line.find("#")
        
        # // ������������R�����g�폜
        if commentStartIndex != -1:
            line = line[:commentStartIndex]

        functionName = checkFunction(line)

        if functionName == "notFound":
            pass
        elif functionName is None:
            pass
        else:
            if functionName.find("(") != -1:
                functionName = functionName[:functionName.index("(")]
            
            # �v���V�[�W���� �s�ԍ� �̌`��
            functions.append(functionName + " " + str(lineNumber))
            #procedures.append(lineNumber)
            
        lineNumber = lineNumber + 1

    return functions
    
#-----------------------------------------------
# �֐�������
#-----------------------------------------------
def checkFunction(line):

    if len(line) == 0:
        return

    # �s�̊e�P����擾
    words = line.split()
    
    if len(words) == 0:
        return

    functionName = "notFound"

    if "def" in words:
        defIndex = words.index("def")

        # �s���֐��錾�݂̂ŏI����Ă��Ȃ��ꍇ
        if len(words)-1 > defIndex:

            functionName = words[defIndex + 1]

    return functionName
