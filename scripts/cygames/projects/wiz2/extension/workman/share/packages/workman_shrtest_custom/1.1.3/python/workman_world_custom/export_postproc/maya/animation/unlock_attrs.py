try:
    import maya.cmds as cmds
except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def apps_executable_on(self):
        return [
                Application.Maya, 
                Application.MotionBuilder,
                Application.Standalone,
            ]

    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False
            
    def order(self):
        return 10
        
    def execute(self, args):
        ro = cmds.ls(ro=True)
        if ro is None:
            ro = []
        dags = cmds.ls(dag=True)
        if dags is None:
            dags = []
        for n in [x for x in dags if x not in ro]:
            attrs = cmds.listAttr(n, l=True)
            if attrs is None:
                continue
            for attr in attrs:
                try:
                    cmds.setAttr(n+'.'+attr, l=False)
                except:
                    print(('Error: cannot unlock: %s.%s' % (n, attr)))
        
        return True

    def default_checked(self):
        return True 

    def getlabel(self):
        return 'Unlock attributes'