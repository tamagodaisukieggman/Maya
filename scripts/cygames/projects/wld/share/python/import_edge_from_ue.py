import json

import pyperclip

import pymel.core as pm

from maya import cmds

from utiltools.custom_locator_manager import command as clm_cmd



lctpath = 'P:/production/share/custom_locators/edgebox.mb'





def load_plugin():

    if not cmds.pluginInfo('curveLocator', q=True, l=True):

        try:

            cmds.loadPlugin('curveLocator')

        except:

            print('Could not loat the plugin')

            return





def delete_curve_locator():

    nodes = pm.ls()

    for node in nodes: 

        if type(node) is pm.nodetypes.Transform:     

            shape = node.getShapes()

            if shape and type(shape[0]) is pm.nodetypes.CurveLocator:

                pm.delete(node)





def create_edge_locator(json_data):

    for edge in json_data['Edges']:

        shape_node = clm_cmd.create_locator(lctpath)

        transform_node = pm.listRelatives( shape_node, allParents=True )[0]

        pos = pm.datatypes.Vector(edge['tx'], edge['ty'], edge['tz'])

        quat = pm.datatypes.Quaternion(edge['w0'], edge['w1'], edge['w2'], edge['w3'])

        scale = pm.datatypes.Vector(edge['sx'], edge['sy'], edge['sz'])

        transform_node.setTranslation(pos)

        transform_node.setRotation(quat)

        transform_node.setScale(scale)

        print pos

        print quat

        print scale





def run():

    load_plugin()

    delete_curve_locator()

    json_data = pyperclip.paste()

    try:

        edge_data = json.loads(json_data)

    except:

        print('Edge data not found in the clipboard')

        return



    create_edge_locator(edge_data)

