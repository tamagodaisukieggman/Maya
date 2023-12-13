# -*- coding: utf-8 -*-
u"""チェッカー (共通)

..
    END__CYGAMES_DESCRIPTION
"""

import maya.cmds as cmds
import maya.mel as mel
# import pymel.core as pm

# from mtku.maya.utils.node import MtkNode
# from mtku.maya.mtklog import MtkLog

import mtku.maya.menus.modeling.checkweights.command as checkweights

# logger = MtkLog(__name__)


class Validation(object):

    @classmethod
    def hierarchey_samename(cls, *args, **kwargs):
        u"""ヒエラルキー内での同一名

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True

        from mtku.maya.menus.file.checker.model.check_mesh import check_name_hierarchy

        node = kwargs.setdefault('node', None)

        error_nodes = check_name_hierarchy._check_name_hierarchy(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def hierarchey_root(cls, *args, **kwargs):
        u"""ヒエラルキーと名前 Root

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True

        from mtku.maya.menus.file.checker.model.check_mesh import check_name_hierarchy_root

        node = kwargs.setdefault('node', None)

        error_nodes = check_name_hierarchy_root._check_name_hierarchy_root(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def hierarchey_first(cls, *args, **kwargs):
        u"""ヒエラルキーと名前 第一階層

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True

        from mtku.maya.menus.file.checker.model.check_mesh import check_name_hierarchy_first

        node = kwargs.setdefault('node', None)

        error_nodes = check_name_hierarchy_first._check_name_hierarchy_first(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def hierarchey_second_env(cls, *args, **kwargs):
        u"""ヒエラルキーと名前 第二階層 env

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True

        from mtku.maya.menus.file.checker.model.check_mesh import check_name_hierarchy_second_env

        node = kwargs.setdefault('node', None)

        error_nodes = check_name_hierarchy_second_env._check_name_hierarchy_second_env(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def hierarchey_second_chara(cls, *args, **kwargs):
        u"""ヒエラルキーと名前 第二階層 chara

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True

        from mtku.maya.menus.file.checker.model.check_mesh import check_name_hierarchy_second_chara

        node = kwargs.setdefault('node', None)

        error_nodes = check_name_hierarchy_second_chara._check_name_hierarchy_second_chara(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_nface(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュ含む)から5角形以上のポリゴンを検出

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_ngon

        meshes = kwargs.setdefault('meshes', None)
        
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_ngon._check_mesh_ngon(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_lamina_faces(cls, *args, **kwargs):
        u"""2重ポリゴンが存在するか

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_lamina_faces

        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_lamina_faces._check_mesh_lamina_faces(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_non_manifold_vertices(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュ含む)から非多様体頂点を検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_non_manifold_vertices

        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_non_manifold_vertices._check_mesh_non_manifold_vertices(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_cvs_value(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュ含む)からCVsの値を検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_cvs

        meshes = kwargs.setdefault('meshes', None).split(",")
        error_nodes = check_mesh_cvs._check_mesh_cvs(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_invalid_vertices(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュ含む)から浮動頂点を検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_invalid_vertices

        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_invalid_vertices._check_mesh_invalid_vertices(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_mesh_size(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュ含む)から大きさを持たないメッシュを検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_bb_size

        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_bb_size._check_mesh_bb_size(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_mesh_colorset(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュ含む)からカラーセットを検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_colorset

        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_colorset._check_mesh_colorset(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_mesh_no_uvset(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュ含む)からUVセットがないメッシュを検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_uvset
        # reload(check_mesh_uvset)

        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_uvset._check_mesh_uvset(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_history(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュ含む)からヒストリーの残ったメッシュを検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_undelete_history
        
        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_undelete_history._check_mesh_undelete_history(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_transform_value(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュのトランスフォームノード)からフリーズされていないトランスフォームノードを検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_transform_freeze_transform

        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_transform_freeze_transform._check_transform_freeze_transform(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_scale_value(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュのトランスフォームノード)からスケールが1でないトランスフォームノードを検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_transform_scale_value
        # reload(check_transform_scale_value)

        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_transform_scale_value._check_transform_scale_value(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def material_name(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュのトランスフォームノード)から不正なマテリアル名を検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_material_name
        
        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_material_name._check_mesh_material_name(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def texture_size(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュのトランスフォームノード)から2のべぎ乗ではないテクスチャを検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_material_texture_size

        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_material_texture_size._check_mesh_material_texture_size(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def texture_name_path(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュのトランスフォームノード)からテクスチャファイル名とパスのチェック

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_material_texture_name

        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_material_texture_name._check_mesh_material_texture_name(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def joint_names(cls, *args, **kwargs):
        u"""選択ノード(が属するルートノード以下の)ジョイントノードの名前確認

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_name_joints

        node = kwargs.setdefault('node', None)

        error_nodes = check_name_joints._check_name_joints(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def joint_names_same_index(cls, *args, **kwargs):
        u"""選択ノード(が属するルートノード以下の)ジョイントノードの重複インデックス確認

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_name_same_index_joints

        node = kwargs.setdefault('node', None)

        error_nodes = check_name_same_index_joints._check_name_same_index_joints(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def joint_names_lr(cls, *args, **kwargs):
        u"""選択ノード(が属するルートノード以下の)ジョイントノードの名前確認 LR

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_name_joints_lr

        node = kwargs.setdefault('node', None)

        error_nodes = check_name_joints_lr._check_name_joints_lr(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def joint_transform_lr(cls, *args, **kwargs):
        u"""選択ノード(が属するルートノード以下の)ジョイントノードのポジション、回転 LR

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_transform_joint_lr

        node = kwargs.setdefault('node', None)

        error_nodes = check_transform_joint_lr._check_transform_joint_lr(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def check_transform_joint_Inverse_scale(cls, *args, **kwargs):
        u"""親のジョイントから見てインバーススケールが掛けられているかを検証

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_transform_joint_Inverse_scale

        node = kwargs.setdefault('node', None)

        error_nodes = check_transform_joint_Inverse_scale._check_transform_joint_Inverse_scale(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def reference_name(cls, *args, **kwargs):
        u"""読み込まれているリファレンスにネームスペースがついているかを検証

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_name_reference

        node = kwargs.setdefault('node', None)

        error_nodes = check_name_reference._check_name_reference(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def unknown_plugin(cls, *args, **kwargs):
        u"""不明なプラグインの削除

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_plugins

        node = kwargs.setdefault('node', None)
        error_nodes = check_plugins._check_plugins()

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def ctrl_set_geometorys(cls, *args, **kwargs):
        u"""「CtrlSet」のセットに含まれていない「_Ctrl」で終わるカーブの検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_set_ctrl_set

        node = kwargs.setdefault('node', None)
        error_nodes = check_set_ctrl_set._check_set_ctrl_set()

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def anim_jt_set(cls, *args, **kwargs):
        u"""「AnimJtSet」のセットに含まれていないジョイント検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_set_anim_jt_set

        node = kwargs.setdefault('node', None)
        error_nodes = check_set_anim_jt_set._check_set_anim_jt_set()

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def controller(cls, *args, **kwargs):
        u"""コントローラの不備をチェック

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_controller

        node = kwargs.setdefault('node', None)

        error_nodes = check_controller._check_controller(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def all_keyframe(cls, *args, **kwargs):
        u"""全てのトランスフォームノードにキーフレームがないかを確認

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_all_transform_key

        node = kwargs.setdefault('node', None)

        error_nodes = check_all_transform_key._check_all_transform_key(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def root_jnt_name_value(cls, *args, **kwargs):
        u"""ルートジョイントの名前と、値が入っているか検証

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_transform_rootjoint

        node = kwargs.setdefault('node', None)

        error_nodes = check_transform_rootjoint._check_transform_rootjoint(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_a_bind_pose(cls, *args, **kwargs):
        u"""バインドポーズが1つか

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}

        :example:
        >>> data_root = 'Z:/mtk_test/tools/maya/2017/modules/mtku/scripts/file/checker/chara/validation'
        >>> maya_scene = '{}/a_bind_pose.ma'.format(data_root)
        >>> cmds.file(maya_scene, f=True, o=True)
        u'Z:/mtk_test/tools/maya/2017/modules/mtku/scripts/file/checker/chara/validation/a_bind_pose.ma'
        >>> CharaValidation.has_a_bind_pose(node='true_model')
        {'result': True, 'error': []}
        >>> CharaValidation.has_a_bind_pose(node='false_model')
        {'result': False, 'error': [u'|false_joint']}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_transform_joint_bindpose
        
        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_transform_joint_bindpose._check_transform_joint_bindpose(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}
    @classmethod
    def has_many_bind(cls, *args, **kwargs):
        u"""1頂点に5ボーン以上のジョイントがバインドされているか

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_weight_influences
        
        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")
        error_nodes = check_mesh_weight_influences._check_mesh_weight_influences(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def is_skining_method_linear(cls, *args, **kwargs):
        u"""スキンクラスターの設定がClassicLinearになっているか

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_skincluster_method
        
        meshes = kwargs.setdefault('meshes', None)
        if meshes:
            meshes = meshes.split(",")

        error_nodes = check_mesh_skincluster_method._check_mesh_skincluster_method(meshes)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}



    @classmethod
    def has_skinnning(cls, *args, **kwargs):
        u"""スキニングされていないオブジェクトがないか検出

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []
        root_node = kwargs.setdefault('node', None)

        # マテリアルアサイン対象を選択
        # cmds.select(root_node, hi=True)

        meshes = cmds.ls(sl=True, type="mesh")
        nurbs_surfaces = cmds.ls(sl=True, type="nurbsSurface")

        target_objects = []
        target_objects.extend(meshes)
        target_objects.extend(nurbs_surfaces)

        # マテリアルがアサインされるオブジェクトがなければリターン
        if not target_objects:
            return {'result': True, 'error': []}

        for target_obj in target_objects:
            object_name = cmds.listRelatives(target_obj, p=True, f=True)[0]
            list_history = cmds.listHistory(target_obj, il=2)
            is_skinning = False
            for node in list_history:
                node_type = cmds.nodeType(node)
                if node_type == "skinCluster" or node_type == "jointCluster":
                    is_skinning = True
            if not is_skinning:
                error_nodes.append(object_name)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_unused_influence(cls, *args, **kwargs):
        u"""使用されていないインフルエンスの検出

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []
        root_node = kwargs.setdefault('node', None)

        # マテリアルアサイン対象を選択
        # cmds.select(root_node, hi=True)

        joints = cmds.ls(sl=True, type="joint")

        for node in joints:
            list_connections = cmds.listConnections(node, type="skinCluster")
            if not list_connections:
                error_nodes.append(node)

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def is_required_rig_sets_exist(cls, *args, **kwargs):
        u"""'AllSet', 'CtrlSet', 'AnimJtSet'が存在するかの確認

                :param args: None
                :param kwargs: 'node' ルートノード
                :return: {'result': bool, 'error': エラーノードのリスト}
                """
        required_sets = (
            'AllSet',
            'CtrlSet',
            'AnimJtSet',
        )
        print(cmds.ls(required_sets, type='objectSet'), required_sets)
        if set(cmds.ls(required_sets, type='objectSet')) == set(required_sets):
            return {'result': True, 'error': []}
        else:
            errors = cmds.ls(required_sets, type='objectSet') if cmds.ls(required_sets, type='objectSet') else required_sets
            
            return {'result': False, 'error': errors}

    @classmethod
    def is_topnode_root(cls, *args, **kwargs):
        u"""'root'がトップノードであるかの確認

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        import re
        result = False
        error = cmds.ls(sl=True)

        for node in cmds.ls(assemblies=True):
            hit = re.match(r'[|]?root$', node)
            if hit:
                result = True
                error = []

        return {'result': result, 'error': error}
        

    @classmethod
    def has_required_transform_in_root(cls, *args, **kwargs):
        u"""rootの階層下にmodel/ rigが存在するか

        :param args: None
        :param kwargs: 'node' ルートノード
        :return: {'result': bool, 'error': エラーノードのリスト}
        """

        result = True
        error = []

        required_transform = (
            'rig',
            'model',
        )
        
        root_node = kwargs.setdefault('node', None)
        
        if not cls.is_topnode_root()['result']:
            result = False
            error.extend(cmds.ls(sl=True))

        if root_node == "root":
            if not list(required_transform) == cmds.listRelatives(cmds.ls('root')[0], children=True):
                result = False
                error.extend(set(cmds.listRelatives(cmds.ls('root')[0], children=True)) & set(required_transform))

        return {'result': result, 'error': error}