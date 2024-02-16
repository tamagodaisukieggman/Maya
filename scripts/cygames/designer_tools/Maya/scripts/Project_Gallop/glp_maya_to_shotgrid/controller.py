# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import json

from PySide2 import QtWidgets
from .settings import define
from .model import exec_playblast, shotgrid, screenshot_capture, sg_asset_default_setting
from .model.util import Util

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass


class Controller(object):

    def __init__(self, view, capture_window, login_dialog):

        self.view = view
        self.capture_window = capture_window
        self.login_dialog = login_dialog

        self.is_setting_setup_finished = False

        # sg関連パラメータ(保存し高速化するため)
        self.is_sg_setting_setup_finished = False
        self.sg_obj = None
        self.sg_project = None
        self.sg_field_set_list = []

        # SG関連 ユーザーデータ
        self.sg_url = ''
        self.sg_project_name = ''
        self.sg_user = ''
        self.sg_password = ''

        self.ui_setting_dict = {
            'target_dir': self.view.ui.target_dir_line,
            'pb_width': self.view.ui.pb_width_spinbox,
            'pb_height': self.view.ui.pb_height_spinbox,
            'pb_is_remove_org_avi': self.view.ui.pb_is_remove_org_avi,
            'pb_is_should_view_mp4': self.view.ui.pb_is_should_view_mp4
        }

        self.ui_setting_capture_window_dict = {
            'cw_width': self.capture_window.width_spinbox,
            'cw_height': self.capture_window.height_spinbox,
            'cw_pos_x': None,
            'cw_pos_y': None
        }

        self.is_setting_setup_finished = self.__load_setting()
        self.is_sg_setting_setup_finished = self.__set_sg_setting()

        self.sg_asset_default_setting = sg_asset_default_setting.SgAssetDefaultSetting()

    def check_loading_shotgun_api_module(self):
        u"""shotgun_api3モジュールが読み込めているかをチェックする
        gallop専用起動バッチ経由でない場合、shotgun_api3モジュールがpathにaddされていないため
        基本的にFalseになる
        """

        if not shotgrid.Shotgrid().check_loaded_shotgun_api_module():
            QtWidgets.QMessageBox().warning(None, 'Warning', u'moduleが読み込めないため、起動できません\ngallop専用Maya起動バッチからMayaを起動してください。')
            return False
        return True

    def __load_setting(self):
        u"""shotgridにアクセスするための情報をロードし変数にセット
        """

        if not self.__set_sg_project_setting():
            return False

        self.__set_sg_user_setting()

        return True

    def load_ui_setting(self):
        u"""UI情報をjsonから取得しセット
        """

        if not os.path.exists(define.UI_SETTING_JSON_PATH):
            return

        with open(define.UI_SETTING_JSON_PATH, 'r') as f:
            setting = json.load(f)

        for key, ui in list(self.ui_setting_dict.items()):

            if isinstance(ui, type(QtWidgets.QLineEdit())):
                ui.setText(self.__get_setting_value(setting, key))
            elif isinstance(ui, type(QtWidgets.QSpinBox())):
                ui.setValue(self.__get_setting_value(setting, key, 256))
            elif isinstance(ui, type(QtWidgets.QCheckBox())):
                ui.setChecked(self.__get_setting_value(setting, key, False))

        for key, ui in list(self.ui_setting_capture_window_dict.items()):

            value = self.__get_setting_value(setting, key, 500)

            if ui is None:

                if key == 'cw_pos_x':
                    self.capture_window.move(value, self.capture_window.pos().y())
                elif key == 'cw_pos_y':
                    self.capture_window.move(self.capture_window.pos().x(), value)

            elif isinstance(ui, type(QtWidgets.QSpinBox())):

                if key == 'cw_width':
                    self.capture_window.resize(value, self.capture_window.size().height())
                elif key == 'cw_height':
                    self.capture_window.resize(self.capture_window.size().width(), value)

                ui.setValue(value)

    def __get_setting_value(self, target_setting, target_key, default_value=''):
        u"""setting(jsonから取得した辞書型)から、該当のkeyがあればそれを返しなければdefault_valueを返却する

        Args:
            target_setting (dict): セッティング情報が入っている辞書
            target_key (str): 取得したい情報のキー
            default_value (str, optional): デフォルト値. Defaults to ''.

        Returns:
            string: 辞書から取得した情報、取得できなかったときはデフォルト値
        """

        return target_setting.get(target_key) if target_setting.get(target_key) else default_value

    def save_ui_setting(self):
        u"""UI情報をjson形式で保存する
        """

        setting = {}

        for key, ui in list(self.ui_setting_dict.items()):

            if isinstance(ui, type(QtWidgets.QLineEdit())):
                setting[key] = ui.text()
            elif isinstance(ui, type(QtWidgets.QSpinBox())):
                setting[key] = ui.value()
            elif isinstance(ui, type(QtWidgets.QCheckBox())):
                setting[key] = ui.isChecked()

        for key, ui in list(self.ui_setting_capture_window_dict.items()):

            if key == 'cw_pos_x':
                setting[key] = self.capture_window.pos().x()
            elif key == 'cw_pos_y':
                setting[key] = self.capture_window.pos().y()

            elif isinstance(ui, type(QtWidgets.QSpinBox())):
                setting[key] = ui.value()

        if not os.path.exists(os.path.dirname(define.UI_SETTING_JSON_PATH)):
            os.makedirs(os.path.dirname(define.UI_SETTING_JSON_PATH))

        with open(define.UI_SETTING_JSON_PATH, 'w') as f:
            json.dump(setting, f, indent=4)

    def __set_sg_project_setting(self):
        u"""ShotgridのProject設定をjsonから取得し変数に設定
        """

        self.sg_url = define.SG_URL
        self.sg_project_name = define.SG_PROJECT_NAME

        return self.sg_url and self.sg_project_name

    def __set_sg_user_setting(self):
        u"""Shotgridのユーザー情報(id/pass)を取得し変数に設定
        IDはjsonに保存されているものを読み込むか、環境変数から読む
        PassはMaya起動中は環境変数に保存されているものを読む
        """

        if os.environ.get('SG_USER'):
            self.sg_user = os.environ.get('SG_USER')
        if os.environ.get('SG_PASSWORD'):
            self.sg_password = os.environ.get('SG_PASSWORD')

        if self.sg_user and self.sg_password:
            return

        if not os.path.exists(define.SG_USER_SETTING_JSON_PATH):
            return

        with open(define.SG_USER_SETTING_JSON_PATH) as f:
            sg_account_setting = json.load(f)
            if self.sg_user != sg_account_setting.get('sg_user'):
                self.sg_user = sg_account_setting.get('sg_user')
                self.sg_password = ''

    def __set_sg_setting(self):
        u"""shotgrid周辺のセッティングを行う

        shotgridの各種設定(shotgridのURL、api用のユーザーID、パスワード)を変数にセット
        shotgridにアクセスするインスタンスを取得し変数にセット
        更にプロジェクトエンティティアセットを変数にセット

        Returns:
            bool: 全てのセットが完了すればTrue, 1つでも問題があればFalse
        """

        sg_url = self.sg_url
        sg_user = self.sg_user
        sg_password = self.sg_password

        if sg_url and isinstance(sg_url, str) is False:
            sg_url = sg_url.encode('utf-8')
        if sg_user and isinstance(sg_user, str) is False:
            sg_user = sg_user.encode('utf-8')
        if sg_password and isinstance(sg_password, str) is False:
            sg_password = sg_password.encode('utf-8')

        tmp_sg_obj = shotgrid.Shotgrid(sg_url, sg_user, sg_password)
        if not tmp_sg_obj.set_shotgrid_instance():
            return False
        self.sg_obj = tmp_sg_obj

        project_info_list = self.sg_obj.get_projects(self.sg_project_name)
        if not project_info_list:
            return False

        self.sg_project = project_info_list[0]

        for field_code in define.SG_FIELD_CODE_LIST:

            field_info = self.sg_obj.get_field_info(field_code)
            if not field_info:
                continue

            field_name = None
            if sys.version_info.major == 2:
                field_name = field_info[field_code]['name']['value'].decode('utf-8')
            else:
                field_name = field_info[field_code]['name']['value']

            self.sg_field_set_list.append(
                {
                    'field_code': field_code,
                    'field_name': field_name
                })

        return True

    def show_login_dialog(self):
        u"""ログインID、パスワード入力用のダイアログを表示
        """

        self.login_dialog.ui.sg_user_line.setText(self.sg_user)
        self.login_dialog.ui.sg_password_line.setText(self.sg_password)

        self.login_dialog.show()

    def set_sg_account_info_for_dialog(self):
        u"""ログイン用ダイアログに入力した情報を利用してShotgrid周辺のセッティングを行う
        """

        account = self.login_dialog.ui.sg_user_line.text()
        password = self.login_dialog.ui.sg_password_line.text()

        if account == '' or password == '':
            QtWidgets.QMessageBox().warning(None, 'Warning', u'メールアドレスまたはpasswordが空欄です')
            self.show_login_dialog()
            return

        self.sg_user = account
        self.sg_password = password

        self.is_sg_setting_setup_finished = self.__set_sg_setting()
        if self.is_sg_setting_setup_finished:

            QtWidgets.QMessageBox().information(None, 'Information', u'Shotgridのログインに成功しました')

            os.environ['SG_USER'] = self.sg_user
            os.environ['SG_PASSWORD'] = self.sg_password

            # user_idをjsonに保存
            if not os.path.exists(os.path.dirname(define.SG_USER_SETTING_JSON_PATH)):
                os.makedirs(os.path.dirname(define.SG_USER_SETTING_JSON_PATH))
            with open(define.SG_USER_SETTING_JSON_PATH, 'w') as f:
                json.dump({'sg_user': self.sg_user}, f, indent=4)

        # アセットビューを更新
        self.update_asset_data_view()

    def __get_sg_asset_data_for_scene(self):
        u"""シーンに対応する「作成済みかどうかのフラグ値/Shotgrid用の初期値/Shotgridアセット情報」をセットした辞書を取得する
        辞書の中は
        {
            'is_create': bool アセットが作成済みかどうかを判別
            'asset': dict 既にアセットが存在する場合のアセット情報の辞書
            'asset_name': string シーン名から取得したshotgrid用のアセット名
            'sg_setting': dict sshotgrid用のアセット一致判定と新規作成に用いる情報の入った辞書
        }

        Returns:
            dict:
        """

        sg_asset_data = {'is_create': False, 'asset': None, 'asset_name': None, 'sg_setting': None}

        sg_setting = self.__get_sg_setting()
        if not sg_setting:
            return sg_asset_data

        sg_asset_data['sg_setting'] = sg_setting
        asset_name = sg_setting['code']

        sg_asset_data['asset_name'] = asset_name

        assets = self.sg_obj.get_entity(asset_name, self.sg_project, set_all_field=True)
        for asset in assets:

            code = asset.get('code')

            if not code or code != asset_name:
                continue

            for target in sg_setting['specific_target_list']:

                field = target.get('field')
                field_item = target.get('field_item')

                if field not in asset:
                    break

                if not field_item and not asset.get(field):
                    continue

                asset_field_item = asset.get(field)
                if sys.version_info.major == 2:
                    asset_field_item = asset_field_item.decode('utf-8') if asset_field_item else asset_field_item
                else:
                    asset_field_item = asset_field_item if asset_field_item else asset_field_item
                if field_item != asset_field_item:
                    break

            else:

                for key, item in list(asset.items()):
                    if sys.version_info.major == 2:
                        asset[key] = item.decode('utf-8') if isinstance(item, str) else item
                    else:
                        asset[key] = item if isinstance(item, str) else item
                sg_asset_data['asset'] = asset
                break

        else:

            sg_asset_data['is_create'] = True

        return sg_asset_data

    def __get_sg_setting(self):
        u"""shotgrid用のアセット一致判定と新規作成に用いる情報の入った辞書を取得する

        Returns:
            dict: shotgrid用のアセット一致判定と新規作成に用いる情報の入った辞書
        """

        sg_setting = self.sg_asset_default_setting.get_scene_sg_asset_default_setting()
        if not sg_setting:
            return None

        # taskTemplate名からtaskTamplateEntityを取得してfield_itemを更新
        # 無ければtaskTemplateをtarget_listから除外
        task_template_delete_target = None
        for target in sg_setting['target_list']:
            if target.get('field') == 'task_template':
                task_template_name = target.get('field_item')
                if not task_template_name:
                    break

                template = self.sg_obj.get_entity(task_template_name, entity_type='TaskTemplate', get_one=True)
                if template:
                    target['field_item'] = template
                else:
                    task_template_delete_target = target

                break

        if task_template_delete_target:
            sg_setting['target_list'].remove(task_template_delete_target)

        return sg_setting

    def set_target_type_obj_to_ui(self, target_type, target_ui):
        u"""対象のUIに対象のタイプのオブジェクト名をセット

        Args:
            target_type (type): 対象の型
            target_ui (Qtwidget): 値をセットするUI
        """

        obj = Util.get_target_type_obj_in_selection(target_type)
        if not obj:
            return

        target_ui.setText(obj)

    def set_target_dir_to_ui(self, target_ui):
        u"""対象のUIにファイルダイアログで選択したフォルダ名をセット

        Args:
            target_ui (Qtwidget): 値をセットするUI
        """

        target_dir = Util.get_dir()
        if not target_dir:
            return

        target_ui.setText(target_dir)

    def open_target_dir_for_ui(self, target_ui):
        u"""対象のUIからフォルダ名を取得し、開く

        Args:
            target_ui (Qtwidget): 値を取得するUI
        """

        target_dir = target_ui.text()
        Util.open_dir(target_dir)

    def setup_scene_reload_scriptjob(self):
        u"""シーンが読み込まれたときに実行されるスクリプトジョブを設定
        """

        Util.set_script_job('SceneOpened', self.update_asset_data_view, self.view.objectName())

    def check_fin_setup_decorator(func):
        u"""セッティング周りの読み込みが完了しているかを取得するデコレータ
        """

        def check_fin_setup(self, *args, **kwargs):

            if not self.is_setting_setup_finished:
                QtWidgets.QMessageBox().warning(None, 'Warning', u'settingを取得できませんでした')
                return None

            if not self.is_sg_setting_setup_finished:
                QtWidgets.QMessageBox().warning(None, 'Warning', u'Shotgridにログインできませんでした')
                self.view.ui.sg_asset_data_view.setPlainText('Shotgridにログインしていません')
                self.show_login_dialog()
                return None

            return func(self, *args, **kwargs)

        return check_fin_setup

    @check_fin_setup_decorator
    def register_playblast_movie(self):
        u"""playblastを指定のカメラで撮影し、shotgridに登録するボタンイベント
        """

        target_dir = self.view.ui.target_dir_line.text()
        pb_width = self.view.ui.pb_width_spinbox.value()
        pb_height = self.view.ui.pb_height_spinbox.value()
        pb_is_remove_org_avi = not self.view.ui.pb_is_remove_org_avi.isChecked()
        pb_is_should_view_mp4 = self.view.ui.pb_is_should_view_mp4.isChecked()

        if not target_dir or not os.path.exists(target_dir):
            QtWidgets.QMessageBox().warning(None, 'Warning', u'保存/読み込み用フォルダが未入力か、存在しませんでした')
            return

        pb_panel = Util.get_focus_model_panel()
        if pb_panel is None:
            QtWidgets.QMessageBox().warning(None, 'Warning', u'直前にfocusされたUIが対象ではありませんでした')
            return

        if not pb_panel:
            QtWidgets.QMessageBox().warning(None, 'Warning', u'対象のPanelが未入力でした')
            return

        scene_name = Util.get_scene_name()
        if not scene_name:
            QtWidgets.QMessageBox().warning(None, 'Warning', u'シーン名が取得できませんでした')
            return

        scene_short_name_without_ext = os.path.splitext(os.path.basename(scene_name))[0]
        mp4_path = os.path.join(target_dir, '{}.mp4'.format(scene_short_name_without_ext))

        # playBlast撮影とmp4圧縮
        if not exec_playblast.ExecPlayblast().exec_playblast(
            dir_path=target_dir,
            width=pb_width,
            height=pb_height,
            remove_org_avi=pb_is_remove_org_avi,
            should_view_mp4=pb_is_should_view_mp4,
            target_panel=pb_panel
        ):
            QtWidgets.QMessageBox().warning(None, 'Warning', u'PlayBlastの撮影に失敗しました')
            return

        # Shotgridに登録

        if self.register_asset(mp4_path):
            QtWidgets.QMessageBox().information(None, 'Information', u'処理が完了しました。')
        else:
            QtWidgets.QMessageBox().warning(None, 'Warning', u'Shotgrid登録に失敗しました')

        self.update_asset_data_view()

    @check_fin_setup_decorator
    def register_screenshot(self):
        u"""スクリーンショットを撮影し、shotgridに登録するボタンイベント
        """

        target_dir = self.view.ui.target_dir_line.text()
        if not target_dir or not os.path.exists(target_dir):
            QtWidgets.QMessageBox().warning(None, 'Warning', u'保存/読み込み用フォルダが未入力か、存在しませんでした')
            return

        scene_name = Util.get_scene_name()
        if not scene_name:
            QtWidgets.QMessageBox().warning(None, 'Warning', u'シーン名が取得できませんでした')
            return

        target_path = os.path.join(target_dir, 'screenshot_capture.png')

        pos_x = self.capture_window.pos().x()
        pos_y = self.capture_window.pos().y()
        size_w = self.capture_window.size().width()
        size_h = self.capture_window.size().height()

        self.save_ui_setting()

        self.capture_window.close()

        ssc = screenshot_capture.ScreenshotCapture()
        if not ssc.screenshot_capture(pos_x, pos_y, size_w, size_h, target_path):
            QtWidgets.QMessageBox().warning(None, 'Warning', u'キャプチャーに失敗しました')
            return

        # Shotgridに登録
        if self.register_asset(target_path):
            QtWidgets.QMessageBox().information(None, 'Information', u'処理が完了しました。')
        else:
            QtWidgets.QMessageBox().warning(None, 'Warning', u'Shotgrid登録に失敗しました')

        self.update_asset_data_view()

    @check_fin_setup_decorator
    def register_new_asset(self):
        u"""新規アセットをshotgridに登録するボタンイベント
        """

        self.register_asset(None, True)

        QtWidgets.QMessageBox().information(None, 'Information', u'処理が完了しました。')

        self.update_asset_data_view()

    @check_fin_setup_decorator
    def register_asset(self, target_path, create_only=False):
        u"""shotgridにアセットの新規登録/更新を行う

        Args:
            target_path (string): アップロードするサムネイル用画像/動画のフルパス
            create_only (bool): アセット新規登録のみ行うかどうか

        Returns:
            bool: 新規作成or更新が完了したらTrue、何らかの理由で異常終了したらFalse
        """

        sg_asset_data = self.__get_sg_asset_data_for_scene()

        version_data = None
        target_asset = None

        # 作成メソッド
        if sg_asset_data.get('is_create'):

            asset_data = {}
            message = u'{}\n{}\n{}\n'.format(
                u'以下のアセットを新規作成します\n宜しければ「OK」を押してください',
                u'-' * 20,
                u'アセット名\t: {}'.format(sg_asset_data.get('asset_name'))
            )
            if sg_asset_data['sg_setting'] and sg_asset_data['sg_setting'].get('target_list'):
                for target in sg_asset_data['sg_setting'].get('target_list'):
                    for sg_field_set in self.sg_field_set_list:
                        if target.get('field') == sg_field_set.get('field_code'):
                            field_item = target.get('field_item')
                            if isinstance(field_item, dict) and field_item.get('code'):
                                field_item = field_item.get('code')
                            message += (u'{}\t: {}\n'.format(sg_field_set.get('field_name'), field_item))
                            break
                    asset_data.update({target.get('field'): target.get('field_item')})

            result = QtWidgets.QMessageBox.question(None, 'Question', message, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)
            if result == QtWidgets.QMessageBox.Cancel:
                return True

            # sg_asset_dataから必要要素を抜き出してassetのdataを作る
            target_asset = self.sg_obj.create_asset(sg_asset_data.get('asset_name'), self.sg_project, asset_data)
            version_data = {'sg_versions': []}

            if create_only:
                QtWidgets.QMessageBox().information(None, 'Information', u'Shotgridへのアセット登録が完了しました')
                return True

        # 更新メソッド
        elif sg_asset_data.get('asset'):

            if create_only:
                QtWidgets.QMessageBox().information(None, 'Information', u'Shotgridにアセットが既に存在する為、\n処理をスキップしました')
                return True

            message = u'既にあるアセットに上書きします\n宜しければ「OK」を押してください'
            result = QtWidgets.QMessageBox.question(None, 'Question', message, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)
            if result == QtWidgets.QMessageBox.Cancel:
                return True

            target_asset = sg_asset_data.get('asset')
            version_data = {'sg_versions': target_asset.get('sg_versions')}

        else:
            QtWidgets.QMessageBox().warning(None, 'Warning', u'対象の設定が見つかりませんでした')
            return True

        if not target_path:
            return False

        # versionアセットを作成する
        version = self.sg_obj.create_asset('new version asset', self.sg_project, {}, entity_type='Version')
        # 取得したversionアセットのIdでcodeを書き直す
        version = self.sg_obj.update_asset(version, {'code': 'New Version {}'.format(str(version.get('id')))})
        # サムネイルをアップロードする
        self.sg_obj.upload_file(version, target_path)

        version_data['sg_versions'].append(
            {'type': version.get('type'), 'id': version.get('id'), 'name': version.get('code')})
        target_asset = self.sg_obj.update_asset(target_asset, version_data)

        return target_asset is not None

    @check_fin_setup_decorator
    def update_asset_data_view(self):
        u"""現在開いているシーンのshotgridのアセット状況が表示されるUI(asset_data_view)を更新する
        """

        print(u'# information: reset_asset_data_view 実行中')

        export_str = ''

        sg_asset_data = self.__get_sg_asset_data_for_scene()
        asset = sg_asset_data.get('asset')
        if asset:
            for sg_field_set in self.sg_field_set_list:
                asset_value = ''
                field_code = sg_field_set.get('field_code')
                field_name = sg_field_set.get('field_name')
                if asset.get(field_code):
                    asset_value = asset.get(field_code)
                    if isinstance(asset_value, dict) and asset_value.get('name'):
                        asset_value = asset_value.get('name')

                export_str += u'{}\t: {}\n'.format(field_name, asset_value)
        else:
            export_str = u'SGアセットが読み込めませんでした'

        self.view.ui.sg_asset_data_view.setPlainText(export_str)
