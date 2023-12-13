from maya import cmds, mel

sel = cmds.ls(os=1)
for obj in sel:
    grp = obj.replace('_ctrlG', '')
    cmds.matchTransform(obj, 'rig:head_model:{0}'.format(grp))

sel = cmds.ls(os=1)
for obj in sel:
    loc = cmds.spaceLocator()
    cmds.matchTransform(loc[0], obj)
    cmds.parentConstraint(loc[0], obj)

cmds.matchTransform()


cmds.matchTransform(pos=1)



from maya import cmds, mel
cmds.matchTransform(pos=1)
cmds.matchTransform()
sel = cmds.ls(os=1, dag=1, type='joint')
for obj in sel:
    ctrl = obj.replace('head_model:', '')
    cmds.parentConstraint('{0}_c'.format(ctrl), obj,w=1,mo=1)
    cmds.scaleConstraint('{0}_c'.format(ctrl), obj,w=1,mo=1)



sel = cmds.ls(os=1, dag=1, type='constraint')
cmds.delete(sel)


cmds.ls(type='tkgmultiattrblendnode')
