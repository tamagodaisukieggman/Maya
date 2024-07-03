# -*- coding: utf-8 -*-
u"""skinweight(GUI)

..
    label=Skin Weight ... : スキンウェイトツール
    command=main()
    order=1000

"""

from . import gui


def main():
    u"""main関数"""

    ui = gui.SkinWeightGUI()
    ui.show()

main()