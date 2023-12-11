# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import re
import os


class PathFinder(object):
    """
    """

    # SVNのデフォルトキャラモデルパス
    SVN_CHARA_MODEL_DIR_PATH = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model'

    # ファイル検索を行う拡張子
    SEARCH_SUFFIX_LIST = ['ma', 'fbx', 'tga']

    # パーツタイプの種類及び短縮語の辞書
    PART_TYPE_PARAM_DICT = {
        'body': 'bdy',
        'head': 'chr',
        'tail': 'tail',
        'toon_prop': 'toon_prop',
        'prop': 'prop',
    }

    # ファイル名検索の際のパーツタイプ変換
    # propのファイル名だけパーツタイプの短縮語規則に当てはまらなかったため
    PART_TYPE_FILE_PARAM_DICT = {
        'prop': 'chr_prop'
    }

    # キャラIDディレクトリ以下の取得したいディレクトリの命名規則
    PARENT_DIR_FIRST_REGEX_LIST = [
        'scenes',
        'sourceimages'
    ]
    # 上記の更に1つ下層のディレクトリの命名規則
    PARENT_DIR_SECOND_REGEX_LIST = [
        '/hair',
        '/face',
        '/num',
        '/offline',
        '/waku',
        '/zekken',
        r'/[0-9]{2}',  # bdy0006 バックダンサー衣装
        ''
    ]

    # キャラIDの基本的な命名規則
    CHARA_ID_REGEX = r'[0-9]{4}_[0-9]{2}'

    # モデルma/fbxでキャラIDの後に付く命名規則
    MODEL_SUFFIX_REGEX_LIST = [
        '_[0-9]{2}_[0-9]_[0-9]_[0-9]',  # fbx 共通衣装
        '_[0-9]{2}_Bust[ML]',  # ma 共通衣装
        '_[0-9]{2}',
        '_face[0-9]{3}',  # ma/fbx chr0001
        '_hair[0-9]{3}',  # ma/fbx chr0001
        '_[0-9]{2}_[0-9]',  # fbx ミニ共通衣装
        '_face[0-9]',  # ma/fbx ミニ共通顔
        '_hair',  # ma/fbx ミニ頭
        ''
    ]

    # テクスチャのキャラID移行のREGEXリスト
    # 利用する時は'|'.join(LIST名)で連続した文字列として使う
    TEXTURE_SECOND_REGEX_LIST = [
        '_num[0-9]{2}',  # bdy0001 num
        '_[0-9]{2}_[0-9]_[0-9]_[0-9]{2}',  # bdy0001 offline 他
        '_[0-9]{2}_waku[0-9]',  # bdy0001 waku
        '_zekken[0-9]_[0-9]',  # bdy0001 zekken
        '_[0-9]{2}_[0-9]_[0-9]_[0-9]',  # 汎用衣装全般
        '_[0-9]{2}_[0-9]_[0-9]_[0-9]{2}',  # bdy0006 バックダンサー衣装
        '_[0-9]{2}_[0-9]_[0-9]',
        '_face[0-9]{3}_[0-9]',
        '_hair[0-9]{3}_[0-9]',
        '_face[0-9]_[0-9]',
        '_[0-9]{4}',  # 汎用tail
        '_eye',
        '_hair',
        '_face',
        '_mayu',
        '_mouth',
        ''
    ]
    TEXTURE_THIRD_REGEX_LIST = [
        '_base', '_ctrl', '_diff', '_shad_c', '_area', '_emi', '_dyn_emi', '_dyn_emi_mask'
        '_cheek_for_maya[0-1]', '_cheek[0-1]', '_eye0', '_eyehi0[0-2]',
        '_rfl', ''
    ]
    TEXTURE_FOURTH_REGEX_LIST = [
        '_wet',
        ''
    ]
    GENERAL_PURPOSE_TEXTURE_LIST = ['tex_chr_tear00.tga']

    def __init__(self, part_type, chara_id=None, is_mini=False, is_directory=False):
        """
        """

        self.part_type = part_type
        self.chara_id = chara_id
        self.is_mini = is_mini
        self.is_directory = is_directory

        self.mini_regex = ''
        self.mini_short_regex = ''
        if self.is_mini:
            self.mini_regex = 'mini/'
            self.mini_short_regex = 'm'

        self.part_type_regex = '|'.join(list(self.PART_TYPE_PARAM_DICT.values()))
        if self.part_type in list(self.PART_TYPE_PARAM_DICT.keys()):
            self.part_type_regex = self.PART_TYPE_PARAM_DICT[self.part_type]

        # 01_model/body等のパーツディレクトリ以下のディレクトリの名前
        # 例: m(chr)[0-9]{4}_[0-9]{2}
        self.default_chara_model_dir_child_regex = '^{0}({1}){2}$'.format(
            self.mini_short_regex,
            self.part_type_regex,
            self.CHARA_ID_REGEX
        )

        # ファイルの親のディレクトリの命名規則
        # ファイル検索の際、ディレクトリ階層の命名規則が正しいかチェックするREGEX
        self.file_parent_full_path_regex = '^{0}/{1}({2})/{3}{4}{5}/({6})({7})$'.format(
            self.SVN_CHARA_MODEL_DIR_PATH,
            self.mini_regex,
            self.part_type,
            self.mini_short_regex,
            self.part_type_regex,
            self.CHARA_ID_REGEX,
            '|'.join(self.PARENT_DIR_FIRST_REGEX_LIST),
            '|'.join(self.PARENT_DIR_SECOND_REGEX_LIST)
        )

        self.file_part_type_regex = self.part_type_regex
        if self.part_type_regex in list(self.PART_TYPE_FILE_PARAM_DICT.keys()):
            self.file_part_type_regex = self.PART_TYPE_FILE_PARAM_DICT[self.file_part_type_regex]

        # model(ma/fbx)の命名規則
        model_default_regex = '^mdl_{0}({1}){2}({3})'.format(
            self.mini_short_regex,
            self.file_part_type_regex,
            self.CHARA_ID_REGEX,
            '|'.join(self.MODEL_SUFFIX_REGEX_LIST)
        )
        self.model_ma_default_regex = model_default_regex + r'.ma$'
        self.model_fbx_default_regex = model_default_regex + r'.fbx$'

        # textureの命名規則
        self.texture_default_regex = '^tex_{0}({1}){2}({3})({4})({5}).tga$'.format(
            self.mini_short_regex,
            self.file_part_type_regex,
            self.CHARA_ID_REGEX,
            '|'.join(self.TEXTURE_SECOND_REGEX_LIST),
            '|'.join(self.TEXTURE_THIRD_REGEX_LIST),
            '|'.join(self.TEXTURE_FOURTH_REGEX_LIST)
        )

        self.dir_list = []
        self.model_ma_list = []
        self.model_fbx_list = []
        self.texture_list = []

        self.set_target_path()

    def reset_path_list(self):
        """
        """

        self.dir_list = []
        self.model_ma_list = []
        self.model_fbx_list = []
        self.texture_list = []

    def set_target_path(self):
        """
        """

        self.reset_path_list()

        dir_regex = self.default_chara_model_dir_child_regex
        model_ma_regex = self.model_ma_default_regex
        model_fbx_regex = self.model_fbx_default_regex
        texture_regex = self.texture_default_regex

        if self.part_type not in list(self.PART_TYPE_PARAM_DICT.keys()):
            return

        if self.chara_id is not None:

            match_regex = re.search('^([0-9]{4}|[0-9])(_[0-9]{2}|)', str(self.chara_id))
            if not match_regex:
                return

            main_id_regex = match_regex.group(1)
            if len(main_id_regex) == 1:
                main_id_regex = main_id_regex + '[0-9]{3}'
            sub_id_regex = match_regex.group(2)
            if not sub_id_regex:
                sub_id_regex = r'_[0-9]{2}'

            dir_regex = '^{0}{1}{2}{3}$'.format(
                self.mini_short_regex,
                self.part_type_regex,
                main_id_regex,
                sub_id_regex
            )

            model_regex = '^mdl_{0}{1}{2}{3}({4})'.format(
                self.mini_short_regex,
                self.file_part_type_regex,
                main_id_regex,
                sub_id_regex,
                '|'.join(self.MODEL_SUFFIX_REGEX_LIST)
            )
            model_ma_regex = model_regex + r'.ma$'
            model_fbx_regex = model_regex + r'.fbx$'

            texture_regex = '^tex_{0}({1}){2}{3}({4})({5})({6}).tga$'.format(
                self.mini_short_regex,
                self.file_part_type_regex,
                main_id_regex,
                sub_id_regex,
                '|'.join(self.TEXTURE_SECOND_REGEX_LIST),
                '|'.join(self.TEXTURE_THIRD_REGEX_LIST),
                '|'.join(self.TEXTURE_FOURTH_REGEX_LIST)
            )

        target_dir_path = '{0}/{1}{2}'.format(self.SVN_CHARA_MODEL_DIR_PATH, self.mini_regex, self.part_type)
        self.dir_list = self.get_target_dir_path_list(target_dir_path, dir_regex)
        if self.is_directory:
            return

        for _dir in self.dir_list:
            tmp_model_ma_list, tmp_model_fbx_list, tmp_texture_list = self.get_target_file_path_list(
                _dir, model_ma_regex, model_fbx_regex, texture_regex
            )

            self.model_ma_list.extend(tmp_model_ma_list)
            self.model_fbx_list.extend(tmp_model_fbx_list)
            self.texture_list.extend(tmp_texture_list)

    def get_target_dir_path_list(self, dir_path, dir_regex):
        """
        渡された命名規則に合致する対象のディレクトリ一覧を返す
        """

        dir_path_list = []

        if not os.path.exists(dir_path):
            return []

        child_dir_name_list = [dir for dir in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, dir))]
        for child_dir_name in child_dir_name_list:
            if dir_regex:
                if not re.search(dir_regex, child_dir_name):
                    continue

            dir_path_list.append(os.path.join(dir_path, child_dir_name))

        return dir_path_list

    def get_target_file_path_list(self, dir_path, model_ma_regex, model_fbx_regex, texture_regex):
        """
        対象のファイルパス一覧を渡された命名規則に従って振り分けて返す
        """

        model_ma_list = []
        model_fbx_list = []
        texture_list = []

        for root, dirs, files in os.walk(dir_path):

            if not re.search(self.file_parent_full_path_regex, root.replace('\\', '/')):
                continue

            for filename in files:
                if filename.split('.')[-1] not in self.SEARCH_SUFFIX_LIST:
                    continue

                if re.search(model_ma_regex, filename):
                    model_ma_list.append(os.path.join(root, filename))
                elif re.search(model_fbx_regex, filename):
                    model_fbx_list.append(os.path.join(root, filename))
                elif re.search(texture_regex, filename):
                    texture_list.append(os.path.join(root, filename))
                elif filename in self.GENERAL_PURPOSE_TEXTURE_LIST:
                    texture_list.append(os.path.join(root, filename))

        return model_ma_list, model_fbx_list, texture_list
