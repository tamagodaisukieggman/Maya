# -*- coding: utf-8 -*-
import os
import subprocess
import maya.cmds as cmds
import maya.mel as mel


def main():
    """
    Wizard2モーション班用、下駄対応アニメーション用スクリプト。
    HipジョイントのアニメーションカーブのTransform Yを1.5上にシフトします。
    ほぼ使い捨てツールなので、必要なくなったら削除しても大丈夫です。
    """
    window_name = 'RaiseHipAnimTYWindow'
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    window = cmds.window(window_name, title="モーション下駄対応", iconName='HipTY', width=100, height=50)
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(l='<a href="https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=495120346">help</a>', hl=True, align='left')
    cmds.text(label='キャラの下駄履き対応のモーション班用ツールです。\n' +
                    '選択したフォルダ内の全てのfbx内のHipジョイントのアニメーションカーブのTransform Yを1.5上にシフトします。\n' +
                    '使い捨てツールなので必要なくなったらメニューから外しますのでTAまでご連絡ください。', align='left', wordWrap=True)
    cmds.button(label='一括', annotation='フォルダ選択ダイアログが出ます', command=batch_fbx)
    cmds.text(label='  ')
    cmds.button(label='現在のシーン', annotation='2度押し注意', command=rase_hip_joint_anim_trans_y)
    cmds.showWindow(window)

def rase_hip_joint_anim_trans_y(*arg, show_popup=True):
    '''
    シーン内のHipジョイントのアニメーションカーブのTranslate Yを
    1.5ユニット上にシフトします。
    '''
    if not cmds.file(q=True, sn=True):
        if show_popup:
            cmds.warning('シーンを開いてから実行してください')
        else:
            print('シーン名が取得できませんでした(シーンが開けていない or エラー)')
        return
    try:
        cmds.selectKey('Hip_translateY', r=True, keyframe=True)
        cmds.keyframe(animation='keys', relative=True, at='ty', valueChange=1.5)
        return True
    except Exception:
        pass

def batch_fbx(*arg):
    '''
    下駄を履いたキャラにアニメーションを対応させるため、フォルダ内のfbxシーン内のHipジョイントの
    アニメーションカーブのTranslate Yを一括で1.5ユニット上げて別フォルダに保存します。
    '''
    # フォルダ選択
    selected_folder = cmds.fileDialog2(caption='モデルのfbxが入っているフォルダを選択してください', 
                                       fileMode=3, dialogStyle=2, okCaption='選択')
    if not selected_folder:
        return
    out_folder = cmds.fileDialog2(caption='出力先のフォルダを選択してください（「HipTY1.5」というフォルダを作り出力します）', 
                                       fileMode=3, dialogStyle=2, okCaption='選択')
    if not out_folder:
        return
    selected_folder = selected_folder[0]
    out_folder = out_folder[0] + '/HipTY1.5/'
    fbx_paths = list_all_fbx_files(selected_folder)
    # フォルダを作る
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for fbx_path in fbx_paths:
        cmds.file(fbx_path, f=True, open=True)
        result = rase_hip_joint_anim_trans_y(show_popup=False)
        if result:
            save_path = out_folder + '/' + os.path.basename(fbx_path)
            mel.eval('FBXExport -f "' + save_path + '"')
        else:
            print('Hip_translateYのアニメーションカーブの設定ができなかったのでエクスポートしません: ' + fbx_path)
    subprocess.Popen('explorer "{}"'.format(os.path.normpath(out_folder)))


def list_all_fbx_files(root_path, ignore_words=[]):
    u"""
    root_path配下のすべての.fbxファイルをリストします。
    :param root_path:
    :return: str[]
    """
    fbx_file_paths = []
    if os.path.exists(root_path):
        for dirpath, dirnames, filenames in os.walk(root_path):
            for filename in filenames:
                name, ext = os.path.splitext(filename)
                if ext == '.fbx':
                    maya_scene_path = os.path.join(dirpath, filename).replace("\\", "/")
                    is_ignore = False
                    for ignore_text in ignore_words:
                        ignore_text = ignore_text.strip()
                        if ignore_text:
                            if ignore_text in maya_scene_path:
                                is_ignore = True
                                break
                    if not is_ignore:
                        fbx_file_paths.append(maya_scene_path)
    return fbx_file_paths
