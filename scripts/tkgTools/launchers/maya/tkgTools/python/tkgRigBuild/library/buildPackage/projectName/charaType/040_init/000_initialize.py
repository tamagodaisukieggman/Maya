# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.post.finalize as tkgFinalize
import tkgRigBuild.libs.attribute as tkgAttr
reload(tkgPart)
reload(tkgModule)
reload(tkgFinalize)
reload(tkgAttr)

# ------------------------------------------------
# hip
# add skeleton plugs
tkgAttr.Attribute(node=self.part_grp, type='plug',
                 value=['Cn_root_JNT'], name='skeletonPlugs',
                 children_name=[self.bind_joints[0]])

# add space plugs
target_list = ['CHAR', 'Cn_global_CTRL', 'Cn_root_02_CTRL', '2']
name_list = ['world', 'global', 'root', 'default_value']

tkgAttr.Attribute(node=self.part_grp, type='plug',
                 value=target_list,
                 name=self.hip_01.ctrl + '_parent',
                 children_name=name_list)

# ------------------------------------------------
