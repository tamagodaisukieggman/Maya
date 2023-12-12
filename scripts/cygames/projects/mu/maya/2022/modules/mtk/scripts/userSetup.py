"""User Setup for mutsunokami (mtk)

Maya起動時点で不必要にモジュールを読み込ませたくないので関数内でimportする。
"""


class MtkUserSetup:
    """Mtk User Setup
    """

    def __init__(self) -> None:
        from mtk import logger
        self.logger = logger
        self.logger.send_launch('MtkUserSetup')

    def _add_menu(self):
        self.logger.debug('Load: "mutsunokami" menu.')

        from maya import utils
        utils.executeDeferred('import mtk.menu as menu;menu.create_menus()')

    def _add_runtime_command(self):
        self.logger.debug('Load: Required Plugins')
        pass

    def _load_required_plugins(self):
        self.logger.debug('Load: Required Plugins')

    def _reset_pref_settings(self):
        self.logger.debug('Reset: Maya Preference settings')

        # from maya import utils
        # utils.executeDeferred(PrefSettings.reset_pref_settings)/

    def _add_cutscene_script_job(self):
        from mtk.cutscene import editor
        editor.create_cutscene_extension_switcher_job()

    def exec_(self):
        """クラス内の処理をそれぞれ実行。
        """
        # self._load_required_plugins()
        # self._reset_pref_settings()
        self._add_menu()
        # self._add_runtime_command()
        self._add_cutscene_script_job()


# class PrefSettings:

#     def _reset_pref_settings(self):
#         import maya.mel as mel
#         mel.eval('source createPreferencesOptVars.mel;')
#         mel.eval('syncPreferencesOptVars("syncCurrentToOpt");')
#         mel.eval('revertToColorManagementDefaults();')

#     def _apply_evaluator_settings(self):
#         from maya import cmds
#         if cmds.about(api=True) >= 201700:
#             # 非表示エバリュエーター設定
#             cmds.evaluator(name='invisibility', en=False)

#     def _apply_pref_settings(self):
#         from maya import cmds
#         from maya import mel
#         save_layout = 0
#         restore_layout = 0

#         cmds.optionVar(iv=["useSaveScenePanelConfig", save_layout])
#         mel.eval("$gUseSaveScenePanelConfig=" + str(save_layout))

#         cmds.optionVar(iv=["useScenePanelConfig", restore_layout])
#         mel.eval("$gUseScenePanelConfig=" + str(restore_layout))

#     def exec_(self):
#         from maya import utils
#         # キューなので、実行して欲しい順序と逆にする

#         utils.executeDeferred(self._apply_pref_settings)
#         utils.executeDeferred(self._apply_evaluator_settings)


if __name__ == '__main__':
    try:
        MUS = MtkUserSetup()
        MUS.exec_()

    except Exception:
        # mtkのuserSetup.pyで問題が起きた時にmtk3dが巻き添えになるので、tryCatchする。
        import traceback
        traceback.print_exc()
