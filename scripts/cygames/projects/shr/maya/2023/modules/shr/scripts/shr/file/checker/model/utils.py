# -*- coding: utf-8 -*-
u"""ユーティリティ関数 (Exporterからも使われる)


..
    END__CYGAMES_DESCRIPTION
"""
from functools import partial

import maya.cmds as cmds
# import openpyxl

from mtku.maya.utils.history import MtkHistory
# from mtku.maya.mtklog import MtkLog


# logger = MtkLog(__name__)

PACKAGE = 'mtku.maya.menus.file.checker.model'

import time
from functools import wraps

def timeit(ndigits=2):
    """Print execution time [sec] of function/method
    - message: message to print with time
    - ndigits: precision after the decimal point
    """
    def outer_wrapper(func):
        # @wraps: keep docstring of "func"
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print("Excecution time for : {sec} [sec]".format(
                sec=round(end-start, ndigits))
            )
            return result
        return inner_wrapper
    return outer_wrapper

class ModelCheckerUtils(object):

    
    def __init__(self, node=None):
        
        self.meshes = []

        # meshes = [x for x in cmds.listRelatives(node, allDescendents=True, fullPath=True, type="mesh") if not cmds.getAttr("{}.intermediateObject".format(x))]
        # meshes = []
        meshes = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="mesh")
        # self.meshes.extend(meshes)
        if meshes:
            for mesh in meshes:
                if mesh and not cmds.getAttr("{}.intermediateObject".format(mesh)):
                    self.meshes.append(mesh)
        # if meshes:
        #     self.meshes.extend(meshes)
            # for mesh in meshes:
            #     self._get_selection_mesh_materials(mesh)

    
    # @timeit(ndigits=2)
    def validate(self, checker, *args, **kwargs):
        u"""チェック用関数の実行

        :param checker: チェッカー用関数の文字列
        :param node: チェック対象のノード (メッシュ、マテリアルなど)
        :return: bool
        """
        modulename = '{0}.validation'.format(PACKAGE)
        classname = '{0}.Validation'.format(modulename)

        node = kwargs.setdefault('node', None)
        meshes = kwargs.setdefault('meshes', None)

        command = '{class_}.{function}(node="{node}", meshes="{meshes}")'.format(
            class_=classname, function=checker, node=node, meshes=",".join(self.meshes)
        )

        # from mtku.maya.menus.file.checker.model.validation.validation import checker
        # print(modulename)
        exec('import {}'.format(modulename))
        # exec('import imp;imp.reload({})'.format(modulename))
        result = eval(command)
        return result


    def modify(self, modifier, nodes, *args, **kwargs):
        u"""修正用関数の実行

        :param nodes: ノードのリスト
        :param modifier: 修正用関数の文字列
        :param all: 修正時に一度に全データを取り扱うか
        :param deletes_histories: 1 Delete Non-Deformer 2 Delete
        """
        # batchmode = kwargs.setdefault('batchmode', False)
        deletes_history = kwargs.setdefault('deletes_history', False)
        all = kwargs.setdefault('all', False)

        modulename = '{0}.modification'.format(PACKAGE)
        classname = '{0}.Modification'.format(modulename)

        if not all:
            for node in nodes:
                command = '{class_}.{function}(node="{node}")'.format(
                    class_=classname, function=modifier, node=node,
                )
                exec('import {}'.format(modulename))
                # exec('import imp;imp.reload({})'.format(modulename))
                eval(command)
                # logger.info(u'修正したノード: {}'.format(', '.join(node)))
        else:
            command = '{class_}.{function}(nodes={nodes})'.format(
                class_=classname, function=modifier, nodes=nodes,
            )
            exec('import {}'.format(modulename))
            # exec('import imp;imp.reload({})'.format(modulename))
            # logger.debug(command)
            eval(command)
            # logger.info(u'修正したノード: {}'.format(', '.join(nodes)))

        if deletes_history:
            tranforms = cmds.ls(nodes, o=True, tr=True, fl=True)
            shapes = cmds.ls(nodes, o=True, s=True, fl=True)
            if shapes:
                if tranforms:
                    tranforms.extend(cmds.listRelatives(shapes, p=True, f=True))
                else:
                    tranforms = cmds.listRelatives(shapes, p=True, f=True)

            if deletes_history == 1:
                for tranform in tranforms:
                    # deletehistory.delete_history(tranform)
                    cmds.select(tranform)
                    MtkHistory.delete_history()
            elif deletes_history == 2:
                for tranform in tranforms:
                    cmds.delete(tranform, ch=True)

        # if not batchmode:
        #     cmds.confirmDialog(m=u'修正しました\n\n詳細はScriptEditorをご覧ください', b=['OK'])
