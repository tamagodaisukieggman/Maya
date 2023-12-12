# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

import codecs
from collections import OrderedDict
from datetime import datetime
import getpass
import json
import os
import re
import traceback

import pdb

# --How to use--
# mtk3d.maya.rig.refresh import common as refresh_common
# reload(refresh_common)
#
# rcr=refresh_common.RefreshScene()
# objects=cmds.ls(os=1)
# rcr.objectValues(objects=objects, export_or_import='export', file_path=None, only_list=None)
#
# rcr=refresh_common.RefreshScene(ctrl_set=['ply00_m_000_000:CtrlSet', 'mob00_m_000_000:CtrlSet'])
# rcr.main()

# script source
from mtk3d.maya.rig.ikfk.ikfkmatch import common as ikfk_common
reload(ikfk_common)

# atomImportExport
if cmds.pluginInfo('atomImportExport', q=True, l=True) == False:
    cmds.loadPlugin("atomImportExport")

dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
dir_path = dir.replace('\\', '/')

logFolder = '{}/log/'.format(dir_path)

default_refresh_file_path='Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/refresh/data/anm_ply00_m_000_anim.json'

class RefreshScene(object):
    def __init__(self, namespace=None, ctrl_set=None, file_path=default_refresh_file_path, optimize=None, ikfk_match=True):
        u"""Initialize

        param:
        """

        self.ctrl_set=ctrl_set
        self.file_path=file_path
        self.optimize=optimize
        self.namespace=namespace
        self.ikfk_match=ikfk_match

    def main(self, current_scene=None, save_path=None, bat_mode=None):
        cmds.undoInfo(openChunk=True)
        cycleCheck_sts = cmds.cycleCheck(q=1, e=1)
        autoKeyframe_sts = cmds.autoKeyframe(q=True, st=True)

        cmds.cycleCheck(e=0)
        cmds.autoKeyframe(st=0)

        try:
            cmds.refresh(su=1)
            self.bakes()
            cmds.refresh(su=0)
        except Exception as e:
            print(e)
            cmds.refresh(su=0)

        cmds.cycleCheck(e=cycleCheck_sts)
        cmds.autoKeyframe(st=autoKeyframe_sts)

        print(u'このシーンはRefreshされました。')
        cmds.undoInfo(closeChunk=True)

        if bat_mode:
            fbxspl = current_scene.split('/')
            fname = fbxspl[-1].split('.')[0]

            cmds.file(rn='{0}/{1}.ma'.format(save_path, fname))
            cmds.file(f=1, save=1)

            print('Saved:{0}/{1}.ma'.format(save_path, fname))

    def bakes(self):
        for c_set in self.ctrl_set:
            print(u'{0}のリフレッシュが開始されました。'.format(c_set))
            cmds.select(c_set, r=1, ne=1)
            self.ctrls = cmds.pickWalk(d='down')

            splns=c_set.split(':')
            self.namespace=':'.join(splns[:-1])

            self.set_init_space()
            print(u'{0}のコントローラがワールドに放たれました。'.format(c_set))
            self.objectValues(objects=self.ctrls, export_or_import='import', file_path=self.file_path)
            self.addkey_of_user_define()
            self.bake_ctrls()
            cmds.delete(self.bake_locs_grp)
            print(u'{0}のコントローラが初期状態でベイクされました。'.format(c_set))
            self.corrective_bakes_for_biped()
            print(u'{0}のコントローラでイレギュラーの処理をしました。'.format(c_set))

            if self.ikfk_match:
                print(u'{0}のIKFKマッチを行っています。'.format(c_set))
                ik2fk_fk2ik=ikfk_common.IKFKMatchMan(namespace=self.namespace)
                ik2fk_fk2ik.main()
                print(u'{0}のIKFKマッチが終わりました。'.format(c_set))

            print(u'{0}のリフレッシュが終わりました。'.format(c_set))

        self.cleaning()

    def objectValues(self, objects=None, export_or_import='export', file_path=None, only_list=None):
        create_json = JsonFile()
        if export_or_import == 'export':
            objects.sort()

            objects_values = OrderedDict()
            for obj in objects:
                listAttrs = cmds.listAttr(obj, k=1)
                if listAttrs:
                    listAttrs.sort()
                    buf_attrs = []
                    for at in listAttrs:
                        new_obj=obj.split(':')[-1]
                        try:
                            objects_values['{0}.{1}'.format(new_obj, at)] = cmds.getAttr('{0}.{1}'.format(obj, at))
                        except:
                            pass
            if not file_path:
                file_path = self.fileDialog_export()
            if not file_path:
                return
            dirname, basename = os.path.split(file_path)
            save_file_path = '{0}/{1}'.format(dirname, basename)
            create_json.write('{0}'.format(save_file_path), objects_values)

            return save_file_path

        elif export_or_import == 'import':
            if not file_path:
                file_path = self.fileDialog_import()
            if not file_path:
                return

            dirname, basename = os.path.split(file_path)
            import_file_path = '{0}/{1}'.format(dirname, basename)
            import_values = create_json.read(import_file_path)

            for key, value in import_values.items():
                # cmds.setAttr(key, value)
                if self.namespace:
                    # dst_namespace = ':'.join(re.split('[:]', key)[:-1])
                    obj_attr = '{0}:{1}'.format(self.namespace, key)
                else:
                    obj_attr = key
                try:
                    if only_list:
                        if obj_attr.split('.')[0].split(':')[-1] in only_list:
                            cmds.setAttr(obj_attr, value)
                    else:
                        cmds.setAttr(obj_attr, value)
                except Exception as e:
                    pass
                    # traceback.print_exc()

            return import_file_path

    # Set init Space
    def set_init_space(self):
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

        # #check and save current autokey state
        # if cmds.autoKeyframe(q=True, st=True):
        #     autoKeyState = 1
        # else:
        #     autoKeyState = 0
        #
        # cmds.autoKeyframe(st=0)
        #
        # if not time_range:
        #     playmin = cmds.playbackOptions(q=1, min=1)
        #     playmax = cmds.playbackOptions(q=1, max=1)
        #
        # else:
        #     playmin = time_range[0]
        #     playmax = time_range[1]
        #
        # start = playmin
        # end = playmax

        #check to see if time range is highlighted
        # if playbackSlider:
        #     gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
        #     if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
        #         frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
        #         start = frameRange[0]
        #         end = frameRange[1]-1
        #     else:
        #         frameRange = cmds.currentTime(q=1)
        #         start = frameRange
        #         end = frameRange-1

        #bookend and key pinner plus all controls in range
        self.setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
        if self.setkey_attrs == []:
            self.setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

        # selection
        if not self.ctrls:
            cmds.warning(u'コントローラを選択してください。')
            return

        # bake_locs_grp
        self.bake_locs_grp = 'bake_locs_grp'
        if cmds.objExists(self.bake_locs_grp):
            cmds.delete(self.bake_locs_grp)

        cmds.createNode('transform', n=self.bake_locs_grp, ss=1)

        bake_locs = [cmds.spaceLocator(n='{0}_bake_loc'.format(obj))[0] for obj in self.ctrls if not cmds.objExists('{0}_bake_loc'.format(obj))]
        bake_locs.sort()
        cmds.parent(bake_locs, self.bake_locs_grp)
        pacons = [cmds.parentConstraint(obj, '{0}_bake_loc'.format(obj))[0] for obj in self.ctrls]

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
                         shape=False,
                         t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                         disableImplicitControl=True,
                         controlPoints=False,
                         at=self.setkey_attrs)

        cmds.delete(pacons)

        for obj in self.ctrls:
            tr_skips = trans_skippy(obj)
            ro_skips = rot_skippy(obj)
            try:
                if not tr_skips == []:
                    cmds.pointConstraint('{0}_bake_loc'.format(obj), obj, **tr_skips)
            except:
                pass
            try:
                if not ro_skips == []:
                    cmds.orientConstraint('{0}_bake_loc'.format(obj), obj, **ro_skips)
            except:
                pass

        if not cmds.objExists('bake_locs_sets'):
            cmds.sets(em=1, n='bake_locs_sets')

        for obj in self.ctrls:
            cmds.sets('{0}_bake_loc'.format(obj), add='bake_locs_sets')

        self.cutkey_of_user_define()

        return self.bake_locs_grp

    def cutkey_of_user_define(self):
        for obj in self.ctrls:
            listAttrs = cmds.listAttr(obj, ud=1)
            if listAttrs:
                for at in listAttrs:
                    listConnections = cmds.listConnections('{0}.{1}'.format(obj, at), s=1)
                    if listConnections:
                        for con_src in listConnections:
                            if (
                                cmds.objectType(con_src) == 'animCurveTA'
                                or cmds.objectType(con_src) == 'animCurveTU'
                                or cmds.objectType(con_src) == 'animCurveTL'
                                ):
                                cmds.cutKey(con_src)

    def addkey_of_user_define(self):
        for obj in self.ctrls:
            listAttrs = cmds.listAttr(obj, ud=1)
            if listAttrs:
                for at in listAttrs:
                    cmds.setKeyframe('{0}.{1}'.format(obj, at))

    def bake_ctrls(self):
        # Merge Layer
        animlays = cmds.ls(type='animLayer')
        if not animlays == []:
            mel.eval('string $animlays[] = `ls -type "animLayer"`;')
            mel.eval('layerEditorMergeAnimLayer($animlays, 0);')

        cmds.bakeResults(self.ctrls,
                         sparseAnimCurveBake=False,
                         minimizeRotation=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         oversamplingRate=1,
                         bakeOnOverrideLayer=False,
                         preserveOutsideKeys=True,
                         simulation=True,
                         sampleBy=1,
                         t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                         disableImplicitControl=True,
                         shape=False,
                         controlPoints=False,
                         at=self.setkey_attrs)

        # eulerfilter
        cmds.filterCurve(self.ctrls, f='euler')

    def cleaning(self):
        # cleaning
        print(u'余分なノードを削除しています。')
        animCurveTLs = cmds.ls(type='animCurveTL')
        animCurveTAs = cmds.ls(type='animCurveTA')
        animCurveTUs = cmds.ls(type='animCurveTU')

        animCurves = animCurveTLs + animCurveTAs + animCurveTUs

        allNodes = cmds.ls(type='transform')
        exclude_nodes = []

        # camera
        camera_shapes = cmds.ls(type='camera')
        camera_transforms = [cmds.listRelatives(obj, p=1)[0] for obj in camera_shapes]
        for obj in camera_transforms:
            exclude_nodes.append(obj)

        # NOTDEL
        NOTDELs = cmds.ls('NOTDEL*')
        NOTDEL_list = []
        for obj in NOTDELs:
            exclude_nodes.append(obj)
            children = cmds.listRelatives(obj, c=1)
            shapes = cmds.listRelatives(obj, s=1)

            if children:
                for chi in children:
                    exclude_nodes.append(chi)

            if shapes:
                for sh in shapes:
                    exclude_nodes.append(sh)

            if cmds.objectType(obj) == 'objectSet':
                cmds.select(obj, r=1, ne=1)
                not_del_objects = cmds.pickWalk(d='down')
                for node in not_del_objects:
                    exclude_nodes.append(node)

        # Reference
        reference_nodes = []
        for rn in cmds.ls(type='reference'):
            try:
                ref_nodes = cmds.referenceQuery(rn, nodes=True)
                if ref_nodes:
                    for ref_node in ref_nodes:
                        reference_nodes.append(ref_node)
            except Exception as e:
                pass
                # print(e)

        reference_nodes = list(set(reference_nodes))
        for rfn in reference_nodes:
            if rfn in allNodes:
                exclude_nodes.append(rfn)

        exclude_nodes = exclude_nodes + animCurves

        for obj in allNodes:
            if cmds.objExists(obj):
                if not obj in exclude_nodes:
                    try:
                        cmds.delete(obj)
                    except Exception as e:
                        pass
                        # print(e)

        if self.optimize:
            mel.eval("cleanUpScene 3")
            cmds.clearCache(all=1)
            cmds.refresh(f=1)
            print(u'シーンが最適化されました(Scene Size Optimized.)。')

        print(u'余分なノードの削除が完了しました。')

    def corrective_bakes_for_biped(self):
        only_list=[u'foot_L_ik_ctrl_revFoot_ball_ctrl',
                   u'foot_L_ik_ctrl_revFoot_heel_ctrl',
                   u'foot_L_ik_ctrl_revFoot_ikbake_ctrl',
                   u'foot_L_ik_ctrl_revFoot_in_ctrl',
                   u'foot_L_ik_ctrl_revFoot_out_ctrl',
                   u'foot_L_ik_ctrl_revFoot_toe_ctrl',
                   u'foot_R_ik_ctrl_revFoot_ball_ctrl',
                   u'foot_R_ik_ctrl_revFoot_heel_ctrl',
                   u'foot_R_ik_ctrl_revFoot_ikbake_ctrl',
                   u'foot_R_ik_ctrl_revFoot_in_ctrl',
                   u'foot_R_ik_ctrl_revFoot_out_ctrl',
                   u'foot_R_ik_ctrl_revFoot_toe_ctrl']

        match_dict={u'foot_L_ik_ctrl_revFoot_ikbake_ctrl':u'foot_L_ik_ctrl',
                    u'ball_L_proxy_jnt':u'foot_L_ik_ctrl_revFoot_holdBall_ctrl',
                    u'foot_R_ik_ctrl_revFoot_ikbake_ctrl':u'foot_R_ik_ctrl',
                    u'ball_R_proxy_jnt':u'foot_R_ik_ctrl_revFoot_holdBall_ctrl'}

        add_ns_only_liist = ['{0}:{1}'.format(self.namespace, ctrl) for ctrl in only_list]

        bake_locs={}
        bake_locs_buf=[]
        pa_cons=[]
        for k, v in match_dict.items():
            loc=cmds.spaceLocator(n='{0}_bake_loc'.format(k))
            bake_locs[v]=loc[0]
            bake_locs_buf.append(loc[0])
            pa_con=cmds.parentConstraint('{0}:{1}'.format(self.namespace, k), loc[0], w=1)
            pa_cons.append(pa_con[0])

        setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

        cmds.bakeResults(bake_locs_buf,
                         sparseAnimCurveBake=False,
                         minimizeRotation=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         oversamplingRate=1,
                         bakeOnOverrideLayer=False,
                         preserveOutsideKeys=True,
                         simulation=True,
                         sampleBy=1,
                         shape=False,
                         t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                         disableImplicitControl=True,
                         controlPoints=False,
                         at=setkey_attrs)

        cmds.delete(pa_cons)

        pa_cons=[]

        for k, v in match_dict.items():
            if 'foot' in v:
                pa_con=cmds.parentConstraint(bake_locs[v], '{0}:{1}'.format(self.namespace, v), w=1)
            elif 'ik_ctrl_revFoot_holdBall' in v:
                pa_con=cmds.orientConstraint(bake_locs[v], '{0}:{1}'.format(self.namespace, v), w=1)
            pa_cons.append(pa_con[0])

        for obj in add_ns_only_liist:
            listAttrs = cmds.listAttr(obj, k=1)
            if listAttrs:
                for at in listAttrs:
                    listConnections = cmds.listConnections('{0}.{1}'.format(obj, at), s=1)
                    if listConnections:
                        for con_src in listConnections:
                            animkey = cmds.objectType(con_src)
                            if (
                                animkey in 'animCurveTL'
                                or animkey in 'animCurveTA'
                                or animkey in 'animCurveTU'
                                ):
                                cmds.cutKey(con_src)
                                # print('CutKey:{0}'.format(con_src))

        self.objectValues(objects=self.ctrls, export_or_import='import', file_path=self.file_path, only_list=only_list)

        ik_ctrls_list = ['{0}:{1}'.format(self.namespace, v) for v in match_dict.values()]

        cmds.bakeResults(add_ns_only_liist+ik_ctrls_list,
                         sparseAnimCurveBake=False,
                         minimizeRotation=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         oversamplingRate=1,
                         bakeOnOverrideLayer=False,
                         preserveOutsideKeys=True,
                         simulation=True,
                         sampleBy=1,
                         t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                         disableImplicitControl=True,
                         at=setkey_attrs)

        cmds.delete(bake_locs_buf)


    def fileDialog_export(self):
        filename = cmds.fileDialog2(ds=2, cap='File', okc='Done', ff='*.json', fm=0)
        if filename is None:
            return False
        return filename[0]

    def fileDialog_import(self):
        filename = cmds.fileDialog2(ds=2, cap='File', okc='Done', ff='*.json', fm=1)
        if filename is None:
            return
        return filename[0]


class JsonFile(object):
    @classmethod
    def read(cls, file_path):
        if not file_path:
            return {}
        if not os.path.isfile(file_path):
            return {}
        with codecs.open(file_path, 'r', 'utf-8') as f:
            try:
                data = json.load(f, object_pairs_hook=OrderedDict)
            except ValueError:
                data = {}
        return data

    @classmethod
    def write(cls, file_path, data):
        if not file_path:
            return
        dirname, basename = os.path.split(file_path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with codecs.open(file_path, 'w', 'utf-8') as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
