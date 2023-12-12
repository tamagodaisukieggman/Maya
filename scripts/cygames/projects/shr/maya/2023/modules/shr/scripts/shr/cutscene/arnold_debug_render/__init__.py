# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from . import app


def start_rendering(view_settings):
    app.ArnoldDebugRender.render(view_settings)

# sample設定
# view_settings["Frame"] = "指定フレーム"
# view_settings["CutName"] = "カット名"
# view_settings["SceneName"] = "シーン名"
# view_settings["FocalLength"] = "フォーカルレングスの値"
# view_settings["is_after_explorer"] = "撮影後エクスプローラーを開くか"
# view_settings["is_draw_outline"] = "文字にアウトラインを入れるか"
# view_settings["camera"] = "指定カメラ名"

