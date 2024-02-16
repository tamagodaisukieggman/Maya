# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from . import checker_method
from . import checker_info
from .model import facial_target_check

try:
    # maya 2022-
    from importlib import reload
except Exception:
    pass

reload(checker_method)
reload(checker_info)
reload(facial_target_check)


param_value_list = [

    {
        'enable': False,

        'ui_type': 'checker, frameが使用可能 未指定はchecker',

        'data_type': 'リストで指定 head,mob_face_head,mob_hair_head,body,base_body,tail,general_tail,prop,mini_face_head,mini_hair_head,mini_body,mini_general_body, facial_targetが指定可能',

        'label': 'UIに表示されるラベル名',
        'check_info': '情報ボタンを押したときのテキスト',
        'error_info': 'エラー表示ボタンを押したときのテキスト',
        'unerror_info': '正常ボタンを押したときのテキスト',
        'target_info': '対象表示ボタンを押したときのテキスト',
        'target_count_info': '何をカウントの対象にしているか表示用のテキスト',
        'target_select': '対象を選択できるかをboolで指定します。',

        'view_type': '対象表示ボタンを押したときのテキスト',

        'error_view': 'エラー表示ボタンの表示',
        'error_select': 'エラー表示ボタンの表示',
        'error_fix': 'エラー表示ボタンの表示',

        'is_warning': '警告表示にするかどうかをboolで指定します',

        'unerror_view': 'エラー表示ボタンの表示',
        'unerror_select': 'エラー表示ボタンの表示',

        'target_view': 'エラー表示ボタンの表示',

        'func': '実行されるメソッド',
        'func_arg': 'メソッド引数'
    },

    {
        'ui_type': 'frame',
        'label': 'パス系',
    },

    {
        'label': 'フォルダの存在確認',
        'check_info': '以下のフォルダの存在確認',
        'error_info': '以下のフォルダが見つかりませんでした',
        'unerror_info': '以下のフォルダが見つかりました',
        'target_info': '以下のフォルダが対象',
        'view_type': 'explorer',
        'error_select': False,
        'unerror_select': False,
        'target_select': False,
        'func': checker_method.check_directory_exist,
    },

    {
        'ui_type': 'frame',
        'label': 'メッシュ系',
    },

    {
        'label': '必須メッシュの存在確認',
        'check_info': '以下の必須メッシュの存在確認',
        'error_info': '以下の必須メッシュの存在しません',
        'unerror_info': '以下の必須メッシュの存在します',
        'target_info': '以下のメッシュが対象',
        'error_select': False,
        'func': checker_method.check_mesh_exist,
    },

    {
        'label': 'メッシュ名の確認',
        'check_info': '以下のメッシュ名が適切か確認',
        'error_info': '以下のメッシュ名が適切ではありません',
        'unerror_info': '以下の通りメッシュ名は適切です',
        'target_info': '以下のメッシュが対象',
        'error_select': True,
        'func': checker_method.check_mesh_name,
    },

    {
        'label': 'メッシュのポリゴン数確認',
        'check_info': '以下のメッシュのポリゴン数を確認',
        'error_info': '以下の通りメッシュのポリゴン数が規定値を超えています',
        'unerror_info': '以下の通りメッシュのポリゴン数は規定内です',
        'target_info': '以下のメッシュが対象',
        'error_select': False,
        'unerror_select': False,
        'target_count_info': 'ポリゴン数',
        'func': checker_method.check_mesh_poly_count,
    },

    {
        'data_type': ['body', 'head', 'mini_hair_head', 'mini_body'],
        'label': 'ポリゴンの合算数確認(社内用)',
        'check_info': '以下のメッシュのポリゴン数を確認',
        'error_info': '以下の通りメッシュのポリゴン数が規定値を超えています',
        'unerror_info': '以下の通りメッシュのポリゴン数は規定内です',
        'target_info': '以下のメッシュが対象',
        'error_select': False,
        'unerror_select': False,
        'target_select': False,
        'target_count_info': 'ポリゴン数',
        'func': checker_method.check_mesh_poly_sum_count,
    },

    {
        'label': 'メッシュの移動、回転、スケール確認',
        'check_info': '以下のメッシュの移動、回転、スケール確認',
        'error_info': '以下のメッシュの移動、回転、スケールは正しくありません',
        'unerror_info': '以下のメッシュの移動、回転、スケールは正しい状態です',
        'target_info': '以下のメッシュが対象',
        'func': checker_method.check_mesh_transform,
    },

    {
        'label': 'メッシュのマテリアルの種類の確認',
        'check_info': '以下のメッシュのマテリアルが正しい種類かどうかの確認',
        'error_info': '以下のメッシュに割り当てられたマテリアルは誤った種類です',
        'unerror_info': '以下のメッシュに割り当てられたマテリアルは正しい種類です',
        'target_info': '以下のメッシュが対象',
        'func': checker_method.check_mesh_material_type,
    },

    {
        'data_type': ['general_body', 'general_sexdiff_body', 'general_multi_area_body'],
        'label': '体型差分のターゲット名チェック',
        'check_info': '以下のメッシュの命名が正しいかどうかの確認',
        'error_info': '以下のメッシュの命名は誤っています',
        'unerror_info': '以下のメッシュの命名は正しいです',
        'target_info': '以下のメッシュが対象',
        'func': checker_method.check_body_diff_target_mesh,
    },

    {
        'data_type': ['prop', 'toon_prop'],
        'label': 'PropのPivotの位置',
        'check_info': 'Pivotの位置が0になっているかの確認',
        'error_info': '以下のメッシュはPirovtの位置が0になっていません',
        'unerror_info': '以下のメッシュはPivotの位置が0になっています',
        'target_info': '以下のメッシュが対象',
        'func': checker_method.check_prop_mesh_pivot,
    },

    {
        'ui_type': 'frame',
        'label': 'NeckEdgeSet系',
    },

    {
        'data_type': ['head', 'body', 'general_body', 'general_sexdiff_body', 'mob_face_head', 'mob_hair_head', 'general_multi_area_body'],
        'label': 'NeckEdgeSetの存在確認',
        'check_info': 'NeckEdgeSetの存在確認',
        'error_info': 'NeckEdgeSetが存在しません',
        'unerror_info': 'NeckEdgeSet',
        'target_info': '',
        'func': checker_method.check_neck_edge_set_exists,
    },

    {
        'data_type': ['head', 'body', 'general_body', 'general_sexdiff_body', 'mob_face_head', 'mob_hair_head', 'general_multi_area_body'],
        'label': 'NeckEdgeSet内のエッジ頂点の法線方向の確認',
        'check_info': '以下のエッジ頂点の法線方向の確認',
        'error_info': '以下のエッジ頂点の法線方向は間違っています',
        'unerror_info': '以下のエッジ頂点の法線方向は正しいです',
        'target_info': '以下のエッジ頂点が対象',
        'func': checker_method.check_neck_edge_normals,
    },

    {
        'data_type': ['head', 'body', 'general_body', 'general_sexdiff_body', 'mob_face_head', 'mob_hair_head', 'general_multi_area_body'],
        'label': 'NeckEdgeSet内のエッジ頂点の頂点カラーの確認',
        'check_info': '以下のエッジ頂点の頂点カラーの確認',
        'error_info': '以下のエッジ頂点の頂点カラーは間違っています',
        'unerror_info': '以下のエッジ頂点の頂点カラーは正しいです',
        'target_info': '以下のエッジ頂点が対象',
        'func': checker_method.check_neck_edge_vtx_colors,
    },

    {
        'data_type': ['head', 'body', 'general_body', 'general_sexdiff_body', 'mob_face_head', 'mob_hair_head', 'general_multi_area_body'],
        'label': 'NeckEdgeSet内のエッジ頂点のウェイトの確認',
        'check_info': '以下のエッジ頂点のウェイトの確認',
        'error_info': '以下のエッジ頂点のウェイトは間違っています',
        'unerror_info': '以下のエッジ頂点のウェイトは正しいです',
        'target_info': '以下のエッジ頂点が対象',
        'func': checker_method.check_neck_edge_weight,
    },

    {
        'data_type': ['head', 'body', 'general_body', 'general_sexdiff_body', 'mob_face_head', 'mob_hair_head', 'general_multi_area_body'],
        'label': 'NeckEdge関連の頂点の位置の確認',
        'check_info': '以下の頂点の位置の確認',
        'error_info': '以下の頂点の位置は間違っています',
        'unerror_info': '以下の頂点の位置は正しいです',
        'target_info': '以下の頂点が対象',
        'func': checker_method.check_neck_edge_vtx_pos,
    },

    {
        'ui_type': 'frame',
        'label': 'クリーンアップ系',
    },

    {
        'label': '5辺以上のフェース確認',
        'check_info': '以下のメッシュの5辺以上のフェース確認',
        'error_info': '以下のフェースは5辺以上のフェースです',
        'unerror_info': '以下のフェースは4辺以下のフェースです',
        'target_info': '以下のフェースが対象',
        'func': checker_method.check_mesh_cleanup,
        'func_arg': ['more4side']
    },

    {
        'label': '凹型フェース確認',
        'check_info': '以下のメッシュの凹型フェース確認',
        'error_info': '以下のフェースは凹型フェースです',
        'unerror_info': '以下のフェースは凹型フェースではありません',
        'target_info': '以下のフェースが対象',
        'func': checker_method.check_mesh_cleanup,
        'func_arg': ['concave']
    },

    {
        'label': '穴のあるフェース確認',
        'check_info': '以下のメッシュの穴のあるフェース確認',
        'error_info': '以下のフェースは穴のあるフェースです',
        'unerror_info': '以下のフェースは穴のあるフェースではありません',
        'target_info': '以下のフェースが対象',
        'func': checker_method.check_mesh_cleanup,
        'func_arg': ['hole']
    },

    {
        'label': 'ラミナフェース確認',
        'check_info': '以下のメッシュのラミナフェース確認',
        'error_info': '以下のフェースはラミナフェースです',
        'unerror_info': '以下のフェースはラミナフェースではありません',
        'target_info': '以下のフェースが対象',
        'func': checker_method.check_mesh_cleanup,
        'func_arg': ['lamina']
    },

    {
        'label': '非多様体フェース確認',
        'check_info': '以下のメッシュの非多様体フェース確認',
        'error_info': '以下のフェースは非多様体フェースです',
        'unerror_info': '以下のフェースは非多様体フェースではありません',
        'target_info': '以下のフェースが対象',
        'func': checker_method.check_mesh_cleanup,
        'func_arg': ['nonmanifold']
    },

    {
        'label': '長さが0のエッジ確認',
        'check_info': '以下のメッシュの長さが0のエッジ確認',
        'error_info': '以下のエッジは長さが0のエッジです',
        'unerror_info': '以下のエッジは長さが0のエッジではありません',
        'target_info': '以下のエッジが対象',
        'func': checker_method.check_mesh_cleanup,
        'func_arg': ['zero_edge']
    },

    {
        'ui_type': 'frame',
        'label': '頂点カラー系',
    },

    {
        'data_type': ['body', 'base_body', 'bdy0001_body', 'bdy0006_body', 'bdy0009_body', 'general_sexdiff_body', 'general_body', 'tail', 'prop', 'toon_prop', 'head', 'general_multi_area_body'],
        'label': '頂点カラーのunsharedの確認',
        'check_info': '以下のメッシュの頂点カラーのunsharedの確認',
        'error_info': '以下の頂点の頂点カラーはunsharedです',
        'unerror_info': '以下の頂点の頂点カラーはunsharedではありません',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': checker_method.check_mesh_unshared_vertex_color,
    },

    # {
    #     'label': '頂点カラーが小数点2桁以下かの確認',
    #     'check_info': '以下のメッシュの頂点カラーが小数点2桁以下かの確認',
    #     'error_info': '以下の頂点の頂点カラーは小数点2桁以下ではありません',
    #     'unerror_info': '以下の頂点の頂点カラーは小数点2桁以下です',
    #     'target_info': '以下の頂点が対象',
    #     'view_type': 'component',
    #     'func': checker_method.check_mesh_vertex_color_round,
    # },

    {
        'label': '頂点カラーのアルファの確認',
        'check_info': '以下のメッシュの頂点カラーのアルファの確認',
        'error_info': '以下の頂点の頂点カラーのアルファ値は1ではありません',
        'unerror_info': '以下の頂点の頂点カラーのアルファ値は1です',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': checker_method.check_mesh_vertex_color_alpha,
    },

    # {
    #     'label': '頂点カラーのノイズ確認',
    #     'check_info': '以下のメッシュの頂点カラーのノイズ確認',
    #     'error_info': '以下の頂点の頂点カラーはノイズがあります',
    #     'unerror_info': '以下の頂点の頂点カラーはノイズはありません',
    #     'target_info': '以下の頂点が対象',
    #     'view_type': 'component',
    #     'func': checker_method.check_mesh_vertex_color_noisy,
    # },

    {
        'label': 'カラーセット数の確認',
        'check_info': '以下のメッシュのカラーセット数の確認',
        'error_info': '以下のメッシュのカラーセット数は正しくありません',
        'unerror_info': '以下のメッシュのカラーセット数は規定値です',
        'target_info': '以下のメッシュが対象',
        'view_type': 'colorset',
        'func': checker_method.check_mesh_colorset,
    },

    {
        'ui_type': 'frame',
        'label': 'ウェイト系',
    },

    {
        'label': 'インフルエンス数が2以内かの確認',
        'check_info': '以下のメッシュのインフルエンス数が2以内かの確認',
        'error_info': '以下の頂点のインフルエンス数は2以内ではありません',
        'unerror_info': '以下の頂点のインフルエンス数は2以内です',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': checker_method.check_mesh_skin_influence,
    },

    {
        'label': '全ジョイントがインフルエンスに含まれているかの確認',
        'check_info': '以下のジョイントが各スキンクラスターのインフルエンスに含まれているかの確認',
        'error_info': '以下のジョイントがインフルエンスから外れてしまっているのでリバインドを行ってください',
        'unerror_info': '以下の頂点はインフルエンスに含まれています',
        'target_info': '以下のジョイントが対象',
        'view_type': 'component',
        'is_warning': True,
        'func': checker_method.check_all_joints_in_influence,
    },

    {
        'label': 'ウェイト精度が小数点以下2桁以内かの確認',
        'check_info': '以下のメッシュのウェイト精度が小数点以下2桁以内かの確認',
        'error_info': '以下の頂点のウェイトは小数点以下2桁以内ではありません',
        'unerror_info': '以下の頂点のウェイトは小数点以下2桁以内です',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': checker_method.check_mesh_skin_round,
    },

    {
        'data_type': ['body', 'general_body', 'general_sexdiff_body', 'base_body', 'head', 'mob_hair_head', 'general_multi_area_body'],
        'label': '不正なジョイントにウェイトがないかの確認',
        'check_info': '以下のジョイントにウェイトがないかの確認',
        'error_info': '以下の頂点は不正なジョイントにウェイトがあります',
        'unerror_info': '以下の頂点は不正なジョイントにウェイトがありません',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': checker_method.check_joint_with_no_skin,
    },

    {
        'label': 'メッシュに不要なスキンがないかの確認',
        'check_info': '以下のメッシュに不要なスキンがないかの確認',
        'error_info': '以下のメッシュには不要なスキンがあります',
        'unerror_info': '以下のメッシュには不要なスキンがありません',
        'target_info': '以下のメッシュが対象',
        'func': checker_method.check_mesh_with_no_skin,
    },

    {
        'ui_type': 'frame',
        'label': 'UV系',
    },

    {
        'label': 'UVセット数の確認',
        'check_info': '以下のメッシュのUVセット数の確認',
        'error_info': '以下のメッシュのUVセット数は正しくありません',
        'unerror_info': '以下のメッシュのUVセット数は規定値です',
        'target_info': '以下のメッシュが対象',
        'view_type': 'uvset',
        'func': checker_method.check_mesh_uvset,
    },

    {
        'label': 'UV座標の確認',
        'check_info': '以下のメッシュのUV座標の確認',
        'error_info': '以下のUVのUV座標は正しくありません',
        'unerror_info': '以下のUVのUV座標は正しい状態です',
        'target_info': '以下のUVが対象',
        'view_type': 'uv',
        'func': checker_method.check_mesh_uv_coordinate,
    },

    {
        'data_type': ['head', 'mob_face_head'],
        'label': 'Eye系のUVセットに含まれるUVの確認',
        'check_info': '以下のメッシュのUVセットの確認',
        'error_info': '以下のuvは正しくありません',
        'unerror_info': '以下のuvは正しい状態です',
        'target_info': '以下のuvが対象',
        'view_type': 'uv',
        'func': checker_method.check_eye_uv_map,
    },

    {
        'ui_type': 'frame',
        'label': 'マテリアル系',
    },

    {
        'label': 'マテリアル存在確認',
        'check_info': '以下のマテリアル存在確認',
        'error_info': '以下のマテリアルは存在していません',
        'unerror_info': '以下のマテリアルは存在しています',
        'target_info': '以下のマテリアルが対象',
        'func': checker_method.check_material_exist,
        'error_select': False,
    },

    {
        'label': '不要マテリアル確認',
        'check_info': '以下のマテリアルの確認',
        'error_info': '以下の不要マテリアルが存在しています',
        'unerror_info': '以下のマテリアルは正しく存在しています',
        'target_info': '以下のマテリアルが対象',
        'func': checker_method.check_wrong_material_exist,
        'error_select': False,
    },

    {
        'label': 'マテリアルの割り当て確認',
        'check_info': '以下のメッシュのマテリアル割り当て確認',
        'error_info': '以下のメッシュのマテリアル割り当てが正しくありません',
        'unerror_info': '以下のメッシュには正しくマテリアルが割り当てられています',
        'target_info': '以下のメッシュが対象',
        'func': checker_method.check_material_link,
        'error_select': False,
    },

    {
        'label': 'マテリアルに割り当たってるテクスチャパス確認',
        'check_info': '以下のマテリアルに割り当たっているテクスチャパス確認',
        'error_info': '以下のマテリアルにはSVN外のテクスチャパスかtga以外のテクスチャパスが割り当たっている可能性があります',
        'unerror_info': '以下のマテリアルには正しいテクスチャパスが割り当たっています',
        'target_info': '以下のマテリアルが対象',
        'func': checker_method.check_material_texture_path,
        'error_select': False,
    },

    {
        # 汎用尻尾、素体はテクスチャ系チェックを行わない
        'ui_type': 'frame',
        'label': 'テクスチャ系',
    },

    {
        'data_type': ['head', 'body', 'general_body', 'general_sexdiff_body', 'tail', 'prop', 'toon_prop', 'mob_face_head', 'mob_hair_head', 'mini_body', 'mini_hair_head', 'general_multi_area_body'],
        'label': 'テクスチャの存在確認',
        'check_info': '以下のテクスチャの存在確認',
        'error_info': '以下のテクスチャは存在していません',
        'unerror_info': '以下のテクスチャは存在しています',
        'target_info': '以下のテクスチャが対象',
        'view_type': 'explorer',
        'error_select': False,
        'unerror_select': False,
        'target_select': False,
        'func': checker_method.check_texture_exist,
        'func_arg': ['texture']
    },

    {
        'data_type': ['head', 'body', 'general_body', 'general_sexdiff_body', 'tail', 'prop', 'toon_prop', 'mob_face_head', 'mob_hair_head', 'mini_body', 'mini_hair_head', 'general_multi_area_body'],
        'label': '編集用テクスチャの存在確認',
        'check_info': '以下の編集用テクスチャの存在確認',
        'error_info': '以下の編集用テクスチャは存在していません',
        'unerror_info': '以下の編集用テクスチャは存在しています',
        'target_info': '以下のテクスチャが対象',
        'view_type': 'explorer',
        'error_select': False,
        'unerror_select': False,
        'target_select': False,
        'func': checker_method.check_texture_exist,
        'func_arg': ['psd']
    },

    {
        'data_type': ['head', 'body', 'general_body', 'general_sexdiff_body', 'tail', 'prop', 'toon_prop', 'mob_face_head', 'mob_hair_head', 'mini_body', 'mini_hair_head', 'general_multi_area_body'],
        'label': 'テクスチャのサイズ確認',
        'check_info': '以下のテクスチャのサイズ確認',
        'error_info': '以下のテクスチャのサイズは正しくありません',
        'unerror_info': '以下のテクスチャのサイズは正しい状態です',
        'target_info': '以下のテクスチャが対象',
        'view_type': 'explorer',
        'error_select': False,
        'unerror_select': False,
        'target_select': False,
        'func': checker_method.check_texture_size,
        'func_arg': ['texture']
    },

    {
        'data_type': ['head', 'body', 'general_body', 'general_sexdiff_body', 'tail', 'prop', 'toon_prop', 'mob_face_head', 'mob_hair_head', 'mini_body', 'mini_hair_head', 'general_multi_area_body'],
        'label': '編集用テクスチャのサイズ確認',
        'check_info': '以下の編集用テクスチャのサイズ確認',
        'error_info': '以下の編集用テクスチャのサイズは正しくありません',
        'unerror_info': '以下の編集用テクスチャのサイズは正しい状態です',
        'target_info': '以下の編集用テクスチャが対象',
        'view_type': 'explorer',
        'error_select': False,
        'unerror_select': False,
        'target_select': False,
        'func': checker_method.check_texture_size,
        'func_arg': ['psd']
    },

    {
        'ui_type': 'frame',
        'label': 'ロケータ系',
    },

    {
        'label': 'ロケータ存在確認',
        'check_info': '以下のロケータ存在確認',
        'error_info': '以下のロケータは存在していません',
        'unerror_info': '以下のロケータは存在しています',
        'target_info': '以下のロケータが対象',
        'error_select': False,
        'func': checker_method.check_locator_exist,
    },

    {
        'label': 'ロケータの移動、回転、スケールの確認',
        'check_info': '以下のロケータの移動、回転、スケールの確認',
        'error_info': '以下のロケータの移動、回転、スケールは正しくありません',
        'unerror_info': '以下のロケータの移動、回転、スケールは正しい状態です',
        'target_info': '以下のロケータが対象',
        'func': checker_method.check_locator_transform,
    },

    {
        'data_type': ['head', 'mob_face_head'],
        'label': '目のジョイントとロケータ位置の確認',
        'check_info': '以下の目のジョイントとロケータ位置の確認',
        'error_info': '以下の目のジョイントとロケータ位置は正しくありません',
        'unerror_info': '以下の目のジョイントとロケータ位置は正しい状態です',
        'target_info': '以下のジョイントとロケータが対象',
        'func': checker_method.check_eye_locator_position,
    },

    {
        'data_type': ['tail'],
        'label': '尻尾のジョイントとロケータ位置の確認',
        'check_info': '以下の尻尾のジョイントとロケータ位置の確認',
        'error_info': '以下の尻尾のジョイントとロケータ位置は正しくありません',
        'unerror_info': '以下の尻尾のジョイントとロケータ位置は正しい状態です',
        'target_info': '以下のジョイントとロケータが対象',
        'func': checker_method.check_tail_locator_position,
    },

    {
        'data_type': ['body', 'base_body', 'tail', 'general_body', 'general_sexdiff_body', 'general_multi_area_body'],
        'label': 'Hipジョイントと尻尾ロケータ位置の確認',
        'check_info': '以下のHipジョイントと尻尾ロケータ位置の確認',
        'error_info': '以下のHipジョイントと尻尾ロケータ位置は正しくありません',
        'unerror_info': '以下のHipジョイントと尻尾ロケータ位置は正しい状態です',
        'target_info': '以下のジョイントとロケータが対象',
        'func': checker_method.check_tail_locator_position_from_hip,
    },

    {
        'data_type': ['body', 'base_body', 'general_body', 'general_sexdiff_body', 'mini_body', 'mob_face_head', 'mob_hair_head', 'general_multi_area_body'],
        'label': 'ロケータのアトリビュートがロックされているかどうかの確認',
        'check_info': '以下のロケータのアトリビュートがロック確認',
        'error_info': '以下のロケータのアトリビュートがロックされています',
        'unerror_info': '以下のロケータのアトリビュートはロックされていません',
        'target_info': '以下のロケータが対象',
        'func': checker_method.check_lock_locator_node,
    },

    {
        'label': 'spec_infoのscale値が基準値内かどうかの確認',
        'check_info': '以下のspec_infoのscale値が正しいかどうかの確認',
        'error_info': '以下のspec_infoのscale値は正しくありません',
        'unerror_info': '以下のspec_infoのscale値は正しいです',
        'target_info': '以下のspec_infoのattrが対象',
        'error_select': False,
        'func': checker_method.check_spec_info_scale_value,
    },

    {
        'label': 'ロケーターのLocalPositionが全て0.0かの確認',
        'check_info': '以下のロケーターのLocalPositionが全て0.0かの確認',
        'error_info': '以下のロケーターのLocalPositionが全て0.0ではありません 正常値:全て0',
        'unerror_info': '以下のロケーターのLocalPositionの値は全て0.0です 正常値:全て0',
        'target_info': '以下のロケーターが対象',
        'error_select': False,
        'func': checker_method.check_locator_local_position_value,
    },

    {
        'data_type': ['head', 'mob_face_head'],
        'label': '特定のロケーターのPivotが全て0.0かの確認',
        'check_info': '以下のロケーターのPivotが全て0.0かの確認',
        'error_info': '以下のロケーターのPivotが全て0.0ではありません 正常値:全て0.0',
        'unerror_info': '以下のロケーターのPivotの値は全て0.0です 正常値:全て0.0',
        'target_info': '以下のロケーターが対象',
        'error_select': False,
        'func': checker_method.check_specific_locater_pivot_value_is_zero,
    },

    {
        'ui_type': 'frame',
        'label': 'ジョイント系',
    },

    {
        'label': 'ジョイントの存在確認',
        'check_info': '以下のジョイントの存在確認',
        'error_info': '以下のジョイントは存在してません',
        'unerror_info': '以下のジョイントは存在しています',
        'target_info': '以下のジョイントが対象',
        'error_select': False,
        'func': checker_method.check_joint_exist,
    },

    {
        'label': 'ジョイントの回転、スケール確認',
        'check_info': '以下の下層のジョイントの回転、スケール確認',
        'error_info': '以下のジョイントの回転、スケールは正しくありません',
        'unerror_info': '以下のジョイントの回転、スケールは正しい状態です',
        'target_info': '以下のジョイントが対象',
        'func': checker_method.check_joint_transform,
    },

    {
        'data_type': ['head', 'tail', 'mob_hair_head', 'mob_face_head'],
        'label': 'ワールド軸設定のジョイントの軸方向確認',
        'check_info': '以下の下層のジョイントの軸方向確認',
        'error_info': '以下のジョイントの軸方向は正しくありません',
        'unerror_info': '以下のジョイントの軸方向は正しい状態です',
        'target_info': '以下のジョイントが対象',
        'func': checker_method.check_world_joint_orient,
    },

    {
        'label': 'ローカル軸設定のジョイントの軸方向確認',
        'check_info': '以下の下層のジョイントの位置確認',
        'error_info': '以下のジョイントのジョイントオリエントがずれています',
        'unerror_info': '以下のジョイントのジョイントオリエントは正しい状態です',
        'target_info': '以下のジョイントが対象',
        'func': checker_method.check_local_joint_orient,
    },

    {
        'label': 'ジョイントの名前の重複確認',
        'check_info': '以下の下層のジョイントの名前の重複確認',
        'error_info': '以下のジョイントの名前は重複しています',
        'unerror_info': '以下のジョイントの名前は重複していません',
        'target_info': '以下のジョイントが対象',
        'func': checker_method.check_joint_overlap_naming,
    },

    # {
    #     'data_type': ['body', 'head', 'tail', 'mob_hair_head', 'mob_face_head'],
    #     'label': 'ジョイントの総数確認',
    #     'check_info': '以下のオブジェクトのジョイントの総数確認',
    #     'error_info': '以下のジョイントは規定値以上です',
    #     'unerror_info': '以下のジョイントは規定値以内です',
    #     'target_info': '以下のジョイントが対象',
    #     'target_count_info': 'ジョイントの総数',
    #     'func': checker_method.check_all_joint_count,

    # },

    {
        'data_type': ['body', 'base_body', 'general_body', 'general_sexdiff_body', 'head', 'mob_hair_head', 'mob_face_head', 'tail', 'general_tail', 'mini_face_head', 'mini_hair_head', 'mini_face_head', 'mini_body', 'mini_general_body', 'mini_tail', 'mini_general_tail', 'general_multi_area_body'],
        'label': 'クロス系以外のジョイントの総数確認',
        'check_info': '以下のオブジェクトのクロス系以外のジョイントの総数確認',
        'error_info': '以下の通りジョイント数が規定値を超えています',
        'unerror_info': '以下の通りジョイント数は規定値以内です',
        'target_info': '以下のジョイントが対象',
        'target_count_info': 'クロス系以外のジョイントの総数',
        'error_select': False,
        'unerror_select': False,
        'func': checker_method.check_nocloth_joint_count,
    },

    {
        'data_type': ['body', 'general_body', 'general_sexdiff_body', 'head', 'mob_hair_head', 'mob_face_head', 'tail', 'general_tail', 'mini_face_head', 'mini_hair_head', 'mini_face_head', 'mini_body', 'mini_general_body', 'mini_tail', 'mini_general_tail', 'general_multi_area_body'],
        'label': 'クロス系ジョイントの総数確認',
        'check_info': '以下のオブジェクトのクロス系ジョイントの総数確認',
        'error_info': '以下の通りジョイント数が規定値を超えています',
        'unerror_info': '以下の通りジョイント数は規定値以内です',
        'target_info': '以下のジョイントが対象',
        'target_count_info': 'クロスジョイントの総数',
        'error_select': False,
        'unerror_select': False,
        'func': checker_method.check_cloth_joint_count,
    },

    {
        'data_type': ['body', 'head', 'mini_hair_head', 'mini_body'],
        'label': 'Spジョイントの合算数確認(社内用)',
        'check_info': '以下のオブジェクトのSpジョイントの総数確認',
        'error_info': '以下の通りジョイント数が規定値を超えています',
        'unerror_info': '以下の通りジョイント数は規定値以内です',
        'target_info': '以下のジョイントが対象',
        'target_count_info': 'Spジョイントの総数',
        'error_select': False,
        'unerror_select': False,
        'target_select': False,
        'func': checker_method.check_cloth_joint_sum_count,
    },

    {
        'data_type': ['body', 'base_body', 'general_body', 'general_sexdiff_body', 'head', 'tail', 'mob_hair_head', 'mob_face_head', 'general_multi_area_body'],
        'label': 'ジョイントの命名規則の確認',
        'check_info': '以下のオブジェクトの命名規則の確認',
        'error_info': '以下のジョイントは命名規則に合っていません',
        'unerror_info': '以下のジョイントは命名規則に合致しています',
        'target_info': '以下のジョイントが対象',
        'target_count_info': '命名規則に合致していないジョイントの総数',
        'func': checker_method.check_joint_regex,
    },

    {
        'data_type': ['head', 'mob_hair_head'],
        'label': '耳のジョイントの位置の確認',
        'check_info': '以下の耳のジョイントの確認',
        'error_info': '以下の耳のジョイントの位置は正しくありません',
        'unerror_info': '以下の耳のジョイントの位置は正しい状態です',
        'target_info': '以下の耳のジョイントが対象',
        'func': checker_method.check_ear_joint_position,
    },

    {
        'data_type': ['body', 'base_body', 'general_body', 'general_sexdiff_body', 'general_multi_area_body'],
        'label': 'バストジョイントのオリエント確認',
        'check_info': '以下のオブジェクトのバストジョイントのオリエント確認',
        'error_info': '以下のバストジョイントのオリエントは正しくありません',
        'unerror_info': '以下のバストジョイントのオリエントは正しい状態です',
        'target_info': '以下のバストジョイントが対象',
        'func': checker_method.check_bust_joint_orient,
    },

    {
        'data_type': ['body', 'base_body', 'general_body', 'general_sexdiff_body', 'general_multi_area_body'],
        'label': 'バストジョイントの位置確認',
        'check_info': '以下のオブジェクトのバストジョイントの位置確認',
        'error_info': '以下のバストジョイントの位置は正しくありません',
        'unerror_info': '以下のバストジョイントの位置は正しい状態です',
        'target_info': '以下のバストジョイントが対象',
        'func': checker_method.check_bust_joint_position,
    },

    {
        'data_type': ['body', 'base_body', 'general_body', 'general_sexdiff_body', 'general_multi_area_body'],
        'label': 'Hipジョイントの位置確認',
        'check_info': 'Hipジョイントの位置確認',
        'error_info': 'Hipジョイントの位置は正しくありません',
        'unerror_info': 'Hipジョイントの位置は正しい状態です',
        'target_info': '以下のノードが対象',
        'func': checker_method.check_hip_joint_position,
    },

    {
        'label': 'ジョイントのアトリビュートがロックされていないかの確認',
        'check_info': 'ジョイントのアトリビュートがロックされていないかの確認',
        'error_info': 'ジョイントのアトリビュートがロックされています',
        'unerror_info': '以下のジョイントはアトリビュートがロックされていません',
        'target_info': '以下のジョイントが対象',
        'func': checker_method.check_lock_joint_node,
    },

    {
        'label': '歯のセグメントスケールがオフになっているかの確認',
        'check_info': '歯のセグメントスケールがオフになっているかの確認',
        'error_info': '歯のセグメントスケールがオンになっています',
        'unerror_info': '以下の歯のセグメントスケールがオフになっています',
        'target_info': '以下の歯のジョイントが対象',
        'func': checker_method.check_tooth_joint_segment_scale,
    },

    {
        'data_type': ['prop', 'toon_prop'],
        'label': '全ジョイントのセグメントスケールがオフになっているかの確認',
        'check_info': '全ジョイントのセグメントスケールがオフになっているかの確認',
        'error_info': '以下のジョイントのセグメントスケールがオフになっていません',
        'unerror_info': '以下のジョイントのセグメントスケールがオフになっています',
        'target_info': '以下のジョイントが対象',
        'func': checker_method.check_all_joint_segment_scale,
    },

    {
        'data_type': ['prop', 'toon_prop'],
        'label': 'トップノードのピボット位置が原点にあるか確認',
        'check_info': 'トップノードのピボット位置が原点にあるか確認',
        'error_info': '以下のノードが原点にありません',
        'unerror_info': '以下のノードが規定通り原点に存在しています',
        'target_info': '以下のノードが対象',
        'func': checker_method.check_top_node_pivot,
    },

    {
        'data_type': ['prop', 'toon_prop'],
        'label': 'Rootが原点にあるか確認',
        'check_info': 'Rootが原点にあるか確認',
        'error_info': 'Rootが原点にありません',
        'unerror_info': 'Rootは原点に存在しています',
        'target_info': '以下のジョイントが対象',
        'func': checker_method.check_root_translate,
    },

    {
        'data_type': ['prop', 'toon_prop'],
        'label': 'Rootのジョイントオリエント確認',
        'check_info': 'Rootのジョイントオリエントがすべて0か',
        'error_info': 'Rootのジョイントオリエントが0になっていません',
        'unerror_info': 'Rootのジョイントオリエントは0になっています',
        'target_info': '以下のジョイントが対象',
        'func': checker_method.check_root_jointorient,
    },

    {
        'label': 'バインドポーズが複数設定されていないか確認',
        'check_info': 'ジョイントのバインドポーズが複数設定されていないか',
        'error_info': 'バインドポーズが複数設定されているためリバインドを行って下さい',
        'unerror_info': 'バインドポーズの設定は一つのみです',
        'target_info': '以下のRootの子階層にあるジョイントが対象',
        'func': checker_method.check_single_bindpose,
    },

    {
        'ui_type': 'frame',
        'label': 'アウトライン系',
    },

    {
        'label': 'Outlineメッシュの存在確認',
        'check_info': '以下のOutlineメッシュの存在確認',
        'error_info': '以下のOutlineメッシュは存在しません',
        'unerror_info': '以下のOutlineメッシュは存在します',
        'target_info': '以下のメッシュが対象',
        'error_select': False,
        'func': checker_method.check_outline_exist,
    },

    {
        'label': 'Outlineメッシュの頂点位置確認',
        'check_info': '以下のOutlineメッシュの頂点位置確認',
        'error_info': '以下の頂点の位置は正しくありません',
        'unerror_info': '以下の頂点の位置は正しい状態です',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': checker_method.check_outline_vtx_position,
    },

    {
        'label': 'Outlineメッシュの頂点カラーの確認',
        'check_info': '以下のOutlineメッシュの頂点カラーの確認',
        'error_info': '以下の頂点の頂点カラーは正しくありません',
        'unerror_info': '以下の頂点の頂点カラーは正しい状態です',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': checker_method.check_outline_vtx_color,
    },

    {
        'label': 'Outlineメッシュのソフトエッジ確認',
        'check_info': '以下のOutlineメッシュのソフトエッジ確認',
        'error_info': '以下のエッジはソフトエッジではありません',
        'unerror_info': '以下のエッジはソフトエッジです',
        'target_info': '以下のエッジが対象',
        'view_type': 'component',
        'func': checker_method.check_outline_softedge,
    },

    {
        'ui_type': 'frame',
        'label': 'その他',
    },

    {
        'label': 'ネームスペースを含むノードの確認',
        'check_info': 'シーン全体のノード確認',
        'error_info': '以下のノードにネームスペースが含まれています',
        'unerror_info': '以下のノードはネームスペースが含まれません',
        'target_info': '以下のノードが対象',
        'func': checker_method.check_namespace,
    },

    {
        'label': 'キーが打たれていないかの確認',
        'check_info': '以下のトランスフォームの配下にキーがないかの確認',
        'error_info': '以下のトランスフォームにキーがあります',
        'unerror_info': '以下のトランスフォームにはキーがありません',
        'target_info': '以下のトランスフォームが対象',
        'func': checker_method.check_transform_with_no_key,
    },

    {
        'data_type': ['head', 'body', 'bdy0001_body', 'bdy0006_body', 'bdy0009_body', 'general_sexdiff_body', 'general_body', 'mob_face_head', 'mob_hair_head', 'general_multi_area_body'],
        'label': 'ロケーターに不要なバインドポーズがないかの確認',
        'check_info': '以下のロケーターに不要なバインドポーズがないかの確認',
        'error_info': '以下のロケーターに不要なバインドポーズがあります',
        'unerror_info': '以下のロケーターには不要なバインドポーズがありません',
        'target_info': '以下のロケーターが対象',
        'func': checker_method.check_locator_with_no_bindpose,
    },

    {
        'label': '不要なアニメーションレイヤーがないかの確認',
        'check_info': 'シーン全体のアニメーションレイヤーの確認',
        'error_info': '以下の不要なアニメーションレイヤーがあります',
        'unerror_info': '以下のシーンには不要なアニメーションレイヤーはありません',
        'target_info': '以下のシーンが対象',
        'func': checker_method.check_animation_layer,
    },

    {
        'label': 'Turtleノードが含まれていないか',
        'check_info': 'Turtleノードが含まれていないかの確認',
        'error_info': '以下のTurtleノードがあります',
        'unerror_info': '以下のシーンにはTurtleノードはありません',
        'target_info': '以下のシーンが対象',
        'func': checker_method.check_turtle_node,
    },

    {
        'label': '不要なディスプレイレイヤーがないかの確認',
        'check_info': 'ディスプレイレイヤーの確認',
        'error_info': '以下の不要なディスプレイレイヤーがあります',
        'unerror_info': '以下のシーンには不要なディスプレイレイヤーはありません',
        'target_info': '以下のシーンが対象',
        'func': checker_method.check_display_layer,
    },

    {
        'data_type': ['body', 'base_body', 'general_body', 'general_sexdiff_body', 'head', 'mob_face_head', 'mob_hair_head', 'general_multi_area_body'],
        'label': '特定のノードの位置が0かどうかの確認',
        'check_info': '以下の特定のノードの位置確認',
        'error_info': '以下の特定のノードの位置は正しくありません',
        'unerror_info': '以下の特定のノードの位置は正しい状態です',
        'target_info': '以下のノードが対象',
        'func': checker_method.check_particular_node_position,
    },

    {
        'data_type': ['body', 'base_body', 'general_body', 'general_sexdiff_body', 'head', 'mob_face_head', 'mob_hair_head', 'general_multi_area_body'],
        'label': '特定のノードのpivot位置が原点(0, 0, 0)かどうかの確認',
        'check_info': '以下の特定のノードのpivot位置確認',
        'error_info': '以下の特定のノードのpivot位置は正しくありません pivotは原点(0, 0, 0)にある必要があります',
        'unerror_info': '以下の特定のノードのpivot位置は正しい状態です',
        'target_info': '以下のノードが対象',
        'func': checker_method.check_particular_node_pivot_position,
    },

    {
        'label': 'unknownノードが含まれていないか',
        'check_info': 'unknownノードが含まれていないかの確認',
        'error_info': '以下のunknownノードがあります',
        'unerror_info': '以下のシーンにはunknownノードはありません',
        'target_info': '以下のシーンが対象',
        'func': checker_method.check_unknown_node,
    },

    {
        'label': 'unknownプラグインが含まれていないか',
        'check_info': 'unknownプラグインが含まれていないかの確認',
        'error_info': '以下のunknownプラグインがあります（チェック後に再発する場合はフェイシャル、頭部、身体、尻尾の関連モデルとそのリファレンス先のクリーニングも行ってください）',
        'unerror_info': '以下のシーンにはunknownプラグインはありません',
        'target_info': '以下のシーンが対象',
        'func': checker_method.check_unknown_plugin,
    },

    {
        'ui_type': 'frame',
        'label': 'フェイシャルターゲット系',
    },

    {
        'data_type': ['head', 'facial_target'],
        'label': 'キバ骨が存在しているか',
        'check_info': 'キバ骨が存在されているかの確認',
        'error_info': '以下のjointに不備があります',
        'unerror_info': '以下のjointは問題ありませんでした',
        'target_info': '以下のjointが対象',
        'error_select': False,
        'is_warning': True,
        'func': facial_target_check.check_kiba_bone,
    },

    {
        'data_type': ['head', 'facial_target'],
        'label': 'キバ骨のコントローラが存在しているか',
        'check_info': 'キバ骨のコントローラが正しいか確認',
        'error_info': '以下のコントローラに不備があります',
        'unerror_info': '以下のコントローラは問題ありませんでした',
        'target_info': '以下のコントローラが対象',
        'error_select': False,
        'is_warning': True,
        'func': facial_target_check.check_kiba_bone_ctrl,
    },

    {
        'data_type': ['head', 'facial_target'],
        'label': 'キバ骨(右)のベースキーが存在しているか',
        'check_info': 'キバ骨(右)のベースキーが存在しているか確認',
        'error_info': '以下のコントローラに不備があります',
        'unerror_info': '以下のコントローラは問題ありませんでした',
        'target_info': '以下のコントローラが対象',
        'error_select': False,
        'is_warning': True,
        'func': facial_target_check.check_kiba_bone_base_key,
    },

    {
        'data_type': ['head', 'facial_target'],
        'label': '対象のアニメーションレイヤにキバ骨コントローラー(右)が追加されているか',
        'check_info': 'Mouth_sub_01_R_Ctrlをアニメーションレイヤに追加しているか確認',
        'error_info': '以下のアニメーションレイヤに追加されていません',
        'unerror_info': '以下のアニメーションレイヤは問題ありませんでした',
        'target_info': '以下のアニメーションレイヤが対象',
        'error_select': False,
        'is_warning': True,
        'func': facial_target_check.check_kiba_bone_anim_layer,
    },

    {
        'data_type': ['head', 'facial_target'],
        'label': '歯のスケールオフセットは適正か',
        'check_info': '歯のスケールオフセットが1.0にセットされているか確認',
        'error_info': '以下のアトリビュートは適正ではありません(Scale値が1.0になっていません)',
        'unerror_info': '以下のアトリビュートは問題ありませんでした',
        'target_info': '以下のコントローラが対象',
        'error_select': False,
        'is_warning': True,
        'func': facial_target_check.check_tooth_scale_offset,
    },

    {
        'data_type': ['head', 'facial_target'],
        'label': '目がX、Yrange内に収まっているか',
        'check_info': '目がX, Yrange内に収まっているか確認',
        'error_info': '以下の目のアトリビュートはX, Yrangeを超えています',
        'unerror_info': '以下のアトリビュートは問題ありませんでした',
        'target_info': '以下のコントローラが対象',
        'error_select': False,
        'func': facial_target_check.check_eyes_within_range,
    },

    {
        'data_type': ['head', 'facial_target'],
        'label': 'base表情のままになっていないか',
        'check_info': 'base表情のままになっていないか確認',
        'error_info': '以下のframeでBase表情のままになっているパーツがあります',
        'unerror_info': '以下のキーは問題ありませんでした',
        'target_info': '以下のパーツが対象',
        'error_select': False,
        'func': facial_target_check.check_facial_keyframes,
    },

    {
        'data_type': ['head', 'facial_target'],
        'label': '左右シンメトリーな表情が正常に設定されているか',
        'check_info': '左右シンメトリーな表情が正常に設定されているか確認',
        'error_info': '以下のフレームでシンメトリーになっていないコントローラーがあります',
        'unerror_info': '以下のフレームは問題ありませんでした',
        'target_info': '以下のコントローラーが対象',
        'error_select': False,
        'func': facial_target_check.check_facial_symmetry,
    },

    # 以下キャラ個別のinfoを出力用
    {
        'ui_type': 'info',
        'label': 'info_ファイル概要',
        'func': checker_info.get_file_info,
    },

    {
        'ui_type': 'info',
        'label': 'info_モデル概要',
        'func': checker_info.get_model_info,
    },

    {
        'ui_type': 'info',
        'label': 'info_メッシュ情報',
        'func': checker_info.get_mesh_info,
    },

    {
        'data_type': ['head', 'body', 'base_body', 'tail', 'prop', 'toon_prop', 'mob_face_head', 'mob_hair_head'],
        'ui_type': 'info',
        'label': 'info_テクスチャ情報',
        'func': checker_info.get_texture_info,
    },

    {
        'ui_type': 'info',
        'label': 'info_マテリアル情報',
        'func': checker_info.get_material_info,
    },
]
