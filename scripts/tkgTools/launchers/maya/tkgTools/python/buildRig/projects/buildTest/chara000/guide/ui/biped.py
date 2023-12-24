# -*- coding: utf-8 -*-
from imp import reload
import os

import buildRig.libs.picker.ui as guide_ui
reload(guide_ui)

class GuideUI:
    def __init__(self):
        self.picker = guide_ui.PickerAnimTools()
        self.picker.buildUI()
        self.picker.show(dockable=True)

def onMayaDroppedPythonFile(*args):
    guideUI = GuideUI()

