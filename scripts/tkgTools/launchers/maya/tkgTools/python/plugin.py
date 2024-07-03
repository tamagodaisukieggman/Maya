# -*- coding: utf-8 -*-
u"""プラグインのロード、アンロードなど

"""
import maya.cmds as cmds

def load(plugin_name):
    u"""pluginのロード

    :param plugin_name: プラグイン名
    :return: bool

    :example:
    >>> load('polyfaceangle.py')
    True
    """
    if not hasattr(cmds, 'pluginInfo'):
        import maya.standalone
        maya.standalone.initialize(name='python')

    if not cmds.pluginInfo(plugin_name, q=True, l=True):
        try:
            print(u'load plugin: {}'.format(plugin_name))
            cmds.loadPlugin(plugin_name)
            return True
        except Exception:
            print(u'プラグインのロードに失敗しました: {0}'.format(plugin_name))
            return False
    return True


def unload(plugin_name):
    u"""pluginのアンロード

    :param plugin_name: プラグイン名
    :return: bool

    :example:
    >>> unload('polyfaceangle.py')
    True
    """
    if not hasattr(cmds, 'pluginInfo'):
        import maya.standalone
        maya.standalone.initialize(name='python')

    if cmds.pluginInfo(plugin_name, q=True, l=True):
        try:
            print(u'unload plugin: {}'.format(plugin_name))
            cmds.unloadPlugin(plugin_name)
            return True
        except Exception:
            print(u'プラグインのアンロードに失敗しました: {0}'.format(plugin_name))
            return False
    return True
