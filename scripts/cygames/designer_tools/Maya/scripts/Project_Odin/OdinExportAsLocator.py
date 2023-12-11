# -*- coding: utf-8 -*-

# OdinExportAsLocator.py

toolName = "OdinExportAsLocator"
__author__ = "Natsuko Kinoshita"

"""
選択しているオブジェクトをTransform情報を持ったロケーターとしてfbxエクスポートします。
Odinの背景のSpriteアニメーション用です。

【背景】Odinの背景制作過程ではMaya上でアニメーションカーブのSpriteアニメーションを目視確認しています。
しかしアニメーションカーブでは表示が崩れるため、Unity上でSpriteアニメーションを置き換える必要があります。
Maya上で確認済みのSpriteアニメーションのメッシュを選択し、位置情報をLocatorとしてfbxエクスポートします。
Redmine チケット#480547

CyMultiExporterUI のUIの作りを参考にしています。
"""
import maya.cmds as cmds
import pymel.core as pm
import os

def UI():
    MainWindow()

##################################################
#メインウィンドウクラス
class MainWindow(object):
    def __init__(self):
        self.type = "window"
        self.fbxSavePath = ""

        #maya設定フォルダのパス
        userAppDirPath = pm.internalVar(userAppDir=1)

        #ツール設定のパス
        self.configFolderPath = userAppDirPath + "Cygames/" + toolName
        self.configFilePath = self.configFolderPath + "/" + toolName + ".ini"

        #既にウィンドウが開いている場合は閉じる
        if pm.window(toolName, q=1, exists=1):
            pm.deleteUI(toolName)

        self.nodeLines = []

        #UIの定義
        self.window = pm.window(toolName, title=toolName, minimizeButton=0, maximizeButton=0, sizeable=1, resizeToFitChildren=1)
        with self.window:
            #フォームレイアウト
            self.formLayout_main = pm.formLayout(numberOfDivisions=100)
            with self.formLayout_main:
                #フレームレイアウト(上部)
                self.frameLayout_header = pm.frameLayout(borderVisible=0, marginWidth=5, marginHeight=5, labelVisible=0, width=500)
                with self.frameLayout_header:
                    cmds.text(u"このツールは選択中のオブジェクトの位置と回転をlocatorとしてfbxエクスポートします。", align="left")
                    with pm.rowLayout(numberOfColumns=2, columnWidth2=(440, 60), adjustableColumn=2, columnAttach=[(1, 'both', 0), (2, 'right', 0)], width=500):
                        self.keepLocators = False # デフォルトでは作業後ロケータを消す
                        chk_keepLocators = cmds.checkBox(label=u"ロケータをシーン内に残す", value=self.keepLocators, align="left", changeCommand=(self.keepLocators_onChange))
                        #「ヘルプ」ボタン
                        self.button_help = pm.button(width=40, height=20, label=u"ヘルプ", align="right", command=pm.Callback(self.helpButton_onClick))

        #フレームレイアウト(ノードリスト)
        self.frameLayout_ctrl = pm.frameLayout(bgc=[0.2,0.4,0.3], borderVisible=1, borderStyle="etchedIn", marginWidth=5, marginHeight=5, labelVisible=0, label="")
        with self.frameLayout_ctrl:
            with pm.rowLayout(numberOfColumns=3, adjustableColumn=2, width=500):
                cmds.text(label=u"FBXの出力先")
                fbxExportPath = cmds.textField()

                self.button_refreshNodeList = pm.button(bgc=[0.6, 0.6, 0.6], width=120, height=20, label=u"FBXエクスポート",
                                                        command=pm.Callback(self.fbxExportButton_onClick))
                self.fbxSavePath = cmds.file(q=True, sn=True)
                # FBXの名前はMayaシーン名 + _OdinExportAsLocator.fbx。　何のデータか後で分かりやすくする為。
                self.fbxSavePath = self.fbxSavePath[0:self.fbxSavePath.rfind(".")] + "_OdinExportAsLocator.fbx" # .ma or .mb と同じ名前の .fbx がデフォルト
                cmds.textField(fbxExportPath, edit=True, changeCommand=(self.updateFbxExportPath), text=self.fbxSavePath) # enterCommand?

        afValue = []
        afValue.append((self.frameLayout_header, "top", 2))
        afValue.append((self.frameLayout_header, "right", 10))
        afValue.append((self.frameLayout_header, "left", 10))
        acValue = []
        acValue.append((self.frameLayout_ctrl, "top", 0, self.frameLayout_header))

        anValue = []
        pm.formLayout(self.formLayout_main, e=1, attachForm=afValue, attachControl=acValue, attachNone=anValue)

    """
    「ヘルプ」ボタンクリック時
    ヘルプのwikiページを開く
    """
    def helpButton_onClick(self):
        cmds.showHelp("https://sannen.cygames.jp/redmine/projects/odin/wiki/TA_Maya_CyExtraAnimation", absolute=1)
        return

    def keepLocators_onChange(self, checkState):
        self.keepLocators = checkState
        return

    """
    「FBXエクスポート」ボタンクリック時
    """
    def fbxExportButton_onClick(self):
        fbxSavePathCheck = self.checkFbxPath()
        if fbxSavePathCheck == False:
            return

        locGroup = self.createTransformLocators()

        if locGroup == None:
            cmds.warning(u"エクスポートはキャンセルされました。")
            return
        cmds.select(locGroup, hi=True)
        # エクスポートFBX
        try:
            cmds.file(self.fbxSavePath, force=True, options="v=0", typ="FBX export", pr=False, es=True)
        except ex:
            cmds.confirmDialog(title="Error", message=u"FBXエクスポート中にエラーが起きました。", button=["OK"])
        finally:
            cmds.confirmDialog(title="Finished!", message=u"ロケータのFBXをエクスポートしました。\n" + self.fbxSavePath, button=["OK"])
        # FBXエクスポート後のロケータを削除
        if self.keepLocators == False:
            cmds.delete(locGroup)

    """
    FBXのエクスポートパスのテキストフィールドが更新された時に呼ばれる。
    エクスポートパスを更新する
    """
    def updateFbxExportPath(self, fieldText):
        self.fbxSavePath = fieldText

    """
    FBXのパスをチェックする。　パスがなければ新規作成するかどうかUserに聞いて作る。
    """
    def checkFbxPath(self):
        if self.fbxSavePath.rfind(".fbx") == -1:
            self.fbxSavePath = self.fbxSavePath + ".fbx"

        dirPath = os.path.dirname(self.fbxSavePath)
        if not os.path.exists(dirPath):
            userChoice = cmds.confirmDialog(title="Confirm", message=u"パスが存在しません。新しく作りますか？", button=["Yes","No"], defaultButton="Yes", cancelButton="No", dismissString="No")
            if userChoice == "Yes":
                os.makedirs(dirPath)
            else:
                return False
        return True

    """
    選択中の「メッシュ」オブジェクトの位置と回転を反映したロケータのグループを作る。
    Memo: Unityでこのロケータの位置と回転を利用してプレハブを置き換えるのに使う。
    @return: 新規で作ったロケータのグループ
    """
    def createTransformLocators(self):
        #selections = cmds.ls(selection=True) # これだとグループノードもロケータになってしまうのでNG
        selections = self.listOnlyMeshFromSelected()# 選択オブジェクトからメッシュのみ選択
        if len(selections) == 0:
            cmds.confirmDialog(title="Confirm", message=u"メッシュを選択してください。", button=["OK"])
            return
        cmds.select(clear=True)

        # できればロケータの名前を元オブジェクトと合わせたかったが、グループを選択している時と子だけを選択している時など対応が難しかったので止めた。
        #for sel in selections:
        #    cmds.select(cmds.duplicate(sel, n=sel.split("|")[-1]+"_copy"), add=True) # 作業用の複製を作成

        cmds.select(cmds.duplicate(selections, rr=True)) # 作業用の複製を作成
        cmds.select(cmds.ls(sl=True), hi=True)
        selections = cmds.ls(sl=True)
        if len(selections) > 0:
            if cmds.listRelatives(selections, p=True) != None: # グループになっていたら
                selections = cmds.parent(selections, w=True) # ノードに入れ子になっている回転や位置情報をなくす為グループ解除
        else:
            cmds.confirmDialog(title="Confirm", message=u"何も選択されていません。", button=["OK"])
            return

        cmds.select(clear=True)
        if cmds.objExists("OdinExportAsLocator_OKtoDelete"): # シーン内に残っていたとき何かわかるような名前にしてます。
            userChoice = cmds.confirmDialog(title="Confirm", message=u"エクスポート用のlocGroupは既に存在します。　上書きしますか？"
                                            , button=["Yes", "No"], defaultButton="Yes", cancelButton="No", dismissString="No")
            if userChoice == "Yes":
                cmds.delete("OdinExportAsLocator_OKtoDelete")
            else:
                return
        locGroup = cmds.group(em=True, name="OdinExportAsLocator_OKtoDelete") # エクスポートするアイテムのグループを作成

        # 選択されたオブジェクトと同じ位置と回転をもったロケータを作成しグループに追加する
        for sel in selections:
            posX = cmds.getAttr(sel + ".translateX")
            posY = cmds.getAttr(sel + ".translateY")
            posZ = cmds.getAttr(sel + ".translateZ")
            rotX = cmds.getAttr(sel + ".rotateX")
            rotY = cmds.getAttr(sel + ".rotateY")
            rotZ = cmds.getAttr(sel + ".rotateZ")
            loc = cmds.spaceLocator(p=(posX, posY, posZ), name=sel, relative=False, absolute=True)
            cmds.parent(loc, "OdinExportAsLocator_OKtoDelete")
            loc = cmds.rename(loc, sel.split("|")[-1]+"_loc")
            cmds.xform(cp=True)  # Center pivots
            if not isinstance(rotX, float):
                cmds.confirmDialog(title="Error", message=u"同じ名前のオブジェクトが2つ以上あるので動作の保証ができません。 中止します。", button=["OK"])
                return
            cmds.xform(r=False, ro=(rotX, rotY, rotZ))
        cmds.delete(selections) # 作業用の複製を削除
        return locGroup

    """
    選択中のオブジェクトからメッシュのみを配列として返します。
    Spriteアニメーションの置換の時はメッシュだけ対象なので。
    """
    def listOnlyMeshFromSelected(self):
        meshes = []
        for o in cmds.ls(selection=True):
            # Error: Problem with the API object returned by __apiobject__ method と出るが大丈夫。
            if pm.listRelatives(o, children=True, s=True) != None:
                for shp in pm.listRelatives(o, children=True, s=True):
                    if pm.nodeType(shp, q=True) == 'mesh':
                        meshes.append(shp)
        return meshes
