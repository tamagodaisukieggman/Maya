# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.post.finalize as tkgFinalize
reload(tkgPart)
reload(tkgModule)
reload(tkgFinalize)

# tkgFinalize.add_color_attributes()
# tkgFinalize.add_switch_ctrl()
# tkgFinalize.add_vis_ctrl()
# tkgFinalize.assemble_skeleton()
# tkgFinalize.assemble_rig()
# tkgFinalize.add_global_scale()
# tkgFinalize.add_rig_sets()

tkgFinalize.finalize_rig()
