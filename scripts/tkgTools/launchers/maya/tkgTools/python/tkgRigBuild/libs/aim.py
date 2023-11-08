from maya import cmds, mel
from collections import OrderedDict
import traceback

def order_dags(dags=None):
    parent_dag = cmds.ls(dags[0], l=1, type='transform')[0].split('|')[1]

    all_hir = cmds.listRelatives(parent_dag, ad=True, f=True)
    hir_split_counter = {}
    parent_node = '|' + parent_dag
    hir_split_counter[parent_node] = len(parent_node.split('|'))
    for fp_node in all_hir:
        hir_split_counter[fp_node] = len(fp_node.split('|'))

    hir_split_counter_sorted = sorted(hir_split_counter.items(), key=lambda x:x[1])

    sorted_joint_list = [dag_count[0] for dag_count in hir_split_counter_sorted]

    all_ordered_dags = cmds.ls(sorted_joint_list)
    return [dag for dag in all_ordered_dags if dag in dags]

def get_dag_nodes(obj=None, type=None, remove_top=None):
    joints = cmds.ls(obj, dag=True, type=type)
    if remove_top:
        joints.remove(obj)

    if not joints:
        return None

    return order_dags(joints)

def aim_nodes(base=None, target=None, aim_axis='z', up_axis='y', worldUpType='object', worldSpace=False):
    axis_dict = {
        'x':[1,0,0],
        'y':[0,1,0],
        'z':[0,0,1],
        '-x':[-1,0,0],
        '-y':[0,-1,0],
        '-z':[0,0,-1]
    }

    aimVector = axis_dict[aim_axis]
    upVector = axis_dict[up_axis]

    settings = {}

    aim_obj = cmds.spaceLocator()[0]
    cmds.matchTransform(aim_obj, base)

    settings = {}

    up_obj = cmds.spaceLocator()[0]
    cmds.matchTransform(up_obj, target)

    if worldUpType == 'object':
        if worldSpace:
            cmds.xform(up_obj, t=[v*10 for v in axis_dict[up_axis]], r=True, ws=True)
        else:
            cmds.xform(up_obj, t=[v*10 for v in axis_dict[up_axis]], r=True, os=True)

    settings['worldUpObject'] = up_obj

    cmds.delete(
        cmds.aimConstraint(
            aim_obj,
            target,
            offset=[0,0,0],
            w=True,
            aimVector=aimVector,
            upVector=upVector,
            worldUpType=worldUpType,
            **settings
        )
    )

    cmds.delete(aim_obj)
    cmds.delete(up_obj)

def aim_nodes_from_root(root_jnt=None, type='jonit', aim_axis='x', up_axis='y', worldUpType='object', worldSpace=False):
    # 選択したトップジョイントを選択して実行
    joints = cmds.ls(root_jnt, dag=True, type=type)
    sorted_joints = order_dags(joints)

    store_joint_values = OrderedDict()
    for sj in sorted_joints:
        store_joint_values[sj] = [cmds.xform(sj, q=True, t=True, ws=True),
                                  cmds.xform(sj, q=True, ro=True, ws=True)]

    tree = OrderedDict()

    for jnt in sorted_joints:
        tree[jnt] = OrderedDict()
        children = cmds.listRelatives(jnt, type=type, c=True)
        branches = OrderedDict()
        if children:
            if 1 < len(children):
                for chd in children:
                    branches[chd] = get_dag_nodes(obj=chd, type=type, remove_top=True)
            else:
                tree[jnt]['child'] = children[0]

        if branches:
            tree[jnt]['children'] = branches


    for jnt, child_info in tree.items():
        if 'child' in child_info.keys():
            child = child_info['child']

            # worldUpType='object' or worldUpType='scene'
            aim_nodes(base=child,
                      target=jnt,
                      aim_axis=aim_axis,
                      up_axis=up_axis,
                      worldUpType=worldUpType,
                      worldSpace=worldSpace)

            wt = store_joint_values[child][0]
            cmds.xform(child, t=wt, ws=True, a=True, p=True)

        # elif 'children' in child_info.keys():
        #     children = child_info['children']
        #     for chi, grand_chi in children.items():
        #         child_info = tree[chi]


        for obj, trs in store_joint_values.items():
            cmds.xform(obj, t=trs[0], ws=True, a=True, p=True)

            # if 'child' in tree[child].keys():
            #     grand_chi = tree[child]['child']
            #     wt = store_joint_values[grand_chi][0]
            #     cmds.xform(grand_chi, t=wt, ws=True, a=True, p=True)
