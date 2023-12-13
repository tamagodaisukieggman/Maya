# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds

from ....base_common import utility as base_utility


class ChangePolygonView(object):

    def change_normal(self, arg):

        normal_type = arg[0]

        if normal_type == 'none':

            cmds.polyOptions(dn=False)

        elif normal_type == 'vertex':

            cmds.polyOptions(dn=True, pt=True)

        elif normal_type == 'face':

            cmds.polyOptions(dn=True, f=True)

        elif normal_type == 'sizeup':

            cmds.polyOptions(sn=1.5, r=True)

        elif normal_type == 'sizedown':

            cmds.polyOptions(sn=0.5, r=True)

    def change_edge(self, arg):

        edge_type = arg[0]

        if edge_type == 'none':

            cmds.polyOptions(ae=True)

        elif edge_type == 'soft':

            cmds.polyOptions(se=True)

        elif edge_type == 'hard':

            cmds.polyOptions(he=True)

        elif edge_type == 'border_off':

            cmds.polyOptions(db=False)

        elif edge_type == 'border_on':

            cmds.polyOptions(db=True)

        elif edge_type == 'wire_off':

            cmds.displayPref(wsa='none')

        elif edge_type == 'wire_on':

            cmds.displayPref(wsa='full')

    def change_vertex_color(self, arg):

        type = arg[0]

        select_list = cmds.ls(sl=True, l=True)

        if not select_list:
            return

        if type == 'vertex_color_off':

            for select in select_list:

                shape = base_utility.mesh.get_mesh_shape(select)

                base_utility.attribute.set_value(
                    shape, 'displayColors', 0
                )

        elif type == 'vertex_color_on':

            for select in select_list:

                shape = base_utility.mesh.get_mesh_shape(select)

                base_utility.attribute.set_value(
                    shape, 'displayColors', 1
                )

    def change_display(self, arg):

        current_panel = self.get_active_panel()

        if current_panel is None:
            return

        display_type = arg[0]

        if display_type == 'flat':

            cmds.modelEditor(current_panel, e=True, displayLights='flat')

        elif display_type == 'default':

            cmds.modelEditor(current_panel, e=True, displayLights='default')

        elif display_type == 'texture_on':

            cmds.modelEditor(current_panel, e=True, displayTextures=True)

        elif display_type == 'texture_off':

            cmds.modelEditor(current_panel, e=True, displayTextures=False)

        elif display_type == 'wire_on':

            cmds.modelEditor(current_panel, e=True, wireframeOnShaded=True)

        elif display_type == 'wire_off':

            cmds.modelEditor(current_panel, e=True, wireframeOnShaded=False)

    def get_active_panel(self):

        current_panel = cmds.getPanel(wf=True)

        if current_panel is None:
            return

        panel_type = cmds.getPanel(to=current_panel)

        if panel_type is None:
            return

        if panel_type != 'modelPanel':
            return

        return current_panel
