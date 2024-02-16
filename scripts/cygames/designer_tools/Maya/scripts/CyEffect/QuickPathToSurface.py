#-*- encoding: utf-8

import maya.cmds as cmds
from maya import OpenMaya as om
import math

#Python3対応
try:
    import _winreg as winreg
except ImportError:
    import winreg

toolName = "QuickPathToSurface"
scriptPrefix = toolName + "."

#=============================================================================================
# 変数
#=============================================================================================
point_count_1 = 8     #ポイント数 Extrude
point_count_2 = 8     #ポイント数 Loft
poly_num = 200       #ポリゴン数
rot_1 = 360.0   #角度 Extrude
radius_1 = 6.0    #半径 Extrude
height_1 = 10.0   #高さ Extrude
rot_2 = 360.0   #角度 Loft
radius_2 = 6.0    #半径 Loft
height_2 = 10.0   #高さ Loft
mesh_name = "_temp_Poly_mesh"

#=============================================================================================
# パスから面を作る　Extrude
#=============================================================================================
def _CreateExtrudeSurface():
    pn_1 = cmds.intFieldGrp('point_num_1',q=True,value1=True)
    ro_1 = cmds.floatSliderGrp('rot_1',q=True,value=True)
    ra_1 = cmds.floatFieldGrp('radius_1',q=True,value1=True)
    hei_1 = cmds.floatFieldGrp('height_1',q=True,value1=True)

    #Unityスケール
    uni_Size = 1

    if cmds.checkBox(checkBox1, q=True, value=True):
        uni_Size = 100

    #パスカーブの作成
    knot_list_1 = []

    #カーブ１
    for i in range(pn_1):  
        radian = ro_1 *  math.pi /  180.0
        Cir = radian * i /pn_1
        x = (ra_1 * math.sin(Cir))
        y = hei_1 *i / pn_1
        z = (ra_1 * math.cos(Cir))
        pos = ( x *uni_Size, y*uni_Size , z*uni_Size )
        knot_list_1.append(pos)

    path_1 = cmds.curve(p = knot_list_1 )

    #カーブ2
    z1 = (0 , 0, 600 -105) 
    z2 = (0 , 0, 600 -35) 
    z3 = (0 , 0, 600 +35) 
    z4 = (0 , 0, 600 + 105) 
    path_2 = cmds.curve( p =[z1, z2 , z3, z4] )

    #Extrude
    cmds.extrude (path_1, path_2, et = 2, ucp = 1 ,upn =True )
    

#=============================================================================================
# パスから面を作る　Loft
#=============================================================================================
def _CreateLoftSurface():    
    pn_2 = cmds.intFieldGrp('point_num_2',q=True,value1=True)
    ro_2 = cmds.floatSliderGrp('rot_2',q=True,value=True)
    ra_2 = cmds.floatFieldGrp('radius_2',q=True,value1=True)
    hei_2 = cmds.floatFieldGrp('height_2',q=True,value1=True)
    

    #Unityスケール
    uni_Size = 1

    if cmds.checkBox(checkBox3, q=True, value=True):
        uni_Size = 100

    #パスカーブの作成
    knot_list_1 = []
    knot_list_2 = []

    #カーブ１
    for i in range(pn_2):  
        radian = ro_2 *  math.pi /  180.0
        Cir = radian * i /pn_2
        x = ra_2 * math.sin(Cir)
        y = hei_2 *i / pn_2
        z = ra_2 * math.cos(Cir) 
        pos = ( x *uni_Size, y*uni_Size , z*uni_Size )
        knot_list_1.append(pos)

    path_1 = cmds.curve(p = knot_list_1 )

    #カーブ2
    for i in range(pn_2):  
        radian = ro_2 *  math.pi /  180.0
        Cir = radian * i /pn_2
        x = ra_2 * math.sin(Cir)
        y = hei_2 *i / pn_2
        z = ra_2 * math.cos(Cir) 
        pos = ( (x + 1) *uni_Size, (y + 1) *uni_Size , (z + 1)*uni_Size )
        knot_list_2.append(pos)

    path_2 = cmds.curve(p = knot_list_2 )

    #loft
    cmds.loft (path_1, path_2, rsn = True)



#=============================================================================================
# FBX Export
#=============================================================================================
def _FBXExport():
    po_num = cmds.intFieldGrp('poly_num',q=True, value1=True)
    me_name = cmds.textFieldGrp('me_name',q=True, text=True)

    obj = cmds.ls(sl =True)

    if not obj:
        print(u"選択オブジェクトがありません")
        return   

    #objectがNurbsSurfaceか判定
    sn = cmds.listRelatives(obj, s = True)  #Shapeノードを取得

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

    unicode_string = result[0].decode('utf-8') #Python3用に変換
    new_path = unicode_string + ("/Assets/") + (me_name)

    print(new_path)

    #FBX出力
    om.MGlobal.executeCommand('FBXExport("-f", "{}", "-s")'.format(new_path))


#=============================================================================================
# GUIの作成
#=============================================================================================
cmds.window(t = 'QuickPathToSurface' )

cmds.columnLayout()

#----------------------------------------------------
# パスから面を作る（Extrude）
#----------------------------------------------------
cmds.frameLayout( label=u" パスから面を作る（Extrude）" , w = 200,  bv =True, cl = True, cll = True)

#ポイントの数
cmds.intFieldGrp('point_num_1', l=u"ポイント数", v1 = point_count_1 ,  cw2=[70,50])

#半径
cmds.floatFieldGrp('radius_1', l=u"半径", v1 = radius_1 ,  cw2=[70,50])

#高さ
cmds.floatFieldGrp("height_1", l=u"高さ", v1 = height_1 ,  cw2=[70,50])

#角度
cmds.floatSliderGrp("rot_1", l=u"角度", v = rot_1 , w = 120, min = 0.0, max = 1080.0, value = 360.0, step = 1.0 ,field =True, cw3=[70,50,1])

#スケール拡大
checkBox1 = cmds.checkBox(label=u'Unityのスケールに合わせて拡大', v = True)

#ExtrudeSurface
cmds.button(l='CreateExtrudeSurface', command= scriptPrefix+'_CreateExtrudeSurface()', w=200, bgc=(0.7968, 0.5, 0.5))


cmds.setParent('..')


#----------------------------------------------------
# パスから面を作る（Loft）
#----------------------------------------------------
cmds.frameLayout( label=u" パスから面を作る（Loft）" , w = 200 , bv =True, cl = True, cll = True)

#ポイントの数
cmds.intFieldGrp('point_num_2', l=u"ポイント数", v1 = point_count_2 ,  cw2=[70,50])

#半径
cmds.floatFieldGrp('radius_2', l=u"半径", v1 = radius_2 ,  cw2=[70,50])

#高さ
cmds.floatFieldGrp("height_2", l=u"高さ", v1 = height_2 ,  cw2=[70,50])

#角度
cmds.floatSliderGrp("rot_2", l=u"角度", v = rot_2 , w = 120, min = 0.0, max = 1080.0, value = 360.0, step = 1.0 ,field =True, cw3=[70,50,1])

#スケール拡大
checkBox3 = cmds.checkBox(label=u'Unityのスケールに合わせて拡大', v = True)

#LoftSurface
cmds.button(l='CreateLoftSurface', command= scriptPrefix+'_CreateLoftSurface()', w=200, bgc=(0.7968, 0.5, 0.5))


cmds.setParent('..')

#----------------------------------------------------
# Unityへエクスポート
#----------------------------------------------------
cmds.frameLayout( label=u" Unityへエクスポート" , w = 200, bv =True, cl = False, cll = True)

#ポリゴン数
cmds.intFieldGrp('poly_num', l=u"ポリゴン数", v1 = poly_num ,  cw2=[70,50])

#mesh名
cmds.textFieldGrp("me_name", l=u"mesh名", text = mesh_name ,  cw2=[70,100])

#FBXExpoart
cmds.button(label='FBX Export', command= scriptPrefix+'_FBXExport()', w=200, bgc=(0.7968, 0.5, 0.5))


cmds.setParent('..')


#----------------------------------------------------
cmds.setParent( '..' )

def UI():
    cmds.showWindow()
