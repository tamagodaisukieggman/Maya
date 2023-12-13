# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from importlib import reload
except:
    pass

from . import checker_method as cm
from . import checker_info as ci

reload(cm)
reload(ci)


param_value_list = [

    {
        'enable': False,

        'ui_type': 'checker, frameが使用可能 未指定はchecker',

        'data_type': 'リストで指定 head,mob_face_head,mob_hair_head,body,base_body,tail,general_tail,prop,mini_face_head,mini_hair_head,mini_body,が指定可能',

        'label': 'UIに表示されるラベル名',
        'check_info': '情報ボタンを押したときのテキスト',
        'error_info': 'エラー表示ボタンを押したときのテキスト',
        'unerror_info': '正常ボタンを押したときのテキスト',
        'target_info': '対象表示ボタンを押したときのテキスト',

        'view_type': '対象表示ボタンを押したときのテキスト',

        'error_view': 'エラー表示ボタンの表示',
        'error_select': 'エラー表示ボタンの表示',
        'error_fix': 'エラー表示ボタンの表示',

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
        'func': cm.check_directory_exist,
    },

    {
        'ui_type': 'frame',
        'label': 'メッシュ系',
    },

    {
        'label': 'メッシュの存在確認',
        'check_info': '以下のメッシュの存在確認',
        'error_info': '以下のメッシュの存在しません',
        'unerror_info': '以下のメッシュの存在します',
        'target_info': '以下のメッシュが対象',
        'error_select': False,
        'func': cm.check_mesh_exist,
    },

    {
        'label': 'メッシュの命名規則の確認',
        'check_info': '以下のメッシュの命名規則の確認',
        'error_info': '以下のメッシュは誤った名前です',
        'unerror_info': '以下のメッシュは正しい名前です',
        'target_info': '以下のメッシュが対象',
        'error_select': False,
        'func': cm.check_mesh_naming_rule,
    },

    {
        'label': 'メッシュの名前の重複確認',
        'check_info': '以下のメッシュの名前の重複確認',
        'error_info': '以下のメッシュの名前は重複しています',
        'unerror_info': '以下のメッシュの名前は重複していません',
        'target_info': '以下のメッシュが対象',
        'error_select': False,
        'func': cm.check_mesh_name_overlap,
    },

    # {
    #     'label': 'メッシュのポリゴン数確認',
    #     'check_info': '以下のメッシュのポリゴン数を確認',
    #     'error_info': '以下の通りメッシュのポリゴン数が規定値を超えています',
    #     'unerror_info': '以下の通りメッシュのポリゴン数は規定内です',
    #     'target_info': '以下のメッシュが対象',
    #     'error_select': False,
    #     'unerror_select': False,
    #     'target_count_info': 'ポリゴン数',
    #     'func': cm.check_mesh_poly_count,
    # },

    {
        'label': 'メッシュの移動、回転、スケール確認',
        'check_info': '以下のメッシュの移動、回転、スケール確認',
        'error_info': '以下のメッシュの移動、回転、スケールは正しくありません',
        'unerror_info': '以下のメッシュの移動、回転、スケールは正しい状態です',
        'target_info': '以下のメッシュが対象',
        'func': cm.check_mesh_transform,
    },

    {
        'label': 'メッシュのマテリアルの種類の確認',
        'check_info': '以下のメッシュのマテリアルが正しい種類かどうかの確認',
        'error_info': '以下のメッシュに割り当てられたマテリアルは誤った種類です',
        'unerror_info': '以下のメッシュに割り当てられたマテリアルは正しい種類です',
        'target_info': '以下のメッシュが対象',
        'func': cm.check_mesh_material_type,
    },

    {
        'label': 'メッシュのshapeノードの名前の確認',
        'check_info': '以下のメッシュのshapeノードが正しい名前かどうかの確認',
        'error_info': '以下のメッシュのshapeノードは誤った名前です',
        'unerror_info': '以下のメッシュのshapeノードは正しい名前です',
        'target_info': '以下のメッシュが対象',
        'func': cm.check_mesh_shape_name,
    },

    {
        'label': 'メッシュの中間ノード(Orig)の数の確認',
        'check_info': '以下のメッシュの中間ノード(Orig)の数の確認',
        'error_info': '以下のメッシュに中間ノード(Orig)が複数存在します',
        'unerror_info': '以下のメッシュの中間ノード(Orig)の数は正しいです',
        'target_info': '以下のメッシュが対象',
        'func': cm.check_mesh_intermeditate_count,
    },

    {
        'label': 'メッシュの中間ノードの名前の確認',
        'check_info': '以下のメッシュの中間ノードの名前の確認',
        'error_info': '以下のメッシュの中間ノードは誤った名前ですす',
        'unerror_info': '以下のメッシュの中間ノードは正しい名前です',
        'target_info': '以下のメッシュの中間ノードが対象',
        'func': cm.check_mesh_intermediate_name,
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
        'func': cm.check_mesh_cleanup,
        'func_arg': ['more4side']
    },

    {
        'label': '凹型フェース確認',
        'check_info': '以下のメッシュの凹型フェース確認',
        'error_info': '以下のフェースは凹型フェースです',
        'unerror_info': '以下のフェースは凹型フェースではありません',
        'target_info': '以下のフェースが対象',
        'func': cm.check_mesh_cleanup,
        'func_arg': ['concave']
    },

    {
        'label': '穴のあるフェース確認',
        'check_info': '以下のメッシュの穴のあるフェース確認',
        'error_info': '以下のフェースは穴のあるフェースです',
        'unerror_info': '以下のフェースは穴のあるフェースではありません',
        'target_info': '以下のフェースが対象',
        'func': cm.check_mesh_cleanup,
        'func_arg': ['hole']
    },

    {
        'label': 'ラミナフェース確認',
        'check_info': '以下のメッシュのラミナフェース確認',
        'error_info': '以下のフェースはラミナフェースです',
        'unerror_info': '以下のフェースはラミナフェースではありません',
        'target_info': '以下のフェースが対象',
        'func': cm.check_mesh_cleanup,
        'func_arg': ['lamina']
    },

    {
        'label': '非多様体フェース確認',
        'check_info': '以下のメッシュの非多様体フェース確認',
        'error_info': '以下のフェースは非多様体フェースです',
        'unerror_info': '以下のフェースは非多様体フェースではありません',
        'target_info': '以下のフェースが対象',
        'func': cm.check_mesh_cleanup,
        'func_arg': ['nonmanifold']
    },

    {
        'label': '長さが0のエッジ確認',
        'check_info': '以下のメッシュの長さが0のエッジ確認',
        'error_info': '以下のエッジは長さが0のエッジです',
        'unerror_info': '以下のエッジは長さが0のエッジではありません',
        'target_info': '以下のエッジが対象',
        'func': cm.check_mesh_cleanup,
        'func_arg': ['zero_edge']
    },

    {
        'ui_type': 'frame',
        'label': '頂点カラー系',
    },

    {
        'data_type': ['avatar', 'unit', 'weapon'],
        'label': '頂点カラーのunsharedの確認',
        'check_info': '以下のメッシュの頂点カラーのunsharedの確認',
        'error_info': '以下の頂点の頂点カラーはunsharedです',
        'unerror_info': '以下の頂点の頂点カラーはunsharedではありません',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': cm.check_mesh_unshared_vertex_color,
    },

    # {
    #     'label': '頂点カラーが小数点2桁以下かの確認',
    #     'check_info': '以下のメッシュの頂点カラーが小数点2桁以下かの確認',
    #     'error_info': '以下の頂点の頂点カラーは小数点2桁以下ではありません',
    #     'unerror_info': '以下の頂点の頂点カラーは小数点2桁以下です',
    #     'target_info': '以下の頂点が対象',
    #     'view_type': 'component',
    #     'func': cm.check_mesh_vertex_color_round,
    # },

    {
        'label': '頂点カラーのアルファの確認',
        'check_info': '以下のメッシュの頂点カラーのアルファの確認',
        'error_info': '以下の頂点の頂点カラーのアルファ値は1ではありません',
        'unerror_info': '以下の頂点の頂点カラーのアルファ値は1です',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': cm.check_mesh_vertex_color_alpha,
    },

    # {
    #     'label': '頂点カラーのノイズ確認',
    #     'check_info': '以下のメッシュの頂点カラーのノイズ確認',
    #     'error_info': '以下の頂点の頂点カラーはノイズがあります',
    #     'unerror_info': '以下の頂点の頂点カラーはノイズはありません',
    #     'target_info': '以下の頂点が対象',
    #     'view_type': 'component',
    #     'func': cm.check_mesh_vertex_color_noisy,
    # },

    {
        'label': 'カラーセット数の確認',
        'check_info': '以下のメッシュのカラーセット数の確認',
        'error_info': '以下のメッシュのカラーセット数は正しくありません',
        'unerror_info': '以下のメッシュのカラーセット数は規定値です',
        'target_info': '以下のメッシュが対象',
        'view_type': 'colorset',
        'func': cm.check_mesh_colorset,
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
        'func': cm.check_mesh_skin_influence,
    },

    {
        'label': 'ウェイト精度少数2桁以内かの確認',
        'check_info': '以下のメッシュのウェイト精度少数2桁以内かの確認',
        'error_info': '以下の頂点のウェイトは少数2桁以内ではありません',
        'unerror_info': '以下の頂点のウェイトは少数2桁以内です',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': cm.check_mesh_skin_round,
    },

    {
        'label': '不正なジョイントにウェイトがないかの確認',
        'check_info': '以下のジョイントにウェイトがないかの確認',
        'error_info': '以下の頂点は不正なジョイントにウェイトがあります',
        'unerror_info': '以下の頂点は不正なジョイントにウェイトがありません',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': cm.check_joint_with_no_skin,
    },

    # {
    #     'label': 'メッシュに不要なスキンがないかの確認',
    #     'check_info': '以下のメッシュに不要なスキンがないかの確認',
    #     'error_info': '以下のメッシュには不要なスキンがあります',
    #     'unerror_info': '以下のメッシュには不要なスキンがありません',
    #     'target_info': '以下のメッシュが対象',
    #     'func': cm.check_mesh_with_no_skin,
    # },

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
        'func': cm.check_mesh_uvset,
    },

    {
        'label': 'UV座標の確認',
        'check_info': '以下のメッシュのUV座標の確認',
        'error_info': '以下のUVのUV座標は正しくありません',
        'unerror_info': '以下のUVのUV座標は正しい状態です',
        'target_info': '以下のUVが対象',
        'view_type': 'uv',
        'func': cm.check_mesh_uv_coordinate,
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
        'func': cm.check_material_exist,
        'error_select': False,
    },

    {
        'label': 'マテリアルの命名規則の確認',
        'check_info': '以下のマテリアルの命名規則の確認',
        'error_info': '以下のマテリアルは誤った名前です',
        'unerror_info': '以下のマテリアルは正しい名前です',
        'target_info': '以下のマテリアルが対象',
        'func': cm.check_material_naming_rule,
        'error_select': False,
    },

    {
        'label': 'マテリアルの割り当て確認',
        'check_info': '以下のマテリアルの割り当て確認',
        'error_info': '以下のマテリアルの割り当てが正しくありません',
        'unerror_info': '以下のマテリアルは正しくメッシュに割り当てられています',
        'target_info': '以下のマテリアルが対象',
        'func': cm.check_material_link,
        'error_select': False,
    },

    {
        # 汎用尻尾、素体はテクスチャ系チェックを行わない
        'ui_type': 'frame',
        'label': 'テクスチャ系',
    },

    {
        'data_type': ['unit', 'avatar', 'weapon', 'prop', 'summon', 'enemy'],
        'label': 'テクスチャの存在確認',
        'check_info': '以下のテクスチャの存在確認',
        'error_info': '以下のテクスチャは存在していません',
        'unerror_info': '以下のテクスチャは存在しています',
        'target_info': '以下のテクスチャが対象',
        'view_type': 'explorer',
        'error_select': False,
        'unerror_select': False,
        'target_select': False,
        'func': cm.check_texture_exist,
        'func_arg': ['texture']
    },

    # {
    #     'data_type': ['head', 'body', 'tail', 'prop', 'mob_face_head', 'mob_hair_head'],
    #     'label': '編集用テクスチャの存在確認',
    #     'check_info': '以下の編集用テクスチャの存在確認',
    #     'error_info': '以下の編集用テクスチャは存在していません',
    #     'unerror_info': '以下の編集用テクスチャは存在しています',
    #     'target_info': '以下のテクスチャが対象',
    #     'view_type': 'explorer',
    #     'error_select': False,
    #     'unerror_select': False,
    #     'target_select': False,
    #     'func': cm.check_texture_exist,
    #     'func_arg': ['psd']
    # },

    {
        'data_type': ['unit', 'avatar', 'weapon', 'prop', 'summon', 'enemy'],
        'label': 'テクスチャのサイズ確認',
        'check_info': '以下のテクスチャのサイズ確認',
        'error_info': '以下のテクスチャのサイズは正しくありません',
        'unerror_info': '以下のテクスチャのサイズは正しい状態です',
        'target_info': '以下のテクスチャが対象',
        'view_type': 'explorer',
        'error_select': False,
        'unerror_select': False,
        'target_select': False,
        'func': cm.check_texture_size,
        'func_arg': ['texture']
    },

    # {
    #     'data_type': ['head', 'body', 'tail', 'prop', 'mob_face_head', 'mob_hair_head'],
    #     'label': '編集用テクスチャのサイズ確認',
    #     'check_info': '以下の編集用テクスチャのサイズ確認',
    #     'error_info': '以下の編集用テクスチャのサイズは正しくありません',
    #     'unerror_info': '以下の編集用テクスチャのサイズは正しい状態です',
    #     'target_info': '以下の編集用テクスチャが対象',
    #     'view_type': 'explorer',
    #     'error_select': False,
    #     'unerror_select': False,
    #     'target_select': False,
    #     'func': cm.check_texture_size,
    #     'func_arg': ['psd']
    # },

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
        'func': cm.check_locator_exist,
    },

    {
        'label': 'ロケータの命名規則の確認',
        'check_info': '以下のロケータの命名規則の確認',
        'error_info': '以下のロケータは誤った名前です',
        'unerror_info': '以下のロケータは正しい名前です',
        'target_info': '以下のロケータが対象',
        'func': cm.check_locator_naming_rule,
    },

    # {
    #     'label': 'ロケータの移動、回転、スケールの確認',
    #     'check_info': '以下のロケータの移動、回転、スケールの確認',
    #     'error_info': '以下のロケータの移動、回転、スケールは正しくありません',
    #     'unerror_info': '以下のロケータの移動、回転、スケールは正しい状態です',
    #     'target_info': '以下のロケータが対象',
    #     'func': cm.check_locator_transform,
    # },

    # {
    #     'data_type': ['head'],
    #     'label': '目のジョイントとロケータ位置の確認',
    #     'check_info': '以下の目のジョイントとロケータ位置の確認',
    #     'error_info': '以下の目のジョイントとロケータ位置は正しくありません',
    #     'unerror_info': '以下の目のジョイントとロケータ位置は正しい状態です',
    #     'target_info': '以下のジョイントとロケータが対象',
    #     'func': cm.check_eye_locator_position,
    # },

    {
        'data_type': ['unit', 'avatar'],
        'label': 'ロケータのアトリビュートがロックされているかどうかの確認',
        'check_info': '以下のロケータのアトリビュートがロック確認',
        'error_info': '以下のロケータのアトリビュートがロックされています',
        'unerror_info': '以下のロケータのアトリビュートはロックされていません',
        'target_info': '以下のロケータが対象',
        'func': cm.check_lock_locator_node,
    },

    {
        'label': 'ロケータの回転の確認',
        'check_info': '以下のロケータの回転の確認',
        'error_info': '以下のロケータの回転は正しくありません',
        'unerror_info': '以下のロケータの回転は正しい状態です',
        'target_info': '以下のロケータが対象',
        'func': cm.check_locator_rotation,
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
        'func': cm.check_joint_exist,
    },

    {
        'label': 'ジョイントの命名規則の確認',
        'check_info': '以下のジョイントの命名規則の確認',
        'error_info': '以下のジョイントは誤った名前です',
        'unerror_info': '以下のジョイントは正しい名前です',
        'target_info': '以下のジョイントが対象',
        'error_select': False,
        'func': cm.check_joint_naming_rule,
    },

    {
        'label': 'ジョイントの回転、スケール確認',
        'check_info': '以下の下層のジョイントの回転、スケール確認',
        'error_info': '以下のジョイントの回転、スケールは正しくありません',
        'unerror_info': '以下のジョイントの回転、スケールは正しい状態です',
        'target_info': '以下のジョイントが対象',
        'func': cm.check_joint_transform,
    },

    # {
    #     'data_type': ['head', 'tail', 'mob_hair_head', 'mob_face_head'],
    #     'label': 'ジョイントの軸方向確認',
    #     'check_info': '以下の下層のジョイントの軸方向確認',
    #     'error_info': '以下のジョイントの軸方向は正しくありません',
    #     'unerror_info': '以下のジョイントの軸方向は正しい状態です',
    #     'target_info': '以下のジョイントが対象',
    #     'func': cm.check_joint_orient,
    # },

    {
        'label': 'ジョイントの名前の重複確認',
        'check_info': '以下の下層のジョイントの名前の重複確認',
        'error_info': '以下のジョイントの名前は重複しています',
        'unerror_info': '以下のジョイントの名前は重複していません',
        'target_info': '以下のジョイントが対象',
        'func': cm.check_joint_overlap_naming,
    },

    {
        'data_type': ['unit', 'avatar'],
        'label': 'セカンダリジョイント数の確認',
        'check_info': '以下の下層のセカンダリジョイント数の確認',
        'error_info': '以下のジョイントは上限数を超過しています',
        'unerror_info': '以下のジョイントは上限数以下です',
        'target_info': '以下のジョイントが対象',
        'error_select': False,
        'unerror_select': False,
        'target_select': False,
        'func': cm.check_ex_joint_count,
    },

    # {
    #     'label': 'ジョイントのアトリビュートがロックされているかの確認',
    #     'check_info': 'ジョイントのアトリビュートがロックされているかの確認',
    #     'error_info': 'ジョイントのアトリビュートがロックされています',
    #     'unerror_info': '以下のジョイントはアトリビュートがロックされていません',
    #     'target_info': '以下のジョイントが対象',
    #     'func': cm.check_lock_joint_node,
    # },

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
        'func': cm.check_outline_exist,
    },

    {
        'label': 'Outlineメッシュの頂点位置確認',
        'check_info': '以下のOutlineメッシュの頂点位置確認',
        'error_info': '以下の頂点の位置は正しくありません',
        'unerror_info': '以下の頂点の位置は正しい状態です',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': cm.check_outline_vtx_position,
    },

    {
        'label': 'Outlineメッシュの頂点カラーの確認',
        'check_info': '以下のOutlineメッシュの頂点カラーの確認',
        'error_info': '以下の頂点の頂点カラーは元メッシュと同じではありません',
        'unerror_info': '以下の頂点の頂点カラーは元メッシュと同じです',
        'target_info': '以下の頂点が対象',
        'view_type': 'component',
        'func': cm.check_outline_vtx_color,
    },

    {
        'label': 'Outlineメッシュのソフトエッジ確認',
        'check_info': '以下のOutlineメッシュのソフトエッジ確認',
        'error_info': '以下のエッジはソフトエッジではありません',
        'unerror_info': '以下のエッジはソフトエッジです',
        'target_info': '以下のエッジが対象',
        'view_type': 'component',
        'func': cm.check_outline_softedge,
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
        'func': cm.check_namespace,
    },

    {
        'label': 'キーが打たれていないかの確認',
        'check_info': '以下のトランスフォームの配下にキーがないかの確認',
        'error_info': '以下のトランスフォームにキーがあります',
        'unerror_info': '以下のトランスフォームにはキーがありません',
        'target_info': '以下のトランスフォームが対象',
        'func': cm.check_transform_with_no_key,
    },

    {
        'label': 'バインドポーズが複数存在しないかの確認',
        'check_info': '以下のジョイントのバインドポーズの数の確認',
        'error_info': '以下のジョイントには複数のバインドポーズが存在します',
        'unerror_info': '以下のジョイントには不要なバインドポーズはありません',
        'target_info': '以下のジョイントが対象',
        'func': cm.check_multiple_bindpose,
    },

    {
        'label': '不要なアニメーションレイヤーがないかの確認',
        'check_info': 'シーン全体のアニメーションレイヤーの確認',
        'error_info': '以下の不要なアニメーションレイヤーがあります',
        'unerror_info': '以下のシーンには不要なアニメーションレイヤーはありません',
        'target_info': '以下のシーンが対象',
        'func': cm.check_animation_layer,
    },

    # {
    #     'data_type': ['body', 'base_body'],
    #     'label': '特定のノードの位置が0かどうかの確認',
    #     'check_info': '以下の特定のノードの位置確認',
    #     'error_info': '以下の特定のノードの位置は正しくありません',
    #     'unerror_info': '以下の特定のノードの位置は正しい状態です',
    #     'target_info': '以下のノードが対象',
    #     'func': cm.check_particular_node_position,
    # },

    {
        'label': '特定のノードのpivot位置が原点かどうかの確認',
        'check_info': '以下の特定のノードの位置確認',
        'error_info': '以下の特定のノードの位置は正しくありません',
        'unerror_info': '以下の特定のノードの位置は正しい状態です',
        'target_info': '以下のノードが対象',
        'func': cm.check_particular_node_pivot_position,
    },

    # 以下キャラ個別のinfoを出力用
    {
        'ui_type': 'info',
        'label': 'info_ファイル概要',
        'func': ci.get_file_info,
    },

    {
        'ui_type': 'info',
        'label': 'info_モデル概要',
        'func': ci.get_model_info,
    },

    {
        'ui_type': 'info',
        'label': 'info_メッシュ情報',
        'func': ci.get_mesh_info,
    },

    # {
    #     'data_type': ['head', 'body', 'base_body', 'tail', 'prop', 'mob_face_head', 'mob_hair_head'],
    #     'ui_type': 'info',
    #     'label': 'info_テクスチャ情報',
    #     'func': ci.get_texture_info,
    # },

    # {
    #     'ui_type': 'info',
    #     'label': 'info_マテリアル情報',
    #     'func': ci.get_material_info,
    # },
]
