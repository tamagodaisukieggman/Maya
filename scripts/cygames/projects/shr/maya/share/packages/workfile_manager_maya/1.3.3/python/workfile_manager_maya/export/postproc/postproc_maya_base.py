# -*- coding: utf-8 -*-

"""
Mayaで実行するパブリッシュポストプロセスのベースクラス

Maya以外のDCC（MotionBuilderなど）からパブリッシュする際にも、ファイナライズ処理にMayaを使用するため、
プラグインの属性定義部分（application()やis_asset_eligible()）などはMaya以外のDCCからもアクセス出来る必要がある。
（execute()は実行出来なくても、モジュールのインポート自体は可能（にしておく必要がある））

当ファイルもMaya依存のモジュール内に配置されているが、これ自体はMayaに依存していない。

"""

from workfile_manager.plugin_utils import PostProcBase, Application

class MayaPostprocBase(PostProcBase):
    def application(self):
        return Application.Maya

    def _is_postproc_root_set(self, x):
        import maya.cmds as cmds
        try:
            if not cmds.attributeQuery('postproc_edit_set', ex=True, n=x):
                return False

            if not cmds.getAttr(x+'.postproc_edit_set'):
                return False

            buf = cmds.listConnections(x+'.message', d=True, s=False, p=True)
            if buf is None:
                return True
                
            for c in buf:
                nodename, attrname = c.split('.')
                if cmds.objectType(nodename) == 'objectSet' and attrname.startswith('dnSetMembers'):
                    return False

        except:
            pass
        
        return False
