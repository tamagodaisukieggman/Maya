------------------------------------------------------------
cyMatchControllerの起動方法
------------------------------------------------------------

1,C:\Users\??????\Documents\maya\scriptsに「cyMatchController」フォルダをそのまま入れてください。

2,Mayaのスクリプトエディタ上で下記のコマンドを実行すると、
cyMatchControllerが起動します。


import cyMatchController
import cyMatchController.ui.ui as UI
reload(cyMatchController)
reload(UI)

UI.ui()