# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
from importlib import reload
#from mtku.maya.utils.external.studiolibrary import studio_library

dockObjName = "mtkAnimatorDock"
dockName = "mtkAnimatorTools"
btsize = 28

def createUI():

    if cmds.dockControl(dockObjName, exists=True):
        cmds.deleteUI(dockObjName)

    myWindow = cmds.window()
    cmds.scrollLayout( 'scrollLayout', cr=True, w=250)
    cmds.columnLayout( adj=True )
    cmds.frameLayout( label='General', mw=10, mh=10, cll=True, fn="boldLabelFont", bgc=(0.16, 0.62, 0.70))
    cmds.columnLayout( adj=True ,rs=10 )
    #cmds.button(l="cyStudioLibrary", h=btsize, ann= u"ポーズライブラリツール", c=studio_library)
    cmds.button(l="Anim School Picker", h=btsize, ann= u"ピッカーツール", c="import maya.cmds as cmds;import maya.mel as mel;cmds.loadPlugin('Z:/mtk/tools/maya/modules/animschool_picker/plug-ins/AnimSchoolPicker.mll',qt=True);mel.eval('AnimSchoolPicker();')")
    cmds.button(l="cyRig Picker", h=btsize, ann= u"人型用 リグセレクターと拡張機能の提供", c="import mtk3d.maya.rig.cyRig.gui as gui;reload(gui);gui.main()")
    cmds.button(l="ikFk Space Switch", h=btsize, ann= u"4足用 FK/IKベイクツール、スペース切り替え", c="import mtk3d.maya.rig.animUtilTools.ikToFk as UI; reload(UI);UI.main()")
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.frameLayout( label='Utility', mw=10, mh=10, cll=True, fn="boldLabelFont", bgc=(0.16, 0.62, 0.70))
    cmds.columnLayout( adj=True ,rs=10 )
    cmds.button(l="bake Animation", h=btsize, ann= u"ベースレイヤへ高速アニメーションベイク", c="import mtku.maya.menus.animation.bakesimulation as bakesimulation; bakesimulation.main()")
    cmds.button(l='Local World Tool', h=btsize, ann= u"人型用 Local / World 切り替えツール", c='import mtk3d.maya.rig.localtoworld as localtoworld;reload(localtoworld);ltw = localtoworld.UI();ltw.show()')
    cmds.button(l='FK/IK Match Tool', h=btsize, ann= u"人型用 FKIKマッチツール", c='from mtk3d.maya.rig.ikfk.ikfkmatch import ui as ikfk_ui;ui = ikfk_ui.UI();ui.show()')
    cmds.button(l='Prop Space Dialog', h=btsize, ann= u"プロップ調整ツール", c='from mtk3d.maya.rig.props import ui as props_ui;reload(props_ui);ui = props_ui.PropSpaceDialog();ui.show_dialog()')
    cmds.button(l=u"伸び切り調整ツール", h=btsize, ann= u"人型用 腕の伸び切りなどを調整するツール", c="import mtk3d.maya.rig.preventoverstretching.prevent_overstretching as nobikiri;nobikiri.create()")
    cmds.button(l="waitPoseMatch", h=btsize, ann= u"4足用 待機ポーズとの差分修正ツール", c="import mtk3d.maya.rig.animUtilTools.waitPoseMatch  as UI; reload(UI);UI.main()")
    cmds.button(l=u"らくらくTimeEditor", h=btsize, ann= u"タイムエディタクリップ便利ツール", c="import mtk3d.maya.anim.timeeditortools.timeeditortools as tet;tet.createUI()")
    cmds.button(l="cyShake Make UI", h=btsize, ann= u"アニメーションカーブノイズジェネレーター", c="import mtk3d.maya.rig.cyShakeMake.ui.makeShakeUI as UI;UI.main()")
    cmds.setParent( '..' )
    cmds.rowLayout( adj=True ,numberOfColumns=2 )
    cmds.button(l=u"mp4 プレイブラスト", h=btsize, ann=u"プレイブラスト動画をmp4で作成", c="import mtku.maya.menus.rendering.ffmpeg_playblast.app as mp4blast; mp4blast.main()")
    cmds.iconTextButton(label=u"設定", ann=u"プレイブラスト設定", h=btsize, style="iconAndTextHorizontal", image1="gear.png", c="mel.eval('performPlayblast 4;')")
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.frameLayout( label='Export', mw=10, mh=10, cll=True, fn="boldLabelFont", bgc=(0.16, 0.62, 0.70))
    cmds.columnLayout( adj=True ,rs=10 )
    cmds.button(l="Cyllista Clip Exporter", h=btsize, ann= u"Cyllistaアニメーションエクスポートウィンドウ", bgc=(0.71, 0.95, 0.29),c="import cyllistaClipWindow;cyllistaClipWindow.show()")
    cmds.button(l=u"Anim Refresh Scene", h=btsize, ann= u"リリース前のシーンをリフレッシュ", bgc=(1.0, 0.69, 0.08),c="import mtk3d.maya.anim.animrefreshscene.animrefreshScene as aref;aref.main()")
    cmds.button(l=u"FBX Export", h=btsize, ann= u"アニメーションをFBXで書き出し", c="import mtk3d.maya.anim.animfbxexport.scenefbxexport as sfe; sfe.execute()")
    #cmds.button(l="Release Window", h=35, ann= u"Cyllistaリリースウィンドウ", bgc=(0.7, 0.7, 0.7))
    #cmds.button(l="Release Window", h=50, ann= u"Cyllistaリリースウィンドウ", bgc=(0.5, 0.08, 0.07),c="import cyllista.assetoperator as assetoperator;assetoperator.main()")
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.frameLayout( label='Generate', mw=10, mh=10, cll=True, fn="boldLabelFont", bgc=(0.16, 0.62, 0.70))
    cmds.columnLayout( adj=True ,rs=10 )
    cmds.button(l=u"Cyllista Clip Config Setup", h=btsize, ann= u"選択したシーンにCyllistaエクスポートのデフォルト設定ファイルを付与する", c="import mtk3d.maya.anim.animsendsceneclipsetup.animsendsceneclipsetup as anmcyexpsetup; anmcyexpsetup.main()")
    cmds.button(l=u"Scene Based Conversion", h=btsize, ann= u"現在のシーンにSceneBasedConversionを実行する(ply、mob未対応)", c="import mtk3d.maya.anim.animscenebasedconversion.animscenebasedconversion as asbc; asbc.execute()")
    cmds.button(l=u"Scene Marge Split", h=btsize, ann= u"シーンを結合、分割する", c="import mtk3d.maya.anim.animscenemargesplit.animscenemargesplit as asms; reload(asms); asms.main()")
    cmds.button(l=u"ステルスキル データ埋め込み", h=btsize, ann= u"プレイヤーのステルスキルモーション事前計算データを埋め込み", c="import mtku.maya.menus.animation.impprecalc.main as impprecalc;impprecalc.main()")
    cmds.button(l=u"Animationリグシーン作成", h=btsize, ann= u"アニメーター用リグシーン / アニメーター用作業シーン作成ツール ※取り扱い注意",c="import mtk3d.maya.anim.animrigscenegenerate.animrigscenegenerate as animrigscene; animrigscene.execute()")
    cmds.setParent( '..' )
    cmds.setParent( '..' )

    allowedAreas = ['right', 'left']
    cmds.dockControl(dockObjName, l=dockName, area='left', content=myWindow, allowedArea=allowedAreas)

createUI()
