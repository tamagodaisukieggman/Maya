# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    import maya.cmds as cmds
    import maya.mel as mel
    
except:
    pass

from workman_world_custom.asset_actions.all import uiutils as aa_uiutils
from workfile_manager import cmds as wcmds, p4utils, postproc_utils
from workfile_manager.ui import uiutils, ui_main
from workfile_manager.plugin_utils import PluginType, Application, AssetAction
from cylibassetdbutils import assetdbutils, assetutils

from Qt import QtWidgets, QtCore, QtGui
import re
import os

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()

class BaseMotionSelector(aa_uiutils.AssetSelector):
    def is_base_asset_valid(self, asset):
        if asset.area() != 'share' :
            uiutils.PromptDialog('Error', 'Select an asset in share area.', btns=['OK']).exec_()
            return False
        elif asset.task != 'animation':
            uiutils.PromptDialog('Error', 'Select an animation asset.', btns=['OK']).exec_()
            return False
        return True

    def base_asset_history_varname(self):
        return 'publish_additive_motion__history'

class Plugin(AssetAction):
    def apps_executable_on(self):
        return [Application.Maya,
            Application.MotionBuilder, 
            Application.UnrealEngine, 
            Application.Houdini,
            Application.Standalone,
            ]

    def is_asset_eligible(self, asset):
        if asset.area() != 'work':
            return False
        if asset.assetgroup != 'character':
            return False
        if asset.task != 'animation':
            return False

        return True

    def getlabel(self):
        return 'Publish additve animations'

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
        
        self.selector = BaseMotionSelector(args, aw=aw, base_asset_label='Base animation')
        aw.init(self.selector)
        try:
            self.other_option_ui.cmb_variant.cmb.setCurrentIndex(self.other_option_ui.cmb_variant.cmb.findText('default'))
        except:
            pass

        
        ui_main.rig_selector = mw = uiutils.PromptWindow(mwin=self.table.mwin, title='Publish additive animations', wd=self.selector, 
                                    btns=[
                                        ('Submit', QtWidgets.QDialogButtonBox.AcceptRole, self._execute),
                                        ('Cancel', QtWidgets.QDialogButtonBox.RejectRole, None)
                                        ], resume_as_name='publish_additive_motion')
        mw.resize(700, 600)
        mw.show()

        return True

    def all_finished(self):
        pass


    def _execute(self):
        output_subcategory = self.other_option_ui.cmb_subcategory.current_text()
        output_assetname = self.other_option_ui.cmb_assetname.current_text()
        output_variant = self.other_option_ui.cmb_variant.current_text()

        self.asset = None
        self.filename = None
        data = self.selector.cmb_his.itemData(self.selector.cmb_his.currentIndex())
        self.selector.add_history(*data)
        base_anim_filename = data[0]

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
            workasset = item._asset
            asset = ui_main.mwin.dccutils().get_instance().create_share_anim_asset({})
            asset.__dict__ = workasset.__dict__
            
            print('asset: ', asset._dictdata)
            if output_subcategory is not None:
                asset.subcategory = output_subcategory
            if output_assetname is not None:
                asset.assetname = output_assetname
            if output_variant is not None:
                asset.variant = output_variant

            comment = '[Additive animation] Base: %s' % base_anim_filename.replace('/', '\\')
            print('x1')
            thumb_src = assetutils.Asset.thumbnail_filepath(asset._filename, asset._version, replace_share_root=False)
            print('x2')
            print('thumb_src: ', thumb_src)
            
            pb_src = re.sub('[.][^.]+$', '.avi', thumb_src)
            sw.elapse('x1')
            args = {
                'selection': ['root_jnt'],
                'export_all': True, 
                'export_only': False,
                'submit_server': True,
                'postproc': postproc_utils.get_postprocs(workasset, ui_main.mwin, only_enabled=True, plugin_type=PluginType.PublishPostProcess,
                                includes=['postproc_publish_additive_motion', 'maya.animation.postproc_plot', 'create_playblast'],
                                excludes=['postproc_edit_set', 'postproc_delete_namespace']),
                'preproc': [],
                'procs': [], 
                'user': p4u.p4.user,
                'commit_to_engine': False,
                'keep_intermediate': True,
                #'animation_file': asset._filename,
                'thumbnail_source': thumb_src, 
                'deadline_batchname': re.sub('[.][^.]*', '', assetdbutils.labelpostfix()),
                'base_anim_file': base_anim_filename,
                'inputfile': asset._filename, 
                'frame_range': None,
                'frame_rate': None, 
                #'specified': ['skeleton'], 
                'execute_child_set': True, 
                'keep_references': True, 
                'sync_files': [{'area':'work', 'filename':asset._filename, 'version':asset._version}],
            }

            #if os.path.exists(pb_src):
            #    args['playblast_source'] = pb_src
            
            print('args:', args)
            
            wfile = {'local_master_path':asset._filename, 'version':asset._version}
            print('wfile: ', wfile)
            
            task = wcmds.PublishTask(asset, asset._tags, wfile, comment, args, tag_cache=all_tags)
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

        uiutils.PromptDialog('Confirmation', u'差分アニメーション生成ジョブを投げました。', btns=['OK']).exec_()
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