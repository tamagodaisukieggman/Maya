# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as old_om
import maya.api.OpenMaya as om
import pymel.core as pm

import importlib
from imp import reload
import math
import os
import pprint
import sys
import traceback

from PySide2 import QtWidgets

import tkgfile.utils as tkgfileutls

maya_version = cmds.about(v=1)
# if 2022 <= float(maya_version):
#     importlib.reload(tkgfileutls)
# else:
#     reload(tkgfileutls)

reload(tkgfileutls)
# tfu=tkgfileutls.TkgUtils()

class TkgUtils(object):
    def __init__(self):
        user=os.environ.get('USER')
        self.save_path='C:/Users/{0}/Documents/maya/scripts/getValues/'.format(user)
        self.create_json = tkgfileutls.JsonFile()
        self.sets_dict = {}

    def lock_keyable_attributes(self, lock=True, keyable=True, channelBox=False, showTransform=True):
        sel = cmds.ls(os=1)
        flags={}
        if sel:
            if lock:
                flags['lock']=1
            else:
                flags['lock']=0
            if keyable:
                flags['keyable']=1
            else:
                flags['keyable']=0
            if channelBox:
                flags['channelBox']=1
            else:
                flags['channelBox']=0

            for obj in sel:
                setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;') or None
                if showTransform:
                    setkey_attrs=[u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz', u'v']
                    flags['lock']=0
                    flags['keyable']=1
                    flags['channelBox']=0

                if setkey_attrs:
                    for at in setkey_attrs:
                        try:
                            cmds.setAttr('{0}.{1}'.format(obj, at), **flags)
                        except:
                            pass


    def round_attrs(self, obj=None, attrs=None):
        for at in attrs:
            set_at = '{}.{}'.format(obj, at)
            val = cmds.getAttr(set_at)
            if not val == 0.0:
                if 'e' in str(val):
                    cmds.setAttr(set_at, 0.0)
                    continue

                try:
                    cmds.setAttr(set_at, truncate(round(val, 3), 3))
                except Exception as e:
                    print(traceback.format_exc())

    def round_transform_attrs(self):
        transforms = cmds.ls(os=1, type='transform')

        attrs = ['tx', 'ty', 'tz',
                 'rx', 'ry', 'rz',
                 'sx', 'sy', 'sz']

        joint_attrs = ['pax', 'pay', 'paz',
                       'jox', 'joy', 'joz',
                       'radius']

        for obj in transforms:
            self.round_attrs(obj, attrs)
            if cmds.objectType(obj) == 'joint':
                self.round_attrs(obj, joint_attrs)

    def check_ik_joint_axis(self, aim_axis = 'x', bend_axis = 'y'):
        all_axis = ['x', 'y', 'z']
        sel = cmds.ls(os=1)

        check_up_list = []
        for obj in sel:
            if cmds.objectType(obj) == 'joint':
                for i, cax in enumerate(all_axis):
                    if not aim_axis in cax:
                        axis_val = cmds.getAttr('{}.t{}'.format(obj, cax))
                        if not axis_val == 0.0:
                            if not obj in check_up_list:
                                check_up_list.append(obj)
                            print('{}.t{}'.format(obj, cax), axis_val)

                    if not bend_axis in cax:
                        bend_val = cmds.getAttr('{}.r{}'.format(obj, cax))
                        if not bend_val == 0.0:
                            if not obj in check_up_list:
                                check_up_list.append(obj)
                            print('{}.r{}'.format(obj, cax), bend_val)

                        jo_val = cmds.getAttr('{}.jo{}'.format(obj, cax))
                        if not jo_val == 0.0:
                            if not obj in check_up_list:
                                check_up_list.append(obj)
                            print('{}.jo{}'.format(obj, cax), jo_val)

        cmds.select(check_up_list, r=1)

    def reconcile_joint_rotate_orient(self):
        # reconcile joint rotate and joint orient
        sel = cmds.ls(os=1, type='joint')
        for obj in sel:
            set_wr = cmds.xform(obj, q=1, ro=1, ws=1)
            cmds.setAttr('{}.jo'.format(obj), *(0, 0, 0))
            cmds.xform(obj, ro=set_wr, ws=1, a=1)


    def connect_the_sameAttr_from_channelBox(self):
        sel = cmds.ls(os=1)
        gChannelBoxName = mel.eval('$temp=$gChannelBoxName')
        at_in_cbx = cmds.channelBox(gChannelBoxName, q=1, sma=1)
        if not at_in_cbx:
            return

        if ('rx' in at_in_cbx
            and 'ry' in at_in_cbx
            and 'rz' in at_in_cbx):
                at_in_cbx.remove('rx')
                at_in_cbx.remove('ry')
                at_in_cbx.remove('rz')

                at_in_cbx.append('r')


        if ('tx' in at_in_cbx
            and 'ty' in at_in_cbx
            and 'tz' in at_in_cbx):
                at_in_cbx.remove('tx')
                at_in_cbx.remove('ty')
                at_in_cbx.remove('tz')

                at_in_cbx.append('t')


        if ('sx' in at_in_cbx
            and 'sy' in at_in_cbx
            and 'sz' in at_in_cbx):
                at_in_cbx.remove('sx')
                at_in_cbx.remove('sy')
                at_in_cbx.remove('sz')

                at_in_cbx.append('s')


        for cat in at_in_cbx:
            cmds.connectAttr('{}.{}'.format(sel[0], cat), '{}.{}'.format(sel[1], cat), f=1)


    def connect_offset_attr_from_channelBox(self):
        sel = cmds.ls(os=1)
        gChannelBoxName = mel.eval('$temp=$gChannelBoxName')
        at_in_cbx = cmds.channelBox(gChannelBoxName, q=1, sma=1)
        if not at_in_cbx:
            return

        for i, cat in enumerate(at_in_cbx):
            adl = cmds.createNode('addDoubleLinear', ss=1)

            cmds.connectAttr('{}.{}'.format(sel[0], cat), '{}.input1'.format(adl), f=1)
            cmds.setAttr('{}.input2'.format(adl), cmds.getAttr('{}.{}'.format(sel[1], cat)))

            cmds.connectAttr('{}.output'.format(adl), '{}.{}'.format(sel[1], cat), f=1)


    def constraint_from_local_matrix(self):
        sel = cmds.ls(os=1)
        connect_src = sel[0]
        connect_dst = sel[1]

        mmx = cmds.createNode('multMatrix', ss=1)
        dcmx = cmds.createNode('decomposeMatrix', ss=1)

        src_pa = cmds.listRelatives(connect_src, p=1, f=1)
        if src_pa:
            src_parents = src_pa[0].split('|')[::-1]

        else:
            src_parents = None

        dup = cmds.duplicate(connect_dst, po=1)
        cmds.parent(dup[0], connect_src)
        cmds.setAttr('{}.matrixIn[0]'.format(mmx), *cmds.getAttr('{}.matrix'.format(dup[0])),  type='matrix')
        cmds.delete(dup)

        # cmds.setAttr('{}.matrixIn[1]'.format(mmx), *cmds.getAttr('{}.matrix'.format(connect_dst)),  type='matrix')
        cmds.connectAttr('{}.matrix'.format(connect_src), '{}.matrixIn[1]'.format(mmx), f=1)

        if src_parents:
            for i, p in enumerate(src_parents):
                if '' == p:
                    pass
                else:
                    print('dst', p)
                    # cmds.setAttr('{}.matrixIn[{}]'.format(mmx, i+2), *cmds.getAttr('{}.matrix'.format(p)),  type='matrix')
                    cmds.connectAttr('{}.matrix'.format(p), '{}.matrixIn[{}]'.format(mmx, i+2), f=1)

            next_connect = len(src_parents)

        else:
            next_connect = 0


        dst_pa = cmds.listRelatives(connect_dst, p=1, f=1)
        if dst_pa:
            dst_parents = dst_pa[0].split('|')

        else:
            dst_parents = None

        if dst_parents:
            for j, p in enumerate(dst_parents):
                if '' == p:
                    pass
                else:
                    print('src', p)
                    # cmds.setAttr('{}.matrixIn[{}]'.format(mmx, next_connect+j+1), *cmds.getAttr('{}.matrix'.format(p)),  type='matrix')
                    mmx_num = next_connect+j+2
                    cmds.connectAttr('{}.inverseMatrix'.format(p), '{}.matrixIn[{}]'.format(mmx, mmx_num), f=1)

        # cmds.connectAttr('{}.inverseMatrix'.format(connect_src), '{}.matrixIn[{}]'.format(mmx, mmx_num+1), f=1)
        cmds.connectAttr('{}.matrixSum'.format(mmx), '{}.inputMatrix'.format(dcmx), f=1)
        cmds.connectAttr('{}.outputRotate'.format(dcmx), '{}.r'.format(connect_dst), f=1)
        cmds.connectAttr('{}.outputTranslate'.format(dcmx), '{}.t'.format(connect_dst), f=1)
        cmds.connectAttr('{}.outputScale'.format(dcmx), '{}.s'.format(connect_dst), f=1)
        cmds.connectAttr('{}.outputShear'.format(dcmx), '{}.shear'.format(connect_dst), f=1)



    def select_hierarchy_form_type(self, type='joint'):
        sel=cmds.ls(os=1, dag=1, type=type)
        if sel:
            cmds.select(sel)
            if type == 'mesh':
                cmds.pickWalk(d='up')

    def delete_dag(self):
        dagPose = pm.ls(type="dagPose")
        for i in dagPose:
            pm.delete(i)

    def get_length(self):
        # get joints distance
        def get_distance(objA, objB):
            gObjA = cmds.xform(objA, q=True, t=True, ws=True)
            gObjB = cmds.xform(objB, q=True, t=True, ws=True)

            return math.sqrt(math.pow(gObjA[0]-gObjB[0],2)+math.pow(gObjA[1]-gObjB[1],2)+math.pow(gObjA[2]-gObjB[2],2))

        jointList = cmds.ls(os=1)

        if len(jointList) <= 1:
            return

        length = 0.0
        i = 0
        for jnt in jointList:
            if i == 0:
                pass
            else:
                length += get_distance(jointList[i-1], jnt)
            i += 1

        print('Length:', length)
        return length

    def set_dag_pose(self):
        sel=cmds.ls(os=1)
        if sel:
            cmds.dagPose(save=1, bp=1)

    def get_object_values(self):
        self.get_obj_values={}
        sel=cmds.ls(sl=1, dag=1, type='transform')
        if sel:
            cmds.select(sel)

        for obj in sel:
            listAttrs=cmds.listAttr(obj, k=1)
            for at in listAttrs:
                try:
                    self.get_obj_values['{0}.{1}'.format(obj, at)]=cmds.getAttr('{0}.{1}'.format(obj, at))
                except Exception as e:
                    pass

        if not os.path.isdir(self.save_path):
            os.makedirs(self.save_path)

        self.create_json.write('{0}/get_object_values.json'.format(self.save_path), self.get_obj_values)
        print('Saved:{0}'.format('{0}/get_object_values.json'.format(self.save_path)))

    def set_object_values(self):
        if os.path.isfile('{0}/get_object_values.json'.format(self.save_path)):
            import_values = self.create_json.read('{0}/get_object_values.json'.format(self.save_path))
            for key, value in import_values.items():
                try:
                    cmds.setAttr(key, value)
                except Exception as e:
                    pass

    def tkg_matchTransform(self):
        sel = cmds.ls(os=1)
        if sel:
            for obj in sel[:-1]:
                cmds.matchTransform(obj, sel[-1])

    def correct_skinCluster_names(self):
        skins=cmds.ls(type='skinCluster')
        if skins:
            for skin in skins:
                geo=cmds.skinCluster(skin, q=1, g=1)
                new_skin_name='{0}_skinCluster'.format(geo[0])
                if not cmds.objExists(new_skin_name):
                    cmds.rename(skin, new_skin_name)

    def remove_nss(self, obj):
        nss = ':'.join(obj.split(':')[:-1:])
        if not ':' in nss:
            nss = nss + ':'
            replace_char = []
            replace_char.append(nss)
            replace_char.append('')

        return obj.replace(replace_char[0], replace_char[1])

    def transfer_skinCluster(self, replace_char=None, select_joints=None, weight_copy=None):
        # get infs
        sel = cmds.ls(os=1)
        if not replace_char:
            nss = ':'.join(sel[0].split(':')[:-1:])
            if not ':' in nss:
                nss = nss + ':'
                replace_char = []
                replace_char.append(nss)
                replace_char.append('')

        scn = mel.eval('findRelatedSkinCluster {};'.format(sel[0]))
        infs = cmds.skinCluster(scn, q=1,inf=1)

        if select_joints == 'source':
            cmds.select(infs, r=1)
            return

        replace_infs = [self.remove_nss(inf) for inf in infs]

        if select_joints == 'replaced':
            cmds.select(replace_infs, r=1)
            return

        skinClusterNode = cmds.skinCluster(
            replace_infs, sel[1], tsb=1, bm=0, sm=0, nw=1, wd=0, mi=4, omi=1, dr=4, rui=0,
            name='{}_skinCluster'.format(sel[1])
        )[0]

        cmds.select(sel, r=1)

        if weight_copy:
            cmds.copySkinWeights(surfaceAssociation='closestPoint',
                                 normalize=1,
                                 influenceAssociation=['label', 'closestJoint'],
                                 noMirror=1)

    def iter_transfer_skinCluster(self):
        base_sel = cmds.ls(os=1)
        dst_sel = [self.remove_nss(src_sel) for src_sel in base_sel]
        for i, (s,d) in enumerate(zip(base_sel, dst_sel)):
            if cmds.objExists(d):
                cmds.select([s,d], r=1)
                self.transfer_skinCluster(weight_copy=True)

    def get_poleVector_position(self, startObj=None, middleObj=None, endObj=None, move=20):
        if startObj == None or middleObj == None or endObj == None:
            sel = cmds.ls(os=1)
            try:
                startObj = sel[0]
                middleObj = sel[1]
                endObj = sel[2]
            except Exception as e:
                return
        start = cmds.xform(startObj ,q= 1 ,ws = 1,t =1 )
        mid = cmds.xform(middleObj ,q= 1 ,ws = 1,t =1 )
        end = cmds.xform(endObj ,q= 1 ,ws = 1,t =1 )
        startV = old_om.MVector(start[0] ,start[1],start[2])
        midV = old_om.MVector(mid[0] ,mid[1],mid[2])
        endV = old_om.MVector(end[0] ,end[1],end[2])
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
        matrixM = old_om.MMatrix()
        old_om.MScriptUtil.createMatrixFromList(matrixV , matrixM)
        matrixFn = old_om.MTransformationMatrix(matrixM)
        rot = matrixFn.eulerRotation()

        pvLoc = cmds.spaceLocator(n='{}_poleVecPosLoc'.format(middleObj))
        cmds.xform(pvLoc[0] , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
        cmds.xform(pvLoc[0] , ws = 1 , rotation = ((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0)))
        cmds.select(pvLoc[0])
        cmds.move(move, 0, 0, r=1, os=1, wd=1)
        cmds.select(cl=True)

        # result = {pvLoc:{'translate':(finalV.x , finalV.y ,finalV.z), 'rotate':((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0))}}
        return pvLoc[0]

    def create_null(self):
        sel = cmds.ls(os=1)
        if sel:
            for obj in sel:
                tr = cmds.createNode('transform', n='{}_null'.format(obj.split(':')[-1]))
                cmds.matchTransform(tr, obj)

    def create_offset(self):
        sel = cmds.ls(os=1)
        if sel:
            for obj in sel:
                tr = cmds.createNode('transform', n='{}_p'.format(obj.split(':')[-1]))
                cmds.matchTransform(tr, obj)
                pa = cmds.listRelatives(obj, p=1, pa=1, f=1) or None
                if pa:
                    cmds.parent(tr, pa[0])
                    cmds.parent(obj, tr)
                else:
                    cmds.parent(obj, tr)

    def create_follicles(self, const=None):
        sel = cmds.ls(os=1, fl=1)
        mesh = sel[-1]

        for obj in sel[:-1:]:
            if 'joint' == cmds.objectType(obj):
                fol_shape = obj
            else:
                fol_shape = cmds.listRelatives(obj, s=1)[0] or None

            if not 'follicle' == cmds.objectType(fol_shape):
                fol_shape = cmds.createNode('follicle', ss=1)
                fol = cmds.listRelatives(fol_shape, p=1)[0]
                cmds.matchTransform(fol, obj, pos=1, rot=1)

            if 'follicle' == cmds.objectType(fol_shape):
                fol = cmds.listRelatives(fol_shape, p=1)[0]
                closest_shape = cmds.listRelatives(mesh, s=1)[0] or None
                if 'mesh' == cmds.objectType(closest_shape):
                    cpt = cmds.createNode('closestPointOnMesh', ss=1)
                    cmds.connectAttr(closest_shape+'.outMesh', cpt+'.inMesh', f=1)
                    cmds.connectAttr(closest_shape+'.outMesh', fol_shape+'.inputMesh', f=1)
                    cmds.connectAttr(closest_shape+'.worldMatrix[0]', fol_shape+'.inputWorldMatrix', f=1)

                elif 'nurbsSurface' == cmds.objectType(closest_shape):
                    cpt = cmds.createNode('closestPointOnSurface', ss=1)
                    cmds.connectAttr(closest_shape+'.worldSpace[0]', cpt+'.inputSurface', f=1)
                    cmds.connectAttr(closest_shape+'.worldSpace[0]', fol_shape+'.inputSurface', f=1)

                dcmx = cmds.createNode('decomposeMatrix', ss=1)
                cmds.connectAttr(fol+'.worldMatrix[0]', dcmx+'.inputMatrix', f=1)
                cmds.connectAttr(dcmx+'.outputTranslate', cpt+'.inPosition', f=1)

                cmds.setAttr(fol_shape+'.parameterU', cmds.getAttr(cpt+'.parameterU'))
                cmds.setAttr(fol_shape+'.parameterV', cmds.getAttr(cpt+'.parameterV'))

                cmds.connectAttr(fol_shape+'.outTranslate', fol+'.translate', f=1)
                cmds.connectAttr(fol_shape+'.outRotate', fol+'.rotate', f=1)

                cmds.delete(cpt, dcmx)

            if const:
                cmds.pointConstraint(fol, obj, w=True)

    def create_curve_from_selection(self):
        sel = cmds.ls(os=1, fl=1)
        pts=[cmds.xform(vtx,q=True,ws=True,t=True) for vtx in sel]
        cmds.curve( ep=pts, d=3, n=sel[0]+'_crv')

    def create_loft_surface(self):
        sel = cmds.ls(os=1, fl=1)
        cuR, cuL = sel[0], sel[1]
        Nurbs=cmds.loft( cuR, cuL, ch=False, rn=True)[0]
        cmds.delete(cuR,cuL)
        cmds.rebuildSurface(Nurbs, rt=0, kc=0, fr=0, ch=1, end=1, sv=0, su=0, kr=0, dir=2, kcp=0, tol=0.01, dv=0, du=0, rpo=1)

    def create_collision_with_keepout(self):
        sel = cmds.ls(os=1)

        cmds.select(sel[0], r=1)
        keepout, keepout_shape, keepout_driven = mel.eval('cMuscle_rigKeepOutSel();')

        cmds.select(sel[1], r=1)
        muscle_obj_shape = mel.eval('cMuscle_makeMuscle(0);')[0]

        cmds.select([sel[1], keepout], r=1)
        muscle_obj_shape = mel.eval('cMuscle_keepOutAddRemMuscle(1);')

        cmds.parent(keepout, w=1)
        cmds.parent(sel[0], keepout_driven)

    def create_collision_rig(self):
        sel = cmds.ls(os=1)
        if not sel:
            return
        else:
            ctrl = sel[0]

        col_offset = cmds.createNode('transform', n='{0}_col_offset'.format(ctrl), ss=1)

        # plane
        col_plane_offset = cmds.createNode('transform', n='{0}_col_plane_offset'.format(ctrl), ss=1)
        col_plane_buf = cmds.polyPlane(cuv=2, sy=10, sx=10, h=1, ch=1, w=1, ax=(0, 1, 0))
        cmds.delete(col_plane_buf[0], ch=1)
        cmds.rename(col_plane_buf[0], '{0}_col_plane'.format(ctrl))

        cmds.parent('{0}_col_plane'.format(ctrl), col_plane_offset)

        # ctrls
        col_ctrl_offset = cmds.createNode('transform', n='{0}_col_ctrl_offset'.format(ctrl), ss=1)
        col_ctrl = cmds.spaceLocator(n='{0}_col_ctrl'.format(ctrl))[0]
        col_point_ctrl = cmds.spaceLocator(n='{0}_col_point_ctrl'.format(ctrl))[0]

        cmds.parent(col_point_ctrl, col_ctrl)
        cmds.parent(col_ctrl, col_ctrl_offset)

        # collision
        col_connect = cmds.createNode('transform', n='{0}_col_connect'.format(ctrl), ss=1)
        col_parent = cmds.createNode('transform', n='{0}_col_parent'.format(ctrl), ss=1)

        cmds.parent(col_parent, col_connect)

        # dag parent
        cmds.parent(col_plane_offset, col_offset)
        cmds.parent(col_ctrl_offset, col_offset)
        cmds.parent(col_connect, col_offset)

        # createNodes
        col_plane_dcmx = cmds.createNode('decomposeMatrix', n='{0}_col_plane_dcmx'.format(ctrl), ss=1)
        col_weight_dcmx = cmds.createNode('decomposeMatrix', n='{0}_col_weight_dcmx'.format(ctrl), ss=1)
        col_disable_dcmx = cmds.createNode('decomposeMatrix', n='{0}_col_disable_dcmx'.format(ctrl), ss=1)
        col_enable_dcmx = cmds.createNode('decomposeMatrix', n='{0}_col_enable_dcmx'.format(ctrl), ss=1)

        col_dif_mmx = cmds.createNode('multMatrix', n='{0}_col_dif_mmx'.format(ctrl), ss=1)
        col_disable_mmx = cmds.createNode('multMatrix', n='{0}_col_disable_mmx'.format(ctrl), ss=1)
        col_enable_mmx = cmds.createNode('multMatrix', n='{0}_col_enable_mmx'.format(ctrl), ss=1)

        col_weight_cdn = cmds.createNode('condition', n='{0}_col_weight_cdn'.format(ctrl), ss=1)

        col_switch_pbn = cmds.createNode('pairBlend', n='{0}_col_switch_pbn'.format(ctrl), ss=1)

        col_plane_cpom = cmds.createNode('closestPointOnMesh', n='{0}_col_plane_cpom'.format(ctrl), ss=1)

        col_plane_vpd_z = cmds.createNode('vectorProduct', n='{0}_col_plane_vpd_z'.format(ctrl), ss=1)
        col_plane_vpd_x = cmds.createNode('vectorProduct', n='{0}_col_plane_vpd_x'.format(ctrl), ss=1)

        col_plane_fbfm = cmds.createNode('fourByFourMatrix', n='{0}_col_plane_fbfm'.format(ctrl), ss=1)

        # setAttr
        cmds.setAttr("{0}.operation".format(col_plane_vpd_z), 2)
        cmds.setAttr("{0}.input1X".format(col_plane_vpd_z), 1)
        cmds.setAttr("{0}.normalizeOutput".format(col_plane_vpd_z), 1)

        cmds.setAttr("{0}.operation".format(col_plane_vpd_x), 2)
        cmds.setAttr("{0}.normalizeOutput".format(col_plane_vpd_x), 1)

        cmds.setAttr("{0}.operation".format(col_weight_cdn), 2)
        cmds.setAttr("{0}.colorIfTrueR".format(col_weight_cdn), 1)
        cmds.setAttr("{0}.colorIfFalseR".format(col_weight_cdn), 0)

        # connect
        cmds.connectAttr('{0}.worldMatrix[0]'.format(col_point_ctrl), '{0}.inputMatrix'.format(col_plane_dcmx), f=1)

        cmds.connectAttr('{0}.outputTranslate'.format(col_plane_dcmx), '{0}.inPosition'.format(col_plane_cpom), f=1)
        cmds.connectAttr('{0}.outMesh'.format('{0}_col_planeShape'.format(ctrl)), '{0}.inMesh'.format(col_plane_cpom), f=1)
        cmds.connectAttr('{0}.worldMatrix[0]'.format('{0}_col_plane'.format(ctrl)), '{0}.inputMatrix'.format(col_plane_cpom), f=1)

        cmds.connectAttr('{0}.positionX'.format(col_plane_cpom), '{0}.in30'.format(col_plane_fbfm), f=1)
        cmds.connectAttr('{0}.positionY'.format(col_plane_cpom), '{0}.in31'.format(col_plane_fbfm), f=1)
        cmds.connectAttr('{0}.positionZ'.format(col_plane_cpom), '{0}.in32'.format(col_plane_fbfm), f=1)

        cmds.connectAttr('{0}.normal'.format(col_plane_cpom), '{0}.input2'.format(col_plane_vpd_z), f=1)

        cmds.connectAttr('{0}.normal'.format(col_plane_cpom), '{0}.input1'.format(col_plane_vpd_x), f=1)
        cmds.connectAttr('{0}.output'.format(col_plane_vpd_z), '{0}.input2'.format(col_plane_vpd_x), f=1)

        cmds.connectAttr('{0}.normalX'.format(col_plane_cpom), '{0}.in10'.format(col_plane_fbfm), f=1)
        cmds.connectAttr('{0}.normalY'.format(col_plane_cpom), '{0}.in11'.format(col_plane_fbfm), f=1)
        cmds.connectAttr('{0}.normalZ'.format(col_plane_cpom), '{0}.in12'.format(col_plane_fbfm), f=1)

        cmds.connectAttr('{0}.outputX'.format(col_plane_vpd_z), '{0}.in20'.format(col_plane_fbfm), f=1)
        cmds.connectAttr('{0}.outputY'.format(col_plane_vpd_z), '{0}.in21'.format(col_plane_fbfm), f=1)
        cmds.connectAttr('{0}.outputZ'.format(col_plane_vpd_z), '{0}.in22'.format(col_plane_fbfm), f=1)

        cmds.connectAttr('{0}.outputX'.format(col_plane_vpd_x), '{0}.in00'.format(col_plane_fbfm), f=1)
        cmds.connectAttr('{0}.outputY'.format(col_plane_vpd_x), '{0}.in01'.format(col_plane_fbfm), f=1)
        cmds.connectAttr('{0}.outputZ'.format(col_plane_vpd_x), '{0}.in02'.format(col_plane_fbfm), f=1)

        cmds.connectAttr('{0}.output'.format(col_plane_fbfm), '{0}.matrixIn[0]'.format(col_dif_mmx), f=1)
        cmds.connectAttr('{0}.worldInverseMatrix[0]'.format(col_point_ctrl), '{0}.matrixIn[1]'.format(col_dif_mmx), f=1)

        cmds.connectAttr('{0}.matrixSum'.format(col_dif_mmx), '{0}.inputMatrix'.format(col_weight_dcmx), f=1)

        cmds.connectAttr('{0}.outputTranslateY'.format(col_weight_dcmx), '{0}.firstTerm'.format(col_weight_cdn), f=1)

        cmds.connectAttr('{0}.outColorR'.format(col_weight_cdn), '{0}.weight'.format(col_switch_pbn), f=1)

        cmds.connectAttr('{0}.matrix'.format(col_ctrl), '{0}.matrixIn[0]'.format(col_disable_mmx), f=1)
        cmds.connectAttr('{0}.matrix'.format(col_ctrl_offset), '{0}.matrixIn[1]'.format(col_disable_mmx), f=1)

        cmds.connectAttr('{0}.matrixSum'.format(col_dif_mmx), '{0}.matrixIn[0]'.format(col_enable_mmx), f=1)
        cmds.connectAttr('{0}.matrix'.format(col_ctrl), '{0}.matrixIn[1]'.format(col_enable_mmx), f=1)
        cmds.connectAttr('{0}.matrix'.format(col_ctrl_offset), '{0}.matrixIn[2]'.format(col_enable_mmx), f=1)

        cmds.connectAttr('{0}.matrixSum'.format(col_disable_mmx), '{0}.inputMatrix'.format(col_disable_dcmx), f=1)
        cmds.connectAttr('{0}.matrixSum'.format(col_enable_mmx), '{0}.inputMatrix'.format(col_enable_dcmx), f=1)

        cmds.connectAttr('{0}.outputRotate'.format(col_disable_dcmx), '{0}.inRotate1'.format(col_switch_pbn), f=1)
        cmds.connectAttr('{0}.outputTranslate'.format(col_disable_dcmx), '{0}.inTranslate1'.format(col_switch_pbn), f=1)

        cmds.connectAttr('{0}.outputRotate'.format(col_enable_dcmx), '{0}.inRotate2'.format(col_switch_pbn), f=1)
        cmds.connectAttr('{0}.outputTranslate'.format(col_enable_dcmx), '{0}.inTranslate2'.format(col_switch_pbn), f=1)

        cmds.connectAttr('{0}.outRotate'.format(col_switch_pbn), '{0}.rotate'.format(col_connect), f=1)
        cmds.connectAttr('{0}.outTranslate'.format(col_switch_pbn), '{0}.translate'.format(col_connect), f=1)


    def create_poleVector_guide(self):
        sel = cmds.ls(os=1)

        dcmx_1 = cmds.createNode('decomposeMatrix', ss=1)
        dcmx_2 = cmds.createNode('decomposeMatrix', ss=1)

        cmds.connectAttr(sel[0]+'.worldMatrix[0]', dcmx_1+'.inputMatrix', f=1)
        cmds.connectAttr(sel[1]+'.worldMatrix[0]', dcmx_2+'.inputMatrix', f=1)

        shape = cmds.listRelatives(sel[2], s=1)[0] or None
        cmds.connectAttr(dcmx_1+'.outputTranslate', shape+'.controlPoints[0]', f=1)

        cvs = cmds.ls(sel[2]+'.cv[*]', fl=1)
        for v in range(len(cvs)-1):
            cmds.connectAttr(dcmx_2+'.outputTranslate', shape+'.controlPoints[{}]'.format(str(v+1)), f=1)

        cmds.setAttr(shape+'.template', 1)

    def create_dynamicJointswithIk(self):
        """
        jointを選択 > 最後にカーブ選択
        """
        sel = cmds.ls(os=1)

        jointHierarchy = sel[:-1:]
        driverCurve = sel[-1]
        driverCurveShape = cmds.listRelatives(driverCurve, shapes=True)[0]
        nucleus = None

        outputCurve = '{0}_{1}'.format(driverCurve, 'output')
        cmds.duplicate(driverCurve, n=outputCurve)
        hairSystem = cmds.createNode( 'hairSystem', n='{0}_{1}'.format(driverCurve, 'hairSystemShape') )
        follicle = cmds.createNode( 'follicle', n='{0}_{1}'.format(driverCurve, 'follicleShape') )
        cmds.setAttr('{0}.restPose'.format(follicle), 1)
        cmds.setAttr('{0}.active'.format(hairSystem), 1)

        # Rebuild driverCurve
        restCurve = '{0}_{1}'.format(driverCurve, 'restCurve')
        cmds.duplicate(driverCurve, n=restCurve)

        # Connect curves to follicle
        cmds.connectAttr((driverCurve + '.worldMatrix[0]'), (follicle + '.startPositionMatrix'))
        cmds.connectAttr((restCurve + '.local'), (follicle + '.startPosition'))

        # Connect follicle to output curve
        cmds.connectAttr((follicle + '.outCurve'), (outputCurve + '.create'))

        # Connect time to hair system and nucleus
        if not nucleus:
            nucleus = cmds.createNode( 'nucleus', n='{0}_{1}'.format(driverCurve, 'nucleus'))
            cmds.connectAttr('time1.outTime', (nucleus + '.currentTime'))
        cmds.connectAttr('time1.outTime', (hairSystem + '.currentTime'))

        # Connect hair system and nucleus together
        nucleus_connections_ia = cmds.listConnections('{0}.inputActive'.format(nucleus))
        nucleus_connections_ias = cmds.listConnections('{0}.inputActiveStart'.format(nucleus))
        if nucleus_connections_ia == None:
            con = 0
        else:
            con = len(nucleus_connections_ia)
        cmds.connectAttr((hairSystem + '.currentState'), (nucleus + '.inputActive[{0}]'.format(str(con))))
        cmds.connectAttr((hairSystem + '.startState'), (nucleus + '.inputActiveStart[{0}]'.format(str(con))))
        cmds.connectAttr((nucleus + '.outputObjects[0]'), (hairSystem + '.nextState'))
        cmds.connectAttr((nucleus + '.startFrame'), (hairSystem + '.startFrame'))

        # Connect hair system to follicle
        cmds.connectAttr((hairSystem + '.outputHair[0]'), (follicle + '.currentPosition'))
        cmds.connectAttr((follicle + '.outHair'), (hairSystem + '.inputHair[0]'))

        splineIK = cmds.ikHandle(sj=jointHierarchy[0], ee=jointHierarchy[-1], sol='ikSplineSolver', c=outputCurve, ccv=False, p=2, w=.5, n='{0}_dyn_ikHandle'.format(jointHierarchy[0]))

        ctl = hairSystem+'_ctl'
        cmds.curve(d=1,p=[(0,0,1),(0,0.5,0.866025),(0,0.866025,0.5),(0,1,0),(0,0.866025,-0.5),(0,0.5,-0.866025),(0,0,-1),(0,-0.5,-0.866025),(0,-0.866025,-0.5),(0,-1,0),(0,-0.866025,0.5),(0,-0.5,0.866025),(0,0,1),(0.707107,0,0.707107),(1,0,0),(0.707107,0,-0.707107),(0,0,-1),(-0.707107,0,-0.707107),(-1,0,0),(-0.866025,0.5,0),(-0.5,0.866025,0),(0,1,0),(0.5,0.866025,0),(0.866025,0.5,0),(1,0,0),(0.866025,-0.5,0),(0.5,-0.866025,0),(0,-1,0),(-0.5,-0.866025,0),(-0.866025,-0.5,0),(-1,0,0),(-0.707107,0,0.707107),(0,0,1)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32],n=ctl)

        ctl_gp = ctl+'_gp'
        cmds.createNode('transform', n=ctl_gp, ss=1)

        cmds.parent(ctl, ctl_gp)

        cmds.matchTransform(ctl_gp, jointHierarchy[0], pos=1, rot=1)

        # cmds.setAttr("{0}.active".format(hairSystem), 1)
        cmds.setAttr("{0}.startDirection".format(follicle), 1)

        # ikOptions
        cmds.addAttr(ctl, ln='ikOptions', keyable=True, at='enum', en='____________')
        cmds.setAttr('{0}.ikOptions'.format(ctl), l=1)
        cmds.addAttr(ctl, ln='roll', keyable=True, at='float', dv=0.0)
        cmds.addAttr(ctl, ln='twist',  keyable=True, at='float', dv=0.0)
        # dynamicOptions
        cmds.addAttr(ctl, ln='dynamicOptions', keyable=True, at='enum', en='____________')
        cmds.setAttr('{0}.dynamicOptions'.format(ctl), l=1)
        # Add attributes to controller for the dynamics
        cmds.addAttr(ctl, min=0, ln='stiffness', max=1, keyable=True, at='double', dv=0.15)
        cmds.addAttr(ctl, min=0, ln='lengthFlex', max=1, keyable=True, at='double', dv=0)
        cmds.addAttr(ctl, ln="pointLock", en="No Attach:Base:Tip:BothEnds:", at="enum", k=1)
        cmds.setAttr('{0}.pointLock'.format(ctl), 1)
        cmds.addAttr(ctl, min=0, ln="drag", max=1, keyable=True, at='double', dv=.05)
        cmds.addAttr(ctl, min=0, ln='friction', max=1, keyable=True, at='double', dv=0.5)
        cmds.addAttr(ctl, min=0, ln="gravity", max=10, keyable=True, at='double', dv=1)
        cmds.addAttr(ctl, min=0, ln="turbulenceStrength", max=1, keyable=True, at='double', dv=0)
        cmds.addAttr(ctl, min=0, ln="turbulenceFrequency", max=2, keyable=True, at='double', dv=0.2)
        cmds.addAttr(ctl, min=0, ln="turbulenceSpeed", max=2, keyable=True, at='double', dv=0.2)
        cmds.addAttr(ctl, min=0, ln="damp", max=10, keyable=True, at='double', dv=0, k=1)
        cmds.addAttr(ctl, min=0, ln="mass", max=10, keyable=True, at='double', dv=1.0, k=1)
        cmds.addAttr(ctl, min=0, ln="attractionDamp", max=1, keyable=True, at='double', dv=0, k=1)
        cmds.addAttr(ctl, min=0, ln="startCurveAttract", max=1, keyable=True, at='double', dv=0, k=1)
        cmds.addAttr(ctl, min=0, ln="motionDrag", max=1, keyable=True, at='double', dv=0, k=1)
        # collisions
        cmds.addAttr(ctl, ln='collisionOptions', keyable=True, at='enum', en='____________')
        cmds.setAttr('{0}.collisionOptions'.format(ctl), l=1)
        cmds.addAttr(ctl, ln="useNucleusSolver", keyable=True, at='bool')
        cmds.addAttr(ctl, min=0, ln="stickiness", keyable=True, at='double', dv=0.0, k=1)
        cmds.addAttr(ctl, ln="solverDisplay", en="Off:Collision Thickness:Self Collision Thickness:", at="enum", k=1)
        cmds.addAttr(ctl, ln="collideWidthOffset", keyable=True, at='double', dv=0, k=1)

        cmds.connectAttr(ctl + ".roll", splineIK[0] + ".roll", f=1)
        cmds.connectAttr(ctl + ".twist", splineIK[0] + ".twist", f=1)
        #Connect attributes on the controller sphere to the follicle node
        cmds.connectAttr(ctl + ".pointLock", follicle + ".pointLock", f=1)
        #Connect attribute on the controller sphere to the hair system node
        cmds.connectAttr(ctl + ".stiffness", hairSystem + ".stiffness", f=1)
        cmds.connectAttr(ctl + ".lengthFlex", hairSystem + ".lengthFlex", f=1)
        cmds.connectAttr(ctl + ".damp", hairSystem + ".damp", f=1)
        cmds.connectAttr(ctl + ".drag", hairSystem + ".drag", f=1)
        cmds.connectAttr(ctl + ".friction", hairSystem + ".friction", f=1)
        cmds.connectAttr(ctl + ".mass", hairSystem + ".mass", f=1)
        cmds.connectAttr(ctl + ".gravity", hairSystem + ".gravity", f=1)
        cmds.connectAttr(ctl + ".turbulenceStrength", hairSystem + ".turbulenceStrength", f=1)
        cmds.connectAttr(ctl + ".turbulenceFrequency", hairSystem + ".turbulenceFrequency", f=1)
        cmds.connectAttr(ctl + ".turbulenceSpeed", hairSystem + ".turbulenceSpeed", f=1)
        cmds.connectAttr(ctl + ".attractionDamp", hairSystem + ".attractionDamp", f=1)
        cmds.connectAttr(ctl + ".startCurveAttract", hairSystem + ".startCurveAttract", f=1)
        cmds.connectAttr(ctl + ".motionDrag", hairSystem + ".motionDrag", f=1)
        # collisions
        cmds.connectAttr(ctl + ".useNucleusSolver", hairSystem + ".active", f=1)
        cmds.connectAttr(ctl + ".stickiness", hairSystem + ".stickiness", f=1)
        cmds.connectAttr(ctl + ".solverDisplay", hairSystem + ".solverDisplay", f=1)
        cmds.connectAttr(ctl + ".collideWidthOffset", hairSystem + ".collideWidthOffset", f=1)

        cmds.parent(driverCurve, ctl)

    def create_rigidBody(self):
        sel = cmds.ls(os=1)

        selection = sel[:-1:]
        nucleus = sel[-1]
        if selection and nucleus:
            if 'nucleus' == cmds.objectType(nucleus) and cmds.objExists(nucleus):
                for obj in selection:
                    if cmds.objExists(obj):
                        rigidBody = 'rigidBody_{0}'.format(obj)
                        if not cmds.objExists(rigidBody):
                            cmds.select(obj, r=1)
                            rigidBodies = cmds.ls(type='nRigid')
                            if rigidBodies == []:
                                collide = mel.eval('makeCollideNCloth;')
                            else:
                                sh = cmds.listRelatives(obj, s=1)
                                if sh:
                                    mesh_shape = sh[0]
                                    listConnections = cmds.listConnections('{0}.worldMesh[0]'.format(mesh_shape), d=1)

                                collide = cmds.ls(cmds.listRelatives(listConnections, s=1), type='nRigid')

                                if collide:
                                    cmds.connectAttr('{0}.currentState'.format(collide[0]), '{0}.inputPassive[0]'.format(nucleus), f=1)
                                    cmds.connectAttr('{0}.startState'.format(collide[0]), '{0}.inputPassiveStart[0]'.format(nucleus), f=1)
                                else:
                                    mel.eval('string $nucleus = "{0}";'.format(nucleus))
                                    mel.eval('setActiveNucleusNode( $nucleus );')
                                    collide = mel.eval('makeCollideNCloth;')

                            if collide == []:
                                continue
                            else:
                                cmds.setAttr('{0}.thickness'.format(collide[0]), 0)
                                cmds.rename(cmds.listRelatives(collide[0], p=1)[0], rigidBody)
                        else:
                            cmds.warning('"{0}" is already exists.'.format(rigidBody))
        else:
            cmds.warning('Set "selection" and "nucleus".')

    def create_emitters_from_selection(self):
        sel = cmds.ls(os=1, fl=1)
        for obj in sel:
            cmds.select(obj, r=1)
            em = mel.eval('emitter -type omni -r 0 -sro 0 -nuv 0 -cye none -cyi 1 -spd 1 -srn 0 -nsp 1 -tsp 0 -mxd 0 -mnd 0 -dx 1 -dy 0 -dz 0 -sp 0 ;')

    def create_closest_points_sets(self):
        def getClosestVertex(mayaMesh,pos=[0,0,0]):
            mVector = om.MVector(pos)#using MVector type to represent position
            selectionList = om.MSelectionList()
            selectionList.add(mayaMesh)
            dPath= selectionList.getDagPath(0)
            mMesh=om.MFnMesh(dPath)
            ID = mMesh.getClosestPoint(om.MPoint(mVector),space=om.MSpace.kWorld)[1] #getting closest face ID
            list=cmds.ls( cmds.polyListComponentConversion (mayaMesh+'.f['+str(ID)+']',ff=True,tv=True),flatten=True)#face's vertices list
            #setting vertex [0] as the closest one
            d=mVector-om.MVector(cmds.xform(list[0],t=True,ws=True,q=True))
            smallestDist2=d.x*d.x+d.y*d.y+d.z*d.z #using distance squared to compare distance
            closest=list[0]
            #iterating from vertex [1]
            for i in range(1,len(list)) :
                d=mVector-om.MVector(cmds.xform(list[i],t=True,ws=True,q=True))
                d2=d.x*d.x+d.y*d.y+d.z*d.z
                if d2<smallestDist2:
                    smallestDist2=d2
                    closest=list[i]
            return closest

        # 別オブジェクトからClosestPointを探る
        sel = cmds.ls(os=1)
        closest_sets = '{}_{}_closest_sets'.format(sel[0], sel[1])
        if not cmds.objExists(closest_sets):
            cmds.sets(em=1, n=closest_sets)

        cmds.select(sel[0], r=1)
        cmds.ConvertSelectionToVertices()
        vtxs = cmds.ls(os=1, fl=1)

        for v in vtxs:
            closest = getClosestVertex(sel[1], cmds.xform(v, q=1, t=1, ws=1))
            if cmds.objExists(closest_sets):
                cmds.sets('{}'.format(closest), add=closest_sets)

        cmds.select(sel, r=1)


    def getUParam(self, pnt = [], crv = None):
        point = old_om.MPoint(pnt[0],pnt[1],pnt[2])
        curveFn = old_om.MFnNurbsCurve(self.getDagPath(crv))
        paramUtill=old_om.MScriptUtil()
        paramPtr=paramUtill.asDoublePtr()
        isOnCurve = curveFn.isPointOnCurve(point)
        if isOnCurve == True:

            curveFn.getParamAtPoint(point , paramPtr,0.001,old_om.MSpace.kObject )
        else :
            point = curveFn.closestPoint(point,paramPtr,0.001,old_om.MSpace.kObject)
            curveFn.getParamAtPoint(point , paramPtr,0.001,old_om.MSpace.kObject )

        param = paramUtill.getDouble(paramPtr)
        return param

    def getDagPath(self, objectName):

        if isinstance(objectName, list)==True:
            oNodeList=[]
            for o in objectName:
                selectionList = old_om.MSelectionList()
                selectionList.add(o)
                oNode = old_om.MDagPath()
                selectionList.getDagPath(0, oNode)
                oNodeList.append(oNode)
            return oNodeList
        else:
            selectionList = old_om.MSelectionList()
            selectionList.add(objectName)
            oNode = old_om.MDagPath()
            selectionList.getDagPath(0, oNode)
            return oNode

    def create_crv_attach_locs(self):
        sel = cmds.ls(os=1)
        if not sel:
            return
        shape = cmds.listRelatives(sel[-1], s=1)
        if shape:
            if 'nurbsCurve' == cmds.objectType(shape[0]):
                attach_crv = sel[-1]
                if 1 == len(sel):
                    crv_cv = cmds.ls('{}.cv[*]'.format(attach_crv), fl=1)
                elif 1 < len(sel):
                    crv_cv = cmds.ls(sel[:-1:])
            else:
                return

        locs = []
        for i, cv in enumerate(crv_cv):
            param = self.getUParam(pnt=cmds.xform(cv, q=1, t=1, ws=1), crv=attach_crv)
            shape = cmds.listRelatives(attach_crv, s=1) or None
            if not shape:
                continue
            poci = cmds.createNode('pointOnCurveInfo', n='{}_poci_{}'.format(attach_crv, str(i).zfill(3)), ss=1)
            loc = cmds.spaceLocator(n='{}_{}_loc'.format(attach_crv, str(i).zfill(3)))
            cmds.connectAttr('{}.worldSpace[0]'.format(shape[0]), '{}.inputCurve'.format(poci), f=1)
            cmds.connectAttr('{}.position'.format(poci), '{}.translate'.format(loc[0]), f=1)

            cmds.setAttr('{}.parameter'.format(poci), param)

            locs.append(loc[0])

        return locs

    def create_joints_into_under_objects(self):
        sel = cmds.ls(os=1, fl=1)
        for obj in sel:
            jt = cmds.createNode('joint', ss=1)
            cmds.matchTransform(jt, obj)
            cmds.parent(jt, obj)

    def setFilterScript(self, name):

    	# We first test for plug-in object sets.
    	try:
    		apiNodeType = cmds.nodeType(name, api=True)
    	except RuntimeError:
    		return False

    	if apiNodeType == "kPluginObjectSet":
    		return True

    	  # We do not need to test is the object is a set, since that test
    	# has already been done by the outliner
    	try:
    		nodeType = cmds.nodeType(name)
    	except RuntimeError:
    		return False

    	# We do not want any rendering sets
    	if nodeType == "shadingEngine":
    		return False

    	# if the object is not a set, return false
    	if not (nodeType == "objectSet" or
    			nodeType == "textureBakeSet" or
    			nodeType == "vertexBakeSet" or
    			nodeType == "character"):
    		return False

    	# We also do not want any sets with restrictions
    	restrictionAttrs = ["verticesOnlySet", "edgesOnlySet", "facetsOnlySet", "editPointsOnlySet", "renderableOnlySet"]
    	if any(cmds.getAttr("{0}.{1}".format(name, attr)) for attr in restrictionAttrs):
    		return False

    	# Do not show layers
    	if cmds.getAttr("{0}.isLayer".format(name)):
    		return False

    	# Do not show bookmarks
    	annotation = cmds.getAttr("{0}.annotation".format(name))
    	if annotation == "bookmarkAnimCurves":
    		return False

    	# Whew ... we can finally show it
    	return True


    def getOutlinerSets(self):
    	return [name for name in cmds.ls(sets=True) if self.setFilterScript(name)]

    def get_sets_objects_recurse(self, sets_dict, object_sets):
        object_sets = list(set(object_sets))
        object_sets.sort()
        for p_node in object_sets:
            c_nodes = cmds.sets(p_node, q=1, no=1)
            if c_nodes:
                c_nodes = list(set(c_nodes))
                c_nodes.sort()
                sets_dict[p_node] = c_nodes
                self.get_sets_objects_recurse(sets_dict, c_nodes)

    def get_sets_objects(self):
        # Test it out
        object_sets = self.getOutlinerSets()
        self.get_sets_objects_recurse(self.sets_dict, object_sets)
        return self.sets_dict

    def set_saved_sets(self, sets_dict=None):
        if sets_dict:
            self.sets_dict = sets_dict

        for sets_node, set_objects in self.sets_dict.items():
            cmds.sets(em=1, n=sets_node)

        for sets_node, set_objects in self.sets_dict.items():
            for s_object in set_objects:
                if cmds.objExists(s_object):
                    cmds.sets(s_object, add=sets_node)

    def copy_curve_settings_to_clipboard(self):
        sel = cmds.ls(os=True)
        if not sel:
            return

        get_points = {}
        for obj in sel:
            cvs = cmds.ls(obj+'.cv[*]', fl=True)
            points = [cmds.pointPosition(cv, w=True) for cv in cvs]
            shape = cmds.listRelatives(obj, s=True) or list()
            degree = 1
            periodic = False
            if shape:
                degree = cmds.getAttr(shape[0]+'.degree')
                form = cmds.getAttr(shape[0]+'.form')
                if form == 2:
                    periodic = True

            get_points[obj] = {}
            get_points[obj]['points'] = points
            get_points[obj]['degree'] = degree
            get_points[obj]['knot'] = create_knots(obj)
            get_points[obj]['periodic'] = periodic


        str_get_points = pprint.pformat(get_points, width=150)
        # print('get_points = {}'.format(str_get_points))
        function_text = '''
controllers = []
for n, points in get_points.items():
    curve_settings = {}
    curve_settings['d'] = points['degree']
    curve_settings['p'] = points['points']
    curve_settings['k'] = points['knot']
    crv = cmds.curve(**curve_settings)
    if points['periodic']:
        cmds.closeCurve(crv, ch=True, ps=0, rpo=True, bb=0.5, bki=False, p=0.1)
    controllers.append(crv)
        '''

        text = 'get_points = ' + str_get_points + '\n' + function_text

        copy_to_clipboard(text)

    def merge_curves(self):
        sel = cmds.ls( os=True )
        # cmds.select(sel[0], r=True)
        # cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        if not sel:
            return
        shape = cmds.listRelatives(sel[0], s=True, f=True) or list()
        # cmds.select(sel[0], r=True)
        # mel.eval('channelBoxCommand -freezeAll;')
        if shape:
            for sh in shape:
                cmds.parent(sh, sel[1], s=True, r=True)

        cmds.delete(sel[0])

        cmds.select(sel[1], r=True)

def set_liw(liw_sts=False):
    mesh = cmds.ls(os=True)
    if mesh:
        mesh = mesh[0]
    else:
        return

    # Get the skin cluster of the mesh
    skin_cluster = cmds.ls(cmds.listHistory(mesh), type='skinCluster')[0]

    # Get the influences (joints) affecting the skin
    influences = cmds.skinCluster(skin_cluster, query=True, inf=True)

    for inf in influences:
        cmds.setAttr(inf + '.liw', liw_sts)

# Copy to Clipboard
def copy_to_clipboard(text):
    cb = QtWidgets.QApplication.clipboard()
    cb.setText(text)

# Curve Knots
def create_knots(crv):
    knots = mel.eval('string $cInfo = `arclen -ch 1 {}`;getAttr($cInfo+".knots[*]");'.format(crv))
    mel.eval('delete $cInfo;')
    return knots

# round value
def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n
