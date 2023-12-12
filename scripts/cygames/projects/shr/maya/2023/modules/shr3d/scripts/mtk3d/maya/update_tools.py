# -*- coding: utf-8 -*-
import datetime
import os
from maya import cmds

from tatool.log import ToolLogging, Stage

from mtku.maya.utils.perforce import MtkP4


MB_SCRIPTS = [
                "Z:/mtk/tools/motion_builder/mtk3d/python/mtk3d"
            ]

MAYA_SCRIPTS = [
                "Z:/mtk/tools/maya/modules/mtku/scripts/mtku",
                "Z:/mtk/tools/maya/modules/mtk3d"
                ]

HOUDINI_HDA = [
                "Z:/mtk/tools/maya/share/hda"
            ]

SCRIPT_PATHS = MB_SCRIPTS + MAYA_SCRIPTS + HOUDINI_HDA


MODULES = {
            "mtku": "MtkMenu",
            "mtk3d": "Mtk3dMenu"
            }

MENU_NAMES = {
            "mtku": "mutsunokami",
            "mtk3d": "mtk3d"
            }

tool_title = u'mtk_update_tools'
project = 'mutsunokami'
toolcategory = 'Maya'
stage = Stage.dev
version = '1.0'

ToolLogging = ToolLogging(projects=project, toolcategory=toolcategory, target_stage=stage, tool_version=version)

logger = ToolLogging.getTemplateLogger(tool_title)

def get_file_status():
    """
    ディレクトリ内のファイルのステータスを全て取得
    """
    script_files = []
    for script_path in SCRIPT_PATHS:
        for dirpath, dirnames, filenames in os.walk(script_path):
            for filename in filenames:
                script_files.append(os.path.join(dirpath,
                                    filename).replace(os.sep, '/'))
                                    
    file_status_ext = MtkP4.status_ext(script_files)
    # for i,x in enumerate(file_status_ext.items()):
    #     print x
    #     if i == 1:
    #         break
    return file_status_ext


class ProgressWindowBlock(object):
    """ProgressWindowを表示させるコンテキストマネージャー
    """

    def __init__(self, title='', progress=0,  minValue=0, maxValue=100, isInterruptable=True, show_progress=True):
        self._show_progress = show_progress and (not cmds.about(q=True, batch=True))

        self.title = title
        self.progress = progress
        self.minValue = minValue
        self.maxValue = maxValue
        self.isInterruptable = isInterruptable

        self._start_time = None

    def __enter__(self):
        logger.info('[ {} ] : Start'.format(self.title))

        if self._show_progress:
            cmds.progressWindow(
                title=self.title,
                progress=int(self.progress),
                status='[ {} ] : Start'.format(self.title),
                isInterruptable=self.isInterruptable,
                min=self.minValue,
                max=self.maxValue + 1
            )

        self._start_time = datetime.datetime.now()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        calc_time = datetime.datetime.now() - self._start_time
        logger.info('[ {} ] : End : Calculation time : {}'.format(self.title, calc_time))

        if self._show_progress:
            cmds.progressWindow(e=True, status='End : Calculation time : {}'.format(calc_time))
            cmds.progressWindow(ep=1)

    def step(self, step):
        if self._show_progress:
            cmds.progressWindow(e=True, step=step)

    def _set_status(self, status):
        if self._show_progress:
            cmds.progressWindow(e=True, status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, status))

    def _get_status(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, status=True)

    status = property(_get_status, _set_status)

    def _set_progress(self, progress):
        if self._show_progress:
            cmds.progressWindow(e=True, progress=progress)

    def _get_progress(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, progress=True)

    progress = property(_get_progress, _set_progress)

    def is_cancelled(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, ic=True)

    @staticmethod
    def wait(sec=1.0):
        cmds.pause(sec=sec)

class UpdateMenu(object):
    def sync_directory(self, dir_path):
        MtkP4.sync([u"{}".format(dir_path)])
        print("{:-<20}  {}".format("P4 Sync", dir_path))
        # logger.info(u'P4 Sync : {}'.format(dir_path))

                
    def rebuild_maya_menu(self, path):
        """
        mtku, mtk3d のメニューモジュールを読み込む
        import もreload も必要あり
        """
        error = []

        package = path.split("/")[-1]
        modulename = "{}.{}.{}".format(package, "maya", "menu")
        
        exec('import {}'.format(modulename))
        print("{:-<20}  {}".format("module load", modulename))
        
        exec('reload({})'.format(modulename))
        print("{:-<20}  {}".format("module reload", modulename))
        
        # logger.info(u'reload module : {}'.format(modulename))

        funcname = "{}.{}.{}".format(modulename, MODULES[package], "main()")
        try:
            result = eval(funcname)
            # logger.info(u'rebuild menu : {}'.format(funcname))
        except Exception as e:
            logger.error(u'rebuild menu error code : {}'.format(e))
            print("{:+<20}  {}".format("error function", funcname))
            error = MENU_NAMES[package]
        
        return error

    def _rebuild_menu(self):
        import mtku.maya.menu as m_meny
        reload(m_meny)
        m_meny.MtkMenu.main()
        # logger.info(u'rebuild menu: {}'.format("mutsunokami"))
        print(u'rebuild menu: {}'.format("mutsunokami"))
        

        import mtk3d.maya.menu as m3d_meny
        reload(m3d_meny)
        m3d_meny.Mtk3dMenu.main()
        # logger.info(u'rebuild menu: {}'.format("mtk3d"))
        print(u'rebuild menu: {}'.format("mtk3d"))

    def do_it(self):
        _rebuild_error = []

        with ProgressWindowBlock(title='Sync P4', maxValue=len(SCRIPT_PATHS)) as prg:
            prg.status = 'Start Sync P4'
            prg.step(1)
            for dir_path in SCRIPT_PATHS:
                self.sync_directory(dir_path)
                prg.step(1)
                prg.status = 'Start Sync P4'

                if prg.is_cancelled():
                    break
        
        with ProgressWindowBlock(title='Re Build Menu', maxValue=len(MAYA_SCRIPTS)) as prg:
            prg.status = 'Re Build Menu'
            prg.step(1)
            for path in MAYA_SCRIPTS:
                _rebuild = self.rebuild_maya_menu(path)
                if _rebuild:
                    _rebuild_error.append(_rebuild)
                prg.step(1)
                prg.status = 'Re Build Menu'

                if prg.is_cancelled():
                    break

        if _rebuild_error:
            cmds.confirmDialog(
                message=u"{}\n\n{}".format("\n".join(_rebuild_error),
                                    u"メニューの更新に失敗しました"),
                title=u'menu builld error',
                button=['OK'],
                defaultButton='OK',
                cancelButton="OK",
                dismissString="OK")

        # if not _sync_error and not _rebuild_error:
        #     cmds.confirmDialog(
        #         message=u"[ mutsunokami ] [ mtk3d ] ツールを更新しました",
        #         title=u'update tools',
        #         button=['OK'],
        #         defaultButton='OK',
        #         cancelButton="OK",
        #         dismissString="OK")

def reload_maya_module(script_path):
    script_path = script_path.replace(os.sep, '/')
    
    base_name = os.path.basename(script_path)
    if base_name[0] == "_":
        return
    
    _ext_split = script_path.split(".")
    if _ext_split[-1].lower() != "py":
        return
    
    script_path = _ext_split[0]
    _path_split = script_path.split("/")

    if not "maya" in _path_split:
        return
    
    if "mtk3d" in _path_split:
        package = "mtk3d"
    else:
        package = "mtku"
    
    _i = [i for i, x in enumerate(_path_split) if x == package][-1]

    modulename = ".".join(_path_split[_i:])

    try:
        exec('import {}'.format(modulename))
        print("{:=<20}  {}".format("module load", modulename))
        
        exec('reload({})'.format(modulename))
        print("{:=<20}  {}".format("module Re load", modulename))
    except Exception as e:
        print(e)

def reload_maya_modules(module_paths):
    for script_path in module_paths:
        for dirpath, dirnames, filenames in os.walk(script_path):
            for filename in filenames:
                # script_files.append(os.path.join(dirpath,
                #                     filename).replace(os.sep, '/'))
                _path = os.path.join(dirpath, filename).replace(os.sep, '/')
                reload_maya_module(_path)

def main():
    befor_file_status_ext = get_file_status()
    
    _up = UpdateMenu()
    _up.do_it()
    
    after_file_status_ext = get_file_status()

    change_files = {}

    if after_file_status_ext:
        for path, states in after_file_status_ext.items():
            if path in befor_file_status_ext.keys():
                if(befor_file_status_ext[path]["haveRev"]
                                < states["haveRev"]):
                    change_files[path] = "Update"
            else:
                change_files[path] = "Add"
    
    if change_files:
        cmds.confirmDialog(
            message=u"{}\n\n{}".format(u"\n\n".join([u"{} \n [ {} ]".format(k, v) for k,v in change_files.items()]),
                                u"上記のツールを更新しました"),
            title=u'以下のファイルを更新しました',
            button=['OK'],
            defaultButton='OK',
            cancelButton="OK",
            dismissString="OK")
        
        """
        変更があったファイルをモジュールとして再インポートする
        """
        with ProgressWindowBlock(title='Re Load Python Modules', maxValue=len(change_files)) as prg:
            prg.status = 'Re Load Python Modules'
            prg.step(1)
            for path, state in change_files.items():
                reload_maya_module(path)
                prg.step(1)
                prg.status = 'Re Load Python Modules'
                if prg.is_cancelled():
                    break

    else:
        cmds.confirmDialog(
            message=u"{: ^50}".format(u"変更はありませんでした"),
            title=u'update tools',
            button=['OK'],
            defaultButton='OK',
            cancelButton="OK",
            dismissString="OK")
    

def _main():
    """
    旧バージョン
    ファイルの比較があった方が良いかと思い、変更した
    """
    file_status_ext = get_file_status()

    not_latest_files = {}
    
    if file_status_ext:
        for path, states in file_status_ext.items():
            if states["action"] and states["action"] != "latest":
                not_latest_files[path] = states
    
    if not_latest_files:
        print("\n\n")
        print("{:-^100}\n".format(" not latest files "))

        for path, state in not_latest_files.items():
            print(path)
            print(state)
        # cmds.confirmDialog(
        #     message=u"{}\n\n{}".format(u"\n".join([u"{} が [ {} ]".format(k, v) for k,v in not_latest_files.items()]),
        #                         u"上記のツールは更新できませんでした"),
        #     title=u'確認',
        #     button=['OK'],
        #     defaultButton='OK',
        #     cancelButton="OK",
        #     dismissString="OK")


