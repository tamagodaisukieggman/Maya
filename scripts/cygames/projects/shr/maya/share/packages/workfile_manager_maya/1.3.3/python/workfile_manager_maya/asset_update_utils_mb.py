# -*- coding: utf-8 -*-
from __future__ import print_function, annotations
import re
import os
import copy
import shutil
import P4

from Qt import QtCore, QtGui, QtWidgets

from cylibassetdbutils import assetdbutils, assetutils, assetvar
from cylibassetdbutils.structures import FileToRegister, CommitArgument
from workfile_manager import p4utils, dbutils, cmds as wcmds
from workfile_manager.ui import ui_dialogs


from maya import cmds


p4u = p4utils.P4Utils.get_instance()

def is_version_already_used(asset, masterfile, latest_file, latest_ver):
    db = assetdbutils.DB.get_instance()
    already_used = []
    if asset.area() == 'work':
        buf = db.get_workasset_versions_3(asset)
        assert len(buf) > 0
        asset_dict = buf[0]
        format = masterfile[masterfile.rindex('.')+1:]
        already_used = db.get_workasset_refs(ref_name=latest_file, ref_revision=latest_ver, include_omit=False, asset=asset, format=format)
        already_used = [x for x in already_used if x['create_date'] > asset_dict['create_date']]

    elif asset.area() == 'share':
        _asset = copy.deepcopy(asset)
        _asset.truncate('version')
        already_used = db.get_share_asset_refs(asset=_asset, ref_filename=latest_file, include_omit=False)
        already_used = [x for x in already_used if x['version'] > asset.version]

    if len(already_used) > 0:
        return True
    else:
        return False

class AssetUpdateUtils():
    def __init__(self, dccutils, force_update=None):
        self.dccutils = dccutils
        self.done = []
        self.hie = []
        self.update_all_later = force_update

    def check_update(self, asset, filename, depth=0, check_self=False, parent_asset=None, silent=False):
        #self.check_self = check_self
        self.silent = silent
        self.parent_asset = copy.deepcopy(parent_asset)

        if self._is_done(asset, filename):
            return
        
        self.hie.append(filename)

        print('\t' * depth + 'check_update: ', filename, flush=True)
        res = None
        if asset.area() == 'share' or asset.area() == 'work' or asset.area() == 'engine':
            res = self._check_update(asset, filename, depth=depth, check_self=check_self)
        else:
            raise Exception('Only share or work asset is supported.')
        
        self.hie.pop(-1)
        return res


    def _check_update_non_share(self, ref, ref_filename, childs, depth):
        from workfile_manager import ReturnState
        db = assetdbutils.DB.get_instance()
        #
        #  Dirty code begin...
        #
        if 'asset_version' in ref and ref['asset_version'] is not None:
            '''
            Refが別のワークマスターファイルの場合
            '''
            buf = db.get_workasset_versions(filename=ref_filename, version=ref['asset_version'], ignore_path_template=True)
            if len(buf) == 0:
                return ReturnState.Continue
            assert len(buf) == 1, 'Multiple workasset_versions found.'
            
            assetdict = buf[0]
            child_asset = self.dccutils.create_work_asset({})
            child_asset.truncate('version')

            for k in list(child_asset.__dict__.keys()):
                child_asset.set_token(k, assetdict[k])

            child_asset.version = buf[0]['version']
            child_asset.path_template = buf[0]['path_template']

            childs.append((child_asset, ref_filename))

            # リファレンスされている他のワークファイルを再帰的に処理しないので、下記文コメントアウト
            #self.check_update(child_asset, ref_filename, depth=depth+1)
        else:
            try:
                buf = p4u.p4_run_xxx('fstat', ref_filename)[0]
                #print 'buf: ', buf
            except:
                buf = None
            if buf is not None:
                if 'headRev' in buf and 'haveRev' in buf and buf['headRev'] > buf['haveRev']:
                    childs.append((None, ref_filename))

        #
        # Dirty code end
        #
        return ReturnState.Success

    def _check_update_proc_work_share(self, asset, masterfile, ch, ref_filename, updates, refs_new):
        db = assetdbutils.DB.get_instance()
        from workfile_manager.ui import uiutils

        '''子供がShareもしくはWorkのアセット'''
        latest_ver = None
        latest_file = None
        
        is_current_used_un_official = None

        if ch.area() == 'share':
            cur_ver = ch.version
            ch.truncate('version')
            
            buf = db.get_sharedasset_versions(ch, ignore_omit=True, only_official=True)
            if len(buf) == 0:
                return

            latest_ver = buf[0]['version']
            latest_file = buf[0]['path']

            
            if cur_ver not in [x['version'] for x in buf]:
                is_current_used_un_official = True

        elif ch.area() == 'work':
            cur_ver = ch.version
            ch.truncate('version')
            buf = db.get_workasset_versions(filename=ref_filename, ignore_path_template=True)
            latest_ver = buf[0]['version']
            latest_file = buf[0]['local_master_path']

        if latest_ver is not None and latest_file is not None:
            if (latest_ver > cur_ver or is_current_used_un_official) and os.path.exists(latest_file):
                print('masterfile: ', masterfile)
                print('latest_file: ', latest_file)
                print('latest_ver: ', latest_ver)
                already_used = is_version_already_used(asset, masterfile, latest_file, latest_ver)
                print('already_used: ', already_used)
                
                if not already_used:
                    filestr = self._get_hie_str()
                    author = buf[0]['author']
                    desc = buf[0]['comment']

                    if ref_filename in [x[0] for x in updates]:
                        if [x[1] for x in updates if x[0]==ref_filename][0] is None:
                            res = 0
                        else:
                            res = 1
                    else:
                        if self.update_all_later is None:
                            res = ui_dialogs.PromptDialog('Confirmation',
                                u'リファレンス先のアセットに新しいバージョンが存在します。\n\n' + \
                                '%s\n\nVersion: %d -> %d\n\n\n\n' % (os.path.basename(ref_filename), cur_ver, latest_ver) + \
                                u'【参照元】\n%s\n\n' % filestr.strip('\n') + \
                                u'【作成者】\n%s\n\n' % author + \
                                u'【コメント】\n%s\n\n' % desc + \
                                u'\n\n\nアップデートしますか？\n\n', 
                                btns=['アップデートする', '以降全てアップデートする', 'しない']).exec_()
                            if res == 2:
                                self.update_all_later = True
                                res = 1
                        else:
                            if self.update_all_later:
                                res = 1
                            else:
                                res = 0

                    if res == 1:
                        if ref_filename not in [x[0] for x in updates]:
                            updates.append((ref_filename, latest_file))

                        idx = refs_new.index(ref_filename)
                        refs_new[idx] = latest_file
                        print('latest_file: ', latest_ver)

                        if ch.area() == 'work':
                            task = wcmds.Task(interactive=False)
                            tmp_asset = copy.deepcopy(ch)
                            tmp_asset.version = latest_ver
                            task.open_workasset(tmp_asset, ref_filename, latest_ver)

    def _check_unused_new_revision(self, ref_filename, latest_ver, cur_ver, filestr):
        if self.update_all_later is None:
            log = p4u.p4_run_xxx('filelog', ref_filename)[0]
            rev_idx = log['rev'].index(str(latest_ver))

            try:
                desc = (log['desc'][rev_idx]).decode('utf-8')
            except:
                # python3
                desc = log['desc'][rev_idx]
                
            user = log['user'][rev_idx]
            w0 = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout(w0)
            cb_update = QtWidgets.QCheckBox(u'アップデートせずに進める')
            w = QtWidgets.QCheckBox(u'以降全てに同じ選択を適用する')
            vbox.addWidget(cb_update)
            vbox.addWidget(w)
            
            d = ui_dialogs.PromptDialog('Confirmation',
                u'使用されていない新しいリビジョンが存在します。\n\nアップデートを実行します。\n\n\n\n' + \
                '%s\n\nRevision: %d -> %d\n\n\n' % (os.path.basename(ref_filename), cur_ver, latest_ver) + \
                u'【参照元】\n%s\n\n' % filestr + \
                u'【作成者】\n%s\n\n' % user + \
                u'\n【コメント】\n\n%s\n\n' % desc,
                btns=['Continue'], wd=w0)
            d.resize(500, d.height())
            d.exec_()
            res = 2 if cb_update.isChecked() else 1


            if w.isChecked():
                self.update_all_later = True if res == 1 else False
        else:
            res = 1 if self.update_all_later else 2
        
        return res

    def _check_update_proc_a_file(self, ch, ref_filename, updates, refs_new, asset, filename):
        db = assetdbutils.DB.get_instance()

        # 子供がPerfoce上の単一ファイル

        try:
            buf = p4u.p4_run_xxx('fstat', ref_filename)[0]
        except:
            buf = None
        if buf is not None:
            if 'headRev' in buf and 'haveRev' in buf and buf['headRev'] > buf['haveRev'] \
                    and ('headAction' in buf and buf['headAction'] != 'delete'):
                cur_ver = int(buf['haveRev'])
                latest_ver = int(buf['headRev'])
                filestr = self._get_hie_str()
                if asset.area() == 'work':
                    wrefs = db.get_workasset_refs(filename=self.hie[-1], ref_name=ref_filename, ref_revision=latest_ver)
                elif asset.area() == 'engine':
                    wrefs = db.get_engine_asset_refs(filename=filename, ref_name=ref_filename, ref_revision=latest_ver)
                else:
                    wrefs = None

                if wrefs is not None and len(wrefs) == 0 and asset.is_reference_updatable():
                    res = self._check_unused_new_revision(ref_filename, latest_ver, cur_ver, filestr)
                    
                    if res == 1:
                        p4u.p4_run_xxx('edit', ref_filename)
                        diff = p4u.p4_run_xxx('diff', '%s' % (ref_filename)) #現在の編集元リビジョンと比較する。'-f'オプションをつけると強制的に#headとの比較になるので注意！
                        task = wcmds.Task()
                        if task._diff_exists(diff):
                            if not self.silent:
                                ui_dialogs.PromptDialog('Confirmation', u'未サブミットのローカルファイルが存在します。\n\nアップデート出来ません。', btns=['Continue']).exec_()
                        else:
                            try:
                                p4u.p4_run_xxx('sync', '--parallel=threads=8', ref_filename)
                            except P4.P4Exception as e:
                                if len(e.errors) == 0:
                                    pass
                                else:
                                    raise(e)
                                
                            p4u.p4_run_xxx('revert', ref_filename)
                            updates.append((ref_filename, buf['clientFile']))
                            idx = refs_new.index(ref_filename)
                            refs_new[idx] = buf['clientFile']
                        
                    
    def _replace_path(self, line, old_path, new_path):
        expr = '"' + old_path.replace('/', '[/]') + '"'
        expr = expr.replace('.', '[.]')
        new_line = re.sub(expr, '"' + new_path + '"', line)
        if new_line != line:
            return new_line
        if assetutils.is_non_cached_share_file(old_path):
            wcmds.cache_sharefile(old_path)
            cache = wcmds.get_cache_path_from_share(old_path)
            expr = '"' + cache.replace('/', '[/]') + '"'
            expr = expr.replace('.', '[.]')
            new_line = re.sub(expr, '"' + new_path + '"', line)
            return new_line
        return line

    def _fix_filetype(self, line, new_path):
        ext = re.sub('.*[.]', '', new_path)
        fmt = 'mayaAscii' if ext == 'ma' else 'mayaBinary'
        new_line = re.sub('-typ "[^"]+"', '-typ "%s"' % fmt, line)
        return new_line

    def _proc_update(self, filename, updates, rfn_updates):
        if len(updates) == 0:
            if filename.endswith('.mb'):
                return
            else:
                with open(filename, 'r') as f:
                    lines = f.readlines()
                return lines

        lines = []
        caches = [None] * len(updates)
        exprs = [None] * len(updates)

        for i, update in enumerate(updates):
            if assetutils.is_non_cached_share_file(update[1]): # False if candidates are cached share files.
                wcmds.cache_sharefile(update[1])
                update = (update[0], wcmds.get_cache_path_from_share(update[1]))
                updates[i] = update
                
            wcmds.cache_sharefile(update[0])
            caches[i] = wcmds.get_cache_path_from_share(update[0])

            expr = '"' + update[0].replace('/', '[/]') + '"'
            exprs[i] = expr.replace('.', '[.]')

        #print('rfn_updates: ', rfn_updates)

        if filename.endswith('.mb'):
            for org_rfn in cmds.ls(type='reference'):
                try:
                    old_ref = cmds.referenceQuery(org_rfn, filename=True, wcn=True)
                except:
                    continue
                old_ref = wcmds.get_share_path_from_cache(old_ref)
                #print('old file: ', old_ref)
                for old_path, new_path in updates:
                    old_path = wcmds.get_share_path_from_cache(old_path)
                    #print('old_path: ', old_path)
                    if old_path == old_ref:
                        cmds.file(new_path, loadReference=org_rfn)
                        #print('replaced %s to %s' % (old_path, new_path))
            return

        else:
            with open(filename, 'r') as f:
                line = ''
                file_context = True
                for _line in f:
                    if _line.startswith('//'):
                        lines.append(_line)
                        continue
                    if _line.startswith('requires '):
                        file_context = False
                    line += _line.strip('\n')
                    if not file_context or line.endswith(';'):
                        prev = line
                        for i, update in enumerate(updates):
                            expr = exprs[i]
                            if re.search(expr, line):
                                line = re.sub(expr, '"' + update[1] + '"', line)
                            elif caches[i] is not None:
                                expr = '"' + caches[i].replace('/', '[/]') + '"'
                                expr = expr.replace('.', '[.]')
                                line = re.sub(expr, '"' + update[1] + '"', line)

                            if prev != line:
                                line = self._fix_filetype(line, update[1])
                                break
                        else:
                            if file_context:
                                for rfn_update in rfn_updates:
                                    rfn = rfn_update['rfn']
                                    old_path = rfn_update['old_path']
                                    new_path = rfn_update['new_path']
                                    new_line = self._replace_path(line, old_path, new_path)
                                    if prev != new_line:
                                        m = re.search(' -rfn "([^"]+)"', line)
                                        if m:
                                            org_rfn = m.group(1)
                                            print('org_rfn: ', org_rfn)
                                            if org_rfn == rfn or org_rfn.endswith(':'+rfn):
                                                line = self._fix_filetype(new_line, new_path)
                                                break
                        line += '\n'
                        lines.append(line)
                        line = ''
                    else:
                        continue
            return lines

        

    def _proc_db_share(self, filename, asset, _asset, lines, refs_org, refs_new, depth) -> tuple[str, assetutils.Asset]:
        db = assetdbutils.DB.get_instance()

        master = db.get_sharedasset_from_file(filename)[0]
        _asset.truncate('version')
        tags = [(x['tag_type'], x['name']) for x in db.get_assigned_tags(_asset)]
        _asset.version = db.next_available_shareasset_version(_asset, tags=tags).version
        outfile = _asset.get_exportname(tags=tags)[0]

        print('\t'*depth + 'exportname: ', outfile)

        if asset.is_updatable():
            if filename.endswith('.mb'):
                cmds.file(rn=outfile)
                cmds.file(save=True, f=True)
            else:
                with open(outfile, 'w') as outf:
                    outf.writelines(lines)
        else:
            shutil.copyfile(filename, outfile)

        print('\t'*depth + 'wrote: ', outfile)

        db.publish(outfile, _asset, '%s [Updated from version:%d]' % (master['comment'], master['version']), username=p4u.user, work_asset_record=None)

        #
        #
        buf = db.get_sharedasset_from_file(outfile)
        if len(buf) != 1:
            raise 'There must be just one sharedasset. found: %d' % len(buf)
        assetdict = buf[0]
        assetdict['success'] = 1
        db.update_versions_shared([assetdict], updatekeys=['success'])

        source_textures = {}
        for ref in refs_org:
            if ref['source'] is None or ref['source_revision'] is None:
                continue
            source_textures[ref['local_path']] = (ref['source'], ref['source_revision'])

        db.publish_share_refs(_asset, assetdict['asset_id'], outfile, refs_new, p4u.user, source_textures=source_textures)

        return outfile, _asset
        

    def _proc_db_work(self, filename, asset, _asset, lines, refs_new, depth) -> tuple[str, assetutils.Asset]|None:
        from workfile_manager.ui import ui_table_work, ui_table
        #print('>>> _proc_db_work: asset: ', asset.get_dict())
        #print('>>> _proc_db_work: _asset: ', _asset.get_dict())
        #print('>>> filename: ', filename)
        
        if filename.endswith('.mb'):
            db = assetdbutils.DB.get_instance()
            buf = db.get_workasset_versions_3(asset)
            if len(buf) > 0:
                original_comment = buf[0]['comment'] + ' '
                if asset.version is None:
                    if asset.private_version is None:
                        verstr = '-'
                    else:
                        verstr = '%s%03d' % (ui_table.PRIVATE_VERSION_PREFIX, asset.private_version)
                else:
                    verstr = 'v%03d' % asset.version
            else:
                original_comment = ''
                verstr = '-'
            comment = '%s[Updated from %s]' % (original_comment, verstr)

            if asset.is_updatable():
                task = wcmds.Task(upload=False if depth == 0 else True)
                _asset.version = _asset.private_version = None
                print('saving workasset...')
                res = task.save_workasset(_asset, refs_new, comment=comment, save_local=True, export_thumbnail=True)
                if res:
                    outfile, out_asset = res
                    print('saving workasset done.', outfile, out_asset)
                else:
                    print('ERROR: Failed to update %s. get_exportname failed.' % filename)
                    return None
            else:
                task = wcmds.Task(upload=False)
                _asset.version = _asset.private_version = None
                res = task.save_workasset(_asset, refs_new, comment=comment, save_local=False, export_thumbnail=False)
                
                if res:
                    outfile, out_asset = res
                else:
                    print('ERROR: Failed to update %s. get_exportname failed.' % filename)
                    return None

                #shutil.copyfile(filename, outfile)
                
            print('>>> outfile: ', outfile)

            return outfile, out_asset

        else:
            task = wcmds.Task(upload=False)
            #_asset.truncate('version')
            #_asset.version = None # ここで新規versionもしくはprivate_versionをセットすること。
            _asset.version = _asset.private_version = None

            db = assetdbutils.DB.get_instance()
            buf = db.get_workasset_versions_3(asset)
            if len(buf) > 0:
                original_comment = buf[0]['comment'] + ' '
            else:
                original_comment = ''

            verstr = ('%s%03d' % (ui_table.PRIVATE_VERSION_PREFIX, asset.private_version)) if asset.private_version is not None else 'v%03d' % asset.version
            res = task.save_workasset(_asset, refs_new, comment='%s[Updated from %s]' % (original_comment, verstr), 
                                        save_local=False, export_thumbnail=False)
            if res:
                outfile, out_asset = res
            else:
                raise Exception('Failed to save workasset.')
            
            _asset.version = out_asset.version
            _asset.private_version = out_asset.private_version
            outfile, _ = _asset.get_exportname(use_path_template=True)
            
            if outfile is None:
                print('ERROR: Failed to update %s. get_exportname failed.' % filename)
                return None

            print('\t'*depth + 'exportname: ', outfile)

            if os.path.exists(outfile):
                import subprocess
                subprocess.call('attrib -R "%s" /S /D' % outfile)

            if asset.is_updatable():
                with open(outfile, 'w') as outf:
                    outf.writelines(lines)
            else:
                shutil.copyfile(filename, outfile)

            print('\t'*depth + 'wrote: ', outfile)

            return outfile, out_asset


    def _proc_db_engine(self, filename, asset, _asset, refs_new, depth) -> tuple[str, assetutils.Asset]|None:
        db = assetdbutils.DB.get_instance()
        #_asset.truncate('version')

        outfile, _ = _asset.get_exportname(use_path_template=True)
        
        if outfile is None:
            print('ERROR: Failed to update %s. get_exportname failed.' % filename)
            return None

        print('\t'*depth + 'exportname: ', outfile)

        files = [filename] + refs_new
        revs = []
        for f in files:
            buf = p4u.p4_run_xxx('fstat', f)[0]
            revs.append((f,buf))

        buf = db.get_engine_assets(asset=asset, filename=filename)
        if len(buf) > 0:
            original_comment = buf[0]['comment'] + ' '
        else:
            original_comment = ''
        
        _asset.version = None
        args = CommitArgument(_asset, p4u.user, comment='%s[Updated from version:%d]' % (original_comment, asset.version))
        outversion = db.commit_to_engine([FileToRegister(x[0], int(x[1]['haveRev']), x[1]['depotFile']) for x in revs], args)
        _asset.version = outversion

        return outfile, _asset


    def _read_ref_info(self, filename):
        res = {}
        if filename.endswith('.mb'):
            #print('_read_ref_info: ', filename)
            from workfile_manager_maya import assetutils_maya
            desc = assetutils_maya.extract_embeded_scene_desc(filename)
            if desc is None:
                return res
            for ref in desc['references']:
                res[ref] = desc['references'][ref]
        else:
            expr = re.compile('^file .*-rfn "([^"]+)".*"([^"]+)";$')
            
            with open(filename, 'r') as fhd:
                cpline = ''
                for line in fhd:
                    if line.startswith('requires '):
                        break
                    cpline += line.strip('\n')
                    if cpline.endswith(';'):
                        m = expr.search(cpline)
                        if m:
                            rfn = m.group(1)
                            sn = m.group(2)
                            res[rfn] = sn
                        cpline = ''
                    else:
                        continue
        return res


    def _check_update(self, asset, filename, depth, check_self):
        from workfile_manager import ReturnState
        db = assetdbutils.DB.get_instance()
        
        from workfile_manager.ui import uiutils
        
        updates = []
        outfile = None
        outversion = None
        out_asset = None

        dont_self_updated_selected = False

        rfn_updates = []

        if asset.area() == 'share':
            filename = wcmds.get_share_path_from_cache(filename)

            # check self updates.
            #
            out_asset = copy.deepcopy(asset)
            if check_self:
                buf = db.get_sharedasset_from_file(filename)
                if len(buf) != 1:
                    raise Exception('More than a record found: ' + filename)

                is_current_official = buf[0]['official']

                _asset:assetvar.ShareAsset = self.dccutils.create_share_asset({})
                _asset.copy_parameters_from_dict(buf[0])
                
                _asset.truncate('version')
                vers = db.get_sharedasset_versions(_asset, ignore_omit=True, only_official=True)


                if len(vers) > 0 and (vers[0]['version'] > buf[0]['version'] or not is_current_official):
                    if not is_current_official:
                        message = '現在リファレンスされている下のアセットはオフィシャルバージョンではありません。\n\n' + \
                                '最新のオフィシャルバージョンに置き換えますか？'
                        btn_label = '置き換える'
                    else:
                        message = u'新しいバージョンが存在します。\n\nアップデートしますか？'
                        btn_label = 'アップデートする'

                    already_used = is_version_already_used(self.parent_asset[0], self.parent_asset[1], vers[0]['path'], vers[0]['version'])
                    if not already_used:
                        if self.update_all_later is None:
                            basename = re.sub('.*[/]', '', vers[0]['path'])
                            d = ui_dialogs.PromptDialog('Confirmation',
                                message + '\n\n\n\n' + \
                                '%s\n\nVersion: %d -> %d\n\n\n' % (basename, buf[0]['version'], vers[0]['version']) + \
                                u'【作成者】\n%s\n\n' % vers[0]['author'] + \
                                u'\n【コメント】\n\n%s\n\n' % vers[0]['comment'],
                                btns=[btn_label, '全て' + btn_label, 'そのままにする'])
                            d.resize(500, d.height())
                            res = d.exec_()
                            if res == 2:
                                self.update_all_later = True
                                res = 1
                        else:
                            if self.update_all_later:
                                res = 1
                            else:
                                res = 0
                        
                        if res == 1:
                            ref_info_old = self._read_ref_info(filename)
                            #print('ref_info_old:', ref_info_old)
                            new_filename = vers[0]['path']
                            ref_info_new = self._read_ref_info(new_filename)
                            #print('ref_info_new:', ref_info_new)
                            
                            for rfn in list(ref_info_old.keys()):
                                if rfn in list(ref_info_new.keys()):
                                    rfn_updates.append({'rfn':rfn, 'old_path':ref_info_old[rfn], 'new_path':ref_info_new[rfn]})

                            #
                            outfile = new_filename
                            filename = new_filename
                            outversion = vers[0]['version']
                            out_asset.version = outversion
                        else:
                            dont_self_updated_selected = True
                        

            refs_org = db.get_share_asset_refs(out_asset, filename)


        elif asset.area() == 'work':
            refs_org = dbutils.DB.getrefs(asset, filename, asset.version, private_version=asset.private_version if hasattr(asset, 'private_version') else None)
        elif asset.area() == 'engine':
            refs_org = db.get_engine_asset_refs(filename=filename, version=asset.version)
        else:
            return

        # check reference updates.
        #
        refs = [x for x in refs_org if x['revision'] is not None]
        print ('\t' * depth + 'refs: ', refs, flush=True)
        if len(refs) == 0:
            if outversion is None:
                return
            else:
                return {'outfile':outfile, 'outversion':outversion, 'rfn_updates':rfn_updates, 'out_asset':out_asset}

        childs = []
        if not dont_self_updated_selected:
            _done = {}
            for ref in refs:
                ref_filename = ref['local_path']
                #print 'ref_filename: ', ref_filename
                #if ref_filename.startswith(assetutils.get_share_root()):
                if assetutils.is_non_cached_share_file(ref_filename):
                    
                    # Refが別のシェアマスターファイルの場合
                    
                    buf = db.get_sharedasset_from_file(ref_filename)
                    if len(buf) == 0:
                        continue
                    assetdict = buf[0]
                    child_asset = self.dccutils.create_share_model_asset({})
                    for k in list(child_asset.__dict__.keys()):
                        child_asset.set_token(k, assetdict[k])
                    childs.append((child_asset, ref_filename))
                    if ref_filename in list(_done.keys()):
                        res = _done[ref_filename]
                    else:
                        if not check_self:
                            res = self.check_update(child_asset, ref_filename, depth=depth+1, check_self=True, parent_asset=(asset, filename))
                            _done[ref_filename] = res
                        else:
                            res = None

                    if res is not None:
                        updated_ref_filename = res['outfile']
                        rfn_updates = res['rfn_updates']
                        print('updated_ref_filename: ', updated_ref_filename)
                        if ref_filename != updated_ref_filename:
                            updates.append((ref_filename, updated_ref_filename))
                        else:
                            updates.append((ref_filename, None))
                    else:
                        updates.append((ref_filename, None))
                    
            
                else:
                    stat = self._check_update_non_share(ref, ref_filename, childs, depth)
                    if stat == ReturnState.Continue:
                        continue
                
        print('\t' *depth + 'childs: ', childs, flush=True)

        refs_new = [x['local_path'] for x in copy.deepcopy(refs_org)]

        for (ch, ref_filename) in childs:
            if ch is not None:
                self._check_update_proc_work_share(asset, filename, ch, ref_filename, updates, refs_new)
            else:
                self._check_update_proc_a_file(ch, ref_filename, updates, refs_new, asset, filename)

        updates = [x for x in updates if x[1] is not None]
        
        if len(updates) > 0:
            if filename.endswith('.mb'):
                cmds.file(filename, o=True, f=True)

                if asset.is_updatable():
                    _updates = [x for x in updates if assetdbutils.normalize_path(x[0]) != assetdbutils.normalize_path(x[1])]
                    #for up in _updates:
                    #    print('_updates: ', up)
                    self._proc_update(filename, _updates, rfn_updates)

                lines = None ###

                if asset.is_updatable() or asset.is_reference_updatable():
                    _asset = copy.deepcopy(asset)
                    if asset.area() == 'share':
                        outfile, out_asset = self._proc_db_share(filename, asset, _asset, lines, refs_org, refs_new, depth)
                        
                    elif asset.area() == 'work':
                        proc_db_result = self._proc_db_work(filename, asset, _asset, lines, refs_new, depth)
                        if proc_db_result is None:
                            return None
                        outfile, out_asset = proc_db_result

                    elif asset.area() == 'engine':
                        proc_db_result = self._proc_db_engine(filename, asset, _asset, refs_new, depth)
                        if proc_db_result is None:
                            return None
                        outfile, out_asset = proc_db_result
                        
                    else:
                        raise Exception('Only share or work asset or enginie asset is supported.')
                    
                    if out_asset is None:
                        return None
            else:
                if asset.is_updatable():
                    _updates = [x for x in updates if assetdbutils.normalize_path(x[0]) != assetdbutils.normalize_path(x[1])]
                    lines = self._proc_update(filename, _updates, rfn_updates)
                else:
                    lines = None

                if asset.is_updatable() or asset.is_reference_updatable():
                    _asset = copy.deepcopy(asset)
                    if asset.area() == 'share':
                        outfile, out_asset = self._proc_db_share(filename, asset, _asset, lines, refs_org, refs_new, depth)
                        
                    elif asset.area() == 'work':
                        proc_db_result = self._proc_db_work(filename, asset, _asset, lines, refs_new, depth)
                        if proc_db_result is None:
                            return None
                        outfile, out_asset = proc_db_result

                    elif asset.area() == 'engine':
                        proc_db_result = self._proc_db_engine(filename, asset, _asset, refs_new, depth)
                        if proc_db_result is None:
                            return None
                        outfile, out_asset = proc_db_result
                        
                    else:
                        raise Exception('Only share or work asset or enginie asset is supported.')
                    
                    if out_asset is None:
                        return None

        
        self.done.append((asset, filename))
        print('\t' * depth + 'Done: ' + filename, flush=True)

        if outfile is None:
            return None
        else:
            return {'outfile':outfile, 'outversion':outversion, 'rfn_updates':rfn_updates, 'out_asset':out_asset}

    def _get_hie_str(self):
        filestr = ''
        for i, f in enumerate(self.hie):
            if i > 0:
                pr = u'└'
            else:
                pr = ''
            filestr += '\t' * (i*2) + pr + os.path.basename(f) + '\n'
        return filestr

    def _is_done(self, asset, filename):
        for d in self.done:
            if self._is_same_asset(asset, d[0]) and filename == d[1]:
                return True
        return False

    def _is_same_asset(self, asset1, asset2):
        if len(list(asset1.__dict__.keys())) != len(list(asset2.__dict__.keys())):
            return False

        for k in list(asset1.__dict__.keys()):
            if hasattr(asset2, k) and getattr(asset1, k) == getattr(asset2, k):
                continue
            else:
                return False
                
        return True



   