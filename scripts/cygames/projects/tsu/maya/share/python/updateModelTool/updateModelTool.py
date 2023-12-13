# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : updateModelTool
# Author  : toi
# Version : 0.0.2
# Update  : 2022/10/12
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
import re
import stat
import datetime
import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm

from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import skinning as sk
from dccUserMayaSharePythonLib import tsubasa_dumspl as tsubasa
from dccUserMayaSharePythonLib import file_dumspl as f
from palette import data as palette_data

setting_dict = f.createSettingFile('updateModelTool')
weight_folder = os.path.join(f.getSettingFilePath('updateModelTool'), 'weight')
if not os.path.isdir(weight_folder):
    os.makedirs(weight_folder)

RIG_INFO = 'rig_info'
scp = None


# =============================================================================
# Work Scene
# =============================================================================
# Export Weight ---------------------------------------------------------------
def exportWeight(*args):
    if not cmds.objExists('LOD0'):
        return 1

    cm.selMeshHierarchy('LOD0')
    mesh_nodes = cmds.ls(sl=True)
    global setting_dict
    export_meshes, xml_files = sk.exportWeightMulti(mesh_nodes, weight_folder, True)
    setting_dict.set('export_meshes', export_meshes)
    setting_dict.set('xml_files', xml_files)


def saveSets(*args):
    global scp
    if not cmds.objExists(RIG_INFO):
        _createRigInfoSet()
    scp = cm.SetsCopyPaste(RIG_INFO)
    scp.copy()


def _createRigInfoSet():
    rig_info_dict = palette_data.getRigInformation(
        'D:\\cygames\\tsubasa\\tools\\dcc_user\\maya\\share\\python\\palette\\_json\\_rig_info.json')
    rig_info_set_name = rig_info_dict[0]
    fase_set_name = rig_info_dict[1]
    exp_pose_at_name = rig_info_dict[2]

    # rename old face set
    old_face_set_list = palette_data.getFaceSetList()
    if old_face_set_list:
        pm.rename(old_face_set_list[0], fase_set_name)

    # ---------------------
    if not pm.objExists(rig_info_set_name):
        rig_info_set = pm.sets(em=True, n=rig_info_set_name)
    else:
        rig_info_set = pm.PyNode(rig_info_set_name)

    # ---------------------
    if not pm.objExists(fase_set_name):
        fase_set = pm.sets(em=True, n=fase_set_name)
    else:
        fase_set = pm.PyNode(fase_set_name)

    # ---------------------
    try:
        pm.sets(rig_info_set, e=True, fe=fase_set)
    except:
        pass

    # ---------------------
    if not pm.objExists(rig_info_set + '.' + exp_pose_at_name):
        pm.addAttr(rig_info_set, ln=exp_pose_at_name, dv=0)


# CleanUp ---------------------------------------------------------------------
def cleanUpWorkScene(*args):
    if cmds.objExists('LOD0'):
        cmds.delete('LOD0')
        deleteUnusedMaterial()
    else:
        return 1


def deleteUnusedMaterial():
    log = '------------------- Delete Unused Material -----------------------\n'
    mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    log += 'Delete Unused Nodes    : Done.\n'

    print(log)
    return log


# Save Count Up ----------------------------------------------------------------
def saveCountUp(*args):
    log = '------------------- Save Count Up -----------------------\n'
    scene_path = args[0]
    if os.path.isfile(scene_path):
        os.chmod(scene_path, stat.S_IWRITE)

    cmds.file(rename=scene_path)
    cmds.file(s=True, f=True)
    log += 'Save Count Up    : Done.\n'

    print(log)
    return scene_path


def getDate():
    return str(datetime.date.today()).replace('-', '')


def getVersionUpSceneName(scene_file_path):
    scene_dir = os.path.dirname(scene_file_path)

    split_file = os.path.basename(scene_file_path).split('_')
    if re.match('\w\d\d\d', split_file[1]):
        version = str(int(split_file[1][1:]) + 1).zfill(3)
    else:
        version = '000'

    new_scene_file_name = split_file[0] + '_v' + version + '_' + getDate() + '.mb'
    new_scene_file_path = os.path.join(scene_dir, new_scene_file_name)
    return new_scene_file_path


# =============================================================================
# New Model Scene
# =============================================================================
# Clean up New Model Scene ----------------------------------------------------
def handler(func, *args):
    return func(*args)


def cleanUpAll(*args):

    func_list = [
        setDefaultUnitEnv,
        deleteAnimKey,
        cleanSkin,
        deleteSkeleton,
        resetMeshDispaly,
        freezeObj,
        # checkUnnecessaryMesh,
        # checkSameNameNode,
        LclDirectory,
        deleteOtherNode
    ]

    for func in func_list:
        try:
            handler(func)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('------------------- {} ---------------------------'.format(func.__name__))
            print('* Error', e)
            print('{}, {}, {}'.format(exc_type, fname, exc_tb.tb_lineno))
            print('')


# -----------------------------------------------------------------------------
def ishex(v):
    try:
        int(v, 16)
        return True
    except ValueError:
        return False


def getIDFromRoot():
    ID = ''
    for i in cmds.ls(typ='transform'):
        if not cm.getParent(i) and len(i) == 6:
            if i[:2].isalpha() and ishex(i[-4:]):
                ID = i
    if ID:
        return ID
    else:
        return None


def setGrid(s=200, sp=50, d=5):
    cmds.grid(s=s, sp=sp, d=d)
    log = 'set grid               : size={0}, spacing={1}, division={2}\n'.format(s, sp, d)
    print(log)
    return log


def setCam(fl=50):
    cmds.setAttr('perspShape.focalLength', fl)
    log = 'set camera             : focalLength={0}\n'.format(fl)
    print(log)
    return log


def setJointSize(s=1.0):
    cmds.jointDisplayScale(s)
    log = 'set joint display size : {0}\n'.format(s)
    print(log)
    return log


def setSmoothWireframe(v=8):
    cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
    cmds.setAttr('hardwareRenderingGlobals.multiSampleCount', v)
    log = 'set anti-aliasing      : ON | count={0}\n'.format(v)
    print(log)
    return log


def setTimeRange(s=0, e=10):
    cmds.playbackOptions(min=s, max=e, ast=s, aet=e, e=True)
    cmds.currentTime(s)
    log = 'set time range         : start={0}, end={1}\n'.format(s, e)
    print(log)
    return log


def setSceneUnit(l='cm', a='deg', t='60fps'):
    cmds.currentUnit(l=l, a=a, t=t)
    log = 'set scene unit         : lniear={0}, angular={1}, time={2}\n'.format(l, a, t)
    print(log)
    return log


def checkLoadPlugin(plugin=''):
    if not cmds.pluginInfo(plugin, l=True, q=True):
        cmds.loadPlugin(plugin)
        print('Plug-in, "{0}", was loaded successfully.'.format(plugin))
    else:
        print('Plug-in, "{0}", is already loaded. <Skipped>'.format(plugin))


def setDefaultUnitEnv():
    print('------------------- Set Unit Log ---------------------------------\n')
    setGrid(200.0, 50.0, 5)
    setCam(50)
    setJointSize(1.0)
    setSmoothWireframe(8)
    setSceneUnit('cm', 'deg', '60fps')
    setTimeRange(0, 10)

    pList = ['matrixNodes', 'mayaHIK', 'mayaCharacterization', 'OneClick']
    for i in pList:
        checkLoadPlugin(i)


def deleteAnimKey():
    log = '------------------- Delete Animation Key -------------------------\n'
    animList = cmds.ls(typ=[i for i in cmds.listNodeTypes('animation') if 'animCurve' in i])
    cmds.delete(animList)
    if animList:
        for i in animList:
            log += 'delete animation key : {0} \n'.format(i)
    else:
        log += 'delete animation key   : No Animation Key in the scene. \n'
    print(log)
    return log


def cleanSkin():
    log = '------------------- Delete Skin Cluster --------------------------\n'
    skList = cmds.ls(typ='skinCluster')
    for i in skList:
        cmds.setAttr('{}.envelope'.format(i), 0)

    cleanMesh()
    log += 'Unbind Mesh     : Done.\n'

    # -- delete bindpose
    cmds.delete(cmds.ls(typ='dagPose'))
    log += 'Delete Bind Pose       : Done.\n'

    # -- deselect
    cmds.select(d=True)
    print(log)
    return log


def cleanMesh():
    log = '------------------- Clean Mesh --------------------------\n'
    for i in cmds.ls(sl=True, typ='transform'):
        skinCls = mm.eval('findRelatedSkinCluster {};'.format(i))
        if skinCls:
            cmds.skinCluster(i, ub=True, e=True)
            mm.eval('DeleteHistory;')
        cmds.move(0, 0, 0, '{}.sp'.format(i), '{}.rp'.format(i), rpr=True)

        # pm.mel.eval('ResetDisplay;')
        cmds.setAttr('{}.useObjectColor'.format(i), 0)

        # -- unlock
        cm.lockAt(i, ['t', 'r', 's', 'tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'], False)


def deleteSkeleton():
    log = '------------------- Delete Skaleton ------------------------------\n'
    if cmds.objExists('null'):
        cmds.delete('null')
    log += 'Reset Skeleton         : Done. \n'
    print(log)
    return log


def resetMeshDispaly():
    log = '------------------- Reset Mesh Dispaly ---------------------------\n'
    id_ = getIDFromRoot()
    if cmds.objExists(id_):
        cmds.select(id_, r=True)
        mm.eval('ResetDisplay;')
    log += 'Reset Mesh Dispaly     : Done. \n'
    print(log)
    return log


def freezeMesh():
    objList = cmds.ls(sl=True)
    cmds.makeIdentity(a=True, t=True, r=True, s=True, n=0, pn=True)
    cmds.lattice(dv=(2, 2, 2), oc=True, ldv=(2, 2, 2))
    cmds.select(objList, r=True)
    mm.eval('DeleteHistory;')


def freezeObj():
    log = '------------------- Freeze Mesh ----------------------------------\n'
    if cmds.objExists('LOD0'):
        lMesh = list(set([cm.getParent(i) for i in cmds.ls('LOD0', dag=True, typ='mesh')]))
        cmds.select(lMesh, r=True)
        freezeMesh()
        log += 'LOD0 | Freeze Mesh     : Done.\n'
    if cmds.objExists('COL'):
        cMesh = list(set([cm.getParent(i) for i in cmds.ls('COL', dag=True, typ='mesh')]))
        cmds.select(cMesh, r=True)
        freezeMesh()
        log += 'COL | Freeze Mesh      : Done.\n'
    print(log)
    return log


def checkUnnecessaryMesh():
    log = '------------------- Unnecessary Shape Check ----------------------\n'
    tgtMesh = []
    if cmds.objExists('LOD0'):
        lMesh = list(set([cm.getParent(i) for i in cmds.ls('LOD0', dag=True, typ='mesh')]))
        if lMesh:
            tgtMesh = [i for i in lMesh if len(cmds.listRelatives(i, c=True, typ='mesh')) > 1]

    if tgtMesh:
        if cmds.objExists('LOD0_unnecessary_shape_set'):
            cmds.delete('LOD0_unnecessary_shape_set')
        cmds.select(tgtMesh, r=True)
        cmds.sets(n='LOD0_unnecessary_shape_set')
        log += 'LOD0 | Shape Check     : LOD0_unnecessary_shape_set.\n'

    tgtMesh = []
    if cmds.objExists('COL'):
        cMesh = list(set([cm.getParent(i) for i in cmds.ls('COL', dag=True, typ='mesh')]))
        if cMesh:
            tgtMesh = [i for i in cMesh if len(cmds.listRelatives(i, c=True, typ='mesh')) > 1]

    if cmds.objExists('COL_unnecessary_shape_set'):
        cmds.delete('COL_unnecessary_shape_set')

    if tgtMesh:
        cmds.select(tgtMesh, r=True)
        cmds.sets(n='COL_unnecessary_shape_set')
        log += 'COL | Shape Check      : COL_unnecessary_shape_set.\n'
    else:
        log += 'Shape Check            : Done.\n'

    print(log)
    return log


def checkSameNameNode():
    log = '------------------- Overlapping Name Check -----------------------\n'
    nodeList = []
    pathList = []

    # -- check scene
    for obj in cmds.ls():
        if '|' in obj:
            nodeList.append(obj.split('|')[-1])
            pathList.append(obj)

    if cmds.objExists('sameName_set'):
        cmds.delete('sameName_set')

    if not len(nodeList) == 0:
        # -- print node names
        for i in range(len(nodeList)):
            log += '{0} : {1} \n'.format(nodeList[i], pathList[i])
        # -- create set
        cmds.sets(pathList, n='sameName_set')

    else:
        log += 'Check node name        : doesn\'t exist in the scene.\n'

    print(log)
    return log


def LclDirectory():
    assetID = getIDFromRoot()
    if assetID:
        astType = assetID[:2]
        lcPath  = r'{0}scenes/{1}/{2}'.format(cmds.workspace(q=True, rd=True), astType, assetID)
    else:
        lcPath  = r'{0}scenes'.format(cmds.workspace(q=True, rd=True))
    return lcPath


def deleteOtherNode():
    log = '------------------- Delete Other Node -----------------------\n'
    del_node_list = [
        'rig_GP',
        'ShaderLightLink',
        'UM',
        'face_reference',
        'workbench',
        'rig_info',
        '_default_character'
    ]

    for d in del_node_list:
        if cmds.objExists(d):
            cmds.delete(d)
            log += d + '\n'
    log += 'Delete Other Node     : Done.\n'
    print(log)
    return log


# Import Work Scene ----------------------------------------------------
def importWorkScene(vup_scene_path):
    ns = 'xxxx:'
    id_ = tsubasa.getId(vup_scene_path)

    if os.path.isfile(vup_scene_path):
        cmds.file(vup_scene_path, i=True, f=True, ns=ns[:-1])

        null_ = ns + 'null'
        if cmds.objExists(null_):
            cmds.parent(null_, id_)

        rig_gp = ns + 'rig_GP'
        if cmds.objExists(rig_gp):
            cmds.parent(rig_gp, id_)

        top = ns + id_
        if cmds.objExists(top):
            cmds.delete(top)

        cmds.namespace(rm=ns[:-1], mergeNamespaceWithRoot=True)


def loadSets(*args):
    if scp is not None:
        scp.paste()


def importWeight(*args):
    import_mode = int(args[0])
    global setting_dict
    export_meshes = setting_dict.get('export_meshes')
    xml_files = setting_dict.get('xml_files')
    joints = sk.importWeightMulti(export_meshes, weight_folder, xml_files, import_mode)

    cmds.select(cl=True)
    for export_mesh in export_meshes:
        if cmds.objExists(export_mesh):
            cmds.select(export_mesh, add=True)
    if joints is not None:
        cmds.select(joints, add=True)


