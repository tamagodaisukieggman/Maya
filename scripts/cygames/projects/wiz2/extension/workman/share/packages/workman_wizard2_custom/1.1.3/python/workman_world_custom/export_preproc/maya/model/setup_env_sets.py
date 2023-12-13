# -*- coding: utf-8 -*-
import re 

try:
    import maya.cmds as cmds
except:
    pass

from workfile_manager import wmlog
from workfile_manager.plugin_utils import Application, PluginType
from workfile_manager_maya.export.preproc.preproc_maya_base import MayaPreprocBase

logger = wmlog.get_logger(__name__)


class Plugin(MayaPreprocBase, object):
    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'model' and asset.assetgroup == 'environment': 
            return True
        else:
            return False

    def execute(self, args):
        from postproc_set_editor import ui_preset
        from postproc_set_editor_maya import ui_maya
        import cypyapiutils
        
        mf = cmds.file(q=True, mf=True)

        sel = cmds.ls(sl=True)

        setobj = None

        try:
            var = cypyapiutils.Variable('PostProcSetEditor_PresetWindow', toolgroup='Maya')
            presets = ui_preset.get_presets(var.var)
            logger.info('presets:%s', presets)

            dcc_cmds = ui_maya.DccCmds()
            
            setobjs = ui_preset.create_set_from_preset(presets, 'combine', dcc_cmds, target_filter=self.target_filter)
            setobj = setobjs[0]

        except Exception as e:
            import traceback
            print((traceback.format_exc()))

        finally:
            if setobj:
                buf = cmds.sets(setobj.pm_set.name(), q=True)
                if len(buf) <= 1:
                    dcc_cmds.clear_set(setobj.pm_set.name())

        if not mf:
            cmds.file(mf=0)

        cmds.select(sel, ne=True)
        
        logger.info('Done.')

        return True, None
        

    def target_filter(self, targets):
        res = []
        for t in targets:
            buf = cmds.listConnections(t+'.instObjGroups', s=False, d=True, type='objectSet')
            if not buf:
                res.append(t)
                continue
            for set_ in buf:
                if not cmds.attributeQuery('postproc_edit_set__operator_name', n=set_, ex=True):
                    continue
                op_name = cmds.getAttr(set_+'.postproc_edit_set__operator_name')
                if op_name != 'combine_mesh':
                    continue
                break
            else:
                res.append(t)
        
        return res


                


    def getlabel(self):
        return 'Setup post-process for env.'
    
    def get_label_jp(self):
        return u'背景用のPostProcessをセットアップする'

    def order(self):
        return 100

    def default_checked(self):
        return True

    def is_editable(self):
        return False
