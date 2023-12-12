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

u"""
from tkgTools.tkgRig.scripts.convert.hik import common as hik_common
reload(hik_common)

# コントローラの書き出し
ctrls = cmds.ls(os=1)
common.objectValues(joints=ctrls, export_or_import='export', fix=True, file_path=None, namespace=None)

# HIKの読み込み
# character2_root_jointをcharacter1_root_jointに流し込む
common.hik_define(character1='char_001', character2='char_000', character1_root_joint='root_jnt', character2_root_joint='root_jnt')

# コントローラの読み込み
ctrls = cmds.ls(os=1)
common.objectValues(joints=ctrls, export_or_import='import', fix=True, file_path=None, namespace=None)
# common.objectValues(joints=ctrls, export_or_import='export', fix=True, file_path=None, namespace=None)

# ジョイントからコントローラに拘束させるときの設定
cConst = common.ConstraintList()

cConst.set_objects(0) # 選択しているオブジェクトを登録 0='parent', 1='point', 2='orient'

cConst.remove_list() # 選択しているオブジェクトを削除

cConst.import_settings() # cacheフォルダの設定を読み込む

cConst.mirror_settings(mirror_names=['_L_', '_R_']) # mirror

cConst.set_objects_in_selection(2) # 選択しているオブジェクト順に登録

cConst.constraint() # jsonファイルからコンストレイント

# 実行コマンド
from maya import cmds, mel

from tkgTools.tkgRig.scripts.convert.hik import common as hik_common
reload(hik_common)

hik_common.hik_define(character1='char_000', character2='char_002', character1_root_joint='root_jnt', character2_root_joint='Reference')

cmds.select('ply00_m_000_000:ctrls_sets', r=1, ne=1)
ctrls = cmds.pickWalk(d='down')
file_path = 'C:/Users/shunsuke/Documents/maya/scripts/tkgTools/tkgRig/scripts/convert/hik/data/characters/char_000/char_000_ctrls.json'
hik_common.objectValues(joints=ctrls, export_or_import='import', fix=True, file_path=file_path, namespace=None)

cConst = hik_common.ConstraintList()
cConst.constraint(file_path='C:/Users/shunsuke/Documents/maya/scripts/tkgTools/tkgRig/scripts/convert/hik/data/characters/char_000/connect_ctrls.json')


"""

class ConstraintList(object):
    def __init__(self):
        self.set_list = {}
        self.const_types = {0:'parent',
                            1:'point',
                            2:'orient',
                            3:'point/orient'}
        self.cache_file_path = '{0}/cache/'.format(dir_path)

        if not os.path.isdir(self.cache_file_path):
            os.mkdir(self.cache_file_path)

        self.import_settings()

    def set_objects(self, const_type, drive_obj=None, driven_obj=None, cache=True):
        if not drive_obj and not driven_obj:
            sel = cmds.ls(os=1)
            drive_obj = sel[0]
            driven_obj = sel[1]
        self.set_list['{0}-{1}'.format(drive_obj, self.const_types[const_type])] = driven_obj
        print(self.set_list)
        if cache:
            if not os.path.isdir(self.cache_file_path):
                os.mkdir(self.cache_file_path)
            self.export_settings(file_path='{0}cache.json'.format(self.cache_file_path))

    def set_objects_in_selection(self, const_type):
        sel = cmds.ls(os=1)
        if sel:
            drivers = sel[::2]
            drivens = sel[1::2]
            for i, (drive_obj, driven_obj) in enumerate(zip(drivers, drivens)):
                self.set_objects(const_type, drive_obj=drive_obj, driven_obj=driven_obj)

    def remove_list(self, cache=True):
        sel = cmds.ls(os=1)
        self.set_list.pop(sel[0])
        print(self.set_list)
        if cache:
            if not os.path.isdir(self.cache_file_path):
                os.mkdir(self.cache_file_path)
            self.export_settings(file_path='{0}cache.json'.format(self.cache_file_path))

    def export_settings(self, file_path=None):
        create_json = JsonFile()
        if not file_path:
            file_path = fileDialog_export()
        if not file_path:
            return
        dirname, basename = os.path.split(file_path)
        save_file_path = '{0}/{1}'.format(dirname, basename)
        create_json.write('{0}'.format(save_file_path), self.set_list)

        return save_file_path

    def import_settings(self, file_path=None, cache=True):
        create_json = JsonFile()
        if cache:
            file_path = '{0}cache.json'.format(self.cache_file_path)
        if not file_path:
            file_path = fileDialog_import()
        if not file_path:
            return

        dirname, basename = os.path.split(file_path)
        import_file_path = '{0}/{1}'.format(dirname, basename)
        import_values = create_json.read(import_file_path)

        self.set_list = import_values

        return import_file_path

    def mirror_settings(self, mirror_names=['', '']):
        for k, v in self.set_list.items():
            print(k)
            mir_k = k.replace(mirror_names[0], mirror_names[1])
            mir_v = v.replace(mirror_names[0], mirror_names[1])
            self.set_list[mir_k] = mir_v

        self.export_settings(file_path='{0}cache.json'.format(self.cache_file_path))

    def constraint(self, file_path=None):
        create_json = JsonFile()
        if not file_path:
            file_path = fileDialog_import()

        dirname, basename = os.path.split(file_path)
        import_file_path = '{0}/{1}'.format(dirname, basename)
        import_values = create_json.read(import_file_path)

        HIK_constraint_sets = 'HIK_constraint_sets'
        if not cmds.objExists(HIK_constraint_sets):
            cmds.sets(em=1, n=HIK_constraint_sets)

        for k, v in import_values.items():
            driver_obj = k.split('-')[0]
            const_type = k.split('-')[1]
            if cmds.objExists(driver_obj) and cmds.objExists(v):
                tr_skips = trans_skippy(v)
                ro_skips = rot_skippy(v)
                if const_type == 'parent':
                    pa_con = cmds.parentConstraint(driver_obj, v, mo=1, w=1)[0]
                    cmds.sets(pa_con, add=HIK_constraint_sets)
                elif const_type == 'point':
                    po_con = cmds.pointConstraint(driver_obj, v, mo=1, w=1, **tr_skips)[0]
                    cmds.sets(po_con, add=HIK_constraint_sets)
                elif const_type == 'orient':
                    or_con = cmds.orientConstraint(driver_obj, v, mo=1, w=1, **ro_skips)[0]
                    cmds.sets(or_con, add=HIK_constraint_sets)
                elif const_type == 'point/orient':
                    po_con = cmds.pointConstraint(driver_obj, v, mo=1, w=1, **tr_skips)[0]
                    or_con = cmds.orientConstraint(driver_obj, v, mo=1, w=1, **ro_skips)[0]
                    cmds.sets(po_con, add=HIK_constraint_sets)
                    cmds.sets(or_con, add=HIK_constraint_sets)
            else:
                print(u'{0}, {1}は存在しません。'.format(driver_obj, v))

    def add_prefix(self, drivers_prefix_name='', drivens_prefix_name=''):
        new_set_list = {}
        for k, v in self.set_list.items():
            print(k)
            pre_k = '{0}{1}'.format(drivers_prefix_name, k)
            pre_v = '{0}{1}'.format(drivens_prefix_name, v)
            new_set_list[pre_k] = pre_v

        self.set_list = new_set_list
        self.export_settings(file_path='{0}cache.json'.format(self.cache_file_path))


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

def hik_define(character1=None, character2=None, character1_root_joint=None, character2_root_joint=None):
    u"""
    character2が元のモーション
    character1が転送先
    """
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


    hiks = cmds.ls('*HIK*')
    for obj in hiks:
        if cmds.objExists(obj):
            cmds.delete(obj)

    # ---
    # character1
    # ---
    if cmds.objExists('HIK_{0}:{1}'.format(character1, character1_root_joint)):
        cmds.delete('HIK_{0}:{1}'.format(character1, character1_root_joint))
    if cmds.namespace(ex='HIK_{0}'.format(character1)):
        cmds.namespace(rm='HIK_{0}'.format(character1))

    cmds.file("{0}/data/characters/{1}/{1}.ma".format(dir_path, character1), pr=1, ignoreVersion=1, i=1, type="mayaAscii", importTimeRange="combine", mergeNamespacesOnClash=False, options="v=0;", namespace='HIK_{0}'.format(character1))

    dst_tree = ET.parse("{0}/data/characters/{1}/{1}.xml".format(dir_path, character1))
    dst_root = dst_tree.getroot()

    mel.eval('HIKCharacterControlsTool;')

    # hikのデフォルトの骨の割り当て
    mel.eval('hikCreateDefinition;')
    # mel.eval('hikCreateCharacter( "Character1" )')
    for i in range(len(dst_root[0])):
        try:
            if dst_root[0][i].get('value') != '':
                try:
                    mel.eval('setCharacterObject("HIK_{2}:{0}","Character1",{1},0);'.format(dst_root[0][i].get('value'), defaultHikJoints[dst_root[0][i].get('key')], character1))
                except KeyError:
                    pass
        except RuntimeError:
            pass
    mel.eval('$gCurrentCharacter = "Character1";refreshAllCharacterLists();hikToggleLockDefinition();')

    # ---
    # character2
    # ---
    if cmds.objExists('HIK_{0}:{1}'.format(character2, character2_root_joint)):
        cmds.delete('HIK_{0}:{1}'.format(character2, character2_root_joint))
    if cmds.namespace(ex='HIK_{0}'.format(character2)):
        cmds.namespace(rm='HIK_{0}'.format(character2))

    cmds.file("{0}/data/characters/{1}/{1}.ma".format(dir_path, character2), pr=1, ignoreVersion=1, i=1, type="mayaAscii", importTimeRange="combine", mergeNamespacesOnClash=False, options="v=0;")

    src_tree = ET.parse("{0}/data/characters/{1}/{1}.xml".format(dir_path, character2))
    src_root = src_tree.getroot()

    # srcの割り当て
    mel.eval('hikCreateDefinition;')
    # mel.eval('hikCreateCharacter( "Character2" )')
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

def objectValues(joints=None, export_or_import='import', fix=True, file_path=None, namespace=None):
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
            if namespace:
                dst_namespace = ':'.join(re.split('[:]', key)[:-1])
                obj_attr = key.replace(dst_namespace, namespace)
            else:
                obj_attr = key
            try:
                cmds.setAttr(obj_attr, value)
            except Exception as e:
                pass
                # traceback.print_exc()

        return import_file_path

def export_ctrl_values(ctrls):
    file_path = objectValues(joints=ctrls, export_or_import='export', fix=True)
    print(file_path)

def import_ctrls_json_file(file_path_txt, CtrlSet, src_namespace):
    file_path = objectValues(joints=self.ctrls, export_or_import='import', fix=True, file_path=file_path_txt, namespace=src_namespace)
    print(file_path)
