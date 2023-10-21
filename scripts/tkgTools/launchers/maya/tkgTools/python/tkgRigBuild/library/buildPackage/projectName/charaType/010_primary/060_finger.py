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

    pinky = tkgPart.build_module(module_type="finger",
                              side=s, part="pinky",
            guide_list=["proxy_Pinky_01" + fs, "proxy_Pinky_02" + fs, "proxy_Pinky_03" + fs],
            ctrl_scale=2, remove_last=False)

    ring = tkgPart.build_module(module_type="finger",
                              side=s, part="ring",
            guide_list=["proxy_Ring_01" + fs, "proxy_Ring_02" + fs, "proxy_Ring_03" + fs],
            ctrl_scale=2, remove_last=False)

    middle = tkgPart.build_module(module_type="finger",
                              side=s, part="middle",
            guide_list=["proxy_Middle_01" + fs, "proxy_Middle_02" + fs, "proxy_Middle_03" + fs],
            ctrl_scale=2, remove_last=False)

    index = tkgPart.build_module(module_type="finger",
                              side=s, part="index",
            guide_list=["proxy_Index_01" + fs, "proxy_Index_02" + fs, "proxy_Index_03" + fs],
            ctrl_scale=2, remove_last=False)

    thumb = tkgPart.build_module(module_type="finger",
                              side=s, part="thumb",
            guide_list=["proxy_Thumb_01" + fs, "proxy_Thumb_02" + fs, "proxy_Thumb_03" + fs],
            ctrl_scale=2, remove_last=False)
