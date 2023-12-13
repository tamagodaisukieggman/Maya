# -*- coding:utf-8 -*-
import maya.cmds as mc
import maya.mel as mm
import os


def envs(*args):
    lang = []
    append = lang.append
    for k, v in os.environ.items():
        if k == "MAYA_UI_LANGUAGE":
            append(v)
    return lang


def viewChange(*args):
    sFeF = args[0]
    env = envs()
    if sFeF == 'start':
        if env:
            if env[0] == 'en_US':
                mm.eval('setNamedPanelLayout("Single Perspective View")')
                mc.modelPanel("modelPanel4", edit=True, up=True)
            elif env[0] == 'ja_JP':
                mm.eval(u'setNamedPanelLayout ("単一のパース ビュー")')
                mc.modelPanel("modelPanel4", edit=True, up=True)
        else:
            mm.eval(u'setNamedPanelLayout ("単一のパース ビュー")')
            mc.modelPanel("modelPanel4", edit=True, up=True)
    else:
        if env:
            if env[0] == 'en_US':
                mm.eval('setNamedPanelLayout("Single Perspective View")')
            elif env[0] == 'ja_JP':
                mm.eval(u'setNamedPanelLayout ("単一のパース ビュー")')
        else:
            mm.eval(u'setNamedPanelLayout ("単一のパース ビュー")')
