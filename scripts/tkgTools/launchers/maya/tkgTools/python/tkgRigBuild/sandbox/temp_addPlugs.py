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
# plugを追加するmodule
part_grp = 'Cn_hip'

# 親にするジョイントの取得
root_jnt = part_ctrls_dict['Cn_root']['partJoints']

# 子にするジョイントの取得
jnts = part_ctrls_dict[part_grp]['partJoints']

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

# 親子関係の情報を設定
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[root_jnt], name='skeletonPlugs',
                 children_name=[jnts[0]])

# tkgFinalize.assemble_rig()


# -------------------------------
# Chest
# -------------------------------
# plugを追加するmodule
part_grp = 'Cn_chest'

# 親にするジョイントの取得
root_jnt = part_ctrls_dict['Cn_spine']['partJoints'][-1]

# 子にするジョイントの取得
jnts = part_ctrls_dict[part_grp]['partJoints']

# spaceを追加するコントローラを取得
ctrl = [n for n in part_ctrls_dict[part_grp]['chestCtrls'].keys()][0]

# spaceの元になるコントローラの取得
target_list = []
hip_ctrl = [n for n in part_ctrls_dict['Cn_hip']['hipCtrls'].keys()][-1]
root_ctrls = [n for n in part_ctrls_dict['Cn_root']['rootCtrls'].keys()]
target_list.append(hip_ctrl)
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

# 親子関係の情報を設定
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[root_jnt], name='skeletonPlugs',
                 children_name=[jnts[0]])

# tkgFinalize.assemble_rig()


# -------------------------------
# Spine
# -------------------------------
# plugを追加するmodule
part_grp = 'Cn_spine'

# 親にするジョイントの取得
root_jnt = part_ctrls_dict['Cn_hip']['partJoints'][-1]

# 子にするジョイントの取得
jnts = part_ctrls_dict[part_grp]['partJoints']

base_name = part_grp

# parentConstraintさせるプラグの設定
driver_list = ['Cn_hip_02_CTRL',
               'Cn_hip_01_CTRL',
               'Cn_chest_02_CTRL']
driven_list = [base_name + '_base_CTRL_CNST_GRP',
               base_name + '_01_FK_CTRL_CNST_GRP',
               base_name + '_tip_CTRL_CNST_GRP']
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=driver_list, name='pacRigPlugs',
                 children_name=driven_list)

# 非表示にするオブジェクトの設定
hide_list = [base_name + '_base_CTRL_CNST_GRP',
             base_name + '_tip_CTRL_CNST_GRP']
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[' '.join(hide_list)], name='hideRigPlugs',
                 children_name=['hideNodes'])


# 親子関係の情報を設定
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[root_jnt], name='skeletonPlugs',
                 children_name=[jnts[0]])

# tkgFinalize.assemble_rig()

# -------------------------------
# Neck
# -------------------------------
# plugを追加するmodule
part_grp = 'Cn_neck'

# 親にするジョイントの取得
root_jnt = part_ctrls_dict['Cn_chest']['partJoints'][-1]

# 子にするジョイントの取得
jnts = part_ctrls_dict[part_grp]['partJoints']

# add parentConstraint rig plugs
driver_list = ['Cn_chest_02_JNT',
               'Cn_head_02_CTRL']
driven_list = [self.base_name + '_base_CTRL_CNST_GRP',
               self.base_name + '_tip_CTRL_CNST_GRP']
tkgAttr.Attribute(node=self.part_grp, type='plug',
                 value=driver_list, name='pacRigPlugs',
                 children_name=driven_list)

# add hide rig plugs
hide_list = [self.base_name + '_tip_CTRL_CNST_GRP']
tkgAttr.Attribute(node=self.part_grp, type='plug',
                 value=[' '.join(hide_list)], name='hideRigPlugs',
                 children_name=['hideNodes'])

# 親子関係の情報を設定
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=[root_jnt], name='skeletonPlugs',
                 children_name=[jnts[0]])
