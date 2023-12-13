# -*- coding: shift-jis -*-
import maya.cmds as cmds
import webbrowser
import json
import os
from collections import OrderedDict
from . import tsubasa_global_reconnect_joint as grj



#�@UI      
def init_ui(*args):
    
    if cmds.window('reconnect_joint_window', ex=True):
        cmds.deleteUI('reconnect_joint_window')
    win = cmds.window('reconnect_joint_window', title="Reconnect_Joint", menuBar=True, widthHeight=(300, 500))
    cmds.menu(l='Help')
    cmds.menuItem(l='Tool help', command= grj.show_toolHelp)
    
    
    cmds.columnLayout(adjustableColumn=True, columnOffset = ['both',10], w=300 , rs=1)
    
  
    cmds.text(l='')
    cmds.separator(st='in')
    
    
    cmds.text(l='')
    cmds.rowColumnLayout(adjustableColumn=2, numberOfColumns=4)
    cmds.text(l='File Path: ')
    cmds.textField('file_path', text= grj.JSON_PATH)
    cmds.text(l='')
    cmds.button(l=u'Set', command= grj.file_set, ann=u'�t�@�C���p�X��I�����܂��B')
    cmds.setParent( '..' )
    cmds.text(l='')
    
    
    cmds.text(l='')
    cmds.text(l=u'�E�v���C�}���W���C���g�ȊO�̃W���C���g�̐e�q�֌W������', al='left')
    cmds.text(l='')
    cmds.rowColumnLayout(adjustableColumn=2, numberOfColumns=3)
    cmds.button(l=u'�ꊇ(PL)', command= grj.id_check_pl ,ann=u'�v���C�A�u���L�����N�^�[�̃v���C�}���W���C���g�ȊO�̃W���C���g�̐e�q�֌W���ꊇ�������܂��B', bgc=[0.4,0.6,0.6], w=135)
    cmds.text(l='')
    cmds.button(l=u'�ꊇ(NPC)', command= grj.id_check_np ,ann=u'NPC�̃v���C�}���W���C���g�ȊO�̃W���C���g�̐e�q�֌W���ꊇ�������܂��B', bgc=[0.4,0.6,0.6], w=135)
    cmds.setParent( '..' )
    
    
    cmds.text(l='')
    cmds.text(l='')
    cmds.text(l=u'�E�I�������W���C���g�̐e�q�֌W������', al='left')
    
        
    cmds.text(l='')
    cmds.button(l=u'�I������', command= grj.disconnect_joint_other, ann=u'�I�������W���C���g�̐e�q�֌W���������܂��B', bgc=[0.4,0.6,0.6])
    cmds.text(l='')
    
    
    cmds.text(l='')
    cmds.separator(st='in')
    cmds.text(l='')
    cmds.text(l=u'�E���������W���C���g���Đڑ�', al='left')
    cmds.text(l='')
    cmds.button(l=u'�Đڑ�', command= grj.connect_joint ,ann=u'���������W���C���g���Đڑ����܂��B', bgc=[1,1,1])
    cmds.text(l='')
    
    
    cmds.text(l='')
    cmds.separator(st='in')
    cmds.text(l='')
    cmds.button(l=u'����', command=('cmds.deleteUI(\"' + win + '\", window=True)'),ann=u'�E�B���h�E����܂��B' , bgc=[0.37, 0.37, 0.37])
    cmds.showWindow(win)




def main():
    init_ui()

main()

