import os
import sys

import pytest

TEST_PATH = "D:/tech-designer/maya_legacy/scripts/Project_Wizard2/tests"


class MayaTester(object):
    @classmethod
    def run(cls, path=None, remote=False):
        maya_output = sys.stdout

        sys.stdout = sys.__stdout__
        if not remote:
            sys.stdout.write = maya_output.write

        tests_path = TEST_PATH
        if path:
            tests_path = path

        pytest.main(["-v", tests_path, "--maxfail=1"])

        sys.stdout = maya_output

        cls._delete_test_modules()

    @classmethod
    def _delete_test_modules(cls):
        name = "test_"
        module_list = [_ for _ in sys.modules]
        module_list.sort()

        for k in module_list:
            if k.startswith(name):
                del sys.modules[k]


if __name__ == "__main__":
    MayaTester.run(remote=True)
