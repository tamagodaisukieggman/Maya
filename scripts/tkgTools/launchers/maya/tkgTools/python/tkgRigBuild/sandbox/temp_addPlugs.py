# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload
from collections import OrderedDict

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.post.finalize as tkgFinalize
import tkgRigBuild.libs.attribute as tkgAttr
reload(tkgPart)
reload(tkgModule)
reload(tkgFinalize)
reload(tkgAttr)

# モジュールからコントローラの情報を抜き出す
part_ctrls_dict = OrderedDict()
for part in cmds.listRelatives('RIG'):
    part_ctrls_dict[part] = OrderedDict()

    part_attrs = cmds.listAttr(part, ud=True)

    for ud_at in part_attrs:
        if 'Ctrls' in ud_at or 'partJoints' in ud_at:
            nodes = cmds.getAttr('{}.{}'.format(part, ud_at)).split(',')
            if 'Ctrls' in ud_at:
                _nodes = OrderedDict()
                for n in nodes:
                    if cmds.objExists(n + '.ctrlDict'):
                        _nodes[n] = cmds.getAttr('{}.ctrlDict'.format(n, ))

                nodes = _nodes

            part_ctrls_dict[part][ud_at] = nodes

# -------------------------------
# Hip
# -------------------------------
# *ジョイント階層の指定
# plugを追加するmodule
part_grp = 'Cn_hip'

# 親にするジョイントの取得
root_jnt = part_ctrls_dict['Cn_root']['partJoints']

# 子にするジョイントの取得
jnts = part_ctrls_dict[part_grp]['partJoints']

# 親子関係の情報を設定
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[root_jnt], name='skeletonPlugs',
                 children_name=[jnts[0]])

# *コントローラの空間の指定
# spaceを追加するコントローラを取得
ctrl = [n for n in part_ctrls_dict[part_grp]['hipCtrls'].keys()][0]

# spaceの元になるコントローラの取得
target_list = [n for n in part_ctrls_dict['Cn_root']['rootCtrls'].keys()]

# spaceの名前を取得する
name_list = [n.replace('Cn_', '').replace('_CTRL', '') for n in target_list]

# spaceのデフォルトにするインデクス
default_idx = 2

# デフォルトのインデクスとdefault_valueを最後に追加
target_list.append(str(default_idx))
name_list.append('default_value')

# parentでのspaceを設定する
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=target_list,
                 name=ctrl + '_parent',
                 children_name=name_list)


# tkgFinalize.assemble_rig()


# -------------------------------
# Chest
# -------------------------------
# *ジョイント階層の指定
# plugを追加するmodule
part_grp = 'Cn_chest'

# 親にするジョイントの取得
root_jnt = part_ctrls_dict['Cn_spine']['partJoints'][-1]

# 子にするジョイントの取得
jnts = part_ctrls_dict[part_grp]['partJoints']

# 親子関係の情報を設定
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[root_jnt], name='skeletonPlugs',
                 children_name=[jnts[0]])

# *コントローラの空間の指定
# spaceを追加するコントローラを取得
ctrl = [n for n in part_ctrls_dict[part_grp]['chestCtrls'].keys()][0]

# spaceの元になるコントローラの取得
target_list = []
hip_ctrls = [n for n in part_ctrls_dict['Cn_hip']['hipCtrls'].keys()]
root_ctrls = [n for n in part_ctrls_dict['Cn_root']['rootCtrls'].keys()]
[target_list.append(n) for n in hip_ctrls]
[target_list.append(n) for n in root_ctrls]

# spaceの名前を取得する
name_list = [n.replace('Cn_', '').replace('_CTRL', '') for n in target_list]

# spaceのデフォルトにするインデクス
default_idx = 0

# デフォルトのインデクスとdefault_valueを最後に追加
target_list.append(str(default_idx))
name_list.append('default_value')

# parentでのspaceを設定する
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=target_list,
                 name=ctrl + '_parent',
                 children_name=name_list)


# tkgFinalize.assemble_rig()


# -------------------------------
# Spine
# -------------------------------
# *ジョイント階層の指定
# plugを追加するmodule
part_grp = 'Cn_spine'

# 親にするジョイントの取得
root_jnt = part_ctrls_dict['Cn_hip']['partJoints'][-1]

# 子にするジョイントの取得
jnts = part_ctrls_dict[part_grp]['partJoints']

# 親子関係の情報を設定
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[root_jnt], name='skeletonPlugs',
                 children_name=[jnts[0]])

# *parentConstraintの設定
# parentConstraintさせるプラグの設定
driver_list = ['Cn_hip_02_CTRL',
               'Cn_hip_01_CTRL',
               'Cn_chest_02_CTRL']
driven_list = [part_grp + '_base_CTRL_CNST_GRP',
               part_grp + '_01_FK_CTRL_CNST_GRP',
               part_grp + '_tip_CTRL_CNST_GRP']
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=driver_list, name='pacRigPlugs',
                 children_name=driven_list)

# *非表示の設定
# 非表示にするオブジェクトの設定
hide_list = [part_grp + '_base_CTRL_CNST_GRP',
             part_grp + '_tip_CTRL_CNST_GRP']
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[' '.join(hide_list)], name='hideRigPlugs',
                 children_name=['hideNodes'])


# add transferAttributes plug
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=['Cn_chest_02_CTRL'], name='transferAttributes',
                 children_name=[part_grp + '_tip_CTRL'])

# delete
delete_list = [part_grp + '_tip_CTRL_CNST_GRP_parentConstraint1']
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[' '.join(delete_list)], name='deleteRigPlugs',
                 children_name=['deleteNodes'])

# tkgFinalize.assemble_rig()

# -------------------------------
# Neck
# -------------------------------
# *ジョイント階層の指定
# plugを追加するmodule
part_grp = 'Cn_neck'

# 親にするジョイントの取得
root_jnt = part_ctrls_dict['Cn_chest']['partJoints'][-1]

# 子にするジョイントの取得
jnts = part_ctrls_dict[part_grp]['partJoints']

# 親子関係の情報を設定
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[root_jnt], name='skeletonPlugs',
                 children_name=[jnts[0]])

# *parentConstraintの設定
# parentConstraintさせるプラグの設定
driver_list = ['Cn_chest_02_JNT',
               part_grp + '_base_CTRL']
driven_list = [part_grp + '_base_CTRL_CNST_GRP',
               part_grp + '_tip_CTRL_CNST_GRP']
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=driver_list, name='pacRigPlugs',
                 children_name=driven_list)

# *非表示の設定
# 非表示にするオブジェクトの設定
# 隠す必要ある？
# hide_list = [part_grp + '_tip_CTRL_CNST_GRP']
# tkgAttr.Attribute(node=part_grp, type='plug',
#                  value=[' '.join(hide_list)], name='hideRigPlugs',
#                  children_name=['hideNodes'])

# tkgFinalize.assemble_rig()

# -------------------------------
# Head
# -------------------------------
# *ジョイント階層の指定
# plugを追加するmodule
part_grp = 'Cn_head'

# 親にするジョイントの取得
root_jnt = part_ctrls_dict['Cn_neck']['partJoints'][-1]

# 子にするジョイントの取得
jnts = part_ctrls_dict[part_grp]['partJoints']

# 親子関係の情報を設定
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[root_jnt], name='skeletonPlugs',
                 children_name=[jnts[0]])

# *コントローラの空間の指定
# spaceを追加するコントローラを取得
ctrls = [n for n in part_ctrls_dict[part_grp]['headCtrls'].keys()]

# spaceの元になるコントローラの取得
target_list = []
root_ctrls = [n for n in part_ctrls_dict['Cn_root']['rootCtrls'].keys()]
chest_ctrls = [n for n in part_ctrls_dict['Cn_chest']['chestCtrls'].keys()]
neck_ctrls = [n for n in part_ctrls_dict['Cn_neck']['neckIkCtrls'].keys()]
[target_list.append(n) for n in root_ctrls]
[target_list.append(n) for n in chest_ctrls]
[target_list.append(n) for n in neck_ctrls]

# spaceの名前を取得する
name_list = [n.replace('Cn_', '').replace('_CTRL', '').title() for n in target_list]
name_list.append('default_value')
point_names = ['point' + n.title() for n in name_list]
orient_names = ['orient' + n.title() for n in name_list]

# spaceのデフォルトにするインデクス
default_idx = len(target_list) - 2

# デフォルトのインデクスとdefault_valueを最後に追加
target_list.append(str(default_idx))

# parentでのspaceを設定する
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=target_list,
                 name=ctrls[0] + '_point',
                 children_name=point_names)

tkgAttr.Attribute(node=part_grp, type='plug',
                 value=target_list,
                 name=ctrls[0] + '_orient',
                 children_name=orient_names)

# *削除するオブジェクトを指定する
delete_list = [part_grp + '_01_JNT_pointConstraint1']
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[' '.join(delete_list)], name='deleteRigPlugs',
                 children_name=['deleteNodes'])

# add transferAttributes plug
# tkgAttr.Attribute(node=part_grp, type='plug',
#                  value=[ctrls[0]], name='transferAttributes',
#                  children_name=['Cn_neck_tip_CTRL'])

# tkgAttr.Attribute(node=part_grp, type='plug',
#                  value=['cmds.ls("Cn_neck_??_driver_JNT", "Cn_neck_??_fk_offset_CTRL")[-1]'],
#                  name='pocRigPlugs',
#                  children_name=[jnts[0]])


# tkgFinalize.assemble_rig()

sides = ['Lf', 'Rt']
force_sides = ['_L', '_R']

for s, fs in zip(sides, force_sides):
    # -------------------------------
    # Clavicle
    # -------------------------------
    # *ジョイント階層の指定
    # plugを追加するmodule
    part_grp = s + '_clavicle'

    # 親にするジョイントの取得
    root_jnt = part_ctrls_dict['Cn_chest']['partJoints'][-1]

    # 子にするジョイントの取得
    jnts = part_ctrls_dict[part_grp]['partJoints']

    # 親子関係の情報を設定
    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=[root_jnt], name='skeletonPlugs',
                     children_name=[jnts[0]])

    # *parentConstraintの設定
    # parentConstraintさせるプラグの設定
    driver_list = [root_jnt,
                   root_jnt]
    driven_list = [s + '_clavicle_CTRL_CNST_GRP',
                   s + '_clavicle_CNST_GRP']
    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=driver_list, name='pacRigPlugs',
                     children_name=driven_list)

for s, fs in zip(sides, force_sides):
    # -------------------------------
    # Arm
    # -------------------------------
    # *ジョイント階層の指定
    # plugを追加するmodule
    part_grp = s + '_arm'
    limb_grp = part_grp + '_RIG_GRP'

    # 親にするジョイントの取得
    root_jnt = part_ctrls_dict['Cn_chest']['partJoints'][-1]

    # 子にするジョイントの取得
    jnts = part_ctrls_dict[part_grp]['partJoints']

    # 親子関係の情報を設定
    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=[root_jnt], name='skeletonPlugs',
                     children_name=[jnts[0]])

    # *コントローラの空間の指定
    fk_ctrls = [n for n in part_ctrls_dict[part_grp]['armFkMainCtrls'].keys()]
    ik_ctrls = [n for n in part_ctrls_dict[part_grp]['armIkCtrls'].keys()]
    ik_main_ctrl = ik_ctrls[1]
    pv_ctrl = ik_ctrls[-1]

    driver_list = [s + '_clavicle_02_driver_JNT',
                   s + '_clavicle_02_driver_JNT',
                   s + '_clavicle_02_driver_JNT',
                   s + '_arm_03_RP_JNT']
    driven_list = [limb_grp,
                   part_grp + '_IK_base_CTRL_CNST_GRP',
                   part_grp + '_up_twist_LOC',
                   s + '_hand_01_CTRL_CNST_GRP']
    # hide_list = [part_grp + '_IK_base_CTRL_CNST_GRP',
    #              part_grp + '_IK_main_CTRL_CNST_GRP']

    pv_targets = ['CHAR', 'Cn_global_CTRL', 'Cn_world_CTRL', 'Cn_local_CTRL',
                  'Cn_chest_02_CTRL', part_grp + '_IK_main_CTRL',
                  '2']
    pv_names = ['CHAR', 'global', 'world', 'local', 'chest', 'hand',
                'default_value']
    ik_ctrl = [s + '_hand_01_CTRL']

    # add pointConstraint rig plugs
    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=[s + '_clavicle_02_driver_JNT'],
                     name='pocRigPlugs',
                     children_name=[
                         s + '_arm_01_fk_CTRL_CNST_GRP'])

    # add space plugs
    target_list = ['Cn_chest_01_CTRL', 'Cn_chest_02_CTRL',
                   s + '_clavicle_02_driver_JNT', '0']
    name_list = ['chest01', 'chest02', 'clavicle', 'default_value']
    orient_names = ['orient' + n.title() for n in name_list]

    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=target_list,
                     name=fk_ctrls[0] + '_orient',
                     children_name=orient_names)

    # add parentConstraint rig plugs
    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=driver_list, name='pacRigPlugs',
                     children_name=driven_list)

    # add hide rig plugs
    # tkgAttr.Attribute(node=part_grp, type='plug',
    #                  value=[' '.join(hide_list)], name='hideRigPlugs',
    #                  children_name=['hideNodes'])

    # add pv space plug
    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=pv_targets,
                     name=pv_ctrl + '_parent',
                     children_name=pv_names)

    # add transferAttributes plug
    # tkgAttr.Attribute(node=part_grp, type='plug',
    #                  value=ik_ctrl, name='transferAttributes',
    #                  children_name=[ik_main_ctrl])

for s, fs in zip(sides, force_sides):
    # -------------------------------
    # Leg
    # -------------------------------
    # *ジョイント階層の指定
    # plugを追加するmodule
    part_grp = s + '_leg'
    limb_grp = part_grp + '_RIG_GRP'

    # 親にするジョイントの取得
    root_jnt = part_ctrls_dict['Cn_hip']['partJoints'][-1]

    # 子にするジョイントの取得
    jnts = part_ctrls_dict[part_grp]['partJoints']

    # 親子関係の情報を設定
    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=[root_jnt], name='skeletonPlugs',
                     children_name=[jnts[0]])

    # *コントローラの空間の指定
    fk_ctrls = [n for n in part_ctrls_dict[part_grp]['legFkMainCtrls'].keys()]

    # parentConstraint
    driver_list = ['Cn_hip_02_CTRL',
                   'Cn_hip_02_CTRL',
                   'Cn_hip_02_CTRL',
                   part_grp + '_IK_base_CTRL']
    driven_list = [limb_grp,
                   part_grp + '_IK_base_CTRL_CNST_GRP',
                   part_grp + '_01_fk_CTRL_CNST_GRP',
                   part_grp + '_up_twist_LOC']

    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=driver_list, name='pacRigPlugs',
                     children_name=driven_list)

    # point and orient Constraint
    driver_list = [s + '_leg_IK_main_CTRL',
                   s + '_foot_ankle_CTRL']
    driven_list = [s + '_foot_01_CTRL_CNST_GRP',
                   part_grp + '_IKH']

    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=driver_list, name='pocRigPlugs',
                     children_name=driven_list)

    # driver_list = [part_grp + '_03_RP_JNT']
    # driven_list = [s + '_foot_02_CTRL_CNST_GRP']

    # tkgAttr.Attribute(node=part_grp, type='plug',
    #                  value=driver_list, name='orcRigPlugs',
    #                  children_name=driven_list)

    # # parent
    # driver_list = [s + '_foot_ankle_CTRL']
    # driven_list = [part_grp + '_IKH']

    # tkgAttr.Attribute(node=part_grp, type='plug',
    #                  value=driver_list, name='parentNodePlugs',
    #                  children_name=driven_list)

    # delete
    delete_list = [part_grp + '_IKH_parentConstraint1']

    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=[' '.join(delete_list)], name='deleteRigPlugs',
                     children_name=['deleteNodes'])

    # add pv space plug
    pv_targets = ['CHAR', 'Cn_global_CTRL', 'Cn_world_CTRL', 'Cn_local_CTRL',
                  'Cn_hip_01_CTRL', s + '_leg_IK_base_CTRL',
                  part_grp + '_IK_main_CTRL', '2']
    pv_names = ['CHAR', 'global', 'world', 'local', 'hip', 'leg', 'foot',
                'default_value']

    tkgAttr.Attribute(node=part_grp, type='plug',
                     value=pv_targets,
                     name=pv_ctrl + '_parent',
                     children_name=pv_names)

# tkgFinalize.assemble_rig()

tkgFinalize.finalize_rig()
