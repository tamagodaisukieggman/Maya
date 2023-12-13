# -*- coding: utf-8 -*-
import os
import sys
import webbrowser

from PySide2.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QErrorMessage,
)
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from maya import cmds
from maya.app.general import mayaMixin

from .joint_geometrize import Geometrize

current_path = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/')

NOT_EXISTS_JOINTS = ["jnt_0000_skl_root", "jnt_mtp", "jnt_cnp", "jnt_move_root"]

class JointGeometrizer(mayaMixin.MayaQWidgetBaseMixin, QMainWindow):

    _windowTitle = "Joint Geometrizer"
    _windowName = _windowTitle.replace(' ', '_')

    def __init__(self, *args):
        super(JointGeometrizer, self).__init__(*args)

        self.setWindowTitle(self._windowTitle)
        self.setObjectName(self._windowName)

        f = QFile(current_path + "/ui/main.ui")
        f.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.UI = loader.load(f)
        self.setCentralWidget(self.UI)

        self.UI.aboutAction.setText("About {}".format(self._windowTitle))

        self.UI.cylinderRadiusDoubleSpinBox.setRange(0, 15)
        self.UI.cylinderRadiusHorizontalSlider.setRange(0, 15)
        self.UI.sphereSizeDoubleSpinBox.setRange(0, 25)
        self.UI.sphereSizeHorizontalSlider.setRange(0, 25)

        self.UI.cylinderRadiusDoubleSpinBox.setValue(7)
        self.UI.cylinderRadiusHorizontalSlider.setValue(7)
        self.UI.sphereSizeDoubleSpinBox.setValue(10)
        self.UI.sphereSizeHorizontalSlider.setValue(10)

        self.set_signals()

        self.resize(300, 100)

        self.geometrizer = Geometrize()


    def set_signals(self):
        self.UI.execPushButton.clicked.connect(self.execute)
        self.UI.resetAction.triggered.connect(self.reset_settings)
        self.UI.aboutAction.triggered.connect(self.open_document)
        self.UI.cylinderRadiusDoubleSpinBox.valueChanged.connect(
            self._cylinderRadiusDoubleSpinBoxValueChanged)
        self.UI.sphereSizeDoubleSpinBox.valueChanged.connect(
            self._sphereSizeDoubleSpinBoxValueChanged)
        self.UI.cylinderRadiusHorizontalSlider.valueChanged.connect(
            self._cylinderRadiusHorizontalSliderValueChnaged)
        self.UI.sphereSizeHorizontalSlider.valueChanged.connect(
            self._sphereSizeHorizontalSliderValueChanged)


    def reset_settings(self):
        self.geometrizer.clean()

        self.UI.cylinderRadiusDoubleSpinBox.setValue(7)
        self.UI.sphereSizeHorizontalSlider.setValue(10)


    def _cylinderRadiusDoubleSpinBoxValueChanged(self):
        self.UI.cylinderRadiusHorizontalSlider.setValue(
            self.UI.cylinderRadiusDoubleSpinBox.value())

        for cylinder in self.geometrizer.cylinders:
            if not cmds.ls(cylinder[0]):
                continue
            cmds.setAttr("{}.radius".format(cylinder[1]), 
            self.UI.cylinderRadiusDoubleSpinBox.value())


    def _sphereSizeDoubleSpinBoxValueChanged(self):
        self.UI.sphereSizeHorizontalSlider.setValue(
            self.UI.sphereSizeDoubleSpinBox.value())

        for sphere in self.geometrizer.spheres:
            if not cmds.ls(sphere[0]):
                continue
            cmds.setAttr("{}.radius".format(sphere[1]),
            self.UI.sphereSizeDoubleSpinBox.value())


    def _cylinderRadiusHorizontalSliderValueChnaged(self):
        self.UI.cylinderRadiusDoubleSpinBox.setValue(
            self.UI.cylinderRadiusHorizontalSlider.value())


    def _sphereSizeHorizontalSliderValueChanged(self):
        self.UI.sphereSizeDoubleSpinBox.setValue(
            self.UI.sphereSizeHorizontalSlider.value())


    def open_document(self):
        webbrowser.open("https://wisdom.cygames.jp/x/zL_xC")


    def execute(self):

        if cmds.ls("JointGeometry"):
            messageBox = QMessageBox()
            result = messageBox.warning(self,
                        "Warning!",
                        u"先に JointGeometry が作られとるばい。\nクリーンして、実行してよか？",
                        QMessageBox.StandardButtons(QMessageBox.Ok | QMessageBox.Cancel))

            if result == QMessageBox.Cancel:
                return
            
            self.geometrizer.clean()

        cylinder_radius = self.UI.cylinderRadiusDoubleSpinBox.value()
        shere_radius = self.UI.sphereSizeDoubleSpinBox.value()

        joints = []
        for joint in cmds.ls(type="joint"):
            _flag = [x for x in NOT_EXISTS_JOINTS if joint.startswith(x)]
            if not _flag:
                joints.append(joint)

        if not joints:
            dialog = QErrorMessage(self)
            dialog.showMessage(u"ジョイントが見つからんばい。\nシーンば間違ったっちゃなかと？")
            return
        
        for joint in joints:
            self.geometrizer.geometrize(joint, cradius=cylinder_radius, sradius=shere_radius)

        group = cmds.group([x[0] for x in self.geometrizer.cylinders], n="JointGeometry")
        cmds.parent([x[0] for x in self.geometrizer.spheres], group)

def main():
    win = JointGeometrizer()
    win.show()


if __name__ == '__main__':
    main()
    