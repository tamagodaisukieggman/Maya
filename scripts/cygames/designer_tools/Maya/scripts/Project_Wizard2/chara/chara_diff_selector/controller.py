import webbrowser
import maya.cmds as cmds

from .view import View
from . import chara_dif_model_selector
from . import chara_dif_texture_selector



class DiffSelectController:
    def __init__(self):
        self.ui = View()
        self.model_selector_view = chara_dif_model_selector.get_view_controller()
        self.texture_selector_view = chara_dif_texture_selector.get_view_controller()
        self.setup_ui()
    
    def setup_ui(self):
        self.ui.gui.diff_model_lay.addWidget(self.model_selector_view.ui)
        self.ui.gui.diff_texture_lay.addWidget(self.texture_selector_view.ui)

        self.ui.gui.target_lock_to_model_diff_target_cbox
        
        self.ui.windowClosed.connect(self.on_diff_mainwindow_closed)
        # modelのコンボボックスの値が変わったとき
        self.model_selector_view.ui.on_change_index_combobox.connect(self.change_model_selector_index)

        self.ui.gui.action_reset_texture_path.triggered.connect(self.on_action_reset_texture_path)
        self.ui.gui.action_document.triggered.connect(self.show_manual)
    
    def change_model_selector_index(self,list_index:int):
        """モデルのコンボボックスが変更されたときにconnectされた処理

        Args:
            list_index (int): 変更されたcomboxの行
        """
        is_target_lock = self.ui.gui.target_lock_to_model_diff_target_cbox.isChecked()
        if is_target_lock:
            selector_widget = self.get_widget_from_row(self.model_selector_view.ui.gui.selector_list,list_index)

            current_model_index = selector_widget.get_current_diff_index()
            target_parts_id = selector_widget.get_current_parts_id()

            self._reset_texture_list_widget(target_parts_id, current_model_index)

            self._change_texture_by_model_index(current_model_index)

    def _reset_texture_list_widget(self, target_parts_id:str, index:int):
        """texture_list_viewの再設定
        baseを選択してからinitializeの実行まで行う
        """
        target_base_name = f"{target_parts_id}_{index}"
        if cmds.objExists(target_base_name):
            cmds.select(target_base_name,r=True)
            self.texture_selector_view.initialize_list()

    def _change_texture_by_model_index(self, current_model_index:int):
        """selectorからテクスチャを設定。現在targetとなっている全てのマテリアルが対象

        Args:
            current_model_index (int): 変更する対象の値
        """
        for material_name in self.texture_selector_view.selectors:
            self.texture_selector_view.set_texture_by_diff_data(material_name,{"model_diff_indexes":current_model_index})
    
    def on_diff_mainwindow_closed(self):
        self.execute_reset_all_material_texture_tool()
    
    def on_action_reset_texture_path(self):
        result = cmds.confirmDialog( title='警告', message='ツールを実行した場合差分変更ツールを終了します。よろしいですか？', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if result == "Yes":
            self.close_ui()


    def execute_reset_all_material_texture_tool(self):
        result = cmds.confirmDialog( title='警告', message='マテリアルにアサインされているテクスチャをデフォルトに戻しますか？', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if result == "Yes":
            self._reset_all_material_texture_path()

    def _reset_all_material_texture_path(self):
        #参照がいた時のために":"をつけた状態とそうでないとき両方で処理
        objects_with_namespace = cmds.ls("*:mt_*", type="lambert")
        objects_without_namespace = cmds.ls("mt_*", type="lambert")
        materials = objects_with_namespace + objects_without_namespace

        if materials:
            texture_selector_controller = chara_dif_texture_selector.get_view_controller()
            for material in materials:
                texture_selector = texture_selector_controller.create_selector(material)
                texture_selector.set_default_indexes()

    def show_manual(self):
        """コンフルのツールマニュアルページを開く"""
        try:
            webbrowser.open(
                "https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=756510863"
            )
        except Exception:
            cmds.warning("マニュアルページがみつかりませんでした")
                
            
    @staticmethod
    def get_widget_from_row(list_widget, row):
        item = list_widget.item(row)
        widget = list_widget.itemWidget(item)
        return widget

    def show_ui(self):
        self.ui.show()

    def close_ui(self):
        self.ui.close()
