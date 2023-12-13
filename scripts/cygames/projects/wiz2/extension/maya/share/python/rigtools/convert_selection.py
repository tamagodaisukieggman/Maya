from __future__ import print_function
import re
from maya import mel, cmds
from collections import OrderedDict

class Task:
    def __init__(self, sel, rig_nodes=None, jnt_nodes=None):
        if type(rig_nodes) is list and type(jnt_nodes) is list:
            self.rig_nodes = get_nodes(rig_nodes)
            self.jnt_nodes = get_nodes(jnt_nodes)    
        else:
            if len(sel) != 2:
                cmds.error('Select a rig group followed by a joint group')
            self.rig_nodes = get_nodes(sel[0])
            self.jnt_nodes = get_nodes(sel[1])
        self.unlocked = []

    def _find_node(self, node_name, buf):
        expr = re.compile('(^|[:\|])%s$' % node_name)
        cands = [x for x in buf if expr.search(x)]
        if len(cands) == 0:
            print ('ERROR: %s not found.' % node_name)
            #raise Exception()
            return None
        elif len(cands) > 1:
            print ('ERROR: more than one objects named %s found.' % node_name)
            raise Exception()
        return cands[0]

    def find_rig_node(self, node_name):
        return self._find_node(node_name, self.rig_nodes)

    def find_jnt_node(self, node_name):
        return self._find_node(node_name, self.jnt_nodes)

    #def exec_(self):
    #    pass

    def exec_(self):
        source_joints = [u'root_jnt',
            u'cog_jnt',
            u'spine_01_jnt',
            u'spine_02_jnt',
            u'spine_03_jnt',
            u'neck_jnt',
            u'head_jnt',
            u'shoulderL_jnt',
            u'armL_jnt',
            u'forearmL_jnt',
            u'handL_jnt',
            u'handWeaponL_offset_jnt',
            u'handWeaponL_bind_jnt',
            u'shoulderR_jnt',
            u'armR_jnt',
            u'forearmR_jnt',
            u'handR_jnt',
            u'handWeaponR_offset_jnt',
            u'handWeaponR_bind_jnt',
            u'hip_jnt',
            u'uplegL_jnt',
            u'legL_jnt',
            u'footL_jnt',
            u'toebaseL_jnt',
            u'uplegR_jnt',
            u'legR_jnt',
            u'footR_jnt',
            u'toebaseR_jnt']

        match_ctrls = OrderedDict()
        match_ctrls[self.find_rig_node('root_ctl')] = [self.find_jnt_node('root_jnt'), 1, 1, 0, 1]
        match_ctrls[self.find_rig_node('cog_ctl')] = [self.find_jnt_node('cog_jnt'), 1, 0, 0, 1]
        match_ctrls[self.find_rig_node('hip_ctl')] = [self.find_jnt_node('hip_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('spine_01_ctl')] = [self.find_jnt_node('spine_01_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('spine_02_ctl')] = [self.find_jnt_node('spine_02_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('spine_03_ctl')] = [self.find_jnt_node('spine_03_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('neck_ctl')] = [self.find_jnt_node('neck_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('head_ctl')] = [self.find_jnt_node('head_jnt'), 0, 1, 0, 1]

        # IK arm
        match_ctrls[self.find_rig_node('shoulderL_ctl')] = [self.find_jnt_node('shoulderL_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('handL_ctl')] = [self.find_jnt_node('handL_jnt'), 1, 0, 0, 1]
        match_ctrls[self.find_rig_node('handL_rot_ctl')] = [self.find_jnt_node('handL_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_con_armL_loc')] = [self.find_jnt_node('armL_jnt'), 1, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_con_forearmL_loc')] = [self.find_jnt_node('forearmL_jnt'), 1, 1, 0, 1]

        match_ctrls[self.find_rig_node('shoulderR_ctl')] = [self.find_jnt_node('shoulderR_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('handR_ctl')] = [self.find_jnt_node('handR_jnt'), 1, 0, 0, 1]
        match_ctrls[self.find_rig_node('handR_rot_ctl')] = [self.find_jnt_node('handR_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_con_armR_loc')] = [self.find_jnt_node('armR_jnt'), 1, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_con_forearmR_loc')] = [self.find_jnt_node('forearmR_jnt'), 1, 1, 0, 1]

        # FK arm
        match_ctrls[self.find_rig_node('fk_armL_ctl')] = [self.find_jnt_node('armL_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_forearmL_ctl')] = [self.find_jnt_node('forearmL_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_handL_ctl')] = [self.find_jnt_node('handL_jnt'), 0, 1, 0, 1]

        match_ctrls[self.find_rig_node('fk_armR_ctl')] = [self.find_jnt_node('armR_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_forearmR_ctl')] = [self.find_jnt_node('forearmR_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_handR_ctl')] = [self.find_jnt_node('handR_jnt'), 0, 1, 0, 1]


        # IK leg
        match_ctrls[self.find_rig_node('footL_ctl')] = [self.find_jnt_node('footL_jnt'), 1, 1, 0, 1]
        match_ctrls[self.find_rig_node('toebaseL_ctl')] = [self.find_jnt_node('toebaseL_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_con_uplegL_loc')] = [self.find_jnt_node('uplegL_jnt'), 1, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_con_legL_loc')] = [self.find_jnt_node('legL_jnt'), 1, 1, 0, 1]

        match_ctrls[self.find_rig_node('footR_ctl')] = [self.find_jnt_node('footR_jnt'), 1, 1, 0, 1]
        match_ctrls[self.find_rig_node('toebaseR_ctl')] = [self.find_jnt_node('toebaseR_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_con_uplegR_loc')] = [self.find_jnt_node('uplegR_jnt'), 1, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_con_legR_loc')] = [self.find_jnt_node('legR_jnt'), 1, 1, 0, 1]

        # FK leg
        match_ctrls[self.find_rig_node('fk_uplegL_ctl')] = [self.find_jnt_node('uplegL_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_legL_ctl')] = [self.find_jnt_node('legL_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_footL_ctl')] = [self.find_jnt_node('footL_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_toebaseL_ctl')] = [self.find_jnt_node('toebaseL_jnt'), 0, 1, 0, 1]

        match_ctrls[self.find_rig_node('fk_uplegR_ctl')] = [self.find_jnt_node('uplegR_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_legR_ctl')] = [self.find_jnt_node('legR_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_footR_ctl')] = [self.find_jnt_node('footR_jnt'), 0, 1, 0, 1]
        match_ctrls[self.find_rig_node('fk_toebaseR_ctl')] = [self.find_jnt_node('toebaseR_jnt'), 0, 1, 0, 1]

        # Weapons
        match_ctrls[self.find_rig_node('handWeaponL_offset_ctl')] = [self.find_jnt_node('handWeaponL_offset_jnt'), 1, 1, 1, 1]
        match_ctrls[self.find_rig_node('handWeaponR_offset_ctl')] = [self.find_jnt_node('handWeaponR_offset_jnt'), 1, 1, 1, 1]

        match_ctrls[self.find_rig_node('handWeaponL_ctl')] = [self.find_jnt_node('handWeaponL_bind_jnt'), 1, 1, 1, 1]
        match_ctrls[self.find_rig_node('handWeaponR_ctl')] = [self.find_jnt_node('handWeaponR_bind_jnt'), 1, 1, 1, 1]



        for jnt in source_joints:
            cmds.xform(self.find_jnt_node(jnt), ro=[0, 0, 0], a=1)

        # root cog zero out
        cmds.xform(self.find_jnt_node('root_jnt'), t=[0, 0, 0], a=1)
        cmds.xform(self.find_jnt_node('cog_jnt'), t=[0, 103.337, 2.88754], a=1)

        # weapon
        cmds.xform(self.find_jnt_node('handWeaponL_offset_jnt'), t=[6.689, -0.526, 0.0], a=1)
        cmds.xform(self.find_jnt_node('handWeaponR_offset_jnt'), t=[-6.689, 0.526, 0.0], a=1)

        cmds.xform(self.find_jnt_node('handWeaponL_bind_jnt'), t=[0, 0, 0], a=1)
        cmds.xform(self.find_jnt_node('handWeaponR_bind_jnt'), t=[0, 0, 0], a=1)

        # const sets
        if not cmds.objExists('bake_cnst_sets'):
            cmds.sets(em=1, n='bake_cnst_sets')


        bake_ctrls = []
        for ctrl, jnt_value in list(match_ctrls.items()):
            if ctrl is None or jnt_value[0] is None:
                continue
            bake_ctrls.append(ctrl)
            try:
                cnsts = self.constraint_convert(jnt_value[0], ctrl, jnt_value[1], jnt_value[2], jnt_value[3], jnt_value[4])
                for ccnn in cnsts:
                    cmds.sets(ccnn, add='bake_cnst_sets')
            except Exception as e:
                import traceback
                print (traceback.format_exc())

        # PoleVectors
        cnsts = self.constraint_convert(self.find_rig_node('fk_con_armL_pv_loc'), self.find_rig_node('forearmL_ctl'), 1, 0, 0, 0)
        for ccnn in cnsts:
            cmds.sets(ccnn, add='bake_cnst_sets')
        cnsts = self.constraint_convert(self.find_rig_node('fk_con_forearmL_pv_loc'), self.find_rig_node('forearmL_ctl'), 1, 0, 0, 0)
        for ccnn in cnsts:
            cmds.sets(ccnn, add='bake_cnst_sets')
        cnsts = self.constraint_convert(self.find_rig_node('fk_con_armR_pv_loc'), self.find_rig_node('forearmR_ctl'), 1, 0, 0, 0)
        for ccnn in cnsts:
            cmds.sets(ccnn, add='bake_cnst_sets')
        cnsts = self.constraint_convert(self.find_rig_node('fk_con_forearmR_pv_loc'), self.find_rig_node('forearmR_ctl'), 1, 0, 0, 0)
        for ccnn in cnsts:
            cmds.sets(ccnn, add='bake_cnst_sets')

        cnsts = self.constraint_convert(self.find_rig_node('fk_con_uplegL_pv_loc'), self.find_rig_node('legL_ctl'), 1, 0, 0, 0)
        for ccnn in cnsts:
            cmds.sets(ccnn, add='bake_cnst_sets')
        cnsts = self.constraint_convert(self.find_rig_node('fk_con_legL_pv_loc'), self.find_rig_node('legL_ctl'), 1, 0, 0, 0)
        for ccnn in cnsts:
            cmds.sets(ccnn, add='bake_cnst_sets')
        cnsts = self.constraint_convert(self.find_rig_node('fk_con_uplegR_pv_loc'), self.find_rig_node('legR_ctl'), 1, 0, 0, 0)
        for ccnn in cnsts:
            cmds.sets(ccnn, add='bake_cnst_sets')
        cnsts = self.constraint_convert(self.find_rig_node('fk_con_legR_pv_loc'), self.find_rig_node('legR_ctl'), 1, 0, 0, 0)
        for ccnn in cnsts:
            cmds.sets(ccnn, add='bake_cnst_sets')

        for n in self.unlocked:
            try:
                print('Locked: ', n)
                cmds.setAttr(n, e=True, lock=True)
            except:
                print('Resuming lock state failed.')
    

    def unlock_attr(self, dst, attrs):
        for at in attrs:
            if cmds.getAttr(dst+'.'+at, lock=True):
                try:
                    cmds.setAttr(dst+'.'+at, e=True, lock=False)
                except:
                    pass
                else:
                    self.unlocked.append(dst+'.'+at)

    def constraint_convert(self, src, dst, pos, rot, scl, mo):
        print(src, dst)
        cnsts = []
        if pos:
            self.unlock_attr(dst, ['t', 'tx', 'ty', 'tz'])
            cnst = cmds.pointConstraint(src, dst, w=1, mo=mo)
            cnsts.append(cnst)
        if rot:
            self.unlock_attr(dst, ['r', 'rx', 'ry', 'rz'])
            if ('fk_forearmL_ctl' in dst
                or 'fk_forearmR_ctl' in dst
                or 'fk_legL_ctl' in dst
                or 'fk_legR_ctl' in dst):
                cnst = cmds.orientConstraint(src, dst, w=1, mo=mo, sk=['x', 'z'])
                cnsts.append(cnst)
            else:
                cnst = cmds.orientConstraint(src, dst, w=1, mo=mo)
                cnsts.append(cnst)
        if scl:
            self.unlock_attr(dst, ['s', 'sx', 'sy', 'sz'])
            cnst = cmds.scaleConstraint(src, dst, w=1, mo=mo)
            cnsts.append(cnst)

        return cnsts

def get_nodes(master):
    clds = cmds.listRelatives(master, ad=True, pa=True)
    buf = ([] if clds is None else clds)
    if type(master) is list:
        nodes = master + buf
    else:    
        nodes = [master] + buf
    return nodes


def match_constraint(rig_nodes=None, jnt_nodes=None):
    task = Task(cmds.ls(sl=True), rig_nodes=rig_nodes, jnt_nodes=jnt_nodes)
    task.exec_()    

