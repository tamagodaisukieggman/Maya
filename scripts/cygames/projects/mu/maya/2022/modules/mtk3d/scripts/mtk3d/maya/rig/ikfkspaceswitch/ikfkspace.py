import os
import os.path
from functools import wraps
# import utils

import maya.cmds as mc
import maya.mel as mm

from .utils.generic import undo

mm.eval("source channelBoxCommand")
dialog = None

import imp

try:
    imp.find_module('PySide2')
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtUiTools import *
    from PySide2.QtWidgets import *

except ImportError:
    from PySide.QtCore import *
    from PySide.QtCore import *
    from PySide.QtUiTools import *

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


# def undo_redo(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         result = None
#         is_error = False
#         mc.undoInfo(ock=True)
#         try:
#             result = func(*args, **kwargs)
#         except Exception:
#             is_error = True
#         finally:
#             mc.undoInfo(cck=True)
#             if is_error:
#                 raise Exception("error.")
#             return result
#
#     return wrapper


class IkToFk(QDialog):
    def __init__(self, parent=None):
        super(IkToFk, self).__init__((parent))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('IkFkMatch UI')
        self.UI = QUiLoader().load(os.path.join(CURRENT_PATH, "ikfkspace.ui"), self)

        # self.setFixedHeight(375)
        # self.setFixedWidth(250)

        file_path = QFile("{}/stylesheets/scheme.qss".format(CURRENT_PATH))
        file_path.open(QFile.ReadOnly | QFile.Text)
        self.stream = QTextStream(file_path)
        self.setStyleSheet(self.stream.readAll())
        file_path.close()

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(0)
        self.layout().setAlignment(Qt.AlignTop)

        self.layout().addWidget(self.UI)

        self._get_namespace()
        self._connect()
        self._createjob()

    def _scenes_open(self):
        self._get_namespace()

    def _createjob(self):
        mc.scriptJob(event=['SceneOpened', self._scenes_open], protected=True)

    def _get_namespace(self):
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

    def _namespace(self):
        ns = self.UI.nmspList.currentText()
        return ns

    def _connect(self):
        self.UI.iktofk_bake.clicked.connect(self.iktofk)
        self.UI.fktoik_bake.clicked.connect(self.fktoik)
        self.UI.selectAll.clicked.connect(self._callback)
        self.UI.switchspace.clicked.connect(self.switchspace)

    def _callback(self):
        buttons = [self.UI.armL, self.UI.armR, self.UI.legL, self.UI.legR]
        if self.UI.selectAll.isChecked():
            for btn in buttons:
                btn.setEnabled(False)
                btn.setChecked(False)

        else:
            for btn in buttons:
                btn.setEnabled(True)
            self.UI.armL.setChecked(True)

    def _callback_control_name(self, *args):
        nmsp = self.UI.nmspList.currentText()
        for obj in args:
            if mc.objExists(nmsp + ":" + obj):
                return obj

    def _controls(self):

        # controllers
        self.controls = []
        self.ik_space = []
        self.switch = []

        # Controller and associated data
        self.fk = {}
        self.ik = {}
        self.baked = {}
        self.hoof_baked = {}
        self.pv = {}
        self.proxy = {}
        self.hoof_fk = {}
        self.hoof_ik = {}
        self.hoof_proxy = {}

        # -------------------------------------------------------------------------------------------------------------#
        # Assigning a controller name

        arm_L = self._callback_control_name("hand_L_01_ctrl", "hand_L_ctrl")
        arm_L_pv = self._callback_control_name("elbow_L_pv_ctrl", "arm_L_pv_ctrl")
        arm_L_org = self._callback_control_name("arm_L_org_locShape")

        arm_R = self._callback_control_name("hand_R_01_ctrl", "hand_R_ctrl")
        arm_R_pv = self._callback_control_name("elbow_R_pv_ctrl", "arm_R_pv_ctrl")
        arm_R_org = self._callback_control_name("arm_R_org_locShape")

        foot_L = self._callback_control_name("foot_L_01_ctrl")
        foot_L_pv = self._callback_control_name("knee_L_pv_ctrl")
        foot_L_org = self._callback_control_name("leg_L_org_locShape")

        foot_R = self._callback_control_name("foot_R_01_ctrl")
        foot_R_pv = self._callback_control_name("knee_R_pv_ctrl")
        foot_R_org = self._callback_control_name("leg_R_org_locShape")

        # -------------------------------------------------------------------------------------------------------------#
        if self.UI.selectAll.isChecked():
            [self.controls.append(x) for x in [arm_L, arm_R, foot_L, foot_R]]
            self.ik_space.append([arm_L, arm_R, foot_L, foot_R,
                                  arm_L_pv, arm_R_pv, foot_L_pv, foot_R_pv])
            self.switch.append([arm_L_org, arm_R_org, foot_L_org, foot_R_org])

        # -------------------------------------------------------------------------------------------------------------#
        if self.UI.armL.isChecked():
            self.controls.append(arm_L)
            self.ik_space.append([arm_L, arm_L_pv])
            self.switch.append([arm_L_org])

        # -------------------------------------------------------------------------------------------------------------#
        if self.UI.armR.isChecked():
            self.controls.append(arm_R)
            self.ik_space.append([arm_R, arm_R_pv])
            self.switch.append([arm_R_org])

        # -------------------------------------------------------------------------------------------------------------#
        if self.UI.legL.isChecked():
            self.controls.append(foot_L)
            self.ik_space.append([foot_L, foot_L_pv])
            self.switch.append([foot_L_org])

        # -------------------------------------------------------------------------------------------------------------#
        if self.UI.legR.isChecked():
            self.controls.append(foot_R)
            self.ik_space.append([foot_R, foot_R_pv])
            self.switch.append([foot_R_org])

        # -------------------------------------------------------------------------------------------------------------#
        # set the name space

        self.controls = map(lambda x: self._namespace() + ":" + x, self.controls)
        self.ik_space = map(lambda x: self._namespace() + ":" + x, sum(self.ik_space, []))
        self.switch = map(lambda x: self._namespace() + ":" + x, sum(self.switch, []))

        # -------------------------------------------------------------------------------------------------------------#

        for control in self.controls:

            self.fk[control] = []
            self.ik[control] = []
            self.pv[control] = []
            self.proxy[control] = []
            self.hoof_fk[control] = []
            self.hoof_ik[control] = []
            self.hoof_proxy[control] = []

            for i in range(1, 5):

                na = control + ".fk" + str(i)
                if mc.objExists(na):
                    self.fk[control].insert(0, mc.listConnections(na, s=False, d=True)[0])

                na = control + ".ik" + str(i)
                if mc.objExists(na):
                    self.ik[control].insert(0, mc.listConnections(na, s=False, d=True)[0])

                na = control + ".pv_dummy" + str(i)
                if mc.objExists(na):
                    self.pv[control].insert(0, mc.listConnections(na, s=False, d=True)[0])

                na = control + ".proxy" + str(i)
                if mc.objExists(na):
                    self.proxy[control].insert(0, mc.listConnections(na, s=False, d=True)[0])

                na = control + ".hoof_fk"
                if mc.objExists(na):
                    self.hoof_fk[control].insert(0, mc.listConnections(na, s=False, d=True)[0])

                na = control + ".hoof_ik1"
                if mc.objExists(na):
                    self.hoof_ik[control].insert(0, mc.listConnections(na, s=False, d=True)[0])

                na = control + ".hoof_ik2"
                if mc.objExists(na):
                    self.hoof_ik[control].insert(0, mc.listConnections(na, s=False, d=True)[0])

                na = control + ".hoof_proxy"
                if mc.objExists(na):
                    self.hoof_proxy[control].insert(0, mc.listConnections(na, s=False, d=True)[0])

            self.ik[control].insert(0, control)
            self.baked[control] = []
            self.hoof_baked[control] = []

    def _setvalue_zero(self, obj, attrs, dc=False):
        """
        :type dc: object
        """
        for attr in attrs:
            if dc:
                mm.eval("CBdeleteConnection " + obj + "." + attr)
            else:
                pass
            try:
                mc.setAttr(obj + "." + attr, 0)
            except:
                pass

    def _get_timerange(self, startFrame=None, endFrame=None):
        if startFrame is None:
            if mm.eval("timeControl -q -rv $gPlayBackSlider"):
                startFrame = mm.eval("timeControl -q -ra $gPlayBackSlider")[0]
            else:
                startFrame = mc.playbackOptions(q=True, min=True)

        if endFrame is None:
            if mm.eval("timeControl -q -rv $gPlayBackSlider"):
                endFrame = mm.eval("timeControl -q -ra $gPlayBackSlider")[1]
            else:
                endFrame = mc.playbackOptions(q=True, max=True)

        return startFrame, endFrame

    def _get_module_type(self, control):
        na = control + ".module_type"
        if mc.objExists(na):
            mt = mc.getAttr(na)
            return mt

    def check_autoKeyframe(self):
        ak = mc.autoKeyframe(st=True, q=True)
        return ak

    def autokeyframe_off(self):
        mc.autoKeyframe(st=False)

    def autokeyframe_on(self):
        mc.autoKeyframe(st=True)

    @undo
    def iktofk(self, startFrame=None, endFrame=None):
        mc.undoInfo(ock=True)

        mc.refresh(su=True)
        self._controls()

        # -------------------------------------------------------------------------------------------------------------#
        # check autoKeyframe
        ak = mc.autoKeyframe(st=True, q=True)
        autoKey = None
        if ak:
            mc.autoKeyframe(st=False)
            autoKey = "ak"

        # -------------------------------------------------------------------------------------------------------------#
        # If there is a key in the attribute of fkikSwitch, delete it and set the value to 0
        print(list(self.switch))
        swt = list(self.switch)
        num = len(swt)
        print(num)
        for i in range(num):
            print(i)
            self._setvalue_zero(swt[i], ["ikFkSwitch"], dc=True)

        # -------------------------------------------------------------------------------------------------------------#
        # make fk control dummy and constraint fk , add baked list
        print(self.fk.keys())
        for control in self.fk.keys():
            for i in range(len(self.fk[control])):
                n = mc.createNode("transform")
                mc.parentConstraint(self.fk[control][i], n)
                self.baked[control].append(n)

        val = self.hoof_fk.values()
        if not val:
            for control in self.hoof_fk.keys():
                hn = mc.createNode("transform")
                mc.parentConstraint(self.hoof_fk[control][0], hn)
                self.hoof_baked[control].append(hn)
                # print(self.hoof_baked[control])

        # -------------------------------------------------------------------------------------------------------------#
        # set start and end range
        timerange = self._get_timerange(startFrame, endFrame)

        # -------------------------------------------------------------------------------------------------------------#
        # bake dummy controller
        mc.bakeResults(sum(self.baked.values(), []), t=(timerange[0], timerange[1]), sm=True,
                       at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

        if not val:
            mc.bakeResults(sum(self.hoof_baked.values(), []), t=(timerange[0], timerange[1]), sm=True,
                           at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

        # -------------------------------------------------------------------------------------------------------------#
        # Set the space value of ik controller to local
        spc = list(self.ik_space)
        num = len(spc)
        print(num)
        for i in range(num):
            self._setvalue_zero(spc[i], ["space"], dc=True)

        # -------------------------------------------------------------------------------------------------------------#
        # Set the value of fk controller to 0
        for n in sum(self.fk.values(), []):
            self._setvalue_zero(n, ["r", "rx", "ry", "rz"], dc=False)

        if not val:
            for n in sum(self.hoof_fk.values(), []):
                self._setvalue_zero(n, ["r", "rx", "ry", "rz"], dc=False)

        # -------------------------------------------------------------------------------------------------------------#
        # here ik ctrl set 0 value
        for l in self.ik.values():
            for i in range(len(l)):
                self._setvalue_zero(l[i], ["tx", "ty", "tz", "rx", "ry", "rz"], dc=True)

        if not val:
            for l in self.hoof_ik.values():
                for i in range(len(l)):
                    print(l[i])
                    self._setvalue_zero(l[i], ["tx", "ty", "tz", "rx", "ry", "rz"], dc=True)

        # -------------------------------------------------------------------------------------------------------------#
        # Create empty node to match ik controller to self.fk
        for control in self.fk.keys():

            # check the controller type
            module_type = self._get_module_type(control)

            # type arm

            if module_type == "arm":
                n = mc.createNode("transform")
                mc.delete(mc.parentConstraint(self.fk[control][0], n))

                # Align ik controller with animated fk controller
                mc.parentConstraint(n, control, mo=True)
                n1 = mc.parent(n, self.baked[control][0])[0]

                # Constrain shoulder rot control
                if len(self.ik[control]) > 2:
                    n = mc.createNode("transform")
                    mc.delete(mc.parentConstraint(self.fk[control][3], n))
                    mc.orientConstraint(n, self.ik[control][1], mo=True)
                    n2 = mc.parent(n, self.baked[control][3])[0]
                else:
                    n2 = None

                self._setvalue_zero(n1, ["tx", "ty", "tz", "rx", "ry", "rz"])
                if n2:
                    self._setvalue_zero(n2, ["r", "rx", "ry", "rz"])

                # -----------------------------------------------------------------------------------------------------#
                # Align ik pv controller with animated fk controller
                for control in self.fk.keys():
                    try:
                        mc.pointConstraint(self.pv[control][0], self.ik[control][2])
                    except:
                        pass

            # ---------------------------------------------------------------------------------------------------------#
            # four joint leg
            elif module_type == "quadruped_leg":
                n = mc.createNode("transform")
                mc.delete(mc.parentConstraint(self.fk[control][0], n))

                # Align ik controller with animated fk controller
                mc.parentConstraint(n, control, mo=True)
                n1 = mc.parent(n, self.baked[control][0])[0]

                # Constrain knee rot control
                if len(self.ik[control]) > 2:
                    n = mc.createNode("transform")
                    mc.delete(mc.parentConstraint(self.fk[control][1], n))
                    mc.orientConstraint(n, self.ik[control][3], mo=True)
                    n2 = mc.parent(n, self.baked[control][1])[0]

                else:
                    n2 = None

                if not val:
                    n = mc.createNode("transform")
                    mc.delete(mc.parentConstraint(self.hoof_fk[control], n))
                    mc.orientConstraint(n, self.hoof_ik[control][1], mo=True)
                    n3 = mc.parent(n, self.hoof_baked[control][0])[0]
                else:
                    n3 = None

                self._setvalue_zero(n1, ["tx", "ty", "tz", "rx", "ry", "rz"])
                if n2:
                    self._setvalue_zero(n2, ["r", "rx", "ry", "rz"])
                if n3:
                    self._setvalue_zero(n3, ["tx", "ty", "tz", "r", "rx", "ry", "rz"])

                # -----------------------------------------------------------------------------------------------------#
                # Align ik pv controller with animated fk controller
                for control in self.fk.keys():
                    try:
                        mc.pointConstraint(self.pv[control][0], self.ik[control][1])
                    except:
                        pass
            else:
                pass

        # -------------------------------------------------------------------------------------------------------------#
        mc.bakeResults(sum(self.ik.values(), []), t=(timerange[0], timerange[1]), sm=True,
                       at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

        if not val:
            mc.bakeResults(sum(self.hoof_ik.values(), []), t=(timerange[0], timerange[1]), sm=True,
                           at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

        # -------------------------------------------------------------------------------------------------------------#
        # bake ik controller

        mc.delete(sum(self.baked.values(), []))
        if not val:
            mc.delete(sum(self.hoof_baked.values(), []))
        [mc.setAttr("{}".format(x) + ".ikFkSwitch", 1) for x in self.switch]

        if not autoKey is None:
            mc.autoKeyframe(st=True)

        mc.refresh(su=False)
        mc.undoInfo(cck=True)

    @undo
    def fktoik(self, startFrame=None, endFrame=None):
        mc.undoInfo(ock=True)
        mc.refresh(su=True)
        self._controls()

        # -------------------------------------------------------------------------------------------------------------#
        # set ikFkSwitch value to 1
        for control in self.switch:
            for a in ["ikFkSwitch"]:
                mm.eval("CBdeleteConnection " + control + "." + a)
                try:
                    mc.setAttr(control + "." + a, 1)
                except:
                    pass

        # -------------------------------------------------------------------------------------------------------------#
        # set start and end range
        timerange = self._get_timerange(startFrame, endFrame)

        # -------------------------------------------------------------------------------------------------------------#
        # Bind an empty node to a proxy controller and bake
        del_const = []
        for control in self.fk.keys():
            for i in range(len(self.fk[control])):
                n = mc.createNode("transform")
                del_const.append(mc.parentConstraint(self.proxy[control][i], n)[0])
                self.baked[control].append(n)

        val = self.hoof_fk.values()
        if not val:
            for control in self.hoof_fk.keys():
                n = mc.createNode("transform")
                del_const.append(mc.parentConstraint(self.hoof_proxy[control][0], n)[0])
                self.hoof_baked[control].append(n)

        mc.bakeResults(sum(self.baked.values(), []), t=(timerange[0], timerange[1]), sm=True,
                       at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

        # if self.hoof_fk:
        if not val:
            mc.bakeResults(sum(self.hoof_baked.values(), []), t=(timerange[0], timerange[1]), sm=True,
                           at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

        mc.delete(del_const)

        # -------------------------------------------------------------------------------------------------------------#
        del_const = []
        for control in self.fk.keys():
            for i in range(len(self.fk[control]))[::-1]:
                del_const.append(mc.orientConstraint(self.baked[control][i], self.fk[control][i])[0])

        # if self.hoof_fk:
        if not val:
            for control in self.hoof_fk.keys():
                del_const.append(mc.orientConstraint(self.hoof_baked[control][i], self.hoof_fk[control][0])[0])

        mc.bakeResults(sum(self.fk.values(), []), t=(timerange[0], timerange[1]), sm=True,
                       at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

        # if self.hoof_fk:
        if not val:
            mc.bakeResults(sum(self.hoof_fk.values(), []), t=(timerange[0], timerange[1]), sm=True,
                           at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

        mc.delete(del_const)
        mc.delete(sum(self.baked.values(), []))

        # if self.hoof_fk:
        if not val:
            mc.delete(sum(self.hoof_baked.values(), []))

        [mc.setAttr("{}".format(x) + ".ikFkSwitch", 0) for x in self.switch]

        mc.refresh(su=False)
        mc.undoInfo(cck=True)

    @undo
    def switchspace(self, startFrame=None, endFrame=None, replace=False):
        controls = mc.ls(sl=True)
        space = self.UI.space.currentText()

        mc.refresh(su=True)


        try:
            if startFrame is None:
                if mm.eval("timeControl -q -rv $gPlayBackSlider"):
                    startFrame = mm.eval("timeControl -q -ra $gPlayBackSlider")[0]
                else:
                    startFrame = mc.playbackOptions(q=True, min=True)
            if endFrame is None:
                if mm.eval("timeControl -q -rv $gPlayBackSlider"):
                    endFrame = mm.eval("timeControl -q -ra $gPlayBackSlider")[1]
                else:
                    endFrame = mc.playbackOptions(q=True, max=True)

            if not replace:
                mc.selectKey(controls, k=True, t=(-999999999, startFrame - 1))
                mc.selectKey(controls, k=True, t=(endFrame + 1, 999999999), add=True)
                mc.copyKey(an="keys")

            baked = {}
            for control in controls:
                if not mc.objExists(control + ".space"): continue
                spaces = mc.attributeQuery("space", node=control, le=True)[0].split(":")
                if space not in spaces: continue
                currentSpaceId = mc.getAttr(control + ".space")
                if spaces[currentSpaceId] == space: continue
                baked[control] = mc.createNode("transform", ss=True)
                mc.parentConstraint(control, baked[control])

            vals = list(baked.values())
            mc.bakeResults(vals, t=(startFrame, endFrame), sm=True,
                           at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

            for control in baked.keys():
                spaces = mc.attributeQuery("space", node=control, le=True)[0].split(":")
                currentSpaceId = mc.getAttr(control + ".space")
                for i in range(len(spaces)):
                    if spaces[i] == space:
                        newSpaceId = i
                        break
                mc.setKeyframe(control + ".space", v=currentSpaceId, t=startFrame - 1)
                mc.setKeyframe(control + ".space", v=newSpaceId, t=startFrame)
                for a in ["t", "tx", "ty", "tz", "r", "rx", "ry", "rz", "space"]:
                    mm.eval("CBdeleteConnection " + control + "." + a)
                    try:
                        mc.setAttr(control + "." + a, 0)
                    except:
                        pass

            constraints = []
            for control in controls:
                for i in range(len(spaces)):
                    if space == spaces[i]:
                        mc.setAttr(control + ".space", i)
                        break
                try:
                    constraints.append(mc.parentConstraint(baked[control], control)[0])
                except:
                    try:
                        constraints.append(mc.pointConstraint(baked[control], control)[0])
                    except:
                        try:
                            constraints.append(mc.orientConstraint(baked[control], control)[0])
                        except:
                            pass

            mc.bakeResults(controls, t=(startFrame, endFrame), sm=True,
                           at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])
            mc.delete(constraints, vals)

            if not replace: mc.pasteKey(controls, o="merge", cp=1, c=False, to=0, fo=0, vo=0)
        except:
            pass

        mc.refresh(su=False)

        mc.select(controls)


def main():
    global dialog
    if dialog is None:
        dialog = IkToFk()
    dialog.show()


def delete():
    global dialog
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None


if __name__ == '__main__':
    main()
