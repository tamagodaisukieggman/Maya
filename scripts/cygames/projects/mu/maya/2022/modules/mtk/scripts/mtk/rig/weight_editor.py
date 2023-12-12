# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from functools import partial
import math

import maya.cmds as cmds
import maya.mel

import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2anim


def get_skincluster(mesh_node):

    _history = cmds.listHistory(mesh_node, pruneDagObjects=True)

    if not _history:
        return None
    _skin_cluster = cmds.ls(_history, type="skinCluster")

    if _skin_cluster:
        return _skin_cluster[0]
    else:
        return None

class WeigtEditor(object):
    def __init__(self) :

        self._joint_weight_dict_vtx_list = []

        self.joints_list_memory = []
        self.weights_list_memory = []
        self._joints_id_memory = []

        self._slider_step = 3
        self._default_decimal_point_length = 10
        self._threshold_range = 0.2
        self._threshold_value = 0.4

        self.joint_short_name_dict = dict()

        self._slider_default_value = 10.0**-self._slider_step
        self._slider_min_value = 10.0** - (self._slider_step + self._slider_step)

        self.WINDOW = "_weight_editorUI"
        self.TITLE = "Weight Editor"
        self._scroll_layout_name = "{}_scroll_layout".format(self.WINDOW)
        self._all_row_colum_layout_name = "{}_all_row_colum_layout".format(self.WINDOW)

        self._joint_list_text_scroll_list_name = "{}_joint_list_text_scroll_list".format(self.WINDOW)
        self._weight_list_text_scroll_list_name = "{}_weight_list_text_scroll_list".format(self.WINDOW)
        self._lock_list_text_scroll_list_name = "{}_lock_list_text_scroll_list".format(self.WINDOW)

        self._only_select_joint_check_box_name = "{}_range_influence_check_box".format(self.WINDOW)
        self._high_low_check_box_name = "{}_high_low_check_box".format(self.WINDOW)
        self._joint_search_text_box_name = "{}_joint_search_text_box".format(self.WINDOW)

        self._weight_lock_btn_name = "{}_lock_btn".format(self.WINDOW)
        self._weight_lock_toggle_btn_name = "{}_toggle_weight_lock_btn".format(self.WINDOW)
        self._weight_unlock_btn_name = "{}_weight_unlock_btn".format(self.WINDOW)

        self._weight_round_btn_name = "{}_weight_round_btn".format(self.WINDOW)
        self._weight_influence_int_field_name = "{}_weight_influence_int_field".format(self.WINDOW)
        self._goto_paint_mode_btn_name = "{}_goto_paint_mode_btn".format(self.WINDOW)
        self._apply_weight_paint_btn_name = "{}_apply_weight_paint_btn".format(self.WINDOW)

        self._paint_opacity_float_field_name = "{}_paint_opacity_float_field".format(self.WINDOW)
        self._paint_value_float_field_name = "{}_paint_value_float_field".format(self.WINDOW)
        self._paint_mode_radio_btn_name = "{}_paint_mode_radio_btn".format(self.WINDOW)
        self._paint_modes = {1:"Smooth", 2:"Replace", 3:"Scale"}

        self._select_value_float_field_name = "{}_select_value_float_field".format(self.WINDOW)
        # self._select_less_btn_name = "{}_select_less_btn".format(self.WINDOW)
        self._select_near_btn_name = "{}_select_near_btn".format(self.WINDOW)
        self._select_more_btn_name = "{}_select_more_btn".format(self.WINDOW)
        self._select_invert_btn_name = "{}_select_invert_btn".format(self.WINDOW)
        self._deselect_btn_name = "{}_deselect_btn".format(self.WINDOW)

        self._absolute_relative_change_radio_btn_name = "{}_absolute_relative_change_radio_btn".format(self.WINDOW)
        self._slider_step_float_field_name = "{}_slider_step_float_field".format(self.WINDOW)
        self._slider_value_float_field_name = "{}_slider_value_float_field".format(self.WINDOW)
        self._int_slider_name = "{}_int_slider".format(self.WINDOW)

        self._point_one_btn_name = "{}_point_one_btn".format(self.WINDOW)
        self._point_two_five_btn_name = "{}_point_two_five_btn".format(self.WINDOW)
        self._point_five_btn_name = "{}_point_five_btn".format(self.WINDOW)
        self._point_seven_five_btn_name = "{}_point_seven_five_btn".format(self.WINDOW)
        self._point_nine_btn_name = "{}_point_nine_btn".format(self.WINDOW)
        self._one_btn_name = "{}_one_btn".format(self.WINDOW)
        self._value_set_minus_btn_name = "{}_value_set_minus_btn".format(self.WINDOW)
        self._value_set_plus_btn_name = "{}_value_set_plus_btn".format(self.WINDOW)

        self._name_original_textfield_name = "{}_name_original_textfield".format(self.WINDOW)
        self._name_change_textfield_name = "{}_name_change_textfield".format(self.WINDOW)

        self._clear_btn_name = "{}_clear_btn".format(self.WINDOW)
        self._copy_btn_name = "{}_copy_btn".format(self.WINDOW)
        self._paste_btn_name = "{}_paste_btn".format(self.WINDOW)

        self._vtx_length_text_name = "{}_vtx_length_text".format(self.WINDOW)

        self._surface_association_option_menu_name = "{}_surface_association_option_menu".format(self.WINDOW)
        self._surface_association_option_menus = ["closestPoint", "rayCast", "closestComponent"]
        self._influence_association_option_menu_name = "{}_influence_association_option_menu".format(self.WINDOW)
        self._influence_association_option_menus = ["oneToOne", "closestJoint", "label"]

        self._mirror_copy_btn_name = "{}_mirror_copy_btn".format(self.WINDOW)

        self._close_btn_name = "{}_close_btn".format(self.WINDOW)


    def create(self):
        try:
            cmds.deleteUI(self.WINDOW)
        except: pass

        cmds.window(self.WINDOW, title=self.TITLE, width=350, maximizeButton=False, titleBarMenu=False)
        cmds.frameLayout(marginHeight=4, marginWidth=6, labelVisible=False)
        scroll_layout = cmds.scrollLayout(self._scroll_layout_name, height=400)
        cmds.setParent('..')
        out_colums = cmds.columnLayout(adjustableColumn=True)
        cmds.setParent(scroll_layout)
        cmds.frameLayout(marginHeight=0, marginWidth=10, labelVisible=False)
        cmds.rowColumnLayout(self._all_row_colum_layout_name, numberOfRows=1, rowHeight=(1, 500))

        cmds.textScrollList(self._joint_list_text_scroll_list_name, width=240,
                            allowMultiSelection=True)
        cmds.textScrollList(self._weight_list_text_scroll_list_name, width=120,
                            allowMultiSelection=True, enable=False)
        cmds.textScrollList(self._lock_list_text_scroll_list_name, width=50,
                            allowMultiSelection=True, enable=False)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent(out_colums)
        cmds.frameLayout(marginHeight=10, marginWidth=10, labelVisible=False)
        cmds.columnLayout(adjustableColumn=True)
        cmds.rowLayout(numberOfColumns=4, adjustableColumn=3, columnWidth4=(140, 80, 100, 100))
        cmds.checkBox(self._only_select_joint_check_box_name, label=u"選択のピン止め",
                                    changeCommand=partial(self.update_window), value=False)
        # cmds.checkBox(self._high_low_check_box_name, label=u"大小文字区別なし", value=True)
        cmds.text(label=u"絞り込み文字列")
        cmds.textField(self._joint_search_text_box_name, changeCommand=partial(self.update_window))
        cmds.button(label=u"clear", command=partial(self.clear_text_field))
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnWidth3=(100, 10, 100))
        cmds.button(self._weight_lock_btn_name, label="Lock", width=130)
        cmds.button(self._weight_lock_toggle_btn_name, label="Toggle", width=10)
        cmds.button(self._weight_unlock_btn_name, label="UnLock", width=130)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=5, adjustableColumn=3, columnWidth5=(100, 30, 5, 100, 100))
        cmds.button(self._weight_round_btn_name, label="Round", width=100, backgroundColor= [0.3, 0.3, 0.3])
        cmds.intField(self._weight_influence_int_field_name, width=30, value=4)
        cmds.text(label="")
        cmds.button(self._goto_paint_mode_btn_name, label="PaintMode", width=100,
                                command=partial(self.go_to_paint_mode))
        cmds.button(self._apply_weight_paint_btn_name, label="Apply", width=100,
                                command=partial(self.paint_apply))
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=6, adjustableColumn=5, columnWidth6=(50, 42, 50, 30, 10, 100))
        cmds.floatField(self._paint_opacity_float_field_name,
                        value=1.0,
                        min=0.000,
                        max=1,
                        pre=3,
                        width=50,
                        changeCommand=partial(self.chenge_paint_opacity))
        cmds.text(label="Opacity")
        cmds.floatField(self._paint_value_float_field_name,
                        value=0.0,
                        min=0.000,
                        max=1,
                        pre=3,
                        width=50,
                        changeCommand=partial(self.change_paint_value))
        cmds.text(label="Value")
        cmds.text(label="")
        cmds.radioButtonGrp(self._paint_mode_radio_btn_name,
                        numberOfRadioButtons=3,
                        select=1,
                        label1=self._paint_modes[1],
                        label2=self._paint_modes[2],
                        label3=self._paint_modes[3],
                        width=185,
                        columnWidth3=[65, 65, 50])
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=7,
                        adjustableColumn=3,
                        columnWidth6=(50, 50, 5, 100, 100, 100))
        cmds.floatField(self._select_value_float_field_name,
                        width=50,
                        min=0,max=1,
                        value=self._threshold_value)
        cmds.text(label="Threshold")
        cmds.text(label="")
        cmds.button(self._select_near_btn_name,
                        label="SelectNear",
                        width=70)
        cmds.button(self._select_more_btn_name,
                        label="SelectMore",
                        width=70)
        cmds.button(self._select_invert_btn_name,
                        label="Invert",
                        width=70)
        cmds.button(self._deselect_btn_name,
                        label="Deselect",
                        width=70)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnWidth3=(60, 5, 100))
        cmds.text(label="Slider Step")
        cmds.text(label="")
        cmds.radioButtonGrp(self._absolute_relative_change_radio_btn_name,
                        adjustableColumn=True,
                        numberOfRadioButtons=2,
                        label1="absolute",
                        select=2,
                        label2="relative",
                        width=160)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=4, adjustableColumn=4, columnWidth4=(50, 5, 50, 100))
        cmds.floatField(self._slider_step_float_field_name,
                        value=self._slider_default_value,
                        min=self._slider_default_value,
                        max=1,
                        pre=self._slider_step,
                        width=50,
                        changeCommand=partial(self.set_step_point_length))
        cmds.text(label="")
        cmds.floatField(self._slider_value_float_field_name,
                        pre=self._slider_step,
                        width=50,
                        min=-1,
                        max=1,
                        value=0)

        cmds.intSlider(self._int_slider_name,
                        min=-100,
                        max=100,
                        value=0,
                        width=100)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, columnWidth2=(250, 130))

        cmds.rowLayout(numberOfColumns=6, adjustableColumn=6, columnWidth6=(40, 40, 40, 40, 40, 40))
        cmds.button(self._point_one_btn_name,
                    label=u".1", width=40)
        cmds.button(self._point_two_five_btn_name,
                    label=u".25", width=40)
        cmds.button(self._point_five_btn_name,
                    label=u".5", width=40)
        cmds.button(self._point_seven_five_btn_name,
                    label=u".75", width=40)
        cmds.button(self._point_nine_btn_name,
                    label=u".9", width=40)
        cmds.button(self._one_btn_name,
                    label=u"1", width=40)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=3, adjustableColumn=1, columnWidth3=(6, 80, 80))
        cmds.text(label="")
        cmds.button(self._value_set_minus_btn_name,
                label=u"-", width=80)
        cmds.button(self._value_set_plus_btn_name,
                label=u"+", width=80)
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=10, adjustableColumn=5, columnWidth6=(100, 50, 100, 50, 5, 100))
        cmds.text(label="Original")
        cmds.textField(self._name_original_textfield_name, width=50, text="")
        cmds.text(label="Change")
        cmds.textField(self._name_change_textfield_name, width=50, text="")
        cmds.text(label="")
        cmds.button(self._clear_btn_name,
                label="Clear", width=50, command=partial(self._clear_copy_text_field))
        cmds.button(self._copy_btn_name,
                label="Copy", width=50)
        cmds.button(self._paste_btn_name,
                label="Paste", width=50)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=3, adjustableColumn=3, columnWidth3=(100, 100, 5))
        cmds.text(width=110, align="left", label="MemoryVertexsData:")
        cmds.text(self._vtx_length_text_name, width=70, align="right", label="0")
        cmds.text(label="")
        cmds.setParent('..')

        # cmds.rowLayout(numberOfColumns=4, adjustableColumn=3, columnWidth4=(130, 90, 5, 50))
        # cmds.optionMenu(self._surface_association_option_menu_name, width=130)

        # for _menu in self._surface_association_option_menus:
        #     cmds.menuItem(label=_menu)

        # cmds.optionMenu(self._influence_association_option_menu_name, width=90)
        # for _menu in self._influence_association_option_menus:
        #     cmds.menuItem(label=_menu)

        # cmds.text(label="")
        # cmds.button(self._mirror_copy_btn_name, label="Mirror Copy", command=partial(self.weight_mirror_copy), width=80)

        # cmds.setParent('..')

        cmds.button(self._close_btn_name, label="CLOSE", height=24, command="maya.cmds.deleteUI('{}')".format(self.WINDOW))
        cmds.showWindow(self.WINDOW)

        cmds.scriptJob(parent=self.WINDOW, event=["SelectionChanged", partial(self.update_window)])
        cmds.scriptJob(parent=self.WINDOW, event=["Undo", partial(self.update_window)])
        cmds.scriptJob(parent=self.WINDOW, event=["Redo", partial(self.update_window)])
        cmds.showWindow(self.WINDOW)
        self.update_window()

    def _clear_copy_text_field(self, *args):
        cmds.textField(self._name_original_textfield_name, edit=True, text='')
        cmds.textField(self._name_change_textfield_name, edit=True, text='')

    def clear_text_field(self, *args):
        cmds.textField(self._joint_search_text_box_name, edit=True, text="")
        self.update_window()

    def go_to_paint_mode(self, *args) :
        paint_mode = cmds.radioButtonGrp(self._paint_mode_radio_btn_name, q=True, select=True)
        paint_opacity = cmds.floatField(self._paint_opacity_float_field_name, q=True, value=True)
        paint_value = cmds.floatField(self._paint_value_float_field_name, q=True, value=True)
        select_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)

        if not select_joints:
            return
        select_joints = [x.split()[-1] for x in select_joints]
        if cmds.currentCtx() != "artAttrSkinContext":
            maya.mel.eval('ArtPaintSkinWeightsTool;')
            maya.mel.eval('artSkinInflListChanging "{}" 1;'.format(select_joints[0]))
            maya.mel.eval('artSkinInflListChanged artAttrSkinPaintCtx;')

            current_mode = self._paint_modes[paint_mode]
            maya.mel.eval('artAttrPaintOperation artAttrSkinPaintCtx {};'.format(current_mode))

            if current_mode != "Smooth" :
                maya.mel.eval('artSkinSetSelectionValue {} false artAttrSkinPaintCtx artAttrSkin;'.format(paint_value))

            maya.mel.eval('artAttrSkinPaintCtx -e -opacity {} `currentCtx`;'.format(paint_opacity))
            maya.mel.eval('artAttrSkinPaintCtx -e -xrayJoints true `currentCtx`;')

            panel = cmds.getPanel(withFocus=True)

            if cmds.getPanel(typeOf=panel) == "modelPanel":
                cmds.modelEditor(panel, edit=True, wireframeOnShaded=True)

    def chenge_paint_opacity(self, *args):
        if cmds.currentCtx() != "artAttrSkinContext":
            return
        try:
            value = cmds.floatField(self._paint_opacity_float_field_name, q=True, value=True)
            maya.mel.eval('artAttrSkinPaintCtx -e -opacity {} `currentCtx`;'.format(value))
            self.update_window()
        except:pass

    def change_paint_value(self, *args):
        if cmds.currentCtx() != "artAttrSkinContext":
            return
        try:
            value = cmds.floatField(self._paint_value_float_field_name, q=True, value=True)
            maya.mel.eval('artSkinSetSelectionValue {} false artAttrSkinPaintCtx artAttrSkin;'.format(value))
            self.update_window()
        except:pass

    def paint_apply(self, *args):
        if cmds.currentCtx() != "artAttrSkinContext":
            return
        try:
            paint_mode = cmds.radioButtonGrp(self._paint_mode_radio_btn_name, q=True, select=True)
            paint_opacity = cmds.floatField(self._paint_opacity_float_field_name, q=True, value=True)
            paint_value = cmds.floatField(self._paint_value_float_field_name, q=True, value=True)
            current_mode = self._paint_modes[paint_mode]
            maya.mel.eval('artAttrPaintOperation artAttrSkinPaintCtx {};'.format(current_mode))
            maya.mel.eval('artSkinSetSelectionValue {} false artAttrSkinPaintCtx artAttrSkin;'.format(paint_value))
            maya.mel.eval('artAttrSkinPaintCtx -e -opacity {} `currentCtx`;'.format(paint_opacity))
            maya.mel.eval('artAttrSkinPaintCtx -e -clear `currentCtx`;')
            self.update_window()
        except:pass

    def weight_paste(self, vertexs, skin_clusters, _state):
        if not vertexs and not self._joint_weight_dict_vtx_list:
            return

        src_text = cmds.textField(self._name_original_textfield_name, q=True, text=True)
        dst_text = cmds.textField(self._name_change_textfield_name, q=True, text=True)
        same_length_flag = len(vertexs) == len(self._joint_weight_dict_vtx_list)

        for i,vtx in enumerate(vertexs):
            skin_cluster = [x for x in cmds.listHistory(vtx) if x in skin_clusters]
            if skin_cluster:
                skin_cluster = skin_cluster[0]
                joints = cmds.skinPercent(skin_cluster, vtx, q=True, transform=None)
                temp_dict = dict([(x, 0.0) for x in joints])

                if same_length_flag:
                    for joint,weight in self._joint_weight_dict_vtx_list[i].items():
                        temp_dict[joint.replace(src_text, dst_text)] = weight
                        if src_text in joint and dst_text in joint:
                            temp_dict[joint] = weight
                else:
                    for joint,weight in self._joint_weight_dict_vtx_list[0].items():
                        temp_dict[joint.replace(src_text, dst_text)] = weight

                try:
                    cmds.skinPercent(skin_cluster, vtx,
                                    normalize=False,
                                    zeroRemainingInfluences=True,
                                    transformValue=(temp_dict.items()))
                except:
                    cmds.warning(u"文字列内に置換ポイントが複数あります、置換文字を工夫してやり直してください")
                    pass
        self.update_window()

    def weight_copy(self, vertexs, skin_clusters, _state):
        if not vertexs:
            return
        self._joint_weight_dict_vtx_list = []

        for vtx in vertexs:
            skin_cluster = [x for x in cmds.listHistory(vtx) if x in skin_clusters]
            if skin_cluster:
                skin_cluster = skin_cluster[0]
                joint_weight_dict = dict(zip(cmds.skinPercent(skin_cluster, vtx, ignoreBelow=0.00000001, q=True, transform=None),
                                        [x for x in cmds.skinPercent(skin_cluster, vtx, q=True, value=True) if x > 0.0]))
                self._joint_weight_dict_vtx_list.append(joint_weight_dict)

        cmds.text(self._vtx_length_text_name, edit=True, label=len(self._joint_weight_dict_vtx_list))


    def get_dag_meshfns(self, meshes):
        sel_list = om2.MSelectionList()
        for mesh in meshes:
            sel_list.add(mesh)

        _dags = []
        mesh_fns = []
        _deps = []

        for i in range(sel_list.length()):
            dag_path = sel_list.getDagPath(i)
            # dep = sel_list.getDependNode(i)
            _dags.append(dag_path)
            # _deps.append(dep)
            mesh_fns.append(om2.MFnMesh(dag_path))
        return mesh_fns, _dags


    def get_more_threshold_weight_vertex_api2(self, meshes, skin_clusters, select_joints, value):

        mesh_fns,_dags = self.get_dag_meshfns(meshes)
        new_sel_list = om2.MSelectionList()

        for mesh_fn,_dag in zip(mesh_fns,_dags):
            _historys = [x for x in cmds.listHistory(_dag) if x in skin_clusters]
            if _historys:
                skin_cluster = _historys[0]
                skinNode = om2.MGlobal.getSelectionListByName(skin_cluster).getDependNode(0)
                skinFn = om2anim.MFnSkinCluster(skinNode)

                indices = range(mesh_fn.numVertices)
                singleIdComp = om2.MFnSingleIndexedComponent()
                vertexComp = singleIdComp.create(om2.MFn.kMeshVertComponent)

                new_singleIdComp = om2.MFnSingleIndexedComponent()
                new_vertexComp = new_singleIdComp.create(om2.MFn.kMeshVertComponent)

                infDags = skinFn.influenceObjects()
                infIndices = om2.MIntArray(len(infDags), 0)

                for x in range(len(infDags)):
                    infIndices[x] = int(skinFn.indexForInfluenceObject(infDags[x]))

                indexs = []

                for x in range(len(infDags)):
                    joint = infDags[x].fullPathName()

                    if joint.split("|")[-1] in [j.split("|")[-1] for j in select_joints]:
                        vtx_weights = skinFn.getWeights(_dag, vertexComp, x)
                        for i, weight in enumerate(vtx_weights):
                            if value <= weight:
                                indexs.append(i)



                new_singleIdComp.addElements(indexs)
                new_sel_list.add((_dag, new_vertexComp))

        if not new_sel_list.isEmpty():
            om2.MGlobal.setActiveSelectionList(new_sel_list, om2.MGlobal.kReplaceList)

    def get_dag_meshfns_comp(self, meshes):
        sel_list = om2.MGlobal.getActiveSelectionList()

        if not sel_list:
            return

        _dags = []
        mesh_fns = []
        _deps = []
        _compObjs = []

        for i in range(sel_list.length()):
            try:
                dagPath, compObj = sel_list.getComponent(i)
                fnComp = om2.MFnSingleIndexedComponent(compObj)
                if compObj.hasFn(om2.MFn.kMeshVertComponent):
                    _compObjs.append(compObj)
            except:
                continue

            dag_path = sel_list.getDagPath(i)
            _dags.append(dag_path)
            mesh_fns.append(om2.MFnMesh(dag_path))
        return mesh_fns, _dags,_compObjs

    def deselect_vertex_api2(self, meshes, skin_clusters, select_joints, value):

        mesh_fns,_dags,compObjs = self.get_dag_meshfns_comp(meshes)

        if len(_dags) != len(compObjs):
            return

        new_sel_list = om2.MSelectionList()

        for mesh_fn,_dag,compObj in zip(mesh_fns,_dags,compObjs):
            _historys = [x for x in cmds.listHistory(_dag) if x in skin_clusters]
            if _historys:
                skin_cluster = _historys[0]
                skinNode  = om2.MGlobal.getSelectionListByName(skin_cluster).getDependNode(0)
                skinFn = om2anim.MFnSkinCluster(skinNode)

                # indices = range(mesh_fn.numVertices)
                fnComp = om2.MFnSingleIndexedComponent(compObj)
                indices = fnComp.getElements()

                singleIdComp = om2.MFnSingleIndexedComponent()
                vertexComp = singleIdComp.create(om2.MFn.kMeshVertComponent)

                new_singleIdComp = om2.MFnSingleIndexedComponent()
                new_vertexComp = new_singleIdComp.create(om2.MFn.kMeshVertComponent)

                infDags = skinFn.influenceObjects()
                infIndices = om2.MIntArray(len(infDags), 0)

                for x in range(len(infDags)):
                    infIndices[x] = int(skinFn.indexForInfluenceObject(infDags[x]))

                indexs = []

                for x in range(len(infDags)):
                    joint = infDags[x].fullPathName()
                    if joint.split("|")[-1] in [j.split("|")[-1] for j in select_joints]:
                        vtx_weights = skinFn.getWeights(_dag, vertexComp, x)
                        for i, weight in enumerate(vtx_weights):
                            if value <= weight:
                                indexs.append(i)

                new_ids = list(set(indices) - set(indexs))

                new_singleIdComp.addElements(new_ids)
                new_sel_list.add((_dag, new_vertexComp))

        if not new_sel_list.isEmpty():
            om2.MGlobal.setActiveSelectionList(new_sel_list, om2.MGlobal.kReplaceList)


    def get_near_threshold_weight_vertex_api2(self, meshes, skin_clusters, select_joints, value):

        mesh_fns,_dags = self.get_dag_meshfns(meshes)
        new_sel_list = om2.MSelectionList()

        for mesh_fn,_dag in zip(mesh_fns,_dags):
            _historys = [x for x in cmds.listHistory(_dag) if x in skin_clusters]
            if _historys:
                skin_cluster = _historys[0]
                skinNode  = om2.MGlobal.getSelectionListByName(skin_cluster).getDependNode(0)
                skinFn = om2anim.MFnSkinCluster(skinNode)

                indices = range(mesh_fn.numVertices)
                singleIdComp = om2.MFnSingleIndexedComponent()
                vertexComp = singleIdComp.create(om2.MFn.kMeshVertComponent)

                new_singleIdComp = om2.MFnSingleIndexedComponent()
                new_vertexComp = new_singleIdComp.create(om2.MFn.kMeshVertComponent)

                infDags = skinFn.influenceObjects()
                infIndices = om2.MIntArray(len(infDags), 0)

                for x in range(len(infDags)):
                    infIndices[x] = int(skinFn.indexForInfluenceObject(infDags[x]))

                indexs = []

                for x in range(len(infDags)):
                    joint = infDags[x].fullPathName()
                    if joint.split("|")[-1] in [j.split("|")[-1] for j in select_joints]:
                        vtx_weights = skinFn.getWeights(_dag, vertexComp, x)
                        for i, weight in enumerate(vtx_weights):
                            if value - self._threshold_range <= weight <= value + self._threshold_range:
                                indexs.append(i)

                new_singleIdComp.addElements(indexs)
                new_sel_list.add((_dag, new_vertexComp))

        if not new_sel_list.isEmpty():
            om2.MGlobal.setActiveSelectionList(new_sel_list, om2.MGlobal.kReplaceList)


    def get_near_threshold_weight_vertex(self, meshes, skin_clusters, select_joints, value):
        select_vertexs = []
        _meshes_dict = dict()
        pre_vid = None
        pre_mesh = None

        for mesh, skin_cluster in zip(meshes, skin_clusters):
            if skin_cluster:
                _need_vertexs = []
                joints = self.get_edit_joints(skin_cluster, select_joints)
                for i in range(cmds.polyEvaluate(mesh, vertex=True)):
                    vertex = "{}.vtx[{}]".format(mesh, i)
                    for joint in joints:
                        weight = cmds.skinPercent(skin_cluster, vertex, q=True, transform=joint, value=True)
                        if value-self._threshold_range <= weight <= 10:
                            _need_vertexs.append(i)
                if _need_vertexs:
                    _meshes_dict[mesh] = _need_vertexs

        for mesh, vertexs in _meshes_dict.items():
            vtx_connection = []
            for i in vertexs:
                if pre_mesh == mesh or pre_mesh is None:
                    if pre_vid == i-1 or pre_vid is None:
                        pre_mesh = mesh
                        pre_vid = i
                        vtx_connection.append(i)
                        continue
                if pre_mesh != mesh:
                    sel_mesh = pre_mesh
                else:
                    sel_mesh = mesh
                select_vertexs.append("{}.vtx[{}:{}]".format(sel_mesh, vtx_connection[0], vtx_connection[-1]))
                pre_mesh = mesh
                vtx_connection = [i]

        return select_vertexs


    def get_more_threshold_weight_vertex(self, meshes, skin_clusters, select_joints, value):
        select_vertexs = []
        _meshes_dict = dict()
        pre_vid = None
        pre_mesh = None

        for mesh, skin_cluster in zip(meshes, skin_clusters):
            if skin_cluster:
                _need_vertexs = []
                joints = self.get_edit_joints(skin_cluster, select_joints)
                for i in range(cmds.polyEvaluate(mesh, vertex=True)):
                    vertex = "{}.vtx[{}]".format(mesh, i)
                    for joint in joints:
                        weight = cmds.skinPercent(skin_cluster, vertex, q=True, transform=joint, value=True)
                        if value <= weight:
                            _need_vertexs.append(i)
                if _need_vertexs:
                    _meshes_dict[mesh] = _need_vertexs

        for mesh, vertexs in _meshes_dict.items():
            vtx_connection = []
            for i in vertexs:
                if pre_mesh == mesh or pre_mesh is None:
                    if pre_vid == i-1 or pre_vid is None:
                        pre_mesh = mesh
                        pre_vid = i
                        vtx_connection.append(i)
                        continue
                if pre_mesh != mesh:
                    sel_mesh = pre_mesh
                else:
                    sel_mesh = mesh
                select_vertexs.append("{}.vtx[{}:{}]".format(sel_mesh, vtx_connection[0], vtx_connection[-1]))
                pre_mesh = mesh
                vtx_connection = [i]

        return select_vertexs


    def deselect_vertex(self, vertexs, meshes, skin_clusters, _state):
        value = cmds.floatField(self._select_value_float_field_name, q=True, value=True)

        select_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)

        if not select_joints:
            return
        select_joints = [x.split()[-1] for x in select_joints]

        select_vertexs = []
        for mesh, skin_cluster in zip(meshes, skin_clusters):
            if skin_cluster:
                joints = self.get_edit_joints(skin_cluster, select_joints)
                _vertexs = cmds.ls("{}.vtx[*]".format(mesh), flatten=True, long=True)
                for joint in joints:
                    for vertex in _vertexs:
                        weight = cmds.skinPercent(skin_cluster, vertex, q=True, transform=joint, value=True)
                        if value-self._threshold_range <= weight <= value+self._threshold_range:
                            select_vertexs.append(vertex)
        if select_vertexs:
            # cmds.undoInfo(swf=False)
            # cmds.select(list(set(vertexs) - set(select_vertexs)), replace=True)
            cmds.select(select_vertexs, deselect=True)
            # cmds.undoInfo(swf=True)

    def select_vertex(self, flag, meshes, skin_clusters, _state):
        value = cmds.floatField(self._select_value_float_field_name, q=True, value=True)
        select_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)
        if not select_joints:
            return
        select_joints = [x.split()[-1] for x in select_joints]
        select_vertexs = []

        if flag == "More":
            select_vertexs = self.get_more_threshold_weight_vertex_api2(meshes, skin_clusters, select_joints, value)
        elif flag == "Near":
            select_vertexs = self.get_near_threshold_weight_vertex_api2(meshes, skin_clusters, select_joints, value)
        elif flag == "Deselect":
            select_vertexs = self.deselect_vertex_api2(meshes, skin_clusters, select_joints, value)
        if select_vertexs:
            # cmds.undoInfo(swf=False)
            cmds.select(select_vertexs, replace=True)
            # cmds.undoInfo(swf=True)

    def select_vertex_invert(self, meshes, _state):
        selections = cmds.ls(selection=True, long=True)
        if not selections:
            return

        vertexs = cmds.filterExpand(cmds.polyListComponentConversion(selections,
                                        toVertex=True),
                                            selectionMask=31, fullPath=True)
        if not vertexs:
            return

        invert_select = []
        for mesh in meshes:
            invert_select.extend(cmds.ls("{}.vtx[*]".format(mesh), flatten=True, long=True))
        # vertex_set = list(set(invert_select) - set(vertexs))
        if invert_select:
            # cmds.undoInfo(swf=False)
            # cmds.select(vertex_set, replace=True)
            cmds.select(invert_select, toggle=True)
            # cmds.undoInfo(swf=True)

    def lock_btn(self, flag, skin_clusters, _state):
        select_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)
        all_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, allItems=True)
        select_joint_indexs = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectIndexedItem=True)
        if not select_joints:
            return
        all_joints = [cmds.ls(x.split()[-1], shortNames=True)[0] for x in all_joints]
        for skin_cluster in skin_clusters:
            if skin_cluster:
                joints = self.get_edit_joints(skin_cluster, select_joints)
                for joint in joints:
                    joint_short_name = cmds.ls(joint, shortNames=True)[0]
                    if flag == "Lock":
                        cmds.skinCluster(skin_cluster, e=True, influence=joint_short_name, lockWeights=True)
                    elif flag == "UnLock":
                        cmds.skinCluster(skin_cluster, e=True, influence=joint_short_name, lockWeights=False)
                    else:
                        cmds.skinCluster(skin_cluster, e=True, influence=joint_short_name,
                            lockWeights=not cmds.skinCluster(skin_cluster, q=True, influence=joint_short_name, lockWeights=True))

        for i in select_joint_indexs:
            cmds.textScrollList(self._lock_list_text_scroll_list_name, edit=True, removeIndexedItem=i)
            if cmds.skinCluster(skin_cluster, influence=all_joints[i-1], q=True, lockWeights=True):
                cmds.textScrollList(self._lock_list_text_scroll_list_name, edit=True, appendPosition=[i, "{0}".format( "Lock" )])
            else :
                cmds.textScrollList(self._lock_list_text_scroll_list_name, edit=True, appendPosition=[i, "{0}".format( "    " )])

    def absolute_or_relative( self, _state, relative_flag=True) :
        slider_size = self.get_slider_size()
        if not relative_flag:
            cmds.intSlider(self._int_slider_name, edit=True, min=0, max=slider_size)
            cmds.floatField(self._slider_value_float_field_name, edit=True, min=0)
            self.set_slider_value()
        else:
            cmds.intSlider(self._int_slider_name, edit=True, min=-slider_size, max= slider_size, value=0)
            cmds.floatField(self._slider_value_float_field_name, edit=True, min=-1, value=0)

    def get_slider_size(self, *args):
        step_value = cmds.floatField(self._slider_step_float_field_name, q=True, value=True)
        slider_size = 1 / step_value
        return slider_size

    def set_slider_value(self, *args):
        slider_size = self.get_slider_size()
        if slider_size == 1.0:
            slider_size = 2.0

        select_joint_indexs = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectIndexedItem=True)

        if select_joint_indexs:
            weights = cmds.textScrollList(self._weight_list_text_scroll_list_name, q=True, allItems=True)
            current_weight = float(weights[select_joint_indexs[0] - 1])
            if cmds.radioButtonGrp(self._absolute_relative_change_radio_btn_name, q=True, select=True) == 1:
                cmds.floatField(self._slider_value_float_field_name, edit=True, value= current_weight)
                cmds.intSlider(self._int_slider_name, e=True,
                                min=0,
                                max=slider_size,
                                value=int(current_weight * slider_size))
            else :
                cmds.intSlider (self._int_slider_name, edit=True,
                                min= -slider_size , max= slider_size, value=0)
                cmds.floatField(self._slider_value_float_field_name, edit=True, min=-1, v=0)

    def act_value(self, vertex, skin_cluster):
        joints,_ = self.clean_list(cmds.skinCluster(skin_cluster, q=True, influence=True))
        all_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, allItems=True)
        if not all_joints:
            return
        all_joints = [x.split()[-1] for x in all_joints]
        for i, joint in enumerate(all_joints):
            if joint in [x.split()[-1] for x in joints]:
                cmds.textScrollList(self._weight_list_text_scroll_list_name, edit=True, removeIndexedItem=i + 1)
                weight = cmds.skinPercent(skin_cluster, vertex, q=True, value=True, transform=joint)
                cmds.textScrollList(self._weight_list_text_scroll_list_name, edit=True, appendPosition=[i + 1, str(weight)])

    def get_skincluster_api2(self, dagPath, sel_list, num):
        skinCluster = cmds.ls(cmds.listHistory(dagPath.fullPathName()), type='skinCluster')
        if not skinCluster:
            return None, None
        clusterName =skinCluster[0]
        sellist = om2.MGlobal.getSelectionListByName(clusterName)

        skinNode = sel_list.getDependNode(num)
        skinFn = om2anim.MFnSkinCluster(skinNode)
        return skinFn, clusterName

    def round_weight_api2(self, *args):
        sel_list = om2.MGlobal.getActiveSelectionList()

        if not sel_list:
            return

        step_value = cmds.floatField(self._slider_step_float_field_name, q=True, value=True)
        point_length = len(str(step_value).split(".")[1])

        vertex_count = 0

        target_mesh_dagPath_names = []
        target_mesh_fns = {}
        target_mesh_vtx = {}
        skin_cluster_name = {}
        target_mesh_dagPath = {}
        maximumInfluences = cmds.intField(self._weight_influence_int_field_name, q=True, value=True)


        _flag = False
        for x in range(sel_list.length()):
            compObj = None
            try:
                dagPath, compObj = sel_list.getComponent(x)
            except:
                dagPath = sel_list.getDagPath(i)
                continue

            if dagPath.hasFn(om2.MFn.kMesh):
                fnMesh = om2.MFnMesh(dagPath)
                skinCluster = cmds.ls(cmds.listHistory(dagPath.fullPathName()), type='skinCluster')

                if not skinCluster:
                    continue

                skinCluster = skinCluster[0]
                dagPath_name = dagPath.fullPathName()
                target_mesh_dagPath_names.append(dagPath_name)
                target_mesh_dagPath[dagPath.fullPathName()] = dagPath
                target_mesh_fns[dagPath.fullPathName()] = fnMesh
                skin_cluster_name[dagPath.fullPathName()] = skinCluster

                comp_flag = True
                if compObj:
                    fnComp = om2.MFnSingleIndexedComponent(compObj)
                    if compObj.hasFn(om2.MFn.kMeshVertComponent):
                        indexs = fnComp.getElements()
                    elif compObj.hasFn(om2.MFn.kMeshEdgeComponent):
                        edges = []
                        [edges.extend(fnMesh.getEdgeVertices(z)) for z in fnComp.getElements()]
                        indexs = list(set(edges))
                    elif compObj.hasFn(om2.MFn.kMeshPolygonComponent):
                        faces = []
                        [faces.extend(fnMesh.getPolygonVertices(z)) for z in fnComp.getElements()]
                        indexs = list(set(faces))
                    else:
                        comp_flag = False

                if not comp_flag:
                    indexs = range(fnMesh.numVertices)
                    fnComp = om2.MFnSingleIndexedComponent()
                vertexComp = fnComp.create(om2.MFn.kMeshVertComponent)

                fnComp.addElements(indexs)
                vertex_count += len(fnComp.getElements())
                target_mesh_vtx[dagPath.fullPathName()] = fnComp

        if target_mesh_dagPath_names:
            _flag = True
            gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

            if vertex_count == 1:
                vertex_count = 2

            cmds.progressBar(gMainProgressBar, edit=True,
                        beginProgress=True, isInterruptable=False,
                        status='Now Rounding...',
                        maxValue=vertex_count)

            for dagPath_name in target_mesh_dagPath_names:

                dagPath = target_mesh_dagPath[dagPath_name]
                fnMesh = target_mesh_fns[dagPath_name]
                fnComp = target_mesh_vtx[dagPath_name]
                skinCluster_name = skin_cluster_name[dagPath_name]

                skinNode = om2.MGlobal.getSelectionListByName(skinCluster_name).getDependNode(0)
                skinFn = om2anim.MFnSkinCluster(skinNode)

                indices = fnComp.getElements()
                fnCompNew = om2.MFnSingleIndexedComponent()
                vertexComp = fnCompNew.create(om2.MFn.kMeshVertComponent)
                fnCompNew.addElements(indices)

                # maximumInfluences = cmds.skinCluster(skinCluster_name, q=True, maximumInfluences=True)

                infDags = skinFn.influenceObjects()
                infIndices = om2.MIntArray(len(infDags), 0)

                for x in range(len(infDags)):
                    # こっちが元　これだと一部でエラーが出る　インデックスが順番になっている必要がある？
                    # infIndices[x] = int(skinFn.indexForInfluenceObject(infDags[x]))
                    infIndices[x] = x

                joint_weights = dict()
                joints = [infDags[inf_id].fullPathName() for inf_id in range(len(infDags))]
                joints_dict = dict([i,jnt] for i,jnt in enumerate(joints))
                try:
                    weights = skinFn.getWeights(dagPath, vertexComp)
                except Exception as e:
                    print('get skin weight error :', e)
                    continue

                shape = len(infDags)

                reshape_weights = [[weights[0][i+j*shape] for i in range(shape)] for j in range(int(len(weights[0])/shape))]

                round_weights_list = []

                for i,_index in enumerate(indices):
                    weight_dic = dict(zip(joints, [round(x,point_length) for x in reshape_weights[i]]))
                    weight_lists = []
                    [weight_lists.extend([k,v]) for k,v in sorted(weight_dic.items(), key=lambda x:x[1], reverse=True)]

                    _weights = weight_lists[1::2]
                    _joints = weight_lists[0::2]

                    if len(_weights) > maximumInfluences:
                        _zero_weights = [0.0 for x in range(len(_weights[maximumInfluences:]))]
                        del _weights[maximumInfluences:]
                        _weights.extend(_zero_weights)

                    if sum(_weights) != 1.0:
                        if step_value >= 1.0:
                            _weights[0] = round(1.0 - sum(_weights[1:]))
                        else:
                            _weights[0] = round(1.0 - sum(_weights[1:]), point_length)
                    round_weights_list.extend([_weights[_joints.index(_jnt)] for _jnt in joints])
                    cmds.progressBar(gMainProgressBar, edit=True, step=1)

                try:
                    skinFn.setWeights(dagPath, vertexComp, infIndices, om2.MDoubleArray(round_weights_list), False)
                except Exception as e:
                    print('set skin weight error :', e.message)
                    continue

        if _flag:
            cmds.progressBar( gMainProgressBar, edit=True, endProgress=True)
            self.update_window()


    def set_value_preset(self, vertexs, skin_clusters, btn_state, value=0.0):
        if not cmds.objExists(vertexs[0]):
            return
        _result = False
        relative_flag = False

        select_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)
        if not select_joints:
            return
        select_joints = [x.split()[-1] for x in select_joints]

        for skin_cluster in skin_clusters:
            if skin_cluster:
                joints = self.get_edit_joints(skin_cluster, select_joints)
                cmds.skinCluster(skin_cluster, e=True, normalizeWeights=1)
                for joint in joints:
                    if joints:
                        _result = self.set_weights(vertexs, skin_cluster, joints, value, relative_flag)
        if _result:
            self.act_value(vertexs[-1], skin_clusters[-1])
        # self.update_window()

    def set_value_plus_minus(self, vertexs, skin_clusters, plus_flag, _state):
        select_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)
        if not select_joints:
            return
        select_joints = [x.split()[-1] for x in select_joints]

        _result = False
        relative_flag = True
        select_joint_indexs = cmds.textScrollList(self._joint_list_text_scroll_list_name,
                                                    q=True, selectIndexedItem=True)

        step_value = cmds.floatField(self._slider_step_float_field_name, q=True, value=True)
        value = step_value if plus_flag else step_value * -1

        all_weights = cmds.textScrollList(self._weight_list_text_scroll_list_name,
                                                    q=True, allItems=True)

        for skin_cluster in skin_clusters:
            if skin_cluster:
                joints = self.get_edit_joints(skin_cluster, select_joints)
                if joints:
                    _result = self.set_weights(vertexs, skin_cluster, joints, value, relative_flag)

        if _result:
            self.act_value(vertexs[-1], skin_clusters[-1])

    def set_feild_value(self, vertexs, skin_clusters, _state):
        slider_size = self.get_slider_size()
        # value = cmds.floatField(self._slider_value_float_field_name, q=True, value=True)
        value = _state

        select_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)
        if not select_joints:
            return
        select_joints = [x.split()[-1] for x in select_joints]
        relative_flag = cmds.radioButtonGrp(self._absolute_relative_change_radio_btn_name, q=True, select=True)
        relative_flag = False if relative_flag == 1 else True

        _result = False
        for skin_cluster in skin_clusters:
            if skin_cluster:
                joints = self.get_edit_joints(skin_cluster, select_joints)
                if joints:
                    _result = self.set_weights(vertexs, skin_cluster, joints, value, relative_flag)

        if _result:
            if not relative_flag:
                cmds.intSlider(self._int_slider_name, edit=True, value=value * slider_size)
            else:
                cmds.floatField(self._slider_value_float_field_name, edit=True, value=0)
            self.act_value(vertexs[-1], skin_clusters[-1])

    def get_edit_joints(self, skin_cluster, select_joints):
        joint_short_names = [cmds.ls(x.split()[-1], shortNames=True)[0] for x in select_joints]
        joints = [x for x in cmds.skinCluster(skin_cluster, q=True, influence=True) if x in joint_short_names]
        return joints

    def set_weights(self, vertexs, skin_cluster, joints, value, relative_flag=True):
        _result = False
        for joint in joints:
            if not cmds.skinCluster(skin_cluster, q=True, influence=joint, lockWeights=True):
                _result = True
                cmds.skinCluster(skin_cluster, edit=True, normalizeWeights=1)
                if relative_flag:
                    cmds.skinPercent(skin_cluster, vertexs, relative=True,
                                pruneWeights=0.0, transformValue= [(joint, value)])
                else:
                    cmds.skinPercent(skin_cluster, vertexs, transformValue= [(joint, value)])
        return _result

    def set_step_point_length(self, *args):
        slider_size = self.get_slider_size()
        relative_flag = cmds.radioButtonGrp(self._absolute_relative_change_radio_btn_name, q=True, select=True)
        if relative_flag == 1:
            current_value = cmds.floatField(self._slider_value_float_field_name, q=True, value=True)
            cmds.intSlider(self._int_slider_name, edit=True, min=0, max=slider_size)
            cmds.intSlider(self._int_slider_name, edit=True, value=slider_size * current_value)

    def slider_drag(self, vertexs, skin_clusters, _state):
        if not cmds.objExists(vertexs[0]):
            return

        select_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)
        if not select_joints:
            return
        select_joints = [x.split()[-1] for x in select_joints]

        step_value = cmds.floatField(self._slider_step_float_field_name, q=True, value=True)
        value = cmds.intSlider(self._int_slider_name, q=True, value=True)
        slider_size = self.get_slider_size()

        relative_flag = cmds.radioButtonGrp(self._absolute_relative_change_radio_btn_name, q=True, select=True)
        relative_flag = False if relative_flag == 1 else True

        _result = False

        float_field_value = cmds.floatField(self._slider_value_float_field_name, q=True, value=True)
        slider_max_size = cmds.intSlider(self._int_slider_name, q=True, max=True)
        value = step_value * value

        if value < 1:
            cmds.floatField(self._slider_value_float_field_name, edit=True, value=value)

        for skin_cluster in skin_clusters:
            joints = self.get_edit_joints(skin_cluster, select_joints)
            if joints:
                _result = self.set_weights(vertexs, skin_cluster, joints, value, relative_flag)

        if _result:
            cmds.floatField(self._slider_value_float_field_name, edit=True, value=value)
            self.act_value(vertexs[-1], skin_clusters[-1])

    def reset_slider(self, *args):
        if cmds.radioButtonGrp(self._absolute_relative_change_radio_btn_name, q=True, select=True) == 2 :
            cmds.floatField(self._slider_value_float_field_name, e=True, value=0)
            cmds.intSlider(self._int_slider_name, edit=True, value=0)

    def selection_change_list(self, mesh, skin_cluster):
        if not skin_cluster:
            return
        select_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)
        if not select_joints:
            return
        select_joints = [x.split()[-1] for x in select_joints]

        joints = self.get_edit_joints(skin_cluster, select_joints)
        hilite_obj = []
        # cmds.select(clear=True)
        # cmds.undoInfo(swf=False)
        if mesh:
            mesh_transform = cmds.listRelatives(mesh, parent=True, path=True)
            cmds.select(mesh_transform, deselect=True)
            hilite_obj.append(mesh)
        if joints:
            hilite_obj.extend(joints)
        if hilite_obj:
            cmds.hilite(hilite_obj, replace=True)
            # cmds.selectType(objectComponent=True, allComponents=True)
            # cmds.selectType(objectComponent=True, vertex=True)
        self.set_slider_value()
        # cmds.undoInfo(swf=True)
        if cmds.currentCtx() == "artAttrSkinContext":
            maya.mel.eval('artSkinInflListChanging "{}" 0;'.format(select_joints[-1]))
            maya.mel.eval('artSkinInflListChanging "{}" 1;'.format(select_joints[-1]))
            maya.mel.eval('artSkinInflListChanged artAttrSkinPaintCtx;')

    def memory_joint_list(self, select_list_joints, joints, weights):
        _joints = []
        _weights = []
        _id = []
        for i, joint in enumerate(joints):
            if joint.split()[-1] in select_list_joints:
                _joints.append(joint)
                _weights.append(weights[i])
                _id.append(i)
        if _joints:
            joints = _joints
            weights = _weights
        self.joints_list_memory = joints
        self.weights_list_memory = weights
        self._joints_id_memory = _id
        return joints, weights


    def update_list(self, vertex, skin_cluster):
        onlly_select_flag = cmds.checkBox(self._only_select_joint_check_box_name, q=True, value=True)
        select_joints = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)
        if select_joints:
            select_joints = [x.split()[-1] for x in select_joints]
        select_joint_ids = cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectIndexedItem=True)

        cmds.textScrollList(self._joint_list_text_scroll_list_name, edit=True, removeAll=True)
        cmds.textScrollList(self._weight_list_text_scroll_list_name, edit=True, removeAll=True)
        cmds.textScrollList(self._lock_list_text_scroll_list_name, edit=True, removeAll=True)

        if not skin_cluster and not cmds.ls(vertex.split(".")[0]):
            return

        if not cmds.skinPercent(skin_cluster, vertex, q=True, value=True):
            return

        influences = cmds.skinCluster(skin_cluster, q=True, influence=True)
        if not influences:
            return

        last_weights = [round(x, self._default_decimal_point_length) if x>=0.0 else 0.0 for x in cmds.skinPercent(skin_cluster,
                                                                vertex, q=True, value=True)]

        joints, weights = self.clean_list(influences, last_weights)


        if onlly_select_flag:
            if select_joints:
                if not self.joints_list_memory:
                    joints, weights = self.memory_joint_list(select_joints, joints, weights)
                else:
                    joints = self.joints_list_memory
                    weights = [x for i,x in enumerate(last_weights) if i in self._joints_id_memory]
        else:
            self.joints_list_memory = []
            self.weights_list_memory = []


        weights_length = len(weights)

        cmds.rowColumnLayout(self._all_row_colum_layout_name, edit=True,
                                                rowHeight=(1, 17 * weights_length + 12))

        cmds.scrollLayout(self._scroll_layout_name, edit=True, height=1.5 * weights_length)

        for joint, weight in zip(joints, weights) :
            joint_long_name = cmds.ls(joint.split()[-1], long=True)[0]
            cmds.textScrollList(self._joint_list_text_scroll_list_name, edit=True,
                                                            append="{}".format(joint))

            cmds.textScrollList(self._weight_list_text_scroll_list_name, edit=True,
                                                            append="{}".format(weight) )

            if cmds.skinCluster(skin_cluster, influence=joint_long_name, q=True, lockWeights=True):
                cmds.textScrollList(self._lock_list_text_scroll_list_name, edit=True,
                                                            append="{}".format("Lock"))
            else :
                cmds.textScrollList(self._lock_list_text_scroll_list_name, edit=True,
                                                            append="{}".format("   "))

        if select_joints:
            _joints = [x for x in joints if x.split()[-1] in select_joints]
            cmds.textScrollList(self._joint_list_text_scroll_list_name, edit=True,
                                selectItem=_joints)
            if cmds.currentCtx() == "artAttrSkinContext":
                maya.mel.eval('artSkinInflListChanging "{}" 0;'.format(select_joints[-1]))

    def focus_joint(self, skin_cluster, *args):
        camera = cmds.ls("perspShape", type="camera")
        if not camera:
            return
        camera = camera[0]
        camera_transform = cmds.listRelatives(camera, parent=True, path=True)
        if not camera_transform:
            return
        camera_transform = camera_transform[0]
        select_joints = [x.split()[-1] for x in cmds.textScrollList(self._joint_list_text_scroll_list_name, q=True, selectItem=True)]

        if not select_joints:
            return

        # cmds.viewLookAt(camera_transform, position=cmds.xform(select_joints[0], q=True, ws=True, t=True))
        cmds.viewFit(select_joints[0], fitFactor=1)

        # maya.mel.eval("fitPanel -selectedNoChildren;")


    def clean_list(self, joints, weights=[0.0]):

        _joints = []
        for joint in joints:
            joint_name_split = cmds.ls(joint, long=True)[0].split("|")
            joint_name = "{:->{}} {}".format("", len(joint_name_split)-1, joint_name_split[-1])

            _joints.append(joint_name)
        joints = _joints

        texts = cmds.textField(self._joint_search_text_box_name, q=True, text=True).split()
        if not texts:
            return joints, weights

        _new_joints = []
        _new_weights = []

        for joint, weight in zip(joints, weights):
            for text in texts:
                if text in joint.split()[-1] and joint not in _new_joints:
                    _new_joints.append(joint)
                    _new_weights.append(weight)

        if _new_joints:
            joints = _new_joints
            weights = _new_weights
        elif weights != [0.0]:
            cmds.warning(u"文字列[ {0:} ]を含む骨はありません".format(",".join(texts)))

        return joints, weights

    def get_current_data(self, *args):
        selections = cmds.ls(selection=True, long=True)

        if not selections:
            selections = [x for x in cmds.ls(hl=True, long=True) if "transform" == cmds.nodeType(x)]
            if not selections:
                selections = cmds.ls(selection=True, objectsOnly=True, long=True)
                if not selections:
                    selections = cmds.ls(hilite=True)

        if not selections:
            return [], [], []

        vertexs = cmds.filterExpand(cmds.polyListComponentConversion(selections,
                                        toVertex=True),
                                            selectionMask=31, fullPath=True)

        if not vertexs:
            return [], [], []

        _nodes = []

        for selecion in selections:
            _node = selecion.split(".",1)[0]
            if not _node in _nodes:
                _nodes.append(_node)

        _mesh_nodes = [x for x in _nodes if cmds.nodeType(x) == "mesh"]
        if not _mesh_nodes:
            _mesh_nodes = cmds.listRelatives(_nodes, shapes=True, type="mesh", fullPath=True)

        if not _mesh_nodes:
            return [], [], []

        _mesh_nodes = [x for x in _mesh_nodes if not cmds.getAttr("{}.intermediateObject".format(x))]

        if not _mesh_nodes:
            return [], [], []

        skin_clusters = []
        for _mesh_node in _mesh_nodes:
            skin_cluster = get_skincluster(_mesh_node)
            if skin_cluster:
                skin_clusters.append(skin_cluster)

        return vertexs, _mesh_nodes, skin_clusters

    def update_window(self, *args):
        # return

        vertexs, meshes, skin_clusters = self.get_current_data()

        if not skin_clusters:
            return

        self.update_list(vertexs[-1], skin_clusters[-1])

        cmds.button(self._point_one_btn_name, edit=True,
                    command=partial(self.set_value_preset, vertexs, skin_clusters, value=0.1))

        cmds.button(self._point_two_five_btn_name, edit=True,
                    command=partial(self.set_value_preset, vertexs, skin_clusters, value=0.25))

        cmds.button(self._point_five_btn_name, edit=True,
                    command=partial(self.set_value_preset, vertexs, skin_clusters, value=0.5))

        cmds.button(self._point_seven_five_btn_name, edit=True,
                    command=partial(self.set_value_preset, vertexs, skin_clusters, value=0.75))

        cmds.button(self._point_nine_btn_name, edit=True,
                    command=partial(self.set_value_preset, vertexs, skin_clusters, value=0.9))

        cmds.button(self._one_btn_name, edit=True,
                    command=partial(self.set_value_preset, vertexs, skin_clusters, value=1.0))

        cmds.floatField(self._slider_value_float_field_name,
                    edit=True, changeCommand=partial(self.set_feild_value, vertexs, skin_clusters))

        cmds.radioButtonGrp(self._absolute_relative_change_radio_btn_name, edit=True,
                        onCommand1=partial(self.absolute_or_relative, relative_flag=False),
                        onCommand2=partial(self.absolute_or_relative, relative_flag=True))

        cmds.button(self._copy_btn_name, edit=True, command=partial(self.weight_copy, vertexs, skin_clusters))
        cmds.button(self._paste_btn_name, edit=True, command=partial(self.weight_paste, vertexs, skin_clusters))

        cmds.button(self._weight_round_btn_name, e=True, command=partial(self.round_weight_api2, vertexs, meshes, skin_clusters))
        cmds.button(self._weight_lock_btn_name, e=True, command=partial(self.lock_btn, "Lock", skin_clusters))
        cmds.button(self._weight_lock_toggle_btn_name, e=True, command=partial(self.lock_btn, "Toggle", skin_clusters))
        cmds.button(self._weight_unlock_btn_name, e=True, command=partial(self.lock_btn, "UnLock", skin_clusters))
        cmds.button(self._select_near_btn_name, e=True, command=partial(self.select_vertex, "Near", meshes, skin_clusters))
        cmds.button(self._select_more_btn_name, e=True, command=partial(self.select_vertex, "More", meshes, skin_clusters))
        cmds.button(self._select_invert_btn_name, e=True, command=partial(self.select_vertex_invert, meshes))
        cmds.button(self._deselect_btn_name, e=True, command=partial(self.select_vertex, "Deselect", meshes, skin_clusters))
        cmds.button(self._value_set_minus_btn_name, edit=True, command=partial(self.set_value_plus_minus, vertexs, skin_clusters, False) )
        cmds.button(self._value_set_plus_btn_name, edit=True, command=partial(self.set_value_plus_minus, vertexs, skin_clusters, True) )
        cmds.textScrollList(self._joint_list_text_scroll_list_name, e=True,
                            selectCommand=partial(self.selection_change_list, meshes[-1], skin_clusters[-1]),
                            dragCallback=partial(self.focus_joint, skin_clusters[-1]))

        cmds.intSlider(self._int_slider_name, edit=True,
                        dragCommand=partial(self.slider_drag, vertexs, skin_clusters),
                        changeCommand=partial(self.reset_slider))

        self.set_slider_value()



def main():
    we = WeigtEditor()
    we.create()


