# -*- coding: utf-8 -*-
u"""チェッカー"""
import os
import yaml
from collections import OrderedDict

import sys
from functools import partial

import maya.cmds as cmds

import mtku.maya.utils.decoration as decoration
from mtku.maya.base.window import BaseWindow
# from mtku.maya.mtklog import MtkLog
from .utils import ModelCheckerUtils
import mtku.maya.menus.file.checker.model.warning
# reload(mtku.maya.menus.file.checker.model.warning)
# from .warning import WarningWindow

config_node = None
CYLISTA_SCRIPT_PATH = "Z:/cyllista/tools/maya/modules/cyllista/scripts/"

if CYLISTA_SCRIPT_PATH not in sys.path:
    sys.path.append(CYLISTA_SCRIPT_PATH)

try:
    import cyllista.config_node as config_node
except Exception:
    print('can\'t import "config_node"')
    exit(1)


# logger = MtkLog(__name__)

WARNING_WINDOW = 'MtkCheckerWarning'


class Checker(BaseWindow):

    def __init__(self, *args, **kwargs):
        u"""初期化"""
        super(Checker, self).__init__(*args, **kwargs)
        self.width = 800
        self.height = 1170

        self.inf_num = 4

        self.mtk_mesh_vet_plugin_name = "mtkMeshVet"
        self.mtk_mesh_vet_plugin = "mtkMeshVet.mll"
        self._use_plugin_flag = True

        self._opvar_pulldown_label = '{}.pulldown_label'.format(__package__)
        self._pulldown = None
        self._pulldown_items = []
        self.checkbox_values = {}
        self._yaml_path = '{}/checklist.yaml'.format(os.path.dirname(__file__))
        with open(self._yaml_path) as f:
            yaml.add_constructor(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                lambda loader, node: OrderedDict(loader.construct_pairs(node))
            )
            self._items = yaml.safe_load(f)
            self._categories = self._items.keys()

            for cat_values in self._items.values():
                for menu_item_values in cat_values:
                    if menu_item_values.get('preset'):
                        self._pulldown_items.extend(menu_item_values['preset'])

        self._pulldown_items = list(set(self._pulldown_items))
        self._pulldown_items.sort()

        

    def get_cylista_config_node_data(self):
        if config_node:
            config = config_node.get_config()
            self.inf_num = config.get("cySkinInfluenceCountMax", 4)

    def setUp_mtkMeshVet(self):
        cmds.loadPlugin(self.mtk_mesh_vet_plugin, quiet=True)

    def _delete_warning_window(self):
        if cmds.window(WARNING_WINDOW, ex=True):
            cmds.deleteUI(WARNING_WINDOW)

    def close(self, *args):
        super(Checker, self).close(*args)
        self._delete_warning_window()

    def create(self):
        u"""Windowのレイアウト作成"""
        super(Checker, self).create()
        
        self.get_cylista_config_node_data()
        
        _frame = cmds.frameLayout(l='Preset')
        _clum = cmds.columnLayout(adj=1)
        self._pulldown = cmds.optionMenuGrp(label='Preset', cw2=[60, 100], h=40, cc=self._change_pulldown_item)
        for item in self._pulldown_items:
            cmds.menuItem(label=item)
        cmds.setParent('..')
        cmds.setParent('..')

        for category in self._categories:
            self.checkbox_values.update(self.add_layout(category))

        self.read_settings()

        self.setUp_mtkMeshVet()
        if not self.mtk_mesh_vet_plugin_name in cmds.pluginInfo(query=True, listPlugins=True):
            self._use_plugin_flag = False



    def add_layout(self, category):
        u"""レイアウトを追加

        :param category: category
        :return: {checkbox: values}
        """
        checkbox_values = {}

        cmds.frameLayout(l=category, cl=False, cll=True)

        form = cmds.formLayout(nd=100)

        column = cmds.columnLayout()

        if category in self._items:
            cell_values = self._items[category]
        else:
            cmds.warning(u'{} does not exist.'.format(category))
            cell_values = []
        
        for values in cell_values:
            # label, error_text, checker, modifier, enabled = value
            # valueのデフォルトは後で記憶したものに変更
            _text = values['text'].rsplit(None,2)
            _text_length = len(_text)

            if _text_length != 1:
                cmds.rowLayout(numberOfColumns=3, columnWidth3=[300,250,150])
            
            checkbox = cmds.checkBox(l=_text[0].format(self.inf_num), v=True, en=True, h=23)
            if _text_length != 1:
                if self._use_plugin_flag and values["checker"] == "has_many_bind" or values["checker"] == "has_cvs_value":
                    cmds.text(label=u"[  {}  ]".format(u"シーン全体"))
                else:
                    cmds.text(label=u"[  {}  ]".format(_text[-2]))

                cmds.text(label=u"[  {}  ]".format(_text[-1]))
                cmds.setParent("..")
            # checkbox_values[checkbox] = {'typ': category}
            # checkbox_values[checkbox].update(values)
            checkbox_values[checkbox] = values

        cmds.formLayout(
            form, e=True,
            af=(
                [column, 'top', 10],
                [column, 'left', 25],
                [column, 'bottom', 10],
            ),
        )
        cmds.setParent('..')  # columnLayout

        cmds.setParent('..')  # formLayout

        cmds.setParent('..')  # frameLayout

        return checkbox_values

    def _change_pulldown_item(self, *args):
        preset = args[0]
        for cb, values in self.checkbox_values.items():
            if values.get('preset') and preset in values['preset']:
                cmds.checkBox(cb, e=True, v=True)
            else:
                cmds.checkBox(cb, e=True, v=False)
        self.save_settings()

    def check_value_check(self, *args):
        default_check_box_values = []
        categorys = []
        current_pulldown_value = cmds.optionMenuGrp(self._pulldown, q=True, value=True)
        _warning = []

        for cat_keys, cat_values in self._items.items():
            for menu_item_values in cat_values:
                if menu_item_values.get('preset'):
                    default_check_box_values.append(menu_item_values['preset'])

        for (checkbox, values),_default_preset in zip(sorted(self.checkbox_values.items()), default_check_box_values):
            _text = values['text'].rsplit(None,2)[0].format(self.inf_num)
            _value = cmds.checkBox(checkbox, q=True, value=True)
            category = cmds.frameLayout(cmds.checkBox(checkbox, q=True, parent=True).rsplit("|",3)[0], q=True, label=True)
            
            if current_pulldown_value in values["preset"] and not _value:
                if not category in categorys:
                    warning_text = u"{:-^26}\n".format(category)
                else:
                    warning_text = ""
                warning_text += u"{: ^4}[  {}  ]".format(u"", _text)
                _warning.append(warning_text)
                print(warning_text)
                categorys.append(category)

        if _warning:
            flag = True
            while flag:
                result = cmds.confirmDialog(title=u'! チェック内容の確認 !',
                    messageAlign="center",
                    message=u"以下の項目のチェックが外れてます、既定のチェック内容と異なり足りません\n\n{}\n\nそのままチェックを実行しますか？".format("\n".join(_warning)),
                    button=["OK","Cansel"],defaultButton="OK",cancelButton="Cansel",dismissString="Cansel")
                if result == "Cansel":
                    return False
                else:
                    flag = False

        return True



    # @decoration.keep_selections
    def apply_(self, *args):
        u"""チェッカーの実行"""
        result = []  # [{'typ': タイプ, 'error_text': "エラーテキスト", 'nodes': ノード, 'modifier': 修正用関数}, ...]

        # nodes = cmds.ls(sl=True)
        # nodes = cmds.ls(sl=True, type="transform", long=True)

        # プラグインがインフルエンス数を見に行くとフリーズするので一時的に不使用に
        # self._use_plugin_flag = False

        # 強制的にルートノードを取るようにした
        root_nodes = list(set([x.split("|")[1] for x in cmds.ls(sl=True, type="transform", long=True)]))
        

        if not root_nodes:
            # logger.warning(u'チェック対象を選択してください')
            cmds.warning(u'チェック対象を選択してください')
            return

        self._delete_warning_window()

        if not self.check_value_check():
            return

        for checkbox, values in sorted(self.checkbox_values.items()):
            if not cmds.checkBox(checkbox, q=True, v=True):
                continue
            if not cmds.checkBox(checkbox, q=True, en=True):
                continue

            error_nodes = []
            if (values["checker"] == "reference_name" or
                        values["checker"] == "controller" or
                        values["checker"] == "all_keyframe" or
                        values["checker"] == "unknown_plugin" or
                        values["checker"] == "ctrl_set_geometorys" or
                        values["checker"] == "anim_jt_set"):
                # 全体チェックのものはこっち

                mdlChecker = ModelCheckerUtils()
                valid_data = mdlChecker.validate(values['checker'], node="")
                if not valid_data['result']:
                    error_nodes.extend(valid_data['error'])
            
            elif self._use_plugin_flag and values["checker"] == "has_many_bind" and not cmds.ls(type='reference', long=True):
                _errors = cmds.mtkMeshVet(skinInfluences=self.inf_num)
                if _errors:
                    error_nodes = cmds.ls(_errors, fl=True)

            elif self._use_plugin_flag and values["checker"] == "has_cvs_value":
                _errors = cmds.mtkMeshVet(hasVtx=True)
                if _errors:
                    error_nodes = cmds.ls(_errors, fl=True)
            
            else:
                env_flag = True
                if values["preset"] == "chara":
                    env_flag = False
                    
                for root_node in root_nodes:
                    mdlChecker = ModelCheckerUtils(root_node)
                    if values["checker"].startswith("hierarchey_second") and env_flag:
                        valid_data = mdlChecker.validate("hierarchey_second_env", node=root_node)
                    elif values["checker"].startswith("hierarchey_second") and not env_flag:
                        valid_data = mdlChecker.validate("hierarchey_second_chara", node=root_node)
                    else:
                        valid_data = mdlChecker.validate(values['checker'], node=root_node)
                    if not valid_data['result']:
                        error_nodes.extend(valid_data['error'])
            if error_nodes:
                d = {'error_nodes': error_nodes}
                d.update(values)
                result.append(d)

        if result:
            mtku.maya.menus.file.checker.model.warning.main(result)
            # win = WarningWindow(info=result)
            # win.show()
        else:
            cmds.confirmDialog(m=u'  エラーは見つかりませんでした　　', b=['OK'])
            # logger.info(u'OK')

    # ------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------

    def save_settings(self, *args):
        u"""設定の保存"""
        cmds.optionVar(sv=(self._opvar_pulldown_label, cmds.optionMenuGrp(self._pulldown, q=True, v=True)))

    def reset_settings(self, *args):
        u"""設定のリセット"""
        for cb, values in self.checkbox_values.items():
            cmds.checkBox(cb, e=True, v=True)
        cmds.optionVar(rm=self._opvar_pulldown_label)
        cmds.optionMenuGrp(self._pulldown, e=True, sl=1)
        # リセット後に設定を保存
        self.save_settings()

    def read_settings(self):
        u"""設定の読み込み"""

        if cmds.optionVar(exists=self._opvar_pulldown_label):
            pulldown_label = cmds.optionVar(q=self._opvar_pulldown_label)
            cmds.optionMenuGrp(self._pulldown, e=True, v=pulldown_label)
            self._change_pulldown_item(pulldown_label)
        else:
            for cb, values in self.checkbox_values.items():
                cmds.checkBox(cb, e=True, v=True)


# ---------------------------------------
# 動作確認後、ここから下は消す
# ---------------------------------------
class CharaChecker(Checker):

    def __init__(self, *args, **kwargs):
        u"""初期化"""
        super(CharaChecker, self).__init__(*args, **kwargs)
        self.width = 800
        self.height = 400
        self._worksheet_name = 'chara'
        self.checkbox_values = {}
        self._yaml_path = '{}/old_checklist.yaml'.format(os.path.dirname(__file__))
        with open(self._yaml_path) as f:
            self._items = yaml.safe_load(f)
            self._categories = self._items.keys()

    def create(self):
        u"""Windowのレイアウト作成"""
        # super(CharaChecker, self).create()
        self.checkbox_values.update(self.add_layout(self._worksheet_name))


class EnvChecker(Checker):

    def __init__(self, *args, **kwargs):
        u"""初期化"""
        super(EnvChecker, self).__init__(*args, **kwargs)
        self.width = 800
        self.height = 400
        self._worksheet_name = 'env'
        self.checkbox_values = {}
        self._yaml_path = '{}/old_checklist.yaml'.format(os.path.dirname(__file__))
        with open(self._yaml_path) as f:
            self._items = yaml.safe_load(f)
            self._categories = self._items.keys()

    def create(self):
        u"""Windowのレイアウト作成"""
        # super(EnvChecker, self).create()
        self.checkbox_values.update(self.add_layout(self._worksheet_name))


class RigChecker(Checker):
    def __init__(self, *args, **kwargs):
        u"""初期化"""
        super(RigChecker, self).__init__(*args, **kwargs)
        self.width = 800
        self.height = 400
        self._worksheet_name = 'rig'
        self.checkbox_values = {}
        self._yaml_path = '{}/old_checklist.yaml'.format(os.path.dirname(__file__))
        with open(self._yaml_path) as f:
            self._items = yaml.safe_load(f)
            self._categories = self._items.keys()

    def create(self):
            u"""Windowのレイアウト作成"""
            self.checkbox_values.update(self.add_layout(self._worksheet_name))