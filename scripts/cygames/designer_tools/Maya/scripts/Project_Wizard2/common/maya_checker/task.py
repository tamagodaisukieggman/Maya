import traceback
import typing as tp

import maya.cmds as cmds

from .data import TaskInfo, DebugData, ErrorType
from .scene_data import MayaSceneDataBase


class CheckTaskBase:
    """チェック項目のベースクラス"""

    def __init__(self, **kwargs):
        self.maya_scene_data = kwargs["maya_scene_data"]

        if kwargs["extra_data"]:
            self.extra_data = kwargs["extra_data"]
        else:
            self.extra_data = {}

        self.post_process_settings = kwargs["post_process_settings"]

        self.error_type = self.get_task_error_type(self.extra_data)
        self.checker_info = TaskInfo()
        self.debug_data: DebugData = DebugData()
        self.dependent_task_names: tp.List[str] = []
        self.default_error_type = ErrorType.ERROR
        self.fix_detail: str = ""

    def get_task_error_type(self, extra_data: dict):
        """taskのyaml上で設定し

        Args:
            extra_data (dict): error_typeを含むextra data
        """
        if extra_data:
            if "error_type" in extra_data:
                error_type = None
                if extra_data["error_type"] == "ERROR":
                    error_type = ErrorType.ERROR
                elif extra_data["error_type"] == "WARNING":
                    error_type = ErrorType.WARNING
                self.error_type = error_type
                return error_type
        return

    def exec_task(self):
        """タスクの実行のmain
        """
        try:
            self.exec_task_method()
            self.exec_task_post_process()
        except Exception as e:
            print("例外 : ", e)

            traceback.print_exc()
            # プログラムエラーが発生した場合は通知
            self.set_error_type(ErrorType.PROGRAMERROR)

    def exec_fix(self):
        try:
            self.exec_fix_method()

        except Exception as e:
            print("例外 : ", e)
            traceback.print_exc()

    def exec_task_method(self):
        """タスクの実行メソッドを記述"""
        ...

    def exec_fix_method(self):
        """エラーがあった場合の解決メソッドを記述"""
        ...

    def reset_debug_data(self):
        """debug_dataをclearする"""
        self.debug_data = DebugData()

    def set_error_data(
        self,
        error_name: str,
        target_objects: str,
        error_message: str,
        is_reset_debug_data: bool = True,
    ):
        """デバッグ用のエラー情報をセットする関数

        Args:
            error_name (str): エラー名
            target_objects (str): 対象オブジェクト
            error_message (str): エラーメッセージ
            is_reset_debug_data(bool): デバッグデータをリセットするかどうか
        """
        if is_reset_debug_data:
            self.reset_debug_data()

        if self.error_type != None:
            self.set_error_type(self.error_type)

        else:
            self.set_error_type(self.default_error_type)

        exclude_objects = []
        if "exclude_objects" in self.extra_data:
            exclude_objects = self.extra_data["exclude_objects"]

        if len(exclude_objects) > 0 and target_objects:
            target_objects = self._remove_exclude_objects(
                target_objects, exclude_objects
            )

        # exclude_objectsを除いて０になった場合はNoerrorに設定
        if not target_objects and isinstance(target_objects, list):
            self.set_error_type(ErrorType.NOERROR)
            return

        if isinstance(target_objects, list):
            self._set_debug_targets_info(error_name, target_objects, error_message)
        else:
            self._set_debug_target_info(error_name, target_objects, error_message)

    def exec_task_post_process(self):
        error_names = self.get_error_names()

        target_objects = []
        has_error = False
        for error_name in error_names:
            target_objects = self.get_debug_target_objects(error_name)

            if target_objects == [None]:
                has_error = True
                continue

            if target_objects:
                exclude_referenced = self.get_post_process_settings_value(
                    "exclude_referenced"
                )

                if exclude_referenced:
                    # 参照オブジェクトを取り除く
                    if target_objects:
                        target_objects = self._exclude_referenced_objects(
                            target_objects
                        )
                        self.set_debug_target_objects(error_name, target_objects)

        if len(target_objects) >= 1:
            has_error = True

        # エラーオブジェクトが0だったら
        if has_error == False:
            if self.debug_data.error_type != ErrorType.NOCHECKED:
                self.set_error_type(ErrorType.NOERROR)
    def get_error_names(self):
        error_name_list = []
        for error_name in self.debug_data.error_target_info:
            error_name_list.append(error_name)
        return error_name_list

    def _remove_exclude_objects(
        self, target_objects: tp.List[str], exclude_objects: tp.List[str]
    ) -> tp.List[str]:
        result = []
        if target_objects:
            result = [item for item in target_objects if item not in exclude_objects]
        return result

    def set_error_type(self, value: ErrorType):
        """エラーの種類をセット

        Args:
            value (ErrorType): エラーの種類
        """
        if value == ErrorType.NOERROR:
            self.reset_debug_data()

        self.debug_data.error_type = value

    def _set_debug_target_info(
        self, error_name: str, target_object: str, error_message: str
    ):
        """debug情報のセット

        Args:
            error_name (str): エラー名
            target_object (str): デバッグオブジェクトの選択に使用するオブジェクト
            error_message (str): エラーに表示するメッセージ
        """
        error_target_info = self.debug_data.error_target_info

        if error_name in error_target_info:
            current_error = {error_name: error_target_info[error_name]}
        else:
            current_error = {error_name: {"target_objects": [], "error_messages": ""}}

        current_object = current_error[error_name]["target_objects"]
        current_message = current_error[error_name]["error_messages"]

        current_object.append(target_object)
        current_message = error_message

        current_error.update(
            {
                error_name: {
                    "target_objects": current_object,
                    "error_messages": current_message,
                }
            }
        )
        self.debug_data.error_target_info.update(current_error)

    def _set_debug_targets_info(
        self, error_name: str, target_objects: tp.List[str], error_message: str
    ):
        """配列でset_debug_target_infoができるようにwrapした関数

        Args:
            error_name (str): エラー名
            target_object (str): デバッグオブジェクトの選択に使用するオブジェクト
            error_message (str): エラーに表示するメッセージ
        """
        for target_object in target_objects:
            self._set_debug_target_info(error_name, target_object, error_message)

    def register_error_info_to_mesh_descendants(
        self,
        get_error_objects_func,
        error_name: str,
        error_message: str,
        error_type: ErrorType = ErrorType.ERROR,
    ):
        """エラーオブジェクトを一括登録する。特定の形に沿っている場合のみ実行可能
        rootの子孫のshapeを所有するトランスフォームの配列をtargetとする関数を"get_error_objects_func"に入れることで
        そこからreturnでかえってきたエラー対象となるオブジェクトの配列をerror dataとして登録する
        基本的には"set_error_data"の方の使用を推奨
        Args:
            get_error_objects_func (function): {"objectname":[error_objects...]}のdict、もしくは配列を返すfunction
            error_name (str): debug_logに表示するエラー名
            error_message (str): debug_logに表示するエラーメッセージ
        """
        transforms = []
        error_objects = []
        for root in self.maya_scene_data.root_nodes:
            transforms.extend(root.get_all_mesh_transform())

        error_objects = get_error_objects_func(transforms)

        self.set_error_type(ErrorType.NOERROR)

        if isinstance(error_objects, dict):
            for i, object_name in enumerate(error_objects):
                is_reset_debug_data = False

                # 最初の一回だけdebugdataの初期化を行う
                if i == 0:
                    is_reset_debug_data = True

                error_object_array = error_objects[object_name]

                if len(error_object_array) > 0:
                    self.set_error_data(
                        error_name,
                        error_object_array,
                        error_message,
                        is_reset_debug_data=is_reset_debug_data,
                    )
        elif isinstance(error_objects, list):
            # error_transformが1以上ならエラー
            if len(error_objects) > 0:
                self.set_error_data(error_name, error_objects, error_message)

        elif error_objects == None:
            return

        else:
            raise ValueError("error_objectsがlist、dictではありません")

    def set_fix_details(self, detail_message: str):
        """修正の詳細情報の記載

        Args:
            detail_message (str): 修正の詳細情報
        """
        self.fix_detail = detail_message

    def get_fix_details(self) -> str:
        """修正の詳細情報の取得

        Returns:
            str: 修正の詳細情報
        """
        return self.fix_detail

    def get_debug_target_objects(self, error_name: str) -> tp.List[str]:
        """エラーとなっているオブジェクトを取得

        Args:
            error_name (str): 取得する対象のエラー

        Returns:
            tp.List[str]: エラーオブジェクト
        """
        target_objects = self.debug_data.error_target_info[error_name]["target_objects"]
        return target_objects

    def set_debug_target_objects(
        self, error_name: str, object_names: tp.List[str]
    ) -> tp.List[str]:
        """エラーとなっているオブジェクトを取得

        Args:
            error_name (str): 取得する対象のエラー

        Returns:
            tp.List[str]: エラーオブジェクト
        """
        self.debug_data.error_target_info[error_name]["target_objects"] = object_names

    @staticmethod
    def _exclude_referenced_objects(obj_names: tp.List[str]) -> tp.List[str]:
        """
        obj_namesから参照オブジェクトを取り除き返す
        Args:
            obj_names (List[str]): オブジェクトの名前のリスト
        Returns:
            List[str]: リファレンスではないオブジェクトのリスト
        """

        non_referenced_objects = []
        for obj in obj_names:
            if obj:
                if cmds.objExists(obj):
                    if not cmds.referenceQuery(obj, isNodeReferenced=True):
                        non_referenced_objects.append(obj)
                    else:
                        print(f"{obj}は参照ノードなのでスキップします")
                else:
                    non_referenced_objects.append(obj)
        return non_referenced_objects

    def get_post_process_settings_value(self, postprocess_name: str):
        """ポストプロセス名から値を取得

        Args:
            postprocess_name (str): ポストプロセス名

        Returns:
            any: ポストプロセス設定の値
        """
        rtn_value = None
        for postprocess_setting in self.post_process_settings:
            if postprocess_setting["name"] == postprocess_name:
                rtn_value = postprocess_setting["value"]
        return rtn_value
