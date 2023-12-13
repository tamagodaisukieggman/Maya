# -*- coding: utf-8 -*-

from workfile_manager import p4utils
from cylibassetdbutils import assetdbutils
from workfile_manager.plugin_utils import Application, AssetActionWithSync, PluginType
from workfile_manager import p4utils
from workfile_manager.ui import uiutils

from Qt import QtWidgets, QtCore, QtGui
import re, os, copy

try:
    import fbx
    from workfile_manager_mbuilder import assetutils_motionbuilder
    from workfile_manager import fbxutils
except:
    pass

p4u = p4utils.P4Utils.get_instance()
db = assetdbutils.DB.get_instance()


class Plugin(AssetActionWithSync):
    def apps_executable_on(self):
        return [Application.MotionBuilder]

    def is_asset_eligible(self, asset):
        if asset.area() != 'work':
            return False
        if asset.assetgroup != 'character':
            return False
        if asset.task != 'animation' and asset.task != 'model':
            return False

        return True

    def getlabel(self):
        return 'Update models'

    def allow_multi_items(self):
        return True

    def sync_done(self, stat):
        args = self.args
        w = UpdateAssetWidget(args)
        update_dialog = uiutils.PromptDialog('Update Assets', '', wd=w, btns=[' Update All (Local)', ' Update All (Server)', 'Close'])

        icon = QtGui.QIcon(':/icons/computer02.png')
        update_dialog.btn_widgets[0].setIcon(icon)
        update_dialog.btn_widgets[0].setIconSize(QtCore.QSize(28, 28))

        icon = QtGui.QIcon(':/icons/cloud.png')
        update_dialog.btn_widgets[1].setIcon(icon)
        update_dialog.btn_widgets[1].setIconSize(QtCore.QSize(25, 25))

        for i in range(3):
            update_dialog.btn_widgets[i].setStyleSheet('QWidget {padding:0px 10px 0px 10px}')
            update_dialog.btn_widgets[i].setFixedHeight(40)


        update_dialog.resize(600, 700)
        res = update_dialog.exec_()
        if res == 1:
            submit_server = False
        elif res == 2:
            submit_server = True
        else:
            return
        
        submitted = False

        import importlib
        from workfile_manager import postproc_utils, cmds as wcmds
        
        for i in range(w.lw_works.count()):
            filename, version, reader = w.lw_works.item(i).data(QtCore.Qt.UserRole)
            assets = get_asset_info(filename, version, reader)
            if assets is None:
                continue

            for asset in assets:
                _, assetdict, latest, _, _, _ = asset
                if assetdict['version'] < latest:
                    # need to update
                    break
            else:
                # no need to update
                continue

            pp = postproc_utils.find_proc_by_name('motionbuilder.all.postproc_update_models', plugin_type=PluginType.PublishPostProcess)

            args = {}
            args['inputfile'] = None
            args['outfile'] = None
            args['target_workfile'] = filename
            args['workfile_version'] = version
            args['assets'] = assets
            args['is_custom_task'] = True
            args['publish_app'] = None
            args['submit_server'] = submit_server
            args['export_all'] = True
            args['commit_to_engine'] = False
            args['user'] = p4u.p4.user
            args['deadline_batchname'] = re.sub('[.][^.]*', '', assetdbutils.labelpostfix())
            
            if args['submit_server']:
                args['postproc'] = [pp]
                tags = []
                comment = ''
                buf = db.get_workasset_versions(filename=filename, ignore_path_template=True, version=version)
                if len(buf) == 0:
                    raise Exception('No workasset found.')
                work_assetdict = buf[0]
                share_asset = assetutils_motionbuilder.ModelAssetMotionBuilder()
                for k in list(share_asset.get_dict().keys()):
                    setattr(share_asset, k, work_assetdict[k])

                wfile = {'local_master_path':filename, 'version':version}
                task = wcmds.PublishTask(share_asset, tags, wfile, comment, args)
                res = task.execute(silent=True)
                submitted = True
                
            else:
                m = importlib.import_module(pp['module_name'])
                m.Plugin().execute(args)


        if submitted:
            d = uiutils.PromptDialog('Confirmation', u'アップデートジョブを投げました。', btns=['OK'])
            d.resize(600, 200)
            d.exec_()


    
class UpdateAssetWidget(QtWidgets.QWidget):
    def __init__(self, args, parent=None):
        def get_label(tx):
            lb = QtWidgets.QLabel(tx)
            lb.setStyleSheet('QLabel {font-size:18px; font-weight:bold}')
            return lb

        super(UpdateAssetWidget, self).__init__(parent)
        self.args = args
        vbox = QtWidgets.QVBoxLayout(self)

        vbox.addWidget(get_label('Workfiles:'))
        self.lw_works = QtWidgets.QListWidget()
        self.lw_works.setStyleSheet('QWidget::item {margin-bottom:5px}')
        self.lw_works.itemSelectionChanged.connect(self.reload_assets)
        vbox.addWidget(self.lw_works)

        vbox.addWidget(get_label('Assets:'))
        self.tbl_assets = tw = QtWidgets.QTableWidget()
        self.tbl_assets.setStyleSheet('QWidget {font-size:17px}')
        

        tw.setColumnCount(3)
        tw.setRowCount(1)
        tw.setWordWrap(False)
        tw.setColumnWidth(0, 150)
        tw.setColumnWidth(1, 100)
        tw.setColumnWidth(2, 100)
        tw.setSortingEnabled(True)
        tw.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        tw.setHorizontalHeaderLabels(['Asset', 'Scene', 'Latest'])
        header = tw.horizontalHeader()
        if type(header) is QtWidgets.QHeaderView:
            header.setSortIndicatorShown(True)
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        tw.verticalHeader().setVisible(False)
        vbox.addWidget(self.tbl_assets)
        print ('UpdateAssetWidget')

    def reload(self):
        from workfile_manager.ui import ui_table
        from workman_world_custom.asset_actions.motionbuilder.publish_parts_base_mbuilder import FBXReader

        table = self.args['table']
        assets = self.args['assets']

        sel = table.selectedIndexes()
        sel = list(set([x.row() for x in sel]))
        print(('sel: ', sel))

        self.lw_works.clear()
        for r in sel:
            vidx = ui_table.find_column(r, ui_table.LabelType.Version)
            vod = table.model().m_data[r][vidx][0]
            if vod is None:
                vod = 0
            filename = table.model().m_data[r][vidx][2][vod]

            if not os.path.exists(filename):
                continue

            reader = FBXReader(filename)
            basename = filename[filename.rindex('/')+1:]
            basename = re.sub('[.][^.]*$', '', basename)
            vstr = table.model().m_data[r][vidx][1][vod]
            lb = '%s (%s)' % (basename, vstr)
            item = QtWidgets.QListWidgetItem(lb)
            version = int(vstr[1:])
            item.setData(QtCore.Qt.UserRole, (filename, version, reader))

            self.lw_works.addItem(item)

        if len(sel) > 0:
            self.lw_works.setCurrentRow(0)
        else:
            self.reload_assets()

    def reload_assets(self):
        #table = self.args['table']
        self.tbl_assets.setRowCount(0)
        buf = self.lw_works.selectedIndexes()
        if len(buf) == 0:
            return
        r = buf[0].row()
        (filename, version, reader) = self.lw_works.item(r).data(QtCore.Qt.UserRole)
        assets = get_asset_info(filename, version, reader)
        if assets is None:
            return
        cnt = len(assets)
        self.tbl_assets.setRowCount(cnt)
        
        for ci, asset in enumerate(assets):
            items = []
            asset_name, assetdict, latest, ns, asset_filename, latest_filename = asset
            print('asset_name:', asset_name)
            asset_version = assetdict['version']
            item = QtWidgets.QTableWidgetItem(asset_name)
            self.tbl_assets.setItem(ci, 0, item)
            items.append(item)

            item = QtWidgets.QTableWidgetItem(str(asset_version))
            item.setTextAlignment(4+0x0080)
            self.tbl_assets.setItem(ci, 1, item)
            items.append(item)

            item = QtWidgets.QTableWidgetItem(str(latest))
            item.setTextAlignment(4+0x0080)
            self.tbl_assets.setItem(ci, 2, item)
            items.append(item)

            if latest > asset_version:
                for item in items:
                    font = item.font()
                    font.setWeight(75)
                    item.setFont(font)

                    fg = item.foreground()
                    fg.setColor(QtCore.Qt.yellow)
                    item.setForeground(fg)
            


def get_asset_info(filename, version, reader):
    if not filename.endswith('.fbx'):
        return None
    print('filename: ', filename)
    print('version: ', version)
    
    res = []
    print('count: ', reader.scene.GetMemberCount())

    cnt = 0
    assetlabels = None
    for i in range(reader.scene.GetMemberCount()):
        n = reader.scene.GetMember(i)
        name = n.GetName()
        if name != 'assetlabels' or type(n) is not fbx.FbxObject:
            continue
        cnt = n.GetSrcObjectCount()
        assetlabels = n
        break
    
    from workfile_manager_mbuilder.assetutils_motionbuilder import ModelAssetMotionBuilder

    assets = []

    for ci in range(cnt):
        cn = assetlabels.GetSrcObject(ci)
        asset_name = cn.GetName()

        child_cnts = cn.GetSrcObjectCount()
        if child_cnts == 0:
            continue
        mnode = cn.GetSrcObject(0)
        lname = mnode.GetName()
        if ':' in lname:
            ns = lname[:lname.rindex(':')]
        else:
            ns = None

        model_asset = ModelAssetMotionBuilder()
        for k in list(model_asset.get_dict().keys()):
            pr = fbxutils.cast_property(cn.FindProperty(k))
            if pr is None:
                continue
            v = pr.Get()
            if type(v) is fbx.FbxString:
                v = v.Buffer()
            setattr(model_asset, k, v)
        assetdict = copy.deepcopy(model_asset.get_dict())
        filename = fbxutils.cast_property(cn.FindProperty('filename')).Get().Buffer()

        model_asset.__dict__.pop('version')

        buf = db.get_sharedassets(model_asset.get_dict())
        latest, latest_filename = [(x['version'], x['path']) for x in buf][-1]
        

        asset = (asset_name, assetdict, latest, ns, filename, latest_filename)
        assets.append(asset)

    return assets


    