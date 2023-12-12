from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
import importlib
import os

from . import scene_data
from . import checker
from . import maya_utils
from . import settings
from . import pyside_gui

from ...utils import gui_util

from . import CHECKER_GUI_NAME
from . import CHECKER_RESULT_GUI_NAME

DEV_MODE = settings.load_config(config_name='DEV_MODE')

if DEV_MODE:
    importlib.reload(checker)
    importlib.reload(pyside_gui)
    importlib.reload(scene_data)
    importlib.reload(maya_utils)


def main():
    gui_util.close_pyside_windows([CHECKER_GUI_NAME,
                                   CHECKER_RESULT_GUI_NAME, ])
    scene_path_obj = scene_data.SceneData()
    if not scene_path_obj.scene_name:
        _d = gui_util.ConformDialog(title="Not Open Scene",
                                    message="Open Scene File")
        _d.exec_()
        return

    # print(scene_path_obj.scene_name)
    # print(scene_path_obj.type)
    # print(scene_path_obj.data_type_category)
    _cheker = checker.Checker()
    _cheker.do_check()

    if _cheker.result:
        _gui = pyside_gui.CheckerGUI()
        _gui.setTableData(_cheker.result, _cheker.scene_path)
        _gui.show()
    else:
        _d = gui_util.ConformDialog(title="Not Fond Error",
                                    message="Not Found Error")
        _d.exec_()





