from workfile_manager.plugin_utils import Application

try:
    import maya.cmds as cmds
except:
    pass


from workman_world_custom.export_postproc.all import postproc_publish_parts_base


class BasePlugin(postproc_publish_parts_base.BasePlugin):
    def application(self):
        return Application.Maya

    def apps_executable_on(self):
        return (
            Application.Maya, Application.Standalone
        )

    def dcccmds(self):
        if not hasattr(self, '_dcccmds'):
            from postproc_set_editor_maya import ui_maya
            self._dcccmds = ui_maya.DccCmds()
        
        return self._dcccmds

    