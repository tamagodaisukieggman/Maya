# coding=utf-8
import os
import sys
import timeit

import cyllista.config_node
import cyllistaClipConfig
import maya.cmds as mc
import maya.mel as mm

rigDir = "z:/mtk/tools/maya/modules/mtku/scripts"
if not rigDir in sys.path:
    sys.path.append(rigDir)

rigDir = "Z:/mtk/tools/techart/python/python27-64/modules"
if not rigDir in sys.path:
    sys.path.append(rigDir)

import mtku.maya.menus.animation.bakesimulation as bakesimulation

if not mc.pluginInfo('mayaHIK', q=True, l=True):
    mc.loadPlugin("mayaHIK")
if not mc.pluginInfo('mayaCharacterization', q=True, l=True):
    mc.loadPlugin("mayaCharacterization")
if not mc.pluginInfo('OneClick', q=True, l=True):
    mc.loadPlugin("OneClick")
if not mc.pluginInfo('fbxmaya', q=True, l=True):
    mc.loadPlugin("fbxmaya")


def main(filePath, savePath, convertScene, nameSpace):
    dirPath = os.path.isdir(filePath)
    file_list = []
    if dirPath:
        fileNames = os.listdir(filePath)
        for fileName in fileNames:
            fl = os.path.join(filePath, fileName).replace('\\', '/')
            if os.path.isfile(fl):
                file_list.append(fl)

    else:
        file_list = filePath.split(' ')

    clock = timeit.default_timer
    start = clock()
    for files in file_list:
        # get cyllista config nodes
        (exp_config, clip_config) = _get_cyllista_nodes(files, savePath)

        # Open convert scene
        _file_open(convertScene)

        # Import animation FBX
        file_contents = _import_fbx(files)

        # set time range
        # _set_timerange(files)

        # strip namespace
        try:
            jnt_name, del_node = strip_namespace(file_contents)
            fp = _export_fbx(files, filePath)
            mc.delete(del_node)
            _import_fbx(fp)

            # delete temp file
            os.remove(fp)

        except:
            pass

        # get joint　ジョイントを取得
        jnt = get_joint()

        # set euler filter
        set_euler_filter(jnt)

        # get control set
        ctrlSet = get_control_set_name(nameSpace)

        # check convert scene file
        path, ext = os.path.splitext(os.path.basename(convertScene))
        sceneType = path.split("_")
        if sceneType[-1] == "bossBattle":
            bossBattleAsset(nameSpace)

        # Bake animation
        # _bake_animations(ctrlSet)

        # set euler filter for controller
        # set_euler_filter(ctrlSet)

        # get controller
        # sel = mc.ls(ctrlSet)
        mc.select(ctrlSet)

        # bakesimulation
        bakesimulation.main()

        # Select other than reference and delete
        mc.select(ado=True)
        mc.delete()

        # add cyllista config nodes to the new scene
        # _add_cyllista_nodes(exp_config, clip_config)

        # create cyllista node
        _create_cyllista_node()

        # set choice on
        cn = check_choise()
        if cn == "True":
            choice_on()

        # Save the scene as ma data and close
        _file_close(files, savePath)

    elapsed = clock() - start
    print("%.3f s" % (elapsed,))


def _file_open(*args):
    mc.file(args[0], f=1, o=1)


def _import_fbx(*args):
    file = mc.file(args[0], i=True, importFrameRate=True, importTimeRange="override", rnn=True)
    return file


def _export_fbx(files, save_path):
    path = os.path.split(files)
    ext = os.path.splitext(path[1])
    file_path = path[0] + "temp" + ".fbx"
    mm.eval('FBXExport -f "{}" -s '.format(file_path))
    return file_path


def strip_namespace(*args):
    sel = mc.ls(args[0], type="joint")
    # parentNode = mc.listRelatives(sel, p=True)
    parentNode = checkTopNode(sel[0])

    del_node = mc.createNode("transform")
    mc.parent(parentNode[0], del_node)
    nmsp = parentNode[0].split(":")
    mc.select(parentNode[0])
    mc.namespace(mergeNamespaceWithParent=True, removeNamespace=nmsp[0])
    return nmsp[1], del_node


def checkTopNode(name):
    parentNode = mc.listRelatives(name, p=True)
    if parentNode != None:
        return checkTopNode(parentNode[0])
    else:
        return name


def _set_timerange(*args):
    path = args[0]

    mm.eval('FBXRead -f "' + path + '";')
    result = mm.eval("FBXGetTakeLocalTimeSpan 1;")
    mm.eval("FBXClose;")
    mc.playbackOptions(e=True, min=result[0])
    mc.playbackOptions(e=True, max=result[1])


def get_joint(*args):
    jnts = []
    if mc.objExists("root_jnt"):
        sel = mc.select(mc.ls("root_jnt", dagObjects=True, type='joint'))
        oSel = mc.ls(sl=True)
        jnts.extend(oSel)
    else:
        print("root_jnt does not exist.")

    return jnts


def set_euler_filter(*args):
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz"]
    for jnt in args[0]:
        for attr in attrs:
            try:
                mc.filterCurve(jnt + "." + attr)
            except:
                print(attr)


def _bake_animations(ctrlSet=None):
    clock = timeit.default_timer
    start = clock()
    mc.refresh(su=True)
    sf = mc.playbackOptions(q=True, min=True)
    ef = mc.playbackOptions(q=True, max=True)

    mc.bakeResults(mc.sets(ctrlSet, q=True), t=(sf, ef), sm=True)
    mc.refresh(su=False)
    elapsed = clock() - start
    print("%.3f s" % (elapsed,))


def _get_cyllista_nodes(file_path, save_dir):
    """
    get cyllista nodes
    now it gets cyllista_config and cyllistaClipConfig
    """
    savePath = _create_savePath(file_path, save_dir)
    print("File path received by get cyllista =", savePath)
    if not os.path.exists(savePath):
        return (None, None)
    _file_open(savePath)

    exp_config = None
    clip_config = None

    exp_configs = cyllista.config_node.find_config_node()
    if exp_configs:
        exp_config = cyllista.config_node.get_config()
    clip_configs = cyllistaClipConfig.findConfigNode()
    if clip_configs:
        clip_config = cyllistaClipConfig.getRootAttr()["clips"]

    print("exp_config=", exp_config)
    print("clip_congig = ", clip_config)
    return (exp_config, clip_config)


def _add_cyllista_nodes(exp_config, clip_config):
    """
    add cyllista nodes
    now it adds cyllista_config and cyllistaClipConfig
    """
    if exp_config:
        exp_node = cyllista.config_node.find_or_create_config_node()
        mc.select(exp_node)
        cyllista.config_node.update_config(exp_config)
        if clip_config:
            clip_node = cyllistaClipConfig.setUpClipConfigNode()
            keys = cyllistaClipConfig.getClipNames()
            for k in keys:
                cyllistaClipConfig.removeClipAttrs(k)
            mc.select(clip_node, add=True)
            for k, v in clip_config.items():
                cyllistaClipConfig.updateClipAttrs(v, k)


def _create_cyllista_node():
    """
    create cyllista node (config_node)
    """
    exp_node = cyllista.config_node.find_or_create_config_node()
    mc.select(exp_node)
    mc.setAttr('cyllista_config.cyExportGfx', False)
    mc.setAttr('cyllista_config.cyExportPhy', False)
    mc.setAttr('cyllista_config.cyExportAnm', True)
    mc.setAttr('cyllista_config.cyExportAnmSkl', False)


def _create_savePath(file_path, save_dir):
    path = os.path.split(file_path)
    ext = os.path.splitext(path[1])

    return save_dir + ext[0] + ".ma"


def _file_close(files, savePath):
    path = os.path.split(files)
    ext = os.path.splitext(path[1])

    mc.file(rename=savePath + ext[0] + ".ma")
    mc.file(f=True, typ='mayaAscii', op='v=0', s=True)
    mc.file(f=True, new=True)


def get_control_set_name(nameSpace):
    ctrlSet = ""
    if mc.objExists("{}:ctrlSet".format(nameSpace)):
        ctrlSet = "{}:ctrlSet".format(nameSpace)

    if mc.objExists("{}:CtrlSet".format(nameSpace)):
        ctrlSet = "{}:CtrlSet".format(nameSpace)

    return ctrlSet


def check_choise():
    cho = mc.ls('*_cho', r=1)
    if not cho == []:
        return "True"
    else:
        return "False"


def choice_on():
    cho = mc.ls('*_cho', r=1)
    mc.select(cho)
    for c in cho:
        mc.setAttr(c + ".selector", 1)


def bossBattleAsset(nameSpace):
    nameSpace = nameSpace
    root = "root"
    rootDummy = "root_dummy "
    zero = (0, 0, 0)
    mainCtrl = "{}:main_ctrl".format(nameSpace)

    rootOff = (mc.createNode("transform", n="root_offset"))
    mc.delete(mc.parentConstraint(root, rootOff))
    if mc.objExists("root_dummy"):
        mc.parent(rootOff, rootDummy)
    mc.parent(root, rootOff)

    mc.setAttr(rootOff + ".translate", *zero)

    dumLoc = mc.spaceLocator(n="dum_loc")
    dumLocOff = mc.spaceLocator(n="dum_loc_offset")

    mc.parentConstraint(root, dumLocOff)
    mc.delete(mc.parentConstraint(root, dumLoc))

    mc.parentConstraint(dumLoc, mainCtrl, mo=True)
    mc.parent(dumLoc, dumLocOff)
    mc.setAttr(dumLoc[0] + ".rotate", *zero)
