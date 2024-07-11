#-*- encoding: utf-8

import maya.cmds as cmds
import os
from maya import OpenMaya as om

#Python3対応
try:
    import _winreg as winreg
except ImportError:
    import winreg

toolName = "QuickPathAnimation"
scriptPrefix = toolName + "."

#=============================================================================================
# 変数
#=============================================================================================
start_frame = 0     #スタートフレーム
end_frame = 30      #エンドフレーム
span_counts = 2      #スパンの数
point_count = 4


#=============================================================================================
# パスアニメーションの作成
#=============================================================================================
def _CreatePathAnimation():
    st_1 = cmds.intField('start',q=True,value=True)
    st_2 = cmds.intField('end',q=True,value=True)
    st_3 = cmds.intField('point_num',q=True,value=True)

    #Unityスケール
    uni_Size = 1

    if cmds.checkBox(checkBox1, q=True, value=True):
        uni_Size = 100

    #パスカーブの作成
    knot_list = []

    for i in range(st_3):  
        pos = ( (-10 *uni_Size) + (i*5*uni_Size), 0 , 0)
        knot_list.append(pos)

    path = cmds.curve(p = knot_list )
    print(knot_list)


    #オブジェクトの作成
    object = cmds.polySphere(sx = 20, sy = 20)
    cmds.scale( uni_Size, uni_Size, uni_Size )
    
    #パスアニメーションの作成
    cmds.pathAnimation( object[0], stu = st_1, etu = st_2, c = path)

    #ベイク
    _BakeAnimation()


#=============================================================================================
# アニメーションのベイク
#=============================================================================================
def _BakeAnimation():
    st_1 = cmds.intField('start',q=True,value=True)
    st_2 = cmds.intField('end',q=True,value=True)
    
    mesh = cmds.ls(sl = True)
    cmds.bakeResults( mesh , t=(st_1,st_2), at=["tx","ty","tz"] )
    
    
#=============================================================================================
# FBX Export
#=============================================================================================
def _FBXExport():
    #パスアニメーションの再設定
    _ReplaceAnimation()

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

    new_path = unicode_string + ("/Assets/_temp")
    print(new_path)

    #FBX出力
    cmds.select('pSphere1')

    om.MGlobal.executeCommand('FBXExport("-f", "{}", "-s")'.format(new_path))




#=============================================================================================
# パスアニメーションの再設定
#=============================================================================================
def _ReplaceAnimation():
    #スタート、エンドキーの再設定
    re_st_1 = cmds.intField('start',q=True,value=True)
    re_st_2 = cmds.intField('end',q=True,value=True)

    #キーを全て削除
    cmds.cutKey( 'pSphere1' )

    #スケール変更の場合
    sx =cmds.getAttr('pSphere1.sx')
    
    if cmds.checkBox(checkBox1, q=True, value=True) and sx == 100:
        cmds.scale( 1, 1, 1, 'pSphere1' ,r=True )
        cmds.scale( 1, 1, 1, 'curve1' ,r=True )
    elif cmds.checkBox(checkBox1, q=True, value=True) and sx == 1:
        cmds.scale( 100, 100, 100, 'pSphere1' ,r=True )
        cmds.scale( 100, 100, 100, 'curve1' ,r=True )
    elif sx == 100:
        cmds.scale( 0.01, 0.01, 0.01, 'pSphere1' ,r=True )
        cmds.scale( 0.01, 0.01, 0.01, 'curve1' ,r=True )
    elif sx == 1:
        cmds.scale( 1, 1, 1, 'pSphere1' ,r=True )
        cmds.scale( 1, 1, 1, 'curve1' ,r=True )

    

    #パスアニメーションの再設定
    cmds.pathAnimation( 'pSphere1', stu = re_st_1, etu = re_st_2, c = 'curve1' )

    #bake
    cmds.bakeResults( 'pSphere1' , t=(re_st_1,re_st_2), at=["tx","ty","tz"] )


#=============================================================================================
# GUIの作成
#=============================================================================================
cmds.window(t = 'QuickPathAnimation' )

cmds.columnLayout()


#----------------------------------------------------
# パスアニメーションの作成
#----------------------------------------------------
cmds.frameLayout( label=u" パスアニメーションの作成" , bv =True)

#フレームレンジ
cmds.rowLayout( nc = 3)
cmds.text( label='Frame Range' , w = 100)
cmds.intField('start', v = start_frame , w = 40)
cmds.intField('end', v = end_frame , w = 40)
cmds.setParent('..')

#ポイントの数
cmds.rowLayout( nc = 2)
cmds.text( label=u'ポイント数        ' , w = 100)
cmds.intField('point_num', v = point_count , w = 40)
cmds.setParent('..')

#スケール拡大
checkBox1 = cmds.checkBox(label=u'Unityのスケールに合わせて拡大', v = True)

#アニメーションパス作成
cmds.button( l='CreatePathAnimation', command= scriptPrefix+'_CreatePathAnimation()' , w = 200, bgc=(0.7968, 0.5, 0.5))


cmds.setParent('..')

#----------------------------------------------------
# エクスポート
#----------------------------------------------------
cmds.frameLayout( label=u" エクスポート" , w = 200, bv =True)



#FBXExpoart
cmds.button(label='FBX Export', command= scriptPrefix+'_FBXExport()' , w = 200 , bgc=(0.7968, 0.5, 0.5))

cmds.setParent('..')





cmds.setParent( '..' )

def UI():
    cmds.showWindow()
