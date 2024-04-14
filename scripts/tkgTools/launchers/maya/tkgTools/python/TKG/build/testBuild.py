# -*- coding: utf-8 -*-
from imp import reload

######################################
# For Limb
######################################
# ik module
import TKG.modules.ikModule as tkgIkModule
reload(tkgIkModule)

ikMod = tkgIkModule.Build('Lt', 'arm')
ikMod.create_ik_limb()

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
reload(tkgNodes)

nodes = cmds.ls(os=True)
surface = tkgNodes.create_loft_from_curves(nodes=nodes, offset=[5,0,0])

surface = 'loftedSurface1'
nodes = cmds.ls(os=True)
for node in nodes:
    tkgNodes.closest_follicle_on_surface(node, surface)