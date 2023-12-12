# -*- coding: utf-8 -*-
import codecs
from datetime import datetime
import os
import sys
import maya.standalone
import maya.cmds as cmds

# チェッカーの場所
# パスを追加する必要がある
module_path = "Z:/mtk/tools/maya/modules/mtku/scripts/mtku/maya/menus/file/new_checker/rig"

# テキストファイルを保存する場所
# 実行スクリプトと同じディレクトリにする
directory_path = os.path.join(os.path.dirname(__file__))

if module_path not in sys.path:
    sys.path.append(module_path)

import check_convert_scene

# 検査対象のパス
# 対象以下のサブディレクトリも全部調べる
ROOT_PATH = "Z:/mtk/work/resources/animations/clips"
CHECK_FILE_NAME = "_convert.ma"

class CheckConvertScenes:

    def __init__(self):
        """コンストラクタ"""

        self.check_files = []
        self.scene_nodes = {}
        self.results = []
        
    def check_scenes(self):
        self.get_convert_scenes()
        
        if not self.check_files:
            print("not found [ {} ] files".format(CHECK_FILE_NAME))
            return
        
        maya.standalone.initialize(name='python')
        
        for i, scene in enumerate(self.check_files):
            cmds.file(scene, o=True, type="mayaAscii", ignoreVersion=True, f=True, options="v=0;")
            result = check_convert_scene.main(scene)
            results = []
            if result:
                results.extend(result)
                self.scene_nodes[scene] = results
            else:
                self.scene_nodes[scene] = []
        
        self.export_result()

        maya.standalone.uninitialize()

    def export_result(self):
        """エラー情報をテキストファイルに書き出し
        """
        
        if not self.scene_nodes:
            print("\n\n Not Found Error Scenes -----------------------\n\n")
            return
        
        _text = u"[u'{}'] u'以下の' ".format(ROOT_PATH)
        _text += u"[u'{}'] u'で終わるファイルをチェックしました'\n\n".format(CHECK_FILE_NAME)

        for k,v in self.scene_nodes.items():
            _text += u"[u'{}']\n".format(k)
            if v:
                for _ in v:
                    _text += u"error_text = [u'{}'], ".format(_[0])
                    _text += u"error_node = [u'{}']".format(_[-1].split("|")[-1])
                    _text += u"\n"
            else:
                _text += u"u'エラーは見つかりませんでした'\n"
            _text += u"\n\n"

        _text_file_path = os.path.join(directory_path, datetime.now().strftime("%Y_%m%d__%H_%M_%S")+".txt")
        with codecs.open(_text_file_path, "w", 'utf-8') as f:
            f.write(_text)

    def get_convert_scenes(self):
        """maファイルの収集
        ROOT_PATH = "Z:/mtk/work/resources/animations/clips"
        以下にある、
        CHECK_FILE_NAME = "_convert.ma"
        で終わるファイルを拾い集める
        """
        for dirpath, dirnames, filenames in os.walk(ROOT_PATH):
            for filename in filenames:
                if filename.endswith(CHECK_FILE_NAME):
                    _file = os.path.join(dirpath, filename).replace(os.sep, '/')
                    self.check_files.append(_file)


def main():
    check_scene = CheckConvertScenes()
    check_scene.check_scenes()


if __name__ == "__main__":
    main()
