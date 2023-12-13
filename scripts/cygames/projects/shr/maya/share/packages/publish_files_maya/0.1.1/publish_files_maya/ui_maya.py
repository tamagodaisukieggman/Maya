from __future__ import annotations
import os
import traceback
from publish_files import ui
from maya.app.general import mayaMixin
from workfile_manager.plugin_utils import Application
from publish_files.user_preference import PublishFilesPreferenceBase
from postproc_set_editor_maya.ui_maya import MayaSetEditorUserPreferences

class MayaPublishFilesPreferences(PublishFilesPreferenceBase):
    def get_tool_group(self) -> str:
        return 'Maya'

    def get_default_preference_file(self) -> str | None:
        return os.path.join(os.path.dirname(__file__), 'default_user_preferences.yaml')


class MainWindow(mayaMixin.MayaQWidgetBaseMixin, ui.MainWindow):
    def __init__(self):
        try:
            user_prefs = MayaPublishFilesPreferences.load()
        except:
            print(traceback.format_exc())
            user_prefs = MayaPublishFilesPreferences()
        
        try:
            set_editor_prefs = MayaSetEditorUserPreferences.load()
        except:
            print(traceback.format_exc())
            set_editor_prefs = MayaSetEditorUserPreferences()

        super(mayaMixin.MayaQWidgetBaseMixin, self).__init__(user_prefs, set_editor_prefs)

    def file_formats(self):
        return ['ma', 'mb']

    def get_workasset_obj(self):
        from workfile_manager_maya import assetutils_maya
        return assetutils_maya.WorkAssetMaya()

    def get_animasset_obj(self):
        from workfile_manager_maya import assetutils_maya
        return assetutils_maya.AnimationAssetMaya()

    def get_reader(self, filename):
        from workman_shenron_custom.asset_actions.maya import publish_parts_base_maya
        return publish_parts_base_maya.get_reader(filename)

    def preprocess_target(self, filename):
        from workman_shenron_custom.asset_actions.maya import publish_parts_base_maya
        if filename.endswith('.ma'):
            tmpfile = publish_parts_base_maya.convert_ma_to_cgkit_readable(filename)
            return tmpfile
        return filename


    def application(self):
        return Application.Maya

    @classmethod
    def get_exportmodule(cls):
        return 'workfile_manager_maya.export.post_publish_files_maya'

    @classmethod
    def get_batchfile(cls):
        from workfile_manager import cmds as wcmds
        wmm_root = os.environ['WORKFILE_MANAGER_MAYA_ROOT']
        workfile_manager_for_maya_version = wcmds.get_package_version('workfile_manager_maya')
        return '%s/workfile_manager_maya/%s/python/workfile_manager_maya/export/post_fbx_export.bat' % (wmm_root, workfile_manager_for_maya_version)

def show():
    global mwin
    try:
        mwin.close()
    except:
        pass
    mwin = MainWindow()
    mwin.resize(800, 600)
    mwin.show()
