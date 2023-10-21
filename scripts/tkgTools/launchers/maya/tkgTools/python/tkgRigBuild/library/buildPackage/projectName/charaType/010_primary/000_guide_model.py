# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
reload(tkgPart)
reload(tkgModule)
rigModule = tkgModule.RigModule()

mp = "C:/Users/kesun/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/p2/p2_sotai01.ma"
gp = "F:/myTechData/Maya/scripts/tkgTools/launchers/maya/tkgTools/python/tkgRigBuild/library/guide/biped_guide_000.ma"

cmds.file(new=True, f=True)

tkgPart.build_module(module_type="root",
                    side="Cn",
                    part="root",
                    model_path=mp,
                    guide_path=gp)
