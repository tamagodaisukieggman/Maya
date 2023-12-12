# -*- coding: utf-8 -*-
u"""skinweight(GUI)

..
    BEGIN__CYGAMES_MENU
    label=Skin Weight ... : スキンウェイトツール
    command=main()
    order=1000
    END__CYGAMES_MENU

"""
import logging
from tatool.log import ToolLogging, Stage
# from mtku.maya.mtklog import MtkLog

from . import gui

logger = ToolLogging("mutsunokami", "maya", target_stage=Stage.dev, tool_version="v1.0.0").getTemplateLogger("Skin Weight ... : スキンウェイトツール")
logger.setLevel(logging.DEBUG)
# logger = MtkLog(__name__)


def main():
    u"""main関数"""
    # logger.usage()

    ui = gui.SkinWeightGUI()
    ui.show()
