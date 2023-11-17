# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma2

import math
import re
import traceback

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtMultimedia import *
    from PySide2.QtMultimediaWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance


DEFAULT_CTRL_SPACES = {
    'Cog_ctrl.space':'main',
    'ik_Ankle_L_ctrl.space':'main',
    'ik_Ankle_R_ctrl.space':'main',
    'ik_Knee_L_ctrl.space':'main',
    'ik_Knee_R_ctrl.space':'main',
    'ik_Wrist_L_ctrl.space':'main',
    'ik_Wrist_R_ctrl.space':'main',
    'ik_Elbow_L_ctrl.space':'main',
    'ik_Elbow_R_ctrl.space':'main',

    'Neck_ctrl.space':'spine',

    'Handattach_L_ctrl.space':'wrist',
    'Handattach_R_ctrl.space':'wrist',

    'ik_Wrist_L_ctrl.autoRot':1,
    'ik_Wrist_R_ctrl.autoRot':1
}

IK_AUTO_ROT_CTRLS = {
    'Wrist_L':'ik_rot_Wrist_L_ctrl',
    'Wrist_R':'ik_rot_Wrist_R_ctrl'
}

BAKE_BEFORE_BTN = 'attributeButton29'
SETKEY_IKFK_BTN = 'attributeButton28'

# Get Objects
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


# Set Objects
def set_enum_attr(ctrl=None, attr=None, val=None, rot_ctrl=None):
    wt = cmds.xform(ctrl, q=True, t=True, ws=True)
    if rot_ctrl:
        wr = cmds.xform(rot_ctrl, q=True, ro=True, ws=True)
    else:
        wr = cmds.xform(ctrl, q=True, ro=True, ws=True)

    list_attrs = cmds.listAttr(ctrl, ud=True, k=True) or list()

    if attr in list_attrs:
        get_en_attrs = cmds.addAttr(ctrl + '.' + attr, q=True, en=True)
        spl_get_en_attrs = get_en_attrs.split(':')
        if val in spl_get_en_attrs:
            enum_idx = spl_get_en_attrs.index(val)
            cmds.setAttr(ctrl+'.'+attr, enum_idx)

        cmds.xform(ctrl, t=wt, ro=wr, ws=True, a=True, p=True)
        if rot_ctrl:
            cmds.xform(rot_ctrl, ro=wr, ws=True, a=True, p=True)

def set_pole_vec(start=None, mid=None, end=None, move=None, obj=None):
    start = cmds.xform(start, q=True, t=True, ws=True)
    mid = cmds.xform(mid, q=True, t=True, ws=True)
    end = cmds.xform(end, q=True, t=True, ws=True)

    startV = om.MVector(start[0] ,start[1],start[2])
    midV = om.MVector(mid[0] ,mid[1],mid[2])
    endV = om.MVector(end[0] ,end[1],end[2])
    startEnd = endV - startV
    startMid = midV - startV
    dotP = startMid * startEnd
    proj = float(dotP) / float(startEnd.length())
    startEndN = startEnd.normal()
    projV = startEndN * proj
    arrowV = startMid - projV
    arrowV*= 0.5
    finalV = arrowV + midV
    cross1 = startEnd ^ startMid
    cross1.normalize()
    cross2 = cross1 ^ arrowV
    cross2.normalize()
    arrowV.normalize()
    matrixV = [arrowV.x , arrowV.y , arrowV.z , 0 ,cross1.x ,cross1.y , cross1.z , 0 ,cross2.x , cross2.y , cross2.z , 0,0,0,0,1]
    matrixM = om.MMatrix()
    om.MScriptUtil.createMatrixFromList(matrixV , matrixM)
    matrixFn = om.MTransformationMatrix(matrixM)
    rot = matrixFn.eulerRotation()

    pvLoc = cmds.spaceLocator(n='poleVecPosLoc')
    cmds.xform(pvLoc[0] , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
    cmds.xform(pvLoc[0] , ws = 1 , rotation = ((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0)))
    cmds.select(pvLoc[0])
    cmds.move(move, 0, 0, r=1, os=1, wd=1)

    cmds.matchTransform(obj, pvLoc[0])
    cmds.delete(pvLoc[0])


# Animation
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

            playmin = cmds.playbackOptions(q=1, min=1)
            playmax = cmds.playbackOptions(q=1, max=1)

            start = playmin
            end = playmax

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

def bake_with_func_for_timeSlider(func):
    def wrapper(*args, **kwargs):
        cur_time=cmds.currentTime(q=1)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = 1
        else:
            autoKeyState = 0

        cmds.autoKeyframe(st=0)

        try:
            cmds.refresh(su=1)

            playmin = cmds.playbackOptions(q=1, min=1)
            playmax = cmds.playbackOptions(q=1, max=1)

            start = playmin
            end = playmax-1

            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            if gPlayBackSlider:
                if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
                    frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
                    start = frameRange[0]
                    end = frameRange[1]
                else:
                    frameRange = cmds.currentTime(q=1)
                    start = frameRange
                    end = frameRange-1
            else:
                end = playmax

            if playmax < end:
                end = playmax

            setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
            if setkey_attrs == []:
                setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

            for i in range (int(start), int(end+1)):
                cmds.currentTime(i, e=True)
                func(*args, **kwargs)

            cmds.refresh(su=0)

        except:
            cmds.refresh(su=0)
            print(traceback.format_exc())

        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)

    return wrapper

def select_time_slider_range(start, end):

    app = QApplication.instance()

    widgetStr = mel.eval('$gPlayBackSlider=$gPlayBackSlider')
    ptr = omui.MQtUtil.findControl(widgetStr)
    slider = wrapInstance(int(ptr), QWidget)

    slider_width = slider.size().width()
    slider_height = slider.size().height()

    # Store time slider settings
    min_time = cmds.playbackOptions(query=True, minTime=True)
    max_time = cmds.playbackOptions(query=True, maxTime=True)
    animation_start_time = cmds.playbackOptions(query=True, animationStartTime=True)
    animation_end_time = cmds.playbackOptions(query=True, animationEndTime=True)
    t = cmds.currentTime(query=True)

    # Set the time slider to the range we want so we have
    # perfect precision to click at the start and end of the
    # time slider.
    cmds.playbackOptions(minTime=start)
    cmds.playbackOptions(maxTime=end-1)

    a_pos = QPoint(0, slider_height / 2.0)
    b_pos = QPoint(slider_width, slider_height / 2.0)

    # Trigger some mouse events on the Time Control
    # Somehow we need to have some move events around
    # it so the UI correctly understands it stopped
    # clicking, etc.
    event = QMouseEvent(QEvent.MouseMove,
                              a_pos,
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.NoModifier)
    app.sendEvent(slider, event)

    event = QMouseEvent(QEvent.MouseButtonPress,
                              a_pos,
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.ShiftModifier)
    app.sendEvent(slider, event)

    event = QMouseEvent(QEvent.MouseMove,
                              b_pos,
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.ShiftModifier)
    app.sendEvent(slider, event)

    event = QMouseEvent(QEvent.MouseButtonRelease,
                              b_pos,
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.ShiftModifier)
    app.sendEvent(slider, event)

    event = QMouseEvent(QEvent.MouseMove,
                              b_pos,
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.NoModifier)
    app.sendEvent(slider, event)
    app.processEvents()

    # Reset time slider settings
    cmds.playbackOptions(minTime=min_time)
    cmds.playbackOptions(maxTime=max_time)
    cmds.playbackOptions(animationStartTime=animation_start_time)
    cmds.playbackOptions(animationEndTime=animation_end_time)
    cmds.currentTime(t)

def get_times_from_bake_before():
    beforeBakeValue = mel.eval('float $at_val = `MGPickerItem -q -atv {}`;'.format(BAKE_BEFORE_BTN))
    times = None
    if beforeBakeValue:
        gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
        times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)

    return beforeBakeValue, times

def get_animCurve(obj=None, attrs=None):
    settings = {
        'p':True,
        's':True,
        'type':'animCurve'
    }
    anim_curves_list = list()
    for at in attrs:
        anim_curves = cmds.listConnections('{}.{}'.format(obj, at), **settings) or None
        if anim_curves: anim_curves_list.append(anim_curves[0])

    return anim_curves_list

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

def quaternionToEuler_no_key(obj=None):
    rot = cmds.xform(obj, q=True, ro=True, os=True)
    rotOrder = cmds.getAttr('{}.rotateOrder'.format(obj))
    euler = om2.MEulerRotation(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder)
    quat = euler.asQuaternion()
    euler = quat.asEulerRotation()
    r = euler.reorder(rotOrder)

    cmds.xform(obj, ro=[math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)], os=True, a=True)

    return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)

@bake_with_func
def get_values_per_frame(ctrl_values=None, ctrls=None):
    frame = cmds.currentTime(q=True)
    ctrl_values[frame] = OrderedDict()
    for ctrl in ctrls:
        ctrl_values[frame][ctrl] = get_values(ctrl)

def merge_ctrl_values(merge_ctrl_dict=None, ctrls=None):
    ctrl_values = OrderedDict()
    get_values_per_frame(ctrl_values=ctrl_values, ctrls=ctrls)

    for merge_da in merge_ctrl_dict:
        merge_src = merge_da['merge_src']
        merge_dst = merge_da['merge_dst']

        for frame, values in ctrl_values.items():
            src_w_val = ctrl_values[frame][merge_src][0]
            dst_w_val = ctrl_values[frame][merge_dst][0]

            src_w_val[merge_src + '.t'] = dst_w_val[merge_dst + '.t']
            src_w_val[merge_src + '.r'] = dst_w_val[merge_dst + '.r']


    for frame, values in ctrl_values.items():
        cmds.currentTime(frame, e=True)
        for ctrl, ctrl_at in values.items():
            ctrl_val = ctrl_at[0]
            wt_val = ctrl_val[ctrl + '.t']
            wr_val = ctrl_val[ctrl + '.r']
            cmds.xform(ctrl, t=wt_val, ro=wr_val, p=True, ws=True, a=True)
            cmds.setKeyframe(ctrl)

def merge_ctrl_values_per_frames(merge_ctrl_dict=None, ctrls=None):
    try:
        cmds.refresh(su=1)

        cur_time=cmds.currentTime(q=1)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = True
        else:
            autoKeyState = False

        cmds.autoKeyframe(st=0)

        merge_ctrl_values(merge_ctrl_dict, ctrls)

        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)

        cmds.refresh(su=0)

    except:
        cmds.refresh(su=0)
        print(traceback.format_exc())


# MGPicker class
class MGP:
    def __init__(self):
        self.cur_mgp_btn = None
        self.mgp_btn_members = []

    def get_current_picker_items(self):
        self.cur_mgp_btn = cmds.MGPicker(q=True, currentItem=True)
        self.mgp_btn_members = cmds.MGPickerItem(self.cur_mgp_btn, q=True, selectMembers=True)

# Namespace class
class Namespace:
    def __init__(self):
        self.cur_nss = None

        try:
            self.get_current_picker_namespace()
        except:
            print(traceback.format_exc())

    def get_current_picker_namespace(self):
        self.cur_nss = mel.eval('MGP_GetCurrentPickerNamespace')

        if self.cur_nss:
            self.cur_nss = self.cur_nss + ':'
        else:
            self.cur_nss = ''

    def set_namespace_via_selection(self):
        sel = cmds.ls(os=True)
        if sel:
            mel.eval("MGP_SetPickerNamespace_Via_Selection;")
        else:
            cmds.MGPickerView(e=1, namespace='')

# Controller class
class Ctrl(Namespace, MGP):
    def __init__(self, prefix=None, suffix=None):
        # Namespace Activate
        self.get_current_picker_namespace()

        self.prefix = prefix
        self.suffix = suffix

        self.all_ctrls = []
        self.all_ctrls_without_namespace = []

        self.get_ctrls()

    def get_ctrls(self):
        all_suffix_ctrls = cmds.ls('{}*{}'.format(self.cur_nss, self.suffix))
        all_prefix_ctrls = cmds.ls('{}{}*'.format(self.cur_nss, self.prefix))

        if all_suffix_ctrls: [self.all_ctrls.append(n) for n in all_suffix_ctrls]
        if all_prefix_ctrls: [self.all_ctrls.append(n) for n in all_prefix_ctrls]

        self.all_ctrls.sort()
        if self.all_ctrls:
            self.all_ctrls = order_dags(self.all_ctrls)
            self.all_ctrls_without_namespace = [n.replace(self.cur_nss, '') for n in self.all_ctrls]
        else:
            print('Ooops! There are no controllers.')

    def zero_out(self):
        for ctrl in self.all_ctrls:
            try:
                cmds.xform(ctrl, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
            except:
                print(traceback.format_exc())

    def reset_spaces(self):
        for ctrl_at, sp_at in DEFAULT_CTRL_SPACES.items():
            if type(sp_at) == str:
                get_en_attrs = cmds.addAttr(self.cur_nss + ctrl_at, q=True, en=True)
                spl_get_en_attrs = get_en_attrs.split(':')
                if sp_at in spl_get_en_attrs:
                    enum_idx = spl_get_en_attrs.index(sp_at)
                    cmds.setAttr(self.cur_nss + ctrl_at, enum_idx)

            elif type(sp_at) == int:
                cmds.setAttr(self.cur_nss + ctrl_at, sp_at)

    def space_match(self, attr=None, val=None, auto_side=None):
        self.get_current_picker_items()
        rot_ctrl = self.cur_nss + IK_AUTO_ROT_CTRLS[auto_side]
        [set_enum_attr(ctrl=ctrl, attr=attr, val=val, rot_ctrl=rot_ctrl) for ctrl in self.mgp_btn_members]

    def get_hand_L_ctrl_values(self):
        ikfk_switch = self.cur_nss+'ikfk_Wrist_L_ctrl.ikfk'
        state = cmds.getAttr(ikfk_switch)
        jnts = [self.cur_nss+'proxy_Arm_L',
                self.cur_nss+'proxy_Elbow_L',
                self.cur_nss+'proxy_Wrist_L']
        ctrls = [self.cur_nss+'Arm_L_ctrl',
                 self.cur_nss+'Elbow_L_ctrl',
                 self.cur_nss+'Wrist_L_ctrl']

        ik_pos_ctrl = self.cur_nss+'ik_Wrist_L_ctrl'
        ik_rot_ctrl = self.cur_nss+'ik_rot_Wrist_L_ctrl'
        ikpv_ctrl = self.cur_nss+'ik_Elbow_L_ctrl'

        pos_match_loc = self.cur_nss+'proxy_Wrist_L_match_loc'
        ikpv_match_loc = self.cur_nss+'proxy_Elbow_L_match_loc'

        return ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc

    def get_foot_L_ctrl_values(self):
        ikfk_switch = self.cur_nss+'ikfk_Ankle_L_ctrl.ikfk'
        state = cmds.getAttr(ikfk_switch)
        jnts = [self.cur_nss+'proxy_Thigh_L',
                self.cur_nss+'proxy_Knee_L',
                self.cur_nss+'proxy_Ankle_L',
                self.cur_nss+'proxy_Toe_L',]
        ctrls = [self.cur_nss+'Thigh_L_ctrl',
                 self.cur_nss+'Knee_L_ctrl',
                 self.cur_nss+'Ankle_L_ctrl',
                 self.cur_nss+'Toe_L_ctrl']

        ik_pos_ctrl = self.cur_nss+'ik_Ankle_L_ctrl'
        ik_rot_ctrl = self.cur_nss+'ik_Toe_L_ctrl'
        ikpv_ctrl = self.cur_nss+'ik_Knee_L_ctrl'

        pos_match_loc = self.cur_nss+'proxy_Ankle_L_match_loc'
        ikpv_match_loc = self.cur_nss+'proxy_Knee_L_match_loc'

        return ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc

    def match_autorot_ctrl(self, ctrl=None, set_ctrl_and_attr='autoRot', force_set=None):
        wt = cmds.xform(ctrl, q=True, t=True, ws=True)
        wr =cmds.xform(ctrl, q=True, ro=True, ws=1)

        if force_set:
            if force_set == 'on':
                cmds.setAttr(set_ctrl_and_attr, 1)
            elif force_set == 'off':
                cmds.setAttr(set_ctrl_and_attr, 0)

        else:
            if cmds.getAttr(set_ctrl_and_attr):
                cmds.setAttr(set_ctrl_and_attr, 0)
            else:
                cmds.setAttr(set_ctrl_and_attr, 1)

        cmds.xform(ctrl, t=wt, ws=True, a=True, p=True)
        cmds.xform(ctrl, ro=wr, ws=True, a=True, p=True)

    def match_foot_roll(self, setkey=None, side='_L_', main_to_foot=None):
        foot_roll_match = {
            self.cur_nss + 'ik_Ankle_L_ctrl':
                {
                    'matchloc':self.cur_nss + 'proxy_Ankle_L_match_loc',
                    'main':self.cur_nss + 'roll_main_Ankle_L_ctrl',
                    'tippytoe':self.cur_nss + 'roll_tippytoe_Ankle_L_ctrl',
                    'heel':self.cur_nss + 'roll_heel_Ankle_L_ctrl',
                    'inside':self.cur_nss + 'roll_in_Ankle_L_ctrl',
                    'outside':self.cur_nss + 'roll_out_Ankle_L_ctrl',
                    'rolltoe':self.cur_nss + 'roll_Toe_L_ctrl',
                    'toe':self.cur_nss + 'ik_Toe_L_ctrl',
                    'rollankle':self.cur_nss + 'roll_Ankle_L_ctrl',
                    'stoptoe':self.cur_nss + 'roll_stoptoe_Toe_L_ctrl',
                },
            self.cur_nss + 'ik_Ankle_R_ctrl':
                {
                    'matchloc':self.cur_nss + 'proxy_Ankle_R_match_loc',
                    'main':self.cur_nss + 'roll_main_Ankle_R_ctrl',
                    'tippytoe':self.cur_nss + 'roll_tippytoe_Ankle_R_ctrl',
                    'heel':self.cur_nss + 'roll_heel_Ankle_R_ctrl',
                    'inside':self.cur_nss + 'roll_in_Ankle_R_ctrl',
                    'outside':self.cur_nss + 'roll_out_Ankle_R_ctrl',
                    'rolltoe':self.cur_nss + 'roll_Toe_R_ctrl',
                    'toe':self.cur_nss + 'ik_Toe_R_ctrl',
                    'rollankle':self.cur_nss + 'roll_Ankle_R_ctrl',
                    'stoptoe':self.cur_nss + 'roll_stoptoe_Toe_R_ctrl',
                },
        }

        for foot_ctrl, match_settings in foot_roll_match.items():
            if side in foot_ctrl:
                matchloc = match_settings['matchloc']
                main = match_settings['main']
                tippytoe = match_settings['tippytoe']
                heel = match_settings['heel']
                inside = match_settings['inside']
                outside = match_settings['outside']
                rolltoe = match_settings['rolltoe']
                toe = match_settings['toe']
                rollankle = match_settings['rollankle']
                stoptoe = match_settings['stoptoe']

                matchloc_wt = cmds.xform(matchloc, q=True, t=True, ws=True)
                matchloc_wr = cmds.xform(matchloc, q=True, ro=True, ws=True)

                footroll_wt = cmds.xform(rolltoe, q=True, t=True, ws=True)
                footroll_wr = cmds.xform(rolltoe, q=True, ro=True, ws=True)

                toe_wr = cmds.xform(toe, q=True, ro=True, ws=True)

                foot_roll_ctrls = [
                    main,
                    tippytoe,
                    heel,
                    inside,
                    outside,
                    rolltoe,
                    toe,
                    rollankle,
                    stoptoe,
                ]

                [cmds.xform(obj, t=[0,0,0], ro=[0,0,0], a=True) for obj in foot_roll_ctrls]

                if main_to_foot:
                    # main > footroll
                    cmds.xform(foot_ctrl, t=[0,0,0], ro=[0,0,0], a=True)
                    cmds.xform(rolltoe, t=footroll_wt, ro=footroll_wr, ws=True, p=True, a=True)

                else:
                    # footroll > main
                    cmds.xform(foot_ctrl, t=matchloc_wt, ro=matchloc_wr, ws=True, p=True, a=True)

                cmds.xform(toe, ro=toe_wr, ws=True, p=True, a=True)

                if setkey:
                    [cmds.setKeyframe(obj) for obj in foot_roll_ctrls]
                    cmds.setKeyframe(foot_ctrl)

    def root_position_under_cog(self):
        cog_ctrl = self.cur_nss + 'Cog_ctrl'
        root_ctrl = self.cur_nss + 'Root_ctrl'

        root_match_constraints_sets = 'root_match_constraints_sets'
        if not cmds.objExists(root_match_constraints_sets):
            cmds.sets(n=root_match_constraints_sets, em=True)


        cog_loc = cmds.spaceLocator()
        ground_loc = cmds.spaceLocator()

        cmds.sets([cog_loc[0], ground_loc[0]], add=root_match_constraints_sets)

        cog_wt = cmds.xform(cog_ctrl, q=True, t=True, ws=True)
        cmds.xform(root_ctrl, t=[cog_wt[0], 0, cog_wt[2]], ws=True)

        cmds.matchTransform(cog_loc, cog_ctrl)
        cmds.pointConstraint(cog_loc, ground_loc, w=True, skip=['y'])

        cmds.xform(cog_loc, t=[0,0,50], r=True, os=True)

        cmds.parentConstraint(cog_ctrl, cog_loc, w=True, mo=True)

        aim_const = cmds.aimConstraint(ground_loc,
                           root_ctrl,
                           w=True,
                           offset=[0,0,0],
                           aimVector=[0,0,1],
                           upVector=[0,1,0],
                           worldUpType='object',
                           worldUpObject=cog_ctrl,
                           skip=['x', 'z'])

        po_const = cmds.pointConstraint(cog_ctrl, root_ctrl, w=True, mo=True, skip=['y'])

        cmds.sets([aim_const[0], po_const[0]], add=root_match_constraints_sets)

    def root_to_main(self):
        merge_ctrl_dict = [
            {
                'merge_src':'main_ctrl',
                'merge_dst':'Root_ctrl',
            }
        ]

        for values in merge_ctrl_dict:
            values['merge_src'] = self.cur_nss + values['merge_src']
            values['merge_dst'] = self.cur_nss + values['merge_dst']

        merge_ctrl_values_per_frames(merge_ctrl_dict, self.all_ctrls)

# Animation class
class Animation:
    def __init__(self, prefix=None, suffix=None):
        self.ctrl = Ctrl(prefix=prefix, suffix=suffix)

    def fullbake(self, sel=None):
        try:
            cmds.refresh(su=True)
            cmds.cycleCheck(e=False)

            playmin = cmds.playbackOptions(q=True, min=True)
            playmax = cmds.playbackOptions(q=True, max=True)

            if not sel:
                sel = cmds.ls(os=True)
            cmds.bakeResults(sel,
                             sm=True,
                             t=(playmin, playmax),
                             sb=True,
                             osr=True,
                             dic=True,
                             pok=True,
                             sac=False,
                             ral=False,
                             rba=False,
                             bol=False,
                             mr=True,
                             cp=False,
                             s=False)

            cmds.filterCurve(sel, f='euler')

            cmds.refresh(su=False)
            cmds.cycleCheck(e=True)
        except:
            cmds.refresh(su=False)
            cmds.cycleCheck(e=True)

    def before_bakes_hand(self, side=None, time_range=None):
        before_bakes = list()
        ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc = self.ctrl.get_hand_L_ctrl_values()

        # left append
        if '_L_' == side or 'both' == side:
            before_bakes.append(ik_pos_ctrl)
            before_bakes.append(ik_rot_ctrl)
            before_bakes.append(ikpv_ctrl)
            [before_bakes.append(ctrl) for ctrl in ctrls]

        # right append
        if '_R_' == side or 'both' == side:
            R_ik_pos_ctrl = mirror_character(['_L', '_R'], ik_pos_ctrl)
            R_ik_rot_ctrl = mirror_character(['_L', '_R'], ik_rot_ctrl)
            R_ikpv_ctrl = mirror_character(['_L', '_R'], ikpv_ctrl)
            R_ctrls = [mirror_character(['_L', '_R'], ctrl) for ctrl in ctrls]

            before_bakes.append(R_ik_pos_ctrl)
            before_bakes.append(R_ik_rot_ctrl)
            before_bakes.append(R_ikpv_ctrl)
            [before_bakes.append(r_ctrl) for r_ctrl in R_ctrls]

        # before bake
        self.fullbake(before_bakes)
        if 1 < time_range[1] - time_range[0]:
            select_time_slider_range(*time_range)

    def before_bakes_foot(self, side=None, time_range=None):
        before_bakes = list()
        ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc = self.ctrl.get_foot_L_ctrl_values()

        # left append
        if '_L_' == side or 'both' == side:
            before_bakes.append(ik_pos_ctrl)
            before_bakes.append(ik_rot_ctrl)
            before_bakes.append(ikpv_ctrl)
            [before_bakes.append(ctrl) for ctrl in ctrls]

            roll_Toe_L_ctrl = self.ctrl.cur_nss + 'roll_Toe_L_ctrl'
            before_bakes.append(roll_Toe_L_ctrl)

        # right append
        if '_R_' == side or 'both' == side:
            R_ik_pos_ctrl = mirror_character(['_L', '_R'], ik_pos_ctrl)
            R_ik_rot_ctrl = mirror_character(['_L', '_R'], ik_rot_ctrl)
            R_ikpv_ctrl = mirror_character(['_L', '_R'], ikpv_ctrl)
            R_ctrls = [mirror_character(['_L', '_R'], ctrl) for ctrl in ctrls]

            before_bakes.append(R_ik_pos_ctrl)
            before_bakes.append(R_ik_rot_ctrl)
            before_bakes.append(R_ikpv_ctrl)
            [before_bakes.append(r_ctrl) for r_ctrl in R_ctrls]

            roll_Toe_R_ctrl = self.ctrl.cur_nss + 'roll_Toe_R_ctrl'
            before_bakes.append(roll_Toe_R_ctrl)

        # before bake
        self.fullbake(before_bakes)
        if 1 < time_range[1] - time_range[0]:
            select_time_slider_range(*time_range)

    @bake_with_func
    def set_and_bake(self, sel=None, xform_set=None):
        [cmds.xform(obj, **xform_set) for obj in sel] if sel else False
        cmds.setKeyframe(sel)

    @bake_with_func
    def correctkeys(self, sel=None):
        if not sel:
            sel = cmds.ls(os=True)
            if not sel:
                return

        [quaternionToEuler(obj=obj) for obj in sel] if sel else False

    def cog_hip_matchbake(self, bake_to=None):
        cog_ctrl = self.ctrl.cur_nss + 'Cog_ctrl'
        hip_ctrl = self.ctrl.cur_nss + 'Hip_ctrl'
        spine_ctrl = self.ctrl.cur_nss + 'Spine1_ctrl'

        hip_jnt = self.ctrl.cur_nss + 'Hip_ctrl_con'

        cog_hip_match_sets = 'cog_hip_match_sets'
        cmds.sets(em=True, n=cog_hip_match_sets) if not cmds.objExists(cog_hip_match_sets) else False

        cog_match_loc_p = cmds.spaceLocator()[0]
        cog_match_loc = cmds.spaceLocator()[0]
        cmds.parent(cog_match_loc, cog_match_loc_p)

        hip_match_loc_p = cmds.spaceLocator()[0]
        hip_match_loc = cmds.spaceLocator()[0]
        cmds.parent(hip_match_loc, hip_match_loc_p)

        spine_match_loc_p = cmds.spaceLocator()[0]
        spine_match_loc = cmds.spaceLocator()[0]
        cmds.parent(spine_match_loc, spine_match_loc_p)

        cmds.matchTransform(cog_match_loc_p, cog_ctrl)
        cmds.matchTransform(hip_match_loc_p, hip_ctrl)
        cmds.matchTransform(spine_match_loc_p, spine_ctrl)

        spine_cog_match_loc_p = cmds.spaceLocator()[0]
        spine_cog_match_loc = cmds.spaceLocator()[0]
        cmds.parent(spine_cog_match_loc, spine_cog_match_loc_p)
        cmds.parentConstraint(spine_ctrl, spine_cog_match_loc_p, w=True, mo=False)
        cmds.sets(spine_cog_match_loc_p, add=cog_hip_match_sets)

        ########
        # Cog > Hip
        ########
        if bake_to == 'hip':
            cmds.parent(hip_match_loc_p, cog_match_loc)
            cmds.parent(spine_match_loc_p, hip_match_loc)

            cmds.sets(cog_match_loc_p, add=cog_hip_match_sets)

            cmds.parentConstraint(cog_ctrl, cog_match_loc_p, w=True, mo=True)
            cmds.parentConstraint(spine_ctrl, spine_match_loc_p, w=True, mo=True)
            self.fullbake([cog_match_loc_p, spine_match_loc_p])
            cmds.parentConstraint(hip_match_loc, hip_ctrl, st=['x', 'y', 'z'], w=True, mo=True)
            self.set_and_bake(sel=[cog_ctrl], xform_set={'ro':[0,0,0], 'a':True})

            self.fullbake([spine_cog_match_loc_p])
            cmds.pointConstraint(spine_cog_match_loc_p, cog_ctrl, w=True, mo=True)
            cmds.pointConstraint(spine_match_loc_p, spine_cog_match_loc_p, w=True, mo=False)
            ori = cmds.orientConstraint(spine_match_loc_p, spine_ctrl, w=True, mo=False)
            cmds.setAttr('{}.interpType'.format(ori[0]), 2)

        ########
        # Hip > Cog
        ########
        if bake_to == 'cog':
            cmds.parent(cog_match_loc_p, hip_match_loc)
            cmds.parent(spine_match_loc_p, cog_match_loc)

            cmds.sets(hip_match_loc_p, add=cog_hip_match_sets)

            cmds.parentConstraint(hip_jnt, cog_match_loc_p, w=True, mo=False)
            cmds.parentConstraint(hip_ctrl, hip_match_loc_p, w=True, mo=False)
            cmds.parentConstraint(spine_ctrl, spine_match_loc_p, w=True, mo=False)
            self.fullbake([cog_match_loc_p, hip_match_loc_p, spine_match_loc_p])
            cmds.parentConstraint(cog_match_loc, cog_ctrl, w=True, mo=False)
            self.set_and_bake(sel=[hip_ctrl], xform_set={'ro':[0,0,0], 'a':True})
            ori = cmds.orientConstraint(spine_match_loc_p, spine_ctrl, w=True, mo=False)
            cmds.setAttr('{}.interpType'.format(ori[0]), 2)


        self.fullbake([cog_ctrl, hip_ctrl, spine_ctrl])
        cmds.select(cog_hip_match_sets, r=True, ne=True)
        bake_objs = cmds.pickWalk(d='down')
        cmds.delete(bake_objs)

    @bake_with_func_for_timeSlider
    def ik_autorot_match_bake(self, ik_autorot_dict=None):
        if ik_autorot_dict:
            for ctrl, ik_auto in ik_autorot_dict.items():
                attr = ik_auto['attr']
                force_set = ik_auto['force_set']
                self.ctrl.match_autorot_ctrl(ctrl=ctrl, set_ctrl_and_attr=attr, force_set=force_set)
                cmds.setKeyframe([ctrl, attr.split('.')[0]])

    def ik_hand_autorot(self, on_off=None):
        autoRot_L_ctrl = self.ctrl.cur_nss + 'ik_rot_Wrist_L_ctrl'
        autoRot_L_attr = self.ctrl.cur_nss +'ik_Wrist_L_ctrl.autoRot'

        autoRot_R_ctrl = self.ctrl.cur_nss + 'ik_rot_Wrist_R_ctrl'
        autoRot_R_attr = self.ctrl.cur_nss +'ik_Wrist_R_ctrl.autoRot'

        ik_autorot_dict = {}

        ctrls = cmds.ls(os=True)
        if (autoRot_L_ctrl in ctrls
            or autoRot_L_attr.split('.')[0] in ctrls):

            ik_autorot_dict[autoRot_L_ctrl] = {}
            ik_autorot_dict[autoRot_L_ctrl]['attr'] = autoRot_L_attr
            ik_autorot_dict[autoRot_L_ctrl]['force_set'] = on_off

        if (autoRot_R_ctrl in ctrls
            or autoRot_R_attr.split('.')[0] in ctrls):

            ik_autorot_dict[autoRot_R_ctrl] = {}
            ik_autorot_dict[autoRot_R_ctrl]['attr'] = autoRot_R_attr
            ik_autorot_dict[autoRot_R_ctrl]['force_set'] = on_off

        self.ik_autorot_match_bake(ik_autorot_dict=ik_autorot_dict)

    @bake_with_func_for_timeSlider
    def foot_roll_match_bake(self,
                             side=['_L_', '_R_'],
                             main_to_foot=None):
        [self.ctrl.match_foot_roll(setkey=True, side=s, main_to_foot=main_to_foot) for s in side]

    def foot_roll_match_bake_before(self,
                                    side='_L_',
                                    main_to_foot=None):

        beforeBakeValue, times = get_times_from_bake_before()

        if beforeBakeValue:
            self.before_bakes_foot(side=side, time_range=times)
        self.foot_roll_match_bake(side=[side], main_to_foot=main_to_foot)

    @bake_with_func_for_timeSlider
    def space_match_bake(self,
                         ctrls=None,
                         space_match=None,
                         space_attr=None,
                         set_space=None,
                         auto_rot_match=None,
                         auto_rot_attr=None,
                         auto_rot_force_set=None):

        if not ctrls:
            ctrls = cmds.ls(os=True)
            if not ctrls:
                return

        ctrls = order_dags(ctrls)

        rot_ctrls = {
            self.ctrl.cur_nss + 'ik_Wrist_L_ctrl':self.ctrl.cur_nss + 'ik_rot_Wrist_L_ctrl',
            self.ctrl.cur_nss + 'ik_Wrist_R_ctrl':self.ctrl.cur_nss + 'ik_rot_Wrist_R_ctrl',
        }

        if space_match:
            for ctrl in ctrls:
                if ctrl in rot_ctrls.keys():
                    set_enum_attr(ctrl=ctrl, attr=space_attr, val=set_space, rot_ctrl=rot_ctrls[ctrl])
                else:
                    set_enum_attr(ctrl=ctrl, attr=space_attr, val=set_space)

            cmds.setKeyframe(ctrls)

        elif auto_rot_match:
            if len(auto_rot_attr) == 2 and type(auto_rot_attr) == list:
                for j, artr in enumerate(auto_rot_attr):
                    for autorot_ctrls in ctrls:
                        self.ctrl.match_autorot_ctrl(ctrl=autorot_ctrls[0], set_ctrl_and_attr=artr, force_set=auto_rot_force_set)
                        cmds.setKeyframe(autorot_ctrls)
            else:
                [self.ctrl.match_autorot_ctrl(ctrl=ctrl, set_ctrl_and_attr=auto_rot_attr, force_set=auto_rot_force_set) for ctrl in ctrls]

                cmds.setKeyframe(ctrls)

    def fix_fbx_anim(self):
        chr_nss = '{}chr:'.format(self.ctrl.cur_nss)
        chr_shapes = cmds.ls(chr_nss+'*', type='mesh')

        influences = []
        for sh in chr_shapes:
            mesh = cmds.listRelatives(sh, p=True) or None
            skin_cluster = cmds.ls(cmds.listHistory(mesh), type='skinCluster')

            # Get the influences (joints) affecting the skin
            if skin_cluster:
                infs = cmds.skinCluster(skin_cluster, query=True, inf=True)
                if infs:
                    for inf in infs:
                        if not inf in influences:
                            influences.append(inf)

        chr_joints = [n.replace(chr_nss, '') for n in influences]

        self.fix_pos_anim(chr_joints=chr_joints, chr_nss=chr_nss)

    def fix_pos_anim(self, chr_joints=None, chr_nss=None):
        # 移動値を残すノード
        delete_pos_nodes = [
            'Root',
            'Hip',
            'Handattach_L',
            'Handattach_R'
        ]

        delete_pos_attrs = [
            'tx',
            'ty',
            'tz'
        ]

        # 回転のアニメーションを削除するノード
        delete_rot_nodes = [
            'HandattachOffset_L',
            'HandattachOffset_R'
        ]

        delete_rot_attrs = [
            'rx',
            'ry',
            'rz'
        ]

        # スケールのアニメーションを削除するノード
        delete_scl_nodes = [
            'HandattachOffset_L',
            'HandattachOffset_R'
        ]

        delete_scl_attrs = [
            'sx',
            'sy',
            'sz'
        ]

        chr_joints = [j for j in chr_joints if cmds.objExists(j)]

        for ch_j in chr_joints:
            if cmds.objectType(ch_j) == 'joint':
                if not ch_j in delete_pos_nodes:
                    anim_curves = get_animCurve(obj=ch_j, attrs=delete_pos_attrs)
                    [cmds.delete(ac.split('.')[0]) for ac in anim_curves]

                    try:
                        cmds.setAttr(ch_j + '.t', *cmds.getAttr(chr_nss + ch_j + '.t')[0])
                    except:
                        print(traceback.format_exc())

                if ch_j in delete_rot_nodes:
                    anim_curves = get_animCurve(obj=ch_j, attrs=delete_rot_attrs)
                    [cmds.delete(ac.split('.')[0]) for ac in anim_curves]

                    try:
                        cmds.setAttr(ch_j + '.r', *cmds.getAttr(chr_nss + ch_j + '.r')[0])
                        # cmds.xform(ch_j, ro=cmds.xform(chr_nss + ch_j, q=True, ro=True, ws=True), ws=True, a=True)
                        quaternionToEuler_no_key(obj=ch_j)
                    except:
                        print(traceback.format_exc())

                if ch_j in delete_scl_nodes:
                    anim_curves = get_animCurve(obj=ch_j, attrs=delete_scl_attrs)
                    [cmds.delete(ac.split('.')[0]) for ac in anim_curves]

                    try:
                        cmds.setAttr(ch_j + '.s', *cmds.getAttr(chr_nss + ch_j + '.s')[0])
                    except:
                        print(traceback.format_exc())


class IKFK:
    def __init__(self, prefix=None, suffix=None):
        self.ctrl = Ctrl(prefix=prefix, suffix=suffix)
        self.anim = Animation(prefix=prefix, suffix=suffix)

    def ik2fk_match(self,
                    ctrls=None,
                    jnts=None,
                    ikfk_switch=None,
                    match=None):
        sel = cmds.ls(os=True)
        # IK to FK
        if match:
            [cmds.matchTransform(ctrl, jt, rot=1, pos=0, scl=0) for ctrl, jt in zip(ctrls, jnts)]
        cmds.setAttr(ikfk_switch, 0)

        cmds.select(sel, r=True)

    def fk2ik_match(self,
                    match_type=None,
                    ik_pos_ctrl=None,
                    pos_match_loc=None,
                    ikpv_ctrl=None,
                    ikpv_match_loc=None,
                    ik_rot_ctrl=None,
                    rot_match_jnt=None,
                    ikfk_switch=None,
                    match=None,
                    start=None,
                    mid=None,
                    end=None,
                    move=None,
                    loc_match=None):

        sel = cmds.ls(os=True)
        # FK to IK
        if match:
            if loc_match:
                cmds.matchTransform(ik_pos_ctrl, pos_match_loc)
                cmds.matchTransform(ikpv_ctrl, ikpv_match_loc)
                cmds.matchTransform(ik_rot_ctrl, rot_match_jnt)
            else:
                cmds.matchTransform(ik_pos_ctrl, pos_match_loc, rot=1, pos=1, scl=0)
                set_pole_vec(start=start, mid=mid, end=end, move=move, obj=ikpv_ctrl)
                # cmds.matchTransform(ikpv_ctrl, ikpv_match_loc, rot=1, pos=1, scl=0)
                cmds.matchTransform(ik_rot_ctrl, rot_match_jnt, rot=1, pos=1, scl=0)

        cmds.setAttr(ikfk_switch, 1)

        cmds.select(sel, r=True)


    def ikfk_hand_L(self,
                    picker=None,
                    match=None,
                    force_state=None,
                    force_state_key=None):
        ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc = self.ctrl.get_hand_L_ctrl_values()

        if force_state:
            if force_state == 'ik2fk':
                state = 1
            elif force_state == 'fk2ik':
                state = 0
            cmds.setAttr(ikfk_switch, state)

            cmds.setKeyframe(ikfk_switch) if force_state_key else False

        if state == 1:
            self.ik2fk_match(ctrls=ctrls,
                        jnts=jnts,
                        ikfk_switch=ikfk_switch,
                        match=match)

            if picker:
                # IK
                mel.eval('MGPickerItem -e -vis false selectButton79;')
                mel.eval('MGPickerItem -e -vis false selectButton88;')
                mel.eval('MGPickerItem -e -vis false selectButton101;')

                # FK
                mel.eval('MGPickerItem -e -vis true selectButton99;')
                mel.eval('MGPickerItem -e -vis true selectButton94;')
                mel.eval('MGPickerItem -e -vis true selectButton91;')

        else:
            self.fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                        pos_match_loc=pos_match_loc,
                        ikpv_ctrl=ikpv_ctrl,
                        ikpv_match_loc=ikpv_match_loc,
                        ik_rot_ctrl=ik_rot_ctrl,
                        rot_match_jnt=jnts[2],
                        ikfk_switch=ikfk_switch,
                        match=match,
                        start=jnts[0],
                        mid=jnts[1],
                        end=jnts[2],
                        move=50,
                        loc_match=True)

            if picker:
                # IK
                mel.eval('MGPickerItem -e -vis true selectButton79;')
                mel.eval('MGPickerItem -e -vis true selectButton88;')
                mel.eval('MGPickerItem -e -vis true selectButton101;')

                # FK
                mel.eval('MGPickerItem -e -vis false selectButton99;')
                mel.eval('MGPickerItem -e -vis false selectButton94;')
                mel.eval('MGPickerItem -e -vis false selectButton91;')

        ctrls.append(ik_pos_ctrl)
        ctrls.append(ik_rot_ctrl)
        ctrls.append(ikpv_ctrl)

        ctrls.append(ikfk_switch) if force_state_key else False

        return ctrls

    def ikfk_hand_R(self,
                    picker=None,
                    match=None,
                    force_state=None,
                    force_state_key=None):
        ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc = self.ctrl.get_hand_L_ctrl_values()

        ikfk_switch = mirror_character(['_L', '_R'], ikfk_switch)
        ik_pos_ctrl = mirror_character(['_L', '_R'], ik_pos_ctrl)
        ik_rot_ctrl = mirror_character(['_L', '_R'], ik_rot_ctrl)
        ikpv_ctrl = mirror_character(['_L', '_R'], ikpv_ctrl)
        pos_match_loc = mirror_character(['_L', '_R'], pos_match_loc)
        ikpv_match_loc = mirror_character(['_L', '_R'], ikpv_match_loc)

        jnts = [mirror_character(['_L', '_R'], jnt) for jnt in jnts]
        ctrls = [mirror_character(['_L', '_R'], ctrl) for ctrl in ctrls]

        state = cmds.getAttr(ikfk_switch)

        if force_state:
            if force_state == 'ik2fk':
                state = 1
            elif force_state == 'fk2ik':
                state = 0
            cmds.setAttr(ikfk_switch, state)

            cmds.setKeyframe(ikfk_switch) if force_state_key else False

        if state == 1:
            self.ik2fk_match(ctrls=ctrls,
                        jnts=jnts,
                        ikfk_switch=ikfk_switch,
                        match=match)

            if picker:
                # IK
                mel.eval('MGPickerItem -e -vis false selectButton110;')
                mel.eval('MGPickerItem -e -vis false selectButton118;')
                mel.eval('MGPickerItem -e -vis false selectButton102;')

                # FK
                mel.eval('MGPickerItem -e -vis true selectButton115;')
                mel.eval('MGPickerItem -e -vis true selectButton75;')
                mel.eval('MGPickerItem -e -vis true selectButton109;')

        else:
            self.fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                        pos_match_loc=pos_match_loc,
                        ikpv_ctrl=ikpv_ctrl,
                        ikpv_match_loc=ikpv_match_loc,
                        ik_rot_ctrl=ik_rot_ctrl,
                        rot_match_jnt=jnts[2],
                        ikfk_switch=ikfk_switch,
                        match=match,
                        start=jnts[0],
                        mid=jnts[1],
                        end=jnts[2],
                        move=50,
                        loc_match=True)

            if picker:
                # IK
                mel.eval('MGPickerItem -e -vis true selectButton110;')
                mel.eval('MGPickerItem -e -vis true selectButton118;')
                mel.eval('MGPickerItem -e -vis true selectButton102;')

                # FK
                mel.eval('MGPickerItem -e -vis false selectButton115;')
                mel.eval('MGPickerItem -e -vis false selectButton75;')
                mel.eval('MGPickerItem -e -vis false selectButton109;')

        ctrls.append(ik_pos_ctrl)
        ctrls.append(ik_rot_ctrl)
        ctrls.append(ikpv_ctrl)

        ctrls.append(ikfk_switch) if force_state_key else False

        return ctrls

    def ikfk_foot_L(self,
                    picker=None,
                    match=None,
                    force_state=None,
                    force_state_key=None):
        ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc = self.ctrl.get_foot_L_ctrl_values()

        roll_Toe_ctrl = self.ctrl.cur_nss + 'roll_Toe_L_ctrl'

        if force_state:
            if force_state == 'ik2fk':
                state = 1
            elif force_state == 'fk2ik':
                state = 0
            cmds.setAttr(ikfk_switch, state)

            cmds.setKeyframe(ikfk_switch) if force_state_key else False

        if state == 1:
            self.ik2fk_match(ctrls=ctrls,
                        jnts=jnts,
                        ikfk_switch=ikfk_switch,
                        match=match)

            cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

            if picker:
                # IK
                mel.eval('MGPickerItem -e -vis false selectButton87;')
                mel.eval('MGPickerItem -e -vis false selectButton81;')
                mel.eval('MGPickerItem -e -vis false selectButton111;')
                mel.eval('MGPickerItem -e -vis false selectButton258;')

                # FK
                mel.eval('MGPickerItem -e -vis true selectButton107;')
                mel.eval('MGPickerItem -e -vis true selectButton77;')
                mel.eval('MGPickerItem -e -vis true selectButton90;')
                mel.eval('MGPickerItem -e -vis true selectButton98;')

        else:
            self.fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                        pos_match_loc=pos_match_loc,
                        ikpv_ctrl=ikpv_ctrl,
                        ikpv_match_loc=ikpv_match_loc,
                        ik_rot_ctrl=ik_rot_ctrl,
                        rot_match_jnt=jnts[3],
                        ikfk_switch=ikfk_switch,
                        match=match,
                        start=jnts[0],
                        mid=jnts[1],
                        end=jnts[2],
                        move=50,
                        loc_match=True)

            cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

            if picker:
                # IK
                mel.eval('MGPickerItem -e -vis true selectButton87;')
                mel.eval('MGPickerItem -e -vis true selectButton81;')
                mel.eval('MGPickerItem -e -vis true selectButton111;')
                mel.eval('MGPickerItem -e -vis true selectButton258;')

                # FK
                mel.eval('MGPickerItem -e -vis false selectButton107;')
                mel.eval('MGPickerItem -e -vis false selectButton77;')
                mel.eval('MGPickerItem -e -vis false selectButton90;')
                mel.eval('MGPickerItem -e -vis false selectButton98;')

        ctrls.append(ik_pos_ctrl)
        ctrls.append(ik_rot_ctrl)
        ctrls.append(ikpv_ctrl)
        ctrls.append(roll_Toe_ctrl)

        ctrls.append(ikfk_switch) if force_state_key else False

        return ctrls

    def ikfk_foot_R(self,
                    picker=None,
                    match=None,
                    force_state=None,
                    force_state_key=None):
        ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc = self.ctrl.get_foot_L_ctrl_values()

        ikfk_switch = mirror_character(['_L', '_R'], ikfk_switch)
        ik_pos_ctrl = mirror_character(['_L', '_R'], ik_pos_ctrl)
        ik_rot_ctrl = mirror_character(['_L', '_R'], ik_rot_ctrl)
        ikpv_ctrl = mirror_character(['_L', '_R'], ikpv_ctrl)
        pos_match_loc = mirror_character(['_L', '_R'], pos_match_loc)
        ikpv_match_loc = mirror_character(['_L', '_R'], ikpv_match_loc)

        jnts = [mirror_character(['_L', '_R'], jnt) for jnt in jnts]
        ctrls = [mirror_character(['_L', '_R'], ctrl) for ctrl in ctrls]

        state = cmds.getAttr(ikfk_switch)

        roll_Toe_ctrl = self.ctrl.cur_nss + 'roll_Toe_R_ctrl'

        if force_state:
            if force_state == 'ik2fk':
                state = 1
            elif force_state == 'fk2ik':
                state = 0
            cmds.setAttr(ikfk_switch, state)

            cmds.setKeyframe(ikfk_switch) if force_state_key else False

        if state == 1:
            self.ik2fk_match(ctrls=ctrls,
                        jnts=jnts,
                        ikfk_switch=ikfk_switch,
                        match=match)

            cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

            if picker:
                # IK
                mel.eval('MGPickerItem -e -vis false selectButton86;')
                mel.eval('MGPickerItem -e -vis false selectButton93;')
                mel.eval('MGPickerItem -e -vis false selectButton112;')
                mel.eval('MGPickerItem -e -vis false selectButton259;')

                # FK
                mel.eval('MGPickerItem -e -vis true selectButton92;')
                mel.eval('MGPickerItem -e -vis true selectButton114;')
                mel.eval('MGPickerItem -e -vis true selectButton106;')
                mel.eval('MGPickerItem -e -vis true selectButton108;')

        else:
            self.fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                        pos_match_loc=pos_match_loc,
                        ikpv_ctrl=ikpv_ctrl,
                        ikpv_match_loc=ikpv_match_loc,
                        ik_rot_ctrl=ik_rot_ctrl,
                        rot_match_jnt=jnts[3],
                        ikfk_switch=ikfk_switch,
                        match=match,
                        start=jnts[0],
                        mid=jnts[1],
                        end=jnts[2],
                        move=50,
                        loc_match=True)

            cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

            if picker:
                # IK
                mel.eval('MGPickerItem -e -vis true selectButton86;')
                mel.eval('MGPickerItem -e -vis true selectButton93;')
                mel.eval('MGPickerItem -e -vis true selectButton112;')
                mel.eval('MGPickerItem -e -vis true selectButton259;')

                # FK
                mel.eval('MGPickerItem -e -vis false selectButton92;')
                mel.eval('MGPickerItem -e -vis false selectButton114;')
                mel.eval('MGPickerItem -e -vis false selectButton106;')
                mel.eval('MGPickerItem -e -vis false selectButton108;')


        ctrls.append(ik_pos_ctrl)
        ctrls.append(ik_rot_ctrl)
        ctrls.append(ikpv_ctrl)
        ctrls.append(roll_Toe_ctrl)

        ctrls.append(ikfk_switch) if force_state_key else False

        return ctrls

    @bake_with_func
    def ikfk_match_with_bake(self, hand_L=None, hand_L_ikfk=None, hand_R=None, hand_R_ikfk=None,
                             foot_L=None, foot_L_ikfk=None, foot_R=None, foot_R_ikfk=None,
                             force_state_key=None):

        hand_L_ctrls = self.ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key) if hand_L else False
        hand_R_ctrls = self.ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key) if hand_R else False
        foot_L_ctrls = self.ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key) if foot_L else False
        foot_R_ctrls = self.ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key) if foot_R else False

        cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
        cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
        cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
        cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

    @bake_with_func_for_timeSlider
    def ikfk_match_with_bake_for_timeSlider(self, hand_L=None, hand_L_ikfk=None, hand_R=None, hand_R_ikfk=None,
                             foot_L=None, foot_L_ikfk=None, foot_R=None, foot_R_ikfk=None,
                             force_state_key=None):

        hand_L_ctrls = self.ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key) if hand_L else False
        hand_R_ctrls = self.ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key) if hand_R else False
        foot_L_ctrls = self.ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key) if foot_L else False
        foot_R_ctrls = self.ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key) if foot_R else False

        cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
        cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
        cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
        cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

    @bake_with_func_for_timeSlider
    def fk2ik_ik2fk_matchbake(self, force_state_key=None):
        force_state_key=force_state_key

        # fk2ik
        hand_L=True
        hand_L_ikfk='fk2ik'

        hand_R=True
        hand_R_ikfk='fk2ik'

        foot_L=True
        foot_L_ikfk='fk2ik'

        foot_R=True
        foot_R_ikfk='fk2ik'

        hand_L_ctrls = self.ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key) if hand_L else False
        hand_R_ctrls = self.ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key) if hand_R else False
        foot_L_ctrls = self.ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key) if foot_L else False
        foot_R_ctrls = self.ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key) if foot_R else False

        cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
        cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
        cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
        cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

        # ik2fk
        hand_L=True
        hand_L_ikfk='ik2fk'

        hand_R=True
        hand_R_ikfk='ik2fk'

        foot_L=True
        foot_L_ikfk='ik2fk'

        foot_R=True
        foot_R_ikfk='ik2fk'

        hand_L_ctrls = self.ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key) if hand_L else False
        hand_R_ctrls = self.ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key) if hand_R else False
        foot_L_ctrls = self.ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key) if foot_L else False
        foot_R_ctrls = self.ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key) if foot_R else False

        cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
        cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
        cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
        cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

    @bake_with_func_for_timeSlider
    def ik2fk_fk2ik_matchbake(self, force_state_key=None):
        force_state_key=force_state_key

        # ik2fk
        hand_L=True
        hand_L_ikfk='ik2fk'

        hand_R=True
        hand_R_ikfk='ik2fk'

        foot_L=True
        foot_L_ikfk='ik2fk'

        foot_R=True
        foot_R_ikfk='ik2fk'

        hand_L_ctrls = self.ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key) if hand_L else False
        hand_R_ctrls = self.ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key) if hand_R else False
        foot_L_ctrls = self.ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key) if foot_L else False
        foot_R_ctrls = self.ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key) if foot_R else False

        cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
        cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
        cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
        cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

        # fk2ik
        hand_L=True
        hand_L_ikfk='fk2ik'

        hand_R=True
        hand_R_ikfk='fk2ik'

        foot_L=True
        foot_L_ikfk='fk2ik'

        foot_R=True
        foot_R_ikfk='fk2ik'

        hand_L_ctrls = self.ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key) if hand_L else False
        hand_R_ctrls = self.ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key) if hand_R else False
        foot_L_ctrls = self.ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key) if foot_L else False
        foot_R_ctrls = self.ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key) if foot_R else False

        cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
        cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
        cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
        cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

    # hand both fk to ik
    def match_bake(self, parts=None, sides=None, match_type=None):
        """
        parts: ['hand', 'foot']
        sides: ['both'] or ['_L_', '_R_']
        """
        beforeBakeValue, times = get_times_from_bake_before()
        if '_L_' in sides:
            side = '_L_'

        if beforeBakeValue:
            if 'hand' in parts:
                self.anim.before_bakes_hand(side=side, time_range=times)
            if 'foot' in parts:
                self.anim.before_bakes_foot(side=side, time_range=times)

        currentValue = mel.eval('float $at_val = `MGPickerItem -q -atv {}`;'.format(SETKEY_IKFK_BTN))

        hand_L = None
        hand_R = None
        foot_L = None
        foot_R = None

        if 'hand' in parts and '_L_' in sides:
            hand_L = True

        if 'hand' in parts and '_R_' in sides:
            hand_R = True

        if 'foot' in parts and '_L_' in sides:
            foot_L = True

        if 'foot' in parts and '_R_' in sides:
            foot_R = True

        self.ikfk_match_with_bake_for_timeSlider(
            hand_L=hand_L, hand_L_ikfk=match_type,
            hand_R=hand_R, hand_R_ikfk=match_type,
            foot_L=foot_L, foot_L_ikfk=match_type,
            foot_R=foot_R, foot_R_ikfk=match_type,
            force_state_key=currentValue
        )

anim = Animation(prefix=None, suffix='_ctrl')
anim.cog_hip_matchbake(bake_to='hip')

anim.ctrl.all_ctrls

sel = cmds.ls(os=True)
anim.fullbake(sel)

# ctrl.reset_spaces()


# print(ctrl.all_ctrls)

# mel.eval('MGP_GetCurrentPickerNamespace')
