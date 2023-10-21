# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
dir_path = dir.replace('\\', '/')
data_path = dir_path.replace(dir_path.split('/')[-1], '000_data')

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
reload(tkgPart)
reload(tkgModule)
rigModule = tkgModule.RigModule()


mp = "C:/Users/kesun/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/p2/p2_sotai01.ma"
gp = "{}biped_guide_000.ma".format(data_path)

print(gp)

cmds.file(new=True, f=True)

tkgPart.build_module(module_type="root",
                    side="Cn",
                    part="root",
                    model_path=mp,
                    guide_path=gp)
