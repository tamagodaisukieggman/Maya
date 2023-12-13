# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    import maya.cmds as cmds
    import maya.mel as mel
    
except:
    pass

from workman_world_custom.asset_actions.all import uiutils as aa_uiutils
from workfile_manager import cmds as wcmds, p4utils, postproc_utils
from workfile_manager.ui import uiutils, ui_main, ui_table
from workfile_manager.plugin_utils import PostProcBase, PluginType, Application, AssetAction
from cylibassetdbutils import assetdbutils, assetutils

from Qt import QtWidgets, QtCore, QtGui
import re
import os

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()

default_xml = 'c:/cygames/wiz2/tools/maya/scripts/rig/convert/hik/data/world/male00/joints.xml'
default_src_skeleton = 'c:/cygames/wiz2/tools/maya/scripts/rig/convert/hik/data/world/male00/joints.ma'

class RigSelector(aa_uiutils.AssetSelector):
    def is_base_asset_valid(self, asset):
        if asset.area() != 'share' :
            uiutils.PromptDialog('Error', 'Select an asset in share area.', btns=['OK']).exec_()
            return False
        elif asset.task != 'model':
            uiutils.PromptDialog('Error', 'Select an model asset.', btns=['OK']).exec_()
            return False
        return True
    
    def base_asset_history_varname(self):
        return 'bake_to_rig__history'


class FileField(QtWidgets.QWidget):
    def __init__(self, label, default=None, fmt='xml'):
        super(FileField, self).__init__()
        self.default = default
        self.fmt = fmt
        hbox = QtWidgets.QHBoxLayout(self)
        self.lb = QtWidgets.QLabel(label)
        hbox.addWidget(self.lb)
        self.le = QtWidgets.QLineEdit()
        hbox.addWidget(self.le, 1)
        self.open_btn = open_btn = QtWidgets.QPushButton()
        icon = QtGui.QIcon(':/icons/folder2.png')
        open_btn.setIcon(icon)
        open_btn.setFixedHeight(28)
        open_btn.clicked.connect(self.browse)
        hbox.addWidget(open_btn)

        self.reset_btn = reset_btn = QtWidgets.QPushButton('Reset')
        reset_btn.setFixedHeight(28)
        reset_btn.clicked.connect(self.reset_path)
        hbox.addWidget(reset_btn)
    
    def set_filepath(self, value):
        self.le.setText(value)
    
    def reset_path(self):
        if self.default is not None:
            self.le.setText(self.default)

    def browse(self):
        current_path = self.le.text().replace('/', '\\')
        res = QtWidgets.QFileDialog.getOpenFileName(ui_main.mwin, '', current_path, '*.'+self.fmt)
        filepath = res[0]
        if filepath == '':
            return
        print('filepath:', filepath)
        self.le.setText(filepath)

    def set_enabled(self, v):
        self.lb.setEnabled(v)
        self.le.setEnabled(v)
        self.open_btn.setEnabled(v)
        self.reset_btn.setEnabled(v)


def add_advance_tab(selector):
    w = QtWidgets.QWidget()
    vbox = QtWidgets.QVBoxLayout(w)
    selector.anim_xml_field = FileField('Animation skeleton xml:', default=default_xml)
    vbox.addWidget(selector.anim_xml_field)
    selector.rig_xml_field = FileField('Rig skeleton xml:', default=default_xml)
    vbox.addWidget(selector.rig_xml_field)
    selector.default_skeleton_field = FileField('Default skeleton for rig:', default=default_src_skeleton, fmt='ma')
    vbox.addWidget(selector.default_skeleton_field)
    lb = QtWidgets.QLabel(u'\t※元ワークファイルがモーションビルダーの場合に、ベイク元スケルトンとして使用されます。')
    vbox.addWidget(lb)
    vbox.addWidget(QtWidgets.QWidget(), 1)
    selector.tab.addTab(w, 'Advance')

    try:
        if ui_main.mwin.dccutils().get_instance().application() != Application.MotionBuilder:
            selector.default_skeleton_field.set_enabled(False)
            lb.setEnabled(False)
    except:
        pass


class Plugin(AssetAction):
    def apps_executable_on(self):
        return [Application.Maya,
            Application.MotionBuilder, 
            Application.UnrealEngine, 
            Application.Houdini,
            Application.Standalone,
            ]

    def is_asset_eligible(self, asset):
        if asset.area() != 'share':
            return False
        if asset.assetgroup != 'character':
            return False
        if asset.task != 'animation':
            return False
        if asset.variant != 'default':
            return False

        return True

    def getlabel(self):
        return 'Bake to controller'

    def allow_multi_items(self):
        return True

    def execute(self, args):
        self.table = args['table']
        
        try:
            ui_main.rig_selector.close()
        except:
            pass
        
        from workman_world_custom.asset_actions.maya import generate_rig_anim_work
        self.other_option_ui = aw = generate_rig_anim_work.AdditionalWidget()
        self.other_option_ui.rb_target_all.setChecked(True)
        self.other_option_ui.rb_target_maya.setEnabled(False)
        self.other_option_ui.rb_target_mbuilder.setEnabled(False)
        
        self.selector = RigSelector(args, aw=aw)
        aw.init(self.selector)
        try:
            self.other_option_ui.cmb_variant.cmb.setCurrentIndex(self.other_option_ui.cmb_variant.cmb.findText('rig'))
        except:
            pass
        add_advance_tab(self.selector)

        
        if self.table.mwin.var.contains_variable('bake_to_rig__anim_skl_xml'):
            xml = self.table.mwin.var.get('bake_to_rig__anim_skl_xml')
        else:
            xml = default_xml
        self.selector.anim_xml_field.set_filepath(xml)

        if self.table.mwin.var.contains_variable('bake_to_rig__rig_skl_xml'):
            xml = self.table.mwin.var.get('bake_to_rig__rig_skl_xml')
        else:
            xml = default_xml
        self.selector.rig_xml_field.set_filepath(xml)

        if self.table.mwin.var.contains_variable('bake_to_rig__default_rig_skeleton'):
            def_skl = self.table.mwin.var.get('bake_to_rig__default_rig_skeleton')
        else:
            def_skl = default_src_skeleton
        self.selector.default_skeleton_field.set_filepath(def_skl)

        ui_main.rig_selector = mw = uiutils.PromptWindow(mwin=self.table.mwin, title='Bake to controller', wd=self.selector, 
                                    btns=[
                                        ('Submit', QtWidgets.QDialogButtonBox.AcceptRole, self._execute),
                                        ('Cancel', QtWidgets.QDialogButtonBox.RejectRole, None)
                                        ], resume_as_name='bake_to_rig')
        mw.resize(700, 600)
        mw.show()

        return True

    def all_finished(self):
        pass

    def loop(self, thread):
        thread.set_maximum.emit(self.selector.lw.count())
        prev = 0
        while self.cnt < self.selector.lw.count():
            if self.cnt > prev:
                thread.value_changed.emit(self.cnt)
                prev = self.cnt
            


    def _execute(self):
        anim_xml_filepath = self.selector.anim_xml_field.le.text()
        self.table.mwin.var.replace('bake_to_rig__anim_skl_xml', anim_xml_filepath)
        rig_xml_filepath = self.selector.rig_xml_field.le.text()
        self.table.mwin.var.replace('bake_to_rig__rig_skl_xml', rig_xml_filepath)
        default_skeleton_filepath = self.selector.default_skeleton_field.le.text()
        self.table.mwin.var.replace('bake_to_rig__default_rig_skeleton', default_skeleton_filepath)
        self.table.mwin.var.save()

        output_subcategory = self.other_option_ui.cmb_subcategory.current_text()
        output_assetname = self.other_option_ui.cmb_assetname.current_text()
        output_variant = self.other_option_ui.cmb_variant.current_text()

        self.asset = None
        self.filename = None
        data = self.selector.cmb_his.itemData(self.selector.cmb_his.currentIndex())
        self.selector.add_history(*data)
        rig_filename = data[0]

        self.mes = []

        sw = uiutils.Stopwatch(force=False)
        sw.reset()

        assets = [self.selector.lw.item(x)._asset for x in range(self.selector.lw.count())]
        _all_tags = db.get_assigned_tags_for_assets_3(assets)
        all_tags = {}
        for n in _all_tags:
            key = (n['leafname'], n['localid'], assetdbutils.normalize_path(n['path_template']))
            if key not in all_tags:
                all_tags[key] = []
            all_tags[key].append(n)

        for idx in range(self.selector.lw.count()):
            sw.reset()
            item = self.selector.lw.item(idx)
            asset = item._asset
            if output_subcategory is not None:
                asset.subcategory = output_subcategory
            if output_assetname is not None:
                asset.assetname = output_assetname
            if output_variant is not None:
                asset.variant = output_variant

            comment = '[Baked] Rig: %s' % rig_filename.replace('/', '\\')
            
            thumb_src = assetutils.Asset.thumbnail_filepath(asset._filename, asset._version, replace_share_root=False)
            pb_src = re.sub('[.][^.]+$', '.avi', thumb_src)
            if asset._dictdata['frame_start'] is None or asset._dictdata['frame_end'] is None or asset._dictdata['frame_rate'] is None:
                self.mes.append('[ERROR] framerange not found: '+ asset._filename)
                continue
            sw.elapse('x1')
            args = {
                'export_all': True, 
                'export_only': False,
                'submit_server': True,
                'postproc': postproc_utils.get_postprocs(asset, ui_main.mwin, only_enabled=True, plugin_type=PluginType.PublishPostProcess,
                                includes=['postproc_bake_to_rig', 'maya.animation.postproc_plot', 'create_playblast'],
                                excludes=['postproc_edit_set']),
                'preproc': [],
                'procs': [], 
                'user': p4u.p4.user,
                'commit_to_engine': False,
                'keep_intermediate': True,
                'animation_file': asset._filename,
                'thumbnail_source': thumb_src, 
                'frame_range': (asset._dictdata['frame_start'], asset._dictdata['frame_end']),
                'frame_rate': asset._dictdata['frame_rate'],
                'deadline_batchname': re.sub('[.][^.]*', '', assetdbutils.labelpostfix()),
                'anim_skeleton_xml': anim_xml_filepath,
                'rig_skeleton_xml': rig_xml_filepath,
                'default_rig_skeleton': default_skeleton_filepath,
            }

            if os.path.exists(pb_src):
                args['playblast_source'] = pb_src
            

            wfile = {'share_filepath':asset._filename, 'version':asset._version}
            
            task = wcmds.PublishTask(asset, asset._tags, wfile, comment, args, scene_file=rig_filename, tag_cache=all_tags)
            sw.elapse('x2')
            res = task.execute(silent=True, refresh_ui=False)
            sw.elapse('x3')
            if res:
                self.filename, _ = res
            self.asset = asset

        try:
            self.table.mwin.tag_tree_reload_done()
        except:
            pass

        uiutils.PromptDialog('Confirmation', u'ベイクジョブを投げました。', btns=['OK']).exec_()
        self.finished()

    def finished(self):
        if len(self.mes) > 0:
            w = QtWidgets.QListWidget()
            for m in self.mes:
                w.addItem(m)

            d = uiutils.PromptDialog('Confirmation', u'下記のアセットはスキップされました。', wd=w, btns=['OK'])
            d.resize(1000, 400)
            d.exec_()

        if not self.filename:
            return

        uiutils.goto_asset(self.filename, self.asset)