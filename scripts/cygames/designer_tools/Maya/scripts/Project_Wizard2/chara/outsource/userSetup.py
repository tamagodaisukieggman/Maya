# -*- coding: utf-8 -*-

def main():
    u"""メニュー追加
    :return: None
    """
    import maya.utils
    menu_cmd = 'from menu import CygamesMenu;CygamesMenu.main()'
    maya.utils.executeDeferred(menu_cmd)


if __name__ == '__main__':
    main()
