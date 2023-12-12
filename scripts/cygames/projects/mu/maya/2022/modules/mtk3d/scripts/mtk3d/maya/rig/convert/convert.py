# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import maya.api.OpenMaya as OpenMaya2
import os
import timeit
import time
import sys
import codecs
import json
import math
from collections import OrderedDict
from datetime import datetime
import xml.etree.ElementTree as ET
import traceback


import attach.animfollowmove as animfollowmove
reload(animfollowmove)

if cmds.pluginInfo('mayaHIK', q=True, l=True) == False:
    cmds.loadPlugin("mayaHIK")
if cmds.pluginInfo('mayaCharacterization', q=True, l=True) == False:
    cmds.loadPlugin("mayaCharacterization")
if cmds.pluginInfo('OneClick', q=True, l=True) == False:
    cmds.loadPlugin("OneClick")
if cmds.pluginInfo('fbxmaya', q=True, l=True) == False:
    cmds.loadPlugin("fbxmaya")

dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
dir_path = dir.replace('\\', '/')

error_results = []
logFolder = '{}/log/'.format(dir_path)

def main(files, save_path, convertType, fps, root_move_to_hip,  animBase):
    # save_path = 'D:/myFolder/myWork/PJ/mutsunokami/JD_new2old'
    countfbx = []
    fbxes = []
    clock = timeit.default_timer
    start = clock()

    listFiles = files.split(' ')
    # print(listFiles)
    for files in listFiles:
        if files.endswith('.fbx') or files.endswith('.ma') or files.endswith('.mb'):
            countfbx.append(files)
            try:
                convert_fbx(files, save_path, convertType, fps, root_move_to_hip,  animBase)
            except Exception as e:
                error_results.append((files, traceback.print_exc()))
        elif os.path.isdir(files):
            fbxes = run_files(files, save_path, convertType, fps, root_move_to_hip,  animBase)
    elapsed = clock() - start

    if error_results: # error_resultがあれば、
        # txt = 'D:/error.csv'
        txt = u'{}/error_{}{:4d}.csv'.format(logFolder, datetime.now().strftime("%Y%m%d_%H%M%S"), datetime.now().microsecond) # 時間は%H%M%S
        # csvで書き出し
        with codecs.open(txt, 'w', 'utf-8') as f:
            for result in error_results:
                f.write(u'{}, {}\n'.format(result[0], result[1]))

    print( time.strftime("%Hh:%Mm:{:.3f}s / {} fbxes".format(elapsed, len(countfbx)+len(fbxes)), time.gmtime(elapsed)) )
    print( time.strftime("%Hh:%Mm:{:.3f}s / 1 fbx".format(elapsed/(len(countfbx)+len(fbxes))), time.gmtime(elapsed/(len(countfbx)+len(fbxes)))) )

def import_ma_to_fbx(file_path, rootJnt, searchText):
    # cmds.file(file_path, pr=1, ignoreVersion=1, i=1, type="mayaAscii", importFrameRate=True, importTimeRange="override", mergeNamespacesOnClash=False, options="v=0;p=17;f=0")

    def delRef():
        refNodes = cmds.ls(rf=True, r=1)
        for refn in refNodes:
            try:
                cmds.file(rfn=refn, ir=True)
            except:
                pass

    delRef()
    delRef()
    delRef()
    delRef()
    delRef()
    delRef()


    nss_in_joints = cmds.ls(searchText, type='joint', r=1)
    nss_buf = ['{}'.format(nss_in.replace(nss_in.split(':')[-1], '')) for nss_in in nss_in_joints]
    nss_list = list(set(nss_buf))
    try:
        nss_list.remove('')
    except:
        pass
    nss = nss_list[0]

    root_jnt = '{}{}'.format(nss, rootJnt)

    playmin = cmds.playbackOptions(q=1, min=1)
    playmax = cmds.playbackOptions(q=1, max=1)

    cmds.refresh(su=1)
    cmds.bakeResults(root_jnt, hi='below', sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
    cmds.refresh(su=0)

    try:
        cmds.parent(root_jnt, w=1)
    except Exception as e:
        traceback.print_exc()

    pm.util.putEnv("MAYA_TESTING_CLEANUP","1")
    pm.runtime.OptimizeScene()

    cam = [u'persp', u'top', u'front', u'side']

    tops = []

    allNodes = cmds.ls(type='transform')
    for to in allNodes:
        pNode = pm.PyNode(to)
        top = pNode.root()
        tops.append(top.name())

    list_tops = list(set(tops))

    protect = cmds.ls(root_jnt, dag=1, type='joint')
    allNodes = cmds.ls(type='transform')
    sets = cmds.ls(type='objectSet')
    for obj in list_tops:
        if obj not in protect:
            cmds.delete(obj)

    for obj in sets:
        if obj not in protect:
            try:
                cmds.delete(obj)
            except:
                pass

    cmds.namespace(setNamespace=':')

    for ns in reversed(cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)):
        if ns != 'UI' and ns != 'shared':
            cmds.namespace(moveNamespace=(ns, ':'), force=True)
            cmds.namespace(removeNamespace=ns)
    try:
        cmds.delete('bindPose*')
    except:
        pass

    """
    #取得
    # a = pm.optionVar["unknownNodesOption"]
    #設定

    nurbsSrfOption
    nurbsCrvOption
    unusedNurbsSrfOption
    locatorOption
    ptConOption
    pbOption
    deformerOption
    unusedSkinInfsOption
    expressionOption
    groupIDnOption
    animationCurveOption
    clipOption
    poseOption
    snapshotOption
    unitConversionOption
    shaderOption
    cachedOption
    transformOption
    displayLayerOption
    renderLayerOption
    setsOption
    partitionOption
    referencedOption
    brushOption
    shadingNetworksOption
    pm.optionVar["unknownNodesOption"] = 1
    """

def run_files(fbx_path, save_path, convertType, fps, root_move_to_hip,  animBase):
    countfbx = []
    if type(fbx_path) == list:
        for fbx in fbx_path:
            try:
                file_exist = convert_fbx(fbx, save_path, convertType, fps,root_move_to_hip,  animBase)
                if file_exist != None:
                    error_results.append((fbx, file_exist))
            except Exception as e:
                error_results.append((fbx, traceback.print_exc()))
    else:
        for root, dirs, files in os.walk(fbx_path):
            for fname in files:
                file_path = os.path.join(root, fname)
                fbx = file_path.replace('\\', '/')
                if fbx.endswith('.fbx') or fbx.endswith('.ma') or fbx.endswith('.mb'):
                    countfbx.append(fbx)
                    try:
                        file_exist = convert_fbx(fbx, save_path, convertType, fps, root_move_to_hip,  animBase)
                        if file_exist != None:
                            error_results.append((fbx, file_exist))
                    except Exception as e:
                        error_results.append((fbx, traceback.print_exc()))
    return countfbx

def convertFrameRate(fbx, toFps):
    mel.eval('FBXImport -file"' + fbx + '";')

    fromFps = cmds.currentUnit(q=1, time=1)
    FPS_MAP = {'game': 15, 'film': 24, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}
    if fromFps in FPS_MAP.keys():
        fromFps = FPS_MAP[fromFps]
    else:
        fromFps = fromFps.replace('fps', '')

    scaleKey = toFps / fromFps
    anim_curves = cmds.ls(type=['animCurveTA', 'animCurveTL', 'animCurveTT', 'animCurveTU'])
    cmds.scaleKey(anim_curves, iub=False, ts=1, tp=0, fs=scaleKey, fp=0, vs=1, vp=0, animation='objects')
    cmds.filterCurve(anim_curves, f='euler')

    cmds.currentUnit(time = '{}fps'.format(toFps))

    mel.eval('FBXExportColladaFrameRate {} ;'.format(toFps))

    file=mel.eval('FBXExport -f"' + fbx.replace('.fbx', '.dae') + '";')
    cmds.file(f=1, new=1)
    mel.eval('FBXImport -file"' + fbx.replace('.fbx', '.dae') + '";')
    cmds.currentUnit(time = '{}fps'.format(toFps))
    file = cmds.file('{}'.format(fbx.replace('.fbx', '_convertDummy.fbx')), f=1, options='v=0;', pr=1, ea=1, type='FBX export')

    return file

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

def const_bake(correct_ctrls=None, ctrl_set=None, from_sets=True, selection=True, select_timeslider=False, timerange=None):
    """
    ctrl_set = 'ply00_m_000_000:CtrlSet' # string
    from_sets = True # bool
    selection = True # bool
    select_timeslider = False # bool
    timerange = None # list [0, 0]
    """

    # timerange > select_timeslider > currentの順で優先される
    playmin = cmds.playbackOptions(q=1, min=1)
    playmax = cmds.playbackOptions(q=1, max=1)

    if timerange:
        select_timeslider = False

    if select_timeslider:
        aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
        rangeArray = cmds.timeControl( aPlayBackSliderPython, q=True, rangeArray=True)

        playmin = rangeArray[0]
        playmax = rangeArray[1]

    if timerange:
        playmin = timerange[0]
        playmax = timerange[1]

    # すべてのコントローラを取得
    if selection:
        ctrls = cmds.ls(sl=1, type='transform')
    if from_sets == True and ctrls == []:
        cmds.select(ctrl_set, r=1, ne=1);cmds.pickWalk(d='down')
        ctrls = cmds.ls(sl=1, type='transform')

    ctrls = [ctrl for ctrl in ctrls if ctrl not in correct_ctrls.keys()]

    # ロケータにキャッシュ
    loc_dict = {}
    consts = []
    for ctrl in ctrls:
        for ctrl_key, ctrl_value in correct_ctrls.items():
            if ctrl == ctrl_value[0]:
                loc = cmds.spaceLocator()[0]
                loc_dict[ctrl_key] = [loc, ctrl_value[0]]
                pa_con = cmds.parentConstraint(ctrl_value[0], loc, w=1)
                consts.append(pa_con[0])

    cmds.bakeResults([loc[0] for loc in loc_dict.values()], sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
    cmds.clearCache(all=True)

    cmds.delete(consts) # コンストレイントを削除

    # それ以外をキャッシュ
    all_loc_dict = {}
    all_consts = []
    for ctrl in ctrls:
        loc = cmds.spaceLocator()[0]
        all_loc_dict[ctrl] = loc
        pa_con = cmds.parentConstraint(ctrl, loc, w=1)
        all_consts.append(pa_con[0])

    cmds.bakeResults(all_loc_dict.values(), sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
    cmds.clearCache(all=True)

    cmds.delete(all_consts)

    # 拘束
    for src, loc in loc_dict.items():
        const_options = correct_ctrls[src][1]
        pa_con = cmds.parentConstraint(loc[0], src, **const_options)
        all_consts.append(pa_con[0])

    cycleCheck_state = cmds.cycleCheck(q=1, e=1)
    if cycleCheck_state:
        cmds.cycleCheck(e=False)

    # それ以外を拘束
    for src, loc in all_loc_dict.items():
        trans_flags = trans_skippy(src)
        po_con = cmds.pointConstraint(loc, src, w=1, mo=1, **trans_flags)
        all_consts.append(po_con[0])
        rotate_flags = rot_skippy(src)
        ori_con = cmds.orientConstraint(loc, src, w=1, mo=1, **rotate_flags)
        all_consts.append(ori_con[0])

    bake_list = [ctrl for ctrl in correct_ctrls.keys()] + all_loc_dict.keys()

    cmds.bakeResults(bake_list, sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
    cmds.clearCache(all=True)

    # コンストレイントを削除
    cmds.delete([loc[0] for loc in loc_dict.values()])
    cmds.delete(all_loc_dict.values())

    cmds.cycleCheck(e=cycleCheck_state)

def quaternionToEuler(obj=None):
    rot = cmds.xform(obj, q=1, ro=1, os=1)
    rotOrder = cmds.getAttr('{}.rotateOrder'.format(obj))
    euler = OpenMaya2.MEulerRotation(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder)
    quat = euler.asQuaternion()
    euler = quat.asEulerRotation()
    r = euler.reorder(rotOrder)
    return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)

def correctAnimationKeys(startFrame=None, endFrame=None, correctList=None):
    if startFrame == None:
        playmin = cmds.playbackOptions(q=1, min=1)
    else:
        playmin = startFrame

    if endFrame == None:
        playmax = cmds.playbackOptions(q=1, max=1)
    else:
        playmax = endFrame

    if correctList == None:
        sel = cmds.ls(os=1)
    else:
        sel = correctList

    x = int(playmin)
    for i in range(int(playmax)+1):
        f = i + x
        cmds.currentTime(f)
        for obj in sel:
            val = quaternionToEuler(obj)
            cmds.xform(obj, ro=[val[0], val[1], val[2]], os=1, a=1)
            attr = cmds.listAttr(obj, k=1)
            for at in attr:
                cmds.setKeyframe('{}.{}'.format(obj, at), breakdown=0)

    cmds.currentTime(playmin)

def convert_fbx(fbx, save_path, convertType, fps, root_move_to_hip, animBase):
    # 保存するファイルタイプの指定　※現状'.ma'固定
    print('Start Convert: {}'.format(fbx))
    fileType = '.ma'

    # 保存するときのファイルタイプ
    if fileType == '.ma':
        fileTypeLn = 'mayaAscii'
    elif fileType == '.mb':
        fileTypeLn = 'mayaBinary'

    # 保存するときの処理
    fbxspl = fbx.split('/')
    fname = fbxspl[-1]

    # 保存先にファイルがあったらスキップする処理
    skip_exfile = os.path.exists('{}/{}'.format(save_path, fname.replace('.fbx', fileType)))
    if skip_exfile == True:
        return 'File Exist:{}'.format('{}/{}'.format(save_path, fname.replace('.fbx', fileType)))

    cmds.cycleCheck(e=0)
    cmds.autoKeyframe(state=False)

    # fkctrls
    fkctrls = []

    # fbxを開き、fpsとタイムレンジ取得
    cmds.file(f=1, new=1)
    cmds.file(fbx, f=1, o=1)
    cmds.currentUnit(time='{}fps'.format(fps))
    playmin = cmds.playbackOptions(q=1, min=1)
    playmax = cmds.playbackOptions(q=1, max=1)

    # convertTypeを指定
    """
    root_jnt = 'コンバート元のジョイント' string
    json_file = '読み込む割り当てのjsonファイル' string
    quaternion_sts = クオータニオン回転にするかしないか bool
    ctrl_sets = '流し込むリグのコントローラセット' string
    searchText = 'コンバート元が.maデータだった際にベイクするジョイント(cmds.ls()で取得するので*BindJtなどでもいける)' string
    """
    hik = False # humanIKで割り当てる設定
    const_dict = None # 強制的に割り当てる設定
    if convertType == 'bossBattleJD':
        root_jnt = 'rootBindJt'
        json_file = 'jd_def_ik.json'
        quaternion_sts = False
        ctrl_sets = 'CTRL_SETS'
        searchText = '*BindJt'
    elif convertType == 'mcjt':
        root_jnt = 'ply00_999_rig:j00_root_mcJt'
        json_file = 'mcJt_def_ik.json'
        quaternion_sts = False
        ctrl_sets = 'CTRL_SETS'
        searchText = '*_mcJt'
    elif convertType == 'rename':
        root_jnt = 'root_jnt'
        json_file = 'rename_def_ik.json'
        quaternion_sts = False
        ctrl_sets = 'CTRL_SETS'
        searchText = 'pelvis_C_001_body_jnt'
    elif convertType == 'sotai':
        root_jnt = 'root_jnt'
        json_file = 'sotai.json'
        quaternion_sts = False
        ctrl_sets = 'CtrlSet'
        searchText = 'pelvis_C_body_jnt'
    elif convertType == 'bindJoints':
        root_jnt = 'root_jnt'
        json_file = 'bindJoints.json'
        quaternion_sts = False
        ctrl_sets = 'CTRL_SETS'
        searchText = 'pelvis_C_body_jnt'
        # fbxのタイムレンジ取得
        if fbx.endswith('.fbx'):
            mel.eval('FBXRead -f "' + fbx + '";')
            result=mel.eval("FBXGetTakeLocalTimeSpan 1;")
            mel.eval("FBXClose;")
            playmin = round(result[0])
            playmax = round(result[1])
        elif fbx.endswith('.ma') or fbx.endswith('.mb'):
            pass

        print(playmin, playmax)
        cmds.currentUnit(time='{}fps'.format(fps))
        cmds.playbackOptions(ast=playmin, min=playmin, max=playmax, aet=playmax)

        maname = fbx.replace('.fbx', '.ma')
        fbx = '{}/temp/{}'.format(dir_path, maname.split('/')[-1])

        cmds.file(rn=fbx)
        cmds.file(f=1, save=1, type='mayaAscii')
    elif convertType == 'bindJoints_HIK':
        root_jnt = 'root_jnt'
        json_file = 'mutsunokami_mocap_hik.json'
        quaternion_sts = False
        ctrl_sets = 'CtrlSet'
        searchText = 'pelvis_C_body_jnt'
        # HumanIK用の変数
        hik_bindJoints_define = 'mutsunokami_biped_template.xml' # json_fileで割り当てた骨にHumanIKも割り当てたxml
        hik_default_define = 'mutsunokami_hik_template.xml'  # CreateSkeltonで作成されるデフォルトのxml
        hik = True
        pelvis = 'pelvis_C_body_jnt' # コンバート元の腰
        pelvis_pos = [0, 104, 0] # コンバート元の腰の位置
        const_dict = {'move_jnt':'move_ctrl', 'root_jnt':'main_ctrl'}
    elif convertType == 'bossBattleJD_HIK':
        root_jnt = 'rootBindJt'
        json_file = 'mutsunokami_mocap_hik.json'
        quaternion_sts = False
        ctrl_sets = 'CtrlSet'
        searchText = '*BindJt'
        # HumanIK用の変数
        hik_bindJoints_define = 'mutsunokami_biped_bossBattle_template.xml' # json_fileで割り当てた骨にHumanIKも割り当てたxml
        hik_default_define = 'mutsunokami_hik_template.xml'  # CreateSkeltonで作成されるデフォルトのxml
        hik = True
        pelvis = 'hipBindJt' # コンバート元の腰
        pelvis_pos = [0, 104, 0] # コンバート元の腰の位置
        const_dict = {'rootBindJt':'move_ctrl'}
        hip_move_ctrl = 'move_ctrl'
        hip_root_ctrl = 'main_ctrl'
        hip_ctrl = 'pelvis_C_fk_ctrl'
    elif convertType == 'MB_sotai':
        root_jnt = 'root_jnt'
        json_file = 'MB_sotai.json'
        quaternion_sts = False
        ctrl_sets = 'CtrlSet'
        searchText = 'pelvis_C_body_jnt'
    if convertType == 'bossBattle_mtp':
        root_jnt = 'rootBindJt'
        json_file = 'jd_def_ik.json'
        quaternion_sts = False
        ctrl_sets = 'CTRL_SETS'
        searchText = '*BindJt'
    else:
        print('コンバートするタイプを確認してください。')

    # fbxかmaかの処理
    # print('fbx or ma(mb)!')
    print('fbx or maya------------{}---------'.format(fbx))
    if fbx.endswith('.fbx'):
        cmds.file(f=1, new=1)
        cmds.file(animBase, f=1, o=1) # 流し込むデータを開く
        # fbxのタイムレンジ取得
        if convertType == 'bossBattleJD':
            pass
        else:
            mel.eval('FBXRead -f "' + fbx + '";')
            result=mel.eval("FBXGetTakeLocalTimeSpan 1;")
            mel.eval("FBXClose;")
            playmin = round(result[0])
            playmax = round(result[1])
        print(playmin, playmax)
    elif fbx.endswith('.ma') or fbx.endswith('.mb'):
        import_ma_to_fbx(fbx, root_jnt, searchText) # ma内を綺麗にする処理
        cmds.file(animBase, pr=1, ignoreVersion=1, i=1, importFrameRate=True, importTimeRange="override", mergeNamespacesOnClash=False, options="v=0;") # 流し込むデータをインポート

    cmds.clearCache(all=True)

    # Namespace取得
    # print('get name space!')
    nss_in_joints_proc = cmds.ls('*_proxy_jnt', type='joint', r=1)
    nss_buf_proc = ['{}'.format(nss_in.replace(nss_in.split(':')[-1], '')) for nss_in in nss_in_joints_proc]
    nss_list_proc = list(set(nss_buf_proc))
    try:
        nss_list_proc.remove('')
    except:
        pass
    nss_proc = nss_list_proc[0]

    # コンバート元のfbxの処理
    # print('import fbx file!')
    cmds.file('{}'.format(fbx), pr=1, ignoreVersion=1, i=1, type="FBX", importTimeRange="combine", mergeNamespacesOnClash=False, options="fbx") # fbxをインポート
    print('import ------------{}---------'.format(fbx))
    # mel.eval('FBXImport -file "{}";'.format(fbx))

    cmds.currentUnit(time='{}fps'.format(fps)) # fpsを設定
    cmds.playbackOptions(ast=playmin, min=playmin, max=playmax, aet=playmax) # タイムレンジを設定

    if convertType == 'bossBattle_mtp':
        # fpsを59.94に引き延ばしたアニメーションをコンバート
        open_path = 'z:/mtk/work/resources/animations/clips/player/ply00_swd/'
        mtp_query = {}
        bossbat_mtp = ['eq_rightHand', 'eq_shield']
        quest_mtp = ['hand01_R_mtp_ctrl', 'lowerarm01_L_mtp_ctrl']
        mtp_ctrls = []
        autokey_sts = cmds.autoKeyframe(q=1, st=1)
        if autokey_sts == True:
            cmds.autoKeyframe(st=False)

        x = int(playmin)
        for i in range(int(playmax)+1):
            f = i + x
            if f == int(playmax)+1:
                break
            else:
                cmds.currentTime(f)
            mtp_query['{}'.format(i)] = {quest_mtp[0]:[bossbat_mtp[0], cmds.xform(bossbat_mtp[0], q=1, t=1, ws=1), cmds.xform(bossbat_mtp[0], q=1, ro=1, ws=1)],
                                              quest_mtp[1]:[bossbat_mtp[1], cmds.xform(bossbat_mtp[1], q=1, t=1, ws=1), cmds.xform(bossbat_mtp[1], q=1, ro=1, ws=1)]}

        cmds.autoKeyframe(st=autokey_sts)

        skip_exfile = os.path.exists('{}/{}'.format(open_path, fname.replace('.fbx', fileType)))
        if skip_exfile == False:
            return 'Not Exist:{}'.format('{}/{}'.format(open_path, fname.replace('.fbx', fileType)))

        cmds.file('{}/{}'.format(open_path, fname.replace('.fbx', fileType)), f=1, o=1) # 流し込むデータを開く

        # orientConstOffset
        # eq_rightHand x -90, Y 90
        # eq_shield x -90, Z 180
        for k, v in mtp_query.items():
            cmds.currentTime(float(k))
            for kk, vv in v.items():
                mtp_ctrls.append('{}{}'.format(nss_proc, kk))
                # translate
                cmds.xform('{}{}'.format(nss_proc, kk), t=vv[1], ro=vv[2], ws=1, a=1)
                cmds.setKeyframe('{}{}'.format(nss_proc, kk), at='translate')
                # rotate
                if vv[0] == 'eq_rightHand':
                    cmds.rotate(0, 0, 0, '{}{}'.format(nss_proc, kk), r=1, os=1, fo=1)
                elif vv[0] == 'eq_shield':
                    cmds.rotate(0, 0, 0, '{}{}'.format(nss_proc, kk), r=1, os=1, fo=1)

                cmds.setKeyframe('{}{}'.format(nss_proc, kk), at='rotate')

        # オイラーフィルター
        cmds.filterCurve(mtp_ctrls, f='euler')

        cmds.file(rn='{}/{}'.format(save_path, fname.replace('.fbx', fileType)))
        cmds.file(f=1, save=1, type=fileTypeLn)
        print('Saved:{}/{}'.format(save_path, fname.replace('.fbx', fileType)))

        return


    # root_jntをworldに
    cmds.xform(root_jnt, t=[0, 0, 0], a=1)

    # rotateを全部0に
    # print('rotate zero!')
    src_jnt = cmds.ls(root_jnt, dag=1, type='joint')
    for jt in src_jnt:
        cmds.xform(jt, ro=[0, 0, 0], a=1)

    # print('import json!')
    # jsonファイルを変数に代入
    json = JsonFile()
    file_path = '{}/attach/{}'.format(dir_path, json_file)
    print('jason ------------{}---------'.format(file_path))

    # fkに切り替え
    if convertType == 'MB_sotai':
        cmds.setAttr("{0}:ball_R_fk_ctrl|{0}:shared_ikfk_crvShape.IKFK".format(nss_proc), 0)
        cmds.setAttr("{0}:hand_L_fk_ctrl|{0}:shared_ikfk_crvShape.IKFK".format(nss_proc), 0)
        cmds.setAttr("{0}:hand_R_fk_ctrl|{0}:shared_ikfk_crvShape.IKFK".format(nss_proc), 0)
        cmds.setAttr("{0}:ball_L_fk_ctrl|{0}:shared_ikfk_crvShape.IKFK".format(nss_proc), 0)

    # hikがTrueの場合の処理
    if hik == True:
        # 割り当てのディクショナリ
        defaultHikJoints = {u'Reference': 0,
                             u'Head': 15,
                             u'Hips': 1,
                             u'HipsTranslation': 49,
                             u'LeafLeftArmRoll1': 176,
                             u'LeafLeftArmRoll2': 184,
                             u'LeafLeftArmRoll3': 192,
                             u'LeafLeftArmRoll4': 200,
                             u'LeafLeftArmRoll5': 208,
                             u'LeafLeftForeArmRoll1': 177,
                             u'LeafLeftForeArmRoll2': 185,
                             u'LeafLeftForeArmRoll3': 193,
                             u'LeafLeftForeArmRoll4': 201,
                             u'LeafLeftForeArmRoll5': 209,
                             u'LeafLeftLegRoll1': 173,
                             u'LeafLeftLegRoll2': 181,
                             u'LeafLeftLegRoll3': 189,
                             u'LeafLeftLegRoll4': 197,
                             u'LeafLeftLegRoll5': 205,
                             u'LeafLeftUpLegRoll1': 172,
                             u'LeafLeftUpLegRoll2': 180,
                             u'LeafLeftUpLegRoll3': 188,
                             u'LeafLeftUpLegRoll4': 196,
                             u'LeafLeftUpLegRoll5': 204,
                             u'LeafRightArmRoll1': 178,
                             u'LeafRightArmRoll2': 186,
                             u'LeafRightArmRoll3': 194,
                             u'LeafRightArmRoll4': 202,
                             u'LeafRightArmRoll5': 210,
                             u'LeafRightForeArmRoll1': 179,
                             u'LeafRightForeArmRoll2': 187,
                             u'LeafRightForeArmRoll3': 195,
                             u'LeafRightForeArmRoll4': 203,
                             u'LeafRightForeArmRoll5': 211,
                             u'LeafRightLegRoll1': 175,
                             u'LeafRightLegRoll2': 183,
                             u'LeafRightLegRoll3': 191,
                             u'LeafRightLegRoll4': 199,
                             u'LeafRightLegRoll5': 207,
                             u'LeafRightUpLegRoll1': 174,
                             u'LeafRightUpLegRoll2': 182,
                             u'LeafRightUpLegRoll3': 190,
                             u'LeafRightUpLegRoll4': 198,
                             u'LeafRightUpLegRoll5': 206,
                             u'LeftArm': 9,
                             u'LeftFingerBase': 21,
                             u'LeftFoot': 4,
                             u'LeftFootExtraFinger1': 118,
                             u'LeftFootExtraFinger2': 119,
                             u'LeftFootExtraFinger3': 120,
                             u'LeftFootExtraFinger4': 121,
                             u'LeftFootIndex1': 102,
                             u'LeftFootIndex2': 103,
                             u'LeftFootIndex3': 104,
                             u'LeftFootIndex4': 105,
                             u'LeftFootMiddle1': 106,
                             u'LeftFootMiddle2': 107,
                             u'LeftFootMiddle3': 108,
                             u'LeftFootMiddle4': 109,
                             u'LeftFootPinky1': 114,
                             u'LeftFootPinky2': 115,
                             u'LeftFootPinky3': 116,
                             u'LeftFootPinky4': 117,
                             u'LeftFootRing1': 110,
                             u'LeftFootRing2': 111,
                             u'LeftFootRing3': 112,
                             u'LeftFootRing4': 113,
                             u'LeftFootThumb1': 98,
                             u'LeftFootThumb2': 99,
                             u'LeftFootThumb3': 100,
                             u'LeftFootThumb4': 101,
                             u'LeftForeArm': 10,
                             u'LeftHand': 11,
                             u'LeftHandExtraFinger1': 70,
                             u'LeftHandExtraFinger2': 71,
                             u'LeftHandExtraFinger3': 72,
                             u'LeftHandExtraFinger4': 73,
                             u'LeftHandIndex1': 54,
                             u'LeftHandIndex2': 55,
                             u'LeftHandIndex3': 56,
                             u'LeftHandIndex4': 57,
                             u'LeftHandMiddle1': 58,
                             u'LeftHandMiddle2': 59,
                             u'LeftHandMiddle3': 60,
                             u'LeftHandMiddle4': 61,
                             u'LeftHandPinky1': 66,
                             u'LeftHandPinky2': 67,
                             u'LeftHandPinky3': 68,
                             u'LeftHandPinky4': 69,
                             u'LeftHandRing1': 62,
                             u'LeftHandRing2': 63,
                             u'LeftHandRing3': 64,
                             u'LeftHandRing4': 65,
                             u'LeftHandThumb1': 50,
                             u'LeftHandThumb2': 51,
                             u'LeftHandThumb3': 52,
                             u'LeftHandThumb4': 53,
                             u'LeftInFootExtraFinger': 163,
                             u'LeftInFootIndex': 159,
                             u'LeftInFootMiddle': 160,
                             u'LeftInFootPinky': 162,
                             u'LeftInFootRing': 161,
                             u'LeftInFootThumb': 158,
                             u'LeftInHandExtraFinger': 151,
                             u'LeftInHandIndex': 147,
                             u'LeftInHandMiddle': 148,
                             u'LeftInHandPinky': 150,
                             u'LeftInHandRing': 149,
                             u'LeftInHandThumb': 146,
                             u'LeftLeg': 3,
                             u'LeftShoulder': 18,
                             u'LeftShoulderExtra': 170,
                             u'LeftToeBase': 16,
                             u'LeftUpLeg': 2,
                             u'Neck': 20,
                             u'Neck1': 32,
                             u'Neck2': 33,
                             u'Neck3': 34,
                             u'Neck4': 35,
                             u'Neck5': 36,
                             u'Neck6': 37,
                             u'Neck7': 38,
                             u'Neck8': 39,
                             u'Neck9': 40,
                             u'RightArm': 12,
                             u'RightFingerBase': 22,
                             u'RightFoot': 7,
                             u'RightFootExtraFinger1': 142,
                             u'RightFootExtraFinger2': 143,
                             u'RightFootExtraFinger3': 144,
                             u'RightFootExtraFinger4': 145,
                             u'RightFootIndex1': 126,
                             u'RightFootIndex2': 127,
                             u'RightFootIndex3': 128,
                             u'RightFootIndex4': 129,
                             u'RightFootMiddle1': 130,
                             u'RightFootMiddle2': 131,
                             u'RightFootMiddle3': 132,
                             u'RightFootMiddle4': 133,
                             u'RightFootPinky1': 138,
                             u'RightFootPinky2': 139,
                             u'RightFootPinky3': 140,
                             u'RightFootPinky4': 141,
                             u'RightFootRing1': 134,
                             u'RightFootRing2': 135,
                             u'RightFootRing3': 136,
                             u'RightFootRing4': 137,
                             u'RightFootThumb1': 122,
                             u'RightFootThumb2': 123,
                             u'RightFootThumb3': 124,
                             u'RightFootThumb4': 125,
                             u'RightForeArm': 13,
                             u'RightHand': 14,
                             u'RightHandExtraFinger1': 94,
                             u'RightHandExtraFinger2': 95,
                             u'RightHandExtraFinger3': 96,
                             u'RightHandExtraFinger4': 97,
                             u'RightHandIndex1': 78,
                             u'RightHandIndex2': 79,
                             u'RightHandIndex3': 80,
                             u'RightHandIndex4': 81,
                             u'RightHandMiddle1': 82,
                             u'RightHandMiddle2': 83,
                             u'RightHandMiddle3': 84,
                             u'RightHandMiddle4': 85,
                             u'RightHandPinky1': 90,
                             u'RightHandPinky2': 91,
                             u'RightHandPinky3': 92,
                             u'RightHandPinky4': 93,
                             u'RightHandRing1': 86,
                             u'RightHandRing2': 87,
                             u'RightHandRing3': 88,
                             u'RightHandRing4': 89,
                             u'RightHandThumb1': 74,
                             u'RightHandThumb2': 75,
                             u'RightHandThumb3': 76,
                             u'RightHandThumb4': 77,
                             u'RightInFootExtraFinger': 169,
                             u'RightInFootIndex': 165,
                             u'RightInFootMiddle': 166,
                             u'RightInFootPinky': 168,
                             u'RightInFootRing': 167,
                             u'RightInFootThumb': 164,
                             u'RightInHandExtraFinger': 157,
                             u'RightInHandIndex': 153,
                             u'RightInHandMiddle': 154,
                             u'RightInHandPinky': 156,
                             u'RightInHandRing': 155,
                             u'RightInHandThumb': 152,
                             u'RightLeg': 6,
                             u'RightShoulder': 19,
                             u'RightShoulderExtra': 171,
                             u'RightToeBase': 17,
                             u'RightUpLeg': 5,
                             u'Spine': 8,
                             u'Spine1': 23,
                             u'Spine2': 24,
                             u'Spine3': 25,
                             u'Spine4': 26,
                             u'Spine5': 27,
                             u'Spine6': 28,
                             u'Spine7': 29,
                             u'Spine8': 30,
                             u'Spine9': 31}

        #
        if convertType == 'bindJoints_HIK' or convertType == 'bossBattleJD_HIK':
            src_xml_path = '{}/attach/hik/{}'.format(dir_path, hik_bindJoints_define)
            dst_xml_path = '{}/attach/hik/{}'.format(dir_path, hik_default_define)

        src_tree = ET.parse(src_xml_path)
        src_root = src_tree.getroot()

        dst_tree = ET.parse(dst_xml_path)
        dst_root = dst_tree.getroot()

        # hikのデフォルトのスケルトンを読み込む
        try:
            cmds.delete('HIK*')
            cmds.delete('Character1_Reference')
            mel.eval('file -import -type "mayaBinary"  -ignoreVersion -mergeNamespacesOnClash false -rpr "defaultHikBase" -options "v=0;"  -pr  -importTimeRange "combine" "//cgs-str-fas05/100_projects/117_mutsunokami/30_design/Rig/02_framework/test/0007/hik/template/defaultHikBase.mb";')
            cmds.select(cl=1)
        except:
            mel.eval('file -import -type "mayaBinary"  -ignoreVersion -mergeNamespacesOnClash false -rpr "defaultHikBase" -options "v=0;"  -pr  -importTimeRange "combine" "//cgs-str-fas05/100_projects/117_mutsunokami/30_design/Rig/02_framework/test/0007/hik/template/defaultHikBase.mb";')
            cmds.select(cl=1)

    # json_fileからオブジェクトを変数に代入する
    objects = json.read('{}'.format(file_path))

    readObjects = []

    # 割り当てのオブジェクトをjson_fileからトランスフォーム
    for obj in objects.keys():
        splObj = obj.split('->')[1]
        splJnt = obj.split('->')[0]
        if cmds.objExists(splJnt) == False:
            continue
        if nss_proc == '':
            selectObject = '{}'.format(splObj)
        else:
            selectObject = '{}:{}'.format(nss_proc, splObj)
        if cmds.objExists(selectObject) == False:
            continue
        cmds.xform(splJnt, t=objects[obj][0], a=1)
        cmds.xform(splJnt, ro=objects[obj][1], a=1)
        cmds.xform(selectObject, t=objects[obj][2], a=1)
        cmds.xform(selectObject, ro=objects[obj][3], a=1)
        readObjects.append(obj)

    if readObjects == []:
        print('not read objects ---------------------')
        error_results.append((fbx, 'not read objects'))
        return

    print('{} read ---------------------'.format(readObjects))

    mcs = 'mocapConnectionsSets'
    if cmds.objExists(mcs) == False:
        cmds.createNode('objectSet', n='mocapConnectionsSets')
    connectObjects = []
    cmds.clearCache(all=True)

    # json_fileの設定から拘束
    for obj in objects.keys():
        splObj = obj.split('->')[1]
        splJnt = obj.split('->')[0]
        if cmds.objExists(splJnt) == False:
            continue
        if nss_proc == '':
            selectObject = '{}'.format(splObj)
        else:
            selectObject = '{}:{}'.format(nss_proc, splObj)
        if cmds.objExists(selectObject) == False:
            continue
        attr = cmds.listAttr(selectObject, k=1)
        if 'PoleVectorCtrl' in objects[obj]:
            # print(selectObject)
            dup = cmds.duplicate(selectObject, po=1)[0]
            connectObjects.append(dup)
            cmds.setAttr('{}.rx'.format(dup), k=1)
            cmds.setAttr('{}.ry'.format(dup), k=1)
            cmds.setAttr('{}.rz'.format(dup), k=1)
            pac = cmds.parentConstraint(splJnt, dup, w=1, mo=1)
            poc = cmds.pointConstraint(dup, selectObject, w=1, mo=1)
            connectObjects.append(pac[0])
            connectObjects.append(poc[0])
        else:
            try:
                if 'translateX' in attr or 'translateY' in attr or 'translateZ' in attr:
                    # print(selectObject)
                    flags = trans_skippy(selectObject)
                    poc = cmds.pointConstraint(splJnt, selectObject, w=1, mo=1, **flags)
                    connectObjects.append(poc[0])
            except Exception as e:
                pass
        try:
            if 'rotateX' in attr or 'rotateY' in attr or 'rotateZ' in attr:
                flags = rot_skippy(selectObject)
                ori = cmds.orientConstraint(splJnt, selectObject, w=1, mo=1, **flags)
                connectObjects.append(ori[0])
                pbn = cmds.createNode('pairBlend', n='{}_pbn'.format(selectObject), ss=1)
                if quaternion_sts == True:
                    cmds.setAttr('{}.rotInterpolation'.format(pbn), 1)
                # print(flags.values()[0])
                enableAttrs = flags.values()[0]
                axis = ['X', 'Y', 'Z']
                for ax in enableAttrs:
                    if ax == 'x':
                        axis.remove('X')
                    if ax == 'y':
                        axis.remove('Y')
                    if ax == 'z':
                        axis.remove('Z')
                for at in axis:
                    cmds.connectAttr('{}.constraintRotate{}'.format(ori[0], at), '{}.inRotate{}2'.format(pbn, at), f=1)
                    cmds.connectAttr('{}.outRotate{}'.format(pbn, at), '{}.rotate{}'.format(selectObject, at), f=1)
        except Exception as e:
            # print('json error', e)
            # error_results.append((fbx, e))
            pass

    if connectObjects == []:
        print('not contraints ---------------------')
        error_results.append((fbx, 'not contraints'))

    if hik == True:
        # hikのデフォルトの骨の割り当て
        mel.eval('hikCreateDefinition;')
        for i in range(len(dst_root[0])):
            try:
                if dst_root[0][i].get('value') != '':
                    try:
                        mel.eval('setCharacterObject("Character1_{0}","Character1",{1},0);'.format(dst_root[0][i].get('value'), defaultHikJoints[dst_root[0][i].get('key')]))
                    except KeyError:
                        pass
            except RuntimeError:
                pass
        mel.eval('$gCurrentCharacter = "Character1";refreshAllCharacterLists();hikToggleLockDefinition();')

        # 流し込み元のデータの処理
        # fbxの骨のrotateをすべて0にするのは上のほうで処理されているので、腰位置を決める
        if convertType == 'bindJoints_HIK' or convertType == 'bossBattleJD_HIK':
            cmds.xform(pelvis, t=pelvis_pos, os=1, a=1)

        # srcの割り当て
        mel.eval('hikCreateDefinition;')
        for i in range(len(src_root[0])):
            try:
                if src_root[0][i].get('value') != '':
                    try:
                        mel.eval('setCharacterObject("{0}","Character2",{1},0);'.format(src_root[0][i].get('value'), defaultHikJoints[src_root[0][i].get('key')]))
                    except KeyError:
                        pass
            except RuntimeError:
                pass
        mel.eval('$gCurrentCharacter = "Character2";refreshAllCharacterLists();hikToggleLockDefinition();')

        # sourceの切替
        mel.eval("""
        $gCurrentCharacter = "Character1";
        refreshAllCharacterLists();
        //optionMenuGrp -e -v "Character1" hikCharacterList;
        //hikUpdateCurrentCharacterFromUI();
        //hikUpdateContextualUI();
        $gCurrentCharacter = "Character2";
        refreshAllCharacterLists();
        mayaHIKsetCharacterInput( "Character1","Character2" );
        //refreshAllSourceLists();
        //optionMenuGrp -e -v " Character2" hikSourceList;
        //hikUpdateCurrentSourceFromUI;
        //hikUpdateContextualUI;
        refreshAllCharacterLists();""")

        # match source
        mel.eval('setAttr "HIKproperties1.ForceActorSpace" 1;')
        cmds.setAttr("neck_C_fk_ctrl_orientConstraint1.offsetX", -6.048825)
        cmds.setAttr("head_C_fk_ctrl_orientConstraint1.offsetX", 2.967921)

    # コネクション用のsetsを作成
    mcss = cmds.listConnections('{}.dagSetMembers'.format(mcs), s=1, d=0)
    if mcss == None:
        i = 0
    else:
        i = len(mcss) + 1
    for obj in connectObjects:
        cmds.connectAttr('{}.instObjGroups[0]'.format(obj), '{}.dagSetMembers[{}]'.format(mcs, i), f=1)
        i += 1
    cmds.clearCache(all=True)

    # ネームスペースをコントローラセットに代入
    if nss_proc == '':
        nss_ctrl_sets = '{}'.format(ctrl_sets)
    else:
        nss_ctrl_sets = '{}{}'.format(nss_proc, ctrl_sets)

    # コントローラsets内を取得
    # print('get connections!')
    print('Ctrls Set :{}'.format(nss_ctrl_sets))
    # ctrls = cmds.listConnections('{}.dagSetMembers'.format(nss_ctrl_sets), s=1, d=0)
    cmds.select(nss_ctrl_sets, r=1, ne=1);cmds.pickWalk(d='down')
    ctrls = cmds.ls(sl=1, type='transform')

    # OPTIMIZE all check
    mel.eval("cleanUpScene 3")
    print('Scene Optimized')
    print('Ctrls :{}'.format(ctrls))

    # fkに切り替え
    if convertType == 'sotai' or convertType == 'bindJoints_HIK' or convertType == 'bossBattleJD_HIK' or convertType == 'MB_sotai':
        cmds.setAttr("{0}ballend_R_fk_ctrl|{0}legs_R_01_IKFK_shared_crvShape.IKFK".format(nss_proc), 0)
        cmds.setAttr("{0}hand_L_fk_ctrl|{0}arms_L_01_IKFK_shared_crvShape.IKFK".format(nss_proc), 0)
        cmds.setAttr("{0}hand_R_fk_ctrl|{0}arms_R_01_IKFK_shared_crvShape.IKFK".format(nss_proc), 0)
        cmds.setAttr("{0}ballend_L_fk_ctrl|{0}legs_L_01_IKFK_shared_crvShape.IKFK".format(nss_proc), 0)

    # 強制的にコンストレイントさせる
    if const_dict == None:
        pass
    elif const_dict != None:
        for k, v in const_dict.items():
            try:
                trans_flags = trans_skippy('{}:{}'.format(nss_proc, v))
                cmds.pointConstraint(k, '{}:{}'.format(nss_proc, v), w=1, mo=1, **trans_flags)
                rotate_flags = rot_skippy('{}:{}'.format(nss_proc, v))
                cmds.orientConstraint(k, '{}:{}'.format(nss_proc, v), w=1, mo=1, **rotate_flags)
            except Exception as e:
                pass
            try:
                trans_flags = trans_skippy('{}{}'.format(nss_proc, v))
                cmds.pointConstraint(k, '{}{}'.format(nss_proc, v), w=1, mo=1, **trans_flags)
                rotate_flags = rot_skippy('{}{}'.format(nss_proc, v))
                cmds.orientConstraint(k, '{}{}'.format(nss_proc, v), w=1, mo=1, **rotate_flags)
            except Exception as e:
                pass

    pa_cons = []
    if convertType == 'MB_sotai':
        zeroOut_rot = [0, 0, 0]
        zeroOut_trans = [0, 0, 0]
        mtp_jnts = cmds.ls('*_mtp_jnt')
        for m_jnt in mtp_jnts:
            # cmds.setAttr('{}.t'.format(m_jnt), *zeroOut_rot);cmds.setAttr('{}.r'.format(m_jnt), *zeroOut_trans)
            try:
                pa_con = cmds.parentConstraint('{}'.format(m_jnt), '{}:{}'.format(nss_proc, m_jnt.replace('_mtp_jnt', '_mtp_ctrl')),  w=1)
                pa_cons.append(pa_con[0])
            except:
                pass
            try:
                pa_con = cmds.parentConstraint('{}'.format(m_jnt), '{}{}'.format(nss_proc, m_jnt.replace('_mtp_jnt', '_mtp_ctrl')),  w=1)
                pa_cons.append(pa_con[0])
            except:
                pass

    # ベイク
    # print('bake!')
    # cmds.refresh(su=1)
    cmds.bakeResults(ctrls, sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
    cmds.clearCache(all=True)

    if pa_cons != []:
        try:
            cmds.delete(pa_cons)
        except:
            pass

    # cmds.refresh(su=0)
    print('Bake Animation')

    # キーのQuaternion変換
    correctAnimationKeys(startFrame=playmin, endFrame=playmax, correctList=ctrls)
    cmds.clearCache(all=True)

    print('correct anim key')

    # fk to ikマッチ
    if convertType == 'sotai' or convertType == 'MB_sotai':
        execfile('Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/convert/matchbake/sotaiiktofk.py')
        print('sotai ik to fk match bake')
    elif convertType == 'bindJoints_HIK' or convertType == 'bossBattleJD_HIK':
        execfile('Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/convert/matchbake/sotaiiktofk.py')
        print('humanik ik to fk match bake')
    else:
        # execfile('Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/convert/matchbake/ikToFkBake.py')
        execfile('Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/convert/matchbake/fkToIkBake.py')

    cmds.clearCache(all=True)

    print('fk to ik match --desable--')

    # オイラーフィルター
    cmds.filterCurve(ctrls, f='euler')
    print('euler filter')

    cmds.refresh(cv=1)

    # コネクションで使ったオブジェクトを削除
    cmds.select(mcs, r=1, ne=1)
    cmds.pickWalk(d='down')
    connections = cmds.ls(sl=1)
    cmds.delete(connections)

    # rootジョイントの削除
    cmds.delete(root_jnt)
    print('delete root joint')
    if hik == True:
        cmds.delete('HIK*')
        cmds.delete('Character1_Reference')

    if convertType == 'rename':
        cmds.file('Z:/mtk/work/resources/animations/clips/player/workscenes/anm_ply00_m_999_rig.ma', loadReference="ply00_m_999_000RN")

    # keyの整理
    dKeys = cmds.ls(type=("animCurveUL","animCurveUA","animCurveUT","animCurveUU"))
    keys = cmds.ls(type='animCurve')
    drivenkeys = list(set(keys) & set(dKeys))
    keys = [sk for sk in keys if sk not in drivenkeys]
    for kk in keys:
        firstKey = cmds.findKeyframe(kk, which='first')
        lastKey = cmds.findKeyframe(kk, which='last')

        if playmin == firstKey:
            pass
        else:
            cmds.cutKey(kk, time=(firstKey, playmin-1))
        if playmax == lastKey:
            pass
        else:
            cmds.cutKey(kk, time=(playmax+1, lastKey))

    if convertType == 'sotai' or convertType == 'bindJoints_HIK' or convertType == 'bossBattleJD_HIK' or convertType == 'MB_sotai':
        cmds.setAttr("{0}ballend_R_fk_ctrl|{0}legs_R_01_IKFK_shared_crvShape.IKFK".format(nss_proc), 1)
        cmds.setAttr("{0}hand_L_fk_ctrl|{0}arms_L_01_IKFK_shared_crvShape.IKFK".format(nss_proc), 1)
        cmds.setAttr("{0}hand_R_fk_ctrl|{0}arms_R_01_IKFK_shared_crvShape.IKFK".format(nss_proc), 1)
        cmds.setAttr("{0}ballend_L_fk_ctrl|{0}legs_L_01_IKFK_shared_crvShape.IKFK".format(nss_proc), 1)

    # main_ctrlとmove_ctrlをヒップに追従
    if root_move_to_hip == 'Yes':
        try:
            cmds.select(cl=1)
            correct_ctrls = {'{}:{}'.format(nss_proc, hip_root_ctrl):['{}:{}'.format(nss_proc, hip_ctrl), {'skipTranslate':'y', 'mo':1, 'weight':1, 'skipRotate':['x', 'z']}]}
            const_bake(correct_ctrls=correct_ctrls, ctrl_set=nss_ctrl_sets, from_sets=True, selection=True, select_timeslider=False, timerange=None)
        except:
            pass
        try:
            cmds.select(cl=1)
            correct_ctrls = {'{}{}'.format(nss_proc, hip_root_ctrl):['{}{}'.format(nss_proc, hip_ctrl), {'skipTranslate':'y', 'mo':1, 'weight':1, 'skipRotate':['x', 'z']}]}
            const_bake(correct_ctrls=correct_ctrls, ctrl_set=nss_ctrl_sets, from_sets=True, selection=True, select_timeslider=False, timerange=None)
        except:
            pass
    else:
        pass

    if convertType == 'bossBattleJD_HIK':
        # オイラーフィルター
        cmds.filterCurve(ctrls, f='euler')
        print('euler filter:bossBattleJD_HIK')


    cmds.file(rn='{}/{}'.format(save_path, fname.replace('.fbx', fileType)))
    cmds.file(f=1, save=1, type=fileTypeLn)
    print('Saved:{}/{}'.format(save_path, fname.replace('.fbx', fileType)))

    if convertType == 'bindJoints':
        # cmds.delete(fbx)
        try:
            os.remove(fbx)
        except Exception as e:
            print(e)

    return None

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

        dirname, basename = os.path.split(file_path) # "/"でsplitされる
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with codecs.open(file_path, 'w', 'utf-8') as f:
            json.dump(data, f, indent=4) # indentフラグはdictionaryをspace4つごとにきれいに書き込み
            f.flush()
            os.fsync(f.fileno()) # ディスクの書き込み
