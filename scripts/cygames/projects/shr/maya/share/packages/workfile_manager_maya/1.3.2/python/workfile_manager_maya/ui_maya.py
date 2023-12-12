# -*- coding: utf-8 -*-
from typing import Type
from Qt import QtCore


from maya.app.general import mayaMixin

from workfile_manager_maya import assetutils_maya
from workfile_manager.ui import ui_main
from workfile_manager import config, dccutils

from postproc_set_editor_maya.ui_maya import MayaSetEditorUserPreferences

config_ = config.Config.get_instance()

class MainWindow(mayaMixin.MayaQWidgetBaseMixin, ui_main.MainWindow):
    def dccutils(self) -> Type[dccutils.DccUtils]:
        return assetutils_maya.MayaUtils

    def parent_func(self, w):
        w.setParent(ui_main.mwin, QtCore.Qt.Window)

def show():
    try:
        if hasattr(ui_main, 'mwin') and hasattr(ui_main.mwin, 'close'):
            ui_main.mwin.close()
            
    except:
        import traceback
        print(traceback.format_exc())

    ui_main.mwin = MainWindow(toolgroup='Default', toolname='workfile_manager')
    ui_main.mwin.setStyleSheet('QWidget {font-size:14px}')
    
    try:
        set_editor_prefs = MayaSetEditorUserPreferences.load()
    except:
        print(traceback.format_exc())
        set_editor_prefs = MayaSetEditorUserPreferences()

    ui_main.mwin.set_editor_prefs = set_editor_prefs

    from publish_files_maya.ui_maya import MainWindow as PublishFilesWindow
    ui_main.mwin.publish_files_window_class = PublishFilesWindow

    try:
        if ui_main.mwin.user_prefs.miscellaneous.display_app_specific_colorbar == True:
            ui_main.mwin.add_application_name_bar("Maya",[127,183,188])
    except:
        pass

    
    ui_main.launch_command = 'from workfile_manager_maya import ui_maya;ui_maya.show()'
    ui_main.mwin.show_()

    if not config_.is_development_mode:
        import tool_log
        logger = tool_log.get_logger('WorkMan for Maya', '1.3.2')
        logger.send_launch("Initial launch")
        print('Launch log sent: WorkMan for Maya')
    
    
