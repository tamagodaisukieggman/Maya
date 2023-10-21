# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
reload(tkgPart)
reload(tkgModule)
rigModule = tkgModule.RigModule()

hip = tkgPart.build_module(module_type="hip", side="Cn", part="hip", guide_list=["proxy_Hip"], offset_hip=-0.5)
