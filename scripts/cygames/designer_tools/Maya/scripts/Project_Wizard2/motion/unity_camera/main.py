# -*- coding: utf-8 -*-
import os
import webbrowser
import math

import maya.cmds as cmds
import maya.mel as mel

try:
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtUiTools import QUiLoader
    from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
    import P4
except Exception:
    pass

g_tool_name = 'Wiz2UnityCamera'
CURRENT_PATH = os.path.dirname(__file__)
UNITY_TOOL_PREFIX = 'ExportUnityCameraForMaya'
CAMERA_WORLD_PREFIX = 'ExportUnityCameraForMaya_WorldRoot'
CAMERA_WORLD_RELATIVE = 'ExportUnityCameraForMaya_RelativeRoot'


def main():
    """Windowの起動
    Returns:
        MotionFBXWindow: ツールウィンドウのインスタンス
    """
    # メインウィンドウが開いていたらクローズして新規で開く
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name)
    ui = UnityCameraWindow()
    ui.show()


class UnityCameraWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """Unityカメラインポートウィンドウ
    """
    def __init__(self, parent=None):
        super(UnityCameraWindow, self).__init__(parent=parent)
        loader = QUiLoader()
        uiFilePath = os.path.join(CURRENT_PATH, 'unity_camera_window.ui')
        self.UI = loader.load(uiFilePath)  # QMainWindow
        self.setCentralWidget(self.UI)
        self.setWindowTitle(g_tool_name)
        self.setObjectName(g_tool_name)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.UI.action_manual.triggered.connect(show_manual)
        # カメラを「選択」ボタン
        self.UI.btn_fbx_select.clicked.connect(self.on_fbx_select)
        # 「カメラ読み込み」ボタン
        self.UI.btn_camera_load.clicked.connect(self.on_load)
        # UIの設定読み込み
        self.load_ui()

    def closeEvent(self, event):
        self.save_ui()

    def on_fbx_select(self):
        """カメラFBXの「選択」ボタンクリック
        UnityのWizard2/Motion/ExportCameraForMaya でエクスポートしたカメラのfbxを読み込む
        """
        directory_mask = '*.fbx'
        txt_fbx_path = self.UI.txt_fbx_path.toPlainText()
        if os.path.exists(txt_fbx_path):
            directory_mask = os.path.dirname(txt_fbx_path) + '/' + directory_mask
        camera_fbx_path = cmds.fileDialog(dm=directory_mask,
                                          title='UnityのWizard2/Motion/ExportCameraForMaya でエクスポートしたカメラのfbxを読み込んでください')
        if not os.path.exists(camera_fbx_path):
            return
        self.UI.txt_fbx_path.setText(camera_fbx_path)
        self.UI.txt_fbx_path.textCursor().movePosition(QtGui.QTextCursor.End)

    def on_load(self):
        # UnityからエクスポートしたExtraAttribute付きのカメラのfbxを読み込む
        import_root = load_unity_camera(self.UI.txt_fbx_path.toPlainText())
        # カメラが「オブジェクトに相対」なら撮影対象のオブジェクトを選択してもらう
        if is_root_relative(import_root):
            popup = PopupWindow(self, 'カメラを相対的な位置に読み込みます\n' +
                                '対象物を選択してOKを押してください', 'OK')
            popup.setWindowTitle('Select Target Object')
            popup.on_click = lambda: on_load_camera(is_relative=True)
            popup.show()
        else:
            on_load_camera(is_relative=False)

    def save_ui(self):
        cmds.optionVar(sv=(g_tool_name + 'txt_fbx_path', self.UI.txt_fbx_path.toPlainText()))

    def load_ui(self):
        if cmds.optionVar(exists=g_tool_name + 'txt_fbx_path'):
            saved_fbx_path = cmds.optionVar(q=g_tool_name + 'txt_fbx_path')
            self.UI.txt_fbx_path.setText(saved_fbx_path)


class PopupWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """シンプルなModelessポップアップウィンドウ
    """
    def __init__(self, parent=None, *argv):
        super(PopupWindow, self).__init__(parent=parent)
        loader = QUiLoader()
        uiFilePath = os.path.join(CURRENT_PATH, 'popup.ui')
        self.UI = loader.load(uiFilePath)  # QMainWindow
        self.setCentralWidget(self.UI)
        message = ''
        btn_label = 'OK'
        if len(argv) >= 1:
            message = argv[0]
        if len(argv) >= 2:
            btn_label = argv[1]
        self.UI.label.setText(message)
        self.UI.button.setText(btn_label)
        self.UI.button.clicked.connect(self.on_click)

    def on_click(self):
        print('Usage: ボタン実行時に実行したい関数を設定してください')


def show_manual():
    """コンフルのツールマニュアルページを開く
    """
    try:
        webbrowser.open('https://wisdom.cygames.jp/pages/viewpage.action?pageId=684077734')
    except Exception:
        cmds.warning('マニュアルページがみつかりませんでした')


def on_load_camera(is_relative):
    rel_object = cmds.ls(sl=True)
    if is_relative and not rel_object:
        cmds.confirmDialog(title='Error',
                           message='相対的なカメラでエクスポートされていますが,' +
                                   '対象オブジェクトが選択されなかったため結果が変わります',
                           button=['OK'])
    import_root = find_import_root()
    import_root = load_camera(import_root, is_relative, rel_object)
    # インポートウィンドウをクローズ
    if cmds.window(g_tool_name, exists=True):
        cmds.deleteUI(g_tool_name)


def load_camera(import_root, is_relative, rel_object):
    """UnityのWizard2/Motion/ExportCameraForMaya でエクスポートしたカメラと同じ見え方を
    シーン内のPerspectiveカメラに設定する
    Orthographicカメラには対応していない
    Args:
        camera_fbx_path (str): インポートするカメラのfbxパス
    Returns:
        str: シーンにインポートしたRootオブジェクト名
    """
    unity_cam_transform = find_unilty_camera_transform()
    if not unity_cam_transform:
        cmds.warning('Unityのカメラが見つかりませんでした')
        return
    unity_cam = get_camera_node(unity_cam_transform)
    # Resolution設定
    resolution = get_screen_resolution(import_root)
    if resolution:
        set_resolution(resolution[0], resolution[1])
    cmds.setAttr('{}.displayResolution'.format(unity_cam), True)
    # UnityのGameビューのScale値
    view_scale = get_screen_scale(import_root)
    cmds.setAttr('{}.postScale'.format(unity_cam), view_scale)
    # カメラのFrustumボックス表示
    cmds.setAttr('{}.displayCameraFrustum'.format(unity_cam), True)
    cmds.setAttr('{}.displayCameraNearClip'.format(unity_cam), True)
    cmds.setAttr('{}.displayCameraFarClip'.format(unity_cam), True)
    if is_relative:
        if not rel_object:
            cmds.warning('Relativeオブジェクトが設定されませんでした')
            cmds.confirmDialog(title='Warning',
                               message='Relativeオブジェクトが設定されませんでした',
                               button=['OK'])
        else:
            rel_mesh_obj = cmds.listRelatives(rel_object, ad=True, type='mesh')
            rel_mesh_obj = cmds.listRelatives(rel_mesh_obj, parent=True)
            if rel_mesh_obj:
                rel_mesh_obj = rel_mesh_obj[0]
            pivot_pos = cmds.xform('{}.scalePivot'.format(rel_mesh_obj), q=True, ws=True, t=True)
            cmds.select(unity_cam_transform)
            cmds.move(pivot_pos[0], pivot_pos[1], pivot_pos[2], relative=True, ws=True)
            # 相対オブジェクトのローテーションに合わせる
            temp_rot_root = cmds.spaceLocator(name='temp_rot_root')[0]
            cmds.copyAttr(rel_object, temp_rot_root, values=True, attribute=['translateX', 'translateY', 'translateZ'])
            cmds.parent(unity_cam_transform, temp_rot_root)
            cmds.copyAttr(rel_object, temp_rot_root, values=True, attribute=['rotateX', 'rotateY', 'rotateZ'])
            cmds.parent(unity_cam_transform, world=True)
            cmds.delete(temp_rot_root)
            cmds.parent(unity_cam_transform, import_root)
            cmds.lookThru('perspView', unity_cam)
    return import_root


def find_import_root():
    """_summary_

    Returns:
        _type_: _description_
    """
    imported_cam_root = cmds.ls(CAMERA_WORLD_PREFIX)
    if imported_cam_root:
        imported_cam_root = imported_cam_root[0]
    else:
        imported_cam_root = cmds.ls(CAMERA_WORLD_RELATIVE)
        if imported_cam_root:
            imported_cam_root = imported_cam_root[0]
    return imported_cam_root


def find_unilty_camera_transform():
    """
    Returns:
        _type_: _description_
    """
    imported_cam_root = find_import_root()
    children = cmds.listRelatives(imported_cam_root, children=True)
    if children:
        for child in children:
            descendents = cmds.listRelatives(child, ad=True)
            if descendents:
                for des in descendents:
                    if cmds.nodeType(des) == 'camera':
                        return child


def find_extra_attr(root_node):
    children = cmds.listRelatives(root_node, ad=True)
    if not children:
        return
    for child in children:
        if child == 'ExtraAttributes':
            return child


def get_screen_resolution(root_node):
    extra_attr = find_extra_attr(root_node)
    if extra_attr:
        scaleX = cmds.getAttr('{0}.scaleX'.format(extra_attr))
        scaleY = cmds.getAttr('{0}.scaleY'.format(extra_attr))
        return (scaleX, scaleY)
    return None


def get_screen_scale(root_node):
    extra_attr = find_extra_attr(root_node)
    if extra_attr:
        scaleZ = cmds.getAttr('{0}.scaleZ'.format(extra_attr))
        return scaleZ
    return None


def set_resolution(width, height):
    pAx = cmds.getAttr("defaultResolution.pixelAspect")
    pAr = cmds.getAttr("defaultResolution.deviceAspectRatio")
    cmds.setAttr("defaultResolution.aspectLock", 0)
    cmds.setAttr("defaultResolution.width", width)
    cmds.setAttr("defaultResolution.height", height)
    cmds.setAttr("defaultResolution.pixelAspect", pAx)
    cmds.setAttr("defaultResolution.deviceAspectRatio", pAr)


def get_camera_node(node):
    if cmds.nodeType(node) == 'camera':
        return node
    children = cmds.listRelatives(node, children=True)
    for child in children:
        return get_camera_node(child)


def load_unity_camera(camera_fbx_path):
    # 以前読み込まれた残骸が残っていないかチェック
    tool_camera_roots = cmds.ls('{}*'.format(UNITY_TOOL_PREFIX))
    if len(tool_camera_roots) > 0:
        user_choice = cmds.confirmDialog(title='Confirm',
                                         message='シーン内に既存の{}カメラがありました\n'.format(UNITY_TOOL_PREFIX) +
                                                 'どのカメラを読み込むか判定できなくなります。\n' +
                                                 '一旦これらを削除しますか?' +
                                                 '\n'.join(tool_camera_roots),
                                                 button=['削除', 'Cancel'],
                                                 defaultButton='削除',
                                                 cancelButton='Cancel',
                                                 dismissString='Cancel')
        if user_choice == 'Cancel':
            return
        cmds.delete(tool_camera_roots)
    if not os.path.exists(camera_fbx_path):
        cmds.warning('指定したファイルが見つかりませんでした: ' + camera_fbx_path)
        return
    prev_undo_state = cmds.undoInfo(q=True, state=True)
    prev_undo_infinity = cmds.undoInfo(q=True, infinity=True)
    prev_undo_length = cmds.undoInfo(q=True, length=True)
    cmds.undoInfo(state=False, infinity=False, length=100)
    cmds.undoInfo(openChunk=True)
    cmds.file(camera_fbx_path, i=True)
    tool_camera_roots = cmds.ls('{}*'.format(UNITY_TOOL_PREFIX))
    if len(tool_camera_roots) == 0:
        cmds.confirmDialog(title='Warning',
                           message='UnityのWizard2/Motion/ExportCameraForMaya でエクスポートしたカメラのfbxを読み込んでください',
                           button=['OK'])
        cmds.undoInfo(closeChunk=True)
        cmds.undo()
        return
    if len(tool_camera_roots) > 1:
        cmds.confirmDialog(title='Warning',
                           message='読み込んでいるfbxが不正です',
                           button=['OK'])
        cmds.undoInfo(closeChunk=True)
        cmds.undo()
        return
    cmds.undoInfo(closeChunk=True)
    cmds.undoInfo(state=prev_undo_state)
    cmds.undoInfo(infinity=prev_undo_infinity)
    cmds.undoInfo(length=prev_undo_length)
    # TODO: WorldかRelativeかの判定を別でする？
    imported_cam_root = cmds.ls(CAMERA_WORLD_PREFIX)
    if imported_cam_root:
        imported_cam_root = imported_cam_root[0]
    else:
        imported_cam_root = cmds.ls(CAMERA_WORLD_RELATIVE)
        if imported_cam_root:
            imported_cam_root = imported_cam_root[0]
    return imported_cam_root


def is_root_relative(imported_root):
    if not imported_root:
        cmds.warning('カメラのRootが見つかりませんでした')
        return
    if imported_root.find(CAMERA_WORLD_RELATIVE) > -1:
        return True
    return False
