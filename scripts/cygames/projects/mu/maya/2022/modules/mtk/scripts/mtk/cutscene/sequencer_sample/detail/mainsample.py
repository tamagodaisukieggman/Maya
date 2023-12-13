# coding=utf-8
"""test Timeline Package - 人間が使うもので、自動ではない！

"""

import typing as tp

import cy.ed.timeline as et
import cy.ed.timeline.guisetting as etconf
# cy
# from cy import codereload, log
from cy import log
# import cy.ed.timeline as et
# import cy.ed.timeline.utility as etutil
# import cy.ed.timeline.guisetting as etconf
# ed.timeline
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from cy import curvemodel, typedef
# from cy.ed import qtex
# from cy.graph import curvemodel
from PySide6 import QtCore, QtGui, QtWidgets

# =============================================
# Utility
# =============================================

_print = log.debug
# _print = print
log = et.log

# =============================================
#
# =============================================


class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MainWindow")
        self.setWindowTitle("ed.timeline Example - How to use ed.timeline")
        self.setCentralWidget(None)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, DockWidget(parent=self))


class DockWidget(QtWidgets.QDockWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.create_inner_widget()

    # def __cy_reload__(self) -> None:
    #     print("hello reload - d")
    #     inner = self.widget()
    #     if inner:
    #         inner.deleteLater()
    #     self.create_inner_widget()

    def create_inner_widget(self) -> None:
        self.setWidget(TabWidget(parent=self))

    # @staticmethod
    # def get_title():
    #     """(override)タイトル名を取得します。"""
    #     return qtex.translate("addon", "Sample Dock")

    # def update_window_title(self, dock_index: int = None, can_dock: bool = None, **captions) -> None:
    #     """(override)ウィンドウタイトルを更新します。
    #
    #     :param dock_index: ドックウィジェットの番号
    #     :param can_dock: ドッキング可能か？
    #     :param captions: キャプション
    #     """
    #     super().update_window_title(dock_index=dock_index, can_dock=can_dock, uianim_name=self._uianim_name, **captions)


class TabWidget(QtWidgets.QTabWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setObjectName("MainWindow__Central")
        bar = self.tabBar()
        bar.setMovable(True)

        if True:
            tab01 = _create_simple_view(parent=self)
            self.addTab(tab01, "Simple Sample")

        # if False:
        if True:
            tab02 = MyEditorView(controller=None, parent=self)
            self.addTab(tab02, "MyEditor - User-defined Types")


# =============================================
# Simple Sample
# =============================================

def _create_simple_model():

    #
    curve1 = curvemodel.Curve({"keys": [{"x": 0.0, "y": 1.0}, {"x": 10.0, "y": 0.1}, {"x": 20, "y": 0.1}]})
    curve2a = curvemodel.Curve({"keys": [{"x": 0.0, "y": 1.0}, {"x": 1.0, "y": 0.1}]})
    curve2b = curvemodel.Curve({"keys": [{"x": 0.0, "y": 1.0}, {"x": 1.0, "y": 0.1}]})

    curve3x = curvemodel.Curve({"keys": [{"x": 50, "y": 1.0}, {"x": 100, "y": 0.1}, {"x": 200, "y": 0.1}]})
    curve3y = curvemodel.Curve({"keys": [{"x": 0.0, "y": 1.0}, {"x": 1.0, "y": 0.1}]})
    curve3z = curvemodel.Curve({"keys": [{"x": 100, "y": 1.0}, {"x": 200, "y": 0.1}]})

    # _print("TestModel - start")
    mdl = et.TimelineItemModel()
    mdl.append_track_row(et.ValueTrackData("1a - Non-group Property ", curve1))

    # Audio Track and Clips
    group3 = mdl.append_track_row(et.GroupTrackData("1b - Group of Clip-based Tracks"))
    au_track = et.AudioTrackData("Audio")
    mdl.append_track_row(au_track, group3)
    au_track.insert_clip(et.AudioClipData(10, 11))
    au_track.insert_clip(et.AudioClipData(30, 31))
    au_track.insert_clip(et.AudioClipData(100, 101))
    # au_track.insert_clip(et.AudioClipData(600, 900))

    # if False:
    if True:
        group2 = mdl.append_track_row(et.GroupTrackData("2 - Group of Curve-based Tracks"))
        mdl.append_track_row(et.ValueTrackData("Property 2a", curve2a), group2)
        mdl.append_track_row(et.ValueTrackData("Property 2b", curve2b), group2)
        mdl.append_track_row(et.ValueTrackData("Property 2c", curve2b), group2)
        group2c = mdl.append_track_row(et.GroupTrackData("3 - Group of Compound Properties"))
        mdl.append_track_row(et.Float3GroupTrackData("3a - Float3 Group", (curve3x, curve3y, curve3z)), group2c)
        mdl.append_track_row(et.Float4GroupTrackData("3b - Float4 Group", (curve3x, curve3y, curve3z, curve3z)), group2c)
        mdl.append_track_row(et.Float3GroupTrackData("3c - Float3 Group", (curve3x, curve3y, curve3z)), group2c)

    # test...
    group4 = mdl.append_track_row(et.GroupTrackData("4 - Group of Clip-based Tracks"))
    mdl.append_track_row(et.Float3GroupTrackData("4a - Float3 Group", (curve3x, curve3y, curve3z)), group4)
    mdl.append_track_row(et.Float4GroupTrackData("4b - Float4 Group", (curve3x, curve3y, curve3z, curve3z)), group4)
    group5 = mdl.append_track_row(et.GroupTrackData("5 - Group of Clip-based Tracks"))
    mdl.append_track_row(et.Float3GroupTrackData("5a - Float3 Group", (curve3x, curve3y, curve3z)), group5)

    # Curve Track
    # curve4 = curvemodel.Curve({"keys": [{"x": 0.0, "y": 1.0}, {"x": 1.0, "y": 0.1}]})
    # group3 = mdl.append_track_row(et.GroupTrackData("4 - Curve-based Group"))
    # mdl.append_track_row(et.AbstractCurveBasedTrackData("Curve", curve4), group3)
    return mdl


def _create_simple_view(controller=None, parent=None):
    # view = et.TimelineView(controller, parent)
    view = et.TimelineView(None, parent)
    mdl = _create_simple_model()
    view.set_model(mdl)
    return view


# =============================================
# MyEditor - User-defined Types
# =============================================

class MyScenePreviewData(et.AbstractClipBasedTrackData):

    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    def track_type(cls) -> et.TrackType:
        """TrackType"""
        return et.TrackType.UserType

    @classmethod
    def gui_height_scale(cls) -> float:
        """GUI 上の見た目の高さのScale"""
        return 3.0

    @classmethod
    def gui_track_color(cls) -> tp.Optional[typedef.Color]:
        """GUI 上の背景カラー"""
        return None


class MyCharaAnimData(et.AbstractClipBasedTrackData):

    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    def track_type(cls) -> et.TrackType:
        """(override) TrackType"""
        return et.TrackType.UserType + 1

    @classmethod
    def gui_height_scale(cls) -> float:
        """(override) GUI 上の見た目の高さのScale"""
        return 1.5

    @classmethod
    def gui_track_color(cls) -> tp.Optional[typedef.Color]:
        """(override) GUI 上の背景カラー"""
        return None


class MyCharaAnimClipData(et.BaseClipData):

    def __init__(self, start: et.Time, end: et.Time, **kwargs):
        super().__init__(start, end)
        # self.clips


class MyEditorView(QtWidgets.QWidget):
    """ My Editor View

    """

    def __init__(self, controller=None, parent=None):
        """

        :param controller:
        :param parent:
        """
        super().__init__(parent)

        class _TempViewObserver:

            def __init__(self, timeline_view: et.TimelineView, **kwargs) -> None:
                super().__init__(**kwargs)
                timeline_view.clip_property_changed.connect(self.on_clip_property_changed)
                timeline_view.treeview_clicked.connect(self.on_treeview_clicked)
                log.info("Sample MyEditorView._TempViewObserver.init")

            # def on_clip_property_changed(self, clip_idx: int, data: et.BaseClipData, dict_: et.ClipProperty2VariantStreamValueDict):
            def on_clip_property_changed(self, clip_idx: int, data: et.BaseClipData, dict_: tp.Dict):
                log.info(f"_TempViewObserver SLOT:on_clip_property_changed {clip_idx} {data}, {dict_}")

            def on_treeview_clicked(self, idx: QtCore.QModelIndex, data: et.AbstractBaseTrackData):
                if idx.column() == etconf.ModelColumnIndex.VISIBILITY:
                    log.info(f"_TempViewObserver SLOT:on_treeview_clicked row={idx.row()}  data={data.display_name()}")

        class MyPaintFunctor(et.AClipItemPaintFunctor):

            def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem,
                      index: QtCore.QModelIndex, clip: et.BaseClipData, delegate: QtWidgets.QStyledItemDelegate) -> None:
                model = index.model()
                item = self.item(index)
                style = option.styleObject.style()

                version = 2
                if version == 1:
                    # for local TEST ONLY
                    delegate.paint(painter, option, index)
                else:
                    # custom  paint
                    font_metrics = painter.fontMetrics()
                    alignment = option.displayAlignment
                    enabled = True

                    # v0.0
                    text = str(model.data(index, QtCore.Qt.DisplayRole))
                    # v0.1 - draw text
                    text = f"<<**** Custom paint by My Sample: (user type id:{str(item.track_type())})  {clip.start_time()}:{clip.end_time()}  ****>>"
                    text_rect: QtCore.QRect = style.itemTextRect(font_metrics, option.rect, alignment, enabled, text)

                    # v2 - use painter
                    painter.save()
                    painter.setBrush(QtCore.Qt.NoBrush)
                    painter.setPen(QtCore.Qt.darkGreen)
                    painter.drawRect(text_rect)
                    pen = QtCore.Qt.darkGreen if not option.state & QtWidgets.QStyle.State_Selected else QtCore.Qt.green
                    painter.setPen(pen)
                    painter.drawStaticText(text_rect.left(), text_rect.top(), QtGui.QStaticText(text))
                    painter.restore()

        class _MyModel(et.TimelineItemModel):

            def flags(self, index):
                """(override)"""

                # disable DnD
                # defaultFlags = super().flags(index)
                if not index.isValid():
                    return QtCore.Qt.NoItemFlags

                if index.column() == etconf.ModelColumnIndex.MODEL_ITEM:
                    return QtCore.Qt.ItemIsSelectable \
                        | QtCore.Qt.ItemIsEnabled

                return QtCore.Qt.NoItemFlags

        def _create_my_mdl():
            curve3x = curvemodel.Curve({"keys": [{"x": 50, "y": 1.0}, {"x": 100, "y": 0.1}, {"x": 200, "y": 0.1}]})
            # curve3y = curvemodel.Curve({"keys": [{"x": 0.0, "y": 1.0}, {"x": 1.0, "y": 0.1}]})
            # curve3z = curvemodel.Curve({"keys": [{"x": 100, "y": 1.0}, {"x": 200, "y": 0.1}]})

            _print("TestModel - start")
            mdl = _MyModel()

            mdl.append_track_row(MyScenePreviewData("1 - MyCamera Track"))

            group2 = mdl.append_track_row(et.GroupTrackData("2 - My Chara 1"))
            mdl.append_track_row(MyCharaAnimData("MyCharaAnim Track 0"), group2)
            mdl.append_track_row(MyCharaAnimData("MyCharaAnim Track 1"), group2)
            mdl.append_track_row(MyCharaAnimData("MyCharaAnim Track 2"), group2)

            group3 = mdl.append_track_row(et.GroupTrackData("3 - My Chara 2"))
            track_c2 = MyCharaAnimData("MyCharaAnim Track 1")
            mdl.append_track_row(track_c2, group3)
            track_c2.insert_clip(MyCharaAnimClipData(10, 25))
            track_c2.insert_clip(MyCharaAnimClipData(40, 45))

            group4 = mdl.append_track_row(et.GroupTrackData("4 - My Chara 3"))
            mdl.append_track_row(et.Float3GroupTrackData(" - Float3 Group", (curve3x, curve3x, curve3x)), group4)

            group4 = mdl.append_track_row(et.GroupTrackData("5 - My Chara 4"))
            mdl.append_track_row(et.Float3GroupTrackData(" - Float3 Group", (curve3x, curve3x, curve3x)), group4)

            # low-level access to QStandardItemModel..moveRows
            # res = mdl.moveRows(group2.index(), 0, 1, group2.index(), 2)
            # _print(f"result={res}")
            return mdl

        # create model
        mdl = _create_my_mdl()

        # prepare view with custom paint
        view = et.TimelineView(controller, parent)
        func_factory = view.paint_func_object_factory()
        func_factory.register_object(MyCharaAnimData.track_type(), MyPaintFunctor)

        # set model
        view.set_model(mdl)
        # v0
        # observer = _TempViewObserver(view.view_observee())        # TEMP.
        # v1
        self._observer = _TempViewObserver(view)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(view)
        self.setLayout(layout)
