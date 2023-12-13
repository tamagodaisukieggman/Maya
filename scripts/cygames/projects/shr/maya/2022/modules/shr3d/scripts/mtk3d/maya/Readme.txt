3dアーティスト用のツール配置場所はこちらです。
下記ディレクトリ階層下にツールを配置して下さい。
Z:\mtk\tools\maya\modules\mtk3d\scripts\mtk3d\maya\*section*

下記パスがPYTHONPATHに追加されます
Z:\mtk\tools\maya\modules\mtk3d\scripts\

# mayaから呼び出す場合は *mtk3d.maya.* を頭につけてインポートして下さい
import mtk3d.maya.TOOL_NAME

mayaメニュー追加方法
下記ファイルにメニューを追記して下さい。
Z:\mtk\tools\maya\modules\mtk3d\scripts\mtk3d\maya\menu.py
_add_items メソッドにメニューを記述すれば表示出来ます。