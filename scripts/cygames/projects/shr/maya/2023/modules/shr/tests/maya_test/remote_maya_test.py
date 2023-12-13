import os
import subprocess
import sys

MAYA_EXE = "C:/Program Files/Autodesk/Maya2022/bin/maya.exe"
TEST_MEL_PATH = "Z:/mtk/tools/maya/2022/modules/mtk/tests/maya_test/exec_maya.mel"


def remote_maya_test():
    os.environ["MAYA_UI_LANGUAGE"] = "en_US"
    os.environ["REMOTE_MAYA_TEST"] = "true"

    proc = subprocess.Popen([MAYA_EXE, "-script", TEST_MEL_PATH],
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True)

    buffer = []

    while True:
        line = proc.stdout.readline()
        buffer.append(line)
        sys.stdout.write(line)
        if not line and proc.poll() is not None:
            break


if __name__ == "__main__":
    remote_maya_test()
