# -*- coding: utf-8 -*-
from maya import cmds, mel
import maya.api.OpenMaya as om2

import codecs
from collections import OrderedDict
import json
import math
import os
import traceback

plugins = [
    'fbxmaya' # ここに追加
]
plugin_results = []
for plugin in plugins:
    plugin_result = cmds.loadPlugin(plugin) if not cmds.pluginInfo(plugin, q=True, l=True) else False
    plugin_results.append(plugin_result)

try:
    DIR_PATH = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
except:
    DIR_PATH = ''

DATA_PATH = DIR_PATH + '/data/'

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
    if operation == 'export':
        try:
            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)
        except:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

    elif operation == 'import':
        try:
            with codecs.open(file_name, 'r', encoding='utf-8') as f:
                return json.load(f, 'utf-8', object_pairs_hook=OrderedDict)
        except:
            with open(file_name, 'r', encoding="utf-8") as f:
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
        type='FBX',
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
