# -*- coding: utf-8 -*-
u"""
カレントの UV マップチャンネルに対して処理します。
選択されている１つのメッシュに対して処理します。

"""
import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel
from logging import getLogger

logger = getLogger(__name__)


class CheckUVPaddingCmd(object):

    @classmethod
    def _get_uv_shells(cls, selection):
        u"""UV Shell 取得

        :param selection: str
        :return: list (uv shells min IDs)
        """
        result = []

        all_uv = cmds.polyListComponentConversion(selection, tuv=True)
        all_uv = cmds.filterExpand(all_uv, sm=35)

        for uv in all_uv:

            cmds.select(uv)
            mel.eval('polySelectBorderShell 0;')
            shell = cmds.ls(sl=True)
            shell = cmds.filterExpand(shell, sm=35)
            if shell[0] not in result:
                result.append(shell[0])

        cmds.select(cl=True)

        return result

    @classmethod
    def _get_uv_from_selection(cls, selection):
        u"""選択 UV が属する UV シェルを取得。

        :param selection: str
        :return: list
        """
        cmds.select(selection, r=True)
        mel.eval('polySelectBorderShell 0;')
        uv_shells = cmds.ls(sl=True, l=True)
        cmds.select(cl=True)
        uvs = cmds.filterExpand(uv_shells, sm=35)
        return uvs

    @classmethod
    def _verify_overlap_faces(cls, shell_padding, uv_shell, all_face):
        u"""UV シェルを 4 方向に移動して重複を検出 maya.cmds 版

        :param shell_padding: float
        :param uv_shell: list
        :param all_face: list
        :return: list
        """

        result = []

        # UVシェルを +U +V 方向に移動
        cmds.polyEditUV(uv_shell, u=shell_padding, v=shell_padding)
        overlap_faces = cmds.polyUVOverlap(all_face, oc=True)
        if overlap_faces:
            result.extend(overlap_faces)
        cmds.polyEditUV(uv_shell, u=-shell_padding, v=-shell_padding)

        # UVシェルを -U -V 方向に移動
        cmds.polyEditUV(uv_shell, u=-shell_padding, v=-shell_padding)
        overlap_faces = cmds.polyUVOverlap(all_face, oc=True)
        if overlap_faces:
            result.extend(overlap_faces)
        cmds.polyEditUV(uv_shell, u=shell_padding, v=shell_padding)

        # UVシェルを -U +V 方向に移動
        cmds.polyEditUV(uv_shell, u=-shell_padding, v=shell_padding)
        overlap_faces = cmds.polyUVOverlap(all_face, oc=True)
        if overlap_faces:
            result.extend(overlap_faces)
        cmds.polyEditUV(uv_shell, u=shell_padding, v=-shell_padding)

        # UVシェルを +U -V 方向に移動
        cmds.polyEditUV(uv_shell, u=shell_padding, v=-shell_padding)
        overlap_faces = cmds.polyUVOverlap(all_face, oc=True)
        if overlap_faces:
            result.extend(overlap_faces)
        cmds.polyEditUV(uv_shell, u=-shell_padding, v=shell_padding)

        return result

    @classmethod
    def _verify_overlap_faces_om(cls, mesh_fn, shell_num, shell_ids, shell_padding, all_face):
        u"""UV シェルを 4 方向に移動して重複を検出 maya.api 版

        :param mesh_fn: MFnMesh Object
        :param shell_num: int
        :param shell_ids: list
        :param shell_padding: float
        :param all_face: list
        :return: list
        """

        result = []

        # UV シェル配列作成
        uv_shell = om.MIntArray()
        for idx, shell_id in enumerate(shell_ids):
            if shell_id == shell_num:
                uv_shell.append(idx)

        # U と V の座標配列作成
        u_array = om.MFloatArray()
        v_array = om.MFloatArray()
        for uv in uv_shell:
            uv_pos = mesh_fn.getUV(uv)
            u_array.append(uv_pos[0])
            v_array.append(uv_pos[1])

        # padding の値で移動させる為の U, V 座標配列 4方向
        u_array_plus = [x + shell_padding for x in u_array]
        u_array_minus = [x - shell_padding for x in u_array]
        v_array_plus = [x + shell_padding for x in v_array]
        v_array_minus = [x - shell_padding for x in v_array]

        # +U +V 右上に移動
        mesh_fn.setSomeUVs(uv_shell, u_array_plus, v_array_plus)
        overlap_faces = cmds.polyUVOverlap(all_face, oc=True)
        if overlap_faces:
            result.extend(overlap_faces)
        mesh_fn.setSomeUVs(uv_shell, u_array, v_array)

        # -U -V 左下に移動
        mesh_fn.setSomeUVs(uv_shell, u_array_minus, v_array_minus)
        overlap_faces = cmds.polyUVOverlap(all_face, oc=True)
        if overlap_faces:
            result.extend(overlap_faces)
        mesh_fn.setSomeUVs(uv_shell, u_array, v_array)

        # +U -V 左上に移動
        mesh_fn.setSomeUVs(uv_shell, u_array_plus, v_array_minus)
        overlap_faces = cmds.polyUVOverlap(all_face, oc=True)
        if overlap_faces:
            result.extend(overlap_faces)
        mesh_fn.setSomeUVs(uv_shell, u_array, v_array)

        # -U +V 左下に移動
        mesh_fn.setSomeUVs(uv_shell, u_array_minus, v_array_plus)
        overlap_faces = cmds.polyUVOverlap(all_face, oc=True)
        if overlap_faces:
            result.extend(overlap_faces)
        mesh_fn.setSomeUVs(uv_shell, u_array, v_array)

        if result:
            result = list(set(result))

        return result

    @classmethod
    def execute_(cls, selection, resolution, shell_padding, tile_padding):
        u""" 隣接する UV シェルとマップ境界間隔のチェック実行

        :param selection: str
        :param resolution: int
        :param shell_padding: float
        :param tile_padding: float
        :return: None
        """

        error_shells = []
        error_tiles = []
        error_meshes = []

        # ピクセル値に変換
        shell_padding = 1.0 / resolution * shell_padding
        tile_padding = 1.0 / resolution * tile_padding

        # 1つ目の選択をノードタイプで判定
        node_type = cmds.nodeType(selection[0])

        if node_type == 'mesh':

            logger.info(u'選択コンポーネントに対して処理を実行します')

            # Shell 又は Tile Padding の値が 0.00 の場合
            calculate_tile = True
            calculate_shell = True

            # UV シェル取得
            uv_shells = cls._get_uv_shells(selection)

            # UV シェル フェイス取得
            cmds.select(uv_shells)
            mel.eval('polySelectBorderShell 0;')
            select_uv = cmds.ls(sl=True)
            cmds.select(cl=True)
            all_face = cmds.polyListComponentConversion(select_uv, tf=True)
            all_face = cmds.filterExpand(all_face, sm=34)

            # UV シェル毎の処理
            for uv in uv_shells:

                uvs = cls._get_uv_from_selection(uv)

                if tile_padding == 0.00:
                    calculate_tile = False
                else:
                    # マップ境界間隔チェック
                    over_uvs = []
                    for uv_id in uvs:
                        u, v = cmds.polyEditUV(uv_id, q=True)
                        if (
                                u < tile_padding
                                or u > 1 - tile_padding
                                or v < tile_padding
                                or v > 1 - tile_padding
                        ):
                            over_uvs.append(uv_id)

                    # マップ境界間隔をフェイスに変換
                    if over_uvs:
                        for over_uv in over_uvs:
                            faces = cmds.polyListComponentConversion(over_uv, tf=True)
                            faces = cmds.filterExpand(faces, sm=34)
                            error_tiles.extend(faces)

                if shell_padding == 0.00:
                    calculate_shell = False
                else:
                    # UV シェルを4方向に移動して重複を検出
                    overlap_faces = cls._verify_overlap_faces(shell_padding, uvs, all_face)
                    if overlap_faces:
                        error_shells.extend(overlap_faces)

            if not calculate_tile:
                hoge = 0
                logger.info(u'Tile Padding が 0.00 の為、マップ境界間隔はチェックしません。')
            if not calculate_shell:
                hoge = 0
                logger.info(u'Shell Padding が 0.00 の為、隣接 UV はチェックしません。')

        elif node_type == 'transform':

            logger.info(u'選択しているトランスフォーム以下のシェイプに対して処理を実行します\n')
            meshes = cmds.ls(selection, dag=True, s=True, ni=True, l=True)

            # Shell 又は Tile Padding の値が 0.00 の場合
            calculate_shell = True
            calculate_tile = True

            # メッシュ毎に処理開始
            for mesh in meshes:

                if cmds.nodeType(mesh) == 'mesh':
                    # 表示用
                    transforms = cmds.listRelatives(mesh, p=True)

                    # 重複フェイスチェック用に全フェイス取得しておく
                    all_face = cmds.polyListComponentConversion(mesh, tf=True)
                    all_face = cmds.filterExpand(all_face, sm=34)

                    sel_list = om.MSelectionList()
                    sel_list.add(mesh)
                    depend_node = sel_list.getDependNode(0)
                    mesh_fn = om.MFnMesh(depend_node)
                    shell_nums, shell_ids = mesh_fn.getUvShellsIds()

                    if not shell_nums:
                        error_meshes.append(transforms[0])
                        continue

                    if shell_padding == 0.00:
                        calculate_shell = False
                    else:
                        # プログレスウィンドウ
                        progress = cmds.progressWindow(
                            t='Progress Window',
                            ii=True,
                            st=u'{} の UV Padding チェック中...'.format(transforms[0]),
                            max=shell_nums,
                        )

                        # 隣接 UV チェック
                        overlap_faces = []
                        for shell_num in range(shell_nums):

                            # プログレスウィンドウ +1
                            cmds.progressWindow(progress, e=True, s=1)

                            # プログレスウィンドウキャンセル
                            if cmds.progressWindow(q=True, ic=True):
                                cmds.progressWindow(progress, e=True, ep=True)
                                cmds.pause(seconds=1)
                                return

                            faces = cls._verify_overlap_faces_om(
                                mesh_fn,
                                shell_num,
                                shell_ids,
                                shell_padding,
                                all_face
                            )
                            if faces:
                                overlap_faces.extend(faces)

                        # プログレスウィンドウ終了
                        cmds.progressWindow(progress, e=True, ep=True)

                        if overlap_faces:
                            error_shells.extend(overlap_faces)

                    if tile_padding == 0.00:
                        calculate_tile = False
                    else:
                        # マップ境界間隔チェック
                        over_uvs = []
                        for uv_id in range(mesh_fn.numUVs()):
                            u, v = mesh_fn.getUV(uv_id)
                            if (
                                    u < tile_padding
                                    or u > 1 - tile_padding
                                    or v < tile_padding
                                    or v > 1 - tile_padding
                            ):
                                over_uvs.append(uv_id)

                        # マップ境界間隔をフェイスに変換
                        uvs = []
                        if over_uvs:
                            for over_uv in over_uvs:
                                over_uv = cmds.ls('{}.map[{}]'.format(transforms[0], over_uv))
                                uvs.extend(over_uv)
                        if uvs:
                            faces = cmds.polyListComponentConversion(uvs, tf=True)
                            faces = cmds.filterExpand(faces, sm=34)
                            error_tiles.extend(faces)

            if not calculate_shell:
                hoge = 0
                logger.info(u'Shell Padding が 0.00 の為、隣接 UV はチェックしません。')
            if not calculate_tile:
                hoge = 0
                logger.info(u'Tile Padding が 0.00 の為、マップ境界間隔はチェックしません。')

        return {
            'error_shells': error_shells,
            'error_tiles': error_tiles,
            'error_meshes': error_meshes,
        }
