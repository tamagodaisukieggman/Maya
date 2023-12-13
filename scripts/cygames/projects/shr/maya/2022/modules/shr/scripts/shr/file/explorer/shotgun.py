import os
from pathlib import Path
from operator import itemgetter

from PySide2.QtCore import (
    Qt,
    QEvent
)
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QAbstractItemView,
    QStyledItemDelegate,
    QComboBox,
    QStyle
)

try:
    import maya.cmds as cmds
    import maya.mel as mel
    if hasattr(cmds, 'about'):
        MODE = 'MAYA'
    else:
        MODE = 'STANDALONE'
except ImportError:
    MODE = 'STANDALONE'

# shotgun test
from mtk.utils.shotgun import MtkSG
import logging

logger = logging.getLogger(__name__)

sg_task_template_data = None

task_template_name = 'mtk Animation Asset'

class ShotgunStatusIconProvider:

    def __init__(self) -> None:
        pass

        self.status_icon_na = self.make_qicon('images/shotgun/status/sg_icon_status_na.png')
        self.status_icon_complete = self.make_qicon('images/shotgun/status/sg_icon_status_comp.png')
        self.status_icon_hold = self.make_qicon('images/shotgun/status/sg_icon_status_hld.png')
        self.status_icon_omit = self.make_qicon('images/shotgun/status/sg_icon_status_omt.png')
        self.status_icon_ready = self.make_qicon('images/shotgun/status/sg_icon_status_rdy.png')
        self.status_icon_retake = self.make_qicon('images/shotgun/status/sg_icon_status_rtk.png')
        self.status_icon_review_pending = self.make_qicon('images/shotgun/status/sg_icon_status_rev.png')
        self.status_icon_review_waiting = self.make_qicon('images/shotgun/status/sg_icon_status_wfr.png')
        self.status_icon_waiting = self.make_qicon('images/shotgun/status/sg_icon_status_wtg.png')

        self.status_icon_deliverable = self.make_qicon('images/shotgun/status/sg_icon_status_deliv.png')
        self.status_icon_delivered = self.make_qicon('images/shotgun/status/sg_icon_status_dlvr.png')
        self.status_icon_final = self.make_qicon('images/shotgun/status/sg_icon_status_fin.png')
        self.status_icon_ip = self.make_qicon('images/shotgun/status/sg_icon_status_ip.png')
        self.status_icon_late = self.make_qicon('images/shotgun/status/sg_icon_status_late.png')

        self.sg_status_icons = {
            'comp': self.status_icon_complete,
            'deliv': self.status_icon_deliverable,
            'dlvr': self.status_icon_delivered,
            'fin': self.status_icon_final,
            'hld': self.status_icon_hold,
            'ip': self.status_icon_ip,
            'late': self.status_icon_late,
            'na': self.status_icon_na,
            'omt': self.status_icon_omit,
            'rdy': self.status_icon_ready,
            'rtk': self.status_icon_retake,
            'rev': self.status_icon_review_pending,
            'wfr': self.status_icon_review_waiting,
            'wtg': self.status_icon_waiting,
        }
    
    def make_qicon(self, file_path) -> QIcon:
        base_path = Path(os.path.dirname(__file__))
        return QIcon(str(base_path.joinpath(file_path)))


    def status_icon(self, sg_status) -> QIcon:
        icon = None
        if sg_status in self.sg_status_icons:
            icon = self.sg_status_icons[sg_status]
        return icon



class MtkExplorerShotgunTaskUIProvider(object):
    _sg_task_template_data = None
    _values = []
    _labels = []

    @classmethod
    def task_template_data(cls):
        if not cls._sg_task_template_data:
            task_template_name = 'mtk Animation Asset'
            task_template_data = MtkSG.task_template_data(task_template_name)

            #print("task template data: {}".format(task_template_data))
            # sort by the sg_sort_order. that way it will appear in the combo box in the same order as Shotgun.
            #cls._sg_task_template_data = sorted(task_template_data, key=lambda k: k['sg_sort_order'])
            cls._sg_task_template_data = sorted(task_template_data, key=itemgetter('sg_sort_order'))

        return cls._sg_task_template_data

    @classmethod
    def values(cls):
        if not cls._values:
            cls._values.append(0)  # default for na/nothing
            task_template_data = cls.task_template_data()
            task_count = len(task_template_data)
            if task_count:
                cls._values.extend(range(1, task_count))
        return cls._values

    @classmethod
    def labels(cls):
        if not cls._labels:
            cls._labels.append(u'na')  # default for na/nothing
            task_template_data = cls.task_template_data()
            for task in task_template_data:
                if 'content' in task:
                    task_name = task['content']
                    cls._labels.append(task_name)  # dont format this
        return cls._labels

    @classmethod
    def value_to_label(cls, value):
        label_list = cls.labels()
        label = label_list[value]
        return label

    @classmethod
    def label_to_value(cls, label):
        value_list = cls.values()
        value = value_list.index(label)
        return value


class ShotgunTaskComboBoxDelegate(QStyledItemDelegate):

    def __init__(self, parent):
        super(ShotgunTaskComboBoxDelegate, self).__init__(parent)

        self.item_text_list = MtkExplorerShotgunTaskUIProvider.labels()

        self.save_restore_dict = {}


    def wheelEvent(self, event):
        # disable the mouse wheel scroll
        event.ignore()

    def getSaveRestoreData(self, sg_asset_name):
        combo_data_dict = {}
        if sg_asset_name in self.save_restore_dict:
            combo_data_dict = self.save_restore_dict[sg_asset_name]
        return combo_data_dict

    # restore the data
    def restore_combobox_state(self, object):
        #print(u"ComboBoxDelegate")
        #print(u"On Combobox Show (Restore Data)")

        # the name of the asset
        combo = object
        sg_asset_name = combo.itemData(0, Qt.UserRole)
        sg_task_name = None
        sg_task_data = {}

        combo_data_dict = {}
        if sg_asset_name in self.save_restore_dict:
            combo_data_dict = self.save_restore_dict[sg_asset_name]
            #print("combo data dict for {} was retrieved from storage ...".format(sg_asset_name))
        #else:
        #    print("combo data dict for {} was NOT retrieved from storage!".format(sg_asset_name))
        #    print("self.save_restore_dict: {}".format(self.save_restore_dict))

        # here, there must be a dict exist check. otherwise it means no data.
        if combo_data_dict:
            if 'sg_task_name' in combo_data_dict:
                sg_task_name = combo_data_dict['sg_task_name']
            if 'sg_task_data' in combo_data_dict:
                sg_task_data = combo_data_dict['sg_task_data']

            # restore the combo box index.
            if 'cb_current_index' in combo_data_dict:
                cb_current_index = combo_data_dict['cb_current_index']

                combo.blockSignals(True)
                combo.setCurrentIndex(cb_current_index)
                combo.blockSignals(False)
                self.commit_editor()

                #print("restoring:")
                #print("sg task name: {}".format(sg_task_name))
                #print("sg task data: {}".format(sg_task_data))
                #print("cb current index: {}".format(cb_current_index))


    # save the data
    def save_combobox_state(self, object):
        #print(u"ComboBoxDelegate")
        #print(u"On Combobox Hide (Save Data) ")

        combo = object
        cb_current_index = combo.currentIndex()
        # the name of the asset
        sg_asset_name = combo.itemData(0, Qt.UserRole)
        # the name of the task
        sg_task_name = combo.itemText(cb_current_index) if cb_current_index > 0 else None
        # the current sg task data associated with this task name
        sg_task_data = combo.itemData(cb_current_index, Qt.UserRole) if cb_current_index > 0 else None

        #print("sg_asset_name: {}".format(sg_asset_name))
        #print("sg_task_name: {}".format(sg_task_name))
        #print("sg_task_data: {}".format(sg_task_data))

        # save the data to the save/restore dict
        combo_data_dict = {}

        if sg_asset_name in self.save_restore_dict:
            combo_data_dict = self.save_restore_dict[sg_asset_name]
            #print("combo data dict for {} was retrieved from storage ...".format(sg_asset_name))
            #print("dict: {}".format(combo_data_dict))
        #else:
            #print("combo data dict for {} was NOT retrieved from storage!".format(sg_asset_name))
            #print("self.save_restore_dict: {}".format(self.save_restore_dict))

        # save the combo state (index, associated task and data)
        combo_data_dict['cb_current_index'] = cb_current_index
        combo_data_dict['sg_task_name'] = sg_task_name
        combo_data_dict['sg_task_data'] = sg_task_data

        self.save_restore_dict[sg_asset_name] = combo_data_dict
        #print("saving:")
        #print("sg task name: {}".format(sg_task_name))
        #print("sg task data: {}".format(sg_task_data))
        #print("cb current index: {}".format(cb_current_index))


    def eventFilter(self, object, event):
        #print(u"ComboBox EventFilter: {}, Object: {}".format(event.type(), object))
        if event.type() == QEvent.HideToParent:
            # save the combo box state when the combobox is hidden
            self.save_combobox_state(object)
        elif event.type() == QEvent.ShowToParent:
            # restore the combobox state when the the combobox is shown
            self.restore_combobox_state(object)

        # upon selection, save. for multi select situation.
        #if event.type() == QEvent.PolishRequest:
        #    self.save_combobox_state(object)

        return QComboBox.eventFilter(self, object, event)

    def print_state_flags(self, state):
        state_data_list = [
            (QStyle.State_None, "State None"),

            (QStyle.State_Active, "State Active"),

            (QStyle.State_AutoRaise, "State AutoRaise"),

            (QStyle.State_Children, "State Children"),

            (QStyle.State_DownArrow, "State DownArrow"),

            (QStyle.State_Editing, "State Editing"),

            (QStyle.State_Enabled, "State Enabled"),

            # (QStyle.State_HasEditFocus, "State HasEditFocus"), # not exist

            (QStyle.State_HasFocus, "State HasFocus"),

            (QStyle.State_Horizontal, "State Horizontal"),

            (QStyle.State_KeyboardFocusChange, "State KeyboardFocusChange"),

            (QStyle.State_MouseOver, "State MouseOver"),

            (QStyle.State_NoChange, "State NoChange"),

            (QStyle.State_Off, "State Off"),

            (QStyle.State_On, "State On"),

            (QStyle.State_Raised, "State Raised"),

            (QStyle.State_ReadOnly, "State ReadOnly"),

            (QStyle.State_Selected, "State Selected"),

            (QStyle.State_Item, "State Item"),

            (QStyle.State_Open, "State Open"),

            (QStyle.State_Sibling, "State Sibling"),

            (QStyle.State_Sunken, "State Sunken"),

            (QStyle.State_UpArrow, "State UpArrow"),

            (QStyle.State_Mini, "State Mini"),

            (QStyle.State_Small, "State Small"),
        ]

        logger.debug(u"State Flags:")
        for state_data in state_data_list:
            state_flag = state_data[0]
            state_label = state_data[1]
            if state & state_flag:
                 logger.debug("{}".format(state_label))

    def activated(self, cbIndex):
        # save the combobox state when the user selects an item
        # this function only triggers when the user changes the selection.
        # it does not trigger when a programmer users 'setCurrentIndex'
        #logger.debug(u"Combobox Delegate")
        #logger.debug(u"activated: {}".format(cbIndex))

        editor = self.sender()
        if editor:
            # save the combobox state
            self.save_combobox_state(editor)

    def index_changed(self, cbIndex):
        # commit the combobox data.
        # this function triggers when a programmer uses 'setCurrentIndex'
        #logger.debug(u"Combobox Delegate")
        #logger.debug(u"index_changed: {}".format(cbIndex))
        editor = self.sender()
        if editor:
            # commit combobox data
            self.commitData.emit(editor)



    def paint(self, painter, option, index):
        #model = index.model()
        #parent = index.parent()
        #isValid = index.isValid()

        if not index.isValid():
            return

        if option.state & QStyle.State_Selected:
            # # logger.debug("paint: index.row {}, index.column {}".format(index.row(), index.column()))
            ## logger.debug("isValid: {}".format(type(isValid)))
            ## logger.debug("model: {}".format(type(model)))  # MtkExplorerFileSortFilterProxyMode
            ## logger.debug("parent: {}".format(type(parent)))  # QModelIndex
            ## logger.debug("self.parent: {}".format(type(self.parent)))   # MtkExplorerFileView
            ## logger.debug("self.parent(): {}".format(type(self.parent())))  # MtkExplorerFileView
            if isinstance(self.parent(), QAbstractItemView):
                ## logger.debug("opening persistent editor: {}".format(type(index)))
                self.parent().openPersistentEditor(index)
        else:
            if isinstance(self.parent(), QAbstractItemView):
                self.parent().closePersistentEditor(index)

        super(ShotgunTaskComboBoxDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        # this function creates the combobox
        logger.debug("ComboBoxDelegate")
        logger.debug("createEditor")

        # create the combobox

        editor = QComboBox(parent)

        editor.installEventFilter(self)

        editor.activated.connect(self.activated)
        editor.currentIndexChanged.connect(self.index_changed)

        # disable scroll on mouse wheel event
        editor.setFocusPolicy(Qt.StrongFocus)
        editor.wheelEvent = self.wheelEvent

        #editor.focusInEvent = self.focusInEvent
        #editor.focusOutEvent = self.focusOutEvent

        # set center text alignment
        editor.setEditable(True)
        editor.lineEdit().setReadOnly(True)
        editor.lineEdit().setAlignment(Qt.AlignCenter)

        editor.clear()
        editor.addItems(self.item_text_list)

        # aquire the asset data from shotgun

        sg_tasks = index.data(Qt.UserRole)

        if not sg_tasks:
            # if data can not be aquired, return with sg task status 'na'
            activeTaskName = 'na'
            activeIndex = self.item_text_list.index(activeTaskName) if activeTaskName else 0
            cbIndex = activeIndex
            # default index is first task that does not have the status of 'wtg' (waiting), else 0.
            editor.setCurrentIndex(cbIndex)
            return editor

        # get the asset name from any of the tasks.
        # save the name to index 0 of the combobox.
        task = next((x for x in sg_tasks), None)
        entity_data = task['entity']
        asset_name = entity_data['name']

        # save / restore data for dynamic combobox.
        combo_data_dict = {}
        if asset_name in self.save_restore_dict:
            combo_data_dict = self.save_restore_dict[asset_name]

        # save all sg task data in case you need it.
        self.save_restore_dict[asset_name] = combo_data_dict



        # set the combobox data

        active_task = None

        # center all item text
        item_count = len(self.item_text_list)

        for i in range(item_count):
            # center the text
            editor.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

            # the first index is for non sg task data
            if i == 0:
                # store the asset name in index 0. 0 is for non sg task.
                editor.setItemData(0, asset_name, Qt.UserRole)
                continue

            # fore each sg task, store task data
            cb_task_name = self.item_text_list[i]

            sg_task = next((x for x in sg_tasks if x['content'] == cb_task_name), None)

            if sg_task:
                sg_task_name = sg_task['content']
                logger.debug(u"Found matching sg task for cb task name: {}".format(sg_task_name))

                # store the sg task data to the corresponding combobox item.
                editor.setItemData(i, sg_task, Qt.UserRole)

                status_code = sg_task['sg_status_list'] if 'sg_status_list' in sg_task else None

                if status_code:
                    logger.debug(u"Task: {}, Status Code: {}".format(sg_task_name, status_code))
                    if status_code != u"wtg" and active_task is None:
                        active_task = sg_task
                    status_icon = ShotgunStatusIconProvider().status_icon(status_code)
                    if status_icon:
                        editor.setItemIcon(i, status_icon)
                else:
                    logger.debug(u"Could not aquire task status.")
                    logger.debug(u"sg task: {}".format(sg_task))
            else:
                logger.debug(u"Did not find matching sg task for cb task name: {}".format(cb_task_name))
                logger.debug(u"sg tasks: {}".format(sg_tasks))

        activeTaskName = active_task['content'] if active_task else None
        activeIndex = self.item_text_list.index(activeTaskName) if activeTaskName else 0
        cbIndex = activeIndex

        # default index is first task that does not have the status of 'wtg' (waiting), else 0.
        editor.setCurrentIndex(cbIndex)

        return editor

    def setEditorData(self, editor, index):
        # for some reason, "logger" does not output to maya script editor, but "logger.debug" does...
        logger.debug("ComboBoxDelegate")
        logger.debug("setEditorData")

        #value = index.model().data(index, Qt.DisplayRole)
        #editor.setCurrentIndex(editor.findText(value))
        #editor.update()
        #return

        task_name = 'NA'
        status_code = "na"
        status_icon = None

        #editor.blockSignals(True)

        # make sure the table view index (row) data is set with the latest task data from shotgun.
        sg_tasks = index.data(Qt.UserRole)

        # center all item text
        item_count = len(self.item_text_list)

        active_task = None

        for i in range(item_count):
            # center the text
            editor.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

            # fore each task, store task data
            cb_task_name = self.item_text_list[i]

            if sg_tasks:

                sg_task = next((x for x in sg_tasks if x['content'] == cb_task_name), None)

                #for task in sg_tasks:
                if sg_task:
                    #task_name = task['content']
                    #task_id = task['id']
                    task_name = sg_task["content"] if 'content' in sg_task else None

                    if task_name and task_name == cb_task_name:
                        # editor.setItemText(i, task_name)
                        editor.setItemData(i, sg_task, Qt.UserRole)

                    status_code = sg_task['sg_status_list'] if 'sg_status_list' in sg_task else None

                    if status_code:
                        logger.debug("Task: {}, Status Code: {}".format(task_name, status_code))

                        if status_code != u"wtg" and active_task is None:
                            active_task = sg_task

                        status_icon = ShotgunStatusIconProvider().status_icon(status_code)
                        if status_icon:
                            editor.setItemIcon(i, status_icon)
                    else:
                        logger.debug("Could not aquire task status.")
                        logger.debug(u"sg task: {}".format(sg_task))
                else:
                    logger.debug(u"Did not find matching sg task for cb task name: {}".format(cb_task_name))
                    logger.debug(u"sg tasks: {}".format(sg_tasks))

        #combo_task_data = editor.itemData(index, Qt.UserRole)
        #if not combo_task_data:
        #    # logger.debug("combo task data is null !!")

        #active_task = None
        activeTaskName = active_task['content'] if active_task else None
        activeIndex = self.item_text_list.index(activeTaskName) if activeTaskName else 0
        cbIndex = activeIndex

        #logger.debug(u"Active Task: {} ({})".format(activeTaskName, activeIndex))
        #logger.debug("Saved CB Index: {}".format(self.saved_cb_index))

        editor.setCurrentIndex(cbIndex)
        editor.update()

        asset_name = None

        if sg_tasks:
            task = next((x for x in sg_tasks), None)
            entity_data = task['entity']
            asset_name = entity_data['name']

        # save the combo box state on first load
        if asset_name not in self.save_restore_dict:
            self.save_combobox_state(editor)
        else:
            # restore the combo box state if not first load
            self.restore_combobox_state(editor)

    def setModelData(self, editor, model, index):
        logger.debug("Combobox Delegate")
        logger.debug("Set Model Data")
        super(ShotgunTaskComboBoxDelegate, self).setModelData(editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def commit_editor(self):
        editor = self.sender()
        self.commitData.emit(editor)

    def commit_and_close_editor(self):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)
