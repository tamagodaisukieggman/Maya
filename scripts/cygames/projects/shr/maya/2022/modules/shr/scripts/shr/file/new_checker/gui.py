# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial

import importlib

from maya import cmds
import maya.mel


from mtk.file.new_checker import gui_util
from mtk.file.new_checker import PATH
from mtk.file.new_checker import PACKAGE
from mtk.file.new_checker import CHARACTER_PATHS
from mtk.file.new_checker import ENV_PATHS
from mtk.file.new_checker import scene_data
from mtk.file.new_checker import checker
from mtk.file.new_checker import maya_utils


# 開発中はTrue、リリース時にFalse
DEV_MODE = False

if not DEV_MODE:
    from mtk.file.new_checker import logger
else:
    importlib.reload(gui_util)
    importlib.reload(checker)
    importlib.reload(scene_data)
    importlib.reload(maya_utils)


class CheckerGUI:
    NAME = "mutsunokami_mdl_checker_result_ui"
    # TITLE = u"[ {} ] データとしてチェックしました。データの確認をお願いします"
    TITLE = '[ {} ]  DataType  '
    _text_a_width = 300
    _text_b_width = 100
    _button_a_width = 200
    _button_b_width = 100
    _spacing = 2
    _scroll_width = _text_a_width + _spacing + _text_b_width + _button_a_width
    _scroll_height = 200
    _frame_width = _scroll_width + 35

    _window_width = _frame_width - 10
    _window_height = 200
    _row_height = 30
    _separetor_height = 2

    _frame = "{}_frame".format(NAME)
    _scroll = "{}_scroll".format(NAME)
    _modify_btn = "{}_modify_btn".format(NAME)

    _rows = []

    modify_result_window = "{}_modify_result_window".format(NAME)
    modify_result_window_title = u"[ {} ] 個の項目を修正しました"
    modify_result_frame = "{}_modify_result_frame".format(NAME)
    modify_result_scroll = "{}_modify_result_scroll".format(NAME)
    modify_result_close_btn = "{}_modify_result_close_btn".format(NAME)

    error_result_window = "{}_error_result_window".format(NAME)
    error_result_window_title = u"[ {} ] 個の項目が修正できませんでした"
    error_result_frame = "{}_error_result_frame".format(NAME)
    error_result_scroll = "{}_error_result_scroll".format(NAME)
    error_result_close_btn = "{}_error_result_close_btn".format(NAME)

    _result_window_width = 850
    _result_window_height = 200

    def __init__(self):
        # self.checker = checker.Check()
        self.memory_clear()

    def memory_clear(self):
        self.results = None
        self.modifies = list()
        self.modify_errors = list()

        self.scene_path_obj = None
        self.modifies = list()
        self.modify_errors = list()
        self.checker = checker.Check()

    def get_datas(self):
        self.scene_path_obj = scene_data.SceneData()

    def do_check(self, *args):

        self.memory_clear()
        self.get_datas()

        if not self.scene_path_obj.scene_name:
            gui_util.confirmDialog(_message="シーンが開かれていない、もしくは保存されていないようです")
            return

        if self.scene_path_obj.error:
            gui_util.confirmDialog(_message=self.scene_path_obj.error)
            return

        # _cheker = checker.Check()
        # _cheker.check_start()
        self.checker.check_start()
        result = self.checker.result_obj

        if result:
            self.results = result
            self.result_window()

        else:
            self._open_export_window()
            _message = "お疲れ様でした、"
            _title = "エラーは見つかりませんでした"
            _message += _title
            gui_util.confirmDialog(_title=_title, _message=_message)

    def modify_data(self, *args):
        self.close_error_and_modify_result_windows()
        if self.results:
            # _cheker = checker.Check()
            modify_messages = self.checker.modify_data(result=self.results)

            # _modifys 修正に成功した結果のリスト
            # _errors 修正に失敗した理由のリスト
            _modifys, _errors = modify_messages

            self.modifies = _modifys
            self.modify_errors = _errors
            self.open_modify_result_new()
        self.do_check()

    def result_window(self):

        self.close_window()

        """
        エラーの種類別にソートして表示させるようにした
        """
        _result_datas = self.results.get_sort_data()

        if not self.scene_path_obj.data_type:
            # _t = self.TITLE.format(u"不明")
            _t = self.TITLE.format("unknown")
        else:
            _t = self.TITLE.format(self.scene_path_obj.data_type)

        _t += f' : Total [ {len(_result_datas)} ] error and warning'

        cmds.window(
            self.NAME,
            title=_t,
            menuBar=True,
            width=self._window_width,
            height=self._window_height
        )

        cmds.menu(label='Help', helpMenu=True)
        cmds.menuItem(label=u'Go to Website',
                      command=partial(gui_util.open_help_site))

        cmds.frameLayout(self._frame,
                         marginHeight=10,
                         marginWidth=10,
                         labelVisible=False,
                         width=self._frame_width)

        # cmds.button(l=u"再検査", c=partial(self.do_check))

        cmds.rowLayout(nc=4, adj=4,
                       cw4=[self._text_a_width, self._spacing,
                            self._text_b_width, self._button_a_width],
                       h=16,
                       bgc=[0.2, 0.2, 0.2]
                       )
        cmds.text(l=u"内容", al="center", w=self._text_a_width)
        cmds.text(l="")
        cmds.text(l=u"種類", al="center", w=self._text_b_width)
        cmds.text(l=u"該当ノード", al="center", w=self._button_a_width)
        cmds.setParent("..")
        cmds.scrollLayout(self._scroll,
                          height=self._scroll_height,
                          width=self._window_width,
                          childResizable=True,
                          verticalScrollBarAlwaysVisible=True)

        _no_waring = []
        # print("\n")
        for result in _result_datas:
            if result.error == "Warning":
                continue
            _no_waring.append(result)

            ann = "None"
            button_name = None

            text = str(result.error_text)
            error = str(result.error)
            # node = f'{", ".join(result.error_nodes)}'
            node = result.error_nodes
            # print(node)

            error_detail = ""

            if ":" in error:
                _split = error.split(":")
                error = _split[0]
                error_detail = _split[-1]

            # logger.info(u"text [ {} ],type [ {}] ,node [ {} ]".format(text, _type, node))

            if node:
                if isinstance(node, list):
                    ann = "{}...".format(node[0])
                    button_name = node[0].split("|")[-1]
                else:
                    ann = " > ".join(node.split("|"))
                    button_name = node.split("|")[-1]

            bgc = [0.2, 0.2, 0.2]
            if "mesh" in error:
                bgc = [0.3, 0.3, 0.5]
            elif "material" in error:
                bgc = [0.5, 0.3, 0.3]
            elif "history" in error:
                bgc = [0.3, 0.5, 0.3]
            elif "node name" in error:
                bgc = [0.3, 0.5, 0.5]
            elif "transform" in error:
                bgc = [0.2, 0.3, 0.5]
            elif "joint" in error:
                bgc = [0.5, 0.5, 0.2]
            elif "texture" in error:
                bgc = [0.5, 0.2, 0.5]
            elif "keyframe" in error:
                bgc = [0.6, 0.2, 0.2]
            elif "display layer" in error:
                bgc = [0.3, 0.6, 0.2]
            elif "no polygon" in error:
                bgc = [0.8, 0.2, 0.2]
            elif "influence" in error:
                bgc = [0.2, 0.5, 0.6]
            elif "weight" in error:
                bgc = [0.3, 0.4, 0.5]
            elif "locked normal" in error:
                bgc = [0.5, 0.5, 0.9]

            cmds.rowLayout(nc=4, adj=4,
                           cw4=[self._text_a_width,
                                self._spacing,
                                self._text_b_width,
                                self._button_a_width],
                           h=self._row_height
                           )

            cmds.text(l=text,
                      w=self._text_a_width,
                      h=self._row_height,
                      al="left",
                      ann="[ {} ]".format(ann)
                      )
            cmds.text(l="")
            cmds.text(l=error,
                      w=self._text_b_width,
                      h=self._row_height,
                      al="center",
                      bgc=bgc
                      )

            cmds.button(l=button_name,
                        c=partial(self.select_error_nodes, result),
                        w=self._button_a_width,
                        ann="[ {} ]".format(ann)
                        )
            cmds.setParent("..")
            cmds.separator(h=self._separetor_height)

        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1,
                       columnWidth2=(100, 100))
        _btn_ann = u"[ グループノード ]のトランスフォームのフリーズ、\n"
        _btn_ann += u"ヒストリーの削除、キーフレームの削除、メッシュのないシェイプの削除、\n"
        _btn_ann += u"コリジョンアトリビュートの追加（デフォルト設定）、を行います"
        cmds.button(self._modify_btn,
                    l=u"解決できるエラーを修正し　再検査",
                    # l="Fix any resolvable errors and Recheck",
                    c=partial(self.modify_data),
                    ann=_btn_ann,
                    en=False,
                    w=self._window_width / 2 - 10)
        cmds.button(
            l=u"エラーを無視して出力ウィンドウを開く",
            # l="Ignore the error and open the output window",
            c=partial(self._open_export_window),
            w=300)
        cmds.setParent("..")

        if self.results:
            cmds.button(self._modify_btn, e=True, en=True)
        cmds.setParent("..")

        cmds.showWindow(self.NAME)

        cmds.scriptJob(parent=self.NAME, event=(
            "SceneOpened", partial(self.close_all_window)))
        cmds.scriptJob(parent=self.NAME, event=(
            "NewSceneOpened", partial(self.close_all_window)))
        print(f'[ {len(_no_waring)} ] errors')

    def select_error_nodes(self, result, *args):

        if not result:
            return

        # if result.error == "material" or result.error == "texture":
        #     #  or result.error == "physical material"
        #     return

        nodes = []
        compornents = []
        if result.category == "mesh":
            for node in result.error_nodes:
                if "." in node:
                    compornents.append(node)
                    nodes.append(node.split(".")[0])
                else:
                    if cmds.nodeType(node) == "mesh":
                        _transform_node = cmds.listRelatives(node,
                                                             parent=True,
                                                             type="transform",
                                                             fullPath=True)
                        if _transform_node:
                            nodes.append(_transform_node[0])
                    else:
                        nodes.append(node)
        else:
            nodes = result.error_nodes

        for node in nodes:
            self.show_hidden_nodes(node)

        if compornents:
            cmds.select(compornents, r=True)
            cmds.hilite(nodes, r=True)
        else:
            cmds.select(nodes, r=True)

        self.fit_view()
        self.fit_outliner()

    def show_hidden_nodes(self, visible_node):
        try:
            cmds.setAttr("{}.visibility".format(visible_node), 1)
        except:
            pass

        for n in maya_utils.iterUpNode(visible_node):
            try:
                cmds.setAttr("{}.visibility".format(n), 1)
            except:
                pass

        shape = cmds.listRelatives(visible_node, shapes=True, fullPath=True)
        if shape:
            try:
                cmds.setAttr("{}.visibility".format(shape[0]), 1)
            except:
                pass

    def fit_view(self):
        _command = 'FrameSelectedWithoutChildren; '
        _command += 'fitPanel -selectedNoChildren;'
        try:
            maya.mel.eval(_command)
        except:
            pass

    def fit_outliner(self):
        _outliners = [x for x in cmds.getPanel(type="outlinerPanel")
                      if x in cmds.getPanel(vis=True)]

        if _outliners:
            [cmds.outlinerEditor(x, e=True, sc=True) for x in _outliners]

    def select_target(self, *args):
        target = args[0]
        if not target or not cmds.objExists(target):
            return

        self.show_hidden_nodes(target)
        cmds.select(target, r=True)
        self.fit_view()
        self.fit_outliner()

    def create_modify_result_window(self, type="modify", datas=None):
        window_name = self.modify_result_window
        window_title = self.modify_result_window_title.format(
            len(self.modifies))
        frame_layout_name = self.modify_result_frame
        scroll_layout_name = self.modify_result_scroll
        close_btn_name = self.modify_result_close_btn

        if type == "modify":
            datas = self.modifies
        elif type == "error":
            datas = self.modify_errors
            window_name = self.error_result_window
            window_title = self.error_result_window_title.format(
                len(self.modify_errors))
            frame_layout_name = self.error_result_frame
            scroll_layout_name = self.error_result_scroll
            close_btn_name = self.error_result_close_btn

        width = self._result_window_width
        height = self._result_window_height

        if not datas:
            return

        cmds.window(
            window_name,
            title=window_title,
            width=width,
            height=height
        )
        cmds.frameLayout(frame_layout_name,
                         marginHeight=10,
                         marginWidth=10,
                         labelVisible=False,
                         width=width-10)
        cmds.scrollLayout(scroll_layout_name,
                          height=height-10,
                          width=width-35,
                          childResizable=True,
                          verticalScrollBarAlwaysVisible=True)

        print(f"\n{type:-^100} Result")
        for i, _mod in enumerate(datas, 1):
            _text = u"[ {:0>5} ]  {}".format(i, _mod)
            print(_text)
            cmds.rowLayout(numberOfColumns=2, adjustableColumn=1,
                           columnWidth2=(100, 100))
            cmds.text(l=_text, align="left")
            cmds.button(label="[ select Target ]",
                        command=partial(self.select_target, _text.split()[4]),
                        enable=cmds.objExists(_text.split()[4]))
            cmds.setParent("..")
        print("{:-^100}\n\n".format(""))
        cmds.setParent("..")
        cmds.button(close_btn_name,
                    label="Close",
                    command=partial(self.close_error_and_modify_result_windows))

        cmds.setParent("..")
        cmds.showWindow(window_name)

    def open_modify_result_new(self, *args):
        if self.modify_errors:
            self.create_modify_result_window(type="error")

        if self.modifies:
            self.create_modify_result_window(type="modify")

    def close_all_window(self):
        self.close_error_result_window()
        self.close_modify_result_window()
        self.close_window()

    @classmethod
    def close_window(self):

        gui_util.close_pyside_windows()

        try:
            cmds.deleteUI(self._scroll)
        except Exception as e:
            pass
        try:
            cmds.deleteUI(self._frame)
        except Exception as e:
            pass
        try:
            cmds.deleteUI(self.NAME)
        except Exception as e:
            pass

    def close_error_and_modify_result_windows(self, *args):
        self.close_error_result_window()
        self.close_modify_result_window()

    def close_error_result_window(self, *args):
        try:
            cmds.deleteUI(self.error_result_scroll)
        except Exception as e:
            pass
        try:
            cmds.deleteUI(self.error_result_frame)
        except Exception as e:
            pass
        try:
            cmds.deleteUI(self.error_result_window)
        except Exception as e:
            pass

    def close_modify_result_window(self, *args):
        try:
            cmds.deleteUI(self.modify_result_scroll)
        except Exception as e:
            pass
        try:
            cmds.deleteUI(self.modify_result_frame)
        except Exception as e:
            pass
        try:
            cmds.deleteUI(self.modify_result_window)
        except Exception as e:
            pass

    def _open_export_window(self, *args):
        self.close_all_window()
        gui_util.open_export_window()


def main():
    print("check scene [ mdl_ ]...")
    if not DEV_MODE:
        logger.send_launch(u'ツール起動')
    _ck = CheckerGUI()
    _ck.do_check()
    print("end----")
