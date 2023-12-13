# -*- coding: utf-8 -*-
from __future__ import print_function
import subprocess
import os
import re
import importlib
import copy
import glob
import shutil
import yaml
import sys
import traceback

import workfile_manager.notification as notif
from workfile_manager import p4utils, wmlog, plugin_utils
from cylibassetdbutils import assetdbutils, assetutils
from workfile_manager_maya import assetutils_maya

try:
    import maya.cmds as cmds
    import maya.mel as mel
    import pymel.core as pm
except:
    pass


#import request_sync

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()
logger = wmlog.get_logger(__name__)

def breakInputConnections(nodeattr):
    nodeattrs = [nodeattr]
    if ':' in nodeattr:
        nodeattrs.append(re.sub('\w*:', '', nodeattr))
    
    for nodeattr in nodeattrs:
        try:
            con = cmds.listConnections(nodeattr, s=True, d=False, p=True, c=True)
            if con is not None:
                mel.eval('disconnectAttr %s %s' % (con[1], con[0]))
        except:
            pass


def create_thumbnail(thumb):
    thumb_path = thumb[:thumb.rindex('.')]
    cmds.displayPref(displayGradient=0)
    cmds.colorManagementPrefs(e=True, cmEnabled=True)
    cmds.colorManagementPrefs(e=True, outputTransformEnabled=True, ott='playblast')
    try:
        cmds.colorManagementPrefs(e=True, viewTransformName='sRGB gamma')
        cmds.colorManagementPrefs(e=True, outputTransformName='sRGB gamma', ott='playblast')
    except:
        import traceback
        print(traceback.format_exc())

    fr = cmds.currentTime(q=True)

    logger.info('playblast: %s', thumb_path.replace('/', '\\'))
    logger.info('frame: %s', fr)
    
    cmds.playblast(format='image', filename=thumb_path, viewer=0, showOrnaments=1, fp=4, percent=100, compression='png', quality=100, fo=True, os=False, widthHeight=(800, 480), ifz=True, fr=fr)
    convcmd = '%s -y -i %s.0000.png ' % (os.environ['FFMPEG_EXE'], thumb_path) + \
        ' -filter_complex "[0]eq=gamma=2.2" ' + \
        thumb_path + '.jpg'
    logger.info('convcmd: %s', convcmd)
    subprocess.call(convcmd)
    os.remove('%s.0000.png' % (thumb_path))

class Task:
    def prepare_input(self):
        if self.inputfile.endswith('.ma'):
            assetutils_maya.remove_garbage_from_ma(self.inputfile)


    def write_tempfile(self, tmpname):
        if self.keep_intermediate:
            if self.inputfile is None:
                #print('wirte_tempfile: inputfile is None. Skipped.')
                assetutils_maya.write_tempfile(tmpname, 'xxx.ma')    
                return
            assetutils_maya.write_tempfile(tmpname, self.inputfile)
            
    def apply_postprocs(self, args, pnodes):
        pnodes = copy.deepcopy(pnodes)

        postproc = args['postproc']
        postproc_outputs = []
        #print 'pnodes: ', pnodes
        source_textures = None
        for pp in postproc:
            print('Post-process: ', pp['label'], flush=True)
            print('module_name: ', pp['module_name'])
            m = importlib.import_module(pp['module_name'])
            print('import_module done.', flush=True)
            #print 'Module: ', reload(m)
            ppargs = pp['args'] if pp['args'] is not None else {}
            for k in list(args.keys()):
                if k != 'postproc' and k != 'selection': # don't use 'selection' because node name may changes.
                    ppargs[k] = args[k]
            
            ppargs['plugin_name'] = pp['module_name']
            #ppargs['selected_pynodes'] = pnodes
            ppargs['global_args'] = args
            ppargs['task'] = self
            print('apply_postprocs - p0', flush=True)
            if 'child_postprocs' in args:
                ppargs['postproc'] = args['child_postprocs'] 
            else:   
                ppargs['postproc'] = args['postproc']

            if 'child_commitprocs' in args:
                ppargs['procs'] = args['child_commitprocs']
            elif 'procs' in args:
                ppargs['procs'] = args['procs']

            print('apply_postprocs - p1', flush=True)
            pm.select([x for x in pnodes if pm.objExists(x)], ne=True)
            try:
                proc = m.Plugin()
                if ('submit_server' not in args or not args['submit_server']) and not proc.execute_on_local_publish():
                    continue

                res = proc.execute(ppargs)
                print('apply_postprocs - p2', flush=True)
                buf = proc.get_outputs()
                if buf is not None:
                    postproc_outputs += buf
                
                if 'postproc_publish_textures' in pp['module_name']:
                    source_textures = res

            except Exception as e:
                print('Exception in ' + pp['label'], flush=True)
                tb = traceback.format_exc()
                tb_short = sys.exc_info()[2]
                self.tracebacks.append((tb, tb_short, e))

            self.write_tempfile('postproc_%s' % pp['module_name'][pp['module_name'].rindex('.')+1:])

        print('apply_postprocs - done', flush=True)
        return source_textures, postproc_outputs


    def import_references(self, rfn):
        print('importing references: ', rfn)
        deletable_ns = []

        try:
            ns = cmds.referenceQuery(rfn, ns=True)
        except:
            ns = None
        clds = cmds.referenceQuery(rfn, child=True, rfn=True)

        try:
            if not cmds.referenceQuery(rfn, il=True):
                print('Loading reference:', rfn)
                cmds.file(lr=rfn)
            cmds.file(ir=True, rfn=rfn)
        except Exception as e:
            print('Exception: import_references...')
            print(traceback.format_exc())
        else:
            print('Reference imported: ', rfn)
            if ns is not None:
                deletable_ns.append(ns)
            
            print('clds: ', clds)
            if type(clds) is list:
                for cld in clds:
                    buf = self.import_references(cld)
                    deletable_ns += buf

        deletable_ns = list(set(deletable_ns))

        return deletable_ns

    def execute(self, presetname=None, inputfile=None, argfile=None):
        from workfile_manager import cmds as wcmds
        from workfile_manager_maya import assetutils_maya
        dccutils = assetutils_maya.MayaUtils.get_instance()

        self.tracebacks = []
        self.inputfile = None
        self.scenefiles = []

        if not cmds.pluginInfo('fbxmaya', q=True, l=True):
            cmds.loadPlugin('fbxmaya')

        with open(argfile) as _argfile:
            args = wcmds.yaml_load(_argfile)

        print('argfile: ', argfile.replace('/', '\\'), flush=True)
        self.user = args['user']
        print('post_fbx_export(maya): wait...')
        while 'lock_file' in args and os.path.exists(args['lock_file']):
            import time
            time.sleep(1)
        print('post_fbx_export(maya): released.', flush=True)

        if 'outfile' in args:
            outfile = args['outfile']
        else:
            outfile = None

        if 'background_subprocess' in args:
            args.pop('background_subprocess')

        if inputfile is None:
            if 'inputfile' in args:
                print('inputfile: ', args['inputfile'].replace('/', '\\'))
                inputfile = args['inputfile']

        if 'sync_files' in args:
            for data in args['sync_files']:
                if data['area'] == 'work':
                    f = data['filename']
                    v = data['version']
                    buf = db.get_workasset_versions(filename=f, ignore_path_template=True, version=v)
                    print('workasset: ', buf)
                    try:
                        wasset = dccutils.create_work_asset({})
                        for k in wasset.get_dict():
                            setattr(wasset, k, buf[0][k])
                        task = wcmds.Task(interactive=False)
                        task.open_workasset(wasset, f, v)
                        print('workfile opend: ', f, v)
                    except Exception as e:
                        tb = traceback.format_exc()
                        tb_short = sys.exc_info()[2]
                        self.tracebacks.append((tb, tb_short, e))
                        print(tb)
                        print('Failed in sync workfile: ', f, v)
                else:
                    # not supported yet.
                    pass
        
        self.keep_intermediate = True if 'keep_intermediate' in args and args['keep_intermediate'] else False

        self.inputfile = inputfile
        self.scenefiles.append(inputfile)
        if 'animation_file' in args:
            self.scenefiles.append(args['animation_file'])
        
        if 'WM_SHARE_CACHED_ROOT' in os.environ:
            self.share_cache_root = assetdbutils.normalize_path(os.environ['WM_SHARE_CACHED_ROOT']).lower()
        else:
            self.share_cache_root = None
            
        if inputfile is None:
            logger.warning('!!!! inputfile is not specified. proceed without opening a file.')
        else:
            self.prepare_input()

            self.write_tempfile('maya_im03')

            #
            if 'textures' in args:
                for p, rev in args['textures']:
                    if rev is None:
                        continue
                    try:
                        print('sync... %s#%d' % (p, rev))
                        p4u.p4_run_xxx('sync', '--parallel=threads=8', '%s#%d' % (p, rev))
                        p4u.p4_run_xxx('revert', p)
                    except Exception as e:
                        print('WARNING: P4 Exception:')
                        print(e)
                        if not os.path.exists(p):
                            try:
                                p4u.p4_run_xxx('revert', p)
                            except:
                                pass
            
            tmpdir = re.sub('[.][^.]+$', '.fbm', inputfile)
            if os.path.exists(tmpdir):
                tmpdir_already_ex = True
            else:
                tmpdir_already_ex = False

            # 
            # If the UI is being launched, a pop-up will be launched if the cache reference does not exist,
            #  but since it is a batch process, it is expected to be ignored.
            cmds.file(inputfile, ignoreVersion=True, f=True, o=True, loadNoReferences=True)
            assetutils_maya.replace_to_cache_online()

            if not tmpdir_already_ex and os.path.exists(tmpdir):
                try:
                    shutil.rmtree(tmpdir)
                except FileNotFoundError:
                    pass


        self.write_tempfile('maya_im00')

        

        #last_job = True if 'last_job' in args and args['last_job'] else False
        
        try:
            assert args['frame_rate'] is not None
            if 'frame_rate' in args:
                print('setting frame rate: ', args['frame_rate'])
                dccutils.set_framerate(args['frame_rate'])
        except:
            args['frame_rate'] = dccutils.get_framerate()
            print ('frame_rate not set. use as is.')
            print('frame_rate:', args['frame_rate'])
            
        try:
            assert args['frame_range'] is not None
            if 'frame_range' in args:
                print('frame_start: ', args['frame_range'][0])
                print('frame_end: ', args['frame_range'][1])
                cmds.playbackOptions(ast=args['frame_range'][0])
                cmds.playbackOptions(aet=args['frame_range'][1])
                cmds.playbackOptions(min=args['frame_range'][0])
                cmds.playbackOptions(max=args['frame_range'][1])
        except:
            args['frame_range'] = dccutils.get_framerange()
            print ('frame_range not set. use as is.')
            print('frame_range: ', args['frame_range'])

        

        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>> outfile: ', outfile, flush=True)

        #
        assetdict = None
        if 'is_custom_task' in args and args['is_custom_task']:
            if 'share_asset' in args:
                if type(args['share_asset']) is dict:
                    args['assetdict'] = assetdict = args['share_asset']    
                else:
                    args['assetdict'] = assetdict = args['share_asset'].get_dict()
        else:
            if 'assetdict' in args:
                assetdict = args['assetdict']
            elif 'share_asset' in args:
                if type(args['share_asset']) is dict:
                    args['assetdict'] = assetdict = args['share_asset']    
                else:
                    args['assetdict'] = assetdict = args['share_asset'].get_dict()
            else:
                buf = db.get_sharedasset_from_file(outfile)
                if len(buf) == 1:
                    args['assetdict'] = assetdict = buf[0]
            
        if assetdict is None:
            raise Exception('ShareAsset not specified.')
            
        #
        if 'is_custom_task' not in args or not args['is_custom_task']:
            outdir = os.path.dirname(outfile)
            if not os.path.exists(outdir):
                os.makedirs(outdir)

            ext_maps = {'mb':'mayaBinary', 'ma':'mayaAscii', 'fbx':'mayaAscii'}
            m = re.search('[.]([^.]+)$', outfile)
            if not m:
                raise Exception('cannot specify extension.')
            ext = m.group(1)


        #
        #res = request_sync.request_sync()
        #print('request_sync: ', res)

        #
        #
        if 'selection' in args and type(args['selection'])==list:
            #print('selection key exists: ', args['selection']) # Too much information.
            selection = args['selection']
            selection = [x for x in selection if cmds.objExists(x)]
            cmds.select(selection, ne=True)
        else:
            print('selection key NOT exists.')
            selection = []
        

        pnodes = []
        for n in cmds.ls(sl=True):
            pnodes.append(pm.PyNode(n))


        # validate references and import.
        #
        deletable_ns = []
        refs = [x for x in assetutils_maya.get_valid_reference_nodes() if cmds.referenceQuery(x, parent=True, rfn=True) is None]
        
        def get_ns(x):
            if '|' in x:
                x = x[:x.index('|')]
            if ':' in x:
                ns = x[:x.rindex(':')]
                return ns
            return ''

        selected_ns = list(set([get_ns(x) for x in selection]))
        print('selected_ns: ', selected_ns)

        for r in refs:
            try:
                ref_ns = cmds.referenceQuery(r, ns=True).strip(':')
            except:
                print('ERROR: Cannot find the associated namespace.')
                continue
            print('ref_ns: ', ref_ns)
            if ref_ns not in selected_ns:
                print('not selected reference. skip.')
                continue

            ref_filename = assetdbutils.normalize_path(cmds.referenceQuery(r, filename=True, wcn=True))
            from workfile_manager import cmds as wcmds
            ref_filename = wcmds.get_share_path_from_cache(ref_filename)

            #if not ref_filename.startswith(assetutils.get_share_root()) :
            if not assetutils.is_non_cached_share_file(ref_filename) :
                message = 'WARNING: Reference outside share area published !!! by %s' % args['user']
                notif.send_to_slack(message, 'takeuchi_kengo')
                if os.path.exists(ref_filename):
                    deletable_ns += self.import_references(r)
            else:
                buf = db.get_sharedasset_from_file(ref_filename)
                print('ref_filename: ', ref_filename)
                print('buf: ', buf)
                if len(buf) == 0:
                    message = 'ERROR: ref_filename not found in DB: ' + ref_filename
                    notif.send_to_slack(message, 'takeuchi_kengo')
                ref_assetdict = buf[0]


                if assetdict is not None and assetdict['task'] == 'animation' and ('keep_references' not in args or not args['keep_references']):
                    if ref_assetdict['task'] != 'animation':
                        deletable_ns += self.import_references(r)

        args['deletable_ns'] = deletable_ns
        print('deletable_ns: ', deletable_ns, flush=True)

        self.write_tempfile('maya_im04')

        # apply postproccess.
        source_textures, postproc_outputs = self.apply_postprocs(args, pnodes)
        print('source_textures: ', source_textures)
        print('postproc_outputs: ', postproc_outputs, flush=True)

        # apply mel cmds.
        if 'mel_cmds' in args and args['mel_cmds']:
            for melcmd in args['mel_cmds']:
                if melcmd.startswith('breakInputConnection'):
                    breakInputConnections(melcmd.split(' ')[1])
                else:
                    try:
                        print('Executing: ', melcmd)
                        mel.eval(melcmd)
                    except Exception as e:
                        print('Trying one without namespce...')
                        melcmd = re.sub('\w*:', '', melcmd)
                        try:
                            mel.eval(melcmd)
                        except Exception as e:
                            tb = traceback.format_exc()
                            tb_short = sys.exc_info()[2]
                            self.tracebacks.append((tb, tb_short, e))

        # quit if is_custom_task
        print('is_custom_task? : ', True if 'is_custom_task' in args and args['is_custom_task'] else False, flush=True)

        if 'is_custom_task' in args and args['is_custom_task']:
            self.write_tempfile('maya_im05')
            return
        
        if 'additional_select' in args:
            for n in args['additional_select']:
                if type(n) is str or wcmds.is_py2_unicode(n):
                    try:
                        pn = pm.PyNode(n)
                    except:
                        pn = None
                    
                    if pn is not None:
                        pnodes.append(pn)

                elif issubclass(type(n), pm.PyNode):
                    pnodes.append(n)

        self.write_tempfile('maya_im001')

        if 'comment' in args:
            comment = args['comment']
        elif 'comment' in assetdict:
            comment = assetdict['comment']
        else:
            comment = ''

        from workfile_manager.plugin_utils import Application
        if args['publish_app'] == Application.Maya:
            print('pnodes: ', pnodes, flush=True)
            ex_pnodes = [x for x in pnodes if pm.objExists(x)]
            print('ex_pnodes: ', ex_pnodes)
            kargs = {'f':True, 'type':ext_maps[ext], 'pr':True}
            if len(ex_pnodes) > 0:
                kargs['es'] = True
                pm.select(ex_pnodes, ne=True)
            else:
                buf = cmds.ls(args['selection'])
                if len(buf) > 0:
                    cmds.select(buf, ne=True)
                    kargs['es'] = True
                else:
                    kargs['save'] = True
            
            # restore cached references to original paths.
            assetutils_maya.replace_to_cache_online(restore=True, texture=False, force_reload=True)

            #
            cmds.file(rename=outfile)
            maya_output = cmds.file(**kargs)
            cmd = 'python("import setup_callback_onsave.setup;setup_callback_onsave.setup.embed_scene_desc(None)");file -f -save;'
            subprocess.call('mayabatch -file %s -command "%s"' % (outfile, cmd.replace('"', '\\"')))
            print('scene description embeded!!!')

            lines = []

            print('maya_output: ', maya_output.replace('/', '\\'))

            self.write_tempfile('maya_im01')

            if maya_output.endswith('.ma'):
                with open(maya_output, 'r') as f:
                    for line in f:
                        line = re.sub('^file ', 'file -iv ', line)
                        lines.append(line)
                with open(maya_output, 'w') as f:
                    f.writelines(lines)
                    
            fbxfile = re.sub('[.][^.]+$', '.fbx', outfile)
            preset = os.path.join(os.path.dirname(__file__), 'fbx_presets', presetname)
            preset = re.sub('\\\\', '/', preset)
            mel.eval('FBXLoadExportPresetFile -f "%s"' % preset)
            mel.eval('FBXExport -s -f "%s"' % fbxfile)
            self.write_tempfile('maya_im02')
            
            # Copy thumbnail and overlay icon
            #
            if 'thumbnail_source' in args and args['thumbnail_source'] and os.path.exists(args['thumbnail_source']):
                thumb = args['thumbnail_source']
                print('>>>>>>>>>>>>>>>>>>> thumbnail_source: ', thumb.replace('/', '\\'))
            else:
                thumb = assetutils.Asset.thumbnail_filepath(outfile, assetdict['version'], replace_share_root=True)
                print('>>>>>>>>>>>>>>>>>   thumbnail: ', thumb.replace('/', '\\'))

            thumb = assetdbutils.normalize_path(thumb)

            if not os.path.exists(thumb):
                if 'dont_create_thumbnail' not in args or not args['dont_create_thumbnail']:
                    try:
                        create_thumbnail(thumb)
                    except Exception as e:
                        logger.error(e)

            thumb_share = assetutils.Asset.thumbnail_filepath(outfile, assetdict['version'], replace_share_root=False)
            thumb_share = assetdbutils.normalize_path(thumb_share)
            if os.path.exists(thumb):
                _dir = os.path.dirname(thumb_share)
                if not os.path.exists(_dir):
                    os.makedirs(_dir)

                ffmpeg = os.environ['FFMPEG_EXE']

                def is_source_on_share(thumb):
                    if 'WM_TMP_DIR' in os.environ:
                        if thumb.startswith(assetdbutils.normalize_path(os.environ['WM_TMP_DIR'])):
                            return False
                    if assetutils.is_non_cached_share_file(thumb):
                        return True
                    return False

                if assetdict['task'] == 'animation' and not is_source_on_share(thumb) and ('dont_overlay_icon' not in args or not args['dont_overlay_icon']):
                    play_icon = os.environ['WM_PLAYBACK_ICON']
                    convcmd = '%s -y -i %s -i %s ' % (ffmpeg, thumb, play_icon) + \
                        ' -filter_complex "[1]geq=r=\'r(X,Y)\':a=\'alpha(X,Y)/3\'[icon];[0][icon]overlay=\'W/2-120\':\'H/2-120\'" ' + thumb_share
                    print('convcmd: ', convcmd)
                    subprocess.call(convcmd)
                else:
                    src = thumb.replace('/', '\\')
                    dst = thumb_share.replace('/', '\\')
                    print('src: ', src)
                    print('dst: ', dst)
                    subprocess.call('%s -y -i %s %s' % (ffmpeg, src, dst), shell=True) # dont use copy cmd in case file format differs.

                if not is_source_on_share(thumb) and not assetutils.is_in_p4_workspace(thumb):
                    os.remove(thumb)

            else:
                logger.error('thumbnail not exists: %s', thumb.replace('/', '\\'))

            # Save references.
            #
            refs = dccutils.getrefs()
            if postproc_outputs is not None:
                refs += postproc_outputs
            
            # resume cached share paths.
            for i, r in enumerate(refs):
                refs[i] = assetdbutils.normalize_path(refs[i])
                if r.lower().startswith(self.share_cache_root):
                    refs[i] = assetutils.get_share_root()
                    if not refs[i].endswith('/'):
                        refs[i] += '/'
                    refs[i] += r[len(self.share_cache_root):].strip('/')

            # exclude non-share refs.
            #  - Not published textures will be excluded here.
            refs = [x for x in refs if x.startswith(assetutils.get_share_root())]
            
            #
            asset = dccutils.create_share_model_asset({})
            
            for k in list(asset.__dict__.keys()):
                asset.set_token(k, assetdict[k])
            
            
            print(source_textures)
            if 'submit_server' in args and args['submit_server']:
                db.publish_refs(asset, outfile, refs, args['user'] if 'user' in args else p4u.user, source_textures=source_textures)
            # Delete temporal files.
            if thumb and os.path.exists(thumb) and thumb != thumb_share \
                    and ('dont_delete_tmp_thumbnail' not in args or not args['dont_delete_tmp_thumbnail']) \
                    and not assetutils.is_in_p4_workspace(thumb):
                os.remove(thumb)
            # update database
            #
            assetdict['success'] = 1
            assetdict['frame_start'] = args['frame_range'][0]
            assetdict['frame_end'] = args['frame_range'][1]
            assetdict['frame_rate'] = args['frame_rate']

            if 'submit_server' in args and args['submit_server']:
                db.update_versions_shared([assetdict], updatekeys=['success', 'frame_start', 'frame_end', 'frame_rate'])

            

            if 'from_publish_files' in args:
                pass
            else:
                if len(self.tracebacks) > 0:
                    header = u'パブリッシュが完了しました。（エラーが発生していますが、対応が必要な場合は管理者からご連絡します。）\n'
                else:
                    header = u'パブリッシュが完了しました。\n'
                
                #
                try:
                    asseturl = asset.get_url(outfile)
                except:
                    asseturl = outfile.replace('/', '\\')

                #   
                message = u'*コメント*\n```%s```' % comment + '\n'
                message += u'*出力アセット*\n' + '```' + asseturl + '```'
                try:
                    notif.send_to_slack(header + message, args['user'])
                except Exception as e:
                    tb = traceback.format_exc()
                    print('ERROR: Failed to send to slack.')
                    tb_short = sys.exc_info()[2]
                    self.tracebacks.append((tb, tb_short, e))   

                    message = u'*コメント*\n```(DecodeError)```\n'
                    message += u'*出力アセット*\n' + '```' + asseturl + '```'
                    try:
                        notif.send_to_slack(header + message, args['user'])
                    except:
                        pass
        else:
            # Commit process will be skipped if publish operation is done within MotionBuilder.
            args['commit_to_engine'] = False

        print('>>>>>>>>>>>>> commit_to_engine?: ', args['commit_to_engine'])

        if args['commit_to_engine']:
            print('Committing to engine...')

            if asset.task == 'model':
                engine_asset = assetutils_maya.MayaUtils.get_instance().create_engine_model_asset({})
            elif asset.task == 'animation':
                engine_asset = assetutils_maya.MayaUtils.get_instance().create_engine_anim_asset({})
            else:
                raise Exception('Not supported asset type.')

            tags = args['tags']

            engine_asset.__dict__ = copy.deepcopy(asset).__dict__
            
            engine_asset.set_path_template(tags=tags)
            
            db.replace_tags(asset=engine_asset, tags=tags, username=args['user'] if 'user' in args else p4u.user)
            
            
            
            args['preset'] = presetname
            args['comment'] = comment
            args['targets'] = [{'filename':outfile, 'asset':engine_asset, 'tags':args['tags'], 'assetdict':assetdict}]

            assetutils_maya.CleanupArgs().execute(args)
            
            try:
                print('args:', args)
                if os.path.exists(argfile):
                    tmpfile = assetutils.get_publish_tempfilename(argfile)
                    print('tmp_argfile:', tmpfile.replace('/','\\'))
                    shutil.copyfile(argfile, tmpfile)
            except Exception as e:
                tb = traceback.format_exc()
                tb_short = sys.exc_info()[2]
                self.tracebacks.append((tb, tb_short, e))

            with open(argfile, 'w') as _argfile:
                yaml.dump(args, _argfile)
            
            from workfile_manager_maya.export.on_commit_proc import on_commit_proc
            on_commit_proc.execute(argfile=argfile, open_scene=True)
            
        try:
            if inputfile is not None and not assetutils.is_non_cached_share_file(inputfile):
                if 'keep_intermediate' not in args or not args['keep_intermediate']:
                    subprocess.call('attrib -R %s' % inputfile)
                    os.remove(inputfile)
        except:
            print('Error: Failed in deleting a source file: ', inputfile)

    print(flush=True)

def postfunc(presetname=None, inputfile=None, argfile=None):
    print('>>>>>>>>>>>>> postfunc')
    task = Task()
    try:
        task.execute(presetname, inputfile, argfile)
    except Exception as e:
        tb = traceback.format_exc()
        tb_short = sys.exc_info()[2]
        task.tracebacks.append((tb, tb_short, e))


    if len(task.tracebacks) > 0:
        message = u'パブリッシュ（もしくはコミット）時にエラーが発生しました。\n' + \
            u'*ユーザー名*\n```' + task.user + '```\n' + \
            u'*シーンファイル*\n' + '```%s```\n' % '\n'.join([x for x in task.scenefiles if x is not None])
        tbs = ('%s\n' % ('='*40)).join([x[0] for x in task.tracebacks])
        print('=== Tracebacks ===============================')
        print(tbs, flush=True)

        try:
            message += u'*エラー*\n' + '```' + tbs + '```\n'
        except UnicodeDecodeError:
            message = u'エラーメッセージ生成時にUnicodeDecodeErrorが発生しました。'

        try:
            # Python2
            import urllib2
            HTTP_ERROR = urllib2.HTTPError
        except:
            # Python3
            import urllib.error, importlib
            HTTP_ERROR = urllib.error.HTTPError

        for tb in task.tracebacks:
            print('>tb: ', tb, flush=True)
            if not issubclass(type(tb[2]), HTTP_ERROR):
                break
        else:
            print(u'No errors exist except HTTPError.', flush=True)
            return
        
        try:
            for user in ['takeuchi_kengo', 'tanaka_ko']:
                #channel = 'C016STV8P0S' # test channel
                channel = 'C033GJ3UW07' # The official channel to send error reports to.
                notif.send_to_slack(message, channel, mentions=['takeuchi_kengo', 'tanaka_ko'], is_channel=True, channel_mention=False, header=(p4u.user, u'パブリッシュ時のエラー通知'))

        except:
            print('ERROR: Failed to send to slack.(2)')
            print(traceback.format_exc(), flush=True)

        
        #sys.exit(1)
        cmds.quit(f=True, exitCode=1)
    
    else:
        cmds.quit(f=True, exitCode=0)
