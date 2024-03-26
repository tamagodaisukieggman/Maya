# -*- coding: utf-8 -*-
from imp import reload

import maya.cmds as cmds
import maya.mel as mel

import rig.convert.hik.hik_convert as hik_convert
reload(hik_convert)

def fileDialog_import(cap='File'):
    filename = cmds.fileDialog2(ds=2, cap=cap, okc='Done', ff='All Files (*.*)', fm=1)
    if filename is None:
        return
    return filename[0]

def do_convert(to_joints_filePath=None, from_joints_filePath=None):
    """
    to_joints_filePath: 新しいジョイント
    from_joints_filePath: 古いジョイント
    """

    if not to_joints_filePath:
        # Affect on Joints
        to_joints_filePath = fileDialog_import(u'Select Import Joints')
    if to_joints_filePath.endswith('ma'):
        to_xml_filePath = to_joints_filePath.replace('.ma', '.xml')
    elif to_joints_filePath.endswith('mb'):
        to_xml_filePath = to_joints_filePath.replace('.mb', '.xml')

    if not from_joints_filePath:
        # Animation Joints
        from_joints_filePath = fileDialog_import(u'Select Mocap Joints')
    if from_joints_filePath.endswith('ma'):
        from_xml_filePath = from_joints_filePath.replace('.ma', '.xml')
    elif from_joints_filePath.endswith('mb'):
        from_xml_filePath = from_joints_filePath.replace('.mb', '.xml')

    hik_convert.convert(
        to_joints_filePath, to_xml_filePath,
        from_joints_filePath, from_xml_filePath
    )
