# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.parts.root as tkgRoot
import tkgRigBuild.build.parts.hip as tkgHip
import tkgRigBuild.build.parts.chest as tkgChest
# import tkgRigBuild.build.parts.fkChain as tkgFkChain
# import tkgRigBuild.build.parts.ikChain as tkgIkChain
import tkgRigBuild.build.parts.bipedLimb as tkgLimb
import tkgRigBuild.build.parts.clavicle as tkgClavicle
import tkgRigBuild.build.parts.spine as tkgSpine
import tkgRigBuild.build.parts.neck as tkgNeck
import tkgRigBuild.build.parts.head as tkgHead
import tkgRigBuild.build.parts.hand as tkgHand
import tkgRigBuild.build.parts.finger as tkgFinger
import tkgRigBuild.build.parts.foot as tkgFoot
# import tkgRigBuild.build.parts.eyes as tkgEyes
import tkgRigBuild.libs.attribute as tkgAttr
reload(tkgRoot)
reload(tkgHip)
reload(tkgChest)
# reload(tkgFkChain)
# reload(tkgIkChain)
reload(tkgLimb)
reload(tkgClavicle)
reload(tkgSpine)
reload(tkgNeck)
reload(tkgHead)
reload(tkgHand)
reload(tkgFinger)
reload(tkgFoot)
# reload(tkgEyes)
reload(tkgAttr)

""" Build Command
import maya.cmds as cmds
from imp import reload
import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
reload(tkgPart)
reload(tkgModule)
rigModule = tkgModule.RigModule()

mp = "C:/Users/kesun/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/p2/p2_sotai01.ma"
gp = "C:/Users/kesun/Documents/maya/scripts/tkgTools/tkgRig/scripts/build/types/biped/wizard2_base_00_000/000_data/chr0006_proxy_joints.ma"

cmds.file(new=True, f=True)

tkgPart.build_module(module_type="root",
                    side="Cn",
                    part="root",
                    model_path=mp,
                    guide_path=gp)

cmds.viewFit("perspShape", fitFactor=1, all=True, animate=True)


hip = tkgPart.build_module(module_type="hip", side="Cn", part="hip",
            guide_list=["proxy_Hip"], offset_hip=-0.5)

chest = tkgPart.build_module(module_type="chest", side="Cn", part="chest",
            guide_list=["proxy_Spine3"])

spine = tkgPart.build_module(module_type="spine",
                            side="Cn",
                            part="spine",
                            guide_list=["proxy_Hip",
                                        "proxy_Spine1",
                                        "proxy_Spine2",
                                        "proxy_Spine3"],
                            ctrl_scale=1)

neck = tkgPart.build_module(module_type="neck",
                            side="Cn",
                            part="neck",
                            guide_list=["proxy_Neck",
                                        "proxy_Head"],
                            ctrl_scale=1)

head = tkgPart.build_module(module_type="head",
                            side="Cn",
                            part="head",
                            guide_list=["proxy_Head"],
                            ctrl_scale=5)

for s in ['Lf', 'Rt']:
    if s == 'Lf':
        fs = '_L'
    else:
        fs = '_R'

    arm = tkgPart.build_module(module_type="bipedLimb",
                              side=s, part="arm",
            guide_list=["proxy_Arm" + fs, "proxy_Elbow" + fs, "proxy_Wrist" + fs])

    clavicle = tkgPart.build_module(module_type="clavicle",
                              side=s, part="clavicle",
            guide_list=["proxy_Shoulder" + fs, "proxy_Arm" + fs],
            local_orient=True,
            ctrl_scale=9)

    leg = tkgPart.build_module(module_type="bipedLimb",
                              side=s, part="leg",
            guide_list=["proxy_Thigh" + fs, "proxy_Knee" + fs, "proxy_Ankle" + fs],
            ctrl_scale=9)

    hand = tkgPart.build_module(module_type="hand",
                              side=s, part="hand",
            guide_list=["proxy_Wrist" + fs],
            ctrl_scale=9)

    endJnt = rigModule.create_endJnt(base='proxy_Toe' + fs, wt=[0,0,5], awt_obj=None)
    foot = tkgPart.build_module(module_type="foot",
                              side=s, part="foot",
            guide_list=["proxy_Ankle" + fs, "proxy_Toe" + fs, endJnt],
            ctrl_scale=9)

    pinky = tkgPart.build_module(module_type="finger",
                              side=s, part="pinky",
            guide_list=["proxy_Pinky_01" + fs, "proxy_Pinky_02" + fs, "proxy_Pinky_03" + fs],
            ctrl_scale=2, remove_last=False)

    ring = tkgPart.build_module(module_type="finger",
                              side=s, part="ring",
            guide_list=["proxy_Ring_01" + fs, "proxy_Ring_02" + fs, "proxy_Ring_03" + fs],
            ctrl_scale=2, remove_last=False)

    middle = tkgPart.build_module(module_type="finger",
                              side=s, part="middle",
            guide_list=["proxy_Middle_01" + fs, "proxy_Middle_02" + fs, "proxy_Middle_03" + fs],
            ctrl_scale=2, remove_last=False)

    index = tkgPart.build_module(module_type="finger",
                              side=s, part="index",
            guide_list=["proxy_Index_01" + fs, "proxy_Index_02" + fs, "proxy_Index_03" + fs],
            ctrl_scale=2, remove_last=False)

    thumb = tkgPart.build_module(module_type="finger",
                              side=s, part="thumb",
            guide_list=["proxy_Thumb_01" + fs, "proxy_Thumb_02" + fs, "proxy_Thumb_03" + fs],
            ctrl_scale=2, remove_last=False)


import tkgRigBuild.post.finalize as tkgFinalize
reload(tkgFinalize)

# tkgFinalize.add_color_attributes()
# tkgFinalize.add_switch_ctrl()
# tkgFinalize.add_vis_ctrl()
# tkgFinalize.assemble_skeleton()
# tkgFinalize.assemble_rig()
# tkgFinalize.add_global_scale()
# tkgFinalize.add_rig_sets()

tkgFinalize.finalize_rig()

"""

# MODULE_DICT = {"root": tkgRoot.Root,
#                "hip": tkgHip.Hip,
#                "chest": tkgChest.Chest,
#                "fk": tkgFkChain.FkChain,
#                "ik": tkgIkChain.IkChain,
#                "bipedLimb": tkgLimb.BipedLimb,
#                "clavicle": tkgClavicle.Clavicle,
#                "spine": tkgSpine.Spine,
#                "neck": tkgNeck.Neck,
#                "head": tkgHead.Head,
#                "hand": tkgHand.Hand,
#                "finger": tkgFinger.Finger,
#                "foot": tkgFoot.Foot,
#                "eyes": tkgEyes.Eyes}

MODULE_DICT = {"root": tkgRoot.Root,
               "hip": tkgHip.Hip,
               "chest": tkgChest.Chest,
               "finger": tkgFinger.Finger,
               "bipedLimb": tkgLimb.BipedLimb,
               "clavicle": tkgClavicle.Clavicle,
               "hand": tkgHand.Hand,
               "foot": tkgFoot.Foot,
               "spine": tkgSpine.Spine,
               "neck": tkgNeck.Neck,
               "head": tkgHead.Head}

def build_module(module_type, **kwargs):
    module = MODULE_DICT[module_type](**kwargs)

    tkgAttr.Attribute(node=module.part_grp,
                     type="string",
                     name="moduleType",
                     value=module_type,
                     lock=True)

    cmds.refresh()
    return module
