import os

from publish_files import ui
import cypyapiutils
from maya.app.general import mayaMixin
from workfile_manager.plugin_utils import Application


class MainWindow(mayaMixin.MayaQWidgetBaseMixin, ui.MainWindow):
    def __init__(self):
        self.default_varfile = os.path.join(os.path.dirname(__file__), 'config.yaml')
        self.var = cypyapiutils.Variable('Publish_files', toolgroup='Maya', defaultfile=self.default_varfile)
        #super(MainWindow, self).__init__(parent=cymobuapiutils.ui_utility.get_main_window())
        super(mayaMixin.MayaQWidgetBaseMixin, self).__init__()

    def file_format(self):
        return 'ma'

    def get_workasset_obj(self):
        from workfile_manager_maya import assetutils_maya
        return assetutils_maya.WorkAssetMaya()

    def get_animasset_obj(self):
        from workfile_manager_maya import assetutils_maya
        return assetutils_maya.AnimationAssetMaya()

    def get_reader(self):
        from workman_world_custom.asset_actions.maya import publish_parts_base_maya as pp
        return pp.MAReader

    def preprocess_target(self, filename):
        from workman_world_custom.asset_actions.maya import publish_parts_base_maya
        tmpfile = publish_parts_base_maya.convert_ma_to_cgkit_readable(filename)
        return tmpfile

    def application(self):
        return Application.Maya

    def get_exportmodule(self):
        return 'workfile_manager_maya.export.post_publish_files_maya'

    def get_batchfile(self):
        wm_maya_ver = os.environ['WORKFILE_MANAGER_MAYA_VERSION']
        return 'c:/cygames/wiz2/tools/projects/world/inhouse/win/extension/maya/share/packages/workfile_manager_maya/%s/python/workfile_manager_maya/export/post_fbx_export.bat' % wm_maya_ver

def show():
    global mwin
    try:
        mwin.close()
    except:
        pass
    mwin = MainWindow()
    mwin.resize(800, 600)
    mwin.show()
