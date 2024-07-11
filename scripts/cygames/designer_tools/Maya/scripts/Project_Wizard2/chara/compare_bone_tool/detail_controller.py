import webbrowser
import typing as tp

import maya.cmds as cmds

from ..chara_utility import utility as chr_utils
from .detail_view import DetailView
from .app import BoneCheckedData


class DetailController:
    def __init__(self, checked_data: BoneCheckedData):
        self.ui = DetailView(checked_data)
        self.ui.gui.joint_name_txt.setText(checked_data.joint_name)
        self.setup_ui()

    def setup_ui(self):
        ...

    def show_manual(self):
        """コンフルのツールマニュアルページを開く"""
        try:
            webbrowser.open(
                "https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=756510863"
            )
        except Exception:
            cmds.warning("マニュアルページがみつかりませんでした")

    def show_ui(self):
        self.ui.show()

    def close_ui(self):
        self.ui.close()
