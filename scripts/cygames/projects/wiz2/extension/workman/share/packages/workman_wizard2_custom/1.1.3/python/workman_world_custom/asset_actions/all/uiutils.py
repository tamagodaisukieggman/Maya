# -*- coding: utf-8 -*-
from __future__ import print_function

from workfile_manager import cmds as wcmds, p4utils, postproc_utils
from workfile_manager.ui import uiutils, ui_main, ui_table
from workfile_manager.plugin_utils import PostProcBase, PluginType, Application, AssetAction
from cylibassetdbutils import assetdbutils, assetutils

from Qt import QtWidgets, QtCore, QtGui
import re
import os

db = assetdbutils.DB.get_instance()

class AssetSelector(QtWidgets.QWidget, object):
    def __init__(self, args, aw=None, base_asset_label='Rig Asset'):
        super(AssetSelector, self).__init__()
        self.args = args
        self.mwin = args['table'].mwin

        vbox = QtWidgets.QVBoxLayout(self)
        self.tab = tab = QtWidgets.QTabWidget()
        vbox.addWidget(tab)
        main_tab_widget = QtWidgets.QWidget()
        tab.addTab(main_tab_widget, 'Main')

        vbox = QtWidgets.QVBoxLayout(main_tab_widget)
        gbox = uiutils.GroupBox(base_asset_label)
        
        vbox1 = QtWidgets.QVBoxLayout(gbox)
        
        hbox = QtWidgets.QHBoxLayout()
        self.icon = icon = QtWidgets.QLabel('None')
        icon.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        icon.setFixedWidth(200)
        icon.setFixedHeight(150)
        
        icon.setFrameShape(QtWidgets.QFrame.Panel)
        hbox.addWidget(icon)
        
        vbox2 = QtWidgets.QVBoxLayout()
        self.lb_rig = lb_rig = QtWidgets.QLabel('Not specified')
        lb_rig.setStyleSheet('font-size:17px')
        self.btn_load_latest = QtWidgets.QPushButton('Load latest')
        
        self.btn_load_latest.clicked.connect(self.load_latest)
        self.btn_load_latest.setFixedWidth(100)
        self.btn_load_latest.setEnabled(False)
        btn_paste = QtWidgets.QPushButton('Paste %s URL' % (base_asset_label.lower()))

        btn_paste.clicked.connect(self.paste_clicked)
        vbox2.addWidget(lb_rig)
        vbox2.addWidget(self.btn_load_latest)
        vbox2.addWidget(QtWidgets.QWidget(), 1)
        vbox2.addWidget(btn_paste)

        hbox.addLayout(vbox2, 1)

        vbox1.addLayout(hbox)
        
        vbox1.addWidget(uiutils.vspacer(10))
        hbox = QtWidgets.QHBoxLayout()
        lb_his = QtWidgets.QLabel('History:')
        #lb_his.setFixedWidth(80)
        hbox.addWidget(lb_his)
        self.cmb_his = cmb_his = QtWidgets.QComboBox()
        cmb_his.currentIndexChanged.connect(self.history_selected)
        hbox.addWidget(cmb_his, 1)
        vbox1.addLayout(hbox)

        gbox.setLayout(vbox1)
        
        vbox.addWidget(gbox)

        gbox = uiutils.GroupBox('Animations')
        
        vbox1 = QtWidgets.QVBoxLayout(gbox)
        self.lw = lw = QtWidgets.QListWidget()
        for asset in args['assets']:
            lb = asset._filename[asset._filename.rfind('/')+1:]
            lb = lb[:lb.rfind('.')]
            item = QtWidgets.QListWidgetItem(lb)
            item._asset = asset
            lw.addItem(item)

        vbox1.addWidget(lw)
        gbox.setLayout(vbox1)
        vbox.addWidget(gbox, 1)

        if aw:
            gbox = uiutils.GroupBox('Others')
            vbox1 = QtWidgets.QVBoxLayout(gbox)
            vbox1.addWidget(aw)
            gbox.setLayout(vbox1)
            vbox.addWidget(gbox)

        his = self.mwin.var.get(self.base_asset_history_varname())
        if his and len(his) > 0:
            filename, version = his[0]
            self.set_(filename, version)
        else:
            self.paste_clicked()

        self.update_history_ui()

    def base_asset_history_varname(self):
        #raise Exception('Override in a derived class.')
        return None

    def update_history_ui(self):
        self.cmb_his.clear()

        his = self.mwin.var.get(self.base_asset_history_varname())
        if type(his) is not list:
            return

        for filename, version in his:
            v = re.sub('[.][^.]+$', '', os.path.basename(filename))
            self.cmb_his.addItem(v, (filename, version))

    def history_selected(self, index):
        data = self.cmb_his.itemData(index)
        if type(data) is list:
            self.set_(data[0], data[1])

    def paste_clicked(self):
        res = self.get_clipped_value()
        if not res:
            return
        self.set_(*res)
        self.add_history(*res)

        
    def is_base_asset_valid(self, asset):
        raise Exception('Override in a derived class.')

    def get_clipped_value(self):
        buf = QtGui.QClipboard().text()
        from workfile_manager import cmds as wcmds
        try:
            res = wcmds.parse_asseturl(ui_main.mwin.dccutils().get_instance(), buf)
        except:
            res = None

        valid = True
        if not res:
            valid = False
        else:
            filename, asset = res[0]
            valid = self.is_base_asset_valid(asset)

        if not valid:
            return

        return filename, asset.version

    def add_history(self, filename, version):
        v = [(filename, version)]
        his = self.mwin.var.get(self.base_asset_history_varname())
        if type(his) is list:
            his = list(set([tuple(x) for x in his]))
            his = [x for x in his if x != v[0]]
            v = v + his
            if len(v) > 10:
                v = v[:10]

        self.mwin.var.replace(self.base_asset_history_varname(), v)
        self.update_history_ui()


    def set_(self, filename, version):
        basename = re.sub('[.][^.]+$', '', os.path.basename(filename))
        self.lb_rig.setText(basename)

        thumb = assetutils.Asset.thumbnail_filepath(filename, version, replace_share_root=False)
        print('thumb: ', thumb)
        pix = QtGui.QPixmap(thumb)
        pix = QtGui.QPixmap(thumb).scaledToHeight(150)
        self.icon.setFixedWidth(pix.width())
        self.icon.setFixedHeight(pix.height())
        self.icon.setPixmap(pix)


        buf = db.get_sharedasset_from_file(filename)
        if len(buf) > 0:
            assetdict = buf[0]
            from cylibassetdbutils import assetvar
            asset = assetvar.ShareAsset()
            for k in list(asset.get_dict().keys()):
                setattr(asset, k, assetdict[k])
            asset.version = None

            vers = db.get_sharedasset_versions(asset, ignore_omit=True)
            if vers[0]['version'] > version:
                self.btn_load_latest.setEnabled(True)
                self.btn_load_latest.filename = vers[0]['path']
                self.btn_load_latest.version = vers[0]['version']
                self.btn_load_latest.setStyleSheet('color:#FFFF00;font-weight:bold')
            else:
                self.btn_load_latest.setEnabled(False)
                self.btn_load_latest.setStyleSheet(None)


    def load_latest(self):
        tpl = (self.btn_load_latest.filename, self.btn_load_latest.version)
        self.set_(*tpl)
        self.add_history(*tpl)

