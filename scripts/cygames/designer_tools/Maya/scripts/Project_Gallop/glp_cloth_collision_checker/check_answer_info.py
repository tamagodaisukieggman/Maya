# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from builtins import object
except Exception:
    pass


class CheckAnswerInfo(object):
    """
    項目チェック後に返す項目
    """

    def __init__(self):
        """
        """

        self.result = True
        self.check_target_item_list = []
        self.invalid_item_list = []
        self.error_message = None
