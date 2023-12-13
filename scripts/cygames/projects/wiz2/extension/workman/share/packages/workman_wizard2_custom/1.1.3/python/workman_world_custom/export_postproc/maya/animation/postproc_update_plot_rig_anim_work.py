# -*- coding: utf-8 -*-
from __future__ import print_function

from workfile_manager import wmlog, cmds as wcmds
from workfile_manager.plugin_utils import PostProcBase, PluginType, Application
from cylibassetdbutils import assetdbutils, assetutils
from postproc_set_editor import ui_preset

try:
    import maya.cmds as cmds
    import maya.mel as mel
    import postproc_set_editor
    import pymel.core as pm
    from postproc_set_editor_maya import ui_maya
    dcc_cmds = ui_maya.DccCmds()

except:
    pass

db = assetdbutils.DB.get_instance()
logger = wmlog.get_logger(__name__)

import re, os, shutil

def list_postproc_sets():
    def is_valid_set(x):
        if dcc_cmds.attribute_query('postproc_edit_set', n=x, ex=True):
            return dcc_cmds.get_attr(dcc_cmds.get_name(x)+'.postproc_edit_set')
        return False
    sets = dcc_cmds.list_nodes(type='objectSet')
    sets = [x for x in sets if is_valid_set(x)]
    return sets

def delete_all_postproc_sets(set_=None):
    if set_ is None:
        for s in [x.name() for x in list_postproc_sets()]:
            delete_all_postproc_sets(s)
    else:
        childs = cmds.sets(set_, q=True)
        if childs is None:
            childs = []
        childs = [x for x in childs if cmds.objectType(x) == 'objectSet']
        
        for c in childs:
            delete_all_postproc_sets(c)
        if len(childs) == 0:
            cmds.delete(set_)


def export_presets(preset_file):
    sets = list_postproc_sets()
    setobjs = []
    for set_ in sets:
        setobj = postproc_set_editor.Set(set_name=dcc_cmds.get_name(set_), dcccmds=dcc_cmds)
        
        buf = cmds.sets(setobj.pm_set.name(), q=True)
        for c in buf:
            if cmds.objectType(c) == 'objectSet' and c.endswith('_target'):
                linked = pm.sets(c, q=True)
                for n in linked:
                    if n.name() not in [x.name() for x in setobj.pm_nodes]:
                        setobj.pm_nodes.append(n)

        setobjs.append(setobj)


    presets = {}
    for setobj in setobjs:
        dict_ = ui_preset.get_dict_from_set(setobj, dcc_cmds)
        dict_['node_name'] = setobj.pm_set.name()
        presets[setobj.get_setname()] = dict_

    print('presets: ', presets)
    if preset_file is not None:
        ui_preset.save_presets(preset_file, presets)
    return str(presets)
    
class Plugin(PostProcBase):
    def apps_executable_on(self):
        return (
            Application.Maya, Application.MotionBuilder, Application.Standalone
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False
            
    def order(self):
        return 0
    
    def getlabel(self):
        return 'Update workfile(s) and plot'

    def default_checked(self):
        return False

    def is_editable(self):
        return False


    def execute(self, args):
        self.rig_file = rig_file = args['rig_file']
        anim_file = args['animation_file']
        buf = db.get_sharedasset_from_file(self.rig_file)
        if len(buf) == 0:
            logger.error('rig not found: ', self.rig_file)
            return

        self.updated_rig = buf[0]

        # Get framerange and framerate.
        buf = db.get_sharedasset_from_file(anim_file)
        if not buf:
            print('filename not registered in db:', anim_file)
            return
        
        src = buf[0]['source']
        if not src.endswith('.ma'):
            return

        src_version = buf[0]['source_version']

        if not src or not src_version:
            print('Source workfile not registered.')
            return

        vers = db.get_workasset_versions_2([(src, src_version)])
        if len(vers) == 0:
            print('Invalid records or none.')
            return

        from workfile_manager_maya import assetutils_maya
        dccutils = assetutils_maya.MayaUtils.get_instance()
        wasset = dccutils.create_work_asset({})

        #
        for k in list(wasset.get_dict().keys()):
            if k in vers[0]:
                wasset.set_token(k, vers[0][k])
        wasset.version = src_version
        work_revision = vers[0]['revision']
        print('workfile:', src)
        print('work revision:', work_revision)

        # p4 sync.
        task = wcmds.Task(interactive=False)
        task.open_workasset(wasset, src, src_version)

        assetutils_maya.replace_to_cache(src)          
        cmds.file(src, f=True, o=True)
        print('src: ', src)

        # Save postproc presets.
        from workman_world_custom.export_postproc.maya.animation import postproc_update_plot_rig_anim_work as update_pp
        preset_file = assetutils.get_publish_tempfilename_local(src)
        preset_file = re.sub('[.][^.]+$', '.yaml', preset_file)
        print('tmp_preset_file: ', preset_file)
        update_pp.export_presets(preset_file)

        #
        crvs = cmds.ls(type='animCurve')
        if len(crvs) > 0:
            times = cmds.keyframe(crvs, q=True, tc=True)
        else:
            times = []
        framerange = (min(times), max(times))
        print('framerange:', framerange)
        
        # Import references.
        assetutils_maya.import_references()

        # Delete namespaces.
        from workman_world_custom.export_postproc.maya.all import postproc_delete_namespace
        postproc_delete_namespace.Plugin().execute({})

        # Plot and export joint animation
        from workman_world_custom.export_postproc.maya.animation import postproc_plot
        cmds.select('::root_jnt')
        pp = postproc_plot.Plugin()
        c_args = {}
        c_args['frame_range'] = framerange
        pp.execute(c_args)
        
        fbxfile = re.sub('[.]ma$', '.fbx', assetutils.get_publish_tempfilename_local(src))

        

        import importlib
        wmod = importlib.import_module('workfile_manager_maya')
        preset = '%s/export/fbx_presets/animation.fbxexportpreset' % wmod.__path__[0].replace('\\', '/')
        mel.eval('FBXLoadExportPresetFile -f "%s"' % preset)
        cmds.select('::root_jnt')
        mel.eval('FBXExport -s -f "%s"' % fbxfile)
        logger.info('Joint Animation Exported: %s', fbxfile.replace('/', '\\'))

        # Open rig
        cmds.file(rig_file, f=True, o=True)

        # Constrain rig to joint
        from workman_world_custom.export_postproc.maya.animation import postproc_bake_to_rig
        pp = postproc_bake_to_rig.Plugin()
        c_args = {}
        c_args['animation_file'] = fbxfile
        print('animation src: ', anim_file)
        c_args['animation_file_source'] = anim_file
        c_args['global_args'] = args
        c_args['anim_skeleton_xml'] = args['anim_skeleton_xml']
        c_args['rig_skeleton_xml'] = args['rig_skeleton_xml']
        c_args['default_rig_skeleton'] = args['default_rig_skeleton']

        pp.execute(c_args)

        # Plot rig
        from workman_world_custom.export_postproc.maya.animation import postproc_plot
        fbxfile = assetutils.get_publish_tempfilename_local(fbxfile)
        pp = postproc_plot.Plugin()
        cmds.select('::rig', ne=True)
        pp.execute({'frame_range':framerange})
        if cmds.objExists('|root'):
            cmds.delete('|root')
        from workman_world_custom.export_postproc.maya.all import postproc_delete_namespace as delns_pp
        delns_pp.Plugin().execute({})


        cmds.select('::rig', ne=True)
        mel.eval('FBXExport -s -f "%s"' % fbxfile)
        logger.info('Rig Animation Exported: %s', fbxfile.replace('/', '\\'))


        # Replace rigs
        workfile, rig_namespace = self.replace_rigs(src, args['tmp_output'])
        
        # NOTICE: p4 sync for src workfile is already done above.
        cmds.file(workfile, o=True, f=True)

        # load unloaded references.
        assetutils_maya.load_unloaded_references()
        
        # Restore post-proc sets
        from workman_world_custom.export_postproc.maya.all import import_postproc_set as ip_pp
        ip_pp.Plugin().execute({'postproc_set_file':preset_file, 'use_node_name':True})

        # Delete reference edits.
        for n in cmds.ls(dag=True):
            cmds.referenceEdit(n, failedEdits=True, successfulEdits=True, editCommand='lock', removeEdits=True)
            cmds.referenceEdit(n, failedEdits=True, successfulEdits=True, editCommand='unlock', removeEdits=True)

        cmds.delete(cmds.ls(type='animCurve'))
        
        # Import rig animation
        if rig_namespace is None:
            model_asset = assetutils_maya.ModelAssetMaya()
            for k in model_asset.get_dict():
                setattr(model_asset, k, self.updated_rig[k])
            #print('model_asset: ', model_asset.get_dict())
            rig_namespace = model_asset.get_namespace()
        print('import animation namespace:', rig_namespace)
        anim_asset = assetutils_maya.AnimationAssetMaya()

        cmds.FBXImportShowUI(v=False)
        anim_asset.import_(fbxfile, namespace_option=2, namespace=rig_namespace)


        print('workfile:', workfile.replace('/', '\\'))
        cmds.file(f=True, save=True)

        # copy a thumbnail
        thumb_filename = assetutils.Asset.thumbnail_filepath(args['tmp_output'], 0)
        print('thumbnail_source: ', args['thumbnail_source'])
        if os.path.exists(args['thumbnail_source']):
            shutil.copyfile(args['thumbnail_source'], thumb_filename)
            print('thumb_filename:', thumb_filename)


    def replace_rigs(self, workfile, outfile):
        ex = re.compile('^(.*")([a-zA-Z]:.*ma)(".*)$')
        nsex = re.compile('^file .* -ns "([^"]+)"')

        with open(workfile, 'r') as fhd:
            lines = fhd.readlines()

        ns = None
        rig_namespace = None

        with open(workfile, 'r') as fhd:
            context = None
            idx = 0
            for line in fhd:
                print('context:', context)
                if line.startswith('\t'):
                    pass
                else:
                    context = line[:line.index(' ')]

                
                if context == 'file':
                    m = nsex.match(line)
                    if m:
                        ns = m.group(1)
                        
                    m = ex.match(line) 
                    if m:
                        ref = m.group(2)
                        print('ref:', ref)
                        match = self.is_target_asset(assetdbutils.normalize_path(ref))
                        print('match: ', match)
                        if match:
                            line = '%s%s%s\n' % (m.group(1), self.rig_file, m.group(3))
                            print('Newline:', line)
                            lines[idx] = line
                            rig_namespace = ns

                elif context == 'requires':
                    break
                idx += 1

        dirname = os.path.dirname(outfile)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(outfile, 'w') as fhd:
            fhd.writelines(lines)

        return outfile, rig_namespace


    def is_target_asset(self, ref):
        ref = wcmds.get_share_path_from_cache(ref)
        print('resumed path:', ref)
        buf = db.get_sharedasset_from_file(ref)
        print('buf:', buf)
        if len(buf) > 0:
            cand = buf[0]
            asset = assetutils.Asset()
            for k in asset.get_dict():
                if k == 'version' or k == 'localid' or k == 'subcategory':
                    continue
                print(k+':')
                print('\t current:', cand[k])
                print('\t updated:', self.updated_rig[k])
                if cand[k] != self.updated_rig[k]:
                    break
            else:
                # match
                return True

        return False


