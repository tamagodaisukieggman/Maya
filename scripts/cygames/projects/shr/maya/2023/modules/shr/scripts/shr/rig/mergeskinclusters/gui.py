# -*- coding: utf-8 -*-

from __future__ import absolute_import

import functools
import traceback

import maya.cmds as cmds

from . import command
import mtk.rig.skinweight.command as skinweight


class MergeTargetPanel(object):
    def __init__(self, item_id='', parent=None):
        self.parent = parent
        self.id = item_id
        self.layout = cmds.columnLayout(adj=True, p=parent.item_layout)
        self.geometry = None
        self.components = None
        self.remove_btn = None
        self.init()

    def init(self):
        option_lay = cmds.columnLayout(adj=True, p=self.layout, rs=4)
        option_row = cmds.rowLayout(nc=2, cw2=(110, 100), cl2=['center', 'left'], adj=1,
                                    ct2=['right', 'left'], p=option_lay)

        setting_lay = cmds.columnLayout(adj=True, p=option_row)

        # geometry
        row = cmds.rowLayout(nc=3, cw3=(110, 100, 50), cl3=['center', 'left', 'left'], adj=2,
                             ct3=['right', 'left', 'left'], p=setting_lay)
        cmds.text(label='Geometry : ', p=row)
        self.geometry = cmds.textField(p=row, w=100)
        cmds.button(label='Set...', c=self._on_set_geometry, w=50)

        # components
        row = cmds.rowLayout(nc=3, cw3=(110, 100, 50), cl3=['center', 'left', 'left'], adj=2,
                             ct3=['right', 'left', 'left'], p=setting_lay)
        cmds.text(label='Target Components : ', p=row)
        self.components = cmds.textField(p=row, w=100)
        cmds.button(label='Set...', c=self._on_set_components, w=50)

        # btn_lay
        btn_lay = cmds.columnLayout(adj=True, p=option_row)
        self.remove_btn = cmds.button(label='remove', p=btn_lay, c=self.remove, bgc=[0.3, 0.3, 0.3])

        cmds.separator(h=10, style='in', p=option_lay)

    def _on_set_geometry(self, *args):
        objects = cmds.ls(sl=True, o=True)
        if not objects:
            return

        sc_nodes = skinweight.list_related_skinClusters(objects[0])
        if not sc_nodes:
            cmds.warning(u'スキニングされているジオメトリを指定して下さい。')
            return

        cmds.textField(self.geometry, e=True, tx=objects[0])

    def _on_set_components(self, *args):
        sels = cmds.ls(sl=True)
        if not sels:
            return

        objects = cmds.ls(sels, o=True)
        comps = skinweight.get_object_filtered_components(objects[0], sels)
        if not comps:
            return
        comps = command.reformat_component_strings(comps)

        cmds.textField(self.components, e=True, tx=' '.join(comps))

    def set_data(self, data):
        if 'geometry' in data:
            cmds.textField(self.geometry, e=True, tx=data['geometry'])

        if 'components' in data:
            cmds.textField(self.components, e=True, tx=' '.join(data['components']))

    def get_data(self):
        geometry = cmds.textField(self.geometry, q=True, tx=True).strip(' ')
        if not geometry:
            return {}

        components = cmds.textField(self.components, q=True, tx=True).strip(' ')
        if not components:
            return {}

        return {
            'id': self.id,
            'geometry': geometry,
            'components': components.split(' '),
        }

    def remove(self, *args):
        cmds.deleteUI(self.layout)


class MergeTargetPanels(object):
    def __init__(self, item_cls=MergeTargetPanel, parent=None):
        self.parent = parent
        self.item_cls = item_cls
        self.items = []

        self.layout = parent.target_list_layout
        btn_lay = cmds.rowLayout(nc=2, cw2=(100, 60), cl2=['center', 'left'], adj=1,
                                 ct2=['right', 'left'], p=self.layout)

        cmds.button(label='---  Add Source Item  ---', p=btn_lay, c=self.on_add_item_btn, h=30)
        cmds.button(label='Remove All', p=btn_lay, c=self.on_remove_all_btn,
                    h=30, w=80, bgc=[0.3, 0.3, 0.3])

        scroll_lay = cmds.scrollLayout(p=self.layout, cr=True, vsb=True)
        self.item_layout = cmds.columnLayout(adj=True, rs=2, p=scroll_lay)

        cmds.formLayout(self.layout, e=True,
                        af=[[btn_lay, 'left', 2],
                            [btn_lay, 'right', 2],
                            [btn_lay, 'top', 2],
                            [scroll_lay, 'left', 2],
                            [scroll_lay, 'right', 2],
                            [scroll_lay, 'bottom', 2],
                            ],
                        ac=[[scroll_lay, 'top', 2, btn_lay]],
                        an=[[btn_lay, 'bottom']]
                        )

    def on_add_item_btn(self, *args):
        """Add ボタンコマンド
        """

        self.add_item(command.get_utcnow())

    def on_remove_all_btn(self, *args):
        """Remove Allボタンコマンド
        登録アイテムを全て削除
        """

        if not self.items:
            return

        ret = cmds.confirmDialog(
            title='Remove All List Items.',
            message='Are you sure you want to delete lists?',
            button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No',
            parent=self.parent._tool_name,
        )

        if ret == 'Yes':
            self.remove_all(save=True)

    def get_item(self, item_id=''):
        """IDに一致するSelectionListItemオブジェクトを取得
        :param str item_id: ID
        :return: SelectionListItem
        :rtype: SelectionListItem
        """
        if not item_id:
            return

        for item in self.items:
            if item_id == item.id:
                return item

    def add_item(self, item_id):
        """アイテム追加
        :return: MergeTargetPanelオブジェクト
        :rtype: MergeTargetPanel
        """

        item = self.item_cls(item_id, parent=self)
        cmds.button(item.remove_btn, e=True, c=functools.partial(self.remove_item, item_id))
        self.items.append(item)
        return item

    def remove_item(self, item_id='', *args):
        """IDに一致するSelectionItemオブジェクトを削除
        :param str item_id: ID
        :param bool save: 削除後にSave処理を行うかのブール値
        """

        if not self.items:
            return

        for item in self.items[::]:
            if item_id == item.id:
                item.remove()
                self.items.remove(item)
                break

    def remove_all(self, save=True, *args):
        """全てのSelectionItemオブジェクトを削除
        :param bool save: 削除後にSave処理を行うかのブール値
        """

        if not self.items:
            return

        for item in self.items[::]:
            self.remove_item(item.id)

    def get_items(self, *args):
        """
        :param args:
        :return: MergeTargetPanelsのデータを辞書で取得
        :rtype: dict
        """

        ret = []

        if not self.items:
            return ret

        for item in self.items:
            item_data = item.get_data()
            if item_data:
                ret.append(item_data)

        return ret


class MergeSkinclusterGUI(object):
    def __init__(self, *args, **kwargs):
        super(MergeSkinclusterGUI, self).__init__(*args, **kwargs)

        self._tool_name = 'mergeskinclusters'
        self.title = 'Merge SkinClusters'
        self._help_url = ''

        self.width = 300
        self.height = 500
        self.margin = 2

        self.target_list_layout = None
        self.target_list_items = None

        self.duplicate_influences = None
        self.merge_target = None

    def show(self, *args):
        """ウィンドウ表示
        """

        self.close()
        win = cmds.window(self._tool_name, title=self.title, mb=True, w=self.width, h=self.height, rtf=True)

        # Edit - Menu
        edit_menu = cmds.menu(label='Edit', p=win)
        cmds.menuItem(label='Load from Selected blendShape', p=edit_menu, c=self.set_data_from_blendshape)
        cmds.menuItem(d=True, p=edit_menu)
        cmds.menuItem(label='Save Settings', p=edit_menu, c=self.save_settings)
        cmds.menuItem(label='Reset Settings', p=edit_menu, c=self.reset_settings)
        cmds.menuItem(d=True, p=edit_menu)
        cmds.menuItem(label='Quit', p=edit_menu, c=self.close)

        # Main Layout
        main_lay = cmds.formLayout(p=win, nd=100)
        self.target_list_layout = cmds.formLayout(nd=100, p=main_lay)
        self.target_list_items = MergeTargetPanels(parent=self)

        main_ctrl = cmds.columnLayout(adj=True, p=main_lay)

        cmds.separator(style='in', p=main_ctrl)

        # merge target
        row = cmds.rowLayout(nc=3, cw3=(110, 100, 50), cl3=['center', 'left', 'left'], adj=2, h=30,
                             ct3=['right', 'left', 'left'], p=main_ctrl)
        cmds.text(label='Merge Geometry : ', p=row)
        self.merge_target = cmds.textField(p=row, w=100)
        cmds.button(label='Set...', c=self._on_set_geometry, w=50)

        row = cmds.rowLayout(nc=2, cw2=[110, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=main_ctrl)
        cmds.text(l='', w=50, p=row)
        self.duplicate_influences = cmds.checkBox(l='Duplicate Influences', v=False, p=row)

        cmds.button(label='Apply Merge', p=main_ctrl, c=self.on_apply_merge, h=40)
        cmds.formLayout(main_lay, e=True,
                        af=[[self.target_list_layout, 'top', self.margin],
                            [self.target_list_layout, 'left', self.margin],
                            [self.target_list_layout, 'right', self.margin],
                            [main_ctrl, 'left', self.margin],
                            [main_ctrl, 'right', self.margin],
                            [main_ctrl, 'bottom', self.margin],
                            ],
                        an=[[main_ctrl, 'top']
                            ],
                        ac=[[self.target_list_layout, 'bottom', self.margin, main_ctrl]
                            ]
                        )

        cmds.showWindow(win)

        self.reset_settings()
        self.load_settings()

    def close(self, *args):
        """ウィンドウを閉じる
        """

        if cmds.window(self._tool_name, q=True, ex=True):
            cmds.deleteUI(self._tool_name)

    def get_settings(self, *args):
        return {
            'merge_target': cmds.textField(self.merge_target, q=True, tx=True).strip(' '),
            'duplicate_influences': cmds.checkBox(self.duplicate_influences, q=True, v=True),

            'source_items': self.target_list_items.get_items()
        }

    def save_settings(self, *args):
        settings = self.get_settings()
        try:
            command.save_optionvar('%s__ui_options' % self._tool_name, settings)

        except Exception as e:
            cmds.error(traceback.format_exc())

    def load_settings(self, *args):
        read_values = command.load_optionvar('%s__ui_options' % self._tool_name)

        if read_values:
            try:
                if 'merge_target' in read_values:
                    cmds.textField(self.merge_target, e=True, tx=read_values.get('merge_target', ''))

                if 'duplicate_influences' in read_values:
                    cmds.checkBox(self.duplicate_influences, e=True, v=read_values.get('duplicate_influences', True))

                if 'source_items' in read_values:
                    for item_data in read_values.get('source_items', []):
                        item = self.target_list_items.add_item(item_data['id'])
                        item.set_data(item_data)

            except Exception as e:
                cmds.error(traceback.format_exc())

    def reset_settings(self, *args):
        cmds.textField(self.merge_target, e=True, tx='')
        cmds.checkBox(self.duplicate_influences, e=True, v=False)

        self.target_list_items.remove_all()

    def set_data_from_blendshape(self, *args):
        sels = cmds.ls(sl=True)
        if not sels:
            return

        bs_nodes = command.list_related_blendShape(sels)
        if not bs_nodes:
            return

        self.target_list_items.remove_all()

        data_list = command.get_merge_data_from_blendshape_weight(bs_nodes[0])
        for key, values in data_list.items():
            if not skinweight.list_related_skinClusters(key):
                print('Add Skip : {} : not found skinCluster node.'.format(key))
                continue

            if skinweight.list_related_skinClusters(key) and values:
                item = self.target_list_items.add_item(command.get_utcnow())
                item.set_data({'geometry': key, 'components': values})

        node = cmds.listRelatives(cmds.blendShape(bs_nodes[0], q=True, g=True), p=True, pa=True)[0]
        cmds.textField(self.merge_target, e=True, tx=node)

    def on_apply_merge(self, *args):
        merge_target = cmds.textField(self.merge_target, q=True, tx=True)
        duplicate_influences = cmds.checkBox(self.duplicate_influences, q=True, v=True)
        item_data = self.target_list_items.get_items()
        components = [data['components'] for data in item_data]
        targets = [data['geometry'] for data in item_data]

        command.merge_skincluster(
            merge_target,
            components,
            targets,
            duplicate_joints=duplicate_influences,
        )

        self.save_settings()

    def _on_set_geometry(self, *args):
        objects = cmds.ls(sl=True, o=True)
        if not objects:
            return

        cmds.textField(self.merge_target, e=True, tx=objects[0])
