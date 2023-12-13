try:
    import maya.cmds as cmds
except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def apps_executable_on(self):
        return (
            Application.Maya,
            Application.MotionBuilder,
            Application.Standalone,
        )
    
    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False

    def order(self):
        return 100000

    def execute(self, args):
        from workfile_manager_maya import assetutils_maya
        ro = cmds.ls(ro=True)
        if ro is None:
            ro = []
        meshes = cmds.ls(type='mesh')
        if meshes is None:
            meshes = []
        
        if len(meshes) > 0:
            meshes = [x for x in meshes if x not in ro]
            trs = cmds.listRelatives(meshes, p=True, pa=True)
            trs = trs if type(trs) is list else []
            trs = [x for x in trs if not self.is_animated(x)]
            targets = trs+meshes
            assetutils_maya.delete_connections(targets)

            try:    
                cmds.delete(targets)
            except:
                import traceback
                print(traceback.format_exc())

        return True

    def getlabel(self):
        return 'Delete Geometries'

    def default_checked(self):
        return True

    def is_animated(self, n):
        buf = cmds.listConnections(n, d=False, s=True, type='animCurve')
        if buf is None or len(buf) == 0:
            return False
        else:
            return True