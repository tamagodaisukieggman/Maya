import glob
import json
import os
import os.path
from functools import wraps

import maya.cmds as mc
import maya.mel as mm

mm.eval("source channelBoxCommand")

dialog = None

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


def undo_redo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        is_error = False
        mc.undoInfo(ock=True)
        try:
            result = func(*args, **kwargs)
        except Exception:
            is_error = True
        finally:
            mc.undoInfo(cck=True)
            if is_error:
                raise ValueError  # shorthand for 'raise ValueError()'
            return result

    return wrapper


class WaitPoseMatch(MayaQWidgetBaseMixin, QMainWindow):
    MaxRecentFiles = 3

    def __init__(self, parent=None):
        super(WaitPoseMatch, self).__init__(parent)
        self.recentFileActs = []
        self.window = self.__class__.__name__
        self.setObjectName(self.window)

        widgets = QApplication.allWidgets()
        for widget in widgets:
            if widget.objectName() == self.window:
                widget.close()

        loader = QUiLoader()
        uiFilePath = os.path.join(CURRENT_PATH, 'waitPoseMatchUtilUI.ui')
        self.UI = loader.load(uiFilePath)
        self.setCentralWidget(self.UI)

        self.setWindowTitle('Wait Pose Match Utility ')
        self._getNameSpace()
        self.createActions()
        self._connect()

        # -------------------------------------------------------------------------------------------------------------#
        nmsp = self.get_nameSpace()

        # set locator name
        self.hip_loc = "hip_loc"
        self.cog_loc = "cog_loc"
        self.spine_loc = "spine_loc"
        self.main_offset_loc = "main_offset_loc"
        self.main_loc = "main_loc"
        self.move_loc = "move_loc"
        self.move_offset_loc = "move_offset_loc"

        # -------------------------------------------------------------------------------------------------------------#
        # set controller name
        self.spine_01_fk_ctrl = nmsp + ":" + "spine_01_fk_ctrl"
        self.pelvis_fk_ctrl = nmsp + ":" + "pelvis_fk_ctrl"
        self.pelvis_ctrl = nmsp + ":" + "pelvis_ctrl"
        self.main_ctrl = nmsp + ":" + "main_ctrl"
        self.main_offset = nmsp + ":" + "main_offset"
        self.move_ctrl = nmsp + ":" + "move_ctrl"

        # -------------------------------------------------------------------------------------------------------------#
        # set pose directory
        self._createJob()
        self._load_setting()

    def _connect(self):
        # -------------------------------------------------------------------------------------------------------------#
        # make locator/ attach locator
        self.UI.make_locator.clicked.connect(self._make_locatror)
        self.UI.match_pose.clicked.connect(self.matchPose)
        self.UI.pose_directory.editingFinished.connect(self._add_file_to_list)
        self.UI.pose_directory.textChanged.connect(self._add_file_to_list)

        # -------------------------------------------------------------------------------------------------------------#
        # import/ export
        self.UI.export_button.clicked.connect(self._export_value)
        self.UI.import_button.clicked.connect(self._import_value)

        # -------------------------------------------------------------------------------------------------------------#
        # pop up
        self.popMenu = QMenu(self)
        self.recent = QMenu("Recent Directories")
        self.popMenu.addMenu(self.recent)
        self.popMenu.addSeparator()

        setting = QSettings("setting.ini", QSettings.IniFormat)
        filePath = setting.value(self.UI.pose_directory.objectName())

        for i in range(WaitPoseMatch.MaxRecentFiles):
            self.recent.addAction(self.recentFileActs[i])

        self.popMenu.addSeparator()
        self.popMenu.addAction(self.openAct)
        self.UI.set_directory.setMenu(self.popMenu)

    def createActions(self):
        # action
        self.openAct = QAction("&Open...", self,
                               statusTip="Open an existing file",
                               triggered=self._open_directory)

        for i in range(WaitPoseMatch.MaxRecentFiles):
            self.recentFileActs.append(
                QAction(self, visible=False,
                        triggered=self.openRecentFile))

    def openRecentFile(self):
        action = self.sender
        if action:
            self.UI.pose_directory.setText(action().text())

    def _open_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Open Directory', os.path.expanduser('~'))
        self.UI.pose_directory.setText(dir_path)

        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])
        try:
            files.remove(dir_path)
        except ValueError:
            pass

        files.insert(0, dir_path)
        del files[WaitPoseMatch.MaxRecentFiles:]

        settings.setValue('recentFileList', files)

        files_no = 0
        if files:
            files_no = len(files)

        numRecentFiles = min(files_no, WaitPoseMatch.MaxRecentFiles)

        for i in range(numRecentFiles):
            self.recentFileActs[i].setText(files[i])
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

    def setCurrentFile(self, fileName):
        self.curFile = fileName

        settings = QSettings('Trolltech', 'Recent Files Example')
        files = list(settings.value('recentFileList', []))

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[MainWindow.MaxRecentFiles:]

        settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.updateRecentFileActions()

    def _clickedCallback(self):
        sender = self.sender().text()

    def _createJob(self):
        mc.scriptJob(event=['SceneOpened', self._scenesOpen], protected=True)

    def _scenesOpen(self):
        self._getNameSpace()

    def _closeEvent(self, event):

        setting = QSettings("setting.ini", QSettings.IniFormat)
        setting.setValue(self.UI.pose_directory.objectName(), self.UI.pose_directory.text())
        setting.setValue("windowState", self.saveState())
        setting.setValue("geometry", self.saveGeometry())

    def _load_setting(self):
        setting = QSettings("setting.ini", QSettings.IniFormat)
        self.UI.pose_directory.setText(setting.value(self.UI.pose_directory.objectName()))
        self.restoreState(setting.value("windowState"))
        self.restoreGeometry(setting.value("geometry"))

    def _getNameSpace(self):
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

    def _add_file_to_list(self):
        self.UI.import_list.clear()
        self.UI.export_list.clear()

        filePath = self.UI.pose_directory.text()
        filePath = glob.glob("{}/*".format(filePath))

        for fl in filePath:
            path = os.path.split(fl)
            ext = os.path.splitext(path[1])
            if ext[1] == ".json":
                ext = ["{}".format(ext[0])]
                self.UI.import_list.addItems(ext)
                self.UI.export_list.addItems(ext)

    def _getAttrKey(self, obj):
        at = [''] * 9
        t = mc.currentTime(q=True)

        at[0] = round(mc.getAttr(obj + '.tx', t=t), 5)
        at[1] = round(mc.getAttr(obj + '.ty', t=t), 5)
        at[2] = round(mc.getAttr(obj + '.tz', t=t), 5)
        at[3] = round(mc.getAttr(obj + '.rx', t=t), 5)
        at[4] = round(mc.getAttr(obj + '.ry', t=t), 5)
        at[5] = round(mc.getAttr(obj + '.rz', t=t), 5)
        at[6] = round(mc.getAttr(obj + '.sx', t=t), 5)
        at[7] = round(mc.getAttr(obj + '.sy', t=t), 5)
        at[8] = round(mc.getAttr(obj + '.sz', t=t), 5)

        attrs = ''
        for a in at:
            attrs = '%s%s%s' % (attrs, a, ',')

        return attrs

    def get_nameSpace(self):
        nmsp = self.UI.nmspList.currentText()
        return nmsp

    @undo_redo
    def _make_locatror(self):
        # -------------------------------------------------------------------------------------------------------------#
        # check old locater
        if mc.objExists(self.hip_loc):
            mc.delete(self.hip_loc)

        if mc.objExists(self.main_offset_loc):
            mc.delete(self.main_offset_loc)

        # -------------------------------------------------------------------------------------------------------------#
        # set locator name and parent
        mc.spaceLocator(n=self.cog_loc)
        mc.spaceLocator(n=self.hip_loc)
        mc.spaceLocator(n=self.spine_loc)

        mc.parent(self.cog_loc, self.hip_loc)
        mc.parent(self.spine_loc, self.hip_loc)

        # -------------------------------------------------------------------------------------------------------------#
        # make constraint and set delete list 
        del_list = [mc.parentConstraint(self.pelvis_ctrl, self.cog_loc)[0],
                    mc.parentConstraint(self.pelvis_fk_ctrl, self.hip_loc)[0],
                    mc.parentConstraint(self.spine_01_fk_ctrl, self.spine_loc)[0]]

        # -------------------------------------------------------------------------------------------------------------#
        # make dummy locator set
        if not mc.objExists("dummyLocSet"):
            ss = mc.sets(n="dummyLocSet", em=True)

        mc.connectAttr(self.cog_loc + ".message", ss + ".dnSetMembers", na=True)
        mc.connectAttr(self.hip_loc + ".message", ss + ".dnSetMembers", na=True)
        mc.connectAttr(self.spine_loc + ".message", ss + ".dnSetMembers", na=True)

        # -------------------------------------------------------------------------------------------------------------#
        # make and set export file name
        sceneName = mc.file(q=True, sceneName=True, shortName=True)
        sceneName = sceneName.split(".")
        poseListName = '{}_{}f'.format(sceneName[0], mc.currentTime(q=True))
        self.UI.export_name.setText(poseListName)

        # -------------------------------------------------------------------------------------------------------------#
        # make main locator and offset locator
        if self.UI.match_main.isChecked():
            self.check(loc=self.main_loc, loc_offset=self.main_offset_loc, base=self.pelvis_ctrl,ctrl=self.main_ctrl)

        # -------------------------------------------------------------------------------------------------------------#
        # make main locator and offset locator
        if self.UI.match_move.isChecked():
            self.check(loc=self.move_loc, loc_offset=self.move_offset_loc, base=self.pelvis_ctrl,ctrl=self.move_ctrl)

        mc.delete(del_list)

    def check(self, loc, loc_offset, base, ctrl):

        if mc.objExists(loc):
            mc.delete(loc)
        else:
            pass

        mc.spaceLocator(n=loc_offset)
        mc.spaceLocator(n=loc)

        mc.delete(mc.pointConstraint(base, loc_offset, skip=["y"]))
        mc.delete(mc.orientConstraint(base, loc_offset))

        mc.delete(mc.pointConstraint(ctrl, loc, skip=["y"]))
        mc.delete(mc.orientConstraint(ctrl, loc, skip=["x", "z"]))

        mc.parent(loc, loc_offset)

    def _break_connection(self):
        hip = mc.listConnections(self.hip_loc, d=True, type="parentConstraint")
        if hip:
            mc.delete(hip)
        hip = mc.listConnections(self.hip_loc, d=True, type="orientConstraint")
        if hip:
            mc.delete(hip)
        cog = mc.listConnections(self.cog_loc, d=True, type="parentConstraint")
        if cog:
            mc.delete(cog)
        spine = mc.listConnections(self.spine_loc, d=True, type="orientConstraint")
        if spine:
            mc.delete(spine)

    @undo_redo
    def matchPose(self):

        # -------------------------------------------------------------------------------------------------------------#
        attrs = ["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"]

        ctrls = [self.pelvis_fk_ctrl, self.spine_loc, self.hip_loc, self.cog_loc]

        # -------------------------------------------------------------------------------------------------------------#
        # Align the locator position to the controller position
        mc.delete(mc.parentConstraint(self.pelvis_fk_ctrl, self.hip_loc))
        mc.orientConstraint(self.spine_loc, self.spine_01_fk_ctrl)
        mc.orientConstraint(self.hip_loc, self.pelvis_fk_ctrl)
        mc.parentConstraint(self.cog_loc, self.pelvis_ctrl)

        # -------------------------------------------------------------------------------------------------------------#
        # Set keys for attributes
        for control in ctrls:
            for attr in attrs:
                try:
                    mc.setKeyframe(control, attribute=attr)
                except:
                    pass

        mc.delete(self.hip_loc)
        # -------------------------------------------------------------------------------------------------------------#
        # Processing when main locator exists

        if mc.objExists(self.main_offset_loc):
            ctrls = [self.main_ctrl, self.move_ctrl, self.pelvis_ctrl]

            # Create a dummy transform to move only main_ctrl and temporarily restrain it
            dummy_trans = mc.createNode("transform")
            mc.parentConstraint(dummy_trans, self.pelvis_ctrl, mo=True)

            # ---------------------------------------------------------------------------------------------------------#
            # match main_loc
            mc.delete(mc.pointConstraint(self.pelvis_ctrl, self.main_offset_loc, skip=["y"]))
            mc.delete(mc.orientConstraint(self.pelvis_ctrl, self.main_offset_loc))

            # Align main_ctrl with main_loc
            mc.parentConstraint(self.main_loc, self.main_ctrl)

            # Align move_ctrl with move_loc
            mc.parentConstraint(self.move_loc, self.move_ctrl)

            # ---------------------------------------------------------------------------------------------------------#
            # Set keys for attributes
            for control in ctrls:
                for attr in attrs:
                    try:
                        mc.setKeyframe(control, attribute=attr)
                    except:
                        pass

            mc.delete(self.main_offset_loc, self.move_offset_loc)
            mc.delete(dummy_trans)

    @undo_redo
    def _export_value(self):
        # export json
        filePath = self.UI.pose_directory.text()
        exportName = self.UI.export_name.text()

        poses = [[]]
        del poses[0]

        loc_list = [self.cog_loc, self.hip_loc, self.spine_loc, self.main_offset_loc, self.main_loc, self.move_loc]
        selObjs = mc.ls(loc_list, long=True)

        # number of locator
        datas = '{},'.format(len(selObjs))

        for obj in selObjs:
            datas = '{}{}'.format(datas, obj + ',')
            datas = '{}{}'.format(datas, self._getAttrKey(obj))

        poses.append([exportName, datas])

        dict(poses)

        # filePath = "z:/mtk/work/resources/animations/clips/boss/bos00/pose/"
        # exportName = "loc_pose"
        f = filePath + "/" + exportName + ".json"
        fp = open(f, 'w')

        # Convert list to dictionary and save in Json format
        dictPoses = dict(poses)
        json.dump(dictPoses, fp, ensure_ascii=False, indent=4)

        self._add_file_to_list()

    @undo_redo
    def _import_value(self, *args):
        self._break_connection()
        filePath = self.UI.pose_directory.text()
        importName = self.UI.import_list.currentItem().text()
        f = filePath + "/" + importName + ".json"
        fp = open(f, 'r')

        jsonData = json.load(fp)
        tempPoses = jsonData.items()
        for i in range(len(tempPoses)):
            tempPoses[i] = list(tempPoses[i])

        paramList = tempPoses[0][1].split(',')
        tempParamList = paramList
        count = int(tempParamList[0])

        del tempParamList[0]

        for i in range(count):
            obj = tempParamList[0]
            txa = float(tempParamList[1])
            tya = float(tempParamList[2])
            tza = float(tempParamList[3])
            rxa = float(tempParamList[4])
            rya = float(tempParamList[5])
            rza = float(tempParamList[6])
            sxa = float(tempParamList[7])
            sya = float(tempParamList[8])
            sza = float(tempParamList[9])

            del tempParamList[0:10]

            try:
                mc.setAttr(obj + '.tx', txa)
                # mc.setKeyframe(obj, at='tx', v=txa)
            except:
                pass

            try:
                mc.setAttr(obj + '.ty', tya)
                # mc.setKeyframe(obj, at='ty', v=tya)
            except:
                pass

            try:
                mc.setAttr(obj + '.tz', tza)
                # mc.setKeyframe(obj, at='tz', v=tza)
            except:
                pass

            try:
                mc.setAttr(obj + '.rx', rxa)
                # mc.setKeyframe(obj, at='rx', v=rxa)
            except:
                pass

            try:
                mc.setAttr(obj + '.ry', rya)
                # mc.setKeyframe(obj, at='ry', v=rya)
            except:
                pass

            try:
                mc.setAttr(obj + '.rz', rza)
                # mc.setKeyframe(obj, at='rz', v=rza)
            except:
                pass

            try:
                mc.setAttr(obj + '.sx', sxa)
                # mc.setKeyframe(obj, at='sx', v=sxa)
            except:
                pass

            try:
                mc.setAttr(obj + '.sy', sya)
                # mc.setKeyframe(obj, at='sy', v=sya)
            except:
                pass


def main():
    QApplication.instance()
    ui = WaitPoseMatch()
    ui.show()
    # sys.exit(app.exec_())
    return ui


if __name__ == '__main__':
    main()
