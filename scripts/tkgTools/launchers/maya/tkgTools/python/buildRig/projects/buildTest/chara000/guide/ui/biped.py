# -*- coding: utf-8 -*-
def onMayaDroppedPythonFile(*args):
    from imp import reload
    import os

    import buildRig.libs.picker.ui as guide_ui
    reload(guide_ui)

    class PickerUI:
        def __init__(self):
            self.picker = guide_ui.PickerAnimTools()
            self.picker.buildUI()
            self.picker.setWindowTitle('GuidePicker')
            self.picker.show(dockable=True)


    pickerui = PickerUI()

