# -*- coding: utf-8 -*-
u"""userSetup"""
import maya.cmds as cmds

class TsubasaDccUserSetup(object):

    @classmethod
    def display_info(cls):
        u"""情報表示"""
        print("[PRJ] {prj:<8} [VER] {ver:<5} [TYPE] {typ}".format(prj='tsubasa', ver='share', typ='dcc user'))

    @classmethod
    def add_menu(cls):
        u"""メニューttsubasa(Artist)」を追加"""
        # import maya.utils
        # maya.utils.executeDeferred('from tsubasa_menu import TsubasaDccUserMenu;TsubasaDccUserMenu.main()')
        # メニューの「tsubasa」の後ろに表示するためこちら側ではevalDeferredを使う
        if not cmds.about(b=True):
            cmds.evalDeferred('from tsubasa_menu import TsubasaDccUserMenu;TsubasaDccUserMenu.main()')

    @classmethod
    def main(cls):
        u"""main関数"""
        cls.display_info()
        cls.add_menu()


if __name__ == '__main__':
    TsubasaDccUserSetup.main()
