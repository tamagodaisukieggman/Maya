# -*- coding: utf-8 -*-
u"""ジョイントのジオメトリ化ツール
"""
from .gui import BakeSimulatedBone


def main():
    u"""main関数"""
    dialog = BakeSimulatedBone()
    dialog.show()
