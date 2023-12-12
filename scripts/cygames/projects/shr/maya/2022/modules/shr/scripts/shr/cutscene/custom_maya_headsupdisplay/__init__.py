# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from collections import OrderedDict

from . import app


def delete_all():
    app.DebugHeadsUpDisplay().delete_all()


def create(section_list=None):
    if section_list is None:
        section_list = OrderedDict()
        section_list["SceneName"] = 9
        section_list["CutName"] = 9
        section_list["Frame"] = 9
        section_list["FocalLength"] = 9

    if type(section_list) != OrderedDict:
        raise ValueError("不正な型です。 collections.OrderedDictを指定してください。")

    app.DebugHeadsUpDisplay.create_all(section_list)
