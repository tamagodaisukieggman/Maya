from __future__ import annotations

import functools
import typing as tp

import cy.ed.timeline as et
from cy.asset.cutscene.common import base_eventdefinition
from shr.cutscene.sequencer.api import (AbstractBaseTrackData,
                                        SequencerClipData,
                                        SequencerGroupTrackData, TrackType)
from shr.cutscene.sequencer.lib.qt import MayaAppBase
from PySide2 import QtCore
from PySide2.QtWidgets import (QApplication, QFormLayout, QLineEdit,
                               QListWidgetItem)

from .view import View


class PropertyEditor(MayaAppBase):
    def __init__(self, controller: et.AbstractDataController, track_data: AbstractBaseTrackData):
        super().__init__()
        self._controller = controller
        self.layout = QFormLayout()

        self.track_data = track_data
        self.properties = track_data.get_property()
        self.invisible_property = []

    def initialize(self, app: QApplication) -> None:
        return super().initialize(app)

    def create_window(self) -> View:
        return View()

    def post_initialize(self) -> None:
        # self._window.gui.okButton.clicked.connect(self.on_pushed_save_button)
        self._window.gui.okButton.clicked.connect(lambda: self.on_pushed_save_button())
        actor_name = self.track_data.display_name()
        self._window.setWindowTitle(f"Property Editor ({actor_name})")

        if isinstance(self.track_data, SequencerGroupTrackData):
            track_type = self.track_data.get_event_type()

            event_widget_item_list = self.create_item(track_type)

            for event_widget_item in event_widget_item_list:
                widget = self._window.convert_property_widgets(event_widget_item)
                property_name = widget.gui.propertyLabel.text()
                if property_name in self.properties:
                    value = self.properties[property_name]
                    widget.gui.set_value(value)

    def create_item(self, event_definition_name) -> tp.List[QListWidgetItem]:
        self._window: View
        property_item_list = []
        definition = base_eventdefinition.get_event_definition(event_definition_name)

        property_list = definition.get_property_definitions()
        for event_property in property_list:
            if event_property["visible"] is True:
                property_item_list.append(self._window.add_widget_item(event_property["type"],
                                                                       event_property["name"],
                                                                       event_property["tooltip"]))
            else:
                self.invisible_property.append(event_property)

        return property_item_list

    def reset(self):
        self._window.gui.property_list.clear()

    def on_pushed_save_button(self):
        widgets = self._window.get_all_item_widgets()

        property_data = {}

        for widget in widgets:
            value = widget.gui.get_value()
            label = widget.gui.propertyLabel.text()
            property_data[label] = value

        exists_property = self.track_data.get_property()
        for event_property in self.invisible_property:
            if event_property["name"] in event_property:
                property_data[event_property["name"]] = exists_property[event_property["name"]]
            else:
                property_data[event_property["name"]] = event_property["default"]

        self.track_data.set_property(property_data)

        self._window.close()
