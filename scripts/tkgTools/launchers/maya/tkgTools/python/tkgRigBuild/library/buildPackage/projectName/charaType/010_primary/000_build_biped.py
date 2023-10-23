# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
reload(tkgPart)
reload(tkgModule)
rigModule = tkgModule.RigModule()

rep_build_file = build_file.replace('\\', '/')
data_path = '{}/{}'.format('/'.join(rep_build_file.split('/')[:-2]), '000_data')

mp = "C:/Users/kesun/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/p2/p2_sotai01.ma"
gp = "{}/biped_guide_000.ma".format(data_path)

tkgPart.build_module(module_type="root", side="Cn", part="root", global_name='global',
                root_01_name='world',
                root_02_name='local', model_path=mp, guide_path=gp)

cmds.viewFit("perspShape", fitFactor=1, all=True, animate=True)
