# -*- coding: utf-8 -*-
from __future__ import print_function

from workfile_manager import cmds as wcmds, p4utils, postproc_utils
from workfile_manager.ui import uiutils, ui_main, ui_table
from workfile_manager.plugin_utils import AssetActionWithSync, PluginType, Application, AssetAction
from cylibassetdbutils import assetdbutils, assetutils
import cypyapiutils

from Qt import QtWidgets, QtCore, QtGui
import re, os, shutil, copy
import yaml

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()


class BasePlugin(AssetActionWithSync):
    def get_reader(self, filename):
        pass
    
    def is_open_valid(self):
        return False

    def open(self, filename):
        pass

    def apps_executable_on(self):
        return [Application.Maya,
            Application.MotionBuilder, 
            Application.UnrealEngine, 
            Application.Houdini,
            Application.Standalone,
            ]

    def allow_multi_items(self):
        return False

    def postproc_name(self):
        raise Exception('Override in derived class: postproc_name')

    def sync_done(self, stat):
        table = ui_main.mwin.uiobj.tab_area.current_table()
        sources = self.get_asset_info(table)
        
        if self.mode == 1 and len(sources) == 1:
            source_filename = sources[0][0]
            self.open(source_filename)

        if table.asset.task == 'model':
            asset = ui_main.mwin.dccutils().get_instance().create_share_model_asset({})
        elif table.asset.task == 'animation':
            asset = ui_main.mwin.dccutils().get_instance().create_share_anim_asset({})
        else:
            raise Exception('Invalid asset task.')

        for k in table.asset.get_dict():
            setattr(asset, k, getattr(table.asset, k))
        asset.truncate('path_template')
        asset.version = 0

        # select parts.
        
        commit = True
        comment = ''
        
        #
        idx = [0]
        parts_selector = w = PartsSelector(self.args, self, sources, asset, comment=comment, commit=commit)
        
        if ui_main.mwin.dccutils().get_instance().application() != Application.Maya:
            w.cmb_use_preset.currentIndexChanged.connect(None)
            w.cmb_use_preset.setCurrentIndex(0)
            w.cmb_use_preset.setEnabled(False)
            w.lb_use_preset.setEnabled(False)
            w.preset_lw.setEnabled(False)

        d = uiutils.PromptDialog('Select parts to publish', '', wd=w,
                                    btns=['Local Test', 'Publish', 'Cancel'], resume_as_name='PartsSelector',
                                    validity_check_func=w.validity_check_func, validity_check_buttons=[1,2])
        w.parent_window = d

        icon = QtGui.QIcon(':/icons/computer02.png')
        d.btn_widgets[0].setEnabled(False)
        d.btn_widgets[0].setIcon(icon)
        d.btn_widgets[0].setIconSize(QtCore.QSize(28, 28))

        icon = QtGui.QIcon(':/icons/cloud.png')
        d.btn_widgets[1].setEnabled(False)
        d.btn_widgets[1].setIcon(icon)
        d.btn_widgets[1].setIconSize(QtCore.QSize(25, 25))
        for btn in d.btn_widgets:
            btn.setMinimumHeight(34)
            btn.setMinimumWidth(150)

        d.btn_widgets[2].setStyleSheet('QPushButton {margin-left:30px}')

        d.resize(370, 600)
        if len(idx) > 0:
            w.reload(idx)

        try:
            if ui_main.mwin.ui_prefs.var['miscellaneous']['show-set-details-at-open']:
                parts_selector.open_content_viewer()
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(e)

        res = d.exec_()

        comment = w.te_comment.toPlainText().strip()
        parts_selector.splt.closed()
        
        if hasattr(d, 'content_viewer'):
            d.content_viewer.parent_window.close()

        if res != 1 and res != 2:
            return
        
        idx = [x.row() for x in w.lw.selectedIndexes()]

        #
        submit_server = True if res==2 else False
        commit = w.commit.isChecked()
        keep_im = w.keep_im.isChecked()
        parts = [x.data(1) for x in w.lw.selectedItems() if x.data(3)]
        print('parts: ', parts)

        if parts_selector.multi_preset:
            self.set_presets = [x.text() for x in w.preset_lw.selectedItems()]
        else:
            if w.cmb_use_preset.currentIndex() == 0:
                self.set_presets = None
            else:
                self.set_presets = [w.cmb_use_preset.currentText()]
        

        if w.cb_use_op.isChecked():
            ops = [x.text() for x in w.lw2.selectedItems()]
        else:
            ops = None
        print('ops: ', ops)
        other_args = {'commit':commit, 'keep_im':keep_im, 'parts':parts, 'comment':comment, 'operators':ops, 'submit_server':submit_server}

        #
        self.publish_cnts = 0
        for src in sources:
            res = self._calc_total_publish_cnts(other_args, src)
        
        print('publish_parts_base: publish_cnts: ', self.publish_cnts)

        # session export
        assert 'COMPUTERNAME' in os.environ
        session = '%s_%s' % (assetdbutils.datetime_to_str(msec=True, for_filename=True), os.environ['COMPUTERNAME'])

        tmpdir = None
        try:
            if os.path.exists(os.environ['WM_TMP_DIR']):
                tmpdir = os.environ['WM_TMP_DIR']
        except:
            pass
        assert tmpdir is not None
        tmpdir = os.path.join(tmpdir, 'commit', session)
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        session_file = os.path.join(tmpdir, 'session.sdesc')
        print('session_file: ', session_file)
        with open(session_file, 'w') as fhd:
            yaml.dump({'commit_ready':[]}, fhd)
        
        other_args['session'] = session

        #
        for src in sources:
            if not submit_server:
                other_args['background_subprocess'] = True

            res = self._publish(other_args, asset, src, exec_preproc=True if len(sources) > 1 else False, included_parts=parts_selector.filename_to_parts[src[0]])

        if submit_server:
            uiutils.PromptDialog('Confirmation', u'パブリッシュジョブを投げました。', btns=['OK']).exec_()
        else:
            uiutils.PromptDialog('Confirmation', u'バックグラウンドでパブリッシュジョブを起動しました。', btns=['OK']).exec_()

        return res # return last result.

    
    def _calc_total_publish_cnts(self, other_args, source):
        source_filename, tags, version, leafname, localid = source
        
        from postproc_set_editor import operator
        reader = self.get_reader(source_filename)

        print('parts: ', other_args['parts'])
        self.publish_cnts += reader.calc_total_publish_cnts(other_args['parts'], other_args['operators'])

        print('publish_cnts: ', self.publish_cnts)
        

    def get_postprocs(self, all_postprocs):
        pass # override derivedclass

    def additional_args(self, args):
        pass

    def _publish(self, other_args, asset, source, exec_preproc, included_parts):
        source_filename, tags, version, leafname, localid = source

        asset.leafname = leafname
        asset.localid = localid
        out_config = asset.check_output_config(tags=tags)
        asset.path_template = asset.evaluate_output(out_config, proc_token=False, proc_tag=True, tags=tags)

        print('----------------------------------')
        print('source_file: ', source_filename)
        print('asset: ', asset.str_hashkey())
        print(' pt: ', asset.path_template)
        print('tags: ', tags)

        # preproc.
        preprocs = postproc_utils.get_postprocs(asset, ui_main.mwin, only_enabled=True, plugin_type=PluginType.PublishPreProcess,
            excludes=['preproc_select_postproc_edit_set'])
            
        if self.mode == 1 and exec_preproc:
            if not wcmds.preproc({'preproc':preprocs}):
                return


        # copy original thumbnail
        thumb_src = assetutils.Asset.thumbnail_filepath(source_filename, version)
        print('thumb_src: ', thumb_src)
        tmpoutfile, _ = asset.get_exportname(use_path_template=False, tags=tags)
        
        tmpthumb_dst = assetutils.Asset.thumbnail_filepath(tmpoutfile, asset.version, replace_share_root=True)
        tmpthumb_dst = assetutils.get_publish_tempfilename(tmpthumb_dst)
        print('tmpthumb_dst: ', tmpthumb_dst)
        
        thumb_dir = os.path.dirname(tmpthumb_dst)
        if not os.path.exists(thumb_dir):
            os.makedirs(thumb_dir)

        if os.path.exists(thumb_src):
            shutil.copyfile(thumb_src, tmpthumb_dst)

        pp = postproc_utils.get_postprocs(asset, ui_main.mwin, only_enabled=True, 
                            plugin_type=PluginType.PublishPostProcess, includes=[self.postproc_name()])
        postprocs, child_postprocs = self.get_postprocs(pp)

        child_commitprocs = postproc_utils.get_postprocs(asset, ui_main.mwin, only_enabled=True,
                            plugin_type=PluginType.CommitProcess)
        
        print('postproc: ', postprocs)
        print('child_commitprocs: ', child_commitprocs)

        refs = db.get_workasset_refs(filename=source_filename, version=version, include_omit=False)
        ref_files = [assetdbutils.normalize_path(x['local_path']) for x in refs]
        
        textures = assetutils._get_textures_2(ref_files)

        print('textures: ', textures)
        comment = other_args['comment']

        
        from cylibassetdbutils import assetvar
        #
        args = {
            'export_all': True, 
            'export_only': False,
            'submit_server': other_args['submit_server'],
            'postproc': postprocs,
            'preproc': preprocs,
            'procs': [], 
            'user': p4u.p4.user,
            'commit_to_engine': other_args['commit'],
            'keep_intermediate': other_args['keep_im'],
            'child_postprocs': child_postprocs,
            'child_commitprocs': child_commitprocs,
            'publish_parts_parts': other_args['parts'],
            'publish_parts_operators': other_args['operators'],
            'source_file': source_filename, 
            'source_version': version, 
            'comment': comment, 
            #'child_asset': assetvar.ShareAsset(base=asset), 
            'child_asset': asset,
            'child_tags': tags, 
            'thumbnail_source': tmpthumb_dst, 
            
            'inputfile_source': source_filename, 
            'textures': textures, 
            'is_custom_task': True,

            'dont_delete_tmp_thumbnail': True,

            'lazy_submit': True if self.publish_cnts > 0 else False,
            'lazy_submit_session': other_args['session'],
            'lazy_publish_cnts': self.publish_cnts,

            'deadline_batchname': re.sub('[.][^.]*', '', assetdbutils.labelpostfix()),
        }

        if included_parts == [] and self.set_presets is not None:
            tmpfile = assetutils.get_publish_tempfilename('postproc_set.yaml')
            print ('postproc_set: ', tmpfile.replace('/', '\\'))

            var = cypyapiutils.Variable('PostProcSetEditor_PresetWindow', toolgroup='Maya')
            from postproc_set_editor import ui_preset
            presets = ui_preset.get_presets(var.var)
            for k in list(presets.keys()):
                if k not in  self.set_presets:
                    presets.pop(k)

            with open(tmpfile, 'w') as hd:
                yaml.dump({'presets':presets}, hd)

            _args = {
                    'preset_file': tmpfile,
                    'dryrun': True, 
                }

            args['postproc_set_file'] = tmpfile
            args['publish_parts_parts'] = self.set_presets



        if 'background_subprocess' in other_args:
            args['background_subprocess'] = other_args['background_subprocess']


        wfile = {'local_master_path':source_filename, 'version':version}
        
        self.additional_args(args)

        task = wcmds.PublishTask(asset, tags, wfile, comment, args, scene_file=source_filename)
        res = task.execute(silent=True)
        print('res: ', res)

        return True

    def is_valid_part(self, part, asset, tags):
        raise Exception('Override in derived class: is_valid_part')

def get_specific_presets(set_names, toolgroup):
    var = cypyapiutils.Variable('PostProcSetEditor_PresetWindow', toolgroup=toolgroup)
    from postproc_set_editor import ui_preset
    presets = ui_preset.get_presets(var.var)
    for k in list(presets.keys()):
        if k not in set_names:
            presets.pop(k)
    
    return presets

def write_specific_presets_to_tempfile(set_names, toolgroup):
    tmpfile = assetutils.get_publish_tempfilename('postproc_set.yaml')
    presets = get_specific_presets(set_names, toolgroup)
    with open(tmpfile, 'w') as hd:
        yaml.dump({'presets':presets}, hd)

    return tmpfile

expr_set = r'^createNode objectSet -n "([^"]+)"'
expr_attr = r'^\s*setAttr .*".postproc_edit_set__name".*"string" "([^"]*)"'

class PartsSelector(QtWidgets.QWidget):
    def __init__(self, args, plugin, sources, asset_org, comment='', commit=True, parent_window=None):
        super(PartsSelector, self).__init__()
        self.args = args
        self.plugin = plugin
        self.parent_window = None
        self.parts = []
        self.filename_to_parts = {}

        self.readers = []

        for filename, tags, _, leafname, localid in sources:
            asset = copy.deepcopy(asset_org)
            asset.leafname = leafname
            asset.localid = localid
            out_config = asset.check_output_config(tags=tags)
            asset.path_template = asset.evaluate_output(out_config, proc_token=False, proc_tag=True, tags=tags)

            reader = plugin.get_reader(filename)
            self.readers.append(reader)

            sets_ = reader.get_sets()
            self.filename_to_parts[filename] = [x[1] for x in sets_]
            for part in [x[1] for x in sets_]:
                if part not in [x[0] for x in self.parts]:
                    self.parts.append((part, self.plugin.is_valid_part(part, asset, tags)))

        vbox = QtWidgets.QVBoxLayout(self)
        from workfile_manager.ui import uiutils_2
        self.splt = splt = uiutils_2.Splitter(QtCore.Qt.Vertical, parent=self, prefs=ui_main.mwin.ui_prefs)
        splt.setObjectName('publish_parts_splitter')
        vbox.addWidget(splt)

        w1 = QtWidgets.QWidget(splt)
        vbox1 = QtWidgets.QVBoxLayout(w1)
        #
        if len(self.readers) == 1:
            lb = QtWidgets.QLabel(u'Post-process sets: （※ダブルクリックで内容を確認）')
        else:
            lb = QtWidgets.QLabel(u'Post-process sets:')

        lb.setAlignment(QtCore.Qt.AlignLeft)
        vbox1.addWidget(lb)

        self.lw = QtWidgets.QListWidget()
        self.lw.setMinimumHeight(5)
        self.lw.setIconSize(QtCore.QSize(0, 0))
        self.lw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        if len(self.readers) == 1:
            self.lw.itemDoubleClicked.connect(self.open_content_viewer)
        self.lw.itemSelectionChanged.connect(self.changed)

        vbox1.addWidget(self.lw)

        #
        w2 = QtWidgets.QWidget(splt)
        vbox2 = QtWidgets.QVBoxLayout(w2)
        hbox_use_preset = QtWidgets.QHBoxLayout()

        self.lb_use_preset = lb_use_preset = QtWidgets.QLabel('Preset to be used if no sets exist: ')
        self.cmb_use_preset = QtWidgets.QComboBox()
        
        hbox_use_preset.addWidget(lb_use_preset)
        hbox_use_preset.addWidget(self.cmb_use_preset, 1)

        vbox2.addLayout(hbox_use_preset)
        self.preset_lw = QtWidgets.QListWidget()
        self.preset_lw.setMinimumHeight(5)
        self.preset_lw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.preset_lw.itemSelectionChanged.connect(self.multi_preset_changed)
        vbox2.addWidget(self.preset_lw)

        

        #
        w3 = QtWidgets.QWidget(splt)
        vbox3 = QtWidgets.QVBoxLayout(w3)

        self.cb_use_op = QtWidgets.QCheckBox('Only specific operators')
        vbox3.addWidget(self.cb_use_op)
        
        if 'publish-only-specific-operators' in ui_main.mwin.ui_prefs.var['miscellaneous']:
            only_spc_op = ui_main.mwin.ui_prefs.var['miscellaneous']['publish-only-specific-operators']
        else:
            only_spc_op = False

        self.cb_use_op.setCheckState(QtCore.Qt.Checked if only_spc_op else QtCore.Qt.Unchecked)

        self.lw2 = QtWidgets.QListWidget()
        #self.lw2.setMinimumHeight(5)
        self.lw2.setIconSize(QtCore.QSize(0, 0))
        self.lw2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lw2.itemSelectionChanged.connect(self.op_selection_changed)

        self.cb_use_op.stateChanged.connect(self.use_op_changed)
        self.use_op_changed(0 if not only_spc_op else 2)
        vbox3.addWidget(self.lw2, 1.5)


        #
        w4 = QtWidgets.QWidget(splt)
        vbox4 = QtWidgets.QVBoxLayout(w4)

        vbox4.addWidget(QtWidgets.QLabel('Comment:'))
        self.te_comment = QtWidgets.QTextEdit()
        self.te_comment.setMinimumHeight(5)
        self.te_comment.setText(comment)
        vbox4.addWidget(self.te_comment, 1)

        #
        hbox = QtWidgets.QHBoxLayout()
        self.btn_comment_from_work = QtWidgets.QPushButton('Load comment from workfile.')
        self.btn_comment_from_work.clicked.connect(self.load_comment)
        self.btn_clear_comment = QtWidgets.QPushButton()
        icon = QtGui.QIcon(':/icons/trash.png')
        self.btn_clear_comment.setIcon(icon)
        self.btn_clear_comment.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_comment.setFixedWidth(30)
        self.btn_clear_comment.clicked.connect(self.clear_comment)
        vbox4.addLayout(hbox)
        
        hbox.addWidget(self.btn_comment_from_work)
        hbox.addWidget(self.btn_clear_comment)


        self.commit = QtWidgets.QCheckBox('Commit to engine')
        self.commit.setChecked(commit)
        self.keep_im = QtWidgets.QCheckBox('Keep intermediates (for debug)')

        vbox4.addWidget(self.commit)
        vbox4.addWidget(self.keep_im)

        self.reload_set_preset() # must call before signal connections built.
        self.cmb_use_preset.currentIndexChanged.connect(self.set_preset_changed)
        splt.restore()
        
    def validity_check_func(self):
        comment = self.te_comment.toPlainText().strip()
        if comment == '':
            d = uiutils.PromptDialog('Confirmation', u'コメントを入力してください。', btns=['OK']).exec_()
            return False
        
        return True

    def set_preset_changed(self, idx):
        ui_main.mwin.ui_prefs.var['miscellaneous']['preset_if_no_sets'] = idx
        ui_main.mwin.ui_prefs.save()
        self.changed()

    def multi_preset_changed(self):
        self.changed()


    def reload_set_preset(self):
        from postproc_set_editor import ui_preset

        items = ["<don't use any preset>"]

        var = cypyapiutils.Variable('PostProcSetEditor_PresetWindow', toolgroup='Maya')
        presets = ui_preset.get_presets(var.var)
        if presets is None:
            presets = {}

        self.cmb_use_preset.addItems(items + [x for x in presets.keys()])

        try:
            idx = ui_main.mwin.ui_prefs.var['miscellaneous']['preset_if_no_sets']
            if idx >= self.cmb_use_preset.count():
                idx = 0
        except:
            idx = 0
        
        self.cmb_use_preset.setCurrentIndex(idx)

        #
        self.preset_lw.addItems(sorted([x for x in presets.keys()]))

        #
        multi_preset = False
        try:
            if ui_main.mwin.ui_prefs.var['miscellaneous']['allow-multi-def-set-presets']:
                multi_preset = ui_main.mwin.ui_prefs.var['miscellaneous']['allow-multi-def-set-presets']
        except:
            pass
        self.cmb_use_preset.setVisible(not multi_preset)
        self.preset_lw.setVisible(multi_preset)
        self.multi_preset = multi_preset


    def open_content_viewer(self):
        try:
            set_ = [x.text() for x in self.lw.selectedItems()][0]
        except:
            return

        if hasattr(self.parent_window, 'content_viewer'):
            try:
                self.parent_window.content_viewer.parent_window.close()
            except:
                pass

        w = ContentViewer(reader=self.readers[0], partname=set_)
        #win = uiutils.PromptDialog('Post-process set:   %s' % set_, '', wd=w, btns=['OK'])
        #win.resize(750, 450)
        #win.exec_()
        self.win = win = uiutils.PromptWindow(mwin=self.parent_window, title='Post-process set:   %s' % set_, wd=w, 
                                    btns=[('Close', QtWidgets.QDialogButtonBox.RejectRole, self.close_content_viewer)], 
                                    resume_as_name='set_detail_window')
        w.parent_window = win

        win.resize(750, 450)
        win.show()
        self.parent_window.content_viewer = w

    def close_content_viewer(self):
        self.win.close()
        

    def load_comment(self):
        self.te_comment.setText(self.args['work_comment'])

    def clear_comment(self):
        self.te_comment.setText('')

    def changed(self):
        selected_sets = self.lw.selectedItems()
        parts = [x.text() for x in selected_sets]
        ops = []
        for reader in self.readers:
            buf = reader.get_operators(parts)
            ops += [x[0] for x in buf]
        #print(ops)
        
        if not hasattr(self, 'mute_op_selection_changed') or not self.mute_op_selection_changed:
            self.lw2.clear()
            ops = list(set(ops))
            self.lw2.addItems(ops)
            self.lw2.selectAll()

        if self.parent_window is not None:
            en = False
            if self.lw.currentRow() < 0:
                valid = True
            else:
                try:
                    part, valid  = self.parts[self.lw.currentRow()]
                except:
                    valid = True
            if valid:
                if len(selected_sets) > 0 or (self.cmb_use_preset.currentIndex() > 0 or len(self.preset_lw.selectedIndexes())>0):
                    if not self.cb_use_op.isChecked() or len(self.lw2.selectedIndexes()) > 0:
                        en = True
            for i in [0,1]:
                self.parent_window.btn_widgets[i].setEnabled(en)
            self.parent_window.btn_widgets[0].setEnabled(False) # Temporally local test functionality disabled.

        if len(parts) > 0 and hasattr(self.parent_window, 'content_viewer'):
            self.parent_window.content_viewer.reload(parts[0])
            
        
    def op_selection_changed(self):
        if hasattr(self, 'mute_op_selection_changed') and self.mute_op_selection_changed:
            return
        self.mute_op_selection_changed = True
        self.changed()
        self.mute_op_selection_changed = False
        

    def use_op_changed(self, state):
        v = True if state>0 else False
        self.lw2.setVisible(v)
        ui_main.mwin.ui_prefs.var['miscellaneous']['publish-only-specific-operators'] = v
        ui_main.mwin.ui_prefs.save()
        self.changed()

    def reload(self, idx=[]):
        self.lw.clear()
        for _, (part, valid) in enumerate(self.parts):
            item = QtWidgets.QListWidgetItem()
            item.setData(0, part + (' (Invalid)' if not valid else ''))
            item.setData(1, part)
            item.setData(3, valid)
            if not valid:
                item.setForeground(QtGui.QBrush(QtGui.QColor(128, 128, 128)))
            self.lw.addItem(item)

        for id in idx:
            if id < self.lw.count():
                self.lw.setCurrentRow(id, QtCore.QItemSelectionModel.Toggle)            
        self.changed()
        
class GroupBox(QtWidgets.QGroupBox):
    def __init__(self, label):
        super(GroupBox, self).__init__(label)
        self.setStyleSheet(
            'QGroupBox {font-weight: bold;border: 1px solid grey;' + \
                'border-radius: 4px;padding: 4px;margin-top: 8px;} ' + \
            'QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top left;' + \
                'left: 20px;padding-left: 3px;padding-right: 5px;' + \
                'padding-top: 0px;padding-bottom: 16px;}'
        )

class ContentViewer(QtWidgets.QWidget):
    def __init__(self, parent=None, reader=None, partname=None):
        super(ContentViewer, self).__init__(parent)
        self.reader = reader
        self.partname = partname
        vbox = QtWidgets.QVBoxLayout(self)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox, 1)

        #
        gb = GroupBox('Linked objects:')
        hbox.addWidget(gb)
        
        vbox_linked = QtWidgets.QVBoxLayout(gb)
        gb.setLayout(vbox_linked)
        self.lw_linked = lw_linked = QtWidgets.QListWidget()
        self.lw_linked.setEnabled(False)
        vbox_linked.addWidget(lw_linked)

        #
        gb = GroupBox('Operators:')
        hbox.addWidget(gb)
        
        vbox_ops = QtWidgets.QVBoxLayout(gb)
        gb.setLayout(vbox_ops)
        hbox_ops = QtWidgets.QHBoxLayout()
        vbox_ops.addLayout(hbox_ops, 1)
        vbox_ops_l = QtWidgets.QVBoxLayout()
        vbox_ops_r = QtWidgets.QVBoxLayout()
        hbox_ops.addLayout(vbox_ops_l)
        hbox_ops.addLayout(vbox_ops_r)

        
        self.lw_ops = lw_ops = QtWidgets.QListWidget()
        self.lw_ops.currentRowChanged.connect(self.operator_selected)
        vbox_ops_l.addWidget(lw_ops, 1)

        self.cl_opprm = QtWidgets.QVBoxLayout()
        self.setStyleSheet('QWidget:disabled {color: #c0c0c0;}')

        vbox_ops_l.addLayout(self.cl_opprm)

        vbox_ops_r.addWidget(QtWidgets.QLabel('Targets:'))
        self.lw_targets = lw_targets = QtWidgets.QListWidget()
        self.lw_targets.setEnabled(False)
        vbox_ops_r.addWidget(lw_targets, 1)

        self.reload_linkedobjs()
        self.reload_operators()

    def reload(self, partname=None):
        if partname is not None:
            self.partname = partname
        self.reload_linkedobjs()
        self.reload_operators()


    def reload_linkedobjs(self):
        self.lw_linked.clear()
        objs = self.reader.get_linked_objects(self.partname)
        if len(objs) > 0:
            self.lw_linked.addItems(objs)

    def reload_operators(self, index=None):
        self.lw_ops.clear()
        ops = self.reader.get_operators([self.partname])
        if len(ops) > 0:
            self.lw_ops.addItems([x[0] for x in ops])
            self.lw_ops.setCurrentRow(0)

        self.refresh_op_parameters()

    def operator_selected(self, row):
        self.reload_targets(row)
        self.refresh_op_parameters(row)

    def reload_targets(self, row):
        self.lw_targets.clear()
        try:
            opname = self.lw_ops.item(row).text()
        except:
            return
        targets = self.reader.get_set_members(opname)
        if len(targets) > 0:
            self.lw_targets.addItems(targets)

    def delete_hie(self, w):
        if w is None:
            return

        if issubclass(type(w), QtWidgets.QWidget):
            w.setParent(None)
        elif type(w) is QtWidgets.QWidgetItem:
            w.widget().setParent(None)
        else:
            cnt = w.count()
            for _ in range(cnt):
                self.delete_hie(w.itemAt(0))
            w.setParent(None)
        del w

    def refresh_op_parameters(self, row=None):
        for _ in range(self.cl_opprm.count()):
            self.delete_hie(self.cl_opprm.itemAt(0))

        try:
            if row is None:
                opsetname = self.lw_ops.selectedItems()[0].text()
            else:
                opsetname = self.lw_ops.item(row).text()
        except:
            return

        from postproc_set_editor import ui_main, operator # must import operator to set operators variable.
        import functools
        optype = self.reader.get_set_attribute(opsetname, 'postproc_edit_set__operator_name')
        

        ui_main.load_operator_params(optype, functools.partial(self.reader.get_set_attribute, opsetname), self.cl_opprm, self, editable=False)

        