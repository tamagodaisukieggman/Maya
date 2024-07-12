# -*- coding: utf-8 -*-
import maya.api.OpenMaya as om2
import maya.cmds as cmds
import json

TANGENT_TYPE_MAP = {
    1: "fixed",
    2: "linear",
    3: "flat",
    5: "step",
    6: "slow",
    7: "fast",
    9: "spline",
    10: "clamped",
    16: "plateau",
    17: "stepNext",
    18: "auto",
    27: "autoMix",
    28: "autoEase",
    29: "autoCustom"
}

def set_driven_keys_from_dict(data_dict):
    """
    Sets driven keys based on the provided dictionary of settings.

    :param data_dict: dict, Dictionary containing driver attribute and keyframes.
    """
    driver_attr = data_dict['driver_attr']
    keyframes = data_dict['keyframes']

    for keyframe in keyframes:
        driver_value = keyframe['driver_value']
        for driven_attr, driven_value in keyframe['driven_values'].items():
            itt = keyframe.get('itt', 'linear')
            ott = keyframe.get('ott', 'linear')

            cmds.setDrivenKeyframe(driven_attr, currentDriver=driver_attr, driverValue=driver_value, value=driven_value, itt=itt, ott=ott)
            print(f"Set driven key: {driver_attr} = {driver_value}, {driven_attr} = {driven_value}, itt={itt}, ott={ott}")

def load_driven_key_settings_from_file(file_path):
    """
    Loads driven key settings from a JSON file and sets the driven keys.

    :param file_path: str, Path to the JSON file containing driven key settings.
    """
    with open(file_path, 'r') as f:
        settings = json.load(f)
        for data_dict in settings:
            set_driven_keys_from_dict(data_dict)

def get_anim_curves_from_node(node):
    """
    Gets all driven animCurve nodes connected to the specified node, including those connected via blendWeighted nodes.

    :param node: str, The name of the node to check for driven animCurve connections.
    :return: list of str, The driven animCurve nodes connected to the node.
    """
    anim_curve_types = [
        'animCurveTA',
        'animCurveTL',
        'animCurveTT',
        'animCurveTU',
        'animCurveUA',
        'animCurveUU',
        'animCurveUL']
    anim_curves = []
    connections = cmds.listConnections(node, source=True, destination=False, skipConversionNodes=True)
    if not connections:
        return anim_curves

    for conn in connections:
        if 'animCurve' in cmds.nodeType(conn):
            anim_curves.append(conn)
        elif cmds.nodeType(conn) == 'blendWeighted':
            anim_curves += get_anim_curves_from_node(conn)

    return anim_curves

def convert_to_list(value):
    """
    Converts a single value to a list if it's not already a list.

    :param value: The value to convert.
    :return: list, The converted value as a list.
    """
    if not isinstance(value, list):
        return [value]
    return value

def get_final_driven_attr_connection(node):
    """
    Recursively finds the final driven attribute connection, skipping conversion nodes.

    :param node: str, The node to check for driven connections.
    :return: str, The final driven attribute connection.
    """
    connections = cmds.listConnections(node, source=False, destination=True, plugs=True, skipConversionNodes=True)
    if not connections:
        return None

    final_connection = connections[0]
    if cmds.nodeType(final_connection.split('.')[0]) in ['blendWeighted', 'unitConversion']:
        return get_final_driven_attr_connection(final_connection.split('.')[0])
    
    return final_connection

def save_driven_keys_to_file(file_path):
    """
    Saves the current driven key settings to a JSON file.

    :param file_path: str, Path to the JSON file to save the driven key settings.
    """
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        om2.MGlobal.displayError("No objects selected.")
        return

    driven_key_data = []
    driver_keyframes = {}

    for obj in selected_objects:
        anim_curves = get_anim_curves_from_node(obj)

        if not anim_curves:
            continue

        for anim_curve in anim_curves:
            connections = cmds.listConnections(anim_curve + '.input', plugs=True)
            if not connections:
                continue
            driver_attr = connections[0]
            driven_attr = get_final_driven_attr_connection(anim_curve)
            if not driven_attr:
                continue

            keyframes = driver_keyframes.get(driver_attr, [])
            driver_values = [ktv[0] for ktv in cmds.getAttr(f'{anim_curve}.ktv[*]')]
            values = [ktv[1] for ktv in cmds.getAttr(f'{anim_curve}.ktv[*]')]
            itts = [TANGENT_TYPE_MAP[itt] for itt in convert_to_list(cmds.getAttr(f'{anim_curve}.kit[*]'))]
            otts = [TANGENT_TYPE_MAP[ott] for ott in convert_to_list(cmds.getAttr(f'{anim_curve}.kot[*]'))]

            for driver_value, value, itt, ott in zip(driver_values, values, itts, otts):
                keyframe = next((kf for kf in keyframes if kf['driver_value'] == driver_value), None)
                if not keyframe:
                    keyframe = {
                        'driver_value': driver_value,
                        'driven_values': {},
                        'itt': itt,
                        'ott': ott
                    }
                    keyframes.append(keyframe)

                keyframe['driven_values'][driven_attr] = value

            driver_keyframes[driver_attr] = keyframes

    for driver_attr, keyframes in driver_keyframes.items():
        driven_key_data.append({
            'driver_attr': driver_attr,
            'keyframes': keyframes
        })

    with open(file_path, 'w') as f:
        json.dump(driven_key_data, f, indent=4)
        print(f"Driven key settings saved to {file_path}")

# # Example usage to load settings
# file_path = 'driven_key_settings.json'
# load_driven_key_settings_from_file(file_path)

# # Example usage to save settings
# output_file_path = 'saved_driven_key_settings.json'
# save_driven_keys_to_file(output_file_path)
