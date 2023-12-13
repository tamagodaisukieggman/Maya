import yaml
import maya.cmds as cmds


def export_selected_joint_attributes():
    yaml_path, base_name = cmds.file(q=True, sn=True).rsplit("/", 1)
    yaml_path = yaml_path + f"/{base_name[:2]}_joint_attributes.yaml"
    selected = cmds.ls(sl=True, type="joint")
    joints = cmds.listRelatives(selected, ad=True, type="joint")
    if joints:
        _export_joint_attrs_to_yaml(joints, yaml_path)

def _export_joint_attrs_to_yaml(node_names, yaml_path: str) -> None:
    """指定されたジョイントノードの属性値をYAMLファイルに書き出す関数
    Args:
        node_names (List[str]): 属性を書き出すジョイントノードのリスト
        yaml_path (str): 属性値を書き出すYAMLファイルのパス
    Returns:
        None
    """

    def to_list(value):
        if isinstance(value, (list, tuple)):
            return [to_list(sub_value) for sub_value in value]
        else:
            return value

    target_attrs = [
        "translate",
        "rotate",
        "scale",
        "shear",
        "rotateAxis",
        "offsetParentMatrix",
        "rotateOrder",
        "stiffness",
        "preferredAngle",
        "jointOrient",
        "minTransLimit",
        "minTransXLimit",
        "minTransYLimit",
        "minTransZLimit",
        "maxTransLimit",
        "maxTransXLimit",
        "maxTransYLimit",
        "maxTransZLimit",
        "minTransLimitEnable",
        "minTransXLimitEnable",
        "minTransYLimitEnable",
        "minTransZLimitEnable",
        "maxTransLimitEnable",
        "maxTransXLimitEnable",
        "maxTransYLimitEnable",
        "maxTransZLimitEnable",
        "minRotLimit",
        "minRotXLimit",
        "minRotYLimit",
        "minRotZLimit",
        "maxRotLimit",
        "maxRotXLimit",
        "maxRotYLimit",
        "maxRotZLimit",
        "minRotLimitEnable",
        "minRotXLimitEnable",
        "minRotYLimitEnable",
        "minRotZLimitEnable",
        "maxRotLimitEnable",
        "maxRotXLimitEnable",
        "maxRotYLimitEnable",
        "maxRotZLimitEnable",
        "minScaleLimit",
        "minScaleXLimit",
        "minScaleYLimit",
        "minScaleZLimit",
        "maxScaleLimit",
        "maxScaleXLimit",
        "maxScaleYLimit",
        "maxScaleZLimit",
        "minScaleLimitEnable",
        "minScaleXLimitEnable",
        "minScaleYLimitEnable",
        "minScaleZLimitEnable",
        "maxScaleLimitEnable",
        "maxScaleXLimitEnable",
        "maxScaleYLimitEnable",
        "maxScaleZLimitEnable",
    ]

    total_output = {}
    for node_name in node_names:
        joint_attrs_data = {}
        for attr_name in target_attrs:
            try:
                attr_value = cmds.getAttr(f"{node_name}.{attr_name}")
                print(attr_name, cmds.getAttr(f"{node_name}.{attr_name}"))
                joint_attrs_data[attr_name] = attr_value
            except:
                print(
                    f'Failed to get the attribute "{attr_name}" for node "{node_name}".'
                )
        total_output[node_name] = joint_attrs_data

    with open(yaml_path, "w") as yaml_file:
        yaml.safe_dump(total_output, yaml_file, default_flow_style=False)

    print(f"Export >> {yaml_path}")
