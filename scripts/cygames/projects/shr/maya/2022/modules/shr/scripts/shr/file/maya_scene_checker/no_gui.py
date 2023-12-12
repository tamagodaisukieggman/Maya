from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import os
import sys

import importlib
from pathlib import Path

MAYA_PROGRAM_PATH = Path(os.getenv("MAYA_LOCATION"))
MAYAPY_PATH = MAYA_PROGRAM_PATH / "bin" / "mayapy.exe"

MODULE_PATHS = [
                r"C:\Program Files\Autodesk\Maya2022\bin",
                r"C:\Program Files\Autodesk\Maya2022\Python37\lib\site-packages",
                r"C:\cygames\shrdev\shr\tools\tp\lib\pyside\2_py39\site-packages",
                r"C:\cygames\shrdev\shr\tools\in\ext\maya\2022\modules",
                r"C:\cygames\shrdev\shr\tools\tp\lib\python\3.9\site-packages",
                r"C:\cygames\shrdev\shr\tools\tp\ext\maya\share\python\3.9\site-packages",
                r"C:\cygames\shrdev\shr\tools\in\ext\maya\2022\modules\shr\scripts",
                r"C:\cygames\shrdev\shr\tools\in\ext\maya\2022\modules\shr\scripts\shr",
                r"C:\cygames\shrdev\shr\tools\in\ext\maya\2022\modules\shr\scripts\shr\file\maya_scene_checker",
                r"C:\cygames\shrdev\shr\tools\tp\ext\maya\share\python\3.9\site-packages",
]

for path in MODULE_PATHS:
    if path not in sys.path:
        sys.path.append(path)

for path in sys.path:
    print(path)

import maya.standalone
from maya import cmds
import maya.mel

import shr.file.maya_scene_checker.scene_data as scene_data
import shr.file.maya_scene_checker.checker as checker

# 開発中はTrue、リリース時にFalse
DEV_MODE = True

if DEV_MODE:
    importlib.reload(checker)
    importlib.reload(scene_data)


class BatchChecker:
    def __init__(self):
        self.scene_path = ""


    def check_maya_scene(self, scene_path=""):
        """Maya シーンを受け取り
        ファイルを開いた手からチェック開始

        Args:
            scene_path (str): Maya scene path
        """
        self.scene_path = scene_path
        self.open_maya_scene()
        self.do_check()

    def open_maya_scene(self):
        """Maya シーンを開く
        """
        if not self.scene_path:
            print("not set maya scene")
            return
        cmds.file(self.scene_path, open=True, f=True, prompt=True, resetError=True)

    def memory_clear(self):
        """メモリクリア
        """
        self.results = None
        self.modifies = list()
        self.modify_errors = list()

        self.scene_path_obj = None
        self.modifies = list()
        self.modify_errors = list()
        self.checker = checker.Checker()

    def get_datas(self):
        """シーンデータの取得
        """
        self.scene_path_obj = scene_data.SceneData()

    def do_check(self):
        """チェック実行
            メモリクリア
            シーン情報取得
            チェック実行
        """

        self.memory_clear()
        self.get_datas()
        print(f' {"Check Start": <12} {"":=>100}')
        self.checker.do_check()
        result = self.checker.result

        if not DEV_MODE:
            logger.info(f'Check Start : [ {self.scene_path_obj.scene_name} ]')
        else:
            print(f'Scene name [ {self.scene_path_obj.scene_name} ]')

        if result:
            self.results = result
            self.print_result()
        else:
            if not DEV_MODE:
                logger.info('Not Found Error')
            else:
                print(f'Not Found Error')
        print(f'Error Num ---- [ {len(result)} ]')
        print(f' {"Check End": <12} {"":=>100}')

    def print_result(self):
        """エラー内容を表示
        """
        _result_datas = self.results.get_sort_data()
        _result = {}
        for result in _result_datas:
            result:scene_data.ResultData = result
            if result.error == "Warning":
                continue

            text = str(result.error_text)
            error = f'{str(result.error)}'

            node = result.error_nodes

            _exists = _result.get(error, None)
            if not _exists:
                _text = f'{len(node)}:{text}'
            else:
                _ = _exists.split(":", 1)
                _text = _[-1]
                num = _[0]
                _text = f'{len(node) + int(num)}:{text}'

            _result[error] = _text
            print(f'{error:-<50}{text:->50}')


class BatchCheck:
    def __init__(self):
        self._i = 0
        self._start_time = time.time()
        self.root_path = None
        # self.set_env()
        maya.standalone.initialize(name='python')
        self.ck = BatchChecker()

    def set_root_path(self, path=""):
        """ルートパスの設定

        Args:
            path (str): パスオブジェクトに入れる
        """
        self.root_path = Path(path)

    def check_one_file(self, path=""):
        """チェックの実行

        Args:
            path (str): ファイルパス
        """

        if not path and path.suffix != ".ma" or path.suffix != ".mb":
            return
        self.ck.check_maya_scene(path)

    def check(self):
        """チェック前の処理
        入力されたパスがディレクトリであれば
        サブディレクトリ以下のファイルも対象にする
        """
        _i = 0

        if self.root_path:
            if self.root_path.is_file():
                try:
                    self.check_one_file(self.root_path)
                    _i += 1
                except Exception as e:
                    print(e)
            else:
                for path in self.root_path.glob('**/*.mb'):
                    try:
                        self.check_one_file(path)
                        _i += 1
                    except Exception as e:
                        print(e)

        self._i = _i
        self.end_procces()

    def set_env(self):
        """環境変数の設定

        """
        mtk_maya_tool_path = os.getenv("MTK_MAYA_TOOL_PATH")
        python_path = os.getenv("PYTHON_PATH")
        maya_plug_in_path = os.getenv("MAYA_PLUG_IN_PATH")
        prj_pythonpath = r'Z:\mtk\tools\techart\python\python37-64\modules;'
        prj_pythonpath += r'Z:\mtk\tools\techart\python\python37-64\cutscene;'
        prj_pythonpath += r'Z:\mtk\tools\maya\share\python37-64\Lib\site-packages;'
        prj_pythonpath += r'{}'.format(python_path)

        os.environ['MAYA_MODULE_PATH'] = r'Z:\mtk\tools\maya\2922\modules'
        os.environ['MTK_MAYA_TOOL_PATH'] = r'{};Z:\mtk\tools\maya\2022'.format(mtk_maya_tool_path)
        os.environ['PRJ_PYTHONPATH'] = prj_pythonpath
        os.environ['PYTHONPATH'] = prj_pythonpath
        # os.environ['MAYA_PLUG_IN_PATH'] = r'Z:\cyllista\tools\maya\modules\anm\plug-ins\2022;{}'.format(maya_plug_in_path)

    def end_procces(self):
        """終了時の処理
        """
        maya.standalone.uninitialize()
        calc_time = time.time() - self._start_time
        print(f'Check End : [ {self._i} ] Maya Scene Files : Time [ {calc_time} ]')

def main(directory_path=""):
    if not directory_path:
        return
    print(f'Input: directory_path [ {directory_path} ]')

    ck = BatchCheck()
    ck.set_root_path(directory_path)
    ck.check()

if __name__ == '__main__':
    # バッチ運用
    main(sys.argv[-1])

    # 個別シーンテスト
    # main(r"C:\cygames\shrdev\shr_art\resources\environments\assets\r01bag\work\maya\r01_bag01_01.mb")

    # ディレクトリ一括テスト
    # main(r"C:\cygames\shrdev\shr_art\resources\environments\assets")





