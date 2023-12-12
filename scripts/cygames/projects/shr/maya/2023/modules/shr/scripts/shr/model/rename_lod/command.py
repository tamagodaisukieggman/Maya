import maya.cmds as cmds


def rename_lods():
    """
    lod~以下に入っているノードの末尾に_lod*をつける
    トップノードを選択している想定
    """
    selected = cmds.ls(sl=True)
    if len(selected) == 0:
        return 0

    transforms = cmds.listRelatives(selected, c=True, type="transform", pa=True) or []
    mesh_pa = [_ for _ in transforms if _.endswith("mesh")]
    lods = cmds.listRelatives(mesh_pa, c=True, type="transform", pa=True) or []

    for lod in lods:
        # #lod0ならスキップ
        # if "lod0" in lod:
        #     continue

        lod_level = lod.rsplit("|", 1)[-1]

        lod_children = cmds.listRelatives(lod, ad=True, pa=True) or []
        for lp in lod_children:
            if lp.endswith(lod_level) == False:
                shortname = lp.rsplit("|", 1)[-1]
                cmds.rename(lp, shortname + "_" + lod_level)

    rename_shapelod()
    return


def rename_shapelod():
    """シーン内のshapeをmaya標準な名称に変更"""
    for lp in cmds.ls(type="transform"):
        try:
            new_name = lp.replace("low_", "")
            cmds.rename(lp, new_name)
        except:
            continue

    for lp in cmds.ls(type=["mesh"]):
        parent = cmds.listRelatives(lp, parent=True, type="transform") or []
        if parent == []:
            continue
        lp = lp.replace("low_", "")
        if "Orig" in lp:
            new_name = parent[0].replace("low_", "") + "ShapeOrig"
            cmds.rename(lp, new_name)
        else:
            new_name = parent[0].replace("low_", "") + "Shape"
            cmds.rename(lp, new_name)
