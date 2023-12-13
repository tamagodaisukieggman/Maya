from __future__ import print_function

try:
    import maya.cmds as cmds
    import pymel.core as pm
    from workfile_manager_maya import assetutils_maya

except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application
from cylibassetdbutils import assetdbutils, assetutils

import re, os

def fetch(path):
    print('fetching ', path)
    from workfile_manager import p4utils
    p4u = p4utils.P4Utils.get_instance()
    try:
        p4u.p4_run_xxx('sync', path)
    except Exception as e:
        print(e)
    try:
        p4u.p4_run_xxx('edit',  path)
    except Exception as e:
        print(e)
    try:
        p4u.p4_run_xxx('revert',  path)
    except Exception as e:
        print(e)

def constrain(namespace, gender, ref_skeleton_src, ref_skeleton_dst, anim_skl_xml, rig_skl_xml):
    fetch('W:/production/tools/maya/...')

    pyscript = 'W:/production/tools/maya/scripts/rig/convert/hik/hik_convert.py'
    if os.path.exists(pyscript):
        print('>>> found: ', pyscript)

    import rig.convert.hik.hik_convert as rchh
 
    maya_version = cmds.about(v=1)
    if 2022 <= float(maya_version):
        import importlib
        importlib.reload(rchh)
    else:
        reload(rchh)
    
    file_path = rchh.__file__.replace('\\', '/')
    
    print('anim_skeleton_xml: ', anim_skl_xml)
    print('rig_skeleton_xml: ', rig_skl_xml)

    bake_cnst_sets, hik_joints_sets = rchh.connect_hik(namespace=namespace,
                                                        gender=gender,
                                                        import_joints_filePath=ref_skeleton_dst,
                                                        import_xml_filePath=rig_skl_xml,
                                                        anim_joints_filePath=ref_skeleton_src,
                                                        anim_xml_filePath=anim_skl_xml, dont_use_hik_for_nonhuman=True)



def ungroup_recursive(nodename):
    prs = cmds.listRelatives(nodename, ap=True, pa=True)
    print('ungroup:', nodename)
    cmds.ungroup(nodename)

    if prs is None or len(prs) == 0:
        return
    for pr in prs:
        ungroup_recursive(pr)


def generate_ref_skeleton(root_jnt_name, filename=None):
    if filename is not None:
        cmds.file(filename, o=True, f=True)
    else:
        filename = cmds.file(q=True, sn=True)
        if filename == '' or filename is None:
            raise('input filename not specified: ', filename)

    from workfile_manager_maya import assetutils_maya
    assetutils_maya.import_references()

    if not cmds.objExists(root_jnt_name):
        raise('Root joint not exists: ' + root_jnt_name)

    #
    try:
        cmds.parent(root_jnt_name, w=True)
    except:
        pass

    #
    jnts = cmds.ls(type='joint')
    assetutils_maya.delete_connections(jnts)
    for jnt in jnts:
        try:
            cmds.setAttr(jnt+'.r', 0, 0, 0)
        except:
            print('Warning: Failed in executing setAttr: ', jnt)

    try:
        for n in cmds.ls():
            if cmds.objExists(n) and cmds.objectType(n) != 'joint':
                cmds.delete(n)
    except:
        pass

    tmpfile = assetutils.get_publish_tempfilename_local(filename)
    print('generate_ref_skeleton: ', tmpfile)
    tmpdir = os.path.dirname(tmpfile)
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)
    cmds.file(rn=tmpfile)
    cmds.file(s=True, f=True, type='mayaAscii')
    return tmpfile

def find_src_rigfile(args):
    anim_file = args['animation_file']
    db = assetdbutils.DB.get_instance()
    anim_file = assetdbutils.normalize_path(anim_file)
    if not anim_file.startswith(assetutils.get_share_root()):
        anim_file = args['animation_file_source']

    q = 'select source,source_version from sharedasset_version_master_02 where path="%s"' % anim_file
    db.cs_execute(q)
    buf = db.cs.fetchall()
    if len(buf) == 0:
        raise('Cannot find any work file as a source: ' + anim_file)
    work = buf[0]
    q = 'select local_path,depot_path,revision from refs_master_02 where master="%s" and version=%d' % (work['source'], work['source_version'])
    db.cs_execute(q)
    buf = db.cs.fetchall()
    buf = [x for x in buf if x['depot_path'] is None]
    if len(buf) == 0:
        raise('Cannot find any source rig: ' + anim_file)
    print('rig cand: ', buf)
    
    for cand in buf:
        q = 'select * from sharedasset_version_master_02 where path="%s"' % cand['local_path']
        db.cs_execute(q)
        share_assets = db.cs.fetchall()
        if len(share_assets) == 0:
            continue
        share_asset = share_assets[0]
        if share_asset['task'] == 'model' and share_asset['variant'] == 'rig':
            break
    else:
        raise('Cannot find any source rig: ' + anim_file)

    print('source rig file: ', cand['local_path'])
    return cand['local_path']


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
        
    def execute(self, args):
        from workfile_manager import plugin_utils
        
        rigfile = cmds.file(q=True, sn=True)
        print('rigfile: ', rigfile)
        animfile = args['animation_file']
        print('animfile: ', animfile)

        keep_intermediate = args['keep_intermediate'] if 'keep_intermediate' in args else False
        tmpfile_base = os.path.join(os.environ['WM_TMP_DIR'], os.path.basename(animfile))


        try:
            src_rigfile = find_src_rigfile(args)
        except:
            if 'default_rig_skeleton' in args:
                src_rigfile = args['default_rig_skeleton']
                print('given default skeleton used: ', src_rigfile)
                fetch(src_rigfile)
            else:
                raise('default rig skeleton not set.')

        ref_skeleton_dst = generate_ref_skeleton('root_jnt')
        ref_skeleton_src = generate_ref_skeleton('root_jnt', filename=src_rigfile)
        print('ref_skeleton_dst:', ref_skeleton_dst)
        print('ref_skeleton_src:', ref_skeleton_src)
        
        db = assetdbutils.DB.get_instance()
        buf = db.get_sharedasset_from_file(rigfile)
        mdlasset = assetutils_maya.ModelAssetMaya()
        for k in list(mdlasset.get_dict().keys()):
            setattr(mdlasset, k, buf[0][k])
        
        rig_ns = mdlasset.get_namespace()

        cmds.file(new=True, f=True)
        mdlasset.import_(rigfile, namespace_option=2, namespace=rig_ns, r=True, import_mode='Append')

        # Retrieve rig's namespace.
        nss = cmds.namespaceInfo(lon=True)
        print('nss: ', nss)
        nss.remove('shared')
        nss.remove('UI')
        if len(nss) > 0:
            ns = nss[0] + ':'
        else:
            raise Exception('Cannot specify namespace for a rig.')

        # import references in the rig.
        excludes = []
        while True:
            refs = [x for x in assetutils_maya.get_valid_reference_nodes() if cmds.referenceQuery(x, parent=True, rfn=True) is None and x not in excludes]
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

        if keep_intermediate:
            plugin_utils.write_tempfile('rig_imported', tmpfile_base)

        m = re.search('^([a-zA-Z]+)\d*', ns)
        if m:
            gender = m.group(1)
        else:
            raise('Not supported asset name.')
        print('>> gender:', gender)

        global_args = args['global_args']
        if 'additional_select' not in global_args:
            global_args['additional_select'] = []
        global_args['additional_select'] += pm.ls('::rig')
        
        anim_skl_xml = args['anim_skeleton_xml']
        rig_skl_xml = args['rig_skeleton_xml']
        constrain(ns, gender, ref_skeleton_src, ref_skeleton_dst, anim_skl_xml, rig_skl_xml)

        if keep_intermediate:
            plugin_utils.write_tempfile('constrained', tmpfile_base)

        try:
            os.remove(ref_skeleton_src)
            os.remove(ref_skeleton_dst)
        except:
            print('Failed in removing ref_skeleton.')
            
        cmds.file(animfile, ignoreVersion=True, i=True, f=True, ns=':', pr=True)
        if keep_intermediate:
            plugin_utils.write_tempfile('anim_imported01', tmpfile_base)

        asset = assetutils_maya.AnimationAssetMaya()
        asset.import_(animfile, namespace_option=0)
        if keep_intermediate:
            plugin_utils.write_tempfile('anim_imported02', tmpfile_base)


        refs = [x for x in assetutils_maya.get_valid_reference_nodes() if cmds.referenceQuery(x, parent=True, rfn=True) is None]
        for r in refs:
            ref_filename = assetdbutils.normalize_path(cmds.referenceQuery(r, filename=True, wcn=True))
            try:
                cmds.file(ref_filename, ir=True)
            except:
                pass

        cmds.select('::rig')

        return True

    def getlabel(self):
        return 'Bake to Rig'

    def default_checked(self):
        return False

    def is_editable(self):
        return False
