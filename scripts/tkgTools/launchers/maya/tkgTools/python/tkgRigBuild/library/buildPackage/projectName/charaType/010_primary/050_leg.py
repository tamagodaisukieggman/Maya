# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
reload(tkgPart)
reload(tkgModule)
rigModule = tkgModule.RigModule()

for s in ['Lf', 'Rt']:
    if s == 'Lf':
        fs = '_L'
    else:
        fs = '_R'

    leg = tkgPart.build_module(module_type="bipedLimb",
                              side=s, part="leg",
            guide_list=["proxy_Thigh" + fs, "proxy_Knee" + fs, "proxy_Ankle" + fs],
            ctrl_scale=9)

    endJnt = rigModule.create_endJnt(base='proxy_Toe' + fs, wt=[0,0,5], awt_obj=None)
    foot = tkgPart.build_module(module_type="foot",
                              side=s, part="foot",
            guide_list=["proxy_Ankle" + fs, "proxy_Toe" + fs, endJnt],
            ctrl_scale=9)
