# -*- coding: utf-8 -*-
u"""mergeskincluster(GUI)

..
    BEGIN__CYGAMES_MENU
    label=Merge Skinclusters...
    command=main()
    order=1000
    END__CYGAMES_MENU

"""

# from mtku.maya.mtklog import MtkLog

from . import gui

# logger = MtkLog(__name__)
import logging
from tatool.log import ToolLogging, Stage

tool_name = "Merge Skinclusters"
logger = ToolLogging("mutsunokami", "maya", target_stage=Stage.dev, tool_version="v1.0.0").getTemplateLogger(tool_name)
logger.setLevel(logging.DEBUG)


def main():
    u"""main関数"""
    # logger.usage()

    ui = gui.MergeSkinclusterGUI()
    ui.show()
