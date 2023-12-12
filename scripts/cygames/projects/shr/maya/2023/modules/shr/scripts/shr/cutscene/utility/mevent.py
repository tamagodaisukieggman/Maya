# -*- coding: utf-8 -*-
"""MEvent回りの機能"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya import cmds
from maya.api import OpenMaya


class MEventManager(object):
    """MEvent用の管理クラス

    MEventMessageとMUserEventMessageを管理する
    """

    __user_event_name_list = []
    __event_list = {}
    __user_event_list = {}

    @classmethod
    def get_event_list(cls):
        return cls.__event_list

    @classmethod
    def get_user_event_name_list(cls):
        return cls.__user_event_name_list

    @classmethod
    def get_user_event_list(cls):
        return cls.__user_event_list

    @classmethod
    def add_event(cls, name, function, event="timeChanged", client_data=None):
        event_id = OpenMaya.MEventMessage.addEventCallback(event, function, client_data)

        if name not in cls.__event_list:
            cls.__event_list[name] = [event_id]
        else:
            cls.__event_list[name].append(event_id)

    @classmethod
    def add_user_event(cls, name, function, event, client_data=None):
        if not OpenMaya.MUserEventMessage.isUserEvent(event):
            cmds.warning("User Event [{}] Not found.".format(event))
            return

        event_id = OpenMaya.MUserEventMessage.addUserEventCallback(event, function, client_data)

        if name not in cls.__user_event_list:
            cls.__user_event_list[name] = [event_id]
        else:
            cls.__user_event_list[name].append(event_id)

    @classmethod
    def remove_event(cls, name):
        if name in cls.__event_list:
            OpenMaya.MEventMessage.removeCallbacks(cls.__event_list[name])
            del cls.__event_list[name]

        if name in cls.__user_event_list:
            OpenMaya.MUserEventMessage.removeCallbacks(cls.__user_event_list[name])
            del cls.__user_event_list[name]

    @classmethod
    def remove_all(cls):
        for event in cls.__event_list:
            OpenMaya.MEventMessage.removeCallbacks(cls.__event_list[event])

        for event in cls.__user_event_list:
            OpenMaya.MUserEventMessage.removeCallbacks(cls.__user_event_list[event])

        cls.__event_list = None
        cls.__user_event_list = None

    @classmethod
    def register_user_event(cls, event_name):
        OpenMaya.MUserEventMessage.registerUserEvent(event_name)

        cls.__user_event_name_list.append(event_name)

    @classmethod
    def deregister_user_event(cls, event_name):
        if OpenMaya.MUserEventMessage.isUserEvent(event_name):
            OpenMaya.MUserEventMessage.deregisterUserEvent(event_name)

            cls.__user_event_name_list.remove(event_name)

    @classmethod
    def post_user_event(cls, event_name):
        OpenMaya.MUserEventMessage.postUserEvent(event_name)
