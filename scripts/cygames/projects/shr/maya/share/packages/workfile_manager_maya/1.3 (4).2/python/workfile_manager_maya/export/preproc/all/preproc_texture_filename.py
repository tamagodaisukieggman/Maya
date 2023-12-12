# -*- coding: utf-8 -*-
import os
import copy

from Qt import QtCore, QtGui, QtWidgets



from workfile_manager.ui import ui_dialogs
from cylibassetdbutils import assetutils

try:
    import maya.cmds as cmds
except:
    pass
from workfile_manager.plugin_utils import Application
from workfile_manager_maya.export.preproc.preproc_maya_base import MayaPreprocBase

'''
This preproc is directly called in publishing.
'''
class Plugin(MayaPreprocBase):
    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        return True


    def execute(self, args):
        files = cmds.ls(type='file')

        stat, res = check_texname_uniquness(files)
        if not stat:
            self.results = []
            for vs in list(res.values()):
                for v in vs:
                    self.results.append(v[1])
            return False, self.results
        else:
            return True, None
        

    def get_label(self):
        return 'Check texture filename'

    def order(self):
        return 1000

    def is_editable(self):
        return False

    def default_checked(self):
        return False

def check_texname_uniquness(files):
    buf = {}
    res = {}
    for f, n in [(cmds.getAttr(x+'.fileTextureName'), x) for x in files]:
        #share_root = assetutils.get_share_root()
        #if assetdbutils.normalize_path(f).startswith(share_root):
        if assetutils.is_non_cached_share_file(f):
            print(('Already published texture: ', f))
            continue

        basename = os.path.basename(f).lower()
        if basename not in buf:
            buf[basename] = [(f, n)]
        else:
            buf[basename].append((f, n))

    for n in list(buf.keys()):
        tbuf = []
        for m in buf[n]:
            if m[0] in [x[0] for x in tbuf]:
                continue
            tbuf.append(m)
        if len(tbuf) > 1:
            res[n] = buf[n]

    if len(list(res.keys())) == 0:
        return True, None
    else:
        w = QtWidgets.QListWidget()
        w.setMinimumWidth(600)
        for k in list(res.keys()):
            w.addItem(k)
            for p, n in res[k]:
                w.addItem(u'      └%s  [%s]' % (p, n))
        d = ui_dialogs.PromptDialog('Error', u'テクスチャファイル名が重複しています。', wd=w, btns=['OK']).exec_()

        return False, res

