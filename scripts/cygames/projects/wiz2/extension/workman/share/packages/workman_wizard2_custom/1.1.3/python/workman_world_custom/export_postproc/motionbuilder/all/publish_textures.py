from __future__ import print_function
from workfile_manager.plugin_utils import PostProcBase, PluginType, Application
from cylibassetdbutils import assetdbutils
import os, re, shutil

try:
    import pyfbsdk as fb
except:
    pass

class Plugin(PostProcBase):
    def application(self):
        return Application.MotionBuilder

    def apps_executable_on(self):
        return (
            Application.MotionBuilder, Application.Standalone
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'model':
            return True

        return False

    def order(self):
        return 10

    def execute(self, args):
        from workfile_manager import p4utils, cmds as wcmds
        from cylibassetdbutils import assetutils
    
        p4u = p4utils.P4Utils.get_instance()
        user = wcmds.get_p4user_on_postproc()
        if user is not None:
            p4u.p4.user = user
        p4u.p4.cwd = os.environ['WM_P4_ROOT_DIR']
        p4u.setclient()

        base = os.path.basename(args['outfile'])
        base = re.sub('[.][^.]+$', '', base)
        texdir = os.path.join(os.path.dirname(os.path.dirname(args['outfile'])), 'textures', base)
        texdir = texdir.replace('\\', '/')
        
        if not os.path.exists(texdir):
            os.makedirs(texdir)

        import cymobuapiutils
        buf = cymobuapiutils.list_all()
        
        texture_names = [x[0] for x in args['textures']]

        maps = {}
        for n in buf:
            if type(n) is fb.FBVideoClipImage:
                if n.ImageSequence:
                    continue
                prop = n.PropertyList.Find('Path')
                path = assetdbutils.normalize_path(prop.Data)
                if assetutils.is_share_file(path) or assetutils.is_cached_share(path):
                    print('Already published texture: ', path)
                    if assetutils.is_cached_share(path):
                        org_path = wcmds.get_share_path_from_cache(path)
                        n.Filename = org_path
                    continue
                
                if path not in texture_names:
                    continue
                
                idx = texture_names.index(path)
                rev = args['textures'][idx][1]
                assert(rev is not None)

                dst = os.path.join(texdir, os.path.basename(path))

                try:
                    p4u.p4_run_xxx('sync', '--parallel=threads=8', '%s#%d' % (path, rev))
                    p4u.p4_run_xxx('revert', path)
                except Exception as e:
                    print('WARNING: P4 Exception:')
                    print(e)
                    if not os.path.exists(path):
                        try:
                            p4u.p4_run_xxx('revert', path)
                        except:
                            pass
                dst = assetdbutils.normalize_path(dst)
                shutil.copyfile(path, dst)
                print('Texture in p4 copied: %s -> %s' % (path, dst))
                maps[dst] = (path, rev)
                
                n.Filename = str(dst)
        
        
        print('publish_textures: ', maps)
        
        return maps


    def getlabel(self):
        return 'Publish Textures'
        
    def default_checked(self):
        return True
        
    def is_editable(self):
        return False

    