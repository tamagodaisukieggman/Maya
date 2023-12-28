# -*- coding: utf-8 -*-

def onMayaDroppedPythonFile(obj):
    from imp import reload
    import os
    import sys

    try:
        import buildRig.libs.picker.guide as guide
        reload(guide)
    except:
        print(traceback.format_exc())

    pickerui = guide.PickerUI()
    pickerui.buildUI()
    pickerui.show(dockable=True)
