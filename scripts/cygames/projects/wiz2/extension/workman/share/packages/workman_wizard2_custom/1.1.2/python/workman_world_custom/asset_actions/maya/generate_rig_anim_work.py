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
from workman_world_custom.asset_actions.maya import bake_to_rig
import workfile_manager.deadline_submit as dls


from Qt import QtWidgets, QtCore, QtGui
import re
import os
import yaml
import subprocess
import shutil
import copy

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()

class ComboBoxWidget(QtWidgets.QWidget):
    def __init__(self, asset, layer, parent=None, parent_layer=None, label='', selector=None):
        super(ComboBoxWidget, self).__init__(parent)
        self.layer = layer
        self.parent_layer = parent_layer
        self.child = None
        self.parent = parent
        self.default_value = None
        self.mute = False
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)

        lb = QtWidgets.QLabel(label+':')
        lb.setFixedWidth(100)
        hbox.addWidget(lb)
        self.cmb = cmb = QtWidgets.QComboBox(lb)
        hbox.addWidget(cmb)
        hbox.addWidget(QtWidgets.QWidget(), 1)

        self.asset = copy.deepcopy(asset)
        
        self.cmb.currentIndexChanged.connect(self.item_changed)
        if self.parent_layer is not None:
            self.parent_layer.child = self

        self.reload()

    def current_data(self):
        v = self.cmb.itemData(self.cmb.currentIndex())
        if v is None:
            v = self.cmb.currentText()
        return v

    def current_text(self):
        v = self.cmb.itemData(self.cmb.currentIndex())
        if v is not None:
            return None
        
        return self.cmb.currentText()

    def set_asset(self, asset):
        v = self.current_data()
        
        setattr(asset, self.layer, v)
        if self.parent_layer is not None:
            self.parent_layer.set_asset(asset)

    def reload(self):
        self.mute = True
        if self.parent.selector is not None:
            table_asset = self.parent.selector.lw.item(0)._asset
            self.default_value = getattr(table_asset, self.layer)

        if self.parent_layer is not None:
            self.parent_layer.set_asset(self.asset)
        
        org_value = self.current_text()
        self.cmb.clear()
        parent_tags = ui_main.mwin.parent_tagbar_values_2(self.layer)

        items = db.get_valid_items(ui_main.mwin.tag_tree, self.asset, parent_tags)
        if self.default_value in items:
            self.cmb.addItem("<don't override>", userData=self.default_value)
        
        self.cmb.addItems(items)

        if org_value is not None:
            if org_value in items:
                self.cmb.setCurrentIndex(self.cmb.findText(org_value))
        self.mute = False
        self.item_changed()

    def item_changed(self, index=None):
        if self.mute:
            return
        if self.child is not None:
            self.child.reload()



class AdditionalWidget(QtWidgets.QWidget, object):
    def __init__(self, parent=None):
        super(AdditionalWidget, self).__init__(parent)
        vbox = QtWidgets.QVBoxLayout(self)
        hbox_1 = QtWidgets.QHBoxLayout()
        lb_target = QtWidgets.QLabel('Target:')
        lb_target.setFixedWidth(100)
        self.rb_target_all = rb1 = QtWidgets.QRadioButton('All')
        self.rb_target_maya = rb2 = QtWidgets.QRadioButton('Only from Maya')
        self.rb_target_mbuilder = rb3 = QtWidgets.QRadioButton('Only from Motionbuilder')
        self.selector = None

        hbox_1.addWidget(lb_target)
        hbox_1.addWidget(rb1)
        hbox_1.addWidget(rb2)
        hbox_1.addWidget(rb3, 1)
        vbox.addLayout(hbox_1)

        asset = assetutils.Asset()
        asset.assetgroup = 'character'
        asset.subcategory = None

        self.cmb_subcategory = cmb_subcategory = ComboBoxWidget(label='Sub Category', asset=asset, layer='subcategory', parent=self)
        cmb_subcategory.cmb.setCurrentIndex(cmb_subcategory.cmb.findText('ply'))
        self.cmb_assetname = cmb_assetname = ComboBoxWidget(label='Asset Name', asset=asset, layer='assetname', parent_layer=cmb_subcategory, parent=self)
        self.cmb_variant = cmb_variant = ComboBoxWidget(label='Variant', asset=asset, layer='variant', parent_layer=cmb_assetname, parent=self)

        vbox.addWidget(cmb_subcategory)
        vbox.addWidget(cmb_assetname)
        vbox.addWidget(cmb_variant)

    def init(self, selector):
        self.selector = selector
        self.cmb_subcategory.reload()
        self.cmb_assetname.reload()
        self.cmb_variant.reload()
        self.cmb_subcategory.cmb.setCurrentIndex(0)
        self.cmb_assetname.cmb.setCurrentIndex(0)
        self.cmb_variant.cmb.setCurrentIndex(0)


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
        if asset.variant != 'rig':
            return False

        return True

    def getlabel(self):
        return 'Generate workfile(s)'

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
        
        self.other_option_ui = aw = AdditionalWidget()
        self.other_option_ui.rb_target_all.setChecked(True)
        self.other_option_ui.rb_target_maya.setEnabled(False)
        self.other_option_ui.rb_target_mbuilder.setEnabled(False)

        self.selector = bake_to_rig.RigSelector(args, aw=aw)
        aw.init(self.selector)
        self.other_option_ui.cmb_variant.cmb.setCurrentIndex(self.other_option_ui.cmb_variant.cmb.findText('rig_tmp'))

        ui_main.rig_selector = mw = uiutils.PromptWindow(mwin=self.table.mwin, title='Generate workfiles', wd=self.selector, 
                                    btns=[
                                        ('Submit', QtWidgets.QDialogButtonBox.AcceptRole, self._execute),
                                        ('Cancel', QtWidgets.QDialogButtonBox.RejectRole, None)
                                        ])
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
        self.asset = None
        self.filename = None
        data = self.selector.cmb_his.itemData(self.selector.cmb_his.currentIndex())
        self.selector.add_history(*data)
        rig_filename = data[0]

        self.mes = []

        anim_files = {}
        deps = []
        deadline_batchname = re.sub('[.][^.]*', '', assetdbutils.labelpostfix())

        output_subcategory = self.other_option_ui.cmb_subcategory.current_text()
        output_assetname = self.other_option_ui.cmb_assetname.current_text()
        output_variant = self.other_option_ui.cmb_variant.current_text()
        output_overrides = {'subcategory':output_subcategory, 'assetname':output_assetname, 'variant':output_variant}

        for idx in range(self.selector.lw.count()):
            item = self.selector.lw.item(idx)
            asset = item._asset
            if output_subcategory is not None:
                asset.subcategory = output_subcategory
            if output_assetname is not None:
                asset.assetname = output_assetname
            if output_variant is not None:
                asset.variant = output_variant
            asset.version = 0 # To avoid failing in get_exportname()

            comment = 'Generated with AssetAction\n' + 'Source:' + asset._filename
            
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
                'postproc': [postproc_utils.find_proc_by_name('postproc_generate_rig_anim_work', plugin_type=PluginType.PublishPostProcess)], 
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

        if len(anim_files.keys()) > 0:
            # Submit a deadline job that collects all workfiles and saves those.
            anim_list_filename = assetutils.get_publish_tempfilename('generate_rig_anim.yaml')
            print('anim_list_filename: ', anim_list_filename)
            with open(anim_list_filename, 'w') as fhd:
                fhd.write(yaml.dump(anim_files))
            
            
            register_commit_job(anim_list_filename, deps, deadline_batchname, comment, output_overrides=output_overrides)

            #####
            uiutils.PromptDialog('Confirmation', u'ワークファイル生成ジョブを投げました。', btns=['OK']).exec_()

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


def register_commit_job(anim_list_filename, deps, deadline_batchname, comment, output_overrides):
    from workfile_manager_maya import assetutils_maya
    from cypyapiutils import envutils
    envutilspath = os.path.dirname(envutils.__file__).replace('\\', '/')

    share_asset = assetutils_maya.AnimationAssetMaya()

    args = {}
    env = envutils.save(os.path.dirname(assetutils.get_publish_tempfilename('generate_rig_anim_work_env.yaml')))
    print('envfile: ', env)
    args['envfile'] = env
    args['deadline_batchname'] = deadline_batchname

    args['export_module_name'] = 'workman_world_custom.asset_actions.maya.generate_rig_anim_work'
    args['postproc'] = []
    args['is_custom_task'] = True
    args['anim_list_filename'] = anim_list_filename
    args['comment'] = comment
    args['user'] = p4u.user
    args['output_overrides'] = output_overrides

    cmd = share_asset.get_postproc_cmd(None, args)
    print ('pycmd: ', cmd.replace('/', '\\'))

    rargs = {}
    rargs['command'] = cmd
    rargs['cyclops_app_name'] = os.environ['WM_MAYA_APP']
    rargs['app_version'] = os.environ['WM_MAYA_APP_VERSION']
    rargs['deps'] = deps
    if 'deadline_batchname' in args:
        rargs['deadline_batchname'] = args['deadline_batchname']

    #
    tool_dir = 'c:/cygames/wiz2/tools'
    wmm_ver = os.environ['WORKFILE_MANAGER_MAYA_VERSION']
    batchfile = '%s/projects/world/inhouse/win/extension/maya/share/packages/workfile_manager_maya/%s/python/workfile_manager_maya/export/post_fbx_export.bat' % (tool_dir, wmm_ver)

    from workfile_manager import deadline_submit as dls
    package_version = '""'
    info = {'name':'Commit workfiles', 'username':p4u.p4.user, 'task':share_asset.task, 'comment':'Submit generated workfiles.'}
    dls.submit(info, envutilspath, env, batchfile, rargs, package_version, share_asset, app=Application.Maya)    



def find_source_work(sharefile):
    buf = db.get_sharedasset_from_file(sharefile)
    src = buf[0]['source']
    src_ver = buf[0]['source_version']
    buf = db.get_workasset_versions(filename=src, ignore_path_template=True, version=src_ver)
    return buf[0], src, src_ver
    




def postfunc(presetname=None, argfile=None):
    try:
        execute_commit(presetname, argfile)
    except:
        import traceback
        print(traceback.format_exc())
        import sys
        sys.exit(1)

def execute_commit(presetname=None, argfile=None):
    from workfile_manager_maya import assetutils_maya
    from workfile_manager import dbutils
    from cylibassetdbutils import tag_tree
    from workfile_manager import cmds as wcmds

    print('argfile:', argfile)
    args = wcmds.yaml_load(argfile)

    # Gather files.
    anim_list_filename = args['anim_list_filename']
    print('anim_list_filename: ', anim_list_filename.replace('/', '\\'))
    anim_list = wcmds.yaml_load(anim_list_filename)
    print('anim_list: ', anim_list)
    print('type:', type(anim_list))

    files_to_submit = []
    for tmp_output in anim_list.keys():
        print('tmp_output:', tmp_output.replace('/', '\\'))

        try:
            workasset, src, src_ver = find_source_work(anim_list[tmp_output]['filename'])
        except:
            workasset = None
        print('workasset:', workasset)
        
        asset = assetutils_maya.WorkAssetMaya()
        if workasset is None:
            asset_dict = anim_list[tmp_output]['asset']
            tags = anim_list[tmp_output]['tags']
            
            for k in asset.get_dict():
                setattr(asset, k, asset_dict[k])
            out_config = asset.check_output_config(tags=tags)
            asset.path_template = asset.evaluate_output(out_config, proc_token=False, proc_tag=True, tags=tags)
        else:
            for k in asset.get_dict():
                setattr(asset, k, workasset[k])
            print('asset_dict: ', asset.get_dict())
            #out_config = asset.check_output_config(tags=tags)
            anim_list[tmp_output]['tags'] = [(x['tag_type'], x['name']) for x in db.get_assigned_tags(asset)]

        # p4 sync
        if workasset is not None:
            task = wcmds.Task(interactive=False)
            task.open_workasset(asset, src, src_ver)
            print('sync: ', asset.get_dict())
            print(' src:', src, src_ver)

        if 'output_overrides' in args:
            if args['output_overrides']['subcategory'] is not None:
                print('output_subcategory:', args['output_overrides']['subcategory'])
                asset.subcategory = args['output_overrides']['subcategory']
            if args['output_overrides']['assetname'] is not None:
                print('output_assetname:', args['output_overrides']['assetname'])
                asset.assetname = args['output_overrides']['assetname']
            if args['output_overrides']['variant'] is not None:
                print('output_variant:', args['output_overrides']['variant'])
                asset.variant = args['output_overrides']['variant']
            

        outfile, _ = asset.get_exportname(use_path_template=True)
        print('outfile:', outfile.replace('/', '\\'))
        if outfile is None:
            print('Warning: outpath not determined.')
            continue

        asset.version = db.next_available_workasset_version(outfile)

        if os.path.exists(outfile):
            subprocess.call('attrib -R "%s"' % outfile)

        print('Copying %s to %s...' % (tmp_output, outfile))
        if not os.path.exists(os.path.dirname(outfile)):
            os.makedirs(os.path.dirname(outfile))
        try:
            shutil.copyfile(tmp_output, outfile)
            print('Copying done.')
        except:
            print('Copying failed.')
        if os.path.exists(tmp_output):
            os.remove(tmp_output)

        tmp_thumb = assetutils.Asset.thumbnail_filepath(tmp_output, 0)
        thumb_filename = assetutils.Asset.thumbnail_filepath(outfile, asset.version)
        print('Copying %s to %s...' % (tmp_thumb, thumb_filename))
        if not os.path.exists(os.path.dirname(thumb_filename)):
            os.makedirs(os.path.dirname(thumb_filename))
        try:
            shutil.copyfile(tmp_thumb, thumb_filename)
            print('Copying done.')
        except:
            print('Copying failed.')

        files_to_submit += [outfile, thumb_filename]

        assetutils_maya.replace_to_cache(outfile)

        refs = []
        if os.path.exists(outfile):
            cmds.file(outfile, f=True, o=True)
            refs = assetutils_maya.MayaUtils.get_instance().getrefs()
            print('refs:', refs)

        anim_list[tmp_output]['outfile'] = outfile
        anim_list[tmp_output]['work_asset'] = asset
        anim_list[tmp_output]['files'] = [outfile, thumb_filename] + refs

    os.remove(anim_list_filename)

    #
    try:
        print('Reconciling...')
        p4u.p4_run_xxx('reconcile', '-ea', files_to_submit)
    except Exception as e:
        print('generate_rig_anim_work.postfunc: ', e)
    
    print('Submitting files...')
    res_org = p4u.submitfiles(files_to_submit, desc=u'%s - by %s' % (args['comment'], args['user']), submit_outside=True)
    print('>> res_org: ', res_org)

    asseturls = []
    tag_tree_ = tag_tree.TagTree.get_instance(os.environ['WM_TAGTREE_CACHE'], 
                        hie_contents_cache_file=os.environ['WM_HIERARCHY_CONTENTS_CACHE'])

    #
    #asset0 = anim_list[list(anim_list.keys())[0]]['work_asset']
    #_all_tags = db.get_assigned_tags_for_assets_3([asset0])
    #all_tags = {}
    #for n in _all_tags:
    #    key = (n['leafname'], n['localid'], assetdbutils.normalize_path(n['path_template']))
    #    if key not in all_tags:
    #        all_tags[key] = []
    #    all_tags[key].append(n)

    #   
    for tmp_output in anim_list.keys():
        asset = anim_list[tmp_output]['work_asset']
        outfile = anim_list[tmp_output]['outfile']
        print('outfile:', outfile.replace('/', '\\'))
        
        print('asset: ', asset.get_dict())
        files = anim_list[tmp_output]['files']
        if len(files) == 0 or not os.path.exists(files[0]):
            continue

        tags = anim_list[tmp_output]['tags']
        
        dbutils.DB.save_workasset_version(asset, files, comment=args['comment'])
        print('save_workasset_version done.')
        db.replace_tags(asset=asset, tags=tags, username=p4u.p4.user)
        print('replace_tags done.')
        #wcmds.edit_tags_in_tagtree(asset, tags, tag_tree_.add_tag, cache=all_tags)

        master = outfile
        try:
            print('>>> asset_dict:', asset.get_dict())
            print('>>> master: ', master)
            asseturl = asset.get_url(master)
            print('>>> asseturl: ', asseturl)
        except:
            asseturls.append(master.replace('/', '\\'))
        else:
            asseturls.append(asseturl)
    print('asseturls: ', asseturls)


    message = u'ワークファイル生成が完了しました。\n' + \
        u'*コメント*\n```' + args['comment'] + '```\n' + \
        u'*出力アセット*\n```' +'\n'.join(asseturls) + '```\n'
    
    from workfile_manager import notification
    notification.send_to_slack(message, args['user'])

