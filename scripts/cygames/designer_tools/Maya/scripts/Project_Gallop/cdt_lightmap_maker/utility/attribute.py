# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Method(object):

    # ===========================================
    @staticmethod
    def exist_attr(target, target_attr):

        if target is None:
            return False

        if target_attr is None:
            return False

        if not cmds.objExists(target):
            return False

        exist = True
        try:
            cmds.getAttr(target, target + '.' + target_attr, type=True)
        except:
            exist = False

        return exist

    # ===========================================
    @staticmethod
    def delete_attr(target, target_attr_list, attr_prefix):

        all_attr_list = cmds.listAttr(target)

        for attr in all_attr_list:

            if attr.find(attr_prefix) != 0:
                continue

            exist_attr = False

            for target_attr in target_attr_list:

                if attr == target_attr:
                    exist_attr = True

            if exist_attr:
                continue

            cmds.deleteAttr(target, at=attr)

    # ===========================================
    @staticmethod
    def add_attr(target, attr_name, attr_nice_name, attr_type, attr_value):

        if target is None:
            return

        if not cmds.objExists(target):
            return

        if Method.exist_attr(target, attr_name):
            return

        if attr_type == 'string':

            cmds.addAttr(target,
                         longName=attr_name,
                         dataType=attr_type,
                         niceName=attr_nice_name)

            cmds.setAttr(target + '.' + attr_name,
                         attr_value,
                         type='string')

        elif attr_type == 'int':

            cmds.addAttr(target,
                         longName=attr_name,
                         attributeType='long',
                         defaultValue=attr_value,
                         niceName=attr_nice_name)

        elif attr_type == 'float':

            cmds.addAttr(target,
                         longName=attr_name,
                         attributeType='float',
                         defaultValue=attr_value,
                         niceName=attr_nice_name)

        elif attr_type == 'bool':

            cmds.addAttr(target,
                         longName=attr_name,
                         attributeType='bool',
                         defaultValue=attr_value,
                         niceName=attr_nice_name)

        elif attr_type == 'color':

            cmds.addAttr(target,
                         longName=attr_name,
                         usedAsColor=True,
                         attributeType='float3')

            cmds.addAttr(target,
                         longName=attr_name + 'R',
                         attributeType='float',
                         parent=attr_name)
            cmds.addAttr(target,
                         longName=attr_name + 'G',
                         attributeType='float',
                         parent=attr_name)
            cmds.addAttr(target,
                         longName=attr_name + 'B',
                         attributeType='float',
                         parent=attr_name)

            cmds.setAttr(target + '.' + attr_name,
                         attr_value[0], attr_value[1], attr_value[2],
                         type='float3')

        elif attr_type == 'array':

            cmds.addAttr(target,
                         longName=attr_name,
                         dataType='Int32Array',
                         multi=True,
                         niceName=attr_nice_name)

        elif attr_type == 'message':

            cmds.addAttr(target,
                         longName=attr_name,
                         at='message',
                         niceName=attr_nice_name)

        elif attr_type == 'list':

            enum_str = ''

            for cnt in range(0, len(attr_value)):

                enum_str += attr_value[cnt]

                if cnt != len(attr_value) - 1:
                    enum_str += ':'

            cmds.addAttr(target,
                         longName=attr_name,
                         at='enum',
                         en=enum_str,
                         niceName=attr_nice_name)

    # ===========================================
    @staticmethod
    def get_attr(target, attr_name, attr_type):

        result_value = None

        if attr_type == 'string':
            result_value = ''

        elif attr_type == 'int':
            result_value = 0

        elif attr_type == 'float':
            result_value = 0

        elif attr_type == 'bool':
            result_value = False

        elif attr_type == 'color':
            result_value = (1, 1, 1)

        elif attr_type == 'radio':
            result_value = ''

        if not cmds.objExists(target):
            return result_value

        if not Method.exist_attr(target, attr_name):
            return result_value

        result_value = cmds.getAttr(target + '.' + attr_name)

        if attr_type == 'color':
            result_value = result_value[0]

        return result_value

    # ===========================================
    @staticmethod
    def set_attr(target, attr_name, attr_type, attr_value):

        if not Method.exist_attr(target, attr_name):
            return

        if attr_type == 'string':

            cmds.setAttr(target + '.' + attr_name, attr_value, type='string')

        elif attr_type == 'int':

            cmds.setAttr(target + '.' + attr_name, attr_value)

        elif attr_type == 'float':

            cmds.setAttr(target + '.' + attr_name, attr_value)

        elif attr_type == 'bool':

            cmds.setAttr(target + '.' + attr_name, attr_value)

        elif attr_type == 'color':

            cmds.setAttr(target + '.' + attr_name,
                         attr_value[0], attr_value[1], attr_value[2],
                         type='float3')

        elif attr_type == 'radio':

            cmds.setAttr(target + '.' + attr_name, attr_value)

    # ===========================================
    @staticmethod
    def connect_attr(src_target, src_attr, dst_target, dst_attr):

        if not Method.exist_attr(src_target, src_attr):
            return

        if not Method.exist_attr(dst_target, dst_attr):
            return

        if cmds.isConnected(src_target + '.' + src_attr,
                            dst_target + '.' + dst_attr):
            return

        if src_target + '.' + src_attr == dst_target + '.' + dst_attr:
            return

        cmds.connectAttr(src_target + '.' + src_attr,
                         dst_target + '.' + dst_attr,
                         force=True)

    # ===========================================
    @staticmethod
    def disconnect_attr(src_target, src_attr, dst_target, dst_attr):

        if not Method.exist_attr(src_target, src_attr):
            return

        if not Method.exist_attr(dst_target, dst_attr):
            return

        if not cmds.isConnected(src_target + '.' + src_attr,
                                dst_target + '.' + dst_attr):
            return

        cmds.disconnectAttr(src_target + '.' + src_attr,
                            dst_target + '.' + dst_attr)
