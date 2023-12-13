from maya import cmds, mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2

from collections import OrderedDict
import functools
import math
import re
import traceback

class UI(object):
    def __init__(self):
        self.MAIN_WINDOW = 'Refresh Tool'

    def show(self):
        if cmds.workspaceControl(self.MAIN_WINDOW, q=1, ex=1):
            cmds.deleteUI(self.MAIN_WINDOW)

        self.win = cmds.workspaceControl(self.MAIN_WINDOW, l=self.MAIN_WINDOW, rt=1)

        self.layout()

        cmds.showWindow(self.win)

        cmds.scriptJob(e=['SceneOpened', self.add_items_in_namespace_menu], p=self.win, rp=1)


    def layout(self):
        self.row_lay_common_settings = {'cw2':(80, 100),
                                   'cl2':['center', 'left'],
                                   'ct2':['right', 'left'],
                                   'h':24}

        self.frm_lay_common_settings = {'cll':1}

        menuBarLayout = cmds.menuBarLayout(p=self.win)
        cmds.menu(label='Maya Menu')
        cmds.menuItem(label='Optimize Scene', c='mel.eval("OptimizeSceneOptions;")')

        # cmds.menuItem(label='Save Settings', c=self.save_settings)
        # cmds.menuItem(label='Reset Settings', c=self.reset_settings)
        # cmds.menuItem(label='Reload Settings', c=self.load_settings)
        # cmds.menuItem(d=1)
        # cmds.menuItem(label='Reload', c=self.all_reload)
        # cmds.menuItem(label='ReferenceEditor', c='cmds.ReferenceEditor()')

        self.scl_lay = cmds.scrollLayout(p=self.MAIN_WINDOW, cr=1)

        self.nss_ops_menu = cmds.optionMenu(l='NameSpace')
        self.add_items_in_namespace_menu()

        self.plot_lay(self.scl_lay)
        self.del_animLayers_lay(self.scl_lay)
        self.run_all_lay(self.scl_lay)

        cmds.setParent('..')


    def list_namespaces(self):
        exclude_list = ['UI', 'shared']

        current = cmds.namespaceInfo(cur=1)
        cmds.namespace(set=':')
        namespaces = ['{}'.format(ns) for ns in cmds.namespaceInfo(lon=1) if ns not in exclude_list]
        cmds.namespace(set=current)

        return namespaces

    def load_menuItems(self, array=None, parent=None):
        for item in array:
            cmds.menuItem(l=item, p=parent)

    def add_items_in_namespace_menu(self):
        namespaces = self.list_namespaces()
        cmds.optionMenu(self.nss_ops_menu, e=1, dai=1)
        cmds.menuItem(l='', p=self.nss_ops_menu)
        self.load_menuItems(array=namespaces, parent=self.nss_ops_menu)

    def change_managed(self, *args, **kwargs):
        print(args, kwargs)

    # Plot
    def plot_lay(self, parent=None):
        # correct
        # self.cor_mch_frm_lay = cmds.frameLayout(p=parent, l='Correct Match', **self.frm_lay_common_settings)

        cmds.separator(p=parent, st='in')
        self.cor_mch_all_cb = cmds.checkBox(l='Correct Match', v=1, p=parent)
        self.cor_mch_row = cmds.rowLayout(adj=5, p=parent, nc=6, **self.row_lay_common_settings)

        self.l_hand_cor_mch_cb = cmds.checkBox(l='Left Hand', v=1, p=self.cor_mch_row)
        self.r_hand_cor_mch_cb = cmds.checkBox(l='Right Hand', v=1, p=self.cor_mch_row)
        self.l_foot_cor_mch_cb = cmds.checkBox(l='Left Foot', v=1, p=self.cor_mch_row)
        self.r_foot_cor_mch_cb = cmds.checkBox(l='Right Foot', v=1, p=self.cor_mch_row)
        cmds.button(l='Done!', c=self.cor_mch_main)


    def cor_mch_main(self, *args):
        namespace = cmds.optionMenu(self.nss_ops_menu, q=1, v=1)
        if not namespace:
            namespace = ''
        elif not namespace.endswith(':'):
            namespace = namespace + ':'

        self.l_hand_cor_mch_val = cmds.checkBox(self.l_hand_cor_mch_cb, q=1, v=1)
        self.r_hand_cor_mch_val = cmds.checkBox(self.r_hand_cor_mch_cb, q=1, v=1)
        self.l_foot_cor_mch_val = cmds.checkBox(self.l_foot_cor_mch_cb, q=1, v=1)
        self.r_foot_cor_mch_val = cmds.checkBox(self.r_foot_cor_mch_cb, q=1, v=1)

        try:
            refresh_tool_correctMatch(namespace=namespace,
                              l_hand=self.l_hand_cor_mch_val,
                              r_hand=self.r_hand_cor_mch_val,
                              l_foot=self.l_foot_cor_mch_val,
                              r_foot=self.r_foot_cor_mch_val)
        except:
            print(traceback.format_exc())


    # Delete AnimationLayers
    def del_animLayers_lay(self, parent=None):
        # correct
        # self.dal_frm_lay = cmds.frameLayout(p=parent, l='Delete AnimLayers', **self.frm_lay_common_settings)

        cmds.separator(p=parent, st='in')
        self.dal_all_cb = cmds.checkBox(l='Delete AnimLayers', v=1, p=parent)
        self.dal_row = cmds.rowLayout(adj=3, p=parent, nc=6, **self.row_lay_common_settings)

        self.dal_cb = cmds.checkBox(l='Exclude BaseAnimation', v=1, p=self.dal_row)
        self.dar_cb = cmds.checkBox(l='Rename animCurves', v=1, p=self.dal_row)
        cmds.button(l='Done!', c=self.del_animLayers_main)


    def del_animLayers_main(self, *args):
        self.dal_cb_val = cmds.checkBox(self.dal_cb, q=1, v=1)
        self.dar_cb_val = cmds.checkBox(self.dar_cb, q=1, v=1)
        try:
            refresh_tool_delete_all_animLayers(exclude_baseAnimation=self.dal_cb_val, rename_animCurves=self.dar_cb_val)
        except:
            print(traceback.format_exc())


    # Run All
    def run_all_lay(self, parent=None):
        cmds.separator(p=parent, st='in')

        self.check_all_row = cmds.rowLayout(adj=2, p=parent, nc=6, **self.row_lay_common_settings)
        self.check_all_cb = cmds.checkBox(l='All Check', v=1, p=self.check_all_row, cc=self.all_check)
        cmds.button(l='Run All!', p=self.check_all_row, c=self.run_all)


    def all_check(self, args):
        cmds.checkBox(self.cor_mch_all_cb, e=1, v=args)
        cmds.checkBox(self.dal_all_cb, e=1, v=args)


    def run_all(self, *args):
        self.cor_mch_all_cb_val = cmds.checkBox(self.cor_mch_all_cb, q=1, v=1)
        if self.cor_mch_all_cb_val:
            self.cor_mch_main()

        self.dal_all_cb_val = cmds.checkBox(self.dal_all_cb, q=1, v=1)
        if self.dal_all_cb_val:
            self.del_animLayers_main()


if __name__ == '__main__':
    ui = UI()
    ui.show()



def get_trs_attrs(obj=None, local=None, pos=True, rot=True, scl=True, roo=True):
    """
    return translate, rotate, scale, rotateOrder, jointOrient
    """
    if not obj:
        sel = cmds.ls(os=1)
        if sel:
            obj = sel[0]
        else:
            return

    rel = 0
    wld = 1

    get_t = None
    get_ro = None
    get_s = None
    get_roo = None
    get_jo = None

    if local:
        rel = 1
        wld = 0

    if pos:
        get_t = cmds.xform(obj, q=1, t=1, ws=wld, os=rel)
    if rot:
        get_ro = cmds.xform(obj, q=1, ro=1, ws=wld, os=rel)
    if scl:
        get_s = cmds.xform(obj, q=1, s=1, ws=wld, os=rel)
    if roo:
        get_roo = cmds.xform(obj, q=1, roo=1)

    if cmds.objectType(obj) == 'joint':
        get_jo = cmds.getAttr(obj+'.jo')
        get_jo = get_jo[0]
        # cmds.setAttr(sel[0]+'.jo', *get_jo[0])

    return get_t, get_ro, get_s, get_roo, get_jo


def get_pole_vec(start=None, mid=None, end=None, move=None):
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

    pv_val = get_trs_attrs(obj=pvLoc[0])

    cmds.delete(pvLoc)
    cmds.select(cl=True)

    return pv_val


def refresh_tool_correctMatch(namespace=None, l_hand=None, r_hand=None, l_foot=None, r_foot=None):
    ##################
    # ik components
    ##################
    # ik_l_hand
    ik_l_hand_src_array = [namespace + 'proxy_armL_jnt',
     namespace + 'proxy_forearmL_jnt',
     namespace + 'proxy_handL_jnt',
     namespace + 'handL_match_loc',
     namespace + 'proxy_handL_jnt']

    ik_l_hand_dst_array = [namespace + 'handL_ctl',
     namespace + 'forearmL_ctl',
     namespace + 'handL_rot_ctl']

    ik_l_hand_ikfk_switch = namespace + 'handL_ikfk_ctl'


    # ik_r_hand
    ik_r_hand_src_array = [namespace + 'proxy_armR_jnt',
     namespace + 'proxy_forearmR_jnt',
     namespace + 'proxy_handR_jnt',
     namespace + 'handR_match_loc',
     namespace + 'proxy_handR_jnt']

    ik_r_hand_dst_array = [namespace + 'handR_ctl',
     namespace + 'forearmR_ctl',
     namespace + 'handR_rot_ctl']

    ik_r_hand_ikfk_switch = namespace + 'handR_ikfk_ctl'


    # ik_l_foot
    ik_l_foot_src_array = [namespace + 'proxy_uplegL_jnt',
     namespace + 'proxy_legL_jnt',
     namespace + 'proxy_footL_jnt',
     namespace + 'footL_match_loc',
     namespace + 'proxy_toebaseL_jnt']

    ik_l_foot_dst_array = [namespace + 'footL_ctl',
     namespace + 'legL_ctl',
     namespace + 'toebaseL_ctl']

    ik_l_foot_ikfk_switch = namespace + 'footL_ikfk_ctl'


    # ik_r_foot
    ik_r_foot_src_array = [namespace + 'proxy_uplegR_jnt',
     namespace + 'proxy_legR_jnt',
     namespace + 'proxy_footR_jnt',
     namespace + 'footR_match_loc',
     namespace + 'proxy_toebaseR_jnt']

    ik_r_foot_dst_array = [namespace + 'footR_ctl',
     namespace + 'legR_ctl',
     namespace + 'toebaseR_ctl']

    ik_r_foot_ikfk_switch = namespace + 'footR_ikfk_ctl'


    ##################
    # fk components
    ##################
    # ik_l_hand
    fk_l_hand_src_array = [namespace + 'proxy_armL_jnt',
     namespace + 'proxy_forearmL_jnt',
     namespace + 'proxy_handL_jnt']

    fk_l_hand_dst_array = [namespace + 'fk_armL_ctl',
     namespace + 'fk_forearmL_ctl',
     namespace + 'fk_handL_ctl']

    # ik_r_hand
    fk_r_hand_src_array = [namespace + 'proxy_armR_jnt',
     namespace + 'proxy_forearmR_jnt',
     namespace + 'proxy_handR_jnt']

    fk_r_hand_dst_array = [namespace + 'fk_armR_ctl',
     namespace + 'fk_forearmR_ctl',
     namespace + 'fk_handR_ctl']

    # ik_l_foot
    fk_l_foot_src_array = [namespace + 'proxy_uplegL_jnt',
     namespace + 'proxy_legL_jnt',
     namespace + 'proxy_footL_jnt',
     namespace + 'proxy_toebaseL_jnt']

    fk_l_foot_dst_array = [namespace + 'fk_uplegL_ctl',
     namespace + 'fk_legL_ctl',
     namespace + 'fk_footL_ctl',
     namespace + 'fk_toebaseL_ctl']

    # ik_r_foot
    fk_r_foot_src_array = [namespace + 'proxy_uplegR_jnt',
     namespace + 'proxy_legR_jnt',
     namespace + 'proxy_footR_jnt',
     namespace + 'proxy_toebaseR_jnt']

    fk_r_foot_dst_array = [namespace + 'fk_uplegR_ctl',
     namespace + 'fk_legR_ctl',
     namespace + 'fk_footR_ctl',
     namespace + 'fk_toebaseR_ctl']

    correct_flips = [namespace + 'proxy_handL_jnt',
                     namespace + 'proxy_handR_jnt']

    def refresh_func(start=None, end=None, match_type=None):
        """
        match_type = 'l_hand'
        match_type = 'r_hand'
        match_type = 'l_foot'
        match_type = 'r_foot'
        """

        if match_type == 'l_hand':
            src_array = ik_l_hand_src_array
            dst_array = ik_l_hand_dst_array
            ikfk_switch = ik_l_hand_ikfk_switch
            fk_src_array = fk_l_hand_src_array
            fk_dst_array = fk_l_hand_dst_array

        if match_type == 'r_hand':
            src_array = ik_r_hand_src_array
            dst_array = ik_r_hand_dst_array
            ikfk_switch = ik_r_hand_ikfk_switch
            fk_src_array = fk_r_hand_src_array
            fk_dst_array = fk_r_hand_dst_array

        elif match_type == 'l_foot':
            src_array = ik_l_foot_src_array
            dst_array = ik_l_foot_dst_array
            ikfk_switch = ik_l_foot_ikfk_switch
            fk_src_array = fk_l_foot_src_array
            fk_dst_array = fk_l_foot_dst_array

        elif match_type == 'r_foot':
            src_array = ik_r_foot_src_array
            dst_array = ik_r_foot_dst_array
            ikfk_switch = ik_r_foot_ikfk_switch
            fk_src_array = fk_r_foot_src_array
            fk_dst_array = fk_r_foot_dst_array


        setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
        if setkey_attrs == []:
            setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

        # ik match
        save_items = OrderedDict()
        for i in range (int(start), int(end+1)):
            cmds.currentTime(i, e=True)
            values = OrderedDict()
            # IK trs
            values[dst_array[0]] = get_trs_attrs(obj=src_array[3])

            # Pole Vec
            values[dst_array[1]] = get_pole_vec(start=get_trs_attrs(obj=src_array[0])[0],
                                        mid=get_trs_attrs(obj=src_array[1])[0],
                                        end=get_trs_attrs(obj=src_array[2])[0],
                                        move=20)

            # IK rot
            get_roo = cmds.xform(src_array[4], q=1, roo=1)
            if src_array[4] in correct_flips:
                cmds.xform(src_array[4], p=1, roo='xyz')

            values[dst_array[2]] = get_trs_attrs(obj=src_array[4])

            if src_array[4] in correct_flips:
                cmds.xform(src_array[4], p=0, roo=get_roo)

            save_items[str(i)] = values


        for frame, obj_array in save_items.items():
            # print(frame, obj_array)
            for obj, value in obj_array.items():
                # print(obj, value)

                # print(obj, value)
                cmds.currentTime(float(frame), e=True)
                cmds.xform(obj, t=value[0], ro=value[1], a=1, ws=1)
                cmds.setKeyframe(obj, at=setkey_attrs)

                cmds.setAttr(ikfk_switch+'.ikfk', 1.0)
                cmds.setKeyframe(ikfk_switch, at=['ikfk'])


        # fk match
        save_items = OrderedDict()
        for i in range (int(start), int(end+1)):
            cmds.currentTime(i, e=True)
            values = OrderedDict()
            for j, (fk_dst, fk_src) in enumerate(zip(fk_dst_array, fk_src_array)):

                get_roo = cmds.xform(fk_src, q=1, roo=1)
                if fk_src in correct_flips:
                    cmds.xform(fk_src, p=1, roo='xyz')

                values[fk_dst] = get_trs_attrs(obj=fk_src)

                if fk_src in correct_flips:
                    cmds.xform(fk_src, p=0, roo=get_roo)

            save_items[str(i)] = values


        for frame, obj_array in save_items.items():
            for obj, value in obj_array.items():
                cmds.currentTime(float(frame), e=True)
                cmds.xform(obj, t=value[0], ro=value[1], a=1, ws=1)
                cmds.setKeyframe(obj, at=setkey_attrs)

        filter_ctrls = dst_array + fk_dst_array
        cmds.filterCurve(filter_ctrls, f='euler')

    ##############################
    cur_time=cmds.currentTime(q=1)

    if cmds.autoKeyframe(q=True, st=True):
        autoKeyState = 1
    else:
        autoKeyState = 0

    cmds.autoKeyframe(st=0)

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

    try:
        cmds.undoInfo(ock=1)
        cmds.refresh(su=1)

        if l_hand:
            refresh_func(start=start, end=end, match_type='l_hand')
        if r_hand:
            refresh_func(start=start, end=end, match_type='r_hand')
        if l_foot:
            refresh_func(start=start, end=end, match_type='l_foot')
        if r_foot:
            refresh_func(start=start, end=end, match_type='r_foot')

        cmds.refresh(su=0)
        cmds.undoInfo(cck=1)

    except Exception as e:
        cmds.refresh(su=0)

        print(traceback.format_exc())

    cmds.autoKeyframe(state=autoKeyState)

    cmds.currentTime(cur_time)


def refresh_tool_delete_all_animLayers(exclude_baseAnimation=None, rename_animCurves=None):
    mel.eval('source "C:/Program Files/Autodesk/Maya{}/scripts/others/performAnimLayerMerge.mel"'.format(cmds.about(version=True)))

    deleteMerged = True
    if cmds.optionVar(exists='animLayerMergeDeleteLayers'):
        deleteMerged = cmds.optionVar(query='animLayerMergeDeleteLayers')

    cmds.optionVar(intValue=('animLayerMergeDeleteLayers', 1))

    animLayers = cmds.ls(type='animLayer')
    if animLayers:
        mel.eval('animLayerMerge {"%s"}' % '","'.join(animLayers))

        if exclude_baseAnimation:
            if 'BaseAnimation' in animLayers:
                animLayers.remove('BaseAnimation')

        [cmds.delete(anl) for anl in animLayers if cmds.objExists(anl)]

    if rename_animCurves:
        def custom_rename(obj=None, rplname=None):
            if cmds.objExists(obj):
                cmds.rename(obj, rplname)

        animCurves = cmds.ls(type=['animCurveTL', 'animCurveTA', 'animCurveTU'])
        not_connects = []
        error_crvs = []
        for ancv in animCurves:
            connected_plug = cmds.listConnections(ancv, d=1, p=1, scn=1) or None
            if not connected_plug:
                not_connects.append(ancv)

            else:
                spl_connected_plugs = re.split('[:\[\].]', connected_plug[0].split(':')[-1])
                spl_connected_plugs_remove_empty = [cprm for cprm in spl_connected_plugs if not cprm == '']
                spl_connected_plug = '_'.join(spl_connected_plugs_remove_empty)
                custom_rename(ancv, spl_connected_plug)
