# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import csv
import re
import sys

import maya.cmds as cmds

import command


def select_root():
    nodes = cmds.ls(l=True, assemblies=True)
    model = r'^\|mdl_(unt|avt|enm|smn)_((([0-9]{4})([0-9]{2}))|(common[S|M]))_([1-3]{1})$'
    pattern = re.compile(model)

    cmds.select(cl=True)

    for node in nodes:
        if pattern.match(node):
            cmds.select(node, r=True)
            return


def retarget(animation_path, rig_path, export_path):
    print('Retarget: {} > {} > {}'.format(animation_path, rig_path, export_path))
    if not os.path.isfile(animation_path):
        print('#'*100)
        print(u'エラー: アニメーションファイルが存在しません。 {}'.format(animation_path))
        print('#'*100)
        return

    if not os.path.isfile(rig_path):
        print('#'*100)
        print(u'エラー: リグファイルが存在しません。 {}'.format(rig_path))
        print('#'*100)
        return

    if not os.path.isdir(os.path.dirname(export_path)):
        print('#'*100)
        print(u'エラー: 出力フォルダが存在しません。 {}'.format(os.path.dirname(export_path)))
        print('#'*100)
        return

    cmds.file(rig_path, o=True, f=True)

    select_root()
    command.main(animation_path)

    cmds.file(rn=export_path)
    cmds.file(s=True, f=True)


def retarget_from_csv(csv_path):
    if not os.path.isfile(csv_path):
        print('#'*100)
        print(u'エラー: csvファイルが存在しません。 {}'.format(csv_path))
        print('#'*100)
        return

    try:
        with open(csv_path) as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
    except Exception:
        print('#'*100)
        print(u'エラー: 不正なcsvファイルです。 {}'.format(csv_path))
        print('#'*100)
        return

    for row in rows:
        if len(row) >= 3:
            retarget(row[0], row[1], row[2])


def main():
    argv = sys.argv[1:]

    if not argv:
        print('#'*100)
        print(u"使用方法: 以下のフォーマットのcsvファイルをドラッグ&ドロップしてください。")
        print(u"アニメーションファイルパス,リグファイルパス,出力ファイルパス")
        print('#'*100)
        return

    retarget_from_csv(argv[0])


if __name__ == "__main__":
    main()
