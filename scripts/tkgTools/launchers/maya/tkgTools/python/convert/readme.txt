（編集中）
■複数のFBXファイルを変換する方法
1. 元のアニメーションFBXを下記パスにコピーしてください。
c:\cygames\wiz2\tools\maya\scripts\rig\convert\fbx\from\
2. Script Editorで下記コマンドを実行します。
-----------------------------
from imp import reload
import rig.convert.runfiles as convertRunfiles
reload(convertRunfiles)
-----------------------------
3. キャラクター別で実行します。それぞれ1番でコピーしたFBXのモーションを変換します。
# p1のモーションをp2に変換する
convertRunfiles.hik_convert_p1_p2()
# p2のモーションをp1に変換する
convertRunfiles.hik_convert_p2_p1()
# p1のモーションをゴーストに変換する
convertRunfiles.hik_convert_p1_enm_m_ghost01()
# p2のモーションをゴーストに変換する
convertRunfiles.hik_convert_p2_enm_m_ghost01()
