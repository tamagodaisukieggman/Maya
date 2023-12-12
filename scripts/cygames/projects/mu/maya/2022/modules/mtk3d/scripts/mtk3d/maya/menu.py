# -*- coding: utf-8 -*-
"""メニュー「 mtk3d 」を追加"""

import maya.cmds as cmds
import maya.mel as mel


class Mtk3dMenu(object):
    # メニュー名
    menu_name = 'mtk3d'

    @classmethod
    def _add_items(cls):
        """mtk3dメニュー"""

        # Common
        cmds.menuItem(l='Common', sm=True, to=True, p=cls.menu_name)

        cmds.menuItem(d=True, dl='File')

        cmds.menuItem(
            l=u'Delivery Model Tool : モデル受け渡しツール',
            ann=u'現在のシーンから別のシーンにモデルを受け渡しするのをサポートするツール。',
            c='maya.mel.eval("fy_deliveryModelTool;")',
        )

        # mustunokami > Develop > Reload Mesnus
        # が2022 では推奨
        # cmds.menuItem(
        #     l=u'Updata InHouse Tools : [ mtk3d ] [ mutsunokami ] ツールを更新',
        #     ann=u'Perforce の最新版を取得し、 [ mtk3d ] [ mutsunokami ] を更新',
        #     c='import mtk3d.maya.update_tools as update_tools;update_tools.main()',
        # )

        cmds.menuItem(d=True, dl='Edit')

        cmds.menuItem(
            l=u'Duplicate Ex : 複製Ex',
            ann=u'選択したオブジェクトを複製します。メッシュコンポーネントを選択時はコンポーネントを複製します。',
            c='maya.mel.eval("fy_duplicateEx;")',
        )

        cmds.menuItem(d=True, dl='Select')

        cmds.menuItem(
            l=u'Select Hard Edges : 選択オブジェクトのハードエッジを選択',
            c='maya.mel.eval("fy_selectHardEdges;")',
        )

        cmds.menuItem(
            l=u'Select UV Boundary Edges : 選択オブジェクトのUV 境界エッジを選択',
            c='maya.mel.eval(\'fy_selectUvBoundaryEdges("select");\')',
        )

        cmds.menuItem(d=True, dl='Transform')

        cmds.menuItem(
            l=u'Step Transform Tool : ステップトランスフォームツール',
            c='maya.mel.eval("fy_stepTransTool;")',
        )

        cmds.menuItem(d=True, dl='Display')
        cmds.menuItem(
            l=u'Grid Controller : グリッドコントローラ',
            c='maya.mel.eval("fy_gridController_UI;")',
        )

        cmds.menuItem(
            l=u'Show/Hide Node : ノード表示/非表示ツール',
            c='maya.mel.eval("mtk_showHideNodeTool_UI;")',
        )

        cmds.menuItem(
            l=u'Display Edge Length : 選択エッジ長・選択2点間距離を計測',
            ann=u'選択したエッジの合計長さ、選択した２頂点間の距離を計測して表示します。',
            c='maya.mel.eval("fy_dispEdgeLength;")',
        )

        cmds.menuItem(
            ob=True,
            c='maya.mel.eval("fy_dispEdgeLengthOption;")',
        )

        cmds.menuItem(d=True, dl='Windows')

        cmds.menuItem(
            l=u'Outliner Ex : アウトライナEx',
            ann=u'複数開くことができるOutliner ウィンドウ。',
            c='maya.mel.eval("fy_outlinerEx_UI;")',
        )

        cmds.menuItem(
            l=u'Outliner Toolkit : アウトライナツールキット',
            c='maya.mel.eval("fy_outlinerToolkit_UI;")',
        )

        cmds.menuItem(
            l=u'Script Editor Toolkit : スクリプトエディタツールキット',
            c='maya.mel.eval("fy_scriptEditorToolkit_UI;")',
        )

        cmds.menuItem(d=True, dl='Edit Mesh')

        cmds.menuItem(
            l=u'Extract Ex : 抽出Ex',
            ann=u'選択したフェースを抽出します。',
            c='maya.mel.eval("fy_polyExtractEx;")',
        )

        cmds.menuItem(d=True, dl='Normals')

        cmds.menuItem(
            l=u'Harden UV Boundary Edges : 選択オブジェクトのUV 境界エッジをハードエッジに',
            c='maya.mel.eval(\'fy_selectUvBoundaryEdges("harden");\')',
        )

        cmds.menuItem(
            ob=True,
            c='maya.mel.eval(\'fy_selectUvBoundaryEdges("option");\')',
        )

        cmds.menuItem(d=True, dl='Materials')

        cmds.menuItem(
            l=u'Material Create and Assign Tool : マテリアル作成・割り当てツール',
            ann=u'規約に沿ったマテリアル名の生成、割り当てをサポートするツール。',
            c='maya.mel.eval("mtk_materialCreateAssignTool;")',
        )

        cmds.menuItem(
            l=u'Assign Checker Map Tool : チェック用テクスチャアサインツール',
            ann=u'UV チェック用テクスチャのアサイン、元に戻すを行うツール。',
            c='maya.mel.eval("fy_assignCheckerMapTool;")',
        )

        cmds.menuItem(d=True, dl='MASH')

        cmds.menuItem(
            l=u'Place On Mesh Tool : メッシュ上に配置ツール',
            ann=u'指定したメッシュ上に、オブジェクトを様々な方法で配置するツール。',
            c='maya.mel.eval("fy_placeOnMeshTool;")',
        )

        cmds.menuItem(
            l=u'Scatter Objects Tool : オブジェクトばらまきツール',
            ann=u'物理シミュレーションでオブジェクトをばらまくツール。',
            c='maya.mel.eval("fy_scatterObjectsTool;")',
        )

        cmds.menuItem(d=True, dl='Tools')

        cmds.menuItem(
            l=u'Node Hierarchy Assistant : ノード階層アシスタント',
            ann=u'ノード階層の作成をサポートするツール。',
            c='maya.mel.eval("mtk_nodeHierarchyAssistant_UI;")',
        )

        cmds.menuItem(
            l=u'Scale Reference Model Import Tool : スケール参照用モデル インポートツール',
            ann=u'各種スケール参照用のモデルをインポートするツール。',
            c='maya.mel.eval("mtk_scaleRefImportTool;")',
        )

        cmds.menuItem(
            l=u'LOD Model Create Tool : LOD モデル作成ツール',
            ann=u'LOD モデルの作成をサポートするツール。',
            c='maya.mel.eval("mtk_instaLodModelCreateTool;")',
        )

        cmds.setParent('..', menu=True)

        # --------------------------------------------------------------------------------------------------------------

        # Character
        cmds.menuItem(l='Character', sm=True, to=True, p=cls.menu_name)
        '''
        cmds.menuItem(
             l='clothToolsUI',
             c='import mtk3d.maya.cfx.clothSetupTool.clothSetupUI as UI;UI.main()',
        )
        '''
        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        # --------------------------------------------------------------------------------------------------------------

        # Environment
        cmds.menuItem(l='Environment', sm=True, to=True, p=cls.menu_name)

        cmds.menuItem(d=True, dl='File')

        cmds.menuItem(
            l=u'Create Asset Folder : アセットフォルダ作成ツール',
            c='maya.mel.eval("fy_createProject;")',
        )

        cmds.menuItem(d=True, dl='Tools')

        cmds.menuItem(
            l=u'Collision Setting Tool : コリジョン・物理マテリアル設定ツール',
            ann=u'コリジョンアトリビュートの自動設定、物理マテリアルの設定サポートを行うツール。',
            c='maya.mel.eval("mtk_collisionSettingTool;")',
        )

        cmds.menuItem(
            l=u'Create Order Form : 発注書作成ツール',
            ann=u'シーン情報を参照し、背景アセットの発注書エクセルファイル作成をサポートするツール。',
            c='maya.mel.eval("mtk_createOrderForm;")',
        )

        cmds.setParent('..', menu=True)

        # --------------------------------------------------------------------------------------------------------------

        # Rigging
        cmds.menuItem(l='Rigging', sm=True, to=True, p=cls.menu_name)
        cmds.menuItem(d=True, dl='Ply')

        cmds.menuItem(
            l='cyRigPicker',
            c='import mtk3d.maya.rig.cyRig.gui as gui;gui.main()',
        )

        cmds.menuItem(
            l='IKFK Match Tool',
            c='from mtk3d.maya.rig.ikfk.ikfkmatch import ui as ikfk_ui;ui = ikfk_ui.UI();ui.show()',
        )

        cmds.menuItem(
            l='Refresh Tool',
            c='import mtk3d.maya.rig.refreshScene.refreshScene as refreshScene;refreshAnim = refreshScene.UI();refreshAnim.show()',
        )

        cmds.menuItem(
            l='Local World Tool',
            c='import mtk3d.maya.rig.localtoworld as localtoworld;ltw = localtoworld.UI();ltw.show()',
        )

        cmds.menuItem(
            l='Prop Space Dialog',
            c='from mtk3d.maya.rig.props import ui as props_ui;ui = props_ui.PropSpaceDialog();ui.show_dialog()',
        )

        cmds.menuItem(
            l='Prevent Overstretching a.k.a NOBIKIRI',
            c='import mtk3d.maya.rig.preventoverstretching.prevent_overstretching as nobikiri;nobikiri.create()',
        )

        cmds.menuItem(d=True, dl='Quadruped')

        cmds.menuItem(
            l='waitPoseMatch',
            c='import mtk3d.maya.rig.weightposematchtool.waitposematch  as UI; UI.main()',
        )

        cmds.menuItem(
            l='ikFkSpaceSwitch',
            c='import mtk3d.maya.rig.ikfkspaceswitch.ikfkspace as UI; UI.main()',
        )

        cmds.menuItem(d=True, dl='Utilities')

        cmds.menuItem(
            l='Instant Ik UI',
            c='import mtk3d.maya.rig.instantikcontroller.instant_ik_controller as instant_ik; instant_ik.create()',
        )

        cmds.menuItem(
            l='cyPoseStoreUI',
            c='import mtk3d.maya.rig.cyPoseStore.ui as UI;UI.ui()',
        )

        cmds.menuItem(
            l='cyShakeMakeUI',
            c='import mtk3d.maya.rig.cyShakeMake.ui.makeShakeUI as UI;UI.main()',
        )

        cmds.menuItem(d=True, dl='Skin')

        cmds.menuItem(
            l='Rename SkinCluster',
            c='import mtk3d.maya.rig.renameskincluster.main as main; main.rename_skin_cluster()',
        )

        cmds.menuItem(
            l='Reset SkinCluster',
            c='import mtk3d.maya.rig.resetskincluster.main as main; main.reset_skin_cluster()',
        )

        cmds.menuItem(d=True, dl='Skelton')
        cmds.menuItem(
            l='Comet Joint Orient',
            c='maya.mel.eval("cometJointOrient;")',
        )

        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        # ---------------------------------------------------------------------------

        # Animation
        cmds.menuItem(l='Animation', sm=True, to=True, p=cls.menu_name)

        cmds.menuItem(
            l='AnimatorTools',
            c='import mtk3d.maya.anim.animatortools.animatortools as ant;ant.createUI()',
        )

        cmds.menuItem(
            l='Anim School Picker',
            c='import maya.cmds as cmds;import maya.mel as mel;cmds.loadPlugin("Z:/mtk/tools/maya/modules/animschool_picker/plug-ins/AnimSchoolPicker.mll",qt=True);mel.eval("AnimSchoolPicker();")',
        )

        cmds.menuItem(
            l='TimeEditorTools',
            c='import mtk3d.maya.anim.timeeditortools.timeeditortools as tet;tet.createUI()',
        )

        cmds.menuItem(
            l='intAttack',
            c='import mtk3d.maya.anim.intattack.intattack as intattack;intattack.execute()',
        )

        cmds.menuItem(
            l=u'KeyframeReduction : アニメーションのキーフレームリダクションツール',
            c='import keyframeReduction.ui;keyframeReduction.ui.show()',
        )

        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        # ---------------------------------------------------------------------------

        # CharacterFX
        cmds.menuItem(l='Character FX', sm=True, to=True, p=cls.menu_name)
        cmds.menuItem(
            l='cfxToolsUI',
            c='import mtk3d.maya.cfx.cfxTools.cfxToolsUI as UI;UI.main()',
            i='menuIconNCloth.png'
        )
        cmds.menuItem(d=True, dl='Cloth')
        cmds.menuItem(d=True, dl='Hair')
        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        # ---------------------------------------------------------------------------

        # FX
        cmds.menuItem(l='FX', sm=True, to=True, p=cls.menu_name)
        '''
        cmds.menuItem(
             l='clothToolsUI',
             c='import mtk3d.maya.cfx.clothSetupTool.clothSetupUI as UI;UI.main()',
        )
        '''
        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)

        # ---------------------------------------------------------------------------

    @classmethod
    def main(cls):
        """メニュー「 mtk3d 」を追加"""

        g_main_window = mel.eval('$temp=$gMainWindow')

        if cmds.menu(cls.menu_name, q=True, ex=True):
            cls.menu = cmds.menu(cls.menu_name, e=True, dai=True, to=True)
        else:
            cls.menu = cmds.menu(
                cls.menu_name, l=cls.menu_name, p=g_main_window, to=True)

        # メニュー追加
        cls._add_items()
