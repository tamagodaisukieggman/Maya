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

try:
    import mtk3d.maya.rig.ikfkMatch.ikfkmatchtools as ikfkmatchtools
    print('mtk3d.maya.rig.ikfkMatch.ikfkmatchtools as ikfkmatchtools')
except:
    import ikfkMatch.ikfkmatchtools as ikfkmatchtools
    print('ikfkmatchtools')
else:
    reload(ikfkmatchtools)

# atomImportExport
if cmds.pluginInfo('atomImportExport', q=True, l=True) == False:
    cmds.loadPlugin("atomImportExport")

class UI(object):
    def __init__(self, cmd=0, CtrlSet=['ply00_m_000_000:CtrlSet'], dialog=None, backupAnim=True, setJsonFile='Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/refreshScene/initData/anm_ply00_m_000_anim.json',
                 ikfk=True, ikfk_switch_attrs=['left_hand', 'right_hand', 'left_leg', 'right_leg'], ikfk_match_namespace=['ply00_m_000_000'], get_namespace=True,
                 optimize=False, ikfk_match=True, replace_namespace=True):

        u"""
        # 西村さん用↓
        import mtk3d.maya.rig.refreshScene.refreshScene as refreshScene
        reload(refreshScene)
        CtrlSet = cmds.ls(os=1, r=1)
        refreshAnim = refreshScene.UI(cmd=1, CtrlSet=CtrlSet) # CtrlSetはリストで　例:CtrlSet = ['ply00_m_000_000:CtrlSet', 'mob00_m_000_000:CtrlSet']
        refreshAnim.call_refresh()


        # 起動用コマンド
        import mtk3d.maya.rig.refreshScene.refreshScene as refreshScene
        reload(refreshScene)
        # CtrlSets = ['ply00_m_000_000:CtrlSet', 'mob00_m_000_000:CtrlSet']
        # CtrlSets = cmds.ls(os=1, r=1)
        # それぞれの設定ファイルから初期値をインポートする場合
        CtrlSets = ['ply00_m_000_000:CtrlSet', 'mob00_m_000_000:CtrlSet']
        namespaces = [ns.replace(':{0}'.format(ns.split(':')[1]), '') for ns in CtrlSets]
        setJsonFile = ['Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/refreshScene/initData/anm_{0}_anim.json'.format(ns) for ns in namespaces]
        refreshAnim = refreshScene.UI(cmd=1, CtrlSet=CtrlSets, ikfk_match=False, ikfk_match_namespace=namespaces, setJsonFile=setJsonFile)
        refreshAnim.call_refresh()

        # ひとつの設定ファイルを読み込んでネームスペースを置き換えてインポートする場合
        CtrlSets = ['ply00_m_000_000:CtrlSet', 'mob00_m_000_000:CtrlSet']
        namespaces = [ns.replace(':{0}'.format(ns.split(':')[1]), '') for ns in CtrlSets]
        setJsonFile = 'Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/refreshScene/initData/anm_ply00_m_000_anim.json'
        refreshAnim = refreshScene.UI(cmd=1, CtrlSet=CtrlSets, ikfk_match=False, ikfk_match_namespace=namespaces, setJsonFile=setJsonFile, replace_namespace=True)
        refreshAnim.call_refresh()

        # refreshAnim.show()
        """

        # 初期設定 -----------------------------------------------------------------------------------------------------------------
        # CtrlSet = 'ply00_m_000_000:ctrls_sets'
        # setJsonFile = 'Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/refreshScene/initData/anm_ply00_m_000_anim.json'
        dialog = None
        # backupAnim = True
        # ikfk = True

        # ikfk_match_namespace = 'ply00_m_000_000'
        # -------------------------------------------------------------------------------------------------------------------------

        self.MAIN_WINDOW = 'Refresh Animation Scene'
        self.cmd = cmd
        self.CtrlSet = CtrlSet
        self.dialog = dialog
        self.backupAnim = backupAnim
        self.setJsonFile = setJsonFile
        self.optimize = optimize
        self.ikfk_match = ikfk_match
        self.replace_namespace = replace_namespace
        self.get_namespace = get_namespace

        # ikfk match
        self.ikfk = ikfk
        self.fk_or_ik_list = []
        self.tags = []
        self.pv_move = 20


    def show(self):
        if cmds.workspaceControl(self.MAIN_WINDOW, q=1, ex=1):
            cmds.deleteUI(self.MAIN_WINDOW)

        self.win = cmds.workspaceControl(self.MAIN_WINDOW, l=self.MAIN_WINDOW)

        self.layout()

        cmds.showWindow(self.win)

    def layout(self):

        cmds.columnLayout(adj=1, rs=7)
        CtrlSet, setJsonFile = self.convert_list_to_strings()
        self.set_sets_tfbg = cmds.textFieldButtonGrp(l=u'コントローラのセットをSet指定', bl='set', bc=self.set_sets, tx=u'{0}'.format(CtrlSet), cw3=[130, 150, 50], ad3=2)
        self.set_export_json_tfbg = cmds.textFieldButtonGrp(l=u'初期値となるJsonファイルの書き出し', bl='Export', bc=self.export_ctrl_values, tx=u'', cw3=[157, 150, 50], ad3=2)
        self.set_init_json_tfbg = cmds.textFieldButtonGrp(l=u'初期値となるJsonファイルの指定', bl='set', bc=self.set_init_json, tx=u'{0}'.format(setJsonFile), cw3=[142, 150, 50], ad3=2)
        self.import_ctrls_values = cmds.button(l=u'指定したJsonファイルをImport', c=self.import_ctrls_json_file)

        self.set_except_ctrls_tfbg = cmds.textFieldButtonGrp(l=u'ベイクから省くコントローラ',
                                                             bl=u'set',
                                                             bc=self.set_except_ctrls,
                                                             tx=u'ply00_m_000_000:clavicle_L_ikAutoRot_ctrl_ikAutoShoulder_ctrl,ply00_m_000_000:clavicle_R_ikAutoRot_ctrl_ikAutoShoulder_ctrl',
                                                             cw3=[130, 150, 50],
                                                             m=0)

        cmds.separator()
        self.backupAnim_cb = cmds.checkBox(l=u'アニメーションをバックアップする', v=1)
        self.ikfk_match_cb = cmds.checkBox(l=u'IKFKマッチをする', v=1)
        self.replace_ns_cb = cmds.checkBox(l=u'初期設定となるJsonファイルを元にネームスペースを置き換える', v=1)

        self.backupAnim_tfbg = cmds.textFieldButtonGrp(l=u'バックアップフォルダ',
                                                         bl='Import Animation',
                                                         bc=self.import_atom,
                                                         tx='',
                                                         cw3=[80, 150, 50],
                                                         m=1,
                                                         ad3=2,
                                                         ed=0)

        cmds.button(l=u'リフレッシュ!', c=self.call_refresh, w=200)

    def convert_list_to_strings(self, *args, **kwargs):
        CtrlSet = ','.join(self.CtrlSet)
        if type(self.setJsonFile) == list:
            setJsonFile = ','.join(self.setJsonFile)
        else:
            setJsonFile = self.setJsonFile
        return CtrlSet, setJsonFile

    def import_atom(self, *args, **kwargs):
        backup_data = cmds.textFieldButtonGrp(self.backupAnim_tfbg, q=1, tx=1)

        filename = cmds.fileDialog2(ds=2, cap='Import Atom', okc='Done', ff='*.atom', fm=1, dir=backup_data)
        if not filename:
            return

        CtrlSet = self.CtrlSet
        cmds.select(CtrlSet, r=1, ne=1)
        ctrls = cmds.pickWalk(d='down')

        filename = filename[0]

        scene_name = '{0}'.format(cmds.file(q=1, sn=1).split('/')[-1].split('.ma')[0])
        cmds.file("{0}".format(filename), pr=1, rpr="{0}".format(scene_name), ignoreVersion=1, i=1, type="atomImport", importTimeRange="combine", mergeNamespacesOnClash=False)

    def objectValues(self, joints=None, export_or_import='import', fix=True, file_path=None, namespace=None, only_list=None):
        create_json = JsonFile()
        if export_or_import == 'export':
            # joints = cmds.ls(type='joint')
            joints.sort()

            joints_values = OrderedDict()
            for jnt in joints:
                listAttrs = cmds.listAttr(jnt, k=1)
                if listAttrs:
                    listAttrs.sort()
                    buf_attrs = []
                    for at in listAttrs:
                        try:
                            joints_values['{0}.{1}'.format(jnt, at)] = cmds.getAttr('{0}.{1}'.format(jnt, at))
                        except:
                            pass
            if not file_path:
                file_path = fileDialog_export()
            if not file_path:
                return
            dirname, basename = os.path.split(file_path)
            save_file_path = '{0}/{1}'.format(dirname, basename)
            create_json.write('{0}'.format(save_file_path), joints_values)

            return save_file_path

        elif export_or_import == 'import':
            if not file_path:
                file_path = fileDialog_import()
            if not file_path:
                return

            dirname, basename = os.path.split(file_path)
            import_file_path = '{0}/{1}'.format(dirname, basename)
            import_values = create_json.read(import_file_path)

            for key, value in import_values.items():
                # cmds.setAttr(key, value)
                if self.cmd == 0:
                    self.replace_namespace = cmds.checkBox(self.replace_ns_cb, q=1, v=1)
                if namespace:
                    dst_namespace = ':'.join(re.split('[:]', key)[:-1])
                    obj_attr = key.replace(dst_namespace, namespace)
                else:
                    obj_attr = key
                try:
                    if only_list:
                        if obj_attr.split('.')[0] in only_list:
                            cmds.setAttr(obj_attr, value)
                    else:
                        cmds.setAttr(obj_attr, value)
                except Exception as e:
                    pass
                    # traceback.print_exc()

            return import_file_path

    def set_sets(self, *args, **kwargs):
        sel = cmds.ls(os=1)
        if 1 < len(sel):
            set_sets = ','.join(sel)
        else:
            set_sets = '{0}'.format(sel[0])
        cmds.textFieldButtonGrp(self.set_sets_tfbg, e=1, tx=set_sets)

    def set_init_json(self, *args, **kwargs):
        filename = cmds.fileDialog2(ds=2, cap='Set Init Scene', okc='Done', ff='*.json', fm=1)
        if not filename:
            return

        filename = filename[0]

        cmds.textFieldButtonGrp(self.set_init_json_tfbg, e=1, tx=filename)

    def export_ctrl_values(self, *args, **kwargs):
        CtrlSet = cmds.textFieldButtonGrp(self.set_sets_tfbg, q=1, tx=1)
        if not cmds.objExists(CtrlSet):
            cmds.warning(u'{0}がありません'.format(CtrlSet))
            return

        cmds.select(CtrlSet, r=1, ne=1)
        ctrls = cmds.pickWalk(d='down')

        file_path = self.objectValues(joints=ctrls, export_or_import='export', fix=True)
        cmds.textFieldButtonGrp(self.set_export_json_tfbg, e=1, tx=u'{0}'.format(file_path))

    def import_ctrls_json_file(self, file_path_txt, CtrlSet, only_list=None):
        src_namespace = None
        if self.cmd == 0:
            self.replace_namespace = cmds.checkBox(self.replace_ns_cb, q=1, v=1)

        if self.replace_namespace:
            src_namespace = ':'.join(re.split('[:]', CtrlSet)[:-1])

        file_path = self.objectValues(joints=self.ctrls, export_or_import='import', fix=True, file_path=file_path_txt, namespace=src_namespace, only_list=only_list)
        print(file_path)

    def set_except_ctrls(self, *args, **kwargs):
        sel = cmds.ls(os=1)
        set_except_ctrls = '{0}'.format(','.join(sel))
        cmds.textFieldButtonGrp(self.set_except_ctrls_tfbg, e=1, tx=set_except_ctrls)


    # Set init Space
    def set_init_space(self, ctrls):
        time_range = None
        playbackSlider = False

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


        #check and save current autokey state
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = 1
        else:
            autoKeyState = 0

        cmds.autoKeyframe(st=0)

        if not time_range:
            playmin = cmds.playbackOptions(q=1, min=1)
            playmax = cmds.playbackOptions(q=1, max=1)

        else:
            playmin = time_range[0]
            playmax = time_range[1]

        start = playmin
        end = playmax

        #check to see if time range is highlighted
        if playbackSlider:
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
                frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
                start = frameRange[0]
                end = frameRange[1]-1
            else:
                frameRange = cmds.currentTime(q=1)
                start = frameRange
                end = frameRange-1

        #bookend and key pinner plus all controls in range
        setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
        if setkey_attrs == []:
            setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

        # selection
        sel = ctrls
        if not sel:
            cmds.warning(u'コントローラを選択してください。')
            return

        # bake_locs_grp
        bake_locs_grp = 'bake_locs_grp'
        if not cmds.objExists(bake_locs_grp):
            cmds.createNode('transform', n=bake_locs_grp, ss=1)

        bake_locs = [cmds.spaceLocator(n='{0}_bake_loc'.format(obj))[0] for obj in sel if not cmds.objExists('{0}_bake_loc'.format(obj))]
        bake_locs.sort()
        cmds.parent(bake_locs, bake_locs_grp)
        pacons = [cmds.parentConstraint(obj, '{0}_bake_loc'.format(obj))[0] for obj in sel]

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
                         t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                         disableImplicitControl=True,
                         at=setkey_attrs)

        cmds.delete(pacons)

        for obj in sel:
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

        for obj in sel:
            cmds.sets('{0}_bake_loc'.format(obj), add='bake_locs_sets')

        return bake_locs_grp

    def call_refresh(self, *args, **kwargs):
        cycleCheck_sts = cmds.cycleCheck(q=1, e=1)
        autoKeyframe_sts = cmds.autoKeyframe(q=True, st=True)

        cmds.cycleCheck(e=0)
        cmds.autoKeyframe(st=0)

        try:
            cmds.refresh(su=1)
            refresh_sts = self.refresh()
            if refresh_sts:
                self.cleaning()
            if self.ikfk_match:
                self.call_ikfk_match()
            cmds.refresh(su=0)
        except Exception as e:
            traceback.print_exc()
            cmds.refresh(su=0)

        cmds.cycleCheck(e=cycleCheck_sts)
        cmds.autoKeyframe(st=autoKeyframe_sts)

        print(u'このシーンはRefreshされました。')

    def call_ikfk_match(self, *args, **kwargs):
        self.ikfk_switch_attrs = []
        if self.get_namespace:
            self.ikfk_match_namespace = [ns.replace(':{0}'.format(ns.split(':')[1]), '') for ns in self.CtrlSet]
        for imn in self.ikfk_match_namespace:
            ikfk_switch_attrs_buf = ["{0}:hand_L_fk_ctrl|{0}:arms_L_01_IKFK_shared_crvShape.IKFK".format(imn),
                                      "{0}:hand_R_fk_ctrl|{0}:arms_R_01_IKFK_shared_crvShape.IKFK".format(imn),
                                      "{0}:ballend_L_fk_ctrl|{0}:legs_L_01_IKFK_shared_crvShape.IKFK".format(imn),
                                      "{0}:ballend_R_fk_ctrl|{0}:legs_R_01_IKFK_shared_crvShape.IKFK".format(imn)]

            self.ikfk_switch_attrs.append(ikfk_switch_attrs_buf)

        print(u'IKFKマッチ:{0}'.format(self.ikfk_match_namespace))

        for i, (imn, ns) in enumerate(zip(self.ikfk_switch_attrs, self.ikfk_match_namespace)):
            self.ikfk_match_func(imn, ns)

    def corrective_bakes_for_biped(self, file_path_txt, CtrlSet):
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

        add_ns_only_liist = ['{0}:{1}'.format(CtrlSet.split(':')[0], ctrl) for ctrl in only_list]

        bake_locs={}
        bake_locs_buf=[]
        pa_cons=[]
        for k, v in match_dict.items():
            loc=cmds.spaceLocator(n='{0}_bake_loc'.format(k))
            bake_locs[v]=loc[0]
            bake_locs_buf.append(loc[0])
            pa_con=cmds.parentConstraint('{0}:{1}'.format(CtrlSet.split(':')[0], k), loc[0], w=1)
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
                         t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                         disableImplicitControl=True,
                         at=setkey_attrs)

        cmds.delete(pa_cons)

        pa_cons=[]

        for k, v in match_dict.items():
            if 'foot' in v:
                pa_con=cmds.parentConstraint(bake_locs[v], '{0}:{1}'.format(CtrlSet.split(':')[0], v), w=1)
            elif 'ik_ctrl_revFoot_holdBall' in v:
                pa_con=cmds.orientConstraint(bake_locs[v], '{0}:{1}'.format(CtrlSet.split(':')[0], v), w=1)
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
                                ):
                                cmds.cutKey(con_src)
                                print('CutKey:{0}'.format(con_src))

        self.import_ctrls_json_file(file_path_txt, CtrlSet, only_list=add_ns_only_liist)

        ik_ctrls_list = ['{0}:{1}'.format(CtrlSet.split(':')[0], v) for v in match_dict.values()]

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

    def refresh(self, *args, **kwargs):
        refresh_yes_no = None
        if self.dialog:
            refresh_yes_no = cmds.confirmDialog(message=u'アニメーションシーンをリフレッシュしますか?.', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        elif not self.dialog:
            refresh_yes_no = 'Yes'
        if refresh_yes_no == 'Yes':
            if self.cmd == 1:
                pass
            elif self.cmd == 0:
                self.CtrlSet = cmds.textFieldButtonGrp(self.set_sets_tfbg, q=1, tx=1)
                self.setJsonFile = cmds.textFieldButtonGrp(self.set_init_json_tfbg, q=1, tx=1)
                self.replace_namespace = cmds.checkBox(self.replace_ns_cb, q=1, v=1)
                self.CtrlSet = re.split('[,]', self.CtrlSet)
                # self.setJsonFile = re.split('[,]', self.setJsonFile)

                if cmds.checkBox(self.backupAnim_cb, ex=1):
                    self.backupAnim = cmds.checkBox(self.backupAnim_cb, q=1, v=1)

            print(u'ベイクされるコントローラセット:{0}'.format(self.CtrlSet))
            print(u'読み込む初期設定:{0}'.format(self.setJsonFile))

            for i, cs in enumerate(self.CtrlSet):
                if not cmds.objExists(cs):
                    cmds.warning(u'{0}がありません'.format(cs))
                    return
                cmds.select(cs, r=1, ne=1)
                self.ctrls = cmds.pickWalk(d='down')
                if self.cmd == 1 and self.replace_namespace != True:
                    init_bake_sts = self.init_bake(self.setJsonFile[i], cs)
                    self.corrective_bakes_for_biped(self.setJsonFile[i], cs)
                elif self.replace_namespace == True:
                    init_bake_sts = self.init_bake(self.setJsonFile, cs)
                    self.corrective_bakes_for_biped(self.setJsonFile, cs)

        return init_bake_sts

    def init_bake(self, file_path_txt, CtrlSet):
        if type(file_path_txt) == list:
            if len(file_path_txt) == 1:
                file_path_txt = file_path_txt[0]
        if not os.path.isfile(file_path_txt):
            print(u'ファイルがありません。{0}'.format(file_path_txt))
            return False
        # eulerfilter
        cmds.filterCurve(self.ctrls, f='euler')

        #bookend and key pinner plus all controls in range
        setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
        if setkey_attrs == []:
            setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

        # Merge Layer
        animlays = cmds.ls(type='animLayer')
        if not animlays == []:
            mel.eval('string $animlays[] = `ls -type "animLayer"`;')
            mel.eval('layerEditorMergeAnimLayer($animlays, 0);')

        # ----
        # ikfk_tools = ikfkmatchtools(cmd=1, fk_or_ik_list=None, tags=None, pv_move=None, namespace=None)
        # ikfk_tools.matchbake()

        bake_locs_grp = self.set_init_space(self.ctrls)
        print(u'ベイクされるコントローラ:{0}'.format(self.ctrls))

        except_cutkeys = ['soft_ik',]

        for obj in self.ctrls:
            listAttrs = cmds.listAttr(obj, ud=1)
            if listAttrs:
                for at in listAttrs:
                    if not at in except_cutkeys:
                        listConnections = cmds.listConnections('{0}.{1}'.format(obj, at), s=1)
                        if listConnections:
                            for con_src in listConnections:
                                animkey = '{0}_{1}'.format(obj.split(':')[-1], at)
                                if animkey in con_src:
                                    cmds.cutKey(con_src)

        self.import_ctrls_json_file(file_path_txt, CtrlSet, None)
        print(u'初期設定のJsonファイルを読み込みました。')

        for obj in self.ctrls:
            listAttrs = cmds.listAttr(obj, ud=1)
            if listAttrs:
                for at in listAttrs:
                    cmds.setKeyframe('{0}.{1}'.format(obj, at))

        print(u'{0}をベイクしています。'.format(CtrlSet))
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
                         at=setkey_attrs)

        print(u'{0}を初期設定の状態でベイクしました。'.format(CtrlSet))
        cmds.delete(bake_locs_grp)

        if self.backupAnim:
            USER_NAME = getpass.getuser()
            mtk_animation_refresh_temp = "C:/Users/{0}/Documents/maya/scripts/mtkAnimationRefreshTemp".format(USER_NAME)

            if not os.path.isdir(mtk_animation_refresh_temp):
                os.mkdir(mtk_animation_refresh_temp)

            scene_name = '{0}'.format(cmds.file(q=1, sn=1).split('/')[-1].split('.ma')[0])
            bktime = u'{}{:4d}'.format(datetime.now().strftime("%Y%m%d_%H%M%S"), datetime.now().microsecond) # 時間は%H%M%S

            cmds.select(self.ctrls, r=1)
            cmds.file("{0}/{1}_{2}.atom".format(mtk_animation_refresh_temp, scene_name, bktime), pr=1, typ="atomExport", force=1, options="", es=1)
            print('Saved .atom in:{0}'.format("{0}/{1}_{2}.atom".format(mtk_animation_refresh_temp, scene_name, bktime)))
            if self.cmd == 0:
                if cmds.textFieldButtonGrp(self.backupAnim_tfbg, ex=1):
                    cmds.textFieldButtonGrp(self.backupAnim_tfbg, e=1, tx="{0}".format(mtk_animation_refresh_temp))

        return True

    def cleaning(self, *args, **kwargs):
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

    def ikfk_match_func(self, ikfk_switch_attrs, namespace):
            if self.cmd == 0:
                self.ikfk = cmds.checkBox(self.ikfk_match_cb, q=1, v=1)

            if self.ikfk == 1:
                for i, ifk_at in enumerate(ikfk_switch_attrs):
                    if i == 0:
                        self.alcb_v = cmds.getAttr(ifk_at)
                    elif i == 1:
                        self.arcb_v = cmds.getAttr(ifk_at)
                    elif i == 2:
                        self.llcb_v = cmds.getAttr(ifk_at)
                    elif i == 3:
                        self.lrcb_v = cmds.getAttr(ifk_at)

                # arms_L
                self.tags.append('arms_L_')
                if self.alcb_v == 1:
                    self.fk_or_ik_list.append('fk')
                else:
                    self.fk_or_ik_list.append('ik')

                # arms_R
                self.tags.append('arms_R_')
                if self.arcb_v == 1:
                    self.fk_or_ik_list.append('fk')
                else:
                    self.fk_or_ik_list.append('ik')

                # legs_L
                self.tags.append('legs_L_')
                if self.llcb_v == 1:
                    self.fk_or_ik_list.append('fk')
                else:
                    self.fk_or_ik_list.append('ik')

                # legs_R
                self.tags.append('legs_R_')
                if self.lrcb_v == 1:
                    self.fk_or_ik_list.append('fk')
                else:
                    self.fk_or_ik_list.append('ik')

                ui = ikfkmatchtools.UI(cmd=1, fk_or_ik_list=self.fk_or_ik_list, tags=self.tags, pv_move=self.pv_move, namespace=namespace)
                print(u'{0} のIKFKマッチを行っています。'.format(namespace))
                ui.matchbake()
                for ikfk_switch in ikfk_switch_attrs:
                    animCurves = cmds.listConnections(re.split('[.|]', ikfk_switch)[1], type='animCurve')
                    if animCurves:
                        cmds.select(animCurves[0])
                        cmds.selectKey(animCurves[0], add=1, k=1)
                        cmds.keyframe(valueChange=1, animation='keys', absolute=1)

                print(u'{0} IKFKマッチが終わりました。'.format(namespace))


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

        dirname, basename = os.path.split(file_path) # "/"��split������
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with codecs.open(file_path, 'w', 'utf-8') as f:
            json.dump(data, f, indent=4) # indent�t���O��dictionary��space4���Ƃɂ��ꂢ�ɏ�������
            f.flush()
            os.fsync(f.fileno()) # �f�B�X�N�̏�������

def fileDialog_export():
    filename = cmds.fileDialog2(ds=2, cap='File', okc='Done', ff='*.json', fm=0)
    if filename is None:
        return False
    return filename[0]

def fileDialog_import():
    filename = cmds.fileDialog2(ds=2, cap='File', okc='Done', ff='*.json', fm=1)
    if filename is None:
        return
    return filename[0]



if __name__ == '__main__':
    ui = UI()
    ui.show()

"""
CtrlSet = 'ply00_m_000_000:CtrlSet'
ui = UI(cmd=1, CtrlSet=CtrlSet, dialog=None, backupAnim=True)
ui.refresh()
"""

"""
CtrlSet = 'ply00_m_000_000:CtrlSet'
ui = UI(cmd=0, CtrlSet=CtrlSet, dialog=None, backupAnim=True)
ui.show()
"""
