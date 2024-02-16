# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds
import maya.mel as mel


# ==================================================
def check_face_with_more_4side(target_transform_list, cleanup):
    """
    4辺より多くの辺を持つフェースをチェック

    :param target_transform_list: トランスフォームリスト
    :param cleanup: クリーンアップをかけるかどうか
    """

    if not target_transform_list:
        return

    cmds.select(target_transform_list, r=True)

    mel_script = \
        "polyCleanupArgList 3 { \"0\",\"replace\",\"1\",\"0\",\"1\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\" }"

    if cleanup:
        mel_script = mel_script.replace("replace", "1")
    else:
        mel_script = mel_script.replace("replace", "2")

    result = mel.eval(mel_script)

    if not result:
        return []

    result = cmds.ls(result, fl=True, l=True)

    return result


# ==================================================
def check_concave_face(target_transform_list, cleanup):
    """
    凹面フェースをチェック

    :param target_transform_list: トランスフォームリスト
    :param cleanup: クリーンアップをかけるかどうか
    """

    if not target_transform_list:
        return

    cmds.select(target_transform_list, r=True)

    mel_script = \
        "polyCleanupArgList 3 { \"0\",\"replace\",\"1\",\"0\",\"0\",\"1\",\"0\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\" }"

    if cleanup:
        mel_script = mel_script.replace("replace", "1")
    else:
        mel_script = mel_script.replace("replace", "2")

    result = mel.eval(mel_script)

    if not result:
        return

    result = cmds.ls(result, fl=True, l=True)

    return result


# ==================================================
def check_face_with_hole(target_transform_list, cleanup):
    """
    穴の開いているフェースチェック

    :param target_transform_list: トランスフォームリスト
    :param cleanup: クリーンアップをかけるかどうか
    """

    if not target_transform_list:
        return

    cmds.select(target_transform_list, r=True)

    mel_script = "polyCleanupArgList 3 { \"0\",\"replace\",\"1\",\"0\",\"0\",\"0\",\"1\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\" }"

    if cleanup:
        mel_script = mel_script.replace("replace", "1")
    else:
        mel_script = mel_script.replace("replace", "2")

    result = mel.eval(mel_script)

    if not result:
        return

    result = cmds.ls(result, fl=True, l=True)

    return result


# ==================================================
def check_lamina_face(target_transform_list, cleanup):
    """
    ラミナフェースチェック

    :param target_transform_list: トランスフォームリスト
    :param cleanup: クリーンアップをかけるかどうか
    """

    if not target_transform_list:
        return

    cmds.select(target_transform_list, r=True)

    mel_script = "polyCleanupArgList 3 { \"0\",\"replace\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"1\" }"

    if cleanup:
        mel_script = mel_script.replace("replace", "1")
    else:
        mel_script = mel_script.replace("replace", "2")

    result = mel.eval(mel_script)

    if not result:
        return

    result = cmds.ls(result, fl=True, l=True)

    return result


# ==================================================
def check_nonmanifold(target_transform_list, cleanup):
    """
    非多様体チェック

    :param target_transform_list: トランスフォームリスト
    :param cleanup: クリーンアップをかけるかどうか
    """

    if not target_transform_list:
        return

    cmds.select(target_transform_list, r=True)

    mel_script = \
        "polyCleanupArgList 3 { \"0\",\"replace\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1\",\"0\" }"

    if cleanup:
        mel_script = mel_script.replace("replace", "1")
    else:
        mel_script = mel_script.replace("replace", "2")

    result = mel.eval(mel_script)

    if not result:
        return

    result = cmds.ls(result, fl=True, l=True)

    return result


# ==================================================
def check_zero_edge(target_transform_list, cleanup):
    """
    ゼロエッジをチェック

    :param target_transform_list: トランスフォームリスト
    :param cleanup: クリーンアップをかけるかどうか
    """

    if not target_transform_list:
        return

    cmds.select(target_transform_list, r=True)

    mel_script = \
        "polyCleanupArgList 3 { \"0\",\"replace\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"1\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\" }"

    if cleanup:
        mel_script = mel_script.replace("replace", "1")
    else:
        mel_script = mel_script.replace("replace", "2")

    result = mel.eval(mel_script)

    if not result:
        return

    result = cmds.ls(result, fl=True, l=True)

    return result
