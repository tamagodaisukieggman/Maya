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


class GUI(MayaQWidgetBaseMixin, QMainWindow):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.window = self.__class__.__name__
        self.setObjectName(self.window)
        self.rubberBand = None
        self.origin = None

        # current pathを取得してそこにあるUIファイルをロードする
        loader = QUiLoader()
        uiFilePath = os.path.join(CURRENT_PATH, 'charaUI.ui')
        self.UI = loader.load(uiFilePath)
        self.setCentralWidget(self.UI)

        qrect = self.UI.geometry()
        self.setWindowTitle('CharaPickerUI')
        self.setGeometry(100, 100, qrect.width(), qrect.height())

        self.getNameSpace()
        self.setHighLowMesh()
        self._connect()
        self.createJob()
        # self.setSelection()
        self.load_setting()

    def createJob(self):
        mc.scriptJob(event=['SceneOpened', self.scenesOpen], protected=True)

    def scenesOpen(self):
        self.getNameSpace()
        # self.setSelection()
        self.setHighLowMesh()

    def setHighLowMesh(self):
        try:
            val = mc.getAttr("ply00_999_rig:" + "displaySet.meshTypeLOD")
            if val == 0:
                self.UI.highLowButton.setCurrentIndex(0)
            elif val == 1:
                self.UI.highLowButton.setCurrentIndex(1)
            else:
                pass
        except Exception as e:
            print(e)

    def getNameSpace(self):
        self.UI.nmspList.clear()
        rn = mc.ls(type="reference")
        for i in rn:
            list = i.split(":")
            count = len(list)
            if count == 1:
                for i in list:
                    NSP = i.split("RN")
                    if NSP[0]:
                        self.UI.nmspList.addItem(NSP[0])
            else:
                pass

    def getNameSpaceFirst(self):
        self.UI.nmspList.clear()
        rn = mc.ls(type="reference")
        for i in rn:
            list = i.split(":")
            count = len(list)
            if count == 1:
                for i in list:
                    NSP = i.split("RN")
                    if NSP[0] == "ply00_999":
                        self.UI.nmspList.addItem(NSP[0])
            else:
                pass

    def comboboxAct(self):
        self.UI.nmspList.currentText()

    def _connect(self):
        # UIファイルのgetNsButtonがクリックされていたらmoduleのgetNssへつなぐ、getNssの処理はUIのnmspListへネームスペースを追加
        self.UI.nmspList.activated.connect(self.comboboxAct)
        # print "test"
        self.UI.highLowButton.activated.connect(self.highLow)

        object_callback = (self.UI.worldOffset, self.UI.localOffset, self.UI.hip_Ctrl, self.UI.spineA_Ctrl, self.UI.spineB_Ctrl, self.UI.chest_Ctrl,
                           self.UI.shoulder_L_Ctrl, self.UI.shoulder_R_Ctrl, self.UI.neck_Ctrl, self.UI.head_Ctrl, self.UI.hand_L_Ctrl, self.UI.arm_L_PVCtrl, self.UI.hand_R_Ctrl, self.UI.arm_R_PVCtrl,
                           self.UI.leg_L_Ctrl, self.UI.heel_L_PivCtrl, self.UI.toe_L_PivCtrl, self.UI.foot_L_APivCtrl, self.UI.foot_L_BPivCtrl, self.UI.toe_L_Ctrl, self.UI.foot_L_Ctrl, self.UI.leg_L_PVCtrl,
                           self.UI.leg_R_Ctrl, self.UI.heel_R_PivCtrl, self.UI.toe_R_PivCtrl, self.UI.foot_R_APivCtrl, self.UI.foot_R_BPivCtrl, self.UI.toe_R_Ctrl, self.UI.foot_R_Ctrl, self.UI.leg_R_PVCtrl,
                           self.UI.wrist_L_Ctrl, self.UI.thumbA_L_Ctrl, self.UI.thumbB_L_Ctrl, self.UI.thumbC_L_Ctrl, self.UI.indexA_L_Ctrl, self.UI.indexB_L_Ctrl, self.UI.indexC_L_Ctrl, self.UI.midA_L_Ctrl,
                           self.UI.midB_L_Ctrl, self.UI.midC_L_Ctrl, self.UI.ringA_L_Ctrl, self.UI.ringB_L_Ctrl, self.UI.ringC_L_Ctrl, self.UI.pinkyA_L_Ctrl, self.UI.pinkyB_L_Ctrl, self.UI.pinkyC_L_Ctrl,
                           self.UI.eq_rightHandCtrl, self.UI.wrist_R_Ctrl, self.UI.thumbA_R_Ctrl, self.UI.thumbB_R_Ctrl, self.UI.thumbC_R_Ctrl, self.UI.indexA_R_Ctrl, self.UI.indexB_R_Ctrl, self.UI.indexC_R_Ctrl,
                           self.UI.midA_R_Ctrl, self.UI.midB_R_Ctrl, self.UI.midC_R_Ctrl, self.UI.ringA_R_Ctrl, self.UI.ringB_R_Ctrl, self.UI.ringC_R_Ctrl, self.UI.pinkyA_R_Ctrl, self.UI.pinkyB_R_Ctrl, self.UI.pinkyC_R_Ctrl,
                           self.UI.eq_leftHandCtrl, self.UI.eq_shieldCtrl, self.UI.arm_L_IkFkSwitcher, self.UI.arm_R_IkFkSwitcher, self.UI.leg_L_IkFkSwitcher, self.UI.leg_R_IkFkSwitcher,
                           self.UI.upLeg_L_fkCtrl, self.UI.leg_L_fkCtrl, self.UI.foot_L_fkCtrl, self.UI.toe_L_fkCtrl, self.UI.upLeg_R_fkCtrl, self.UI.leg_R_fkCtrl, self.UI.foot_R_fkCtrl, self.UI.toe_R_fkCtrl,
                           self.UI.upArm_L_fkCtrl, self.UI.arm_L_fkCtrl, self.UI.upArm_R_fkCtrl, self.UI.arm_R_fkCtrl,
                           self.UI.root_mtp_ctrl_09, self.UI.root_mtp_ctrl_08, self.UI.root_mtp_ctrl_07, self.UI.root_mtp_ctrl_06, self.UI.root_mtp_ctrl_05, self.UI.root_mtp_ctrl_04,
                           self.UI.root_mtp_ctrl_03, self.UI.root_mtp_ctrl_02, self.UI.root_mtp_ctrl_01, self.UI.root_mtp_ctrl_00,
                           self.UI.root_mtp_ctrl_19, self.UI.root_mtp_ctrl_18, self.UI.root_mtp_ctrl_17, self.UI.root_mtp_ctrl_16, self.UI.root_mtp_ctrl_15, self.UI.root_mtp_ctrl_14,
                           self.UI.root_mtp_ctrl_13, self.UI.root_mtp_ctrl_12, self.UI.root_mtp_ctrl_11, self.UI.root_mtp_ctrl_10, self.UI.ctrlSet, self.UI.moveCtrl,
                           self.UI.dummt_R_defCtrl, self.UI.dummt_L_defCtrl)

        for object in object_callback:
            # UIファイルの選択ボタンがクリックされていたらmoduleのcallbackへつなぐ、callbackの処理はUIのボタンが押されているかを判定してリグのコントローラーを選択
            # object.clicked.connect(partial(slc.callback, self.UI))
            object.clicked.connect(self.callback)

    def callback(self, *args):
        mc.select(clear=True)
        # GUI上のQPushButtonを検索
        buttons = self.findChildren(QPushButton)
        # リストから選択されているネームスペースを取得
        Nmsp = self.UI.nmspList.currentText()
        Nmsp = Nmsp + ':'
        ctrlList = []
        for i in buttons:
            # QPushButtonがチェックされていたらctrlListへ追加する
            if i.isChecked():
                ctrlList.append(i)
            else:
                pass

        # ctrlListに追加されたQPushButtonのobjectNameからコントローラーを判定
        for node in ctrlList:
            buttons = node.objectName()
            mc.select(Nmsp + buttons, add=True)

    def getNss(self, *args):
        # textScrollListをクリアする
        self.UI.nmspList.clear()

        # referenceTypeをリストアップする
        rn = mc.ls(type='reference')
        # referenceオブジェクトをforで回し":"でスプリットする。
        for i in rn:
            list = i.split(":")
            count = len(list)
            if count == 1:
                for i in list:
                    NSP = i.split("RN")
                    self.UI.nmspList.addItem(NSP[0])
        else:
            pass

    def highLow(self, *args):
        # textScrollListをクリアする
        # normalization
        Nmsp = self.UI.nmspList.currentText()
        Nmsp = Nmsp + ':'
        vals = self.UI.highLowButton.currentIndex()
        if vals == 0:
            mc.setAttr(Nmsp + "displaySet.meshTypeLOD", 0)
        elif vals == 1:
            mc.setAttr(Nmsp + "displaySet.meshTypeLOD", 1)
        else:
            pass

    def load_setting(self):

        setting = QSettings("setting.ini", QSettings.IniFormat)
        # self.ui.saveTest.setText(setting.value(self.ui.saveTest.objectName()))
        self.restoreState(setting.value("windowState"))
        self.restoreGeometry(setting.value("geometry"))

    def closeEvent(self, event):

        setting = QSettings("setting.ini", QSettings.IniFormat)
        # setting.setValue(self.ui.saveTest.objectName(), self.ui.saveTest.text())
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
# GUIの起動


def main():
    QApplication.instance()
    ui = GUI()
    ui.show()
    # sys.exit(app.exec_())
    return ui


if __name__ == '__main__':
    main()
