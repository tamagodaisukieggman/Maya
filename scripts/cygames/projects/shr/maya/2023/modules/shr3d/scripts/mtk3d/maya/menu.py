# -*- coding: utf-8 -*-
"""メニュー「 shenron3d 」を追加"""

import maya.cmds as cmds
import maya.mel as mel

# TODO: shenron 様にリネームする場合はリネーム対応が必用


class Mtk3dMenu(object):
    # メニュー名
    menu_name = 'shenron3d'

    @classmethod
    def _add_items(cls):
        """shenron3dメニュー"""

        # Common
        cmds.menuItem(l='Common', sm=True, to=True, p=cls.menu_name)

        # mutsu 環境に依存しているためメニューから削除（安藤）
        # cmds.menuItem(d=True, dl='File')
        # cmds.menuItem(
        #     l=u'Updata InHouse Tools : [ mtk3d ] [ mutsunokami ] ツールを更新',
        #     ann=u'Perforce の最新版を取得し、 [ mtk3d ] [ mutsunokami ] を更新',
        #     c='import mtk3d.maya.update_tools as update_tools;update_tools.main()',
        # )

        cmds.setParent('..', menu=True)

        # --------------------------------------------------------------------------------------------------------------

        # Character
        cmds.menuItem(l='Character', sm=True, to=True, p=cls.menu_name)
        '''
        cmds.menuItem(
             l='clothToolsUI',
             c='import mtk3d.maya.cfx.clothSetupTool.clothSetupUI as UI;UI.main()',
        )
        '''
        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        # --------------------------------------------------------------------------------------------------------------

        # Environment
        cmds.menuItem(l='Environment', sm=True, to=True, p=cls.menu_name)

        cmds.setParent('..', menu=True)

        # --------------------------------------------------------------------------------------------------------------

        # Rigging
        cmds.menuItem(l='Rigging', sm=True, to=True, p=cls.menu_name)
        cmds.menuItem(d=True, dl='Ply')

        cmds.menuItem(
            l='cyRigPicker',
            c='import mtk3d.maya.rig.cyRig.gui as gui;reload(gui);gui.main()',
        )

        cmds.menuItem(
            l='IKFK Match Tool',
            c='from mtk3d.maya.rig.ikfk.ikfkmatch import ui as ikfk_ui;reload(ikfk_ui);ui = ikfk_ui.UI();ui.show()',
        )

        cmds.menuItem(
            l='Refresh Tool',
            c='import mtk3d.maya.rig.refreshScene.refreshScene as refreshScene;reload(refreshScene);refreshAnim = refreshScene.UI();refreshAnim.show()',
        )

        cmds.menuItem(
            l='Local World Tool',
            c='import mtk3d.maya.rig.localtoworld as localtoworld;reload(localtoworld);ltw = localtoworld.UI();ltw.show()',
        )

        cmds.menuItem(
            l='Prop Space Dialog',
            c='from mtk3d.maya.rig.props import ui as props_ui;reload(props_ui);ui = props_ui.PropSpaceDialog();ui.show_dialog()',
        )

        cmds.menuItem(
            l='Prevent Overstretching a.k.a NOBIKIRI',
            c='import mtk3d.maya.rig.preventoverstretching.prevent_overstretching as nobikiri;nobikiri.create()',
        )

        cmds.menuItem(d=True, dl='Quadruped')

        cmds.menuItem(
            l='waitPoseMatch',
            c='import mtk3d.maya.rig.animUtilTools.waitPoseMatch  as UI; reload(UI);UI.main()',
        )

        cmds.menuItem(
            l='ikFkSpaceSwitch',
            c='import mtk3d.maya.rig.animUtilTools.ikToFk as UI; reload(UI);UI.main()',
        )

        cmds.menuItem(d=True, dl='Utilities')

        cmds.menuItem(
            l='Instant Ik UI',
            c='import mtk3d.maya.rig.instantikcontroller.instant_ik_controller as i_ik;reload(i_ik);i_ik.create()',
        )

        cmds.menuItem(
            l='cyPoseStoreUI',
            c='import mtk3d.maya.rig.cyPoseStore.ui as UI;UI.ui()',
        )

        cmds.menuItem(
            l='cyShakeMakeUI',
            c='import mtk3d.maya.rig.cyShakeMake.ui.makeShakeUI as UI;UI.main()',
        )

        cmds.menuItem(d=True, dl='Skin')

        cmds.menuItem(
            l='Rename SkinCluster',
            c='import mtk3d.maya.rig.renameskincluster.main as main; main.rename_skin_cluster()',
        )

        cmds.menuItem(
            l='Reset SkinCluster',
            c='import mtk3d.maya.rig.resetskincluster.main as main; main.reset_skin_cluster()',
        )

        cmds.menuItem(d=True, dl='Skelton')
        cmds.menuItem(
            l='Comet Joint Orient',
            c='maya.mel.eval("cometJointOrient;")',
        )

        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        # ---------------------------------------------------------------------------

        # Animation
        cmds.menuItem(l='Animation', sm=True, to=True, p=cls.menu_name)

        cmds.menuItem(
            l='AnimatorTools',
            c='import mtk3d.maya.anim.animatortools.animatortools as ant;ant.createUI()',
        )

        cmds.menuItem(
            l='Anim School Picker',
            c='import maya.cmds as cmds;import maya.mel as mel;cmds.loadPlugin("Z:/mtk/tools/maya/modules/animschool_picker/plug-ins/AnimSchoolPicker.mll",qt=True);mel.eval("AnimSchoolPicker();")',
        )

        cmds.menuItem(
            l='TimeEditorTools',
            c='import mtk3d.maya.anim.timeeditortools.timeeditortools as tet;tet.createUI()',
        )

        cmds.menuItem(
            l='intAttack',
            c='import mtk3d.maya.anim.intattack.intattack as intattack;intattack.execute()',
        )

        cmds.menuItem(
            l=u'KeyframeReduction : アニメーションのキーフレームリダクションツール',
            c='import keyframeReduction.ui;keyframeReduction.ui.show()',
        )

        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        # ---------------------------------------------------------------------------

        # CharacterFX
        cmds.menuItem(l='Character FX', sm=True, to=True, p=cls.menu_name)
        cmds.menuItem(
            l='cfxToolsUI',
            c='import mtk3d.maya.cfx.cfxTools.cfxToolsUI as UI;UI.main()',
            i='menuIconNCloth.png'
        )
        cmds.menuItem(d=True, dl='Cloth')
        cmds.menuItem(d=True, dl='Hair')
        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        # ---------------------------------------------------------------------------

        # FX
        cmds.menuItem(l='FX', sm=True, to=True, p=cls.menu_name)
        '''
        cmds.menuItem(
             l='clothToolsUI',
             c='import mtk3d.maya.cfx.clothSetupTool.clothSetupUI as UI;UI.main()',
        )
        '''
        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        # ---------------------------------------------------------------------------

    @classmethod
    def main(cls):
        """メニュー「 shenron3d 」を追加"""

        g_main_window = mel.eval('$temp=$gMainWindow')

        if cmds.menu(cls.menu_name, q=True, ex=True):
            cls.menu = cmds.menu(cls.menu_name, e=True, dai=True, to=True)
        else:
            cls.menu = cmds.menu(cls.menu_name, l=cls.menu_name, p=g_main_window, to=True)

        # メニュー追加
        cls._add_items()
