# -*- coding: utf-8 -*-

import maya.cmds as cmds
import webbrowser

# チェック
def error_check(*args):

    # 選択しているノードのリストの取得
    sel_list = cmds.ls(sl=True)

    #error文
    if len(sel_list) < 2:
        cmds.confirmDialog(message=u'複数のジョイントを選択してください', icn='warning')
        return

    # 選択しているノードのリストの取得
    sel_list = cmds.ls(sl=True)

    copy_joint_list = cmds.ls( sel_list[0], sl=True, dag=True, type='joint')
    paste_joint_list = cmds.ls( sel_list[1], sl=True, dag=True, type='joint')

    if len(copy_joint_list) == len(paste_joint_list):
        jointlabel_copy(sel_list, copy_joint_list, paste_joint_list)

    else:
        cmds.confirmDialog(message=u'ジョイントの数が異なります', icn='warning')
        return


# 既存のジョイントラベルを取得
def jointlabel_name_check(*args):

    sel_list = cmds.ls(sl=True)
    joint_label = cmds.getAttr(sel_list[0] + '.otherType')
    joint_side = cmds.getAttr(sel_list[0] + '.side')

    if joint_label:
        cmds.textField('jointlabel_name', e=True, tx=joint_label)

    if joint_side == 0:
        cmds.optionMenuGrp('jointlabel_side', e=True, v='Center')
    elif joint_side == 1:
        cmds.optionMenuGrp('jointlabel_side', e=True, v='Left')
    elif joint_side == 2:
        cmds.optionMenuGrp('jointlabel_side', e=True, v='Right')


# Segment Scale Compensate OFF
def ssc_off(*args):

    # 選択しているノードのリストの取得
    sel_list = cmds.ls(sl=True)
    joint_list = cmds.ls(sel_list[0], sl=True, dag=True, type='joint')

    for j in joint_list:
        cmds.setAttr(j + '.segmentScaleCompensate', 0)


# ジョイントラベルを設定
def jointlabel_set(*args):

    # 入力値の取得
    joint_side = cmds.optionMenuGrp('jointlabel_side', q=True, v=True)
    joint_type = cmds.optionMenuGrp('jointlabel_type', q=True, v=True)
    joint_othertype = cmds.textField('jointlabel_name', q=True, tx=True)

    sel_list = cmds.ls(sl=True)
    joint_list = cmds.ls(sel_list[0], sl=True, dag=True, type='joint')

    # ジョイントラベルの変更
    for i in range (len(joint_list)):
        cmds.setAttr(joint_list[i] + '.otherType', str(joint_othertype) + str(i + 1), type='string')

        # Side
        if joint_side == 'Center':
            cmds.setAttr(joint_list[i] + '.side', 0)
        elif joint_side == 'Left':
            cmds.setAttr(joint_list[i] + '.side', 1)
        elif joint_side == 'Right':
            cmds.setAttr(joint_list[i] + '.side', 2)

        # Type
        cmds.setAttr(joint_list[i] + '.type', 18)


# ジョイントラベルをミラーコピー
def jointlabel_copy(sel_list, copy_joint_list, paste_joint_list):

    # ジョイントラベルの取得
    # ジョイントラベルの変更
    for i in range (len(copy_joint_list)):
        joint_label = cmds.getAttr( copy_joint_list[i] + '.otherType')
        cmds.setAttr(paste_joint_list[i] + '.otherType', joint_label, type='string')

        # nodeのグローバル座標を取得
        # sideの変更
        joint_gcoord = cmds.xform(copy_joint_list[i], q=True, t=True, ws=True)
        if joint_gcoord[0] <= 0:
            cmds.setAttr(paste_joint_list[i] + '.side', 1)
            cmds.setAttr(copy_joint_list[i] + '.side', 2)

        else:
            cmds.setAttr(paste_joint_list[i] + '.side', 2)
            cmds.setAttr(copy_joint_list[i] + '.side', 1)

        # Typeの変更
        cmds.setAttr(paste_joint_list[i] + '.type', 18)

# UI
def init_ui():

    if cmds.window('copy_jointlael_window', ex=True):
        cmds.deleteUI('copy_jointlael_window')
    win = cmds.window('copy_jointlael_window', title="Copy JointLabel", menuBar=True, widthHeight=(300, 500))
    cmds.menu(l='Help')
    cmds.menuItem(l='Tool help', command=show_toolHelp)

    cmds.columnLayout(adjustableColumn=True, columnOffset = ['both',10], w=300 , rs=1)

    cmds.text(l='')
    cmds.separator(st='in')
    cmds.text(l='')
    cmds.text(l=u'・Segment Scale Compensate OFF', al='left')
    cmds.text(l='')
    cmds.button(l=u'実行', command= ssc_off ,ann=u'選択しているジョイント階層のSegment Scale Compensateをオフにします。', bgc=[0.5,0.5,1])

    cmds.text(l='')
    cmds.separator(st='in')
    cmds.text(l='')
    cmds.text(l=u'・ジョイントラベルを設定', al='left')
    cmds.optionMenuGrp('jointlabel_side',l='Side   ')
    cmds.menuItem(l='Center')
    cmds.menuItem(l='Left')
    cmds.menuItem(l='Right')
    cmds.optionMenuGrp('jointlabel_type',l='Type   ')
    cmds.menuItem(l='Other  ')
    cmds.rowColumnLayout(adjustableColumn=2, numberOfColumns=3)
    cmds.text(l='Other Type   ')
    cmds.textField('jointlabel_name')
    cmds.button(l=u'＜＜Set', command= jointlabel_name_check ,ann=u'選択しているジョイントラベルをセットします。')
    cmds.setParent( '..' )
    cmds.text(l='')
    cmds.button(l=u'実行', command= jointlabel_set ,ann=u'ジョイントラベルを設定します。', bgc=[0.5,0.5,1])

    cmds.text(l='')
    cmds.separator(st='in')
    cmds.text(l='')
    cmds.text(l=u'・ジョイントラベルをミラーコピー', al='left')
    cmds.text(l=u'　※複数のジョイントを選択し、実行してください', al='left')
    cmds.text(l='')
    cmds.button(l=u'実行', command= error_check ,ann=u'ジョイントラベルをコピーします。', bgc=[0.5,0.5,1])

    cmds.text(l='')
    cmds.separator(st='in')
    cmds.text(l='')
    cmds.button(l=u'閉じる', command=('cmds.deleteUI(\"' + win + '\", window=True)'),ann=u'ウィンドウを閉じます。' , bgc=[1,1,1])
    cmds.showWindow(win)


# Help
def show_toolHelp(*args):
    toolHelp_url = r'https://wisdom.cygames.jp/x/k2tyFw'
    webbrowser.open_new_tab(toolHelp_url)


def main():
    init_ui()

main()
