#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import glob
import os
import yaml

import maya.cmds as cmds
import maya.mel as mel


class Menu():
    u"""Menuクラス"""

    @staticmethod
    def get_menu_yaml_path_list():
        menu_yaml_list = []
        for menu_yaml_dir_path in os.getenv('MAYA_MENU_PATH').split(';'):
            menu_yaml = glob.glob(menu_yaml_dir_path + '\menu.yaml')
            if menu_yaml:
                menu_yaml_list.append(menu_yaml[0])
        return menu_yaml_list

    def create_menu(self, data, is_root=True):
        for k in list(data.keys()):
            if is_root:
                maya_win_name = mel.eval("$temp=$gMainWindow")
                cmds.setParent(maya_win_name)
                if k == 'cygames':
                    cmds.setParent('CyMenuUI', menu=True)
                    cmds.menuItem(d=True)
                else:
                    cmds.menu(k, p=maya_win_name, l=k, to=True)
            else:
                if k == 'Separator':
                    cmds.menuItem(d=True)
                else:
                    cmds.menuItem(sm=True, l=k, to=True)

            for v in data[k]:
                if type(v) is dict:
                    if 'name' in list(v.keys()):
                        args = {}
                        if 'label' in list(v.keys()):
                            args['l'] = v['label']
                        if 'shelfName' in list(v.keys()):
                            args['iol'] = v['shelfName']
                        if ('type' in list(v.keys())) and ('command' in list(v.keys())):
                            args['c'] = self.get_boot_command(v['type'], v['command'])
                        if 'optionBox' in list(v.keys()):
                            args['ob'] = v['optionBox']
                        if 'annotation' in list(v.keys()):
                            args['annotation'] = v['annotation']
                        cmds.menuItem(**args)
                    else:
                        self.create_menu(v, False)
                elif v == 'separator':
                    cmds.menuItem(d=True)

            cmds.setParent('..', menu=True)

    def reload_tools(self, *args):
        self.load_menu()

    @staticmethod
    def get_boot_command(typ, command):
        if typ == "Mel":
            command = "mel.eval(\"%s\")" % command
        elif typ == "Python":
            command = command

        return command

    def load_menu(self):
        for menu_yaml_path in self.get_menu_yaml_path_list():
            print(menu_yaml_path)
            f = codecs.open(menu_yaml_path, 'r', 'utf-8')
            data = yaml.load(f)
            f.close()
            print(data)
            self.create_menu(data)


def main():
    menu = Menu()
    menu.load_menu()
