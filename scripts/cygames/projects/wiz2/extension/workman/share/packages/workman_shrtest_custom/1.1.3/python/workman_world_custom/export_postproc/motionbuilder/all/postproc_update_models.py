# -*- coding: utf-8 -*-
from __future__ import print_function

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application
from cylibassetdbutils import assetdbutils
import os, re, shutil, copy

try:
    import pyfbsdk as fb
    from workfile_manager_mbuilder import assetutils_motionbuilder
    from postproc_set_editor_mbuilder import ui_mbuilder
    dcccmds = ui_mbuilder.DccCmds()
    import cymobuapiutils
except:
    pass

from workfile_manager import p4utils, notification as notif

p4u = p4utils.P4Utils.get_instance()
db = assetdbutils.DB.get_instance()

##
# @class Plugin
# @brief モーションビルダーのワークファイルをアップデートするポストプロセス
# @details 
# @warning
# @note
class Plugin(PostProcBase):
    def application(self):
        return Application.MotionBuilder

    def apps_executable_on(self):
        return [Application.MotionBuilder]

    def is_asset_eligible(self, asset):
        return False

    def set_camera_discard_settings(self, opt):
        opt.Cameras = fb.FBElementAction.kFBElementActionDiscard
        opt.CurrentCameraSettings = False
        opt.CameraSwitcherSettings = False
        opt.BaseCameras = False

    def execute(self, args):
        from workfile_manager_mbuilder.export import post_fbx_export
        write_temp = False
        print('postproc_update_models.')

        workfile = args['target_workfile']
        workfile_version = args['workfile_version']
        print('filename: ', workfile)
        print('version: ', workfile_version)
        
        # sync workfile & textures
        buf = db.get_workasset_versions(filename=workfile, version=workfile_version, ignore_path_template=True)
        print('buf: ', buf)
        if len(buf) == 0:
            raise Exception('Cannot find any workfile version.')
        print('work count: ', len(buf))
        workfile_revision = buf[0]['revision']
        print('workfile: %s#%d' % (buf[0], workfile_revision))

        work_asset = assetutils_motionbuilder.WorkAssetMotionBuilder()
        for k in list(work_asset.get_dict().keys()):
            setattr(work_asset, k, buf[0][k])

        try:
            p4u.p4_run_xxx('sync', '--parallel=threads=8', '-f', '%s#%d' % (workfile, workfile_revision))
        except:
            pass
        try:
            p4u.p4_run_xxx('revert', '-f', workfile)
        except:
            pass
        refs = db.get_workasset_refs(filename=workfile, version=workfile_version, include_omit=False)
        for ref in refs:
            ref_file = ref['local_path']
            print('ref: %s#%d' % (ref_file, ref['revision']))
            try:
                p4u.p4_run_xxx('sync', '--parallel=threads=8', '-f', '%s#%d' % (ref_file, ref['revision']))
            except:
                pass
            try:
                p4u.p4_run_xxx('revert', '-f', ref_file)
            except:
                pass


        #            
        work_without_labels = self.create_work_without_labels(workfile)
        print('work_without_labels:', work_without_labels)
        res = self.create_basefile(workfile, args['assets'])
        if res is None:
            basefile = params = None
        else:
            basefile, params = res
        print('basefile: ', basefile)
        #print('params: ', params) 
        #print('To re-characterize: ', self.characters)

        fb.FBApplication().FileNew()
        
        #
        if basefile is not None:
            opt = fb.FBFbxOptions(True)
            fb.FBApplication().FileMerge(str(basefile), False, opt)
            if write_temp:
                post_fbx_export.write_tempfile('basefile_merged', workfile)
            if not write_temp:
                os.remove(basefile)

        #
        asset_objs = []
        idx = 0
        for asset in args['assets']:
            idx += 1
            asset_name, assetdict, latest, ns, filename, latest_filename = asset
            latest_filename = str(latest_filename)
            if not latest_filename.endswith('.fbx'):
                latest_filename = latest_filename[:latest_filename.rindex('.')] + '.fbx'

            if assetdict['version'] >= latest:
                continue
            opt = fb.FBFbxOptions(True)
            if ns is not None:
                opt.NamespaceList = str(ns)

            _asset = assetutils_motionbuilder.ModelAssetMotionBuilder()
            for k in list(_asset.get_dict().keys()):
                setattr(_asset, k, assetdict[k])
            _asset.version = latest

            if write_temp:
                post_fbx_export.write_tempfile('tmp_%d_0' % idx, workfile)
            _asset.pre_import()
            if write_temp:
                post_fbx_export.write_tempfile('tmp_%d_1' % idx, workfile)
            
            print('Merging latest asset:', latest_filename)
            fb.FBApplication().FileMerge(str(latest_filename), False, opt)
            
            if write_temp:
                post_fbx_export.write_tempfile('tmp_%d_2' % idx, workfile)
            _asset.post_import()
            if write_temp:
                post_fbx_export.write_tempfile('tmp_%d_3' % idx, workfile)
            asset_objs.append(_asset)


        #
        if False:
            if basefile is not None:
                opt = fb.FBFbxOptions(True)
                fb.FBApplication().FileMerge(str(basefile), False, opt)
                if write_temp:
                    post_fbx_export.write_tempfile('basefile_merged', workfile)
                if not write_temp:
                    os.remove(basefile)

        #
        opt = fb.FBFbxOptions(True)
        opt.SetAll(fb.FBElementAction.kFBElementActionDiscard, True)
        opt.Constraints = fb.FBElementAction.kFBElementActionMerge
        opt.Groups = fb.FBElementAction.kFBElementActionMerge
        self.set_camera_discard_settings(opt)
        fb.FBApplication().FileMerge(str(workfile) if work_without_labels is None else str(work_without_labels), False, opt)
        if write_temp:
            post_fbx_export.write_tempfile('work_merged', workfile)

        # resume params.
        for nodename in params.keys():
            obj = fb.FBFindModelByLabelName(nodename)
            if obj is None:
                continue
            for prname in params[nodename].keys():
                pr = obj.PropertyList.Find(prname)
                if pr is None:
                    continue
                for attrname in params[nodename][prname].keys():
                    v = params[nodename][prname][attrname]
                    if attrname == 'IsLocked':
                        pr.SetLocked(v)


        #
        for asset_obj in asset_objs:
            asset_obj.create_assetlabel()

        self.characterize()

        assetutils_motionbuilder.cache_textures()
        self.save_and_register(args, work_asset, workfile)

    ##
    # @brief 生成したワークファイルを保存しデータベースに登録する
    # @details
    # @param None
    # @return None
    # @warning
    # @note   
    def save_and_register(self, args, work_asset, workfile):
        from workfile_manager import cmds
        task = cmds.Task(interactive=False, thread=False, finished_callback=self.save_finish_cb, separate_p4_proc=True)
        version = work_asset.version
        buf = db.get_workasset_versions(filename=workfile, version=version, asset=work_asset, ignore_path_template=True)
        if len(buf) > 0:
            original_comment = buf[0]['comment'] + ' '
        else:
            original_comment = ''
        work_asset.truncate('version')
        comment = '%s[Updated from v%03d]' % (original_comment, version)
        task.save_workasset(work_asset, None, comment=comment, keep_edit=False)

        fb.FBApplication().FileNew()

        message = u'ワークファイルのアップデートが完了しました。\n=====================\n' + \
            u'*出力シーンファイル*\n' + workfile.replace('/', '\\')
        notif.send_to_slack(message, args['user'])

    def save_finish_cb(self, res):
        print('workfile updated.')
        if res:
            filename, _ = res
        else:
            return

    ##
    # @brief キャラクターのテンプレートファイルを使用してキャラクタライズを行う。
    # @details
    # @param None
    # @return None
    # @warning
    # @note 
    def characterize(self):
        orgfile = save_selection_to_tmpfile(save_all=True)
        import apiutils.utils
        tmpls = {}
        for n in fb.FBSystem().Scene.Characters:
            if n.GetCharacterize():
                continue
            tmpl = apiutils.char_template(self.char_params[n.LongName]['tmpfile'])
            tmpls[n.LongName] = tmpl

        fb.FBApplication().FileOpen(orgfile, False)

        for char in fb.FBSystem().Scene.Characters:
            if char.GetCharacterize():
                print('>>>>>>>>>> Skipped characterization: ', char.LongName)
                continue
            apiutils.utils.characterize_with_template_2(char, tmpls[char.LongName])
            char.ActiveInput = self.char_params[char.LongName]['params'][0]
            char.InputType = self.char_params[char.LongName]['params'][1]

    def getlabel(self):
        return 'Update models in workfiles'
        
    def default_checked(self):
        return False
        
    def is_editable(self):
        return False

    ##
    # @brief assetlabel以外の要素を一時ファイルとして書き出す。
    # @details コンストレインとグループを復元するために使用されます。それ以外のノード(フォルダーも含む)はマージする際にDiscardされます。\n
    # @param None
    # @return 一時ファイルのパス
    # @warning
    # @note 
    def create_work_without_labels(self, workfile):
        import apiutils.utils
        fb.FBApplication().FileOpen(str(workfile))

        self.char_params = {}
        for n in fb.FBSystem().Scene.Characters:
            cymobuapiutils.clear_selection()
            n.Selected = True
            tmpfile = save_selection_to_tmpfile(ascii=True)
            self.char_params[n.LongName] = {'tmpfile':tmpfile, 'params':(n.ActiveInput, n.InputType)}

        #tmpls = {}
        for n in fb.FBSystem().Scene.Characters:
            print('>> Character: ', n.LongName)
            self.char_params[n.LongName]['ctrl_nodes'] = []
            try:
                ctrl = n.PropertyList.Find('ControlSet')[0]
                self.char_params[n.LongName]['ctrl'] = ctrl.LongName
                print('>> ControlSet: ', ctrl.LongName)
                for p in ctrl.PropertyList:
                    if p.Name.endswith('Effector'):
                        for mdl in p:
                            print('>> Model: ', mdl.LongName)
                            self.char_params[n.LongName]['ctrl_nodes'].append(mdl.LongName)
            except:
                self.char_params[n.LongName]['ctrl'] = None

        
        fb.FBApplication().FileOpen(str(workfile))

        #
        buf = dcccmds.list_nodes('assetlabels', type='objectSet')
        if len(buf) > 0:
            assetlabel_node = buf[0]
        else:
            return None

        #
        constraints_in_assets = []
        label_nodes = dcccmds.sets(assetlabel_node, q=True)
        for label_node in label_nodes:
            _mems = dcccmds.sets(label_node, q=True)
            mems = []
            for m in _mems:
                mems.append(m)
            clds = cymobuapiutils.list_children(targets=mems, select_parent=True, include_components=True)
            for cld in clds:
                if type(cld) is fb.FBConstraintRelation:
                    if cld not in constraints_in_assets:
                        constraints_in_assets.append(cld)
            label_node.FBDelete()

        print('constraints_in_assets: ', constraints_in_assets)
        for cnst in constraints_in_assets:
            print('Deleting ', cnst.Name)
            cnst.FBDelete()

        #
        import tempfile
        tmpdir = tempfile.gettempdir()
        ctime = re.sub('[- :._]', '', assetdbutils.labelpostfix())
        tmpfilename = os.path.join(tmpdir, '%s.fbx' % ctime)

        opt = fb.FBFbxOptions(False)
        opt.SaveSelectedModelsOnly = False
        fb.FBApplication().FileSave(str(tmpfilename), opt)
        print('work_without_updatelabel saved: ', tmpfilename)
        return tmpfilename
    
    def check_if_character_in_asset(self, char, all_asset_nodes):
        print('check_if_character_in_asset:', char.LongName)
        try:
            ctrl_name = self.char_params[char.LongName]['ctrl']
            print('ctrl_name:', ctrl_name)
            for ctrl_node_name in self.char_params[char.LongName]['ctrl_nodes']:
                print('>> ctrl_node_name: ', ctrl_node_name)
                if ctrl_node_name in [x.LongName for x in all_asset_nodes]:
                    print('>> char in asset.')
                    return True
        except:
            ctrl = None

        return False
        
    def check_if_controler_in_asset(self, ctrl, all_asset_nodes):
        print('check_if_controler_in_asset:', ctrl.LongName)
        for char_name in self.char_params.keys():
            print('char_name:', char_name)
            print('ctrl:', ctrl)
            print('ctrl2: ', self.char_params[char_name]['ctrl'])
            if ctrl.LongName == self.char_params[char_name]['ctrl']:
                print('Match')
                for ctrl_node_name in self.char_params[char_name]['ctrl_nodes']:
                    print('>> ctrl_node_name: ', ctrl_node_name)
                    if ctrl_node_name in [x.LongName for x in all_asset_nodes]:
                        print('>> ctrl in asset.')
                        return True
        return False

    ##
    # @brief アセットとassetlabel以外の要素を一時ファイルとして書き出します。
    # @details 後の工程では、最初にアップデートアセットを全てインポートした後に、この一時ファイルがマージされます。\n
    # アセットに内包されているコンストレインも書き出し対象に含みません。
    # @param None
    # @return (一時ファイルのパス, 後で復元すべきアセットのパラメータ―(dict))
    # @warning
    # @note
    def create_basefile(self, workfile, assets):
        fb.FBApplication().FileOpen(str(workfile))
        buf = dcccmds.list_nodes('assetlabels', type='objectSet')
        if len(buf) > 0:
            assetlabel_node = buf[0]
        else:
            return None
        
        #
        all_asset_nodes = []
        del_nodes = []
        cymobuapiutils.select_all()
        
        #
        label_nodes = dcccmds.sets(assetlabel_node, q=True)
        for label_node in label_nodes:
            _mems = dcccmds.sets(label_node, q=True)
            mems = []
            for m in _mems:
                mems.append(m)
            clds = cymobuapiutils.list_children(targets=mems, select_parent=True, include_components=True)
            for cld in clds:
                if cld not in all_asset_nodes:
                    all_asset_nodes.append(cld)
            label_node.Selected = False

        params = {}
        for n in all_asset_nodes:
            if type(n) is fb.FBCharacter:
                if not self.check_if_character_in_asset(n, all_asset_nodes):
                    continue
            elif type(n) is fb.FBControlSet:
                if not self.check_if_controler_in_asset(n, all_asset_nodes):
                    continue
            n.Selected = False
            if n.LongName not in params:
                params[n.LongName] = {}
            for pr in n.PropertyList:
                if pr.Name not in params[n.LongName]:
                    params[n.LongName][pr.Name] = {}
                params[n.LongName][pr.Name]['IsLocked'] = pr.IsLocked()
        
        #
        for set_ in dcccmds.list_nodes(type='objectSet'):
            mms = list_member_objects(set_)
            for mm in mms:
                if mm not in all_asset_nodes:
                    break
            else:
                set_.Selected = False

        #    
        for label_node in label_nodes:
            _mems = dcccmds.sets(label_node, q=True)
            mems = []
            for m in _mems:
                mems.append(m)
            if len(mems) == 0:
                continue
            mt = re.search('^(.*):', mems[0].LongName)
            if mt:
                scene_asset_ns = mt.group(1)
            else:
                scene_asset_ns = None

            for asset in assets:
                asset_name, assetdict, latest, ns, filename, latest_filename = asset
                if ns == scene_asset_ns and assetdict['version'] < latest and is_same_asset(label_node, assetdict):
                    # need to update
                    break
            else:
                _mems = dcccmds.sets(label_node, q=True)
                cymobuapiutils.select_children(targets=mems, select_parent=True, include_components=True)

        sel = cymobuapiutils.get_selection()

        if len(sel) > 0:
            for n in fb.FBSystem().Scene.Folders:
                n.Selected = True
            tmpfilename = save_selection_to_tmpfile()
            print('basefile exported: ', tmpfilename)
        else:
            tmpfilename = None
        return tmpfilename, params


def is_same_asset(label_node, assetdict):
    import fbx
    
    for k in assetdict:
        if k == 'version':
            continue
        v = dcccmds.get_attr(dcccmds.get_name(label_node)+'.'+k)
        if type(v) is fbx.FbxString:
            v = v.Buffer()
        if v != assetdict[k]:
            return False
    return True


def delete_hie(n):
    import cymobuapiutils
    clds = cymobuapiutils.list_children(targets=n, select_parent=False, include_components=False)
    for cld in clds:
        delete_hie(cld)
    n.FBDelete()




def save_selection_to_tmpfile(ascii=False, save_all=False):
    import tempfile
    tmpdir = tempfile.gettempdir()
    ctime = re.sub('[- :._]', '', assetdbutils.labelpostfix())
    tmpfilename = os.path.join(tmpdir, '%s.fbx' % ctime)
    opt = fb.FBFbxOptions(False)
    opt.SaveSelectedModelsOnly = not save_all
    opt.EmbedMedia = False
    opt.UseASCIIFormat = ascii

    fb.FBApplication().FileSave(str(tmpfilename), opt)
    return str(tmpfilename)

def list_member_objects(set_):
    res = []
    clds = dcccmds.sets(set_, q=True)
    for cld in clds:
        if type(cld) is fb.FBGroup:
            res += list_member_objects(cld)
        else:
            res.append(cld)
    return res
