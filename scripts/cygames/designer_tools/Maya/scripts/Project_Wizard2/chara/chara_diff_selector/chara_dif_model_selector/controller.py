from .view import ModelSelectorMainWindow
import maya.cmds as cmds
from ...chara_utility import utility as chara_utility
from .app import DifModelVisibilitySetter


class DiffModelSelectController:
    def __init__(self):
        self.ui = ModelSelectorMainWindow()
        self.setup_ui()

    def setup_ui(self):
        self.ui.gui.re_search_btn.clicked.connect(self.clicked_re_search_btn)
        self.ui.on_change_index_combobox.connect(self.set_visibility)

    def reset_root_object(self):
        """root objectのオブジェクトのリセット"""
        selected = cmds.ls(sl=True, type="transform")
        if not selected:
            cmds.warning("対象となるノードを選択して実行してください。")
            return
        object = cmds.ls(sl=True, type="transform")[0]
        self.root = chara_utility.get_root_node(object)
        self.ui.set_root_name(self.root)
        self.visibility_setter = DifModelVisibilitySetter(self.root)
        self.ui.initialize_list(self.visibility_setter.diff_datas)

    def set_visibility(self, index):
        current_selector = self.ui.selectors[index]
        current_id = current_selector.get_current_parts_id()
        current_index = current_selector.get_current_diff_index()
        self.visibility_setter.set_visibility(current_id, current_index)

    def clicked_re_search_btn(self):
        self.reset_root_object()

    def close_ui(self):
        self.ui.close()

    def show_ui(self):
        self.ui.show()
