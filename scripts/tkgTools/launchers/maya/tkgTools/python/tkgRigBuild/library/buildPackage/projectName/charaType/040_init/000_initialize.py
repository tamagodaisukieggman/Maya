# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.buildPart as tkgPart
import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.post.finalize as tkgFinalize
import tkgRigBuild.libs.attribute as tkgAttr
reload(tkgPart)
reload(tkgModule)
reload(tkgFinalize)
reload(tkgAttr)

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
hip_jnts = part_ctrls_dict[part_grp]['partJoints']

# spaceを追加するコントローラを取得
hip_ctrl = [n for n in part_ctrls_dict[part_grp]['hipCtrls'].keys()][0]

# spaceの元になるコントローラの取得
target_list = [n for n in part_ctrls_dict['Cn_root']['rootCtrls'].keys()]

# spaceの名前を取得する
name_list = [n.replace('Cn_', '').replace('_CTRL', '') for n in target_list]

# spaceのデフォルトにするインデクス
default_idx = 0

# 親子関係の情報を設定
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=root_jnt, name='skeletonPlugs',
                 children_name=hip_jnts)

# デフォルトのインデクスとdefault_valueを最後に追加
target_list.append(str(default_idx))
name_list.append('default_value')

# parentでのspaceを設定する
tkgAttr.Attribute(node=part_grp, type='plug',
                 value=target_list,
                 name=hip_ctrl + '_parent',
                 children_name=name_list)
