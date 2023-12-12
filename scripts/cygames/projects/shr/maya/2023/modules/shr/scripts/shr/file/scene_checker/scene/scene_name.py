from pathlib import Path
import maya.cmds as cmds

from .. import data
from .. import scene_data

_current_file = Path(__file__)
CHECKER = " ".join(_current_file.stem.split("_"))


def check(maya_scene_data:scene_data.MayaSceneData, check_result:data.CheckResultData, checker:data.Checker):
    # カテゴリでチェックする必要のないもの排除 ,ENVIRONMENT ,CHARACTER ,PROP ,ANIMATION ,RIG ,UNKNOWN
    # if maya_scene_data.current_category == 'ANIMATION' or maya_scene_data.current_category == 'RIG':
    #     return

    # エラー表示の色設定
    checker.result.color = [100, 60, 110]

    # print(maya_scene_data.name_split_all)
    # print(maya_scene_data.current_project.get('DATA_TYPE_CATEGORY'))
    data_type_category:dict = maya_scene_data.current_project_setting.get('DATA_TYPE_CATEGORY')
    if not data_type_category:
        return
    MAYA_EXT: dict = maya_scene_data.current_project_setting.get('MAYA_EXT')
    current_scene_ext: str = MAYA_EXT.get(maya_scene_data.ext)

    check_category = data_type_category.get(maya_scene_data.current_category)
    # if data_type_category.get(maya_scene_data.current_category) != maya_scene_data.name_split_all[-6]:
    # print(maya_scene_data.current_category)
    # print(data_type_category)
    # print(check_category)
    # print(data_type_category.get(maya_scene_data.current_category))
    # print(maya_scene_data.name_split_all[4])

    if not current_scene_ext:
        checker.result.error_nodes.append('')
        checker.result.error_message_list.append(f'Scene File Extension Error: {maya_scene_data.ext}')

    print(f'{CHECKER} -- {current_scene_ext}')

    # プロジェクト独自の設定となる、パスの途中にカテゴリ名が入る場合
    # category_from_path = maya_scene_data.name_split_all[5]

    # if maya_scene_data.current_category != 'UNKNOWN':
    #     if check_category != category_from_path:
    #         checker.result.warning_nodes.append('')
    #         checker.result.warning_message_list.append(f'Scene Path Warning category: [{check_category}]')

    # if maya_scene_data.current_category == 'ENVIRONMENT':
    #     basename_split = maya_scene_data.basename.split('_')
    #     if len(basename_split) != 4:
    #         checker.result.error_nodes.append('')
    #         checker.result.error_message_list.append(f'Error Scene Name :[{maya_scene_data.basename}]')

        # _id_name = maya_scene_data.name_split_all[7]
        # _id_name_from_path = maya_scene_data.basename.split('mdl_', 1)[-1].rsplit('_', 1)[0]

        # if _id_name_from_path != _id_name:
        #     # print(_id_name, _id_name_from_path)
        #     # print(_id_name_from_path.split())
        #     checker.result.warning_nodes.append('')
        #     checker.result.warning_message_list.append(f'Scene Name Warning ID name: [{_id_name}] [{maya_scene_data.basename}]')




def modify(modify_data:data.ResultData, modify_result:data.ModifyResult):
    return
