# -*- coding: utf-8 -*-
"""Selection List

..
    END__CYGAMES_DESCRIPTION
"""

import functools
import traceback

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

from tatool.config import Config

from . import command


def save_optionvar(key, value, force=True):
    """optionVarに保存

    :param str key: キー名
    :param mixin value: 値
    :param bool force: 強制的に上書きするかのブール値

    :return: 保存できたかどうかのブール値
    :rtype: bool
    """

    v = str(value)
    if force:
        cmds.optionVar(sv=[key, v])
        return True
    else:
        if not cmds.optionVar(ex=key):
            cmds.optionVar(sv=[key, v])
            return True
        else:
            return False


def load_optionvar(key):
    """optionVarを取得

    :param str key: キー名
    :return: 保存された値, キーが見つからない場合は None
    :rtype: value or None
    """

    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None


class SelectionListItem(object):
    def __init__(self, item_id='', label='', parent=None):
        self.parent = parent
        self.layout = cmds.columnLayout(adj=True, p=parent.item_layout)
        self.id = item_id
        self.label = label
        self._items = []
        self.init()

    def init(self):
        option_lay = cmds.columnLayout(adj=True, p=self.layout, rs=4)

        btn_lay = cmds.rowLayout(nc=4, cw4=(100, 24, 24, 30), cl4=['center', 'left', 'left', 'left'], adj=1,
                                 ct4=['right', 'left', 'left', 'left'], p=option_lay)

        self.select_btn = cmds.button(label=self.label, p=btn_lay, h=24, w=100,
                                      c=self.select, bgc=[0.4, 0.4, 0.4],
                                      ann=u'修飾キー\n'
                                          u'None : Replace\n'
                                          u'Shift : Add\n'
                                          u'Ctrl : Toggle\n'
                                          u'Alt : Deselect'
                                      )

        self.edit_label_btn = cmds.button(label='E', p=btn_lay, h=24, w=24, c=self.change_label,
                                          ann=u'アイテムラベルの変更')

        self.show_btn = cmds.button(label='P', p=btn_lay, h=24, w=24, c=self.show_items,
                                    ann=u'登録アイテムの表示')

        self.remove_btn = cmds.iconTextButton(label='remove', p=btn_lay, h=24, w=30,
                                              i=command.get_icon('remove.png'), style='iconOnly',
                                              ann=u'登録アイテムの削除',
                                              c=self.remove, bgc=[0.4, 0.4, 0.4])

        # modifiers : None
        ctl = cmds.popupMenu(b=3, p=self.select_btn)
        cmds.popupMenu(ctl, e=True,
                       pmc=functools.partial(self.populate_namespace_menu, ctl, 0))

        # modifiers : Shift
        ctl = cmds.popupMenu(b=3, sh=True, p=self.select_btn)
        cmds.popupMenu(ctl, e=True,
                       pmc=functools.partial(self.populate_namespace_menu, ctl, 1))

        # modifiers : Ctrl
        ctl = cmds.popupMenu(b=3, ctl=True, p=self.select_btn)
        cmds.popupMenu(ctl, e=True,
                       pmc=functools.partial(self.populate_namespace_menu, ctl, 4))

        # modifiers : Alt
        ctl = cmds.popupMenu(b=3, alt=True, p=self.select_btn)
        cmds.popupMenu(ctl, e=True,
                       pmc=functools.partial(self.populate_namespace_menu, ctl, 8))

    def _set_items(self, items):
        self._items = items

    def _get_items(self):
        return self._items

    items = property(_get_items, _set_items)

    def show_items(self, *args):
        """アイテムの表示
        """

        OpenMaya.MGlobal.displayInfo(self.items)

    def remove(self, *args):
        """アイテムの削除
        """
        cmds.deleteUI(self.layout)

    def select(self, namespace='', modifiers=0, *args):
        """アイテムの選択
        :param str namespace: ネームスペース名
        :param int modifiers: keyboard modifiers
        """

        modifiers = modifiers if modifiers else cmds.getModifiers()

        # alt
        if (modifiers & 8) > 0:
            select_option = {'deselect': True}

        # ctrl
        elif (modifiers & 4) > 0:
            select_option = {'toggle': True}

        # shift
        elif (modifiers & 1) > 0:
            select_option = {'add': True}

        else:
            select_option = {'replace': True}

        if not namespace:
            valid_items = [item for item in self.items if cmds.objExists(item)]
            if not valid_items:
                cmds.warning(u'Item not found : {}'.format(self.items))
                return

            if self.parent.parent.keep_order:
                if select_option.get('replace', False):
                    cmds.select(cl=True)
                    [cmds.select(item, add=True, noExpand=True) for item in valid_items]

                elif select_option.get('add', False) or select_option.get('toggle', False):
                    [cmds.select(item, noExpand=True, **select_option) for item in valid_items]

                else:
                    cmds.select(valid_items, noExpand=True, **select_option)
            else:
                cmds.select(valid_items, noExpand=True, **select_option)

        else:
            ns_items = [command.replace_namespace(item, namespace) for item in self.items]
            valid_items = [item for item in ns_items if cmds.objExists(item)]
            if not valid_items:
                cmds.warning(u'Item not found : {}'.format(ns_items))
                return

            if self.parent.parent.keep_order:
                if select_option.get('replace', False):
                    cmds.select(cl=True)
                    [cmds.select(item, add=True, noExpand=True) for item in valid_items]

                elif select_option.get('add', False) or select_option.get('toggle', False):
                    [cmds.select(item, noExpand=True, **select_option) for item in valid_items]

                else:
                    cmds.select(valid_items, noExpand=True, **select_option)
            else:
                cmds.select(valid_items, noExpand=True, **select_option)

    def list_namespaces(self):
        """シーン内のルートネームスペースをリスト
        :return: ネームスペース名のリスト
        :rtype: list
        """
        return [':'] + command.list_namespaces(root_namespace=':', recurse=True)

    def populate_namespace_menu(self, ctl, modifiers, *args):
        """右クリックメニューの表示
        :param str ctl: popupMenuコントロール名
        :param int modifiers: keyboard modifiersの数値

        """

        cmds.popupMenu(ctl, e=True, dai=True)
        # cmds.menuItem(l='Change Label', radialPosition='N', p=ctl, c=self.change_label)
        for namespace in self.list_namespaces():
            cmds.menuItem(p=ctl, l=namespace,
                          c=functools.partial(self.select, namespace, modifiers))

    def change_label(self, *args):
        """アイテムラベルの変更
        """

        result = cmds.promptDialog(
            title='Change Label',
            message='Enter New Item Label',
            text=self.label,
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel',
            parent=self.parent.parent._tool_name,
        )

        if result == 'OK':
            self.label = cmds.promptDialog(query=True, text=True)
            cmds.button(self.select_btn, e=True, l=self.label)
            self.parent.parent.save_selection_items()


class SelectionListItems(object):
    def __init__(self, item_cls=SelectionListItem, parent=None):
        self.parent = parent
        self.item_cls = item_cls
        self.items = []

        self.layout = parent.selection_list_layout
        btn_lay = cmds.rowLayout(nc=2, cw2=(100, 60), cl2=['center', 'left'], adj=1,
                                 ct2=['right', 'left'], p=self.layout)

        cmds.button(label='---  Add  ---', p=btn_lay, c=self.on_add_item_btn, h=30)
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
        """Addボタンコマンド
        選択ノードをSelectionListに追加
        """

        selections = cmds.ls(os=True)
        if not selections:
            cmds.warning(u'登録したいノードを選択して下さい。')
            return

        text = ', '.join(selections) if len(selections) < 5 else (', '.join(selections[:5]) + ' ...')
        result = cmds.promptDialog(
            title='Add Item Dialog',
            message='Enter New Item Label',
            text=text,
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel',
            parent=self.parent._tool_name,
        )

        if result == 'OK':
            text = cmds.promptDialog(query=True, text=True)

            self.add_item(command.get_utcnow(), text, selections)

    def on_remove_all_btn(self, *args):
        """Remove Allボタンコマンド
        登録アイテムを全て削除
        """

        if not self.items:
            return

        ret = cmds.confirmDialog(
            title='Remove All Selection List Items.',
            message='Are you sure you want to delete selection lists?',
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

    def add_item(self, item_id, label, items, save=True):
        """アイテム追加
        :param str item_id: id
        :param str label: ラベル
        :param list items: 追加アイテムのリスト
        :return: SelectionListItemオブジェクト
        :rtype: SelectionListItem
        """
        if not item_id:
            return

        item = self.item_cls(item_id, label, parent=self)
        item.items = items
        cmds.iconTextButton(item.remove_btn, e=True, c=functools.partial(self.remove_item, item_id))
        self.items.append(item)

        if save:
            self.parent.save_selection_items()

        return item

    def remove_item(self, item_id='', save=True, *args):
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

        if save:
            self.parent.save_selection_items()

    def remove_all(self, save=True, *args):
        """全てのSelectionItemオブジェクトを削除
        :param bool save: 削除後にSave処理を行うかのブール値
        """

        if not self.items:
            return

        for item in self.items[::]:
            self.remove_item(item.id, save=save)

    def get_item_dict(self, *args):
        """
        :param args:
        :return: SelectionListItemsのデータを辞書で取得
        :rtype: dict
        """

        ret = {}

        if not self.items:
            return ret

        for item in self.items:
            ret[item.id] = {'label': item.label, 'item': item.items}

        return ret


class SelectionListGUI(object):
    def __init__(self, *args, **kwargs):
        super(SelectionListGUI, self).__init__(*args, **kwargs)

        self._tool_name = 'selectionlist'
        self.title = 'Selection List'
        self._help_url = 'https://wisdom.cygames.jp/display/mutsunokami/SelectionList'

        self.width = 300
        self.height = 500
        self.margin = 2

        self.keep_order_menu = None
        self.selection_list_layout = None
        self.selection_list_items = None
        self._namespace = None
        
        self.config = Config("Selection List", 'selections')

    def show(self, *args):
        """ウィンドウ表示
        """

        self.close()
        win = cmds.window(self._tool_name, title=self.title, mb=True, w=self.width, h=self.height, rtf=True)

        # Edit - Menu
        edit_menu = cmds.menu(label='Edit', p=win)
        cmds.menuItem(label='Reload Items', p=edit_menu, c=self.load_selection_items,
                      ann=u'アイテムデータを再読み込み : {}'.format(self.config.config_file))
        cmds.menuItem(d=True, p=edit_menu)
        self.keep_order_menu = cmds.menuItem(
            label='Keep Order', p=edit_menu, checkBox=True, ann=u'選択順を記憶', c=self.save_settings)

        cmds.menuItem(d=True, p=edit_menu)
        cmds.menuItem(label='Quit', p=edit_menu, c=self.close)

        # Help - Menu
        help_menu = cmds.menu(label='Help', p=win)
        cmds.menuItem(label='Help on {}'.format(self.title), p=help_menu, c=self.help)

        # Main Layout
        main_lay = cmds.formLayout(p=win, nd=100)
        self.selection_list_layout = cmds.formLayout(nd=100, p=main_lay)
        self.selection_list_items = SelectionListItems(parent=self)

        cmds.formLayout(main_lay, e=True,
                        af=[[self.selection_list_layout, 'top', self.margin],
                            [self.selection_list_layout, 'left', self.margin],
                            [self.selection_list_layout, 'right', self.margin],
                            [self.selection_list_layout, 'bottom', self.margin],
                            ],
                        )

        cmds.showWindow(win)

        self.load_settings()
        self.load_selection_items()

    def close(self, *args):
        """ウィンドウを閉じる
        """

        if cmds.window(self._tool_name, q=True, ex=True):
            cmds.deleteUI(self._tool_name)

    def save_selection_items(self, *args):
        """アイテムリストを外部ファイルに保存
        """
        self.config.data['selections'] = self.selection_list_items.get_item_dict()
        self.config.save()

    
    def load_selection_items(self, *args):
        """アイテムリストを外部ファイルから再読み込み
        """
        self.config.load()

        self.selection_list_items.remove_all(save=False)

        data = self.config.data['selections']
        for key in sorted(list(data.keys())):
            self.selection_list_items.add_item(key, data[key]['label'], data[key]['item'], save=False)


    def help(self, *args):
        """ヘルプの表示
        """
        cmds.showHelp(self._help_url, a=True)

    @property
    def keep_order(self):
        return cmds.menuItem(self.keep_order_menu, q=True, cb=True)

    def save_settings(self, *args):
        """設定の保存
        """
        try:
            ui_options = {
                'keep_order': cmds.menuItem(self.keep_order_menu, q=True, cb=True)
            }
            save_optionvar('%s__ui_options' % self._tool_name, ui_options)

        except Exception as e:
            cmds.error(traceback.format_exc())

    def load_settings(self, *args):
        read_values = load_optionvar('%s__ui_options' % self._tool_name)

        if read_values:
            try:
                if 'keep_order' in read_values:
                    cmds.menuItem(self.keep_order_menu, e=True, cb=read_values.get('keep_order', True))

            except Exception as e:
                cmds.error(traceback.format_exc())
