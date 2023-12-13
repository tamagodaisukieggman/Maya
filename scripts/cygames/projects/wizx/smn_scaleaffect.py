from maya import cmds, mel

# head_rigファイルで
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

# body_rigファイルで
cmds.setAttr("head_head_scaleConstraint1.dummy_head_headW1", 0)
cmds.setAttr("head_rig:dummy_jaw.segmentScaleCompensate", 0)
cmds.setAttr("head_rig:dummy_tooth_top.segmentScaleCompensate", 0)
cmds.setAttr("head_rig:dummy_tooth_bottom.segmentScaleCompensate", 0)
dup_L = cmds.duplicate('body_model:L_eye_01', n='dummy_affect_L_eye_01', po=1)
dup_R = cmds.duplicate('body_model:R_eye_01', n='dummy_affect_R_eye_01', po=1)
dup_L_child = cmds.duplicate('body_model:L_eye_02', n='dummy_affect_L_eye_02', po=1)
dup_R_child = cmds.duplicate('body_model:R_eye_02', n='dummy_affect_R_eye_02', po=1)
cmds.parent(dup_L_child, dup_L)
cmds.parent(dup_R_child, dup_R)
cmds.parent(dup_L, 'head_rig:dummy_head_head')
cmds.parent(dup_R, 'head_rig:dummy_head_head')
cmds.orientConstraint('head_rig:dummy_L_eye_01', dup_L, w=1, mo=1)
cmds.orientConstraint('head_rig:dummy_R_eye_01', dup_R, w=1, mo=1)
del_nodes = cmds.ls(['body_model:L_eye_01', 'body_model:R_eye_01'],
dag=1, type='constraint')
cmds.delete(del_nodes)
cmds.parentConstraint('dummy_affect_L_eye_01', 'body_model:L_eye_01', w=1, mo=1)
cmds.parentConstraint('dummy_affect_R_eye_01', 'body_model:R_eye_01', w=1, mo=1)
cmds.scaleConstraint('dummy_affect_L_eye_01', 'body_model:L_eye_01', w=1, mo=1)
cmds.scaleConstraint('dummy_affect_R_eye_01', 'body_model:R_eye_01', w=1, mo=1)
cmds.orientConstraint('dummy_affect_L_eye_02', 'body_model:L_eye_02', w=1, mo=1)
cmds.parentConstraint('dummy_affect_R_eye_02', 'body_model:R_eye_02', w=1, mo=1)
cmds.orientConstraint('dummy_affect_L_eye_02', 'body_model:L_eye_02', w=1, mo=1)
cmds.scaleConstraint('dummy_affect_R_eye_02', 'body_model:R_eye_02', w=1, mo=1)
cmds.scaleConstraint('proxy_head_body_fk_ctrl', 'head_rig:dummy_head_head', w=1, mo=1)
