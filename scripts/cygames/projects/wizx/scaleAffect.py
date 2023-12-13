from maya import cmds, mel

sel = cmds.ls(os=1, type='joint', dag=1)

for obj in sel:
    cmds.setAttr('{}.segmentScaleCompensate'.format(obj), 1)

cmds.connectAttr('head_head_Ctrl.scale', 'dummy_Ik.scale', f=1)
cmds.connectAttr('head_head_Ctrl.scale', 'dummy_L_eye_01.scale', f=1)
cmds.connectAttr('head_head_Ctrl.scale', 'dummy_R_eye_01.scale', f=1)

cmds.scaleConstraint('neck_head_Ctrl', 'dummy_neck_head', w=1, mo=1)

pma_L = cmds.createNode('plusMinusAverage', ss=1)
cmds.setAttr('{}.input3D[0].input3Dz'.format(pma_L), 10)
cmds.connectAttr('L_eye_Ctrl.translate', '{}.input3D[1]'.format(pma_L), f=1)
cmds.connectAttr('all_eye_Ctrl.translate', '{}.input3D[2]'.format(pma_L), f=1)
cmds.connectAttr('{}.output3D'.format(pma_L), 'Leye_IK.translate', f=1)
cmds.delete('Leye_IK_pointConstraint1')

pma_R = cmds.createNode('plusMinusAverage', ss=1)
cmds.setAttr('{}.input3D[0].input3Dz'.format(pma_R), 10)
cmds.connectAttr('R_eye_Ctrl.translate', '{}.input3D[1]'.format(pma_R), f=1)
cmds.connectAttr('all_eye_Ctrl.translate', '{}.input3D[2]'.format(pma_R), f=1)
cmds.connectAttr('{}.output3D'.format(pma_R), 'Reye_IK.translate', f=1)
cmds.delete('Reye_IK_pointConstraint1')
