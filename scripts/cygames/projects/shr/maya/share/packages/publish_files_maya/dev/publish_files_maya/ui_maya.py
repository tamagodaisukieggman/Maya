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

    def file_formats(self):
        return ['ma', 'mb']

    def get_workasset_obj(self):
        from workfile_manager_maya import assetutils_maya
        return assetutils_maya.WorkAssetMaya()

    def get_animasset_obj(self):
        from workfile_manager_maya import assetutils_maya
        return assetutils_maya.AnimationAssetMaya()

    def get_reader(self, filename):
        from workman_shenron_custom.asset_actions.maya import publish_parts_base_maya as pp
        return pp.BasePlugin().get_reader(filename)

    def preprocess_target(self, filename):
        from workman_shenron_custom.asset_actions.maya import publish_parts_base_maya
        if filename.endswith('.ma'):
            tmpfile = publish_parts_base_maya.convert_ma_to_cgkit_readable(filename)
            return tmpfile
        return filename


    def application(self):
        return Application.Maya

    def get_exportmodule(self):
        return 'workfile_manager_maya.export.post_publish_files_maya'

    def get_batchfile(self):
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
