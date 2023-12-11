# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except:
    pass

import sys

def template_exec_cmd():
    """
    クラスと同階層の実行関数
    """

    template_classes = TemplateClasses()
    template_classes.exec_cmd()


class TemplateClasses(object):
    """
    """

    def __init__(self):
        """
        """

        pass

    def exec_cmd(self, *args):
        """
        """

        arg_str = ''
        arg_list = []
        for arg in args:
            
            if sys.version_info.major == 2:
                if type(arg) == str or type(arg) == unicode:
                    arg_list.append(arg)
                else:
                    arg_list.append(str(arg))
            else:
                if type(arg) == str or type(arg) == bytes:
                    arg_list.append(arg)
                else:
                    arg_list.append(str(arg))

        if arg_list:
            arg_str = ','.join(arg_list)

        print('*' * 20)
        print('実行テスト')
        print('引数 : {0}'.format(arg_str))
        print('*' * 20)
