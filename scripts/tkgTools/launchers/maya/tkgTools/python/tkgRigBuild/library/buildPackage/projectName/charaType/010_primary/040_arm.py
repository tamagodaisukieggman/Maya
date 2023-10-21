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

    arm = tkgPart.build_module(module_type="bipedLimb",
                              side=s, part="arm",
            guide_list=["proxy_Arm" + fs, "proxy_Elbow" + fs, "proxy_Wrist" + fs])

    clavicle = tkgPart.build_module(module_type="clavicle",
                              side=s, part="clavicle",
            guide_list=["proxy_Shoulder" + fs, "proxy_Arm" + fs],
            local_orient=True,
            ctrl_scale=9)

    hand = tkgPart.build_module(module_type="hand",
                              side=s, part="hand",
            guide_list=["proxy_Wrist" + fs],
            ctrl_scale=9)
