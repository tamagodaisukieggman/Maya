from maya import cmds, mel

def bake(fk_handL_jnts, fk_handL_ctrls, ik_handL_ctrls, ik_handL_matches, handL_match, handL_match_state, handL_ikfk_ctrl,
         fk_handR_jnts, fk_handR_ctrls, ik_handR_ctrls, ik_handR_matches, handR_match, handR_match_state, handR_ikfk_ctrl,
         fk_footL_jnts, fk_footL_ctrls, ik_footL_ctrls, ik_footL_matches, footL_match, footL_match_state, footL_ikfk_ctrl,
         fk_footR_jnts, fk_footR_ctrls, ik_footR_ctrls, ik_footR_matches, footR_match, footR_match_state, footR_ikfk_ctrl,
         fk_spine_ctrls, ik_spine_match_locs, spine_match,
         footrollL_ctl_pos_loc, footroll_footL_ctl, footroll_toebaseL_ctl, footrollR_ctl_pos_loc, footroll_footR_ctl, footroll_toebaseR_ctl, footlockL_loc, footlockR_loc, toelockL_loc, toelockR_loc, reverseFoot_match):
    cur_time=cmds.currentTime(q=1)
    if cmds.autoKeyframe(q=True, st=True):
        autoKeyState = 1
    else:
        autoKeyState = 0

    cmds.autoKeyframe(st=0)

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

    if playmax < end:
        end = playmax

    setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
    if setkey_attrs == []:
        setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

    for i in range (int(start), int(end+1)):
        cmds.currentTime(i, e=True)
        # handL
        if handL_match:
            if handL_match_state == 0:
                cmds.setAttr(handL_ikfk_ctrl+'.ikfk', 1)
                ik2fk(fk_handL_jnts, fk_handL_ctrls)
                cmds.setAttr(handL_ikfk_ctrl+'.ikfk', 0)
                cmds.setKeyframe(handL_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(fk_handL_ctrls, at=setkey_attrs)
            elif handL_match_state == 1:
                cmds.setAttr(handL_ikfk_ctrl+'.ikfk', 0)
                fk2ik(ik_handL_ctrls, ik_handL_matches, False)
                cmds.setAttr(handL_ikfk_ctrl+'.ikfk', 1)
                cmds.setKeyframe(handL_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(ik_handL_ctrls, at=setkey_attrs)

        # handR
        if handR_match:
            if handR_match_state == 0:
                cmds.setAttr(handR_ikfk_ctrl+'.ikfk', 1)
                ik2fk(fk_handR_jnts, fk_handR_ctrls)
                cmds.setAttr(handR_ikfk_ctrl+'.ikfk', 0)
                cmds.setKeyframe(handR_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(fk_handR_ctrls, at=setkey_attrs)
            elif handR_match_state == 1:
                cmds.setAttr(handR_ikfk_ctrl+'.ikfk', 0)
                fk2ik(ik_handR_ctrls, ik_handR_matches, False)
                cmds.setAttr(handR_ikfk_ctrl+'.ikfk', 1)
                cmds.setKeyframe(handR_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(ik_handR_ctrls, at=setkey_attrs)

        # footL
        if footL_match:
            if footL_match_state == 0:
                cmds.setAttr(footL_ikfk_ctrl+'.ikfk', 1)
                ik2fk(fk_footL_jnts, fk_footL_ctrls)
                cmds.setAttr(footL_ikfk_ctrl+'.ikfk', 0)
                cmds.setKeyframe(footL_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(fk_footL_ctrls, at=setkey_attrs)
            elif footL_match_state == 1:
                cmds.setAttr(footL_ikfk_ctrl+'.ikfk', 0)
                fk2ik(ik_footL_ctrls, ik_footL_matches, True)
                cmds.setAttr(footL_ikfk_ctrl+'.ikfk', 1)
                cmds.setKeyframe(footL_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(ik_footL_ctrls, at=setkey_attrs)

        # footR
        if footR_match:
            if footR_match_state == 0:
                cmds.setAttr(footR_ikfk_ctrl+'.ikfk', 1)
                ik2fk(fk_footR_jnts, fk_footR_ctrls)
                cmds.setAttr(footR_ikfk_ctrl+'.ikfk', 0)
                cmds.setKeyframe(footR_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(fk_footR_ctrls, at=setkey_attrs)
            elif footR_match_state == 1:
                cmds.setAttr(footR_ikfk_ctrl+'.ikfk', 0)
                fk2ik(ik_footR_ctrls, ik_footR_matches, True)
                cmds.setAttr(footR_ikfk_ctrl+'.ikfk', 1)
                cmds.setKeyframe(footR_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(ik_footR_ctrls, at=setkey_attrs)

        # spines
        if spine_match:
            ik2fk_spines(fk_spine_ctrls, ik_spine_match_locs)
            cmds.setKeyframe(ik_spine_match_locs, at=setkey_attrs)

        # reverseFoot
        if reverseFoot_match:
            cmds.matchTransform(footrollL_ctl_pos_loc, footroll_footL_ctl, pos=1, rot=1, scl=0)
            cmds.matchTransform(footlockL_loc, footroll_footL_ctl, pos=1, rot=1, scl=0)
            cmds.matchTransform(toelockL_loc, footroll_toebaseL_ctl, pos=1, rot=1, scl=0)

            cmds.matchTransform(footrollR_ctl_pos_loc, footroll_footR_ctl, pos=1, rot=1, scl=0)
            cmds.matchTransform(footlockR_loc, footroll_footR_ctl, pos=1, rot=1, scl=0)
            cmds.matchTransform(toelockR_loc, footroll_toebaseR_ctl, pos=1, rot=1, scl=0)

            cmds.setKeyframe([footrollL_ctl_pos_loc, footrollR_ctl_pos_loc], at=setkey_attrs)

            # cmds.setKeyframe([footrollL_ctl_pos_loc, footrollR_ctl_pos_loc,
            #                   footlockL_loc, footlockR_loc,
            #                   toelockL_loc, toelockR_loc], at=setkey_attrs)


    cmds.currentTime(cur_time)
    cmds.autoKeyframe(state=autoKeyState)


def ik2fk(jnts, ctrls):
    for i, jt in enumerate(jnts):
        cmds.matchTransform(ctrls[i], jt, rot=1, pos=0, scl=0)

def ik2fk_spines(ctrls, locs):
    for i, ctrl in enumerate(ctrls):
        cmds.matchTransform(locs[i], ctrl, rot=1, pos=1, scl=0)

def ik2fk_spines_matchConstraints(ik_spine_ctrls, ik_spine_pos_ctrl, fk_spine_ctrls):
    spines_ikfk_constraints_sets = 'spines_ikfk_constraints_sets'
    if not cmds.objExists(spines_ikfk_constraints_sets):
        cmds.sets(em=1, n=spines_ikfk_constraints_sets)

    for i, (ik_s_ctrl, fk_s_ctrl) in enumerate(zip(ik_spine_ctrls, fk_spine_ctrls)):
        ori = cmds.orientConstraint(ik_s_ctrl, fk_s_ctrl, w=1, mo=1)
        cmds.sets(ori[0], add=spines_ikfk_constraints_sets)

    po = cmds.pointConstraint(fk_spine_ctrls[0], ik_spine_pos_ctrl, w=1, mo=1)
    cmds.sets(po[0], add=spines_ikfk_constraints_sets)


# const
def reverseFoot_matchConstraints(footroll_footL_ctl, footroll_toebaseL_ctl, footroll_footR_ctl, footroll_toebaseR_ctl, footlockL_loc, footlockR_loc, toelockL_loc, toelockR_loc):
    reverseFoot_constraints_sets = 'reverseFoot_constraints_sets'
    if not cmds.objExists(reverseFoot_constraints_sets):
        cmds.sets(em=1, n=reverseFoot_constraints_sets)

    # left
    ori = cmds.orientConstraint(footlockL_loc, footroll_footL_ctl, w=1, mo=1)
    cmds.sets(ori[0], add=reverseFoot_constraints_sets)

    po = cmds.pointConstraint(footlockL_loc, footroll_footL_ctl, w=1, mo=1)
    cmds.sets(po[0], add=reverseFoot_constraints_sets)

    ori = cmds.orientConstraint(toelockL_loc, footroll_toebaseL_ctl, w=1, mo=1)
    cmds.sets(ori[0], add=reverseFoot_constraints_sets)

    # right
    ori = cmds.orientConstraint(footlockR_loc, footroll_footR_ctl, w=1, mo=1)
    cmds.sets(ori[0], add=reverseFoot_constraints_sets)

    po = cmds.pointConstraint(footlockR_loc, footroll_footR_ctl, w=1, mo=1)
    cmds.sets(po[0], add=reverseFoot_constraints_sets)

    ori = cmds.orientConstraint(toelockR_loc, footroll_toebaseR_ctl, w=1, mo=1)
    cmds.sets(ori[0], add=reverseFoot_constraints_sets)


def root_matchConstraints(root_pos_ctl_loc, root_ctl, root_pos_ctl, cog_root_state):
    root_match_constraints_sets = 'root_match_constraints_sets'
    if not cmds.objExists(root_match_constraints_sets):
        cmds.sets(em=1, n=root_match_constraints_sets)

    if cog_root_state == 0:
        pa = cmds.parentConstraint(root_pos_ctl_loc, root_pos_ctl, w=1)
        cmds.sets(pa[0], add=root_match_constraints_sets)



def fk2ik(ctrls, matches, foot):
    cmds.matchTransform(ctrls[0], matches[0], rot=0, pos=1, scl=0)
    if foot:
        cmds.matchTransform(ctrls[0], matches[0], rot=1, pos=0, scl=0)
    cmds.matchTransform(ctrls[1], matches[1], rot=1, pos=0, scl=0)
    cmds.matchTransform(ctrls[2], matches[2], rot=0, pos=1, scl=0)


def matchbake(handL_ikfk_state=False, handR_ikfk_state=False, handL_fk_ik=0, handR_fk_ik=0,
              footL_ikfk_state=False, footR_ikfk_state=False, footL_fk_ik=0, footR_fk_ik=0,
              spine_ikfk_state=False,
              reverseFoot_state=False,
              cog_root_state=False, cog_root=0):

    """
    handL_ikfk_state=False, handR_ikfk_state=False, handL_fk_ik=fk:0,ik:1, handR_fk_ik=fk:0,ik:1,
    footL_ikfk_state=False, footR_ikfk_state=False, footL_fk_ik=fk:0,ik:1, footR_fk_ik=fk:0,ik:1,
    spine_ikfk_state=False,
    reverseFoot_state=False
    """

    #get the namespace of current picker file.
    # try:
    #     currentPickerNamespace = mel.eval('MGP_GetCurrentPickerNamespace')

    #     if currentPickerNamespace:
    #         currentPickerNamespace = currentPickerNamespace + ':'
    #     else:
    #         currentPickerNamespace = ''

    # except Exception as e:
    sel = cmds.ls(os=1)
    if ':' in sel[0]:
        spl_names = sel[0].split(':')
        currentPickerNamespace = ':'.join(spl_names[:-1:]) + ':'
    else:
        currentPickerNamespace = ''


    ##################
    # HandL
    ##################

    ikfk_handL_switch_ctrl = currentPickerNamespace+'handL_ikfk_ctl'

    # IK to FK
    fk_handL_jnts = [currentPickerNamespace+'proxy_armL_jnt',
            currentPickerNamespace+'proxy_forearmL_jnt',
            currentPickerNamespace+'proxy_handL_jnt']

    fk_handL_ctrls = [currentPickerNamespace+'fk_armL_ctl',
             currentPickerNamespace+'fk_forearmL_ctl',
             currentPickerNamespace+'fk_handL_ctl']

    # FK to IK
    ik_handL_pos_ctrl = currentPickerNamespace+'handL_ctl'
    ik_handL_rot_ctrl = currentPickerNamespace+'handL_rot_ctl'
    ik_elbowL_ctrl = currentPickerNamespace+'forearmL_ctl'
    ik_handL_match_loc = currentPickerNamespace+'handL_match_loc'
    ik_forearmL_match_loc = currentPickerNamespace+'forearmL_match_loc'

    ik_handL_ctrls = [ik_handL_pos_ctrl, ik_handL_rot_ctrl, ik_elbowL_ctrl]
    ik_handL_matches = [ik_handL_match_loc, fk_handL_jnts[2], ik_forearmL_match_loc]


    ##################
    # HandR
    ##################

    ikfk_handR_switch_ctrl = currentPickerNamespace+'handR_ikfk_ctl'

    # IK to FK
    fk_handR_jnts = [currentPickerNamespace+'proxy_armR_jnt',
            currentPickerNamespace+'proxy_forearmR_jnt',
            currentPickerNamespace+'proxy_handR_jnt']

    fk_handR_ctrls = [currentPickerNamespace+'fk_armR_ctl',
             currentPickerNamespace+'fk_forearmR_ctl',
             currentPickerNamespace+'fk_handR_ctl']

    # FK to IK
    ik_handR_pos_ctrl = currentPickerNamespace+'handR_ctl'
    ik_handR_rot_ctrl = currentPickerNamespace+'handR_rot_ctl'
    ik_elbowR_ctrl = currentPickerNamespace+'forearmR_ctl'
    ik_handR_match_loc = currentPickerNamespace+'handR_match_loc'
    ik_forearmR_match_loc = currentPickerNamespace+'forearmR_match_loc'

    ik_handR_ctrls = [ik_handR_pos_ctrl, ik_handR_rot_ctrl, ik_elbowR_ctrl]
    ik_handR_matches = [ik_handR_match_loc, fk_handR_jnts[2], ik_forearmR_match_loc]


    ##################
    # FootL
    ##################

    ikfk_footL_switch_ctrl = currentPickerNamespace+'footL_ikfk_ctl'

    # IK to FK
    fk_footL_jnts = [currentPickerNamespace+'proxy_uplegL_jnt',
            currentPickerNamespace+'proxy_legL_jnt',
            currentPickerNamespace+'proxy_footL_jnt',
            currentPickerNamespace+'proxy_toebaseL_jnt']
    fk_footL_ctrls = [currentPickerNamespace+'fk_uplegL_ctl',
             currentPickerNamespace+'fk_legL_ctl',
             currentPickerNamespace+'fk_footL_ctl',
             currentPickerNamespace+'fk_toebaseL_ctl']

    # FK to IK
    ik_footL_pos_ctrl = currentPickerNamespace+'footL_ctl'
    ik_footL_rot_ctrl = currentPickerNamespace+'toebaseL_ctl'
    ik_kneeL_ctrl = currentPickerNamespace+'legL_ctl'
    ik_footL_match_loc = currentPickerNamespace+'footL_match_loc'
    ik_legL_match_loc = currentPickerNamespace+'legL_match_loc'

    ik_footL_ctrls = [ik_footL_pos_ctrl, ik_footL_rot_ctrl, ik_kneeL_ctrl]
    ik_footL_matches = [ik_footL_match_loc, fk_footL_jnts[3], ik_legL_match_loc]



    ##################
    # FootR
    ##################

    ikfk_footR_switch_ctrl = currentPickerNamespace+'footR_ikfk_ctl'

    # IK to FK
    fk_footR_jnts = [currentPickerNamespace+'proxy_uplegR_jnt',
            currentPickerNamespace+'proxy_legR_jnt',
            currentPickerNamespace+'proxy_footR_jnt',
            currentPickerNamespace+'proxy_toebaseR_jnt']
    fk_footR_ctrls = [currentPickerNamespace+'fk_uplegR_ctl',
             currentPickerNamespace+'fk_legR_ctl',
             currentPickerNamespace+'fk_footR_ctl',
             currentPickerNamespace+'fk_toebaseR_ctl']

    # FK to IK
    ik_footR_pos_ctrl = currentPickerNamespace+'footR_ctl'
    ik_footR_rot_ctrl = currentPickerNamespace+'toebaseR_ctl'
    ik_kneeR_ctrl = currentPickerNamespace+'legR_ctl'
    ik_footR_match_loc = currentPickerNamespace+'footR_match_loc'
    ik_legR_match_loc = currentPickerNamespace+'legR_match_loc'

    ik_footR_ctrls = [ik_footR_pos_ctrl, ik_footR_rot_ctrl, ik_kneeR_ctrl]
    ik_footR_matches = [ik_footR_match_loc, fk_footR_jnts[3], ik_legR_match_loc]

    ##################
    # Spine
    ##################
    # FK to IK
    fk_spine_ctrls = [currentPickerNamespace+'spine_01_ctl',
            currentPickerNamespace+'spine_02_ctl',
            currentPickerNamespace+'spine_03_ctl']

    ik_spine_match_locs = [currentPickerNamespace+'ik_spine_01_ctl_gp_loc',
             currentPickerNamespace+'ik_spine_02_ctl_gp_loc',
             currentPickerNamespace+'ik_spine_03_ctl_gp_loc']

    ik_spine_ctrls = [currentPickerNamespace+'ik_rot_spine_01_ctl',
             currentPickerNamespace+'ik_rot_spine_02_ctl',
             currentPickerNamespace+'ik_spine_03_ctl']

    ik_spine_pos_ctrl = currentPickerNamespace+'ik_spine_01_ctl'


    ##################
    # ReverseFoot
    ##################
    # Foot L
    footrollL_ctl_pos_loc = currentPickerNamespace+'footrollL_ctl_pos_loc'
    footroll_footL_ctl = currentPickerNamespace+'footL_ctl'
    footroll_toebaseL_ctl = currentPickerNamespace+'toebaseL_ctl'

    footlockL_loc = currentPickerNamespace+'footlockL_loc'
    toelockL_loc = currentPickerNamespace+'toelockL_loc'

    # Foot R
    footrollR_ctl_pos_loc = currentPickerNamespace+'footrollR_ctl_pos_loc'
    footroll_footR_ctl = currentPickerNamespace+'footR_ctl'
    footroll_toebaseR_ctl = currentPickerNamespace+'toebaseR_ctl'

    footlockR_loc = currentPickerNamespace+'footlockR_loc'
    toelockR_loc = currentPickerNamespace+'toelockR_loc'


    ##################
    # ReverseFoot
    ##################
    root_pos_ctl_loc = currentPickerNamespace+'root_pos_ctl_loc'
    root_pos_ctl = currentPickerNamespace+'root_pos_ctl'
    root_ctl = currentPickerNamespace+'root_ctl'



    try:
        cmds.refresh(su=1)

        bake(fk_handL_jnts, fk_handL_ctrls, ik_handL_ctrls, ik_handL_matches, handL_ikfk_state, handL_fk_ik, ikfk_handL_switch_ctrl,
             fk_handR_jnts, fk_handR_ctrls, ik_handR_ctrls, ik_handR_matches, handR_ikfk_state, handR_fk_ik, ikfk_handR_switch_ctrl,
             fk_footL_jnts, fk_footL_ctrls, ik_footL_ctrls, ik_footL_matches, footL_ikfk_state, footL_fk_ik, ikfk_footL_switch_ctrl,
             fk_footR_jnts, fk_footR_ctrls, ik_footR_ctrls, ik_footR_matches, footR_ikfk_state, footR_fk_ik, ikfk_footR_switch_ctrl,
             fk_spine_ctrls, ik_spine_match_locs, spine_ikfk_state,
             footrollL_ctl_pos_loc, footroll_footL_ctl, footroll_toebaseL_ctl, footrollR_ctl_pos_loc, footroll_footR_ctl, footroll_toebaseR_ctl, footlockL_loc, footlockR_loc, toelockL_loc, toelockR_loc, reverseFoot_state)

        cmds.refresh(su=0)
    except Exception as e:
        print(e)
        cmds.refresh(su=0)


    # ik2fk_spines
    if spine_ikfk_state:
        ik2fk_spines_matchConstraints(ik_spine_ctrls, ik_spine_pos_ctrl, fk_spine_ctrls)

    # reverseFoot
    if reverseFoot_state:
        reverseFoot_matchConstraints(footroll_footL_ctl, footroll_toebaseL_ctl, footroll_footR_ctl, footroll_toebaseR_ctl, footlockL_loc, footlockR_loc, toelockL_loc, toelockR_loc)

    # root constraint
    if cog_root_state:
        root_matchConstraints(root_pos_ctl_loc, root_ctl, root_pos_ctl, cog_root)


matchbake(handL_ikfk_state=False, handR_ikfk_state=False, handL_fk_ik=1, handR_fk_ik=1,
              footL_ikfk_state=False, footR_ikfk_state=False, footL_fk_ik=1, footR_fk_ik=1,
              spine_ikfk_state=False,
              reverseFoot_state=False,
              cog_root_state=True, cog_root=0)
