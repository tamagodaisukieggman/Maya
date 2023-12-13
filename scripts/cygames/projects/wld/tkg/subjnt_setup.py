# -*- coding: utf-8 -*-
from collections import OrderedDict

from maya import cmds, mel


delete_nodes = cmds.ls(type=['expression', 'blendWeighted', 'animCurve'])
try:
    cmds.delete(delete_nodes)
except:
    pass

# set mainjoint
mainjnt_dict = OrderedDict()

mainjnt_dict['armL_jnt'] = OrderedDict()
mainjnt_dict['armL_jnt']['parent'] = 'shoulderL_jnt'
mainjnt_dict['armL_jnt']['label'] = 'arm'
mainjnt_dict['armL_jnt']['pos'] = [14.3, 0.0, 0.0]
mainjnt_dict['armL_jnt']['rot'] = [0.0, 5.0, -50.0]
mainjnt_dict['armL_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['armR_jnt'] = OrderedDict()
mainjnt_dict['armR_jnt']['parent'] = 'shoulderR_jnt'
mainjnt_dict['armR_jnt']['label'] = 'arm'
mainjnt_dict['armR_jnt']['pos'] = [14.3, 0.0, 0.0]
mainjnt_dict['armR_jnt']['rot'] = [0.0, 5.0, 50.0]
mainjnt_dict['armR_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['camera_jnt'] = OrderedDict()
mainjnt_dict['camera_jnt']['parent'] = 'root_jnt'
mainjnt_dict['camera_jnt']['label'] = 'camera'
mainjnt_dict['camera_jnt']['pos'] = [0.0, 0.0, 0.0]
mainjnt_dict['camera_jnt']['rot'] = [0.0, 0.0, 0.0]
mainjnt_dict['camera_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['cog_jnt'] = OrderedDict()
mainjnt_dict['cog_jnt']['parent'] = 'root_jnt'
mainjnt_dict['cog_jnt']['label'] = 'cog'
mainjnt_dict['cog_jnt']['pos'] = [0.0, 103.4, 0.0]
mainjnt_dict['cog_jnt']['rot'] = [0.0, 0.0, 0.0]
mainjnt_dict['cog_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['footL_jnt'] = OrderedDict()
mainjnt_dict['footL_jnt']['parent'] = 'legL_jnt'
mainjnt_dict['footL_jnt']['label'] = 'foot'
mainjnt_dict['footL_jnt']['pos'] = [46.3, 0.0, 0.0]
mainjnt_dict['footL_jnt']['rot'] = [2.4, -2.4, 0.0]
mainjnt_dict['footL_jnt']['jo'] = [0.0, -60.0, 0.0]

mainjnt_dict['footR_jnt'] = OrderedDict()
mainjnt_dict['footR_jnt']['parent'] = 'legR_jnt'
mainjnt_dict['footR_jnt']['label'] = 'foot'
mainjnt_dict['footR_jnt']['pos'] = [46.3, 0.0, 0.0]
mainjnt_dict['footR_jnt']['rot'] = [-2.4, -2.4, 0.0]
mainjnt_dict['footR_jnt']['jo'] = [0.0, -60.0, 0.0]

mainjnt_dict['forearmL_jnt'] = OrderedDict()
mainjnt_dict['forearmL_jnt']['parent'] = 'armL_jnt'
mainjnt_dict['forearmL_jnt']['label'] = 'forearm'
mainjnt_dict['forearmL_jnt']['pos'] = [27.3, 0.0, 0.0]
mainjnt_dict['forearmL_jnt']['rot'] = [0.0, -15.8, 0.0]
mainjnt_dict['forearmL_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['forearmR_jnt'] = OrderedDict()
mainjnt_dict['forearmR_jnt']['parent'] = 'armR_jnt'
mainjnt_dict['forearmR_jnt']['label'] = 'forearm'
mainjnt_dict['forearmR_jnt']['pos'] = [27.3, 0.0, 0.0]
mainjnt_dict['forearmR_jnt']['rot'] = [0.0, -15.8, 0.0]
mainjnt_dict['forearmR_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['handL_jnt'] = OrderedDict()
mainjnt_dict['handL_jnt']['parent'] = 'forearmL_jnt'
mainjnt_dict['handL_jnt']['label'] = 'hand'
mainjnt_dict['handL_jnt']['pos'] = [25.8, 0.0, 0.0]
mainjnt_dict['handL_jnt']['rot'] = [0.0, 0.0, 0.0]
mainjnt_dict['handL_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['handR_jnt'] = OrderedDict()
mainjnt_dict['handR_jnt']['parent'] = 'forearmR_jnt'
mainjnt_dict['handR_jnt']['label'] = 'hand'
mainjnt_dict['handR_jnt']['pos'] = [25.8, 0.0, 0.0]
mainjnt_dict['handR_jnt']['rot'] = [0.0, 0.0, 0.0]
mainjnt_dict['handR_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['head_jnt'] = OrderedDict()
mainjnt_dict['head_jnt']['parent'] = 'neck_jnt'
mainjnt_dict['head_jnt']['label'] = 'head'
mainjnt_dict['head_jnt']['pos'] = [16.8, 0.0, 0.0]
mainjnt_dict['head_jnt']['rot'] = [0.0, 3.5, 0.0]
mainjnt_dict['head_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['hip_jnt'] = OrderedDict()
mainjnt_dict['hip_jnt']['parent'] = 'cog_jnt'
mainjnt_dict['hip_jnt']['label'] = 'hip'
mainjnt_dict['hip_jnt']['pos'] = [0.0, -0.1, 0.0]
mainjnt_dict['hip_jnt']['rot'] = [0.0, 0.0, 0.0]
mainjnt_dict['hip_jnt']['jo'] = [0.0, 0.0, -90.0]

mainjnt_dict['legL_jnt'] = OrderedDict()
mainjnt_dict['legL_jnt']['parent'] = 'uplegL_jnt'
mainjnt_dict['legL_jnt']['label'] = 'leg'
mainjnt_dict['legL_jnt']['pos'] = [38.6, 0.0, 0.0]
mainjnt_dict['legL_jnt']['rot'] = [0.0, 1.0, 0.0]
mainjnt_dict['legL_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['legR_jnt'] = OrderedDict()
mainjnt_dict['legR_jnt']['parent'] = 'uplegR_jnt'
mainjnt_dict['legR_jnt']['label'] = 'leg'
mainjnt_dict['legR_jnt']['pos'] = [38.6, 0.0, 0.0]
mainjnt_dict['legR_jnt']['rot'] = [0.0, 1.0, 0.0]
mainjnt_dict['legR_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['neck_jnt'] = OrderedDict()
mainjnt_dict['neck_jnt']['parent'] = 'spine_03_jnt'
mainjnt_dict['neck_jnt']['label'] = 'neck'
mainjnt_dict['neck_jnt']['pos'] = [15.8, 0.0, 0.0]
mainjnt_dict['neck_jnt']['rot'] = [0.0, -16.5, 0.0]
mainjnt_dict['neck_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['root_jnt'] = OrderedDict()
mainjnt_dict['root_jnt']['parent'] = 'None'
mainjnt_dict['root_jnt']['label'] = 'root'
mainjnt_dict['root_jnt']['pos'] = [0.0, 0.0, 0.0]
mainjnt_dict['root_jnt']['rot'] = [0.0, 0.0, 0.0]
mainjnt_dict['root_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['shoulderL_jnt'] = OrderedDict()
mainjnt_dict['shoulderL_jnt']['parent'] = 'spine_03_jnt'
mainjnt_dict['shoulderL_jnt']['label'] = 'shoulder'
mainjnt_dict['shoulderL_jnt']['pos'] = [11.7, -2.7, 0.0]
mainjnt_dict['shoulderL_jnt']['rot'] = [0.0, 13.0, 0.73]
mainjnt_dict['shoulderL_jnt']['jo'] = [0.0, 0.0, -90.0]

mainjnt_dict['shoulderR_jnt'] = OrderedDict()
mainjnt_dict['shoulderR_jnt']['parent'] = 'spine_03_jnt'
mainjnt_dict['shoulderR_jnt']['label'] = 'shoulder'
mainjnt_dict['shoulderR_jnt']['pos'] = [11.7, 2.7, 0.0]
mainjnt_dict['shoulderR_jnt']['rot'] = [0.0, 13.0, -0.73]
mainjnt_dict['shoulderR_jnt']['jo'] = [0.0, 0.0, 90.0]

mainjnt_dict['spine_01_jnt'] = OrderedDict()
mainjnt_dict['spine_01_jnt']['parent'] = 'cog_jnt'
mainjnt_dict['spine_01_jnt']['label'] = 'spine_01'
mainjnt_dict['spine_01_jnt']['pos'] = [0.0, 0.1, 0.0]
mainjnt_dict['spine_01_jnt']['rot'] = [0.0, -2.8, 0.0]
mainjnt_dict['spine_01_jnt']['jo'] = [0.0, 0.0, 90.0]

mainjnt_dict['spine_02_jnt'] = OrderedDict()
mainjnt_dict['spine_02_jnt']['parent'] = 'spine_01_jnt'
mainjnt_dict['spine_02_jnt']['label'] = 'spine_02'
mainjnt_dict['spine_02_jnt']['pos'] = [15.4, 0.0, 0.0]
mainjnt_dict['spine_02_jnt']['rot'] = [0.0, 4.5, 0.0]
mainjnt_dict['spine_02_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['spine_03_jnt'] = OrderedDict()
mainjnt_dict['spine_03_jnt']['parent'] = 'spine_02_jnt'
mainjnt_dict['spine_03_jnt']['label'] = 'spine_03'
mainjnt_dict['spine_03_jnt']['pos'] = [15.0, 0.0, 0.0]
mainjnt_dict['spine_03_jnt']['rot'] = [0.0, 9.4, 0.0]
mainjnt_dict['spine_03_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['toebaseL_jnt'] = OrderedDict()
mainjnt_dict['toebaseL_jnt']['parent'] = 'footL_jnt'
mainjnt_dict['toebaseL_jnt']['label'] = 'toebase'
mainjnt_dict['toebaseL_jnt']['pos'] = [15.7, 0.0, 0.0]
mainjnt_dict['toebaseL_jnt']['rot'] = [0.0, 1.6, 0.0]
mainjnt_dict['toebaseL_jnt']['jo'] = [0.0, -30.0, 0.0]

mainjnt_dict['toebaseR_jnt'] = OrderedDict()
mainjnt_dict['toebaseR_jnt']['parent'] = 'footR_jnt'
mainjnt_dict['toebaseR_jnt']['label'] = 'toebase'
mainjnt_dict['toebaseR_jnt']['pos'] = [15.7, 0.0, 0.0]
mainjnt_dict['toebaseR_jnt']['rot'] = [0.0, 1.6, 0.0]
mainjnt_dict['toebaseR_jnt']['jo'] = [0.0, -30.0, 0.0]

mainjnt_dict['uplegL_jnt'] = OrderedDict()
mainjnt_dict['uplegL_jnt']['parent'] = 'hip_jnt'
mainjnt_dict['uplegL_jnt']['label'] = 'upleg'
mainjnt_dict['uplegL_jnt']['pos'] = [7.8, 10.5, -1.7]
mainjnt_dict['uplegL_jnt']['rot'] = [0.0, 1.5, -2.0]
mainjnt_dict['uplegL_jnt']['jo'] = [0.0, 0.0, 0.0]

mainjnt_dict['uplegR_jnt'] = OrderedDict()
mainjnt_dict['uplegR_jnt']['parent'] = 'hip_jnt'
mainjnt_dict['uplegR_jnt']['label'] = 'upleg'
mainjnt_dict['uplegR_jnt']['pos'] = [7.8, -10.5, -1.7]
mainjnt_dict['uplegR_jnt']['rot'] = [0.0, 1.5, 2.0]
mainjnt_dict['uplegR_jnt']['jo'] = [0.0, 0.0, 0.0]


cmds.select(cl=1)
for obj, inf in mainjnt_dict.items():
    cmds.setAttr('{}.type'.format(obj), 18)
    cmds.setAttr('{}.otherType'.format(obj), inf['label'], type='string')

    cmds.xform(obj, t=inf['pos'], ro=inf['rot'])
    cmds.setAttr('{}.jo'.format(obj), *inf['jo'])

# Create sub Joints
subjnt_dict = OrderedDict()

subjnt_dict['armL_bend_subjnt'] = OrderedDict()
subjnt_dict['armL_bend_subjnt']['parent'] = 'shoulderL_jnt'
subjnt_dict['armL_bend_subjnt']['label'] = 'arm_bend'
subjnt_dict['armL_bend_subjnt']['pos'] = [14.3, 0.0, 0.0]
subjnt_dict['armL_bend_subjnt']['rot'] = [0.0, 0.0, -22.5]
subjnt_dict['armL_bend_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['armL_fwd_subjnt'] = OrderedDict()
# subjnt_dict['armL_fwd_subjnt']['parent'] = 'armL_bend_subjnt'
# subjnt_dict['armL_fwd_subjnt']['label'] = 'arm_fwd'
# subjnt_dict['armL_fwd_subjnt']['pos'] = [2.584, -3.516, 8.269]
# subjnt_dict['armL_fwd_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['armL_fwd_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['armL_out_subjnt'] = OrderedDict()
# subjnt_dict['armL_out_subjnt']['parent'] = 'armL_bend_subjnt'
# subjnt_dict['armL_out_subjnt']['label'] = 'arm_out'
# subjnt_dict['armL_out_subjnt']['pos'] = [1.748, 5.616, 0.498]
# subjnt_dict['armL_out_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['armL_out_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['armL_twist_subjnt'] = OrderedDict()
subjnt_dict['armL_twist_subjnt']['parent'] = 'armL_jnt'
subjnt_dict['armL_twist_subjnt']['label'] = 'arm_twist'
subjnt_dict['armL_twist_subjnt']['pos'] = [18.335, 0.0, 0.0]
subjnt_dict['armL_twist_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['armL_twist_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['armR_bend_subjnt'] = OrderedDict()
subjnt_dict['armR_bend_subjnt']['parent'] = 'shoulderR_jnt'
subjnt_dict['armR_bend_subjnt']['label'] = 'arm_bend'
subjnt_dict['armR_bend_subjnt']['pos'] = [14.3, 0.0, 0.0]
subjnt_dict['armR_bend_subjnt']['rot'] = [0.0, 0.0, 22.5]
subjnt_dict['armR_bend_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['armR_fwd_subjnt'] = OrderedDict()
# subjnt_dict['armR_fwd_subjnt']['parent'] = 'armR_bend_subjnt'
# subjnt_dict['armR_fwd_subjnt']['label'] = 'arm_fwd'
# subjnt_dict['armR_fwd_subjnt']['pos'] = [2.584, 3.516, 8.269]
# subjnt_dict['armR_fwd_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['armR_fwd_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['armR_out_subjnt'] = OrderedDict()
# subjnt_dict['armR_out_subjnt']['parent'] = 'armR_bend_subjnt'
# subjnt_dict['armR_out_subjnt']['label'] = 'arm_out'
# subjnt_dict['armR_out_subjnt']['pos'] = [1.748, -5.616, 0.498]
# subjnt_dict['armR_out_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['armR_out_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['armR_twist_subjnt'] = OrderedDict()
subjnt_dict['armR_twist_subjnt']['parent'] = 'armR_jnt'
subjnt_dict['armR_twist_subjnt']['label'] = 'arm_twist'
subjnt_dict['armR_twist_subjnt']['pos'] = [18.335, 0.0, 0.0]
subjnt_dict['armR_twist_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['armR_twist_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['forearmL_bicep_subjnt'] = OrderedDict()
# subjnt_dict['forearmL_bicep_subjnt']['parent'] = 'armL_twist_subjnt'
# subjnt_dict['forearmL_bicep_subjnt']['label'] = 'forearm_bicep'
# subjnt_dict['forearmL_bicep_subjnt']['pos'] = [-1.376, -0.391, 6.042]
# subjnt_dict['forearmL_bicep_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['forearmL_bicep_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['forearmL_elbow_subjnt'] = OrderedDict()
subjnt_dict['forearmL_elbow_subjnt']['parent'] = 'forearmL_jnt'
subjnt_dict['forearmL_elbow_subjnt']['label'] = 'forearm_elbow'
subjnt_dict['forearmL_elbow_subjnt']['pos'] = [1.907, -0.194, -4.838]
subjnt_dict['forearmL_elbow_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['forearmL_elbow_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['forearmL_twist_subjnt'] = OrderedDict()
subjnt_dict['forearmL_twist_subjnt']['parent'] = 'forearmL_jnt'
subjnt_dict['forearmL_twist_subjnt']['label'] = 'forearm_twist'
subjnt_dict['forearmL_twist_subjnt']['pos'] = [13.366, 0.0, 0.0]
subjnt_dict['forearmL_twist_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['forearmL_twist_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['forearmR_bicep_subjnt'] = OrderedDict()
# subjnt_dict['forearmR_bicep_subjnt']['parent'] = 'armR_twist_subjnt'
# subjnt_dict['forearmR_bicep_subjnt']['label'] = 'forearm_bicep'
# subjnt_dict['forearmR_bicep_subjnt']['pos'] = [-1.376, 0.391, 6.042]
# subjnt_dict['forearmR_bicep_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['forearmR_bicep_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['forearmR_elbow_subjnt'] = OrderedDict()
subjnt_dict['forearmR_elbow_subjnt']['parent'] = 'forearmR_jnt'
subjnt_dict['forearmR_elbow_subjnt']['label'] = 'forearm_elbow'
subjnt_dict['forearmR_elbow_subjnt']['pos'] = [1.907, 0.194, -4.838]
subjnt_dict['forearmR_elbow_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['forearmR_elbow_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['forearmR_twist_subjnt'] = OrderedDict()
subjnt_dict['forearmR_twist_subjnt']['parent'] = 'forearmR_jnt'
subjnt_dict['forearmR_twist_subjnt']['label'] = 'forearm_twist'
subjnt_dict['forearmR_twist_subjnt']['pos'] = [13.366, 0.0, 0.0]
subjnt_dict['forearmR_twist_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['forearmR_twist_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['handL_bend_subjnt'] = OrderedDict()
subjnt_dict['handL_bend_subjnt']['parent'] = 'handL_jnt'
subjnt_dict['handL_bend_subjnt']['label'] = 'hand_bend'
subjnt_dict['handL_bend_subjnt']['pos'] = [0.0, 0.0, 0.0]
subjnt_dict['handL_bend_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['handL_bend_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['handL_slide_subjnt'] = OrderedDict()
# subjnt_dict['handL_slide_subjnt']['parent'] = 'handL_jnt'
# subjnt_dict['handL_slide_subjnt']['label'] = 'hand_slide'
# subjnt_dict['handL_slide_subjnt']['pos'] = [0.272, 2.846, -0.748]
# subjnt_dict['handL_slide_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['handL_slide_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['handR_bend_subjnt'] = OrderedDict()
subjnt_dict['handR_bend_subjnt']['parent'] = 'handR_jnt'
subjnt_dict['handR_bend_subjnt']['label'] = 'hand_bend'
subjnt_dict['handR_bend_subjnt']['pos'] = [0.0, 0.0, 0.0]
subjnt_dict['handR_bend_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['handR_bend_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['handR_slide_subjnt'] = OrderedDict()
# subjnt_dict['handR_slide_subjnt']['parent'] = 'handR_jnt'
# subjnt_dict['handR_slide_subjnt']['label'] = 'hand_slide'
# subjnt_dict['handR_slide_subjnt']['pos'] = [0.272, -2.846, -0.749]
# subjnt_dict['handR_slide_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['handR_slide_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['legL_out_subjnt'] = OrderedDict()
subjnt_dict['legL_out_subjnt']['parent'] = 'legL_jnt'
subjnt_dict['legL_out_subjnt']['label'] = 'leg_out'
subjnt_dict['legL_out_subjnt']['pos'] = [1.273, -1.139, 5.2]
subjnt_dict['legL_out_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['legL_out_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['legL_twist_subjnt'] = OrderedDict()
subjnt_dict['legL_twist_subjnt']['parent'] = 'legL_jnt'
subjnt_dict['legL_twist_subjnt']['label'] = 'leg_twist'
subjnt_dict['legL_twist_subjnt']['pos'] = [13.264, 0.0, 0.0]
subjnt_dict['legL_twist_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['legL_twist_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['legR_out_subjnt'] = OrderedDict()
subjnt_dict['legR_out_subjnt']['parent'] = 'legR_jnt'
subjnt_dict['legR_out_subjnt']['label'] = 'leg_out'
subjnt_dict['legR_out_subjnt']['pos'] = [1.273, 1.139, 5.2]
subjnt_dict['legR_out_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['legR_out_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['legR_twist_subjnt'] = OrderedDict()
subjnt_dict['legR_twist_subjnt']['parent'] = 'legR_jnt'
subjnt_dict['legR_twist_subjnt']['label'] = 'leg_twist'
subjnt_dict['legR_twist_subjnt']['pos'] = [13.264, 0.0, 0.0]
subjnt_dict['legR_twist_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['legR_twist_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['neck_twist_subjnt'] = OrderedDict()
# subjnt_dict['neck_twist_subjnt']['parent'] = 'neck_jnt'
# subjnt_dict['neck_twist_subjnt']['label'] = 'neck_twist'
# subjnt_dict['neck_twist_subjnt']['pos'] = [9.724, 0.0, 0.0]
# subjnt_dict['neck_twist_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['neck_twist_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['shoulderL_latis_subjnt'] = OrderedDict()
# subjnt_dict['shoulderL_latis_subjnt']['parent'] = 'shoulderL_jnt'
# subjnt_dict['shoulderL_latis_subjnt']['label'] = 'shoulder_latis'
# subjnt_dict['shoulderL_latis_subjnt']['pos'] = [5.097, -7.248, -12.529]
# subjnt_dict['shoulderL_latis_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['shoulderL_latis_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['shoulderL_pecto_subjnt'] = OrderedDict()
# subjnt_dict['shoulderL_pecto_subjnt']['parent'] = 'shoulderL_jnt'
# subjnt_dict['shoulderL_pecto_subjnt']['label'] = 'shoulder_pecto'
# subjnt_dict['shoulderL_pecto_subjnt']['pos'] = [3.83, -3.531, 9.89]
# subjnt_dict['shoulderL_pecto_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['shoulderL_pecto_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['shoulderL_trape_subjnt'] = OrderedDict()
# subjnt_dict['shoulderL_trape_subjnt']['parent'] = 'shoulderL_jnt'
# subjnt_dict['shoulderL_trape_subjnt']['label'] = 'shoulder_trape'
# subjnt_dict['shoulderL_trape_subjnt']['pos'] = [5.696, 9.564, -0.852]
# subjnt_dict['shoulderL_trape_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['shoulderL_trape_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['shoulderR_latis_subjnt'] = OrderedDict()
# subjnt_dict['shoulderR_latis_subjnt']['parent'] = 'shoulderR_jnt'
# subjnt_dict['shoulderR_latis_subjnt']['label'] = 'shoulder_latis'
# subjnt_dict['shoulderR_latis_subjnt']['pos'] = [5.097, 7.248, -12.529]
# subjnt_dict['shoulderR_latis_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['shoulderR_latis_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['shoulderR_pecto_subjnt'] = OrderedDict()
# subjnt_dict['shoulderR_pecto_subjnt']['parent'] = 'shoulderR_jnt'
# subjnt_dict['shoulderR_pecto_subjnt']['label'] = 'shoulder_pecto'
# subjnt_dict['shoulderR_pecto_subjnt']['pos'] = [3.83, 3.531, 9.89]
# subjnt_dict['shoulderR_pecto_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['shoulderR_pecto_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['shoulderR_trape_subjnt'] = OrderedDict()
# subjnt_dict['shoulderR_trape_subjnt']['parent'] = 'shoulderR_jnt'
# subjnt_dict['shoulderR_trape_subjnt']['label'] = 'shoulder_trape'
# subjnt_dict['shoulderR_trape_subjnt']['pos'] = [5.696, -9.564, -0.852]
# subjnt_dict['shoulderR_trape_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['shoulderR_trape_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['uplegL_bend_subjnt'] = OrderedDict()
subjnt_dict['uplegL_bend_subjnt']['parent'] = 'hip_jnt'
subjnt_dict['uplegL_bend_subjnt']['label'] = 'upleg_bend'
subjnt_dict['uplegL_bend_subjnt']['pos'] = [7.8, 10.5, -1.7]
subjnt_dict['uplegL_bend_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['uplegL_bend_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['uplegL_fwd_subjnt'] = OrderedDict()
# subjnt_dict['uplegL_fwd_subjnt']['parent'] = 'uplegL_bend_subjnt'
# subjnt_dict['uplegL_fwd_subjnt']['label'] = 'upleg_fwd'
# subjnt_dict['uplegL_fwd_subjnt']['pos'] = [3.405, -1.754, 9.472]
# subjnt_dict['uplegL_fwd_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['uplegL_fwd_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['uplegL_twist_subjnt'] = OrderedDict()
subjnt_dict['uplegL_twist_subjnt']['parent'] = 'uplegL_jnt'
subjnt_dict['uplegL_twist_subjnt']['label'] = 'upleg_twist'
subjnt_dict['uplegL_twist_subjnt']['pos'] = [20.26, 0.0, 0.0]
subjnt_dict['uplegL_twist_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['uplegL_twist_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['uplegR_bend_subjnt'] = OrderedDict()
subjnt_dict['uplegR_bend_subjnt']['parent'] = 'hip_jnt'
subjnt_dict['uplegR_bend_subjnt']['label'] = 'upleg_bend'
subjnt_dict['uplegR_bend_subjnt']['pos'] = [7.8, -10.5, -1.7]
subjnt_dict['uplegR_bend_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['uplegR_bend_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['uplegR_fwd_subjnt'] = OrderedDict()
# subjnt_dict['uplegR_fwd_subjnt']['parent'] = 'uplegR_bend_subjnt'
# subjnt_dict['uplegR_fwd_subjnt']['label'] = 'upleg_fwd'
# subjnt_dict['uplegR_fwd_subjnt']['pos'] = [3.405, 1.754, 9.472]
# subjnt_dict['uplegR_fwd_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['uplegR_fwd_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['uplegR_twist_subjnt'] = OrderedDict()
subjnt_dict['uplegR_twist_subjnt']['parent'] = 'uplegR_jnt'
subjnt_dict['uplegR_twist_subjnt']['label'] = 'upleg_twist'
subjnt_dict['uplegR_twist_subjnt']['pos'] = [20.26, 0.0, 0.0]
subjnt_dict['uplegR_twist_subjnt']['rot'] = [0.0, 0.0, 0.0]
subjnt_dict['uplegR_twist_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['armL_bck_subjnt'] = OrderedDict()
# subjnt_dict['armL_bck_subjnt']['parent'] = 'armL_bend_subjnt'
# subjnt_dict['armL_bck_subjnt']['label'] = 'arm_bck'
# subjnt_dict['armL_bck_subjnt']['pos'] = [2.992, -1.863, -8.219]
# subjnt_dict['armL_bck_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['armL_bck_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['armR_bck_subjnt'] = OrderedDict()
# subjnt_dict['armR_bck_subjnt']['parent'] = 'armR_bend_subjnt'
# subjnt_dict['armR_bck_subjnt']['label'] = 'arm_bck'
# subjnt_dict['armR_bck_subjnt']['pos'] = [2.992, 1.863, -8.219]
# subjnt_dict['armR_bck_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['armR_bck_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['footL_calf_subjnt'] = OrderedDict()
# subjnt_dict['footL_calf_subjnt']['parent'] = 'legL_twist_subjnt'
# subjnt_dict['footL_calf_subjnt']['label'] = 'foot_calf'
# subjnt_dict['footL_calf_subjnt']['pos'] = [-10.504, -1.385, -6.416]
# subjnt_dict['footL_calf_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['footL_calf_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['footR_calf_subjnt'] = OrderedDict()
# subjnt_dict['footR_calf_subjnt']['parent'] = 'legR_twist_subjnt'
# subjnt_dict['footR_calf_subjnt']['label'] = 'foot_calf'
# subjnt_dict['footR_calf_subjnt']['pos'] = [-10.504, 1.385, -6.416]
# subjnt_dict['footR_calf_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['footR_calf_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['uplegL_bck_subjnt'] = OrderedDict()
# subjnt_dict['uplegL_bck_subjnt']['parent'] = 'uplegL_bend_subjnt'
# subjnt_dict['uplegL_bck_subjnt']['label'] = 'upleg_bck'
# subjnt_dict['uplegL_bck_subjnt']['pos'] = [3.184, -3.118, -9.599]
# subjnt_dict['uplegL_bck_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['uplegL_bck_subjnt']['jo'] = [0.0, 0.0, 0.0]

# subjnt_dict['uplegR_bck_subjnt'] = OrderedDict()
# subjnt_dict['uplegR_bck_subjnt']['parent'] = 'uplegR_bend_subjnt'
# subjnt_dict['uplegR_bck_subjnt']['label'] = 'upleg_bck'
# subjnt_dict['uplegR_bck_subjnt']['pos'] = [3.184, 3.118, -9.599]
# subjnt_dict['uplegR_bck_subjnt']['rot'] = [0.0, 0.0, 0.0]
# subjnt_dict['uplegR_bck_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['shoulderL_bend_subjnt'] = OrderedDict()
subjnt_dict['shoulderL_bend_subjnt']['parent'] = 'spine_03_jnt'
subjnt_dict['shoulderL_bend_subjnt']['label'] = 'shoulder_bend'
subjnt_dict['shoulderL_bend_subjnt']['pos'] = [11.7, -2.7, 0.0]
subjnt_dict['shoulderL_bend_subjnt']['rot'] = [0.0, 13, 0.73]
subjnt_dict['shoulderL_bend_subjnt']['jo'] = [0.0, 0.0, 0.0]

subjnt_dict['shoulderR_bend_subjnt'] = OrderedDict()
subjnt_dict['shoulderR_bend_subjnt']['parent'] = 'spine_03_jnt'
subjnt_dict['shoulderR_bend_subjnt']['label'] = 'shoulder_bend'
subjnt_dict['shoulderR_bend_subjnt']['pos'] = [11.7, 2.7, 0.0]
subjnt_dict['shoulderR_bend_subjnt']['rot'] = [0.0, 13, -0.73]
subjnt_dict['shoulderR_bend_subjnt']['jo'] = [0.0, 0.0, 0.0]


cmds.select(cl=1)
for obj, inf in subjnt_dict.items():
    if not cmds.objExists(obj):
        cmds.createNode('joint', n=obj, ss=1)

    try:
        cmds.parent(obj, inf['parent'])
    except:
        pass

    cmds.setAttr('{}.type'.format(obj), 18)
    cmds.setAttr('{}.otherType'.format(obj), inf['label'], type='string')

for obj, inf in subjnt_dict.items():
    cmds.xform(obj, t=inf['pos'], ro=inf['rot'])
    cmds.setAttr('{}.jo'.format(obj), *inf['jo'])


# expressions
# arm
exp_name = 'subjnt_exp'
cmds.expression(s="""
proc float linear(float $input_x, float $sigma_val)
{
	return 1 - (($sigma_val - clamp(0.0, $sigma_val, $input_x)) / $sigma_val);
}

proc float cubic(float $input_x, float $sigma_val)
{
	$input_x /= $sigma_val;
	return 1 - max(1 - ($input_x * $input_x * $input_x), 0);
}

proc float gaussian(float $input_x, float $sigma_val)
{
	return 1 - exp(-$input_x * ((1.0 / $sigma_val) * (1.0 / $sigma_val)));
}

/*
proc float gaussian(float $input_x, float $center_u, float $sigma_val)
{
	float $total_num = ($input_x - $center_u) * ($input_x - $center_u);
	if ($sigma_val == 0.0)
	{
	return 0.0;
	}
	else
	{
	return exp(-$total_num / (2 * $sigma_val * $sigma_val));
	}
}
*/


////////////////////////////////////////////////////////////
// Quaternion
proc float convert_to_degrees(float $radians){
    float $pi = 3.1415927;
    float $result = $radians*180 / $pi;
    return $result;
}

proc float convert_to_radians(float $degrees){
    float $pi = 3.1415927;
    float $result = $degrees/180 * $pi;
    return $result;
}

proc float[] toQuaternion(float $yaw_z, float $pitch_y, float $roll_x, int $order){
    // yaw (Z), pitch (Y), roll (X)
    $yaw = convert_to_radians($yaw_z);
    $pitch = convert_to_radians($pitch_y);
    $roll = convert_to_radians($roll_x);

    float $qx = 0;
    float $qy = 0;
    float $qz = 0;
    float $qw = 0;

    float $qurt[];

    if ($order == 0){
		$qx += sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
        $qy += sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) + cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qz += cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) + sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }
    else if ($order == 1){
        $qx += sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
        $qy += cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5);
        $qz += cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) + sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) + sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }
    else if ($order == 2){
        $qx += sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) + cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
        $qy += cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5);
        $qz += cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) + sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }
    else if ($order == 3){
        $qx += sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) + cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
        $qy += sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) + cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qz += cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }
    else if ($order == 4){
        $qx += sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
        $qy += sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) + cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qz += cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) + sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }
    else if ($order == 5){
        $qx += cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5) + sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5);
        $qy += cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5);
        $qz += sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5) + cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }

    $qurt[0] = $qw;
    $qurt[1] = $qx;
    $qurt[2] = $qy;
    $qurt[3] = $qz;

    return $qurt;

}

proc float[] toEuler(float $quartw, float $quartx, float $quarty, float $quartz){
    float $euler[];

    // roll (x-axis rotation)
    float $sinr_cosp = 2 * ($quartw * $quartx + $quarty * $quartz);
    float $cosr_cosp = 1 - 2 * ($quartx * $quartx + $quarty * $quarty);

    $euler[0] = convert_to_degrees(atan2($sinr_cosp, $cosr_cosp));

    // pitch (y-axis rotation)
    float $sinp = 2 * ($quartw * $quarty - $quartz * $quartx);
    float $pi = 3.1415927;
    if (abs($sinp) >= 1){
        $euler[1] = convert_to_degrees(-1 * $pi / 2);
    }
    else{
        $euler[1] = convert_to_degrees(asin($sinp));
    }

    // yaw (z-axis rotation)
    float $siny_cosp = 2 * ($quartw * $quartz + $quartx * $quarty);
    float $cosy_cosp = 1 - 2 * ($quarty * $quarty + $quartz * $quartz);
    $euler[2] = convert_to_degrees(atan2($siny_cosp, $cosy_cosp));

    return $euler;
}

proc float crop_rotation(float $angle){
    if ($angle > 180){
        return $angle -360;
    }
    else if ($angle < -180){
        return $angle + 360;
    }
    else{
        return $angle;
    }
}

proc float[] quaternion_multiply(float $q0w, float $q0x, float $q0y, float $q0z, float $q1w, float $q1x, float $q1y, float $q1z){
	float $mm0 = -$q1x * $q0x - $q1y * $q0y - $q1z * $q0z + $q1w * $q0w;
	float $mm1 = $q1x * $q0w + $q1y * $q0z - $q1z * $q0y + $q1w * $q0x;
	float $mm2 = -$q1x * $q0z + $q1y * $q0w + $q1z * $q0x + $q1w * $q0y;
	float $mm3 = $q1x * $q0y - $q1y * $q0x + $q1z * $q0w + $q1w * $q0z;

	float $mm[];
	$mm[0] = $mm0;
	$mm[1] = $mm1;
	$mm[2] = $mm2;
	$mm[3] = $mm3;

	return $mm;

}

proc float dot_quaternion(float $q0w, float $q0x, float $q0y, float $q0z, float $q1w, float $q1x, float $q1y, float $q1z){
	float $dotValue = ($q0w * $q1w) + ($q0x * $q1x) + ($q0y * $q1y) + ($q0z * $q1z);
	if ($dotValue < -1.0){
		$dotValue = -1.0;
	}
	else if ($dotValue > 1.0){
		$dotValue = 1.0;
	}
	return $dotValue;
}


proc float[] quaternion_to_angle(float $qw, float $qx, float $qy, float $qz){
	float $angle_results[];
	float $angle = 2 * acos($qw);
	$angle_results[0] = convert_to_degrees($angle);

	float $s = sqrt(1-$qw*$qw);
	if ($s < 0.00000001) {
		$angle_results[1] = $qx;
		$angle_results[2] = $qy;
		$angle_results[3] = $qz;
	}
	else
	{
		$angle_results[1] = $qx / $s;
		$angle_results[2] = $qy / $s;
		$angle_results[3] = $qz / $s;
	}
	return $angle_results;
}


proc float[] angle_to_quaternion(float $angle, float $qx, float $qy, float $qz){
	float $s = sin($angle/2);
	float $q[];
	$q[0] = cos($angle/2);
	$q[1] = $qx * $s;
	$q[2] = $qy * $s;
	$q[3] = $qz * $s;
	return $q;
}


proc float[] quaternion_slerp(float $q0w, float $q0x, float $q0y, float $q0z, float $q1w, float $q1x, float $q1y, float $q1z, float $lambda){
	float $dotproduct = dot_quaternion($q0w, $q0x, $q0y, $q0z, $q1w, $q1x, $q1y, $q1z);

	$lambda=$lambda/2.0;

	float $theta = acos($dotproduct);
	if ($theta<0.0){
		$theta=-$theta;
	}

	float $st = sin($theta);
	float $sut = sin($lambda*$theta);
	float $sout = sin((1-$lambda)*$theta);
	float $coeff1 = $sout/$st;
	float $coeff2 = $sut/$st;

	float $qr[];

	$qr[0] = $coeff1*$q0w + $coeff2*$q1w;
	$qr[1] = $coeff1*$q0x + $coeff2*$q1x;
	$qr[2] = $coeff1*$q0y + $coeff2*$q1y;
	$qr[3] = $coeff1*$q0z + $coeff2*$q1z;

	return $qr;
}


proc float[] angleRot_from_rotToQuat(float $rx, float $ry, float $rz, float $order, float $slerp){
    float $quartd_A[] = toQuaternion($rz, $ry, $rx, 0);
    float $quat_slerp[] = quaternion_slerp(0,0,0,0,$quartd_A[0], $quartd_A[1], $quartd_A[2], $quartd_A[3], $slerp);
    float $quat_angle[] = quaternion_to_angle($quat_slerp[0], $quat_slerp[1], $quat_slerp[2], $quat_slerp[3]);
    return $quat_angle;
}

/////////////////////////////////
// head and neck
/////////////////////////////////
// float $quat_angle_neck[] = angleRot_from_rotToQuat(head_jnt.rotateX, head_jnt.rotateY, head_jnt.rotateZ, 0, 2);
// neck_twist_subjnt.rotateX = $quat_angle_neck[1]*$quat_angle_neck[0]*0.2;

/////////////////////////////////
// shoulder
/////////////////////////////////
float $shoulder_trape_init_x = 5.696;
float $shoulder_trape_init_y = 9.564;

float $shoulder_pecto_init_x = 3.83;
float $shoulder_pecto_init_z = 9.89;

float $shoulder_latis_init_x = 5.097;
float $shoulder_latis_init_z = 12.529;


/*L*/
float $quat_angle_shoulderL[] = angleRot_from_rotToQuat(shoulderL_jnt.rotateX, shoulderL_jnt.rotateY, shoulderL_jnt.rotateZ, 0, 2);

// shoulderL_bend_subjnt.rotateX = $quat_angle_shoulderL[1]*$quat_angle_shoulderL[0];
shoulderL_bend_subjnt.rotateY = $quat_angle_shoulderL[2]*$quat_angle_shoulderL[0]*0.5;
shoulderL_bend_subjnt.rotateZ = $quat_angle_shoulderL[3]*$quat_angle_shoulderL[0]*0.5;

// shoulderL_trape_subjnt.translateX = clamp($shoulder_trape_init_x, 20, linear($quat_angle_shoulderL[0], 90) * $quat_angle_shoulderL[3] * 20 + $shoulder_trape_init_x);
// shoulderL_trape_subjnt.translateY = clamp($shoulder_trape_init_y, 20, linear($quat_angle_shoulderL[0], 90) * $quat_angle_shoulderL[3] * 10 + $shoulder_trape_init_y);

// shoulderL_pecto_subjnt.translateX = clamp($shoulder_pecto_init_x, 20, linear($quat_angle_shoulderL[0], 90) * $quat_angle_shoulderL[2] * -10 + $shoulder_pecto_init_x);
// shoulderL_pecto_subjnt.translateZ = clamp($shoulder_pecto_init_z, 20, linear($quat_angle_shoulderL[0], 90) * $quat_angle_shoulderL[2] * -10 + $shoulder_pecto_init_z);

// shoulderL_latis_subjnt.translateX = clamp($shoulder_latis_init_x, 20, linear($quat_angle_shoulderL[0], 90) * $quat_angle_shoulderL[2] * 20 + $shoulder_latis_init_x);
// shoulderL_latis_subjnt.translateZ = clamp(-20, -$shoulder_latis_init_z, linear($quat_angle_shoulderL[0], 90) * $quat_angle_shoulderL[2] * -10 + -$shoulder_latis_init_z);

/*R*/
float $quat_angle_shoulderR[] = angleRot_from_rotToQuat(shoulderR_jnt.rotateX, shoulderR_jnt.rotateY, shoulderR_jnt.rotateZ, 0, 2);

// shoulderR_bend_subjnt.rotateX = $quat_angle_shoulderR[1]*$quat_angle_shoulderR[0];
shoulderR_bend_subjnt.rotateY = $quat_angle_shoulderR[2]*$quat_angle_shoulderR[0]*0.5;
shoulderR_bend_subjnt.rotateZ = $quat_angle_shoulderR[3]*$quat_angle_shoulderR[0]*0.5;


// shoulderR_trape_subjnt.translateX = clamp($shoulder_trape_init_x, 20, linear($quat_angle_shoulderR[0], 90) * $quat_angle_shoulderR[3] * -20 + $shoulder_trape_init_x);
// shoulderR_trape_subjnt.translateY = clamp(-20, -$shoulder_trape_init_y, linear($quat_angle_shoulderR[0], 90) * $quat_angle_shoulderR[3] * 10 + -$shoulder_trape_init_y);

// shoulderR_pecto_subjnt.translateX = clamp($shoulder_pecto_init_x, 20, linear($quat_angle_shoulderR[0], 90) * $quat_angle_shoulderR[2] * -10 + $shoulder_pecto_init_x);
// shoulderR_pecto_subjnt.translateZ = clamp($shoulder_pecto_init_z, 20, linear($quat_angle_shoulderR[0], 90) * $quat_angle_shoulderR[2] * -10 + $shoulder_pecto_init_z);

// shoulderR_latis_subjnt.translateX = clamp($shoulder_latis_init_x, 20, linear($quat_angle_shoulderR[0], 90) * $quat_angle_shoulderR[2] * 20 + $shoulder_latis_init_x);
// shoulderR_latis_subjnt.translateZ = clamp(-20, -$shoulder_latis_init_z, linear($quat_angle_shoulderR[0], 90) * $quat_angle_shoulderR[2] * -10 + -$shoulder_latis_init_z);

/////////////////////////////////
// arm
/////////////////////////////////
float $arm_out_init_x = 1.748;
float $arm_out_init_y = 5.616;

float $arm_fwd_init_x = 2.584;
float $arm_fwd_init_z = 8.269;

float $arm_bck_init_x = 2.992;
float $arm_bck_init_z = 8.219;


/*L*/
float $quat_angle_armL[] = angleRot_from_rotToQuat(armL_jnt.rotateX, armL_jnt.rotateY, armL_jnt.rotateZ, 0, 2);

// armL_bend_subjnt.rotateX = $quat_angle_armL[1]*$quat_angle_armL[0];
armL_bend_subjnt.rotateY = $quat_angle_armL[2]*$quat_angle_armL[0]*0.5;
armL_bend_subjnt.rotateZ = $quat_angle_armL[3]*$quat_angle_armL[0]*0.5;

armL_twist_subjnt.rotateX = $quat_angle_armL[1]*$quat_angle_armL[0]*-0.5;

// armL_out_subjnt.translateX = clamp($arm_out_init_x, 20, linear($quat_angle_armL[0], 90) * $quat_angle_armL[3] * 5 + $arm_out_init_x);
// armL_out_subjnt.translateY = clamp($arm_out_init_y, 20, linear($quat_angle_armL[0], 90) * $quat_angle_armL[3] * 10 + $arm_out_init_y);

// armL_fwd_subjnt.translateX = clamp(-20, $arm_fwd_init_x, linear($quat_angle_armL[0], 90) * $quat_angle_armL[2] * 5 + $arm_fwd_init_x);
// armL_fwd_subjnt.translateZ = clamp($arm_fwd_init_z, 20, linear($quat_angle_armL[0], 90) * $quat_angle_armL[2] * -10 + $arm_fwd_init_z);

// armL_bck_subjnt.translateX = clamp($arm_bck_init_x, 20, linear($quat_angle_armL[0], 90) * $quat_angle_armL[2] * 5 + $arm_bck_init_x);
// armL_bck_subjnt.translateZ = clamp(-20, -$arm_bck_init_z, linear($quat_angle_armL[0], 90) * $quat_angle_armL[2] * -10 + -$arm_bck_init_z);

/*R*/
float $quat_angle_armR[] = angleRot_from_rotToQuat(armR_jnt.rotateX, armR_jnt.rotateY, armR_jnt.rotateZ, 0, 2);

// armR_bend_subjnt.rotateX = $quat_angle_armR[1]*$quat_angle_armR[0];
armR_bend_subjnt.rotateY = $quat_angle_armR[2]*$quat_angle_armR[0]*0.5;
armR_bend_subjnt.rotateZ = $quat_angle_armR[3]*$quat_angle_armR[0]*0.5;

armR_twist_subjnt.rotateX = $quat_angle_armR[1]*$quat_angle_armR[0]*-0.5;

// armR_out_subjnt.translateX = clamp($arm_out_init_x, 20, linear($quat_angle_armR[0], 90) * $quat_angle_armR[3] * -5 + $arm_out_init_x);
// armR_out_subjnt.translateY = clamp(-20, -$arm_out_init_y, linear($quat_angle_armR[0], 90) * $quat_angle_armR[3] * 10 + -$arm_out_init_y);

// armR_fwd_subjnt.translateX = clamp(-20, $arm_fwd_init_x, linear($quat_angle_armR[0], 90) * $quat_angle_armR[2] * 5 + $arm_fwd_init_x);
// armR_fwd_subjnt.translateZ = clamp($arm_fwd_init_z, 20, linear($quat_angle_armR[0], 90) * $quat_angle_armR[2] * -10 + $arm_fwd_init_z);

// armR_bck_subjnt.translateX = clamp($arm_bck_init_x, 20, linear($quat_angle_armR[0], 90) * $quat_angle_armR[2] * 5 + $arm_bck_init_x);
// armR_bck_subjnt.translateZ = clamp(-20, -$arm_bck_init_z, linear($quat_angle_armR[0], 90) * $quat_angle_armR[2] * -10 + -$arm_bck_init_z);


/////////////////////////////////
// elbow
/////////////////////////////////
float $forearm_bicep_init_z = 6.042;

float $forearm_elbow_init_x = 1.907;
float $forearm_elbow_init_z = 4.838;


/*L*/
float $quat_angle_forearmL[] = angleRot_from_rotToQuat(forearmL_jnt.rotateX, forearmL_jnt.rotateY, forearmL_jnt.rotateZ, 0, 2);

// forearmL_bicep_subjnt.translateZ = clamp($forearm_bicep_init_z, 20, linear($quat_angle_forearmL[0], 120) * $quat_angle_forearmL[2] * -5 + $forearm_bicep_init_z);

forearmL_elbow_subjnt.translateX = clamp(-20, $forearm_elbow_init_x, linear($quat_angle_forearmL[0], 90) * $quat_angle_forearmL[2] * 10 + $forearm_elbow_init_x);
forearmL_elbow_subjnt.translateZ = clamp(-20, -$forearm_elbow_init_z, linear($quat_angle_forearmL[0], 90) * $quat_angle_forearmL[2] * 5 + -$forearm_elbow_init_z);

/*R*/
float $quat_angle_forearmR[] = angleRot_from_rotToQuat(forearmR_jnt.rotateX, forearmR_jnt.rotateY, forearmR_jnt.rotateZ, 0, 2);

// forearmR_bicep_subjnt.translateZ = clamp($forearm_bicep_init_z, 20, linear($quat_angle_forearmR[0], 120) * $quat_angle_forearmR[2] * -5 + $forearm_bicep_init_z);

forearmR_elbow_subjnt.translateX = clamp(-20, $forearm_elbow_init_x, linear($quat_angle_forearmR[0], 90) * $quat_angle_forearmR[2] * 10 + $forearm_elbow_init_x);
forearmR_elbow_subjnt.translateZ = clamp(-20, -$forearm_elbow_init_z, linear($quat_angle_forearmR[0], 90) * $quat_angle_forearmR[2] * 5 + -$forearm_elbow_init_z);


/////////////////////////////////
// hand
/////////////////////////////////
float $hand_slide_init_x = 0.272;

/*L*/
float $quat_angle_handL[] = angleRot_from_rotToQuat(handL_jnt.rotateX, handL_jnt.rotateY, handL_jnt.rotateZ, 0, 2);

handL_bend_subjnt.rotateX = $quat_angle_handL[1]*$quat_angle_handL[0]*-1;
handL_bend_subjnt.rotateY = $quat_angle_handL[2]*$quat_angle_handL[0]*-0.5;
handL_bend_subjnt.rotateZ = $quat_angle_handL[3]*$quat_angle_handL[0]*-0.5;

forearmL_twist_subjnt.rotateX = $quat_angle_handL[1]*$quat_angle_handL[0]*0.5;

// handL_slide_subjnt.translateX = clamp($hand_slide_init_x, 20, linear($quat_angle_handL[0], 120) * $quat_angle_handL[3] * 5 + $hand_slide_init_x);

/*R*/
float $quat_angle_handR[] = angleRot_from_rotToQuat(handR_jnt.rotateX, handR_jnt.rotateY, handR_jnt.rotateZ, 0, 2);

handR_bend_subjnt.rotateX = $quat_angle_handR[1]*$quat_angle_handR[0]*-1;
handR_bend_subjnt.rotateY = $quat_angle_handR[2]*$quat_angle_handR[0]*-0.5;
handR_bend_subjnt.rotateZ = $quat_angle_handR[3]*$quat_angle_handR[0]*-0.5;

forearmR_twist_subjnt.rotateX = $quat_angle_handR[1]*$quat_angle_handR[0]*0.5;

// handR_slide_subjnt.translateX = clamp($hand_slide_init_x, 20, linear($quat_angle_handR[0], 120) * $quat_angle_handR[3] * -5 + $hand_slide_init_x);


/////////////////////////////////
// upleg
/////////////////////////////////
float $upleg_fwd_init_z = 9.472;
float $upleg_bck_init_z = 9.599;

/*L*/
float $quat_angle_uplegL[] = angleRot_from_rotToQuat(uplegL_jnt.rotateX, uplegL_jnt.rotateY, uplegL_jnt.rotateZ, 0, 2);

uplegL_bend_subjnt.rotateY = $quat_angle_uplegL[2]*$quat_angle_uplegL[0]*0.5;
uplegL_bend_subjnt.rotateZ = $quat_angle_uplegL[3]*$quat_angle_uplegL[0]*0.5;

uplegL_twist_subjnt.rotateX = $quat_angle_uplegL[1]*$quat_angle_uplegL[0]*-0.5;

// uplegL_fwd_subjnt.translateZ = clamp($upleg_fwd_init_z, 20, linear($quat_angle_uplegL[0], 90) * $quat_angle_uplegL[2] * -10 + $upleg_fwd_init_z);

// uplegL_bck_subjnt.translateZ = clamp(-20, -$upleg_bck_init_z, linear($quat_angle_uplegL[0], 90) * $quat_angle_uplegL[2] * -10 + -$upleg_bck_init_z);


/*R*/
float $quat_angle_uplegR[] = angleRot_from_rotToQuat(uplegR_jnt.rotateX, uplegR_jnt.rotateY, uplegR_jnt.rotateZ, 0, 2);

uplegR_bend_subjnt.rotateY = $quat_angle_uplegR[2]*$quat_angle_uplegR[0]*0.5;
uplegR_bend_subjnt.rotateZ = $quat_angle_uplegR[3]*$quat_angle_uplegR[0]*0.5;

uplegR_twist_subjnt.rotateX = $quat_angle_uplegR[1]*$quat_angle_uplegR[0]*-0.5;

// uplegR_fwd_subjnt.translateZ = clamp($upleg_fwd_init_z, 20, linear($quat_angle_uplegR[0], 90) * $quat_angle_uplegR[2] * -10 + $upleg_fwd_init_z);

// uplegR_bck_subjnt.translateZ = clamp(-20, -$upleg_bck_init_z, linear($quat_angle_uplegR[0], 90) * $quat_angle_uplegR[2] * -10 + -$upleg_bck_init_z);


/////////////////////////////////
// leg, calf
/////////////////////////////////
float $leg_out_init_z = 5.2;

float $foot_calf_init_x = 10.504;
float $foot_calf_init_z = 6.416;

/*L*/
float $quat_angle_legL[] = angleRot_from_rotToQuat(legL_jnt.rotateX, legL_jnt.rotateY, legL_jnt.rotateZ, 0, 2);

legL_out_subjnt.translateZ = clamp($leg_out_init_z, 20, linear($quat_angle_legL[0], 90) * $quat_angle_legL[2] * 3 + $leg_out_init_z);

// footL_calf_subjnt.translateX = clamp(-$foot_calf_init_x, 20, linear($quat_angle_legL[0], 90) * $quat_angle_legL[2] * 5 + -$foot_calf_init_x);
// footL_calf_subjnt.translateZ = clamp(-20, -$foot_calf_init_x, linear($quat_angle_legL[0], 90) * $quat_angle_legL[2] * -5 + -$foot_calf_init_x);

/*R*/
float $quat_angle_legR[] = angleRot_from_rotToQuat(legR_jnt.rotateX, legR_jnt.rotateY, legR_jnt.rotateZ, 0, 2);

legR_out_subjnt.translateZ = clamp($leg_out_init_z, 20, linear($quat_angle_legR[0], 90) * $quat_angle_legR[2] * 3 + $leg_out_init_z);

// footR_calf_subjnt.translateX = clamp(-$foot_calf_init_x, 20, linear($quat_angle_legR[0], 90) * $quat_angle_legR[2] * 5 + -$foot_calf_init_x);
// footR_calf_subjnt.translateZ = clamp(-20, -$foot_calf_init_x, linear($quat_angle_legR[0], 90) * $quat_angle_legR[2] * -5 + -$foot_calf_init_x);


/////////////////////////////////
// foot
/////////////////////////////////
/*L*/
float $quat_angle_footL[] = angleRot_from_rotToQuat(footL_jnt.rotateX, footL_jnt.rotateY, footL_jnt.rotateZ, 0, 2);

legL_twist_subjnt.rotateX = $quat_angle_footL[1]*$quat_angle_footL[0]*0.7;

/*R*/
float $quat_angle_footR[] = angleRot_from_rotToQuat(footR_jnt.rotateX, footR_jnt.rotateY, footR_jnt.rotateZ, 0, 2);

legR_twist_subjnt.rotateX = $quat_angle_footR[1]*$quat_angle_footR[0]*0.7;


""", n='{0}'.format(exp_name), ae=0)

# handWeapons
handWeapon_joints = cmds.ls('*handWeapon*', type='joint')

# primary
primary_joints = cmds.ls('*_jnt', type='joint')
for hw_j in handWeapon_joints:
    primary_joints.remove(hw_j)

# sub
sub_joints = cmds.ls('*_subjnt*', type='joint')

# all
all_joints = cmds.ls('*root_jnt*', type='joint', dag=1)

# len(all_joints)
# len(primary_joints)
# len(sub_joints)
# len(handWeapon_joints)

# primary_joints_set
primary_joints_set = 'primary_joints_set'
if not cmds.objExists(primary_joints_set):
    cmds.sets(em=1, n=primary_joints_set)

for p_j in primary_joints:
    cmds.sets(p_j, add=primary_joints_set)

# sub_joints_set
sub_joints_set = 'sub_joints_set'
if not cmds.objExists(sub_joints_set):
    cmds.sets(em=1, n=sub_joints_set)

for p_j in sub_joints:
    cmds.sets(p_j, add=sub_joints_set)

# handWeapon_joints_set
handWeapon_joints_set = 'handWeapon_joints_set'
if not cmds.objExists(handWeapon_joints_set):
    cmds.sets(em=1, n=handWeapon_joints_set)

for p_j in handWeapon_joints:
    cmds.sets(p_j, add=handWeapon_joints_set)

# set colors
def set_colors(objects=None, color=None, outlinear=None):
    for obj in objects:
        cmds.setAttr('{}.overrideEnabled'.format(obj), 1)
        cmds.setAttr('{}.overrideRGBColors'.format(obj), 1)
        cmds.setAttr('{}.overrideColorRGB'.format(obj), *color)

        if outlinear:
            cmds.setAttr('{}.useOutlinerColor'.format(obj), 1)
            try:
                mel.eval("AEdagNodeCommonRefreshOutliners();")
            except:
                pass

            cmds.setAttr('{}.outlinerColor'.format(obj), *color)

set_colors(objects=all_joints, color=[1, 0, 0.5], outlinear=False)
set_colors(objects=sub_joints, color=[0, 0.5, 1], outlinear=True)
