# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import shutil
import subprocess
import glob

try:
    import maya.cmds as cmds
except:
    pass

from cylibassetdbutils import assetutils, assetdbutils
from workfile_manager.plugin_utils import PluginType, PostProcBase, Application

class Plugin(PostProcBase):
    def application(self):
        return Application.Maya
        
    def apps_executable_on(self):
        return [
            Application.Maya, 
            Application.Standalone,
        ]

    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False

    def order(self):
        return 20

    def execute(self, args):
        outfile = args['outfile']
        assetdict = args['assetdict']
        movpath = assetutils.Asset.thumbnail_filepath(outfile, assetdict['version'], replace_share_root=False)
        movpath = re.sub('[.][^.]+$', '', movpath)
        print('movpath: ', movpath)

        if 'playblast_source' in args:
            m = re.search('[.]([^.]+)$', args['playblast_source'])
            fmt = m.group(1)
            shutil.copyfile(args['playblast_source'], movpath+'.'+fmt)

        else:
            cmds.displayPref(displayGradient=0)
            cmds.colorManagementPrefs(e=True, cmEnabled=True)
            #cmds.colorManagementPrefs(e=True, viewTransformName='sRGB gamma')
            cmds.colorManagementPrefs(e=True, outputTransformEnabled=True, ott='playblast')
            try:
                cmds.colorManagementPrefs(e=True, outputTransformName='sRGB gamma', ott='playblast')
            except:
                import traceback
                print(traceback.format_exc())

            file_fmt = 'png'
            fmt = 'image'
            compress = 'png'
            
            cmds.playblast(format=fmt, filename=movpath, viewer=0, showOrnaments=1, fp=4, percent=100, compression=compress, quality=100, fo=True, os=False, widthHeight=(800, 480), ifz=True)
            convcmd = 'W:/production/tools/cygames/thirdparty/win/standalone/FFmpeg/v4.0.2/bin/ffmpeg.exe -y -r 60 -start_number 0 -i %s.%%04d.%s -vcodec libx264 -pix_fmt yuv420p -r 60 ' % (movpath, file_fmt) + \
                ' -filter_complex "[0]split=3[org][fg][a];[a]extractplanes=a[a];[fg]eq=gamma=2.2[fg];[fg][a]alphamerge[comp];[org][comp]overlay" ' + \
                movpath + '.avi'
            print('cmd: ', convcmd)
            subprocess.call(convcmd)

            files = glob.glob(movpath+'.*.%s' % file_fmt)

            
            for f in files:
                print('temporal file: ', f.replace('/', '\\'))
                if 'keep_intermediate' not in args or not args['keep_intermediate']:
                    print('del: ', f.replace('/', '\\'))
                    os.remove(f)

    def getlabel(self):
        return 'Create Playblast'

    def default_checked(self):
        return True

    def is_editable(self):
        return False