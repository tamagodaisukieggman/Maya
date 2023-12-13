# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds


def _check_plugins():

    errors = []
    plugings = cmds.unknownPlugin( query=True, list=True )
    
    if plugings:
        errors = plugings
        for p in plugings:
            cmds.unknownPlugin(p, remove=True)

    return errors