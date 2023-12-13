# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds


def _check_all_transform_key(node):

    errors = []

    _all_transform = cmds.ls(type="transform", long=True)

    for _transform in _all_transform:
        if cmds.keyframe(_transform, q=True):
            errors.append(_transform)

    return errors