

class Validation(object):

    @classmethod
    def has_nface(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュ含む)から5角形以上のポリゴンを検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_ngon
        # reload(check_mesh_ngon)

        _c = check_mesh_ngon.Check_Mesh_Ngon()
        error_nodes = _c.do()

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def has_lamina_faces(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュ含む)から2重ポリゴンを検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_lamina_faces
        # reload(check_mesh_lamina_faces)

        _c = check_mesh_lamina_faces.Check_Mesh_Lamina_Faces()
        error_nodes = _c.do()

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
        # reload(check_mesh_non_manifold_vertices)

        _c = check_mesh_non_manifold_vertices.Check_Mesh_Non_Manifold_Vertices()
        error_nodes = _c.do()

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
        # reload(check_mesh_cvs)

        _c = check_mesh_cvs.Check_Mesh_Cvs()
        error_nodes = _c.do()

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
        # reload(check_mesh_invalid_vertices)

        _c = check_mesh_invalid_vertices.Check_Mesh_Invalid_Vertices()
        error_nodes = _c.do()

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
        # reload(check_mesh_bb_size)

        _c = check_mesh_bb_size.Check_Mesh_BB_Size()
        error_nodes = _c.do()

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
        # reload(check_mesh_colorset)

        _c = check_mesh_colorset.Check_Mesh_Colorset()
        error_nodes = _c.do()

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

        _c = check_mesh_uvset.Check_Mesh_Uvset()
        error_nodes = _c.do()

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
        # reload(check_mesh_undelete_history)

        _c = check_mesh_undelete_history.Check_Mesh_Undelete_History()
        error_nodes = _c.do()

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
        # reload(check_transform_freeze_transform)

        _c = check_transform_freeze_transform.Check_Transform_Freeze_Transform()
        error_nodes = _c.do()

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

        _c = check_transform_scale_value.Check_Transform_Scale_Value()
        error_nodes = _c.do()

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
        # reload(check_mesh_material_name)

        _c = check_mesh_material_name.Check_Mesh_Material_Name()
        error_nodes = _c.do()

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}

    @classmethod
    def texture_name(cls, *args, **kwargs):
        u"""選択ノード(子ノードのメッシュのトランスフォームノード)から2のべぎ乗ではないテクスチャを検出

        :param args: None
        :param kwargs: None
        :return: {'result': bool, 'error': エラーノードのリスト}
        """
        result = True
        error_nodes = []

        from mtku.maya.menus.file.checker.model.check_mesh import check_mesh_material_texture_size
        # reload(check_mesh_material_texture_size)

        _c = check_mesh_material_texture_size.Check_Mesh_Material_Texture_Size()
        error_nodes = _c.do()

        if error_nodes:
            result = False

        return {'result': result, 'error': error_nodes}