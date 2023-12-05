from collections import OrderedDict
import math
from functools import partial

from maya import cmds, mel

FUNCTIONS = {
    'aim_child':['z', 'y'],
    'freeze_rotate':[],
    'merge_joint_rotate':[],
    'round_transform_attrs':[],
    'check_ssc':[],
    'joint_labeling':[],
    'set_preferred_angle':[],
    'mirror_joint':[],
    'mirror_joint_color':[],
    'adjust_mirrors':[[180, 0, 0]],
}

FUNCTIONS_NAMES = {
    'aim_child':'Aim Child',
    'freeze_rotate':'Freeze Rotate',
    'merge_joint_rotate':'Merge Joint Rotate',
    'round_transform_attrs':'Round Attributes',
    'check_ssc':'Check segmentScaleCompensate',
    'joint_labeling':'Joint Labeling',
    'set_preferred_angle':'Set Preferred Angle',
    'mirror_joint':'Mirror Joint',
    'mirror_joint_color':'Mirror Joint Color',
    'adjust_mirrors':'Adjust Mirrors'
}


def aim_child(aim_axis='z', up_axis='y', dummy=None):
    print(aim_axis, up_axis)
    sel = cmds.ls(os=True)
    if not sel: return

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

    up_obj = cmds.spaceLocator()[0]
    cmds.matchTransform(up_obj, sel[1])
    cmds.xform(up_obj, t=[v*10 for v in axis_dict[up_axis]], r=True, os=True)

    pa = cmds.listRelatives(sel[0], p=True) or None
    if pa: cmds.parent(sel[0], w=True)

    cmds.delete(
        cmds.aimConstraint(
            sel[0],
            sel[1],
            offset=[0,0,0],
            w=True,
            aimVector=aimVector,
            upVector=upVector,
            worldUpType="object",
            worldUpObject=up_obj
        )
    )

    if pa: cmds.parent(sel[0], pa[0])

    cmds.delete(up_obj)

def freeze_rotate(dummy=None):
    sel = cmds.ls(os=True, type='joint')
    if not sel: return
    [cmds.makeIdentity(obj, n=False, s=False, r=True, t=False, apply=True, pn=True) for obj in sel]

def merge_joint_rotate(dummy=None):
    sel = cmds.ls(os=True, type='joint')
    if not sel:
        return

    for obj in sel:
        set_wr = cmds.xform(obj, q=1, ro=1, ws=1)
        cmds.setAttr('{}.jo'.format(obj), *(0, 0, 0))
        cmds.xform(obj, ro=set_wr, ws=1, a=1)

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

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

def round_transform_attrs(dummy=None):
    transforms = cmds.ls(os=1, type='transform')

    attrs = ['tx', 'ty', 'tz',
             'rx', 'ry', 'rz',
             'sx', 'sy', 'sz']

    joint_attrs = ['pax', 'pay', 'paz',
                   'jox', 'joy', 'joz',
                   'radius']

    for obj in transforms:
        round_attrs(obj, attrs)
        if cmds.objectType(obj) == 'joint':
            round_attrs(obj, joint_attrs)

def check_ssc(dummy=None):
    joints = [j for j in cmds.ls(os=True, type='joint', dag=True) if cmds.getAttr(j+'.ssc')]
    if joints:
        print('#'*50)
        print(u'segmentScaleCompensateがオンの骨が見つかりました。')
        print(joints)
        print('#'*50)

        result = cmds.confirmDialog(
            title='Confirm',
            message=u'segmentScaleCompensateがオンの骨が見つかりました。\n修正しますか？',
            button=['Yes','No'],
            defaultButton='Yes',
            cancelButton='No',
            dismissString='No'
        )
        if result == 'Yes':
            [cmds.setAttr(jnt+'.ssc', False) for jnt in joints]

    else:
        print('#'*50)
        print(u'segmentScaleCompensateがオンの骨は見つかりませんでした。')
        print('#'*50)

def joint_labeling(dummy=None):
    joints = cmds.ls(os=True, type='joint', dag=True)
    if not joints: return

    for obj in joints:
        if obj.endswith('_L') or obj.endswith('_R'):
            spl_obj = '_'.join(obj.split('_')[:-1])
            if obj.endswith('_L'):
                cmds.setAttr(obj+'.side', 1)
            if obj.endswith('_R'):
                cmds.setAttr(obj+'.side', 2)
        else:
            spl_obj = obj

        cmds.setAttr(obj+'.type', 18)
        cmds.setAttr(obj+'.otherType', spl_obj, type='string')

def set_preferred_angle(dummy=None):
    joints = cmds.ls(os=True, type='joint')
    if not joints: return
    [cmds.joint(jnt, e=True, spa=True, ch=True) for jnt in joints]

def adjust_mirrors(force_values=[180, 0, 0], dummy=None):
    # ジョイントを選択して実行
    sel = cmds.ls(os=True)

    if not sel: return

    for obj in sel:
        pa = cmds.listRelatives(obj, p=True) or None
        if pa: cmds.parent(obj, w=True)
        children = cmds.listRelatives(obj, c=True) or None
        if children: [cmds.parent(ch, w=True) for ch in children]

        cmds.xform(obj, ro=force_values, p=True, os=True, r=True)

        if pa: cmds.parent(obj, pa[0])
        if children: [cmds.parent(ch, obj) for ch in children]

def mirror_character(mirrors=['_L', '_R'], replace_src=None):
    mirrors_src_found = re.findall(mirrors[0], replace_src)

    renamed_char = replace_src.replace(mirrors[0], mirrors[1])

    if len(mirrors_src_found) > 1:
        splited_src = replace_src.split('_')
        splited_mir_src = [mir for mir in mirrors[0].split('_') if not mir == '']
        splited_mir_dst = [mir for mir in mirrors[1].split('_') if not mir == '']
        replace_src_idx = 0
        for spl_d in splited_src:
            for spl_ms in splited_mir_src:
                if spl_d == spl_ms:
                    replace_src_idx = splited_src.index(spl_d)
                    break

        combined = []
        for i, repl_d in enumerate(splited_src):
            if i == replace_src_idx:
                repl_d = ''.join(splited_mir_dst)

            combined.append(repl_d)

        renamed_char = '_'.join(combined)

    return renamed_char


def mirror_joint_color(dummy=None):
    sel = cmds.ls(os=True)
    colors_dict = OrderedDict()
    for obj in sel:
        colors_dict[obj] = OrderedDict({
            'useObjectColor':cmds.getAttr(obj+'.useObjectColor'),
            'wireColorRGB':cmds.getAttr(obj+'.wireColorRGB')[0],
            'useOutlinerColor':cmds.getAttr(obj+'.useOutlinerColor'),
            'outlinerColor':cmds.getAttr(obj+'.outlinerColor')[0],
        })

    for obj, setting in colors_dict.items():
        mir_obj = mirror_character(mirrors=['_L', '_R'], replace_src=obj)

        cmds.setAttr(mir_obj+'.useObjectColor', setting['useObjectColor'])
        cmds.setAttr(mir_obj+'.wireColorRGB', *setting['wireColorRGB'])

        cmds.setAttr(mir_obj+'.useOutlinerColor', setting['useOutlinerColor'])
        cmds.setAttr(mir_obj+'.outlinerColor', *setting['outlinerColor'])

def modify_joints():
    # ウィンドウの作成
    window_name = "ModifyJointAxis"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    cmds.window(window_name, title="Modify Joint Axis", sizeable=True)
    main_layout = cmds.columnLayout(adjustableColumn=True)

    # 指定された数のボタンを作成
    f_fields = []
    for func, args in FUNCTIONS.items():
        if args:
            if (func == 'aim_child'):
                    cmds.rowLayout(nc=4, parent=main_layout)

                    cmds.radioButtonGrp(
                        'aim_child_aim_radio_btn_grp',
                        label='Aim Axis',
                        labelArray3=["X", "Y", "Z"],
                        numberOfRadioButtons=3,
                        select=3,
                        onCommand=on_radio_button_changed,
                    )

                    cmds.checkBox('aim_child_aim_check', label='Negative', cc=on_radio_button_changed)

                    cmds.setParent('..')

                    cmds.rowLayout(nc=4, parent=main_layout)

                    cmds.radioButtonGrp(
                        'aim_child_up_radio_btn_grp',
                        label='Up Axis',
                        labelArray3=["X", "Y", "Z"],
                        numberOfRadioButtons=3,
                        select=2,
                        onCommand=on_radio_button_changed,
                    )

                    cmds.checkBox('aim_child_up_check', label='Negative', cc=on_radio_button_changed)

                    cmds.setParent('..')

            elif (func == 'adjust_mirrors'):
                cmds.rowLayout(nc=4, parent=main_layout)

                x_field = cmds.floatField(minValue=-360.0, maxValue=360.0, value=180.0)
                y_field = cmds.floatField(minValue=-360.0, maxValue=360.0, value=0.0)
                z_field = cmds.floatField(minValue=-360.0, maxValue=360.0, value=0.0)

                f_fields = [x_field, y_field, z_field]

                cmds.button(label='Zero', c=partial(zero_values, f_fields))

                cmds.setParent('..')

            cmds.button(func+'_obj', label=FUNCTIONS_NAMES[func], command=partial(eval(func), *args))

        if not args:
            cmds.button(func+'_obj', label=FUNCTIONS_NAMES[func], command=partial(eval(func)))

    if f_fields: set_change_commands(f_fields)


    # ウィンドウを表示
    cmds.showWindow(window_name)

def on_radio_button_changed(*args):
    aim_selected_axis = cmds.radioButtonGrp('aim_child_aim_radio_btn_grp', query=True, select=True)
    up_selected_axis = cmds.radioButtonGrp('aim_child_up_radio_btn_grp', query=True, select=True)

    aim_child_aim_check_v = cmds.checkBox('aim_child_aim_check', q=True, v=True)
    if aim_child_aim_check_v:
        aim_selected_axis = aim_selected_axis + 3

    aim_child_up_check_v = cmds.checkBox('aim_child_up_check', q=True, v=True)
    if aim_child_up_check_v:
        up_selected_axis = up_selected_axis + 3

    axis_num = {
        1:'x',
        2:'y',
        3:'z',
        4:'-x',
        5:'-y',
        6:'-z'
    }

    cmds.button('aim_child_obj', e=True, command=partial(eval('aim_child'), axis_num[aim_selected_axis], axis_num[up_selected_axis]))

def zero_values(f_fields=None, dummy=None):
    [cmds.floatField(f, e=True, value=0.0) for f in f_fields]

def set_change_commands(f_fields=None):
    [cmds.floatField(f, e=True, cc=partial(eval('change_commands_for_adjust_mirrors'), f_fields)) for f in f_fields]

def change_commands_for_adjust_mirrors(f_fields=None, dummy=None):
    values = [cmds.floatField(f, q=True, value=True) for f in f_fields]
    cmds.button('adjust_mirrors_obj', e=True, command=partial(eval('adjust_mirrors'), values))

def mirror_joint(dummy=None):
    cmds.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=["_L", "_R"])

if __name__ == '__main__':
    modify_joints(FUNCTIONS)
