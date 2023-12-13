import maya.cmds as cmds


class MtkHistory(object):

    @classmethod
    def _get_skin_cluster(cls, mesh):
        u"""skinClusterの取得

        :param mesh: メッシュ
        :return: skinCluster

        :example:
        >>> _get_skin_cluster('mesh|body|body|bodyShape')
        u'skinCluster48'
        """
        skin_clusters = cmds.ls(cmds.listHistory(mesh), typ='skinCluster')
        if skin_clusters:
            return skin_clusters[0]
        else:
            return []

    @classmethod
    def _get_root_joint(cls, mesh):
        u"""ルートジョイントの取得

        :param mesh: メッシュ
        :return: ルートジョイント

        :example:
        >>> _get_root_joint('mesh|body|body|bodyShape')
        u'rootBindJt'
        """
        skin_cluster = cls._get_skin_cluster(mesh)
        if not skin_cluster:
            return

        joints = cmds.ls(cmds.skinCluster(skin_cluster, q=True, influence=True), long=True)

        if not joints:
            return

        root_joint = None

        for _node in joints[0].split("|"):
            if _node and cmds.objectType(_node) == "joint":
                root_joint = _node
                break

        return root_joint

    @classmethod
    def _get_max_influence(cls, skin_cluster):
        u"""Max Influenceの取得

        :param skin_cluster: skinCluster
        :return: Max Influence
        """
        return cmds.getAttr('{}.maxInfluences'.format(skin_cluster))

    @classmethod
    def _smooth_bind(cls, mesh, root_joint, max_influence):
        u"""スムーズバインド

        :param mesh: メッシュ
        :param root_joint: root joint
        :param max_influence: Max Influence
        """
        cmds.skinCluster(mesh, root_joint, omi=True, bm=1, mi=max_influence)

    @classmethod
    def _copy_skin_weights(cls, src_mesh, dst_mesh):
        u"""ウェイトのコピー

        :param src_mesh: コピー元のメッシュ
        :param dst_mesh:  コピー先のメッシュ
        """
        cmds.select([src_mesh, dst_mesh])
        cmds.copySkinWeights(sa='closestPoint', ia='closestJoint', nm=True)

    @classmethod
    def _bind_and_copy_weights(cls, source_mesh, forward_mesh):
        u"""スムーズバインドしてウェイトをコピー

        :param source_mesh: コピー元のメッシュ
        :param forward_mesh:  コピー先のメッシュ
        """
        # コピー元のメッシュからジョイント、スキンクラスタを取得
        root_joint = cls._get_root_joint(source_mesh)

        skin_cluster = cls._get_skin_cluster(source_mesh)

        # skinning meshではない場合、複製して終了
        if not skin_cluster:
            return

        # スキンクラスタの最大インフルエンス数の取得
        max_influence = cls._get_max_influence(skin_cluster)

        # コピー先のメッシュをスムーズバインド、ウェイトコピー
        cls._smooth_bind(forward_mesh, root_joint, max_influence)
        cls._copy_skin_weights(source_mesh, forward_mesh)



if __name__ == '__main__':
    import doctest
    import maya.standalone

    maya.standalone.initialize(name='python')
    doctest.testmod()
