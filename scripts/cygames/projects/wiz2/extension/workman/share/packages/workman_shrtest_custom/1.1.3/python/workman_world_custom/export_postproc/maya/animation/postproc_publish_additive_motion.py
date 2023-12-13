from __future__ import print_function

try:
    import maya.cmds as cmds
    import pymel.core as pm
    from workfile_manager_maya import assetutils_maya

except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application
from cylibassetdbutils import assetdbutils, assetutils
from workfile_manager import cmds as wcmds

import re, os

class Plugin(PostProcBase):
    def apps_executable_on(self):
        return (
            Application.Maya, Application.MotionBuilder, Application.Standalone
        )

    def is_asset_eligible(self, asset):
        if asset.area() == 'work' and asset.task == 'animation':
            return True
        else:
            return False
            
    def order(self):
        return 999999
        
    def execute(self, args):
        comp_root = cmds.ls('::root_jnt', fl=True)[0]
        base_anim_file = args['base_anim_file']
        print('>>>>>>>> base_anim_file: ', base_anim_file)
        cmds.file(base_anim_file, i=True, ns=':')
        task = GenerateAdditiveMotion('root_jnt', comp_root)

        self.import_base_skeleton()
        task.execute()
        return True

    def getlabel(self):
        return 'Publish additive motion'

    def default_checked(self):
        return False

    def is_editable(self):
        return False

    def import_base_skeleton(self):
        from cylibassetdbutils import assetdbutils
        db = assetdbutils.DB.get_instance()
        refs = cmds.ls(type='reference')
        for ref in refs:
            print('ref:', ref)
            fn = cmds.referenceQuery(ref, filename=True)
            fn = wcmds.get_share_path_from_cache(fn)
            print('ref_filename:', fn)

            buf = db.get_sharedasset_from_file(filename=fn)
            if len(buf) == 0:
                continue
            sasset = buf[0]
            if sasset['assetgroup'] != 'character' or sasset['task'] != 'model' or sasset['variant'] != 'default':
                continue
            
            cmds.file(fn, i=True, ns='base_skeleton')
            break

class GenerateAdditiveMotion():
    def __init__(self, base_root, composited_root):
        
        ts = re.sub('.*[|]', '', composited_root)
        self.cp_ns = ts[:ts.index(':')]

        self.anim_layer = None
        self.base_root = base_root
        self.composited_root = composited_root
        
    def create_animlayer(self):
        cmds.select(self.base_root, hi=True)
        self.anim_layer = cmds.animLayer(aso=True)

    def constrain(self, src_ns, dst_ns, node=None):
        if node == None:
            node = src_ns + ':root_jnt'
        leaf = re.sub('.*[|]', '', node)
        leaf = re.sub('.*:', '', leaf)
        buf = cmds.ls(dst_ns + ':' + leaf)
        if len(buf) > 0:
            opnode = buf[0]
            # const.
            print('Constraining %s to %s...' % (node, opnode))
            cmds.parentConstraint(opnode, node, mo=False)
        else:
            cmds.warning('Cannot find any node for: ', node)
        
        clds = cmds.listRelatives(node, pa=True, c=True)
        if clds is not None:
            for c in clds:
                self.constrain(src_ns, dst_ns, node=c)

    def bake(self):
        st = int(cmds.playbackOptions(q=True, ast=True))
        ed = int(cmds.playbackOptions(q=True, aet=True))
        cmds.select(self.base_root, hi=True)
        for fr in [x+st for x in range(ed-st+1)]:
            print('currentframe:', fr)
            cmds.currentTime(fr)
            cmds.setKeyframe(al=self.anim_layer, at='rotate')


    def delete_constraint(self):
        nodes = cmds.listRelatives(self.base_root, ad=True, pa=True)
        if nodes is not None:
            consts = cmds.ls(nodes, type='constraint')
            if len(consts) > 0:
                cmds.delete(consts)

    def set_current_layer(self, layer):
        for n in cmds.ls(type='animLayer'):
            if n == layer:
                cmds.animLayer(n, e=True, selected=True, preferred=True)
            else:
                cmds.animLayer(n, e=True, selected=False, preferred=False)

    def execute(self):
        orgsel = cmds.ls(sl=True)

        from maya import mel
        self.create_animlayer()
        self.constrain('', self.cp_ns)
        self.bake()
        self.delete_constraint()
        cmds.animLayer(self.anim_layer, e=True, override=True)
        self.set_current_layer('BaseAnimation')

        nodes = cmds.listRelatives('root_jnt', ad=True, pa=True) + ['root_jnt']
        cmds.select(nodes)
        del_attrs = ('tx', 'ty', 'tz', 'sx', 'sy', 'sz')
        cmds.cutKey(cl=True, t=(), at=del_attrs)
        self.resume_default()

        self.set_current_layer(self.anim_layer)
        cmds.currentTime(int(cmds.playbackOptions(q=True, ast=True)))
        cmds.select(self.base_root, hi=True)
        cmds.setKeyframe()
        for n in nodes:
            for at in del_attrs:
                mel.eval('source channelBoxCommand; CBdeleteConnection %s.%s' % (n, at))
        
        st = cmds.playbackOptions(q=True, ast=True)
        ed = cmds.playbackOptions(q=True, aet=True)
        cmds.bakeResults('root_jnt', t=(st, ed), simulation=True, hierarchy='below', sampleBy=1, oversamplingRate=1,
                            disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False,
                            removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False, 
                            at=("rx", "ry", "rz"))
        cmds.delete(self.anim_layer)

        cmds.select(orgsel, ne=True)
        

    def resume_default(self, node=None):
        if node is None:
            node = 'root_jnt'
        leaf = re.sub('.*[|]', '', node)
        
        for at in ['t', 's']:
            v = cmds.getAttr('base_skeleton:' + leaf + '.' + at)[0]
            cmds.setAttr(node + '.' + at, v[0], v[1], v[2])
        
        clds = cmds.listRelatives(node, c=True, pa=True)
        if clds is not None:
            for cld in clds:
                self.resume_default(node=cld)


