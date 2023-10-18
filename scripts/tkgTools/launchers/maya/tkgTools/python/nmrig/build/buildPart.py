# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload

import nmrig.build.parts.root as nmRoot
import nmrig.build.parts.hip as nmHip
import nmrig.build.parts.chest as nmChest
# import nmrig.build.parts.fkChain as nmFkChain
# import nmrig.build.parts.ikChain as nmIkChain
import nmrig.build.parts.bipedLimb as nmLimb
import nmrig.build.parts.clavicle as nmClavicle
import nmrig.build.parts.spine as nmSpine
import nmrig.build.parts.neck as nmNeck
import nmrig.build.parts.head as nmHead
import nmrig.build.parts.hand as nmHand
import nmrig.build.parts.finger as nmFinger
import nmrig.build.parts.foot as nmFoot
# import nmrig.build.parts.eyes as nmEyes
import nmrig.libs.attribute as nmAttr
reload(nmRoot)
reload(nmHip)
reload(nmChest)
# reload(nmFkChain)
# reload(nmIkChain)
reload(nmLimb)
reload(nmClavicle)
reload(nmSpine)
reload(nmNeck)
reload(nmHead)
reload(nmHand)
reload(nmFinger)
reload(nmFoot)
# reload(nmEyes)
reload(nmAttr)

""" Build Command
import maya.cmds as cmds
from imp import reload
import nmrig.build.buildPart as nmPart
import nmrig.build.rigModule as nmModule
reload(nmPart)
reload(nmModule)
rigModule = nmModule.RigModule()

mp = "C:/Users/kesun/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/p2/p2_sotai01.ma"
gp = "C:/Users/kesun/Documents/maya/scripts/tkgTools/tkgRig/scripts/build/types/biped/wizard2_base_00_000/000_data/chr0006_proxy_joints.ma"

cmds.file(new=True, f=True)

nmPart.build_module(module_type="root",
                    side="Cn",
                    part="root",
                    model_path=mp,
                    guide_path=gp)

cmds.viewFit("perspShape", fitFactor=1, all=True, animate=True)


hip = nmPart.build_module(module_type="hip", side="Cn", part="hip",
            guide_list=["proxy_Hip"], offset_hip=-0.5)

chest = nmPart.build_module(module_type="chest", side="Cn", part="chest",
            guide_list=["proxy_Spine3"])

spine = nmPart.build_module(module_type="spine",
                            side="Cn",
                            part="spine",
                            guide_list=["proxy_Hip",
                                        "proxy_Spine1",
                                        "proxy_Spine2",
                                        "proxy_Spine3"],
                            ctrl_scale=1)

neck = nmPart.build_module(module_type="neck",
                            side="Cn",
                            part="neck",
                            guide_list=["proxy_Neck",
                                        "proxy_Head"],
                            ctrl_scale=1)

head = nmPart.build_module(module_type="head",
                            side="Cn",
                            part="head",
                            guide_list=["proxy_Head"],
                            ctrl_scale=5)

for s in ['Lf', 'Rt']:
    if s == 'Lf':
        fs = '_L'
    else:
        fs = '_R'

    arm = nmPart.build_module(module_type="bipedLimb",
                              side=s, part="arm",
            guide_list=["proxy_Arm" + fs, "proxy_Elbow" + fs, "proxy_Wrist" + fs])

    clavicle = nmPart.build_module(module_type="clavicle",
                              side=s, part="clavicle",
            guide_list=["proxy_Shoulder" + fs, "proxy_Arm" + fs],
            local_orient=True,
            ctrl_scale=9)

    leg = nmPart.build_module(module_type="bipedLimb",
                              side=s, part="leg",
            guide_list=["proxy_Thigh" + fs, "proxy_Knee" + fs, "proxy_Ankle" + fs],
            ctrl_scale=9)

    hand = nmPart.build_module(module_type="hand",
                              side=s, part="hand",
            guide_list=["proxy_Wrist" + fs],
            ctrl_scale=9)

    endJnt = rigModule.create_endJnt(base='proxy_Toe' + fs, wt=[0,0,5], awt_obj=None)
    foot = nmPart.build_module(module_type="foot",
                              side=s, part="foot",
            guide_list=["proxy_Ankle" + fs, "proxy_Toe" + fs, endJnt],
            ctrl_scale=9)

    pinky = nmPart.build_module(module_type="finger",
                              side=s, part="pinky",
            guide_list=["proxy_Pinky_01" + fs, "proxy_Pinky_02" + fs, "proxy_Pinky_03" + fs],
            ctrl_scale=2, remove_last=False)

    ring = nmPart.build_module(module_type="finger",
                              side=s, part="ring",
            guide_list=["proxy_Ring_01" + fs, "proxy_Ring_02" + fs, "proxy_Ring_03" + fs],
            ctrl_scale=2, remove_last=False)

    middle = nmPart.build_module(module_type="finger",
                              side=s, part="middle",
            guide_list=["proxy_Middle_01" + fs, "proxy_Middle_02" + fs, "proxy_Middle_03" + fs],
            ctrl_scale=2, remove_last=False)

    index = nmPart.build_module(module_type="finger",
                              side=s, part="index",
            guide_list=["proxy_Index_01" + fs, "proxy_Index_02" + fs, "proxy_Index_03" + fs],
            ctrl_scale=2, remove_last=False)

    thumb = nmPart.build_module(module_type="finger",
                              side=s, part="thumb",
            guide_list=["proxy_Thumb_01" + fs, "proxy_Thumb_02" + fs, "proxy_Thumb_03" + fs],
            ctrl_scale=2, remove_last=False)


import nmrig.post.finalize as nmFinalize
reload(nmFinalize)

# nmFinalize.add_color_attributes()
# nmFinalize.add_switch_ctrl()
# nmFinalize.add_vis_ctrl()
# nmFinalize.assemble_skeleton()
# nmFinalize.assemble_rig()
# nmFinalize.add_global_scale()
# nmFinalize.add_rig_sets()

nmFinalize.finalize_rig()

"""

# MODULE_DICT = {"root": nmRoot.Root,
#                "hip": nmHip.Hip,
#                "chest": nmChest.Chest,
#                "fk": nmFkChain.FkChain,
#                "ik": nmIkChain.IkChain,
#                "bipedLimb": nmLimb.BipedLimb,
#                "clavicle": nmClavicle.Clavicle,
#                "spine": nmSpine.Spine,
#                "neck": nmNeck.Neck,
#                "head": nmHead.Head,
#                "hand": nmHand.Hand,
#                "finger": nmFinger.Finger,
#                "foot": nmFoot.Foot,
#                "eyes": nmEyes.Eyes}

MODULE_DICT = {"root": nmRoot.Root,
               "hip": nmHip.Hip,
               "chest": nmChest.Chest,
               "finger": nmFinger.Finger,
               "bipedLimb": nmLimb.BipedLimb,
               "clavicle": nmClavicle.Clavicle,
               "hand": nmHand.Hand,
               "foot": nmFoot.Foot,
               "spine": nmSpine.Spine,
               "neck": nmNeck.Neck,
               "head": nmHead.Head}

def build_module(module_type, **kwargs):
    module = MODULE_DICT[module_type](**kwargs)

    nmAttr.Attribute(node=module.part_grp,
                     type="string",
                     name="moduleType",
                     value=module_type,
                     lock=True)

    cmds.refresh()
    return module
