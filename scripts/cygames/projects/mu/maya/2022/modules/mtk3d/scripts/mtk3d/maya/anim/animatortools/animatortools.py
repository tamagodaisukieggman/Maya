# -*- coding: utf-8 -*-
import maya.cmds as cmds

dockObjName = "mtkAnimatorDock" #ウィンドウオブジェクトの識別用
dockName = "mtkAnimatorTools" #ウィンドウの表示タイトル

bth = 28  # 共通のボタンサイズ

#UI作成
def createUI():
    #既にウィンドウが表示されている場合は前回のウィンドウを閉じる
    if cmds.dockControl(dockObjName, exists=True):
        cmds.deleteUI(dockObjName)

    myWindow = cmds.window()

    cmds.scrollLayout('scrollLayout', cr=True, w=250)
    cmds.columnLayout(adj=True)

    cmds.frameLayout(label='General', mw=10, mh=10, cll=True, fn="boldLabelFont", bgc=(0.16, 0.62, 0.70))
    cmds.columnLayout(adj=True, rs=10)
    # General
    cmds.button(l="StudioLibrary", h=bth, ann=u"ポーズライブラリツール", c="import studiolibrary;studiolibrary.main()")
    cmds.button(l="Anim School Picker", h=bth, ann=u"ピッカーツール",c="""
from maya import cmds
from maya import mel
cmds.loadPlugin("Z:/mtk/tools/maya/{}/modules/animschool_picker/plug-ins/AnimSchoolPicker.mll".format(cmds.about(version=True)),qt=True)
mel.eval("AnimSchoolPicker();")
""")
    cmds.button(l="cyRig Picker", h=bth, ann=u"人型用 リグセレクターや拡張機能のメニュー",
                c="import mtk3d.maya.rig.cyRig.gui as gui;import importlib;importlib.reload(gui);gui.main()")
    cmds.button(l="ikFk Space Switch", h=bth, ann=u"4足用 FK/IKベイクツール、スペース切り替え",
                c="import mtk3d.maya.rig.ikfkspaceswitch.ikfkspace as UI; import importlib; importlib.reload(UI);UI.main()")

    cmds.setParent('..')
    cmds.setParent('..')

    cmds.frameLayout(label='Utility', mw=10, mh=10, cll=True, fn="boldLabelFont", bgc=(0.16, 0.62, 0.70))
    cmds.columnLayout(adj=True, rs=10)
    # Utility
    cmds.button(l="bake Animation", h=bth, ann=u"ベースレイヤへ高速アニメーションベイク",
                c="import mtk.animation.bakesimulation as bs;bs.main()")
    cmds.button(l='Local World Tool', h=bth, ann=u"人型用 Local / World 切り替えツール",
                c='import mtk3d.maya.rig.localtoworld as localtoworld;import importlib;importlib.reload(localtoworld);ltw = localtoworld.UI();ltw.show()')
    cmds.button(l='FK/IK Match Tool', h=bth, ann=u"人型用 FKIKマッチツール",
                c='from mtk3d.maya.rig.ikfk.ikfkmatch import ui as ikfk_ui;ui = ikfk_ui.UI();ui.show()')
    cmds.button(l='Prop Space Dialog', h=bth, ann=u"プロップ調整ツール",
                c='from mtk3d.maya.rig.props import ui as props_ui;import importlib;importlib.reload(props_ui);ui = props_ui.PropSpaceDialog();ui.show_dialog()')
    cmds.button(l=u"伸び切り調整ツール", h=bth, ann=u"人型用 腕の伸び切りなどを調整するツール",
                c="import mtk3d.maya.rig.preventoverstretching.prevent_overstretching as nobikiri;nobikiri.create()")
    cmds.button(l="waitPoseMatch", h=bth, ann=u"4足用 待機ポーズとの差分修正ツール",
                c="import mtk3d.maya.rig.weightposematchtool.waitposematch  as UI; import importlib; importlib.reload(UI);UI.main()")
    cmds.button(l=u"らくらくTimeEditor", h=bth, ann=u"タイムエディタクリップ便利ツール",
                c="import mtk3d.maya.anim.timeeditortools.timeeditortools as tet;tet.createUI()")
    cmds.setParent('..')
    cmds.rowLayout(adj=True, numberOfColumns=2)
    cmds.button(l=u"mp4 プレイブラスト", h=bth, ann=u"プレイブラスト動画をmp4で作成",
                c="import mtk.render.ffmpeg_playblast as playblast;playblast.main()")
    cmds.iconTextButton(label=u"設定", ann=u"プレイブラスト設定", h=bth, style="iconAndTextHorizontal", image1="gear.png",
                        c="mel.eval('performPlayblast 4;')")

    cmds.setParent('..')
    cmds.setParent('..')

    cmds.frameLayout(label='Export', mw=10, mh=10, cll=True, fn="boldLabelFont", bgc=(0.16, 0.62, 0.70))
    cmds.columnLayout(adj=True, rs=10)
    # Export
    cmds.button(l="Cyllista Clip Exporter", h=bth, ann=u"Cyllistaアニメーションエクスポートウィンドウ", bgc=(0.71, 0.95, 0.29),
                c="import cyllistaClipWindow;cyllistaClipWindow.show()")
    cmds.button(l=u"FBX Export", h=bth, ann=u"アニメーションをFBXで書き出し",
                c="import mtk3d.maya.anim.animfbxexport.scenefbxexport as sfe; sfe.execute()")

    cmds.setParent('..')
    cmds.setParent('..')

    cmds.frameLayout(label='Generate', mw=10, mh=10, cll=True, fn="boldLabelFont", bgc=(0.16, 0.62, 0.70))
    cmds.columnLayout(adj=True, rs=10)
    # Generate
    cmds.button(l=u"Cyllista Clip Config Setup", h=bth, ann=u"選択したシーンにCyllistaエクスポートのデフォルト設定ファイルを付与する",
                c="import mtk3d.maya.anim.animsendsceneclipsetup.animsendsceneclipsetup as anmcyexpsetup; anmcyexpsetup.main()")
    cmds.button(l=u"Scene Based Conversion", h=bth, ann=u"現在のシーンにSceneBasedConversionを実行する(ply、mob未対応)",
                c="import mtk3d.maya.anim.animscenebasedconversion.animscenebasedconversion as asbc; asbc.execute()")
    cmds.button(l=u"Scene Marge Split", h=bth, ann=u"シーンを結合、分割する",
                c="import mtk3d.maya.anim.animscenemargesplit.animscenemargesplit as asms; import importlib; importlib.reload(asms); asms.main()")
    cmds.button(l=u"ステルスキル データ埋め込み", h=bth, ann=u"プレイヤーのステルスキルモーション事前計算データを埋め込み",
                c="import mtk.animation.impprecalc.main as impprecalc;impprecalc.main()")
    cmds.button(l=u"Animationリグシーン作成", h=bth, ann=u"アニメーター用リグシーン / アニメーター用作業シーン作成ツール ※取り扱い注意",
                c="import mtk3d.maya.anim.animrigscenegenerate.animrigscenegenerate as animrigscene; animrigscene.execute()")

    cmds.setParent('..')
    cmds.setParent('..')

    #dock化する
    allowedAreas = ['right', 'left']
    cmds.dockControl(dockObjName, l=dockName, area='left', content=myWindow, allowedArea=allowedAreas)
