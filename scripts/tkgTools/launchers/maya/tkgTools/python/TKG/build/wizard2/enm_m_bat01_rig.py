from collections import OrderedDict
import math
import re

from maya import cmds, mel

def get_distance(obj_A=None, obj_B=None, gobj_A=None, gobj_B=None):
    if not gobj_A:
        gobj_A = cmds.xform(obj_A, q=True, t=True, ws=True)

    if not gobj_B:
        gobj_B = cmds.xform(obj_B, q=True, t=True, ws=True)

    x = math.pow(gobj_A[0] - gobj_B[0], 2)
    y = math.pow(gobj_A[1] - gobj_B[1], 2)
    z = math.pow(gobj_A[2] - gobj_B[2], 2)

    return math.sqrt(x + y + z)


def get_length(nodes=None):
    length_ord_dict = OrderedDict()
    if len(nodes) <= 1:
        return

    length = 0.0
    for i, node in enumerate(nodes):
        if i == 0:
            pass
        else:
            distance = get_distance(nodes[i-1], node)
            length += distance

            length_ord_dict['{}-{}'.format(nodes[i-1], node)] = distance

    return length_ord_dict

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
         u'fly': {'degree': 1,
          'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
          'periodic': False,
          'points': [[0.7068334874903152, 0.07626081496804736, 1.569485624775691e-16],
                     [0.5526954697265705, 0.16117702901697772, 1.2272304721929094e-16],
                     [0.8414839532593945, 0.3246996775218697, 1.8684697195223574e-16],
                     [0.6098247754984263, 0.3633346992441682, 1.3540830134904395e-16],
                     [1.0000000000000002, 0.5934488571761581, 2.220446049250313e-16],
                     [0.41289363283583835, 0.5534159452119349, 9.168080357909464e-17],
                     [3.5392392753749443e-17, 0.15939316681753624, 0.0],
                     [-0.41289363283583813, 0.5534159452119352, -9.168080357909464e-17],
                     [-0.9999999999999999, 0.5934488571761586, -2.220446049250313e-16],
                     [-0.6098247754984261, 0.36333469924416845, -1.3540830134904395e-16],
                     [-0.8414839532593943, 0.32469967752187, -1.8684697195223574e-16],
                     [-0.5526954697265705, 0.16117702901697795, -1.2272304721929094e-16],
                     [-0.7068334874903152, 0.07626081496804767, -1.569485624775691e-16],
                     [-0.4876664799872207, -0.019129994149875425, -1.082837108839431e-16],
                     [-0.5877769336857814, -0.14599156004075325, -1.3051269702430566e-16],
                     [-0.366798621334302, -0.18462658182678118, -8.144565496122124e-17],
                     [-0.4696444934471726, -0.2942828971663854, -1.0428202600269388e-16],
                     [-0.14110099766075418, -0.4318982197647379, -3.133071528010991e-17],
                     [-1.3177211703489134e-16, -0.593448857176158, 0.0],
                     [0.141100997660754, -0.431898219764738, 3.133071528010991e-17],
                     [0.46964449344717246, -0.2942828971663856, 1.0428202600269388e-16],
                     [0.3667986213343019, -0.18462658182678135, 8.144565496122124e-17],
                     [0.5877769336857814, -0.14599156004075353, 1.3051269702430566e-16],
                     [0.4876664799872207, -0.01912999414987564, 1.082837108839431e-16],
                     [0.7068334874903152, 0.07626081496804736, 1.569485624775691e-16]]},
         u'jack': {'degree': 1,
                   'knot': [0,
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12,
                            13,
                            14,
                            15,
                            16,
                            17,
                            18,
                            19,
                            20,
                            21,
                            22,
                            23,
                            24,
                            25,
                            26,
                            27,
                            28,
                            29,
                            30,
                            31,
                            32,
                            33,
                            34,
                            35,
                            36,
                            37,
                            38,
                            39,
                            40,
                            41,
                            42,
                            43,
                            44,
                            45,
                            46,
                            47,
                            48,
                            49,
                            50,
                            51,
                            52,
                            53,
                            54,
                            55,
                            56,
                            57,
                            58,
                            59,
                            60,
                            61,
                            62,
                            63,
                            64,
                            65,
                            66,
                            67,
                            68,
                            69,
                            70,
                            71,
                            72,
                            73,
                            74,
                            75,
                            76,
                            77,
                            78,
                            79,
                            80,
                            81,
                            82,
                            83],
                   'periodic': False,
                   'points': [[0.0, 0.0, 0.0],
                              [0.75, 0.0, 0.0],
                              [1.0, 0.25, 0.0],
                              [1.25, 0.0, 0.0],
                              [1.0, -0.25, 0.0],
                              [0.75, 0.0, 0.0],
                              [1.0, 0.0, 0.25],
                              [1.25, 0.0, 0.0],
                              [1.0, 0.0, -0.25],
                              [1.0, 0.25, 0.0],
                              [1.0, 0.0, 0.25],
                              [1.0, -0.25, 0.0],
                              [1.0, 0.0, -0.25],
                              [0.75, 0.0, 0.0],
                              [0.0, 0.0, 0.0],
                              [-0.75, 0.0, 0.0],
                              [-1.0, 0.25, 0.0],
                              [-1.25, 0.0, 0.0],
                              [-1.0, -0.25, 0.0],
                              [-0.75, 0.0, 0.0],
                              [-1.0, 0.0, 0.25],
                              [-1.25, 0.0, 0.0],
                              [-1.0, 0.0, -0.25],
                              [-1.0, 0.25, 0.0],
                              [-1.0, 0.0, 0.25],
                              [-1.0, -0.25, 0.0],
                              [-1.0, 0.0, -0.25],
                              [-0.75, 0.0, 0.0],
                              [0.0, 0.0, 0.0],
                              [0.0, 0.75, 0.0],
                              [0.0, 1.0, -0.25],
                              [0.0, 1.25, 0.0],
                              [0.0, 1.0, 0.25],
                              [0.0, 0.75, 0.0],
                              [-0.25, 1.0, 0.0],
                              [0.0, 1.25, 0.0],
                              [0.25, 1.0, 0.0],
                              [0.0, 1.0, 0.25],
                              [-0.25, 1.0, 0.0],
                              [0.0, 1.0, -0.25],
                              [0.25, 1.0, 0.0],
                              [0.0, 0.75, 0.0],
                              [0.0, 0.0, 0.0],
                              [0.0, -0.75, 0.0],
                              [0.0, -1.0, -0.25],
                              [0.0, -1.25, 0.0],
                              [0.0, -1.0, 0.25],
                              [0.0, -0.75, 0.0],
                              [-0.25, -1.0, 0.0],
                              [0.0, -1.25, 0.0],
                              [0.25, -1.0, 0.0],
                              [0.0, -1.0, -0.25],
                              [-0.25, -1.0, 0.0],
                              [0.0, -1.0, 0.25],
                              [0.25, -1.0, 0.0],
                              [0.0, -0.75, 0.0],
                              [0.0, 0.0, 0.0],
                              [0.0, 0.0, -0.75],
                              [0.0, 0.25, -1.0],
                              [0.0, 0.0, -1.25],
                              [0.0, -0.25, -1.0],
                              [0.0, 0.0, -0.75],
                              [-0.25, 0.0, -1.0],
                              [0.0, 0.0, -1.25],
                              [0.25, 0.0, -1.0],
                              [0.0, 0.25, -1.0],
                              [-0.25, 0.0, -1.0],
                              [0.0, -0.25, -1.0],
                              [0.25, 0.0, -1.0],
                              [0.0, 0.0, -0.75],
                              [0.0, 0.0, 0.0],
                              [0.0, 0.0, 0.75],
                              [0.0, 0.25, 1.0],
                              [0.0, 0.0, 1.25],
                              [0.0, -0.25, 1.0],
                              [0.0, 0.0, 0.75],
                              [-0.25, 0.0, 1.0],
                              [0.0, 0.0, 1.25],
                              [0.25, 0.0, 1.0],
                              [0.0, 0.25, 1.0],
                              [-0.25, 0.0, 1.0],
                              [0.0, -0.25, 1.0],
                              [0.25, 0.0, 1.0],
                              [0.0, 0.0, 0.75]]},
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

    ctrl_jnt = obj.split(':')[-1]


    if (not prefix
        and not suffix
        and not replace
        and not mirrors):
        ctrl = ctrl_jnt+'_ctrl'
    else:
        ctrl = temp_rename(ctrl_jnt, prefix, suffix, replace, mirrors)

    cmds.rename(joint, ctrl)
    cmds.rename(shape, ctrl+'Shape')

    return ctrl


def create_temp_ctrls(joints=None, sim_parent=None):
    ctrls = list()
    ctrl_p = None
    consts = list()
    joints = order_joints(joints)
    hier = {}
    right_color = [0.5, 0.5, 1]
    left_color = [1, 0.214, 0.214]
    for jnt in joints:
        wst = cmds.xform(jnt, q=True, t=True, ws=True)
        if wst[0] < 0:
            rgb_color = right_color
        elif wst[0] > 0:
            rgb_color = left_color
        else:
            rgb_color = [1, 1, 0.2]

        if jnt == 'chr:Spine1':
            ctrl = create_controller(obj=jnt, ctrl_type='jack', edge_axis=None,
                                  pos=None, rot=None, scl=[5, 5, 5], line_width=2,
                                  prefix=None, suffix='_ctrl', replace=None, mirrors=None, rgb=[1, 1, 0.2])

        else:
            ctrl = create_controller(obj=jnt, ctrl_type='cube', edge_axis=None,
                                  pos=None, rot=None, scl=[5, 5, 5], line_width=2,
                                  prefix=None, suffix='_ctrl', replace=None, mirrors=None, rgb=rgb_color)


        ctrls.append(ctrl)

        ch = cmds.listRelatives(jnt, c=True) or None
        pa = cmds.listRelatives(jnt, p=True) or None

        if pa:
            p_jnt = pa[0].split(':')[-1]
            p_ctrl = p_jnt + '_ctrl'
            if cmds.objExists(p_ctrl):
                hier[ctrl] = p_ctrl

        ori = cmds.orientConstraint(ctrl, jnt, w=True)
        cmds.setAttr(ori[0]+'.interpType', 2)
        consts.append(ori[0])

    for h_ctrl, p_ctrl in hier.items():
        cmds.parent(h_ctrl, p_ctrl)


    ctrl_p_grp = '{}_grp'.format(ctrls[0])
    if not cmds.objExists(ctrl_p_grp):
        cmds.createNode('transform', n=ctrl_p_grp, ss=True)

    if sim_parent:
        cmds.matchTransform(ctrl_p_grp, sim_parent)
        cmds.parentConstraint(sim_parent, ctrl_p_grp)

    cmds.parent(ctrls[0], ctrl_p_grp)

    for ctrl in ctrls:
        cmds.setAttr(ctrl+'.tx', k=False, cb=False, l=True)
        cmds.setAttr(ctrl+'.ty', k=False, cb=False, l=True)
        cmds.setAttr(ctrl+'.tz', k=False, cb=False, l=True)
        cmds.setAttr(ctrl+'.sx', k=False, cb=False, l=True)
        cmds.setAttr(ctrl+'.sy', k=False, cb=False, l=True)
        cmds.setAttr(ctrl+'.sz', k=False, cb=False, l=True)
        cmds.setAttr(ctrl+'.radius', k=False, cb=False, l=True)
        cmds.setAttr(ctrl+'.v', k=False, cb=False, l=True)

    return ctrl_p_grp, ctrls, consts


def rename_duplicate_objects(all_objects):
    objects_dict = {}

    for obj in all_objects:
        short_name = obj.split('|')[-1]
        if short_name in objects_dict:
            new_name = cmds.rename(obj, short_name + '_RN_##')
        else:
            objects_dict[short_name] = obj

def get_axis_cvs(objects):
    axis_cvs = {}
    for obj in objects:
        x_cvs = []
        y_cvs = []
        z_cvs = []

        neg_x_cvs = []
        neg_y_cvs = []
        neg_z_cvs = []

        verts = cmds.ls(obj+'.cv[*]', fl=True)
        for v in verts:
            lt = cmds.xform(v, q=True, t=True, os=True)
            if lt[0] > 0:
                x_cvs.append(v)
            if lt[1] > 0:
                y_cvs.append(v)
            if lt[2] > 0:
                z_cvs.append(v)

            if lt[0] < 0:
                neg_x_cvs.append(v)
            if lt[1] < 0:
                neg_y_cvs.append(v)
            if lt[2] < 0:
                neg_z_cvs.append(v)

        axis_cvs[obj] = {}
        axis_cvs[obj]['x'] = x_cvs
        axis_cvs[obj]['y'] = y_cvs
        axis_cvs[obj]['z'] = z_cvs
        axis_cvs[obj]['-x'] = neg_x_cvs
        axis_cvs[obj]['-y'] = neg_y_cvs
        axis_cvs[obj]['-z'] = neg_z_cvs

    return axis_cvs

chara_root_joint = 'Root'
namespace = 'chr'

ref_path = 'c:/cygames/wiz2/team/3dcg/chr/enm/minion/bat01/scenes/enm_m_bat01.ma'
# ref_path = 'C:/cygames/wiz2/team/3dcg/rig/work/share/enm/bat01/scenes/enm_m_bat01.ma'
cmds.file(ref_path, ignoreVersion=1, namespace=namespace, r=1, gl=1, mergeNamespacesOnClash=1, options="v=0;")

if not namespace.endswith(':'):
    namespace = namespace + ':'

joints = cmds.ls(namespace + chara_root_joint, dag=True, type='joint')

jaw_joints = cmds.ls('*:Jaw*', type='joint')
lip_joints = cmds.ls('*:*Lip*', type='joint')

joints = [j for j in joints if not j in jaw_joints]
joints = [j for j in joints if not j in lip_joints]

# spine_jnt = 'Spine1'
# cmds.joint(n=spine_jnt)
# cmds.xform(spine_jnt, t=[0, 31.205, 1.519], ws=True, a=True)
# joints = cmds.ls(os=True, dag=True, type='joint')
# joints = cmds.ls('Root', dag=True, type='joint')
rename_duplicate_objects(joints)

# joints = cmds.ls(os=True, dag=True, type='joint')
ctrl_p_grp, ctrls, consts = create_temp_ctrls(joints=joints)

spine_ctrl = 'Spine1_ctrl'

spine_ctrl_p_grp = '{}_grp'.format(spine_ctrl)
if not cmds.objExists(spine_ctrl_p_grp):
    cmds.createNode('transform', n=spine_ctrl_p_grp, ss=True)

cmds.matchTransform(spine_ctrl_p_grp, spine_ctrl)
cmds.setAttr(spine_ctrl+'.tx', l=False, k=True)
cmds.setAttr(spine_ctrl+'.ty', l=False, k=True)
cmds.setAttr(spine_ctrl+'.tz', l=False, k=True)

cmds.parent(spine_ctrl, spine_ctrl_p_grp)
cmds.parent(spine_ctrl_p_grp, 'Root_ctrl')

axis_cvs = get_axis_cvs(ctrls)


left_ctrls = []
right_ctrls = []
for ctrl in ctrls:
    wt = cmds.xform(ctrl, q=True, t=True, ws=True)
    if wt[0] > 0:
        left_ctrls.append(ctrl)
    if wt[0] < 0:
        right_ctrls.append(ctrl)

def shape_cv_move(left_ctrls=None, left_axis='x', right_ctrls=None, right_axis='-x', axis_cvs=None):

    left_ctrl_cv_nums = [0, 1, 4, 5, 8, 9, 10, 13]
    right_ctrl_cv_nums = [2, 3, 6, 7, 11, 12, 14, 15]

    axis_dict = {
        'x':{
            'scl':[0.8, 0.2, 0.2],
            'value':[1, 0, 0]
        },
        'y':{
            'scl':[0.2, 0.8, 0.2],
            'value':[0, 1, 0]
        },
        'z':{
            'scl':[0.2, 0.2, 0.8],
            'value':[0, 0, 1]
        },
        '-x':{
            'scl':[0.8, 0.2, 0.2],
            'value':[-1, 0, 0]
        },
        '-y':{
            'scl':[0.2, 0.8, 0.2],
            'value':[0, -1, 0]
        },
        '-z':{
            'scl':[0.2, 0.2, 0.8],
            'value':[0, 0, -1]
        },
    }

    left_scl = axis_dict[left_axis]['scl']
    right_scl = axis_dict[right_axis]['scl']

    left_value = axis_dict[left_axis]['value']
    right_value = axis_dict[right_axis]['value']

    for i, (lc, rc) in enumerate(zip(left_ctrls, right_ctrls)):
        if i == 0:
            continue

        left_dis = get_distance(left_ctrls[i-1], lc)
        right_dis = get_distance(right_ctrls[i-1], rc)

        left_fix_value = [left_dis*val for val in left_value]
        right_fix_value = [right_dis*val for val in right_value]

        if lc in axis_cvs.keys():
            left_sel_cvs = axis_cvs[lc][left_axis]

        if rc in axis_cvs.keys():
            right_sel_cvs = axis_cvs[rc][right_axis]

        # left_sel_cvs = ['{}.cv[{}]'.format(left_ctrls[i-1], j) for j in left_ctrl_cv_nums]
        # right_sel_cvs = ['{}.cv[{}]'.format(right_ctrls[i-1], j) for j in right_ctrl_cv_nums]

        cmds.select(left_sel_cvs, r=True)
        cmds.move(r=True, os=True, wd=True, *left_fix_value)
        cmds.scale(r=True, *left_scl)

        cmds.select(right_sel_cvs, r=True)
        cmds.move(r=True, os=True, wd=True, *right_fix_value)
        cmds.scale(r=True, *right_scl)


shape_cv_move(left_ctrls=left_ctrls, left_axis='x', right_ctrls=right_ctrls, right_axis='-x', axis_cvs=axis_cvs)

# Root
cmds.setAttr('Root_ctrl.tx', l=False, k=True)
cmds.setAttr('Root_ctrl.ty', l=False, k=True)
cmds.setAttr('Root_ctrl.tz', l=False, k=True)

cmds.pointConstraint('Root_ctrl', namespace + 'Root', w=True)

# Spine1
cmds.pointConstraint('Spine1_ctrl', namespace + 'Spine1', w=True)

# Jaw
jaw = namespace + 'Jaw'
ctrl_p_grp, ctrls, consts = create_temp_ctrls(joints=[jaw])
set_rgb_color(ctrl=ctrls[0], color=[0.2, 0.1, 0.9])

mel.eval('''
select -r Jaw_ctrl.cv[0] Jaw_ctrl.cv[7:9] Jaw_ctrl.cv[12:15] ;
move -r -os -wd 0 0 36.217899 ;

select -r Jaw_ctrl.cv[1:6] Jaw_ctrl.cv[10:11] ;
scale -r -p 0cm 45.156493cm -7.141019cm 15 1 1 ;

select -r Jaw_ctrl.cv[9] Jaw_ctrl.cv[12:14] ;
move -r -os -wd 0 -27.172281 0 ;

transformLimits -rx -30 -30 -erx 1 0 Jaw_ctrl;
''')

cmds.parent(ctrl_p_grp, 'Spine1_ctrl')

# Lip Driven
mel.eval('''
// setAttr
setAttr "Jaw_ctrl.rotateZ" 0;
setAttr "Jaw_ctrl.rotateX" 0;
setAttr "Jaw_ctrl.rotateY" 0;

// left
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_L.rotateX;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_L.rotateY;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_L.rotateZ;

setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_L.rotateX;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_L.rotateY;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_L.rotateZ;

// right
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_R.rotateX;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_R.rotateY;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_R.rotateZ;

setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_R.rotateX;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_R.rotateY;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_R.rotateZ;

// setAttr
setAttr "Jaw_ctrl.rotateZ" 0;
setAttr "Jaw_ctrl.rotateX" -30;
setAttr "Jaw_ctrl.rotateY" 0;

setAttr "chr:LowerLip_01_R.rotateX" -18.121;
setAttr "chr:LowerLip_01_L.rotateX" -18.121;
setAttr "chr:LowerLip_01_R.rotateY" 5.363;
setAttr "chr:LowerLip_01_L.rotateY" 5.363;
setAttr "chr:LowerLip_01_R.rotateZ" -6.258;
setAttr "chr:LowerLip_01_L.rotateZ" -6.258;

setAttr "chr:LowerLip_02_R.rotateX" 39.16;
setAttr "chr:LowerLip_02_L.rotateX" 39.16;
setAttr "chr:LowerLip_02_R.rotateY" 19.96;
setAttr "chr:LowerLip_02_L.rotateY" 19.96;
setAttr "chr:LowerLip_02_R.rotateZ" 23.323;
setAttr "chr:LowerLip_02_L.rotateZ" 23.323;

// set driven
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_L.rotateX;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_L.rotateY;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_L.rotateZ;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_L.rotateX;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_L.rotateY;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_L.rotateZ;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_R.rotateX;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_R.rotateY;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_01_R.rotateZ;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_R.rotateX;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_R.rotateY;
setDrivenKeyframe -currentDriver Jaw_ctrl.rotateX chr:LowerLip_02_R.rotateZ;

// reset
setAttr "Jaw_ctrl.rotateZ" 0;
setAttr "Jaw_ctrl.rotateX" 0;
setAttr "Jaw_ctrl.rotateY" 0;

''')

#######################################################
# Create Sets
#######################################################

L_ctrls = cmds.ls('*_L_ctrl')
R_ctrls = cmds.ls('*_R_ctrl')

create_sets = {
    'all_sets':None,
    'export_sets':{
        'add':['all_sets']
    },
    'ctrl_sets':{
        'add':['all_sets']
    },

    'fk_ctrl_sets':{
        'add':['ctrl_sets'],
        'items':[
            'Root_ctrl'
        ]
    },

    'wing_ctrl_sets':{
        'add':['fk_ctrl_sets'],
    },

    'left_wing_ctrl_sets':{
        'add':['wing_ctrl_sets'],
        'items':L_ctrls
    },

    'right_wing_ctrl_sets':{
        'add':['wing_ctrl_sets'],
        'items':R_ctrls
    },
}

empty_sets = [sets for sets in create_sets.keys()]
[cmds.sets(em=True, n=sets) for sets in empty_sets if not cmds.objExists(sets)]

for sets in empty_sets:
    sets_settings = create_sets[sets]
    if sets_settings:
        if 'add' in sets_settings.keys():
            [cmds.sets(sets, add=add_item) for add_item in sets_settings['add']]

        if 'items' in sets_settings.keys():
            [cmds.sets(item, add=sets) for item in sets_settings['items']]

[joints.append(j) for j in jaw_joints]
[joints.append(j) for j in lip_joints]

[cmds.sets(obj, add='export_sets') for obj in joints]

cmds.createNode('transform', n='rig')
cmds.addAttr('rig', ln="geoVisibility", dv=1, at='double', min=0, max=1, k=1)
cmds.addAttr('rig', ln="geoOverrideEnabled", dv=1, at='double', min=0, max=1, k=1)
cmds.addAttr('rig', ln="geoChangeDisplayType", en="Normal:Template:Reference:", at="enum", k=1)
cmds.addAttr('rig', ln="jntVisibility", dv=1, at='double', min=0, max=1, k=1)
cmds.addAttr('rig', ln="jntOverrideEnabled", dv=1, at='double', min=0, max=1, k=1)
cmds.addAttr('rig', ln="jntChangeDisplayType", en="Normal:Template:Reference:", at="enum", k=1)

cmds.parent('Root_ctrl_grp', 'rig')

ref_top_nodes = cmds.ls(rn=True, assemblies=True)
# ref_top_nodes = ['obj']

if ref_top_nodes:
    geo_grp = 'geo_grp'
    cmds.createNode('transform', n=geo_grp)
    [cmds.parent(ref_top_node, geo_grp) for ref_top_node in ref_top_nodes]
    cmds.parent(geo_grp, 'rig')

    cmds.connectAttr('rig.geoVisibility', '{}.v'.format(geo_grp), f=1)
    cmds.connectAttr('rig.geoOverrideEnabled', '{}.overrideEnabled'.format(geo_grp), f=1)
    cmds.connectAttr('rig.geoChangeDisplayType', '{}.overrideDisplayType'.format(geo_grp), f=1)

    cmds.connectAttr('rig.jntVisibility', '{}.v'.format(namespace + chara_root_joint), f=1)
    cmds.connectAttr('rig.jntOverrideEnabled', '{}.overrideEnabled'.format(namespace + chara_root_joint), f=1)
    cmds.connectAttr('rig.jntChangeDisplayType', '{}.overrideDisplayType'.format(namespace + chara_root_joint), f=1)

    cmds.setAttr('rig.geoChangeDisplayType', 2)
    cmds.setAttr('rig.jntVisibility', 0)

##
mel.eval('''
select -r Root_ctrlShape.cv[0:15] ;
scale -r 9.131633 1 9.131633 ;

select -r Spine1_ctrlShape.cv[0:83] ;
scale -r -p 0cm 31.205cm 1.519cm 6.611546 6.611546 6.611546 ;

select -r Arm_01_L_ctrlShape.cv[0:1] Arm_01_L_ctrlShape.cv[4:5] Arm_01_L_ctrlShape.cv[8:10] Arm_01_L_ctrlShape.cv[13] ;
move -r -os -wd 21.405974 0 0 ;

select -r Arm_01_R_ctrlShape.cv[2:3] Arm_01_R_ctrlShape.cv[6:7] Arm_01_R_ctrlShape.cv[11:12] Arm_01_R_ctrlShape.cv[14:15] ;
move -r -os -wd -21.405974 0 0 ;

select -r FeatherA_02_L_ctrl.cv[0:1] FeatherA_02_L_ctrl.cv[4:5] FeatherA_02_L_ctrl.cv[8:10] FeatherA_02_L_ctrl.cv[13] ;
move -r -os -wd -21.611215 0 0 ;

select -r FeatherA_02_R_ctrl.cv[2:3] FeatherA_02_R_ctrl.cv[6:7] FeatherA_02_R_ctrl.cv[11:12] FeatherA_02_R_ctrl.cv[14:15] ;
move -r -os -wd 21.611215 0 0 ;

select -r FeatherC_01_L_ctrlShape.cv[0:1] FeatherC_01_L_ctrlShape.cv[4:5] FeatherC_01_L_ctrlShape.cv[8:10] FeatherC_01_L_ctrlShape.cv[13] ;
move -r -os -wd 21.711149 0 0 ;

select -r FeatherC_01_R_ctrlShape.cv[2:3] FeatherC_01_R_ctrlShape.cv[6:7] FeatherC_01_R_ctrlShape.cv[11:12] FeatherC_01_R_ctrlShape.cv[14:15] ;
move -r -os -wd -21.711149 0 0 ;

select -r FeatherD_01_L_ctrlShape.cv[0:1] FeatherD_01_L_ctrlShape.cv[4:5] FeatherD_01_L_ctrlShape.cv[8:10] FeatherD_01_L_ctrlShape.cv[13] ;
move -r -os -wd 36.039723 0 0 ;

select -r FeatherD_01_R_ctrlShape.cv[2:3] FeatherD_01_R_ctrlShape.cv[6:7] FeatherD_01_R_ctrlShape.cv[11:12] FeatherD_01_R_ctrlShape.cv[14:15] ;
move -r -os -wd -36.039723 0 0 ;

''')
"""
mel.eval('''
select -r Arm_02_L_ctrlShape.cv[0:1] Arm_02_L_ctrlShape.cv[4:5] Arm_02_L_ctrlShape.cv[8:10] Arm_02_L_ctrlShape.cv[13] ;
move -r -os -wd -7.062409 0 0 ;

select -r Arm_02_R_ctrlShape.cv[2:3] Arm_02_R_ctrlShape.cv[6:7] Arm_02_R_ctrlShape.cv[11:12] Arm_02_R_ctrlShape.cv[14:15] ;
move -r -os -wd 7.062409 0 0 ;
''')

mel.eval('''
select -r Arm_03_L_ctrlShape.cv[0:1] Arm_03_L_ctrlShape.cv[4:5] Arm_03_L_ctrlShape.cv[8:10] Arm_03_L_ctrlShape.cv[13] ;
move -r -os -wd -2.897612 0 0 ;

select -r Arm_03_R_ctrlShape.cv[2:3] Arm_03_R_ctrlShape.cv[6:7] Arm_03_R_ctrlShape.cv[11:12] Arm_03_R_ctrlShape.cv[14:15] ;
move -r -os -wd 2.897612 0 0 ;
''')

mel.eval('''
select -r Arm_04_L_ctrlShape.cv[0:1] Arm_04_L_ctrlShape.cv[4:5] Arm_04_L_ctrlShape.cv[8:10] Arm_04_L_ctrlShape.cv[13] ;
move -r -os -wd -13.650192 0 0 ;

select -r Arm_04_R_ctrlShape.cv[2:3] Arm_04_R_ctrlShape.cv[6:7] Arm_04_R_ctrlShape.cv[11:12] Arm_04_R_ctrlShape.cv[14:15] ;
move -r -os -wd 13.650192 0 0 ;

''')

mel.eval('''
select -r FeatherC_01_L_ctrlShape.cv[2:3] FeatherC_01_L_ctrlShape.cv[6:7] FeatherC_01_L_ctrlShape.cv[11:12] FeatherC_01_L_ctrlShape.cv[14:15] ;
move -r -os -wd 5.226668 0 0 ;

select -r FeatherC_01_R_ctrlShape.cv[0:1] FeatherC_01_R_ctrlShape.cv[4:5] FeatherC_01_R_ctrlShape.cv[8:10] FeatherC_01_R_ctrlShape.cv[13] ;
move -r -os -wd -5.226668 0 0 ;

''')

mel.eval('''
select -r FeatherE_01_L_ctrlShape.cv[0:1] FeatherE_01_L_ctrlShape.cv[4:5] FeatherE_01_L_ctrlShape.cv[8:10] FeatherE_01_L_ctrlShape.cv[13] ;
move -r -os -wd -21.041722 0 0 ;

select -r FeatherE_01_R_ctrlShape.cv[2:3] FeatherE_01_R_ctrlShape.cv[6:7] FeatherE_01_R_ctrlShape.cv[11:12] FeatherE_01_R_ctrlShape.cv[14:15] ;
move -r -os -wd 21.041722 0 0 ;

''')

mel.eval('''
select -r FeatherD_02_L_ctrlShape.cv[0:1] FeatherD_02_L_ctrlShape.cv[4:5] FeatherD_02_L_ctrlShape.cv[8:10] FeatherD_02_L_ctrlShape.cv[13] ;
move -r -os -wd -7.635235 0 0 ;

select -r FeatherD_02_R_ctrlShape.cv[2:3] FeatherD_02_R_ctrlShape.cv[6:7] FeatherD_02_R_ctrlShape.cv[11:12] FeatherD_02_R_ctrlShape.cv[14:15] ;
move -r -os -wd 7.635235 0 0 ;

''')
"""

cmds.select(cl=True)

# # spine fix
unlock_ctrls = [
    'Arm_01_L_ctrl',
    'Arm_01_R_ctrl'
]
# for ctrl in unlock_ctrls:
#     cmds.setAttr(ctrl+'.tx', l=False, k=True)
#     cmds.setAttr(ctrl+'.ty', l=False, k=True)
#     cmds.setAttr(ctrl+'.tz', l=False, k=True)

#     cmds.parent(ctrl, spine_ctrl)

# cmds.setAttr(spine_ctrl+'.radius', l=True, k=False, cb=False)
# cmds.setAttr(spine_ctrl+'.v', l=True, k=False, cb=False)
# cmds.setAttr(spine_ctrl+'.sx', l=True, k=False, cb=False)
# cmds.setAttr(spine_ctrl+'.sy', l=True, k=False, cb=False)
# cmds.setAttr(spine_ctrl+'.sz', l=True, k=False, cb=False)

for ctrl in unlock_ctrls:
    # cmds.setAttr(ctrl+'.tx', l=True, k=False)
    # cmds.setAttr(ctrl+'.ty', l=True, k=False)
    # cmds.setAttr(ctrl+'.tz', l=True, k=False)

    # cmds.setAttr(ctrl+'.sx', l=True, k=False)
    # cmds.setAttr(ctrl+'.sy', l=True, k=False)
    # cmds.setAttr(ctrl+'.sz', l=True, k=False)

    cmds.pointConstraint(ctrl, namespace + ctrl.replace('_ctrl', ''))

cmds.sets(spine_ctrl, add='fk_ctrl_sets')

cmds.sets('Jaw_ctrl', add='fk_ctrl_sets')

# cmds.delete(spine_jnt)

# all fix
def all_locks(nodes):
    for gr in nodes:
        cmds.setAttr(gr+'.tx', l=True, k=False, cb=False)
        cmds.setAttr(gr+'.ty', l=True, k=False, cb=False)
        cmds.setAttr(gr+'.tz', l=True, k=False, cb=False)

        cmds.setAttr(gr+'.rx', l=True, k=False, cb=False)
        cmds.setAttr(gr+'.ry', l=True, k=False, cb=False)
        cmds.setAttr(gr+'.rz', l=True, k=False, cb=False)

        cmds.setAttr(gr+'.sx', l=True, k=False, cb=False)
        cmds.setAttr(gr+'.sy', l=True, k=False, cb=False)
        cmds.setAttr(gr+'.sz', l=True, k=False, cb=False)

        cmds.setAttr(gr+'.v', l=True, k=False, cb=False)

grps = cmds.ls('*_grp', type='transform')
all_locks(grps)

all_locks(['rig'])

ctrls = cmds.ls('*_ctrl', tr=True)
for ctrl in ctrls:
    cmds.setAttr(ctrl + '.rotateOrder', 0)
    cmds.setAttr(ctrl + '.rotateOrder', l=True)


#####################################
# Add Old Joints
"""
ctrl_match_dict = {}

L_ctrls = cmds.ls('*_L_ctrl')
ref_L_ctrls = cmds.ls('*:*_L_ctrl')

for ctrl in L_ctrls:
    ctrl_wt = cmds.xform(ctrl, q=True, t=True, ws=True)
    ro_ctrl_wt = [round(v, 3) for v in ctrl_wt]
    for ref_ctrl in ref_L_ctrls:
        ref_ctrl_wt = cmds.xform(ref_ctrl, q=True, t=True, ws=True)
        ro_ref_ctrl_wt = [round(v, 3) for v in ref_ctrl_wt]

        if ro_ctrl_wt == ro_ref_ctrl_wt:
            ctrl_match_dict[ctrl] = ref_ctrl.replace('aaaa:', '').replace('_ctrl', '')

"""


# Root & Spine1_ctrl scale
cmds.setAttr('Root_ctrl' + '.sx', l=False, k=True, cb=False)
cmds.setAttr('Root_ctrl' + '.sy', l=False, k=True, cb=False)
cmds.setAttr('Root_ctrl' + '.sz', l=False, k=True, cb=False)
cmds.scaleConstraint('Root_ctrl', namespace+'Root', w=True)

cmds.setAttr(spine_ctrl + '.sx', l=False, k=True, cb=False)
cmds.setAttr(spine_ctrl + '.sy', l=False, k=True, cb=False)
cmds.setAttr(spine_ctrl + '.sz', l=False, k=True, cb=False)
cmds.scaleConstraint(spine_ctrl, namespace+'Spine1', w=True)

cmds.select('ctrl_sets', ne=True)
ctrls = cmds.pickWalk(d='down');cmds.ls(os=True)
for ctrl in ctrls:
    cmds.setAttr(ctrl + '.ssc', 0)
