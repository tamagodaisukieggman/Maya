# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from maya import cmds, mel
from maya import OpenMayaUI as omui
import maya.api.OpenMaya as om2

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtMultimedia import *
    from PySide2.QtMultimediaWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin

import base64
import codecs
import enum
import fnmatch
import glob
import json
import math
import os
import pickle
import re
import subprocess
import sys
import time
import traceback

from collections import OrderedDict
from functools import partial
from imp import reload
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from timeit import default_timer as timer

try:
    DIR_PATH = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
except:
    DIR_PATH = ''

#############################
# GraphicsScene class
#############################
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)

        # settings
        self.gridSize = 10

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)

        self.setBackgroundBrush(self._color_background)

    def drawBackground(self, painter, rect):
        super(GraphicsScene, self).drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        lines_light = []
        for x in range(first_left, right, self.gridSize):
            lines_light.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            lines_light.append(QLine(left, y, right, y))

        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)

    def dropEvent(self, event):
        item = self.itemAt(event.scenePos())
        if item.setAcceptDrops == True:
            try:
               item.dropEvent(event)
            except RuntimeError:
                pass

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

#############################
# GraphicsRectItem class
#############################
class ShapeType(enum.Enum):
    Rectangle = 1
    Circle = 2
    Triangle = 3
    Diamond = 4
    Cross = 5

class GraphicsRectItem(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(GraphicsRectItem, self).__init__(*args, **kwargs)

        self.shapeType = ShapeType.Rectangle

        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

        self.block_size = -1
        self.init_rect = None
        self.rect_edit_mode = None
        self.rect_move = None
        self.selected_items = None
        self.show_hide_key = None

        # self.text_item = QGraphicsTextItem(self.name)
        # self.text_item.setDefaultTextColor(QColor(0, 0, 0))
        # self.text_item.setParentItem(self)
        # self.text_pos = self.pos()
        # self.text_item.setPos(self.text_pos.x(), self.text_pos.y())

        self._last_mouse_position = QPoint()

    def setShape(self, shapeType):
        self.shapeType = shapeType
        self.update()  # 更新して再描画

    def paint(self, painter, option, widget):
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        
        if self.shapeType == ShapeType.Rectangle:
            painter.drawRect(self.rect())
        elif self.shapeType == ShapeType.Circle:
            painter.drawEllipse(self.rect())
        elif self.shapeType == ShapeType.Triangle:
            polygon = QPolygonF([QPointF(self.rect().x() + self.rect().width() / 2, self.rect().y()),
                                 QPointF(self.rect().x() + self.rect().width(), self.rect().y() + self.rect().height()),
                                 QPointF(self.rect().x(), self.rect().y() + self.rect().height())])
            painter.drawPolygon(polygon)
        elif self.shapeType == ShapeType.Diamond:
            polygon = QPolygonF([QPointF(self.rect().x() + self.rect().width() / 2, self.rect().y()),
                                 QPointF(self.rect().x() + self.rect().width(), self.rect().y() + self.rect().height() / 2),
                                 QPointF(self.rect().x() + self.rect().width() / 2, self.rect().y() + self.rect().height()),
                                 QPointF(self.rect().x(), self.rect().y() + self.rect().height() / 2)])
            painter.drawPolygon(polygon)
        elif self.shapeType == ShapeType.Cross:
            path = QPainterPath()
            path.moveTo(self.rect().x() + self.rect().width() / 2, self.rect().y())
            path.lineTo(self.rect().x() + self.rect().width() / 2, self.rect().y() + self.rect().height())
            path.moveTo(self.rect().x(), self.rect().y() + self.rect().height() / 2)
            path.lineTo(self.rect().x() + self.rect().width(), self.rect().y() + self.rect().height() / 2)
            painter.drawPath(path)

    def mouseMoveEvent(self, event):
        if self.rect_move:
            pos = event.pos()
            local_rect = self.mapToScene(pos.x(), pos.y())

            cur_x = local_rect.x() - self.init_rect.x()
            cur_y = local_rect.y() - self.init_rect.y()

            snap_pos = QPointF(cur_x, cur_y)

            new_pos_x = round(snap_pos.x(), self.block_size)
            new_pos_y = round(snap_pos.y(), self.block_size)

            cur_pos = QPointF(new_pos_x, new_pos_y)
            self.setPos(cur_pos)

            self.update()

            # delta = self.mapToScene(event.pos() - self._last_mouse_position)
            # for item in self.selected_items:
            #     if isinstance(item, GraphicsRectItem):
            #         item.setPos(self.startPositions[item] + delta)

            #         item._last_mouse_position = self.mapToScene(event.pos())

        super(GraphicsRectItem, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.init_rect = event.pos()
        if event.button() == Qt.LeftButton:
            self.selected_items = self.scene().selectedItems()
            # self.scene().clearSelection()
            # self.setSelected(True)
            # self.startPositions = {item: item.mapToScene(item.pos()) for item in self.selected_items}

            # self._last_mouse_position = event.pos()

        elif event.button() == Qt.RightButton:
            self.selected_items = self.scene().selectedItems()

        # スーパークラスのcontextMenuEventを呼び出さなければ選択は外れない
        # super(GraphicsRectItem, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selected_items = self.scene().selectedItems()

        super(GraphicsRectItem, self).mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        context_menu = QMenu()
        size_action = context_menu.addAction('Set Size')
        move_unlock_action = context_menu.addAction('Move Unlock')
        move_lock_action = context_menu.addAction('Move Lock')
        show_hide_text_action = context_menu.addAction('Text Visibility')
        set_text_size_action = context_menu.addAction('Set Text Size')

        selected_action = context_menu.exec_(event.screenPos())

        if selected_action == move_unlock_action:
            for item in self.selected_items:
                if isinstance(item, GraphicsRectItem):
                    item.rect_move = True
        elif selected_action == move_lock_action:
            for item in self.selected_items:
                if isinstance(item, GraphicsRectItem):
                    item.rect_move = False
        elif selected_action == size_action:
            self.change_size()
        elif selected_action == show_hide_text_action:
            self.show_hide_text()
        elif selected_action == set_text_size_action:
            self.change_text_size()

    def change_size(self):
        new_size, ok = QInputDialog.getInt(None, "Set Size", "Size:", int(self.rect().width()), 10, 1000)
        if ok:
            for item in self.selected_items:
                if isinstance(item, GraphicsRectItem):
                    item.setRect(item.rect().x(), item.rect().y(), new_size, new_size)
                    item.update()

    def change_text_size(self):
        new_size, ok = QInputDialog.getInt(None, "Set Text Size", "Size:", int(self.rect().width()), 0, 20)
        if ok:
            for item in self.selected_items:
                if isinstance(item.text_item, QGraphicsTextItem):
                    font = QFont('Arial', new_size)
                    item.text_item.setFont(font)

    def show_hide_text(self):
        for item in self.selected_items:
            if isinstance(item.text_item, QGraphicsTextItem):
                if item.text_item.isVisible():
                    item.text_item.setVisible(False)
                else:
                    item.text_item.setVisible(True)

    def add_text(self, name=None, size=None, offset_pos=[0,0]):
        self.text_item = QGraphicsTextItem(name, self)
        self.text_pos = QPoint(self.rect().x()+offset_pos[0],
                               self.rect().y()+offset_pos[1])
        self.text_item.setPos(self.text_pos)
        font = QFont('Arial', size)
        self.text_item.setFont(font)
        self.text_item.setVisible(False)

#############################
# GraphicsView class
#############################
class GraphicsView(QGraphicsView):
    def __init__(self, picker_items=None):
        super().__init__()

        self.picker_items = picker_items

        # self.picker_items = {
        #     # Hand Left
        #     'thumb_L_000':{
        #             'item_name':'Thumb_01_L_ctrl',
        #             'rect':[-100, -100, 15, 15],
        #             'color':[255, 128, 255],
        #             'edge_color':[0, 0, 0],
        #             'width':1,
        #             'text_size':2,
        #             'text_offset_pos':[-5, -10]
        #     },
        #     'thumb_L_001':{
        #             'item_name':'Thumb_02_L_ctrl',
        #             'rect':[-120, -100, 15, 15],
        #             'color':[255, 128, 255],
        #             'edge_color':[0, 0, 0],
        #             'width':1,
        #             'text_size':2,
        #             'text_offset_pos':[-5, -10]
        #     },
        # }


        self.center = None
        self.zoom = 0
        self.selection_stock = list()

        self.names = list()
        self.item_names = list()

        self.seleced_item_indexes = list()
        self.selected_item_names = list()
        self.selected_scene_items = OrderedDict()

        # GraphicsView settings
        self.setAcceptDrops(True)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        # self.setDragMode(QGraphicsView.RubberBandDrag) # 範囲選択

        # scene settings
        self.scene_size = None
        self.scene = GraphicsScene()
        # self.scene.setSceneRect(-500, -500, 1000, 1000)
        self.setScene(self.scene)
        self.scene.selectionChanged.connect(self.selection_changed)

        self.enable_wheelEvent = True

        # mouse event
        self._is_panning = False
        self._last_mouse_position = QPoint()

        [self.add_pick_item(name=name, **item_values) for name, item_values in self.picker_items.items()]

    ######################
    # add picker items
    ######################
    def add_pick_item(self,
                      name='rectTest',
                      item_name=None,
                      shape=1,
                      rect=[-100, -100, 80, 100],
                      color=[128, 220, 190],
                      edge_color=[196, 255, 220],
                      width=4,
                      text_size=10,
                      text_offset_pos=[-10, 30]):
        self.rect_pos = QRect(*rect)
        rect_item = GraphicsRectItem(self.rect_pos)

        shape_dict = {
            1:ShapeType.Rectangle,
            2:ShapeType.Circle,
            3:ShapeType.Triangle,
            4:ShapeType.Diamond,
            5:ShapeType.Cross,
        }

        rect_item.setShape(shape_dict[shape])
        rect_item.add_text(name, text_size, text_offset_pos)
        self.scene.addItem(rect_item)

        # self.text_pos = QPoint(self.rect_pos.x(), self.rect_pos.y())
        # _text = self.scene.addText(name)
        # _text.setPos(self.text_pos)
        # _text.setParentItem(rect_item)

        gradient = QLinearGradient(20, 180, 120, 260)
        gradient.setColorAt(0.0, QColor(*color))
        rect_item.setBrush(gradient)

        pen = QPen(QColor(*edge_color))
        pen.setWidth(width)
        rect_item.setPen(pen)

        rect_item.setFlags(QGraphicsItem.ItemIsSelectable)
        # rect_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        rect_item.setData(0,
            {
                'name':name,
                'item_name':item_name
            }
        )

        # set and add tool tip
        self.set_tool_tip_item(
            rect_item,
            name,
            item_name,
            rect,
            color,
            edge_color,
            width
        )

        self.add_tool_tip_item(
            None,
            name,
            item_name,
            rect,
            color,
            edge_color,
            width
        )

        # set dict
        self.picker_items[name] = {
            'item_name':item_name,
            'rect':rect,
            'color':color,
            'edge_color':edge_color,
            'width':width
        }

        return rect_item

    def add_drop_items(self, event):
        selected_objects = cmds.ls(os=True)
        for obj in selected_objects:
            nss = ':'.join(obj.split(':')[0:-1]) + ':'
            obj = obj.replace(nss, '')
            self.add_pick_item(
                name=obj,
                item_name=obj,
                rect=[
                    self.mapToScene(event.pos()).x()+25,
                    self.mapToScene(event.pos()).y()-25,
                    50,
                    50],
                color=[128, 220, 190],
                edge_color=[196, 255, 220],
                width=4)

    ##################
    # tool tips
    ##################
    def add_tool_tip_item(self, item=None, name='rectTest', item_name=None, rect=[-100, -100, 80, 100], color=[128, 220, 190], edge_color=[196, 255, 220], width=4):
        keys_ = ['Name', 'ItemName', 'Geometory', 'Color', 'EdgeColor', 'width']
        values_ = [name, item_name, rect, color, edge_color, width]
        tool_tip = ['<p>{}'.format(key_) + ':' + '<b>{}</b></p>'.format(val_) for key_, val_ in zip(keys_, values_)]
        if item:
            item.setToolTip('\n'.join(tool_tip))

    def set_tool_tip_item(self, rect_item, name, item_name, rect, color, edge_color, width):
        # tool tipを更新するために個別化
        keys_ = ['Name', 'ItemName', 'Geometory', 'Color', 'EdgeColor', 'width']
        values_ = [name, item_name, rect, color, edge_color, width]
        tool_tip = ['<p>{}'.format(key_) + ':' + '<b>{}</b></p>'.format(val_) for key_, val_ in zip(keys_, values_)]
        rect_item.setToolTip('\n'.join(tool_tip))
        return tool_tip

    #################
    # events
    #################
    def _fitInView(self):
        r = self.scene.sceneRect()
        self.fitInView(r, Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        self.scene_size = self.size()
        self._fitInView()
        super(GraphicsView, self).resizeEvent(event)

    def updateCenter(self):
        center = self.geometry().center()
        self.center = self.mapToScene(center)

    def updateCoordinatesDisplay(self, position):
        # 座標を表示するテキストアイテムを作成または更新します
        # position は QPointF または QPoint オブジェクトです
        text = f"X: {position.x()}, Y: {position.y()}"
        if not hasattr(self, '_coordinates_item'):
            self._coordinates_item = QGraphicsTextItem(text)
            self._coordinates_item.setDefaultTextColor(Qt.gray)
            self.scene().addItem(self._coordinates_item)
        else:
            self._coordinates_item.setPlainText(text)
        self._coordinates_item.setPos(position)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.viewport().setCursor(Qt.ArrowCursor)
            self.setDragMode(QGraphicsView.RubberBandDrag)

        elif event.button() == Qt.MidButton:
            self._is_panning = True
            self._last_mouse_position = self.mapToScene(event.pos())

            self.viewport().setCursor(Qt.ClosedHandCursor)

            # self.setDragMode(QGraphicsView.ScrollHandDrag)
            # self.viewport().setCursor(Qt.ClosedHandCursor)
            # handmade_event = QMouseEvent(QEvent.MouseButtonPress,QPointF(event.pos()),Qt.LeftButton,event.buttons(),Qt.KeyboardModifiers())
            # self.mousePressEvent(handmade_event)

        super(GraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.viewport().setCursor(Qt.ArrowCursor)

        elif event.button() == Qt.MidButton:
            self._is_panning = False

            # self.setDragMode(QGraphicsView.NoDrag)
            # self.viewport().setCursor(Qt.OpenHandCursor)
            # handmade_event = QMouseEvent(QEvent.MouseButtonRelease,QPointF(event.pos()),Qt.LeftButton,event.buttons(),Qt.KeyboardModifiers())
            # self.mouseReleaseEvent(handmade_event)

        self.viewport().setCursor(Qt.ArrowCursor)
        self.setDragMode(QGraphicsView.NoDrag)

        super(GraphicsView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_panning:
            delta = self.mapToScene(event.pos()) - self._last_mouse_position
            self._last_mouse_position = self.mapToScene(event.pos())
            self.translate(delta.x(), delta.y())
        super(GraphicsView, self).mouseMoveEvent(event)

    def wheelEvent(self, event):
        if self.enable_wheelEvent:
            if event.angleDelta().y() > 0:
                factor = 1.25
                self.zoom += 1
            else:
                factor = 0.8
                self.zoom -= 1

            if self.zoom < 5:
                self.zoom = 5
            elif self.zoom > -5:
                self.zoom = -5

            if self.zoom > 0 or self.zoom < 0:
                self.scale(factor, factor)
            elif self.zoom == 0:
                self._fitInView()

            super(GraphicsView, self).wheelEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setAccepted(True)
            self.dragOver = True
            self.update()

        super(GraphicsView, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        # print('move event', event)
        super(GraphicsView, self).dragMoveEvent(event)

    def dropEvent(self, event):
        data = event.mimeData().text()
        if data: self.add_drop_items(event)
        event.accept()

    def selection_changed(self):
        self.names = list()
        self.item_names = list()
        self._current_selection = self.scene.selectedItems()
        if not self._current_selection:
            cmds.select(cl=True)
            self.names = list()
            self.item_names = list()

        for sel in self._current_selection:
            name = sel.data(0)['name']
            if not name in self.names:
                self.names.append(name)

            item_name = sel.data(0)['item_name']
            if not item_name in self.item_names:
                self.item_names.append(item_name)

        # view select
        add_nss_list = [n for n in self.item_names if cmds.objExists(n)]
        if add_nss_list: cmds.select(add_nss_list, r=True)

        panel = cmds.getPanel(withFocus=True)
        cmds.setFocus('MayaWindow')

    def get_located_items(self):
        items = self.scene.items()
        for item in items:
            if 'GraphicsRectItem' == item.__class__.__name__:
                name = item.data(0)['name']
                self.selected_scene_items[name] = item

def save_optionVar(save_items=None):
    for key, value in save_items.items():
        cmds.optionVar(sv=[key, str(value)])

def load_optionVar(key=None):
    return eval(cmds.optionVar(q=key)) if cmds.optionVar(ex=key) else False

def json_transfer(fileName=None, operation=None, export_values=None, export_type=None, import_type=None):
    if operation == 'export':
        if not export_type:
            with open(fileName, "w") as f:
                json.dump(export_values, f)

        if export_type == 'utf-8':
            with codecs.open(fileName, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

        elif export_type == 'pickle':
            s = base64.b64encode(pickle.dumps(export_values)).decode("utf-8")
            d = {"pickle": s}
            with open(fileName, "w") as f:
                json.dump(d, f)

    elif operation == 'import':
        if not import_type:
            with open(fileName) as f:
                return json.load(f)

        elif import_type == 'utf-8':
            with codecs.open(fileName, 'r', encoding='utf-8') as f:
                return json.load(f, 'utf-8', object_pairs_hook=OrderedDict)

        elif import_type == 'pickle':
            with open(fileName) as f:
                d = json.load(f)
            s = d["pickle"]
            return pickle.loads(base64.b64decode(s.encode()))


