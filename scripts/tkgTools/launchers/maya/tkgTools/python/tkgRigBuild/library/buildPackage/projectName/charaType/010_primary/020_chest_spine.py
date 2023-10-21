# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
reload(tkgPart)
reload(tkgModule)
rigModule = tkgModule.RigModule()

chest = tkgPart.build_module(module_type="chest", side="Cn", part="chest", guide_list=["proxy_Spine3"])

spine = tkgPart.build_module(module_type="spine",
                            side="Cn",
                            part="spine",
                            guide_list=["proxy_Hip",
                                        "proxy_Spine1",
                                        "proxy_Spine2",
                                        "proxy_Spine3"],
                            ctrl_scale=1)
