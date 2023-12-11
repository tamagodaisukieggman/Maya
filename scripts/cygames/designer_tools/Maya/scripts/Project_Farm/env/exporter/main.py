# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from ...base_common import utility as base_utility
from ..common import command as env_cmd
from . import command
from .gui import *

try:
    # Maya 2022-
    from importlib import reload
except:
    pass

reload(base_utility)
reload(env_cmd)
reload(command)


def show():
    if not env_cmd.get_models():
        base_utility.ui.dialog.open_ok(
            u'FarmEnvExporter',
            u'命名規則に一致するモデルが見つかりません。')
        return

    window = MainWindow()
    window.update()
    window.show()


def batch_export():
    command.batch_export()
