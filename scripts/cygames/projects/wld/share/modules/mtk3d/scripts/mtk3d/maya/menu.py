# -*- coding: utf-8 -*-
"""メニュー「 mtk3d 」を追加"""

import maya.cmds as cmds
import maya.mel as mel


class Mtk3dMenu(object):
    # メニュー名
    menu_name = 'mtk3d'

    @classmethod
    def _add_items(cls):
        """mtk3dメニュー"""

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

        #---------------------------------------------------------------------------

        # Environment
        cmds.menuItem(l='Environment', sm=True, to=True, p=cls.menu_name)
        '''
        cmds.menuItem(
             l='clothToolsUI',
             c='import mtk3d.maya.cfx.clothSetupTool.clothSetupUI as UI;UI.main()',
        )
        '''
        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        #---------------------------------------------------------------------------

        # Rigging
        cmds.menuItem(l='Rigging', sm=True, to=True, p=cls.menu_name)
        cmds.menuItem(d=True, dl='Ply')

        cmds.menuItem(
             l='charaCtrlSelecterUI',
             c='import mtk3d.maya.rig.cyCharaControllerSelecter.ui.charaCtrlSelecterUI as UI;UI.main()',
        )

        cmds.menuItem(d=True, dl='Dragon')

        cmds.menuItem(
            l='dragonCtrlSelecterUI',
            c='import mtk3d.maya.rig.cyControllerSelecter.ui.ui as UI;UI.main()',
        )

        cmds.menuItem(
            l='dragonToolUI',
            c='import mtk3d.maya.rig.cyDragonTool.ui.cyDragonToolUI as UI;UI.main()',
        )

        cmds.menuItem(d=True, dl='Utilities')

        cmds.menuItem(
            l='matchControllerUI',
            c='import mtk3d.maya.rig.cyMatchController.ui.ui as UI;UI.ui()',
        )

        cmds.menuItem(
            l='cyPoseStoreUI',
            c='import mtk3d.maya.rig.cyPoseStore.ui as UI;UI.ui()',
        )

        cmds.menuItem(
            l='cyShakeMakeUI',
            c='import mtk3d.maya.rig.cyShakeMake.ui.makeShakeUI as UI;UI.main()',
        )


        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        #---------------------------------------------------------------------------

        # Animation
        cmds.menuItem(l='Animation', sm=True, to=True, p=cls.menu_name)
        '''
        cmds.menuItem(
             l='clothToolsUI',
             c='import mtk3d.maya.cfx.clothSetupTool.clothSetupUI as UI;UI.main()',
        )
        '''
        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        #---------------------------------------------------------------------------

        # CharacterFX
        cmds.menuItem(l='Character FX', sm=True, to=True, p=cls.menu_name)
        cmds.menuItem(d=True, dl='Cloth')
        cmds.menuItem(
             l='clothToolsUI',
             c='import mtk3d.maya.cfx.clothSetupTool.clothSetupUI as UI;UI.main()',
        )
        cmds.menuItem(d=True, dl='Hair')
        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        #---------------------------------------------------------------------------

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

        #---------------------------------------------------------------------------

    @classmethod
    def main(cls):
        """メニュー「 mtk3d 」を追加"""

        g_main_window = mel.eval('$temp=$gMainWindow')

        if cmds.menu(cls.menu_name, q=True, ex=True):
            cls.menu = cmds.menu(cls.menu_name, e=True, dai=True, to=True)
        else:
            cls.menu = cmds.menu(cls.menu_name, l=cls.menu_name, p=g_main_window, to=True)

        # メニュー追加
        cls._add_items()
