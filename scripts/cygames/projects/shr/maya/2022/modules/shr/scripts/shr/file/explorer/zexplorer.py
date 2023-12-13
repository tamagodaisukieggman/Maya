import os
import re
import subprocess
import shutil
import ntpath

from PySide2.QtCore import (Qt,
    QRegExp,
    QRect,
    QPoint,
    QSize
)
from PySide2.QtWidgets import (QWidget,
    QVBoxLayout,
    QMenu,
    QAction,
    QWidgetAction,
    QLabel
)

from mtk.utils.perforce import MtkP4
from .dialog import MtkExplorerDialog, MtkExplorerPromptDialog
from .header import MtkExplorerHeader
from .view import MtkExplorerBody

from .filemodel.filemodelcolumn import MtkExplorerFileModelColumn

# shotgun
from mtk.utils.shotgun import MtkSG
from .shotgun import ShotgunStatusIconProvider

from functools import partial
import pyperclip
from mtk.utils import getCurrentSceneFilePath

try:
    import maya.cmds as cmds
    import maya.mel as mel
    if hasattr(cmds, 'about'):
        from logging import getLogger
        MODE = 'MAYA'
        #logger = MtkLog(__name__)  # enable this line to log perforce actions to the kibana tool log server.
        logger = getLogger(__name__)
    else:
        from logging import getLogger
        MODE = 'STANDALONE'
        logger = getLogger(__name__)
except ImportError:
    from logging import getLogger
    MODE = 'STANDALONE'
    logger = getLogger(__name__)

# DEBUG
"""
import logging
from logging import getLogger

import maya.cmds as cmds
import maya.mel as mel
import inspect
logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)
MODE = 'MAYA'
"""

BAT_ROOT_PATH = os.environ.get('MTK_MAYA_BAT_ROOT', '').replace(os.sep, '/')


class MtkExplorer(QWidget):

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(MtkExplorer, self).__init__(parent=kwargs.setdefault('parent', None))

        self._boot = True

        self._header = MtkExplorerHeader()
        self._body = MtkExplorerBody()

        self.bookmark = self._header.bookmark
        self.category = self._header.category
        self.sets_workspace = self._header.sets_workspace
        self.checkouts = self._header.checkouts
        self.sets_sg_task_status = self._header.sets_sg_task_status
        self.address_bar = self._header.address_bar
        self.search_box = self._body.search_box
        self.p4_status_filter_box = self._body.p4_status_filter_box

        self.dir_view = self._body.dir_view
        self.file_view = self._body.file_view

        # Maya Prefs に保存するオプション名
        self.key_bookmarks = '{}.bookmark'.format(__package__)
        self.key_category = '{}.category'.format(__package__)
        self.key_search_box = '{}.search_box'.format(__package__)
        self.key_p4_status_filter_box = '{}.p4_status_filter_box'.format(__package__)
        self.key_root_path = '{}.root_path'.format(__package__)

        if MODE == 'MAYA':
            self._export_bat = u'{}/fbxexport/motion_export_{}.bat'.format(BAT_ROOT_PATH, cmds.about(v=True))
        else:
            self._export_bat = u'{}/fbxexport/motion_export_2018.bat'.format(BAT_ROOT_PATH)

        self._setup()

        self._boot = False

        self._enable_sg = self.file_view._enable_sg

    def _setup(self):
        u"""setup"""
        self.setGeometry(QRect(QPoint(100, 100), QSize(250, 800)))
        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self._header)
        layout.addWidget(self._body)

        self._connect()

    def _bookmark_activated(self, *args):
        if not args:
            return

        text = self.bookmark.pulldown.itemText(args[0])
        self.address_bar.textbox.setText(text)

        root = u'/'.join(text.split('/')[:4])
        self.dir_view.setRootIndex(self.dir_view.model().setRootPath(root))

        categories = self.category.get_categories()
        for category in categories:
            if text.find(category) != -1:
                for i in range(self.category.pulldown.count()):
                    if self.category.pulldown.itemText(i) == category:
                        self.category.pulldown.setCurrentIndex(i)

    def category_activated(self, *args):
        # logger.debug("Category Activated")
        category = self.category.pulldown.currentText()

        root_path = self.address_bar._text
        dir_path = os.path.join(root_path, category)

        dir_path = dir_path.replace("//", "/")
        dir_path = dir_path.replace("\\", "/")

        currentPath = self.address_bar.textbox.text()

        if not os.path.exists(dir_path):
            # logger.debug("path does not exist.")
            return

        if dir_path == currentPath:
            # logger.debug("path is already set.")
            return

        # logger.debug("setting new path")

        self._body.reload(dir_path)

        index = self.dir_view.model().index(dir_path)

        self._reload_dir_text_box(dir_path)
        self._reload_dir_view(index)
        self._reload_file_view(index)
        self._reload_search_box()
        self._resize_file_view()

        if MODE == 'MAYA' and not self._boot:
            # logger.debug('Save Category')
            cmds.optionVar(sv=(self.key_category, self.category.pulldown.currentIndex()))

    def p4_status_filter_activated(self, *args):
        u"""P4 Status Filter Box Selection Changed"""
        p4_status = self.p4_status_filter_box.pulldown.currentText()

        if p4_status == 'none':
            self.file_view.proxy_model.setFilterString("")
            self._resize_file_view()
        else:
            self.file_view.proxy_model.setFilterString(p4_status)
            self._resize_file_view()

        if MODE == 'MAYA' and not self._boot:
            # logger.debug('Save P4 Status Filter')
            cmds.optionVar(sv=(self.key_p4_status_filter_box, self.p4_status_filter_box.pulldown.currentIndex()))

    def _connect(self):
        u"""Connect"""
        self.bookmark.pulldown.activated.connect(self._bookmark_activated)
        self.category.pulldown.activated.connect(self.category_activated)
        self.address_bar.textbox.textChanged.connect(self._dir_text_changed)
        self.search_box.textbox.textChanged.connect(self._search_text_changed)
        self.p4_status_filter_box.pulldown.activated.connect(self.p4_status_filter_activated)

        # ディレクトリ クリック
        self.dir_view.clicked.connect(self._dir_clicked)

        # ファイル ダブルクリック
        self.file_view.doubleClicked.connect(self._maya_file_open)

        # ファイル 右クリック
        self.dir_view.customContextMenuRequested.connect(self._dir_right_clicked)
        self.file_view.customContextMenuRequested.connect(self._file_right_clicked)

    def _exec_subprocess(self, cmd):
        u"""コマンド実行"""
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
        try:
            p.communicate()
        except Exception as e:
            p.kill()
            logger.error(e)

    def _reload_dir_view(self, index):
        u"""update dir view"""
        # logger.debug('"reload directory view')
        self.dir_view.expand(index)
        self.dir_view.setCurrentIndex(index)

    def _reload_file_view(self, index):
        u"""update file view"""
        # logger.debug('"reload file view')
        if MODE == 'MAYA':
            mel.eval('global int $g_mtk_explorer_escape;$g_mtk_explorer_escape=true;')

        # QSortFilterProxyModelのフィルターをInvalidateにする必要があります
        if self.file_view.proxy_model:
            self.file_view.proxy_model.invalidateFilter()

        section = self.file_view.horizontalHeader().sortIndicatorSection()
        order = self.file_view.horizontalHeader().sortIndicatorOrder()

        self.file_view.source_model.clear()
        dir_path = self.dir_view.model().filePath(index)
        if not self._boot:
            if not self.file_view.use_abstract_table_model:
                self.file_view.source_model.root_path = dir_path
                self.file_view.source_model.set_cells()
            else:
                self.file_view.source_model.load_data(dir_path)

        if self.file_view:
            self.file_view.horizontalHeader().setSortIndicator(section, order)
            self.file_view.resizeColumnsToContents()
            self.file_view.resizeRowsToContents()

    def _reload_category(self, dir_path):
        # logger.debug("reload category")
        self.category.reload(dir_path)

    def _reload_dir_text_box(self, dir_path):
        u"""update dir textbox"""
        # logger.debug('"reload directory textbox')
        self.address_bar.textbox.setText(dir_path)

    def _reload_search_box(self):
        u"""update searchbox"""
        # logger.debug('"reload searchbox')
        if not self.search_box.textbox.text():
            self.file_view.proxy_model.setFilterRegExp('')
        else:
            words = set(self.search_box.textbox.text().split(' '))
            s = '^'
            for word in words:
                if word:
                    s += '(?=.*{})'.format(word)
            self.file_view.proxy_model.setFilterRegExp(QRegExp(s))

    def reload_table_row_data(self):
        u"""アイコン表示のアップデート"""
        # logger.debug('"reload icon')
        file_name_column = MtkExplorerFileModelColumn.Name_Id()
        p4_rev_column = MtkExplorerFileModelColumn.Rev_Id()
        p4_date_column = MtkExplorerFileModelColumn.Date_Modified_Id()
        p4_status_column = MtkExplorerFileModelColumn.P4_Status_Id()
        #sg_asset_status_column = MtkExplorerFileModelColumn.SG_Asset_Status_Id()
        sg_task_column = MtkExplorerFileModelColumn.SG_Task_Id()
        #sg_task_status_column = MtkExplorerFileModelColumn.SG_Task_Status_Id()
        p4_users_column = MtkExplorerFileModelColumn.P4_Users_Id()

        file_paths = []
        asset_names = []
        dir_path = self.dir_view.model().filePath(self.dir_view.currentIndex())
        file_name_indices = self.file_view.selectionModel().selectedRows(file_name_column) #name/icon
        p4_rev_indices = self.file_view.selectionModel().selectedRows(p4_rev_column) #rev
        #p4_date_indices = self.file_view.selectionModel().selectedRows(p4_date_column ) #date
        p4_status_indices = self.file_view.selectionModel().selectedRows(p4_status_column) #p4
        sg_task_indices = self.file_view.selectionModel().selectedRows(sg_task_column) # sg task
        p4_users_indices = self.file_view.selectionModel().selectedRows(p4_users_column)

        for index in file_name_indices:
            file_name = self.file_view.source_model.itemFromIndex(self.file_view.proxy_model.mapToSource(index)).text()
            file_paths.append(u'{}/{}'.format(dir_path, file_name))

        if not file_paths:
            return

        # get the perforce statuses
        file_status = MtkP4.status_ext(file_paths)

        # get the shotgun statuses
        asset_names = [ntpath.basename(x).split(".")[0] for x in file_paths]

        sg_asset_task_dict = MtkSG.asset_task_batch(asset_names)

        for i, (file_path, status) in enumerate(file_status.items()):

            p4_status_action = status['action'] if status['action'] else 'none'
            p4_users_list = status['users']

            sg_asset_name = ntpath.basename(file_path).split(".")[0]

            new_sg_task_data = None

            if sg_asset_task_dict and sg_asset_name in sg_asset_task_dict:
                new_sg_task_data = sg_asset_task_dict[sg_asset_name]

            # legacy support for regular table model (unused)
            if not self.file_view.use_abstract_table_model:
                asset_name_item = self.file_view.source_model.itemFromIndex(self.file_view.proxy_model.mapToSource(file_name_indices[i]))
                p4_rev_item = self.file_view.source_model.itemFromIndex(self.file_view.proxy_model.mapToSource(p4_rev_indices[i]))
                #p4_date_item = self.file_view.source_model.itemFromIndex(self.file_view.proxy_model.mapToSource(p4_date_indices[i]))
                p4_status_item = self.file_view.source_model.itemFromIndex(self.file_view.proxy_model.mapToSource(p4_status_indices[i]))
                sg_task_item = self.file_view.source_model.itemFromIndex(self.file_view.proxy_model.mapToSource(sg_task_indices[i]))
                p4_users_item = self.file_view.source_model.itemFromIndex(self.file_view.proxy_model.mapToSource(p4_users_indices[i]))

                icon = self.file_view.source_model.action_icon[p4_status_action]
                rev = '{}/{}'.format(status['haveRev'], status['headRev'])
                p4_status = '{}'.format(p4_status_action)
                p4_users = '{}'.format(p4_users_list)

                if asset_name_item is not None:
                    asset_name_item.setIcon(icon)
                if p4_rev_item is not None:
                    p4_rev_item.setText(rev)
                if p4_status_item is not None:
                    p4_status_item.setText(p4_status)
                if sg_task_item is not None:
                    sg_task_item.setData(new_sg_task_data)
                if p4_users_item is not None:
                    p4_users_item.setText(p4_users)

            else:
                # new support for abstract table model (default)
                index = self.file_view.proxy_model.mapToSource(file_name_indices[i])
                row_id = index.row()
                row_data = self.file_view.source_model.get_row_data(row_id)
                if row_data is not None:
                    row_file_name = row_data[file_name_column]

                    row_p4_rev = row_data[p4_rev_column]
                    row_p4_date = row_data[p4_date_column]
                    row_p4_status = row_data[p4_status_column]
                    row_sg_task = row_data[sg_task_column]
                    row_p4_users = row_data[p4_users_column]

                    new_p4_status = p4_status_action
                    new_p4_users_list = p4_users_list
                    self.file_view.source_model.update_row_data(row_id,
                                                                row_file_name,
                                                                row_p4_rev,
                                                                row_p4_date,
                                                                new_p4_status,
                                                                new_sg_task_data,
                                                                new_p4_users_list
                                                                )

    def _resize_file_view(self):
        u"""resize file view"""
        # logger.debug('"resize file view')
        self.file_view.resizeColumnsToContents()
        self.file_view.resizeRowsToContents()

    def _dir_clicked(self, *args):
        u"""Directory Clicked"""
        # logger.debug('"Directory Clicked')
        index = self.dir_view.currentIndex()

        self._reload_dir_view(index)
        self._reload_file_view(index)
        self._reload_search_box()
        self._resize_file_view()

    def _dir_right_clicked(self, *args):
        u"""右クリック"""
        # logger.debug('Standalone: Dir Right Clicked')
        point = args[0]

        menu = QMenu()

        perforceSectionLabel = QLabel()
        mtkSectionLabel = QLabel()
        mayaSectionLabel = QLabel()

        perforceSectionLabel.setTextFormat(Qt.RichText)
        mtkSectionLabel.setTextFormat(Qt.RichText)
        mayaSectionLabel.setTextFormat(Qt.RichText)

        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        base_path = base_path.replace('\\', '/')

        perforce_icon_path = ('{}/images/perforce/perforce_p4_icon.png'.format(base_path))
        mtk_icon_path = ('{}/images/mtk/mtk_icon.png'.format(base_path))
        maya_icon_path = ('{}/images/maya/maya_2018_icon.png'.format(base_path))

        icon_size = 24
        perforceHtml = r"<img src='{0}' width='{1}' height='{2}'> ".format(perforce_icon_path, icon_size, icon_size)
        mtkHtml = r"<img src='{0}' width='{1}' height='{2}'> ".format(mtk_icon_path, icon_size, icon_size)
        mayaHtml = r"<img src='{0}' width='{1}' height='{2}'> ".format(maya_icon_path, icon_size, icon_size)

        perforceSectionLabel.setText(perforceHtml + "Perforce".format(perforce_icon_path))
        mtkSectionLabel.setText(mtkHtml + "Mtk".format(mtk_icon_path))
        mayaSectionLabel.setText(mayaHtml + "Maya".format(maya_icon_path))

        perforceSection = QWidgetAction(menu)
        mtkSection = QWidgetAction(menu)
        mayaSection = QWidgetAction(menu)

        perforceSection.setDefaultWidget(perforceSectionLabel)
        mtkSection.setDefaultWidget(mtkSectionLabel)
        mayaSection.setDefaultWidget(mayaSectionLabel)

        # perforce menu actions
        action_func_standalone = [
            (perforceSection, self._no_function),
            (QAction(u'最新リビジョンを取得', self.dir_view), self._p4_sync_dir),
        ]

        # mtk menu actions
        action_func_mtk = [
            (mtkSection, self._no_function),
            (QAction(u'ブックマークを追加', self.dir_view), self._add_bookmark),
            (QAction(u'', self.dir_view), None),
            (QAction(u'ブックマークから削除', self.dir_view), self._delete_bookmark),
            (QAction(u'', self.dir_view), None),
            (QAction(u'エクスプローラで表示', self.dir_view), self._show_explorer),
            (QAction(u'', self.dir_view), None),
            (QAction(u'Export (Motion)', self), self._maya_export_motion_dir),
        ]

        # maya menu actions
        action_func_for_maya = [
            (mayaSection, self._no_function),
            #(QAction(u'', self.dir_view), None),
            (QAction(u'現在のシーンを選択フォルダへ保存...', self.dir_view), self._save_current_scene_to_selection_dir),
        ]

        action_func = action_func_standalone + action_func_mtk

        if MODE == 'MAYA':
            action_func = action_func + action_func_for_maya

        for action, func in action_func:
            if action:
                menu.addAction(action)
            if func:
                action.triggered.connect(func, Qt.UniqueConnection)
            else:
                action.setSeparator(True)

        menu.exec_(self.dir_view.mapToGlobal(point))

    def _file_right_clicked(self, *args):
        u"""ファイル右クリック"""
        # logger.debug('File Right Click')
        point = args[0]

        menu = QMenu()

        perforceSectionLabel = QLabel()
        shotgunSectionLabel = QLabel()
        mayaSectionLabel = QLabel()
        winfileSectionLabel = QLabel()

        #perforceSectionLabel.setAlignment(Qt.AlignCenter)
        #shotgunSectionLabel.setAlignment(Qt.AlignCenter)
        #mayaSectionLabel.setAlignment(Qt.AlignCenter)

        #perforceSectionLabel.setScaledContents(True)
        #shotgunSectionLabel.setScaledContents(True)
        #mayaSectionLabel.setScaledContents(True)

        perforceSectionLabel.setTextFormat(Qt.RichText)
        shotgunSectionLabel.setTextFormat(Qt.RichText)
        mayaSectionLabel.setTextFormat(Qt.RichText)
        winfileSectionLabel.setTextFormat(Qt.RichText)

        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        base_path = base_path.replace('\\', '/')

        perforce_icon_path = ('{}/images/perforce/perforce_p4_icon.png'.format(base_path))
        shotgun_icon_path = ('{}/images/shotgun/shotgun_sg_icon.png'.format(base_path))
        maya_icon_path = ('{}/images/maya/maya_2018_icon.png'.format(base_path))
        winfile_icon_path = ('{}/images/windows/file_explorer_icon.png'.format(base_path))

        icon_size = 24
        perforceHtml = r"<img src='{0}' width='{1}' height='{2}'> ".format(perforce_icon_path, icon_size, icon_size)
        shotgunHtml = r"<img src='{0}' width='{1}' height='{2}'> ".format(shotgun_icon_path, icon_size, icon_size)
        mayaHtml = r"<img src='{0}' width='{1}' height='{2}'> ".format(maya_icon_path, icon_size, icon_size)
        winfileHtml = r"<img src='{0}' width='{1}' height='{2}'> ".format(winfile_icon_path, icon_size, icon_size)

        perforceSectionLabel.setText(perforceHtml + "Perforce".format(perforce_icon_path))
        shotgunSectionLabel.setText(shotgunHtml + "Shotgun".format(shotgun_icon_path))
        mayaSectionLabel.setText(mayaHtml + "Maya".format(maya_icon_path))
        winfileSectionLabel.setText(winfileHtml + "File".format(winfile_icon_path))

        perforceSection = QWidgetAction(menu)
        shotgunSection = QWidgetAction(menu)
        mayaSection = QWidgetAction(menu)
        winfileSection = QWidgetAction(menu)

        perforceSection.setDefaultWidget(perforceSectionLabel)
        shotgunSection.setDefaultWidget(shotgunSectionLabel)
        mayaSection.setDefaultWidget(mayaSectionLabel)
        winfileSection.setDefaultWidget(winfileSectionLabel)

        # perforce menu actions
        action_func_standalone = [
            (perforceSection, self._no_function),
            (QAction(u'サブミット', self.file_view), self._p4_submit),
            (QAction(u'', self.file_view), None),
            (QAction(u'最新リビジョンを取得', self.file_view), self._p4_sync_files),
            (QAction(u'', self.file_view), None),
            (QAction(u'追加 / チェックアウト', self.file_view), self._p4_checkout),
            (QAction(u'', self.file_view), None),
            (QAction(u'変更していなければ元に戻す', self.file_view), self._p4_revert_if_unchanged),
            (QAction(u'元に戻す...', self.file_view), self._p4_revert),
            (QAction(u'', self.file_view), None),
            (QAction(u'Export (Motion)', self.file_view), self._maya_export_motion_files),
        ]

        # shotgun menu actions
        sg_status_icon_provider = ShotgunStatusIconProvider()
        status_icon_wtg = sg_status_icon_provider.status_icon('wtg')
        status_icon_rdy = sg_status_icon_provider.status_icon('rdy')
        status_icon_wfr = sg_status_icon_provider.status_icon('wfr')
        status_icon_rev = sg_status_icon_provider.status_icon('rev')
        status_icon_rtk = sg_status_icon_provider.status_icon('rtk')
        status_icon_hld = sg_status_icon_provider.status_icon('hld')
        status_icon_comp = sg_status_icon_provider.status_icon('comp')
        status_icon_omt = sg_status_icon_provider.status_icon('omt')
        action_func_shotgun = [
            (shotgunSection, self._no_function),
            (QAction(status_icon_wtg, u'未着手 (wtg)', self.file_view), partial(self._sg_set_asset_task_status, "wtg")),
            (QAction(status_icon_rdy, u'着手中 (rdy)', self.file_view), partial(self._sg_set_asset_task_status, "rdy")),
            (QAction(status_icon_wfr, u'レビュー待ち (wfr)', self.file_view), partial(self._sg_set_asset_task_status, "wfr")),
            (QAction(status_icon_rev, u'Pending Review (rev)', self.file_view), partial(self._sg_set_asset_task_status, "rev")),
            (QAction(status_icon_rtk, u'リテイク中 (rtk)', self.file_view), partial(self._sg_set_asset_task_status, "rtk")),
            (QAction(status_icon_hld, u'On Hold (hld)', self.file_view), partial(self._sg_set_asset_task_status, "hld")),
            (QAction(status_icon_comp, u'作業完了 (comp)', self.file_view), partial(self._sg_set_asset_task_status, "comp")),
            (QAction(status_icon_omt, u'Omit (omt)', self.file_view), partial(self._sg_set_asset_task_status, "omt")),
        ]

        # maya menu actions
        action_func_for_maya = [
            (mayaSection, self._no_function),
            (QAction(u'', self.file_view), None),
            (QAction(u'Open', self.file_view), self._maya_file_open),
            (QAction(u'Import', self.file_view), self._maya_file_import),
            (QAction(u'Reference', self.file_view), self._maya_file_reference),
            (QAction(u'', self.file_view), None),
            (QAction(u'選択ファイルを同一フォルダへ別名保存', self.dir_view), self._maya_file_save_as),
        ]

        # file (windows explorer) menu actions
        action_func_winfile = [
            (winfileSection, self._no_function),
            (QAction(u'ファイル名をコピー', self.file_view), self._winfile_copy_file_name),
            (QAction(u'ファイルのパスをコピー', self.file_view), self._winfile_copy_file_path),
            (QAction(u'ファイルのフォルダをエクスプローラーで開く', self.file_view), self._winfile_open_folder),
        ]

        if MODE == 'MAYA':
            action_func = action_func_standalone

            if self._enable_sg:
                action_func = action_func + action_func_shotgun

            action_func = action_func + action_func_for_maya

            action_func = action_func + action_func_winfile

        else:
            action_func = action_func_standalone

        for action, func in action_func:
            if action:
                menu.addAction(action)
            if func:
                action.triggered.connect(func, Qt.UniqueConnection)
            else:
                action.setSeparator(True)

        menu.exec_(self.file_view.mapToGlobal(point))

    def _no_function(self, *args):
        return

    def _add_bookmark(self, *args):
        u"""ブックマークを追加"""
        # logger.debug('MODE: {}'.format(MODE))
        if args:
            bookmark = args[0]
        else:
            index = self.dir_view.currentIndex()
            bookmark = self.dir_view.model().filePath(index)

        for i in range(self.bookmark.pulldown.count()):
            if bookmark == self.bookmark.pulldown.itemText(i):
                return

        # logger.debug(bookmark)
        self.bookmark.pulldown.addItem(bookmark)

        if MODE == 'MAYA':
            # logger.debug('Save Bookmark')
            if cmds.optionVar(q=self.key_bookmarks):
                bookmark = '{},{}'.format(cmds.optionVar(q=self.key_bookmarks), bookmark)
                # logger.debug(bookmark)

            cmds.optionVar(sv=[self.key_bookmarks, bookmark])
            # logger.debug('Bookmark: {}'.format(cmds.optionVar(q=self.key_bookmarks)))

    def _delete_bookmark(self, *args):
        u"""ブックマークから削除"""
        if args:
            bookmark = args[0]
        else:
            index = self.dir_view.currentIndex()
            bookmark = self.dir_view.model().filePath(index)

        deletes = False

        for i in range(self.bookmark.pulldown.count()):
            if bookmark == self.bookmark.pulldown.itemText(i):
                self.bookmark.pulldown.removeItem(i)
                deletes = True
                break

        if MODE == 'MAYA' and deletes:
            if cmds.optionVar(q=self.key_bookmarks):
                bookmarks = cmds.optionVar(q=self.key_bookmarks).split(',')
                if bookmark in bookmarks:
                    bookmarks.remove(bookmark)
                    cmds.optionVar(sv=(self.key_bookmarks, ','.join(bookmarks)))

    def get_file_paths_from_cell(self):
        u"""fileViewのセルからファイルパスを取得"""
        file_paths = []
        dir_path = self.dir_view.model().filePath(self.dir_view.currentIndex())
        indices = self.file_view.selectionModel().selectedRows(0)

        for index in indices:
            name = self.file_view.source_model.itemFromIndex(
                self.file_view.proxy_model.mapToSource(index)
            ).text()
            file_paths.append(u'{}/{}'.format(dir_path, name))

        return file_paths

    def _p4_sync_dir(self, *args):
        u"""最新リビジョンの取得"""
        # logger.debug('sync directory')
        index = self.dir_view.currentIndex()
        dir_path = re.sub('/', r'\\\\', self.dir_view.model().filePath(index))
        MtkP4.sync(dir_path)
        logger.info(u'Sync: {}'.format(dir_path))

        self._reload_file_view(index)
        self._reload_search_box()
        self._resize_file_view()

    def _p4_sync_files(self, *args):
        u"""最新リビジョンの取得"""
        # logger.debug('sync files')
        file_paths = self.get_file_paths_from_cell()
        MtkP4.sync(file_paths)
        [logger.info(u'Sync: {}'.format(file_path)) for file_path in file_paths]

        self.reload_table_row_data()

    def _p4_checkout(self, *args):
        u"""追加 / チェックアウト"""
        file_paths = self.get_file_paths_from_cell()
        # logger.debug('checkout: {}'.format(file_paths))
        MtkP4.edit(file_paths)
        [logger.info(u'ADD / Checkout: {}'.format(file_path)) for file_path in file_paths]
        self.reload_table_row_data()

    def _p4_revert_if_unchanged(self, *args):
        u"""変更していなければ元に戻す"""
        file_paths = self.get_file_paths_from_cell()
        MtkP4.revert(file_paths, '-a')
        [logger.info(u'Revert if unchanged: {}'.format(file_path)) for file_path in file_paths]
        self.reload_table_row_data()

    def _p4_revert(self, *args):
        u"""元に戻す"""
        dialog = MtkExplorerDialog(title='Warning: Revert', message=u'本当に元に戻しても良いですか?')
        result = dialog.exec_()
        if not result:
            return

        file_paths = self.get_file_paths_from_cell()
        MtkP4.revert(file_paths)
        [logger.info(u'Revert: {}'.format(file_path)) for file_path in file_paths]
        self.reload_table_row_data()

    def _p4_submit(self, *args):
        u"""サブミット"""
        file_paths = self.get_file_paths_from_cell()
        dialog = MtkExplorerPromptDialog(title='Write a description', message='Write a description')
        result = dialog.exec_()
        if not result:
            return

        description = dialog.textValue()
        MtkP4.submit(file_paths, description)
        [logger.info(u'Submit: {}'.format(file_path)) for file_path in file_paths]
        self.reload_table_row_data()

    # -----------------------------------------------------------------------------------------------------------------
    # Autodesk Shotgun Functions
    # -----------------------------------------------------------------------------------------------------------------
    def _sg_set_asset_task_status(self, sg_status):

        if not self._enable_sg:
            return

        print("zexplorer")
        print("right click : _sg_set_asset_task_status {}".format(sg_status))

        asset_names = []

        file_name_column = MtkExplorerFileModelColumn.Name_Id()
        sg_task_column = MtkExplorerFileModelColumn.SG_Task_Id()

        file_name_indices = self.file_view.selectionModel().selectedRows(file_name_column)
        sg_task_indices = self.file_view.selectionModel().selectedRows(sg_task_column)

        # prepare the asset names
        for index in file_name_indices:
            file_name = self.file_view.source_model.itemFromIndex(self.file_view.proxy_model.mapToSource(index)).text()
            asset = ntpath.basename(file_name).split(".")[0]
            asset_names.append(u'{}'.format(asset))

        # get the sg task combobox delegate from the table
        task_cb_delegate = self.file_view.itemDelegateForColumn(sg_task_column)

        # get the sg task data from the combobox delegate
        for asset_name in asset_names:
            #sg_task_name = None
            sg_task_data = {}
            combo_data_dict = task_cb_delegate.getSaveRestoreData(asset_name)

            #if 'sg_task_name' in combo_data_dict:
            #    sg_task_name = combo_data_dict['sg_task_name']

            # skip the non task item. it means no sg task.
            #if sg_task_name and sg_task_name == 'na':
            #    continue

            if 'sg_task_data' in combo_data_dict:
                sg_task_data = combo_data_dict['sg_task_data']

            if sg_task_data:
                # get the sg task id
                if 'id' in sg_task_data:
                    task_id = sg_task_data['id']
                    # change the sg task status
                    print(u"changing task id/status: {}/{}".format(task_id, sg_status))
                    MtkSG.set_asset_task_status(sg_task_id=task_id, sg_status=sg_status)

        # reload the table row data
        self.reload_table_row_data()

        # reload the sg task comboboxes
        # (this is the only way to do it)
        for index in sg_task_indices:
            index.model().dataChanged.emit(index, index)


    def _show_explorer(self, *args):
        u"""エクスプローラで表示"""
        index = self.dir_view.currentIndex()
        dir_path = re.sub('/', r'\\\\', self.dir_view.model().filePath(index))
        self._exec_subprocess('cmd /c start "" {}'.format(dir_path))

    def _maya_export_motion_dir(self, *args):
        u"""Motion Export"""
        index = self.dir_view.currentIndex()
        # dir_path = re.sub('/', r'\\\\', self.dir_view.model().filePath(index))
        dir_path = self.dir_view.model().filePath(index)
        # self._exec_subprocess('start {0} {1}'.format(self._export_bat, dir_path))
        mel.eval('system("start {0} {1}")'.format(self._export_bat, dir_path))

    def _maya_export_motion_files(self, *args):
        u"""Motion Export"""
        file_paths = []
        dir_path = self.dir_view.model().filePath(self.dir_view.currentIndex())
        indices = self.file_view.selectionModel().selectedRows(0)

        for index in indices:
            name = self.file_view.source_model.itemFromIndex(self.file_view.proxy_model.mapToSource(index)).text()
            file_paths.append(u'{}/{}'.format(dir_path, name))

        argument = ' '.join(file_paths)
        # self._exec_subprocess('start {0} {1}'.format(self._export_bat,  argument))
        mel.eval('system("start {0} {1}")'.format(self._export_bat, argument))

    def _root_path_changed(self, root_path):
        #logger.debug("Root Path Changed")

        if not os.path.exists(root_path):
            return

        # logger.debug("path: {}".format(root_path))
        self._header.reload(root_path)
        self._body.reload(root_path)


    def _dir_text_changed(self, *args):
        u"""Directory Text Changed"""
        # logger.debug("Directory Text Changed")
        # logger.debug("Callstack: {}".format(inspect.stack()[1][3]))

        dir_path = self.address_bar.textbox.text()

        if not os.path.exists(dir_path):
            return

        # logger.debug("path: {}".format(dir_path))

        self._body.reload(dir_path)

        index = self.dir_view.model().index(dir_path)

        self.address_bar.reload(dir_path)

        self._reload_category(dir_path)
        self._reload_dir_view(index)
        self._reload_file_view(index)
        self._reload_search_box()
        self._resize_file_view()

        if MODE == 'MAYA' and not self._boot:
            # logger.debug('Save Root Path')
            cmds.optionVar(sv=(self.key_root_path, dir_path))


    def _search_text_changed(self, *args):
        u"""Search Text Changed"""
        # logger.debug("Search Text Changed")
        self._reload_search_box()
        self._resize_file_view()

    def _save_current_scene_to_selection_dir(self, *args):
        u"""現在のシーンを選択したディレクトリに保存"""
        if MODE != 'MAYA':
            return

        index = self.dir_view.currentIndex()
        dir_path = self.dir_view.model().filePath(index)
        if not dir_path:
            return

        file_path = getCurrentSceneFilePath()

        text, _ = os.path.splitext(os.path.basename(file_path))
        result = cmds.promptDialog(
            title='Filename',
            message='Enter Filename:',
            text=text,
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel',
        )
        if result == 'OK':
            name = cmds.promptDialog(query=True, text=True)

            if file_path:
                shutil.copyfile(file_path, u'{}/{}.ma'.format(dir_path, name))
            else:
                cmds.file(rename='{}/{}.ma'.format(dir_path, name))
                cmds.file(s=True, f=True)

            self._reload_file_view(index)
            self._reload_search_box()
            self._resize_file_view()

    def _set_workspace(self, file_path):
        if not file_path:
            return

        workspace_path = os.path.dirname(os.path.dirname(file_path))

        if workspace_path != cmds.workspace(q=True, o=True):
            result = cmds.confirmDialog(
                title='Warning: Workspace',
                message=u'Workspaceをセットしますか？',
                button=['OK', 'Cancel'],
                defaultButton='Cancel',
                cancelButton='Cancel',
                dismissString='Cancel',
            )
            if result == 'OK':
                cmds.workspace(workspace_path, o=True)

    def _maya_file_open(self, *args):
        u"""ファイルを開く"""
        if MODE != 'MAYA':
            return

        file_paths = self.get_file_paths_from_cell()
        if not file_paths:
            return
        file_path = file_paths[0]

        sets_workspace = self.sets_workspace.isChecked()
        checkouts = self.checkouts.isChecked()
        sets_sg_task_status = self.sets_sg_task_status.isChecked()
        current_scene = getCurrentSceneFilePath()
        if cmds.file(q=True, mf=True):
            message = 'Save changes to\n{}?'.format(current_scene) if current_scene else 'Save changes to untitled scene?'

            result = cmds.confirmDialog(
                title='Warning: Scene Not Saved',
                message=message,
                button=['Save', "Don't Save", 'Cancel'],
                defaultButton='Cancel',
                cancelButton='Cancel',
                dismissString='Cancel',
            )

            # logger.debug(result)

            if result == 'Save':
                # automatically set current shotgun task status to rdy
                if sets_sg_task_status:
                    self._sg_set_asset_task_status("rdy")

                if checkouts:
                    MtkP4.edit(file_path)
                    self.reload_table_row_data()

                if sets_workspace:
                    self._set_workspace(file_path)

                cmds.file(s=True, f=True)
                cmds.file(file_path, o=True, f=True)
            elif result == "Don't Save":
                # automatically set current shotgun task status to rdy
                if sets_sg_task_status:
                    self._sg_set_asset_task_status("rdy")

                if checkouts:
                    MtkP4.edit(file_path)
                    self.reload_table_row_data()

                if sets_workspace:
                    self._set_workspace(file_path)

                cmds.file(file_path, o=True, f=True)
        else:
            result = cmds.confirmDialog(
                title='Warning',
                message=u'ファイルを開きますか？',
                button=['OK', 'Cancel'],
                defaultButton='Cancel',
                cancelButton='Cancel',
                dismissString='Cancel',
            )
            if result == 'Cancel':
                return

            # automatically set current shotgun task status to rdy
            if sets_sg_task_status:
                self._sg_set_asset_task_status("rdy")

            if checkouts:
                MtkP4.edit(file_path)
                self.reload_table_row_data()

            if sets_workspace:
                self._set_workspace(file_path)

            cmds.file(file_path, o=True, f=True)

    def _maya_file_import(self, *args):
        u"""ファイルをインポート"""
        if MODE != 'MAYA':
            return

        file_paths = self.get_file_paths_from_cell()
        if not file_paths:
            return
        file_path = file_paths[0]
        cmds.file(file_path, i=True, f=True)

    def _maya_file_reference(self, *args):
        u"""リファレンス読み込み"""
        if MODE != 'MAYA':
            return

        file_paths = self.get_file_paths_from_cell()
        if not file_paths:
            return
        file_path = file_paths[0]
        text, _ = os.path.splitext(os.path.basename(file_path))
        result = cmds.promptDialog(
            title='Namespace',
            message='Enter Namespace:',
            text=text,
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel',
        )
        if result == 'OK':
            namespace = cmds.promptDialog(query=True, text=True)
            cmds.file(file_path, r=True, ns=namespace, f=True)

    def _maya_file_save_as(self, *args):
        u"""選択したファイルを別名で保存"""
        if MODE != 'MAYA':
            return

        file_paths = self.get_file_paths_from_cell()
        if not file_paths:
            return
        file_path = file_paths[0]
        dir_path = re.sub(r'\\', '/', os.path.dirname(file_path))
        result = cmds.promptDialog(
            title='Filename',
            message='Enter Filename:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel',
        )
        if result == 'OK':
            name = cmds.promptDialog(query=True, text=True)
            shutil.copyfile(file_path, u'{}/{}.ma'.format(dir_path, name))

            index = self.dir_view.currentIndex()

            self._reload_file_view(index)
            self._reload_search_box()
            self._resize_file_view()

    def _winfile_copy_file_name(self, *args):
        u"""ファイル名をコピー"""
        if MODE != 'MAYA':
            return

        file_paths = self.get_file_paths_from_cell()

        if not file_paths:
            return

        fileNameList = []
        for filePath in file_paths:
            fileName = os.path.basename(filePath)
            fileNameList.append(fileName)
        #print("copy file names: {}".format(fileNameList))
        pyperclip.copy('\n'.join(fileNameList))

    def _winfile_copy_file_path(self, *args):
        u"""ファイルのパスをコピー"""
        if MODE != 'MAYA':
            return

        file_paths = self.get_file_paths_from_cell()

        if not file_paths:
            return

        #print("copy file paths: {}".format(file_paths))
        pyperclip.copy('\n'.join(file_paths))

    def _winfile_open_folder(self, *args):
        u"""ファイルのフォルダをエクスプローラーで開く"""
        if MODE != 'MAYA':
            return

        file_paths = self.get_file_paths_from_cell()

        if not file_paths:
            return

        file_path = file_paths[0]
        folder_path = os.path.dirname(file_path)
        #print("open folder path: {}".format(folder_path))
        os.startfile(folder_path)


def main():
    import sys

    try:
        from PySide2.QtWidgets import QApplication
    except ImportError:
        from PySide.QtGui import QApplication

    app = QApplication(sys.argv)
    widget = MtkExplorer()

    qss = 'qdarkstyle/style.qss'
    if os.path.exists(qss):
        with open(qss, 'r') as f:
            widget.setStyleSheet(f.read())
    elif os.path.exists('{}/{}'.format(os.path.dirname(__file__), qss)):
        with open('{}/{}'.format(os.path.dirname(__file__), qss), 'r') as f:
            widget.setStyleSheet(f.read())
    widget.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()