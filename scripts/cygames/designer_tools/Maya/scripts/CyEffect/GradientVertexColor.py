#-*- encoding: utf-8
# 頂点カラーをグラデーションカラーで塗る


import maya.cmds as cmds
import maya.mel as mm

toolName = "GradientVertexColor"
scriptPrefix = toolName + "."

#=============================================================================================
# グラデーションタイプとモードの判定
#=============================================================================================
def _ModeCheck():
    selected_mode = cmds.radioButtonGrp('radioButtonGrp3', q=True, select=True) #Mode
    selected = cmds.radioButtonGrp('radioButtonGrp1', q=True, select=True)  #Gradient Type
    selected_2 = cmds.radioButtonGrp('radioButtonGrp2', q=True, select=True)

    obj = cmds.ls(sl =True)

    if selected_mode == 2 and selected == 1 and selected_2 == 4:   #エラー処理
        print(u"Directionは x , y , z のどれかを選択してください")
        return

    if selected_mode == 2 and selected == 1:   #Mesh
        if str(obj).find(".vtx") > 0:   #メッシュ選択なのに頂点選択されている場合
            print(u"頂点が選択されています オブジェクトを選択してください")
            return   

        if not obj: #メッシュ選択なのに何も選択されていない
            print(u"何も選択されていません")
            return

        vtxNum = cmds.polyEvaluate(v=True)  #頂点数

        #オブジェクトを選択しているの場合　頂点全体を選択する
        for i in range(vtxNum):
            sel =cmds.ls(sl =True)
            selName = sel[0]

            obj_vert = selName + '.vtx[000]'
            new_obj_vert = obj_vert.replace("000", str(i))

            cmds.select(new_obj_vert, add=True)

        _MeshBounds()

    elif selected_mode == 2 and  selected == 2 and selected_2 == 4: #Point to Point xyz
        if str(obj).find(".vtx") < 0:   #頂点編集モードなのに頂点選択されていない場合
            print(u"頂点選択されていません")
            return   

        _2PointsXYZ()

    elif selected_mode == 2 and  selected == 2: #Point to Point
        if str(obj).find(".vtx") < 0:   #頂点編集モードなのに頂点選択されていない場合
            print(u"頂点選択されていません")
            return   
        
        _PointToPoint()
        
    elif selected_mode == 2 and  selected == 3: #MulitPointsGradetion
        if str(obj).find(".vtx") < 0:   #頂点編集モードなのに頂点選択されていない場合
            print(u"頂点選択されていません")
            return   
        
        _MulitPointsGradetion()

    elif selected_mode == 1: #single
        if str(obj).find(".vtx") < 0:   #頂点編集モードなのに頂点選択されていない場合
            print(u"頂点選択されていません")
            return   
        
        _SingleColor()



#=============================================================================================
# メッシュ全体
#=============================================================================================
def _MeshBounds():    
    
    #------------------------------------------------------------------------------------------
    # ローカル変数
    #------------------------------------------------------------------------------------------
    selVetex_list = cmds.ls(sl=True)   #選択オブジェクトの頂点リスト
    selVertex_num =cmds.filterExpand(selVetex_list , sm=31) #頂点のセレクションマスク　sm=31

    main_color_preview = cmds.colorSliderGrp('_values_1', q=True, rgb=True)  #メインカラー
    sub_color_preview = cmds.colorSliderGrp('_values_2', q=True, rgb=True)  #サブカラー
    main_color_alpha = cmds.floatSliderGrp('_alpha_1', q=True, value=True) #メインアルファ
    sub_color_alpha = cmds.floatSliderGrp('_alpha_2', q=True, value=True)  #サブアルファ

    c1 = main_color_preview #カラー 1
    c2 = sub_color_preview  #カラー 2  
    a1 = main_color_alpha   #アルファ 1
    a2 = sub_color_alpha    #アルファ 2

    new_dismax_list=[]

    #------------------------------------------------------------------------------------------
    # 計算
    #------------------------------------------------------------------------------------------
    #distance_value minmax
    min_max_dist = getDistacceValueMax(selVertex_num, new_dismax_list)
    max_distance_value = min_max_dist[0]
    min_distance_value = min_max_dist[1]


    #------------------------------------------------------------------------------------------
    # 描画
    #------------------------------------------------------------------------------------------
    for i in range(len(selVertex_num)):
        vertex_pos = cmds.pointPosition(selVertex_num[i], local = True)
        distance_value = getVertexDistance(vertex_pos)  #2点間の距離

        ndv = nomalizeDistacceValue( min_distance_value, max_distance_value, distance_value)
        normalize_distance = ndv

        ng = normalize_grad(c1, c2, a1, a2, ndv, normalize_distance)
        normalize_color_r = ng[0]
        normalize_color_g = ng[1]
        normalize_color_b = ng[2]
        normalize_color_a = ng[3]

        cmds.polyColorPerVertex(selVertex_num[i], rgb=(normalize_color_r ,normalize_color_g ,normalize_color_b) ,a=normalize_color_a ,cdo=True )

#=============================================================================================
# 2頂点平行グラデーション
#=============================================================================================
def _PointToPoint():

    #------------------------------------------------------------------------------------------
    # ローカル変数
    #------------------------------------------------------------------------------------------
    main_color_preview = cmds.colorSliderGrp('_values_1', q=True, rgb=True)  #メインカラー
    sub_color_preview = cmds.colorSliderGrp('_values_2', q=True, rgb=True)  #サブカラー
    main_color_alpha = cmds.floatSliderGrp('_alpha_1', q=True, value=True) #メインアルファ
    sub_color_alpha = cmds.floatSliderGrp('_alpha_2', q=True, value=True)  #サブアルファ

    c1 = main_color_preview
    c2 = sub_color_preview    
    a1 = main_color_alpha
    a2 = sub_color_alpha

    vtxNum = cmds.polyEvaluate(v=True)  #頂点数

    bo = cmds.selectPref(q=True, tso =True) #頂点インデックスを選択順に取得

    new_dismax_list=[]

    selected = cmds.radioButtonGrp('radioButtonGrp1', q=True, select=True)
    selected_2 = cmds.radioButtonGrp('radioButtonGrp2', q=True, select=True)    #グラデ方向の分岐

    #------------------------------------------------------------------------------------------
    # 計算
    #------------------------------------------------------------------------------------------
    #選択順に取得出来ているかチェック　Preferences ⇒ Selection ⇒ Track selection orderがOFFならばONにする
    if bo == True:
        print(u"既にONだった") 
    else:
        print(u"既にOFFだった") 
        cmds.selectPref(tso = True) 
        
    
    component = cmds.ls(os = True)    
    print(component)


    #選択2頂点
    si_point = cmds.ls(os = True)

    #【エラー処理】　選択頂点が2点でない
    if len(si_point) != 2:
        print(u"頂点を2点選択してください")
        return

    pos_1 = cmds.pointPosition(si_point[0] , local = True) #選択頂点 1座標
    pos_2 = cmds.pointPosition(si_point[1] , local = True) #選択頂点 2座標

    print("pos_1 = " +str(pos_1))
    print("pos_2 = " +str(pos_2))
    

    #【エラー処理】　2点選択で、両方Y=0の時にY軸方向グラデーションを指定したとき　
    if pos_1[1] == 0 and pos_2[1] == 0 and  selected == 2 and selected_2 == 2:
        print(u"Y座標が0なのにY方向のグラデーションを指定しています")
        return


    #オブジェクト名
    si_point_objname =cmds.ls(sl=True, o=True, s=False)  

    #全頂点選択
    cmds.select(cl =True)  #今選択している2頂点をクリア
    cmds.select(si_point_objname) #再度オブジェクト選択


    #2頂点選択を全頂点選択に変換
    for i in range(vtxNum):
        selName = si_point_objname[0]
        obj_vert = selName + '.vtx[000]'
        new_obj_vert = obj_vert.replace("000", str(i))

        cmds.select(new_obj_vert, add=True) #全頂点選択


    selVetex_list = cmds.ls(sl=True)   #選択オブジェクトの頂点リスト
    selVertex_num =cmds.filterExpand(selVetex_list , sm=31) #頂点のセレクションマスク　sm=31
   

    #distance_value minmax
    min_max_dist = getDistacceValueMax(selVertex_num,  new_dismax_list)
    max_distance_value = min_max_dist[0]
    min_distance_value = min_max_dist[1]


    #グラデ方向
    if selected_2 == 1:
        d = 0
    elif selected_2 == 2:
        d = 1
    elif selected_2 == 3:
        d = 2
    
    #------------------------------------------------------------------------------------------
    # 描画
    #------------------------------------------------------------------------------------------
    for i in range(len(selVertex_num)):
        vertex_pos = cmds.pointPosition(selVertex_num[i], local = True)

        distance_value = getVertexDistance(vertex_pos)  #2点間の距離

        ndv = nomalizeDistacceValue( min_distance_value, max_distance_value, distance_value)
        normalize_distance = ndv


        #グラデーション
        if d == 0 or d == 1:  #X軸もしくはY軸
            if pos_1[d] > pos_2[d] :   #pos_1 > pos_2
                if vertex_pos[d] < pos_2[d] or vertex_pos[d] == pos_2[d]:  
                    normalize_color_r = c2[0]
                    normalize_color_g = c2[1]
                    normalize_color_b = c2[2]
                    normalize_color_a = a2
                elif (vertex_pos[d] < pos_1[d] and vertex_pos[d] > pos_2[d] ): 
                    ng = normalize_grad_2(c1, c2, a1, a2, ndv, normalize_distance)
                    normalize_color_r = ng[0]
                    normalize_color_g = ng[1]
                    normalize_color_b = ng[2]
                    normalize_color_a = ng[3]              
                elif vertex_pos[d] > pos_1[d] or vertex_pos[d] == pos_1[d]: 
                    normalize_color_r = c1[0]
                    normalize_color_g = c1[1]
                    normalize_color_b = c1[2]
                    normalize_color_a = a1 
            elif pos_1[d] < pos_2[d]:   #pos_1 < pos_2 
                if vertex_pos[d] < pos_1[d] or vertex_pos[d] == pos_1[d]:   
                    normalize_color_r = c1[0]
                    normalize_color_g = c1[1]
                    normalize_color_b = c1[2] 
                    normalize_color_a = a1          
                elif vertex_pos[d] > pos_1[d] and vertex_pos[d] < pos_2[d] :
                    ng = normalize_grad(c1, c2, a1, a2, ndv, normalize_distance)
                    normalize_color_r = ng[0]
                    normalize_color_g = ng[1]
                    normalize_color_b = ng[2]   
                    normalize_color_a = ng[3]                              
                elif vertex_pos[d] > pos_2[d] or vertex_pos[d] == pos_2[d]: 
                    normalize_color_r = c2[0]
                    normalize_color_g = c2[1]
                    normalize_color_b = c2[2]   
                    normalize_color_a = a2           
        if d == 2:  #Z軸
            if pos_1[d] > pos_2[d] :   #pos_1 > pos_2
                if vertex_pos[d] < pos_2[d] or vertex_pos[d] == pos_2[d]:  
                    normalize_color_r = c2[0]
                    normalize_color_g = c2[1]
                    normalize_color_b = c2[2]
                    normalize_color_a = a2
                elif (vertex_pos[d] < pos_1[d] and vertex_pos[d] > pos_2[d] ): 
                    ng = normalize_grad(c1, c2, a1, a2, ndv, normalize_distance)
                    normalize_color_r = ng[0]
                    normalize_color_g = ng[1]
                    normalize_color_b = ng[2]
                    normalize_color_a = ng[3]              
                elif vertex_pos[d] > pos_1[d] or vertex_pos[d] == pos_1[d]: 
                    normalize_color_r = c1[0]
                    normalize_color_g = c1[1]
                    normalize_color_b = c1[2]
                    normalize_color_a = a1   
            elif pos_1[d] < pos_2[d]:   #pos_1 < pos_2 
                if vertex_pos[d] < pos_1[d] or vertex_pos[d] == pos_1[d]:   
                    normalize_color_r = c1[0]
                    normalize_color_g = c1[1]
                    normalize_color_b = c1[2] 
                    normalize_color_a = a1          
                elif vertex_pos[d] > pos_1[d] and vertex_pos[d] < pos_2[d] :
                    ng = normalize_grad_2(c1, c2, a1, a2, ndv, normalize_distance)
                    normalize_color_r = ng[0]
                    normalize_color_g = ng[1]
                    normalize_color_b = ng[2]   
                    normalize_color_a = ng[3]                              
                elif vertex_pos[d] > pos_2[d] or vertex_pos[d] == pos_2[d]: 
                    normalize_color_r = c2[0]
                    normalize_color_g = c2[1]
                    normalize_color_b = c2[2]   
                    normalize_color_a = a2 


        cmds.polyColorPerVertex(selVertex_num[i], rgb=(normalize_color_r ,normalize_color_g ,normalize_color_b) ,a=normalize_color_a ,cdo=True )


#=============================================================================================
# 2点で全方向
#=============================================================================================
def _2PointsXYZ():

    #------------------------------------------------------------------------------------------
    # ローカル変数
    #------------------------------------------------------------------------------------------
    main_color_preview = cmds.colorSliderGrp('_values_1', q=True, rgb=True)  #メインカラー
    sub_color_preview = cmds.colorSliderGrp('_values_2', q=True, rgb=True)  #サブカラー
    main_color_alpha = cmds.floatSliderGrp('_alpha_1', q=True, value=True) #メインアルファ
    sub_color_alpha = cmds.floatSliderGrp('_alpha_2', q=True, value=True)  #サブアルファ

    c1 = main_color_preview
    c2 = sub_color_preview    
    a1 = main_color_alpha
    a2 = sub_color_alpha

    vtxNum = cmds.polyEvaluate(v=True)  #頂点数


    #------------------------------------------------------------------------------------------
    # 計算
    #------------------------------------------------------------------------------------------

    #p1, p2の2点間の距離Aを取る
    #選択2頂点
    si_point = cmds.ls(os = True)

    #【エラー処理】　選択頂点が2点でない
    if len(si_point) != 2:
        print(u"頂点を2点選択してください")
        return

    pos_1 = cmds.pointPosition(si_point[0] , local = True) #選択頂点 1座標
    pos_2 = cmds.pointPosition(si_point[1] , local = True) #選択頂点 2座標

    print("pos_1 = " +str(pos_1))
    print("pos_2 = " +str(pos_2))

    mm.eval("vector $vertex_pos_0 = << %s , %s , %s >>; " % (pos_1 [0] ,pos_1 [1] ,pos_1 [2]))
    mm.eval("vector $vertex_pos_1 = << %s , %s , %s >>; " % (pos_2 [0] ,pos_2 [1] ,pos_2 [2]))
    mm.eval("vector $vertex_Vector = $vertex_pos_0 - $vertex_pos_1;") 

    ini_distance_value = mm.eval("mag $vertex_Vector;") #2点間の距離

    print("ini_distance_value = " +str(ini_distance_value))


    #オブジェクト名
    si_point_objname =cmds.ls(sl=True, o=True, s=False)  

    #全頂点選択
    cmds.select(cl =True)  #今選択している2頂点をクリア
    cmds.select(si_point_objname) #再度オブジェクト選択

    #2頂点選択を全頂点選択に変換
    for i in range(vtxNum):
        selName = si_point_objname[0]
        obj_vert = selName + '.vtx[000]'
        new_obj_vert = obj_vert.replace("000", str(i))

        cmds.select(new_obj_vert, add=True) #全頂点選択


    selVetex_list = cmds.ls(sl=True)   #選択オブジェクトの頂点リスト
    selVertex_num =cmds.filterExpand(selVetex_list , sm=31) #頂点のセレクションマスク　sm=31



    #------------------------------------------------------------------------------------------
    # 描画
    #------------------------------------------------------------------------------------------
    for j in range(len(selVertex_num)):
        vertex_pos = cmds.pointPosition(selVertex_num[j], local = True)

        distance_value = getVertexDistance_xyz(vertex_pos, pos_1)  #2点間の距離

        ndv2 = distance_value / ini_distance_value 

        #1を超えたら1に
        if ndv2 > 1.0:
            ndv2 = 1.0
        else:
            ndv2 = ndv2 

        
        normalize_color_r = (c1[0] * (1.0 -ndv2)) + (c2[0] * (ndv2))
        normalize_color_g = (c1[1] * (1.0-ndv2)) + (c2[1] * (ndv2))
        normalize_color_b = (c1[2] * (1.0 -ndv2)) + (c2[2] * (ndv2))
        normalize_color_a = (a1 * (1.0 -ndv2)) + (a2 * (ndv2))   

        cmds.polyColorPerVertex(selVertex_num[j], rgb=(normalize_color_r ,normalize_color_g ,normalize_color_b) ,a=normalize_color_a ,cdo=True )





#=============================================================================================
# マルチポイントグラデーション
#=============================================================================================
def _MulitPointsGradetion():

    #------------------------------------------------------------------------------------------
    # ローカル変数
    #------------------------------------------------------------------------------------------
    main_color_preview = cmds.colorSliderGrp('_values_1', q=True, rgb=True)  #メインカラー
    sub_color_preview = cmds.colorSliderGrp('_values_2', q=True, rgb=True)  #サブカラー
    main_color_alpha = cmds.floatSliderGrp('_alpha_1', q=True, value=True) #メインアルファ
    sub_color_alpha = cmds.floatSliderGrp('_alpha_2', q=True, value=True)  #サブアルファ

    c1 = main_color_preview
    c2 = sub_color_preview    
    a1 = main_color_alpha
    a2 = sub_color_alpha

    bo = cmds.selectPref(q=True, tso =True) #頂点インデックスを選択順に取得

    new_dismax_list=[]


    #------------------------------------------------------------------------------------------
    # 計算
    #------------------------------------------------------------------------------------------
    #選択順に取得出来ているかチェック　Preferences ⇒ Selection ⇒ Track selection orderがOFFならばONにする
    if bo == True:
        print(u"既にONだった") 
    else:
        print(u"既にOFFだった") 
        cmds.selectPref(tso = True) 
        
    
    component = cmds.ls(os = True)    
    print(component)


    #選択頂点
    si_point = cmds.ls(os = True)
    #print("si_point = " + str(si_point))

    #【エラー処理】　選択頂点が2点より小さい
    if len(si_point) < 2:
        print(u"頂点を1点より大きい数を選択してください")
        return

    #選択頂点の座標取得
    for i in range(len(si_point)):
        si_point[i] = cmds.pointPosition(si_point[i] , local = True) #選択頂点座標

    
    selVetex_list = cmds.ls(sl=True)   #選択オブジェクトの頂点リスト
    selVertex_num =cmds.filterExpand(selVetex_list , sm=31) #頂点のセレクションマスク　sm=31


    #distance_value minmax
    min_max_dist = getDistacceValueMax(selVertex_num,  new_dismax_list)
    max_distance_value = min_max_dist[0]
    min_distance_value = min_max_dist[1]


    #------------------------------------------------------------------------------------------
    # 描画
    #------------------------------------------------------------------------------------------
    for j in range(len(si_point)):
        vertex_pos = cmds.pointPosition(selVertex_num[j], local = True)

        distance_value = getVertexDistance(vertex_pos)  #2点間の距離

        ndv = nomalizeDistacceValue( min_distance_value, max_distance_value, distance_value)
        normalize_distance = ndv


        #グラデーション
        if normalize_distance < 1.0:
            normalize_color_r = (c1[0] * (1.0 - normalize_distance)) + (c2[0] * (normalize_distance))
            normalize_color_g = (c1[1] * (1.0 - normalize_distance)) + (c2[1] * (normalize_distance))
            normalize_color_b = (c1[2] * (1.0 - normalize_distance)) + (c2[2] * (normalize_distance))
            normalize_color_a = (a1 * (1.0 - normalize_distance)) + (a2 * (normalize_distance))
        else:
            normalize_color_r = c2[0]
            normalize_color_g = c2[1]
            normalize_color_b = c2[2]
            normalize_color_a = a2


        cmds.polyColorPerVertex(selVertex_num[j], rgb=(normalize_color_r ,normalize_color_g ,normalize_color_b) ,a=normalize_color_a ,cdo=True )


#=============================================================================================
# 単色
#=============================================================================================
def _SingleColor():
    #------------------------------------------------------------------------------------------
    # ローカル変数
    #------------------------------------------------------------------------------------------
    main_color_preview = cmds.colorSliderGrp('_values_1', q=True, rgb=True)  #メインカラー
    main_color_alpha = cmds.floatSliderGrp('_alpha_1', q=True, value=True) #メインアルファ
    c1 = main_color_preview
    a1 = main_color_alpha

    #選択頂点
    selVetex_list = cmds.ls(sl=True)   #選択オブジェクトの頂点リスト
    selVertex_num =cmds.filterExpand(selVetex_list , sm=31) #頂点のセレクションマスク　sm=31

    #描画
    for j in range(len(selVertex_num)):
        normalize_color_r = c1[0]
        normalize_color_g = c1[1]
        normalize_color_b = c1[2]
        normalize_color_a = a1 

        cmds.polyColorPerVertex(selVertex_num[j], rgb=(normalize_color_r ,normalize_color_g ,normalize_color_b) ,a=normalize_color_a ,cdo=True )



#=============================================================================================
# ポジションのmin,maxを取得する
#=============================================================================================
def getDistance(selVertex_num,new_list):

    for i in range(len(selVertex_num)):
        vertex_pos = cmds.pointPosition(selVertex_num[i], local = True)
        new_list.extend(vertex_pos)

    max_positionValue = max(new_list)
    min_positionValue = min(new_list)

    
    return max_positionValue, min_positionValue

#=============================================================================================
# 2点間の距離
#=============================================================================================
def getVertexDistance(vertex_pos):
    selected = cmds.radioButtonGrp('radioButtonGrp1', q=True, select=True)
    selected_2 = cmds.radioButtonGrp('radioButtonGrp2', q=True, select=True)

    selVetex_list = cmds.ls(sl=True)   #選択オブジェクトの頂点リスト
    selVertex_num =cmds.filterExpand(selVetex_list , sm=31) #頂点のセレクションマスク　sm=31

    vert_pos_s = cmds.pointPosition(selVertex_num[0], local = True) # 最初の点


    if selected == 1 and selected_2 == 1:   #Mesh BoundsでX
        cx = -1
        cy = 0
        cz = 0
        mm.eval("vector $vertex_pos_0 = << %s , %s , %s >>; " % (cx ,cy ,cz))
        mm.eval("vector $vertex_pos_1 = << %s , %s , %s >>; " % (vertex_pos[0],vertex_pos[1],vertex_pos[2]))
        mm.eval("vector $vertex_Vector = $vertex_pos_0 - $vertex_pos_1;")
    elif selected == 1 and selected_2 == 2:    #Mesh BoundsでY
        cx = 0
        cy = 1
        cz = 0
        mm.eval("vector $vertex_pos_0 = << %s , %s , %s >>; " % (cx ,cy ,cz))
        mm.eval("vector $vertex_pos_1 = << %s , %s , %s >>; " % (vertex_pos[0],vertex_pos[1],vertex_pos[2]))
        mm.eval("vector $vertex_Vector = $vertex_pos_0 - $vertex_pos_1;")
    elif selected == 1 and selected_2 == 3:    #Mesh BoundsでZ
        cx = 0
        cy = 0
        cz = -1
        mm.eval("vector $vertex_pos_0 = << %s , %s , %s >>; " % (cx ,cy ,cz))
        mm.eval("vector $vertex_pos_1 = << %s , %s , %s >>; " % (vertex_pos[0],vertex_pos[1],vertex_pos[2]))
        mm.eval("vector $vertex_Vector = $vertex_pos_0 - $vertex_pos_1;")        
    elif selected == 2 and selected_2 == 1:   #Poiny to PointでDirection X
        cx = vert_pos_s[0] 
        cy = vert_pos_s[1] 
        cz = vert_pos_s[2] 
        mm.eval("vector $vertex_pos_0 = << %s , %s , %s >>; " % (cx ,cy ,cz))
        mm.eval("vector $vertex_pos_1 = << %s , %s , %s >>; " % (vertex_pos[0], cy, cz))
        mm.eval("vector $vertex_Vector = $vertex_pos_0 - $vertex_pos_1;")
    elif selected == 2 and selected_2 == 2:   #Poiny to PointでDirection Y
        cx = vert_pos_s[0]
        cy = vert_pos_s[1]
        cz = vert_pos_s[2]  
        mm.eval("vector $vertex_pos_0 = << %s , %s , %s >>; " % (cx ,cy ,cz))
        mm.eval("vector $vertex_pos_1 = << %s , %s , %s >>; " % (cx, vertex_pos[1], cz))
        mm.eval("vector $vertex_Vector = $vertex_pos_0 - $vertex_pos_1;")
    elif selected == 2 and selected_2 == 3:   #Poiny to PointでDirection Z
        cx = vert_pos_s[0]
        cy = vert_pos_s[1]
        cz = vert_pos_s[2]       
        mm.eval("vector $vertex_pos_0 = << %s , %s , %s >>; " % (cx ,cy ,cz))
        mm.eval("vector $vertex_pos_1 = << %s , %s , %s >>; " % (cx, cy , vertex_pos[2]))  
        mm.eval("vector $vertex_Vector = $vertex_pos_0 - $vertex_pos_1;") 
    elif selected == 3 :   #MulitPointsGradetion
        cx = vert_pos_s[0]
        cy = vert_pos_s[1]
        cz = vert_pos_s[2]       
        mm.eval("vector $vertex_pos_0 = << %s , %s , %s >>; " % (cx ,cy ,cz))
        mm.eval("vector $vertex_pos_1 = << %s , %s , %s >>; " % (vertex_pos[0],vertex_pos[1],vertex_pos[2]))
        mm.eval("vector $vertex_Vector = $vertex_pos_0 - $vertex_pos_1;") 
    

    distance_value = mm.eval("mag $vertex_Vector;") #2点間の距離


    return distance_value

#=============================================================================================
# 2点間の距離_xyz
#=============================================================================================
def getVertexDistance_xyz(vertex_pos, pos_1):

    mm.eval("vector $vertex_pos_0 = << %s , %s , %s >>; " % (pos_1 [0] ,pos_1 [1] ,pos_1 [2]))
    mm.eval("vector $vertex_pos_1 = << %s , %s , %s >>; " % (vertex_pos[0],vertex_pos[1],vertex_pos[2]))
    mm.eval("vector $vertex_Vector = $vertex_pos_0 - $vertex_pos_1;")

    distance_value = mm.eval("mag $vertex_Vector;") #2点間の距離


    return distance_value

#=============================================================================================
# distance_value minmax
#=============================================================================================
def getDistacceValueMax(selVertex_num, new_dismax_list):
    for i in range(len(selVertex_num)):
        vertex_pos = cmds.pointPosition(selVertex_num[i], local = True)
        distance_value = getVertexDistance(vertex_pos)  #2点間の距離
        new_dismax_list.append(distance_value)

    max_distance_value = max(new_dismax_list)
    min_distance_value = min(new_dismax_list)

    print("max_distance_value = "+ str(max_distance_value))
    print("min_distance_value = "+ str(min_distance_value))

    return max_distance_value, min_distance_value


#=============================================================================================
# distance_valueの正規化
#=============================================================================================
def nomalizeDistacceValue( min_distance_value, max_distance_value, distance_value):

    normalize_distance = (distance_value - min_distance_value)/(max_distance_value - min_distance_value) 

    return normalize_distance


#=============================================================================================
# normalize grad
#=============================================================================================
def normalize_grad(c1, c2, a1, a2, ndv, normalize_distance):

    max_distance = 1.0

    if normalize_distance < 1.0:
        normalize_color_r = (c1[0] * (max_distance -ndv)) + (c2[0] * (ndv))
        normalize_color_g = (c1[1] * (max_distance -ndv)) + (c2[1] * (ndv))
        normalize_color_b = (c1[2] * (max_distance -ndv)) + (c2[2] * (ndv))
        normalize_color_a = (a1 * (max_distance -ndv)) + (a2 * (ndv))
    else:
        normalize_color_r = c2[0]
        normalize_color_g = c2[1]
        normalize_color_b = c2[2]
        normalize_color_a = a2


    return normalize_color_r, normalize_color_g, normalize_color_b, normalize_color_a    

#=============================================================================================
# normalize grad 2
#=============================================================================================
def normalize_grad_2(c1, c2, a1, a2, ndv, normalize_distance):

    max_distance = 1.0

    if normalize_distance < 1.0:
        normalize_color_r = (c1[0] *(ndv)) + (c2[0] *  (max_distance -ndv))
        normalize_color_g = (c1[1] *(ndv)) + (c2[1] *  (max_distance -ndv))
        normalize_color_b = (c1[2] *(ndv)) + (c2[2] *  (max_distance -ndv))
        normalize_color_a = (a1 * (ndv)) + (a2 * (max_distance -ndv))  
    else:
        normalize_color_r = c2[0]
        normalize_color_g = c2[1]
        normalize_color_b = c2[2]
        normalize_color_a = a2


    return normalize_color_r, normalize_color_g, normalize_color_b, normalize_color_a    



#=============================================================================================
# カラークリア
#=============================================================================================
def _Clear():   
    obj = cmds.ls(sl =True)

    if not obj:
        print(u"何も選択されていません")
        return
    else:
        #選択頂点のカラーをクリア
        cmds.polyColorPerVertex( rem = True )


#=============================================================================================
# SwapColor
#=============================================================================================
def _SwapColor():
    main_color_preview = cmds.colorSliderGrp('_values_1', q=True, rgb=True)  #メインカラー
    sub_color_preview = cmds.colorSliderGrp('_values_2', q=True, rgb=True)  #サブカラー
    main_color_alpha = cmds.floatSliderGrp('_alpha_1', q=True, value=True) #メインアルファ
    sub_color_alpha = cmds.floatSliderGrp('_alpha_2', q=True, value=True)  #サブアルファ


    swm_r = main_color_preview[0]
    swm_g = main_color_preview[1]
    swm_b = main_color_preview[2]
    swm_a = main_color_alpha

    sws_r = sub_color_preview[0]
    sws_g = sub_color_preview[1]
    sws_b = sub_color_preview[2]
    sws_a = sub_color_alpha

    cmds.colorSliderGrp('_values_1', e=True, rgb=[sws_r, sws_g, sws_b])  #メインカラー
    cmds.colorSliderGrp('_values_2', e=True, rgb=[swm_r, swm_g, swm_b])  #サブカラー
    cmds.floatSliderGrp('_alpha_1', e=True, value= sws_a) #メインアルファ
    cmds.floatSliderGrp('_alpha_2', e=True, value= swm_a)  #サブアルファ



#=============================================================================================
# GUIの作成
#=============================================================================================
cmds.window(t = 'GradientVertexColor' )

cmds.columnLayout()

#----------------------------------------------------
# 設定
#----------------------------------------------------
cmds.frameLayout( label=u" Setiing" , w = 400, bv =True, cl = False, cll = True)

#カラーの塗り方
cmds.radioButtonGrp( 'radioButtonGrp3', label='Mode: ', labelArray2=['single', 'gradient'], numberOfRadioButtons=2 ,  cw3=[120,100,100], select = 2)

cmds.setParent('..')

#----------------------------------------------------
# カラー
#----------------------------------------------------
cmds.frameLayout( label=u" Color" , w = 400, bv =True, cl = False, cll = True)

#カラーピッカー
main_color_preview = cmds.colorSliderGrp( '_values_1' ,l="Main Color: ",  rgb=(0.5, 0.5, 0.5) ,  cw3=[100,50,100] ) #メインカラー
main_color_alpha = cmds.floatSliderGrp('_alpha_1' ,l="Main Alpha: ", field=True, minValue=0.0, maxValue=1.0,  value=1.0,  cw3=[100,50,100])    #メインアルファ

#swap color
cmds.button( l=u'↑↓', command= scriptPrefix+'_SwapColor()' , w = 100, bgc=(0.267, 0.267, 0.267))


sub_color_preview = cmds.colorSliderGrp( '_values_2' ,l="Sub Color: ",  rgb=(0.5, 0.5, 0.5) ,  cw3=[100,50,100] ) #サブカラー
sub_color_alpha = cmds.floatSliderGrp('_alpha_2' ,l="Sub Alpha: ", field=True, minValue=0.0, maxValue=1.0,  value=1.0,  cw3=[100,50,100])    #サブアルファ


cmds.setParent('..')

#----------------------------------------------------
# グラデーションオプション
#----------------------------------------------------
cmds.frameLayout( label=u" Gradient Option" , w =400, bv =True, cl = False, cll = True)

#グラデーション形状
cmds.radioButtonGrp( 'radioButtonGrp1', label='Gradient Type: ', labelArray3=['Mesh', 'Point to Point', 'MultiplePoints'], numberOfRadioButtons=3 ,  cw4=[100,70,100,100], select =1)

#グラデーションの方向
cmds.radioButtonGrp( 'radioButtonGrp2', label='Gradient Direction: ', labelArray4=['x', 'y', 'z', 'xyz'], numberOfRadioButtons=4 ,  cw5=[120,40,40,40,40], select =1)

cmds.setParent('..')

#----------------------------------------------------
# 決定ボタン
#----------------------------------------------------
#cmds.frameLayout( label=u""  )

cmds.rowLayout(numberOfColumns=2, cw2 = (198, 198) ,columnAttach2=('both', 'both')  )

#実行
cmds.button( l=u'Apply', command= scriptPrefix+'_ModeCheck()' , bgc=(0.7968, 0.5, 0.5))

#クリア
cmds.button( l=u'Clear', command= scriptPrefix+'_Clear()' , bgc=(0.7968, 0.5, 0.5))



cmds.setParent('..')

#----------------------------------------------------
cmds.setParent( '..' )

def UI():
    cmds.showWindow()
    





