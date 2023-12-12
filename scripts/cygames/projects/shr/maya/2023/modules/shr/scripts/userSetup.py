"""User Setup

Maya起動時点で不必要にモジュールを読み込ませたくないので関数内でimportする。
"""


class UserSetup:
    """User Setup"""

    def __init__(self) -> None:
        from shr import logger

        self.logger = logger
        self.logger.send_launch("UserSetup")

    def _add_menu(self):
        self.logger.debug("Load menu.")

        from maya import utils

        utils.executeDeferred("import shr.menu as menu;menu.create_menus()")

    def _add_runtime_command(self):
        self.logger.debug("Load: Required Plugins")
        pass

    def _load_required_plugins(self):
        self.logger.debug("Load: Required Plugins")

    def _reset_pref_settings(self):
        self.logger.debug("Reset: Maya Preference settings")

        # from maya import utils
        # utils.executeDeferred(PrefSettings.reset_pref_settings)/

    def _add_cutscene_script_job(self):
        from shr.cutscene import editor

        editor.create_cutscene_extension_switcher_job()

    def _color_management(self):
        from maya import utils

        utils.executeDeferred(
            "from shr.utils.color_management import ColorManagement;ColorManagement._enable_color_management()"
        )

    def _reset_pref_settings(self):
        # fpsの設定
        from maya import utils

        utils.executeDeferred(
            'from shr.utils.editor_settings import FramerateSettings;fps_settings = FramerateSettings("ntscf");fps_settings.set_framerate()'
        )

    def exec_(self):
        """クラス内の処理をそれぞれ実行。"""
        # self._load_required_plugins()
        self._reset_pref_settings()
        self._add_menu()
        # self._add_runtime_command()

        # self._add_cutscene_script_job()
        self._color_management()


if __name__ == "__main__":
    try:
        us = UserSetup()
        us.exec_()

    except Exception:
        # mtkのuserSetup.pyで問題が起きた時にmtk3dが巻き添えになるので、tryCatchする。
        import traceback

        traceback.print_exc()
