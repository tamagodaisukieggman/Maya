import os
from cy.asset import asset, assetutil

# 背景班マスターマテリアルのパスにあるアセットパスを取得
asset_path_list = assetutil.listdir(asset.path(virtualpath="content/mtk/runtime/resources/env/mst/material"), assetutil.ListDirFlags.TYPE_FILE)

# マスターマテリアル名リスト
mtl_list = []

for asset_path in sorted(asset_path_list):

    # マテリアルアセットの場合
    if asset.Path.PROP_WIN64 in asset_path.properties and asset_path.ext == ".mtl":

        # マスターマテリアル名をリストに追加
        mtl_list.append(os.path.basename(asset_path.virtualpath()))

for mtl in mtl_list:
    print(mtl)