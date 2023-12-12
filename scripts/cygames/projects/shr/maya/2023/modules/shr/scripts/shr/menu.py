""" 'mutsunokami' メニューを追加
"""

import os
import sys
import yaml
import importlib
from pathlib import Path
from maya import cmds
from maya import mel

from shr import logger

HERE = Path(os.path.dirname(os.path.abspath(__file__)))


class Menu:

    def __init__(self) -> None:
        self.menu_config = self._load_menu_config()

    def _load_menu_config(self) -> dict:
        with open(HERE.joinpath('menu.yaml'), encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config

    def find_icon(self, icon_file: str) -> Path:
        icon = ''

        if not icon_file:
            return icon

        if icon_file:
            icon = HERE.joinpath('../../icons/{}'.format(icon_file))
            if not icon.exists():
                logger.warning('Icon file {icon_file} is not found at "{icon_path}"'.format(
                    icon_file=icon_file,
                    icon_path=str(icon.resolve().as_posix()))
                )
                return ''
        return icon

    def _create_menu_item(self, item: dict, is_child=False) -> None:
        """コンフィグ情報を元にメニューアイテムを作成
        """
        type_ = item.get('type')
        label = item.get('label', 'NO LABEL')
        tearoff = item.get('tearoff', True)
        enable = item.get('enable', True)
        command = item.get('command', '')
        option_command = item.get('optionCommand', '')
        document = item.get('document', '')
        annotation = item.get('annotaion', '')
        icon = self.find_icon(item.get('icon', ''))

        # Sub Menu Type
        if type_ == 'submenu' and not is_child:
            cmds.menuItem(label=label,
                          subMenu=True,
                          tearOff=tearoff,
                          parent=self.menu_config['name'],
                          image=icon,
                          enable=enable)

            # Create Children
            if item.get('children'):
                self._create_childmenus(item)
            else:
                logger.warning('This submenu "{}" does not have children.'.format(label))

        # Command Type
        if type_ == 'command':
            if not command:
                logger.error('Command is not set at "{}" command type menu.'.format(label))
                enable = False
                command = 'print("Command is not found")'

            cmds.menuItem(label=label,
                          annotation=annotation,
                          command=command,
                          image=icon,
                          enable=enable)

            if option_command:
                cmds.menuItem(command=option_command,
                              optionBox=True)

        # Divider Type
        if type_ == 'divider':
            label = item.get('label', '')
            cmds.menuItem(divider=True, dividerLabel=label)

        # Document Type
        if type_ == 'document':
            cmds.menuItem(label=label,
                          command='import webbrowser;webbrowser.open("{}")'.format(document),
                          image=icon)

    def _create_childmenus(self, item: dict) -> None:
        """Create submenu children
        """

        # Create child submenus
        children = item['children']
        for child in children:
            type_ = child.get('type')
            if not type_:
                continue  # typeが入力されて無い場合は無視

            self._create_menu_item(child, is_child=True)

        # End submenu
        cmds.setParent('..', menu=True)

    def init(self) -> None:
        """menu.yamlファイルからロードしたコンフィグ情報を元にメニューを初期構築
        """
        main_window = mel.eval('$temp=$gMainWindow')

        # コンフィグで、nameが設定されていない場合はエラーを出して終了
        menu_name = self.menu_config.get('name')
        if not menu_name:
            logger.error('Menu object name key "name" is not set in the config.')
            return
        menu_lable = self.menu_config.get('label', menu_name)

        # コンフィグで、menusが設定されてない場合はエラーを出して終了
        menus = self.menu_config.get('menus')
        if not menus:
            logger.error('Loading menu.yaml or getting menu info is failed.')
            return

        # Main Menuの追加
        self.menu = cmds.menu(menu_name,
                              label=menu_lable,
                              parent=main_window,
                              tearOff=True,
                              allowOptionBoxes=True)

        # Sub Menuを追加
        for item in menus:
            type_ = item.get('type', None)
            if not type_:
                continue  # typeが入力されて無い場合は無視

            self._create_menu_item(item)

    def reload(self) -> None:
        logger.debug('Reaoad "shr" modules.')
        importlib.reload(sys.modules['shr'])

        main_window = mel.eval('$temp=$gMainWindow')

        menu_name = self.menu_config.get('name')
        if not menu_name:
            logger.error('Menu object name key "name" is not set in the config.')
            return
        menu_lable = self.menu_config.get('label', menu_name)

        logger.debug('Delete all items of "{}" menu.'.format(menu_lable))
        if cmds.menu(menu_name, label=menu_lable,
                     parent=main_window, exists=True):
            cmds.deleteUI(cmds.menu(menu_name, deleteAllItems=True, edit=True))

        logger.debug('Recreate "{}" menu items.'.format(menu_lable))
        self.init()


def create_menus():
    menu = Menu()
    menu.init()


def reload_menus():
    cmds.evalDeferred("import shr.menu;menu.Menu().reload()")
