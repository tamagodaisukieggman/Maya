import os
import timeit

import maya.cmds as mc
import maya.mel as mm
import pymel.core as pm

if not mc.pluginInfo('fbxmaya', q=True, l=True):
    mc.loadPlugin("fbxmaya")

# eST3
try:
    if not mc.pluginInfo('eST3cmds', q=True, l=True):
        mc.loadPlugin("eST3cmds")
    if not mc.pluginInfo('eST3constraints', q=True, l=True):
        mc.loadPlugin("eST3constraints")
    if not mc.pluginInfo('eST3controllers', q=True, l=True):
        mc.loadPlugin("eST3controllers")
    if not mc.pluginInfo('eST3expressionRuntime', q=True, l=True):
        mc.loadPlugin("eST3expressionRuntime")
    if not mc.pluginInfo('eST3falloffDeformer', q=True, l=True):
        mc.loadPlugin("eST3falloffDeformer")
    if not mc.pluginInfo('eST3locators', q=True, l=True):
        mc.loadPlugin("eST3locators")
    if not mc.pluginInfo('eST3magnetDeformer', q=True, l=True):
        mc.loadPlugin("eST3magnetDeformer")
    if not mc.pluginInfo('eST3meshDeformer', q=True, l=True):
        mc.loadPlugin("eST3meshDeformer")
    if not mc.pluginInfo('eST3nodes', q=True, l=True):
        mc.loadPlugin("eST3nodes")
    if not mc.pluginInfo('eST3polyUVCluster', q=True, l=True):
        mc.loadPlugin("eST3polyUVCluster")
    if not mc.pluginInfo('eST3pose', q=True, l=True):
        mc.loadPlugin("eST3pose")
    if not mc.pluginInfo('eST3preview', q=True, l=True):
        mc.loadPlugin("eST3preview")
    if not mc.pluginInfo('eST3rigConnector', q=True, l=True):
        mc.loadPlugin("eST3rigConnector")
    if not mc.pluginInfo('eST3sculptDeformer', q=True, l=True):
        mc.loadPlugin("eST3sculptDeformer")
    if not mc.pluginInfo('eST3softModDeformer', q=True, l=True):
        mc.loadPlugin("eST3softModDeformer")
    if not mc.pluginInfo('eST3surfaceCluster', q=True, l=True):
        mc.loadPlugin("eST3surfaceCluster")
    if not mc.pluginInfo('eST3wheelUnitUtility', q=True, l=True):
        mc.loadPlugin("eST3wheelUnitUtility")
except:
    pass


def main(file_path, save_path, namespace):
    dir_path = os.path.isdir(file_path)
    list_files = []
    if dir_path:
        file_names = os.listdir(file_path)
        for file_name in file_names:
            fl = os.path.join(file_path, file_name).replace('\\', '/')
            if os.path.isfile(fl):
                list_files.append(fl)

    else:
        list_files = file_path.split(' ')

    for files in list_files:
        # Open convert scene
        _file_open(files)

        # import reference
        _import_reference()

        # get joint set
        jt_set_name = _get_jt_set_name(ns=namespace)

        # Bake animation
        _bake_animations(jt_set_name)

        # rename
        check_for_the_name_root_and_rename_it()

        # Remove the specified namespace
        _remove_specified_namespace(ns=namespace)

        # remove namespace
        # _remove_namespace()

        # get joint
        jnt = get_joint()

        # set euler filter
        set_euler_filter(jnt)

        # change top root name
        _change_transform_root_name()

        # get root joint name
        root_jnt = _get_root_joint_name()

        # set time range
        _set_timerange()

        # select obj
        sel = mc.ls(root_jnt)
        mc.select(sel)

        # export fbx
        _export_fbx(files, save_path)

        # Save the scene as ma data and close
        _file_close()


def _file_open(*args):
    mc.file(args[0], f=1, o=1)


def _file_close():
    mc.file(f=True, new=True)


def _set_timerange():
    start_frame = mc.playbackOptions(q=True, minTime=True)
    end_frame = mc.playbackOptions(q=True, maxTime=True)
    mc.rangeControl(minRange=start_frame, maxRange=end_frame)


def _get_jt_set_name(ns=""):
    global jt_set_name
    if mc.objExists("{}:animJtSet".format(ns)):
        jt_set_name = "{}:animJtSet".format(ns)
    elif mc.objExists("{}:AnimJtSet".format(ns)):
        jt_set_name = "{}:AnimJtSet".format(ns)
    else:
        print("There is no set for joint")

    return jt_set_name


def _select_obj(*args):
    jt_set_name = args[0]
    mc.select(mc.sets(jt_set_name, q=True))
    sel = mc.ls(sl=True, type="joint")
    mc.select(sel)


def check_for_the_name_root_and_rename_it():
    sel = pm.ls("root")
    num = len(sel)
    for i in range(num):
        pm.rename(sel[i], "{}_{}".format(sel[i], i))


def _remove_namespace():
    while True:
        all_namespace = mc.namespaceInfo(listOnlyNamespaces=True)
        li_uniq = list(set(all_namespace))
        nums = len(li_uniq)
        if nums == 2:
            break
        else:
            for i in range(nums):
                if li_uniq[i] != "UI" and li_uniq[i] != "shared":
                    mc.namespace(mergeNamespaceWithParent=True, removeNamespace=li_uniq[i])


def _remove_specified_namespace(ns):
    mc.namespace(mergeNamespaceWithParent=True, removeNamespace=ns)


def _import_reference():
    while True:
        refs = [f for f in mc.file(q=1, r=1) if mc.referenceQuery(f, il=1) == True]
        nums = len(refs)
        if nums == 0:
            break
        else:
            for i in range(nums):
                mc.file(refs[i], ir=1)


def _get_root_joint_name():
    global root_jnt
    if mc.objExists("root"):
        sel = pm.ls("root", type="joint")
        pm.select(sel)
        root_jnt = pm.selected()

    if mc.objExists("root_jnt"):
        root_jnt = "root_jnt"

    if mc.objExists("jnt_0000_skl_root"):
        root_jnt = "jnt_0000_skl_root"

    return root_jnt


def _change_transform_root_name():
    sel = pm.ls("root")
    num = len(sel)
    try:
        for i in range(num):
            if sel[i].type() == "joint":
                pass
            else:
                mc.rename("|root", "root_")
    except:
        pass


def _export_fbx(files, save_path):
    path = os.path.split(files)
    ext = os.path.splitext(path[1])
    file_path = save_path + ext[0] + ".fbx"
    mm.eval('FBXExport -f "{}" -s '.format(file_path))


def _bake_animations(*args):
    anim_jt_set = args[0]
    clock = timeit.default_timer
    start = clock()
    mc.refresh(su=True)
    sf = mc.playbackOptions(q=True, min=True)
    ef = mc.playbackOptions(q=True, max=True)
    mc.bakeResults(mc.sets(anim_jt_set, q=True), t=(sf, ef), sm=True)
    mc.refresh(su=False)
    elapsed = clock() - start
    print("%.3f s" % (elapsed,))


def get_joint(*args):
    jnts = []
    if mc.objExists("root_jnt"):
        sel = mc.select(mc.ls("root_jnt", dagObjects=True, type='joint'))
        oSel = mc.ls(sl=True)
        jnts.extend(oSel)

    elif mc.objExists("jnt_0000_skl_root"):
        sel = mc.select(mc.ls("jnt_0000_skl_root", dagObjects=True, type='joint'))
        oSel = mc.ls(sl=True)
        jnts.extend(oSel)

    else:
        print("root_jnt does not exist.")

    return jnts


def set_euler_filter(*args):
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz"]
    for jnt in args[0]:
        for attr in attrs:
            mc.filterCurve(jnt + "." + attr)
