# -*- coding: utf-8 -*-
import os
import sys
import timeit
import logging

import maya.cmds as mc

rigDir = "Z:/mtk/tools/techart/python/python37-64/modules"
if not rigDir in sys.path:
    sys.path.append(rigDir)

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


def main(file_path, save_path, new_scene, name_space):
    file_list = _create_files_list(file_path)
    _run_replace_path(file_list, name_space, new_scene, save_path)


def timer(func):
    def wrapper(*args, **kwargs):
        clock = timeit.default_timer
        start = clock()
        try:
            ret = func(*args, **kwargs)
        finally:
            elapsed = clock() - start
            print("%.3f s" % (elapsed,))
        return ret

    return wrapper


@timer
def _run_replace_path(file_list, name_space, new_scene, save_path):
    for files in file_list:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("./replacereference.log")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s %(asctime)s [%(name)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error("エラーファイル: {}".format(files))

        _file_open(files)

        reference_status = _item_reference_check(name_space)

        # replace reference
        _replace_reference(name_space, new_scene)

        _set_reference_status(name_space, reference_status)

        # Save the scene as ma data and close
        _file_close(files, save_path)


def _item_reference_check(*args):
    items = ["rig_prp_bow00_000", "rig_prp_arw00_000", "rig_prp_osw00_000", "rig_prp_sld00_000", "rig_prp_spr00_000",
             "rig_prp_gsw00_000", "rig_prp_itm00_043", "rig_prp_knf00_000"]
    exists = []
    for itm in items:
        try:
            ref_name = mc.referenceQuery("{}:{}RN".format(args[0], itm), rfn=True)
            if not mc.file(rfn=ref_name, q=True, dr=True):
                exists.append(itm)
            else:
                pass
        except:
            print("対象のアイテムがリファレンスされていません")
    return exists


def _set_reference_status(nmsp, items):
    for itm in items:
        try:
            mc.file(rfn="{}:{}RN".format(nmsp, itm), lr=True)
        except:
            pass


def _create_files_list(file_path):
    dir_path = os.path.isdir(file_path)
    files = []
    if dir_path:
        file_names = os.listdir(file_path)
        for fileName in file_names:
            fl = os.path.join(file_path, fileName).replace('\\', '/')
            if os.path.isfile(fl):
                root, ext = os.path.splitext(fl)
                if ext == ".ma":
                    files.append(fl)

    else:
        if os.path.isfile(file_path):
            root, ext = os.path.splitext(file_path)
            if ext == ".ma":
                files = file_path.split(' ')

    return files


def _file_open(*args):
    mc.file(args[0], f=1, o=1)


def _replace_reference(*args):
    mc.file(args[1], loadReference="{}RN".format(args[0]))


def _create_save_path(file_path, save_dir):
    path = os.path.split(file_path)
    ext = os.path.splitext(path[1])

    return save_dir + ext[0] + ".ma"


def _file_close(files, save_path):
    path = os.path.split(files)
    ext = os.path.splitext(path[1])

    mc.file(rename=save_path + ext[0] + ".ma")
    mc.file(f=True, typ='mayaAscii', op='v=0', s=True)
    mc.file(f=True, new=True)
