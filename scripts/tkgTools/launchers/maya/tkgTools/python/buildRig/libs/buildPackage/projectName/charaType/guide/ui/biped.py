# -*- coding: utf-8 -*-

def onMayaDroppedPythonFile():
    from imp import reload
    import os
    import sys

    import buildRig.libs.picker.guide as guide
    reload(guide)

    pickerui = guide.PickerUI()

