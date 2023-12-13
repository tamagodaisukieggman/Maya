# callbacks for editing check boxes
def selectAllCallback(ui, *args):
    callback_object = [ui.HandL, ui.HandR, ui.LegL, ui.LegR]
    if ui.selectAllCheck.isChecked():
        for i in callback_object:
            i.setChecked(False)
            i.setEnabled(False)
    else:
        for i in callback_object:
            # i.setChecked(False)
            i.setEnabled(True)


def selectHandLeg(ui, *args):
    ui.selectAllCheck.setChecked(False)


# callbacks for editing check boxes
def translateAllCallback(ui, *args):
    ui.translateXCheck.setChecked(False)
    ui.translateYCheck.setChecked(False)
    ui.translateZCheck.setChecked(False)


def translateXYZCallback(ui, *args):
    ui.translateAllCheck.setChecked(False)


def rotateAllCallback(ui, *args):
    ui.rotateXCheck.setChecked(False)
    ui.rotateYCheck.setChecked(False)
    ui.rotateZCheck.setChecked(False)


def rotateXYZCallback(ui, *args):
    ui.rotateAllCheck.setChecked(False)


def idleModeCallback(ui, *args):
    if ui.idleModeCheck.isChecked():
        ui.useFrame.setEnabled(True)
    else:
        ui.useFrame.setEnabled(False)
