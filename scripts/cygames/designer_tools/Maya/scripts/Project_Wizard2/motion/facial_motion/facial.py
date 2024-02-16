# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import re
import csv
from importlib import reload

from PySide2 import QtGui, QtCore, QtWidgets

import maya.cmds as cmds

try:
    import json
except Exception as ex:
    print(ex)
try:
    from ..common import common
    reload(common)
except Exception as ex:
    print(ex)

g_chara_root_regex = '^(p1|p2)(:chr)?(:(p1|p2))?$'
g_facial_event_id = {'eye': 0, 'mouth': 1}
g_eyebrow_sizes = ['S', 'M', 'L']
CURRENT_PATH = os.path.dirname(__file__)


def try_find_chara_root_in_scene():
    """シーン内にキャラの命名規則にあったルートノードがあれば返す
    Returns:
        str: 見つかったキャラグループのルートノード名
    """
    # ダイレクトにp1, p2で検索し見つかれば返す
    chara_root = cmds.ls('p1', type='transform')
    if chara_root:
        return chara_root
    chara_root = cmds.ls('p2', type='transform')
    if chara_root:
        return chara_root
    # トップNodeでRegexにマッチするものがあれば返す
    top_nodes = cmds.ls(assemblies=True)
    for node in top_nodes:
        match_obj = re.match(g_chara_root_regex, node)
        if match_obj:
            chara_root = node
            return chara_root
    # シーン内のTransformでRegexにマッチするものがあれば返す
    transforms = cmds.ls(type='transform')
    for node in transforms:
        match_obj = re.match(g_chara_root_regex, node)
        if match_obj:
            chara_root = node
            return chara_root


def find_chara_root_from_selection():
    """選択からキャラの命名規則にあったルートノードがあれば返す
    Returns:
        str: 見つかったキャラグループのルートノード名
    """
    # シーン内のTransformでRegexにマッチするものがあれば返す
    cmds.select(cmds.ls(sl=True), hi=True)
    transforms = cmds.ls(sl=True, type='transform')
    for node in transforms:
        match_obj = re.match(g_chara_root_regex, node)
        if match_obj:
            chara_root = node
            return chara_root


def find_eyebrow_mesh_from_selection(with_blendshape=True):
    """選択配下から眉メッシュ(_e_)のtransformを見つけ返す
    Args:
        with_blendshape (bool): Trueならブレンドシェイプがある眉メッシュのみ返す
    Returns:
        str: 眉メッシュ(meshのtransform)名
    """
    selection = cmds.ls(sl=True)
    if not selection:
        return
    selection = cmds.listRelatives(selection, ad=True, type='mesh')
    if not selection:
        return
    for mesh in selection:
        if mesh.find('_e_') > -1:
            transforms = cmds.listRelatives(mesh, parent=True)
            if transforms:
                if with_blendshape:
                    if has_blendshapes(transforms[0]):
                        return transforms[0]
                else:
                    return transforms[0]


def find_eyebrow_brendshape_mesh_in_scene():
    """
    シーン内からブレンドシェイプ付きの眉メッシュ(_e_)のtransformを見つけ返す
    上記find_eyebrow_mesh_from_selectionで見つけられなかった場合に使う想定
    """
    blend_shapes = cmds.ls('eyebrow:*', type='blendShape')
    if not blend_shapes:
        return
    for blend_shape in blend_shapes:
        skin_cluster = cmds.listConnections(blend_shape, s=False, d=True, type='skinCluster')
        eyebrow_mesh = cmds.listConnections(skin_cluster, s=False, d=True, type='mesh')
        if eyebrow_mesh:
            return eyebrow_mesh[0]


def find_face_mesh_from_selection():
    """chara_root配下の_f_sotaiがついたメッシュのTransformを一つ返す
    複数ある場合は最初の一つを返す
    Returns:
        str: フェイスメッシュ名
    """
    selection = cmds.ls(sl=True)
    if not selection:
        return
    selection = cmds.listRelatives(selection, ad=True, type='mesh')
    for mesh in selection:
        if mesh.find('_f_sotai') > -1:
            face_transform = cmds.listRelatives(mesh, parent=True)
            if face_transform:
                return face_transform[0]
    # 上記で見つからなかった場合 (chara_rootと違う眉モデルをインポートしていた場合等)
    for mesh in selection:
        if mesh.find('_f_') > -1:
            transforms = cmds.listRelatives(mesh, parent=True)
            if transforms:
                return transforms[0]


def read_csv(csvPath, showDialog=True):
    """
    csvファイルを読み込み配列として返します。
    :param csvPath: csvファイルのパス
    :return:
    """
    if not os.path.exists(csvPath):
        if showDialog:
            cmds.confirmDialog(title='Error',
                               message='csvファイルがありません: ' + csvPath,
                               button=['OK'], defaultButton='OK')
        cmds.error('csvファイルがありません: ' + csvPath)
        return
    csvFile = None
    # csvファイルが既にエクセルで開いているとIOErrorになるので先にチェック
    try:
        csvFile = open(csvPath, 'r')
    except Exception:
        if showDialog:
            cmds.confirmDialog(title='Usage',
                               message='ファイルを閉じてから実行してください: ' + csvPath, button=['OK'],
                               defaultButton='OK')
        cmds.error('ァイルを閉じてから実行してください: ' + csvPath)
        return
    csvDataRows = []
    try:
        csvReader = csv.reader(csvFile)
    except Exception as ex:
        cmds.warning(ex)
    for row in csvReader:
        csvDataRows.append(row)

    csvFile.close()
    return csvDataRows


def set_uv(face_mesh, face_part, faceIndex, u, v, checkbox_key):
    """
    表情ボタンを押した際にUVをシフトする。
    setKeyがTrueならマテリアルのplace2dTextureのoffsetU、offsetVアトリビュートにキーフレームを打つ。
    :param face_mesh: 顔メッシュ
    :faceIndex: 表情ボタンの番号
    :param u: マテリアルのplace2dTextureノードにセットするoffsetUの値。csvに指定されている。
    :param v: マテリアルのplace2dTextureノードにセットするoffsetVの値。csvに指定されている。
    :param checkbox_key: QtWidgets.QCheckBox or bool
    """
    set_key = False
    if isinstance(checkbox_key, QtWidgets.QCheckBox):
        if checkbox_key.checkState() == QtCore.Qt.CheckState.Checked:
            set_key = True
    elif isinstance(checkbox_key, bool):
        set_key = checkbox_key
    if not face_mesh or not cmds.objExists(face_mesh):
        cmds.warning('face meshが見つかりませんでした: ' + str(face_mesh))
        return
    cmds.select(face_mesh)
    face_part_mats = list_materials_from_selecion('{0}_for_facial_edit'.format(face_part))
    if not face_part_mats:
        cmds.confirmDialog(title='Usage',
                           message='目/口は「作業用マテリアルに切り替え」ボタンを押してから使ってください',
                           button=['OK'])
        return
    edit_mat = face_part_mats[0]
    textureFileNode = get_files_from_material(edit_mat)
    if textureFileNode is None:
        cmds.warning('ファイルノードの取得に失敗しました: ' + edit_mat)
        return
    place2dTextures = cmds.listConnections(textureFileNode, type='place2dTexture')
    place2dTextures = list(dict.fromkeys(place2dTextures))
    if len(place2dTextures) != 4:
        cmds.warning('作業用のplace2dTexturesの数が4ではありません。正しく動作しないので中止します。')
        return
    place2dTexture_part_0 = None
    place2dTexture_part_1 = None
    place2dTexture_part_2 = None
    place2dTexture_part_3 = None
    for tex2d in place2dTextures:
        if re.match('^place2dTexture__?(.+?)_({0})_0_'.format(face_part), tex2d):
            place2dTexture_part_0 = tex2d
        elif re.match('^place2dTexture__?(.+?)_({0})_1_'.format(face_part), tex2d):
            place2dTexture_part_1 = tex2d
        elif re.match('^place2dTexture__?(.+?)_({0})_2_'.format(face_part), tex2d):
            place2dTexture_part_2 = tex2d
        elif re.match('^place2dTexture__?(.+?)_({0})_3_'.format(face_part), tex2d):
            place2dTexture_part_3 = tex2d
    blendColor_part = cmds.listConnections(edit_mat, type='blendColors')
    if blendColor_part:
        blendColor_part = blendColor_part[0]
    blendColors2 = cmds.listConnections(blendColor_part, type='blendColors')
    blendColor_part_0_1 = None
    blendColor_part_2_3 = None
    if blendColors2 and len(blendColors2) == 2:
        for bc in blendColors2:
            if re.match('^blendColor_?(.+?)_({0})_0_1_'.format(face_part), bc):
                blendColor_part_0_1 = bc
            if re.match('^blendColor_?(.+?)_({0})_2_3_'.format(face_part), bc):
                blendColor_part_2_3 = bc
    else:
        cmds.warning('BlendColorの取得に失敗しました')
        return
    texture2d = ''
    if faceIndex < 16:
        texture2d = place2dTexture_part_0
        cmds.setAttr('%s.b' % blendColor_part, 1)
        cmds.setAttr('%s.b' % blendColor_part_0_1, 1)
        if set_key:
            cmds.setKeyframe('%s.b' % blendColor_part, outTangentType='step')
            cmds.setKeyframe('%s.b' % blendColor_part_0_1, outTangentType='step')
    elif faceIndex < 32:
        texture2d = place2dTexture_part_1
        cmds.setAttr('%s.b' % blendColor_part, 1)
        cmds.setAttr('%s.b' % blendColor_part_0_1, 0)
        if set_key:
            cmds.setKeyframe('%s.b' % blendColor_part, outTangentType='step')
            cmds.setKeyframe('%s.b' % blendColor_part_0_1, outTangentType='step')
    elif faceIndex < 48:
        texture2d = place2dTexture_part_2
        cmds.setAttr('%s.b' % blendColor_part, 0)
        cmds.setAttr('%s.b' % blendColor_part_2_3, 1)
        if set_key:
            cmds.setKeyframe('%s.b' % blendColor_part, outTangentType='step')
            cmds.setKeyframe('%s.b' % blendColor_part_2_3, outTangentType='step')
    else:
        texture2d = place2dTexture_part_3
        cmds.setAttr('%s.b' % blendColor_part, 0)
        cmds.setAttr('%s.b' % blendColor_part_2_3, 0)
        if set_key:
            cmds.setKeyframe('%s.b' % blendColor_part, outTangentType='step')
            cmds.setKeyframe('%s.b' % blendColor_part_2_3, outTangentType='step')
    try:
        cmds.select(texture2d, r=True)
        cmds.setAttr(texture2d + '.offsetU', u)
        cmds.setAttr(texture2d + '.offsetV', v)
        if set_key:
            cmds.setKeyframe(texture2d, attribute=['offsetU', 'offsetV'], time=cmds.currentTime(query=True), outTangentType='step')
            # ダメ押しでステップカーブ
            cmds.keyTangent(texture2d, outTangentType='step')
            cur_frame = cmds.currentTime(q=True)
            print('キーフレームを設定しました: {0}frame {1}, {2} u:{3}, v{4}'.format(cur_frame, texture2d, faceIndex, u, v))
    except Exception as ex:
        cmds.warning('キーが打てませんでした: ' + str(texture2d))
        print(ex)


def clear_facial_key(face_mesh, face_part):
    """
    目、口の作業用マテリアルからキーフレームを削除 (眉はmainのclear_all_eyebrow_keyを使う)
    :param face_mesh: 顔メッシュ
    :face_part: eye または mouth
    """
    if not face_mesh or not cmds.objExists(face_mesh):
        return
    cmds.select(face_mesh)
    face_part_mats = list_materials_from_selecion('{0}_for_facial_edit'.format(face_part))
    if not face_part_mats:
        cmds.confirmDialog(title='Info', message='キーを打つ対象の作業用マテリアル自体がありません', button=['OK'])
        return
    edit_mat = face_part_mats[0]
    textureFileNode = get_files_from_material(edit_mat)
    if textureFileNode is None:
        cmds.warning('ファイルノードの取得に失敗しました: ' + edit_mat)
        return
    place2dTextures = cmds.listConnections(textureFileNode, type='place2dTexture')
    place2dTextures = list(dict.fromkeys(place2dTextures))
    cleard = False
    for texture2d in place2dTextures:
        try:
            cmds.select(texture2d, r=True)
            cmds.setAttr(texture2d + '.offsetU', 0)
            cmds.setAttr(texture2d + '.offsetV', 0)
            time_range_start = cmds.playbackOptions(q=True, minTime=True)
            time_range_end = cmds.playbackOptions(q=True, maxTime=True)
            cmds.selectKey(texture2d, time=(time_range_start,time_range_end), hierarchy='none', controlPoints=False)
            cmds.cutKey(animation='keys', clear=True)
            cleard = True
        except Exception as ex:
            print(ex)
    if cleard:
        print('キーをクリアしました: ' + face_part)


class PicButton(QtWidgets.QPushButton):
    """表情切り替えようの画像付きボタン
    """
    def __init__(self, imagepath, x, y, w, h, label='Set UV', parent=None, function=None, *args, **kwargs):
        super(PicButton, self).__init__(QtGui.QIcon(), label)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.clicked.connect(self.onclick)
        try:
            x = int(x)
            y = int(y)
            w = int(w)
            h = int(h)
        except Exception as ex:
            cmds.warning('Error: PicButtonの作成に失敗しました。')
            print(ex)
            return
        self.btnIcon = self.getIcon(imagepath, x, y, w, h)
        if self.btnIcon:
            self.setIconSize(QtCore.QSize(64, 32))
            self.setIcon(self.btnIcon)

    def onclick(self):
        self.function(*self.args, **self.kwargs)

    def getIcon(self, imagepath, left, top, width, height):
        if os.path.exists(imagepath):
            sprite = QtGui.QImage(imagepath)
            format = sprite.format()
            if sprite.format() == QtGui.QImage.Format.Format_Invalid:
                btnImage = QtGui.QImage(QtCore.QSize(width, height), QtGui.QImage.Format.Format_Invalid)
            else:
                btnImage = QtGui.QImage(QtCore.QSize(width, height), format)
                painter = QtGui.QPainter(btnImage)
                painter.drawImage(0, 0, sprite, left, top, width, height)
                painter.end()
            return QtGui.QIcon(QtGui.QPixmap.fromImage(btnImage))
        else:
            return None


def get_assigned_materials(mesh):
    """メッシュにアサインされたマテリアル名を返す
    Args:
        mesh (str): メッシュ名
    Returns:
        str: マテリアル名
    """
    materials = []
    if cmds.objectType(mesh) == 'transform':
        shapes = cmds.listRelatives(mesh, shapes=True, path=True)
        if shapes:
            mesh = shapes[0]
    if cmds.objectType(mesh) == 'mesh':
        shading_groups = cmds.listConnections(mesh, type='shadingEngine')
        if shading_groups: 
            for sg in shading_groups:
                connected_materials = cmds.ls(cmds.listConnections(sg), materials=True)
                if connected_materials:
                    for mat in connected_materials:
                        if mat not in materials:
                            materials.append(mat)
    return materials


def list_materials_from_selecion(mat_name=''):
    """
    選択されているモデルにアサインされているマテリアルをリストする。
    param: mat_name string. マテリアルの名前が指定されていたらその名前を含むマテリアルのみ返す。
    """
    selection = cmds.ls(sl=True)
    materials = []
    all_materials = []
    for sel in selection:
        all_materials.extend(get_assigned_materials(sel))
    all_materials = list(set(all_materials))
    if mat_name:
        for mat in all_materials:
            if mat.find(mat_name) > -1:
                materials.append(mat)
    else:
        materials = all_materials
    return materials


def get_files_from_material(mat_name):
    """
    マテリアルについているfileを返します。
    param mat_name: string. マテリアル名。
    return: string file名
    """
    files = cmds.listConnections(mat_name, source=True, destination=False, type='file')
    if not files:
        files = []
    conns = cmds.listConnections(mat_name, source=True, destination=False)
    if conns:
        for conn in conns:
            files2 = get_files_from_material(conn)
            files += files2
    return files


def switch_mat(from_mat, to_mat):
    """マテリアルの切り替え
    Args:
        from_mat (str): meshにアサインされているマテリアル
        to_mat (str): meshにアサインするマテリアル
    """
    to_mat_shading_group = cmds.listConnections(to_mat, type='shadingEngine')[0]
    cmds.select(from_mat)
    # from_matがアサインされているメッシュを選択
    cmds.hyperShade(objects='')
    if cmds.ls(sl=True):
        cmds.sets(e=True, forceElement=to_mat_shading_group)
    # フェイスが選択されているので選択解除
    cmds.select(clear=True)


def create_edit_mat(orig_mat):
    """表情編集用マテリアルを作成
    末尾に_for_facial_editがついている
    Args:
        orig_mat (str): 元々使われていた顔のマテリアル. 例: p1:chr:mt_p1_f_sotai01_eye
    Returns:
        str: 作成された編集用マテリアル名. 例：p1:chr:mt_p1_f_sotai01_eye_for_facial_edit
    """
    mat_edit_name = '{0}_for_facial_edit'.format(orig_mat)
    # 現状目と口のテクスチャ1枚ずつでボタン用テクスチャ流用なのでハードコード
    # 必要とあれば変える
    if orig_mat.find('eye') > -1:
        tgaPath = get_button_texture('eye')
    else:
        tgaPath = get_button_texture('mouth')
    mat_edit = cmds.ls(mat_edit_name)
    if mat_edit:
        mat_edit = mat_edit[0]
        mat_edit_sg = cmds.listConnections(mat_edit, type='hadingEngine')[0]
    else:
        # 新規
        mat_edit = cmds.shadingNode('lambert', asShader=True, name=mat_edit_name)
        mat_edit_sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='%sSG' % mat_edit)
        cmds.connectAttr('%s.outColor' % mat_edit, '%s.surfaceShader' % mat_edit_sg, force=True)
        # 2個目以降nameに連番が付くのだが、最後が数字だとそれがincrementされてしまうので最後に_を付けている
        blendColor = cmds.shadingNode('blendColors', asUtility=True, name=f'blendColor_{0}'.format(orig_mat))
        blendColor_0_1 = cmds.shadingNode('blendColors', asUtility=True, name='blendColor_{0}_0_1_'.format(orig_mat))
        blendColor_2_3 = cmds.shadingNode('blendColors', asUtility=True, name='blendColor_{0}_2_3_'.format(orig_mat))
        cmds.connectAttr('%s.output' % blendColor, '%s.color' % mat_edit, force=True)
        cmds.connectAttr('%s.output' % blendColor_0_1, '%s.color1' % blendColor, force=True)
        cmds.connectAttr('%s.output' % blendColor_2_3, '%s.color2' % blendColor, force=True)
        # 将来的に複数テクスチャ対応できる準備
        for i in range(0, 4):
            place2dTexture = ''
            if os.path.exists(tgaPath):
                place2dTexture = create_texture2d_file('file_{0}_{1}_'.format(orig_mat, str(i)),
                                                       'place2dTexture_{0}_{1}_'.format(orig_mat, str(i)),
                                                       tgaPath)
            else:
                place2dTexture = create_texture2d_file('file_{0}_{1}_'.format(orig_mat, str(i)),
                                                       'place2dTexture_{0}_{1}_'.format(orig_mat, str(i)),
                                                       '')
            # テクスチャーファイルノードとBlendColorノードを繋ぐ
            if i == 0:
                cmds.connectAttr('%s.outColor' % place2dTexture, '%s.color1' % blendColor_0_1, force=True)
            elif i == 1:
                cmds.connectAttr('%s.outColor' % place2dTexture, '%s.color2' % blendColor_0_1, force=True)
            elif i == 2:
                cmds.connectAttr('%s.outColor' % place2dTexture, '%s.color1' % blendColor_2_3, force=True)
            elif i == 3:
                cmds.connectAttr('%s.outColor' % place2dTexture, '%s.color2' % blendColor_2_3, force=True)
        # とりあえず表情1にする
        cmds.setAttr('%s.blender' % blendColor, 1)
        cmds.setAttr('%s.blender' % blendColor_0_1, 1)
        cmds.setAttr('%s.blender' % blendColor_2_3, 1)
    return mat_edit


def create_texture2d_file(file_name, texture2d_name, texture_path):
    """Texture2Dノードを作成する
    編集用マテリアルに使う
    Args:
        file_name (str): Texture2DノードにつながるFileノード名. 例:file_p1:chr:mt_p1_f_sotai01_eye_0_
        texture2d_name (str): Texture2Dノード名. 例:place2dTexture_p1:chr:mt_p1_f_sotai01_eye_0_
        texture_path (str): Fileノードに設定するテクスチャーのパス. 例：...cyg-techart\scripts\Project_Wizard2\motion\facial_motion\images\p2_f_sotai01_001_eye_all.png
    Returns:
        _type_: _description_
    """
    file0 = cmds.shadingNode('file', asTexture=True, isColorManaged=True, name=file_name)
    tex0 = cmds.shadingNode('place2dTexture', asUtility=True, name=texture2d_name)
    cmds.connectAttr('%s.coverage' % tex0, '%s.coverage' % file0, force=True)
    cmds.connectAttr('%s.translateFrame' % tex0, '%s.translateFrame' % file0, force=True)
    cmds.connectAttr('%s.rotateFrame' % tex0, '%s.rotateFrame' % file0, force=True)
    cmds.connectAttr('%s.stagger' % tex0, '%s.stagger' % file0, force=True)
    cmds.connectAttr('%s.offset' % tex0, '%s.offset' % file0, force=True)
    cmds.connectAttr('%s.rotateUV' % tex0, '%s.rotateUV' % file0, force=True)
    cmds.connectAttr('%s.noiseUV' % tex0, '%s.noiseUV' % file0, force=True)
    cmds.connectAttr('%s.vertexUvOne' % tex0, '%s.vertexUvOne' % file0, force=True)
    cmds.connectAttr('%s.vertexUvTwo' % tex0, '%s.vertexUvTwo' % file0, force=True)
    cmds.connectAttr('%s.vertexUvThree' % tex0, '%s.vertexUvThree' % file0, force=True)
    cmds.connectAttr('%s.vertexCameraOne' % tex0, '%s.vertexCameraOne' % file0, force=True)
    cmds.connectAttr('%s.outUV' % tex0, '%s.uv' % file0, force=True)
    cmds.connectAttr('%s.outUvFilterSize' % tex0, '%s.uvFilterSize' % file0, force=True)
    if os.path.isfile(texture_path):
        cmds.setAttr('%s.fileTextureName' % file0, texture_path, type='string')
    return file0


def is_edit_mat(face_mesh, face_part):
    """編集用マテリアルに切り替わっていればTrueを返す
    Args:
        face_mesh (str): 顔メッシュ名
        face_part (str): eye 又は mouth
    Returns:
        bool: 編集用マテリアルならTrue
    """
    if not face_mesh or not cmds.objExists(face_mesh):
        return
    cmds.select(face_mesh)
    mats = list_materials_from_selecion(face_part)
    for mat in mats:
        if mat.find('_for_facial_edit') >= 0:
            return True
    return False


def switch_to_edit_mat(face_mesh, face_part, show_popup=True):
    """
    表情切り替え作業用のマテリアルに切り替える
    Args:
        face_mesh (str): 顔のメッシュtransformの名前
        face_part (str): eye もしくは mouth
        show_popup (bool, optional): ポップアップ出すか. Defaults to True.
    Returns:
        tuple(str, str): (作業用に置き換える前のマテリアル名, 作業用マテリアル名）
    """
    if not face_mesh or not cmds.objExists(face_mesh):
        return
    cmds.select(face_mesh)
    orig_mats = list_materials_from_selecion(face_part)
    if len(orig_mats) == 0:
        if show_popup:
            cmds.confirmDialog(title='Usage',
                               message='キャラモデルのシーンを読み込んでからツールを開いてください\n' +
                               '{0}マテリアルがありませんでした'.format(face_part),
                               button=['OK'])
        else:
            cmds.warning('{0}マテリアルがありませんでした'.format(face_part))
        return
    orig_mat = ''
    for orig_mat in orig_mats:
        if orig_mat.find('_for_facial_edit') >= 0:
            if show_popup:
                cmds.confirmDialog(title='Info',
                                   message='既に作業用マテリアルです',
                                   button=['OK'])
            else:
                cmds.warning('既に作業用マテリアルです')
            return (orig_mat, orig_mat)
    # このキャラ用の作業用マテリアル名
    edit_mat_name = orig_mat + '_for_facial_edit'
    # 作業用マテリアル
    edit_mat = cmds.ls(edit_mat_name)
    if edit_mat:
        # 既存
        edit_mat = edit_mat[0]
    else:
        # 新規
        edit_mat = create_edit_mat(orig_mat)
    switch_mat(orig_mat, edit_mat)
    print('作業用マテリアルに置き換えました: ' + orig_mat + ' to ' + edit_mat)
    return (orig_mat, edit_mat)


def switch_to_orig_mat(face_mesh, face_part, delete_edit_mat, show_popup=True):
    """
    作業用マテリアルから元々のマテリアルに切り替え、作業用マテリアルを削除する
    Args:
        face_mesh (str): 顔のメッシュtransformの名前
        face_part (str): eye もしくは mouth
        delete_edit_mat (bool): 作業用マテリアルを削除
        show_popup (bool, optional): ポップアップ出すか. Defaults to True.
    """
    if not face_mesh or not cmds.objExists(face_mesh):
        return
    cmds.select(face_mesh)
    cur_mats = list_materials_from_selecion(face_part)
    if len(cur_mats) == 0:
        if show_popup:
            cmds.confirmDialog(title='Usage',
                               message='{0}マテリアルがありませんでした'.format(face_part),
                               button=['OK'])
        else:
            cmds.warning('{0}マテリアルがありませんでした'.format(face_part))
        return
    edit_mat = ''
    for mat in cur_mats:
        if mat.find('_for_facial_edit') >= 0:
            edit_mat = mat
            break
    if not edit_mat:
        if show_popup:
            cmds.confirmDialog(title='Info',
                               message='作業用マテリアルではありません',
                               button=['OK'])
        else:
            cmds.warning('作業用マテリアルではありません')
        return
    # 作業用マテリアル名に対応しているオリジナルマテリアル名
    orig_mat_name = edit_mat.split('_for_facial_edit')[0]
    if cmds.ls(orig_mat_name):
        switch_mat(edit_mat, orig_mat_name)
        print('マテリアルを切り替えました: ' + edit_mat + ', ' + orig_mat_name)
        if delete_edit_mat:
            cmds.delete(edit_mat)
    else:
        if show_popup:
            cmds.confirmDialog(title='Usage',
                               message='{0}マテリアルがありませんでした\n'.format(orig_mat_name) +
                               '手動で戻してください',
                               button=['OK'])
        else:
            cmds.warning('{0}マテリアルがありませんでした\n'.format(orig_mat_name) +
                         '手動で戻してください')
        # フェイスが選択されているので選択解除
        cmds.select(clear=True)


def get_button_texture(face_part):
    """表情ボタン用にfacial_uv.csvに指定されたテクスチャパスを返す
    編集用マテリアルにアサインする際に使っている
    Args:
        face_part (str): eye 又は mouth
    Returns:
        str: ボタン表示用の表情テクスチャーパス
    """
    label_index_dict = {}
    csv_rows = read_csv(os.path.join(CURRENT_PATH, 'csv', 'facial_uv.csv'))
    for i, csv_row in enumerate(csv_rows):
        if i == 0:
            for index, label in enumerate(csv_row):
                label_index_dict[label] = index
        else:
            try:
                rowPart = csv_row[label_index_dict.get('Face Part')]
                if face_part == rowPart:
                    btn_img_path = os.path.join(os.path.join(CURRENT_PATH, 'images'),
                                                csv_row[label_index_dict.get('Default Icon Image')])
                    if os.path.exists(btn_img_path):
                        return btn_img_path
            except Exception:
                print('Error フェイシャルcsvの読み取りに失敗しました')


def select_key_node(face_mesh, face_part, texture_num=0, add_to_selection=False):
    """表情のUVスクロールのキーを打っているTexture2Dを選択する
    Args:
        face_mesh (str): 顔メッシュ名
        face_part (str): eye or mouth
        texture_num (int, optional): 4枚あるTexture2Dのどれか. Defaults to 0.
    Returns:
        bool: 選択できたらTrueを返す
    """
    if not face_mesh or not cmds.objExists(face_mesh):
        cmds.confirmDialog(title='Warning',
                           message='顔メッシュがありません',
                           button=['OK'])
        return False
    cmds.select(face_mesh, add=add_to_selection)
    face_part_mats = list_materials_from_selecion('{0}_for_facial_edit'.format(face_part))
    if not face_part_mats:
        cmds.confirmDialog(title='Usage', 
                           message='目/口は「作業用マテリアルに切り替え」ボタンを押してから使ってください',
                           button=['OK'])
        return False
    edit_mat = face_part_mats[0]
    textureFileNode = get_files_from_material(edit_mat)
    if not textureFileNode:
        cmds.warning('ファイルノードの取得に失敗しました: ' + edit_mat)
        return False
    place2dTextures = cmds.listConnections(textureFileNode, type='place2dTexture')
    place2dTextures = list(set(place2dTextures))
    if not place2dTextures:
        cmds.warning('place2dTextureが取得できませんでした: ' + edit_mat)
        return False
    else:
        regex = '^place2dTexture__?(.+?)_(' + face_part + ')_(\\d{1})_'
        for tex2d in place2dTextures:
            match_obj = re.match(regex, tex2d)
            if match_obj and len(match_obj.groups()) > 2:
                # match_obj.group(3) は0～3
                tex_num = match_obj.group(3)
                if int(tex_num) == texture_num:
                    print('key node: ' + tex2d)
                    cmds.select(tex2d, add=add_to_selection)
    return True


def get_face_id_from_uv(face_part, u, v, texture_num, csv_rows):
    """Texture2Dにつけた表情のスクロール値から表情番号を返す
    Args:
        face_part (str): eye または mouth
        u (float): テクスチャUスクロール値
        v (float): テクスチャVスクロール値
        texture_num (int): 複数テクスチャの場合何番目のテクスチャか(表情テクスチャ4枚まで対応)
        csv_rows (str[]): facial_uv.csvから読み込んだ値
    Returns:
        str: 表情番号のstr
    """
    label_col_dict = {}
    for row, csv_row in enumerate(csv_rows):
        if row == 0:
            for col, label in enumerate(csv_row):
                label_col_dict[label] = col
        else:
            tex_num = csv_row[label_col_dict.get('Texture Num')]
            try:
                if int(tex_num) != int(texture_num):
                    continue
            except Exception as ex:
                cmds.error(ex)
                continue
            row_part = csv_row[label_col_dict.get('Face Part')]
            if row_part == face_part:
                try:
                    row_u = float(csv_row[label_col_dict.get('Translate Frame U')])
                    row_v = float(csv_row[label_col_dict.get('Translate Frame V')])
                except Exception:
                    cmds.error('facial_uv.csvからの表情番号取得失敗')
                    continue
                if row_u == u and row_v == v:
                    try:
                        face_id = int(csv_row[label_col_dict.get('Face ID')])
                        return face_id
                    except Exception as ex:
                        cmds.error('Face IDの取得に失敗しました\n' + str(ex))


def get_face_uv_from_id(face_part, id, csv_rows):
    """表情番号からテクスチャー番号(現状1枚なので0)とuv値を返す
    Args:
        id (int): 表情番号
        face_part (str): eye または mouth
        csv_rows (str[]): facial_uv.csvから読み込んだ値
    Returns:
        dict: {'u': (float): テクスチャUスクロール値, 'v': (float) テクスチャVスクロール値}
    """
    label_col_dict = {}
    for row, csv_row in enumerate(csv_rows):
        if row == 0:
            for col, label in enumerate(csv_row):
                label_col_dict[label] = col
        else:
            row_part = csv_row[label_col_dict.get('Face Part')]
            row_id = 0
            if row_part == face_part:
                try:
                    row_id = int(csv_row[label_col_dict.get('Face ID')])
                except Exception:
                    cmds.error('facial_uv.csvからの表情番号取得失敗')
                    continue
                if row_id == id:
                    try:
                        row_u = float(csv_row[label_col_dict.get('Translate Frame U')])
                        row_v = float(csv_row[label_col_dict.get('Translate Frame V')])
                        return {'u':row_u, 'v': row_v}
                    except Exception as ex:
                        cmds.error('Face IDの取得に失敗しました\n' + str(ex))


def get_facial_list(face_mesh, face_part, csv_rows, fps=30):
    """
    出力jsonに書き込むための表情パーツのフェイシャルモーションリストを返す
    Args:
        face_mesh (str): 顔メッシュ名
        face_part (str): eye or mouth
        csv_rows (str[]): csvを読み込んだリスト
        fps (int, optional): フレームレート(デフォルトは30)
    Returns:
        [{Event:0, Time:0, Param1:0}...]: ディクショナリのリスト
        UnityのAvatarFacialExpressionAnimEventScriptableObjectに追加するパラメータ
    """
    if not face_mesh or not cmds.objExists(face_mesh):
        return
    cmds.select(face_mesh)
    eye_mats = list_materials_from_selecion(face_part)
    if not eye_mats:
        cmds.confirmDialog(title='Usage', message='{0}マテリアルがありませんでした'.format(face_part))
        return
    face_part_mat = ''
    edit_part_mat = ''
    # 作業用マテリアルがアサインされた状態の場合
    for face_part_mat in eye_mats:
        if face_part_mat.find('_for_facial_edit') >= 0:
            edit_part_mat = face_part_mat
            break
    # 作業用マテリアルがアサインされていない場合
    if not edit_part_mat:
        edit_mat_name = '{0}_for_facial_edit'.format(face_part_mat)
        edit_eye_mats = cmds.ls(edit_mat_name)
        if not edit_eye_mats:
            cmds.confirmDialog(title='Usage', message='{0}のモーションはありません\n'.format(face_part) +
                               '{0}マテリアルがありませんでした\n'.format(edit_mat_name))
            return
        else:
            edit_part_mat = edit_eye_mats[0]
    face_part_files = get_files_from_material(edit_part_mat)
    place2dTextures = cmds.listConnections(face_part_files, type='place2dTexture')
    place2dTextures = list(set(place2dTextures))
    facials = []
    if not place2dTextures:
        cmds.confirmDialog(title='Error', message='{0}のモーションはありません\n'.format(face_part) +
                           '{0}マテリアルがありませんでした\n'.format(edit_mat_name))
        return
    # 4枚まで表情テクスチャ対応しているが使っていないものもある
    for tex2d in place2dTextures:
        regex = '^place2dTexture__?(.+?)_(' + face_part + ')_(\\d{1})_'
        match_obj = re.match(regex, tex2d)
        if match_obj and len(match_obj.groups()) > 2:
            # match_obj.group(3) は0～3
            texture_num = match_obj.group(3)
            numKeyframes = cmds.keyframe(tex2d + '.offsetU', query=True, keyframeCount=True)
            uValues = cmds.keyframe(tex2d + '.offsetU', query=True, index=(0, numKeyframes), valueChange=True)
            vValues = cmds.keyframe(tex2d + '.offsetV', query=True, index=(0, numKeyframes), valueChange=True)
            keyframes = cmds.keyframe(tex2d + '.offsetU', query=True, index=(0, numKeyframes), timeChange=True)
            if numKeyframes == 0:
                continue
            else:
                for i, u_val in enumerate(uValues):
                    v_val = vValues[i]
                    face_id = get_face_id_from_uv(face_part, u_val, v_val, texture_num, csv_rows)
                    if not face_id:
                        cmds.warning('表情IDの取得に失敗しました')
                    else:
                        dict = {}
                        dict['Event'] = g_facial_event_id.get(face_part)
                        dict['Time'] = keyframes[i]/fps
                        dict['Param1'] = face_id
                        facials.append(dict)
    return facials


def load_facial(face_mesh, face_part, csv_rows, facial_list, fps=30):
    """
    目と口のフェイシャルモーションをjsonから読み込む
    Args:
        face_mesh (str): 顔メッシュ名
        face_part (str): eye or mouth
        csv_rows (str[]): 表情定義のcsvを読み込んだリスト
        fps (int, optional): フレームレート(デフォルトは30)
    """
    if not face_mesh or not cmds.objExists(face_mesh):
        return
    cmds.select(face_mesh)
    eye_mats = list_materials_from_selecion(face_part)
    if not eye_mats:
        cmds.confirmDialog(title='Usage', message='{0}マテリアルがありませんでした'.format(face_part))
        return
    face_part_mat = ''
    edit_part_mat = ''
    # 作業用マテリアルがアサインされた状態の場合
    for face_part_mat in eye_mats:
        if face_part_mat.find('_for_facial_edit') >= 0:
            edit_part_mat = face_part_mat
            break
    # 作業用マテリアルがアサインされていない場合
    if not edit_part_mat:
        edit_mat_name = '{0}_for_facial_edit'.format(face_part_mat)
        edit_eye_mats = cmds.ls(edit_mat_name)
        if not edit_eye_mats:
            cmds.confirmDialog(title='Usage', message='{0}のモーションはありません\n'.format(face_part) +
                               '{0}マテリアルがありませんでした\n'.format(edit_mat_name))
            return
        else:
            edit_part_mat = edit_eye_mats[0]
    face_part_files = get_files_from_material(edit_part_mat)
    place2dTextures = cmds.listConnections(face_part_files, type='place2dTexture')
    place2dTextures = list(set(place2dTextures))
    if not place2dTextures:
        cmds.confirmDialog(title='Error', message='{0}のモーションはありません\n'.format(face_part) +
                           '{0}マテリアルがありませんでした\n'.format(edit_mat_name))
        return
    clear_facial_key(face_mesh, face_part)
    # jsonデータ
    for event in facial_list:
        facial_dict = None
        try:
            time = event.get('Time')
            frame = round(float(time) * fps)
            facial_id = int(event.get('Param1'))
            facial_dict = get_face_uv_from_id(face_part, facial_id, csv_rows)
        except Exception:
            pass
        if not facial_dict:
            cmds.warning('表情番号のUV情報が見つかりませんでした: ' + str(facial_id))
            continue
        u = facial_dict.get('u')
        v = facial_dict.get('v')
        if u != None and v != None:
            cmds.currentTime(frame, edit=True, update=True)
            set_uv(face_mesh, face_part, facial_id, u, v, True)


def get_eyebrow_list(eyebrow_mesh, fps=30):
    """出力jsonに書き込むための眉パーツのモーションリストを返す
    jsonはUnity側で以下のスクリプトで読み込む
    Assets/_Debug/Scripts/AvatarViewer/Editor/AvatarViewerFacialExpressionAnimFromMaya.cs
    Args:
        eyebrow_mesh (str): 眉メッシュ
        fps (int, optional): フレームレート(デフォルトは30)
    Returns:
        [{Event:0, Time:0, Param1:0}...]: ディクショナリのリスト
        UnityのAvatarFacialExpressionAnimEventScriptableObjectに追加するパラメータ
    """
    facials = []
    if not eyebrow_mesh:
        return facials
    history = cmds.listHistory(eyebrow_mesh)
    blendshapes = cmds.ls(history, type='blendShape')
    if not blendshapes:
        cmds.confirmDialog(title='Usage', message='眉のモーションはありません\n' + eyebrow_mesh)
    else:
        try:
            target_shapes = cmds.blendShape(eyebrow_mesh, q=True, target=True)
        except Exception:
            return
        target_shapes = remove_namespace(target_shapes)
        for shape in target_shapes:
            expression = shape.split('_')[-1]
            if expression == 'size':
                continue
            times = cmds.keyframe('{0}.{1}'.format(blendshapes[0], shape), query=True)
            if not times:
                continue
            # 開始フレームチェック
            if round(times[0]) != times[0]:
                cmds.warning('Warning: 開始フレームが整数ではないため分割のポーズがズレているかもしれません')
            for time in times:
                val = cmds.keyframe('{0}.{1}'.format(blendshapes[0], shape), query=True, t=(time,time), valueChange=True)
                if val:
                    val = int(val[0] * 100)
                dict = {}
                dict['Event'] = 2
                dict['Time'] = time/fps
                dict['Param1'] = 0
                dict['EyebrowParamList'] = True
                dict['ExpressionShapeName'] = expression
                dict['ShapeWeight'] = val
                facials.append(dict)
    return facials


def load_eyebrow_motion(eyebrow_mesh, facial_list, current_eyebrow_size, fps=30):
    """眉パーツのモーションをjsonから読み込む
    Args:
        eyebrow_mesh (str): 眉メッシュ
        facial_list (list[dict]): [{Event:0, Time:0, Param1:0}...]: ディクショナリのリスト
        current_eyebrow_size (str): S, M, Lのどれか
        fps (int, optional): フレームレート(デフォルトは30)
    """
    if not eyebrow_mesh:
        return
    history = cmds.listHistory(eyebrow_mesh)
    blendshapes = cmds.ls(history, type='blendShape')
    if not blendshapes:
        cmds.confirmDialog(title='Usage', message='眉のモーションはありません\n' + eyebrow_mesh)
    else:
        blendshape = blendshapes[0]
        try:
            target_shapes = cmds.blendShape(eyebrow_mesh, q=True, target=True)
        except Exception:
            return
        target_shapes = remove_namespace(target_shapes)
        # Clearキー
        for shape in target_shapes:
            cmds.cutKey('{0}.{1}'.format(blendshape, shape))
            print('キーをクリアしました: {0}.{1}'.format(blendshape, shape))
        # jsonデータ
        for event in facial_list:
            try:
                time = float(event.get('Time'))
                frame = int(time * fps)
                shape_name = event.get('ExpressionShapeName')
                weight = float(event.get('ShapeWeight')) / 100.0
            except Exception:
                cmds.warning('データのフォーマットが想定外です')
                continue
            for shape in target_shapes:
                expression = shape.split('_')[-1]
                size = shape.split('_')[0]
                if expression == 'size':
                    continue
                if size != current_eyebrow_size:
                    continue
                if expression == size:
                    cmds.warning('ブレンドシェイプのフォーマットが想定外です: サイズ_表情')
                    continue
                if size not in g_eyebrow_sizes:
                    cmds.warning('想定外のサイズです: ' + size)
                    continue
                if shape_name == expression:
                    cmds.currentTime(frame, edit=True, update=True)
                    if not cmds.setKeyframe('{0}.{1}'.format(blendshape, shape), value=weight, outTangentType='step'):
                        cmds.warning('セットキー失敗')
                        return
                    print('キーフレームを設定しました: {0}frame {1}.{2}'.format(frame, blendshape, shape))
                    # ダメ押しでステップカーブ
                    cmds.keyTangent('{0}.{1}'.format(blendshape, shape), ott='step')


def export_split_animation(out_folder, base_file_name, facials, fps):
    """
    timing_boxのscaleZに指定されているキーでIN, LOOP, OUT部分に分けたアニメーションfbxをエクスポートします。
    出力ファイル名はbase_file_name にそれぞれ _IN, _LOOP, _OUT がつきます。
    0スタートにはせず、シーンのキーフレームそのままで出す。
    シーン内のtiming_boxのExtraAttrubuteにIN,LOOP,OUTがついている場合はTrueのものだけエクスポートする。
    ExtraAttributeにIN,LOOP,OUTがない場合はキーがあれば全部エクスポートする。
    ExtraAttrubuteのLOOPがTrueでLOOPのキーがない場合はINとOUTの境目の1フレームをLOOPとしてエクスポートする(jumpなど)。
    wizard2_motion.fbxexportpreset プリセットを使ってエクスポートする。
    Args:
        out_folder (str): 出力フォルダパス
        base_file_name (str): ベースファイル名
    Returns:
        str[] 分割出力したシーンファイルパスの列
    """
    if not facials:
        return
    timing_box = cmds.ls('timing_box', recursive=True)
    if timing_box:
        timing_box = timing_box[0]
    # ExtraAttributeのIN,LOOP,OUTチェックボックス
    is_export_IN = True
    is_export_LOOP = True
    is_export_OUT = True
    is_jump = False
    try:
        is_export_IN = cmds.getAttr('{}.IN'.format(timing_box))
    except Exception:
        pass
    try:
        is_export_LOOP = cmds.getAttr('{}.LOOP'.format(timing_box))
    except Exception:
        pass
    try:
        is_export_OUT = cmds.getAttr('{}.OUT'.format(timing_box))
    except Exception:
        pass
    try:
        is_jump = cmds.getAttr('{}.IsJump'.format(timing_box))
    except Exception:
        pass
    exported_files = []
    # 同じモーションタイプが複数存在する場合連番をつけるのに使う
    num_in = 0
    num_loop = 0
    num_out = 0
    start_split_frame_value = common.get_first_split_frame()
    if not start_split_frame_value:
        return
    end_split_frame_value = common.get_last_split_frame()
    end_split_frame = end_split_frame_value[0]
    next_split_frame_value = common.get_next_split_frame(start_split_frame_value)
    prev_motion_type = None
    while True:
        if not start_split_frame_value:
            break
        from_frame = start_split_frame_value[0]
        motion_type = int(start_split_frame_value[1])
        if next_split_frame_value:
            to_frame = next_split_frame_value[0]
        else:
            # 最後に1フレームだけ別のモーションがある場合は1フレームだけ出力
            if prev_motion_type != motion_type and from_frame == end_split_frame:
                to_frame = end_split_frame
            else:
                break
        file_name = ''
        do_export = True
        if motion_type == 1:
            if not is_export_IN:
                do_export = False
            else:
                if num_in > 0:
                    file_name = base_file_name + '_IN' + str(num_in+1) + '.json'
                else:
                    file_name = base_file_name + '_IN.json'
                num_in += 1
        elif motion_type == 2:
            if not is_export_LOOP:
                do_export = False
            else:
                if num_loop > 0:
                    file_name = base_file_name + '_LOOP' + str(num_loop+1) + '.json'
                else:
                    file_name = base_file_name + '_LOOP.json'
                num_loop += 1
        elif motion_type == 3:
            if not is_export_OUT:
                do_export = False
            else:
                if num_out > 0:
                    file_name = base_file_name + '_OUT' + str(num_out+1) + '.json'
                else:
                    file_name = base_file_name + '_OUT.json'
                num_out += 1
            # ユーザーがExtraAttrubuteのIs Jumpにチェックを入れていて、timing_boxにLOOPのキーが打っていないようなら
            # 別途OUTの開始1フレームをLOOPとしてエクスポートする
            if is_jump:
                if common.has_loop_split_frame():
                    print('Warning: 「Is Jump」はLOOPキーがない時OUTの最初のフレームを' +
                          'LOOPとして出力しますが、LOOPキーがある為LOOPキーを優先します')
                elif not is_export_LOOP:
                    # Is JumpがonでもLOOPがoffなら出力しない
                    pass
                else:
                    # Jumpの時ににLOOPのキーはないので連番はつかない
                    num_loop += 1
                    export_into_takes(facials, out_folder + '/' + base_file_name + '_LOOP.json', from_frame, to_frame, fps)
        if do_export:
            export_path = out_folder + '/' + file_name
            export_into_takes(facials, export_path, from_frame, to_frame, fps)
        prev_motion_type = motion_type
        start_split_frame_value = next_split_frame_value
        next_split_frame_value = common.get_next_split_frame(start_split_frame_value)
    return exported_files


def export_into_takes(facials, export_path, from_frame, to_frame, fps):
    """facialsに入っている表情イベントのTimeがfrom_frameとto_frameの間の
    イベントだけjsonでエクスポートする
    Unity側で
    ・モーション遷移時にはデフォルト表情に戻る
    ・ループ時には表情を引き継ぐ
    となるため、from_frameより前の表情イベントがあれば分割のjsonの最初のフレームにイベント設定
    体の分割モーションのfbx内のスタートフレームは0でなくてもUnity上のアニメーションクリップは
    0スタートになっているため、分割後の表情イベント時間もIN, LOOP, OUTそれぞれ0スタートにする
    Args:
        facials (dict): 表情イベントのディクショナリ
        export_path (str): 出力jsonパス
        from_frame (int): 出力開始フレーム
        to_frame (int): 出力終了フレーム
        fps (int): フレームレート(Unity側はフレームではなく秒なので変換用)
    """
    if not facials:
        print('出力する表情イベントがありません')
        return
    split_dict = {}
    for facial in facials:
        split_events = []
        try:
            events = facials[facial]
            had_event_at_start = False  # 分割の最初のフレームにイベントがあるか
            prev_event = None
            for event in events:
                if event['Time'] < from_frame:
                    prev_event = event
                elif event['Time'] > to_frame:
                    break
                else:
                    if event.get('Time') == from_frame:
                        had_event_at_start = True
                    converted_event = event.copy()
                    converted_event['Time'] = (event['Time'] - from_frame)/fps
                    split_events.append(converted_event)
            # 分割の最初のフレームにイベントがない場合
            # ひとつ前のイベントをjsonの分割最初に設定
            if not had_event_at_start:
                # INの場合0フレーム目にイベントがなければWarning
                if export_path.endswith('IN.json'):
                    cmds.confirmDialog(title='Warning',
                                        message='開始フレームにイベントがありません')
                else:
                    converted_event = prev_event.copy()
                    converted_event['Time'] = 0
                    split_events.insert(0, converted_event)
            split_dict[facial] = split_events
        except Exception as ex:
            cmds.warning(ex)
            break
    json_file = open(export_path, mode='w')
    json.dump(split_dict, json_file)
    json_file.close()
    print('出力しました: ' + export_path)


def has_blendshapes(mesh):
    """メッシュがブレンドシェイプを持っているならTrueを返す
    Args:
        mesh (str): メッシュ名
    Returns:
        bool: ブレンドシェイプを持っているならTrue
    """
    try:
        target_shapes = cmds.blendShape(mesh, q=True, target=True)
    except Exception:
        return False
    if target_shapes:
        return True
    else:
        return False


def has_keyframe(blendshape, shape):
    """特定のブレンドシェイプにキーフレームがあるならTrueを返す
    Args:
        blendshape (str): Deformer名
        shape (str): シェイプターゲット名
    Returns:
        bool: キーフレームがあるならTrue
    """
    try:
        num_keys = cmds.keyframe('{0}.{1}'.format(blendshape, shape), q=True, keyframeCount=True)
        if num_keys > 0:
            return True
    except:
        return False
    return False


def remove_namespace(items):
    """リストのアイテムからネームスペースを削除したリストを返す
    Args:
        items (str[]): ノード名のリストを想定
    Returns:
        str[]: ネームスペースなしのノード名のリスト
    """
    ret = []
    for item in items:
        ret.append(item.split(':')[-1])
    return ret


def has_blendshapes_with_sml(eyebrow_mesh):
    """
    メッシュがサイズ変更用のブレンドシェイプを持っていればTrueを返す
    Mはデフォルトの眉メッシュなのでM_sizeはない
    Args:
        eyebrow_mesh (str): 眉メッシュ名
    Returns:
        bool: S, M, LのブレンドシェイプがそろっていたらTrueを返す
    """
    for size in g_eyebrow_sizes:
        if not get_facial_shapes_by_size(eyebrow_mesh, size, True):
            return False
    return True


def get_facial_shapes_all(eyebrow_mesh, do_remove_namespace=True):
    """指定した眉メッシュの表情のシェイプリストを返す
    「_size」で終わっているシェイプはUnity読み込み時に使わない為
    UIのスライダーバーに表示しないためシェイプリストには含まない
    Args:
        eyebrow_mesh (str): 眉メッシュ名
        do_remove_namespace (bool): シェイプのネームスペースを取る場合はTrue
    Returns:
        str[]: 表情シェイプリスト(_sizeはシェイプ含まない)
    """
    if not eyebrow_mesh:
        return
    if not cmds.objExists(eyebrow_mesh):
        return
    try:
        target_shapes = cmds.blendShape(eyebrow_mesh, q=True, target=True)
    except Exception as ex:
        cmds.warning(ex)
        return
    if do_remove_namespace:
        target_shapes = remove_namespace(target_shapes)
    shapes = []
    for shape in target_shapes:
        # sizeシェイプは含まない
        if shape.endswith('_size'):
            continue
        shapes.append(shape)
    return shapes


def get_facial_shapes_by_size(eyebrow_mesh, size, do_remove_namespace):
    """指定したsizeの表情のシェイプリストを返す
    「_size」で終わっているシェイプはUnity読み込み時に使わない為
    UIのスライダーバーに表示しないためシェイプリストには含まない
    Args:
        eyebrow_mesh (str): 眉メッシュ名
        size (str): S, M, L のどれか
        do_remove_namespace (bool): シェイプのネームスペースを取る場合はTrue
    Returns:
        str[]: 指定したsizeの以外の表情シェイプリスト(_sizeはシェイプ含まない)
    """
    if not eyebrow_mesh:
        return
    if not cmds.objExists(eyebrow_mesh):
        return
    if not size or size not in g_eyebrow_sizes:
        return
    try:
        target_shapes = cmds.blendShape(eyebrow_mesh, q=True, target=True)
    except Exception as ex:
        cmds.warning(ex)
        return
    shapes = []
    if do_remove_namespace:
        target_shapes = remove_namespace(target_shapes)
    for shape in target_shapes:
        # sizeシェイプは含まない
        if shape.endswith('_size'):
            continue
        if shape.startswith(size + '_'):
            shapes.append(shape)
    return shapes


def get_base_size_shape(eyebrow_mesh, size):
    """指定した眉メッシュのサイズ変更用シェイプ(x_size)を返す
    sizeがMの場合は大元の眉メッシュを返す(_sizeは付かない)
    Args:
        eyebrow_mesh (str): 大元の眉メッシュ名
        size (str): S, M, Lのどれか
    Returns:
        str: 指定したsizeのブレンドシェイプのシェイプ
    """
    if not eyebrow_mesh:
        return
    if not cmds.objExists(eyebrow_mesh):
        return
    if not size or size not in g_eyebrow_sizes:
        return
    try:
        target_shapes = cmds.blendShape(eyebrow_mesh, q=True, target=True)
    except Exception:
        cmds.warning('メッシュのブレンドシェイプがありません: ' + eyebrow_mesh)
        return
    # Mサイズは大元の眉メッシュ
    if size == 'M':
        return eyebrow_mesh
    target_shapes = remove_namespace(target_shapes)
    for shape in target_shapes:
        if shape.endswith('_size') and shape.startswith(size + '_'):
            return shape


def switch_base_size(eyebrow_mesh, size, eyebrow_sizes):
    """眉のS, M, Lのベースサイズを切り替える
    DeformerメッシュはMサイズでできているので、SかLの時に
    S_sizeもしくはL_sizeのブレンド値を1にし、他を0にする
    Args:
        eyebrow_mesh (str): 眉Deformer
        size (str): S, M, Lのどれか
        eyebrow_sizes (str[]): [S, M, L]
    """
    if not eyebrow_mesh:
        cmds.warning('switch_base_size 眉メッシュがありません')
        return
    if not cmds.objExists(eyebrow_mesh):
        cmds.warning('switch_base_size 眉メッシュがありません: ' + eyebrow_mesh)
        return
    if size not in eyebrow_sizes:
        cmds.warning('サイズがありません: ' + eyebrow_mesh + ', ' + size)
        return
    history = cmds.listHistory(eyebrow_mesh)
    blendshapes = cmds.ls(history, type='blendShape')
    if not blendshapes:
        return
    # Mは大元のメッシュなのでM_sizeはない
    for button_size in eyebrow_sizes:
        if button_size == 'M':
            continue
        base_shape = get_base_size_shape(eyebrow_mesh, button_size)
        if button_size == size:
            time_range_start = cmds.playbackOptions(q=True, minTime=True)
            cmds.setKeyframe('{0}.{1}'.format(blendshapes[0], base_shape), time=time_range_start, value=1, outTangentType='step')
        else:
            if has_keyframe(blendshapes[0], base_shape):
                cmds.setAttr('{0}.{1}'.format(blendshapes[0], base_shape), 0)
                cmds.cutKey('{0}.{1}'.format(blendshapes[0], base_shape))


def switch_weight_to_another_size(eyebrow_mesh, from_size, to_size):
    """切替前のサイズのブレンドシェイプのウェイトを切替後のサイズのブレンドシェイプに反映する
    キーが打っていない時のサイズ切替に使う想定
    Args:
        from_size (str): S, M, Lのどれか
        to_size (srt): S, M, Lのどれか
    """
    if not eyebrow_mesh:
        cmds.warning('switch_weight_to_another_size 眉メッシュがありません')
        return
    if not cmds.objExists(eyebrow_mesh):
        cmds.warning('switch_weight_to_another_size 眉メッシュがありません: ' + eyebrow_mesh)
        return
    history = cmds.listHistory(eyebrow_mesh)
    blendshapes = cmds.ls(history, type='blendShape')
    if not blendshapes:
        cmds.warning('ブレンドシェイプがありませんでした')
        return
    all_shapes = get_facial_shapes_all(eyebrow_mesh, True)
    from_shapes = get_facial_shapes_by_size(eyebrow_mesh, from_size, True)
    to_shapes = get_facial_shapes_by_size(eyebrow_mesh, to_size, True)
    # 切替前のサイズの表情ウェイトを切替後のサイズの表情ウェイトにセットする
    for from_shape in from_shapes:
        from_expression = from_shape.split('_')[-1]
        for to_shape in to_shapes:
            to_expression = to_shape.split('_')[-1]
            if from_expression == to_expression:
                if from_size == to_size:
                    continue
                # getAttrする前に現在のフレーム更新
                cur_time = cmds.currentTime(query=True)
                cmds.currentTime(cur_time, update=True)
                weight = cmds.getAttr('{0}.{1}'.format(blendshapes[0], from_shape))
                cmds.setAttr('{0}.{1}'.format(blendshapes[0], to_shape), weight)
                cmds.setAttr('{0}.{1}'.format(blendshapes[0], from_shape), 0)
    for shape in all_shapes:
        # From と Toに関係ないやつはリセット
        if shape not in from_shapes and shape not in to_shapes:
            cmds.setAttr('{0}.{1}'.format(blendshapes[0], shape), 0)


def replace_facial_keys_to_another_size(eyebrow_mesh, from_size, to_size):
    """切替前のサイズのブレンドシェイプにキーがあったら切替後のサイズのブレンドシェイプにキーをコピーし、切替前はクリアする
    Args:
        eyebrow_mesh (str): 眉メッシュ名
        from_size (str): S, M, Lのどれか
        to_size (srt): S, M, Lのどれか
    """
    if from_size == to_size:
        return
    if not eyebrow_mesh:
        cmds.warning('replace_facial_keys_to_another_size 眉メッシュがありません')
        return
    if not cmds.objExists(eyebrow_mesh):
        cmds.warning('replace_facial_keys_to_another_size 眉メッシュがありません: ' + eyebrow_mesh)
        return
    history = cmds.listHistory(eyebrow_mesh)
    blendshapes = cmds.ls(history, type='blendShape')
    if not blendshapes:
        cmds.warning('ブレンドシェイプがありませんでした')
        return
    all_shapes = get_facial_shapes_all(eyebrow_mesh, True)
    from_shapes = get_facial_shapes_by_size(eyebrow_mesh, from_size, True)
    to_shapes = get_facial_shapes_by_size(eyebrow_mesh, to_size, True)
    if len(from_shapes) != len(to_shapes):
        user_choice = cmds.confirmDialog(title='Warning', message='サイズ間のブレンドシェイプの数が違います\n' +
                                            '正しい結果にならないかもしれません\n' +
                                            '続行しますか?',
                                            button=['続行', 'Cancel'])
        if user_choice == 'Cancel':
            return
    # 切替前のサイズの表情キーを切替後のサイズの表情キーオブジェクトにコピーする
    for from_shape in from_shapes:
        from_expression = from_shape.split('_')[-1]
        for to_shape in to_shapes:
            to_expression = to_shape.split('_')[-1]
            if from_expression == to_expression:
                if not has_keyframe(blendshapes[0], from_shape):
                    continue
                try:
                    if cmds.copyKey('{0}.{1}'.format(blendshapes[0], from_shape)):
                        if cmds.pasteKey('{0}.{1}'.format(blendshapes[0], to_shape)):
                            cmds.cutKey('{0}.{1}'.format(blendshapes[0], from_shape))
                            cmds.setAttr('{0}.{1}'.format(blendshapes[0], from_shape), 0)
                except Exception as ex:
                    cmds.warning(ex)
                    pass
    for shape in all_shapes:
        # From と Toに関係ないやつはリセット
        if shape not in from_shapes and shape not in to_shapes:
            cmds.cutKey('{0}.{1}'.format(blendshapes[0], shape))
            cmds.setAttr('{0}.{1}'.format(blendshapes[0], shape), 0)


def get_keyed_eyebrow_size(eyebrow_mesh):
    """キーのあるブレンドシェイプのサイズを返す
    Args:
        eyebrow_mesh (str): 眉メッシュ
    Returns:
        str: S, M, L またはNone
    """
    if not eyebrow_mesh:
        cmds.warning('get_keyed_eyebrow_size 眉メッシュがありません')
        return
    if not cmds.objExists(eyebrow_mesh):
        cmds.warning('get_keyed_eyebrow_size 眉メッシュがありません: ' + eyebrow_mesh)
        return
    history = cmds.listHistory(eyebrow_mesh)
    blendshapes = cmds.ls(history, type='blendShape')
    if not blendshapes:
        cmds.warning('ブレンドシェイプがありませんでした')
        return
    all_shapes = get_facial_shapes_all(eyebrow_mesh, True)
    for shape in all_shapes:
        if has_keyframe(blendshapes[0], shape):
            size = shape.split('_')[0]
            return size
