from maya import cmds, mel


def cache_transform(ctrls):
    cache_dict = {}
    for ctrl in ctrls:
        wt = cmds.xform(ctrl, q=1, t=1, ws=1)
        wr = cmds.xform(ctrl, q=1, ro=1, ws=1)
        cache_dict[ctrl] = [wt, wr]

    return cache_dict


def space_match(ctrl=None, set_spc_at=None, spaces=None, setkey=None):
    space_dict = {}
    for spc in spaces:
        listAttrs = cmds.listAttr(ctrl, ud=1, k=1)
        if listAttrs:
            for at in listAttrs:
                if at == spc:
                    cur_val = cmds.getAttr(ctrl+'.'+spc)
                    space_dict[spc] = cur_val

    space_dict[set_spc_at] = 1.0

    for set_spc, val in space_dict.items():
        listAttrs = cmds.listAttr(ctrl, ud=1, k=1)
        if listAttrs:
            if not set_spc in listAttrs:
                return

            if set_spc == set_spc_at:
                cmds.setAttr(ctrl+'.'+set_spc, val)
            else:
                cmds.setAttr(ctrl+'.'+set_spc, 0.0)

        if setkey:
            cmds.setKeyframe([ctrl], at=set_spc)




def space_match_bake(ctrls=None, set_spc_at=None):
    if ctrls:

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

        get_transforms_frames = {}
        for i in range (int(start), int(end+1)):
            cmds.currentTime(i, e=True)
            get_transforms = cache_transform(ctrls)
            get_transforms_frames[i] = get_transforms

        for i in range (int(start), int(end+1)):
            cmds.currentTime(i, e=True)
            # space match
            for ctrl in ctrls:
                space_match(ctrl=ctrl, set_spc_at=set_spc_at, spaces=spaces, setkey=True)
                wt, wr = get_transforms_frames[i][ctrl]
                cmds.xform(ctrl, t=wt, ro=wr, a=1, ws=1)

                cmds.setKeyframe([ctrl], at=setkey_attrs)

        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)


spaces = ['rootSpace',
          'cogSpace',
          'hipSpace',
          'spineSpace',
          'shoulderSpace',
          'handSpace',
          'footSpace']

ctrls = cmds.ls(os=1)
set_spc_at = 'cogSpace'

space_match_bake(ctrls=ctrls, set_spc_at=set_spc_at)
