# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os
import random
import subprocess
import sys
import time
from xml.etree import cElementTree

import maya.cmds as cmds


class JsxBridge(object):

    VERSION = '22050201'

    ADOBE_ROOT_PATH = 'C:/Program Files/Adobe'
    PS_EXE_NAME = 'Photoshop.exe'

    ALLOWED_DATA_TYPE = ['int', 'float', 'str', 'bool', 'list', 'tuple', 'long', 'unicode']
    AUTOMATIC_ITEMNAME_PREFIX = 'jb_array_'

    def __init__(self):
        self.__xml_arg_root = None
        self.__array_count = None
        self.__session_id = None

        self.locking_time_out = None
        self.result_time_out = None

        self.working_folder = None
        self.xml_setting_path = None
        self.xml_result_path = None
        self.lock_file_path = None
        self.result_xml_data = None

    def initialize(self, looking_time_out, result_time_out):
        """
        実際にクラスを使っていくために値を初期化する。
        """

        self.__xml_arg_root = None
        self.__array_count = 0
        self.__session_id = random.randint(0, 100000000)

        self.locking_time_out = looking_time_out
        self.result_time_out = result_time_out

        self.working_folder = os.path.dirname(__file__)
        self.xml_setting_path = os.path.join(self.working_folder, 'xml_setting.xml')
        self.xml_result_path = os.path.join(self.working_folder, 'jsx_bridge_result.xml')
        self.lock_file_path = os.path.join(self.working_folder, 'jsx_bridge.lock')
        self.result_xml_data = None

    # ===============================================
    def exec_jsx(self, target_jsx_path, force_reset_lock_file=False, locking_time_out=10, result_time_out=0, **func_kwargs):
        """
        JSXを対象のアプリケーションで実行。
        args:
            target_jax_path: str: 実行したいJSXファイルの場所
            force_reset_lock_file: bool: bindファイルを削除するか
            locking_time_out: int: 多重実行時にタイムアウトするまで時間を指定する
            result_time_out: int: 結果を待つ際にどれだけでタイムアウトするかを指定する
            func_kwargs: kwargs: JSXに渡す引数はここに入れる。型は、ALLOWED_DATA_TYPEでなければならない
        return:
            bool: subprocessの実行まで成功したかが返る
        """

        self.initialize(locking_time_out, result_time_out)

        # target_jsx_pathは必ず存在している必要がある
        if target_jsx_path is None or not os.path.exists(target_jsx_path):
            cmds.warning('対象のJSXパスが存在しません')
            return False

        # Appのexeファイルがなくても止める
        app_path = self.__get_app_path()
        if app_path is None:
            cmds.warning('Photoshopの実行ファイルを発見できません')
            return False

        # bootloaderファイルがなくても止める
        bootloader_path = os.path.join(os.path.dirname(__file__), 'bootloader.jsx')
        if not os.path.exists(bootloader_path):
            cmds.warning('JSX bootloaderが見つかりません')
            return False

        # 二重起動防止
        if not force_reset_lock_file:
            if os.path.exists(self.lock_file_path):

                self.__wait_for_file_disposal(self.locking_time_out, [self.lock_file_path])

                if os.path.exists(self.lock_file_path):
                    cmds.warning('ロックされています')
                    return False

        # 前セッションのファイルなどが残っていたら消す
        self.reset_former_session_data(force_reset_lock_file)

        try:
            xml_obj = self.__create_setting_xml(target_jsx_path, func_kwargs)
            self.__export_arg_xml_file(xml_obj)
        except TypeError as e:
            cmds.warning(e)
            return False
        except AttributeError as e:
            cmds.warning(e)
            return False

        subprocess.Popen([app_path, bootloader_path], shell=True)

        return True

    # ===============================================
    def reset_former_session_data(self, force_reset_lock_file=False):
        """
        前のセッションで削除せずに終了したデータを削除。
        args:
            force_reset_lock_file: bool: 二重起動を抑止しているlockファイルを強制的に削除する。以前のセッションがJSX bootloader側で失敗していた場合に有効
        """

        if force_reset_lock_file:
            if os.path.exists(self.lock_file_path):
                os.remove(self.lock_file_path)

        if os.path.exists(self.xml_setting_path):
            os.remove(self.xml_setting_path)

        if os.path.exists(self.xml_setting_path):
            os.remove(self.xml_result_path)

    # ===============================================
    def get_return_code(self):
        """
        JSXのリターンコードを取得。
        return:
            str: リターンコードを返す
        """

        # 結果データが更新されていない場合はとりあえず、取得メソッドを試す
        if self.result_xml_data is None:
            self.__update_xml_result()

        # 一回更新は試しているのでここで取得できていない場合には、何らかのエラーなのでreturn
        if self.result_xml_data is None:
            return None

        ret = self.__xml_get_element_value(self.result_xml_data, './status')

        return ret

    # ===============================================
    def get_return_detail(self):
        """
        addResultInfoで登録された文字のリストを返されたXMLから取得。
        return:
            None / list : 返ってくる内容はJSX側でaddResultInfoで登録されたもの
        """

        # 結果データが更新されていない場合はとりあえず、取得メソッドを試す
        if self.result_xml_data is None:
            self.__update_xml_result()

        # 一回更新は試しているのでここで取得できていない場合には、何らかのエラーなのでreturn
        if self.result_xml_data is None:
            return None

        detail_list = self.__xml_get_all_element_value(self.result_xml_data, './info/item')

        return detail_list

    # ===============================================
    def __get_app_path(self):
        """
        アプリケーションのパスを返す
        return:
            str: アプリケーションのパスを返す
        """

        ps_exe_path = None

        years_last_two_digit = int(str(datetime.date.today().year)[-2:])

        for num in reversed(range(years_last_two_digit + 2)):

            # Phothoshop2020以降はフォルダ名に「CC」が付かなくなっている
            if num < 20:
                this_ps_exe_path = self.ADOBE_ROOT_PATH + '/Adobe Photoshop CC 20{}/'.format(num) + self.PS_EXE_NAME
                if os.path.isfile(this_ps_exe_path):
                    ps_exe_path = this_ps_exe_path
                    break

            else:
                this_ps_exe_path = self.ADOBE_ROOT_PATH + '/Adobe Photoshop 20{}/'.format(num) + self.PS_EXE_NAME
                if os.path.isfile(this_ps_exe_path):
                    ps_exe_path = this_ps_exe_path
                    break

        return ps_exe_path

    # ===============================================
    def __create_setting_xml(self, target_jsx_path, func_kwargs):
        """
        設定XMLを作成。
        args:
            target_jsx_path: str: 実行対象のJSXファイルのパスを指定する
            func_kwargs: dict: パラメータとして渡したい値を辞書形式で指定する。この辞書の中に辞書を含むことはできない
        return:
            xml.etree.ElementTree.Element: 作成されたXMLオブジェクトが返る
        """

        target_jsx_path = target_jsx_path.replace('\\', '/')

        # 必須設定部
        root = self.__xml_create_element('setting', '')
        target_info_element = self.__xml_create_element('target_info', '')
        self.__xml_add_element(target_info_element, 'path', target_jsx_path)
        self.__xml_add_element(target_info_element, 'session_id', self.__session_id)
        root.append(target_info_element)

        # 引数部
        if not func_kwargs == {}:
            self.__xml_arg_root = self.__xml_create_element('args', '')
            self.__create_arg_xml(func_kwargs, self.__xml_arg_root)
            root.append(self.__xml_arg_root)

        return root

    # ===============================================
    def __create_arg_xml(self, serialize_obj, parent_element):
        """
        引数部のXMLを作成。
        このセクションでは失敗した場合、例外をthrowするがこれは中途半端なデータがJSXにわたってしまうリスクを抑止するため。
        args:
            serialize_obj: ALLOWED_DATA_TYPE + dict, xml.itemに変換する対象。型はALLOWED_DATA_TYPEを満たす必要がある
            parent_element: xml.Element: アイテムを格納する対象になるxml.Elementの指定に使う
        """

        if parent_element == self.__xml_arg_root:

            for key, value in serialize_obj.items():

                # 名前はjb_array_から始まってはいけない(衝突防止のため)
                if key.startswith(self.AUTOMATIC_ITEMNAME_PREFIX):
                    raise AttributeError('引数に、{}から始まる名称はつけられません'.format(self.AUTOMATIC_ITEMNAME_PREFIX))

                self.__create_arg_parts_xml(key, value, parent_element)

        else:
            for value in serialize_obj:
                self.__create_arg_parts_xml('', value, parent_element)

    # ===============================================
    def __create_arg_parts_xml(self, key, value, parent_element):
        """
        引数部のXMLの実際の各部のパーツを作成。
        このセクションでは失敗した場合、例外をthrowするがこれは中途半端なデータがJSXにわたってしまうリスクを抑止するため。
        args:
            key: str: アイテムの名前として何か設定する必要がある場合に指定する
            value: ALLOWED_DATA_TYPE: xmlに値として登録することになる値。これ以外の型を渡すとTypeErrorによって処理が中止される
            parent_element: xml.Element: アイテムを格納する対象になるxml.Elementの指定に使用する
        """
        # データ型検証
        value_type = type(value).__name__
        if value_type not in self.ALLOWED_DATA_TYPE:
            raise TypeError('引数として、許可されていない型です')

        # itemの作成部
        if value_type != 'list' and value_type != 'tuple':

            # Python2向けにユニコード文字列に変換をかける
            # Python3環境では未検証のため、デコードは踏ませない
            if sys.version_info.major == 2:
                if type(value).__name__ == 'str':
                    value = value.decode('cp932')

            item_xml = self.__xml_create_element('item', '')

            # Add tag
            if key:
                item_xml.set('name', key)
            item_xml.set('type', value_type)

            self.__xml_add_element(item_xml, 'value', value)

            parent_element.append(item_xml)

        # arrayの作成部
        else:
            array_xml = self.__xml_create_element('array', '')

            if key:
                # Args_root上の場合
                array_xml.set('name', key)
            else:
                # Args_root上の以外
                new_array_name = self.AUTOMATIC_ITEMNAME_PREFIX + str(self.__array_count)
                self.__array_count += 1
                array_xml.set('name', new_array_name)

                # アレイの情報を上層に追加
                item_xml = self.__xml_create_element('item', '')
                item_xml.set('type', 'array')
                self.__xml_add_element(item_xml, 'value', '@array/{0}'.format(new_array_name))
                self.__xml_arg_root.append(array_xml)
                parent_element.append(item_xml)

            self.__create_arg_xml(value, array_xml)

            # JSX側で復元する際、多次元のアレイになっているとネスト先が先に入っていないと
            # 問題のため、XML書き込みはこの順番から変更しない。
            self.__xml_arg_root.append(array_xml)

    # ===============================================
    def __update_xml_result(self):
        """
        結果のXMLファイルをとってきて、self.result_xml_dataを更新。
        """
        if os.path.exists(self.lock_file_path) or os.path.exists(self.xml_setting_path):

            self.__wait_for_file_disposal(self.result_time_out, [self.lock_file_path, self.xml_setting_path])

            if os.path.exists(self.lock_file_path) or os.path.exists(self.xml_setting_path):
                cmds.warning('JSXファイルが実行中です')
                return

        if not os.path.exists(self.xml_result_path):
            cmds.warning('結果のファイルが発見できませんでした')
            return

        self.result_xml_data = self.__load_result_xml_file()
        if not self.__validation_session_id():
            self.result_xml_data = None
            # 自身のセッションのファイルでない場合、当該セッションが取りに来る可能性もあるので
            # ファイルは消さずにおく
            return

        # 使い終わったら削除
        os.remove(self.xml_result_path)

    # ===============================================
    def __validation_session_id(self):
        """
        取得したXMLのデータが自身のセッションのものか確認。
        """
        session_id = self.__xml_get_element_value(self.result_xml_data, './session_id')
        if str(session_id) != str(self.__session_id):
            print('session id not match!')
            return False

        return True

    # ===============================================
    def __load_result_xml_file(self):
        """
        XMLファイルを読み込む。
        return:
            cElementTree.Element: 読み込まれたElement
        """
        if not self.xml_result_path:
            return

        if not os.path.isfile(self.xml_result_path):
            return

        element_tree = cElementTree.parse(self.xml_result_path)
        if element_tree is None:
            return

        root_element = element_tree.getroot()
        if root_element is None:
            return

        return root_element

    # ===============================================
    def __export_arg_xml_file(self, xml_element):
        """
        XMLファイルを保存。
        args:
            xml_element: cElementTree.Element: 書き込む対象のElement
        """
        if xml_element is None or not self.xml_setting_path:
            return

        element_tree = cElementTree.ElementTree(element=xml_element)
        element_tree.write(self.xml_setting_path, encoding='utf-8')

    # ===============================================
    def __xml_get_element_value(self, xml_element, target_xml_path):
        """
        XMLのエレメントの値を検索する。複数ヒットした場合一番最初のものが返る。
        args:
            xml_element: cElementTree.Element: 検索対象のElement
            target_xml_path: str: xml_element上で検索したいパス
        return:
            str: 当該elementの値(JSX->Pythonデコード済み)
        """
        if xml_element is None or not target_xml_path:
            return

        target_element = xml_element.find(target_xml_path)
        if target_element is None:
            return

        return self.__decode_jsx_reserve_txt(target_element.text)

    # ===============================================
    def __xml_get_all_element_value(self, xml_element, target_xml_path):
        """
        XMLから検索したいエレメントのtextを集めて返す。
        args:
            xml_element: cElementTree.Element:検索対象のElement
            target_xml_path: str: 探したいXMLパス
        return:
            list(str): 当該element達の値(JSX->Pythonデコード済み)
        """
        if xml_element is None or not target_xml_path:
            return

        element_list = xml_element.findall(target_xml_path)
        if not element_list:
            return

        # 2Byte対応
        element_value_list = []
        for element in element_list:
            element_value_list.append(self.__decode_jsx_reserve_txt(element.text))

        return element_value_list

    # ===============================================
    def __xml_create_element(self, element_name, element_value):
        """
        XMLのエレメントを作成。
        args:
            element_name: str: 新規に作成するエレメント名
            element_value: str/int/float/unicode: エレメントの値として登録したい値
        return:
            cElementTree.Element: 新規で作成されたElement
        """
        if not element_name:
            return

        new_element = cElementTree.Element(element_name)

        if element_value is not None:
            if type(element_value).__name__ == 'unicode':
                new_element.text = element_value
            else:
                new_element.text = str(element_value)

        return new_element

    # ===============================================
    def __xml_add_element(self, target_element, element_name, element_value):
        """
        sub elementをtarget_element下に作成し返す。
        args:
            target_element: cElementTree.Element: 親にするElement
            element_name: str: 新規に作成するエレメント名
            element_value: str/int/float/unicode: エレメントの値として登録したい値
        return:
            cElementTree.Element: 新規で作成されたElement
        """
        if target_element is None:
            return

        if not element_name:
            return

        new_element = cElementTree.SubElement(target_element, element_name)
        if element_value is not None:
            if type(element_value).__name__ == 'unicode':
                new_element.text = element_value
            else:
                new_element.text = str(element_value)

        return new_element

    # ===============================================
    def __decode_jsx_reserve_txt(self, text):
        """
        JSXは"%"でエスケープだが、pythonは"\"なので変換してデコードし2byte文字を戻す。
        args:
            text: str: 変換対象の文字列
        return:
            str: 変換された文字列
        """
        if not text:
            return

        if '%u' in text:
            text = text.replace('%', '\\')
            text = text.decode('unicode-escape')

        return text

    # ===============================================
    def __wait_for_file_disposal(self, time_out_second, file_list):
        """
        ファイルが破棄されるかタイムアウトするまで待機。
        args:
            time_out_second: int: 最大で待機する時間を指定する
            file_list: list(str): ここで指定されたファイルが破棄されるのを待つ
        """

        if time_out_second is None:
            return

        if not file_list:
            return

        # タイムアウトするまで待つ
        elapsed_time = 0
        if time_out_second > 0:
            while True:
                time.sleep(1)
                elapsed_time += 1

                if elapsed_time >= time_out_second:
                    return

                # 与えられたファイルのリストがすべて破棄されているか確認する
                for file in file_list:
                    if os.path.exists(file):
                        break
                else:
                    return
