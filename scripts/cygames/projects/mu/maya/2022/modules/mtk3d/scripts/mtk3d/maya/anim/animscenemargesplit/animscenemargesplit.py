# -*- coding: utf-8 -*-
import maya.cmds as cmds
import cylSplitAnimation
import cylCombineAnimation
import os

rowLists = []

def executeMargeScene(_):
    file_list = cmds.fileDialog2(dialogStyle=2, fileMode=4)
    combine_file = cylCombineAnimation.export_combine_anim_files(file_list)

def executeCurrentScene(_):

    intValues = []

    for rowContent in rowLists:
        print(rowContent)
        rowsIntFieldValue = cmds.rowLayout(rowContent,q=True,childArray=True)[1]
        intFieldValue = cmds.intField("%s"%rowsIntFieldValue,q=True,v=True)
        intValues.append(intFieldValue)

    print(intValues)
    filename = cmds.file(q=True,sn=True)
    cylSplitAnimation.export_splited_anim_files(intValues,filename)

def main():

    window = cmds.window(title='Maya Scene Merger & Splitter')

    column = cmds.columnLayout()
    # add FrameList
    def add_row(_) :
        cmds.setParent(column)
        this_row = cmds.rowLayout(nc=6, cw6 = (72, 72, 72, 72, 48, 48) )
        rowLists.append(this_row)
        cmds.text(l=u'Frame Range')
        start = cmds.intField(width=220)
        # note: buttons always fire a useless
        # argument; the _ here just ignores
        # that in both of these callback functions
        def do_delete(_):
            if this_row in rowLists:
                rowLists.remove(this_row)
            cmds.deleteUI(this_row)

        cmds.button(l=u'delete',c=do_delete)

    cmds.setParent()
    cmds.columnLayout(adj=True, rowSpacing=5, width=340)
    cmds.frameLayout( label=u'シーン結合ツール', mw=5, mh=5, fn="boldLabelFont", bgc=(0.16, 0.62, 0.70))
    cmds.button( label=u'結合ツールを起動', h=30, bgc=(0.71, 0.95, 0.29), command=executeMargeScene)
    cmds.setParent('..')
    cmds.columnLayout(adj=True, rowSpacing=5, width=340)
    cmds.frameLayout( label=u'シーン分割ツール', mw=5, mh=5, fn="boldLabelFont", bgc=(0.16, 0.62, 0.70))
    cmds.button( label=u'現在のシーンで分割', h=30, bgc=(0.71, 0.95, 0.29), command=executeCurrentScene )
    cmds.button( label=u'分割フレームを追加', h=30, command=add_row )
    cmds.text( label=u'▼ 分割するタイミングのフレーム値を入力',h=15 )
    cmds.setParent('..')

    add_row(column)

    cmds.setParent('..')

    cmds.showWindow(window)
