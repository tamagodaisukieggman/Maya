# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
reload(tkgPart)
reload(tkgModule)
rigModule = tkgModule.RigModule()

neck = tkgPart.build_module(module_type="neck",
                            side="Cn",
                            part="neck",
                            guide_list=["proxy_Neck",
                                        "proxy_Head"],
                            ctrl_scale=10)

head = tkgPart.build_module(module_type="head",
                            side="Cn",
                            part="head",
                            guide_list=["proxy_Head"],
                            ctrl_scale=10)
