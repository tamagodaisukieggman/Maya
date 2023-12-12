import os
import pathlib
import sys
import time
from pathlib import Path

import pytest
from maya import cmds, utils

REMOTE_MAYA_TEST = os.environ.get("REMOTE_MAYA_TEST", False)

print("REMOTE_MAYA_TEST", type(REMOTE_MAYA_TEST))
print("REMOTE_MAYA_TEST", REMOTE_MAYA_TEST)

if REMOTE_MAYA_TEST:
    sys.path.append("Z:/mtk/tools/maya/2022/modules/mtk/scripts")
    sys.path.append("Z:/mtk/tools/techart/python/python37-64/modules")
    sys.path.append("Z:/mtk/tools/techart/python/python37-64/cutscene")
    sys.path.append("Z:/mtk/tools/maya/share/python37-64/Lib/site-packages")
    sys.path.append("Z:/mtk/tools/maya/share/python37-64/devLib/site-packages")


@pytest.fixture(scope="session", autouse=REMOTE_MAYA_TEST)
def auto_quit_maya_application():
    yield
    utils.executeDeferred(lambda: cmds.quit())

# TODO: 未来的には各関数のタイムアウトを設定する。
