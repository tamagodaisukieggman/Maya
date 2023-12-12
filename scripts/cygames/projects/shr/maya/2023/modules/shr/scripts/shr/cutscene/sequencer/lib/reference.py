"""MayaのReference周りの"""
from __future__ import annotations

import os
import stat
import typing as tp

from maya import cmds


def root_node(ref_node) -> tp.List[str]:
    """ルートノードを取得する

    TODO: パフォーマンスが悪いので改善必要
    """
    top_nodes = cmds.ls(assemblies=True)

    namespace_node = []
    for node in top_nodes:
        try:
            ref_name = cmds.referenceQuery(node, referenceNode=True, topReference=True)
            if ref_name == ref_node:
                namespace_node.append(node)
        except RuntimeError:
            continue
    return namespace_node


def save_reference(reference_path) -> bool:
    """編集内容を適用する

    Returns:
        bool: 保存成功
    """
    os.chmod(path=reference_path, mode=stat.S_IWRITE)
    cmds.file(reference_path, force=True, saveReference=True)


def get_namespace(ref_node) -> str:
    namespace = cmds.referenceQuery(ref_node, namespace=True)
    return namespace
