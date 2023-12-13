from workfile_manager.plugin_utils import Application
from workman_world_custom.export_postproc.all import postproc_publish_parts_base

class BasePlugin(postproc_publish_parts_base.BasePlugin):
    def application(self):
        return Application.MotionBuilder

    def apps_executable_on(self):
        return (
            Application.MotionBuilder, Application.Standalone
        )

    def dcccmds(self):
        if not hasattr(self, '_dcccmds'):
            from postproc_set_editor_mbuilder import ui_mbuilder
            self._dcccmds = ui_mbuilder.DccCmds()
        
        return self._dcccmds

    