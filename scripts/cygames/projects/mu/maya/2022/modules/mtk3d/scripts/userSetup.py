# -*- coding: utf-8 -*-

def main():
    print('Load: mutsunokami (3DCG)')

    import maya.utils
    maya.utils.executeDeferred('from mtk3d.maya.menu import Mtk3dMenu;Mtk3dMenu.main()')

if __name__ == '__main__':
    main()
