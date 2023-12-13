# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    import maya.cmds as cmds
    import maya.mel as mel
    
except:
    pass

from workfile_manager import cmds as wcmds, p4utils, postproc_utils
from workfile_manager.ui import uiutils, ui_main, ui_table
from workfile_manager.plugin_utils import PostProcBase, PluginType, Application, AssetAction
from cylibassetdbutils import assetdbutils, assetutils
import workfile_manager.deadline_submit as dls


from Qt import QtWidgets, QtCore, QtGui
import re
import os
import yaml
import subprocess

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()

default_xml = 'W:/production/tools/maya/scripts/rig/convert/hik/data/world/male00/joints.xml'

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
        return 'Update maya workfiles and plot'

    
    def annotation(self):
        return u'Mayaワークファイルのリグを更新してアニメーションをプロットします'

    def allow_multi_items(self):
        return True

    def reload_table(self):
        return False

    def execute(self, args):
        self.table = args['table']
        
        try:
            ui_main.rig_selector.close()
        except:
            pass
        
        from workman_world_custom.asset_actions.maya import generate_rig_anim_work
        from workman_world_custom.asset_actions.maya import bake_to_rig
        self.other_option_ui = aw = generate_rig_anim_work.AdditionalWidget()
        self.other_option_ui.rb_target_maya.setChecked(True)
        self.other_option_ui.rb_target_all.setEnabled(False)
        self.other_option_ui.rb_target_mbuilder.setEnabled(False)

        self.selector = bake_to_rig.RigSelector(args, aw=self.other_option_ui)
        aw.init(self.selector)
        self.other_option_ui.cmb_variant.cmb.setCurrentIndex(self.other_option_ui.cmb_variant.cmb.findText('rig'))
        
        bake_to_rig.add_advance_tab(self.selector)

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


        ui_main.rig_selector = mw = uiutils.PromptWindow(mwin=self.table.mwin, title='Update workfiles and plot', wd=self.selector, 
                                    btns=[
                                        ('Submit', QtWidgets.QDialogButtonBox.AcceptRole, self._execute),
                                        ('Cancel', QtWidgets.QDialogButtonBox.RejectRole, None)
                                        ], resume_as_name='RigSelector')
        mw.show()

        

        return True


    def _execute(self):
        anim_xml_filepath = self.selector.anim_xml_field.le.text()
        self.table.mwin.var.replace('bake_to_rig__anim_skl_xml', anim_xml_filepath)
        rig_xml_filepath = self.selector.rig_xml_field.le.text()
        self.table.mwin.var.replace('bake_to_rig__rig_skl_xml', rig_xml_filepath)
        default_skeleton_filepath = self.selector.default_skeleton_field.le.text()
        self.table.mwin.var.replace('bake_to_rig__default_rig_skeleton', default_skeleton_filepath)
        self.table.mwin.var.save()

        self.asset = None
        self.filename = None
        data = self.selector.cmb_his.itemData(self.selector.cmb_his.currentIndex())
        self.selector.add_history(*data)
        rig_filename = data[0]

        self.mes = []

        anim_files = {}
        deps = []
        deadline_batchname = re.sub('[.][^.]*', '', assetdbutils.labelpostfix())

        filenames = [self.selector.lw.item(x)._asset._filename for x in range(self.selector.lw.count())]
        conds = ' or '.join(['path="%s"' % x for x in filenames])
        q = 'select path, source from sharedasset_version_master_02 where %s' % conds
        db.cs_execute(q)
        res = db.cs.fetchall()
        print('res:', res)

        src_to_share = {}
        for r in res:
            if self.other_option_ui.rb_target_maya.isChecked():
                if not r['source'].endswith('.ma'):
                    continue
            elif self.other_option_ui.rb_target_mbuilder.isChecked():
                if not r['source'].endswith('.fbx'):
                    continue
            src_to_share[r['source']] = r['path']
        print('src_to_share:', src_to_share)

        items = []
        for src in src_to_share.keys():
            filename = src_to_share[src]
            idx = filenames.index(filename)
            items.append(self.selector.lw.item(idx))

        output_subcategory = self.other_option_ui.cmb_subcategory.current_text()
        output_assetname = self.other_option_ui.cmb_assetname.current_text()
        output_variant = self.other_option_ui.cmb_variant.current_text()
        output_overrides = {'subcategory':output_subcategory, 'assetname':output_assetname, 'variant':output_variant}

        for item in items:
            asset = item._asset
            print('item._asset: ', item._asset.get_dict())
            if output_subcategory is not None:
                asset.subcategory = output_subcategory
            if output_assetname is not None:
                asset.assetname = output_assetname
            if output_variant is not None:
                asset.variant = output_variant
            asset.version = 0 # To avoid failing in get_exportname()

            comment = 'Updated with AssetAction\n' + 'Source:' + asset._filename
            
            thumb_src = assetutils.Asset.thumbnail_filepath(asset._filename, asset._version, replace_share_root=False)
            pb_src = re.sub('[.][^.]+$', '.avi', thumb_src)
            if asset._dictdata['frame_start'] is None or asset._dictdata['frame_end'] is None or asset._dictdata['frame_rate'] is None:
                self.mes.append('[ERROR] framerange not found: '+ asset._filename)
                continue

            tmp_output = assetutils.get_publish_tempfilename(asset._filename)

            args = {
                'export_all': True, 
                'export_only': False,
                'submit_server': True,
                'postproc': [postproc_utils.find_proc_by_name('postproc_update_plot_rig_anim_work', plugin_type=PluginType.PublishPostProcess)], 
                'preproc': [],
                'procs': [], 
                'user': p4u.p4.user,
                'commit_to_engine': False,
                'keep_intermediate': False,
                'rig_file': rig_filename,
                'animation_file': asset._filename,
                'thumbnail_source': thumb_src, 
                'frame_range': (asset._dictdata['frame_start'], asset._dictdata['frame_end']),
                'frame_rate': asset._dictdata['frame_rate'],
                'is_custom_task': True,
                'tmp_output': tmp_output,
                'deadline_batchname': deadline_batchname,
                'comment':comment,
                'anim_skeleton_xml': anim_xml_filepath,
                'rig_skeleton_xml': rig_xml_filepath,
                'default_rig_skeleton': default_skeleton_filepath,
                'output_overrides': output_overrides,
            }
            
            anim_files[tmp_output] = {'asset':asset.get_dict(), 'tags':asset._tags, 'filename':asset._filename}
            wfile = {'share_filepath':asset._filename, 'version':asset._version}
            
            print('rig:', rig_filename)
            print('asset:', asset.get_dict())

            task = wcmds.PublishTask(asset, asset._tags, wfile, comment, args, scene_file=rig_filename)
            res = task.execute(silent=True)
            if res:
                self.filename, _ = res
            self.asset = asset
            if task.last_deadline_jobid is not None:
                deps.append(task.last_deadline_jobid)


        # Submit a deadline job that collects all workfiles and saves those.
        anim_list_filename = assetutils.get_publish_tempfilename('generate_rig_anim.yaml')
        print('anim_list_filename: ', anim_list_filename)
        with open(anim_list_filename, 'w') as fhd:
            fhd.write(yaml.dump(anim_files))

        from workman_world_custom.asset_actions.maya import generate_rig_anim_work
        generate_rig_anim_work.register_commit_job(anim_list_filename, deps, deadline_batchname, comment, output_overrides=output_overrides)
        
        #####
        uiutils.PromptDialog('Confirmation', u'ワークファイル生成ジョブを投げました。', btns=['OK']).exec_()

        if len(self.mes) > 0:
            w = QtWidgets.QListWidget()
            for m in self.mes:
                w.addItem(m)

            d = uiutils.PromptDialog('Confirmation', u'下記のアセットはスキップされました。', wd=w, btns=['OK'])
            d.resize(1000, 400)
            d.exec_()



