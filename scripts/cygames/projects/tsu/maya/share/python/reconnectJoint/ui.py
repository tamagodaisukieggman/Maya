# -*- coding: shift-jis -*-
import maya.cmds as cmds
import webbrowser
import json
import os
from collections import OrderedDict
from . import tsubasa_global_reconnect_joint as grj



#　UI      
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
    cmds.button(l=u'Set', command= grj.file_set, ann=u'ファイルパスを選択します。')
    cmds.setParent( '..' )
    cmds.text(l='')
    
    
    cmds.text(l='')
    cmds.text(l=u'・プライマリジョイント以外のジョイントの親子関係を解除', al='left')
    cmds.text(l='')
    cmds.rowColumnLayout(adjustableColumn=2, numberOfColumns=3)
    cmds.button(l=u'一括(PL)', command= grj.id_check_pl ,ann=u'プレイアブルキャラクターのプライマリジョイント以外のジョイントの親子関係を一括解除します。', bgc=[0.4,0.6,0.6], w=135)
    cmds.text(l='')
    cmds.button(l=u'一括(NPC)', command= grj.id_check_np ,ann=u'NPCのプライマリジョイント以外のジョイントの親子関係を一括解除します。', bgc=[0.4,0.6,0.6], w=135)
    cmds.setParent( '..' )
    
    
    cmds.text(l='')
    cmds.text(l='')
    cmds.text(l=u'・選択したジョイントの親子関係を解除', al='left')
    
        
    cmds.text(l='')
    cmds.button(l=u'選択解除', command= grj.disconnect_joint_other, ann=u'選択したジョイントの親子関係を解除します。', bgc=[0.4,0.6,0.6])
    cmds.text(l='')
    
    
    cmds.text(l='')
    cmds.separator(st='in')
    cmds.text(l='')
    cmds.text(l=u'・解除したジョイントを再接続', al='left')
    cmds.text(l='')
    cmds.button(l=u'再接続', command= grj.connect_joint ,ann=u'解除したジョイントを再接続します。', bgc=[1,1,1])
    cmds.text(l='')
    
    
    cmds.text(l='')
    cmds.separator(st='in')
    cmds.text(l='')
    cmds.button(l=u'閉じる', command=('cmds.deleteUI(\"' + win + '\", window=True)'),ann=u'ウィンドウを閉じます。' , bgc=[0.37, 0.37, 0.37])
    cmds.showWindow(win)




def main():
    init_ui()

main()

