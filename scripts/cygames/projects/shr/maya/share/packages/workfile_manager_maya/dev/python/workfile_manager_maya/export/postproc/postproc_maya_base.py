# -*- coding: utf-8 -*-

from workfile_manager.plugin_utils import PostProcBase, Application

class MayaPostprocBase(PostProcBase):
    def application(self):
        return Application.Maya

    def _is_postproc_root_set(self, x):
        import maya.cmds as cmds
        try:
            if not cmds.attributeQuery('postproc_edit_set', ex=True, n=x):
                return False

            if not cmds.getAttr(x+'.postproc_edit_set'):
                return False

            buf = cmds.listConnections(x+'.message', d=True, s=False, p=True)
            if buf is None:
                return True
                
            for c in buf:
                nodename, attrname = c.split('.')
                if cmds.objectType(nodename) == 'objectSet' and attrname.startswith('dnSetMembers'):
                    return False

        except:
            pass
        
        return False
