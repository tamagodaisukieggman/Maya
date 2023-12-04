# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
import sys
import traceback
import importlib
from imp import reload

import maya.cmds as cmds
import maya.mel as mel

try:
    import pymel.core as pm
except Exception as e:
    print(e)

plugins = ['atomImportExport', 'MayaMuscle', 'MASH', 'matrixNodes', 'fbxmaya']
for pl in plugins:
    try:
        if cmds.pluginInfo(pl, q=True, l=True) == False:
            cmds.loadPlugin(pl)
    except Exception as e:
        print(e)

maya_version = cmds.about(v=1)
if 2022 <= float(maya_version):
    imp_line = 'import importlib;importlib.reload'
else:
    imp_line = 'reload'

class CreateMenu(object):
    u"""
    import tkgTools_menu
    reload(tkgTools_menu)
    tm=tkgTools_menu.TkgTools()
    tm.main()
    """
    # メニュー名
    menu_name = 'TkgTools'
    menu_label = 'TkgTools'

    file_menu='file'
    gui_menu='gui'
    model_menu='model'
    rig_menu='rig'
    anim_menu='anim'

    dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
    dir_path = dir.replace('\\', '/')
    print('{} path:{}'.format(menu_name, dir_path))


    @classmethod
    def _add_items(cls):
        # file
        cmds.menuItem(
            cls.file_menu,
            l=u'{0}'.format(cls.file_menu),
            sm=True,
            to=True,
            p=cls.menu_name
        )

        cmds.menuItem(
            l=u'Default Snap',
            c='import tkgfile.utils as tkgfileuls;reload(tkgfileuls);tkgfileuls.default_snap()',
            ann=u'デフォルトのカメラ設定でスクショを撮ります（デスクトップに保存）'
        )

        cmds.menuItem(
            l=u'Select reference before opening file',
            c='import tkgfile.window as tkgfilewin;reload(tkgfilewin);ttd=tkgfilewin.TkgDialogs();ttd.get_PreloadReferenceEditor()',
            ann=u'ファイルを開く前に読み込むリファレンスを選択してから開く'
        )

        cmds.menuItem(
            l=u'Reopen current file',
            c='import tkgfile.utils as tkgfileuls;reload(tkgfileuls);tut=tkgfileuls.TkgUtils();tut.re_file_open()',
        )


        cmds.menuItem(
            l=u'Check all references',
            c='import tkgfile.utils as tkgfileuls;reload(tkgfileuls);tut=tkgfileuls.TkgUtils();tut.allreferences_uncheck_remove("check")',
        )

        cmds.menuItem(
            l=u'Uncheck all references',
            c='import tkgfile.utils as tkgfileuls;reload(tkgfileuls);tut=tkgfileuls.TkgUtils();tut.allreferences_uncheck_remove("uncheck")',
        )

        cmds.menuItem(
            l=u'Remove all references',
            c='import tkgfile.utils as tkgfileuls;reload(tkgfileuls);tut=tkgfileuls.TkgUtils();tut.allreferences_uncheck_remove("remove")',
        )

        cmds.menuItem(
            l=u'Delete all "setAttr" in reference edit',
            c='import tkgfile.utils as tkgfileuls;reload(tkgfileuls);tut=tkgfileuls.TkgUtils();tut.allreferences_uncheck_remove("removeEdits", "setAttr")',
            ann=u'リファレンスの編集(setAttr)をすべて削除'
        )

        cmds.menuItem(
            l=u'Import All References',
            c='import tkgfile.utils as tkgfileuls;reload(tkgfileuls);tut=tkgfileuls.TkgUtils();tut.importAllReferences()',
        )

        cmds.menuItem(
            l=u'Delete All Namespaces',
            c='import tkgfile.utils as tkgfileuls;reload(tkgfileuls);tut=tkgfileuls.TkgUtils();tut.remove_all_namespace()',
        )

        cmds.menuItem(
            l=u'Delete CgAbBlastPanelOptChangeCallback',
            c='import tkgfile.utils as tkgfileuls;reload(tkgfileuls);tut=tkgfileuls.TkgUtils();tut.remove_CgAbBlastPanelOptChangeCallback()',
        )
        cmds.menuItem(
            l=u'MultiFileBrowser',
            c='import tkgfile.multiFileBrowser.filedirectorytree as filedirectorytree;reload(filedirectorytree);fst = filedirectorytree.FileDirectoryTree();fst.buildUI();fst.show(dockable=True)',
        )
        cmds.menuItem(
            l=u'StatusChecker:tsubasa',
            c='import tkgfile.checkStatus.statusChecker as statusChecker;reload(statusChecker);sc = statusChecker.StatusChecker();sc.project="tsubasa";sc.buildUI();sc.show(dockable=True);sc.whatsNew()',
        )
        cmds.menuItem(
            l=u'StatusChecker:world',
            c='import tkgfile.checkStatus.statusChecker as statusChecker;reload(statusChecker);sc = statusChecker.StatusChecker();sc.project="world";sc.buildUI();sc.show(dockable=True)',
        )
        cmds.menuItem(
            l=u'avatarReferenceTool:wizard2',
            c='import tkgfile.avatarReferenceTool.ui as avatarReferenceToolUI;\
            reload(avatarReferenceToolUI);\
            fbx_mxui = avatarReferenceToolUI.AvatarReferenceTool();\
            fbx_mxui.buildUI();\
            fbx_mxui.show(dockable=True)',
        )


        cmds.setParent('..', menu=True)

        # gui
        cmds.menuItem(
            cls.gui_menu,
            l=u'{0}'.format(cls.gui_menu),
            sm=True,
            to=True,
            p=cls.menu_name
        )

        cmds.menuItem(
            l=u'Widy ShelfLayout',
            c='mel.eval("layout -e -height 97 ShelfLayout;")'
        )

        cmds.menuItem(
            l=u'When saving panel with file:ON',
            c='mel.eval("$gUseSaveScenePanelConfig = true;file -uc true;savePrefsChanges;")'
        )

        cmds.menuItem(
            l=u'When saving panel with file:OFF',
            c='mel.eval("$gUseSaveScenePanelConfig = false;file -uc false;savePrefsChanges;")'
        )

        cmds.menuItem(
            l=u'When opening panel from file:ON',
            c='mel.eval("$gUseScenePanelConfig = true;file -uc true;savePrefsChanges;")'
        )

        cmds.menuItem(
            l=u'When opening panel from file:OFF',
            c='mel.eval("$gUseScenePanelConfig = false;file -uc false;savePrefsChanges;")'
        )

        cmds.menuItem(
            l=u'Set 5 precisions in channelBox',
            c='gChannelBoxName = mel.eval("$temp=$gChannelBoxName");cmds.channelBox(gChannelBoxName, e=1, pre=5)'
        )

        cmds.menuItem(
            l=u'Set 8 precisions in channelBox',
            c='gChannelBoxName = mel.eval("$temp=$gChannelBoxName");cmds.channelBox(gChannelBoxName, e=1, pre=8)'
        )

        cmds.setParent('..', menu=True)


        # model
        cmds.menuItem(
            cls.model_menu,
            l=u'{0}'.format(cls.model_menu),
            sm=True,
            to=True,
            p=cls.menu_name
        )

        cmds.menuItem(
            l=u'Get UV param from vertices',
            c='import tkgmodel.info as tkgmodelif;reload(tkgmodelif);tmg = tkgmodelif.Getdaze();tmg.get_uv_param_from_mesh()',
            ann=u'頂点からUVのパラメータを取得'
        )

        cmds.setParent('..', menu=True)

        # rig
        cmds.menuItem(
            cls.rig_menu,
            l=u'{0}'.format(cls.rig_menu),
            sm=True,
            to=True,
            p=cls.menu_name
        )

        cmds.menuItem(
            l=u'select',
            sm=True,
            to=True
        )

        cmds.menuItem(
            l=u'Select only joints in hierarchy',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.select_hierarchy_form_type(type="joint")',
            ann=u'階層内のジョイントのみ選択する'
        )

        cmds.menuItem(
            l=u'Select only constraints in hierarchy',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.select_hierarchy_form_type(type="constraint")',
            ann=u'階層内のコンストレイントのみ選択する'
        )

        cmds.menuItem(
            l=u'Select only mesh in hierarchy',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.select_hierarchy_form_type(type="mesh")',
            ann=u'階層内のメッシュのみ選択する'
        )

        cmds.menuItem(
            l=u'Get Sets Hierarchy',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();local_get_sets_ = tut.get_sets_objects()',
            ann=u'シーン内のsetsを取得する'
        )

        cmds.menuItem(
            l=u'Set Sets Hierarchy',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.set_saved_sets(local_get_sets_)',
            ann=u'取得したsetsを設定する'
        )

        cmds.setParent('..', menu=True)


        cmds.menuItem(
            l=u'attribute',
            sm=True,
            to=True
        )

        cmds.menuItem(
            l=u'Lock Attrs from channelBox',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.lock_keyable_attributes(lock=True, keyable=True, channelBox=False, showTransform=False)',
            ann=u'選択しているアトリビュートのロック'
        )

        cmds.menuItem(
            l=u'Unlock Attrs from channelBox',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.lock_keyable_attributes(lock=False, keyable=True, channelBox=False, showTransform=False)',
            ann=u'選択しているアトリビュートのアンロック'
        )

        cmds.menuItem(
            l=u'Hide Attrs from channelBox',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.lock_keyable_attributes(lock=False, keyable=False, channelBox=False, showTransform=False)',
            ann=u'選択しているアトリビュートの非表示'
        )

        cmds.menuItem(
            l=u'Show Attrs from channelBox',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.lock_keyable_attributes(lock=False, keyable=True, channelBox=False, showTransform=False)',
            ann=u'選択しているアトリビュートの表示'
        )

        cmds.menuItem(
            l=u'Lock & Hide Attrs from chennelbox',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.lock_keyable_attributes(lock=True, keyable=False, channelBox=False, showTransform=False)',
            ann=u'選択しているアトリビュートのロック・非表示'
        )

        cmds.menuItem(
            l=u'Enable Inherent Attrs',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.lock_keyable_attributes(lock=False, keyable=False, channelBox=False, showTransform=True)',
            ann=u'選択しているノードの基本アトリビュートを有効にする'
        )

        cmds.menuItem(
            l=u'Get distance from 2 objects',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.get_length()',
            ann=u'選択しているオブジェクトの距離を取得する'
        )

        cmds.menuItem(
            l=u'Round Attrs',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.round_transform_attrs()',
            ann=u'選択しているオブジェクトの基本アトリビュートの値を0.001の桁で四捨五入する'
        )

        cmds.menuItem(
            l=u'Copy Objects Values[Select objects]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.get_object_values()',
            ann=u'値をクリップボードにコピーする'
        )

        cmds.menuItem(
            l=u'Paste Objects Values[]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.set_object_values()',
            ann=u'値をクリップボードにコピーした情報をペーストする'
        )

        cmds.setParent('..', menu=True)

        cmds.menuItem(
            l=u'joint',
            sm=True,
            to=True
        )

        cmds.menuItem(
            l=u'cometJointOrient',
            c='mel.eval("cometJointOrient")',
        )

        cmds.menuItem(
            l=u'Check IK Joints(aim:x, bend:y)[Select joints]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.check_ik_joint_axis(aim_axis="x", bend_axis="y")',
            ann=u'IK用のジョイントを確認する(aim:x, bend:y)'
        )

        cmds.menuItem(
            l=u'Check IK Joints(aim:x, bend:z)[Select joints]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.check_ik_joint_axis(aim_axis="x", bend_axis="z")',
            ann=u'IK用のジョイントを確認する(aim:x, bend:z)'
        )

        cmds.menuItem(
            l=u'Check IK Joints(aim:y, bend:x)[Select joints]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.check_ik_joint_axis(aim_axis="y", bend_axis="x")',
            ann=u'IK用のジョイントを確認する(aim:y, bend:x)'
        )

        cmds.menuItem(
            l=u'Check IK Joints(aim:y, bend:z)[Select joints]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.check_ik_joint_axis(aim_axis="y", bend_axis="z")',
            ann=u'IK用のジョイントを確認する(aim:y, bend:z)'
        )

        cmds.menuItem(
            l=u'Check IK Joints(aim:z, bend:x)[Select joints]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.check_ik_joint_axis(aim_axis="z", bend_axis="x")',
            ann=u'IK用のジョイントを確認する(aim:z, bend:x)'
        )

        cmds.menuItem(
            l=u'Check IK Joints(aim:z, bend:y)[Select joints]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.check_ik_joint_axis(aim_axis="z", bend_axis="y")',
            ann=u'IK用のジョイントを確認する(aim:z, bend:y)'
        )

        cmds.menuItem(
            l=u'Merge Joints Rotation from Joint Orient[Select joints]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.reconcile_joint_rotate_orient()',
            ann=u'見た目を保持したままジョイントオリエントを回転値に転送する(回転値は0の状態で行う)'
        )

        cmds.menuItem(
            l=u'Aim + Up +',
            sm=True,
            to=True
        )

        ## + +
        # X X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # X Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # X Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        cmds.setParent('..', menu=True)

        cmds.menuItem(
            l=u'Aim + Up -',
            sm=True,
            to=True
        )

        ## + -
        # X X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:-X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:-X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # X Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:-Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:-Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # X Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:-Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:X, Up:-Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="x", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:-Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:-Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:-X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:-X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:-Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Y, Up:-Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="y", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:-Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:-Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:-X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:-X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:-Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:Z, Up:-Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="z", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        cmds.setParent('..', menu=True)

        cmds.menuItem(
            l=u'Aim - Up +',
            sm=True,
            to=True
        )

        ## - +
        # X X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # X Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # X Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        cmds.setParent('..', menu=True)

        cmds.menuItem(
            l=u'Aim - Up -',
            sm=True,
            to=True
        )

        ## - -
        # X X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:-X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:-X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # X Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:-Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:-Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # X Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:-Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-X, Up:-Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-x", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:-Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:-Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:-X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:-X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Y Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:-Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Y, Up:-Z, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-y", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z Z
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:-Z, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:-X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="-z", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z X
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:-X, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:-X, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="-x", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        # Z Y
        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:-Y, worldSpace:False)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=False)'
        )

        cmds.menuItem(
            l=u'Aim & Correct Joints(Aim:-Z, Up:-Y, worldSpace:True)[Select Each Root Joint]',
            c='import tkgRigBuild.libs.modifyJoints as tkgMJ;reload(tkgMJ); \
            tkgMJ.aim_correct_joints(sel=None, aim_axis="-z", up_axis="-y", worldUpType="object", ssc_sts=False, worldSpace=True)'
        )

        cmds.setParent('..', menu=True) # submenu

        cmds.setParent('..', menu=True)

        cmds.menuItem(
            l=u'skinning',
            sm=True,
            to=True
        )

        cmds.menuItem(
            l=u'SkinEditor',
            c='import SkinEditor.ui as SkinEditorUI;reload(SkinEditorUI);sse = SkinEditorUI.EditSkinUI();sse.show()'
        )

        cmds.menuItem(
            l=u'WeightManager',
            c='import tkgrig.weightmanager as weightmanager;reload(weightmanager);wmer=weightmanager.WeightManager();wmer.buildUI();wmer.show(dockable=True)'
        )

        cmds.menuItem(
            l=u'WeightSmoother',
            c='import tkgrig.weightsmoother as weightsmoother;reload(weightsmoother);wser=weightsmoother.UI();wser.show()'
        )

        cmds.menuItem(
            l=u'Save DAG Pose',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.set_dag_pose()',
            ann=u'dagPoseを設定する'
        )

        cmds.menuItem(
            l=u'Delete DAG Pose',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.delete_dag()',
            ann=u'dagPoseをすべて削除する'
        )

        cmds.menuItem(
            l=u'Correct skinCluster names[Select objects]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.correct_skinCluster_names()',
            ann=u'skinClusterノードの名前をオブジェクトに合わせる'
        )

        cmds.menuItem(
            l=u'Select influences from skinmesh[Select skinmesh]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.transfer_skinCluster(select_joints="source")',
            ann=u'選択したオブジェクトのinfluenceを選択する'
        )

        cmds.menuItem(
            l=u'Select influences from skinmesh without namespace[Select skinmesh]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.transfer_skinCluster(select_joints="replaced")',
            ann=u'選択したオブジェクトのネームスペースを除いたinfluenceを選択する'
        )

        cmds.menuItem(
            l=u'Bind the same influences to object[Select base skin binded object > select target object]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.transfer_skinCluster()',
            ann=u'1つ目に選択したメッシュのネームスペースを除いたinfluenceから2番目に選択したメッシュにバインドする'
        )

        cmds.menuItem(
            l=u'Bind the same influences to object(copy)[Select base skin binded object > select target object]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.transfer_skinCluster(weight_copy=True)',
            ann=u'1つ目に選択したメッシュのネームスペースを除いたinfluenceから2番目に選択したメッシュにバインドし、コピーまでする'
        )

        cmds.menuItem(
            l=u'Bind the same influences to objects(copy)[Select base skin binded objects]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.iter_transfer_skinCluster()',
            ann=u'選択したメッシュすべてのネームスペースを除いたinfluenceからネームスペースを除いたメッシュにすべてにバインドし、コピーまでする'
        )

        cmds.menuItem(
            l=u'Add Labels to PaintSkinWeightTool',
            c='exec(open(str("{0}"), encoding="utf-8").read()) if 2022 <= float(maya_version) else execfile(r"{0}")'.format(cls.dir_path+'/python/tkgrig/showJointLabelsInPSWT.py')
        )


        cmds.setParent('..', menu=True)

        cmds.menuItem(
            l=u'setup',
            sm=True,
            to=True
        )

        cmds.menuItem(
            l=u'ObjectsRenamer',
            c='import tkgrig.renamer as renamer;reload(renamer);ror = renamer.ObjectsRenamer();ror.buildUI();ror.show(dockable=True)',
        )

        cmds.menuItem(
            l=u'ConnectAttr from channelBox[Select object > select attrs in channelBox]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.connect_the_sameAttr_from_channelBox()',
            ann=u'2つのオブジェクトをchannelBox上で選択したアトリビュートどうし接続する'
        )

        cmds.menuItem(
            l=u'ConnectAttr(Offset) from channelBox[Select object > select attrs in channelBox]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.connect_offset_attr_from_channelBox()',
            ann=u'2つのオブジェクトをchannelBox上で選択したアトリビュートを相殺して接続する'
        )

        cmds.menuItem(
            l=u'Matrix Constraint[Select 2 objects]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.constraint_from_local_matrix()',
            ann=u'選択した2つのオブジェクトをmatrixでコンストレイントする'
        )

        cmds.menuItem(
            l=u'Match Objects[Select objects]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.tkg_matchTransform()',
            ann=u'最後に選択したオブジェクトにマッチさせる'
        )

        cmds.menuItem(
            l=u'Create PoleVector Locator[Select start, middle and end joints]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.get_poleVector_position()',
            ann=u'PoleVectorの位置にロケータを作成する'
        )


        cmds.menuItem(
            l=u'Create Null[Select object]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_null()',
            ann=u'選択したオブジェクトのヌルを作成する'
        )

        cmds.menuItem(
            l=u'Create Offset Node[Select object]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_offset()',
            ann=u'選択したオブジェクトのオフセットノードを作成する'
        )

        cmds.menuItem(
            l=u'Create Joint in Selected Item[Select object]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_joints_into_under_objects()',
            ann=u'選択したオブジェクトの子にジョイントを作成する'
        )

        cmds.menuItem(
            l=u'Create Follicle from closest objects[Select objects > Select Mesh or Surface]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_follicles()',
            ann=u'選択したオブジェクトの最近傍点にfollicleノードを作成する'
        )

        cmds.menuItem(
            l=u'Closest Vertices[Select 2 objects > return 2 vertices]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_closest_points_sets()',
            ann=u'二つ目に選択したオブジェクトの最近傍頂点のsetsを作成する'
        )

        cmds.menuItem(
            l=u'CreateCurve from objects[Select objects]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_curve_from_selection()',
            ann=u'選択したオブジェクトまたは頂点などを通るNurbsカーブを作成する'
        )

        cmds.menuItem(
            l=u'Create guide curve from objects[Select 2 objects]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_poleVector_guide()',
            ann=u'選択した2つのオブジェクトにガイドのカーブを作成する'
        )

        cmds.menuItem(
            l=u'Create Surface from 2 curves[Select 2 curves]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_loft_surface()',
            ann=u'選択した2つのNurbsカーブでloftしてSurfaceを作成する'
        )

        cmds.menuItem(
            l=u'Create Locators from Curve (on object)[(SelectObject > )SelectCurve]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_crv_attach_locs()',
            ann=u'選択したカーブにロケータを作成する'
        )

        cmds.menuItem(
            l=u'Create keepout node for collision rig[Select 2 objects]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_collision_with_keepout()',
            ann=u'コリジョンリグ用のkeepoutノードを作成する(1つ目のobjectが影響範囲を決め、2つ目のobjectがコントローラになる)'
        )

        cmds.menuItem(
            l=u'Create Collision Rig[SelectObject]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_collision_rig()',
            ann=u'コリジョンリグを作成する'
        )

        cmds.menuItem(
            l=u'Create nHair with IKSpline[Select Joints > Select Curve]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_dynamicJointswithIk()',
            ann=u'ジョイントにIKSpline付きのnHairを構築する(ジョイントを選択 > カーブを選択 > 実行)'
        )

        cmds.menuItem(
            l=u'CreatePassiveColider[SelectObject > SelectNucleus]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_rigidBody()',
            ann=u'パッシブコライダを作成する'
        )

        cmds.menuItem(
            l=u'CreateEmitter[SelectVertices]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.create_emitters_from_selection()',
            ann=u'選択した頂点にエミッターを作成する'
        )

        cmds.menuItem(
            l=u'Copy Curve Settings to Clipboard[Select Curve Objects]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.copy_curve_settings_to_clipboard()',
            ann=u'選択したカーブの設定をクリップボードにコピーします'
        )

        cmds.menuItem(
            l=u'Merge Curves[Select Curve Objects]',
            c='import tkgrig.utils as tkgriguls;reload(tkgriguls);tut=tkgriguls.TkgUtils();tut.merge_curves()',
            ann=u'選択したカーブのShapeをマージします(マージ元がずれる場合はフリーズさせる必要があります)'
        )

        cmds.menuItem(
            l=u'codeControllers',
            c='import tkgrig.codeControllers as codeControllers;reload(codeControllers);controllerLibrary=codeControllers.ControllerLibrary();controllerLibrary.show()'
        )

        cmds.menuItem(
            l=u'rig101wireControllers',
            c='import rig101wireControllers as rig101WC;reload(rig101WC);ui = rig101WC.rig101();ui.rig101WireControllers()'
        )

        cmds.menuItem(
            l=u'mz_ctrlCreator',
            c='import mz_ctrl.mz_ctrlCreator as mz_ctrlCreator;reload(mz_ctrlCreator)'
        )

        cmds.menuItem(
            l=u'Ctrl_O',
            c='import Ctrl_O.ctrlo as ctrlo;reload(ctrlo);ctrlo.Display_CtrlO_UI()'
        )

        cmds.menuItem(
            l=u'Matrix Collision Rig',
            c='import matrix_collision_rig as mcr;reload(mcr);mcr.show()'
        )

        cmds.setParent('..', menu=True)

        cmds.menuItem(
            l=u'tkgRigSetUpBat',
            c="""mel.eval('system("start C:/Users/{0}/Documents/maya/scripts/tkgTools/tkgRig/scripts/build/rigbuild.bat");')""".format(os.getenv('USER'))
        )

        cmds.setParent('..', menu=True)


        # anim
        cmds.menuItem(
            cls.anim_menu,
            l=u'{0}'.format(cls.anim_menu),
            sm=True,
            to=True,
            p=cls.menu_name
        )

        cmds.menuItem(
            l=u'ExportFBX[Select root joint]',
            c='import tkganim.utils as tkganimuls;reload(tkganimuls);tut=tkganimuls.TkgUtils();tut.export_fbx()',
            ann=u'Jointのfbx書き出し'
        )

        cmds.menuItem(
            l=u'ClampAnimRange(-180, 180)[Select Objects]',
            c='import tkganim.utils as tkganimuls;reload(tkganimuls);tut=tkganimuls.TkgUtils();tut.bake(playbackSlider=True, correctAnimKeys=True)',
            ann=u'Keyframeを-180から180まででクランプする'
        )

        cmds.menuItem(
            l=u'AnimCopy[Select Objects]',
            c='import tkganim.utils as tkganimuls;reload(tkganimuls);tut=tkganimuls.TkgUtils();tut.copy_anim()',
            ann=u'選択しているobjectのkeyをNamespaceの無いobjectにコピーする'
        )

        cmds.setParent('..', menu=True)

        cmds.menuItem(d=True)

        # Reload menu
        cmds.menuItem(
            l=u'ReloadMenu',
            c='import tkgTools_menu;reload(tkgTools_menu);tm=tkgTools_menu.TkgTools();tm.main();'
        )

        cmds.menuItem(
            l=u'CommandReference',
            c="import webbrowser;webbrowser.open('https://help.autodesk.com/view/MAYAUL/'+cmds.about(v=1)+'/JPN/?guid=__CommandsPython_index_html')"
        )

        cmds.menuItem(
            l=u'APIReference',
            c="import webbrowser;webbrowser.open('https://help.autodesk.com/view/MAYAUL/'+cmds.about(v=1)+'/ENU/?guid=__py_ref_classes_html')"
        )

        cmds.menuItem(
            l=u'Replace Clipboard Path',
            c='import tkgfile.utils as tkgfileuls;reload(tkgfileuls);tkgfileuls.replace_clipboard_path()',
            ann=u'クリップボードのパスをバックスラッシュからスラッシュに変換します'
        )

    @classmethod
    def main(cls):
        g_main_window = mel.eval('$temp=$gMainWindow')

        if cmds.menu(cls.menu_name, q=True, ex=True):
            cls.menu = cmds.menu(cls.menu_name, e=True, dai=True, to=True)
        else:
            cls.menu = cmds.menu(cls.menu_name, l=cls.menu_name, p=g_main_window, to=True)

        # 基本メニュー
        cls._add_items()

        cmds.setParent('..', menu=True)

if __name__ == '__main__':
    try:
        TkgTools.main()
    except:
        print(traceback.format_exc())
