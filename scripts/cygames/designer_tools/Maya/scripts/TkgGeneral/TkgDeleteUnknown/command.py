# -*- coding: utf-8 -*-
'''TkgDeleteUnknown
アンノウンノードの削除用スクリプトです
'''


import maya.cmds as cmds


#//========================================================== const


TOOL_NAME = u"TkgDeleteUnknown"
'''ツール名
'''


CONFIRM_OK = u"OK"
'''確認ダイアログのOKボタン
'''


CONFIRM_CANCEL = u"Cancel"
'''確認ダイアログのキャンセルボタン
'''


#//==========================================================


# アンノウンノードの削除処理
def execute():
    '''アンノウンノードの削除処理
    '''

    nodes = cmds.ls(type="unknown")
    cmds.lockNode(nodes, lock=0)
    cmds.delete(nodes)
    pass


# メイン関数
# ダイアログ等のUIも含めてしまっています
def main():
    '''確認ダイアログを表示しての削除実行
    '''

    # Unknownノードを列挙
    nodes = cmds.ls(type="unknown")

    # Unknownがない場合告知して終了
    if len(nodes) == 0:
        cmds.confirmDialog(
            title = TOOL_NAME,
            message=u"Unknownノードはありません．"
            )
        return 0

    # 実行確認メッセージの作成
    message = []
    message.append(u"次のノードを削除しますがよろしいですか？")
    for node in nodes:
        message.append(node)
    message = "\n".join(message)

    # 確認ダイアログの表示
    confirm = cmds.confirmDialog(
        title = TOOL_NAME,
        message = message,
        button = [CONFIRM_OK, CONFIRM_CANCEL],
        defaultButton = CONFIRM_OK,
        dismissString = CONFIRM_CANCEL,
        )

    # ダイアログの結果次第で処理を実行
    if confirm == CONFIRM_OK:
        execute()
        cmds.confirmDialog(
            title = TOOL_NAME,
            message = u"【{0}】件のアンノウンノードを削除しました．".format(len(nodes))
            )
    
    elif confirm == CONFIRM_CANCEL:
        cmds.confirmDialog(
            title = TOOL_NAME,
            message = u"アンノウンノードの削除をキャンセルします．"
            )
    
    else:
        cmds.confirmDialog(
            title = TOOL_NAME,
            message = u"ダイアログから不明な値【{0}】が返りました．TAまで報告をお願いします．"
            )
        return -1

    return 0


if __name__ == "__main__":
    sys.exit(int(main() or 0))