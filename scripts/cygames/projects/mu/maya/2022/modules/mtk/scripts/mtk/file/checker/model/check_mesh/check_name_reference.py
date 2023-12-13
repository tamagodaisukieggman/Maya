# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


from maya import cmds


def _check_name_reference(node):
    # リファレンスノードに不要な名前がないかのチェック
    # 不要とは「：」で区切ったときに[0]に入るもの
    # ファイル名をネームスペースとして読んだ場合になりうる
    # 仕様では無名でリファレンスを読み込む
    # ただし、referenceQueryでは「：」の有無で調べても
    # 文字列にそれが含まれない
    # なので、splitしてリストの内容を確認
    # どこかに値が入っていればそれは仕様に合っていない
    
    errors = []

    _reference_nodes = [x for x in cmds.ls(type='reference', long=True) if "sharedReferenceNode" != x]
    for _reference_node in _reference_nodes:
        # if ":" in cmds.referenceQuery(_reference_node, namespace=True):
        #     errors.append(_reference_node)
        _name_split = cmds.referenceQuery(_reference_node, namespace=True).split(":")
        if [x for x in _name_split if x]:
            errors.append(_reference_node)
    
    return errors
    