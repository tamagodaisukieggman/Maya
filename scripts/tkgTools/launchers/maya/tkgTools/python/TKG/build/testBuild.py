# -*- coding: utf-8 -*-
from imp import reload

######################################
# For Limb
######################################
# ik limb
import TKG.modules.ikModule as tkgIkModule
reload(tkgIkModule)

ikMod = tkgIkModule.Build('Lt', 'arm')
ikMod.create_ik_limb()

# ik spline
import TKG.modules.ikModule as tkgIkModule
reload(tkgIkModule)

ikMod = tkgIkModule.Build('Lt', 'arm')
ikMod.create_ik_spline()

# fk module
import TKG.modules.fkModule as tkgFkModule
reload(tkgFkModule)

fkMod = tkgFkModule.Build('Lt', 'arm')
fkMod.create_fk_limb()

# bendy module
import TKG.modules.bendyModule as tkgBendyModule
reload(tkgBendyModule)

bendyMod = tkgBendyModule.Build('Lt', 'arm')
bendyMod.create_bendy_limb()

# blend module
import TKG.modules.blendModule as tkgBlendModule
reload(tkgBlendModule)

blendMod = tkgBlendModule.Build('Lt', 'arm')
blendMod.create_blend_limb()


######################################
# For Ribbon
######################################
# ribbon module

import TKG.nodes as tkgNodes
import TKG.modules.ribbonModule as tkgRibbonModule
reload(tkgNodes)
reload(tkgRibbonModule)

nodes = cmds.ls(os=True)

ribbonMod = tkgRibbonModule.Build('Lt', 'arm')
ribbonMod.create_ribbon(nodes)
