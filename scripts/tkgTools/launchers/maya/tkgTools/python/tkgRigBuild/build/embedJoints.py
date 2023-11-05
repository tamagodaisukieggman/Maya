# -*- coding: utf-8 -*-
import maya.cmds as cmds
import json

def create_joint(name=None, position=None):
    joint = cmds.createNode( 'joint' , name=name )
    cmds.xform( joint , worldSpace=True , translation=position )
    return joint

# This method creates a few joints to see the embedding.
def create_joints_from_embedding( embedding ):
    embedded_joints = [create_joint(name=name, position=position)
                        for name , position in embedding[ 'joints' ].items( )]
    return embedded_joints

def get_mid_point(pos1, pos2, percentage=0.5):
    mid_point = [pos1[0] + (pos2[0] - pos1[0]) * percentage,
                 pos1[1] + (pos2[1] - pos1[1]) * percentage,
                 pos1[2] + (pos2[2] - pos1[2]) * percentage]
    return mid_point

def add_segments(start_position=None, end_position=None, base_name=None, count=3, embedding=None):
    # base_name = 'spine'
    # count = 3
    step = 1.0 / count
    max_rate = 1 - step
    rate = 0
    for i in range(count):
        mid_point = get_mid_point(start_position, end_position, rate)
        embedding['joints']['{}_{}'.format(base_name, str(i+1).zfill(2))] = mid_point
        rate += step

# First select the shape, not the transform.
sel = cmds.ls(os=True)
shape = cmds.listRelatives(sel[0], s=True)[0]
cmds.select( shape , r=True )

result = cmds.skeletonEmbed()
embedding = json.loads( result )

# Exchange keys
embedding['joints']['left_arm'] = embedding['joints'].pop('left_shoulder')
embedding['joints']['right_arm'] = embedding['joints'].pop('right_shoulder')

# Fixing spine
embedding['joints']['spine'] = embedding['joints'].pop('back')

# Fixing arm and shoulder
shoulders_position = embedding['joints']['shoulders']
left_arm_position = embedding['joints']['left_arm']
right_arm_position = embedding['joints']['right_arm']

left_arm_mid_point = get_mid_point(shoulders_position, left_arm_position)
right_arm_mid_point = get_mid_point(shoulders_position, right_arm_position)

embedding['joints'].update({'left_shoulder':left_arm_mid_point})
embedding['joints'].update({'right_shoulder':right_arm_mid_point})

# Fixing neck
embedding['joints']['neck'] = embedding['joints'].pop('shoulders')
neck_position = embedding['joints']['neck']
head_position = embedding['joints']['head']

neck_head_mid_point = get_mid_point(neck_position, head_position, 0.3)
embedding['joints']['neck'] = neck_head_mid_point

# Fixing head
fix_head_mid_point = get_mid_point(neck_position, head_position, 0.7)
embedding['joints']['head'] = fix_head_mid_point

# Fixing Side
left_sides = {}
for joint, position in embedding['joints'].items():
    if 'left_' in joint:
        left_sides[joint] = position

for joint, position in embedding['joints'].items():
    if 'left_' in joint:
        l_pos = left_sides[joint]
        r_pos = []
        r_pos.append(l_pos[0]*-1)
        r_pos.append(l_pos[1])
        r_pos.append(l_pos[2])
        embedding['joints'][joint.replace('left_', 'right_')] = r_pos

# Fixing Straight
for s in ['left_', 'right_']:
    for i, p in enumerate([['arm', 'elbow', 'hand'], ['thigh', 'knee', 'ankle']]):
        start_position = embedding['joints'][s+p[0]]
        end_position = embedding['joints'][s+p[2]]
        embedding['joints'][s+p[1]] = get_mid_point(start_position, end_position)

for joint in ['hips', 'spine', 'neck', 'head']:
    old_pos = embedding['joints'][joint]
    new_pos = []
    new_pos.append(old_pos[0]*0)
    new_pos.append(old_pos[1])
    new_pos.append(old_pos[2])
    embedding['joints'][joint] = new_pos

# Add Spine Segments
spine_count=3
if spine_count != 1:
    start_position = embedding['joints']['hips']
    end_position = embedding['joints']['neck']
    add_segments(start_position=start_position,
                 end_position=end_position,
                 base_name='spine',
                 count=spine_count,
                 embedding=embedding)
    embedding['joints'].pop('spine')

# Add Neck Segments
neck_count=2
if neck_count != 1:
    start_position = embedding['joints']['neck']
    end_position = embedding['joints']['head']
    add_segments(start_position=start_position,
                 end_position=end_position,
                 base_name='neck',
                 count=neck_count,
                 embedding=embedding)
    embedding['joints'].pop('neck')

# Add Root Joint
embedding['joints']['root'] = [0, 0, 0]

# Add Neck Segments
root_count=1
if root_count != 1:
    start_position = embedding['joints']['root']
    end_position = embedding['joints']['root']
    add_segments(start_position=start_position,
                 end_position=end_position,
                 base_name='root',
                 count=root_count,
                 embedding=embedding)
    embedding['joints'].pop('root')


# Connect Joints
mirror = ['left_', 'right_']
parent_hierarchy = {
    'hips':'root',
    'spine_01':'hips',
    'spine_02':'spine_01',
    'spine_03':'spine_02',
    'neck_01':'spine_03',
    'neck_02':'neck_01',
    'head':'neck_02',

    'left_hand':'left_elbow',
    'left_elbow':'left_arm',
    'left_arm':'left_shoulder',
    'left_shoulder':'spine_03',

    'right_hand':'right_elbow',
    'right_elbow':'right_arm',
    'right_arm':'right_shoulder',
    'right_shoulder':'spine_03',

    'left_foot':'left_ankle',
    'left_ankle':'left_knee',
    'left_knee':'left_thigh',
    'left_thigh':'hips',

    'right_foot':'right_ankle',
    'right_ankle':'right_knee',
    'right_knee':'right_thigh',
    'right_thigh':'hips',

}

# create joints
# 実際に作成するのはembeddingに格納した値を確認してから
embedded_joints = create_joints_from_embedding( embedding )

for child, parent in parent_hierarchy.items():
    cmds.parent(child, parent)
