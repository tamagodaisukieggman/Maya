# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogFrame(object):

    # ===============================================
    def __init__(self):

        self.ui_id = None
        self.ui_log_text_scroll = None

        self.__create_ui()

        self.clear()

    # ===============================================
    def __create_ui(self):

        cmds.frameLayout(l=u'ログ', cll=0, cl=0, bv=0, mw=5, mh=5)

        self.ui_log_text_scroll = \
            cmds.scrollField(editable=False, wordWrap=True)

        cmds.button(label=u'クリア', c=self.__on_clear_log)

        cmds.setParent('..')

    # ===============================================
    def __on_clear_log(self, arg):

        self.clear()

    # ===============================================
    def write(self, text):

        current_text = cmds.scrollField(
            self.ui_log_text_scroll, q=True, text=True)

        result_text = ''
        if current_text != '':
            result_text = u'{0}\n{1}'.format(current_text, text)
        else:
            result_text = text

        cmds.scrollField(self.ui_log_text_scroll, e=True, text=result_text)

        cmds.scrollField(self.ui_log_text_scroll, e=True, ip=0, it='')

    # ===============================================
    def clear(self):

        cmds.scrollField(self.ui_log_text_scroll, e=True, text='')
