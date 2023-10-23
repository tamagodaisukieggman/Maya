# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.post.finalize as tkgFinalize
reload(tkgPart)
reload(tkgModule)
reload(tkgFinalize)
rigModule = tkgModule.RigModule()

rep_build_file = build_file.replace('\\', '/')
data_path = '{}/{}'.format('/'.join(rep_build_file.split('/')[:-2]), '000_data')

mp = "C:/Users/kesun/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/p2/p2_sotai01.ma"
gp = "{}/biped_guide_000.ma".format(data_path)


tkgPart.build_module(module_type="root", side="Cn", part="root", global_name='global',
                root_01_name='world',
                root_02_name='local', model_path=mp, guide_path=gp)

cmds.viewFit("perspShape", fitFactor=1, all=True, animate=True)

hip = tkgPart.build_module(module_type="hip", side="Cn", part="hip", guide_list=["proxy_Hip"])

chest = tkgPart.build_module(module_type="chest", side="Cn", part="chest", guide_list=["proxy_Spine3"])

spine = tkgPart.build_module(module_type="spine",
                            side="Cn",
                            part="spine",
                            local_ctrl=False,
                            joint_num=4,
                            guide_list=["proxy_Hip",
                                        "proxy_Spine1",
                                        "proxy_Spine2",
                                        "proxy_Spine3"],
                            ctrl_scale=10)

neck = tkgPart.build_module(module_type="neck",
                            side="Cn",
                            part="neck",
                            guide_list=["proxy_Neck",
                                        "proxy_Head"],
                            ctrl_scale=10)

head = tkgPart.build_module(module_type="head",
                            side="Cn",
                            part="head",
                            guide_list=["proxy_Head"],
                            ctrl_scale=40)

sides = ['Lf', 'Rt']
force_sides = ['_L', '_R']

for s, fs in zip(sides, force_sides):
    if fs == '_L':
        edge_axis = '-x'
    else:
        edge_axis = 'x'

    arm = tkgPart.build_module(module_type="bipedLimb",
                              side=s, part="arm",
            guide_list=["proxy_Arm" + fs, "proxy_Elbow" + fs, "proxy_Wrist" + fs],
            ctrl_scale=9, fk_ctrl_edge_axis=edge_axis,
            pv_guide='proxy_Elbow{}_match_loc'.format(fs))

    clavicle = tkgPart.build_module(module_type="clavicle",
                              side=s, part="clavicle",
            guide_list=["proxy_Shoulder" + fs, "proxy_Arm" + fs],
            local_orient=True,
            ctrl_scale=9)

    hand = tkgPart.build_module(module_type="hand",
                              side=s, part="hand",
            guide_list=["proxy_Wrist" + fs],
            ctrl_scale=10)

for s, fs in zip(sides, force_sides):
    if fs == '_L':
        edge_axis = '-x'
    else:
        edge_axis = 'x'

    leg = tkgPart.build_module(module_type="bipedLimb",
                              side=s, part="leg",
            guide_list=["proxy_Thigh" + fs, "proxy_Knee" + fs, "proxy_Ankle" + fs],
            ctrl_scale=9, fk_ctrl_edge_axis=edge_axis,
            pv_guide='proxy_Knee{}_match_loc'.format(fs))

    endJnt = rigModule.create_endJnt(base='proxy_Toe' + fs, wt=[0,0,5], awt_obj=None)
    foot = tkgPart.build_module(module_type="foot",
                              side=s, part="foot",
            guide_list=["proxy_Ankle" + fs, "proxy_Toe" + fs, endJnt],
            ctrl_scale=9)

for s, fs in zip(sides, force_sides):
    if fs == '_L':
        edge_axis = '-x'
    else:
        edge_axis = 'x'

    pinky = tkgPart.build_module(module_type="finger",
                              side=s, part="pinky",
            guide_list=["proxy_Pinky_01" + fs, "proxy_Pinky_02" + fs, "proxy_Pinky_03" + fs],
            ctrl_scale=2, remove_last=False, fk_ctrl_edge_axis=edge_axis,)

    ring = tkgPart.build_module(module_type="finger",
                              side=s, part="ring",
            guide_list=["proxy_Ring_01" + fs, "proxy_Ring_02" + fs, "proxy_Ring_03" + fs],
            ctrl_scale=2, remove_last=False, fk_ctrl_edge_axis=edge_axis,)

    middle = tkgPart.build_module(module_type="finger",
                              side=s, part="middle",
            guide_list=["proxy_Middle_01" + fs, "proxy_Middle_02" + fs, "proxy_Middle_03" + fs],
            ctrl_scale=2, remove_last=False, fk_ctrl_edge_axis=edge_axis,)

    index = tkgPart.build_module(module_type="finger",
                              side=s, part="index",
            guide_list=["proxy_Index_01" + fs, "proxy_Index_02" + fs, "proxy_Index_03" + fs],
            ctrl_scale=2, remove_last=False, fk_ctrl_edge_axis=edge_axis,)

    thumb = tkgPart.build_module(module_type="finger",
                              side=s, part="thumb",
            guide_list=["proxy_Thumb_01" + fs, "proxy_Thumb_02" + fs, "proxy_Thumb_03" + fs],
            ctrl_scale=2, remove_last=False, fk_ctrl_edge_axis=edge_axis,)


# tkgFinalize.add_color_attributes()
# tkgFinalize.add_switch_ctrl()
# tkgFinalize.add_vis_ctrl()
# tkgFinalize.assemble_skeleton()

# tkgFinalize.assemble_rig()

# tkgFinalize.add_global_scale()
# tkgFinalize.add_rig_sets()

tkgFinalize.finalize_rig()
