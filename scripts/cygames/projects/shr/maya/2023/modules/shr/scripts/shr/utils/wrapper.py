import os

from maya import cmds


def getCurrentSceneFilePath(normalized=False):
    """
    cmds.file(q=path, sn=True) に準拠。
    新しいシーンの場合は None を返す。
    """

    if 0:
        # 2021/12/23: Maya 2022 は適切な値を返さない不具合あり。
        path = cmds.file(q=True, sn=True)  # FIXME
    else:
        import maya.OpenMaya as om
        path = om.MFileIO.currentFile()
        # 新規の場合は ".../untitled" が帰ってくるので拡張子が無ければ新規とみなす。
        if not os.path.splitext(path)[1]:
            path = None

    if path and normalized:
        path = os.path.normpath(path)
    return path


def getCurrentSceneName(normalized=False):
    file_path = getCurrentSceneFilePath(normalized)
    if file_path:
        return os.path.basename(file_path)
    else:
        return None
