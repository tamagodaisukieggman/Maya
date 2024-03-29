# -*- coding: utf-8 -*-
import fnmatch
from imp import reload
import math
import os
import traceback

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

from imp import reload
import rig.convert.hik.common as hik_convert
reload(hik_convert)
# hik_convert.do_convert()

MAYA_LOCATION = os.environ['MAYA_LOCATION']
mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikGlobalUtils.mel"')
mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikCharacterControlsUI.mel"')
mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikDefinitionOperations.mel"')

FROM_PATH = 'C:/cygames/wiz2/tools/maya/scripts/rig/convert/fbx/from'
SAVE_PATH = 'C:/cygames/wiz2/tools/maya/scripts/rig/convert/fbx/save'

p1_JOINT_PATH = 'c:/cygames/wiz2/tools/maya/scripts/rig/convert/hik/data/wizard2/p1/p1.ma'
p2_JOINT_PATH = 'c:/cygames/wiz2/tools/maya/scripts/rig/convert/hik/data/wizard2/p2/p2.ma'
enm_m_ghost01_JOINT_PATH = 'c:/cygames/wiz2/tools/maya/scripts/rig/convert/hik/data/wizard2/ghost01/enm_m_ghost01.ma'

FPS = 30

mel.eval('FBXProperty Import|AdvOptGrp|UI|ShowWarningsManager -v 0;')
mel.eval('FBXProperty Export|AdvOptGrp|UI|ShowWarningsManager -v 0;')

def find_files(directory=None, pattern=None, exact=None):
    for root, dirs, files in os.walk(directory):
        if root.endswith(exact):
            continue
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def file_import(file_path):
    if file_path.endswith('.ma'):
        scene_type = 'mayaAscii'
        scene_options = 'v=0;p=17;f=0'
    elif file_path.endswith('.mb'):
        scene_type = 'mayaBinary'
        scene_options = 'v=0;'
    elif file_path.endswith('.fbx'):
        scene_type = 'FBX'
        scene_options = 'fbx'

        print('FBXRead -f "' + file_path + '";')

        mel.eval('FBXRead -f "' + file_path + '";')
        result=mel.eval('FBXGetTakeLocalTimeSpan 1;')
        mel.eval('FBXClose;')
        playmin = round(result[0])
        playmax = round(result[1])

    cmds.file(file_path,
              pr=True,
              ignoreVersion=True,
              i=True,
              type=scene_type,
              importFrameRate=True,
              importTimeRange="override",
              mergeNamespacesOnClash=False,
              options=scene_options)

    cmds.currentUnit(time='{}fps'.format(FPS))
    cmds.playbackOptions(min=playmin, max=playmax, ast=playmin, aet=playmax)

    return playmin, playmax

def bake(nodes=None, playmin=None, playmax=None, at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz']):
    cmds.bakeResults(nodes,
                     simulation=True,
                     sampleBy=True,
                     oversamplingRate=True,
                     disableImplicitControl=True,
                     preserveOutsideKeys=True,
                     sparseAnimCurveBake=False,
                     removeBakedAttributeFromLayer=False,
                     removeBakedAnimFromLayer=False,
                     bakeOnOverrideLayer=False,
                     minimizeRotation=True,
                     at=at,
                     t=(playmin, playmax)
                     )

def get_animation_status():
    # アニメーションの設定の取得
    start = cmds.playbackOptions(q=True, min=True)
    end = cmds.playbackOptions(q=True, max=True)
    animstart = cmds.playbackOptions(q=True, ast=True)
    animend = cmds.playbackOptions(q=True, aet=True)
    curtime = cmds.currentTime(q=True)
    if cmds.autoKeyframe(q=True, st=True):
        autoKeyState = True
    else:
        autoKeyState = False
    cmds.autoKeyframe(st=False)
    return start, end, animstart, animend, curtime, autoKeyState

def set_animation_status(start, end, animstart, animend, curtime, autoKeyState):
    # get_animation_statusで取得した値の設定
    cmds.playbackOptions(min=start)
    cmds.playbackOptions(max=end)
    cmds.playbackOptions(ast=animstart)
    cmds.playbackOptions(aet=animend)
    cmds.currentTime(curtime)
    cmds.autoKeyframe(st=autoKeyState)

def bake_with_func(func):
    # 1フレームごとに処理する
    def wrapper(*args, **kwargs):
        try:
            cmds.refresh(su=1)

            # get
            start, end, animstart, animend, curtime, autoKeyState = get_animation_status()

            for i in range (int(start), int(end+1)):
                cmds.currentTime(i, e=True)
                func(*args, **kwargs)

            # set
            set_animation_status(start, end, animstart, animend, curtime, autoKeyState)

            cmds.refresh(su=0)

        except:
            cmds.refresh(su=0)
            print(traceback.format_exc())

    return wrapper

def quaternionToEuler(obj=None):
    rot = cmds.xform(obj, q=True, ro=True, os=True)
    rotOrder = cmds.getAttr('{}.rotateOrder'.format(obj))
    euler = om2.MEulerRotation(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder)
    quat = euler.asQuaternion()
    euler = quat.asEulerRotation()
    r = euler.reorder(rotOrder)

    cmds.xform(obj, ro=[math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)], os=True, a=True)

    cmds.setKeyframe(obj, at='rotate')

    return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)

@bake_with_func
def correctkeys(objects=None):
    [quaternionToEuler(obj=obj) for obj in objects] if objects else False

def get_top_node(node):
    parent = cmds.listRelatives(node, parent=True)
    while parent:
        node = parent[0]
        parent = cmds.listRelatives(node, parent=True)
    return node

def bake_undo(nodes=None, playmin=None, playmax=None, at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz']):
    cmds.undoInfo(openChunk=True)

    # bake
    bake(nodes, playmin, playmax, at)

    # delete humanik
    cmds.delete('HIK*')

    # set scale
    [cmds.setAttr(n+'.s', *[1,1,1]) for n in nodes]

    # correct rotate
    correctkeys(nodes)

    # clean up
    cmds.delete('Root')
    cmds.namespace(mergeNamespaceWithParent=True, removeNamespace='import')
    mesh_shapes = cmds.ls(type='mesh') or None
    top_node = get_top_node(mesh_shapes[0])
    cmds.delete(top_node)

    cmds.undoInfo(closeChunk=True)

def options_enm_m_ghost01():
    cmds.delete('Thigh_L', 'Thigh_R')

def convert_files(convert_type=None, match_source=False):
    if convert_type == 'p1_p2':
        to_joints_filePath, from_joints_filePath = p2_JOINT_PATH, p1_JOINT_PATH
    elif convert_type == 'p2_p1':
        to_joints_filePath, from_joints_filePath = p1_JOINT_PATH, p2_JOINT_PATH
    elif convert_type == 'p1_enm_m_ghost01':
        to_joints_filePath, from_joints_filePath = enm_m_ghost01_JOINT_PATH, p1_JOINT_PATH
    elif convert_type == 'p2_enm_m_ghost01':
        to_joints_filePath, from_joints_filePath = enm_m_ghost01_JOINT_PATH, p2_JOINT_PATH

    hik_convert.do_convert(to_joints_filePath, from_joints_filePath)
    from_files = find_files(FROM_PATH, '*.fbx', 'old')

    for file in from_files:
        _file = file.replace('\\', '/')

        # import
        playmin, playmax = file_import(_file)

        # Match Source
        if match_source:
            cmds.setAttr('HIKproperties1.ForceActorSpace', True)

        # bake
        nodes = cmds.ls('import:Root', dag=True, type='joint')
        bake_undo(nodes, playmin, playmax, ['tx', 'ty', 'tz', 'rx', 'ry', 'rz'])

        # options
        if 'enm_m_ghost01' in convert_type:
            options_enm_m_ghost01()

        # export
        fbxspl = _file.split('/')
        fname = fbxspl[-1].split('.')[0]

        save_file = '{}/{}.fbx'.format(SAVE_PATH, fname)
        cmds.file(save_file, f=True, options='v=0;', type='FBX export', pr=True, ea=True)

        # bake undo
        cmds.undo()
        cmds.undo()


def hik_convert_p1_p2():
    convert_files('p1_p2')

def hik_convert_p2_p1():
    convert_files('p2_p1')

def hik_convert_p1_enm_m_ghost01():
    convert_files('p1_enm_m_ghost01')

def hik_convert_p2_enm_m_ghost01():
    convert_files('p2_enm_m_ghost01')
