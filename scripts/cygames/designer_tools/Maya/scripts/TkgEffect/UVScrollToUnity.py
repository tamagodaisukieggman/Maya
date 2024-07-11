#-*- encoding: utf-8

import maya.cmds as cmds
from maya import OpenMaya as om

#Python3対応
try:
    import _winreg as winreg
except ImportError:
    import winreg

toolName = "UVScrollToUnity"
scriptPrefix = toolName + "."

#=============================================================================================
# 変数
#=============================================================================================
start = 0     #スタートフレーム
end = 30     #エンドフレーム
u_start = 0     #Uのスタート値
u_end = 1       #Uのエンド値
v_start = 0     #Uのスタート値
v_end = 1       #Uのエンド値
su_start = 1    #スケールUのスタート値
su_end = 1      #スケールUのエンド値
sv_start = 1    #スケールUのスタート値
sv_end = 1      #スケールUのエンド値
poly_num = 200       #ポリゴン数
mesh_name = "_temp_UVScroll"

#=============================================================================================
# オブジェクトからマテリアル取得
#=============================================================================================
def _GetMaterialsFromObj(objList):
    cmds.select(objList, replace=True )
    cmds.hyperShade(smn=True)
    matList = cmds.ls(sl=True, mat=True)

    return matList

#=============================================================================================
# place2dTextureにエクスプレッションを作成する
#=============================================================================================
def _CreateExp():    

    selObjs = cmds.ls(sl=True, transforms=True)   #選択オブジェクト 
    selMats = cmds.ls(sl=True, materials=True)    #マテリアル
    selMat = []

    #ロケーターの名前　ベイクさせるかで分ける
    if cmds.checkBoxGrp('c_box', q=True, v1=True):
        UV_Locator_name = "_eff_UVlocator_bake"
    else:
        UV_Locator_name = "_eff_UVlocator"



    if len(selObjs) > 0:
        selMats = _GetMaterialsFromObj(selObjs)

    if len(selMats) > 0:
        selMat = selMats[0]

    if len(selMat) == 0:
        cmds.warning(u"メッシュかマテリアルを選択してください")
        return

    else:
        nodeList1 = cmds.listConnections(selMat, destination=True, plugs=True)  #ノードに接続されたアトリビュート名

        print(nodeList1)

        exp_1 = 0 
        exp_2 = 0
        
        for connectNode1 in nodeList1:
            if not "outColor" in connectNode1: #nodeList1からoutColorノードを探す
                continue
                
            else:
                #outColorからfileNodeを見つける　
                fileNode = connectNode1[0 : connectNode1.rfind("outColor")-1]   #file1.outColor
                print(fileNode)


                nodeList2 = cmds.listConnections(fileNode, connections=True, plugs=True)    #fileノードの前後のアトリビュート名を取得
                print(nodeList2)

                exp_1 = 1

                for connectNode2 in nodeList2:
                    if not "outUV" in connectNode2: #nodeList2からoutUVノードを探す
                        continue
                    else:
                        #outUVからplace2dTextureNodeを見つける
                        place2dTextureNode = connectNode2[0 : connectNode2.rfind("outUV")-1]    #place2dTexture1.outUV

                        # すでにUVアニメーションがあったら削除しておく
                        if len(place2dTextureNode) != 0:
                            place2dTex_Anim = cmds.listConnections(place2dTextureNode, type="animCurve")
                            if place2dTex_Anim != None:
                                print(u"すでにUVアニメーションがあったので上書きして更新しました")
                                cmds.delete(place2dTex_Anim)
                                
                        #ロケーターモデル
                        locater_UVNodes = cmds.ls(UV_Locator_name, transforms=True) 

                        #すでにロケーターUVアニメーションがあったら削除しておく
                        if len(locater_UVNodes) != 0:
                            locater_UVAnim = cmds.listConnections(locater_UVNodes[0], type="animCurve")  
                            if locater_UVAnim != None:   
                                print(u"すでにロケーターUVアニメーションがあったので上書きして更新しました")
                                cmds.delete(locater_UVAnim)
                                

                        # _animノードがすでにあった場合削除しておく
                        animGruopNodes = cmds.ls("%s_anim*" %selMat, transforms=True)
                        
                        if len(animGruopNodes) != 0:
                            print(u"すでに_anim ノードがあったので上書きして更新しました")
                            cmds.delete(animGruopNodes)


                        #ロケーターがある場合一旦削除
                        if len(locater_UVNodes) != 0:
                            print(u"すでにロケーターモデルがあったので削除しました")
                            cmds.delete(locater_UVNodes[0])

                        #ロケーターを新たに作成
                        locater_UVanim  = cmds.spaceLocator(name = UV_Locator_name, position=[0, 0, 0])[0]    

                        #エクスプレッションがすでにあったら作成する前に削除しておく
                        expressionList = cmds.ls(type='expression')
                        if "UV_exp_%s"%selMat in expressionList:
                            cmds.delete("UV_exp_%s"%selMat)


                        #エクスプレッション作成
                        cmds.expression(name = "UV_exp_%s"%selMat,
                                        ae = 0,
                                        string =
                                        """
                                            %(p2T)s.offsetU = %(trs_uv)s.translateX; \n
                                            %(p2T)s.offsetV = %(trs_uv)s.translateY; \n
                                            %(p2T)s.repeatU = %(trs_uv)s.scaleX; \n
                                            %(p2T)s.repeatV = %(trs_uv)s.scaleY; \n
                                        """
                                        %{ "p2T" : place2dTextureNode, "trs_uv" : locater_UVanim}
                                        )

                        exp_2 = 1

                break # outUVノードを見つけたらループを抜ける

       
    if(exp_1 == 0):
        cmds.warning(u"マテリアルにカラーがありません")

    if(exp_2 == 0):
        cmds.warning(u"マテリアルにUVがありません")


    
    #TangentType
    Tangent = cmds.optionMenuGrp( "Menu_01" , q=True , v=True )
    print(Tangent)
    
    if(Tangent == "spline"):
        inTangentType = "spline"
        outTangentType = "spline"
    if(Tangent == "linear"):
        inTangentType = "linear"
        outTangentType = "linear"
    if(Tangent == "fast"):
        inTangentType = "fast"
        outTangentType = "fast"
    if(Tangent == "slow"):
        inTangentType = "slow"
        outTangentType = "slow"
    if(Tangent == "flat"):
        inTangentType = "flat"
        outTangentType = "flat"
    if(Tangent == "step"):
        inTangentType = "step"
        outTangentType = "step"
    if(Tangent == "clamped"):
        inTangentType = "clamped"
        outTangentType = "clamped"


    #ロケーターにUVスクロール用のキーを打つ
    start = cmds.intFieldGrp('f_range',q=True,v1=True)
    end = cmds.intFieldGrp('f_range',q=True,v2=True)

    #Offset U
    u_1 = cmds.intFieldGrp('u_value',q=True,v1=True)
    u_2 = cmds.intFieldGrp('u_value',q=True,v2=True)

    cmds.setKeyframe( UV_Locator_name, at ='translateX', v = u_1 ,time = start, itt = inTangentType, ott = outTangentType)
    cmds.setKeyframe( UV_Locator_name, at ='translateX', v = u_2 ,time = end, itt = inTangentType, ott = outTangentType)

    #Offset V
    v_1 = cmds.intFieldGrp('v_value',q=True,v1=True)
    v_2 = cmds.intFieldGrp('v_value',q=True,v2=True)

    cmds.setKeyframe( UV_Locator_name, at ='translateY', v = v_1 ,time = start, itt = inTangentType, ott = outTangentType)
    cmds.setKeyframe( UV_Locator_name, at ='translateY', v = v_2 ,time = end, itt = inTangentType, ott = outTangentType)

    #Scale U
    su_1 = cmds.intFieldGrp('su_value',q=True,v1=True)
    su_2 = cmds.intFieldGrp('su_value',q=True,v2=True)

    cmds.setKeyframe( UV_Locator_name, at ='scaleX', v = su_1 ,time = start, itt = inTangentType, ott = outTangentType)
    cmds.setKeyframe( UV_Locator_name, at ='scaleX', v = su_2 ,time = end, itt = inTangentType, ott = outTangentType)

    #Scale V
    sv_1 = cmds.intFieldGrp('sv_value',q=True,v1=True)
    sv_2 = cmds.intFieldGrp('sv_value',q=True,v2=True)

    cmds.setKeyframe( UV_Locator_name, at ='scaleY', v = sv_1 ,time = start, itt = inTangentType, ott = outTangentType)
    cmds.setKeyframe( UV_Locator_name, at ='scaleY', v = sv_2 ,time = end, itt = inTangentType, ott = outTangentType)


#=============================================================================================
# アニメーションのベイク
#=============================================================================================
def _BakeAnimation():
    locator = cmds.ls(sl = True)
    cmds.bakeResults( locator ,  at=["tx","ty","sx", "sy"] )



#=============================================================================================
# FBX Export
#=============================================================================================
def _FBXExport():
    obj = cmds.ls(sl =True)

    if not obj:
        print(u"選択オブジェクトがありません")
        return   


    #ロケーターの名前　ベイクさせるかで分ける
    if cmds.checkBoxGrp('c_box', q=True, v1=True):
        _BakeAnimation()
    

    po_num = cmds.intFieldGrp('poly_num',q=True, value1=True)

    sn = []


    #objectがNurbsSurfaceか判定
    for i in range(len(obj)):
        sn = cmds.listRelatives(obj[i], s = True)  #Shapeノードを取得

        if cmds.objectType( sn ) == "nurbsSurface" :
            print(u"サーフェスです")
            cmds.nurbsToPoly( obj , f = 0, pc = po_num )    #NurbsSurfaceをPolygonMeshに変換
        else:
            print(u"ポリゴンメッシュです")
    

    #Unityのパスを指定
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Unity Technologies\Unity Editor 5.x')
    regInfo = winreg.QueryInfoKey(key)

    result = []

    for i in range(regInfo[1]):
        v = winreg.EnumValue(key, i)

        if 'RecentlyUsedProjectPaths-' in v[0]:
            result.append(v[1][:-1]) # 最後の文字がx00なので除外


    if len(result) == 0:
        return


    #エクスポート
    unicode_string = result[0].decode('utf-8') #Python3用に変換
    new_path = unicode_string + ("/Assets/")  + obj[0]
   

    print(new_path)

    #FBX出力
    om.MGlobal.executeCommand('FBXExport("-f", "{}", "-s")'.format(new_path))
    

#=============================================================================================
# GUIの作成
#=============================================================================================
cmds.window(t = 'UVScrollToUnity' )

cmds.columnLayout()

#----------------------------------------------------
# UVのエクスプレッションを適応する
#----------------------------------------------------
cmds.frameLayout( label=u" UVスクロール用ロケーター作成" , w = 200, bv =True, cl = False, cll = True)


#フレームレンジ
cmds.intFieldGrp('f_range',  l="Frame Range", numberOfFields=2, v1 = start , v2 = end ,  cw3=[80,50,50])

#オフセット　U値
cmds.intFieldGrp('u_value',  l="Offset U", numberOfFields=2, v1 = u_start , v2 = u_end ,  cw3=[80,50,50])

#オフセット　V値
cmds.intFieldGrp('v_value',  l="Offset V", numberOfFields=2, v1 = v_start , v2 = v_end ,  cw3=[80,50,50])

#スケール　U値
cmds.intFieldGrp('su_value',  l="Scale U", numberOfFields=2, v1 = su_start , v2 = su_end ,  cw3=[80,50,50])

#スケール　V値
cmds.intFieldGrp('sv_value',  l="Scale V", numberOfFields=2, v1 = sv_start , v2 = sv_end ,  cw3=[80,50,50])


#接線
Menu_01 = cmds.optionMenuGrp( "Menu_01", label='Tangent', cw2=[80,50])
cmds.menuItem("_spline", parent=(Menu_01 +'|OptionMenu'),  label=u"spline" )
cmds.menuItem("_linear", parent=(Menu_01 +'|OptionMenu'), label=u"linear")
cmds.menuItem("_fast", parent=(Menu_01 +'|OptionMenu'),   label=u"fast")
cmds.menuItem("_slow", parent=(Menu_01 +'|OptionMenu'),   label=u"slow")
cmds.menuItem("_flat", parent=(Menu_01 +'|OptionMenu'),   label=u"flat")
cmds.menuItem("_step", parent=(Menu_01 +'|OptionMenu'),   label=u"step")
cmds.menuItem("_clamped", parent=(Menu_01 +'|OptionMenu'),   label=u"clamped")


#ベイクするか
checkBox1 = cmds.checkBoxGrp('c_box', label=u'キーをベイクする',  v1 = True,  cw2=[85,50])

#実行
cmds.button( l=u'CreateExpLocator', command= scriptPrefix+'_CreateExp()' , w = 200, bgc=(0.7968, 0.5, 0.5))




cmds.setParent('..')



#----------------------------------------------------
# Unityへエクスポート
#----------------------------------------------------
cmds.frameLayout( label=u" Unityへエクスポート" , w = 200, bv =True, cl = False, cll = True)

#ポリゴン数
cmds.intFieldGrp('poly_num', l=u"ポリゴン数", v1 = poly_num ,  cw2=[70,50])

#FBXExpoart
cmds.button(label='FBX Export', command= scriptPrefix+'_FBXExport()' , w = 200 , bgc=(0.7968, 0.5, 0.5))


cmds.setParent('..')


#----------------------------------------------------
cmds.setParent( '..' )


def UI():
    cmds.showWindow()
