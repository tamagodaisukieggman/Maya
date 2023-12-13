
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
# from tatool.log import ToolLogging, Stage
import maya.mel
import maya.cmds as cmds
import webbrowser
import os
import glob
import codecs

from functools import partial
from shr.utils import getCurrentSceneFilePath

tool_title = 'HDA Loader'
project = "mutsunokami"
toolcategory = 'Maya'
version = '1.0'

# stage = Stage.dev

# ToolLogging = ToolLogging(projects=project,
#                           toolcategory=toolcategory,
#                           target_stage=stage,
#                           tool_version=version)

# logger = ToolLogging.getTemplateLogger(tool_title)


HOST = os.environ['COMPUTERNAME']
PORT = 7325
# PORT = 7002

# HDA_PATH = "D:/ando/Houdini"
PLUGIN_PATH = "Z:/mtk/tools/maya/modules/houdini_engine/plug-ins"
HOUDINI_SCRIPTS_PATH = "Z:/mtk/tools/maya/modules/houdini_engine/scripts/houdini_engine_for_maya"
HDA_PATH = "Z:/mtk/tools/maya/share/hda"
TITLE = tool_title
NAME = "mtk_hda_loader_ui"
TOOL_NAME = "MutsunokamiHDALoader"

# # スクリプトパスの追加
# if HOUDINI_SCRIPTS_PATH not in sys.path:
#     sys.path.append(HOUDINI_SCRIPTS_PATH)

# # import houdiniEngineSelection


class ShaderTexture:
    def __init__(self, hda=None, nodes=None):
        self.hda = hda
        self.nodes = nodes
        # houGeo = cmds.listConnections(nodes, s=True, d=False, type='houdiniInputGeometry')
        self.meshes = [x for x in cmds.listRelatives(nodes, allDescendents=True, fullPath=True, type="mesh")if not cmds.getAttr("{}.intermediateObject".format(x))]
        self.get_shading_engine()

    def get_shading_engine(self, *args):
        self.mesh_sg_dict = {}
        self.sgs = []
        # print(self.meshes)
        for mesh in self.meshes:
            sgs = cmds.listConnections(mesh, type='shadingEngine')
            if sgs:
                sg = sgs[0]
                self.sgs.append(sg)
                self.mesh_sg_dict[mesh] = sg
        self.sgs = list(set(self.sgs))

    def set_attribute(self, *args):
        cmds.setAttr("{}.houdiniAssetParm.houdiniAssetParm_sg_texture_path".format(self.hda), self._text, type="string")

    def get_textures(self, *args):
        self.sg_tex_dict = {}
        self._text = ''
        if self.sgs:
            for sg in self.sgs:
                print(sg, " ------shading group")
                connections = cmds.listConnections(sg, s=True, d=False)
                mat = cmds.ls(connections, mat=True)
                fileNodes = cmds.ls(cmds.listHistory(mat), type="file")
                print(fileNodes, " -------textures")
                if fileNodes:
                    texture = cmds.getAttr("{}.ftn".format(fileNodes[0])).replace(os.sep, '/')
                    print(texture, " -----texture path")
                    self.sg_tex_dict[sg] = texture
                    self._text += "{},{}|".format(sg, texture)
        if self.hda and self._text:
            self.set_attribute()


class Texture:
    def __init__(self, path="", shadingEngine=""):
        self.shadingEngine = shadingEngine
        self.path = path.replace(os.sep, '/')
        self.name = os.path.basename(path)
        self.base_name = os.path.splitext(self.name)[0]
        self.texture_name, self.texture_type = self.base_name.rsplit("_", 1)
        self.dir = os.path.split(path)[0]

    def __repr__(self):
        return self.path


def send_to_houdini_texture_paths(shadingEngines=[]):

    if not shadingEngines:
        return

    # group_dict_list = []
    # group_dict = {}
    send_text = ""
    for shadingEngine in shadingEngines:
        connections = cmds.listConnections(shadingEngine, s=True, d=False)
        mat = cmds.ls(connections, mat=True)
        fileNodes = cmds.ls(cmds.listHistory(mat), type="file")

        if fileNodes:
            texture = cmds.getAttr("{}.ftn".format(fileNodes[0])).replace(os.sep, '/')
            if os.path.exists(texture):
                texObj = Texture(texture, shadingEngine)
                send_text += "{},{}|".format(shadingEngine, texObj.path)
                search_files = [x.replace(os.sep, '/') for x in glob.glob(os.path.join(texObj.dir, texObj.texture_name) + "*") if texObj.name != os.path.basename(x)]
                if search_files:
                    send_text += "".join(["{},{}|".format(shadingEngine, x) for x in search_files])
                    # group_dict_list.append(search_files)
        send_text += "*"
    return send_text


def send_to_houdini_texture_path(shadingEngines=[]):

    if not shadingEngines:
        return

    send_text = ""

    for shadingEngine in shadingEngines:
        connections = cmds.listConnections(shadingEngine, s=True, d=False)
        mat = cmds.ls(connections, mat=True)
        fileNodes = cmds.ls(cmds.listHistory(mat), type="file")

        if fileNodes:
            texture = cmds.getAttr("{}.ftn".format(fileNodes[0])).replace(os.sep, '/')
            if os.path.exists(texture):
                # texObj = Texture(texture, shadingEngine)
                send_text += "{},{}|".format(shadingEngine, texture)
                # search_files = [x.replace(os.sep, '/') for x in glob.glob(os.path.join(texObj.dir, texObj.texture_name) + "*") if texObj.name != os.path.basename(x)]
                # if search_files:
                #     send_text += "".join(["{},{}|".format(shadingEngine, x) for x in search_files])
        # send_text += "*"
    return send_text


def get_texture_path(shadingEngine=None):
    file_path = ""
    # if not cmds.ls(shadingEngine):
    #     return
    connections = cmds.listConnections(shadingEngine, s=True, d=False)
    # if not connections:
    #     return

    mat = cmds.ls(connections, mat=True)
    fileNodes = cmds.ls(cmds.listHistory(mat), type="file")

    if fileNodes:
        texture = cmds.getAttr("{}.ftn".format(fileNodes[0])).replace(os.sep, '/')
        file_path = texture
        if os.path.exists(texture):
            file_path = texture
            # texture_directory = os.path.split(texture)[0]
            # texture_obj = Textrue(texture, shadingEngine)
            # file_name = os.path.basename(texture)
            # file_basename = os.path.splitext(file_name)[0]
            # texture_name,texture_type = file_basename.rsplit("_",1)
    # print(shadingEngine)
    print(file_path)
    # return file_path


def set_colorset_no_display(_hda):
    _shape_node = cmds.listRelatives(_hda,
                                     allDescendents=True,
                                     fullPath=True,
                                     type="mesh")

    if not _shape_node:
        return

    _shape_node = _shape_node[0]
    cmds.setAttr("{}.displayColors".format(_shape_node), 0)


def set_colorset_display(_hda):

    if not _hda:
        return

    _flag = cmds.getAttr("{}.houdiniAssetParm_show_mask".format(_hda))

    if not _flag:
        return

    _shape_node = cmds.listRelatives(_hda,
                                     allDescendents=True,
                                     fullPath=True,
                                     type="mesh")

    if not _shape_node:
        return

    _shape_node = _shape_node[0]
    cmds.select(_shape_node, r=True)
    cmds.polyColorSet(currentColorSet=True, colorSet="Cd")
    cmds.setAttr("{}.displayColors".format(_shape_node), 0)
    cmds.setAttr("{}.displayColors".format(_shape_node), 1)
    cmds.setAttr("{}.displayColorChannel".format(_shape_node),
                 "Ambient+Diffuse",
                 type="string")
    cmds.setAttr("{}.materialBlend".format(_shape_node), 0)
    cmds.select(_hda, r=True)


class HDAData:
    def __init__(self, name="", path=""):
        self.name = name
        self.short_name = name.split("/")[-1]
        self.path = path.replace(os.sep, '/')
        self.btn_name = "{}_{}_btn".format(NAME, name)


class HDALoader(object):

    _SessionType = {"houdiniEngineSessionType": 2}
    _SessionPipeCustom = {"houdiniEngineSessionPipeCustom": 0}
    _ThriftPipe = {"houdiniEngineThriftPipe": "hapi"}

    HOUDINI_ENGINE_NAME = "houdiniEngine"
    PLUGIN_EXT = ".mll"

    _window_width = 300
    _window_hight = 150

    _scroll_layout_name = "{}_scroll_layout".format(NAME)
    _reload_btn_name = "{}_reload_btn".format(NAME)
    _sample_radio_btn_neme = "{}_sample_radio_btn".format(NAME)
    _develop_check_btn_name = "{}_develop_check".format(NAME)
    _filter_text_field_name = "{}_filter_text_field".format(NAME)
    _filter_clear_btn_name = "{}_filter_clear_btn".format(NAME)

    _radio_btn_dict = {
        u"ワールド": 0,
        u"モデル": 1,
        u"コンポーネント": 4,
        u"トポロジ": 5
    }
    _buttons = []
    _tso_flag = False

    # logger.send_launch('{}-Launch'.format(tool_title))

    def remove_memory(self):
        self.nodename_filename = []
        self._scene_hdas = {}

    def create(self):
        try:
            cmds.deleteUI(NAME)
        except BaseException:
            pass

        if not os.path.exists(HDA_PATH):
            _message = "not_find_path {}".format(HDA_PATH.replace(os.sep, '/'))
            # logger.send_crash('{}-Crash-{}'.format(tool_title, _message))
            cmds.confirmDialog(message=u"[ {} ]\nディレクトリがありません".format(HDA_PATH.replace(os.sep, '/')),
                               title=u'ディレクトリの確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        self.glob_hda()

        if not self.maya_hda:
            _message = "not_find_hda"
            # logger.send_crash('{}-Crash-{}'.format(tool_title, _message))
            cmds.confirmDialog(message=u"[ HDA ]ファイルがありません",
                               title=u'HDAの確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        if not self._check_plugin():
            _message = "not_find_plugin"
            # logger.send_crash('{}-Crash-{}'.format(tool_title, _message))
            cmds.confirmDialog(message=u"Z ドライブに [ houdiniEngine ] プラグインがありません",
                               title=u'プラグインの確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        self._set_option_var()

        _option_setting = self._check_option_var()
        if _option_setting:
            _message = "can_not_change_option_var_{}".format(_option_setting)
            # logger.send_crash('{}-Crash-{}'.format(tool_title, _message))
            cmds.confirmDialog(message=u"オプション設定 [{}] を変更できません".format(_option_setting),
                               title=u'オプション設定の確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        if not self.set_active_z_drive_plugin():
            _message = "can_not_activate_z_drive_plugin"
            # logger.send_crash('{}-Crash-{}'.format(tool_title, _message))
            cmds.confirmDialog(message=u"Z ドライブの [ houdiniEngine ] プラグインをアクティブにできません",
                               title=u'プラグインの確認',
                               button=['OK'],
                               defaultButton='OK',
                               cancelButton="OK",
                               dismissString="OK")
            return

        cmds.window(NAME, title=TITLE,
                    width=self._window_width,
                    height=self._window_hight,
                    resizeToFitChildren=True,
                    closeCommand=partial(self.change_tso))
        cmds.frameLayout(labelVisible=False, width=self._window_width)

        cmds.checkBox(self._develop_check_btn_name,
                      l=u"開発者モード",
                      value=False,
                      changeCommand=partial(self._get_hda))
        # cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
        # self._develop_radio_btn = cmds.radioCollection()
        # cmds.radioButton(label=u"リリース版", select=True)
        # cmds.radioButton(label=u"開発版")
        # cmds.setParent("..")

        cmds.button(self._reload_btn_name,
                    label=u"全ての HDA をリロード",
                    # width=self._window_width / 2,
                    height=25,
                    # enable=False,
                    command=partial(self._get_hda))
        cmds.separator(height=5)
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
        cmds.text(l=u"絞り込み検索")
        cmds.text(l="")
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
        cmds.textField(self._filter_text_field_name,
                       aie=True,
                       cc=partial(self._get_hda), h=25)
        cmds.button(self._filter_clear_btn_name, l=u"clear",
                    c=partial(self.clear_filter_text_field), h=25)
        cmds.setParent("..")

        cmds.scrollLayout(self._scroll_layout_name,
                          height=self._window_hight - 10,
                          width=self._window_width,
                          childResizable=True,
                          verticalScrollBarAlwaysVisible=True)

        cmds.setParent("..")
        cmds.button(label=u"ベイクアセット", command=partial(self._bake_asset))
        cmds.rowLayout(numberOfColumns=4, adjustableColumn=4)
        self._sample_radio_btn_neme = cmds.radioCollection()
        cmds.radioButton(label=u"ワールド", select=True)
        cmds.radioButton(label=u"モデル")
        cmds.radioButton(label=u"コンポーネント")
        cmds.radioButton(label=u"トポロジ")
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
        cmds.button(label=u"UVの転送",
                    command=partial(self._transfer_attributes, "uv"),
                    width=self._window_width / 2)
        cmds.button(label=u"法線の転送",
                    command=partial(self._transfer_attributes, "normal"),
                    width=self._window_width / 2)
        cmds.setParent("..")

        cmds.separator(height=1)

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
        cmds.button(label=u"アイソレートセレクトトグル",
                    command=partial(self.isolate_select),
                    width=self._window_width / 2)
        cmds.button(label=u"ワイヤー表示トグル",
                    command=partial(self.wire_display),
                    width=self._window_width / 2)
        cmds.setParent("..")

        cmds.scriptJob(parent=NAME, event=("SceneOpened", partial(self.remove_memory)))
        cmds.scriptJob(parent=NAME, event=("NewSceneOpened", partial(self.remove_memory)))

        self._get_hda()
        self._trackSelectionOrder_flag()
        # self.port_open()
        cmds.showWindow(NAME)

    def apply_filter(self, *args):
        _text = cmds.textField(self._filter_text_field_name, q=True, tx=True)

    def clear_filter_text_field(self, *args):
        cmds.textField(self._filter_text_field_name, e=True, tx="")
        self._get_hda()

    def show_wire(self, *args):
        cmds.displayPref(wireframeOnShadedActive='full')

    def show_all(self, *args):
        _Panels = cmds.getPanel(type="modelPanel")
        for _Panel in _Panels:
            cmds.isolateSelect(_Panel, state=False)
            cmds.isolateSelect(_Panel, removeSelected=True)

    def wire_display(self, *args):
        if cmds.displayPref(q=True, wireframeOnShadedActive=True) == 'full':
            cmds.displayPref(wireframeOnShadedActive='none')
        else:
            cmds.displayPref(wireframeOnShadedActive='full')

    def isolate_select(self, *args):
        _Panels = cmds.getPanel(type="modelPanel")
        _state = cmds.isolateSelect(_Panels[-1], q=True, state=True)
        for _Panel in _Panels:
            if _state:
                cmds.isolateSelect(_Panel, state=False)
                cmds.isolateSelect(_Panel, removeSelected=True)
            else:
                cmds.isolateSelect(_Panel, state=True)
                cmds.isolateSelect(_Panel, addSelected=True)

    def glob_hda(self, dev_mode=None, *args):
        self.maya_hda = []
        hda = glob.glob(HDA_PATH + "/*.hda")
        if dev_mode:
            develop_path = os.path.join(HDA_PATH, "develop")
            develop = glob.glob(develop_path + "/*.hda*")
            if develop:
                hda.extend(develop)
        self.maya_hda = hda

    def change_tso(self, *args):
        cmds.selectPref(tso=self._tso_flag)
        self.show_wire()
        self.show_all()

    def _trackSelectionOrder_flag(self):
        _tso_flag = cmds.selectPref(q=True, tso=True)
        self._tso_flag = _tso_flag
        if not _tso_flag:
            cmds.selectPref(tso=True)
        return _tso_flag

    def _transfer_attributes(self, *args):
        _type_flag = args[0]

        _select_btn = cmds.radioCollection(self._sample_radio_btn_neme,
                                           q=True,
                                           select=True)
        _select_label = cmds.radioButton(_select_btn, q=True, l=True)
        _current_space = self._radio_btn_dict[_select_label]

        if _type_flag == "uv":
            transferUVs = True
            transferNormals = False
        elif _type_flag == "normal":
            transferUVs = False
            transferNormals = True

        sel = cmds.ls(orderedSelection=True, type="transform")

        if not sel or len(sel) == 1:
            _message = u"二つ以上のノードを選択してから実行してください"
            print(_message)
            cmds.warning(u"二つ以上のノードを選択してから実行してください")
            return

        source = sel.pop(0)

        for s in sel:
            # print(source,s," -----transfer-----")
            cmds.transferAttributes(source, s,
                                    transferPositions=False,
                                    transferColors=False,
                                    transferNormals=transferNormals,
                                    transferUVs=transferUVs,
                                    sampleSpace=_current_space,
                                    searchMethod=3,
                                    )

    def _reload_houdini_asset(self, *args):
        nodes = cmds.ls(type="transform")
        houdini_assets = []
        for node in nodes:
            try:
                if cmds.nodeType(node) == "houdiniAsset":
                    houdini_assets.append(node)
            except Exception as e:
                print("error--- ", e)

        if houdini_assets:
            for houdini_asset in houdini_assets:
                cmds.houdiniAsset(reloadAsset=houdini_asset)

    def _get_hda(self, *args):
        _error = []
        _text = cmds.textField(self._filter_text_field_name, q=True, tx=True)
        # mods = cmds.getModifiers()
        dev_mode = cmds.checkBox(self._develop_check_btn_name, q=True, value=True)
        # if dev_mode:
        #     # cmds.unloadPlugin(self.HOUDINI_ENGINE_NAME, force=True)
        #     self._check_plugin(force=True)

        self.remove_memory()
        self.glob_hda(dev_mode)

        for _h in self.maya_hda:
            _h = _h.replace(os.sep, '/')

            _asset_names = ""
            try:
                _asset_names = cmds.houdiniAsset(listAssets=_h)
            except Exception as e:
                _error.append(_h)
                print(e)

            if _asset_names:
                for _asset_name in _asset_names:
                    if _text:
                        if _text in _asset_name:
                            _hda_data = HDAData(_asset_name, _h)
                            self.nodename_filename.append(_hda_data)
                    else:
                        _hda_data = HDAData(_asset_name, _h)
                        self.nodename_filename.append(_hda_data)

        self._create_buttons()
        # self._reload_houdini_asset()

    def _remove_buttons(self):
        if self._buttons:
            for x in self._buttons:
                try:
                    cmds.deleteUI(x)
                except BaseException:
                    pass
            self._buttons = []

    def _create_buttons(self):
        _message = u"コンフルページがあれば、中ボタンクリックで解説ページを開きます"
        if self.nodename_filename:
            self._remove_buttons()
            for hda in self.nodename_filename:

                _btn = cmds.button(hda.btn_name,
                                   label=hda.short_name,
                                   width=self._window_width - 20,
                                   command=partial(self.command, hda),
                                   statusBarMessage=u"[ {} ]  {}".format(hda.name, _message),
                                   annotation=u"[ {} ]\n{}".format(hda.name, _message),
                                   dragCallback=partial(self._help, hda),
                                   parent=self._scroll_layout_name)
                self._buttons.append(_btn)

    def _help(self, *args):
        _path = args[0].path
        _web_site = None
        if os.path.exists(_path):
            with codecs.open(_path, "rb") as f:
                _flag = False
                for x in f.readlines():
                    if str("HelpSite") in x:
                        _flag = True
                    if _flag and str("default") in x:
                        _web_site = x.split()
                        if len(_web_site) > 2:
                            _web_site = _web_site[2]
                            break
        if _web_site:
            try:
                webbrowser.open(_web_site)
            except Exception as e:
                print("error--- ", e)

    def port_open(self, *args):
        _open_port = '{}:{}'.format(HOST, PORT)
        _port_list = cmds.commandPort(listPorts=True, q=True)

        if _open_port not in _port_list:

            try:
                cmds.commandPort(name=_open_port, sourceType="python", echoOutput=True, bufferSize=4096)
            except Exception as e:
                # logger.send_crash('{}-Crash-{}'.format(tool_title, e))
                print(_port_list)
                cmds.error("!!---can not open port---  {}".format(e))

        print('{:-^100}'.format('Open Oprt List'))
        print(cmds.commandPort(listPorts=True, q=True))

    def _bake_asset(self, *args):
        selections = cmds.ls(sl=True, type="houdiniAsset")
        if not selections:
            return

        for selection in selections:
            self.bake_asset(selection)

    def bake_asset(self, _hda):
        # maya.mel.eval('houdiniEngine_bakeAsset Faceweightedvertexnormals1;')
        maya.mel.eval('houdiniEngine_bakeAsset {};'.format(_hda))

    def command(self, hda=None, *args):
        if not hda:
            return

        sel = cmds.ls(orderedSelection=True)

        if not sel:
            return

        # self.port_open()

        _test_baker_flag = False
        if "test_baker" in hda.name:
            _test_baker_flag = True

        _atlus_texture_flag = False
        if "atlus_texture_maker" in hda.name:
            _atlus_texture_flag = True
            _atlus_name = 'atlus.tga'
            scene_name = getCurrentSceneFilePath()
            # _bake_export_path = 'D:/ando/Maya/atlus_test/bake/atuls.tga'
            _bake_export_path = os.path.split(scene_name)[0]
            _bake_export_path = os.path.join(_bake_export_path, _atlus_name).replace(os.sep, '/')

        _leaf_flag = False
        if "leaf_maker" in hda.name or "alpha_to_geometory" in hda.name:
            _leaf_flag = True
            fileNodes = []

        _boolean_flag = False
        if "boolean" in hda.name:
            _boolean_flag = True

        _mesh_tilre_flag = False
        if "mesh_tiler" in hda.name:
            _mesh_tilre_flag = True

        _uv_unwarp_flag = False
        if "uv_unwarp" in hda.name:
            _uv_unwarp_flag = True

        _gronund_collision_flag = False
        if "create_ground_collision" in hda.name:
            _gronund_collision_flag = True

        if _boolean_flag or _test_baker_flag:
            _first_sel = sel.pop(0)
            mel_string = '{{ {} }}'.format('"{}"'.format(_first_sel))
            mel_string_array = '{{ {} }}'.format(', '.join(['"{}"'.format(s) for s in sel]))
        elif _leaf_flag:
            meshs = [x for x in cmds.listRelatives(sel[0],
                                                   allDescendents=True, fullPath=True, type="mesh")
                     if not cmds.getAttr("{}.intermediateObject".format(x))]
            _shading_engines = cmds.listConnections(meshs[0], s=False, d=True, type='shadingEngine')

            # mat = cmds.ls(cmds.listConnections(_shading_engines, s=True, d=False), mat=True)
            fileNodes = cmds.ls(cmds.listHistory(cmds.ls(cmds.listConnections(_shading_engines, s=True, d=False), mat=True)), type='file')
            if fileNodes:
                fileNodes = fileNodes[0]
            mel_string = '{{ {} }}'.format('"{}"'.format(sel[0]))
        elif _mesh_tilre_flag:
            _end_sel = sel.pop(-1)
            mel_string = '{{ {} }}'.format('"{}"'.format(_end_sel))
            mel_string_array = '{{ {} }}'.format(', '.join(['"{}"'.format(s) for s in sel]))
        else:
            mel_string_array = '{{ {} }}'.format(', '.join(['"{}"'.format(s) for s in sel]))

        _hda = cmds.houdiniAsset(loadAsset=[hda.path, hda.name])

        if _uv_unwarp_flag:
            _houdini_input = cmds.listConnections(_hda, d=False, t="houdiniInputGeometry")
            _houdini_input = _houdini_input[0]
            edges = cmds.filterExpand(sel, sm=32, ex=True)
            edges = [x.rsplit(".", 1)[-1] for x in edges]
            cmds.setAttr("{}.inputComponents".format(_houdini_input), len(edges), edges, type="componentList")
            # setAttr -type "string" houdiniInputGeometry1.primComponentGroup "uv_seam";

        # _hda = maya.mel.eval('houdiniEngine_loadAsset "{}" "{}";'.format(hda.path, hda.name))

        print(hda.path, hda.name, "  ----hda.path, hda.name")
        print(_hda, " -----houdiniEngine_loadAsset")
        # logger.info("{} - load hda".format(hda.name))
        # print(_hda,"--_hda")
        # cmds.select(faces, r=True)
        try:
            if _boolean_flag or _test_baker_flag:
                maya.mel.eval("houdiniEngine_setAssetInput {} {}".format(_hda + ".input[0].inputNodeId", mel_string))
                maya.mel.eval("houdiniEngine_setAssetInput {} {}".format(_hda + ".input[1].inputNodeId", mel_string_array))
            elif _leaf_flag:
                maya.mel.eval("houdiniEngine_setAssetInput {} {}".format(_hda + ".input[0].inputNodeId", mel_string))
                if fileNodes:
                    cmds.setAttr("{}.houdiniAssetParm.houdiniAssetParm_input_image".format(_hda),
                                 "{}".format(cmds.getAttr("{}.ftn".format(fileNodes))), type="string")
                try:
                    cmds.sets(_hda, e=True, forceElement=_shading_engines[0])
                except Exception as e:
                    print("!! can not connection --- {}".format(e))
            elif _mesh_tilre_flag:
                maya.mel.eval("houdiniEngine_setAssetInput {} {}".format(
                    _hda + ".input[1].inputNodeId", mel_string))
                maya.mel.eval("houdiniEngine_setAssetInput {} {}".format(
                    _hda + ".input[0].inputNodeId", mel_string_array))

            else:
                maya.mel.eval("houdiniEngine_setAssetInput {} {}".format(
                    _hda + ".input[0].inputNodeId", mel_string_array))

            if _atlus_texture_flag:
                shadingTextures = ShaderTexture(_hda, sel)
                print(shadingTextures.get_textures(), "  --------------shadingTextures")
                cmds.setAttr('{}.houdiniAssetParm.houdiniAssetParm_file_path'.format(_hda),
                             _bake_export_path, type='string')

                for x in cmds.lsUI(type="button", long=True):
                    if (x.startswith("AttributeEditor")
                            and "Get Textures" == cmds.button(x, q=True, label=True)):

                        cmds.scriptJob(
                            attributeChange=[
                                "{}.houdiniAssetParm.houdiniAssetParm_get_textures__button".format(_hda),
                                partial(shadingTextures.get_textures)],
                            protected=False,
                            killWithScene=True,
                            parent=x.split("|")[-2])

                        shadingTextures.get_textures()
                        # cmds.button(x, e=True, c=partial(shadingTextures.get_textures))
                        break

            if _gronund_collision_flag:

                set_colorset_display(_hda)

                cmds.scriptJob(
                    attributeChange=[
                        "{}.houdiniAssetParm_show_mask".format(_hda),
                        partial(set_colorset_display, _hda)],
                    replacePrevious=True,
                    protected=False,
                    killWithScene=True,
                    parent=NAME)
            else:
                set_colorset_no_display(_hda)

        except Exception as e:
            print("error--- ", e)

        # try:
        #     maya.mel.eval('houdiniEngine_setAssetInput({}.input[0].inputNodeId, {})'.format(_hda, ",".join(faces)))
        # except:pass
        cmds.select(_hda, r=True)
        # self.bake_asset(_hda)

    def _check_option_var(self):
        _type = cmds.optionVar(q=list(self._SessionType.keys())[0])
        _session = cmds.optionVar(q=list(self._SessionPipeCustom.keys())[0])
        _pipe = cmds.optionVar(q=list(self._ThriftPipe.keys())[0])

        _type_default = list(self._SessionType.values())[0]
        _session_default = list(self._SessionPipeCustom.values())[0]
        _pipe_default = list(self._ThriftPipe.values())[0]

        print("{:-<36} idDefault [{}]".format(list(self._SessionType.keys())[0], _type == list(self._SessionType.values())[0]))
        print("{:-<36} idDefault [{}]".format(list(self._SessionPipeCustom.keys())[0], _session == list(self._SessionPipeCustom.values())[0]))
        print("{:-<36} idDefault [{}]".format(list(self._ThriftPipe.keys())[0], _pipe == list(self._ThriftPipe.values())[0]))

        if _type != _type_default:
            return list(self._SessionType.keys())[0]
        elif _session != _session_default:
            return list(self._SessionPipeCustom.keys())[0]
        elif _pipe != _pipe_default:
            return list(self._ThriftPipe.keys())[0]
        else:
            return

    def _set_option_var(self):
        cmds.optionVar(iv=[list(self._SessionType.keys())[0], list(self._SessionType.values())[0]])

        cmds.optionVar(iv=[list(self._SessionPipeCustom.keys())[0], list(self._SessionPipeCustom.values())[0]])

        cmds.optionVar(sv=[list(self._ThriftPipe.keys())[0], list(self._ThriftPipe.values())[0]])

    def _check_plugin(self):
        self.houdini_engine_path = ""
        _houdini_engine_plugin_path = os.path.join(PLUGIN_PATH,
                                                   self.HOUDINI_ENGINE_NAME + self.PLUGIN_EXT).replace(os.sep, '/')

        if not os.path.exists(_houdini_engine_plugin_path):
            return False
        else:
            self.houdini_engine_path = _houdini_engine_plugin_path
            return True

    def set_active_z_drive_plugin(self):
        _load_flag = True
        if self.HOUDINI_ENGINE_NAME in cmds.pluginInfo(query=True, listPlugins=True):
            _plugin_path = cmds.pluginInfo(self.HOUDINI_ENGINE_NAME, q=True, path=True).replace(os.sep, '/')

            if _plugin_path != self.houdini_engine_path:
                cmds.unloadPlugin(self.HOUDINI_ENGINE_NAME, force=True)
                _load_flag = False
        else:
            _load_flag = False

        if not _load_flag:
            try:
                cmds.loadPlugin(self.houdini_engine_path, qt=True)
                cmds.pluginInfo(self.houdini_engine_path, edit=True, autoload=True)
            except Exception as e:
                # logger.send_crash('{}-Crash-{}'.format(tool_title, e))
                print("error--- ", e)
                return False

        if self.HOUDINI_ENGINE_NAME not in cmds.pluginInfo(query=True, listPlugins=True):
            return False
        else:
            return True


def main():

    hda_loder = HDALoader()
    hda_loder.create()
