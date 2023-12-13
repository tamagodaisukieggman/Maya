"""User Setup

Maya起動時点で不必要にモジュールを読み込ませたくないので関数内でimportする。
"""


class UserSetup:
    """User Setup
    """

    def _add_menu(self):

        from maya import utils
        utils.executeDeferred('import shr3d.menu as menu;menu.create_menus()')


    def exec_(self):
        """クラス内の処理をそれぞれ実行。
        """
        self._add_menu()


if __name__ == '__main__':
    try:
        us = UserSetup()
        us.exec_()

    except Exception:
        # mtkのuserSetup.pyで問題が起きた時にmtk3dが巻き添えになるので、tryCatchする。
        import traceback
        traceback.print_exc()
