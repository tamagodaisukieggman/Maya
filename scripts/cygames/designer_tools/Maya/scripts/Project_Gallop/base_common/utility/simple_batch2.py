# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    # Maya 2022-
    from builtins import str
except Exception:
    pass

import subprocess
import os
import time
import codecs
import maya.cmds as cmds


REQUIRED_PLUGINS = ['mtoa.mll']


# 初代simple_batchが対象ファイルパスを環境変数に渡す方式だが
# 日本語パスを渡せなかったり不便なので代わりになる関数を作成


def execute_mayabatch(module, func, wait, **func_kwargs):
    """mayabatch.exeでPythonを実行する
    コマンドプロンプトで実行できる文字数に上限(8000文字程度)がある為
    パラメータを分割して実行する場合listやdictの分割の全てのパターンに対応できないので
    パラメータをテキストファイルに書き出して実行する。
    Args:
        module (str): importしたいモジュール。
                      (例)'Project_Gallop.glp_chara_facial_tool.main'
        func (str): 上記モジュールで呼び出す関数名
        wait (bool): プロレスの終了を待ってから後続処理を実行する場合はTrue
        func_kwargs: funcに渡すキーワードパラメータ
    """
    maya_version = cmds.about(v=True)
    if not maya_version:
        cmds.warning('mayaのversionが特定できませんでした。TAにご相談ください')
        return

    batch_file_path = __search_batch_file_path()
    if not batch_file_path:
        cmds.warning('mayabatchが見つかりませんでした。TAにご相談ください。')
        return

    save_kwargs(func_kwargs)

    # maファイルにおいてrequire mtoaが欠如して実行できないファイルが発生していたため、当該エラーが起きないようにする暫定対応
    command = 'import Project_Gallop.base_common.utility.simple_batch2 as glp_simple_bat2;glp_simple_bat2.load_required_plugins();'

    command += 'import ' + module + ';' + module + '.' + func

    # 日本語がパスに含まる場合バイトコードの中のバックスラッシュがエスケープされないようにする
    command = command.replace('\\', '\\\\')
    command = command.replace(' ', '__space__')
    if wait:
        subprocess.call([batch_file_path, maya_version, '"' + command + '"'])
    else:
        subprocess.Popen([batch_file_path, maya_version, '"' + command + '"'])


def save_kwargs(func_kwargs):
    """このスクリプトファイルのあるフォルダにsimple_batch_tmp.txtファイル
    を作り、mayabatch経由でパラメータを渡す。
    以前はsimple_batch.execute関数で環境変数にパラメータを保存していたが
    日本語対応できないので移行。
    Args:
        func_kwargs (_type_): simple_batchを通して実行する関数に渡すパラメータ
    """
    param_tmp_file_path = os.path.join(
        os.path.dirname(__file__), 'simple_batch_tmp.txt')
    with codecs.open(param_tmp_file_path, 'w', 'utf-8') as f:
        f.write(str(func_kwargs))
    time.sleep(5)


def get_kwargs():
    """save_kwargsで保存されたこのスクリプトファイルのあるフォルダの
    simple_batch_tmp.txtファイルに書き込まれたパラメータを読み込み値を返す。
    読み終わったsimple_batch_tmp.txtは削除する。
    Returns:
        tuple: タプルに入った関数に渡すパラメータ
    """
    param_tmp_file_path = os.path.join(os.path.dirname(__file__), 'simple_batch_tmp.txt')
    kwargs = ''
    try:
        with codecs.open(param_tmp_file_path, 'r', encoding='utf-8') as f:
            kwargs = f.read()
            f.close()
    except Exception:
        return kwargs
    try:
        os.remove(param_tmp_file_path)
    except Exception:
        cmds.warning('Failed removing simple_batch_tmp.txt')
    return eval(kwargs)


# ===============================================
def __search_batch_file_path():
    """
    base_common/utility/_resource/simple_batch フォルダ内のmayabatchファイルパスを返す
    """
    script_file_path = os.path.abspath(__file__).replace('\\', '/')

    if not os.path.isfile(script_file_path):
        return

    script_dir_path = os.path.dirname(script_file_path)

    if not os.path.isdir(script_dir_path):
        return

    resource_dir_path = script_dir_path + '/_resource/simple_batch'

    if not os.path.isdir(resource_dir_path):
        return

    batch_file_path = '{0}/mayabatch.bat'.format(resource_dir_path)

    if not batch_file_path:
        return

    if not os.path.isfile(batch_file_path):
        return

    return batch_file_path


# ===============================================
def load_required_plugins():
    """ファイルを読み込むうえで必須なプラグインをロードする

    maファイルにおいてrequire mtoaが欠如して実行できないファイルが発生していたため、当該エラーが起きないようにする暫定対応
    """
    for plugin in REQUIRED_PLUGINS:
        # プラグインが既にロードされているかどうかを確認
        if not cmds.pluginInfo(plugin, q=True, loaded=True):
            try:
                # プラグインをロード
                cmds.loadPlugin(plugin)
            except Exception:
                pass
