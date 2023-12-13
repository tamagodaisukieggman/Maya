# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import maya.cmds as cmds


def eye_cover_bake(src, dst, file_name, file_format='psd', height=512, width=512):
    """目隠し用ベイク

    キャラ班作のHS_BakeToolの設定でベイクを実行する
    Mayaの基本機能では「Lighting/Shading > TransferMaps」

    Args:
        src: ベイク元メッシュ
        dst: ベイク先メッシュ
        file_name(str): 出力ファイルパスから拡張子を抜いたもの
        file_format(str): 出力ファイルのフォーマット（使用可能フォーマットはMayaのコマンドに従う）
        height(int): 出力テクスチャの縦サイズ
        width(int): 出力テクスチャの横サイズ

    """

    cmds.surfaceSampler(
        target=dst,
        source=src,
        uvSet='map1',
        searchOffset=0,
        maxSearchDistance=0,
        searchCage='',
        mapOutput='diffuseRGB',
        mapWidth=width,
        mapHeight=height,
        maximumValue=1,
        mapMaterials=True,
        shadows=True,
        filename=file_name,
        fileFormat=file_format,
        superSampling=2,
        filterType=0,
        filterSize=3,
        overscan=2,
        searchMethod=0,
        useGeometryNormals=True,
        ignoreMirroredFaces=False,
        flipU=False,
        flipV=False,
    )


def texture_bake(src, dst):
    """テクスチャのベイク

    Args:
        src: ベイク元メッシュ
        dst: ベイク先メッシュ
    """

    if not cmds.objExists(src) or not cmds.objExists(dst):
        return

    # 出力先のチェック
    ma_path = cmds.file(q=True, sn=True)

    if not ma_path:
        return
    
    project_path = os.path.dirname(os.path.dirname(ma_path))
    sourceimages_path = os.path.join(project_path, 'sourceimages')
    if not os.path.exists(sourceimages_path):
        return
    output_name = os.path.join(sourceimages_path, 'EyeCoverBaked')

    # ベイク実行
    try:
        eye_cover_bake(src, dst, output_name, 'psd', 512, 512)
        return '{}.{}'.format(output_name, 'psd')
    except Exception:
        return ''