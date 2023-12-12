# -*- coding: utf-8 -*-
import maya.cmds as cmds
import yaml
import re
import os


CHR_SRC_DIR = r"c:\\cygames\\shrdev\\shr_art\\resources\\characters\\"
SHR_3D_Path = "C:\\cygames\\shrdev\\shr\\tools\\in\\ext\\maya\\2023\\modules\\shr3d\\scripts\\shr3d\\"
YAML_DATA = (
    SHR_3D_Path
    + "animation\\animation_defaultscene_settings\\animation_defaultscene.yaml"
)


def get_directories(path: str, file_suffix="") -> dict:
    """path以下のフォルダ取得取得(フォルダのみ)

    Args:
        path (str): 親階層
        recursive (bool): 再帰的に処理するかどうか
    Returns:
        dict:
    """
    files_dir = []
    files_file = []

    if not os.path.exists(path):
        return {"folder": files_dir, "files": files_file}

    files = os.listdir(path)

    files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
    files_file = [
        f
        for f in files
        if os.path.isfile(os.path.join(path, f)) and f.endswith(file_suffix)
    ]

    return {"folder": files_dir, "files": files_file}


def get_character_folders() -> list:
    """キャラクターのフォルダー以下を取得

    Returns:
        list: directories
    """

    return get_directories(CHR_SRC_DIR)["folder"]


def get_character_ws_folders(chara_type: str) -> list:
    """workspaceのrootを取得

    Args:
        chara_type (str): キャラクターの種類を限定

    Returns:
        list: 対応するfolder path
    """
    directories = []
    for lp in get_character_folders():
        if chara_type in lp:
            for current_dir in get_directories(lp):
                if current_dir == lp[:3]:
                    directories.append(current_dir)

    return directories


def get_yaml_data() -> dict:
    """yamlで書かれたデータを取得

    Args:
        path (str): _description_

    Returns:
        dict: _description_
    """
    # とりあえず仮で決め打ち
    obj = {}
    with open(YAML_DATA, encoding="utf-8") as file:
        obj = yaml.safe_load(file)

    return obj


def get_nodes_by_namespace(ns: str, type: str) -> list:
    """nsに一致する名前空間のノードを返す

    Args:
        ns (str): ターゲットとするnamespace

    Returns:
        list: 対応するnode
    """
    rtn = cmds.ls("{}:*".format(ns), r=True, type=type)
    return rtn


def get_root_node(node: str) -> str:
    """nodeの一番親を返す

    Args:
        node (str): targetとなるnode

    Returns:
        str: rootとなるnode
    """
    while True:
        parent = cmds.listRelatives(node, parent=True)
        if not parent:
            break

        node = parent[0]

    return node


def constraint_by_namespace(ns_source: str, ns_target: str):
    """namespaceでconstraintを作成

    Args:
        ns_source (str): source側のnamespace名を指定
        ns_target (str): target側のnamespace名を指定
    """
    source = cmds.ls("{}:*".format(ns_source), r=True, type="joint")
    target = cmds.ls("{}:*".format(ns_target), r=True, type="joint")
    constraint_similar_joint(source, target)


def constraint_similar_joint(source_joints: list, target_joints: list) -> None:
    """同名のジョイントをparent constraingt

    Args:
        source_joints (list): コンストレイン元となるジョイント
        target_joints (list): コンストレイン先となるジョイント
    """
    for tgt in target_joints:
        for src in source_joints:
            if tgt.split(":")[1] == src.split(":")[1]:
                cmds.parentConstraint(tgt, src)


def set_reference(paths: list, namespace="") -> None:
    """pathをリファレンスで読み込む

    Args:
        paths (list): リファレンスで読み込むパス達

    Return:
        str: namespace_name
    """

    for path in paths:
        filename = os.path.basename(path.split(".")[0])

        namespace_name = ""
        if namespace != "":
            namespace_name = namespace
        else:
            namespace_name = filename

        max_suffix = check_max_namespace_suffix(namespace_name)
        namespace_name = namespace_name + "_" + str(max_suffix).zfill(2)
        cmds.file(path, reference=True, ns=namespace_name)
    return namespace_name


def set_display_layer_by_namespace(namespace):
    """_summary_

    Args:
        namespace (str): ネームスペースを基準に作成
    """
    joints = cmds.ls("{}:root_jnt".format(namespace), r=True, type="joint")
    transforms = cmds.ls("{}:mesh".format(namespace), r=True, type="transform")
    save_layer = cmds.createDisplayLayer(
        joints, name=namespace + ":save_notref", number=1
    )
    cmds.setAttr("{}.visibility".format(save_layer), 0)
    cmds.setAttr("{}.displayType".format(save_layer), 2)

    geo_layer = cmds.createDisplayLayer(
        transforms, name=namespace + ":geo_notref", number=1
    )
    cmds.setAttr("{}.visibility".format(geo_layer), 1)
    cmds.setAttr("{}.displayType".format(geo_layer), 2)


def check_already_exist_namespace(check_namespace_name: str) -> bool:
    """namespaceが使用されているかどうか調べる

    Args:
        check_namespace_name (str): チェックするnamespace

    Returns:
        bool: 存在しているかどうか
    """
    allNameSpace = cmds.namespaceInfo(listOnlyNamespaces=True)
    return check_namespace_name in allNameSpace


def check_max_namespace_suffix(check_namespace_name: str) -> int:
    """check_namespace_nameのnamespaceの中で一番sufixが大きい値を取る

    Args:
        check_namespace_name (str): チェックするnamespace

    Returns:
        int: 一番大きいsuffixを取得
    """
    max_num = 0
    if check_already_exist_namespace(check_namespace_name + "_00"):
        allNameSpace = cmds.namespaceInfo(listOnlyNamespaces=True)
        for lp in allNameSpace:
            if check_namespace_name in lp:
                try:
                    num = int(lp.split("_")[-1])
                    if max_num < num:
                        max_num = num
                except ValueError:
                    continue
    return max_num


def get_current_chrdata(chr_type: str) -> dict:
    """chr_typeに基づいたデータを返す

    Args:
        chr_type (str): labelに当たるデータを入力

    Returns:
        dict: character infoのデータ
    """

    yaml_datas = get_yaml_data()["character_info"]
    current_type_data = {}
    for lp in yaml_datas:
        if chr_type == lp["label"]:
            current_type_data = lp
    return current_type_data


def get_share_path(path: str) -> str:
    """shareのpathと連携したパスを返す

    Args:
        path (str): _description_

    Returns:
        str: _description_
    """
    yaml_datas = get_yaml_data()["project_path"]
    return yaml_datas["share_path"] + path


def get_mb_path(chr_type: str, parts_name: str, version: str) -> str:
    """_summary_

    Args:
        chr_type (str): character_typeを指定
        parts_name (str): partsの名前を指定
        version(str): versionを指定

    Returns:
        str: 引数を元にmbのパスを返す
    """
    current_type_data = get_current_chrdata(chr_type)
    scene_name = parts_name.split("_")[0]
    return_path = "{0}/{1}/{2}/maya/{3}_{4}.mb".format(
        get_share_path(current_type_data["path"]),
        scene_name[:3],
        parts_name,
        scene_name,
        version,
    )
    return return_path


def save_file_dialog(file_name: str, chr_type: str, parts_name: str):
    """保存時のダイアログ

    Args:
        filename (str): 保存時の名前

    """
    current_type_data = get_current_chrdata(chr_type)
    path = "{0}/{1}/{2}/maya/default/".format(
        current_type_data["path"].replace("rigs", "animations"),
        current_type_data["id"],
        parts_name,
    )
    if not os.path.exists(path):
        result = cmds.confirmDialog(
            title="Warning",
            message="Folder does not exist. Are you sure you want to create a folder in this location?\n{}".format(
                path
            ),
            button=["Yes", "No"],
            defaultButton="Yes",
            cancelButton="No",
            dismissString="No",
        )
        if result == "Yes":
            os.makedirs(path, exist_ok=True)
        else:
            cmds.warning("end processing")
    path = cmds.fileDialog2(ds=2, fm=2, dir=path)[0]
    save_path = path + "/" + file_name + ".mb"
    cmds.file(rename=save_path)
    cmds.file(save=True, de=False, type="mayaBinary")
    print("save file >> {}".format(save_path))


def get_versions(files: list) -> list:
    """versionの文字列として取得 v***の形の配列で返ってくる

    Args:
        files (list): strの配列

    Returns:
        list: v***の形のstrの配列
    """
    pattern = re.compile(".*(v\d{3}).*")
    rtn_versions = []
    for file in files:
        version = re.search(pattern, file).groups()[0]
        rtn_versions.append(version)
    return rtn_versions


def get_latest_version(files: list) -> str:
    """最新のバージョンを取得

    Args:
        files (list): strの配列

    Returns:
        str: 最大のversionの文字列
    """
    versions = get_versions(files)
    max_value = 0
    for version in versions:
        current_value = int(version[1:])
        if max_value < current_value:
            max_value = current_value
    return "v" + str(max_value).zfill(3)
