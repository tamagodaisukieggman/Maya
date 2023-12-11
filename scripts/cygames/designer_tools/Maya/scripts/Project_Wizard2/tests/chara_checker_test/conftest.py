import os
import sys
import pytest

# Whether the tests are running in mayapy or not.
HAS_MAYA: bool
try:
    import maya.standalone
except ImportError:
    HAS_MAYA = False
else:
    HAS_MAYA = True

def pytest_sessionstart(session: pytest.Session):
    print("start")
    os.environ["PYTHONPATH"] = "D:/tech-designer/maya_legacy/scripts"
    
    maya.standalone.initialize("ptyhon")


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    # Uninitialize maya standalone only if it is running in mayapy.
    maya.standalone.uninitialize()
    
    print("finish")