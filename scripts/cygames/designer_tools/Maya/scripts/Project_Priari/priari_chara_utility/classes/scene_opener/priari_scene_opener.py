# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except:
    pass

import os
import re

import maya.cmds as cmds
import maya.mel as mel

from ....priari_common.utility import model_define as define


class PriariSceneOpener(object):
    """
    """

    def open_file(self, path):
        """シーンを開く
        作業者が使っていたmelに準拠した処理で開く

        Args:
            path (str): 開くシーンパス
        """

        if not os.path.exists(path):
            return

        # 前処理
        self.__pre_process(path)

        # melで読めなくなるので、パスの区切りを統一
        path = path.replace('\\', '/')

        # 以下作業者が読み込みに使っていたオープンコマンド
        cmd = ''
        cmd += 'source "performFileAction.mel";'
        cmd += 'global string $gOperationMode;'
        cmd += '$gOperationMode = "Open";'
        cmd += 'int $fileMode = "1";'
        cmd += 'string $type = "Best Guess";'
        cmd += 'performFileAction("{}",$fileMode,$type);'.format(path)
        mel.eval(cmd)

        # 後処理
        self.__post_process()

    def __pre_process(self, path):
        """オープン前の処理
        作業者が使っていたmelに準拠

        Args:
            path (str): 開こうとしているファイルパス
        """

        # ロック法線の保持
        if path.endswith('.fbx'):
            mel.eval('FBXProperty "Import|IncludeGrp|Geometry|OverrideNormalsLock" -v on;')

        if cmds.window('hyperShadePanel1Window', ex=True):
            cmds.deleteUI('hyperShadePanel1Window')

    def __post_process(self):
        """ファイルオープン後の処理
        作業者が使っていたmelに準拠
        """

        # mayaScanScene
        mel.eval('if(`exists ScanSceneNow`) ScanSceneNow;')

        # ノードのアンロック
        unlockNodes = ['initialShadingGroup', 'initialParticleSE']

        for node in unlockNodes:
            if cmds.objExists(node) and cmds.lockNode(node, q=True)[0]:
                cmds.lockNode(node, lock=False)
                cmds.warning('{} ノードのロックを解除しました'.format(node))

        # uiConfigurationScriptNode警告
        message = '\"uiConfigurationScriptNode\"が含まれています\nUI設定の書き換えに注意してください\n（UI保存がオンの場合はオフに設定してください）'
        if cmds.objExists('uiConfigurationScriptNode'):
            cmds.confirmDialog(title=u'注意！', message=message)

    def search_files(self, root_path, data_type, id_str, target_ext_str):
        """priariのモデルファイルを検索
        「ルートdir/タイプdir/キャラdir/差分dir/scenes/シーンファイル」という構成

        Args:
            root_path (str): モデルルートのパス
            data_type (str): avatar, unit などのデータタイプ
            id_str (str): 検索するIDの文字列（モデル固有のIDと部分一致）
            target_ext_str (str): 検索する拡張子。self.ext_listの中から指定する想定。

        Returns:
            list: ヒットしたファイルのパスリスト
        """

        if not os.path.exists(root_path):
            return ['{} が見つかりません'.format(root_path)]

        # ルート子階層にある該当タイプのフォルダリストを取得
        type_dir_paths = []
        if data_type == 'all':
            files = os.listdir(root_path)
            type_dir_paths = [os.path.join(root_path, f) for f in files if os.path.isdir(os.path.join(root_path, f))]
        else:
            type_dir_paths = [os.path.join(root_path, data_type)]

        if not type_dir_paths:
            return ['該当するファイルが見つかりません']

        # タイプフォルダ以下にある該当idのフォルダリストを取得
        hit_dir_path_list = []
        for type_dir in type_dir_paths:

            if not os.path.exists(type_dir):
                continue

            files = os.listdir(type_dir)
            dir_list = [f for f in files if os.path.isdir(os.path.join(type_dir, f))]

            for dir in dir_list:
                model_id = self.__get_model_id(dir)
                if model_id.find(id_str) >= 0:
                    hit_dir_path_list.append(os.path.join(type_dir, dir))

        if not hit_dir_path_list:
            return ['該当するファイルが見つかりません']

        # 該当idを持つファイルをscenesフォルダ内で検索
        hit_file_list = []
        for dir_path in hit_dir_path_list:

            for curDir, dirs, files in os.walk(dir_path):

                if curDir.find('scenes') < 0:
                    continue

                for file in files:

                    model_id = self.__get_model_id(file)
                    if model_id.find(id_str) < 0:
                        continue

                    if target_ext_str == 'all':
                        if file.endswith('.ma') or file.endswith('.fbx'):
                            hit_file_list.append(os.path.join(curDir, file))
                    else:
                        if file.endswith(target_ext_str):
                            hit_file_list.append(os.path.join(curDir, file))

        if len(hit_file_list) == 0:
            hit_file_list.append('該当するファイルが見つかりません')

        return hit_file_list

    def __get_model_id(self, file_name):
        """モデル固有のidを返す
        モデル固有のIDはavatarなら7桁の先頭5桁、それ以外は6桁の先頭4桁

        Args:
            file_name (_type_): _description_

        Returns:
            _type_: _description_
        """

        if file_name.find(define.AVATAR_SHORT_DATA_TYPE) >= 0 or file_name.find(define.AVATAR_DATA_TYPE) >= 0:
            m = re.search(r'([0-9]{5})[0-9]{2}', file_name)
            if m:
                return m.group(1)

        else:
            m = re.search(r'([0-9]{4})[0-9]{2}', file_name)
            if m:
                return m.group(1)

        return ''
