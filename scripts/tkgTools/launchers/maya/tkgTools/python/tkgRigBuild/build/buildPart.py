# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.parts.root as tkgRoot
import tkgRigBuild.build.parts.hip as tkgHip
import tkgRigBuild.build.parts.chest as tkgChest
import tkgRigBuild.build.parts.fkChain as tkgFkChain
import tkgRigBuild.build.parts.ikChain as tkgIkChain
import tkgRigBuild.build.parts.bipedLimb as tkgLimb
import tkgRigBuild.build.parts.clavicle as tkgClavicle
import tkgRigBuild.build.parts.spine as tkgSpine
import tkgRigBuild.build.parts.neck as tkgNeck
import tkgRigBuild.build.parts.head as tkgHead
import tkgRigBuild.build.parts.hand as tkgHand
import tkgRigBuild.build.parts.finger as tkgFinger
import tkgRigBuild.build.parts.foot as tkgFoot
import tkgRigBuild.build.parts.eyes as tkgEyes
import tkgRigBuild.libs.attribute as tkgAttr
reload(tkgRoot)
reload(tkgHip)
reload(tkgChest)
reload(tkgFkChain)
reload(tkgIkChain)
reload(tkgLimb)
reload(tkgClavicle)
reload(tkgSpine)
reload(tkgNeck)
reload(tkgHead)
reload(tkgHand)
reload(tkgFinger)
reload(tkgFoot)
reload(tkgEyes)
reload(tkgAttr)

MODULE_DICT = {"root": tkgRoot.Root,
               "hip": tkgHip.Hip,
               "chest": tkgChest.Chest,
               'fk': tkgFkChain.FkChain,
               'ik': tkgIkChain.IkChain,
               "finger": tkgFinger.Finger,
               "bipedLimb": tkgLimb.BipedLimb,
               "clavicle": tkgClavicle.Clavicle,
               "hand": tkgHand.Hand,
               "foot": tkgFoot.Foot,
               "spine": tkgSpine.Spine,
               "neck": tkgNeck.Neck,
               "head": tkgHead.Head,
               "eyes":tkgEyes.Eyes}

def build_module(module_type, **kwargs):
    module = MODULE_DICT[module_type](**kwargs)

    tkgAttr.Attribute(node=module.part_grp,
                     type="string",
                     name="moduleType",
                     value=module_type,
                     lock=True)

    cmds.refresh()
    return module
