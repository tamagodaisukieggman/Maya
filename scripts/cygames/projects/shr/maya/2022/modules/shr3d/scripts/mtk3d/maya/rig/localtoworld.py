# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

# human
pick_ctrls_00 = [u'calf_L_ik_pv_ctrl',
                 u'calf_R_ik_pv_ctrl',
                 u'foot_L_ik_ctrl',
                 u'foot_R_ik_ctrl',
                 u'hand_L_ikRot_ctrl_ikRot_ctrl',
                 u'hand_L_ik_ctrl',
                 u'hand_R_ikRot_ctrl_ikRot_ctrl',
                 u'hand_R_ik_ctrl',
                 u'main_ctrl',
                 u'move_ctrl',
                 u'pelvis_C_fkRot_ctrl',
                 u'pelvis_C_fk_ctrl',
                 u'spine_C_01_fk_ctrl',
                 u'spine_C_02_fk_ctrl',
                 u'spine_C_03_fk_ctrl',
                 u'upperarm_L_ik_pv_ctrl',
                 u'upperarm_R_ik_pv_ctrl',
                 u'world_ctrl']

# land griffon/ goat/ cow/ great horn/ bear
pick_ctrls_01 = [u'hand_L_01_ctrl',
                 u'hand_R_01_ctrl',
                 u'elbow_R_pv_ctrl',
                 u'elbow_L_pv_ctrl',
                 u'foot_R_01_ctrl',
                 u'foot_L_01_ctrl',
                 u'knee_R_pv_ctrl',
                 u'knee_L_pv_ctrl',
                 u'pelvis_ctrl',
                 u'pelvis_fk_ctrl']

# bird
pick_ctrls_02 = [u'foot_R_02_ctrl',
                 u'foot_L_02_ctrl',
                 u'foot_L_01_pv_ctrl',
                 u'foot_R_01_pv_ctrl']

# wyvern/ sky lizard
pick_ctrls_03 = [u'main_ctrl',
                 u'local_ctrl',
                 u'move_ctrl',
                 u'hand_L_ctrl',
                 u'arm_L_pv_ctrl',
                 u'hand_R_ctrl',
                 u'arm_R_pv_ctrl',
                 u'foot_L_01_ctrl',
                 u'foot_R_01_ctrl',
                 u'knee_R_pv_ctrl',
                 u'knee_L_pv_ctrl',
                 u'pelvis_ctrl',
                 u'pelvis_fk_ctrl']


def get_ctrl_list(*args):
    post_ctrl_list = []
    for i in args:
        post_ctrl_list.extend(i)
    return list(set(post_ctrl_list))


def get_pick_ctrl(namespace="", ctrl_list=[]):
    ctrls = []
    nmsp = namespace
    for obj in ctrl_list:
        if cmds.objExists(nmsp + obj):
            ctrls.append(nmsp + obj)
    return ctrls


def parent_bake_locs(ctrls=None, main_parent=None, world_parent=None, all_world_parent=None, pelvis_children=None,
                     spine_parent=None):
    world_ctrl = ''
    main_ctrl = ''
    pelvis_children_excepts = []
    spines_children = []

    ns = [ctrls[0].split(':')[0] + ":"][0]

    for obj in ctrls:
        if 'local_ctrl' in obj:
            world_ctrl = ns + "main_ctrl_bake_loc"
            main_ctrl = ns + "local_ctrl_bake_loc"

        elif 'world_ctrl' in obj:
            world_ctrl = ns + 'world_ctrl_bake_loc'
            main_ctrl = ns + 'main_ctrl_bake_loc'

        elif 'pelvis_C_fk_ctrl' in obj or 'pelvis_ctrl' in obj:
            pelvis_ctrl = obj

        elif 'pelvis_C_fkRot_ctrl' in obj or 'pelvis_fk_ctrl' in obj:
            pelvis_C_fkRot_ctrl = obj

        elif 'knee_L_pv_ctrl' in obj or 'knee_R_pv_ctrl' in obj \
                or 'foot_L_01_ctrl' in obj or 'foot_R_01_ctrl' in obj \
                or 'move_ctrl' in obj \
                or 'calf_L_ik_pv_ctrl' in obj or 'calf_R_ik_pv_ctrl' in obj \
                or 'foot_L_ik_ctrl' in obj or 'foot_R_ik_ctrl' in obj \
                or 'foot_L_02_ctrl' in obj or 'foot_R_02_ctrl' in obj \
                or 'foot_L_01_pv_ctrl' in obj or 'foot_R_01_pv_ctrl' in obj:
            pelvis_children_excepts.append(obj)

        elif 'hand_L_ik_ctrl' in obj or 'hand_L_01_ctrl' in obj:
            hand_L_ik_ctrl = obj

        elif 'hand_R_ik_ctrl' in obj or 'hand_R_01_ctrl' in obj:
            hand_R_ik_ctrl = obj

        elif 'spine_C_' in obj or 'spine_01_fk_':
            spines_children.append(obj)

        pelvis_children_excepts.append(world_ctrl)
        pelvis_children_excepts.append(main_ctrl)

    for obj in ctrls:
        if main_ctrl in obj:
            if world_parent:
                cmds.parent(main_ctrl, world_ctrl)

        elif not world_ctrl in obj:
            if 'move_ctrl' in obj:
                pass
            else:
                if main_parent:
                    cmds.parent(obj, main_ctrl)
                else:
                    if all_world_parent:
                        cmds.parent(obj, world_ctrl)

    # pelvis children
    if pelvis_children:
        for obj in ctrls:
            if not obj in pelvis_children_excepts:
                try:
                    cmds.parent(obj, pelvis_ctrl)
                except Exception as e:
                    pass

    # ikRot parent
    for obj in ctrls:
        if '_L_ikRot_' in obj:
            cmds.parent(obj, hand_L_ik_ctrl)
        elif '_R_ikRot_' in obj:
            cmds.parent(obj, hand_R_ik_ctrl)

    # pelvis fkRot parent
    try:
        cmds.parent(pelvis_C_fkRot_ctrl, pelvis_ctrl)
    except:
        pass

    # spine_parent
    if spine_parent:
        spines_children.sort()
        spines_children_buf = []
        for spn in spines_children:
            if spines_children_buf == []:
                try:
                    cmds.parent(spn, pelvis_ctrl)
                except:
                    pass
            else:
                try:
                    cmds.parent(spn, spines_children_buf[-1])
                except:
                    pass
            spines_children_buf.append(spn)

    for spn in spines_children[::-1]:
        cmds.reorder(spn, f=1)
    cmds.reorder(pelvis_ctrl, f=1)
    cmds.reorder(main_ctrl, f=1)
    cmds.reorder(world_ctrl, f=1)
    cmds.reorder(pelvis_C_fkRot_ctrl, f=1)


class UI():
    def __init__(self, time_range=False, playbackSlider=False):
        self.MAIN_WINDOW = 'Local to World (Locators)'
        self.time_range = time_range
        self.playbackSlider = playbackSlider

    def show(self):
        if cmds.workspaceControl(self.MAIN_WINDOW, q=1, ex=1):
            cmds.deleteUI(self.MAIN_WINDOW)

        win = cmds.workspaceControl(self.MAIN_WINDOW, l=self.MAIN_WINDOW)

        self.layout()

        cmds.showWindow(win)
        cmds.scriptJob(e=['SceneOpened', self.namespaces_optionMenu], p=win, rp=True)

    def layout(self):

        cmds.columnLayout(adj=1, rs=7)
        cmds.rowLayout(nc=2, adj=1)
        self.namespaces_om = cmds.optionMenu(label='Namespace')
        self.namespaces_optionMenu()
        cmds.button(l='Refresh', c=self.namespaces_optionMenu)
        cmds.setParent('..')
        self.all_world_parent_cb = cmds.checkBox(l=u'world_ctrlのロケータに他のロケータをペアレントさせる', v=1)
        self.main_parent_cb = cmds.checkBox(l=u'main_ctrlのロケータに他のロケータをペアレントさせる')
        self.world_parent_cb = cmds.checkBox(l=u'main_ctrlをworld_ctrlにペアレントさせる')
        self.pelvis_children_cb = cmds.checkBox(l=u'他のコントローラをpelvis_C_fk_ctrlにペアレントさせる(上半身のロケータ群)')

        cmds.button(l=u'Bake!', c=self.doIt, w=400)
        cmds.button(l=u'bake_locs_grpを消す', c=self.delete_bake_locs_grp, w=400)

    def get_namespaces(self, *args, **kwargs):
        return self.get_current_namespaces()

    def namespaces_optionMenu(self, *args, **kwargs):
        itemList = cmds.optionMenu(self.namespaces_om, q=1, ill=1)
        if itemList:
            [cmds.deleteUI(item) for item in itemList or []]
        nss = self.get_namespaces()
        if nss == '':
            cmds.menuItem(label=nss, p=self.namespaces_om)
        else:
            for ns in nss:
                cmds.menuItem(label=ns, p=self.namespaces_om)

    def get_current_namespaces(self, *args, **kwargs):
        exclude_list = ['UI', 'shared']

        current = cmds.namespaceInfo(cur=True)
        cmds.namespace(set=':')
        namespaces = ['{}:'.format(ns) for ns in cmds.namespaceInfo(lon=True) if ns not in exclude_list]
        cmds.namespace(set=current)

        # Reference Nodes
        rn = cmds.ls(type="reference", r=1)
        for i in rn:
            ref_ns = i.split("RN")
            ns = '{0}:'.format(ref_ns[0])
            if not ns in namespaces:
                namespaces.append(ns)

        if namespaces == []:
            namespaces = ''

        return namespaces

    def delete_bake_locs_grp(self, *args, **kwargs):
        if cmds.objExists('bake_locs_grp'):
            cmds.lockNode('bake_locs_grp', l=0)
            cmds.delete('bake_locs_grp')

    def doIt(self, *args, **kwargs):
        def rot_skippy(obj):
            flags = {}
            axis = ['x', 'y', 'z']
            attr = cmds.listAttr(obj, k=1, sn=1)
            for at in attr:
                if 'rx' in at:
                    axis.remove('x')
                if 'ry' in at:
                    axis.remove('y')
                if 'rz' in at:
                    axis.remove('z')
            flags['skip'] = axis
            return flags

        def trans_skippy(obj):
            flags = {}
            axis = ['x', 'y', 'z']
            attr = cmds.listAttr(obj, k=1, sn=1)
            for at in attr:
                if 'tx' in at:
                    axis.remove('x')
                if 'ty' in at:
                    axis.remove('y')
                if 'tz' in at:
                    axis.remove('z')
            flags['skip'] = axis
            return flags

        # set time range
        time_range = self.time_range
        playbackSlider = self.playbackSlider

        # check and save current autokey state
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = 1
        else:
            autoKeyState = 0

        cmds.autoKeyframe(st=0)

        if not time_range:
            playmin = cmds.playbackOptions(q=1, min=1)
            playmax = cmds.playbackOptions(q=1, max=1)

        else:
            playmin = time_range[0]
            playmax = time_range[1]

        start = playmin
        end = playmax

        # check to see if time range is highlighted
        if playbackSlider:
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
                frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
                start = frameRange[0]
                end = frameRange[1] - 1
            else:
                frameRange = cmds.currentTime(q=1)
                start = frameRange
                end = frameRange - 1

        # bookend and key pinner plus all controls in range
        setkey_attrs = mel.eval(
            'string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
        if setkey_attrs == []:
            setkey_attrs = [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

        # get all_controllers
        pre_ctrls = get_ctrl_list(pick_ctrls_00, pick_ctrls_01, pick_ctrls_02, pick_ctrls_03)
        self.ns = cmds.optionMenu(self.namespaces_om, q=1, v=1)
        # get pick_ctrls
        pick_ctrls = get_pick_ctrl(self.ns, pre_ctrls)
        pick_ctrls.sort()

        if not pick_ctrls:
            # selection
            sel = cmds.ls(os=1)
            if not sel:
                cmds.warning(u'コントローラを選択してください。')
                return
        else:
            # self.ns = cmds.optionMenu(self.namespaces_om, q=1, v=1)
            # sel = ['{0}{1}'.format(self.ns, obj) for obj in pick_ctrls]
            sel = pick_ctrls

        # bake_locs_grp
        self.delete_bake_locs_grp()
        bake_locs_grp = 'bake_locs_grp'
        if not cmds.objExists(bake_locs_grp):
            cmds.createNode('transform', n=bake_locs_grp, ss=1)

        cmds.lockNode(bake_locs_grp, l=1)

        bake_locs = [cmds.spaceLocator(n='{0}_bake_loc'.format(obj))[0] for obj in sel if
                     not cmds.objExists('{0}_bake_loc'.format(obj))]
        bake_locs.sort()
        children = cmds.listRelatives(bake_locs_grp, c=1)
        for obj in bake_locs:
            if not children or not obj in children:
                cmds.parent(obj, bake_locs_grp)

        pacons = [cmds.parentConstraint(obj, '{0}_bake_loc'.format(obj))[0] for obj in sel]

        main_parent = cmds.checkBox(self.main_parent_cb, q=1, v=1)
        world_parent = cmds.checkBox(self.world_parent_cb, q=1, v=1)
        all_world_parent = cmds.checkBox(self.all_world_parent_cb, q=1, v=1)
        pelvis_children = cmds.checkBox(self.pelvis_children_cb, q=1, v=1)

        parent_bake_locs(ctrls=bake_locs, main_parent=main_parent, world_parent=world_parent,
                         all_world_parent=all_world_parent, pelvis_children=pelvis_children, spine_parent=False)

        cmds.bakeResults(bake_locs,
                         sparseAnimCurveBake=False,
                         minimizeRotation=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         oversamplingRate=1,
                         bakeOnOverrideLayer=False,
                         preserveOutsideKeys=True,
                         simulation=True,
                         sampleBy=1,
                         t=(start, end),
                         disableImplicitControl=True,
                         at=setkey_attrs)

        cmds.delete(pacons)

        for obj in sel:
            tr_skips = trans_skippy(obj)
            ro_skips = rot_skippy(obj)
            if not tr_skips == []:
                cmds.pointConstraint('{0}_bake_loc'.format(obj), obj, **tr_skips)
            if not ro_skips == []:
                cmds.orientConstraint('{0}_bake_loc'.format(obj), obj, **ro_skips)

        if not cmds.objExists('bake_locs_sets'):
            cmds.sets(em=1, n='bake_locs_sets')

        for obj in sel:
            cmds.sets('{0}_bake_loc'.format(obj), add='bake_locs_sets')

        cmds.autoKeyframe(e=1, st=autoKeyState)


if __name__ == '__main__':
    ui = UI()
    ui.show()
