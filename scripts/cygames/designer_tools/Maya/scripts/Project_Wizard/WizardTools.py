# -*- coding: utf-8 -*-

"""
Wizard用ツール群

"""

toolName = "WizardTools"
__author__ = "Cygames, Inc. Yuta Kimura"

import pymel.core as pm


#-------------------------------------------------
#メイン
def main():
    #メインウィンドウオブジェクトの生成
    toolWindow = MainWindow()
    return


#-------------------------------------------------
#メインウィンドウクラス
class MainWindow(object):
    def __init__(self):
        #既にウィンドウが開いている場合は閉じる
        if pm.window(toolName, q=1, exists=1):
            pm.deleteUI(toolName)

        #UIの定義
        self.window = pm.window(toolName, title=u"Wizardツール", minimizeButton=0, maximizeButton=0, sizeable=1)
        with self.window:
            self.columnLayout_top = pm.columnLayout("columnLayout_top", columnOffset=("left", 5))
            with self.columnLayout_top:
                pm.separator("separator_space0", w=1, h=5, style="none")

                #モデルエクスポーター
                self.frameLayout_modelExport = pm.frameLayout(label=u"モデルエクスポート", borderStyle="etchedIn", font="plainLabelFont", marginWidth=7, marginHeight=5)
                with self.frameLayout_modelExport:
                    self.rowLayout_modelExport = pm.rowLayout("rowLayout_modelExport", numberOfColumns=4)
                    with self.rowLayout_modelExport:
                        #Unity用モデルをエクスポート
                        self.button_exportModel = pm.button("button_exportModel", w=100, h=20, label=u"Unity用モデル", bgc=[1,1,1], command="import CyExportModel;reload(CyExportModel);CyExportModel.main('fbx')")

                        #xNormal用モデルをエクスポート
                        self.button_exportXnModel = pm.button("button_exportXnModel", w=100, h=20, label=u"xNormal用モデル", bgc=[1,1,1], command="import CyExportXnModel;reload(CyExportXnModel);CyExportXnModel.export()")

                pm.separator("separator_space1", w=1, h=10, style="none")

                #テクスチャベイク
                self.frameLayout_textureBake = pm.frameLayout(label=u"テクスチャベイク", borderStyle="etchedIn", font="plainLabelFont", marginWidth=7, marginHeight=5)
                with self.frameLayout_textureBake:
                    self.columnLayout_textureBake = pm.columnLayout("columnLayout_textureBake", columnOffset=("left", 5))
                    with self.columnLayout_textureBake:
#                       self.rowLayout_textureBakeSetName = pm.rowLayout("rowLayout_textureBakeSetName", numberOfColumns=2)
#                       with self.rowLayout_textureBakeSetName:
                            #textureBakeSet名
#                           self.text_textureBakeSetName = pm.text("text_textureBakeSetName", label=u"textureBakeSet名 : ", font="boldLabelFont", width=110)

#                           self.textField_textureBakeSetName = pm.textField("textField_textureBakeSetName", text="", width=200,
#                                                                    changeCommand=pm.Callback(self.textField_onChange, self),
#                                                                    enterCommand=pm.Callback(self.textField_onChange, self))

                        pm.separator("separator_space2", w=1, h=5, style="none")

                        self.rowLayout_textureBake = pm.rowLayout("rowLayout_textureBake", numberOfColumns=7)
                        with self.rowLayout_textureBake:
                            #切り替え
                            with pm.columnLayout("columnLayout_changeRenderLayer", rowSpacing=2):
                                self.button_changeSetting_light     = pm.button("button_changeSetting_light", w=50, h=20, label=u"Light", bgc=[0.8,0.6,0.6], command="import WizardChangeTextureBakeSetting;reload(WizardChangeTextureBakeSetting);WizardChangeTextureBakeSetting.change('light',0,0)")
                                self.button_changeSetting_light2    = pm.button("button_changeSetting_light2", w=50, h=20, label=u"Light2", bgc=[0.8,0.6,0.6], command="import WizardChangeTextureBakeSetting;reload(WizardChangeTextureBakeSetting);WizardChangeTextureBakeSetting.change('light',0,0,0,1)")

                                self.button_changeSetting_shadow    = pm.button("button_changeSetting_shadow", w=50, h=20, label=u"Shadow", bgc=[0.6,0.8,0.6], command="import WizardChangeTextureBakeSetting;reload(WizardChangeTextureBakeSetting);WizardChangeTextureBakeSetting.change('shadow',0,0)")
                                self.button_changeSetting_gi        = pm.button("button_changeSetting_gi", w=50, h=20, label=u"GI", bgc=[0.6,0.8,0.9], command="import WizardChangeTextureBakeSetting;reload(WizardChangeTextureBakeSetting);WizardChangeTextureBakeSetting.change('gi',0,0,1,0)")
                                self.button_changeSetting_ao        = pm.button("button_changeSetting_ao", w=50, h=20, label=u"AO", bgc=[0.5,0.5,0.5], command="import WizardChangeTextureBakeSetting;reload(WizardChangeTextureBakeSetting);WizardChangeTextureBakeSetting.change('ao',0,0)")
                                self.button_changeSetting_ao2       = pm.button("button_changeSetting_ao2", w=50, h=20, label=u"AO2", bgc=[0.5,0.5,0.5], command="import WizardChangeTextureBakeSetting;reload(WizardChangeTextureBakeSetting);WizardChangeTextureBakeSetting.change('ao',0,0,0,1)")
                                self.button_changeSetting_specular  = pm.button("button_changeSetting_specular", w=50, h=20, label=u"Specular", bgc=[0.8,0.8,0.5], command="import WizardChangeTextureBakeSetting;reload(WizardChangeTextureBakeSetting);WizardChangeTextureBakeSetting.change('specular',0,0)")

                            pm.separator("separator_space3", w=1, h=5, style="none")

                            #512ベイク
                            with pm.columnLayout("columnLayout_bake512", rowSpacing=2):
                                self.button_bake512_light       = pm.button("button_bake512_light", w=60, h=20, label=u"512 px", bgc=[0.8,0.6,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['light'],512,512)")
                                self.button_bake512_light2      = pm.button("button_bake512_light2", w=60, h=20, label=u"512 px", bgc=[0.8,0.6,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['light'],512,512,0,1)")

                                self.button_bake512_shadow      = pm.button("button_bake512_shadow", w=60, h=20, label=u"512 px", bgc=[0.6,0.8,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['shadow'],512,512)")
                                self.button_bake512_gi          = pm.button("button_bake512_gi", w=60, h=20, label=u"512 px", bgc=[0.6,0.8,0.9], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['gi'],512,512,1,0)")
                                self.button_bake512_ao          = pm.button("button_bake512_ao", w=60, h=20, label=u"512 px", bgc=[0.5,0.5,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['ao'],512,512)")
                                self.button_bake512_ao2         = pm.button("button_bake512_ao2", w=60, h=20, label=u"512 px", bgc=[0.5,0.5,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['ao'],512,512,0,1)")

                                self.button_bake512_specular    = pm.button("button_bake512_specular", w=60, h=20, label=u"512 px", bgc=[0.8,0.8,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['specular'],512,512)")

                            #1024ベイク
                            with pm.columnLayout("columnLayout_bake1024", rowSpacing=2):
                                self.button_bake1024_light      = pm.button("button_bake1024_light", w=60, h=20, label=u"1024 px", bgc=[0.8,0.6,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['light'],1024,1024)")
                                self.button_bake1024_light2     = pm.button("button_bake1024_light2", w=60, h=20, label=u"1024 px", bgc=[0.8,0.6,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['light'],1024,1024,0,1)")

                                self.button_bake1024_shadow     = pm.button("button_bake1024_shadow", w=60, h=20, label=u"1024 px", bgc=[0.6,0.8,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['shadow'],1024,1024)")
                                self.button_bake1024_gi         = pm.button("button_bake1024_gi", w=60, h=20, label=u"1024 px", bgc=[0.6,0.8,0.9], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['gi'],1024,1024,1,0)")
                                self.button_bake1024_ao         = pm.button("button_bake1024_ao", w=60, h=20, label=u"1024 px", bgc=[0.5,0.5,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['ao'],1024,1024)")
                                self.button_bake1024_ao2        = pm.button("button_bake1024_ao2", w=60, h=20, label=u"1024 px", bgc=[0.5,0.5,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['ao'],1024,1024,0,1)")

                                self.button_bake1024_specular   = pm.button("button_bake1024_specular", w=60, h=20, label=u"1024 px", bgc=[0.8,0.8,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['specular'],1024,1024)")

                            #2048ベイク
                            with pm.columnLayout("columnLayout_bake2048", rowSpacing=2):
                                self.button_bake2048_light      = pm.button("button_bake2048_light", w=60, h=20, label=u"2048 px", bgc=[0.8,0.6,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['light'],2048,2048)")
                                self.button_bake2048_light2     = pm.button("button_bake2048_light2", w=60, h=20, label=u"2048 px", bgc=[0.8,0.6,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['light'],2048,2048,0,1)")

                                self.button_bake2048_shadow     = pm.button("button_bake2048_shadow", w=60, h=20, label=u"2048 px", bgc=[0.6,0.8,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['shadow'],2048,2048)")
                                self.button_bake2048_gi         = pm.button("button_bake2048_gi", w=60, h=20, label=u"2048 px", bgc=[0.6,0.8,0.9], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['gi'],2048,2048,1,0)")
                                self.button_bake2048_ao         = pm.button("button_bake2048_ao", w=60, h=20, label=u"2048 px", bgc=[0.5,0.5,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['ao'],2048,2048)")
                                self.button_bake2048_ao2        = pm.button("button_bake2048_ao2", w=60, h=20, label=u"2048 px", bgc=[0.5,0.5,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['ao'],2048,2048,0,1)")

                                self.button_bake2048_specular   = pm.button("button_bake2048_specular", w=60, h=20, label=u"2048 px", bgc=[0.8,0.8,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['specular'],2048,2048)")

                            #2048ベイク
                            with pm.columnLayout("columnLayout_bakeProduction", rowSpacing=2):
                                self.button_bake4096_light      = pm.button("button_bake4096_light", w=60, h=20, label=u"4096 px", bgc=[0.8,0.6,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['light'],4096,4096)")
                                self.button_bake4096_light2     = pm.button("button_bake4096_light2", w=60, h=20, label=u"4096 px", bgc=[0.8,0.6,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['light'],4096,4096,0,1)")

                                self.button_bake4096_shadow     = pm.button("button_bake4096_shadow", w=60, h=20, label=u"4096 px", bgc=[0.6,0.8,0.6], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['shadow'],4096,4096)")
                                self.button_bake4096_gi         = pm.button("button_bake4096_gi", w=60, h=20, label=u"4096 px", bgc=[0.6,0.8,0.9], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['gi'],4096,4096,1,0)")
                                self.button_bake4096_ao         = pm.button("button_bake4096_ao", w=60, h=20, label=u"4096 px", bgc=[0.5,0.5,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['ao'],4096,4096)")
                                self.button_bake4096_ao2        = pm.button("button_bake4096_ao2", w=60, h=20, label=u"4096 px", bgc=[0.5,0.5,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['ao'],4096,4096,0,1)")

                                self.button_bake4096_specular   = pm.button("button_bake4096_specular", w=60, h=20, label=u"4096 px", bgc=[0.8,0.8,0.5], command="import WizardBakeTexture;reload(WizardBakeTexture);WizardBakeTexture.bake(['specular'],4096,4096)")

                pm.separator("separator_space6", w=1, h=10, style="none")

                #その他ツール
                self.frameLayout_toos = pm.frameLayout(label=u"その他ツール", borderStyle="etchedIn", font="plainLabelFont", marginWidth=7, marginHeight=5)
                with self.frameLayout_toos:
                    self.rowLayout_toos = pm.rowLayout("rowLayout_toos", numberOfColumns=4)
                    with self.rowLayout_toos:
                        buttonWidth = 60

                        #相対移動ツール
                        self.button_relativeTransform = pm.button("button_relativeTransform", w=buttonWidth, h=20, label=u"相対移動", bgc=[1,1,1], command="import CyRelativeTransformTool;reload(CyRelativeTransformTool);CyRelativeTransformTool.main()")

                        #整列ツール
                        self.button_align = pm.button("button_align", w=buttonWidth, h=20, label=u"整列", bgc=[1,1,1], command="import CyAlignTool;reload(CyAlignTool);CyAlignTool.main()")

                        #UV編集
                        self.button_editUV = pm.button("button_editUV", w=buttonWidth, h=20, label=u"UV編集", bgc=[1,1,1], command="import CyUVAdjuster;reload(CyUVAdjuster);CyUVAdjuster.main()")

                        #ミラーコピー
                        self.button_mirrorCopy = pm.button("button_mirrorCopy", w=buttonWidth, h=20, label=u"鏡面複製", bgc=[1,1,1], command="import CyMirrorCopy;reload(CyMirrorCopy);CyMirrorCopy.main()")

        #ウィンドウのサイズ変更
        winWidthValue = 350
        winHeightValue = 325
        if pm.util.getEnv("MAYA_UI_LANGUAGE") == "ja":
            winHeightValue = winHeightValue
        self.window.setWidthHeight([winWidthValue, winHeightValue])

        #ウィンドウを開く
        pm.showWindow(self.window)

        return

    ##########################
    #テキストフィールドの値が変更された時に発生
    def textField_onChange(self):
        inputtedFolderPath = self.textField_textureBakeSetName.getText()

        return


#-------------------------------------------------
if __name__ == "__main__":
    main()
