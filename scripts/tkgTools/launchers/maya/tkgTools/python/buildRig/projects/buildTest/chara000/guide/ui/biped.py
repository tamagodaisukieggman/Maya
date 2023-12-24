# -*- coding: utf-8 -*-
from imp import reload

import buildRig.libs.ui as guide_ui
reload(guide_ui)

class GuideUI:
    def __init__(self):
        self.picker = guide_ui.PickerAnimTools()
        self.picker.show(dockable=True)