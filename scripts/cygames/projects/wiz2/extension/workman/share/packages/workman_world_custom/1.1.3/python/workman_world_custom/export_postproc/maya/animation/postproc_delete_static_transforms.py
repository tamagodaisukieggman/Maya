import re

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
        return 100


    def execute(self, args):
        self.types = ['transform', 'joint']
        self.animated = {}

        # get undeletable nodes.
        #
        undeletables = []
        buf = cmds.ls() # "ls -ud" doesn't work. That also returns deleable nodes.
                        # In addition, that causes the scene modification flag to get on.
        for n in buf:
            sn = re.sub('.*[|]', '', n)
            try:
                cmds.rename(n, sn)
            except:
                undeletables.append(n)
        #
        #

        nodes = cmds.ls(type=self.types)
        for node in [x for x in nodes if x not in undeletables]:
            if not cmds.objExists(node):
                continue
            if node not in self.animated:
                self.animated[node] = self.is_animated(node)
            if not self.animated[node]:
                cmds.delete(node)

        return True

    def getlabel(self):
        return 'Delete Static Transform Nodes'

    def default_checked(self):
        return True

    def is_animated(self, n):
        buf = cmds.listConnections(n, d=False, s=True, type='animCurve')
        if buf and len(buf) > 0:
            self.animated[n] = True
            return True
        else:
            chlds = cmds.listRelatives(n, f=True, c=True, type=self.types)
            if chlds and len(chlds) > 0:
                if True in [self.is_animated(x) for x in chlds]:
                    self.animated[n] = True
                    return True
                else:
                    self.animated[n] = False
                    return False
            else:
                self.animated[n] = False
                return False
        raise Exception('Invalid')
