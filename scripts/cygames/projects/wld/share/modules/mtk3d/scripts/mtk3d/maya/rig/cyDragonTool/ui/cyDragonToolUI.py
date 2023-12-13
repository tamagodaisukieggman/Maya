# -*- coding: utf-8 -*-
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from functools import partial
import maya.cmds as mc
import os
import string
from functools import wraps
import mtk3d.maya.rig.cyDragonTool.module.buttonCallback as callback
import mtk3d.maya.rig.cyDragonTool.module.viewChange as vc
# import cyDragonTool.module.buttonCallback as callback
# import cyDragonTool.module.viewChange as vc
from collections import OrderedDict

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


def undo_redo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        is_error = 0
        mc.undoInfo(ock=1)
        try:
            result = func(*args, **kwargs)
        except Exception:
            is_error = 1
        finally:
            mc.undoInfo(cck=1)
            if is_error:
                raise
            return result

    return wrapper


class DragonTool(MayaQWidgetBaseMixin, QMainWindow):
    def __init__(self, *args, **kwargs):
        super(DragonTool, self).__init__(*args, **kwargs)

        self.window = self.__class__.__name__
        self.setObjectName(self.window)

        uiFile = '{}/dragonToolUI.ui'.format(CURRENT_PATH.translate(string.maketrans('\\', '/')))
        self.ui = self.load_file(uiFile)
        ui_geometry = self.ui.geometry()
        self.setWindowTitle('cyDragonTool')
        self.setGeometry(100, 100, ui_geometry.width(), ui_geometry.height())

        self.get_namespace()
        mc.scriptJob(event=['SceneOpened', self.scenes_open], protected=1)
        self._connect()
        self.rubberBand = None
        self.origin = None

    def load_file(self, ui_file):
        file_ = QFile(ui_file)
        file_.open(QFile.ReadOnly)
        loader = QUiLoader()
        ui = loader.load(file_, self)
        file_.close()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(ui)
        return ui

    def show(self):
        widgets = QApplication.allWidgets()
        for widget in widgets:
            if widget.objectName() == self.window:
                widget.close()
        super(DragonTool, self).show()

    def combobox_act(self):
        self.ui.nmspList.currentText()

    def scenes_open(self):
        self.get_namespace()

    def get_namespace(self):
        self.ui.nmspList.clear()
        rn = mc.ls(type="reference")
        for i in rn:
            split = i.split(":")

            count = len(split)
            if count == 1:
                for i in split:
                    NSP = i.split("RN")
                    if NSP[0]:
                        self.ui.nmspList.addItem(NSP[0])
            else:
                pass

    def _connect(self):
        self.ui.nmspList.activated.connect(self.combobox_act)
        self.ui.FKIKButton.clicked.connect(self.fkik_match)
        self.ui.IKFKButton.clicked.connect(self.fkik_match)
        self.ui.IKFKBakeButton.clicked.connect(self.fk_to_ik_bake)
        self.ui.FKIKBakeButton.clicked.connect(self.fk_to_ik_bake)
        self.ui.selectAllCheck.clicked.connect(partial(callback.selectAllCallback, self.ui))
        handLeg_callback = [self.ui.HandL, self.ui.HandR, self.ui.LegL, self.ui.LegR]
        for h in handLeg_callback:
            h.clicked.connect(partial(callback.selectHandLeg, self.ui))

        self.ui.SetButton.clicked.connect(self.root_set)
        self.ui.BakeButton.clicked.connect(self.root_bake)

        self.ui.translateAllCheck.clicked.connect(partial(callback.translateAllCallback, self.ui))
        tra_callback = [self.ui.translateXCheck, self.ui.translateYCheck, self.ui.translateZCheck]
        for t in tra_callback:
            t.clicked.connect(partial(callback.translateXYZCallback, self.ui))
        self.ui.rotateAllCheck.clicked.connect(partial(callback.rotateAllCallback, self.ui))
        rot_callback = [self.ui.rotateXCheck, self.ui.rotateYCheck, self.ui.rotateZCheck]
        for r in rot_callback:
            r.clicked.connect(partial(callback.rotateXYZCallback, self.ui))
        self.ui.idleModeCheck.clicked.connect(partial(callback.idleModeCallback, self.ui))

    @undo_redo
    def fk_to_ik_bake(self):
        vc.viewChange('start')
        sF = mc.playbackOptions(q=1, minTime=1)
        eF = mc.playbackOptions(q=1, maxTime=1)
        eF = eF + 2

        for j in range(int(sF), int(eF), 1):
            ctrlList = self.fkik_match()
            for i in ctrlList:
                mc.setKeyframe(i)
            mc.currentTime(int(j), e=1)
        vc.viewChange('end')

    @undo_redo
    def fkik_match(self):
        checkBoxAttr = self.get_checkbox_attr()
        checkBoxAttr_text = checkBoxAttr[0].objectName()
        sender_text = self.sender().text()
        return self.ctrl_dictlist(sender_text, checkBoxAttr_text)

    def get_checkbox_attr(self):
        checkBoxList = [self.ui.selectAllCheck, self.ui.HandL, self.ui.HandR, self.ui.LegL, self.ui.LegR]
        ctrlList = [i for i in checkBoxList if i.isChecked() == 1]
        return ctrlList

    def ctrl_dictlist(self, *args):
        sdTxt = args[0]
        cbTxt = args[1]

        ikfkArm = (('arm_ _fkJtProxy', 'arm_ _fkCtrl'), ('hand_ _fkJtProxy', 'hand_ _fkCtrl'),
                   ('handAuxA_ _ikCtrl', 'handAuxA_ _FkCtrl'), ('handAuxB_ _ikCtrl', 'handAuxB_ _FkCtrl'),
                   ('foreArm_ _fkJtProxy', 'foreArm_ _fkCtrl'), ('hand_ _RotBCtrl', 'hand_ _fkRotCtrl'),
                   ('handPinkyB_ _IkCtrl', 'handPinkyB_ _FkCtrl'), ('handRingB_ _IkCtrl', 'handRingB_ _FkCtrl'),
                   ('handMiddleB_ _IkCtrl', 'handMiddleB_ _FkCtrl'), ('handIndexB_ _IkCtrl', 'handIndexB_ _FkCtrl'),
                   ('handPinkyA_ _IkCtrl', 'handPinkyA_ _FkCtrl'), ('handRingA_ _IkCtrl', 'handRingA_ _FkCtrl'),
                   ('handMiddleA_ _IkCtrl', 'handMiddleA_ _FkCtrl'), ('handIndexA_ _IkCtrl', 'handIndexA_ _FkCtrl'),
                   ('handThumbA_ _IkCtrl', 'handThumbA_ _FkCtrl'), ('footF_ _RotCtrl', 'hand_ _fkCtrl'))
        ikvalToFk_arm = OrderedDict(ikfkArm)

        ikfkLeg = (('upLeg_ _fkJtProxy', 'upLeg_ _fkCtrl'), ('foot_ _fkJtProxy', 'foot_ _BFkCtrl'),
                   ('toe_ _fkJtProxy', 'toe_ _BFkCtrl'), ('legAuxA_ _ikCtrl', 'legAuxA_ _FkCtrl'),
                   ('leg_ _fkJtProxy', 'leg_ _fkCtrl'), ('legRingB_ _IkCtrl', 'legRingB_ _FkCtrl'),
                   ('legMiddleB_ _IkCtrl', 'legMiddleB_ _FkCtrl'), ('legIndexB_ _IkCtrl', 'legIndexB_ _FkCtrl'),
                   ('legRingA_ _IkCtrl', 'legRingA_ _FkCtrl'), ('legMiddleA_ _IkCtrl', 'legMiddleA_ _FkCtrl'),
                   ('legIndexA_ _IkCtrl', 'legIndexA_ _FkCtrl'), ('legThumbA_ _IkCtrl', 'legThumbA_ _FkCtrl'),
                   ('toe_ _BCtrl', 'toe_ _BFkCtrl'))
        ikvalToFk_leg = OrderedDict(ikfkLeg)

        fkikArm = (('arm_ _dummyCtrl', 'footF_ _Ctrl'), ('zero', ('hand_ _RotCtrl', 'footF_ _RotCtrl')),
                   ('hand_ _fkCtrl', 'footF_ _RotCtrl'), ('armF_ _dummyCtrl', 'arm_ _BPoleVectorCtrl'),
                   ('handAuxA_ _FkCtrl', 'handAuxA_ _ikCtrl'), ('handAuxB_ _FkCtrl', 'handAuxB_ _ikCtrl'),
                   ('handPinkyA_ _FkCtrl', 'handPinkyA_ _IkCtrl'), ('handPinkyB_ _FkCtrl', 'handPinkyB_ _IkCtrl'),
                   ('handRingA_ _FkCtrl', 'handRingA_ _IkCtrl'), ('handMiddleA_ _FkCtrl', 'handMiddleA_ _IkCtrl'),
                   ('handIndexA_ _FkCtrl', 'handIndexA_ _IkCtrl'), ('handThumbA_ _FkCtrl', 'handThumbA_ _IkCtrl'),
                   ('hand_ _fkRotCtrl', 'hand_ _RotBCtrl'), ('hand_ _fkCtrl', 'footF_ _RotCtrl'))
        fkvalToIk_arm = OrderedDict(fkikArm)

        fkikLeg = (('foot_ _dummyCtrl', 'foot_ _Ctrl'), ('zero', 'leg_ _BCtrl'),
                   ('toe_ _BFkCtrlDummy', 'toe_ _BCtrl'), ('legPoleVec_ _dummyCtrl', 'leg_ _BPoleVectorCtrl'),
                   ('toe_ _BFkCtrl', 'toe_ _BCtrl'), ('legAuxA_ _FkCtrl', 'legAuxA_ _ikCtrl'),
                   ('legAuxB_ _FkCtrl', 'legAuxB_ _ikCtrl'), ('legRingA_ _FkCtrl', 'legRingA_ _IkCtrl'),
                   ('legMiddleA_ _FkCtrl', 'legMiddleA_ _IkCtrl'), ('legIndexA_ _FkCtrl', 'legIndexA_ _IkCtrl'),
                   ('legIndexB_ _FkCtrl', 'legIndexB_ _IkCtrl'), ('legThumbA_ _FkCtrl', 'legThumbA_ _IkCtrl'))
        fkvalToIk_leg = OrderedDict(fkikLeg)

        armList = ikvalToFk_arm if sdTxt == 'ikValue_to_fk' or sdTxt == 'ikValue_to_fkBake' else fkvalToIk_arm
        legList = ikvalToFk_leg if sdTxt == 'ikValue_to_fk' or sdTxt == 'ikValue_to_fkBake' else fkvalToIk_leg

        if cbTxt == 'HandL':
            return self.match(armList, 'L')
        elif cbTxt == 'HandR':
            return self.match(armList, 'R')
        elif cbTxt == 'LegL':
            return self.match(legList, 'L')
        elif cbTxt == 'LegR':
            return self.match(legList, 'R')
        elif cbTxt == 'selectAllCheck':

            a = self.match(armList, 'L')
            b = self.match(armList, 'R')
            c = self.match(legList, 'L')
            d = self.match(legList, 'R')
            return a + b + c + d

    def create_name(self, *args):
        names = self.ui.nmspList.currentText()
        Nmsp = names if names == 1 else names + ''
        Nmsp += ':'
        args_ = args[0]
        direction = args[1]
        ctrlName = args_.translate(string.maketrans(' ', '{}'.format(direction)))
        return Nmsp + ctrlName

    @undo_redo
    def match(self, *args):
        dictList = args[0]
        direction = args[1]

        zero = (0, 0, 0)

        irregularCtrl = ['hand_ _fkRotCtrl', 'hand_ _RotBCtrl']
        irregularAttr = ['footF_ _RotCtrl', 'toe_ _BCtrl', 'hand_ _fkCtrl', 'toe_ _BFkCtrl']
        self.ctrlList = []

        for src, dst in dictList.items():
            if src == 'zero':
                n = len(dst)
                if n == 2:
                    for i in dst:
                        dst = self.create_name(i, direction)
                        mc.setAttr(dst + '.rotate', *zero)
                        self.ctrlList.append(dst)
                else:
                    dst = self.create_name(dst, direction)
                    mc.setAttr(dst + '.rotate', *zero)
                    self.ctrlList.append(dst)

            elif dst in irregularCtrl:
                src = self.create_name(src, direction)
                dst = self.create_name(dst, direction)
                self.ctrlList.append(dst)
                keyableAttr = mc.listAttr(dst, keyable=1)
                for j in keyableAttr:
                    value = mc.getAttr('.'.join([src, j]))
                    mc.setAttr('.'.join([dst, j]), value * -1)
                    self.ctrlList.append(dst)

            elif src in irregularAttr:
                src = self.create_name(src, direction)
                dst = self.create_name(dst, direction)
                spredValue = mc.getAttr(src + '.fingerSpred')
                closeValue = mc.getAttr(src + '.fingerClose')
                mc.setAttr(dst + '.fingerSpred', spredValue)
                mc.setAttr(dst + '.fingerClose', closeValue)
                self.ctrlList.append(dst)

            else:
                src = self.create_name(src, direction)
                dst = self.create_name(dst, direction)
                self.ctrlList.append(dst)
                keyableAttr = mc.listAttr(dst, keyable=1, unlocked=True, visible=True,
                                          connectable=True, scalar=True, write=True, hd=True)
                userDefinedAttr = mc.listAttr(dst, keyable=1, userDefined=True)
                if userDefinedAttr:
                    for i in userDefinedAttr:
                        if i is not None:
                            keyableAttr.remove(i)

                for j in keyableAttr:
                    value = mc.getAttr('.'.join([src, j]))
                    mc.setAttr('.'.join([dst, j]), value)
                    self.ctrlList.append(dst)

        return self.ctrlList

    def root_checkbox_attr(self):
        checkbox_list = [self.ui.translateAllCheck,
                         self.ui.translateXCheck, self.ui.translateYCheck,
                         self.ui.translateZCheck,
                         self.ui.rotateAllCheck,
                         self.ui.rotateXCheck, self.ui.rotateYCheck,
                         self.ui.rotateZCheck]

        ctrl = [obj for obj in checkbox_list if obj.isChecked() == 1]
        ctrl_list = []

        for i in ctrl:
            if i.objectName() == 'translateAllCheck':
                trans_list = ['tx', 'ty', 'tz']
                for j in trans_list:
                    ctrl_list.append(j)
            elif i.objectName() == 'translateXCheck':
                ctrl_list.append('tx')
            elif i.objectName() == 'translateYCheck':
                ctrl_list.append('ty')
            elif i.objectName() == 'translateZCheck':
                ctrl_list.append('tz')
            elif i.objectName() == 'rotateAllCheck':
                rotate_list = ['rx', 'ry', 'rz']
                for j in rotate_list:
                    ctrl_list.append(j)
            elif i.objectName() == 'rotateXCheck':
                ctrl_list.append('rx')
            elif i.objectName() == 'rotateYCheck':
                ctrl_list.append('ry')
            elif i.objectName() == 'rotateZCheck':
                ctrl_list.append('rz')

        return ctrl_list

    @undo_redo
    def root_set(self):
        names = self.ui.nmspList.currentText()
        nmsp = names if names == 1 else names + ''
        nmsp += ':'

        checkbox_attr = self.root_checkbox_attr()

        move_ctrl = 'moveCtrl'
        dum = 'moveCtrlDummySpineAvr'

        self.get_move = mc.xform(nmsp + "moveCtrlDummySpineAvr", q=True, t=True)
        self.get_move_z = self.get_move[2] - 54
        mc.setAttr(nmsp + "moveCtrlDummySpineAvr.tz", self.get_move_z)

        for j in checkbox_attr:
            value = mc.getAttr('.'.join([nmsp + dum, j]))
            mc.setAttr('.'.join([nmsp + move_ctrl, j]), value)
        mc.setAttr(nmsp + "moveCtrlDummySpineAvr.tz", self.get_move[2])

        ctrls = nmsp + move_ctrl
        return ctrls

    def idle_func(self, *args):

        mc.currentTime(args[2])
        ctrls = self.root_set()
        for j in range(int(args[0]), int(args[1] + 2), 1):
            mc.select(ctrls, r=True)
            mc.setKeyframe(ctrls)
            mc.currentTime(int(j), e=True)

    def curve_type_func(self):
        curve_type = self.ui.curveType.currentText()
        return curve_type

    def offset_func(self, *args):
        sf = args[0]
        ef = args[1]
        ef = int(ef)

        offset = args[2]

        offset_start_a = sf + offset + 1
        offset_start_b = sf + offset + offset + 2
        offset_end_a = ef - offset - 1
        offset_end_b = ef - offset - offset - 1

        # startKeyFrame
        mc.currentTime(int(sf), e=True)
        ctrls = self.root_set()
        mc.select(ctrls, r=True)
        mc.setKeyframe(ctrls)

        # 0の状態 startと同じ
        mc.currentTime(int(offset_start_a), e=True)
        mc.setKeyframe(ctrls)

        # end keyframe
        mc.currentTime(int(ef), e=True)
        ctrls = self.root_set()
        mc.select(ctrls, r=True)
        mc.setKeyframe(ctrls)

        mc.keyframe('drg00_999_rig:moveCtrl', t=(ef, ef), timeChange=offset_end_a)

        # end keyframe
        mc.currentTime(int(ef), e=True)
        ctrls = self.root_set()
        mc.select(ctrls, r=True)
        mc.setKeyframe(ctrls)

        for j in range(int(offset_start_b), int(offset_end_b), 1):
            mc.currentTime(int(j), e=True)
            ctrls = self.root_set()
            mc.select(ctrls, r=True)
            mc.setKeyframe(ctrls)
            mc.currentTime(int(j), e=True)

        if self.curve_type_func() == 'Linear':
            mc.cutKey('drg00_999_rig:moveCtrl', t=(offset_start_b, offset_end_b))

    @undo_redo
    def root_bake(self):
        vc.viewChange('start')

        names = self.ui.nmspList.currentText()
        nmsp = names if names == 1 else names + ''
        nmsp += ':'

        sf = mc.playbackOptions(q=1, minTime=1)
        ef = mc.playbackOptions(q=1, maxTime=1)
        # ef = ef + 1

        idle = self.ui.idleModeCheck.isChecked()
        sf_ef = self.ui.useFrame.currentText()

        offset = self.ui.FrameOffsetValue.text()
        offset = float(offset)

        dst = mc.listConnections(nmsp + "moveCtrl", d=0, s=1)
        if dst:
            for i in dst:
                mc.delete(i)
        else:
            pass

        if idle:
            if sf_ef == 'start':
                self.idle_func(sf, ef, sf)
            else:
                self.idle_func(sf, ef, ef)

        else:
            if offset > 0:
                self.offset_func(sf, ef, offset)

            else:
                for j in range(int(sf), int(ef + 1), 1):
                    mc.currentTime(int(j), e=True)
                    ctrls = self.root_set()
                    mc.select(ctrls, r=True)
                    mc.setKeyframe(ctrls)
                    mc.currentTime(int(j), e=True)
                if self.curve_type_func() == 'Linear':
                    mc.cutKey(nmsp + "moveCtrl", t=(sf + 1, ef - 1))

        mc.filterCurve(nmsp + 'moveCtrl')

        vc.viewChange('end')

# GUIの起動


def main():
    QApplication.instance()
    ui = DragonTool()
    ui.show()
    # sys.exit(app.exec_())
    return ui


if __name__ == '__main__':
    main()
