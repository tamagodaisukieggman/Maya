from workfile_manager.plugin_utils import PreprocBase, Application, PluginType

try:
    import maya.cmds as cmds
except:
    pass

class MayaPreprocBase(PreprocBase):
    def application(self):
        return Application.Maya

    def init(self):
        self.results = []
        
    def func_in_error(self):
        if len(self.results) > 0:
            cmds.select(self.results, ne=True)
            print((self.results))

    def add_intermediate_selection(self, args, nodes):
        if type(nodes) is list and len(nodes) > 0:
            if 'selection' not in args:
                args['selection'] = cmds.ls(sl=True)

            cmds.select(nodes, ne=True, add=True)
    
   