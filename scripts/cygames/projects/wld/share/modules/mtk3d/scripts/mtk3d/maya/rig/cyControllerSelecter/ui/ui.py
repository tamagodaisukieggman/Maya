# -*- coding: utf-8 -*-

import os
import os.path
import maya.cmds as mc

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import imp

try:
    imp.find_module('PySide2')
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtUiTools import *
    from PySide2.QtWidgets import *

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import *

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class CtrlSelecter(MayaQWidgetBaseMixin, QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CtrlSelecter, self).__init__(*args, **kwargs)
        self.window = self.__class__.__name__
        self.setObjectName(self.window)
        self.rubberBand = None
        self.origin = None

        # current pathを取得してそこにあるUIファイルをロードする
        loader = QUiLoader()
        ui_file_path = os.path.join(CURRENT_PATH, 'UI.ui')
        self.UI = loader.load(ui_file_path)
        self.setCentralWidget(self.UI)

        qrect = self.UI.geometry()
        self.setWindowTitle('DragonPickerUI')
        self.setGeometry(100, 100, qrect.width(), qrect.height())

        self.get_namespace()
        self.create_job()
        self._connect()
        self.load_setting()

    def create_job(self):
        mc.scriptJob(event=['SceneOpened', self.scenes_open], protected=True)

    def scenes_open(self):
        self.get_namespace()

    def _connect(self):
        self.UI.nmspList.activated.connect(self.combobox_act)

        object_callback = (
            self.UI.worldOffset, self.UI.localOffset, self.UI.cogCtrl, self.UI.spineACtrl, self.UI.spineBCtrl,
            self.UI.neckACtrl, self.UI.neckBCtrl, self.UI.headCtrl,
            self.UI.jawCtrl, self.UI.headAimCtrl, self.UI.shoulder_R_Ctrl, self.UI.shoulder_L_Ctrl, self.UI.hipCtrl,
            self.UI.foot_L_Ctrl, self.UI.leg_L_BCtrl,
            self.UI.toe_L_BCtrl, self.UI.foot_R_Ctrl, self.UI.leg_R_BCtrl, self.UI.toe_R_BCtrl, self.UI.footF_L_Ctrl,
            self.UI.footF_L_RotCtrl,
            self.UI.footF_R_Ctrl, self.UI.footF_R_RotCtrl, self.UI.leg_L_BPoleVectorCtrl, self.UI.leg_R_BPoleVectorCtrl,
            self.UI.arm_L_BPoleVectorCtrl,
            self.UI.arm_R_BPoleVectorCtrl, self.UI.spineCCtrl, self.UI.tail_00ikJtSplineCrvCtrlJtAD,
            self.UI.tail_00ikJtSplineCrvCtrlJtAC,
            self.UI.tail_00ikJtSplineCrvCtrlJtAB, self.UI.tail_08fkJtfkCtrl, self.UI.tail_07fkJtfkCtrl,
            self.UI.tail_06fkJtfkCtrl, self.UI.tail_05fkJtfkCtrl,
            self.UI.tail_04fkJtfkCtrl, self.UI.tail_03fkJtfkCtrl, self.UI.tail_02fkJtfkCtrl, self.UI.tail_01fkJtfkCtrl,
            self.UI.tail_00fkJtfkCtrl, self.UI.tail_00ikJtSplineCrvCtrlJtAA, self.UI.spineAIkCtrl,
            self.UI.spineBIkCtrl, self.UI.neckAIkCtrl, self.UI.spineCIkCtrl, self.UI.hand_L_fkCtrl,
            self.UI.foot_L_BFkCtrl, self.UI.toe_L_BFkCtrl, self.UI.hand_R_fkCtrl, self.UI.foot_R_BFkCtrl,
            self.UI.toe_R_BFkCtrl, self.UI.leg_R_IkFkSwitcher, self.UI.arm_R_IkFkSwitcher,
            self.UI.leg_L_IkFkSwitcher, self.UI.arm_L_IkFkSwitcher, self.UI.leg_R_fkCtrl, self.UI.upLeg_R_fkCtrl,
            self.UI.leg_L_fkCtrl, self.UI.upLeg_L_fkCtrl,
            self.UI.foreArm_R_fkCtrl, self.UI.arm_R_fkCtrl, self.UI.foreArm_L_fkCtrl, self.UI.arm_L_fkCtrl,
            self.UI.hand_L_RotCtrl, self.UI.hand_R_RotCtrl,
            self.UI.inEyelid_R_ctrl, self.UI.eyeAim_R_Ctrl, self.UI.eyeRot_R_Ctrl, self.UI.downEyelid_R_ctrl,
            self.UI.upEyelid_R_ctrl, self.UI.inEyelid_L_ctrl,
            self.UI.eyeAim_L_Ctrl, self.UI.eyeRot_L_Ctrl, self.UI.downEyelid_L_ctrl, self.UI.upEyelid_L_ctrl,
            self.UI.legThumbA_R_IkCtrl, self.UI.legRingB_R_IkCtrl,
            self.UI.legRingA_R_IkCtrl, self.UI.legMiddleB_R_IkCtrl, self.UI.legMiddleA_R_IkCtrl, self.UI.legIndexB_R_IkCtrl,
            self.UI.legIndexA_R_IkCtrl,
            self.UI.handThumbA_R_IkCtrl, self.UI.handThumbA_L_IkCtrl, self.UI.handIndexB_L_IkCtrl,
            self.UI.handIndexA_L_IkCtrl,
            self.UI.handMiddleB_L_IkCtrl, self.UI.handMiddleA_L_IkCtrl, self.UI.handRingB_L_IkCtrl,
            self.UI.handRingA_L_IkCtrl, self.UI.handPinkyB_L_IkCtrl,
            self.UI.handPinkyA_L_IkCtrl, self.UI.handIndexB_R_IkCtrl, self.UI.handIndexA_R_IkCtrl,
            self.UI.handMiddleB_R_IkCtrl, self.UI.handMiddleA_R_IkCtrl,
            self.UI.handRingB_R_IkCtrl, self.UI.handRingA_R_IkCtrl, self.UI.handPinkyB_R_IkCtrl,
            self.UI.handPinkyA_R_IkCtrl, self.UI.legRingB_R_FkCtrl,
            self.UI.legRingA_R_FkCtrl, self.UI.legMiddleB_R_FkCtrl, self.UI.legMiddleA_R_FkCtrl, self.UI.legIndexB_R_FkCtrl,
            self.UI.legIndexA_R_FkCtrl,
            self.UI.legThumbA_R_FkCtrl, self.UI.legRingB_L_FkCtrl, self.UI.legRingA_L_FkCtrl, self.UI.legMiddleB_L_FkCtrl,
            self.UI.legMiddleA_L_FkCtrl,
            self.UI.legThumbA_L_FkCtrl, self.UI.handThumbA_R_FkCtrl, self.UI.handIndexB_R_FkCtrl,
            self.UI.handIndexA_R_FkCtrl,
            self.UI.handMiddleB_R_FkCtrl, self.UI.handMiddleA_R_FkCtrl, self.UI.handRingB_R_FkCtrl,
            self.UI.handRingA_R_FkCtrl, self.UI.handPinkyB_R_FkCtrl,
            self.UI.handPinkyA_R_FkCtrl, self.UI.handThumbA_L_FkCtrl, self.UI.handIndexB_L_FkCtrl,
            self.UI.handIndexA_L_FkCtrl,
            self.UI.handMiddleB_L_FkCtrl, self.UI.handMiddleA_L_FkCtrl, self.UI.handRingB_L_FkCtrl,
            self.UI.handRingA_L_FkCtrl, self.UI.handPinkyB_L_FkCtrl,
            self.UI.handPinkyA_L_FkCtrl, self.UI.neck_02FkJtCtrl, self.UI.legThumbA_L_IkCtrl, self.UI.legIndexA_L_IkCtrl,
            self.UI.legIndexB_L_IkCtrl,
            self.UI.legMiddleA_L_IkCtrl, self.UI.legMiddleB_L_IkCtrl, self.UI.legRingA_L_IkCtrl, self.UI.legRingB_L_IkCtrl,
            self.UI.hand_L_RotBCtrl,
            self.UI.hand_R_RotBCtrl, self.UI.hand_L_fkRotCtrl, self.UI.hand_R_fkRotCtrl, self.UI.legIndexA_L_FkCtrl,
            self.UI.legIndexB_L_FkCtrl, self.UI.foot_R_RotCtrl, self.UI.foot_L_RotCtrl, self.UI.cogSpaceCtrl,
            self.UI.root_mtp_ctrl_00, self.UI.root_mtp_ctrl_01, self.UI.root_mtp_ctrl_02, self.UI.head_mtp_ctrl_10,
            self.UI.head_mtp_ctrl_11, self.UI.head_mtp_ctrl_12,
            self.UI.neck00_mtp_ctrl_20, self.UI.neck00_mtp_ctrl_21, self.UI.neck00_mtp_ctrl_22,
            self.UI.spine_02_mtp_ctrl_30, self.UI.spine_02_mtp_ctrl_31, self.UI.spine_02_mtp_ctrl_32,
            self.UI.leftHand_mtp_ctrl_40, self.UI.leftHand_mtp_ctrl_41, self.UI.leftHand_mtp_ctrl_42,
            self.UI.rightHand_mtp_ctrl_50, self.UI.rightHand_mtp_ctrl_51, self.UI.rightHand_mtp_ctrl_52,
            self.UI.leftToeBase_mtp_ctrl_60, self.UI.leftToeBase_mtp_ctrl_61, self.UI.leftToeBase_mtp_ctrl_62,
            self.UI.rightToeBase_mtp_ctrl_70, self.UI.rightToeBase_mtp_ctrl_71, self.UI.rightToeBase_mtp_ctrl_72)

        for object in object_callback:
            object.clicked.connect(self.callback)

    def combobox_act(self):
        self.UI.nmspList.currentText()

    def callback(self, *args):
        mc.select(clear=True)
        buttons = self.findChildren(QPushButton)
        nmsp = self.UI.nmspList.currentText()
        nmsp = nmsp + ':'
        ctrl_list = []
        for i in buttons:
            if i.isChecked():
                ctrl_list.append(i)
            else:
                pass

        for node in ctrl_list:
            buttons = node.objectName()
            mc.select(nmsp + buttons, add=True)

    def get_namespace(self, *args):
        self.UI.nmspList.clear()
        exclude_list = ['UI', 'shared']
        mc.namespaceInfo(cur=True)
        mc.namespace(set=':')
        namespaces = ['{}'.format(ns) for ns in mc.namespaceInfo(lon=True) if ns not in exclude_list]
        [self.UI.nmspList.addItem(x) for x in namespaces]

    def load_setting(self):
        setting = QSettings("setting.ini", QSettings.IniFormat)
        self.restoreState(setting.value("windowState"))
        self.restoreGeometry(setting.value("geometry"))

    def close_event(self, event):

        setting = QSettings("setting.ini", QSettings.IniFormat)
        setting.setValue("windowState", self.saveState())
        setting.setValue("geometry", self.saveGeometry())

    def mousePressEvent(self, event):
        self.origin = event.pos()
        if not self.rubberBand:
            self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.rubberBand.setGeometry(QRect(self.origin, QSize()))
        self.rubberBand.show()

    # mouseをドラッグすると四角を描画する
    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    # mouseRelease時の挙動
    def mouseReleaseEvent(self, event):

        modifiers = QApplication.keyboardModifiers()

        # shiftが押されていた場合
        if modifiers == Qt.ShiftModifier:
            print('Shift+Click')
            self.rubberBand.hide()
            getBtn = self.findChildren(QPushButton)
            selected = []
            rect = self.rubberBand.geometry()

            for child in self.findChildren(QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)

            for j in selected:
                if j.isChecked():
                    j.click()

                else:
                    j.click()

        # controlが押されていた場合
        elif modifiers == Qt.ControlModifier:
            print('Control+Click')
            self.rubberBand.hide()
            getBtn = self.findChildren(QPushButton)
            selected = []
            rect = self.rubberBand.geometry()

            for child in self.findChildren(QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)
            for j in selected:
                if j.isChecked():
                    j.click()
                else:
                    pass

        # shift + ctrlが押されていた場合
        elif modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            print('Control + Shift + Click')
            self.rubberBand.hide()
            getBtn = self.findChildren(QPushButton)
            selected = []
            rect = self.rubberBand.geometry()

            for child in self.findChildren(QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)
            for j in selected:
                if j.isChecked():
                    pass
                else:
                    j.click()

        # 何も押されていなかった場合
        else:
            print('Click')

            self.rubberBand.hide()
            getBtn = self.findChildren(QPushButton)
            for i in getBtn:
                if i.isChecked():
                    i.click()

            selected = []
            rect = self.rubberBand.geometry()

            for child in self.findChildren(QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)

            for j in selected:
                j.click()


def main():
    QApplication.instance()
    ui = CtrlSelecter()
    ui.show()
    # sys.exit(app.exec_())
    return ui


if __name__ == '__main__':
    main()