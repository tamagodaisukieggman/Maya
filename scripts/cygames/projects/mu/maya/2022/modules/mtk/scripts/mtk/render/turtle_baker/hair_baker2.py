# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import codecs
import os
import json
import subprocess
import maya.cmds as cmds
import pymel.core as pm
import pymel.util.path as pmp

class HairBaker2(object):

    def __init__(self):

        # このツールの内部名とタイトル名
        self.NAME = "hair_baker2_UI"
        self.TITLE = u"Hair Baker2"

        self._turtle_name = "Turtle"

        # ベイクするマップのサイズプリセット
        self._bake_map_sizes = ["512","1024","2048","4092"]

        # チェックボックスのリスト
        self._ckb_list = []

        # ベイクしたマップの出力パス
        self.exprot_path = ""

        # 設定を保存するjsonのファイル名
        self._prefs_file_name = "hair_baker_prefs.json"

        self._json_data = {}
        self._filename_prefix = ""

        self._baker_name = "ilrBakeLayer_mtk"
        self._render_global_name = "defaultRenderGlobals"
        self._turtle_render_option_name = "TurtleRenderOptions"
        self._render_global_name = "defaultRenderGlobals"
        self._layer_manager_name = "TurtleBakeLayerManager"
        
    def create(self):
        
        try:
            pm.deleteUI(self.NAME)
        except:pass

        # Trurtleプラグインのチェック
        # プラグインがなければツール終了
        if not self.turtle_check():
            return

        _separator_height = 5
        _check_box_height = 25

        with pm.window(self.NAME, title=self.TITLE, width=50, height=50) as self.WINDOW:
            with pm.columnLayout(adjustableColumn=True):
                with pm.rowLayout(numberOfColumns=2, columnWidth2=[50,10]):
                    self._export_path_field = pm.textField(text="", width=300)
                    self._file_dialog_btn = pm.button(label=u"...",
                                        command=pm.Callback(self._open_filedialog))
                self._bake_map_size = pm.optionMenu(label=u" ベイクマップの出力サイズ",
                                                    height=30)

                pm.text(label=u"",
                        height = 20,
                        backgroundColor=[0.1,0.1,0.1])

                self._chack_all_btn = pm.button(label=u"チェックボックス一括トグル",
                                                command = pm.Callback(self.toggle_all_check))

                self._color_map_ckb = pm.checkBox(label=u"{: <80}".format(u"Color Map"),
                                                value=True,
                                                backgroundColor=[0.5,0.3,0.3],
                                                height=_check_box_height)
                pm.separator(height = _separator_height)

                self._alpha_map_ckb = pm.checkBox(label=u"{: <80}".format(u"Alpha Map"),
                                                value=True,
                                                backgroundColor=[0.3,0.3,0.3],
                                                height=_check_box_height)
                pm.separator(height = _separator_height)

                self._normal_map_ckb = pm.checkBox(label=u"{: <80}".format(u"Normal Map"),
                                                value=True,
                                                backgroundColor=[0.5,0.5,0.7],
                                                height=_check_box_height)
                pm.separator(height = _separator_height)

                self._shadow_map_ckb = pm.checkBox(label=u"{: <80}".format(u"Shadow Map"),
                                                value=True,
                                                backgroundColor=[0.5,0.5,0.5],
                                                height=_check_box_height)
                pm.separator(height = _separator_height)

                self._id_map_ckb = pm.checkBox(label=u"{: <80}".format(u"ID Map"),
                                                value=True,
                                                backgroundColor=[0.6,0.6,0.1],
                                                height=_check_box_height)
                pm.separator(height = _separator_height)
                
                self._flow_map_ckb = pm.checkBox(label=u"{: <80}".format(u"Flow Map"),
                                                value=True,
                                                backgroundColor=[0.5,0.7,0.5],
                                                height=_check_box_height)
                pm.separator(height = _separator_height)

                self._depth_map_ckb = pm.checkBox(label=u"{: <80}".format(u"Depth Map"),
                                                value=True,
                                                backgroundColor=[0.2,0.2,0.2],
                                                height=_check_box_height)
                pm.separator(height = _separator_height)

                self._root_map_ckb = pm.checkBox(label=u"{: <80}".format(u"Root Map"),
                                                value=True,
                                                backgroundColor=[0.3,0.4,0.5],
                                                height=_check_box_height)

                self._bake_btn = pm.button(label=u"Bake Maps",
                            command=pm.Callback(self.bake_maps),
                            height=40)
                pm.separator(height = _separator_height)
                self._open_exploer_btn = pm.button(label=u"ベイク先をエクスプローラで開く",
                            command=pm.Callback(self.open_exploer),
                            backgroundColor=[0.2,0.2,0.2])
                
        # self._ckb_listリストにチェックボックスUIを追加
        self._ckb_list.append(self._color_map_ckb)
        self._ckb_list.append(self._alpha_map_ckb)
        self._ckb_list.append(self._normal_map_ckb)
        self._ckb_list.append(self._shadow_map_ckb)
        self._ckb_list.append(self._id_map_ckb)
        self._ckb_list.append(self._flow_map_ckb)
        self._ckb_list.append(self._depth_map_ckb)
        self._ckb_list.append(self._root_map_ckb)

        # ベイクサイズのオプションメニューをここで追加
        self._bake_map_size.addMenuItems(self._bake_map_sizes)
        
        # シーンが開かれているかのチェック
        # シーンが開かれていない場合は処理をしない
        # シーンが開かれている場合、テキストフィールドに自動で出力パスを設定
        self._get_scene_name()
        
        # スクリプトジョブでシーンが開かれるごとにシーン名の確認
        pm.scriptJob(parent=self.NAME, event=["SceneOpened", pm.Callback(self._get_scene_name)])
        pm.scriptJob(parent=self.NAME, event=["SceneSaved", pm.Callback(self._get_scene_name)] )

    def _open_filedialog(self):
        #
        # ファイルダイアログの表示
        #
        _path = pmp(self._export_path_field.getText())
        if not _path.exists():
            _path = pmp("C:/")
        result = pm.fileDialog2(startingDirectory=_path,
                                fileMode=3,
                                dialogStyle=2,
                                okCaption=u"選択",
                                caption=u"出力ディレクトリを選択してください")
        
        if not result:
            return
        self._export_path_field.setText(result[0].replace("\\","/"))

    def open_exploer(self):
        #
        # subprocess
        # を使ってテキストフィールドに入力されたパスを開きます
        #
        _path = pmp(self._export_path_field.getText())
        if not _path:
            pm.system.displayWarning(u"シーンを保存するか、開いてから実行してください")
            return
        if not _path.exists():
            pm.system.displayWarning(u"[ {} ] は存在しません".format(_path.replace("\\","/")))
            return
        try:
            subprocess.Popen(['explorer', _path.normpath()])
        except:
            pm.system.displayWarning(_path.replace("\\","/") + u" が開けませんでした")
            pass

    def _check_prefs(self):
        #
        #  初期設定があるか確認する
        #  C:/Users/S09251/Documents
        # "hair_baker_prefs.json"
        #
        _home_dir = pmp(os.getenv("HOME"))
        self._prefs_file = _home_dir.joinpath(self._prefs_file_name)
    
    def _load_prefs(self):
        #
        # jsonを読み込み設定があればそれを読み込みます
        # 設定がなければ初期設定を適用します
        # ここでテクスチャサイズの初期値を設定しています
        #
        self._check_prefs()
        if self._prefs_file.exists():
            with open(self._prefs_file, "r") as _json_file:
                self._json_data = json.load(_json_file)
            
            if self._filename_prefix in self._json_data.keys():
                self._bake_map_size.setSelect(self._bake_map_sizes.index(
                                self._json_data[self._filename_prefix]["bake_size"]) + 1)
                self._export_path_field.setText(self._json_data[self._filename_prefix]["export_path"].replace("\\", "/"))
                self._color_map_ckb.setValue(self._json_data[self._filename_prefix]["Color Map"])
                self._alpha_map_ckb.setValue(self._json_data[self._filename_prefix]["Alpha Map"])
                self._normal_map_ckb.setValue(self._json_data[self._filename_prefix]["Normal Map"])
                self._shadow_map_ckb.setValue(self._json_data[self._filename_prefix]["Shadow Map"])
                self._id_map_ckb.setValue(self._json_data[self._filename_prefix]["ID Map"])
                self._flow_map_ckb.setValue(self._json_data[self._filename_prefix]["Flow Map"])
                self._depth_map_ckb.setValue(self._json_data[self._filename_prefix]["Depth Map"])
                self._root_map_ckb.setValue(self._json_data[self._filename_prefix]["Root Map"])
            else:
                # UIの初期設定
                # ベイクサイズは「1k」が基準
                # 出力マップは全部

                self._bake_map_size.setSelect(2)
                self._color_map_ckb.setValue(True)
                self._alpha_map_ckb.setValue(True)
                self._normal_map_ckb.setValue(True)
                self._shadow_map_ckb.setValue(True)
                self._id_map_ckb.setValue(True)
                self._flow_map_ckb.setValue(True)
                self._depth_map_ckb.setValue(True)
                self._root_map_ckb.setValue(True)


    def _save_prefs(self):
        #
        # UIで設定された情報をjsonに保存します
        #
        #

        self._check_prefs()
        
        with open(self._prefs_file, "w") as _json_file:
            _json_data = json.dumps(
                            self._json_data,
                            indent=4,
                            sort_keys=True,
                            separators=(',', ': '))
            
            _json_file.write(_json_data)

    def turtle_check(self):
        #
        # Turtleの強制読み込みをします
        # そもそもプラグインがない場合はUIが表示されないようにしました
        #
        pm.loadPlugin(self._turtle_name, quiet=True)
        if self._turtle_name not in cmds.pluginInfo(query=True, listPlugins=True):
            pm.system.displayWarning(u"{} プラグインが見つかりません".format(self._turtle_name))
            return False
        return True


    def toggle_all_check(self):
        #
        # UI上のチェックボックスを一括で操作したいかなぁ、とつけてみました
        # 正直あまり有用ではないかと、、
        #
        if sum([x.getValue() for x in self._ckb_list]) < len(self._ckb_list) - 1:
            [x.setValue(True) for x in self._ckb_list]
        else:
            [x.setValue(False) for x in self._ckb_list]


    def _get_scene_name(self):
        #
        # スクリプトジョブにより、シーンを開いたとき、シーンを保存した時に実行されます
        # 出力パスの設定と初期設定の読み込みです
        #
        self.scene_name = pm.sceneName()
        if self.scene_name:
            #  シーン名「Z:/mtku/work/chara/ply/ply00/999/scenes/ply00_999.ma」
            #  Z:/mtku/work/chara/ply/ply00/999/scenes
            #  Z:/mtku/work/chara/ply/ply00/999
            #  Z:/mtku/work/chara/ply/ply00/999/subdata
            #  にする
            self.exprot_path = self.scene_name.splitpath()[0]
            self.exprot_path = self.exprot_path.splitpath()[0]
            self.exprot_path = self.exprot_path.joinpath("subdata", "hair")
            self._filename_prefix = self.scene_name.namebase
            
            self._bake_btn.setEnable(True)
        else:
            self.exprot_path = self.scene_name
            
            self._bake_btn.setEnable(False)
        
        self._export_path_field.setText(self.exprot_path.replace("\\", "/"))
        self._load_prefs()

    def setting_turtle(self):
        # Turtleの設定
        _render_global = pm.ls(self._render_global_name)
        if not _render_global:
            pm.displayError(u"{} がありません!!".format(self._render_global_name))
            return False
        self._render_global = _render_global[0]

        self._render_global.currentRenderer.set(self._turtle_name.lower())

        _baker = pm.ls(self._baker_name, type=pm.nt.IlrBakeLayer)
        if not _baker:
            self._baker = pm.createNode("ilrBakeLayer", name=self._baker_name)
        else:
            self._baker = _baker[0]

        _layer_manager = pm.ls(self._layer_manager_name, type=pm.nt.IlrBakeLayerManager)
        if not _layer_manager:
            self._layer_manager = pm.createNode("ilrBakeLayerManager", name=self._layer_manager_name)
            pm.connectAttr(self._baker + ".index", self._layer_manager+".bakeLayerId[0]")
        else:
            self._layer_manager = _layer_manager[0]

        _turtle_render_option = pm.ls(self._turtle_render_option_name)
        if not _turtle_render_option:
            self._turtle_render_option = pm.createNode("ilrOptionsNode", name=self._turtle_render_option_name)
            self._turtle_render_option.message >> self._baker.renderOptions
        else:
            self._turtle_render_option = _turtle_render_option[0]
        
        self._turtle_render_option.renderer.set(1)
        return True


    def bake_maps(self):

        # ベイクするノードを限定するため選択を取得
        _current_selections = pm.ls(orderedSelection=True, type=pm.nt.Transform)
        if len(_current_selections) != 2:
            pm.confirmDialog(message=u"ハイメッシュ、ローメッシュの順番で2つのノードを選択してください",
                            title=u'選択を確認してください',
                            button=['OK'],
                            defaultButton='OK',
                            cancelButton="OK",
                            dismissString="OK")
            return
        
        # UIのプルダウンメニューから出力サイズを取得
        # self._bake_map_sizesリストの　self._bake_map_size.getSelect()で取得される intの「-1」
        _export_size = self._bake_map_sizes[self._bake_map_size.getSelect() - 1]

        # UIのチェックボックスから出力するマップの種類を取得
        # 出力サイズと共に、辞書に入れる

        _map_beke_type = {
                "Color Map":self._color_map_ckb.getValue(),
                "Alpha Map":self._alpha_map_ckb.getValue(),
                "Normal Map":self._normal_map_ckb.getValue(),
                "Shadow Map":self._shadow_map_ckb.getValue(),
                "ID Map":self._id_map_ckb.getValue(),
                "Flow Map":self._flow_map_ckb.getValue(),
                "Depth Map":self._depth_map_ckb.getValue(),
                "Root Map":self._root_map_ckb.getValue()
        }

        # 後でfor文でチェックボックスから取った辞書を使いたいので
        # プリファレンス用に辞書を複製、必要な情報を追加
        _map_beke_pref = _map_beke_type.copy()
        _map_beke_pref["bake_size"] = _export_size
        _map_beke_pref["export_path"] = self._export_path_field.getText().replace("\\", "/")
        
        # ファイル名のキーとマップ設定の値でさらに辞書を作る
        _prefs_data = {self._filename_prefix:_map_beke_pref}

        # 読まれているjsonデータに現在のプリセットをセット
        self._json_data[self._filename_prefix] = _map_beke_pref

        # プリセットをjsonとして保存
        self._save_prefs()

        # 出力先のディレクトリがなければまとめて作成
        if not self.exprot_path.exists():
            self.exprot_path.makedirs()
        
        # ベイクソースとベイクターゲット
        # 選択以下のメッシュノードをそれぞれに充てる
        _source_meshes = _current_selections[0].listRelatives(allDescendents=True, type=pm.nt.Mesh)
        _target_meshes = _current_selections[1].listRelatives(allDescendents=True, type=pm.nt.Mesh)

        # Turtleの設定
        # 「defaultRenderGlobals」が見つからないと処理を中止
        if not self.setting_turtle():
            return

        _map_type = "Normal Map"
        _alpha_flag = 0
        _full_shading_flag = 0
        _normal_map_flag = 1
        _custom_shader_use_flag = 0
        _custom_shader = ""

        self.turtle_bake(_target_meshes,
                        _source_meshes,
                        _alpha_flag,
                        _export_size,
                        _map_type,
                        _full_shading_flag,
                        _normal_map_flag,
                        _custom_shader_use_flag,
                        _custom_shader)
    
    def create_custom_shader(self, _source_meshes):
        _ilr_occ_sampler = pm.shadingNode("ilrOccSampler", asShader=True)
        _shading_group = pm.sets(_ilr_occ_sampler,
                        renderable=True,
                        noSurfaceShader=True,
                        empty=True,
                        name="{}SG".format(_ilr_occ_sampler.name()))
        
        pm.sets(_shading_group, forceElement=_source_meshes)
        _ilr_occ_sampler.outColor >> _shading_group.surfaceShader
        _ilr_occ_sampler.outColor >> _baker.customShader

    def turtle_bake(self,   _target_meshes,
                            _source_meshes,
                            _alpha_flag,
                            _size,
                            _map_type,
                            _full_shading_flag,
                            _normal_map_flag,
                            _custom_shader_use_flag,
                            _custom_shader):
        
        # 「Normal Map」などの文字列からスペース前半部分のみを抽出
        _map_type = _map_type.split(_map_type)[0]

        # Turtleのベイクコマンド「ilrTextureBakeCmd」が
        # Pythonでもtarget とsourceの引き渡しが文字列のようなので
        # 元のmelのままでコマンド実行
        _cmds_eval = '''
                    ilrTextureBakeCmd 
                    {0:} 
                    {1:} 
                    -frontRange 0 
                    -backRange 200 
                    -frontBias 0 
                    -backBias -100 
                    -transferSpace 1 
                    -selectionMode 0 
                    -mismatchMode 0 
                    -envelopeMode 0 
                    -ignoreInconsistentNormals 1 
                    -considerTransparency 0 
                    -transparencyThreshold 0.001000000047 
                    -camera "persp" 
                    -normalDirection 1 
                    -shadows 0 
                    -alpha {2:} 
                    -viewDependent 0 
                    -orthoRefl 1 
                    -backgroundColor 0.5 0.5 1 
                    -frame 1 
                    -bakeLayer {3:} 
                    -width {4:} 
                    -height {4:} 
                    -saveToRenderView 0 
                    -saveToFile 1 
                    -directory "{5:}" 
                    -fileName "{6:}" 
                    -fileFormat 0 
                    -visualize 0 
                    -uvRange 0 
                    -uMin 0 
                    -uMax 1 
                    -vMin 0 
                    -vMax 1 
                    -uvSet "" 
                    -tangentUvSet "" 
                    -edgeDilation 5 
                    -bilinearFilter 1 
                    -merge 1 
                    -conservative 0 
                    -windingOrder 1 
                    -fullShading {7:} 
                    -normals {8:} 
                    -normalsCoordSys 0 
                    -normalsFlipChannel 0 
                    -normalsFaceTangents 0 
                    -normalsUseBump 0 
                    -stencilBake 0 
                    -useRenderView 0 
                    -layer defaultRenderLayer
                    -custom {9:} 
                    -customShader {10:}
                    '''.format(''.join(['-target "{}" '.format(x.name()) for x in _target_meshes]),
                                ''.join(['-source "{}" '.format(x.name()) for x in _source_meshes]),
                                _alpha_flag,
                                self._baker_name,
                                _size,
                                self.exprot_path.replace("\\","/"),
                                "{}_{}.tga".format(self._filename_prefix,_map_type),
                                _full_shading_flag,
                                _normal_map_flag,
                                _custom_shader_use_flag,
                                _custom_shader)

        pm.mel.eval(_cmds_eval)



    def _start_bake(self, _size = "1024"):

        _current_selections = pm.ls(orderedSelection=True, type=pm.nt.Transform)
        if len(_current_selections) != 2:
            pm.confirmDialog(message=u"ハイメッシュ、ローメッシュの順番で2つのノードを選択してください",
                            title=u'選択を確認してください',
                            button=['OK'],
                            defaultButton='OK',
                            cancelButton="OK",
                            dismissString="OK")
            return
        
        # _all_transform = pm.ls(type=pm.nt.Transform)

        # _source_meshes = []
        # _target_meshes = []
        
        # [_source_meshes.extend(pm.ls(x, type=pm.nt.Transform)) for x in _current_selections[0].longName().split("|")]
        # [_target_meshes.extend(pm.ls(x, type=pm.nt.Transform)) for x in _current_selections[1].longName().split("|")]
        # print _source_meshes
        # print _target_meshes
        # _show_meshes = _source_meshes + _target_meshes
        # print _show_meshes
        # print list(set(_all_transform) - set(_show_meshes))
        # [x.hide() for x in list(set(_all_transform) - set(_show_meshes))]
        # [x.show() for x in _show_meshes]
        # return
        _source_meshes = _current_selections[0].listRelatives(allDescendents=True, type=pm.nt.Mesh)
        # _source_meshes = _current_selections[0].listRelatives(allDescendents=True, type=pm.nt.EditGuidesShape)
        _target_meshes = _current_selections[1].listRelatives(allDescendents=True, type=pm.nt.Mesh)

        # if not _source_meshes:
        #     return
        # if not _target_meshes:
        #     return
        
        _render_global = pm.ls(self._render_global_name)
        if not _render_global:
            pm.displayError(u"{} がありません!!".format(self._render_global_name))
            return
        self._render_global = _render_global[0]

        self._render_global.currentRenderer.set(self._turtle_name.lower())

        
        _baker = pm.ls(self._baker_name, type=pm.nt.IlrBakeLayer)
        if not _baker:
            self._baker = pm.createNode("ilrBakeLayer", name=self._baker_name)
        else:
            self._baker = _baker[0]

        # _baker.renderSelection.set(False)
        # _baker.fullShading.set(True)
        # _baker.tbMerge.set(True)
        # _baker.custom.set(True)


        _layer_manager = pm.ls(self._layer_manager_name, type=pm.nt.IlrBakeLayerManager)
        if not _layer_manager:
            self._layer_manager = pm.createNode("ilrBakeLayerManager", name=self._layer_manager_name)
            # _baker.index >> _layer_manager.bakeLayerId[0]
            pm.connectAttr(self._baker + ".index", self._layer_manager+".bakeLayerId[0]")
        else:
            self._layer_manager = _layer_manager[0]


        _turtle_render_option = pm.ls(self._turtle_render_option_name)
        if not _turtle_render_option:
            self._turtle_render_option = pm.createNode("ilrOptionsNode", name=self._turtle_render_option_name)
            self._turtle_render_option.message >> self._baker.renderOptions
            # pm.connectAttr(_turtle_render_option + ".message", _baker + ".renderOptions")
            # pm.displayError(u"{} がありません!!".format(self._turtle_render_option_name))
            # return
        else:
            self._turtle_render_option = _turtle_render_option[0]
        
        self._turtle_render_option.renderer.set(1)
        # _turtle_render_option.imageFormat.set(0)

        # _baker.tbSaveToFile(True)
        # _baker.tbDirectory(self.exprot_path.replace("\\","/"))

        # pm.mel.eval("ilrClearTargetSurfaces();")
        
        # _baker.addMembers(_target_meshes)
        # for i,_source_mesh in enumerate(_source_meshes):
        #     _source_mesh.message >> _baker.sourceLinks[i].sourceLinkFrom
        
        # _ilr_occ_sampler = pm.shadingNode("ilrOccSampler", asShader=True)
        # _shading_group = pm.sets(_ilr_occ_sampler,
        #                 renderable=True,
        #                 noSurfaceShader=True,
        #                 empty=True,
        #                 name="{}SG".format(_ilr_occ_sampler.name()))
        
        # pm.sets(_shading_group, forceElement=_target_meshes)
        # _ilr_occ_sampler.outColor >> _shading_group.surfaceShader
        # _ilr_occ_sampler.outColor >> _baker.customShader

        _alpha_flag = 0
        _full_shading_flag = 0
        _normal_map_flag = 1
        _custom_shader_use_flag = 0
        _custom_shader = ""

        _cmds_eval = '''
                    ilrTextureBakeCmd 
                    {0:} 
                    {1:} 
                    -frontRange 0 
                    -backRange 200 
                    -frontBias 0 
                    -backBias -100 
                    -transferSpace 1 
                    -selectionMode 0 
                    -mismatchMode 0 
                    -envelopeMode 0 
                    -ignoreInconsistentNormals 1 
                    -considerTransparency 0 
                    -transparencyThreshold 0.001000000047 
                    -camera "persp" 
                    -normalDirection 0 
                    -shadows 0 
                    -alpha {2:} 
                    -viewDependent 0 
                    -orthoRefl 1 
                    -backgroundColor 0.5 0.5 1 
                    -frame 1 
                    -bakeLayer {3:} 
                    -width {4:} 
                    -height {4:} 
                    -saveToRenderView 0 
                    -saveToFile 1 
                    -directory "{5:}" 
                    -fileName "{6:}" 
                    -fileFormat 0 
                    -visualize 0 
                    -uvRange 0 
                    -uMin 0 
                    -uMax 1 
                    -vMin 0 
                    -vMax 1 
                    -uvSet "" 
                    -tangentUvSet "" 
                    -edgeDilation 5 
                    -bilinearFilter 1 
                    -merge 1 
                    -conservative 0 
                    -windingOrder 1 
                    -fullShading {7:} 
                    -normals {8:} 
                    -normalsCoordSys 0 
                    -normalsFlipChannel 0 
                    -normalsFaceTangents 0 
                    -normalsUseBump 0 
                    -stencilBake 0 
                    -useRenderView 0 
                    -layer defaultRenderLayer
                    -custom {9:} 
                    -customShader {10:}
                    '''.format(''.join(['-target "{}" '.format(x.name()) for x in _target_meshes]),
                                ''.join(['-source "{}" '.format(x.name()) for x in _source_meshes]),
                                _alpha_flag,
                                self._baker_name,
                                _size,
                                self.exprot_path.replace("\\","/"),
                                "{}_{}.tga".format(self._filename_prefix,"Normal"),
                                _full_shading_flag,
                                _normal_map_flag,
                                _custom_shader_use_flag,
                                _custom_shader)

        pm.mel.eval(_cmds_eval)



    def _start_bake_old(self, size = "1024"):

        _current_selections = pm.ls(orderedSelection=True, type=pm.nt.Transform)
        if len(_current_selections) != 2:
            pm.confirmDialog(message=u"ハイメッシュ、ローメッシュの順番で2つのノードを選択してください",
                            title=u'選択を確認してください',
                            button=['OK'],
                            defaultButton='OK',
                            cancelButton="OK",
                            dismissString="OK")
            return
        
        _source_meshes = _current_selections[0].listRelatives(allDescendents=True, type=pm.nt.Mesh)
        _target_meshes = _current_selections[1].listRelatives(allDescendents=True, type=pm.nt.Mesh)

        if not _source_meshes:
            return
        if not _target_meshes:
            return
        
        self._baker_name = "ilrBakeLayer_mtk"
        self._render_global_name = "defaultRenderGlobals"
        self._turtle_render_option_name = "TurtleRenderOptions"
        self._render_global_name = "defaultRenderGlobals"
        self._layer_manager_name = "TurtleBakeLayerManager"

        _render_global = pm.ls(self._render_global_name)
        if not _render_global:
            pm.displayError(u"{} がありません!!".format(self._render_global_name))
            return
        _render_global = _render_global[0]

        _render_global.currentRenderer.set(self._turtle_name.lower())

        
        _baker = pm.ls(_baker_name, type=pm.nt.IlrBakeLayer)
        if not _baker:
            _baker = pm.createNode("ilrBakeLayer", name=_baker_name)
        else:
            _baker = _baker[0]

        _baker.renderSelection.set(False)
        _baker.fullShading.set(True)
        _baker.tbMerge.set(True)
        _baker.custom.set(True)


        _layer_manager = pm.ls(self._layer_manager_name, type=pm.nt.IlrBakeLayerManager)
        if not _layer_manager:
            _layer_manager = pm.createNode("ilrBakeLayerManager", name=self._layer_manager_name)
            # _baker.index >> _layer_manager.bakeLayerId[0]
            pm.connectAttr(_baker + ".index", _layer_manager+".bakeLayerId[0]")
        else:
            _layer_manager = _layer_manager[0]


        _turtle_render_option = pm.ls(self._turtle_render_option_name)
        if not _turtle_render_option:
            _turtle_render_option = pm.createNode("ilrOptionsNode", name=self._turtle_render_option_name)
            _turtle_render_option.message >> _baker.renderOptions
            # pm.connectAttr(_turtle_render_option + ".message", _baker + ".renderOptions")
            # pm.displayError(u"{} がありません!!".format(self._turtle_render_option_name))
            # return
        else:
            _turtle_render_option = _turtle_render_option[0]
        
        _turtle_render_option.renderer.set(1)
        _turtle_render_option.imageFormat.set(0)

        # _baker.tbSaveToFile(True)
        # _baker.tbDirectory(self.exprot_path.replace("\\","/"))

        pm.mel.eval("ilrClearTargetSurfaces();")
        
        _baker.addMembers(_target_meshes)
        for i,_source_mesh in enumerate(_source_meshes):
            _source_mesh.message >> _baker.sourceLinks[i].sourceLinkFrom
        
        _ilr_occ_sampler = pm.shadingNode("ilrOccSampler", asShader=True)
        _shading_group = pm.sets(_ilr_occ_sampler,
                        renderable=True,
                        noSurfaceShader=True,
                        empty=True,
                        name="{}SG".format(_ilr_occ_sampler.name()))
        
        pm.sets(_shading_group, forceElement=_target_meshes)
        _ilr_occ_sampler.outColor >> _shading_group.surfaceShader
        _ilr_occ_sampler.outColor >> _baker.customShader

        _cmds_eval = '''
        ilrTextureBakeCmd -target "{0:}" 
        -frontRange 0 -backRange 200 -frontBias 0 -backBias -100 
        -transferSpace 1 -selectionMode 0 -mismatchMode 0 -envelopeMode 0 
        -ignoreInconsistentNormals 1 -considerTransparency 0 
        -transparencyThreshold 0.001000000047 
        -camera "persp" -normalDirection 0 -shadows 1 -alpha 0 
        -viewDependent 0 -orthoRefl 1 
        -backgroundColor 0 0 0 -frame 0 -bakeLayer {1:} -width {2:} -height {2:} 
        -saveToRenderView 0 -saveToFile 1 -directory "{3:}" 
        -fileName "{4:}" 
        -fileFormat 0 -visualize 0 -uvRange 0 -uMin 0 -uMax 1 -vMin 0 
        -vMax 1 -uvSet "" -tangentUvSet "" 
        -edgeDilation 5 -bilinearFilter 1 -merge 0 -conservative 0 
        -windingOrder 1 -fullShading 1 -custom 1 -customShader {5:} -useRenderView 1 
        -layer defaultRenderLayer'''.format(",".join([x.name() for x in _target_meshes]),
                                        _baker_name,
                                        size,
                                        self.exprot_path.replace("\\","/"),
                                        "{}_{}.tga".format(self._filename_prefix,"AO"),
                                        _ilr_occ_sampler)

        pm.mel.eval(_cmds_eval)


    def _ao_bake(self, size = "1024"):
        pass

def main():
    hb2 = HairBaker2()
    hb2.create()

main()