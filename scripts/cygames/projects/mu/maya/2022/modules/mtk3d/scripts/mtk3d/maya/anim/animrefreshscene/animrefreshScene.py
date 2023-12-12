# -*- coding: utf-8 -*-

import maya.cmds as mc
import re

checkText = []

def main():
    #ダイアログ作成
    dialog = mc.confirmDialog( title=u'リフレッシュ確認', message=u"""【シーンリフレッシュ】
以下の処理を行います。

■ 選択されているセット内のアニメーションをベイク
■ アニメーションレイヤのベイク （ベースレイヤ以外削除）
■ リファレンスされていないオブジェクトの削除
■ IK/FKをベイクし、デフォルトへ戻す
■ スペースをベイクし、全てのスペースをデフォルトへ戻す
■ SceneOptimize （シーンの最適化）

※※ リリース直前に行ってください！ ※※

よろしいですか？
""", button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No', icn='warning' )

    if dialog == "Yes":

        ctrlSet = mc.ls(os=1)

        #CtrlSetが選択されているかチェックする
        if ctrlSet == [] :
            mc.confirmDialog(title=u'エラー', message=u"CtrlSetを選択してください。")
        else :
            for l in range(len(ctrlSet)):
                checkText = re.split(':', ctrlSet[l])[1]
                if checkText == "CtrlSet" :
                    print("Verify.")
                else :
                    mc.confirmDialog(title=u'エラー', message=u"CtrlSetを選択してください。")
                    break
            else:
                print("All set are rights.")
                execute(ctrlSet)

    elif dialog == "No":
        print("Canceled.")


def execute(ctrlSet):

    CtrlSet = ctrlSet

    from mtk3d.maya.rig.refresh import common as refresh_common
    reload(refresh_common)

    rcr=refresh_common.RefreshScene(ctrl_set=CtrlSet)
    rcr.main()
