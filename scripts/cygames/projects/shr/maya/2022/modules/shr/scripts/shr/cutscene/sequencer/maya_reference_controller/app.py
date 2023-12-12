import os
import shutil
import stat
import sys
import typing as tp

from maya import cmds
from shr.utils import getCurrentSceneFilePath


class MayaReferenceController(object):
    """Mayaのリファレンス周りの操作クラス

    リファレンスを作成
    """
    WORK_FOLDER_NAME = "exportresources"

    _instance = None

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create_work_folder(self) -> str:
        work_folder_path = self._crate_work_folder_path()
        if not self._check_folder(work_folder_path):
            os.makedirs(work_folder_path)
        return work_folder_path

    def _check_folder(self, path) -> bool:
        if os.path.exists(path):
            return True
        else:
            return False

    def _crate_work_folder_path(self) -> str:
        scene_path = getCurrentSceneFilePath()
        if not scene_path:
            raise SystemError("Not found scene path.")
        scene_dir = os.path.dirname(scene_path)
        work_folder_path = os.path.join(scene_dir, self.WORK_FOLDER_NAME)
        return work_folder_path

    def _duplicate_file(self, path) -> str:
        ...

    def delete(self, ref_node, is_file=True) -> str:
        ref_file_path = cmds.referenceQuery(ref_node, filename=True)
        cmds.file(ref_file_path, removeReference=True)

        if is_file:
            os.chmod(path=ref_file_path, mode=stat.S_IWRITE)
            os.remove(ref_file_path)

    def import_(self, clip_name: str, reference_file_path: str) -> str:
        """読み込み

        Returns:
            str: Reference node.
        """
        work_folder_path = self.create_work_folder()
        reference_file_ext = os.path.splitext(os.path.basename(reference_file_path))[1]
        duplicate_reference_path = os.path.join(work_folder_path, clip_name + reference_file_ext)

        if os.path.exists(duplicate_reference_path):
            raise ValueError("既に存在するClip")

        if cmds.namespace(exists=clip_name):
            raise ValueError("既に存在するNamespace")

        # if os.path.exists(duplicate_reference_path):
        #     os.chmod(path=duplicate_reference_path, mode=stat.S_IWRITE)
        #     os.remove(duplicate_reference_path)

        shutil.copy(reference_file_path, duplicate_reference_path)

        ref_node = cmds.file(duplicate_reference_path, reference=True, mergeNamespacesOnClash=False, namespace=clip_name)
        return ref_node

    def save(self, reference_path) -> bool:
        """編集内容を適用する

        Returns:
            bool: 保存成功
        """
        os.chmod(path=reference_path, mode=stat.S_IWRITE)
        cmds.file(reference_path, force=True, saveReference=True)

    def get_ref_path_from_selected_node(self) -> tp.Optional[tp.List[str]]:
        """選択中のノードからref_pathを取得する

        referenceじゃなかったらNoneを返す
        """
        selection_list = cmds.ls(selection=True)
        if selection_list == []:
            return None

        ref_node_list = []

        for selection_node in selection_list:
            if cmds.referenceQuery(selection_node, isNodeReferenced=True):
                root_node = self._relactive_collect_root_ref(selection_node)
                ref_node_list.append(cmds.referenceQuery(root_node, filename=True, withoutCopyNumber=True))

        if ref_node_list == []:
            return None

        return ref_node_list

    def _relactive_collect_root_ref(self, ref_node):
        """再帰的にreferenceNodeの親を取得する
        #TODO: topReferenceだけで良いので不要。
        """

        parent_ref_node = cmds.referenceQuery(ref_node, parent=True, referenceNode=True)

        if parent_ref_node is None:
            return ref_node
        else:
            return self._relactive_collect_root_ref(parent_ref_node)

    def get_namespace(self, ref_path):
        namespace: str = cmds.referenceQuery(ref_path, namespace=True)
        if namespace[0] == ":":
            namespace = namespace.lstrip(":")

        return namespace
