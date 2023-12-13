# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import os
import subprocess
import glob
import shutil
import copy

from Qt import QtCore, QtWidgets

try:
    import maya.cmds as cmds
    import maya.mel as mel
    import pymel.core as pm
    from workfile_manager_maya.export.preproc.all import preproc_texture_filename as preproc_tex
except:
    pass

from cylibassetdbutils import assetvar

from cylibassetdbutils import assetutils, assetdbutils

from workfile_manager import dccutils
from workfile_manager.ui import uiutils, ui_main

db = assetdbutils.DB.get_instance()

def clear_modelpanel_callback():
    for item in pm.lsUI(editors=True):
        if isinstance(item, pm.ui.ModelEditor):
            ecc = pm.modelEditor(item, q=True, editorChanged=True)
            if ecc in 'CgAbBlastPanelOptChangeCallback':
                pm.modelEditor(item, edit=True, editorChanged="")

def replace_to_cache(filename, depth=0, done=[]):
    if filename in done:
        return
    print('replace_to_cache: ', filename)
    from workfile_manager import cmds
    if 'WM_SHARE_CACHED_ROOT' not in os.environ:
        return

    def does_match_cache(expr_c, line, done=[]):
        m = expr_c.search(line)
        if m:
            ref = m.group(1) + m.group(2)
            orgfile = cmds.get_share_path_from_cache(ref)
            cmds.cache_sharefile(orgfile)
            if ref.endswith('.ma'):
                replace_to_cache(ref, depth=depth+1, done=done)
            return True
        else:
            return False

    def does_match_share(expr, line, done=[], replace_to_current_share_root=False):
        m = expr.search(line)
        if m:
            if replace_to_current_share_root:
                ref = os.environ['WM_SHARE_ROOT'] + m.group(2)
            else:
                ref = m.group(1) + m.group(2)
            _, cached = cmds.cache_sharefile(ref)
            if cached.endswith('.ma'):
                replace_to_cache(cached, depth=depth+1, done=done)
            line = expr.sub('"%s"' % cached, line)
            return line
        else:
            return None

    lockfile = filename + '.lock'
    lockfile_dir = os.path.dirname(lockfile)
    if not os.path.exists(lockfile_dir):
        os.makedirs(lockfile_dir)
    import filelock
    lock = filelock.FileLock(lockfile)
    print('Acquiring filelock: ', lockfile, '(replace_to_cache)')
    with lock.acquire():
        croot = assetdbutils.normalize_path(os.environ['WM_SHARE_CACHED_ROOT'])
        
        share_root = assetdbutils.normalize_path(os.environ['WM_SHARE_ROOT'])
        expr = re.compile('"(%s)([^"]*)"' % share_root, re.IGNORECASE)

        if 'WM_SHARE_ROOT_ALT' in os.environ:
            share_root_alt = assetdbutils.normalize_path(os.environ['WM_SHARE_ROOT_ALT'])
            _share_root_alt = re.sub('[/]', '[/]', share_root_alt)
            exp_str = '"(%s)([^"]*)"' % _share_root_alt
            expr_alt = re.compile(exp_str, re.IGNORECASE)
        else:
            expr_alt = None

        expr_c = re.compile('"(%s)([^"]*)"' % croot, re.IGNORECASE)
        outlines = []
        modified = False
        try:
            skip_line = False
            with open(filename, 'r') as fhd:
                for line in fhd:
                    line_org = line
                    if line.startswith('createNode'):
                        node_type = line[11:][:line[11:].find(' ')].strip()
                        if node_type != 'file':
                            skip_line = True
                        else:
                            skip_line = False
                        outlines.append(line)
                        continue
                    else:
                        if skip_line:
                            outlines.append(line)
                            continue

                    if not does_match_cache(expr_c, line, done=done):
                        res = does_match_share(expr, line)
                        if res is None:
                            if expr_alt:
                                res = does_match_share(expr_alt, line, done=done, replace_to_current_share_root=True)
                                if res is not None:
                                    line = res
                        else:
                            line = res
                    
                    outlines.append(line)
                    if line != line_org:
                        modified = True
        except:
            import traceback
            print(traceback.format_exc())
            done.append(filename)
            return False

        else:
            if modified:
                tmpfile = assetutils.get_publish_tempfilename_local(filename)
                tmpdir = os.path.dirname(tmpfile)
                if not os.path.exists(tmpdir):
                    os.makedirs(tmpdir)
                
                with open(tmpfile, 'w') as fhd:
                    fhd.writelines(outlines)
                shutil.copystat(filename, tmpfile)

                subprocess.call('attrib -R "%s"' % filename)
                shutil.copyfile(tmpfile, filename)
                shutil.copystat(tmpfile, filename)
                os.remove(tmpfile)
                
                subprocess.call('attrib +R "%s"' % filename)
                print('replaced file written: ', filename)
            done.append(filename)
            return True

def remove_malicious_scriptjobs():
    def remove_prompt(fpath):
        m = u'PCに不正なMayaの設定ファイルが検出されました。\n\n意図したものでなければ削除することを強く推奨します。\n\n' + \
            u'（複数ファイル存在する場合は、複数回このポップアップが起動することがあります。）\n\n'
        wd = QtWidgets.QTextEdit(fpath.replace('/', '\\'))
        wd.setReadOnly(True)
        w = uiutils.PromptDialog('Warning', m, btns=['Delete', 'Cancel'], wd=wd)
        w.resize(800, 200)
        res = w.exec_()
        if res == 1:
            fpath = fpath.replace('\\', '/')
            print('fpath:', fpath)
            try:
                os.remove(fpath)
            except:
                w = uiutils.PromptDialog('Warning', u'ファイルが使用中のため削除できませんでした。\n\n該当アプリケーションを閉じた後にあらためて削除をお願いします。\n\n', wd=wd, btns=['OK'])
                w.resize(800, 200)
                w.exec_()

    jobs = cmds.scriptJob(lj=True)
    buf = [x for x in jobs if 'leukocyte.antivirus' in x]
    if len(buf) > 0:
        for job in buf:
            jobid = int(job[:job.index(':')])
            cmds.scriptJob(f=True, k=jobid)

        path = 'C:/Users/%s/Documents/maya/scripts' % os.environ['USERNAME']
        for _file in os.listdir(path):
            fpath = os.path.join(path, _file)
            if _file.startswith('vaccine.py'):
                remove_prompt(fpath)
            elif _file == 'userSetup.py':
                with open(fpath, 'r') as fhd:
                    lines = fhd.readlines()
                    buf = [x for x in lines if 'import vaccine' in x]
                    if len(buf) > 0:
                        remove_prompt(fpath)

class WorkAssetMaya(assetvar.WorkAsset):
    def open(self, filename):
        try:
            rem_garbage = ui_main.mwin.ui_prefs.var['miscellaneous']['cleanup-in-file-open']
        except:
            import traceback
            print(traceback.format_exc())
            rem_garbage = False

        print('rem_garbage:', rem_garbage)

        if rem_garbage:
            remove_garbage_from_ma(filename)
        try:
            cmds.file(filename, ignoreVersion=True, o=True, f=True)
        except Exception as e:
            print(e)
   
    def exportself(self, filename, args=None):
        if filename is None or filename == '':
            return None, ''

        #
        remove_malicious_scriptjobs()
        buf = cmds.ls(['breed_gene', 'vaccine_gene'], type='script')
        if len(buf) > 0:
            cmds.delete(buf)

        #
        orgproj = cmds.workspace(q=True, rd=True)
        scn = os.path.dirname(filename)
        proj = os.path.dirname(scn)
        mel.eval('setProject "%s"' % proj)

        if not check_texture_path():
            mel.eval('setProject "%s"' % orgproj)
            return None, ''

        cmds.file(rename=filename)
        if cmds.file(q=True, mf=True):
            #cmds.file(type='mayaAscii', save=True)
            _save({'type':'mayaAscii'})
        return filename, ''
    
    def get_extension(self):
        return 'ma'

    def export_thumbnail(self, filename, ver, mwin=None):
        return MayaUtils.get_instance().export_thumbnail(filename, ver)

    def dccutils(self):
        return MayaUtils

    def is_updatable(self):
        return True

    def is_reference_updatable(self):
        return True

    def replace_to_cache(self, filename):
        replace_to_cache(filename, done=[])

    def post_save(self, args):
        cmds.file(mf=0)


def _save(args):
    filename = cmds.file(q=True, sn=True)
    subprocess.call('attrib -R "%s" /S /D' % filename)
    cmds.file(s=True, f=True, **args)
    if filename.endswith('ma'):
        _filename = filename + '~'
        shutil.copyfile(filename, _filename)
        _fix_reference_and_etc(_filename, filename)
        os.remove(_filename)

class MayaAsciiContext:
    CreateUIiConfig = 1,

def _fix_reference_and_etc(_filename, filename):
    pt = re.compile(r'^\s*file ')
    pt2 = re.compile(r'^\s*createNode script .*"uiConfigurationScriptNode"')
    pt3 = re.compile(r'^\s+')
    context =  None

    with open(_filename, 'r') as f:
        with open(filename, 'w') as of:
            for line in f:
                if context is None:
                    if pt.search(line):
                        if not re.search('^\s*file -ignoreVersion ', line):
                            line = pt.sub('file -ignoreVersion ', line)
                    elif pt2.search(line):
                        context = MayaAsciiContext.CreateUIiConfig
                        continue
                elif context == MayaAsciiContext.CreateUIiConfig:
                    if pt3.search(line):
                        continue
                    else:
                        context = None

                of.write(line)


ext_maps = {'mayaBinary':'mb', 'mayaAscii':'ma'}

def get_kargs(args):
    kargs = {'f':True, 'type':'mayaAscii', 'pr':True}
    sel = cmds.ls(sl=True)
    if 'export_all' not in args or not args['export_all']:
        if len(sel) == 0:
            raise Exception('Nothing selected.')
        kargs['es'] = True
    else:
        kargs['ea'] = True
    return kargs

class ToDelete(object):
        pass

class CleanupArgs:
    def __init__(self):
        self.done = []

    def execute(self, args, all_pynodes=False):
        ###########
        return
        ###########

        import pymel.core.general

        if type(args) is list or type(args) is dict:
            buf = [x for x in self.done if x is args]
            if len(buf) > 0:
                return args
            self.done.append(args)

        if type(args) is dict:
            for k in copy.deepcopy(list(args.keys())):
                res = self.execute(args[k], all_pynodes=all_pynodes)
                if type(res) is ToDelete:
                    args.pop(k)
                else:
                    args[k] = res
            
            return args

        elif type(args) is list:
            for i, v in enumerate(args):
                res = self.execute(v, all_pynodes=all_pynodes)
                if type(res) is ToDelete:
                    args[i] = None
                else:
                    args[i] = res

            while None in args:
                idx = args.index(None)
                args.pop(idx)

            return args

        else:
            if issubclass(type(args), pymel.core.general.PyNode):
                if not all_pynodes and cmds.objExists(args.name()):
                    return args
                else:
                    return ToDelete()
            else:
                return args

class ShareAssetMaya(assetvar.ShareAsset):
    def exportself(self, filename, args):
        #print '>>>>>>>>>>>>>>>>>>> cleanupArgs...', args
        CleanupArgs().execute(args, all_pynodes=True)
        #print '>>>>>>>>>>>>>>>>>>> cleanupDone.', args
        return self.exportbase(filename, args)

    def dccutils(self):
        return MayaUtils
        
    def dirname(self):
            return 'fbx'

    def open(self, filename):
        cmds.file(filename, ignoreVersion=True, o=True, f=True)

    def select(self, items):
        MayaUtils.get_instance().select(items)

    def get_postproc_cmd(self, filename, args):
        CleanupArgs().execute(args, all_pynodes=True)
        cmd = 'python("%s")' % self._get_postproc_cmd(args)
        return cmd

    def get_framerange(self):
        return MayaUtils.get_instance().get_framerange()

    def get_framerate(self):
        return MayaUtils.get_instance().get_framerate()

    def set_framerate(self, v):
        return MayaUtils.get_instance().set_framerate(v)
        


    def _get_namespace1(self, namespace_option, self_namespace, r):
        ns = ':'
        if namespace_option == 0:
            pass
        elif namespace_option == 1:
            global ns_input
            ns_input = ''
            w = QtWidgets.QWidget()
            hbox = QtWidgets.QHBoxLayout(w)
            lb = QtWidgets.QLabel('Namespace: ')
            le = QtWidgets.QLineEdit()
            le.textEdited.connect(self._ns_le_clicked)
            hbox.addWidget(lb)
            hbox.addWidget(le)

            res = uiutils.PromptDialog('Reference' if r else 'Import' , \
                'Input %s namespace' % ('reference' if r else 'import'), wd=w, btns=['OK', 'Cancel']).exec_()
            if res != 1:
                return
            ns = ns_input

        elif namespace_option == 2:
            ns = self_namespace
        elif namespace_option == 3:
            buf = cmds.ls(sl=True)
            if len(buf) == 0:
                #ns = self_namespace
                pass
            else:
                m = re.search('([^|:]+):[^|:]*$', buf[0])
                if m:
                    ns = m.group(1)
                else:
                    #ns = namespace
                    pass
        else:
            raise Exception('Invalid namespace option specified.')
        
        return ns

    def get_import_namespace(self, ns1, self_namespace):
        return ns1
    def get_target_namespace(self, ns1, self_namespace):
        return ns1

    def import_(self, filename, namespace_option=3, namespace=None, r=False, import_mode='Update'):
        all_objs = cmds.ls(l=True)

        sel = pm.ls(sl=True)

        if not cmds.pluginInfo('fbxmaya', q=True, l=True):
            cmds.loadPlugin('fbxmaya')
            
        

        filename = self.exact_filename(filename)
        
        if not filename or not os.path.exists(filename):
            uiutils.PromptDialog('Error', u'ファイルが存在しません', btns=['OK']).exec_()
            return
   
        self.load_import_preset()
        
        ns_org = cmds.namespaceInfo(cur=True)
        ns1 = self._get_namespace1(namespace_option, namespace, r)
        
        import_namespace = self.get_import_namespace(ns1, namespace)
        target_namespace = self.get_target_namespace(ns1, namespace)

        id = 0
        exns = cmds.namespaceInfo(':', lon=True)
        for n_ in exns:
            print('exns: ', n_)

        if import_mode != 'Update' or r:
            while True:
                if import_namespace not in exns:
                    break
                id += 1
                m = re.search('_\d{3}$', import_namespace)
                if m:
                    import_namespace = re.sub('_\d{3}$', '_%03d' % id, import_namespace)
                else:
                    import_namespace += '_%03d' % id

        cur_set = False
        if import_namespace and not r and import_mode == 'Update':
            if not cmds.namespace(ex=import_namespace):
                cmds.namespace(add=import_namespace)
            cmds.namespace(set=import_namespace)
            cur_set = True

        print('import_namespace: ', import_namespace)
        print('import_mode: ', import_mode)
        mel.eval('FBXImportMode -v %s' % ('add' if import_mode=='Append' else 'merge'))

        if r or import_mode == 'Append':
            cmds.file(filename, ignoreVersion=True, r=True, f=True, ns=import_namespace, pr=True, rfn=namespace+'RN')
        else:
            cmds.file(filename, ignoreVersion=True, i=True, f=True, pr=True)
        
        if cur_set:
            cmds.namespace(set=ns_org)


        self.post_import(filename, import_namespace=import_namespace, target_namespace=target_namespace)
    
        _sel = []
        for n in sel:
            if pm.objExists(n):
                _sel.append(n)
        if len(_sel) > 0:
            pm.select(_sel)

        imported_object = []
        for n in cmds.ls(l=True):
            if n not in all_objs:
                imported_object.append(n)
        return {'imported_object':imported_object, 'import_namespace':import_namespace}


    def _ns_le_clicked(self, v):
        global ns_input
        ns_input = v

    def post_import(self, filename, import_namespace, target_namespace):
        return


    #def reference(self, filename, ns):
    #    cmds.file(filename, ignoreVersion=True, r=True, f=True, ns=ns)

    def get_extension(self):
        return 'ma'

    def export_thumbnail(self, filename, ver, mwin=None):
        return MayaUtils.get_instance().export_thumbnail(filename, ver)


    def store_other_args(self, filename, args):
        sel = cmds.ls(sl=True)
        if 'export_all' not in args or not args['export_all']:
            if len(sel) == 0:
                return None, 'Nothing selected.'

        kargs = get_kargs(args)
        
        unknowns = cmds.ls(type='unknown')
        if len(unknowns) > 0:
            kargs['type'] = cmds.file(q=True, type=True)[0]
            filename = re.sub('[.][^.]+$', '.' + ext_maps[kargs['type']], filename)
        
        if 'selection' not in args:
            if len(sel) > 0:
                args['selection'] = sel
            else:
                args['selection'] = None
        

        try:
            if 'textures' not in args:
                target_nodes = get_nodes_to_export_selection()
                buf = _get_textures(target_nodes=target_nodes)
                args['textures'] = assetutils._get_textures_2(buf)
        except Exception as e:
            print(e.args)

            return None, '\n'.join([str(x) for x in e.args])


        return filename, None

    def save_tempfile(self, tmpfilename, args):
        kargs = get_kargs(args)

        if not os.path.exists(os.path.dirname(tmpfilename)):
            os.makedirs(os.path.dirname(tmpfilename))
        
        cmds.select('persp', add=True)

        if 'inputfile_source' in args:
            print('inputfile_source: ', args['inputfile_source'])
            shutil.copyfile(args['inputfile_source'], tmpfilename)
        else:
            try:
                cmds.file(tmpfilename, **kargs)

            except Exception as e:
                m = 'Invalid cmds.file argument: ' + str(kargs)
                uiutils.ErrorDialog(message=m).exec_()
                raise Exception('Failed in save_tempfile.')

        lines = []
        with open(tmpfilename, 'r') as f:
            for line in f:
                line = re.sub('^file ', 'file -iv ', line)
                lines.append(line)
        with open(tmpfilename, 'w') as f:
            f.writelines(lines)

    

    def is_updatable(self):
        return True

    def is_reference_updatable(self):
        return True

    def replace_to_cache(self, filename):
        replace_to_cache(filename, done=[])

def _get_refnodes_and_textures(target_nodes=None):
    buf = []
    for _type in texture_types:
        try:
            nodes = cmds.ls(type=_type['type'])
        except:
            continue

        _nodes = nodes if target_nodes is None else [x for x in nodes if x in target_nodes]
        for node in _nodes:
            if 'get_command' in _type:
                files = _type['get_command'](node)
            else:
                f_ = assetdbutils.normalize_path(cmds.getAttr(node+'.'+_type['attr']))
                files = [f_]

            buf += [(node, x) for x in files]

    return buf

def _get_textures(target_nodes=None):
    buf = _get_refnodes_and_textures(target_nodes=target_nodes)
            
    res = []
    for f in [x[1] for x in buf]:
        if not os.path.exists(f) or not os.path.isfile(f):
            continue
        if not re.search('^[^:]+:', f) and not re.search('^/', f):
            wd = cmds.workspace(q=True, rd=True)
            f = os.path.join(wd, f)
        
        f = assetdbutils.normalize_path(f)
        if os.path.exists(f) and f not in res:
            res.append(f)
            
    return res

def get_textures_from_filenode(filenode):
    f_ = assetdbutils.normalize_path(cmds.getAttr(filenode+'.fileTextureName'))
    files = [f_]
    if cmds.getAttr(filenode+'.uvTilingMode') == 3:
        m = re.search('^(.*)[.]\d{4}[.](.*)$', f_)
        if m:
            ptn = '%s.*.%s' % (m.group(1), m.group(2))
            files = glob.glob(ptn)

    files = [assetdbutils.normalize_path(x) for x in files]
    return files

#def get_cache_from_geomcache(cachenode):
#    path = cmds.getAttr(cachenode+'.cachePath')
#    prefix = cmds.getAttr(cachenode+'.cacheName')
#    files = []
#    buf = glob.glob(os.path.join(path, prefix)+'.xml')
#    if len(buf) > 0:
#        files += buf
#    buf = glob.glob(os.path.join(path, prefix)+'Frame*.mcx')
#    if len(buf) > 0:
#        files += buf
#
#    files = [assetdbutils.normalize_path(x) for x in files]
#    return files

texture_types = [
    {
        'type':'file',
        'attr':'fileTextureName',
        'get_command':get_textures_from_filenode,
    },
    {
        'type':'GLSLShader',
        'attr':'shader',
    },
    {
        'type':'AlembicNode',
        'attr':'abc_File',
    },
    #{
    #    'type':'cacheFile',
    #    'attr':'cachePath',
    #    'get_command':get_cache_from_geomcache,
    #},

]


class AnimationAssetMaya(ShareAssetMaya):
    def presetname(self):
        return 'animation.fbxexportpreset'

    def load_import_preset(self):
        preset = os.path.join(os.path.dirname(__file__), 'import', 'fbx_presets', 'animation.fbximportpreset')
        preset = preset.replace('\\', '/')
        mel.eval('FBXLoadImportPresetFile -f "%s"' % preset)

    def exact_filename(self, filename):
        return re.sub('[.][^.]+$','.fbx', filename)

class ModelAssetMaya(ShareAssetMaya):
    def presetname(self):
        return 'model.fbxexportpreset'

    def load_import_preset(self):
        preset = os.path.join(os.path.dirname(__file__), 'import', 'fbx_presets', 'model.fbximportpreset')
        preset = preset.replace('\\', '/')
        print('preset: ', preset)

        mel.eval('FBXLoadImportPresetFile -f "%s"' % preset)

    
    def exact_filename(self, filename):
        return filename

class MaterialAssetMaya(ShareAssetMaya):
    def presetname(self):
        return 'model.fbxexportpreset'

    def load_import_preset(self):
        preset = os.path.join(os.path.dirname(__file__), 'import', 'fbx_presets', 'model.fbximportpreset')
        preset = preset.replace('\\', '/')
        print('preset: ', preset)

        mel.eval('FBXLoadImportPresetFile -f "%s"' % preset)

    
    def exact_filename(self, filename):
        return filename

    def get_import_namespace(self, ns1, self_namespace):
        nss = cmds.namespaceInfo(ls=True)
        i = 1
        newname = self_namespace
        while True:
            if newname in nss:
                newname = re.sub('_\d+$', '', newname) + '_%d' % i
                i += 1
                continue
            else:
                break
        return newname

        return self_namespace

    def post_import(self, filename, import_namespace, target_namespace):
        print('post_import.')
        from workfile_manager import cmds as wcmds
        filename = wcmds.get_share_path_from_cache(filename)

        import yaml
        refs = db.get_share_asset_refs(filename=filename)
        print('filename: ', filename)
        print('refs: ', refs)
        for ref in [x['local_path'] for x in refs]:
            print('>>', ref)
            if not ref.endswith('.material_info'):
                continue
            hdl = open(ref, 'r')
            info = wcmds.yaml_load(hdl)
            break
        else:
            return
            
        if 'assignment' not in info:
            return

        assign = info['assignment']
        print('assign: ', assign)
        for se in list(assign.keys()):
            _members = assign[se]
            members = _members.split(' ')
            print('memebers: ', members)
            cmds.select(cl=True)
            for m in members:
                if target_namespace != ':':
                    m = target_namespace + ':' + m
                print('m: ', m)
                if cmds.objExists(m):
                    cmds.select(m, add=True)
            print('targets: ', cmds.ls(sl=True))
            if len(cmds.ls(sl=True)) == 0:
                continue
            se = import_namespace + ':' + se if import_namespace is not None else se
            print('shadingEngine: ', se)
            cmds.sets(e=True, forceElement=se)



class SetdressAssetMaya(ShareAssetMaya):
    pass

class EngineAssetMaya(assetvar.EngineAsset, object):
    def is_reference_updatable(self):
        return True
        
    def dccutils(self):
        return MayaUtils
        
    def open(self, filename, uassets=None, updated_files=None):
        from workfile_manager import cmds as wcmds
        if not cmds.pluginInfo('fbxmaya', q=True, l=True):
            cmds.loadPlugin('fbxmaya')
        cmds.file(filename, ignoreVersion=True, o=True, f=True)

        # Import extra parameters.
        #
        ex_filename = re.sub('[.][^.]+$', '.exprm', filename)
        if os.path.exists(ex_filename):
            import yaml
            with open(ex_filename, 'r') as fhd:
                params = wcmds.yaml_load(fhd)
                nodes = params['application']['maya']['nodes']
                for nodename in nodes:
                    for item in nodes[nodename]:
                        pname = item['attribute']
                        value = item['value']
                        ptype = item['attr_type']
                        try:
                            if ptype == 'string':
                                cmds.setAttr(nodename+'.'+pname, value, type='string')
                            else:
                                cmds.setAttr(nodename+'.'+pname, value)

                        except Exception as e:
                            print(e)
                            print('Error: Failed in setting parameter: ', nodename, pname, value)
                            continue


def captureViewport(mPanel, filename, extension, w=-1, h=-1, aspect=True):
    import maya.OpenMaya as om
    import maya.OpenMayaUI as omui

    img = om.MImage()
    view = omui.M3dView()
    omui.M3dView.getM3dViewFromModelPanel(mPanel, view)
    view.refresh(False, True)
    view.readColorBuffer(img, True)
    
    img.writeToFile(filename, extension)

class MayaUtils(dccutils.DccUtils):
    def application(self):
        from workfile_manager.plugin_utils import Application
        return Application.Maya

    def export_thumbnail(self, filename, ver):
        from workfile_manager.ui import uiutils
        import tempfile

        try:
            ffmpeg_exe = os.environ['FFMPEG_EXE']
        except Exception as e:
            print(e)
            return None

        thumbname = assetutils.Asset.thumbnail_filepath(filename, ver) # temporal thumbnail

        thumbname_orgsize = re.sub('[.][^.]+$', '.png', thumbname)
        _jpg = re.sub('[.][^.]+$', '.jpg', thumbname)
        
        basename = os.path.basename(_jpg)
        _jpg = os.path.join(tempfile.gettempdir(), basename)

        if not os.path.exists(os.path.dirname(thumbname)):
            os.makedirs(os.path.dirname(thumbname))
        try:
            pnl = cmds.getPanel(withLabel='Persp View')
            if pnl is None:
                pnl = cmds.getPanel(withLabel=u'パース ビュー')

            captureViewport(pnl, _jpg, 'jpg')
            if os.path.exists(_jpg):
                if os.path.exists(thumbname):
                    subprocess.call('attrib -R "%s" /S /D' % thumbname)
                #convcmd = '%s -y -i %s %s & %s -y -i %s -vf "scale=512:-1" -q 5 %s' % (ffmpeg_exe, _jpg, thumbname_orgsize, ffmpeg_exe, _jpg, thumbname)
                convcmd = '%s -y -i %s %s' % (ffmpeg_exe, _jpg, thumbname_orgsize)
                subprocess.call(convcmd)
                print('created thumbname_orgsize: ', thumbname_orgsize.replace('/', '\\'))

                if os.path.exists(thumbname_orgsize):
                    subprocess.call('attrib -R "%s" /S /D' % thumbname_orgsize)
                convcmd = '%s -y -i %s -vf "scale=512:-1" -q 5 %s' % (ffmpeg_exe, _jpg, thumbname)
                subprocess.call(convcmd)
                print('created thumbname: ', thumbname.replace('/', '\\'))


                os.remove(_jpg)

        except  Exception as e:
            print(e)
            return None
        return thumbname

    def getrefs(self):
        res = _get_textures()

        refnodes = get_valid_reference_nodes()
        for refnode in refnodes:
            try:
                parent = cmds.referenceQuery(refnode, p=True, rfn=True)
            except:
                print('refnode could be a sharedReferenceNode. Skipped.')
                continue
            if parent is not None:
                continue
            filename = cmds.referenceQuery(refnode, f=True, wcn=True)
            filename = assetdbutils.normalize_path(filename)
            res.append(filename)

        return res

    def create_work_asset(self, args):
        return WorkAssetMaya(**args)

    def create_share_asset(self, args):
        return ShareAssetMaya(**args)

    def create_share_model_asset(self, args):
        return ModelAssetMaya(**args) 

    def create_share_material_asset(self, args):
        return MaterialAssetMaya(**args) 

    def create_share_anim_asset(self, args):
        return AnimationAssetMaya(**args)
    
    def create_share_setdress_asset(self, args):
        return SetdressAssetMaya(**args)

    def create_engine_asset(self, args):
        return EngineAssetMaya(**args)

    def create_engine_model_asset(self, args):
        return EngineAssetMaya(**args)

    def create_engine_anim_asset(self, args):
        return EngineAssetMaya(**args)

    def pre_publish(self, args):
        if cmds.file(q=True, mf=True):
            uiutils.PromptDialog('Confirmation', u'シーンが保存されていません。', btns=['OK']).exec_()
            return False


        sel = cmds.ls(sl=True)
        if len(sel) == 0:
            uiutils.PromptDialog('Confirmation', 'Nothing selected.', btns=['OK']).exec_()
            return False

        mats = cmds.ls(sl=True, mat=True)
        if len(mats) > 0:
            ses = cmds.listConnections(mats, s=False, d=True, type='shadingEngine')
            if len(ses) > 0:
                cmds.select(ses, ne=True)

        refs = get_valid_reference_nodes()
        ref_nodes = {}
        for r in refs:
            res, filename = self._parent_outside_share(r)
            if not res:
                continue
            buf = cmds.referenceQuery(r, nodes=True)
            if buf is None:
                buf = []
            ref_nodes[r] = (buf, filename)

        exp_nodes = get_nodes_to_export_selection()
        for n in exp_nodes:
            for r in list(ref_nodes.keys()):
                _refnodes, filename = ref_nodes[r]
                if n in _refnodes:
                    m = u'エクスポートされるノードがShare領域外の下記リファレンスに含まれています。\n\n' + \
                        u'%s\n\n\n\nShare領域外へのリファレンスをPublishすることは出来ません。\n\n' % filename

                    uiutils.PromptDialog('Confirmation', m, btns=['OK']).exec_()
                    return False


        return True
        

    def _parent_outside_share(self, rfn):
        filename = cmds.referenceQuery(rfn, filename=True, wcn=True)
        if not assetutils.is_share_file(filename):
            #croot = assetdbutils.normalize_path(os.environ['WM_SHARE_CACHED_ROOT']) if 'WM_SHARE_CACHED_ROOT' in os.environ else None
            #if croot is not None:
            #    if not filename.lower().startswith(croot.lower()):
            #        return True, filename
            #else:
            #    return True, filename
            if assetutils.is_cached_share(filename):
                return False, None
            else:
                return True, filename
        
        parent = cmds.referenceQuery(rfn, parent=True, rfn=True)
        if parent is not None:
            return self._parent_outside_share(parent)
        else:
            return False, None    


    def preopen(self, need_to_save=False):
        clear_modelpanel_callback()

        if cmds.file(q=True, mf=True):
            sn = cmds.file(q=True, sn=True)
            
            d = uiutils.PromptDialog('Save Changes', 'Save changes to current scene file?\n\n'+sn, btns=['Save', "Dont't Save", 'Cancel'])
            res = d.exec_()
            if res == 3:
                return False
            elif res == 1:
                if not sn or sn == '':
                    uiutils.PromptDialog('Error', u'シーンファイル名を特定できません。', btns=['OK']).exec_()
                    return False
                #cmds.file(s=True, f=True)
                _save({})
            elif need_to_save:
                return False
        return True

    def post_open(self, filename):
        import threading
        import time
        class Thread(threading.Thread):
            def run(self):
                time.sleep(2)
                cmds.file(mf=0)
                print('force modified flag to be false.')


        sn = cmds.file(q=True, sn=True)
        print('sn: ', sn)
        if not sn or sn == '':
            cmds.file(rn=filename)
            uiutils.PromptDialog('Warning', 'シーンにエラーが含まれるため（Mayaの仕様により）オープン直後ですが編集された状態となっています。', btns=['OK']).exec_()
        else:
            # force modified flag to be false.
            th = Thread()
            th.start()

    def open_supported(self):
        return ['ma', 'mb', 'fbx']

    def save_supported(self):
        return ['ma', 'mb', 'fbx~']

    def current_scenefilename(self):
        return cmds.file(q=True, sn=True)

    def save(self, filename):
        cmds.file(rename=filename)
        if os.path.exists(filename):
            subprocess.call('attrib -R "%s"' % filename)
        cmds.file(save=True, f=True)

    def open(self, filename):
        cmds.file(filename, ignoreVersion=True, o=True, f=True)
        
    def get_framerange(self):
        st = cmds.playbackOptions(q=True, min=True)
        et = cmds.playbackOptions(q=True, max=True)
        return (st, et)

    def get_framerate(self):
        map_ = {
                'game':15,
                'film':24,
                'pal':25,
                'ntsc':30,
                'show':48,
                'palf':50,
                'ntscf':60,
            }

        fps = cmds.currentUnit(q=True, time=True)
        m = re.search('^[0-9.]+', fps)
        if m:
            return float(m.group(0))
        elif fps in map_:
            return map_[fps]
        else:
            raise Exception('Invalid frame range detected.')

    def set_framerate(self, v):
        try:
            fps = '%f' % v
            if '.' in fps:
                fps = fps[:fps.index('.')]
            cmds.currentUnit(time=fps+'fps')
        except:
            print('ERROR: Invalid fps specified: ', v)
            return

    def set_framerange(self, frame_start, frame_end, set_edit_range=False):
        if set_edit_range:
            cmds.playbackOptions(ast=frame_start)
            cmds.playbackOptions(aet=frame_end)
        cmds.playbackOptions(min=frame_start)
        cmds.playbackOptions(max=frame_end)

    def use_thread(self):
        return True

    def select(self, items):
        if items is not None and len(items) > 0:
            try:
                cmds.select(items, ne=True)
            except:
                print('Warning: Failed to select:', items)

    def get_selection(self):
        return cmds.ls(sl=True)

    def prefer_separate_p4_proc(self):
        return False

    



class RepathWidget(QtWidgets.QWidget):
    def __init__(self):
        super(RepathWidget, self).__init__()
        vbox = QtWidgets.QVBoxLayout(self)
        hbox = QtWidgets.QHBoxLayout()
        lb1 = QtWidgets.QLabel('Project Dir: ')
        lb1.setMinimumWidth(70)
        self.projdir = QtWidgets.QLineEdit()
        self.projdir.setText(cmds.workspace(q=True, rd=True))
        self.projdir.setMinimumWidth(500)
        self.projdir.setReadOnly(True)
        hbox.addWidget(lb1)
        hbox.addWidget(self.projdir)
        hbox2 = QtWidgets.QHBoxLayout()
        lb2 = QtWidgets.QLabel('Tex Dir: ')
        lb2.setMinimumWidth(70)
        self.texdir = QtWidgets.QLineEdit('textures')
        self.texdir.setMaximumWidth(200)
        hbox2.addWidget(lb2, 0)
        hbox2.addWidget(self.texdir, 0)
        hbox2.addWidget(QtWidgets.QWidget(), 1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)

def check_texture_path():
    outside = []
    notexists = []
    files = cmds.ls(type='file')

    projdir = assetdbutils.normalize_path(cmds.workspace(q=True, rd=True))
    
    expr = re.compile('^'+projdir, re.IGNORECASE)

    engine_expr = None
    if 'WM_ENGINE_ROOT' in os.environ:
        engine_root = os.environ['WM_ENGINE_ROOT']
        engine_expr = re.compile('^'+engine_root.replace('\\', '/'), re.IGNORECASE)

    for n in files:
        path = cmds.getAttr(n+'.fileTextureName')
        path = assetdbutils.normalize_path(path)

        if not os.path.exists(path):
            notexists.append(path)
        
        elif not expr.search(path) and not assetutils.is_share_file(path) and \
                not assetutils.is_cached_share(path) and \
                not (engine_expr is not None and engine_expr.search(path)):
            outside.append((path, n))

    if len(notexists)>0:
        w = QtWidgets.QListWidget()
        w.setMinimumWidth(600)
        for p in notexists:
            w.addItem(p)

        d = uiutils.PromptDialog('Warning', u'下記テクスチャは存在しません。', wd=w, btns=['OK'])
        d.exec_()

    if len(outside)>0:
        tw = QtWidgets.QTableWidget()
        tw.setColumnCount(3)
        tw.setRowCount(len(outside))
        tw.setWordWrap(False)
        tw.setColumnWidth(0, 150)
        tw.setColumnWidth(1, 300)
        tw.setColumnWidth(2, 300)
        tw.setSortingEnabled(True)
        tw.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        tw.setHorizontalHeaderLabels(['Node', 'Directory', 'Filename'])
        header = tw.horizontalHeader()
        if type(header) is QtWidgets.QHeaderView:
            header.setSortIndicatorShown(True)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        for i in range(len(outside)):
            item = QtWidgets.QTableWidgetItem(outside[i][1])
            tw.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem(os.path.dirname(outside[i][0]))
            tw.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem(os.path.basename(outside[i][0]))
            
            tw.setItem(i, 2, item)

            tw.setRowHeight(i, 20)

            dirname = assetdbutils.normalize_path(outside[i][0])
            workarea = assetdbutils.normalize_path(assetutils.get_resource_root())
            if not os.path.dirname(dirname).startswith(workarea):
                for r in range(3):
                    tw.setCurrentCell(i, r, QtCore.QItemSelectionModel.Toggle)
            
        tw.sortByColumn(1, QtCore.Qt.AscendingOrder)
        
        
            
        d = uiutils.PromptDialog('Warning', u'下記テクスチャはMayaプロジェクトのテクスチャ領域外です。\n\n' + \
            u'ファイルをプロジェクト下にコピーして差し替えますか？（選択したテクスチャのみ処理されます。）\n\n', 
                wd=tw, btns=['Yes', 'No and Continue', 'Cancel'])
        d.resize(750, 400)
        res = d.exec_()

        if res == 3 or res == 0:
            return False
        elif res == 1 and len(tw.selectedIndexes()) > 0:
            files_to_copy = []
            for index in tw.selectedIndexes():
                dirname = tw.item(index.row(), 1).text()
                basename = tw.item(index.row(), 2).text()
                filename = os.path.join(dirname, basename)

                node = tw.item(index.row(), 0).text()
                if (filename, node) not in files_to_copy:
                    files_to_copy.append((filename, node))
            

            stat, _ = preproc_tex.check_texname_uniquness([x[1] for x in files_to_copy])
            if not stat:
                return False

            w = RepathWidget()
            d = uiutils.PromptDialog('Copy and repath textures', '', wd=w, btns=['Copy and Repath', 'Cancel'])
            res = d.exec_()

            if res != 1:
                return False

            if not os.path.exists(w.projdir.text()):
                uiutils.PromptDialog('Error', 'Project Dir not exists', btns=['OK']).exec_()
                return False
            texdir = os.path.join(w.projdir.text(), w.texdir.text())
            if not os.path.exists(texdir):
                os.makedirs(texdir)
            copied = []
            for p, n in files_to_copy:
                basename = os.path.basename(p)
                fpath = os.path.join(texdir, basename)

                if p not in copied:
                    subprocess.call('attrib -R "%s"' % fpath)
                    shutil.copy(p, texdir)
                    copied.append(p)
                
                set_texture(n, fpath)
                
            
    return True        


def set_texture(filenode, tex_path):
    buf = [x for x in texture_types if x['type']==cmds.objectType(filenode)]
    assert len(buf) > 0
    _type = buf[0]
    
    if _type['type'] == 'file':
        cs = cmds.getAttr(filenode + '.colorSpace')
        print('orginal color space: ', cs)

    cmds.setAttr(filenode + '.'+_type['attr'], tex_path, type='string')

    if _type['type'] == 'file':
        cmds.setAttr(filenode + '.colorSpace', cs, type='string')
        print('color space2: ', cmds.getAttr(filenode + '.colorSpace'))

def get_nodes_to_export_selection(sel=None):
    def does_exist(x):
        try:
            if cmds.objExists(x):
                return True
        except:
            import traceback
            print(traceback.format_exc())
        return False

    org_sel = cmds.ls(sl=True)
    if type(sel) is not list:
        sel = cmds.ls(sl=True)
    sel = [x for x in sel if does_exist(x)]
    if len(sel) == 0:
        return []
    ad = cmds.listRelatives(sel, ad=True, pa=True)
    ps = get_upper_nodes(sel)
    se = None
    try:
        se = cmds.ls(cmds.listHistory(ad, f=True, lv=1), type='shadingEngine')
        
        '''なぜかGLSLShaderが取得出来ないことがあるので、直接コネクションも確認↓'''
        cmds.select(cl=True)
        if ad is not None:
            cmds.select(ad, r=True, ne=True)
        try:
            buf = cmds.listConnections('.instObjGroups', '.instObjGroups[*].objectGroups', s=False, d=True, type='shadingEngine')
            if buf is None:
                buf = []
        except:
            buf = []
        cmds.select(org_sel, r=True, ne=True)
        if se is None:
            se = buf
        else:
            se += buf
        se = list(set(se))
        print('se:', se)

    except:
        import traceback
        print(traceback.format_exc())
        se = None

    buf = sel
    if ad is not None:
        buf += ad
    if ps is not None:
        buf += ps
    if se is not None:
        buf += [x for x in se if x != 'initialShadingGroup']
    
    buf = list(set(buf))
    his = cmds.listHistory(buf, ac=True) # acオプションをつけないとfileノードが取得出来ない場合がある。GLSLShaderのシェーディンググループを起点とする場合など。
    
    if his is not None:
        buf += his
    
    res = list(set(buf))
    cmds.select(org_sel, ne=True)
    return res


def get_upper_nodes(nodes):
    assert type(nodes) is list
    nodes = [x for x in nodes if cmds.objExists(x)]
    ps = cmds.listRelatives(nodes, p=True, pa=True)
    
    if ps is None:
        return nodes
    else:
        buf = get_upper_nodes(ps)
        return buf + nodes

def get_valid_reference_nodes():
    res = []
    refnodes = cmds.ls(type='reference')
    for refnode in refnodes:
        try:
            cmds.referenceQuery(refnode, p=True, rfn=True)
        except:
            pass
        else:
            res.append(refnode)
    return res


def transfer_to_z_up(_t, _r, _s):
    t = [_t[0], _t[2], _t[1]]
    s = [_s[0], _s[2], _s[1]]
    import maya.api.OpenMaya as om
    _r = [x * 3.141592 / 180 for x in _r]

    er = om.MEulerRotation(_r[0], _r[1], _r[2])
    _quat = om.MQuaternion()
    _quat.setValue(er)
    quat = om.MQuaternion(_quat.x, _quat.z, _quat.y, -_quat.w)

    _r = quat.asEulerRotation()
    r = [_r.x, _r.y, _r.z]
    r = [x*180.0/3.141592 for x in r]

    return t, r, s


def remove_garbage_from_ma(filename, copy=False):
    sw = uiutils.Stopwatch(force=True)
    sw.reset()
    pt_ai_trans = re.compile(r'setAttr ".ai_translator"')
    pt_nan = re.compile(r'setAttr .* -nan')
    buf = []
    edited = False
    replace_cache = False
    
    if copy:
        idx = filename.rindex('.')
        outfile = filename[:idx]+'_post' + filename[idx:]
    else:
        outfile = filename

    lockfile = outfile + '.lock'
    import filelock
    lock = filelock.FileLock(lockfile)
    print('Acquiring filelock: ', lockfile, '(remove_garbage_from_ma)')
    with lock.acquire():
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('\tsetAttr '):
                    m = pt_ai_trans.search(line)
                    if m:
                        edited = True
                        continue
                    m = pt_nan.search(line)
                    if m:
                        edited = True
                        continue
                
                buf.append(line)

        if edited or replace_cache:
            with open(outfile, 'w') as of:
                of.writelines(buf)
        sw.elapse('remove_garbage_from_ma done')
    return outfile

def import_references():
    excludes = []
    while True:
        refs = [x for x in get_valid_reference_nodes() if cmds.referenceQuery(x, parent=True, rfn=True) is None and x not in excludes]
        print('refs:', len(refs))
        if len(refs) == 0:
            break
        for r in refs:
            ref_filename = assetdbutils.normalize_path(cmds.referenceQuery(r, filename=True, wcn=True))
            print('ref_filename: ', ref_filename)
            try:
                cmds.file(ref_filename, ir=True)
            except:
                excludes.append(r)


def delete_connections(targets):
    con = cmds.listConnections(targets, s=True, d=False, p=True, c=True)
    if con:
        for i in range(len(con[::2])):
            try:
                cmds.disconnectAttr(con[i*2+1], con[i*2])
            except Exception as e:
                import traceback
                print(traceback.format_exc())

    
    con = cmds.listConnections(targets, s=False, d=True, p=True, c=True)
    if con:
        for i in range(len(con[::2])):
            try:
                cmds.disconnectAttr(con[i*2], con[i*2+1])
            except Exception as e:
                import traceback
                print(traceback.format_exc())

def load_unloaded_references():
    print('>> assetutils_maya.load_unloaded_references.')
    # Load unloaded references
    while True:
        loaded = False
        for ref in get_valid_reference_nodes():
            is_loaded = cmds.referenceQuery(ref, il=True)
            if is_loaded:
                continue
            loaded = True
            filename = cmds.referenceQuery(ref, f=True)
            print('filename:', filename)
            cmds.file(filename, loadReferenceDepth="asPrefs", loadReference=ref)
        if not loaded:
            break