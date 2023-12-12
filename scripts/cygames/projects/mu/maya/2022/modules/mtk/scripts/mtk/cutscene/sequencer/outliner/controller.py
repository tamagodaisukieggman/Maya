from __future__ import annotations

import typing as tp
from pprint import pprint

from mtk.cutscene.sequencer.lib.qt import MayaAppBase, MayaMainWindowBase
from PySide2.QtWidgets import QApplication

from .view import OutlineWindow


class MayaApp(MayaAppBase):
    def __init__(self):
        super().__init__()

    def initialize(self, app: QApplication) -> None:
        return super().initialize(app)

    def create_window(self) -> MayaMainWindowBase:
        return OutlineWindow()


if __name__ == "__main__":
    base = MayaApp()
    base.execute()
