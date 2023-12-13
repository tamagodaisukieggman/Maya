# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial
import itertools

import maya.cmds as cmds
import maya.mel


def __loadCyPolyNormalPerVertex():
        u"""プラグイン「CyPolyNormalPerVertex」をロード"""
        plugin_name = 'cypolynormal.py'
        if not(cmds.pluginInfo(plugin_name, q=True, l=True)):
            try:
                cmds.loadPlugin(plugin_name)
                return True
            except:
                cmds.warning(u'プラグインのロードに失敗しました: {0}'.format(plugin_name))
                return False
        return True


def get_poly_comp(flag = "vtx"):
    node = None

    flags = ["vtx","edge","face","uv","vtxFace"]
    sm = [31,32,34,35,70]
    kwArgs = ["tv","te","tf","tuv","tvf"]

    if flag not in flags:
        return -1

    sel = cmds.ls(selection=True)
    kw = {x:{y:1} for x,y in zip(flags,kwArgs)}
    smKW = dict(zip(flags,sm))

    comp = None
    comp = cmds.filterExpand(cmds.polyListComponentConversion(sel,**kw[flag]),
                            selectionMask=smKW[flag],
                            expand=True)

    if comp:
        node = list(set([x.split(".",1)[0] for x in comp]))

    return node,comp

def seach_mesh_node(_nodes):
    _mesh_type_flag = False
    for _obj in _nodes:
        if cmds.listRelatives(_obj, type="mesh"):
            _mesh_type_flag = True

    return _mesh_type_flag

def smooth_normal(*args):
    select_obj = cmds.ls(selection=True)
    if not select_obj:
        return
    # print(select_obj,"-----------")
    # print(seach_mesh_node(select_obj))
    # if not seach_mesh_node(select_obj):
    #     return

    vertexs = []

    # _face_flag = select_obj[0].split(".")

    # if _face_flag and _face_flag[-1][0] == "f":
    #     vertexs.extend(cmds.filterExpand(cmds.polyListComponentConversion(
    #                                 select_obj,
    #                                 toVertexFace=True),
    #                                 selectionMask=70,
    #                                 expand=True))
    # else:

    vertexs.extend(cmds.filterExpand(cmds.polyListComponentConversion(
                                select_obj,
                                toVertex=True),
                                selectionMask=31,
                                expand=True))
    if not vertexs:
        return


    _num = len(vertexs)
    if _num == 1:
        _num = 2

    if _num > 5000:
        gMainProgressBar = maya.mel.eval( '$tmp = $gMainProgressBar' )
        cmds.progressBar( gMainProgressBar,
                            edit=True,
                            beginProgress=True,
                            isInterruptable=True,
                            status='Smooth Normal...',
                            maxValue=_num)

        cmds.undoInfo(stateWithoutFlush=False)

    for vtx in vertexs:
        _around_vtx_normals = []
        [_around_vtx_normals.append(cmds.polyNormalPerVertex(x,q=True, xyz=True)[0:3])
            for x in cmds.ls(cmds.polyListComponentConversion(
                        cmds.polyListComponentConversion(vtx,
                            tf=True),tv=True),fl=True)]

        _vtx_normals_zip = zip(*_around_vtx_normals)
        cmds.polyNormalPerVertex(vtx,
                xyz= [sum(_vtx_normals_zip[0])/len(_vtx_normals_zip[0]),
                sum(_vtx_normals_zip[1])/len(_vtx_normals_zip[1]),
                sum(_vtx_normals_zip[2])/len(_vtx_normals_zip[2])])
        if _num > 5000:
            cmds.progressBar( gMainProgressBar, edit=True, step=1 )

            if cmds.progressBar(gMainProgressBar, q=True, isCancelled=True):
                cmds.undoInfo(stateWithoutFlush=True)
                break

    if _num > 5000:
        cmds.progressBar( gMainProgressBar, edit=True, endProgress=True )

        cmds.undoInfo(stateWithoutFlush=True)

    for _o in select_obj:
        try:
            cmds.setAttr("{}.displayNormal".format(_o),1)
            cmds.setAttr("{}.normalType".format(_o),2)
        except:pass


def spherical_normal(bb_center=[0.0, 0.0, 0.0]):
    select_obj = cmds.ls(selection=True)
    if not select_obj:
        return

    if not seach_mesh_node(select_obj):
        return
    # exactWorldBoundingBox だと単体の場合正確な値が取れなかった
    # # 戻り値	xmin、ymin、zmin、xmax、ymax、zmax
    # bb_size = cmds.exactWorldBoundingBox(_obj, calculateExactly=True)

    # if _center == "center":
    #     bb_center = [(bb_size[0] + bb_size[3]) / 2,
    #                     (bb_size[1] + bb_size[4]) / 2,
    #                     ((bb_size[2] + bb_size[5]) / 2) + _center_offset]

    # elif _center == "bottom":
    #     bb_center = [(bb_size[0] + bb_size[3]) / 2,
    #                     bb_size[1],
    #                     ((bb_size[2] + bb_size[5]) / 2) + _center_offset]


    # 戻り値  ((xmin,xmax),(ymin,ymax),(zmin,zmax))
    # bb_size = cmds.polyEvaluate(boundingBox=True)

    # if _center == "center":
    #     bb_center = [(bb_size[0][0] + bb_size[0][1]) / 2 + _center_offset[0],
    #                     (bb_size[1][0] + bb_size[1][1]) / 2 + _center_offset[1],
    #                     ((bb_size[2][0] + bb_size[2][1]) / 2) + _center_offset[2]]

    # elif _center == "bottom":
    #     bb_center = [(bb_size[0][0] + bb_size[0][1]) / 2 + _center_offset[0],
    #                     (bb_size[1][0] + bb_size[1][1]) / 2 + _center_offset[1],
    #                     ((bb_size[2][0] + bb_size[2][1]) / 2) + _center_offset[2]]


    vertexs = []
    vertexs.extend(cmds.filterExpand(cmds.polyListComponentConversion(
                                select_obj,
                                toVertex=True),
                                selectionMask=31,
                                expand=True))
    if not vertexs:
        return

    cmds.makeIdentity(apply=True,
                    translate=True,
                    rotate=True,
                    scale=True,
                    normal=True,
                    preserveNormals=True)

    cmds.delete(constructionHistory=True)

    _num = len(vertexs)
    if _num == 1:
        _num = 2

    if _num > 5000:
        gMainProgressBar = maya.mel.eval( '$tmp = $gMainProgressBar' )
        cmds.progressBar( gMainProgressBar,
                            edit=True,
                            beginProgress=True,
                            isInterruptable=True,
                            status='Spherical Normal...',
                            maxValue=_num)

        cmds.undoInfo(stateWithoutFlush=False)

    for vtx in vertexs:
        _point_position = cmds.pointPosition(vtx, world=True)

        # cmds.CyPolyNormalPerVertex(vtx, xyz= [x-y for (x,y) in zip(_point_position, bb_center)], ws=True)
        cmds.polyNormalPerVertex(vtx, xyz= [x-y for (x,y) in zip(_point_position, bb_center)])
        if _num > 5000:
            cmds.progressBar( gMainProgressBar, edit=True, step=1 )

            if cmds.progressBar(gMainProgressBar, q=True, isCancelled=True):
                cmds.undoInfo(stateWithoutFlush=True)
                break

    if _num > 5000:
        cmds.progressBar( gMainProgressBar, edit=True, endProgress=True )

        cmds.undoInfo(stateWithoutFlush=True)

    for _o in cmds.ls(selection=True, objectsOnly=True):
        try:
            cmds.setAttr("{}.displayNormal".format(_o),1)
            cmds.setAttr("{}.normalType".format(_o),2)
        except:pass


def toggle_normal_display(*args):
    _selection = cmds.ls(hilite=True)
    if not _selection:
        _selection = cmds.ls(selection=True, objectsOnly=True)

    if not _selection:
        return

    try:
        _flag = cmds.getAttr("{}.displayNormal".format(_selection[0]))
        [[cmds.setAttr("{}.displayNormal".format(x),not _flag),
            cmds.setAttr("{}.normalType".format(x),2)] for x in _selection]
    except:pass

class EditNormal(object):
    def __init__(self):
        self.TITLE = u"Edit Normal Tool"
        self.NAME = u"normal_editing_tool_ui"
        self._window_width = 300
        self._window_height = 135

        self._locator_name = "_mtku_normal_edit_center_locator"

        self._float_slider_x_name = "_normal_edit_float_slider_x"
        self._float_slider_y_name = "_normal_edit_float_slider_y"
        self._float_slider_z_name = "_normal_edit_float_slider_z"

        self._spherical_normal_btn_name = "_normal_edit_btnA"
        self._normal_copy_btn_name = "_normal_edit_btnB"
        self._normal_paste_btn_name = "_normal_edit_btnC"
        self._value_reset_btn_name = "_normal_edit_btnD"

        self._bottom_center_btn_name = "_normal_edit_btnE"
        self._smooth_normal_btn_name = "_normal_edit_btnF"

        self._normal_values = []
        self._center_locator = ""


    def create(self):
        try:
            cmds.deleteUI(self.NAME)
        except:pass

        # self._check_locator()

        _separator_height = 10
        _min_value = -5.0
        _max_value = 5.0

        cmds.window(self.NAME,
                    title=self.TITLE,
                    width=self._window_width +2 ,
                    height=self._window_height + 2,
                    closeCommand=partial(self._delete_locator))


        cmds.columnLayout(adjustableColumn=True, width = self._window_width, height=self._window_height)


        # cmds.text(label=u"中心点の変更", backgroundColor=[0.1, 0.1, 0.1], height=20)


        # cmds.attrFieldSliderGrp(self._float_slider_x_name,
        #                         label="Center X",
        #                         min=_min_value, max=_max_value,
        #                         fieldMaxValue = 10000,
        #                         fieldMinValue = -10000,
        #                         columnAlign3=["center", "left", "left"],
        #                         columnWidth3=[50,80,150],
        #                         backgroundColor=[0.3, 0.1, 0.1],
        #                         height=30)

        # cmds.attrFieldSliderGrp(self._float_slider_y_name,
        #                         label="Center Y",
        #                         min=_min_value, max=_max_value,
        #                         fieldMaxValue = 10000,
        #                         fieldMinValue = -10000,
        #                         columnAlign3=["center", "left", "left"],
        #                         columnWidth3=[50,80,150],
        #                         backgroundColor=[0.1, 0.3, 0.1],
        #                         height=30)

        # cmds.attrFieldSliderGrp(self._float_slider_z_name,
        #                         label="Center Z",
        #                         min=_min_value, max=_max_value,
        #                         fieldMaxValue = 10000,
        #                         fieldMinValue = -10000,
        #                         columnAlign3=["center", "left", "left"],
        #                         columnWidth3=[50,80,150],
        #                         backgroundColor=[0.1, 0.1, 0.3],
        #                         height=30)

        # cmds.separator(height = _separator_height)

        # cmds.rowLayout(adjustableColumn=1,
        #                 numberOfColumns=2,
        #                 columnWidth2=[self._window_width / 2,
        #                                 self._window_width / 2],
        #                 width=self._window_width)
        # cmds.button(self._value_reset_btn_name,
        #             label=u"現在の選択中心に移動",
        #             width=self._window_width / 2 - 5,
        #             command=partial(self._value_reset))

        # cmds.button(self._bottom_center_btn_name,
        #             label=u"現在の選択の中心底辺に移動",
        #             width=self._window_width / 2 - 5,
        #             command=partial(self._value_bottom))
        # cmds.setParent("..")


        # cmds.separator(height = _separator_height)

        # cmds.button(self._spherical_normal_btn_name,
        #             label=u"Normal 球状化実行",
        #             width=self._window_width,
        #             backgroundColor=[0.3, 0.2, 0.2],
        #             command=partial(self._spherical_normal))

        cmds.text(label=u"法線のスムーズ", backgroundColor=[0.1, 0.1, 0.1], height=20)
        cmds.button(self._smooth_normal_btn_name,
                    label=u"選択範囲の法線スムーズ",
                    command=partial(smooth_normal))

        cmds.text(label=u"法線のコピーペースト", backgroundColor=[0.1, 0.1, 0.1], height=20)


        cmds.rowLayout(adjustableColumn=1,
                        numberOfColumns=2,
                        columnWidth2=[self._window_width / 2,
                                        self._window_width / 2],
                        width=self._window_width)

        cmds.button(self._normal_copy_btn_name,
                    label=u"法線 コピー",
                    width=self._window_width / 2 - 5,
                    command=partial(self._copy_normal_value))

        cmds.button(self._normal_paste_btn_name,
                    label=u"法線 ペースト",
                    width=self._window_width / 2 - 5,
                    command=partial(self._paste_normal_value))

        cmds.setParent("..")

        cmds.text(label=u"法線の表示", backgroundColor=[0.1, 0.1, 0.1], height=20)
        cmds.button(label=u"選択の法線表示トグル", command=partial(toggle_normal_display))

        cmds.setParent("..")

        cmds.showWindow(self.NAME)

        # self._value_reset()

        # cmds.scriptJob(parent=self.NAME, event=["SelectionChanged", partial(self._get_center)])
        # cmds.scriptJob(parent=self.NAME, event=["SceneOpened", partial(self._delete_locator)])

    def _hide_locator(self, *args):
        _locator = cmds.ls("*{}*".format(self._locator_name))
        if _locator:
            _result = []
            for _loc in _locator:
                cmds.hide(_loc)

    def _delete_locator(self, *args):
        _locator = cmds.ls("*{}*".format(self._locator_name))
        if _locator:
            # _result = []
            for _loc in _locator:
                try:
                    cmds.delete(_loc)
                except:
                    # _result.append(_loc)
                    pass
            # if _result:
            #     print("[ {} ] can not delete!!".format(", ".join(_result)))

    def _create_center_locator(self, *args):
        _sel = cmds.ls(orderedSelection=True)
        # _hilite = cmds.ls(hilite=True)

        self._center_locator = cmds.createNode("transform",
                                name=self._locator_name, skipSelect=True)

        _locator_shape = cmds.createNode("locator",
                                name="{}Shape".format(self._locator_name),
                                skipSelect=True, parent=self._center_locator)

        cmds.setAttr("{}.overrideEnabled".format(_locator_shape), True)
        cmds.setAttr("{}.overrideColor".format(_locator_shape), 9)



        # if _hilite:
        #     cmds.hilite(_hilite)


    def _check_locator(self, *args):
        if cmds.objExists(self._locator_name):
            self._center_locator = self._locator_name
        else:
            self._create_center_locator()


    def _get_center(self, *args):
        self.bb_bottom = 0.0
        self.bb_size = []
        self.bb_center = [0.0, 0.0, 0.0]

        _obj = cmds.ls(selection=True)

        if not _obj:
            return


        bb_size = cmds.polyEvaluate(boundingBoxComponent=True)

        _bb_not_polygonal_flag = False

        # float[]	xmin、ymin、zmin、xmax、ymax、zmax
        if bb_size == "Nothing counted : no polygonal object is selected.":
            bb_size = cmds.exactWorldBoundingBox(_obj)
            _bb_not_polygonal_flag = True

        # ((xmin,xmax),(ymin,ymax),(zmin,zmax))
        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            bb_size = cmds.polyEvaluate(boundingBox=True)


        if _bb_not_polygonal_flag:
            bb_center = [(bb_size[0] + bb_size[3]) / 2,
                        (bb_size[1] + bb_size[4]) / 2,
                        (bb_size[2] + bb_size[5]) / 2]
            self.bb_bottom = bb_size[1]

        else:
            bb_center = [(bb_size[0][0] + bb_size[0][1]) / 2,
                    (bb_size[1][0] + bb_size[1][1]) / 2,
                    ((bb_size[2][0] + bb_size[2][1]) / 2)]
            self.bb_bottom = bb_size[1][0]


        self.bb_size = bb_size
        self.bb_center = bb_center

        # _bb_flatten = list(itertools.chain.from_iterable(bb_size))
        # _max_value = abs(max(_bb_flatten))
        # _min_value = abs(min(_bb_flatten))
        # if _min_value >= _max_value:
        #     _max_value = _min_value

        # cmds.move(self.bb_center[0], self.bb_center[1], self.bb_center[2], self._center_locator, absolute=True)

        if self._center_locator:
            cmds.attrFieldSliderGrp(self._float_slider_x_name,
                                    edit=True,
                                    # min=-_max_value,
                                    # max=_max_value,
                                    attribute="{}.tx".format(self._center_locator))

            cmds.attrFieldSliderGrp(self._float_slider_y_name,
                                    edit=True,
                                    # min=-_max_value,
                                    # max=_max_value,
                                    attribute="{}.ty".format(self._center_locator))

            cmds.attrFieldSliderGrp(self._float_slider_z_name,
                                    edit=True,
                                    # min=-_max_value,
                                    # max=_max_value,
                                    attribute="{}.tz".format(self._center_locator))


    def _value_bottom(self, *args):
        self._check_locator()
        if self._center_locator:
            self._get_center()
            cmds.setAttr("{}.t".format(self._locator_name), self.bb_center[0],self.bb_bottom,self.bb_center[2])


    def _value_reset(self, *args):
        self._check_locator()
        if self._center_locator:
            self._get_center()
            cmds.setAttr("{}.t".format(self._locator_name), *self.bb_center)


    def _copy_normal_value(self, *args):
        _selection = cmds.ls(selection=True)
        if not _selection:
            return
        self._normal_values = []
        vertexs = cmds.filterExpand(cmds.polyListComponentConversion(
                                _selection,
                                toVertex=True),
                                selectionMask=31,
                                expand=True)

        self._normal_values.extend([cmds.polyNormalPerVertex(x,q=True, xyz=True)[:3] for x in vertexs])

    # def _paste_normal_value_pymel(self, *args):
    #     if not self._normal_values:
    #         return

    #     _selection = pm.ls(selection=True, type=pm.nt.Transform)
    #     if not _selection:
    #         return
    #     for _obj in _selection:
    #         _vtxs = _obj.vtx
    #         _rot = _obj.r.get()
    #         for _normal_value,_vtx in zip(self._normal_values,_vtxs):
    #             _val = pm.dt.Vector(_normal_value)
    #             # print(_val.rotateBy(_rot))
    #             pm.polyNormalPerVertex(_vtx, xyz= _val)

    def _paste_normal_value(self, *args):
        if not self._normal_values:
            return

        _selection = cmds.ls(selection=True)
        if not _selection:
            return

        for _obj in _selection:
            _vtxs = cmds.filterExpand(cmds.polyListComponentConversion(
                                _obj,
                                toVertex=True),
                                selectionMask=31,
                                expand=True)

            for _normal_value,_vtx in zip(self._normal_values,_vtxs):
                cmds.polyNormalPerVertex(_vtx, xyz= _normal_value)

        for _obj in _selection:
            try:
                cmds.setAttr("{}.displayNormal".format(_obj),1)
                cmds.setAttr("{}.normalType".format(_obj),2)
            except:pass

    def _transfer_attibute(self, *args):
        _selection = cmds.ls(orderedSelection=True, type="transform")

        if not _selection:
            return

        _base = _selection[0]
        for _mesh in _selection[1:]:
            cmds.transferAttributes(_base,
                                    _mesh,
                                    sampleSpace=3,
                                    sourceUvSpace="map1",
                                    targetUvSpace="map1",
                                    transferPositions=0,
                                    transferUVs=0,
                                    transferNormals=1,
                                    transferColors=0,
                                    searchMethod=3,
                                    flipUVs=0,
                                    colorBorders=1)


    def _spherical_normal(self, *args):
        self._check_locator()
        _values = cmds.getAttr("{}.t".format(self._center_locator))[0]
        spherical_normal(_values)


def main():
    # stat = __loadCyPolyNormalPerVertex()
    # if stat:
    proc = EditNormal()
    proc.create()

# main()
# import mtku.maya.menus.modeling.edit_normal as edit_normal
# reload(edit_normal)
# edit_normal.main()