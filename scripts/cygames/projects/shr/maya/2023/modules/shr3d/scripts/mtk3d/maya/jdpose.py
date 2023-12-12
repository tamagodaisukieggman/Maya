# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import functools


class UI(object):
    WINDOW_NAME = 'A_or_T_Pose'
    def __init__(self, *args, **kwargs): # noqa
        pass

    def show(self, *args, **kwargs):
        if cmds.window(self.WINDOW_NAME, q=True, ex=True):
            cmds.deleteUI(self.WINDOW_NAME)

        win = cmds.window(self.WINDOW_NAME, title=self.WINDOW_NAME, mb=True)

        tabColA = cmds.columnLayout(adj=True)
        self.poseA = 'A'
        self.poseT = 'T'

        self.tfg = cmds.textFieldGrp(p=tabColA, l='Namespace', tx='', fcc=True)
        self.pum = cmds.popupMenu(b=0, p=self.tfg, pmc='')
        cmds.popupMenu(self.pum, e=True, pmc=functools.partial(self._get_nameSpace_pop, self.pum, self.tfg))

        layA = cmds.button(p=tabColA, l='mcJt > A pose', c=functools.partial(self.Apose_mcJt, self.poseA)) # noqa
        layB = cmds.button(p=tabColA, l='mcJt > T pose', c=functools.partial(self.Tpose_mcJt, self.poseT)) # noqa
        layC = cmds.button(p=tabColA, l='ctrls > A pose', c=functools.partial(self.Apose_ctrls, self.poseA)) # noqa
        layD = cmds.button(p=tabColA, l='ctrls > T pose', c=functools.partial(self.Tpose_ctrls, self.poseT)) # noqa

        cmds.separator()

        layE = cmds.button(p=tabColA, l='mst:mcJt > A pose', c=functools.partial(self.Apose_mcJt_mst, self.poseA)) # noqa
        layF = cmds.button(p=tabColA, l='mst:mcJt > T pose', c=functools.partial(self.Tpose_mcJt_mst, self.poseT)) # noqa
        layG = cmds.button(p=tabColA, l='mst:ctrls > A pose', c=functools.partial(self.Apose_ctrls_mst, self.poseA)) # noqa
        layH = cmds.button(p=tabColA, l='mst:ctrls > T pose', c=functools.partial(self.Tpose_ctrls_mst, self.poseT)) # noqa

        cmds.showWindow(win)

    # A
    def Apose_mcJt(self, *pose):
        namespace = cmds.textFieldGrp(self.tfg, q=True, tx=True)
        if pose[0]=='A': # noqa
            mel.eval("""
                     //spineB
                     setAttr "{0}j10_spineB_mcJt.rotateY" -5.5;

                     //neck
                     setAttr "{0}j12_neck_mcJt.rotateY" 24;

                     //head
                     setAttr "{0}j13_head_mcJt.rotateY" -18.5;

                     //shoulder_L
                     setAttr "{0}j14_shoulder_L_mcJt.rotateX" 2.484;
                     setAttr "{0}j14_shoulder_L_mcJt.rotateY" 0.232;
                     setAttr "{0}j14_shoulder_L_mcJt.rotateZ" -17.67;

                     //shoulder_R
                     setAttr "{0}j34_shoulder_R_mcJt.rotateX" 2.484;
                     setAttr "{0}j34_shoulder_R_mcJt.rotateY" 0.232;
                     setAttr "{0}j34_shoulder_R_mcJt.rotateZ" -17.67;

                     //arm_L
                     setAttr "{0}j15_arm_L_mcJt.rotateX" 3.93;
                     setAttr "{0}j15_arm_L_mcJt.rotateY" 4.137;
                     setAttr "{0}j15_arm_L_mcJt.rotateZ" -27.157;

                     //arm_R
                     setAttr "{0}j35_arm_R_mcJt.rotateX" 3.93;
                     setAttr "{0}j35_arm_R_mcJt.rotateY" 4.137;
                     setAttr "{0}j35_arm_R_mcJt.rotateZ" -27.157;

                     //thumb_L
                     setAttr "{0}j18_thumbA_L_mcJt.rotateX" -29.092;
                     setAttr "{0}j18_thumbA_L_mcJt.rotateY" 10.438;
                     setAttr "{0}j18_thumbA_L_mcJt.rotateZ" -25.674;
                     setAttr "{0}j19_thumbB_L_mcJt.rotateY" -37.472;

                     //thumb_R
                     setAttr "{0}j38_thumbA_R_mcJt.rotateX" -29.092;
                     setAttr "{0}j38_thumbA_R_mcJt.rotateY" 10.438;
                     setAttr "{0}j38_thumbA_R_mcJt.rotateZ" -25.674;
                     setAttr "{0}j39_thumbB_R_mcJt.rotateY" -37.472;

                     //index_L
                     setAttr "{0}j21_indexA_L_mcJt.rotateX" 18.448;
                     setAttr "{0}j21_indexA_L_mcJt.rotateY" -0.863;
                     setAttr "{0}j21_indexA_L_mcJt.rotateZ" -14.931;

                     //index_R
                     setAttr "{0}j41_indexA_R_mcJt.rotateX" 18.448;
                     setAttr "{0}j41_indexA_R_mcJt.rotateY" -0.863;
                     setAttr "{0}j41_indexA_R_mcJt.rotateZ" -14.931;

                     //mid_L
                     setAttr "{0}j24_midA_L_mcJt.rotateX" -3.044;
                     setAttr "{0}j24_midA_L_mcJt.rotateY" 1.01;
                     setAttr "{0}j24_midA_L_mcJt.rotateZ" 0.924;

                     //mid_R
                     setAttr "{0}j44_midA_R_mcJt.rotateX" -3.044;
                     setAttr "{0}j44_midA_R_mcJt.rotateY" 1.01;
                     setAttr "{0}j44_midA_R_mcJt.rotateZ" 0.924;

                     //ring_L
                     setAttr "{0}j28_ringA_L_mcJt.rotateX" -13.535;
                     setAttr "{0}j28_ringA_L_mcJt.rotateY" 1.079;
                     setAttr "{0}j28_ringA_L_mcJt.rotateZ" 16.044;

                     //ring_R
                     setAttr "{0}j48_ringA_R_mcJt.rotateX" -13.535;
                     setAttr "{0}j48_ringA_R_mcJt.rotateY" 1.079;
                     setAttr "{0}j48_ringA_R_mcJt.rotateZ" 16.044;

                     //pinky_L
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateX" -20.81;
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateY" 5.671;
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateZ" 31.791;

                     //pinky_R
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateX" -20.81;
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateY" 5.671;
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateZ" 31.791;

                     //upleg_L
                     setAttr "{0}j02_upleg_L_mcJt.rotateY" -4;

                     //upleg_R
                     setAttr "{0}j06_upleg_R_mcJt.rotateY" -4;

                     //leg_L
                     setAttr "{0}j04_foot_L_mcJt.rotateY" 4;

                     //leg_R
                     setAttr "{0}j08_foot_R_mcJt.rotateY" 4;

                     """.format(namespace))

    # T
    def Tpose_mcJt(self,*pose): # noqa
        namespace = cmds.textFieldGrp(self.tfg, q=True, tx=True)
        if pose[0]=='T': # noqa
            mel.eval("""
                     //spineB
                     setAttr "{0}j10_spineB_mcJt.rotateY" 0;

                     //neck
                     setAttr "{0}j12_neck_mcJt.rotateY" 0;

                     //head
                     setAttr "{0}j13_head_mcJt.rotateY" 0;

                     //shoulder_L
                     setAttr "{0}j14_shoulder_L_mcJt.rotateX" 0;
                     setAttr "{0}j14_shoulder_L_mcJt.rotateY" 0;
                     setAttr "{0}j14_shoulder_L_mcJt.rotateZ" 0;

                     //shoulder_R
                     setAttr "{0}j34_shoulder_R_mcJt.rotateX" 0;
                     setAttr "{0}j34_shoulder_R_mcJt.rotateY" 0;
                     setAttr "{0}j34_shoulder_R_mcJt.rotateZ" 0;

                     //arm_L
                     setAttr "{0}j15_arm_L_mcJt.rotateX" 0;
                     setAttr "{0}j15_arm_L_mcJt.rotateY" 0;
                     setAttr "{0}j15_arm_L_mcJt.rotateZ" 0;

                     //arm_R
                     setAttr "{0}j35_arm_R_mcJt.rotateX" 0;
                     setAttr "{0}j35_arm_R_mcJt.rotateY" 0;
                     setAttr "{0}j35_arm_R_mcJt.rotateZ" 0;

                     //thumb_L
                     setAttr "{0}j18_thumbA_L_mcJt.rotateX" 0;
                     setAttr "{0}j18_thumbA_L_mcJt.rotateY" 0;
                     setAttr "{0}j18_thumbA_L_mcJt.rotateZ" 0;
                     setAttr "{0}j19_thumbB_L_mcJt.rotateY" 0;

                     //thumb_R
                     setAttr "{0}j38_thumbA_R_mcJt.rotateX" 0;
                     setAttr "{0}j38_thumbA_R_mcJt.rotateY" 0;
                     setAttr "{0}j38_thumbA_R_mcJt.rotateZ" 0;
                     setAttr "{0}j39_thumbB_R_mcJt.rotateY" 0;

                     //index_L
                     setAttr "{0}j21_indexA_L_mcJt.rotateX" 0;
                     setAttr "{0}j21_indexA_L_mcJt.rotateY" 0;
                     setAttr "{0}j21_indexA_L_mcJt.rotateZ" 0;

                     //index_R
                     setAttr "{0}j41_indexA_R_mcJt.rotateX" 0;
                     setAttr "{0}j41_indexA_R_mcJt.rotateY" 0;
                     setAttr "{0}j41_indexA_R_mcJt.rotateZ" 0;

                     //mid_L
                     setAttr "{0}j24_midA_L_mcJt.rotateX" 0;
                     setAttr "{0}j24_midA_L_mcJt.rotateY" 0;
                     setAttr "{0}j24_midA_L_mcJt.rotateZ" 0;

                     //mid_R
                     setAttr "{0}j44_midA_R_mcJt.rotateX" 0;
                     setAttr "{0}j44_midA_R_mcJt.rotateY" 0;
                     setAttr "{0}j44_midA_R_mcJt.rotateZ" 0;

                     //ring_L
                     setAttr "{0}j28_ringA_L_mcJt.rotateX" 0;
                     setAttr "{0}j28_ringA_L_mcJt.rotateY" 0;
                     setAttr "{0}j28_ringA_L_mcJt.rotateZ" 0;

                     //ring_R
                     setAttr "{0}j48_ringA_R_mcJt.rotateX" 0;
                     setAttr "{0}j48_ringA_R_mcJt.rotateY" 0;
                     setAttr "{0}j48_ringA_R_mcJt.rotateZ" 0;

                     //pinky_L
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateX" 0;
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateY" 0;
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateZ" 0;

                     //pinky_R
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateX" 0;
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateY" 0;
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateZ" 0;

                     //upleg_L
                     setAttr "{0}j02_upleg_L_mcJt.rotateY" 0;

                     //upleg_R
                     setAttr "{0}j06_upleg_R_mcJt.rotateY" 0;

                     //leg_L
                     setAttr "{0}j04_foot_L_mcJt.rotateY" 0;

                     //leg_R
                     setAttr "{0}j08_foot_R_mcJt.rotateY" 0;

                     """.format(namespace))

    # A
    def Apose_mcJt_mst(self, *pose):
        namespace = cmds.textFieldGrp(self.tfg, q=True, tx=True)
        if pose[0]=='A': # noqa
            mel.eval("""
                     //spineB
                     setAttr "{0}j10_spineB_mcJt.rotateY" -5.5;

                     //neck
                     setAttr "{0}j12_neck_mcJt.rotateY" 24;

                     //head
                     setAttr "{0}j13_head_mcJt.rotateY" -18.5;

                     //shoulder_L
                     setAttr "{0}j14_shoulder_L_mcJt.rotateX" 2.484;
                     setAttr "{0}j14_shoulder_L_mcJt.rotateY" 0.232;
                     setAttr "{0}j14_shoulder_L_mcJt.rotateZ" -17.67;

                     //shoulder_R
                     setAttr "{0}j34_shoulder_R_mcJt.rotateX" 2.484;
                     setAttr "{0}j34_shoulder_R_mcJt.rotateY" 0.232;
                     setAttr "{0}j34_shoulder_R_mcJt.rotateZ" -17.67;

                     //arm_L
                     setAttr "{0}j15_arm_L_mcJt.rotateX" 3.93;
                     setAttr "{0}j15_arm_L_mcJt.rotateY" 4.137;
                     setAttr "{0}j15_arm_L_mcJt.rotateZ" -27.157;

                     //arm_R
                     setAttr "{0}j35_arm_R_mcJt.rotateX" 3.93;
                     setAttr "{0}j35_arm_R_mcJt.rotateY" 4.137;
                     setAttr "{0}j35_arm_R_mcJt.rotateZ" -27.157;

                     //thumb_L
                     setAttr "{0}j18_thumbA_L_mcJt.rotateX" -29.092;
                     setAttr "{0}j18_thumbA_L_mcJt.rotateY" 10.438;
                     setAttr "{0}j18_thumbA_L_mcJt.rotateZ" -25.674;
                     setAttr "{0}j19_thumbB_L_mcJt.rotateY" -37.472;

                     //thumb_R
                     setAttr "{0}j38_thumbA_R_mcJt.rotateX" -29.092;
                     setAttr "{0}j38_thumbA_R_mcJt.rotateY" 10.438;
                     setAttr "{0}j38_thumbA_R_mcJt.rotateZ" -25.674;
                     setAttr "{0}j39_thumbB_R_mcJt.rotateY" -37.472;

                     //index_L
                     setAttr "{0}j21_indexA_L_mcJt.rotateX" 18.448;
                     setAttr "{0}j21_indexA_L_mcJt.rotateY" -0.863;
                     setAttr "{0}j21_indexA_L_mcJt.rotateZ" -14.931;

                     //index_R
                     setAttr "{0}j41_indexA_R_mcJt.rotateX" 18.448;
                     setAttr "{0}j41_indexA_R_mcJt.rotateY" -0.863;
                     setAttr "{0}j41_indexA_R_mcJt.rotateZ" -14.931;

                     //mid_L
                     setAttr "{0}j24_midA_L_mcJt.rotateX" -3.044;
                     setAttr "{0}j24_midA_L_mcJt.rotateY" 1.01;
                     setAttr "{0}j24_midA_L_mcJt.rotateZ" 0.924;

                     //mid_R
                     setAttr "{0}j44_midA_R_mcJt.rotateX" -3.044;
                     setAttr "{0}j44_midA_R_mcJt.rotateY" 1.01;
                     setAttr "{0}j44_midA_R_mcJt.rotateZ" 0.924;

                     //ring_L
                     setAttr "{0}j28_ringA_L_mcJt.rotateX" -13.535;
                     setAttr "{0}j28_ringA_L_mcJt.rotateY" 1.079;
                     setAttr "{0}j28_ringA_L_mcJt.rotateZ" 16.044;

                     //ring_R
                     setAttr "{0}j48_ringA_R_mcJt.rotateX" -13.535;
                     setAttr "{0}j48_ringA_R_mcJt.rotateY" 1.079;
                     setAttr "{0}j48_ringA_R_mcJt.rotateZ" 16.044;

                     //pinky_L
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateX" -20.81;
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateY" 5.671;
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateZ" 31.791;

                     //pinky_R
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateX" -20.81;
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateY" 5.671;
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateZ" 31.791;

                     //upleg_L
                     setAttr "{0}j02_upleg_L_mcJt.rotateY" -4;

                     //upleg_R
                     setAttr "{0}j06_upleg_R_mcJt.rotateY" -4;

                     //leg_L
                     setAttr "{0}j04_foot_L_mcJt.rotateY" 4;

                     //leg_R
                     setAttr "{0}j08_foot_R_mcJt.rotateY" 4;

                     """.format(namespace))

    # T
    def Tpose_mcJt_mst(self,*pose): # noqa
        namespace = cmds.textFieldGrp(self.tfg, q=True, tx=True)
        if pose[0]=='T': # noqa
            mel.eval("""
                     //spineB
                     setAttr "{0}j10_spineB_mcJt.rotateY" 0;

                     //neck
                     setAttr "{0}j12_neck_mcJt.rotateY" 0;

                     //head
                     setAttr "{0}j13_head_mcJt.rotateY" 0;

                     //shoulder_L
                     setAttr "{0}j14_shoulder_L_mcJt.rotateX" 0;
                     setAttr "{0}j14_shoulder_L_mcJt.rotateY" 0;
                     setAttr "{0}j14_shoulder_L_mcJt.rotateZ" 0;

                     //shoulder_R
                     setAttr "{0}j34_shoulder_R_mcJt.rotateX" 0;
                     setAttr "{0}j34_shoulder_R_mcJt.rotateY" 0;
                     setAttr "{0}j34_shoulder_R_mcJt.rotateZ" 0;

                     //arm_L
                     setAttr "{0}j15_arm_L_mcJt.rotateX" 0;
                     setAttr "{0}j15_arm_L_mcJt.rotateY" 0;
                     setAttr "{0}j15_arm_L_mcJt.rotateZ" 0;

                     //arm_R
                     setAttr "{0}j35_arm_R_mcJt.rotateX" 0;
                     setAttr "{0}j35_arm_R_mcJt.rotateY" 0;
                     setAttr "{0}j35_arm_R_mcJt.rotateZ" 0;

                     //thumb_L
                     setAttr "{0}j18_thumbA_L_mcJt.rotateX" 0;
                     setAttr "{0}j18_thumbA_L_mcJt.rotateY" 0;
                     setAttr "{0}j18_thumbA_L_mcJt.rotateZ" 0;
                     setAttr "{0}j19_thumbB_L_mcJt.rotateY" 0;

                     //thumb_R
                     setAttr "{0}j38_thumbA_R_mcJt.rotateX" 0;
                     setAttr "{0}j38_thumbA_R_mcJt.rotateY" 0;
                     setAttr "{0}j38_thumbA_R_mcJt.rotateZ" 0;
                     setAttr "{0}j39_thumbB_R_mcJt.rotateY" 0;

                     //index_L
                     setAttr "{0}j21_indexA_L_mcJt.rotateX" 0;
                     setAttr "{0}j21_indexA_L_mcJt.rotateY" 0;
                     setAttr "{0}j21_indexA_L_mcJt.rotateZ" 0;

                     //index_R
                     setAttr "{0}j41_indexA_R_mcJt.rotateX" 0;
                     setAttr "{0}j41_indexA_R_mcJt.rotateY" 0;
                     setAttr "{0}j41_indexA_R_mcJt.rotateZ" 0;

                     //mid_L
                     setAttr "{0}j24_midA_L_mcJt.rotateX" 0;
                     setAttr "{0}j24_midA_L_mcJt.rotateY" 0;
                     setAttr "{0}j24_midA_L_mcJt.rotateZ" 0;

                     //mid_R
                     setAttr "{0}j44_midA_R_mcJt.rotateX" 0;
                     setAttr "{0}j44_midA_R_mcJt.rotateY" 0;
                     setAttr "{0}j44_midA_R_mcJt.rotateZ" 0;

                     //ring_L
                     setAttr "{0}j28_ringA_L_mcJt.rotateX" 0;
                     setAttr "{0}j28_ringA_L_mcJt.rotateY" 0;
                     setAttr "{0}j28_ringA_L_mcJt.rotateZ" 0;

                     //ring_R
                     setAttr "{0}j48_ringA_R_mcJt.rotateX" 0;
                     setAttr "{0}j48_ringA_R_mcJt.rotateY" 0;
                     setAttr "{0}j48_ringA_R_mcJt.rotateZ" 0;

                     //pinky_L
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateX" 0;
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateY" 0;
                     setAttr "{0}j31_pinkyA_L_mcJt.rotateZ" 0;

                     //pinky_R
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateX" 0;
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateY" 0;
                     setAttr "{0}j51_pinkyA_R_mcJt.rotateZ" 0;

                     //upleg_L
                     setAttr "{0}j02_upleg_L_mcJt.rotateY" 0;

                     //upleg_R
                     setAttr "{0}j06_upleg_R_mcJt.rotateY" 0;

                     //leg_L
                     setAttr "{0}j04_foot_L_mcJt.rotateY" 0;

                     //leg_R
                     setAttr "{0}j08_foot_R_mcJt.rotateY" 0;

                     """.format(namespace))


    # ctrls

    def Apose_ctrls(self,*pose): # noqa
        namespace = cmds.textFieldGrp(self.tfg, q=True, tx=True)
        if pose[0]=='A': # noqa
            cmds.xform('{}hand_L_Ctrl'.format(namespace), t=[-17.217956518700248, -45.19760424233918, -2.417218189907139], a=True)
            cmds.xform('{}hand_R_Ctrl'.format(namespace), t=[17.2179586692953, -45.19761995154485, -2.4172724837901063], a=True)
            cmds.xform('{}leg_L_Ctrl'.format(namespace), t=[1.7763568394002505e-15, 0.20340355827902812, -5.824690659685834], a=True)
            cmds.xform('{}leg_R_Ctrl'.format(namespace), t=[-5.453415496958769e-13, 0.20340355827803336, -5.8246906904298], a=True)
            cmds.xform('{}leg_L_PVCtrl'.format(namespace), t=[1.2434497875801753e-14, -4.097065353690752, -3.076431241152868], a=True)
            cmds.xform('{}leg_R_PVCtrl'.format(namespace), t=[1.3204284030621238e-06, -4.0691625222715615, -3.0754568443326775], a=True)
            cmds.xform('{}arm_L_PVCtrl'.format(namespace), t=[-8.901975440014986, -25.046387424314148, -2.3656443803747678], a=True)
            cmds.xform('{}arm_R_PVCtrl'.format(namespace), t=[8.902052744184132, -25.047458217031974, -2.365691970430042], a=True)
            cmds.xform('{}spineB_Ctrl'.format(namespace), ro=[0.0, -5.5, 0.0], a=True)
            cmds.xform('{}neck_Ctrl'.format(namespace), ro=[0.0, 24.0, 0.0], a=True)
            cmds.xform('{}head_Ctrl'.format(namespace), ro=[0.0, -18.5, 0.0], a=True)
            cmds.xform('{}shoulder_L_Ctrl'.format(namespace), ro=[2.4840000000002576, 0.23200000000008086, -17.670000000001693], a=True)
            cmds.xform('{}shoulder_R_Ctrl'.format(namespace), ro=[2.4840000000002336, 0.23200000000007218, -17.670000000001686], a=True)
            cmds.xform('{}thumbA_L_Ctrl'.format(namespace), ro=[-29.091991976672258, 10.43798358524365, -25.67399854651129], a=True)
            cmds.xform('{}indexA_L_Ctrl'.format(namespace), ro=[18.448, -0.8630000000000007, -14.931018212772198], a=True)
            cmds.xform('{}midA_L_Ctrl'.format(namespace), ro=[-3.044, 1.01, 0.9239817872278003], a=True)
            cmds.xform('{}ringA_L_Ctrl'.format(namespace), ro=[-13.535000000000002, 1.079, 16.043999800179964], a=True)
            cmds.xform('{}pinkyA_L_Ctrl'.format(namespace), ro=[-20.809999999999995, 5.670999999999998, 31.790999800179954], a=True)
            cmds.xform('{}thumbA_R_Ctrl'.format(namespace), ro=[-29.091998243935457, 10.437998030931414, -25.673999771482848], a=True)
            cmds.xform('{}indexA_R_Ctrl'.format(namespace), ro=[18.448001222557153, -0.8629996740312732, -14.93100254130824], a=True)
            cmds.xform('{}midA_R_Ctrl'.format(namespace), ro=[-3.043998734834536, 1.0099999795982768, 0.9239974994064083], a=True)
            cmds.xform('{}ringA_R_Ctrl'.format(namespace), ro=[-13.535000000000002, 1.079, 16.043999800180014], a=True)
            cmds.xform('{}pinkyA_R_Ctrl'.format(namespace), ro=[-20.81, 5.671, 31.79099980018001], a=True)
            cmds.xform('{}thumbB_L_Ctrl'.format(namespace), ro=[0.0, -37.47200000000001, 0.0], a=True)
            cmds.xform('{}thumbB_R_Ctrl'.format(namespace), ro=[0.0, -37.47200000000002, 0.0], a=True)

    def Tpose_ctrls(self,*pose): # noqa
        namespace = cmds.textFieldGrp(self.tfg, q=True, tx=True)
        if pose[0]=='T': # noqa
            cmds.xform('{}hand_L_Ctrl'.format(namespace), t=[0, 0, 0], a=True)
            cmds.xform('{}hand_R_Ctrl'.format(namespace), t=[0, 0, 0], a=True)
            cmds.xform('{}leg_L_Ctrl'.format(namespace), t=[0, 0, 0], a=True)
            cmds.xform('{}leg_R_Ctrl'.format(namespace), t=[0, 0, 0], a=True)
            cmds.xform('{}leg_L_PVCtrl'.format(namespace), t=[0, 0, 0], a=True)
            cmds.xform('{}leg_R_PVCtrl'.format(namespace), t=[0, 0, 0], a=True)
            cmds.xform('{}arm_L_PVCtrl'.format(namespace), t=[0, 0, 0], a=True)
            cmds.xform('{}arm_R_PVCtrl'.format(namespace), t=[0, 0, 0], a=True)
            cmds.xform('{}spineB_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}neck_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}head_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}shoulder_L_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}shoulder_R_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}thumbA_L_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}indexA_L_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}midA_L_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}ringA_L_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}pinkyA_L_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}thumbA_R_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}indexA_R_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}midA_R_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}ringA_R_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}pinkyA_R_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}thumbB_L_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)
            cmds.xform('{}thumbB_R_Ctrl'.format(namespace), ro=[0, 0, 0], a=True)


    def Apose_ctrls_mst(self,*pose): # noqa
        namespace = cmds.textFieldGrp(self.tfg, q=True, tx=True)
        if pose[0]=='A': # noqa
            cmds.xform("{}arm_L_IkFkSwitcher".format(namespace), t=[0.0, 2.842170943040401e-14, 0.0], a=True)
            cmds.xform("{}arm_L_IkFkSwitcher".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_L_PVCtrl".format(namespace), t=[-15.164288229712866, -34.82386623315321, -3.1593944137781307], a=True)
            cmds.xform("{}arm_L_PVCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_R_IkFkSwitcher".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_R_IkFkSwitcher".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_R_PVCtrl".format(namespace), t=[15.152616142550443, -34.81093417891498, -3.1597674852969817], a=True)
            cmds.xform("{}arm_R_PVCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}chest_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}chest_Ctrl".format(namespace), ro=[0.0, -5.5, 0.0], a=True)
            cmds.xform("{}eq_rightHandCtrl".format(namespace), t=[0.00029572702710822796, -2.2224741021759087e-05, 0.00014005258660176878], a=True)
            cmds.xform("{}eq_rightHandCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_APivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_APivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_BPivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_BPivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_Ctrl".format(namespace), t=[-13.891999999999992, -4.618527782440651e-14, 2.3092638912203256e-14], a=True)
            cmds.xform("{}foot_L_Ctrl".format(namespace), ro=[0.0, 0.0, -1.5144350217238549e-19], a=True)
            cmds.xform("{}foot_R_APivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_R_APivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_R_BPivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_R_BPivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_R_Ctrl".format(namespace), t=[-13.892023611936267, -0.00044433559709133874, 1.924679653519945e-05], a=True)
            cmds.xform("{}foot_R_Ctrl".format(namespace), ro=[-2.324337246379148e-19, -3.1805546814635195e-15, 9.224183487416335e-20], a=True)
            cmds.xform("{}hand_L_AuxCtrl".format(namespace), t=[1.4210854715202004e-14, 0.0, -2.842170943040401e-14], a=True)
            cmds.xform("{}hand_L_AuxCtrl".format(namespace), ro=[2.54445345145341e-14, 1.9875433545835341e-16, 3.975693351829395e-16], a=True)
            cmds.xform("{}hand_L_Ctrl".format(namespace), t=[-29.551954551165437, -71.64399594041635, -3.0855200818868678], a=True)
            cmds.xform("{}hand_L_Ctrl".format(namespace), ro=[-89.99999999999999, -1.5530052155583578e-18, -0.026000000000010813], a=True)
            cmds.xform("{}hand_R_AuxCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hand_R_AuxCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hand_R_Ctrl".format(namespace), t=[29.55230033518319, -71.64399999974455, -3.0855199999990823], a=True)
            cmds.xform("{}hand_R_Ctrl".format(namespace), ro=[-90.00000001585754, 3.494501097574177e-05, -0.026000000000010823], a=True)
            cmds.xform("{}head_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}head_Ctrl".format(namespace), ro=[0.0, -16.464, 0.0], a=True)
            cmds.xform("{}heel_L_PivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}heel_L_PivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}heel_R_PivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}heel_R_PivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hip_Ctrl".format(namespace), t=[-2.842170943040401e-14, 0.0, 1.401298464324817e-45], a=True)
            cmds.xform("{}hip_Ctrl".format(namespace), ro=[-7.016709298534875e-15, 7.016709298534876e-15, -4.296495291499102e-31], a=True)
            cmds.xform("{}indexA_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexA_L_Ctrl".format(namespace), ro=[-0.11998580349950087, -0.16127910049773897, -8.46913892255599], a=True)
            cmds.xform("{}indexA_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexA_R_Ctrl".format(namespace), ro=[-0.11980138833168262, -0.1613211884349981, -8.469144872746455], a=True)
            cmds.xform("{}indexB_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexB_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexB_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexB_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexC_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexC_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexC_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexC_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_L_Ctrl".format(namespace), t=[-9.414691248821327e-13, 0.3588600230060166, -10.230193549698416], a=True)
            cmds.xform("{}leg_L_Ctrl".format(namespace), ro=[-1.0189999941706087, -0.00024205202498520543, -6.317808934770511e-06], a=True)
            cmds.xform("{}leg_L_IkFkSwitcher".format(namespace), t=[0.0, 2.842170943040401e-14, 0.0], a=True)
            cmds.xform("{}leg_L_IkFkSwitcher".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_L_PVCtrl".format(namespace), t=[4.618527782440651e-14, -4.051473419267936, -4.901086626298465], a=True)
            cmds.xform("{}leg_L_PVCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_R_Ctrl".format(namespace), t=[0.0, 0.35890000000286193, -10.230230559494402], a=True)
            cmds.xform("{}leg_R_Ctrl".format(namespace), ro=[-1.018999994170192, 0.00024206095479324156, 6.2996097799362575e-06], a=True)
            cmds.xform("{}leg_R_IkFkSwitcher".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_R_IkFkSwitcher".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_R_PVCtrl".format(namespace), t=[3.197442310920451e-14, -4.0232052079551295, -4.9001134463749665], a=True)
            cmds.xform("{}leg_R_PVCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}localOffset".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}localOffset".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midA_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midA_L_Ctrl".format(namespace), ro=[0.2705294945369226, -4.949692498971204, -2.5259977439371406], a=True)
            cmds.xform("{}midA_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midA_R_Ctrl".format(namespace), ro=[0.27070923020387955, -4.949753455210896, -2.5260186828310127], a=True)
            cmds.xform("{}midB_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midB_L_Ctrl".format(namespace), ro=[0.0, 6.572446759639444, 0.0], a=True)
            cmds.xform("{}midB_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midB_R_Ctrl".format(namespace), ro=[0.0, 6.572446759639444, 0.0], a=True)
            cmds.xform("{}midC_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midC_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midC_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midC_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}moveCtrl".format(namespace), t=[-2.524354896707238e-29, 0.0, -1.401298464324817e-45], a=True)
            cmds.xform("{}moveCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}neck_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}neck_Ctrl".format(namespace), ro=[0.0, 25.964, 0.0], a=True)
            cmds.xform("{}pinkyA_L_Ctrl".format(namespace), t=[0.0, 1.7763568394002505e-15, 0.0], a=True)
            cmds.xform("{}pinkyA_L_Ctrl".format(namespace), ro=[0.0030290544038823193, 2.3973764414307066, 10.76729132551301], a=True)
            cmds.xform("{}pinkyA_R_Ctrl".format(namespace), t=[0.0, 1.7763568394002505e-15, 0.0], a=True)
            cmds.xform("{}pinkyA_R_Ctrl".format(namespace), ro=[0.0031894466346891396, 2.3972759448153327, 10.767292603564684], a=True)
            cmds.xform("{}pinkyB_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyB_L_Ctrl".format(namespace), ro=[0.0, 3.240000078537074, 0.0], a=True)
            cmds.xform("{}pinkyB_R_Ctrl".format(namespace), t=[0.0, -1.7763568394002505e-15, 0.0], a=True)
            cmds.xform("{}pinkyB_R_Ctrl".format(namespace), ro=[0.0, 3.240000078537074, 0.0], a=True)
            cmds.xform("{}pinkyC_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyC_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyC_R_Ctrl".format(namespace), t=[0.0, -1.7763568394002505e-15, 0.0], a=True)
            cmds.xform("{}pinkyC_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringA_L_Ctrl".format(namespace), t=[0.0, 8.881784197001252e-16, 0.0], a=True)
            cmds.xform("{}ringA_L_Ctrl".format(namespace), ro=[0.0034976316108620165, -1.591294520181302, 4.710671568972065], a=True)
            cmds.xform("{}ringA_R_Ctrl".format(namespace), t=[-2.842170943040401e-14, 2.6645352591003757e-15, 0.0], a=True)
            cmds.xform("{}ringA_R_Ctrl".format(namespace), ro=[0.0036676580577857322, -1.5913775474538774, 4.710661416256153], a=True)
            cmds.xform("{}ringB_L_Ctrl".format(namespace), t=[0.0, 8.881784197001252e-16, 0.0], a=True)
            cmds.xform("{}ringB_L_Ctrl".format(namespace), ro=[-0.32918081704228536, 1.2526881939278245, -3.3762752925552446], a=True)
            cmds.xform("{}ringB_R_Ctrl".format(namespace), t=[0.0, -8.881784197001252e-16, 0.0], a=True)
            cmds.xform("{}ringB_R_Ctrl".format(namespace), ro=[-0.32918081704228536, 1.2526881939278245, -3.3762752925552446], a=True)
            cmds.xform("{}ringC_L_Ctrl".format(namespace), t=[-2.842170943040401e-14, 8.881784197001252e-16, 0.0], a=True)
            cmds.xform("{}ringC_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringC_R_Ctrl".format(namespace), t=[2.842170943040401e-14, -8.881784197001252e-16, 0.0], a=True)
            cmds.xform("{}ringC_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}shoulder_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}shoulder_L_Ctrl".format(namespace), ro=[-2.1592984517123393e-13, 1.302039572724308e-14, 9.605275138019818e-13], a=True)
            cmds.xform("{}shoulder_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}shoulder_R_Ctrl".format(namespace), ro=[-5.267793691173897e-15, 5.814451527050539e-15, 1.0368541288221144e-12], a=True)
            cmds.xform("{}spineA_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}spineA_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}spineB_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}spineB_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbA_L_Ctrl".format(namespace), t=[-1.4210854715202004e-14, 0.0, 2.842170943040401e-14], a=True)
            cmds.xform("{}thumbA_L_Ctrl".format(namespace), ro=[-0.013977009050537387, 1.8412836417250602, -23.818997973611307], a=True)
            cmds.xform("{}thumbA_R_Ctrl".format(namespace), t=[0.0, -2.842170943040401e-14, -1.4210854715202004e-14], a=True)
            cmds.xform("{}thumbA_R_Ctrl".format(namespace), ro=[-0.013820443101097814, 1.841349211949376, -23.81907674347085], a=True)
            cmds.xform("{}thumbB_L_Ctrl".format(namespace), t=[0.0, 5.684341886080802e-14, -1.7763568394002505e-15], a=True)
            cmds.xform("{}thumbB_L_Ctrl".format(namespace), ro=[4.094999999960026, -26.268000000008087, -9.105999999949823], a=True)
            cmds.xform("{}thumbB_R_Ctrl".format(namespace), t=[2.842170943040401e-14, -2.842170943040401e-14, 1.7763568394002505e-15], a=True)
            cmds.xform("{}thumbB_R_Ctrl".format(namespace), ro=[4.094999999957783, -26.26800000000839, -9.105999999948796], a=True)
            cmds.xform("{}thumbC_L_Ctrl".format(namespace), t=[-2.842170943040401e-14, -2.842170943040401e-14, 5.329070518200751e-15], a=True)
            cmds.xform("{}thumbC_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbC_R_Ctrl".format(namespace), t=[0.0, -2.842170943040401e-14, -1.7763568394002505e-15], a=True)
            cmds.xform("{}thumbC_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_L_Ctrl".format(namespace), ro=[7.102068377999705e-07, 5.915849738044545e-05, -1.2729454642710108e-06], a=True)
            cmds.xform("{}toe_L_PivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_L_PivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_R_Ctrl".format(namespace), ro=[7.345029282179987e-07, 5.917373529909279e-05, -1.2650267400712094e-06], a=True)
            cmds.xform("{}toe_R_PivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_R_PivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}worldOffset".format(namespace), t=[-3.1554436208840472e-30, 0.0, 1.7516230804060213e-46], a=True)
            cmds.xform("{}worldOffset".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}wrist_L_Ctrl".format(namespace), t=[0.0, 8.881784197001252e-16, 0.0], a=True)
            cmds.xform("{}wrist_L_Ctrl".format(namespace), ro=[0.12209924686401416, 4.941502447337351, 0.3710070267973698], a=True)
            cmds.xform("{}wrist_R_Ctrl".format(namespace), t=[-2.842170943040401e-14, 0.0, 0.0], a=True)
            cmds.xform("{}wrist_R_Ctrl".format(namespace), ro=[0.12215872304740115, 4.941203147345245, 0.37133691349617365], a=True)

    def Tpose_ctrls_mst(self,*pose): # noqa
        namespace = cmds.textFieldGrp(self.tfg, q=True, tx=True)
        if pose[0]=='T': # noqa
            cmds.xform("{}arm_L_IkFkSwitcher".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_L_IkFkSwitcher".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_L_PVCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_L_PVCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_R_IkFkSwitcher".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_R_IkFkSwitcher".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_R_PVCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}arm_R_PVCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}chest_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}chest_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}eq_rightHandCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}eq_rightHandCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_APivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_APivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_BPivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_BPivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_R_APivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_R_APivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_R_BPivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_R_BPivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}foot_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hand_L_AuxCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hand_L_AuxCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hand_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hand_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hand_R_AuxCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hand_R_AuxCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hand_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hand_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}head_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}head_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}heel_L_PivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}heel_L_PivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}heel_R_PivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}heel_R_PivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hip_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}hip_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexA_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexA_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexA_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexA_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexB_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexB_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexB_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexB_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexC_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexC_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexC_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}indexC_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_L_IkFkSwitcher".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_L_IkFkSwitcher".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_L_PVCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_L_PVCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_R_IkFkSwitcher".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_R_IkFkSwitcher".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_R_PVCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}leg_R_PVCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}localOffset".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}localOffset".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midA_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midA_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midA_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midA_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midB_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midB_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midB_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midB_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midC_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midC_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midC_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}midC_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}moveCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}moveCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}neck_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}neck_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyA_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyA_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyA_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyA_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyB_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyB_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyB_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyB_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyC_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyC_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyC_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}pinkyC_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringA_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringA_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringA_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringA_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringB_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringB_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringB_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringB_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringC_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringC_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringC_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}ringC_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}shoulder_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}shoulder_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}shoulder_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}shoulder_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}spineA_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}spineA_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}spineB_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}spineB_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbA_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbA_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbA_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbA_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbB_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbB_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbB_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbB_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbC_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbC_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbC_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}thumbC_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_L_PivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_L_PivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_R_PivCtrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}toe_R_PivCtrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}worldOffset".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}worldOffset".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}wrist_L_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}wrist_L_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}wrist_R_Ctrl".format(namespace), t=[0.0, 0.0, 0.0], a=True)
            cmds.xform("{}wrist_R_Ctrl".format(namespace), ro=[0.0, 0.0, 0.0], a=True)

    def _list_namespaces(self, *args, **kwargs):  # noqa
        exclude_list = ['UI', 'shared']

        current = cmds.namespaceInfo(cur=True)
        cmds.namespace(set=':')
        namespaces = ['{}'.format(ns) for ns in cmds.namespaceInfo(lon=True) if ns not in exclude_list]
        cmds.namespace(set=current)

        return namespaces

    def _setCommand_textFieldGrpText(self, *args, **kwargs): # noqa
        if args[1] == '':
            cmds.textFieldGrp(args[0], e=True, tx=args[1])
        else: # noqa
            cmds.textFieldGrp(args[0], e=True, tx=args[1]+':') # noqa

    def _get_nameSpace_pop(self, *args, **kwargs):  # noqa
        # mc.textScrollList('nameSpList', e=True, removeAll=True)
        cmds.popupMenu(args[0], e=True, dai=True)

        # cmds.menuItem(p=self.popC, l=u'Ctrls Constraint.', c=functools.partial(self._ctrls_constraint_))
        rn = cmds.ls(type='reference')
        nsl = self._list_namespaces()
        if rn is not None:
            cmds.menuItem(p=args[0], l='-ReferenceNode-', bld=True)
            for ns in rn:
                if 0 < ns.count('sharedReferenceNode'):
                    continue
                else:
                    ns2 = ns.replace('RN', '')
                    miA = cmds.menuItem(p=args[0], l=ns2, c='')
                    cmds.menuItem(miA, e=True, c=functools.partial(self._setCommand_textFieldGrpText, args[1], ns2))
        if nsl is not None:
            cmds.menuItem(p=args[0], l='-Namespace-', bld=True)
            for nss in nsl:
                miB = cmds.menuItem(p=args[0], l=nss, c='')
                cmds.menuItem(miB, e=True, c=functools.partial(self._setCommand_textFieldGrpText, args[1], nss))
