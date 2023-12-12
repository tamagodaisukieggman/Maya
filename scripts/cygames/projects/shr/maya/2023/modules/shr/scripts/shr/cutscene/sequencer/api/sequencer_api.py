# coding=utf-8
"""
Mayaに依存しないシーケンサー用のAPI
"""

import functools
import json
import os
import typing
from enum import IntEnum, auto

import cy.ed.timeline as et
from cy import util as cyutil
from cy.asset.cutscene.common import base_eventdefinition
from cy.ed import propertygui, qtex
from cy.ed.timeline.guiextension.modelhelper import *
from PySide6 import QtCore, QtWidgets


@enum.unique
class TrackType(IntEnum):
    Camera = et.TrackType.USER_TYPE
    Motion = enum.auto()
    Event = enum.auto()


class ClipStatus(IntEnum):
    Nothing = 0
    Check = auto()
    Disable = auto()
    Edit = auto()


class ApplicationType(enum.Flag):
    """Maya用の機能か、Cyllista側の機能かの識別フラグ"""
    Maya = enum.auto()
    Cyllista = enum.auto()
    Any = Maya | Cyllista


SequencerClipData = typing.Union["CameraClipData", "MotionClipData"]


def create_clip_property_dict(top_key: str) -> tp.Dict[str, tp.Any]:
    """プロパティ定義ファイルを元にデフォルトデータを含める辞書を作成する。"""
    result = {}
    event_def = base_eventdefinition.get_event_definition(top_key)
    properties = event_def.get_property_definitions()
    for property in properties:
        # print(property)
        name = property['name']
        type = property['type']
        if 'default' in property:
            default_value = property['default']
        else:
            default_value = event_def.get_default_value(type)
        result[name] = default_value

    return result


# ===========================================================================
# Clipに表示するアイコン用クラス
# ===========================================================================


class SequencerIcons(object):

    check = None
    disable = None
    edit = None
    icon_dict = {}

    @classmethod
    def init_icons(cls):
        # TODO アイコン取得忘れ防止のため、pixmapがちゃんと読み取れたかチェックいれたほうがいいか・・・？
        SequencerIcons.check = qtex.create_pixmap("editor/sequencer/check_icon.png")
        SequencerIcons.disable = qtex.create_pixmap("editor/sequencer/disable_icon.png")
        SequencerIcons.edit = qtex.create_pixmap("editor/sequencer/edit_icon.png")
        SequencerIcons.icon_dict = {
            ClipStatus.Nothing: None,
            ClipStatus.Check: SequencerIcons.check,
            ClipStatus.Disable: SequencerIcons.disable,
            ClipStatus.Edit: SequencerIcons.edit,
        }

    @classmethod
    def get_icon_from_status(cls, status: ClipStatus):
        return SequencerIcons.icon_dict[status]


# ===========================================================================
# クリップ用データ
# ===========================================================================


class ClipParameters(object):
    """
    クリップの start, end, in, out, offset などのパラメーターをまとめただけクラス。
    クリップ作成時などに引数に渡して使うことを想定。クリップのセーブの際にもこのデータをセーブすれば良い。
    実際の Clip データはこのクラスの情報とは全く別に内部にデータを保持している。
    初期化時にデータをセットするだけで、後からデータを編集することは想定されていない。
    関数の引数等に渡されてデータを読むだけの想定。
    """

    def __init__(self, start, end, offset, in_time=0, out_time=-1):
        self._start = start
        self._end = end
        self._offset = offset
        self._in_time = in_time
        if out_time != -1:
            self._out_time = out_time
        else:
            self._out_time = self._end

    def get_dict_data(self):
        temp_dict = {}
        temp_dict["start"] = self._start
        temp_dict["end"] = self._end
        temp_dict["offset"] = self._offset
        temp_dict["in"] = self._in_time
        temp_dict["out"] = self._out_time
        return temp_dict

    def __str__(self):
        return f"start={self._start}, end={self._end}, offset={self._offset}, in={self._in_time}, out={self._out_time}"

    def __getitem__(self, index):
        # add_sequencer_clip() でフレームを指定したタプルと同等に使えるようにインターフェースを整える用
        temp_list = [self._start, self._end, self._offset, self._in_time, self._out_time]
        if 0 <= index < 5:
            return temp_list[index]
        else:
            log.error("Index must be 0 - 4.")
            return None

    def __len__(self):
        # 5つのパラメーターが必ず存在する
        return 5


class SequencerClipDataInterfaceMixIn(object):
    """シーケンサー用のClipが共通にもつインターフェースをまとめたクラス。ClipDataに多重継承させて使う。"""

    def __init__(self):
        self._status: ClipStatus = ClipStatus.Nothing
        self._signals = SequencerSignals.get_instance()
        self._property = None
        self._updated = None

    def get_parent_track(self) -> tp.Optional["SequencerGroupTrackData"]:
        """
        このクリップが格納されているトラックが属するグループトラックを取得。
        グループに含まれない場合は None が返る。
        """
        # TODO Core側にいれるか？
        track: SequencerTrack = self.track_data()
        parent_track = track.get_parent_group_track_data()
        return parent_track

    def get_clip_property(self):
        """このクリップに格納されているプロパティを取得。"""
        return self._property

    def get_row_index(self) -> int:
        """このクリップが格納されているトラックのデータモデル内での Row Index を取得。"""
        # TODO Core側にいれるか？
        track: SequencerTrack = self.track_data()
        item = track.get_track_item()
        index = item.index().row()
        return index

    def get_status(self) -> ClipStatus:
        return self._status

    def set_clip_property(self, _property):
        """ クリップにプロパティを格納。データ形式は何でもよい。"""
        self._property = _property

    def set_status(self, status: ClipStatus, rebuild: bool = True):
        """ステータスをセット、そしてついでにアイコンもセット"""
        self._status = status
        icon = SequencerIcons.get_icon_from_status(status)
        self.set_icon(icon)

        if rebuild:
            # Rectを描画するためにシグナル送信
            self._signals.clip_status_changed.emit(self)

    def get_updated(self):
        return self._updated

    def set_updated(self, value):
        self._updated = value


class CameraClipData(et.BaseClipData, SequencerClipDataInterfaceMixIn):
    """
    カメラクリップデータ。
    タイムは全てフレームで指定する。
    """

    def __init__(self, start: et.Time, end: et.Time, label: str, **kwargs):
        super().__init__(start, end, label, **kwargs)

    def get_clip_parameters(self) -> tp.Tuple:
        # in, out の無いクリップなので、start_time, end_time のパラメーターしか存在しない。
        return ClipParameters(self._start_time, self._end_time, 0, 0, 0)


class MotionClipData(et.BaseClipDataWithInOut, SequencerClipDataInterfaceMixIn):
    """
    モーションクリップデータ。
    タイムは全てフレームで指定する。
    """

    def __init__(self, start: et.Time, end: et.Time, clip_start: et.Time, label: str, **kwargs):
        super().__init__(start, end, clip_start, label, **kwargs)

    def get_clip_parameters(self) -> tp.Tuple:
        """
        クリップの内部のフレームのデータを返します。
        clip.start_time, clip.end_time, clip.in_time, clip.out_time などのプロパティはシーケンサーが評価する際に使われる値が取得できるのであって、
        クリップが内部に保持しているフレームと一致しない。その為上記のデータをそのままセーブすると正しくデータが再現できない。
        そこで、この関数で内部のフレームデータをそのまま取得できます。
        返された ClipParameters オブジェクトは add_sequencer_clip() の引数にそのまま渡せます。

        """
        # return self._start_time, self._end_time, self._clip_offset, self._in_time_offset, self._out_time_offset
        return ClipParameters(self._start_time, self._end_time, self._clip_offset, self._in_time_offset, self._out_time_offset)


class EventClipData(et.BaseClipData, SequencerClipDataInterfaceMixIn):
    """
    イベントクリップデータ。
    タイムは全てフレームで指定する。
    """

    def __init__(self, start: et.Time, end: et.Time, label: str, **kwargs):
        super().__init__(start, end, label, **kwargs)
        # Maya では評価されないので必要最低限のパラメーターを引数に取る

    def get_clip_parameters(self) -> tp.Tuple:
        # in, out の無いクリップなので、start_time, end_time のパラメーターしか存在しない。
        return ClipParameters(self._start_time, self._end_time, 0, 0, 0)


class EvaluatedClip(object):
    """
    特定のフレームで評価されたクリップのデータが複雑になってきたので、クリップと評価された内部フレームをまとめたクラス
    """

    def __init__(self, clip: et.BaseClipData, frame: int):
        self._clip = clip
        self._frame = frame

    def __str__(self):
        return f"{self._clip} at {self._frame}"

    @property
    def clip(self):
        return self._clip

    @property
    def frame(self):
        return self._frame


# ===========================================================================
# シーケンサー用のモデル
# ===========================================================================


class SequencerModel(ExtendedTimelineModel):

    def __init__(self):
        super().__init__()

    def find_group(self, name: str, get_index: bool = False) -> tp.Optional[tp.Union[et.TimelineGroupItem, QtCore.QModelIndex]]:
        """
        グループトラックが既に存在するか調べ、存在すればそのグループトラックを返します。
        get_index が True の場合は、グループトラックの代わりに Model Index を返します。
        存在しない場合は None が返ります。
        現在はトップレベルのグループしか検知しません。
        """
        model_index = QtCore.QModelIndex()
        row_count = self.rowCount(model_index)

        for row in range(row_count):
            index: QtCore.QModelIndex = self.index(row, 0, model_index)
            item: et.TimelineGroupItem = self.itemFromIndex(index)

            if isinstance(item, et.TimelineGroupItem) and item.text() == name:
                if get_index:
                    return index
                else:
                    return item

        return None

    def get_track_from_name(self, group_name: str, track_name: str) -> tp.Optional["SequencerTrack"]:
        """
        グループ名とトラック名を指定して、トラックデータを取得します。
        名前が一致しなかった場合は None が返ります。
        """
        group_index = self.find_group(group_name, get_index=True)
        row_count = self.rowCount(group_index)
        for row in range(row_count):
            row_index: QtCore.QModelIndex = self.index(row, 0, group_index)
            item: AbstractTimelineBaseTrackItem = self.itemFromIndex(row_index)
            track_data = item.track_data()
            if track_data.display_name() == track_name:
                return track_data

        return None


# ===========================================================================
# Group に登録する用のトラックデータ
# ===========================================================================

class SequencerGroupTrackData(et.GroupTrackData):
    """
    Group に登録する用のトラックデータ。
    シーケンサー用のトラックに追加するTrackDataとは異なるインターフェースになっているので注意。
    """

    def __init__(self, name: str, event_type, **kwargs):
        super().__init__(name, **kwargs)
        self._event_type = event_type
        self._properties = {}
        self.track_usage = ApplicationType.Any  # グループトラックがアプリ側で評価されるかどうか判別用

    @classmethod
    def track_base_type(cls) -> et.TrackBaseType:
        """(override)"""
        return et.TrackBaseType.GroupBasedTrack

    @classmethod
    def track_type(cls) -> et.TrackType:
        """(override)"""
        return et.TrackType.SimpleGroup

    @classmethod
    def gui_height_scale(cls) -> float:
        """GUI 上の見た目の高さのScale"""
        return 1.0

    def add_or_edit_property(self, name: str, value: str):
        """トラックプロパティの新規追加。キーが既にあればデータの変更。"""
        self._properties[name] = value

    def get_event_type(self) -> str:
        """グループトラックのイベントタイプを返します。"""
        return self._event_type

    def get_property(self) -> tp.Dict:
        """トラックプロパティを返す。"""
        return self._properties

    def get_track_usage(self):
        return self.track_usage

    def set_name(self, name: str):
        """グループトラックの名前をセットします。"""
        self._name = name
        item = self.get_track_item()
        item.setText(name)

    def set_property(self, properties: tp.Dict):
        """トラックプロパティをセット。"""
        self._properties = properties

    def set_track_usage(self, app_type: ApplicationType):
        self.track_usage = app_type


# ===========================================================================
# シーケンサー用のトラック
# ===========================================================================

class SequencerTrack(et.AbstractClipBasedTrackData):
    """
    Sequencerで扱うベースとなるトラック。インスタンス化されない想定
    """
    height_scale = 4.0
    track_usage = ApplicationType.Any

    def __init__(self, name: str):
        super().__init__(name)
        self._properties = {}

    @classmethod
    def track_type(cls) -> et.TrackType:
        """(override) TrackType"""
        raise NotImplementedError()

    @classmethod
    def gui_height_scale(cls) -> float:
        """(override) GUI 上の見た目の高さのScale"""
        return cls.height_scale

    @classmethod
    def get_track_usage(cls):
        return cls.track_usage

    @classmethod
    def set_height_scale(cls, value):
        """(virtual)"""
        cls.height_scale = value

    @classmethod
    def set_track_usage(cls, usage: ApplicationType):
        cls.track_usage = usage

    def add_sequencer_clip(self, clip_parm: tp.Union[tp.Tuple, ClipParameters], label,
                           status: ClipStatus = ClipStatus.Nothing) -> tp.Optional[SequencerClipData]:
        """
        自身のトラックにクリップを追加します。
        自身のトラックタイプによって適切なクリップが自動で追加されます。
        clip_parm は次のようなタプル (start, end, start_offset, in, out), もしくは ClipParameters オブジェクトを想定。
        in, out のないカメラクリップではタプルの start, end さえあれば良いので、要素数は２つだけあれば良い。
        ClipParameters オブジェクトは上記のタプルの様に[]にインデックスを付けてアクセス付けるので同等に扱える。
        """
        # TODO helperクラスを使った実装に書き直す。用はここでは追加せずに_notifyだけをして、ヘルパークラス側で追加をする。
        item: AbstractTimelineBaseTrackItem = self.get_track_item()
        if not item:
            log.error("you can't add a clip before adding this track to Timeline.")
            return None

        model: et.TimelineItemModel = item.model()
        model.time_in_track_data_update_begin.emit(None)

        if self.track_type() == TrackType.Camera:
            new_clip = CameraClipData(clip_parm[0], clip_parm[1], label)
            # 定義ファイルを元にデフォルトのプロパティデータを入れる
            property_data = create_clip_property_dict("Camera")
            new_clip.set_clip_property(property_data)

        elif self.track_type() == TrackType.Motion:
            new_clip = MotionClipData(clip_parm[0], clip_parm[1], clip_parm[2], label)
            # in, out のパラメーターが渡されていれば、in, out も設定する
            if len(clip_parm) == 5:
                new_clip._in_time_offset = clip_parm[3]
                new_clip._out_time_offset = clip_parm[4]
            # 定義ファイルを元にデフォルトのプロパティデータを入れる
            property_data = create_clip_property_dict("Motion")
            new_clip.set_clip_property(property_data)

        elif self.track_type() == TrackType.Event:
            new_clip = EventClipData(clip_parm[0], clip_parm[1], label)
            # 定義ファイルを元にデフォルトのプロパティデータを入れる
            parent = self.get_parent_group_track_data()
            if parent:
                property_data = create_clip_property_dict(parent.get_event_type())
                new_clip.set_clip_property(property_data)

        else:
            log.error(f"unknown type {self.track_type()}. failed to add sequencer clip")
            return None

        result = self.insert_clip(new_clip)
        new_clip.set_status(status)
        model.time_in_track_data_update_end.emit(None)

        if result:
            return new_clip
        else:
            log.error("failed to add sequencer clip")
            return None

    def get_event_type(self) -> tp.Optional[str]:
        """
        このトラックのが属するグループのイベントタイプを返します。
        グループに属していない場合はNoneが返ります。
        """
        group_track = self.get_parent_group_track_data()
        if group_track:
            return group_track.get_event_type()
        else:
            return None

    def get_parent_group_track_data(self) -> tp.Optional[SequencerGroupTrackData]:
        item: et.AbstractTimelineBaseTrackItem = self.get_track_item()
        group_item: et.AbstractTimelineBaseTrackItem = item.parent()
        if group_item:
            group_track_data = group_item.track_data()
            return group_track_data
        else:
            return None

    def remove_sequencer_clip(self, clip: SequencerClipData) -> bool:
        """
        アプリ側から直接呼ばずに、Sequencer.remove_sequencer_clip() からこの関数を呼び出して削除する想定
        Sequencer.notify_clip_delete() → Sequencer.remove_sequencer_clip() → この関数が呼ばれる
        """
        item: AbstractTimelineBaseTrackItem = self.get_track_item()
        model: et.TimelineItemModel = item.model()
        model.time_in_track_data_update_begin.emit(None)
        result = self.remove_clip(clip)
        model.time_in_track_data_update_end.emit(None)  # このタイミングでGUI再描画してrectも消される
        if result:
            return True
        else:
            log.error("failed to remove clip")
            return False

    def add_or_edit_property(self, name: str, value: str):
        """トラックプロパティの新規追加。キーが既にあればデータの変更。"""
        self._properties[name] = value

    def get_property(self) -> tp.Dict:
        """トラックプロパティを返す。"""
        return self._properties

    def set_name(self, name: str):
        """トラックの名前をセットします。"""
        self._name = name
        item = self.get_track_item()
        item.setText(name)

    def set_property(self, properties: tp.Dict):
        """トラックプロパティをセット。"""
        self._properties = properties


class MotionTrack(SequencerTrack):
    """
    モーションクリップ格納用のトラック。
    """
    height_scale = 2.0
    track_usage = ApplicationType.Any

    def __init__(self, name: str):
        super().__init__(name)
        self.set_element_color("#008000")

    @classmethod
    def track_type(cls) -> TrackType:
        """(override) TrackType"""
        return TrackType.Motion


class CameraTrack(SequencerTrack):
    """
    カメラクリップ格納用のトラック。
    """
    height_scale = 2.0
    track_usage = ApplicationType.Any

    def __init__(self, name: str):
        super().__init__(name)
        self.set_element_color("#305ba1")

    @classmethod
    def track_type(cls) -> TrackType:
        """(override) TrackType"""
        return TrackType.Camera


class EventTrack(SequencerTrack):
    """
    SE格納用のトラック。
    """
    height_scale = 2.0
    track_usage = ApplicationType.Cyllista

    def __init__(self, name: str):
        super().__init__(name)
        self.set_element_color("#8F468E")

    @classmethod
    def track_type(cls) -> TrackType:
        """(override) TrackType"""
        return TrackType.Event


# ===========================================================================
# シーケンサーの左側のトラックが表示されている部分の TreeView クラス
# ===========================================================================


class EditPropertyDialog(QtWidgets.QDialog):
    """トラックデータのプロパティ編集ダイアログ"""

    def __init__(self, controller: et.AbstractDataController, model_index: QtCore.QModelIndex, track_data: AbstractBaseTrackData):
        super().__init__()
        self._controller = controller
        self._model_index = model_index  # 疑似サーバーに渡すために必要
        self.setWindowTitle("Edit Property")
        self.layout = QtWidgets.QFormLayout()

        self.properties = track_data.get_property()
        for property_name in self.properties.keys():
            value = self.properties[property_name]
            line_edit = propertygui.StringLineEdit()
            line_edit.value = value
            line_edit.editing_finished.connect(functools.partial(self.on_property_data_changed, property_name))
            self.layout.addRow(property_name, line_edit)

        self.setLayout(self.layout)

    def on_property_data_changed(self, property_name, new_text):
        """ Signal を Emit してサーバー側でデータの更新処理をする"""
        # print(f"new value is {new_text}")
        change_property = {"change_track_property_data": et.variantstream.Dictionary({property_name: new_text})}
        self._controller.view_observee().track_property_changed.emit(self._model_index, change_property)


class SequencerTreeView(et.TimelineTreeView):
    """シーケンサーの左側のトラックが表示されている部分のビュー。クラス継承しているので、ここでカスタマイズをする"""

    def __init__(self, controller: et.AbstractDataController, parent=None, **kwargs) -> None:
        super().__init__(controller, parent, **kwargs)
        self._controller = controller
        self.edit_dialog_func = self._edit_property
        self.add_default_menu_action()

    def add_default_menu_action(self):
        self.add_context_menu_action("Edit Property", self.edit_dialog_func)

    def get_selected_track_data(self):
        index = self.currentIndex()
        track_index = index.siblingAtColumn(et.conf.ModelColumnIndex.MODEL_ITEM)
        item = self.model().itemFromIndex(track_index)
        return item.track_data()

    def set_edit_dialog_func(self, func=None):
        if func:
            self.edit_dialog_func = func
        self._context_menu.clear()
        self.add_default_menu_action()

    def _edit_property(self):
        track_data = self.get_selected_track_data()
        properties = track_data.get_property()
        # print(f"{track_data} Property = {properties}")
        if len(properties) > 0:
            model_index: QtCore.QModelIndex = self.currentIndex()
            dlg = EditPropertyDialog(self._controller, model_index, track_data)
            dlg.exec()


# ===========================================================================
# TimeSlider クラス。オーバーライドしてカスタマイズする用
# ===========================================================================

class SequencerTimeSlider(et.TimelineTimeSlider):
    def __init__(self, controller: et.AbstractDataController, parent=None):
        super().__init__(controller, parent)
        # print("custom time slider!")
        self.app_type = ApplicationType.Cyllista  # デフォルトで汎用タイムラインの機能を使う。

    def emit_signal(self, sec: float):
        frame = et.utility.sec_to_frame(sec)
        signals = SequencerSignals.get_instance()
        signals.time_slider_mouse_moved.emit(frame)

    # def mousePressEvent(self, event):
    #     if self.app_type & ApplicationType.Cyllista:
    #         super().mousePressEvent(event)
    #     else:
    #         # Maya側は現在フレーム変更せずにシグナル出すだけ
    #         self.emit_signal(self._calc_click_sec(event))
    #         self._has_dragged_guide = True
    #
    # def mouseMoveEvent(self, event):
    #     if self.app_type & ApplicationType.Cyllista:
    #         super().mouseMoveEvent(event)
    #     else:
    #         # Maya側は現在フレーム変更せずにシグナル出すだけ
    #         if self._has_dragged_guide:
    #             self.emit_signal(self._calc_click_sec(event))

    def set_app_type(self, app_type: ApplicationType):
        self.app_type = app_type

    def _set_current_time(self, sec: float):
        # この関数をオーバーライドしたほうが実装が楽だが、副作用がある可能性あり。
        # 問題がある場合はマウスイベントのオーバーライドに変更する
        # Play Range を変更した時に、勝手に現在フレームが変わる場合があるが、その時はシグナルが発火しない。
        if self.app_type & ApplicationType.Cyllista:
            super()._set_current_time(sec)
        else:
            self.emit_signal(sec)

# ===========================================================================
# シーケンサー用のTimelineViewクラス
# ===========================================================================


class SequencerTimelineView(et.TimelineView):
    """TimelineViewをカスタマイズする用のクラス"""

    def __init__(self, controller: et.AbstractDataController = None):
        super().__init__(controller)
        self.get_playback_panel().hide_stop_and_loop_icons()
        self.get_footer().set_visible_range_edit(True)
        self.get_controller().set_is_bounds_reset_on_timeline_length_changed(False)

        self.seq_ctrl: Sequencer = None

    @classmethod
    def create_time_slider(cls, controller: et.AbstractDataController, parent: QtWidgets.QWidget = None) -> et.TimelineTimeSlider:
        # return et.TimelineTimeSlider(controller, parent)
        return SequencerTimeSlider(controller, parent)

    @classmethod
    def create_tree_view(cls, controller: et.AbstractDataController, parent: QtWidgets.QWidget = None) -> et.TimelineTreeView:
        """ シーケンサー用のTreeViewを作成 """
        return SequencerTreeView(controller, parent)

    def disable_playback_signal(self):
        # print("disconnecting")
        playback_panel = self.get_playback_panel()
        playback_panel.backward_button.clicked.disconnect(self._on_backward_clicked)
        playback_panel.skip_backward_button.clicked.disconnect(self._on_skip_backward_clicked)
        playback_panel.stop_button.clicked.disconnect(self._on_stop_clicked)
        playback_panel.play_button.toggled.disconnect(self._on_play_clicked)
        playback_panel.skip_forward_button.clicked.disconnect(self._on_skip_forward_clicked)
        playback_panel.forward_button.clicked.disconnect(self._on_forward_clicked)
        playback_panel.loop_button.clicked.disconnect(self._on_loop_clicked)

    def set_ctrl(self, ctrl):
        self.seq_ctrl = ctrl

    # def mouseDoubleClickEvent(self, event) -> None:
    #     print('double click')
    #     self.seq_ctrl.evaluate_current_frame()
    #     clips = self.seq_ctrl.get_selected_clips()
    #     for clip in clips:
    #         prop = clip.get_clip_property()
    #         print(prop)


# ===========================================================================
# オブザーバーとシグナル
# ===========================================================================


class SequencerObserver(TimelineBasicViewObserver):
    """
    シグナル監視用クラス。
    ベースクラスの関数をオーバーライドしたりしてカスタマイズする。
    """

    def __init__(self, sequence_ctrl, model: et.TimelineItemModel, view_observable: et.ViewObservableInterface, **kwargs):
        super().__init__(model, view_observable, **kwargs)
        self._sequencer_ctrl = sequence_ctrl
        self._signals = SequencerSignals.get_instance()
        self._view_observable: et.ViewObservableInterface = view_observable
        self._view_observable.trackview_rect_double_clicked.connect(self._sequencer_ctrl.on_clip_double_clicked)

    def _clip_create(self, clip_idx: int, clipd: et.BaseClipData, value):
        ...

    def _clip_delete(self, clip_idx: int, clip: et.BaseClipData, value):
        """(override) on_clip_property_changed() から呼ばれる関数。アプリ側でoverrideしてカスタマイズ可能"""
        if value is None:
            # delete キーによって削除された場合
            self._sequencer_ctrl.remove_sequencer_clip(clip)

    def _clip_moved(self, clip_idx: int, clip: et.BaseClipData, new_frame):
        """(override) クリップが移動した時の処理"""
        if clip.is_with_in_out():
            new_frame = new_frame - clip._in_time_offset
        self._sequencer_ctrl.on_clip_moved(clip, clip.start_time, new_frame)

    def _clip_start_changed(self, clip_idx: int, clip: et.BaseClipData, new_start_frame):
        """(override) start の変更、すなわち in が変更された時の処理"""
        self._sequencer_ctrl.on_clip_in_changed(clip, new_start_frame)

    def _clip_duration_changed(self, clip_idx: int, clip: et.BaseClipData, duration):
        """(override) duration の変更、すなわち out が変更された時の処理"""
        if clip.is_with_in_out():
            new_frame = clip.in_time + duration
        else:
            new_frame = clip.end_time
        self._sequencer_ctrl.on_clip_out_changed(clip, new_frame)

    def _track_delete(self, midx: QtCore.QModelIndex, item: et.AbstractTimelineBaseTrackItem):
        track_data = item.track_data()

        # グループトラックの場合は内部トラックを先に消す
        if track_data.track_base_type() == et.TrackBaseType.GroupBasedTrack:
            for row in range(self._model.rowCount(midx)):
                # 子供の数だけ削除シグナルを出す。子供のIndexは0を指定しないと削除のタイムラグで全ての子供が正しく削除されない。
                child_index: QtCore.QModelIndex = self._model.index(0, 0, midx)
                self._view_observable.track_property_changed.emit(child_index, {"delete_track": None})
            # グループ内のトラックが全て削除できてから、グループトラック自体を削除
            self._sequencer_ctrl.remove_sequencer_track(track_data)

        # 普通のトラックなら内部クリップを全て消してから自身を削除
        else:
            change_properties = {"delete_clip": None}
            clips = track_data.clips()
            for i in range(len(clips)):  # Clipの数だけリストの最初の要素を消す。消すたびにリストの中身が変更されるので常に0番目を削除
                # print(clips)
                self._view_observable.clip_property_changed.emit(0, clips[0], change_properties)  # clip_index は使われていないので0でOK
            # トラック内のClipが全て削除できてから、トラック自体を削除
            self._sequencer_ctrl.remove_sequencer_track(track_data)

    def _track_property_data_changed(self, item: AbstractTimelineBaseTrackItem, dict_: et.ClipProperty2VariantStreamValueDict):
        track_data: SequencerTrack = item.track_data()
        property_dict = track_data.get_property()
        data_dict = dict_.get_raw_value()
        key = list(data_dict.keys())[0]
        value = data_dict[key]
        property_dict[key] = value


class SequencerSignals(QtWidgets.QWidget):
    """
    Core側で実装されていない、Sequencerアプリ側で必要なシグナルを集めたクラス。
    どこからでもアクセスできるようにシングルトンにしてある。
    """
    __instance = None
    motion_clip_evaluated = QtCore.Signal(object)  # dict
    clip_status_changed = QtCore.Signal(object)  # clip
    time_slider_mouse_moved = QtCore.Signal(int)  # frame
    play_range_changed = QtCore.Signal(int, int)  # start_frame, end_frame
    timeline_length_changed  = QtCore.Signal(int)  # frame

    def __init__(self):
        super().__init__()

    @classmethod
    def get_instance(cls):
        """
        このクラスのインスタンスを取得。
        """
        if cls.__instance is None:
            cls.__instance = SequencerSignals()
        return cls.__instance


# ===========================================================================
# シーケンサー本体
# ===========================================================================

class Sequencer(object):
    """
    メインのシーケンサー。
    MayaとCyllista共通のAPI。
    Singletonとして存在し、簡単にアクセスできるようにした。
    全ての操作はこのクラスを通して出来るようにする想定
    """

    # クラス変数
    __instance = None

    def __init__(self, timeline_view=None):
        if timeline_view:
            self._timeline_view: et.TimelineView = timeline_view
        else:
            self._timeline_view: SequencerTimelineView = SequencerTimelineView(controller=None)

        self._timeline_view.set_ctrl(self)
        self._model: SequencerModel = SequencerModel()
        self._timeline_view.set_model(self._model)
        # self._timeline_view.get_tree_view().setColumnHidden(conf.ModelColumnIndex.LOCK, False)
        self._model.set_time_controller(self._timeline_view.get_controller().time_ctrl)
        self._observer = SequencerObserver(self, self._model, self._timeline_view)
        self._controller = self._timeline_view.get_controller()
        self._time_ctrl = self._controller.time_ctrl
        self._signals = SequencerSignals.get_instance()
        self._timeline_view.get_track_view().set_is_zoom_on_wheel_enabled(True)
        self._timeline_view.get_track_view().set_is_middle_drag_pan_enabled(True)
        self._application_type = ApplicationType.Any

        SequencerIcons.init_icons()

        # signal
        self._model.current_time_evaluated.connect(self.on_current_frame_evaluated)
        self._controller.track_play_bounds_changed.connect(self.on_track_play_bounds_changed)
        self._controller.track_length_changed.connect(self.on_timeline_length_changed)
        self._signals.motion_clip_evaluated.connect(self.on_motion_clip_evaluated)
        self._signals.clip_status_changed.connect(self.on_clip_status_changed)

    def __del__(self):
        print('disconnecting signal')
        self._model.current_time_evaluated.disconnect(self.on_current_frame_evaluated)
        self._signals.motion_clip_evaluated.disconnect(self.on_motion_clip_evaluated)

    @classmethod
    def get_instance(cls):
        """
        このクラスのインスタンスを取得。
        Mayaシーケンサー側ではオーバーライドされた関数が呼ばれるので、これは純粋にAPI用の関数。
        """
        if cls.__instance is None:
            cls.__instance = Sequencer()
        return cls.__instance

    def add_group_track(self, event_type: str, name: str = "") -> tp.Optional[et.AbstractTimelineBaseTrackItem]:
        """タイムラインにグループトラックを追加します。"""
        group = self._model.find_group(name)

        # nameがパラメーターとして渡され、既に同名のグループがあった場合は追加しない。
        if name and group:
            return None

        group_track_item = self._model.append_track_row(SequencerGroupTrackData(name, event_type))
        return group_track_item

    def add_track(self, track: SequencerTrack, group_item: et.AbstractTimelineBaseTrackItem = None) -> SequencerTrack:
        """トラックをモデルに追加します。引数に取ったトラックをそのまま返します。"""
        # TODO append_track_row()でNoneが返ってくるらしいのでチェックせよ
        if group_item:
            self._model.append_track_row(track, group_item)
            self._timeline_view.get_track_view().expandAll()
            self._timeline_view._treeview.expandAll()
            track_usage = track.get_track_usage()
            group_track = group_item.track_data()
            group_track.set_track_usage(track_usage)

        else:
            self._model.append_track_row(track)
        return track

    def clear_model(self) -> None:
        """タイムラインデータを全部削除します。"""
        self._model.clear()

    def evaluate_current_frame(self) -> None:
        """
        明示的に時間変更シグナルを出すことで、現在のフレームを処理します。
        すなわち、シーケンサーだと現在フレームでのMotionClipが評価されます。
        """
        time = self._time_ctrl.current_time
        self._time_ctrl.current_time_changed.emit(time)

    def find_clips(self, name) -> tp.Optional[tp.List[et.BaseClipData]]:
        """
        クリップが既に存在するか調べ、存在すればそのクリップを返します。
        存在しない場合は None が返ります。
        """
        # TODO 同名クリップを許すかどうか・・・。現在は同名クリップが可能なので、戻り値はリストになる。
        result = []
        clips = self.get_all_clips()
        for clip in clips:
            if clip.get_label() == name:
                result.append(clip)

        return result

    def find_group(self, name) -> tp.Optional[et.TimelineGroupItem]:
        """
        グループトラックが既に存在するか調べ、存在すればそのグループトラックを返します。
        存在しない場合は None が返ります。
        """
        return self._model.find_group(name)

    def find_tracks(self, name) -> tp.Optional[tp.List[SequencerTrack]]:
        """
        トラックが既に存在するか調べ、存在すればそのトラックを返します。
        存在しない場合は None が返ります。
        """
        # TODO 同名トラックを許すかどうか・・・。現在は同名トラックが可能なので、戻り値はリストになる。名前 get のほうがいいか？
        result = []
        tracks = self.get_all_tracks()
        for track in tracks:
            if track.display_name() == name:
                result.append(track)

        return result

    def filter_evaluated_clip_data(self, data: tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]], app_type: ApplicationType):
        """
        on_motion_clip_evaluated()の引数に渡される data をフィルターする関数
        APIの仕様では、現在フレームが評価されるとMaya用のクリップとCyllista用のクリップの両方が評価される。
        それをアプリ側でMaya用だけのデータ、Cyllista用だけのデータにフィルターする為にこの関数を使う。
        """
        remove_group_list = []
        for group in data:
            # print(group)
            group_usage = group.get_track_usage()
            if ~group_usage & app_type:  # ビット演算わかりにくいか・・・
                remove_group_list.append(group)

        for group in remove_group_list:
            data.pop(group)

        return data

    def get_all_groups(self, model_index=QtCore.QModelIndex()) -> tp.List[SequencerGroupTrackData]:
        """Timeline 上の全てのGroupを取得します。"""
        result = []

        for row in range(self._model.rowCount(model_index)):
            idx: QtCore.QModelIndex = self._model.index(row, 0, model_index)
            item: AbstractTimelineBaseTrackItem = self._model.itemFromIndex(idx)
            if item.track_base_type() == TrackBaseType.GroupBasedTrack:
                result.append(item.track_data())

        return result

    def get_all_tracks(self, model_index=QtCore.QModelIndex()) -> tp.List[SequencerTrack]:
        """Timeline 上の全てのTrackを取得します。"""
        result = []
        for row in range(self._model.rowCount(model_index)):
            idx: QtCore.QModelIndex = self._model.index(row, 0, model_index)
            item: AbstractTimelineBaseTrackItem = self._model.itemFromIndex(idx)
            if item.track_base_type() == TrackBaseType.GroupBasedTrack:
                track = self.get_all_tracks(idx)
                result += track
            elif item.track_base_type() == TrackBaseType.ClipBasedTrack:
                track = item.track_data()
                result.append(track)

        return result

    def get_all_clips(self, model_index=QtCore.QModelIndex()) -> tp.List[SequencerClipData]:
        """Timeline 上の全てのクリップを取得します。"""
        result = []

        for row in range(self._model.rowCount(model_index)):
            idx: QtCore.QModelIndex = self._model.index(row, 0, model_index)  # mdl.invisibleRoot()
            item: AbstractTimelineBaseTrackItem = self._model.itemFromIndex(idx)
            if item.track_base_type() == TrackBaseType.GroupBasedTrack:
                clips = self.get_all_clips(idx)
                result = result + clips
            elif item.track_base_type() == TrackBaseType.ClipBasedTrack:
                clips = item.track_data().clips()
                result = result + clips

        return result

    def get_application_type(self) -> ApplicationType:
        """シーケンサーアプリが、Maya用かCyllista用かなどを示す ApplicationType を返します。"""
        return self._application_type

    def get_selected_track_data(self) -> SequencerTrack:
        """タイムラインで選択中の SequencerTrack を返します"""
        # 別のColumnを選択していると正しくTrack Dataが取れないことがあるので、最初のColumnを指定することで確実にTrack Data取得
        item: AbstractTimelineBaseTrackItem = self.get_selected_track_item()  # このitemが track_item とは限らない。
        index: QtCore.QModelIndex = self._model.indexFromItem(item)
        track_index = index.siblingAtColumn(et.conf.ModelColumnIndex.MODEL_ITEM)
        track_item = self._model.itemFromIndex(track_index)
        return track_item.track_data()

    def get_selected_track_item(self):
        """タイムラインで選択中の Item を返します"""
        index = self._timeline_view._treeview.selectionModel().currentIndex()
        return self._model.itemFromIndex(index)

    def get_selected_clips(self) -> tp.Optional[SequencerClipData]:
        """
        選択中のクリップ(複数)を返します。
        """
        def _get_all_selected_rects(model_index: QtCore.QModelIndex = QtCore.QModelIndex()) -> tp.List[et.TrackViewRectOnTrackItem]:
            """Model内部を再帰ループしながら、全トラックの選択されているRectを返す。"""
            rects = []
            model = self._timeline_view._trackview.get_model()
            row_count = model.rowCount(model_index)

            # debug print
            # item = model.itemFromIndex(model_index)
            # if item:
            #     track_data = item.track_data()
            #     print(track_data, row_count)

            track_view = self._timeline_view.get_track_view()
            for row in range(row_count):
                row_index: QtCore.QModelIndex = model.index(row, 0, model_index)
                rects += _get_all_selected_rects(row_index)

                widget: et.TrackViewItemWidget = track_view.indexWidget(row_index)
                if widget:
                    rects += widget.get_selected_rects()

            return rects

        rects = _get_all_selected_rects()

        clips = []
        for rect in rects:
            clip = rect.get_elm_data()
            clips.append(clip)

        return clips

    def get_timeline_view_widget(self) -> et.TimelineView:
        return self._timeline_view

    def notify_clip_add(self, track: SequencerTrack, play_range, label):
        """クリップの追加の入り口となる関数。この通知を元にObserver側で追加関数の呼び出しが行われる。未実装"""
        # TODO 何とかして引数のデータをDictにする。
        # change_properties: ClipProperty2VariantStreamValueDict = {"add_clip": None}
        # self._timeline_view.clip_property_changed.emit(index, clip, change_properties)
        ...

    def notify_clip_delete(self, clip: SequencerClipData):
        """クリップの削除の入り口となる関数。この通知を元にObserver側で削除関数の呼び出しが行われる。"""
        change_properties: ClipProperty2VariantStreamValueDict = {"delete_clip": None}
        track_data = clip.track_data()
        index = track_data.find_track_element_index(clip)
        self._timeline_view.clip_property_changed.emit(index, clip, change_properties)

    def notify_track_delete(self, track: SequencerTrack):
        item = track.get_track_item()
        model_index = self._model.indexFromItem(item)
        self._timeline_view.track_property_changed.emit(model_index, {"delete_track": None})

    def on_clip_double_clicked(self, data):
        """
        (virtual)
        トラックビューで Clip をダブルクリックされた際に呼び出される関数です。
        data にはクリックされた Clip のデータが渡されます。
        """
        # print(data)
        ...

    def on_clip_in_changed(self, clip: SequencerClipData, frame):
        """(virtual) クリップの in が変更されたときに呼ばれます。"""
        # print(f"app clip in changed, {clip}, {frame}")
        ...

    def on_clip_moved(self, clip: SequencerClipData, old_frame, new_frame):
        """(virtual) クリップが移動されたときに呼ばれます。"""
        # print(f"api clip moved {clip}, from {old_frame} to {new_frame}")
        ...

    def on_clip_out_changed(self, clip: SequencerClipData, frame):
        """(virtual) クリップの out が変更されたときに呼ばれます。"""
        # print(f"app clip out changed, {clip}, {frame}")
        ...

    def on_clip_status_changed(self, clip: BaseClipData):
        """クリップのステータスが変更された時に呼ばれます。"""
        # アイコンは既にセット済みなので、Rectを再描画
        self._model.time_in_track_data_update_begin.emit(None)
        track_item: AbstractTimelineBaseTrackItem = clip.track_data().get_track_item()
        index: QModelIndex = self._model.indexFromItem(track_item)
        self._model.time_in_track_data_update_end.emit(index)  # このクリップが含まれるトラックのRectだけ再描画

    def on_current_frame_evaluated(self, data_elements: tp.Sequence):
        """
        現在のフレームで評価された Motion Clip をディクショナリ化してシグナルをエミットします。
        現在のフレームが変わるたびに毎回呼び出されます。
        """
        # TODO 関数長いのでリファクタリングしたい。しかしどうやって分けたらいいものか・・・

        def _print_clip(group_dict: tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]]):
            """返すDictデータのデバッグ用に"""
            for group_track in group_dict:
                print(group_track)
                for evaluated_clip in group_dict[group_track]:
                    print(f"    {evaluated_clip}")

        def _find_top_track_index(group: SequencerGroupTrackData,
                                  group_dict: tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]]) -> int:
            """クリップのディクショナリデータから、一番上に存在するクリップのトラックの index を計算する。"""
            index = 9999
            for evaluated_clip in group_dict[group]:
                temp_index = evaluated_clip.clip.get_row_index()
                if temp_index < index:
                    index = temp_index
            return index

        def _create_group_dict(evaluated_clips: tp.List[EvaluatedClip]) -> tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]]:
            """tp.List[EvaluatedClip] からグループを Key に持つ [EvaluatedClip] のディクショナリを作成"""
            group_dict: tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]] = {}
            for evaluated_clip in evaluated_clips:
                parent_group_track: SequencerGroupTrackData = evaluated_clip.clip.get_parent_track()
                # print(f"{clip}, {index}, {parent_track}")
                if parent_group_track:
                    if parent_group_track not in group_dict:
                        group_dict[parent_group_track] = [evaluated_clip]
                    else:
                        group_dict[parent_group_track].append(evaluated_clip)
            return group_dict

        def _extract_top_clips(group_dict: tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]]) -> tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]]:
            """_create_group_dict() で作られたグループごとのClipデータから、一番上のクリップだけを含むDictを作成"""
            new_group_dict: tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]] = {}
            for group_track in group_dict:
                # Cyllista関連のグループトラックならば全てのクリップを含める
                group_usage = group_track.get_track_usage()
                if group_usage == ApplicationType.Cyllista:
                    # print(group_dict[group_track])
                    new_group_dict[group_track] = group_dict[group_track]
                    continue

                top_index = _find_top_track_index(group_track, group_dict)
                # print(f"group={group}, index={top_index}")
                for evaluated_clip in group_dict[group_track]:
                    index = evaluated_clip.clip.get_row_index()
                    if top_index == index:
                        if group_track not in new_group_dict:
                            new_group_dict[group_track] = [evaluated_clip]
                        else:
                            new_group_dict[group_track].append(evaluated_clip)
            return new_group_dict

        # on_current_frame_evaluated()のメイン処理は以下から
        # data_elements には Key や Clip など全データが来るので、クリップだけフィルターし、評価フレームを合成したデータ作成
        current_frame = self._time_ctrl.current_frame
        evaluated_clips: tp.List[EvaluatedClip] = []
        for elm in data_elements:
            if isinstance(elm, et.BaseClipData):
                clip_evaluation_frame = elm.evaluate(current_frame)
                evaluated_clips.append(EvaluatedClip(elm, clip_evaluation_frame))

        # グループとクリップのディクショナリ作成。グループが無いトップのトラックは除外
        group_dict = _create_group_dict(evaluated_clips)

        # 最上部のクリップだけを含む新しいディクショナリ作成
        new_group_dict = _extract_top_clips(group_dict)

        # _print_clip(new_group_dict)
        self._signals.motion_clip_evaluated.emit(new_group_dict)

    def on_motion_clip_evaluated(self, data: tp.Dict[SequencerGroupTrackData, tp.List[EvaluatedClip]]):
        """
        (virtual)
        現在のフレームでの MotionClip と評価されたフレームがディクショナリ形式で渡されます。
        現在のフレームが変わるたびに毎回呼び出されます。
        motion_clip_evaluatedシグナルのスロット。
        """
        ...
        # data = self.filter_evaluated_clip_data(data, ApplicationType.Maya)
        # print("")
        # for group in data:
        #     print(group)
        #     evaluated_clips = data[group]
        #     for clip in evaluated_clips:
        #         print(f"    {clip.clip}, {clip.frame}")

    def on_track_play_bounds_changed(self):
        """TimelineのPlayRangeが変更された時に呼ばれる。ここからシーケンサー用の別のシグナルをEmitする。"""
        start, end = self._controller.play_range_in_frame
        self._signals.play_range_changed.emit(start, end)

    def on_timeline_length_changed(self):
        """Timelineの尺が変更された時に呼ばれる。ここからシーケンサー用の別のシグナルをEmitする。"""
        length = self._controller.timeline_length_by_frame
        self._signals.timeline_length_changed.emit(length)

    def remove_sequencer_clip(self, clip: SequencerClipData) -> bool:
        """
        Observer から呼ばれる関数。アプリ側でOverrideして挙動の変更ができます。クリップが削除された時に呼ばれます。
        この関数は直接呼ばずに、notify_clip_delete() 経由でこの関数が呼ばれることを想定。
        """
        track_data: SequencerTrack = clip.track_data()
        return track_data.remove_sequencer_clip(clip)

    def remove_sequencer_track(self, track: SequencerTrack) -> bool:
        """
        Observer から呼ばれる関数。アプリ側でOverrideして挙動の変更ができます。トラックが削除された時に呼ばれます。
        この関数は直接呼ばずに、notify_track_delete() 経由でこの関数が呼ばれることを想定。
        """
        # print(f"track delete, {track}")
        item = track.get_track_item()
        self._model.remove_track_row(item)

    def remove_selected_sequencer_clip(self) -> None:
        """選択中のトラック内で選択中のClipを削除します。"""
        clips = self.get_selected_clips()
        for clip in clips:
            if clip:
                self.notify_clip_delete(clip)

    def remove_selected_track_item(self) -> None:
        """選択中のトラックを削除します。"""
        item = self.get_selected_track_item()
        self.remove_track_item(item)

    def remove_track(self, track: SequencerTrack):
        """指定したトラックを削除します。"""
        self.notify_track_delete(track)

    def remove_track_item(self, item: et.AbstractTimelineBaseTrackItem) -> None:
        """指定したトラックItemを削除します。"""
        track = item.track_data()
        self.notify_track_delete(track)

    def rebuild(self) -> None:
        self._timeline_view._trackview.rebuild_items()

    def set_application_type(self, app_type: ApplicationType):
        """シーケンサーアプリが、Maya用かCyllista用かなどを示す ApplicationType をセットします。"""
        self._application_type = app_type

    def set_frame_range(self, view_start, view_end, play_start, play_end) -> None:
        """
        Timelineのフレームレンジをセットします。
        end フレームはタイムラインの尺以上に伸ばすことは出来ないので、先に self.set_timeline_length() で尺を設定してください。
        """
        self._controller.set_track_view_bounds(et.utility.frame_to_sec(view_start), et.utility.frame_to_sec(view_end))
        self._controller.set_track_play_bounds(et.utility.frame_to_sec(play_start), et.utility.frame_to_sec(play_end))

    def set_curernt_frame(self, frame: int):
        """現在のフレームをセットします。"""
        self._controller.set_current_time(frame)

    def set_timeline_length(self, length: int):
        """ Timeline の尺を設定します。将来的に start end で設定するので関数の名前自体変わる予定"""
        self._controller.set_timeline_length(length)

    def set_time_slider_app_type(self, app_type: ApplicationType):
        """
        タイムスライダの挙動をMayaか、それ以外かによって切り替えます。
        Maya: タイムスライダのPlayHead動かないでシグナルを出すだけ
        Cyllista: タイムスライダのPlayHeadが動くが、シグナルは出さない
        """
        self._timeline_view.get_time_slider().set_app_type(app_type)

    def split_selected_clip(self) -> tp.Tuple:
        """
        選択中のクリップ（１つだけ）を現在のフレームで分割し、二つに分かれたClipをタプルで返します。
        現在フレームがクリップ外などで Split できない場合は空のタプルが返るので、タプルの要素数をチェックして成功したか確認してください。
        """
        clips = self.get_selected_clips()
        if len(clips) != 1:
            log.error("The number of selected clip must be 1.")
            return ()

        clip = clips[0]
        track_data: AbstractClipBasedTrackData = clip.track_data()
        clip_index = track_data.find_track_element_index(clip)
        track_item = track_data.get_track_item()
        model_index = self._model.indexFromItem(track_item)

        split_time = self._controller.second_to_time_in_data(self._controller.time_ctrl.current_time)

        new_clips = self._model.split_track_element(model_index, clip_index, split_time)
        return new_clips


def get_sequencer() -> Sequencer:
    """
    シーケンサーのシングルトン取得関数
    Sequencer.get_instance()をしているだけですが、モジュールの外から簡単にアクセスする用です。
    API用で、Maya側からの使用は想定していません。
    """
    return Sequencer.get_instance()
