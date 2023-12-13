import os
import timeit

import maya.cmds as mc
import maya.mel as mm


def main(filePath, savePath, nameSpace):
    # -----------------------------------------------------------------------------------------------------------------#
    # check file path type

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

    # -----------------------------------------------------------------------------------------------------------------#
    clock = timeit.default_timer
    start = clock()
    for files in file_list:
        # Open convert scene
        _file_open(files)

        # replace reference
        _replaceReference(nameSpace)

        # save file
        _file_close(files, savePath)

    elapsed = clock() - start
    print("%.3f s" % (elapsed,))


def _file_open(*args):
    mc.file(args[0], f=1, o=1)


def _replaceReference(nameSpace):
    ns = nameSpace.split("_")
    mdl_RN = "{}:mdl_{}_{}RN".format(nameSpace, ns[0], ns[1])
    rig_RN = "{}:rig_{}_{}RN".format(nameSpace, ns[0], ns[1])
    anm_RN = "{}RN".format(nameSpace)

    mdl_path = mc.referenceQuery(mdl_RN, filename=True)
    rig_path = mc.referenceQuery(rig_RN, filename=True)
    anim_rig_path = mc.referenceQuery(rig_RN, filename=True, parent=True)

    wb = "/workbench/maya/rigVersion"
    anim_rig_wb = "/workscenes/workbench/rigVersion"

    wb_path = rig_path.replace("/" + ns[1], "/" + ns[1] + wb)
    anim_rig_wb_path = anim_rig_path.replace("/workscenes", anim_rig_wb)

    mm.eval('file -loadReference "{}" -type "mayaAscii" -options "v=0;" "{}";'.format(anm_RN, anim_rig_wb_path))
    mm.eval('file -unloadReference "{}" "{}";'.format(mdl_RN, mdl_path))
    mm.eval('file -loadReference "{}" -type "mayaAscii" -options "v=0;" "{}";'.format(rig_RN, wb_path))

    return wb_path


def _create_savePath(file_path, save_dir):
    path = os.path.split(file_path)
    ext = os.path.splitext(path[1])

    return save_dir + ext[0] + ".ma"


def _file_close(files, savePath):
    path = os.path.split(files)
    ext = os.path.splitext(path[1])

    mc.file(rename=savePath + ext[0] + ".ma")
    mc.file(f=True, typ='mayaAscii', op='v', s=True)
    mc.file(f=True, new=True)
