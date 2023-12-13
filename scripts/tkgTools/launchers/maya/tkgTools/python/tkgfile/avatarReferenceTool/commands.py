# -*- coding: utf-8 -*-
from maya import cmds, mel
import maya.api.OpenMaya as om2

import codecs
from collections import OrderedDict
import fnmatch
import json
import math
import os
import re
import traceback

# プラグインのロード
plugins = [
    'fbxmaya' # ここに追加
]
plugin_results = []
for plugin in plugins:
    plugin_result = cmds.loadPlugin(plugin) if not cmds.pluginInfo(plugin, q=True, l=True) else False
    plugin_results.append(plugin_result)

# fbxを読み込む際の値をoptionVarから取得
FILE_DIALOG_STYLE = cmds.optionVar(q='FileDialogStyle')
if FILE_DIALOG_STYLE == 1:
    FBX_TYPE = 'Fbx'
elif FILE_DIALOG_STYLE == 2:
    FBX_TYPE = 'FBX'

# このファイルのパスの取得
try:
    DIR_PATH = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
except:
    DIR_PATH = ''

# このファイル同階層のdataパスの取得
DATA_PATH = DIR_PATH + '/data/'

###########################
# p4vの設定
P4_MODULE_IMPORT = None
try:
    from P4 import P4, P4Exception
    # p4のインスタンスを作っておく
    p4 = P4()
    P4_MODULE_IMPORT = True
except:
    print(traceback.format_exc())

def p4v_set_from_config(file_name='C:/cygames/wiz2/.p4config'):
    text = None
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    if not text:
        return

    p4_equal_split = text.split('=')
    p4_split = list()
    for txt in p4_equal_split:
        enter_spl = txt.split('\n')
        if enter_spl:
            for tspl in enter_spl:
                if not tspl in p4_split:
                    p4_split.append(tspl)
        else:
            if not txt in p4_split:
                p4_split.append(txt)

    for i, line in enumerate(p4_split):
        if line == 'P4PORT':
            p4.port = p4_split[i+1]
        elif line == 'P4USER':
            p4.user = p4_split[i+1]
        elif line == 'P4CLIENT':
            p4.client = p4_split[i+1]

if P4_MODULE_IMPORT:
    P4V_CONNECT_STATUS = True
    WIZARD2_P4V_PORT = 'ssl:wizard2-perforce.cygames.jp:1666'
    if p4.port != WIZARD2_P4V_PORT:
        try:
            p4v_set_from_config()
        except:
            print(traceback.format_exc())
            P4V_CONNECT_STATUS = False
###########################

def avatar_collection():
    # 着せ替えリストの読み込み
    return json_transfer(DATA_PATH + 'avatar_collection.json', 'import')

def avatar_parts():
    # 着せ替えのIDと名称を読み込み
    return json_transfer(DATA_PATH + 'avatar_parts.json', 'import')

def prop_collection():
    # プロップのリストの読み込み
    return json_transfer(DATA_PATH + 'prop_collection.json', 'import')

def get_animation_status():
    # アニメーションの設定の取得
    start = cmds.playbackOptions(q=True, min=True)
    end = cmds.playbackOptions(q=True, max=True)
    animstart = cmds.playbackOptions(q=True, ast=True)
    animend = cmds.playbackOptions(q=True, aet=True)
    curtime = cmds.currentTime(q=True)
    if cmds.autoKeyframe(q=True, st=True):
        autoKeyState = True
    else:
        autoKeyState = False
    return start, end, animstart, animend, curtime, autoKeyState

def set_animation_status(start, end, animstart, animend, curtime, autoKeyState):
    # get_animation_statusで取得した値の設定
    cmds.playbackOptions(min=start)
    cmds.playbackOptions(max=end)
    cmds.playbackOptions(ast=animstart)
    cmds.playbackOptions(aet=animend)
    cmds.currentTime(curtime)
    cmds.autoKeyframe(st=autoKeyState)

def the_world(func):
    # ファイルのインポート、リファレンス時に状態を保持するデコレータ
    def wrapper(*args, **kwargs):
        try:
            cmds.refresh(su=1)

            # get
            start, end, animstart, animend, curtime, autoKeyState = get_animation_status()

            # 処理
            func(*args, **kwargs)

            # set
            set_animation_status(start, end, animstart, animend, curtime, autoKeyState)

            cmds.refresh(su=0)

        except:
            cmds.refresh(su=0)
            print(traceback.format_exc())

    return wrapper

@the_world
def create_ref(ref_name=None, path=None, type='avatar'):
    # 着せ替えの作成
    cmds.autoKeyframe(state=False)

    if path:
        if os.path.isfile(path):
            cmds.file(
                path,
                namespace=ref_name,
                r=True,
                type=FBX_TYPE,
                ignoreVersion=True,
                gl=True,
                mergeNamespacesOnClash=False,
            )

        cmds.currentTime(0.0)

        cmds.joint(ref_name+':Root', e=True, apa=True, ch=True)

        force_displaylayer_on(ref_name)

        if type == 'avatar':
            joint_connection(namespace=ref_name, connect=True)
            delete_sim_temps(sim_namespace=ref_name)
            create_sim_temp_ctrls(sim_namespace=ref_name, path=path)
        elif type == 'prop':
            create_prop_temp_ctrls(prop_namespace=ref_name, path=path)

@the_world
def replace_ref(ref_name=None, path=None, type='avatar'):
    # 着せ替えの更新
    cmds.autoKeyframe(state=False)

    if path:
        if os.path.isfile(path):
            cmds.file(
                path,
                loadReference=ref_name+'RN',
                type=FBX_TYPE
            )

        cmds.currentTime(0.0)

        cmds.joint(ref_name+':Root', e=True, apa=True, ch=True)

        force_displaylayer_on(ref_name)

        if type == 'avatar':
            joint_connection(namespace=ref_name, connect=True)
            delete_sim_temps(sim_namespace=ref_name)
            create_sim_temp_ctrls(sim_namespace=ref_name, path=path)
        elif type == 'prop':
            create_prop_temp_ctrls(prop_namespace=ref_name, path=path)

@the_world
def delete_ref(ref_name=None):
    # 着せ替えの削除
    joint_connection(namespace=ref_name, connect=False)
    if cmds.objExists(ref_name+'RN'):
        cmds.file(rr=True, referenceNode=ref_name+'RN')

    try:
        cmds.namespace(mergeNamespaceWithParent=True, removeNamespace=ref_name)
    except:
        # print(traceback.format_exc())
        pass

    delete_sim_temps(sim_namespace=ref_name)

def order_dags(dags=None):
    # アウトライナでベースでリストを整理する
    parent_dag = cmds.ls(dags[0], l=1, type='transform')[0].split('|')[1]

    all_hir = cmds.listRelatives(parent_dag, ad=True, f=True)
    hir_split_counter = {}
    for fp_node in all_hir:
        hir_split_counter[fp_node] = len(fp_node.split('|'))

    hir_split_counter_sorted = sorted(hir_split_counter.items(), key=lambda x:x[1])

    sorted_joint_list = [dag_count[0] for dag_count in hir_split_counter_sorted]

    all_ordered_dags = cmds.ls(sorted_joint_list)
    return [dag for dag in all_ordered_dags if dag in dags]

def go_to_bindPose_for_rig(namespace=None):
    # コントローラをbindPoseにする
    sel = cmds.ls(os=True)
    cmds.select(namespace + 'ctrl_sets', r=True, ne=True)
    ctrls = cmds.pickWalk(d='down')

    ctrls = order_dags(ctrls)

    for ctrl in ctrls:
        bt = cmds.getAttr(ctrl + '.bindPoseTranslate')[0]
        br = cmds.getAttr(ctrl + '.bindPoseRotate')[0]
        cmds.xform(ctrl, t=bt, ro=br, ws=True, p=True, a=True)

    if sel:
        cmds.select(sel, r=True)

def joint_connection(namespace=None, connect=None):
    # 読み込んだ着せ替えとキャラの骨を拘束する
    avatar_types_sets = 'avatar_types_sets'
    if not cmds.objExists(avatar_types_sets): cmds.sets(em=True, n=avatar_types_sets)

    type_sets = 'avatar_{}_sets'.format(namespace)

    if connect:
        if not cmds.objExists(type_sets): cmds.sets(em=True, n=type_sets)
        cmds.sets(type_sets, add=avatar_types_sets)

        chr_joints = cmds.ls('*:chr:Root', dag=True, type='joint')
        if not chr_joints:
            return

        chr_nss = chr_joints[0].replace(':Root', '')
        # print('chr_nss', chr_nss)
        # print('namespace', namespace)

        pa_cons = list()
        for chr_j in chr_joints:
            ty_j = chr_j.replace(chr_nss, namespace)
            try:
                pa_cons.append(cmds.parentConstraint(chr_j, ty_j, w=True)[0])
            except:
                print(traceback.format_exc())

        [cmds.sets(p, add=type_sets) for p in pa_cons]

    else:
        if cmds.objExists(type_sets):
            cmds.select(type_sets, r=True)
            pa_cons = cmds.pickWalk(d='down')
            cmds.delete(pa_cons)


def avatar_update(reference_set_dict, reference_cbox_dict):
    # 着せ替えの更新
    ref_info, ret_no_files = get_reference_info()
    for ref_name, type_path in reference_set_dict.items():
        print('ReferenceName: {}, Path: {}'.format(ref_name, type_path))

        cbox = reference_cbox_dict[ref_name]
        path = type_path[1]
        parts_type = type_path[0]

        try:
            anim_temp_save(ref_name=ref_name, parts_type=parts_type, operation='export')
        except:
            print(traceback.format_exc())

        if cbox.isChecked():
            if path:
                if os.path.isfile(path):
                    # replace
                    # replaceはやめて、delete > createにしてみる
                    # replace_ref(ref_name=ref_name, path=path)

                    # delete
                    delete_ref(ref_name=ref_name)

                    # create
                    create_ref(ref_name=ref_name, path=path)

                else:
                    print('#'*50)
                    print('{} part is not exist'.format(ref_name))
                    print('{}'.format(path))
                    print('#'*50)

        else:
            delete_ref(ref_name=ref_name)

def prop_update(ref_name, path, unload, chr_nss):
    # プロップの更新をする
    if unload:
        delete_ref(ref_name=ref_name)
        return

    create_ref(ref_name=ref_name, path=path, type='prop')
    go_to_bindPose_for_rig(namespace=chr_nss)

@the_world
def match_transform(src, dst, chr_nss):
    if cmds.objExists(src) and cmds.objExists(dst):
        go_to_bindPose_for_rig(namespace=chr_nss)
        cmds.matchTransform(src, dst, pos=True, rot=True, scl=False)

def get_offSet_Root(attach_node=None, filter=None):
    oft_roots = cmds.ls(attach_node, r=True)
    offSet_Root = None
    if oft_roots:
        if len(oft_roots) == 1:
            offSet_Root = oft_roots[0]
        else:
            for oft_r in oft_roots:
                if filter in oft_r:
                    offSet_Root = oft_r
                    break
        return offSet_Root



def force_constraint(src=None, tgt=None):
    cnsts = []
    try:
        con = cmds.pointConstraint(src, tgt, w=True)
        cnsts.append(con[0])
    except:
        print(traceback.format_exc())

    try:
        con = cmds.orientConstraint(src, tgt, w=True)
        cnsts.append(con[0])
    except:
        print(traceback.format_exc())

    try:
        con = cmds.scaleConstraint(src, tgt, w=True)
        cnsts.append(con[0])
    except:
        print(traceback.format_exc())

    return cnsts

def fbx_to_rig_for_prop(attach_ctrl=None, ref_name=None):
    bake_objects = []
    bake_objects.append(attach_ctrl)

    delete_objects = []
    # attach_ctrl = 'p2:Handattach_R_ctrl'
    # ref_name = 'pro_0'
    wt = cmds.xform(attach_ctrl, q=True, t=True, ws=True)
    wr = cmds.xform(attach_ctrl, q=True, ro=True, ws=True)

    temp_jnt_sets = '{}_prop_temp_jnt_sets'.format(ref_name)
    # cmds.select(temp_jnt_sets, r=True, ne=True)
    # base_joints = cmds.pickWalk(d='down');cmds.ls(os=True)

    dups = cmds.duplicate(ref_name + ':Root')
    consts = cmds.ls(dups[0], dag=True, type='constraint', l=True)
    [cmds.delete(c) for c in consts]
    dup_jnts = cmds.ls(dups[0], dag=True, l=True)
    # cmds.makeIdentity(dup_jnts, n=False, s=True, r=True, t=True, apply=True, pn=True)
    [cmds.setAttr(jnt+'.ssc', False) for jnt in dup_jnts]
    delete_objects.append(dups[0])

    temp_ctrl_sets = '{}_prop_temp_ctrl_sets'.format(ref_name)
    cmds.select(temp_ctrl_sets, r=True, ne=True)
    ctrls = cmds.pickWalk(d='down');cmds.ls(os=True)

    ordered_ctrls = order_dags(ctrls)

    all_consts = []
    for ctrl in ordered_ctrls:
        bake_objects.append(ctrl)
        spl_ctrl = ctrl.split(':')[-1]
        jnt = spl_ctrl.replace('_ctrl', '')
        if 'Root' in jnt:
            con = cmds.pointConstraint(jnt, attach_ctrl, w=True)
            all_consts.append(con[0])

            con = cmds.orientConstraint(jnt, attach_ctrl, w=True)
            all_consts.append(con[0])

            cmds.connectAttr(jnt+'.sx', ref_name + ':Root_ctrl.sx', f=True)
            cmds.connectAttr(jnt+'.sy', ref_name + ':Root_ctrl.sy', f=True)
            cmds.connectAttr(jnt+'.sz', ref_name + ':Root_ctrl.sz', f=True)

        else:
            # cmds.matchTransform(jnt, ctrl)
            #
            # consts = force_constraint(src=jnt, tgt=ctrl)
            # [all_consts.append(c) for c in consts]

            con = cmds.pointConstraint(jnt, ctrl, w=True)
            all_consts.append(con[0])

            con = cmds.orientConstraint(jnt, ctrl, w=True)
            all_consts.append(con[0])

            cmds.connectAttr(jnt+'.rx', ctrl+'.rx', f=True)
            cmds.connectAttr(jnt+'.ry', ctrl+'.ry', f=True)
            cmds.connectAttr(jnt+'.rz', ctrl+'.rz', f=True)

            cmds.connectAttr(jnt+'.sx', ctrl+'.sx', f=True)
            cmds.connectAttr(jnt+'.sy', ctrl+'.sy', f=True)
            cmds.connectAttr(jnt+'.sz', ctrl+'.sz', f=True)

    cmds.xform(attach_ctrl, t=wt, ws=True, a=True)
    cmds.xform(attach_ctrl, ro=wr, ws=True, a=True)

    [delete_objects.append(con) for con in all_consts]

    return bake_objects, delete_objects

def parent_constraint(src, dst):
    pos_con = cmds.pointConstraint(src, dst, w=True)
    ori_con = cmds.orientConstraint(src, dst, w=True)
    return pos_con[0], ori_con[0]

def get_prop_enum_spaces(obj):
    if cmds.objExists(obj + '.propLocalSpace'):
        enums = cmds.addAttr(obj + '.propLocalSpace', q=True, en=True)
        current = cmds.getAttr(obj + '.propLocalSpace')

    elif cmds.objExists(obj + '.space'):
        enums = cmds.addAttr(obj + '.space', q=True, en=True)
        current = cmds.getAttr(obj + '.space')

    enums_list = enums.split(':')
    return enums_list, current


def switch_prop_space(obj, space):
    if cmds.objExists(obj + '.propLocalSpace') or cmds.objExists(obj + '.space'):
        wt = cmds.xform(obj, q=True, t=True, ws=True)
        wr = cmds.xform(obj, q=True, ro=True, ws=True)

        enums_list, current = get_prop_enum_spaces(obj)
        if space in enums_list:
            en_num = enums_list.index(space)
            if cmds.objExists(obj + '.propLocalSpace'):
                cmds.setAttr(obj + '.propLocalSpace', en_num)
            elif cmds.objExists(obj + '.space'):
                cmds.setAttr(obj + '.space', en_num)

        cmds.xform(obj, t=wt, ro=wr, ws=True, a=True)

def create_prop_network(ctrl, jnt, root_ctrl, attach_node, pro_part, pro_id, space, path, pos_con=None, ori_con=None):
    # ctrl = 'p1:PropAttach_01_ctrl'
    # jnt = 'pro_0:Root'
    # attach_node = 'pro_0:offSet_Root'
    # pro_part = 'pro_aasdasdasd'
    # pro_id = 'pro_aaa'
    # space = 'Spine3'
    # path =

    prop_network_sets = 'prop_network_sets'
    if not cmds.objExists(prop_network_sets):
        cmds.sets(em=True, n=prop_network_sets)

    ctrl_prop_network = '{}_prop_network'.format(ctrl)
    if not cmds.objExists(ctrl_prop_network):
        cmds.createNode('network', n=ctrl_prop_network, ss=True)

    # pro part
    if not cmds.objExists(ctrl_prop_network + '.propPart'):
        cmds.addAttr(ctrl_prop_network, ln='propPart', dt='string')
        cmds.setAttr(ctrl_prop_network + '.propPart', e=True, cb=True)
        cmds.setAttr(ctrl_prop_network + '.propPart', pro_part, type='string')

    # pro id
    if not cmds.objExists(ctrl_prop_network + '.propID'):
        cmds.addAttr(ctrl_prop_network, ln='propID', dt='string')
        cmds.setAttr(ctrl_prop_network + '.propID', e=True, cb=True)
        cmds.setAttr(ctrl_prop_network + '.propID', pro_id, type='string')

    # pro path
    if not cmds.objExists(ctrl_prop_network + '.propPath'):
        cmds.addAttr(ctrl_prop_network, ln='propPath', dt='string')
        cmds.setAttr(ctrl_prop_network + '.propPath', e=True, cb=True)
        cmds.setAttr(ctrl_prop_network + '.propPath', path, type='string')

    # space
    if not cmds.objExists(ctrl_prop_network + '.space'):
        cmds.addAttr(ctrl_prop_network, ln='space', dt='string')
        cmds.setAttr(ctrl_prop_network + '.space', e=True, cb=True)
        cmds.setAttr(ctrl_prop_network + '.space', space, type='string')

    # const
    if not cmds.objExists(ctrl_prop_network + '.constraints'):
        cmds.addAttr(ctrl_prop_network, ln='constraints', dt='string')
        cmds.setAttr(ctrl_prop_network + '.constraints', e=True, cb=True)
        if pos_con and ori_con:
            cmds.setAttr(ctrl_prop_network + '.constraints', '{},{}'.format(pos_con, ori_con), type='string')

    affects = [
        ctrl,
        jnt,
        root_ctrl,
        attach_node
    ]

    for i, af in enumerate(affects):
        if af == ctrl:
            at = 'ctrl'
        elif af == jnt:
            at = 'Root'
        elif af == root_ctrl:
            at = 'RootCtrl'
        elif af == attach_node:
            at = 'attachNode'

        if not cmds.objExists(ctrl_prop_network + '.' + at):
            cmds.addAttr(ctrl_prop_network, ln=at, dt='string')
        cmds.setAttr(ctrl_prop_network + '.' + at, e=True, cb=True)
        cmds.setAttr(ctrl_prop_network + '.' + at, af, type='string')

    if cmds.objExists(prop_network_sets):
        cmds.sets(ctrl_prop_network, add=prop_network_sets)

def get_reference_info():
    ret = []
    ret_no_files = OrderedDict()

    refNodes = cmds.ls(references=True)
    for RNnode in refNodes:
        ref = {}
        try:
            file_name = cmds.referenceQuery(RNnode, filename=True, failedEdits=True)

            if os.path.isfile(file_name):
                ref.update({
                    'namespace' : cmds.referenceQuery(RNnode, namespace=True, failedEdits=True),
                    'filename'   : cmds.referenceQuery(RNnode, filename=True, failedEdits=True),
                    'w_filenam' : cmds.referenceQuery(RNnode, filename=True, withoutCopyNumber=True, failedEdits=True),
                    'isLoaded'  : cmds.referenceQuery(RNnode, isLoaded=True, failedEdits=True),
                    'nodes'     : cmds.referenceQuery(RNnode, nodes=True, failedEdits=True),
                    'node'      : cmds.referenceQuery(RNnode, nodes=True, failedEdits=True),
                    })
                ret.append(ref)

            else:
                ret_no_files[RNnode.replace('RN', '')] = file_name

        except:
            cmds.lockNode(RNnode, l=False)
            cmds.delete(RNnode)

            ret_no_files[RNnode.replace('RN', '')] = None
            print(traceback.format_exc())

    return ret, ret_no_files

def force_displaylayer_on(namespace=None):
    disp_lays = cmds.ls(type='displayLayer')
    [cmds.setAttr(dl+'.displayType', 2) for dl in disp_lays if namespace+':' in dl]


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

def round_value(value=None, digit=None):
    return truncate(round(value, digit), digit)

def order_joints(joints=None):
    parent_jnt = cmds.ls(joints[0], l=1, type='joint')[0].split('|')[1]

    all_hir = cmds.listRelatives(parent_jnt, ad=True, f=True)
    hir_split_counter = {}
    for fp_node in all_hir:
        hir_split_counter[fp_node] = len(fp_node.split('|'))

    hir_split_counter_sorted = sorted(hir_split_counter.items(), key=lambda x:x[1])

    sorted_joint_list = [jnt_count[0] for jnt_count in hir_split_counter_sorted]

    all_ordered_jnts = cmds.ls(sorted_joint_list)
    return [jnt for jnt in all_ordered_jnts if jnt in joints]


def round_attrs(obj=None, attrs=None):
    for at in attrs:
        set_at = '{}.{}'.format(obj, at)
        val = cmds.getAttr(set_at)
        if not val == 0.0:
            if 'e' in str(val):
                cmds.setAttr(set_at, 0.0)
                continue

            try:
                cmds.setAttr(set_at, truncate(round(val, 3), 3))
            except Exception as e:
                print(traceback.format_exc())

def get_round_trs(obj=None, obj_values=None):
    obj_values[obj] = {}
    obj_values[obj]['lt'] = [truncate(round(val, 3), 3) for val in cmds.xform(obj, q=True, t=True)]
    obj_values[obj]['lr'] = [truncate(round(val, 3), 3) for val in cmds.xform(obj, q=True, ro=True, os=True)]
    obj_values[obj]['s'] = [truncate(round(val, 3), 3) for val in cmds.xform(obj, q=True, s=True, os=True)]
    obj_values[obj]['wt'] = [truncate(round(val, 3), 3) for val in cmds.xform(obj, q=True, t=True, ws=True)]
    obj_values[obj]['wr'] = [truncate(round(val, 3), 3) for val in cmds.xform(obj, q=True, ro=True, ws=True)]
    obj_values[obj]['jo'] = [truncate(round(val, 3), 3) for val in cmds.getAttr(obj+'.jo')[0]]
    obj_values[obj]['p'] = cmds.listRelatives(obj, p=True)[0] or None

def import_export_joint_values(top_node=None, operation='export', save_path=None):
    if top_node:
        nodes = cmds.ls(top_node, type='joint', dag=True)
        ordered = order_joints(nodes)

    obj_values = OrderedDict()
    if operation == 'export':
        for obj in ordered:
            get_round_trs(obj, obj_values)

    user_path = os.environ['USER']
    make_path = 'C:/Users/'+user_path+'/Documents/maya/scripts/joint_values'
    if not os.path.isdir(make_path):
        os.makedirs(make_path)

    if not save_path:
        save_path = make_path + '/' + 'joints.json'

    if operation == 'import':
        return json_transfer(save_path, 'import')
    elif operation == 'export':
        json_transfer(save_path, 'export', obj_values)

    print('#'*20)
    print('Save Joint Values', save_path)
    print('#'*20)

def json_transfer(file_name=None, operation=None, export_values=None):
    u"""
    param:
        file_name = 'file_path'
        operation = 'import' or 'export'
        export_values = dict

    dict = json_transfer(file_name, 'import')
    json_transfer(file_name, 'export', dict)
    """
    encodings = ["utf-8", "shift_jis", "iso-2022-jp", "euc-jp"]
    if operation == 'export':
        try:
            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)
        except:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

    elif operation == 'import':
        for encoding in encodings:
            try:
                with codecs.open(file_name, 'r', encoding=encoding) as f:
                    return json.load(f, encoding, object_pairs_hook=OrderedDict)
            except:
                with open(file_name, 'r', encoding=encoding) as f:
                    return json.load(f, object_pairs_hook=OrderedDict)

def set_init_values(joint_values=None, namespace=None, set_type=''):
    if not namespace:
        namespace = ''

    for obj, values in joint_values.items():
        set_obj = namespace + obj

        lt = values['lt']
        lr = values['lr']
        s = values['s']
        wt = values['wt']
        wr = values['wr']
        jo = values['jo']
        p = values['p']

        settings = {}
        if set_type == 'local_translate':
            settings['t'] = lt
            settings['a'] = True

        if cmds.objExists(set_obj): cmds.xform(set_obj, **settings)

def import_fbx(fbx_path=None, nss=None, new_scene=None):
    if new_scene: cmds.file(new=True, f=True)

    if not cmds.namespace(ex=nss): cmds.namespace(add=nss)
    cmds.namespace(set=nss)

    basename_without_ext = os.path.splitext(os.path.basename(fbx_path))[0]
    cmds.file(
        fbx_path,
        i=True,
        type=FBX_TYPE,
        ignoreVersion=True,
        mergeNamespacesOnClash=False,
        pr=True,
        importTimeRange='override',
        importFrameRate=True,
        ra=True,
        namespace=basename_without_ext
    )

    cmds.namespace(set=':')

    nss = nss + ':'
    return cmds.ls('{}*'.format(nss), type='transform')

def save_fbx_maya(nss=None, fbx_path=None):
    temp_ma_ext = os.path.basename(fbx_path).replace('.fbx', '.ma')

    temp_folder = os.environ['TEMP'].replace('\\', '/') + '/FBX_Mixer/'
    if not os.path.isdir(temp_folder):
        os.makedirs(temp_folder)

    ma_path = temp_folder + nss + '_' + temp_ma_ext

    cmds.file(rn=ma_path)
    cmds.file(f=True, save=True, options='v=0', type='mayaAscii')

    cmds.file(new=True, f=True)

    return ma_path

def import_maya(nss=None, ma_path=None):
    cmds.file(
        fbx_path,
        i=True,
        ignoreVersion=True,
        mergeNamespacesOnClash=False,
        pr=True,
        importTimeRange='override',
        importFrameRate=True,
        ra=True,
        namespace=nss
    )

def get_anim_curves(nodes=None):
    connections = cmds.listConnections(nodes, s=True, d=True)
    if not connections:
        return

    connection_lists = om2.MSelectionList()
    [connection_lists.add(connection) for connection in connections]
    iter_ = om2.MItSelectionList(connection_lists, om2.MFn.kAnimCurve)
    anim_curves = list()
    while not iter_.isDone():
        # cmds.delete(iter_.getStrings())
        anim_curves.append(iter_.getStrings()[0])
        iter_.next()

    return anim_curves

def move_anim_start(nodes=None, start=None):
    anim_curves = get_anim_curves(nodes)
    [cmds.keyframe(anc, e=True, iub=True, r=True, o='over', tc=start) for anc in anim_curves]


def delete_anim_curves(nodes=None, delete_types=None):
    anim_curves = get_anim_curves(nodes)

    if delete_types:
        for anim_curve in anim_curves:
            dst_plugs = cmds.listConnections(anim_curve, d=True, p=True)
            for dt in delete_types:
                translate_connects = [p for p in dst_plugs if dt in p]
                if translate_connects:
                    cmds.delete(anim_curve)

    else:
        cmds.delete(anim_curves)

def bake_with_func(func):
    def wrapper(*args, **kwargs):
        try:
            cmds.refresh(su=1)

            cur_time=cmds.currentTime(q=1)
            if cmds.autoKeyframe(q=True, st=True):
                autoKeyState = True
            else:
                autoKeyState = False

            cmds.autoKeyframe(st=0)

            start = cmds.playbackOptions(q=1, min=1)
            end = cmds.playbackOptions(q=1, max=1)

            for i in range (int(start), int(end+1)):
                cmds.currentTime(i, e=True)
                func(*args, **kwargs)

            cmds.currentTime(cur_time)
            cmds.autoKeyframe(state=autoKeyState)

            cmds.refresh(su=0)

        except:
            cmds.refresh(su=0)
            print(traceback.format_exc())

    return wrapper

def quaternionToEuler(obj=None):
    rot = cmds.xform(obj, q=True, ro=True, os=True)
    rotOrder = cmds.getAttr('{}.rotateOrder'.format(obj))
    euler = om2.MEulerRotation(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder)
    quat = euler.asQuaternion()
    euler = quat.asEulerRotation()
    r = euler.reorder(rotOrder)

    cmds.xform(obj, ro=[math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)], os=True, a=True)

    cmds.setKeyframe(obj, at='rotate')

    return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)

@bake_with_func
def correctkeys(objects=None):
    [quaternionToEuler(obj=obj) for obj in objects] if objects else False

def remove_namespace():
    while True:
        all_namespace = cmds.namespaceInfo(listOnlyNamespaces=True)
        li_uniq = list(set(all_namespace))
        nums = len(li_uniq)
        if nums == 2:
            break
        else:
            for i in range(nums):
                if li_uniq[i] != "UI" and li_uniq[i] != "shared":
                    cmds.namespace(mergeNamespaceWithParent=True, removeNamespace=li_uniq[i])

def find_files(directory=None, pattern=None, exact=None):
    for root, dirs, files in os.walk(directory):
        if root.endswith(exact):
            continue
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def in_line_for_files(ret_no_files=None):
    files = OrderedDict()
    if ret_no_files:
        for nss, file in ret_no_files.items():
            ret_not_dir = os.path.dirname(file)
            found_files = os.listdir(ret_not_dir)
            files[nss] = ['{}/{}'.format(ret_not_dir, f) for f in found_files]
    return files

def export_avatar_collection(type='avatar'):
    if type == 'avatar':
        root_path = 'c:/cygames/wiz2/team/3dcg/chr/ply/'
    elif type == 'prop':
        root_path = 'c:/cygames/wiz2/team/3dcg/chr/pro/'

    tools_path = 'c:/cygames/wiz2/tools/maya/scripts/rig/'
    main_cat_num = 7

    searched_files = find_files(root_path, '*.fbx', 'old')
    files = OrderedDict()
    for f in searched_files:
        spl_file = f.replace('\\', '/')
        main_cat = spl_file.split('/')[main_cat_num]

        file_name = os.path.splitext(os.path.basename(spl_file))[0]
        if not main_cat in files.keys():
            files[main_cat] = OrderedDict()

        files[main_cat][file_name] = spl_file

    try:
        export_path = 'C:/Users/'+os.getenv('USER')+'/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/python/tkgfile/avatarReferenceTool/data/{}_collection.json'.format(type)
        json_transfer(file_name=export_path, operation='export', export_values=files)
    except Exception as e:
        pass

    p4v_status = True
    try:
        # from P4 import P4, P4Exception
        #
        # p4 = P4()

        # Perforceサーバーへの接続情報を設定
        # p4.port = "ssl:wizard2-perforce.cygames.jp:1666"
        # p4.user = "takagi_shunsuke"
        # p4.password = "your-password"
        # p4.client = "your-workspace-name"

        def checkout_file(file_path):
            try:
                p4.connect()

                # ファイルをチェックアウト
                p4.run_edit(file_path)
                # print(f"ファイル '{file_path}' をチェックアウトしました。")

            except P4Exception as e:
                for warning in p4.warnings:
                    print(warning)
                for error in p4.errors:
                    print(error)

            finally:
                p4.disconnect()

        export_path = tools_path + 'avatarReferenceTool/data/{}_collection.json'.format(type)
        if P4V_CONNECT_STATUS:
            checkout_file(export_path)
        json_transfer(file_name=export_path, operation='export', export_values=files)

    except Exception as e:
        p4v_status = False
        print(traceback.format_exc())

    return p4v_status

def revert_file(file_path):
    try:
        # from P4 import P4, P4Exception
        # p4 = P4()
        #
        # p4v_set_from_config()

        if P4V_CONNECT_STATUS:
            try:
                p4.connect()
                # ファイルをリバート
                p4.run_revert(file_path)
            except P4Exception as e:
                for warning in p4.warnings:
                    print(warning)
                for error in p4.errors:
                    print(error)
            finally:
                p4.disconnect()

    except Exception as e:
        print(traceback.format_exc())


def extract_fbx_(combine_fbx=None, base_fbx=None, hip_pos=None, save_fbx=None, set_local_translate=None):
    fbx_dict = {
        'combine':combine_fbx,
        'base':base_fbx,
        'extract':base_fbx
    }

    apply_fbx = {}
    for nss, fbx_path in fbx_dict.items():
        imported_objects = import_fbx(fbx_path, nss, new_scene=None)
        apply_fbx[nss] = imported_objects

    combine_jnts = cmds.ls(apply_fbx['combine'], type='joint')
    base_jnts = cmds.ls(apply_fbx['base'], type='joint')
    extract_jnts = cmds.ls(apply_fbx['extract'], type='joint')

    print("combine")
    print(combine_jnts)
    print("base")
    print(base_jnts)
    print("extract")
    print(extract_jnts)

    combine_jnts.sort()
    base_jnts.sort()
    extract_jnts.sort()

    correctkeys(objects=combine_jnts)
    correctkeys(objects=base_jnts)

    delete_anim_curves(nodes=extract_jnts)

    start = cmds.playbackOptions(q=True, min=True)
    end = cmds.playbackOptions(q=True, max=True)

    animated = list()
    extract_pairBlend_sets = 'extract_pairBlend_sets'
    if not cmds.objExists(extract_pairBlend_sets): cmds.sets(n=extract_pairBlend_sets, em=True)
    for combine_jnt, base_jnt, extract_jnt in zip(combine_jnts, base_jnts, extract_jnts):
        combine_pb = cmds.createNode('pairBlend', ss=True)
        base_pb = cmds.createNode('pairBlend', ss=True)
        double_pb = cmds.createNode('pairBlend', ss=True)

        cmds.sets(combine_pb, add=extract_pairBlend_sets)
        cmds.sets(base_pb, add=extract_pairBlend_sets)
        cmds.sets(double_pb, add=extract_pairBlend_sets)

        cmds.setAttr('{}.weight'.format(combine_pb), 0.5)
        cmds.setAttr('{}.weight'.format(base_pb), -1)
        cmds.setAttr('{}.weight'.format(double_pb), 2)

        cmds.connectAttr(
            '{}.r'.format(base_jnt),
            '{}.inRotate2'.format(base_pb),
            f=True
        )

        cmds.connectAttr(
            '{}.outRotate'.format(base_pb),
            '{}.inRotate1'.format(combine_pb),
            f=True
        )

        cmds.connectAttr(
            '{}.r'.format(combine_jnt),
            '{}.inRotate2'.format(combine_pb),
            f=True
        )

        cmds.connectAttr(
            '{}.outRotate'.format(combine_pb),
            '{}.inRotate2'.format(double_pb),
            f=True
        )

        cmds.connectAttr(
            '{}.outRotate'.format(double_pb),
            '{}.r'.format(extract_jnt),
            f=True
        )


        cmds.refresh(su=True)

        cur_time=cmds.currentTime(q=True)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = True
        else:
            autoKeyState = False

        cmds.autoKeyframe(st=False)

        cmds.currentTime(start, e=True)
        wt = cmds.xform(extract_jnt, q=True, t=True)
        wr = cmds.xform(extract_jnt, q=True, ro=True)

        wt = [round_value(t, 4) for t in wt]
        wr = [round_value(r, 4) for r in wr]
        for i in range (int(start), int(end+1)):
            cmds.currentTime(i, e=True)
            cur_wt = [round_value(t, 4) for t in cmds.xform(extract_jnt, q=True, t=True)]
            cur_wr = [round_value(r, 4) for r in cmds.xform(extract_jnt, q=True, ro=True)]

            if (wt != cur_wt
                or wr != cur_wr):
                    animated.append(extract_jnt)
                    break

            wt = cmds.xform(extract_jnt, q=True, t=True)
            wr = cmds.xform(extract_jnt, q=True, ro=True)

            wt = [round_value(t, 4) for t in wt]
            wr = [round_value(r, 4) for r in wr]

        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)

        cmds.refresh(su=False)

    cmds.bakeResults(
        animated,
        simulation=True,
        t=(start, end),
        sampleBy=1,
        oversamplingRate=1,
        disableImplicitControl=True,
        preserveOutsideKeys=True,
        sparseAnimCurveBake=False,
        removeBakedAttributeFromLayer=False,
        removeBakedAnimFromLayer=False,
        bakeOnOverrideLayer=False,
        minimizeRotation=True,
        at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
    )

    cmds.select(extract_pairBlend_sets, r=True, ne=True);cmds.pickWalk(d='down')
    extract_pairBlend_list = cmds.ls(os=True)
    cmds.delete(extract_pairBlend_list)

    base_anim_nodes = cmds.ls('base:*')
    cmds.delete(base_anim_nodes)

    combine_anim_nodes = cmds.ls('combine:*')
    cmds.delete(combine_anim_nodes)

    # identical
    cmds.joint('extract:Root', e=True, apa=True, ch=True)
    cmds.xform('extract:Hip', t=hip_pos, a=True)
    #

    try:
        cmds.select('extract:Root', r=True)
        cmds.GoToBindPose()
    except:
        print(traceback.print_exc())

    [cmds.xform(n, ro=[0,0,0], a=True) for n in extract_jnts]

    start = cmds.playbackOptions(q=True, min=True)
    cmds.currentTime(start + 1)
    cmds.currentTime(start)

    cmds.bakeResults(
        extract_jnts,
        simulation=True,
        t=(start, start),
        sampleBy=1,
        oversamplingRate=1,
        disableImplicitControl=True,
        preserveOutsideKeys=True,
        sparseAnimCurveBake=False,
        removeBakedAttributeFromLayer=False,
        removeBakedAnimFromLayer=False,
        bakeOnOverrideLayer=False,
        minimizeRotation=True,
        at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
    )

    extract_anim_nodes = cmds.ls('extract:*', assemblies=True)
    cmds.select(extract_anim_nodes[0], r=True)

    remove_namespace()

    if set_local_translate:
        import_path = DATA_PATH + '/' + set_local_translate
        joint_values = import_export_joint_values(operation='import', save_path=import_path)

        extract_joints = [j for j in joint_values.keys()]
        delete_anim_curves(nodes=extract_joints, delete_types=['translate'])

        set_init_values(joint_values=joint_values, namespace=None, set_type='local_translate')

    if save_fbx:
        cmds.file(save_fbx, es=True, options='v=0;', typ='FBX export', pr=True, f=True)


# cmds.file(new=True, f=True)
# combine_fbx = "C:/Users/CF0990/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/additive/20230113/W_004_layer6_to_takagi_base_hand.fbx"
# base_fbx = "C:/Users/CF0990/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/additive/20230113/W_004_layer6_to_takagi_base.fbx"
# save_fbx = "C:/Users/CF0990/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/additive/20230113/W_004_layer6_to_takagi_hand.fbx"
# hip_pos=[0, 81.371, 0]
#
# extract_fbx_(combine_fbx, base_fbx, hip_pos, save_fbx)


##################################################

def combine_fbx_(base_fbx=None, extract_fbx=None, save_fbx=None):
    # fbx_dict = {
    #     'base':base_fbx,
    #     'extract':extract_fbx,
    #     'combine':base_fbx,
    # }

    fbx_dict = OrderedDict()
    fbx_dict['base'] = base_fbx
    fbx_dict['extract'] = extract_fbx
    fbx_dict['combine'] = base_fbx

    apply_fbx = {}
    maya_paths = list()
    maya_path_nss = list()
    time_ranges = OrderedDict()
    for nss, fbx_path in fbx_dict.items():
        # imported_objects = import_fbx(fbx_path, nss, new_scene=None)
        maya_path_nss.append(nss)

        cmds.file(new=True, f=True)

        imported_objects = import_fbx(fbx_path=fbx_path, nss=nss, new_scene=None)
        start = cmds.playbackOptions(q=1, min=1)
        end = cmds.playbackOptions(q=1, max=1)
        time_ranges[nss] = [start, end]

        if nss == 'extract':
            base_time = time_ranges['base']
            move_start_time = base_time[0] - start
            move_anim_start(nodes=imported_objects, start=move_start_time)

        ma_path = save_fbx_maya(nss=nss, fbx_path=fbx_path)
        apply_fbx[nss] = imported_objects
        maya_paths.append(ma_path)

    for maya_nss, maya_path in zip(maya_path_nss, maya_paths):
        basename_without_ext = os.path.splitext(os.path.basename(fbx_path))[0]
        cmds.file(
            maya_path,
            i=True,
            ignoreVersion=True,
            mergeNamespacesOnClash=False,
            pr=True,
            importTimeRange='override',
            importFrameRate=True,
            ra=True,
            rpr=basename_without_ext
        )

    combine_jnts = cmds.ls(apply_fbx['combine'], type='joint')
    base_jnts = cmds.ls(apply_fbx['base'], type='joint')
    extract_jnts = cmds.ls(apply_fbx['extract'], type='joint')

    combine_jnts.sort()
    base_jnts.sort()
    extract_jnts.sort()

    correctkeys(objects=base_jnts)

    delete_anim_curves(nodes=combine_jnts)
    combine_pairBlend_sets = 'combine_pairBlend_sets'
    if not cmds.objExists(combine_pairBlend_sets): cmds.sets(n=combine_pairBlend_sets, em=True)
    for combine_jnt, base_jnt, extract_jnt in zip(combine_jnts, base_jnts, extract_jnts):
        base_double_pb = cmds.createNode('pairBlend', ss=True)
        extract_double_pb = cmds.createNode('pairBlend', ss=True)
        combine_pb = cmds.createNode('pairBlend', ss=True)

        cmds.sets(base_double_pb, add=combine_pairBlend_sets)
        cmds.sets(extract_double_pb, add=combine_pairBlend_sets)
        cmds.sets(combine_pb, add=combine_pairBlend_sets)

        cmds.setAttr('{}.weight'.format(base_double_pb), 2)
        cmds.setAttr('{}.weight'.format(extract_double_pb), 2)
        cmds.setAttr('{}.weight'.format(combine_pb), 0.5)

        cmds.connectAttr(
            '{}.r'.format(base_jnt),
            '{}.inRotate2'.format(base_double_pb),
            f=True
        )

        cmds.connectAttr(
            '{}.r'.format(extract_jnt),
            '{}.inRotate2'.format(extract_double_pb),
            f=True
        )

        cmds.connectAttr(
            '{}.outRotate'.format(base_double_pb),
            '{}.inRotate1'.format(combine_pb),
            f=True
        )

        cmds.connectAttr(
            '{}.outRotate'.format(extract_double_pb),
            '{}.inRotate2'.format(combine_pb),
            f=True
        )

        cmds.connectAttr(
            '{}.outRotate'.format(combine_pb),
            '{}.r'.format(combine_jnt),
            f=True
        )

    # identical
    cmds.connectAttr('base:Root.t', 'combine:Root.t', f=True)
    cmds.connectAttr('base:Hip.t', 'combine:Hip.t', f=True)

    start = cmds.playbackOptions(q=True, min=True)
    end = cmds.playbackOptions(q=True, max=True)

    cmds.bakeResults(
        combine_jnts,
        simulation=True,
        t=(start, end),
        sampleBy=1,
        oversamplingRate=1,
        disableImplicitControl=True,
        preserveOutsideKeys=True,
        sparseAnimCurveBake=False,
        removeBakedAttributeFromLayer=False,
        removeBakedAnimFromLayer=False,
        bakeOnOverrideLayer=False,
        minimizeRotation=True,
        at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
    )

    cmds.select(combine_pairBlend_sets, r=True, ne=True);cmds.pickWalk(d='down')
    combine_pairBlend_list = cmds.ls(os=True)
    cmds.delete(combine_pairBlend_list)

    base_anim_nodes = cmds.ls('base:*')
    cmds.delete(base_anim_nodes)

    extract_anim_nodes = cmds.ls('extract:*')
    cmds.delete(extract_anim_nodes)

    combine_anim_nodes = cmds.ls('combine:*', assemblies=True)
    cmds.select(combine_anim_nodes[0], r=True)

    remove_namespace()

    if save_fbx:
        cmds.file(save_fbx, es=True, options='v=0;', typ='FBX export', pr=True, f=True)

def ctrl_transform(ctrl=None, edge_axis='-x', pos=None, rot=None, scl=None, line_width=2):
    if edge_axis:
        bbx = cmds.xform(ctrl, q=True, bb=True)

        pivot_axis = {
            'x':bbx[3],
            'y':bbx[4],
            'z':bbx[5],
            '-x':bbx[0],
            '-y':bbx[1],
            '-z':bbx[2],
        }

        pivot_value = {
            'x':[pivot_axis[edge_axis], 0, 0],
            'y':[0, pivot_axis[edge_axis], 0],
            'z':[0, 0, pivot_axis[edge_axis]],
            '-x':[pivot_axis[edge_axis], 0, 0],
            '-y':[0, pivot_axis[edge_axis], 0],
            '-z':[0, 0, pivot_axis[edge_axis]],
        }

        cmds.move(*pivot_value[edge_axis], ctrl+'.scalePivot', ctrl+'.rotatePivot', r=True)

    cmds.select(ctrl+'.cv[*]', r=True)
    if scl:
        cmds.scale(r=True, *scl)
    if rot:
        cmds.rotate(r=True, ocp=True, os=True, fo=True, *rot)
    if pos:
        cmds.move(r=True, os=True, wd=True, *pos)

    ctrl_shape = cmds.listRelatives(ctrl, s=True)[0]
    cmds.setAttr(ctrl_shape+'.lineWidth', line_width)

def set_rgb_color(ctrl=None, color=[1,1,1]):
    rgb = ("R","G","B")
    shape = cmds.listRelatives(ctrl, s=1)[0]
    cmds.setAttr(shape + ".overrideEnabled",1)
    cmds.setAttr(shape + ".overrideRGBColors",1)
    for channel, color in zip(rgb, color):
        cmds.setAttr(shape + ".overrideColor{}".format(channel), color)

def set_obj_color(obj=None, color=[0.5, 0.5, 0.5], outliner=None):
    cmds.setAttr(obj+'.useObjectColor', 2)
    cmds.setAttr(obj+'.wireColorRGB', *color)

    if outliner:
        cmds.setAttr(obj+'.useOutlinerColor', 1)
        cmds.setAttr(obj+'.outlinerColor', *color)

def temp_rename(obj=None, prefix=None, suffix=None, replace=None, mirrors=None):
    """
    obj=None, prefix=None, suffix=None, replace=None
    """
    # replace
    replace_name = obj
    if replace:
        replace_name = obj.replace(*replace)

    # prefix
    if not prefix:
        prefix = ''
    prefix_name = re.sub("^", prefix, replace_name)

    # suffix
    if not suffix:
        suffix = ''
    renamed = re.sub("$", suffix, prefix_name)

    if mirrors:
        return self.mirror(mirrors=mirrors, src=renamed)
    return renamed


def create_controller(obj=None, ctrl_type='cube', edge_axis='-x',
                      pos=None, rot=None, scl=None, line_width=2,
                      prefix=None, suffix=None, replace=None, mirrors=None, rgb=[0.1, 0.9, 0.5]):

    if (not prefix
        and not suffix
        and not replace
        and not mirrors):
        ctrl = obj+'_ctrl'
    else:
        ctrl = temp_rename(obj, prefix, suffix, replace, mirrors)

    if cmds.objExists(ctrl):
        return False

    controller_settings = {
        u'cube': {
            'degree': 1,
            'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            'periodic': False,
            'points': [[0.5, 0.5, 0.5],
                      [0.5, 0.5, -0.5],
                      [-0.5, 0.5, -0.5],
                      [-0.5, -0.5, -0.5],
                      [0.5, -0.5, -0.5],
                      [0.5, 0.5, -0.5],
                      [-0.5, 0.5, -0.5],
                      [-0.5, 0.5, 0.5],
                      [0.5, 0.5, 0.5],
                      [0.5, -0.5, 0.5],
                      [0.5, -0.5, -0.5],
                      [-0.5, -0.5, -0.5],
                      [-0.5, -0.5, 0.5],
                      [0.5, -0.5, 0.5],
                      [-0.5, -0.5, 0.5],
                      [-0.5, 0.5, 0.5]]},
         u'cross': {'degree': 1,
                    'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    'periodic': False,
                    'points': [[0.4, 0.0, -0.4],
                               [0.4, 0.0, -2.0],
                               [-0.4, 0.0, -2.0],
                               [-0.4, 0.0, -0.4],
                               [-2.0, 0.0, -0.4],
                               [-2.0, 0.0, 0.4],
                               [-0.4, 0.0, 0.4],
                               [-0.4, 0.0, 2.0],
                               [0.4, 0.0, 2.0],
                               [0.4, 0.0, 0.4],
                               [2.0, 0.0, 0.4],
                               [2.0, 0.0, -0.4],
                               [0.4, 0.0, -0.4]]},
         u'rombus3': {'degree': 1,
                      'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                      'periodic': False,
                      'points': [[0.0, 0.0, 2.0],
                                 [-0.707107, 0.707107, 0.0],
                                 [0.0, 0.0, -2.0],
                                 [0.707107, 0.707107, 0.0],
                                 [0.0, 0.0, 2.0],
                                 [0.707107, -0.707107, 0.0],
                                 [0.0, 0.0, -2.0],
                                 [-0.707107, -0.707107, 0.0],
                                 [0.707107, -0.707107, 0.0],
                                 [0.707107, 0.707107, 0.0],
                                 [-0.707107, 0.707107, 0.0],
                                 [-0.707107, -0.707107, 0.0],
                                 [0.0, 0.0, 2.0]]},
         u'locator': {'degree': 1,
                      'knot': [0, 1, 2, 3, 4, 5, 6, 7],
                      'periodic': False,
                      'points': [[-2.0, 0.0, 0.0],
                                 [2.0, 0.0, 0.0],
                                 [0.0, 0.0, 0.0],
                                 [0.0, 0.0, 2.0],
                                 [0.0, 0.0, -2.0],
                                 [0.0, 0.0, 0.0],
                                 [0.0, 2.0, 0.0],
                                 [0.0, -2.0, 0.0]]},
         u'sphere': {'degree': 1,
                     'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
                     'periodic': False,
                     'points': [[0.0, 0.0, 1.0],
                                [0.0, 0.5, 0.866025],
                                [0.0, 0.866025, 0.5],
                                [0.0, 1.0, 0.0],
                                [0.0, 0.866025, -0.5],
                                [0.0, 0.5, -0.866025],
                                [0.0, 0.0, -1.0],
                                [0.0, -0.5, -0.866025],
                                [0.0, -0.866025, -0.5],
                                [0.0, -1.0, 0.0],
                                [0.0, -0.866025, 0.5],
                                [0.0, -0.5, 0.866025],
                                [0.0, 0.0, 1.0],
                                [0.707107, 0.0, 0.707107],
                                [1.0, 0.0, 0.0],
                                [0.707107, 0.0, -0.707107],
                                [0.0, 0.0, -1.0],
                                [-0.707107, 0.0, -0.707107],
                                [-1.0, 0.0, 0.0],
                                [-0.866025, 0.5, 0.0],
                                [-0.5, 0.866025, 0.0],
                                [0.0, 1.0, 0.0],
                                [0.5, 0.866025, 0.0],
                                [0.866025, 0.5, 0.0],
                                [1.0, 0.0, 0.0],
                                [0.866025, -0.5, 0.0],
                                [0.5, -0.866025, 0.0],
                                [0.0, -1.0, 0.0],
                                [-0.5, -0.866025, 0.0],
                                [-0.866025, -0.5, 0.0],
                                [-1.0, 0.0, 0.0],
                                [-0.707107, 0.0, 0.707107],
                                [0.0, 0.0, 1.0]]},

    }

    curve_settings = {}
    curve_settings['d'] = controller_settings[ctrl_type]['degree']
    curve_settings['p'] = controller_settings[ctrl_type]['points']
    curve_settings['k'] = controller_settings[ctrl_type]['knot']
    crv = cmds.curve(**curve_settings)
    shape = cmds.listRelatives(crv, s=True) or None
    if shape: cmds.setAttr(shape[0] + '.ihi', 0)
    set_rgb_color(crv, rgb)
    set_obj_color(obj=crv, color=rgb, outliner=True)
    ctrl_transform(crv, edge_axis, pos, rot, scl, line_width)

    if controller_settings[ctrl_type]['periodic']:
        cmds.closeCurve(crv, ch=True, ps=0, rpo=True, bb=0.5, bki=False, p=0.1)

    shape = cmds.listRelatives(crv, s=True)[0]
    joint = cmds.createNode('joint', ss=True)
    cmds.parent(shape, joint, r=True, s=True)
    cmds.setAttr(joint+'.drawStyle', 2)
    cmds.matchTransform(joint, obj)
#        cmds.joint(joint, e=True, spa=True, ch=True)
    cmds.makeIdentity(joint, n=False, s=False, r=True, t=False, apply=True, pn=True)

    cmds.delete(crv)

    cmds.rename(joint, ctrl)
    cmds.rename(shape, ctrl+'Shape')

    return ctrl


def create_temp_ctrls(joints=None, sim_parent=None, type='sim'):
    ctrls = list()
    ctrl_p = None
    consts = list()
    for jnt in joints:
        if type == 'sim':
            ctrl = create_controller(obj=jnt, ctrl_type='cube', edge_axis='-z',
                                  pos=None, rot=None, scl=[3, 10, 5], line_width=2,
                                  prefix=None, suffix='_ctrl', replace=None, mirrors=None, rgb=[0.1, 0.7, 0.8])

        elif type == 'prop':
            ctrl = create_controller(obj=jnt, ctrl_type='sphere', edge_axis=None,
                                  pos=None, rot=None, scl=[5, 5, 5], line_width=3,
                                  prefix=None, suffix='_ctrl', replace=None, mirrors=None, rgb=[0.1, 0.7, 0.4])

        if not ctrl:
            continue

        ctrls.append(ctrl)

        if ctrl_p:
            cmds.parent(ctrl, ctrl_p)

        ctrl_p = ctrl

        ori = cmds.orientConstraint(ctrl, jnt, w=True)
        cmds.setAttr(ori[0]+'.interpType', 2)
        consts.append(ori[0])
        # if type == 'prop':
        #     poc = cmds.pointCOnstraint(ctrl, jnt, w=True)
        #     scc = cmds.scaleConstraint(ctrl, jnt, w=True)
        #     consts.append(poc[0])
        #     consts.append(scc[0])


    ctrl_p_grp = '{}_grp'.format(ctrls[0])
    if not cmds.objExists(ctrl_p_grp):
        cmds.createNode('transform', n=ctrl_p_grp, ss=True)

    cmds.matchTransform(ctrl_p_grp, sim_parent)

    cmds.parentConstraint(sim_parent, ctrl_p_grp)

    cmds.parent(ctrls[0], ctrl_p_grp)

    pa = None
    for i, ctrl in enumerate(ctrls):
        if type == 'sim':
            cmds.setAttr(ctrl+'.tx', k=False, cb=False, l=True)
            cmds.setAttr(ctrl+'.ty', k=False, cb=False, l=True)
            cmds.setAttr(ctrl+'.tz', k=False, cb=False, l=True)
            cmds.setAttr(ctrl+'.sx', k=False, cb=False, l=True)
            cmds.setAttr(ctrl+'.sy', k=False, cb=False, l=True)
            cmds.setAttr(ctrl+'.sz', k=False, cb=False, l=True)

        elif type == 'prop':
            ctrl_ofs_grp = '{}_ofs_grp'.format(ctrl)
            if not cmds.objExists(ctrl_ofs_grp):
                cmds.createNode('transform', n=ctrl_ofs_grp, ss=True)
            cmds.matchTransform(ctrl_ofs_grp, ctrl)
            cmds.parent(ctrl, ctrl_ofs_grp)
            if i == 0:
                cmds.parent(ctrl_ofs_grp, ctrl_p_grp)
            if pa:
                cmds.parent(ctrl_ofs_grp, pa)
            pa = ctrl

            poc = cmds.pointConstraint(ctrl, ctrl.replace('_ctrl', ''), w=True)
            scc = cmds.scaleConstraint(ctrl, ctrl.replace('_ctrl', ''), w=True)
            consts.append(poc[0])
            consts.append(scc[0])


        cmds.setAttr(ctrl+'.radius', k=False, cb=False, l=True)
        cmds.setAttr(ctrl+'.v', k=False, cb=False, l=True)

    return ctrl_p_grp, ctrls, consts


def create_sim_temp_ctrls(sim_namespace=None, path=None):
    # chara_ids = ['p1', 'p2']
    # for cid in chara_ids:
    #     head_jnt = '{}:chr:Head'.format(cid)
    #     if cmds.objExists(head_jnt):
    #         break

    sim_p_grp = '{}_sim_temp_grp'.format(sim_namespace)
    if cmds.objExists(sim_p_grp):
        cmds.delete(sim_p_grp)

    if not cmds.objExists(sim_p_grp):
        cmds.createNode('transform', n=sim_p_grp, ss=True)

    sim_joints = cmds.ls('{}:UJ_*'.format(sim_namespace))
    if not sim_joints:
        if cmds.objExists(sim_p_grp):
            cmds.delete(sim_p_grp)

        return

    sim_root_joints = list()
    for jnt in sim_joints:
        if ('_01' in jnt
            or '_01_L' in jnt):
            if cmds.objectType(jnt) == 'joint':
                sim_root_joints.append(jnt)

    # 中央スカートをスキップする処理
    # for jnt in sim_root_joints:
    #     if ('SkirtA_01_R' in jnt
    #         or 'SkirtE_01_R' in jnt):
    #         sim_root_joints.remove(jnt)

    # ケルベロスの骨に合わせて対応
    if 'cerberus01' in path:
        add_belts = ['UJ_Belt_02_L', 'UJ_Belt_02_R']
        [sim_root_joints.append('{}:{}'.format(sim_namespace, belt_jnt)) for belt_jnt in add_belts]

    # print('sim_root_joints', sim_root_joints)

    for sim_root_jnt in sim_root_joints:
        create_ctrls_sts = True
        pa = cmds.listRelatives(sim_root_jnt, p=True)
        if pa:
            sim_parent = pa[0]

        joints = cmds.ls(sim_root_jnt, dag=True, type='joint')

        # ケルベロスの骨に合わせて対応
        if 'cerberus01' in path:
            belt_01 = sim_namespace + ':' + 'UJ_Belt_01'
            if belt_01 in joints:
                joints = [belt_01]

        joints = order_joints(joints)

        try:
            ctrl_p_grp, ctrls, consts = create_temp_ctrls(joints=joints, sim_parent=sim_parent)
        except:
            create_ctrls_sts = False

        if not create_ctrls_sts:
            continue

        cmds.parent(ctrl_p_grp, sim_p_grp)

        sim_temp_sets = '{}_sim_temp_sets'.format(sim_namespace)
        if not cmds.objExists(sim_temp_sets):
            cmds.sets(em=True, n=sim_temp_sets)

        # ctrls
        sim_ctrl_sets = '{}_sim_temp_ctrl_sets'.format(sim_namespace)
        if not cmds.objExists(sim_ctrl_sets):
            cmds.sets(em=True, n=sim_ctrl_sets)

        cmds.sets(sim_ctrl_sets, add=sim_temp_sets)

        ctrls.sort()
        for ctrl in ctrls:
            removed_nss = ctrl.replace(sim_namespace + ':', '')
            splited = removed_nss.split('_')[1::]

            part_sets = sim_namespace + '_' + splited[0] + '_ctrl_sets'
            if not cmds.objExists(part_sets):
                cmds.sets(em=True, n=part_sets)

            cmds.sets(part_sets, add=sim_ctrl_sets)

            if '_L_' in ctrl or '_R_' in ctrl:
                part_side_sets = sim_namespace + '_' + splited[0] + '_' + splited[2] + '_ctrl_sets'
                if not cmds.objExists(part_side_sets):
                    cmds.sets(em=True, n=part_side_sets)

                cmds.sets(part_side_sets, add=part_sets)

                cmds.sets(ctrl, add=part_side_sets)

            else:
                cmds.sets(ctrl, add=part_sets)

        # joint
        sim_jnt_sets = '{}_sim_temp_jnt_sets'.format(sim_namespace)
        if not cmds.objExists(sim_jnt_sets):
            cmds.sets(em=True, n=sim_jnt_sets)

        cmds.sets(sim_jnt_sets, add=sim_temp_sets)

        for jnt in joints:
            cmds.sets(jnt, add=sim_jnt_sets)

        # consts
        sim_const_sets = '{}_sim_temp_const_sets'.format(sim_namespace)
        if not cmds.objExists(sim_const_sets):
            cmds.sets(em=True, n=sim_const_sets)

        cmds.sets(sim_const_sets, add=sim_temp_sets)

        for const in consts:
            cmds.sets(const, add=sim_const_sets)

def create_prop_temp_ctrls(prop_namespace=None, path=None):
    prop_p_grp = '{}_prop_temp_grp'.format(prop_namespace)
    if cmds.objExists(prop_p_grp):
        cmds.delete(prop_p_grp)

    if not cmds.objExists(prop_p_grp):
        cmds.createNode('transform', n=prop_p_grp, ss=True)

    prop_joints = cmds.ls('{}:*'.format(prop_namespace))
    if not prop_joints:
        if cmds.objExists(prop_p_grp):
            cmds.delete(prop_p_grp)

        return

    prop_root_joints = list()
    for jnt in prop_joints:
        if cmds.objectType(jnt) == 'joint':
            prop_root_joints.append(jnt)

    prop_temp_sets = '{}_prop_temp_sets'.format(prop_namespace)
    if not cmds.objExists(prop_temp_sets):
        cmds.sets(em=True, n=prop_temp_sets)

    # ctrls
    prop_ctrl_sets = '{}_prop_temp_ctrl_sets'.format(prop_namespace)
    if not cmds.objExists(prop_ctrl_sets):
        cmds.sets(em=True, n=prop_ctrl_sets)

    cmds.sets(prop_ctrl_sets, add=prop_temp_sets)

    prop_root_joints = order_joints(prop_root_joints)

    ctrls = []
    consts = []
    for i, jnt in enumerate(prop_root_joints):
        ctrl = create_controller(obj=jnt, ctrl_type='sphere', edge_axis=None,
                              pos=None, rot=None, scl=[5, 5, 5], line_width=3,
                              prefix=None, suffix='_ctrl', replace=None, mirrors=None, rgb=[0.1, 0.7, 0.4])

        ctrl_p_grp = '{}_grp'.format(ctrl)
        if not cmds.objExists(ctrl_p_grp):
            cmds.createNode('transform', n=ctrl_p_grp, ss=True)

        cmds.parent(ctrl, ctrl_p_grp)
        cmds.xform(ctrl, t=[0,0,0], ro=[0,0,0], a=True)
        cmds.setAttr(ctrl + '.jo', *[0,0,0])
        cmds.matchTransform(ctrl_p_grp, jnt)

        ctrls.append(ctrl)

        pa = cmds.listRelatives(jnt, p=True, type='joint') or None
        if pa:
            cmds.parent(ctrl_p_grp, pa[0] + '_ctrl')

        pac = cmds.pointConstraint(ctrl, jnt, w=True)
        orc = cmds.orientConstraint(ctrl, jnt, w=True)
        scc = cmds.scaleConstraint(ctrl, jnt, w=True)
        consts.append(pac[0])
        consts.append(orc[0])
        consts.append(scc[0])

    cmds.parent(ctrls[0]+'_grp', prop_p_grp)

    for ctrl in ctrls:
        removed_nss = ctrl.replace(prop_namespace + ':', '')
        splited = removed_nss.split('_')[0::]

        part_sets = prop_namespace + '_' + splited[0] + '_ctrl_sets'
        if not cmds.objExists(part_sets):
            cmds.sets(em=True, n=part_sets)

        cmds.sets(part_sets, add=prop_ctrl_sets)

        if '_L_' in ctrl or '_R_' in ctrl:
            part_side_sets = prop_namespace + '_' + splited[0] + '_' + splited[2] + '_ctrl_sets'
            if not cmds.objExists(part_side_sets):
                cmds.sets(em=True, n=part_side_sets)

            cmds.sets(part_side_sets, add=part_sets)

            cmds.sets(ctrl, add=part_side_sets)

        else:
            cmds.sets(ctrl, add=part_sets)

    # joint
    prop_jnt_sets = '{}_prop_temp_jnt_sets'.format(prop_namespace)
    if not cmds.objExists(prop_jnt_sets):
        cmds.sets(em=True, n=prop_jnt_sets)

    cmds.sets(prop_jnt_sets, add=prop_temp_sets)

    cmds.sets(prop_namespace + ':Root', add=prop_jnt_sets)

    for jnt in prop_root_joints:
        cmds.sets(jnt, add=prop_jnt_sets)

    # consts
    prop_const_sets = '{}_prop_temp_const_sets'.format(prop_namespace)
    if not cmds.objExists(prop_const_sets):
        cmds.sets(em=True, n=prop_const_sets)

    cmds.sets(prop_const_sets, add=prop_temp_sets)

    for const in consts:
        cmds.sets(const, add=prop_const_sets)


def prop_scale_connection(ctrl, ctrl_nss, prop_namespace):
    prop_p_grp = '{}_prop_temp_grp'.format(prop_namespace)
    ctrl_grps = cmds.listRelatives(prop_p_grp, c=True, type='transform')
    # handattach = ctrl.replace('_ctrl', '').replace(ctrl_nss, ctrl_nss + 'chr:')
    handattach = prop_namespace +':Root_ctrl'
    for grp in ctrl_grps:
        # cmds.connectAttr(handattach+'.s', grp+'.s', f=True)
        if handattach in grp:
            root_cnst = 'Root_ctrl_grp_parentConstraint1'
            if cmds.objExists(root_cnst):
                cmds.delete(root_cnst)
                cmds.parentConstraint(ctrl, grp, w=True)

    cmds.connectAttr(handattach +'.s', prop_namespace + ':Root.s', f=True)

    cmds.setAttr(handattach+'.tx', l=True, k=False, cb=False)
    cmds.setAttr(handattach+'.ty', l=True, k=False, cb=False)
    cmds.setAttr(handattach+'.tz', l=True, k=False, cb=False)
    cmds.setAttr(handattach+'.rx', l=True, k=False, cb=False)
    cmds.setAttr(handattach+'.ry', l=True, k=False, cb=False)
    cmds.setAttr(handattach+'.rz', l=True, k=False, cb=False)
    cmds.setAttr(handattach+'.v', l=True, k=False, cb=False)
    cmds.setAttr(handattach+'.radius', l=True, k=False, cb=False)

def delete_sim_temps(sim_namespace=None):
    # sim temp ctrls
    delete_sim_temp_list = [
        '{}_sim_temp_grp'.format(sim_namespace),
        '{}_sim_temp_sets'.format(sim_namespace),
        '{}_sim_temp_ctrl_sets'.format(sim_namespace),
        '{}_sim_temp_jnt_sets'.format(sim_namespace),
        '{}_sim_temp_const_sets'.format(sim_namespace)
    ]
    for dsts in delete_sim_temp_list:
        if cmds.objExists(dsts):
            if 'sim_temp_const_sets' in dsts:
                cmds.select(dsts, ne=True, r=True)
                objs = cmds.pickWalk(d='down')
                cmds.delete(objs)

            cmds.delete(dsts)


def anim_temp_save(ref_name=None, parts_type=None, operation='export'):
    # print('ref_name, parts_type, operation', ref_name, parts_type, operation)
    documents_path = 'C:/Users/'+os.environ['USER']+'/Documents/maya/avatarReferenceTool'

    if not os.path.isdir(documents_path):
        os.makedirs(documents_path)

    path = documents_path + '/' + parts_type + '.atom'

    sim_ctrl_sets = '{}_sim_temp_ctrl_sets'.format(ref_name)
    if cmds.objExists(sim_ctrl_sets):
        cmds.select(sim_ctrl_sets, ne=True, r=True)
        objs = cmds.pickWalk(d='down')
    else:
        return

    if operation == 'export':
        if os.path.isfile(path):
            cmds.file(
                path,
                f=True,
                options='',
                typ='atomExport',
                pr=True,
                es=True
            )
            print('export', path)

    elif operation == 'import':
        if os.path.isfile(path):
            cmds.file(
                path,
                i=True,
                typ='atomImport',
                ignoreVersion=True,
                mergeNamespacesOnClash=False,
                pr=True,
                importTimeRange='override'
            )

def fullbake(ctrls=None):
    # フルベイク
    try:
        cmds.refresh(su=1)

        # get
        start, end, animstart, animend, curtime, autoKeyState = get_animation_status()

        attrs = list(set(cmds.listAttr(ctrls, k=True)))
        cmds.bakeResults(
            ctrls,
            simulation=True,
            t=(start, end),
            sampleBy=1,
            oversamplingRate=1,
            disableImplicitControl=True,
            preserveOutsideKeys=True,
            sparseAnimCurveBake=False,
            removeBakedAttributeFromLayer=False,
            removeBakedAnimFromLayer=False,
            bakeOnOverrideLayer=False,
            minimizeRotation=True,
            at=attrs
        )

        # set
        set_animation_status(start, end, animstart, animend, curtime, autoKeyState)

        cmds.refresh(su=0)

    except:
        cmds.refresh(su=0)
        print(traceback.format_exc())


@bake_with_func
def space_match_bake(obj, space, match_space):
    switch_prop_space(obj, space)
    cmds.setKeyframe('{}'.format(obj))
    switch_prop_space(obj, match_space)
    cmds.setKeyframe('{}'.format(obj))

def prop_rotate_from(obj, rot):
    mat_ats = OrderedDict({
        'default':[0,0,0],
        '(90, 90, 0)':[90, 90, 0],
        '(90, 0, 90)':[90, 0, 90],
        '(0, 90, 90)':[0, 90, 90],
        '(-90, 90, 0)':[-90, 90, 0],
        '(-90, 0, 90)':[-90, 0, 90],
        '(0, -90, 90)':[0, -90, 90],
        '(90, -90, 0)':[90, -90, 0],
        '(90, 0, -90)':[90, 0, -90],
        '(0, 90, -90)':[0, 90, -90],
        '(-90, -90, 0)':[-90, -90, 0],
        '(-90, 0, -90)':[-90, 0, -90],
        '(0, -90, -90)':[0, -90, -90],
    })

    cmds.setAttr(obj + '.r', *mat_ats[rot])


# cmds.file(new=True, f=True)
# base_fbx = "C:/Users/CF0990/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/20230315/01/an_p2_cmn_stand_idle_02_LOOP.fbx"
# extract_fbx = "C:/Users/CF0990/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/20230315/01/an_p2_cmn_add_stand_talk_listener_01.fbx"
# save_fbx = "C:/Users/CF0990/Documents/maya/scripts/tkgTools/tkgRig/data/projects/wizard2/data/20230315/01/combine_test.fbx"
# combine_fbx_(base_fbx, extract_fbx, save_fbx)


#
# cmds.file(new=True, f=True)

# nss = 'base'
# fbx_path=base_fbx

# imported_objects = import_fbx(fbx_path=fbx_path, nss=nss, new_scene=None)

# temp_ma_ext = os.path.basename(fbx_path).replace('.fbx', '.ma')

# temp_folder = os.environ['TEMP'].replace('\\', '/') + '/FBX_Mixer/'
# if not os.path.isdir(temp_folder):
#     os.makedirs(temp_folder)

# ma_path = temp_folder + temp_ma_ext

# cmds.file(rn=ma_path)
# cmds.file(f=True, save=True, options='v=0', type='mayaAscii')



# maya_path_nss, maya_paths = ['base', 'extract', 'combine'], ['C:/Users/CF0990/AppData/Local/Temp/FBX_Mixer/an_p2_cmn_stand_idle_02_LOOP.ma', 'C:/Users/CF0990/AppData/Local/Temp/FBX_Mixer/an_p2_cmn_add_stand_talk_listener_01.ma', 'C:/Users/CF0990/AppData/Local/Temp/FBX_Mixer/an_p2_cmn_stand_idle_02_LOOP.ma']
