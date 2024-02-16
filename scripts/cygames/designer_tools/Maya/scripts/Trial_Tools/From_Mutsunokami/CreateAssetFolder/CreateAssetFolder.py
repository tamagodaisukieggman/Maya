# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
import subprocess
from maya import cmds
import pymel.core as pm
from functools import partial
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin
from yaml import safe_dump
from ui_CreateAssetFolder import Ui_Form  # Mayaの画面の後ろに行かないように

#from tatool.config import Config, get_config_path, get_config_file

TITLE = u"Create_Asset_Folder"
SETTING_FILE = u"user_settings"
EXT_YAML = u".yaml"
SUCCESS_MESSAGE = u"作成が完了しました。"
ALREADY_EXISTS_MESSAGE = u"既にサブフォルダが存在します。 \n 作成を終了します。"
NO_DIRECTORY_MESSAGE = u"ディレクトリが指定されていません。 \n 1) の設定を見直してください。"
NO_ASSET_FOLDER_NAME_MESSAGE = u"アセットフォルダ名が指定されていません。 \n 2) の設定を見直してください。"
LOAD_CONFIG_FAILD = u"設定ファイルのロードに失敗しました。 \n 処理を中断しました。"
NOT_FOUND_PROJECT_WORK_ASSET_PATH = u"フォルダが見つかりませんでした。 \n 処理を中断しました。"

# ウィンドウサイズ
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 500

# ラジオボタンで選択させるルートディレクトリ
PATH = ["",
        "Resources{os.sep}3D{os.sep}Project",
        "Resources{os.sep}3D{os.sep}Props{os.sep}Model"
        ]

# ラジオボタンの判別に使用
LOCAL_FOLDER = 0
MVBG_FOLDER = 1
PROPS_FOLDER = 2

# ラジオボタンで選択されたディレクトリに対し、作成するべきサブディレクトリのindexリスト
"""
0: scene
1: sourceimages
2: Materials
3: Meshes
4: Motions
5: Prefab
6: Prefabs
7: Textures
"""
# [0]:Local, [1]MVBG, [2]Props
SUB_FOLDERS = [[0, 1, 2, 3, 4, 5, 6, 7], [2, 3, 4, 5, 7], [2, 3, 4, 6, 7]]

# フラグ判定を言語化
# FLAG_ON = 1
FLAG_OFF = 0

# ユーザーのローカルフォルダを記憶したConfigファイルの情報
KEY_CONFIG_LOCAL_FOLDER_DIRECTORY = "local_folder_directory"
KEY_CONFIG_PROJECT_WORK_FOLDER_DIRECTORY = "project_work_folder_directory"

class CreateAssetFolder(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CreateAssetFolder, self).__init__(*args, **kwargs)

        # 処理を却下したかどうかの判定
        self.is_initialized = True

        # ラジオボタンのどこを選択しているか
        self.target_type = 0

        # ユーザーの入力したローカルフォルダのディレクトリ
        self.local_dir = ""
        self.directory = ""
        self.asset_folder_name = ""
        self.project_work_dir = ""

        # configデータをロード
        #self.loaded_config_data = self.load_config_file()
        if self.is_initialized is False:
            cmds.confirmDialog(title=TITLE, message=LOAD_CONFIG_FAILD)
            return None  # ロードに失敗したら処理を終了

        # GUIを初期化
        self.setup_gui()

    def setup_gui(self):
        """
        GUIを初期化
        """
        # UIの親を作成
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.setWindowTitle("CreateAssetFolder")

        # ウィンドウサイズを固定
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # レイアウトを初期化
        self.ui = Ui_Form()
        self.ui.setupUi(self.widget)

        # ディレクトリのテキストボックスをconfigの値で初期化
        self.ui.le_local_dir.setText(self.local_dir)
        #self.ui.le_project_work_dir.setText(self.project_work_dir)

        # ローカルフォルダ設定ボタンとローカルディレクトリ選択ディレクトリを表示する処理との紐づけ
        self.ui.pb_select_local_dir.clicked.connect(self.clicked_select_local_dir)
        # projectWork設定ボタンとprojectWork選択ディレクトリを表示する処理との紐づけ
        #self.ui.pb_select_project_work_dir.clicked.connect(self.clicked_select_project_work_dir)

        # アセット名を決定するボタンの処理の紐づけ
        self.ui.pb_set_asset_name.clicked.connect(self.reflesh_directory_text)

        # ラジオボタンの選択とID（self.local_dir）を連携させる処理の紐づけ
        #self.ui.rb_local.clicked.connect(partial(self.set_target_type, 0))
        #self.ui.rb_unity_mv.clicked.connect(partial(self.set_target_type, 1))
        #self.ui.rb_unity_props.clicked.connect(partial(self.set_target_type, 2))

        # ラジオボタンをクリックしたときにサブフォルダ群を設定しなおす処理の紐づけ
        #self.ui.rb_local.clicked.connect(self.reflesh_sub_folder_list)
        #self.ui.rb_unity_mv.clicked.connect(self.reflesh_sub_folder_list)
        #self.ui.rb_unity_props.clicked.connect(self.reflesh_sub_folder_list)

        # ラジオボタンがクリックされたときにディレクトリを表示しているテキストラベルを更新する処理の紐づけ
        #self.ui.rb_local.clicked.connect(self.reflesh_directory_text)
        #self.ui.rb_unity_mv.clicked.connect(self.reflesh_directory_text)
        #self.ui.rb_unity_props.clicked.connect(self.reflesh_directory_text)

        # 選択されているディレクトリをテキストボックスで表示
        self.ui.le_export_dir.setText(self.directory)

        # 作成ボタン
        self.ui.pb_mkdir.clicked.connect(self.clicked_mkdir)

        # 表示を更新
        self.reflesh()

    def set_target_type(self, id):
        """
        どのラジオボタンが選択されているかを設定

        Args:
            id (int): ラジオボタンに割り振られた番号
        """
        if id is not self.target_type:
            self.target_type = id

    def reset_sub_folder_list(self):
        """
        サブフォルダに関するフラグとチェック項目をリセットする
        """
        # ToDo: ここでフラグを全てリセットする
        for idx in range(self.ui.lw_sub_folders.count()):

            item_flags = self.ui.lw_sub_folders.item(idx).flags()

            # EnabledフラグがONだったら
            if item_flags & QtCore.Qt.ItemIsEnabled != FLAG_OFF:
                # OFFにする
                item_flags = item_flags ^ QtCore.Qt.ItemIsEnabled

                # フラグを更新
                self.ui.lw_sub_folders.item(idx).setFlags(item_flags)  # Enable
                self.ui.lw_sub_folders.item(idx).setCheckState(QtCore.Qt.Unchecked)  # checkState

    def reflesh_sub_folder_list(self):
        """
            ユーザーのラジオ選択からサブフォルダリストを一括設定
        """

        # 一旦Enabledとチェックをリセット
        self.reset_sub_folder_list()

        # 全ての項目のEnabledとsetCheckedをOFFにしたので、必要なフラグだけ立てる
        for idx in SUB_FOLDERS[self.target_type]:
            # print("idx is {}".format(idx))
            item_flags = self.ui.lw_sub_folders.item(idx).flags()

            # フラグをチェックし
            # ItemIsEnabled: リスト項目を選択できるか
            # 初期化してOFFになっているはずなので
            if item_flags & QtCore.Qt.ItemIsEnabled == FLAG_OFF:
                # ONにする
                item_flags = item_flags | QtCore.Qt.ItemIsEnabled

            # フラグを更新
            self.ui.lw_sub_folders.item(idx).setFlags(item_flags)  # Enable
            self.ui.lw_sub_folders.item(idx).setCheckState(QtCore.Qt.Checked)  # checkState

        # フラグを更新しただけだと反映されないので表示を更新
        self.widget.update()

        # ---

        # フラグ設定サンプル
        """
            # ONであったなら
            if item_flags & QtCore.Qt.ItemIsEnabled != 0:
                # OFFにする
                item_flags = item_flags ^ QtCore.Qt.ItemIsEnabled
            # ONでないなら
            else:
                # ONにする
                item_flags = item_flags | QtCore.Qt.ItemIsEnabled

            # 現在の状況をチェック
            if item_flags & QtCore.Qt.ItemIsEnabled != 0:
                print ("Yes")
            else:
                print ("No")

            # 0x0000 Qt::NoItemFlag
            # 0x0001 Qt::ItemIsSelectable
            # 0x0010 Qt::ItemIsEditable
            # 0x0100 Qt::ItemIsDragEnable
        """

    def clicked_select_local_dir(self):
        """
        ダイアログからユーザーがローカルディレクトリを指定
        """
        dir = pm.fileDialog2(caption="フォルダを選択",
                             fileFilter="Folder",
                             fileMode=3,
                             )
        if dir is not None:  # キャンセルされていなければ
            self.directory = dir[0].replace("/", os.sep)
            self.local_dir = self.directory  # ローカルディレクトリを再度選択した時に復帰できるよう別で保持
            self.ui.le_local_dir.setText(self.directory)  # UIのLabel上に反映
            if self.target_type is LOCAL_FOLDER:
                self.ui.le_export_dir.setText(self.local_dir)
            """
            self.create_user_dir_counfig()  # configファイルの保存
            """

    def check_project_work_asset_dir(self, dir, show_dialog=True):
        """
        選択された「_Work」ディレクトリ内に想定したアセットフォルダがあるか確認

        Args:
            dir (string)): 選択された「_Work」ディレクトリ

        Returns:
            bool: パスが見つかったかどうかの判定
        """
        for d in PATH:
            if d == "":  # ラジオボタンローカルディレクトリ用のダミーインデックスは確認対象から除外
                pass
            elif not os.path.exists("{0}{os.sep}{1}".format(dir, d)):  # MVのパスがあるか
                if show_dialog is True:
                    cmds.confirmDialog(title=TITLE, message="'{0}' {1}".format(d, NOT_FOUND_PROJECT_WORK_ASSET_PATH))
                return False
        return True

    def clicked_select_project_work_dir(self):
        """
        ダイアログからユーザーが「_Work」ディレクトリを指定

        Returns:
            string: 「_Work」のパス
        """
        dir = pm.fileDialog2(caption="_Workフォルダを選択",
                             fileFilter="Folder",
                             fileMode=3,
                             )

        if dir is not None:  # キャンセルされていなければ
            dir = dir[0].replace("/", os.sep)
            if self.check_project_work_asset_dir(dir) is False:  # アセットディレクトリが見つからなかったら中断
                return None
            else:  # 見つかったら続行
                self.directory = dir
                self.project_work_dir = self.directory  # ローカルディレクトリを再度選択した時に復帰できるよう別で保持
                self.ui.le_project_work_dir.setText(self.project_work_dir)
                self.create_user_dir_counfig()  # configファイルの保存
                return dir

    def reflesh_directory_text(self):
        """
        ラジオボタンの選択に合わせてテキストラベルで表示しているディレクトリを更新
        """
        if self.target_type is LOCAL_FOLDER:
            self.directory = self.local_dir
            self.asset_folder_name = self.ui.tl_asset_name.text()
        else:
            # UIのLabel上に反映
            self.ui.le_export_dir.setText("{0}{os.sep}{1}{os.sep}{2}".format(self.project_work_dir,
                                                                 PATH[self.target_type],
                                                                 self.ui.tl_asset_name.text()))
            self.directory = "{0}{1}".format(self.project_work_dir, PATH[self.target_type])
            self.asset_folder_name = self.ui.tl_asset_name.text()

    def reflesh(self):
        """
        リフレッシュ処理を一斉に行う
        """
        self.reflesh_sub_folder_list()
        self.reflesh_directory_text()

    def create_user_dir_counfig(self):
        """
        ユーザーの設定したディレクトリを記述したconfigファイルを作成して保存
        """
        #self.my_config = Config(TITLE, SETTING_FILE, True)
        #self.my_config.data = {KEY_CONFIG_LOCAL_FOLDER_DIRECTORY: self.local_dir,
        #                       KEY_CONFIG_PROJECT_WORK_FOLDER_DIRECTORY: self.project_work_dir}
        #self.my_config.save()
        return

    def load_config_file(self):
        """
        ユーザーの設定ファイルを読み込み

        Returns:
            None: 取得に失敗した場合
        """
        # Configファイルを読み込み
        self.my_config = Config(TITLE, SETTING_FILE, True)

        self.config_file = get_config_file(TITLE, "{0}{1}".format(SETTING_FILE, EXT_YAML))
        # 設定ファイルが存在したらローカルディレクトリの値として割り当て
        if os.path.exists(self.config_file):
            self.my_config.load()
            if type(self.my_config.data) is dict:
                if self.my_config.data.get(KEY_CONFIG_LOCAL_FOLDER_DIRECTORY) is not None \
                        and self.my_config.data.get(KEY_CONFIG_PROJECT_WORK_FOLDER_DIRECTORY) is not None:
                    self.local_dir = self.my_config.data[KEY_CONFIG_LOCAL_FOLDER_DIRECTORY]  # ローカルフォルダ
                    if os.path.exists(self.local_dir) is False:
                        self.local_dir = ""  # 以前選択したパスが存在しなかった場合ディレクトリを空に
                    self.project_work_dir = self.my_config.data[KEY_CONFIG_PROJECT_WORK_FOLDER_DIRECTORY]  # _Work
                    if self.check_project_work_asset_dir(self.project_work_dir, False) is False:
                        self.project_work_dir = ""  # 以前選択したパスに想定したフォルダが存在しなかった場合ディレクトリを空に
                # どちらかの値が存在しなければ初期化
                else:
                    self.is_initialized = self.initialize_config()
                    if self.is_initialized is False:
                        return None
            # そもそもデータのディクショナリの形になっていない場合エラーになるので別途初期化分岐
            else:
                self.is_initialized = self.initialize_config()
                if self.is_initialized is False:
                    return None
        # 設定ファイル自体存在しなければ初期化
        else:
            self.is_initialized = self.initialize_config()
            if self.is_initialized is False:
                return None

    def clicked_mkdir(self):
        """
        ラジオボタンの選択とリストのチェックを参照してディレクトリを作成
        """
        itm = ""
        mes = ""

        if self.directory == "":  # パスは指定されているか
            mes = NO_DIRECTORY_MESSAGE
        elif self.asset_folder_name == "":  # アセットフォルダ名は入力されているか
            mes = NO_ASSET_FOLDER_NAME_MESSAGE
        else:
            for x in range(self.ui.lw_sub_folders.count()):
                itm = self.ui.lw_sub_folders.item(x)
                if str(itm.checkState()).split(".")[-1] == "Checked":  # リストからチェックが入っていたら
                    if not os.path.exists("{}{os.sep}{}{os.sep}{}".format(self.directory, self.asset_folder_name, itm.text())):
                        if self.target_type == LOCAL_FOLDER:  # ローカル指定なら
                            os.makedirs("{}{os.sep}{}{os.sep}{}".format(self.directory, self.asset_folder_name, itm.text()))
                            mes = SUCCESS_MESSAGE
                            """
                            self.create_user_dir_counfig()  # ローカルフォルダを記憶しておくためのファイルを作成
                            """
                        else:
                            os.makedirs("{0}{os.sep}{1}{os.sep}{2}{os.sep}{3}".format(self.project_work_dir,
                                                                    PATH[self.target_type],
                                                                    self.asset_folder_name,
                                                                    itm.text()))
                        mes = SUCCESS_MESSAGE
                    else:
                        mes = ALREADY_EXISTS_MESSAGE  # 既に作成しようとしているディレクトリが存在した場合
                        break

        cmds.confirmDialog(title=TITLE, message=mes)  # 結果を出力

        # チェックボックスが選択されており、作成に成功していた場合、書き出し先フォルダを開く
        if self.ui.cb_wanna_open_exported_folder.isChecked() is True \
           and mes == SUCCESS_MESSAGE:
            if self.target_type is LOCAL_FOLDER:
                subprocess.Popen(["explorer", "{0}{os.sep}{1}".format(self.directory,
                                                                self.asset_folder_name)],
                                 shell=True)
            elif self.target_type is MVBG_FOLDER or self.target_type is PROPS_FOLDER:
                subprocess.Popen(["explorer", "{0}{os.sep}{1}{os.sep}{2}".format(self.project_work_dir,
                                                                     PATH[self.target_type],
                                                                     self.asset_folder_name)],
                                 shell=True)

    def initialize_config(self):
        """
        tatool configによって生成された設定ファイルの初期化

        Returns:
            bool: 失敗するとFalseが返る
        """
        if self.project_work_dir is not None:
            self.my_config.data = {KEY_CONFIG_LOCAL_FOLDER_DIRECTORY: self.local_dir,
                                   KEY_CONFIG_PROJECT_WORK_FOLDER_DIRECTORY: self.project_work_dir}
            self.my_config.save()
        else:
            return False


def show():
    """
        windowを表示
    """

    #print("起動")

    create_asset_folder = CreateAssetFolder()

    # 初期化に失敗した（しなかった）場合終了
    if create_asset_folder.is_initialized is False:
        return

    create_asset_folder.show()

    # tatool configデバッグ用
    # config_test = ConfigTest()
    # config_test.print_out()


if __name__ == "__main__":
    show()



