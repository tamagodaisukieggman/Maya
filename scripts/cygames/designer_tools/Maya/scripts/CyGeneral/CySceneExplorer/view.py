# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

from PySide2 import QtWidgets, QtGui, QtCore
from maya.app.general import mayaMixin

from .ui import cy_scene_explorer_gui
from .ui import collection_file_widget
from .ui import setting_dialog
from . import utility

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(cy_scene_explorer_gui)
reload(collection_file_widget)
reload(setting_dialog)


# アイコン
ICON_SET_ROOT = QtGui.QPixmap(utility.get_icon_path('set_root.png'))
ICON_RELOAD = QtGui.QPixmap(utility.get_icon_path('reload.png'))
ICON_UP = QtGui.QPixmap(utility.get_icon_path('up.png'))
ICON_DOWN = QtGui.QPixmap(utility.get_icon_path('down.png'))
ICON_ADD = QtGui.QPixmap(utility.get_icon_path('plus.png'))
ICON_ADD_DARK = QtGui.QPixmap(utility.get_icon_path('plus_dark.png'))
ICON_DEL = QtGui.QPixmap(utility.get_icon_path('delete.png'))
ICON_DEL_DARK = QtGui.QPixmap(utility.get_icon_path('delete_dark.png'))
ICON_CLIPBOARD = QtGui.QPixmap(utility.get_icon_path('clipboard.png'))
ICON_DEL_LINE = QtGui.QPixmap(utility.get_icon_path('delete_line.png'))
ICON_PAINT = QtGui.QPixmap(utility.get_icon_path('paint.png'))
ICON_PAINT_DARK = QtGui.QPixmap(utility.get_icon_path('paint_dark.png'))
ICON_PEN = QtGui.QPixmap(utility.get_icon_path('pen.png'))
ICON_PEN_DARK = QtGui.QPixmap(utility.get_icon_path('pen_dark.png'))

ICON_MAYA = QtGui.QPixmap(utility.get_icon_path('maya.png'))
ICON_FBX = QtGui.QPixmap(utility.get_icon_path('fbx.png'))
ICON_FILE = QtGui.QPixmap(utility.get_icon_path('file.png'))
ICON_FOLDER = QtGui.QPixmap(utility.get_icon_path('folder.png'))


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """メインウインドウ
    """

    def __init__(self, root, parent=None):
        super(View, self).__init__(parent)

        self.root = root
        self.ui = cy_scene_explorer_gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setStyleSheet('QToolTip { color: #ffffff; background-color: #000000; border: 0px; }')

        self.ui.set_root_button.setIcon(ICON_SET_ROOT)
        self.ui.update_button.setIcon(ICON_RELOAD)
        self.ui.up_button.setIcon(ICON_UP)
        self.ui.down_button.setIcon(ICON_DOWN)
        self.ui.add_button.setIcon(ICON_ADD)
        self.ui.del_button.setIcon(ICON_DEL)
        self.ui.root_dir_line.setStyleSheet('padding:3px; border-radius:6px;')
        self.ui.search_line.setStyleSheet('padding:3px; border-radius:6px;')
        self.ui.update_recent_file_button.setIcon(ICON_RELOAD)
        self.ui.copy_to_clipboard_button.setIcon(ICON_CLIPBOARD)

        color = 'color: white;'
        default_bg = 'background-color: rgb(36, 36, 36);'
        border_style = 'padding:5px; border-radius: 10px;'
        hover_style = 'QPushButton:hover{background-color: rgb(96, 96, 96);}'
        load_save_button_style = 'QPushButton{%s %s %s}%s' % (color, default_bg, border_style, hover_style)

        self.ui.col_new_button.setStyleSheet(load_save_button_style)
        self.ui.col_load_button.setStyleSheet(load_save_button_style)
        self.ui.col_save_button.setStyleSheet(load_save_button_style)
        self.ui.col_save_as_button.setStyleSheet(load_save_button_style)

        self.ui.item_search_line.setStyleSheet('padding:3px; border-radius:6px;')
        self.ui.col_add_button.setIcon(ICON_ADD)
        self.ui.copy_item_to_clipboard_button.setIcon(ICON_CLIPBOARD)

        self.col_list = DragListWidget(self)
        self.col_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.col_list.setDropIndicatorShown(True)
        self.ui.col_list_layout.addWidget(self.col_list)

        self.col_file_list = DragListWidget(self)
        self.col_file_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.ui.col_file_list_layout.addWidget(self.col_file_list)

        self.clear_icon = None
        self.clear_action = None
        self.clear_event = None

        self.col_item_clear_icon = None
        self.col_item_clear_action = None
        self.col_item_clear_event = None

    def setUiSearchLine(self, clearEvent):
        """キーワード検索のテキスト入力欄をセットアップする

        Args:
            clear_event (func):削除アイコン押下時にhookする関数
        """

        self.clear_icon = ICON_DEL_LINE
        self.ui.search_line.textChanged.connect(self.OnSearchLineTextChanged)
        self.OnSearchLineTextChanged()

        self.clear_event = clearEvent

    def setColUiSearchLine(self, clearEvent):
        """キーワード検索のテキスト入力欄をセットアップする

        Args:
            clear_event (func):削除アイコン押下時にhookする関数
        """

        self.col_item_clear_icon = ICON_DEL_LINE
        self.ui.item_search_line.textChanged.connect(self.OnColItemSearchLineTextChanged)
        self.OnColItemSearchLineTextChanged()

        self.col_item_clear_event = clearEvent

    def OnSearchLineTextChanged(self):
        """キーワード検索のテキスト入力欄変更時のイベント
        """

        if self.ui.search_line and self.ui.search_line.text():
            if not self.clear_action:
                self.clear_action = self.ui.search_line.addAction(self.clear_icon, QtWidgets.QLineEdit.TrailingPosition)
                self.clear_action.triggered.connect(self._OnSearchLineClearIconClicked)
        elif self.clear_action and self.ui.search_line and not self.ui.search_line.text():
            self.ui.search_line.removeAction(self.clear_action)
            self.clear_action = None

    def OnColItemSearchLineTextChanged(self):
        """キーワード検索のテキスト入力欄変更時のイベント
        """

        if self.ui.item_search_line and self.ui.item_search_line.text():
            if not self.col_item_clear_action:
                self.col_item_clear_action = self.ui.item_search_line.addAction(self.col_item_clear_icon, QtWidgets.QLineEdit.TrailingPosition)
                self.col_item_clear_action.triggered.connect(self._OnColItemSearchLineClearIconClicked)
        elif self.col_item_clear_action and self.ui.item_search_line and not self.ui.item_search_line.text():
            self.ui.item_search_line.removeAction(self.col_item_clear_action)
            self.col_item_clear_action = None

    def _OnSearchLineClearIconClicked(self):
        """キーワード検索のテキスト入力欄の削除アイコン押下時のイベント
        """

        self.ui.search_line.clear()
        if self.clear_event:
            self.clear_event()

    def _OnColItemSearchLineClearIconClicked(self):
        """キーワード検索のテキスト入力欄の削除アイコン押下時のイベント
        """

        self.ui.item_search_line.clear()
        if self.col_item_clear_event:
            self.col_item_clear_event()

    def closeEvent(self, event):
        """ウインドウを閉じるときの処理
        """

        accept_to_proceed = self.saveCollectionConfirm()

        # キャンセルされたら終了イベント自体を無視する
        if not accept_to_proceed:
            event.ignore()
            return

        super(View, self).closeEvent(event)

        self.saveRootSetting()

    def saveRootSetting(self):
        """ツール設定を保存する
        """

        if self.root:
            self.root.save_setting()

    def saveCollectionConfirm(self):
        """コレクション設定を保存する

        Returns:
            bool: 処理を進行するか
        """

        if self.root:

            # コレクションの保存確認
            if self.root.collection_tab.is_dirty:

                result = self.root.collection_tab.col_save_confirm_event()
                if result == 'Save':
                    self.root.collection_tab.col_save_event()
                elif result == 'Cancel':
                    return False

        return True


class DragListWidget(QtWidgets.QListWidget):
    """ドラッグで並び替えられるリストウィジェット
    InternalMoveを設定しただけだと特定条件でアイテムが消える不具合があったためdragMoveEventをオーバーライドして対応した
    """

    def __init__(self, parent):
        super(DragListWidget, self).__init__(parent)

        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(False)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.setAcceptDrops(True)
        self.setAlternatingRowColors(True)
        self.setDropIndicatorShown(True)

        self.dropIndicatorRect = QtCore.QRect()

    def dragMoveEvent(self, event):

        target = self.row(self.itemAt(event.pos()))
        current = self.currentRow()
        if target == current + 1 or (current == self.count() - 1 and target == -1):
            event.ignore()
        else:
            super(DragListWidget, self).dragMoveEvent(event)


class SettingDialog(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QDialog):
    """設定ダイアログ
    """

    def __init__(self, parent):
        super(SettingDialog, self).__init__(parent)
        self.setParent(parent)
        self.ui = setting_dialog.Ui_Dialog()
        self.ui.setupUi(self)


class ColObjDelConfirmDialog(QtWidgets.QDialog):
    """設定ダイアログ
    """

    def __init__(self, parent):
        super(ColObjDelConfirmDialog, self).__init__(parent)
        self.setParent(parent)
        self.set_ui()
        self.set_event()
    
    def set_ui(self):

        self.setModal(True)
        v_layout = QtWidgets.QVBoxLayout(self)

        message_label = QtWidgets.QLabel('削除してもよろしいですか？')
        v_layout.addWidget(message_label)

        button_layout = QtWidgets.QHBoxLayout()
        v_layout.addLayout(button_layout)

        self.ok_button = QtWidgets.QPushButton()
        self.ok_button.setText('YES')
        button_layout.addWidget(self.ok_button)

        self.ng_button = QtWidgets.QPushButton()
        self.ng_button.setText('NO')
        button_layout.addWidget(self.ng_button)

        self.never_show_again_check = QtWidgets.QCheckBox()
        self.never_show_again_check.setText('次回から削除確認をしない')
        v_layout.addWidget(self.never_show_again_check)
    
    def set_event(self):

        self.ok_button.clicked.connect(self.accept)
        self.ng_button.clicked.connect(self.reject)


class BookmarkListItemWidget(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):
    """ブックマークリストアイテムのカスタムウィジェット
    """

    def __init__(self, path='', parent=None):

        super(BookmarkListItemWidget, self).__init__(parent)

        self.path = path

        self.setUi()

    def setUi(self):
        """UIの設定
        """

        self.setToolTip(self.path)

        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setSpacing(0)

        ext = os.path.splitext(self.path)[-1]
        icon = None

        if ext:
            if ext == '.ma' or ext == '.mb':
                icon = ICON_MAYA
            elif ext == '.fbx':
                icon = ICON_FBX
            else:
                icon = ICON_FILE
        else:
            icon = ICON_FOLDER

        self.folderIcon = QtWidgets.QLabel()

        self.folderIcon.setPixmap(icon)
        self.folderIcon.setScaledContents(True)
        self.folderIcon.setMaximumSize(QtCore.QSize(16, 16))

        self.pathLabel = QtWidgets.QLabel()
        text = os.path.basename(self.path)
        if text == '':  # ドライブを指定した場合basenameが空になる
            text = self.path
        self.pathLabel.setText(text)

        horizontalLayout.addWidget(self.folderIcon)
        horizontalLayout.addWidget(self.pathLabel)

        self.setLayout(horizontalLayout)


class CollectionWidget(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):
    """コレクションのカスタムウィジェット
    """

    # シグナル
    change_collection_name = QtCore.Signal(str)
    change_color = QtCore.Signal(str)
    add_collection_item = QtCore.Signal(str)
    del_collection = QtCore.Signal(str)

    def __init__(self, id='', name='', col_color=[0, 0, 0], parent=None):

        super(CollectionWidget, self).__init__(parent)

        self.col_id = id
        self.col_color = col_color
        self.name = name
        self.is_active = False

        self.set_ui()
        self.set_up_widget_event()

    def set_ui(self):
        """UIの設定
        """

        root_layout = QtWidgets.QHBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.color_button = QtWidgets.QPushButton()
        self.color_button.setMaximumWidth(20)
        self.color_button.setMinimumHeight(50)
        self.color_button.setToolTip('ラベル色を変更')
        self.color_button.setIcon(ICON_PAINT)
        root_layout.addWidget(self.color_button)

        self.frame = QtWidgets.QFrame()
        self.frame.setMinimumHeight(50)
        self.frame.setStyleSheet('background-color: rgb(0, 0, 0);')
        root_layout.addWidget(self.frame)

        inner_layout = QtWidgets.QHBoxLayout()
        inner_layout.setContentsMargins(20, 0, 20, 0)
        inner_layout.setSpacing(6)
        self.frame.setLayout(inner_layout)

        self.name_icon_button = QtWidgets.QPushButton()
        self.name_icon_button.setIcon(ICON_PEN)
        self.name_icon_button.setToolTip('名前を編集')
        self.name_icon_button.setFlat(True)
        self.name_icon_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed))
        inner_layout.addWidget(self.name_icon_button)

        font = QtGui.QFont()
        font.setPointSize(9)
        self.name_label = QtWidgets.QLabel()
        self.name_label.setFont(font)
        self.name_label.setText(self.name)
        self.name_label.setToolTip('ダブルクリックで名前を編集')
        inner_layout.addWidget(self.name_label)

        self.add_item_button = QtWidgets.QPushButton()
        self.add_item_button.setIcon(ICON_ADD)
        self.add_item_button.setText('シーン追加')
        self.add_item_button.setFlat(True)
        self.add_item_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed))
        inner_layout.addWidget(self.add_item_button)

        self.del_button = QtWidgets.QPushButton()
        self.del_button.setIcon(ICON_DEL)
        self.del_button.setFlat(True)
        self.del_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed))
        inner_layout.addWidget(self.del_button)

        self.setLayout(root_layout)
        self.set_color()

    def set_up_widget_event(self):

        self.name_icon_button.clicked.connect(self.change_name_event)
        self.color_button.clicked.connect(self.change_color_event)
        self.add_item_button.clicked.connect(self.add_item_event)
        self.del_button.clicked.connect(self.delete_collection_event)

    def set_color(self, rgb=None):
        """カラーをセット

        Args:
            rgb (list, optional): カラー. Defaults to None.
        """

        if rgb:
            self.col_color = rgb
        self.update_fore_col()
        self.update_bg_col()

    def update_bg_col(self):
        """背景色の更新
        """

        # ボタンは常に色を乗せる
        self.color_button.setStyleSheet(
            'background-color: rgb({0}, {1}, {2});'.format(self.col_color[0], self.col_color[1], self.col_color[2])
        )

        # ボディは選択時のみ
        # rgb = self.col_color if self.is_active else [0, 0, 0]

        if self.is_active:
            self.frame.setStyleSheet(
                'background-color: rgb({0}, {1}, {2});'.format(self.col_color[0], self.col_color[1], self.col_color[2])
            )
        else:
            self.frame.setStyleSheet('')

    def update_fore_col(self):
        """文字やアイコン色の更新
        """

        q_col = QtGui.QColor(self.col_color[0], self.col_color[1], self.col_color[2])
        value = q_col.valueF()

        is_color_icon_dark = value > 0.5
        if is_color_icon_dark:
            self.color_button.setIcon(ICON_PAINT_DARK)
        else:
            self.color_button.setIcon(ICON_PAINT)

        # 背景色の明るさで明暗を決める
        is_fore_dark = value > 0.5 and self.is_active
        rgb = [10, 10, 10] if is_fore_dark else [245, 245, 245]

        self.name_label.setStyleSheet('color: rgb({0}, {1}, {2});'.format(rgb[0], rgb[1], rgb[2]))
        self.add_item_button.setStyleSheet('color: rgb({0}, {1}, {2});'.format(rgb[0], rgb[1], rgb[2]))
        self.del_button.setStyleSheet('color: rgb({0}, {1}, {2});'.format(rgb[0], rgb[1], rgb[2]))

        if is_fore_dark:
            self.name_icon_button.setIcon(ICON_PEN_DARK)
            self.add_item_button.setIcon(ICON_ADD_DARK)
            self.del_button.setIcon(ICON_DEL_DARK)
        else:
            self.name_icon_button.setIcon(ICON_PEN)
            self.add_item_button.setIcon(ICON_ADD)
            self.del_button.setIcon(ICON_DEL)

    def change_name_event(self):
        """名前変更シグナルを発火
        """

        self.change_collection_name.emit(self.col_id)

    def change_color_event(self):
        """色変更シグナルを発火
        """

        self.change_color.emit(self.col_id)

    def add_item_event(self):
        """アイテム追加イベントを発火
        """

        self.add_collection_item.emit(self.col_id)

    def delete_collection_event(self):
        """コレクション削除イベントを発火
        """

        self.del_collection.emit(self.col_id)


class CollectionFileItemWidget(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):

    change_collection_desc = QtCore.Signal(str)
    delete_collection_item = QtCore.Signal(str)

    def __init__(self, item_id, path, desc, bg_col=[0, 0, 0], parent=None):

        super(CollectionFileItemWidget, self).__init__(parent)

        self.ui = collection_file_widget.Ui_Form()
        self.ui.setupUi(self)

        self.item_id = item_id
        self.path = path
        self.exists = os.path.exists(self.path)
        self.desc = desc
        self.col_color = bg_col

        self.set_ui()
        self.set_up_widget_event()

    def set_ui(self):
        """UIの設定
        """

        self.setToolTip(self.path)

        self.ui.col_frame.setStyleSheet(
            'background-color: rgb({0}, {1}, {2});'.format(self.col_color[0], self.col_color[1], self.col_color[2])
        )

        self.ui.name_label.setText(os.path.basename(self.path))
        self.ui.desc_icon_button.setIcon(ICON_PEN)
        self.ui.desc_icon_button.setToolTip('説明を編集')
        self.ui.desc_label.setText(self.desc)

        if not self.exists:
            self.ui.file_info_label.setText('(No File)')

        self.ui.col_item_del_button.setIcon(ICON_DEL)

    def set_up_widget_event(self):

        self.ui.desc_icon_button.clicked.connect(self.change_description)
        self.ui.col_item_del_button.clicked.connect(self.delete_col_item_event)

    def change_description(self):
        """説明文変更イベントを発火
        """

        self.change_collection_desc.emit(self.item_id)

    def delete_col_item_event(self):
        """アイテム削除イベントを発火
        """

        self.delete_collection_item.emit(self.item_id)


class DragItemFilter(QtCore.QObject):
    """アイテムドラッグを検知するフィルター
    """

    drop_item = QtCore.Signal()

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.ChildRemoved:
            self.drop_item.emit()

        return False
