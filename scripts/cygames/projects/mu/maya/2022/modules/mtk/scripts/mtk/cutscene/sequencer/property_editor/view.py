from __future__ import annotations

import types
import typing as tp

from mtk.cutscene.sequencer.lib.qt import MayaMainWindowBase
from mtk.cutscene.sequencer.property_editor.gui import bool_item
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QListWidgetItem, QWidget

from .gui import (file_item, float2_item, float3_item, float4_item, float_item,
                  int_item, main, string_item)


class View(MayaMainWindowBase):
    def __init__(self):
        super().__init__()

    def setup(self, central_widget) -> None:
        self.setObjectName(self.abolute_name)
        self.setWindowTitle("Property Editor")

        self.gui = main.Ui_Form()
        self.gui.setupUi(central_widget)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def save(self):
        ...

    def load(self):
        ...

    def showEvent(self, event):
        self.load()
        super(View, self).showEvent(event)

    def closeEvent(self, event):
        self.save()
        super(View, self).closeEvent(event)

    def add_widget_item(self, type_name, property_name, tooltip) -> QListWidgetItem:
        item_widget = QWidget()

        form = self._get_type_widget_item(type_name)

        form.setupUi(item_widget)
        item_widget.gui = form

        item_widget.gui.propertyLabel.setText(property_name)
        item_widget.gui.propertyLabel.setToolTip(tooltip)

        item = QListWidgetItem()
        item.setSizeHint(item_widget.size())
        self.gui.property_list.addItem(item)
        self.gui.property_list.setItemWidget(item, item_widget)
        return item

    def selected_property_items(self) -> tp.List[QListWidgetItem]:
        """選択中のプロパティウィジェットアイテムを取得する

        Returns:
            tp.List[QListWidgetItem]: プロパティウィジェットアイテム
        """
        items = self.gui.property_list.selectedItems()
        return items

    def selected_property_widgets(self) -> tp.List[string_item.Ui_Item]:
        """選択中のプロパティウィジェットを取得する

        Returns:
            tp.List[string_item.Ui_Item]: プロパティウィジェットリスト
        """
        selected_widgets = []

        items = self.selected_property_items()
        for item in items:
            widget = self.convert_property_widgets(item)
            selected_widgets.append(widget)

        return selected_widgets

    def get_all_items(self) -> tp.List[QListWidgetItem]:
        items = []
        for index in range(self.gui.property_list.count()):
            items.append(self.gui.property_list.item(index))

        return items

    def get_all_item_widgets(self):
        item_widgets = []
        items = self.get_all_items()

        for item in items:
            item_widgets.append(self.convert_property_widgets(item))

        return item_widgets

    def convert_property_widgets(self, item: QListWidgetItem) -> QWidget:
        widget = self.gui.property_list.itemWidget(item)

        return widget

    def _get_type_widget_item(self, name) -> tp.Union[string_item.Ui_Item, float_item.Ui_Item, float2_item.Ui_Item, float3_item.Ui_Item, float4_item.Ui_Item, int_item.Ui_Item, file_item.Ui_Item, bool_item.Ui_Item]:
        """TypeごとのWidgetItemを取得する

        Args:
            name (str)): 型タイプ名

        Returns:
            _type_: _description_
        """
        if name == "string":
            def set_value(self, value: str):
                self.propertyValueLine.setText(value)

            def get_value(self):
                return self.propertyValueLine.text()

            item_class = string_item.Ui_Item()

        elif name == "float":
            def set_value(self, value: float):
                self.propertyValueFloat.setValue(value)

            def get_value(self):
                return self.propertyValueFloat.value()

            item_class = float_item.Ui_Item()

        elif name == "float2":
            def set_value(self, values: tp.List[float]):
                self.propertyValueFloatX.setValue(values[0])
                self.propertyValueFloaty.setValue(values[1])

            def get_value(self):
                return [self.propertyValueFloatX.value(), self.propertyValueFloatY.value()]

            item_class = float2_item.Ui_Item()

        elif name == "float3":
            def set_value(self, values: tp.List[float]):
                self.propertyValueFloatX.setValue(values[0])
                self.propertyValueFloatY.setValue(values[1])
                self.propertyValueFloatZ.setValue(values[2])

            def get_value(self):
                return [self.propertyValueFloatX.value(), self.propertyValueFloatY.value(), self.propertyValueFloatZ.value()]

            item_class = float3_item.Ui_Item()

        elif name == "color":
            def set_value(self, values: tp.List[float]):
                self.propertyValueFloatX.setValue(values[0])
                self.propertyValueFloatY.setValue(values[1])
                self.propertyValueFloatZ.setValue(values[2])
                self.propertyValueFloatW.setValue(values[3])

            def get_value(self):
                return [self.propertyValueFloatX.value(),
                        self.propertyValueFloatY.value(),
                        self.propertyValueFloatZ.value(),
                        self.propertyValueFloatW.value()]

            item_class = float4_item.Ui_Item()

        elif name == "int":
            def set_value(self, value: int):
                self.propertyValueInt.setValue(value)

            def get_value(self):
                return self.propertyValueInt.value()

            item_class = int_item.Ui_Item()

        elif name == "file":
            def set_value(self, value: str):
                self.propertyValuePath.setText(value)

            def get_value(self):
                return self.propertyValuePath.text()

            item_class = file_item.Ui_Item()

        elif name == "bool":
            def set_value(self, value: bool):
                self.propertyValueBool.setChecked(value)

            def get_value(self):
                return self.propertyValueBool.isChecked()

            item_class = bool_item.Ui_Item()

        else:
            raise ValueError(f"Not found item class type. {name}")

        item_class.set_value = types.MethodType(set_value, item_class)
        item_class.get_value = types.MethodType(get_value, item_class)

        return item_class
