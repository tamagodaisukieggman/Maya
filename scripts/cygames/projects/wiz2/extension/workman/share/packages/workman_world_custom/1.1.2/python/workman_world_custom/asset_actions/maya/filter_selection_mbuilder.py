# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    import maya.cmds as cmds
    import maya.mel as mel
    from workfile_manager_maya import assetutils_maya
    from workman_world_custom.asset_actions.maya import uiutils as aa_uiutils
    fields = assetutils_maya.AnimationAssetMaya().get_dict().keys()
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
import shutil

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()

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
        if asset.variant != 'rig' and asset.variant != 'default':
            return False

        return True

    def getlabel(self):
        return 'Filter selection > from MotionBuilder'

    def allow_multi_items(self):
        return True

    def reload_table(self):
        return False

    def execute(self, args):
        from workfile_manager_maya import assetutils_maya
        from workfile_manager import cmds as wcmds
        sw = wcmds.Stopwatch(force=False)
        fbxfiles = []
        toclip = ''

        conds = []
        for asset in args['assets']:
            filename = asset._filename
            conds.append('path="%s"' % filename)

        q = 'select %s, path, source, source_version, asset_id from sharedasset_version_master_02 where %s' % (','.join(fields), ' or '.join(conds))
        db.cs.execute(q)
        buf = db.cs.fetchall()
        sw.elapse('filter_selection - p1')
        self.db_cache = {}
        for b in buf:
            print ('Cached:', b['path'])
            self.db_cache[b['path']] = b
        sw.elapse('filter_selection - p2')
        for asset in args['assets']:
            filename = asset._filename
            #print('filename:', filename)
            version = asset._version
            src, src_version, record = self.get_source(filename, version)
            #print(' ->src:', src)
            if src.endswith('.fbx'):
                fbxfiles.append((filename, version, record))
        sw.elapse('filter_selection - p3')
        for share_filename, share_version, record in fbxfiles:
            asset = assetutils_maya.AnimationAssetMaya()
            for k in asset.get_dict():
                setattr(asset, k, record[k])

            try:
                asseturl = asset.get_url(share_filename, self.db_cache[share_filename])
            except Exception as e:
                print(e)
                print('AssetURL not retrieved: ', share_filename)
            else:
                toclip += asseturl + '\n'
        sw.elapse('filter_selection - p4')   
        if toclip != '':
            QtGui.QClipboard().setText(toclip)
            print('Copied to clipboard:\n' + toclip)
            args['table'].mwin.uiobj.paste_asset_url_btn.cb_clicked(select_all_at_deault=True)
        else:
            uiutils.PromptDialog('Confirmation', 'Nothing found.', btns=['OK']).exec_()
        sw.elapse('filter_selection - p5')
        return True


    def get_source(self, filename, version):
        #print('finding src... for:', filename)
        if assetutils.is_share_file(filename):
            if filename in self.db_cache.keys():
                buf = [self.db_cache[filename]]
            else:
                buf = db.get_sharedasset_from_file(filename, fields=fields+['source', 'source_version'])
            if len(buf) == 0:
                print('Error: asset not found: ', filename)
                return None
            src = buf[0]['source']
            res = self.get_source(src, buf[0]['source_version'])
            if res is None:
                # It's an exceptional case to pass here. Only when nothing found in db for "src".
                return filename, version, buf[0]
            else:
                if res is None:
                    return res
                else:
                    return (res[0], res[1], buf[0])
        else:
            return filename, version, None