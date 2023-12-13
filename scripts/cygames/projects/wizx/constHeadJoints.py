from maya import cmds, mel

facial_chara_joints = cmds.ls('head_model:neck_head', dag=1, type='joint')
for jnt in facial_chara_joints:
    try:
        if cmds.objExists(jnt) and cmds.objExists(jnt.replace('head_model:', 'head_rig:dummy_')):
            cmds.pointConstraint(jnt.replace('head_model:', 'head_rig:dummy_'), jnt, mo=1)
        else:
            cmds.pointConstraint(jnt.replace('head_model:', 'targets:facial_proxy_'), jnt, mo=1)
    except:
        pass
    try:
        if cmds.objExists(jnt) and cmds.objExists(jnt.replace('head_model:', 'head_rig:dummy_')):
            cmds.orientConstraint(jnt.replace('head_model:', 'head_rig:dummy_'), jnt, mo=1)
        else:
            cmds.orientConstraint(jnt.replace('head_model:', 'targets:facial_proxy_'), jnt, mo=1)
    except:
        pass
    try:
        if cmds.objExists(jnt) and cmds.objExists(jnt.replace('head_model:', 'head_rig:dummy_')):
            cmds.scaleConstraint(jnt.replace('head_model:', 'head_rig:dummy_'), jnt, mo=1)
        else:
            cmds.scaleConstraint(jnt.replace('head_model:', 'targets:facial_proxy_'), jnt, mo=1)
    except:
        pass
