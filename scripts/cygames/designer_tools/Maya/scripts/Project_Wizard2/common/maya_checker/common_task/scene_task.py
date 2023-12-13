import typing as tp
from collections import Counter

from ..task import CheckTaskBase
from ..scene_data import MayaSceneDataBase
from ..data import ErrorType

import maya.cmds as cmds


class ExistsReference(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "参照ノード"

    def exec_task_method(self):
        has_reference = ExistsReference.has_reference_nodes()

        if has_reference:
            self.set_error_data(
                "exists_reference",
                None,
                "リファレンスが存在しています",
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    @staticmethod
    def has_reference_nodes():
        """
        シーン内に参照ノードが存在するか確認
        Returns:
            bool: 参照ノードが存在すればTrue、存在しなければFalse
        """
        refs = cmds.file(query=True, reference=True)
        if refs:
            return True
        else:
            return False


class ExistsNameSpace(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ネームスペースを含むノード"

    def exec_task_method(self):
        """checkのテスト"""
        exists_namespace = self._check_namespace_exists()
        if exists_namespace:
            self.set_error_data(
                "exists_namespace",
                self._get_namespace_nodes(),
                "namespaceが含まれるノード",
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        """ネームスペースの削除"""
        target_objects = self.debug_data.error_target_info["exists_namespace"][
            "target_objects"
        ]
        self.delete_namespaces()

    def _check_namespace_exists(self):
        """
        シーン内にネームスペースが入っているノードが存在しているかどうかチェックする関数。

        Returns:
            bool: ネームスペースが含まれるノードが存在する場合はTrue、存在しない場合はFalse
        """
        namespace_nodes = self._get_namespace_nodes()
        if len(namespace_nodes) > 0:
            return True
        return False

    def _get_namespace_nodes(self):
        namespace_nodes = cmds.ls("*:*")
        return namespace_nodes

    def delete_namespaces(self):
        """対象のネームスペースを削除する

        Args:
            namespaces (tp.List[str]): 不用なネームスペース

        """
        cmds.namespace(setNamespace=":")

        for ns in reversed(cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)):
            try:
                if ns != "UI" and ns != "shared":
                    cmds.namespace(moveNamespace=(ns, ":"), force=True)
                    cmds.namespace(removeNamespace=ns)
            except:
                continue

    @staticmethod
    def get_unique_namespaces(obj_names: tp.List[str]) -> tp.List[str]:
        """
        Get the unique namespaces of given objects considering nested namespaces.
        Args:
            obj_names (List[str]): The names of the objects.
        Returns:
            List[str]: A list of unique namespaces including nested ones.
        """
        namespaces = set()
        for obj in obj_names:
            if ":" in obj:
                all_namespaces = obj.split(":")[:-1]  # -1 to ignore the object name
                if "|" in all_namespaces:
                    all_namespaces = all_namespaces.rsplit("|")[-1]
                for i in range(len(all_namespaces)):
                    namespaces.add(":".join(all_namespaces[: i + 1]))
        return list(namespaces)


class ExistsTurtleNodes(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "Turtle関連のノードを検出"

    def exec_task_method(self):
        has_turtle_nodes = self._check_turtle_nodes()
        if has_turtle_nodes:
            self.set_error_data(
                "has_turtle_nodes", self._get_turtle_nodes(), "turtleのノードが含まれています。"
            )

        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        turtle_nodes = self.get_debug_target_objects("has_turtle_nodes")
        self.delete_turtle_nodes(turtle_nodes)

    def delete_turtle_nodes(self, turtle_nodes) -> None:
        """
        シーン内のTurtleノードをすべて削除する関数。
        Args: なし
        Returns: なし
        """
        # # シーン内のすべてのTurtleノードを取得
        # turtle_nodes = cmds.ls(type="ilr*")

        # 各Turtleノードを削除
        for node in turtle_nodes:
            # ノードがロックされている場合、アンロックする
            if cmds.lockNode(node, q=True):
                cmds.lockNode(node, lock=False)
            cmds.delete(node)

    def _check_turtle_nodes(self):
        """
        シーン内にTurtle関連のノードが存在するかどうかをチェックする。

        Returns:
            bool: Turtle関連のノードが存在する場合はTrue、存在しない場合はFalse
        """
        if len(self._get_turtle_nodes()) > 0:
            return True
        return False

    def _get_turtle_nodes(self):
        """
        シーン内にTurtle関連のノードが存在するかどうかをチェックする。

        Returns:
            bool: Turtle関連のノードが存在する場合はTrue、存在しない場合はFalse
        """
        # Turtle関連のノードタイプ
        turtle_node_types = [
            "TurtleBakeLayer",
            "TurtleDefaultBakeLayer",
            "TurtleRenderOptions",
            "TurtleUIOptions",
            "TurtleBakeLayerManager",
        ]
        turtle_nodes = []

        # シーン内の全ノードを取得
        all_nodes = cmds.ls()
        # 各ノードのタイプをチェックし、Turtle関連のノードがあればTrueを返す
        for node in all_nodes:
            if node in turtle_node_types:
                turtle_nodes.append(node)
        return turtle_nodes


class ExistsUnknownNode(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "unknownノード・不要なノード"

    def exec_task_method(self):
        if self._check_unknown_nodes_exist():
            self.set_error_data(
                "exists_unknown_node", self._get_unknown_nodes(), "unknownのノード", True
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        debug_targets = self.get_debug_target_objects("exists_unknown_node")
        cmds.delete(debug_targets)

    def _get_unknown_nodes(self) -> tp.List[str]:
        """Mayaシーン内のunknownノードのリストを取得する。
        Returns:
            list: シーン内のunknownノードのリスト。
        """
        unknown_nodes = cmds.ls(type="unknown")
        return unknown_nodes

    def _check_unknown_nodes_exist(self):
        """シーン内にunknownノードが存在するかどうかをチェックする。
        Returns:
            bool: unknownノードが存在する場合はTrue、存在しない場合はFalse。
        """
        unknown_nodes = self._get_unknown_nodes()
        return bool(unknown_nodes)


class ExistsUnknownPlugin(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "unknownプラグイン"

    def exec_task_method(self):
        if self._check_unknown_plugins_exist():
            self.set_error_data(
                "exists_unknown_plugin", self._get_unknown_plugins(), "unknownのplugin"
            )
        else:
            self.debug_data.error_type = ErrorType.NOERROR

    def exec_fix_method(self):
        self.remove_unknown_plugins()

    def _get_unknown_plugins(self):
        """Mayaシーン内のunknownプラグインのリストを取得する。
        Returns:
            list: シーン内のunknownプラグインのリスト。
        """
        unknown_plugins = cmds.unknownPlugin(q=True, list=True)
        return unknown_plugins

    def _check_unknown_plugins_exist(self):
        """シーン内にunknownプラグインが存在するかどうかをチェックする。
        Returns:
            bool: unknownプラグインが存在する場合はTrue、存在しない場合はFalse。
        """
        unknown_plugins = self._get_unknown_plugins()
        return bool(unknown_plugins)

    def remove_unknown_plugins(self):
        """シーン内のunknownプラグインを削除する。"""
        unknown_plugins = self._get_unknown_plugins()
        if unknown_plugins:
            for plugin in unknown_plugins:
                cmds.unknownPlugin(plugin, remove=True)


class HasDuplicateNodeNames(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = "ノード名の重複"

    def exec_task_method(self):
        if self.check_duplicate_objects():
            self.set_error_data(
                "has_duplicate_node_names", self._get_duplicate_node_names(), "ノード名の重複"
            )
        else:
            self.set_error_type(ErrorType.NOERROR)

    def exec_fix_method(self):
        ...

    def _get_duplicate_node_names(self) -> tp.List[str]:
        """シーン内の重複している全てのノード名を配列で返す。
        Returns:
            list: 重複しているノード名のリスト。
        """
        all_nodes = cmds.ls(long=True)
        short_names = [node.rsplit("|")[-1] for node in all_nodes]

        name_counts = Counter(short_names)
        duplicate_names = [name for name, count in name_counts.items() if count > 1]

        all_duplicate_names = []
        for name in duplicate_names:
            for lp in cmds.ls(f"*{name}"):
                all_duplicate_names.append(lp)
        return all_duplicate_names

    def check_duplicate_objects(self):
        """重複オブジェクトが存在する場合はTrueを返し、存在しない場合はFalseを返す。
        Returns:
            bool: 重複オブジェクトが存在する場合はTrue、存在しない場合はFalse。
        """
        duplicate_node_names = self._get_duplicate_node_names()
        return bool(duplicate_node_names)
