# -*- coding: utf-8 -*-
import re 

try:
    import maya.cmds as cmds
    from workfile_manager_maya import assetutils_maya
except:
    pass

from workfile_manager.plugin_utils import Application, PluginType
from workfile_manager_maya.export.preproc.preproc_maya_base import MayaPreprocBase

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
        for n in cmds.ls(type='mesh'):
            try:
                self.exec_mesh(n)
            except Exception as e:
                print(e)

        if len(self.results) > 0:
            return False, self.results
        else:
            return True, None

    def exec_mesh(self, mesh):
        tr = cmds.listRelatives(mesh, pa=True, p=True)[0]

        attrs = [('translate', 't', 'string'), 
                ('rotate', 'r', 'string'),
                ('scale', 's', 'string'),
                ('axisDirection', None, 'string')]

        type_map = {'double3':'at', 'string':'dt'}
        done = []

        for at in cmds.listAttr(tr):
            if at.startswith('edgebox_'):
                cmds.deleteAttr(tr, at=at)

        try:
            lcts = cmds.ls(type='curveLocator')
            lcts = [x for x in lcts if cmds.getAttr(x+'.locatorTypeName')=='edgebox']
        except:
            lcts = []

        for n in lcts:
            pr = cmds.listRelatives(n, pa=True, p=True)[0]
            leaf = re.sub('.*[|]', '', pr)
            
            name_ = leaf

            if name_ in done:
                if n not in self.results:
                    self.results.append(n)
                continue

            values = {}
            for _, attr, _ in attrs:
                if attr is None:
                    continue
                values[attr] = cmds.getAttr(pr+'.'+attr)[0]
            
            values['t'], values['r'], values['s'] = assetutils_maya.transfer_to_z_up(values['t'], values['r'], values['s'])
            

            for label, attr, attr_type in attrs:
                attrname = 'edgebox_%s_%s' % (label, name_)
                if not cmds.attributeQuery(attrname, ex=True, n=tr):
                    args = {type_map[attr_type]:attr_type}
                    try:
                        cmds.addAttr(tr, ln=attrname, **args)
                        if attr_type == 'double3':
                            for axis in 'XYZ':
                                cmds.addAttr(tr, ln=attrname+axis, at='double', p=attrname)

                    except Exception as e:
                        print(e)
                        self.results.append(n)
                        continue

                if attr is not None:
                    #cmds.setAttr(tr+'.'+attrname, *values[attr], type=attr_type)
                    cmds.setAttr(tr+'.'+attrname, ', '.join(['%s=%f' % (x, y) for x,y in zip('XYZ', values[attr])]), type=attr_type)
                else:
                    if label == 'axisDirection':
                        cmds.setAttr(tr+'.'+attrname, 'Y-UP(RH)', type='string')

            done.append(name_)
        

    def getlabel(self):
        return 'Export edgebox'

    def get_label_jp(self):
        return u'edgeboxをエクスポート'

    def get_discription(self):
        return 'test'

    def order(self):
        return 100

    def default_checked(self):
        return True


    
        