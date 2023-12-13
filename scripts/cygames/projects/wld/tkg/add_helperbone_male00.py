# -*- coding: utf-8 -*-

from pyfbsdk import *

def GetObj(name = None):
    u'''
    シーン内のコンポーネントを探索
    '''
    lComps = FBSystem().Scene.Components
    lGetObjects = [lCm for lCm in lComps if lCm.LongName == name]
    return lGetObjects


def Find_AnimationNode( pParent, pName ):
    u'''
    # Boxが指定された名前のノードを持っているかを調べる。
    '''
    lResult = None
    for lNode in pParent.Nodes:
        if lNode.Name == pName:
            lResult = lNode
            break
    return lResult


def BoxExists_In_RelationCnst(lConst = None, lExBox = None):
    u'''
    Relation Constraint 内にlExBoxが存在するかどうか
    '''
    for lBox in lConst.Boxes:
        if lBox.LongName == lExBox:
            return True
            break

    return False


def MergeFile(CnstPath):
    u'''
    FBXをMerge
    '''
    FbxMergeOptions = FBFbxOptions(True)

    # すべて無効
    FbxMergeOptions.SetAll(FBElementAction.kFBElementActionDiscard, False)
    FbxMergeOptions.BaseCameras = FBElementAction.kFBElementActionDiscard
    FbxMergeOptions.CameraSwitcherSettings = FBElementAction.kFBElementActionDiscard
    FbxMergeOptions.CurrentCameraSettings = FBElementAction.kFBElementActionDiscard
    FbxMergeOptions.GlobalLightingSettings = FBElementAction.kFBElementActionDiscard
    FbxMergeOptions.TransportSettings = FBElementAction.kFBElementActionDiscard

    # コンストレイントのみ有効
    FbxMergeOptions.Constraints = FBElementAction.kFBElementActionMerge

    # FBXがロードされる前のスパンに設定
    FbxMergeOptions.TakeSpan = FBTakeSpanOnLoad.kFBLeaveAsIs

    FBApplication().FileMerge(CnstPath, False, FbxMergeOptions)


def Connect_Boxes(lConst = None):
    u'''
    Relation Constraint ごとに処理
    '''
    # ---------------------------
    # "armL_subjnt_Relation_cnst"
    # ---------------------------
    if lConst.Name == "armL_subjnt_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="armL_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="armL_subjnt")

        lSkel_src = GetObj(name = "armL_jnt")
        lSkel_dst = GetObj(name = "armL_subjnt")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender = lConst.SetAsSource( lSkel_src[0] )
        lSender.UseGlobalTransforms = False
        lSend_Rot  = Find_AnimationNode( lSender.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Rot  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Rotation' )

        for lBox in lConst.Boxes:
            if lBox.LongName == "Vector to Number 1":
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v )

            if lBox.LongName == "Number to Vector":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Rot )
                FBConnect( ntv_r, lRece_Rot )

    # ---------------------------
    # "armR_subjnt_Relation_cnst"
    # ---------------------------
    if lConst.Name == "armR_subjnt_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="armR_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="armR_subjnt")

        lSkel_src = GetObj(name = "armR_jnt")
        lSkel_dst = GetObj(name = "armR_subjnt")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender = lConst.SetAsSource( lSkel_src[0] )
        lSender.UseGlobalTransforms = False
        lSend_Rot  = Find_AnimationNode( lSender.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Rot  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Rotation' )

        for lBox in lConst.Boxes:
            if lBox.LongName == "Vector to Number 2":
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v )

            if lBox.LongName == "Number to Vector 1":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Rot )
                FBConnect( ntv_r, lRece_Rot )

    # ---------------------------
    # "uplegL_subjnt_Relation_cnst"
    # ---------------------------
    if lConst.Name == "uplegL_subjnt_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="uplegL_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="uplegL_subjnt_1")

        lSkel_src = GetObj(name = "uplegL_jnt")
        lSkel_dst = GetObj(name = "uplegL_subjnt_1")
        lSkel_dst_2 = GetObj(name = "uplegL_subjnt_2")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender = lConst.SetAsSource( lSkel_src[0] )
        lSender.UseGlobalTransforms = False
        lSend_Rot  = Find_AnimationNode( lSender.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Rot  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Rotation' )

        lRecever_2 = lConst.ConstrainObject( lSkel_dst_2[0] )
        lRecever_2.UseGlobalTransforms = False
        lRece_Rot_2  = Find_AnimationNode( lRecever_2.AnimationNodeInGet(), 'Lcl Rotation' )

        for lBox in lConst.Boxes:
            # uplegL_subjnt_1
            if lBox.LongName == "Vector to Number 3":
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v )

            if lBox.LongName == "Number to Vector 2":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Rot )
                FBConnect( ntv_r, lRece_Rot )

            # uplegL_subjnt_2
            if lBox.LongName == "Vector to Number":
                vtn1_v_2  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v_2 )

            if lBox.LongName == "Number to Vector 3":
                print lBox.LongName
                ntv_r_3  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r_3, lRece_Rot_2 )
                FBConnect( ntv_r_3, lRece_Rot_2 )

    # ---------------------------
    # "uplegR_subjnt_Relation_cnst"
    # ---------------------------
    if lConst.Name == "uplegR_subjnt_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="uplegR_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="uplegR_subjnt_1")

        lSkel_src = GetObj(name = "uplegR_jnt")
        lSkel_dst = GetObj(name = "uplegR_subjnt_1")
        lSkel_dst_2 = GetObj(name = "uplegR_subjnt_2")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender = lConst.SetAsSource( lSkel_src[0] )
        lSender.UseGlobalTransforms = False
        lSend_Rot  = Find_AnimationNode( lSender.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Rot  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Rotation' )

        lRecever_2 = lConst.ConstrainObject( lSkel_dst_2[0] )
        lRecever_2.UseGlobalTransforms = False
        lRece_Rot_2  = Find_AnimationNode( lRecever_2.AnimationNodeInGet(), 'Lcl Rotation' )

        for lBox in lConst.Boxes:
            # uplegL_subjnt_1
            if lBox.LongName == "Vector to Number 4":
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v )

            if lBox.LongName == "Number to Vector 4":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Rot )
                FBConnect( ntv_r, lRece_Rot )

            # uplegL_subjnt_2
            if lBox.LongName == "Vector to Number 5":
                vtn1_v_2  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v_2 )

            if lBox.LongName == "Number to Vector 5":
                print lBox.LongName
                ntv_r_3  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r_3, lRece_Rot_2 )
                FBConnect( ntv_r_3, lRece_Rot_2 )

    # ---------------------------
    # "kneeL_subjnt_Relation_cnst"
    # ---------------------------
    if lConst.Name == "kneeL_subjnt_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="legL_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="kneeL_subjnt")

        lSkel_src = GetObj(name = "legL_jnt")
        lSkel_dst = GetObj(name = "kneeL_subjnt")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender = lConst.SetAsSource( lSkel_src[0] )
        lSender.UseGlobalTransforms = False
        lSend_Rot  = Find_AnimationNode( lSender.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Trs  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Translation' )
        lRece_Rot  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Rotation' )

        for lBox in lConst.Boxes:
            if lBox.LongName == "Vector to Number 6":
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v )

            if lBox.LongName == "Number to Vector 7":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Trs )
                FBConnect( ntv_r, lRece_Trs )

            if lBox.LongName == "Number to Vector 6":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Rot )
                FBConnect( ntv_r, lRece_Rot )

    # ---------------------------
    # "kneeR_subjnt_Relation_cnst"
    # ---------------------------
    if lConst.Name == "kneeR_subjnt_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="legR_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="kneeR_subjnt")

        lSkel_src = GetObj(name = "legR_jnt")
        lSkel_dst = GetObj(name = "kneeR_subjnt")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender = lConst.SetAsSource( lSkel_src[0] )
        lSender.UseGlobalTransforms = False
        lSend_Rot  = Find_AnimationNode( lSender.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Trs  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Translation' )
        lRece_Rot  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Rotation' )

        for lBox in lConst.Boxes:
            if lBox.LongName == "Vector to Number 7":
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v )

            if lBox.LongName == "Number to Vector 8":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Trs )
                FBConnect( ntv_r, lRece_Trs )

            if lBox.LongName == "Number to Vector 9":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Rot )
                FBConnect( ntv_r, lRece_Rot )

    # ---------------------------
    # "armpitL_Relation_cnst"
    # ---------------------------
    if lConst.Name == "armpitL_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="shoulderL_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="armpitL_subjnt")

        lSkel_src_shl = GetObj(name = "shoulderL_jnt")
        lSkel_src_arm = GetObj(name = "armL_jnt")
        lSkel_dst = GetObj(name = "armpitL_subjnt")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender_shl = lConst.SetAsSource( lSkel_src_shl[0] )
        lSender_shl.UseGlobalTransforms = False
        lSend_Rot_shl  = Find_AnimationNode( lSender_shl.AnimationNodeOutGet(), 'Lcl Rotation' )

        lSender_arm = lConst.SetAsSource( lSkel_src_arm[0] )
        lSender_arm.UseGlobalTransforms = False
        lSend_Rot_arm  = Find_AnimationNode( lSender_arm.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Trs  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Translation' )

        for lBox in lConst.Boxes:
            if (lBox.LongName == "Vector to Number 8"
                or lBox.LongName == "Vector to Number 10"
                or lBox.LongName == "Vector to Number 12"):
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot_shl, vtn1_v )

            if (lBox.LongName == "Vector to Number 9"
                or lBox.LongName == "Vector to Number 11"
                or lBox.LongName == "Vector to Number 13"):
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot_arm, vtn1_v )

            if lBox.LongName == "Number to Vector 10":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Trs )
                FBConnect( ntv_r, lRece_Trs )

    # ---------------------------
    # "armpitR_Relation_cnst"
    # ---------------------------
    if lConst.Name == "armpitR_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="shoulderR_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="armpitR_subjnt")

        lSkel_src_shl = GetObj(name = "shoulderR_jnt")
        lSkel_src_arm = GetObj(name = "armR_jnt")
        lSkel_dst = GetObj(name = "armpitR_subjnt")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender_shl = lConst.SetAsSource( lSkel_src_shl[0] )
        lSender_shl.UseGlobalTransforms = False
        lSend_Rot_shl  = Find_AnimationNode( lSender_shl.AnimationNodeOutGet(), 'Lcl Rotation' )

        lSender_arm = lConst.SetAsSource( lSkel_src_arm[0] )
        lSender_arm.UseGlobalTransforms = False
        lSend_Rot_arm  = Find_AnimationNode( lSender_arm.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Trs  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Translation' )

        for lBox in lConst.Boxes:
            if (lBox.LongName == "Vector to Number 14"
                or lBox.LongName == "Vector to Number 16"
                or lBox.LongName == "Vector to Number 18"):
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot_shl, vtn1_v )

            if (lBox.LongName == "Vector to Number 15"
                or lBox.LongName == "Vector to Number 17"
                or lBox.LongName == "Vector to Number 19"):
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot_arm, vtn1_v )

            if lBox.LongName == "Number to Vector 11":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Trs )
                FBConnect( ntv_r, lRece_Trs )

    # ---------------------------
    # "elbowL_subjnt_Relation_cnst"
    # ---------------------------
    if lConst.Name == "elbowL_subjnt_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="forearmL_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="elbowL_subjnt")

        lSkel_src = GetObj(name = "forearmL_jnt")
        lSkel_dst = GetObj(name = "elbowL_subjnt")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender = lConst.SetAsSource( lSkel_src[0] )
        lSender.UseGlobalTransforms = False
        lSend_Rot  = Find_AnimationNode( lSender.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Trs  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Translation' )
        lRece_Rot  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Rotation' )

        for lBox in lConst.Boxes:
            if lBox.LongName == "Vector to Number 20":
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v )

            if lBox.LongName == "Number to Vector 12":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Trs )
                FBConnect( ntv_r, lRece_Trs )

            if lBox.LongName == "Number to Vector 13":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Rot )
                FBConnect( ntv_r, lRece_Rot )

    # ---------------------------
    # "elbowR_subjnt_Relation_cnst"
    # ---------------------------
    if lConst.Name == "elbowR_subjnt_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="forearmR_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="elbowR_subjnt")

        lSkel_src = GetObj(name = "forearmR_jnt")
        lSkel_dst = GetObj(name = "elbowR_subjnt")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender = lConst.SetAsSource( lSkel_src[0] )
        lSender.UseGlobalTransforms = False
        lSend_Rot  = Find_AnimationNode( lSender.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Trs  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Translation' )
        lRece_Rot  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Rotation' )

        for lBox in lConst.Boxes:
            if lBox.LongName == "Vector to Number 21":
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v )

            if lBox.LongName == "Number to Vector 14":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Trs )
                FBConnect( ntv_r, lRece_Trs )

            if lBox.LongName == "Number to Vector 15":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Rot )
                FBConnect( ntv_r, lRece_Rot )

    # ---------------------------
    # "handL_subjnt_Relation_cnst"
    # ---------------------------
    if lConst.Name == "handL_subjnt_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="handL_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="handL_subjnt")

        lSkel_src = GetObj(name = "handL_jnt")
        lSkel_dst = GetObj(name = "handL_subjnt")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender = lConst.SetAsSource( lSkel_src[0] )
        lSender.UseGlobalTransforms = False
        lSend_Rot  = Find_AnimationNode( lSender.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Rot  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Rotation' )

        for lBox in lConst.Boxes:
            if lBox.LongName == "Vector to Number 22":
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v )

            if lBox.LongName == "Number to Vector 16":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Rot )
                FBConnect( ntv_r, lRece_Rot )

    # ---------------------------
    # "handR_subjnt_Relation_cnst"
    # ---------------------------
    if lConst.Name == "handR_subjnt_Relation_cnst":
        lSenderSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="handR_jnt")
        lReceverSts = BoxExists_In_RelationCnst(lConst=lConst, lExBox="handR_subjnt")

        lSkel_src = GetObj(name = "handR_jnt")
        lSkel_dst = GetObj(name = "handR_subjnt")

        if lSenderSts or lReceverSts:
            print "Sender or Recever already exists."
            return

        # センダーを作成
        lSender = lConst.SetAsSource( lSkel_src[0] )
        lSender.UseGlobalTransforms = False
        lSend_Rot  = Find_AnimationNode( lSender.AnimationNodeOutGet(), 'Lcl Rotation' )

        # レシーバーを作成
        lRecever = lConst.ConstrainObject( lSkel_dst[0] )
        lRecever.UseGlobalTransforms = False
        lRece_Rot  = Find_AnimationNode( lRecever.AnimationNodeInGet(), 'Lcl Rotation' )

        for lBox in lConst.Boxes:
            if lBox.LongName == "Vector to Number 23":
                vtn1_v  = Find_AnimationNode( lBox.AnimationNodeInGet(), 'V' )
                FBConnect( lSend_Rot, vtn1_v )

            if lBox.LongName == "Number to Vector 17":
                print lBox.LongName
                ntv_r  = Find_AnimationNode( lBox.AnimationNodeOutGet(), 'Result' )
                print ( ntv_r, lRece_Rot )
                FBConnect( ntv_r, lRece_Rot )


def Connect_Boxes_In_RelationConstraints():
    u'''
    RelationConstraint をそれぞれ接続する
    '''
    lConstraints = FBSystem().Scene.Constraints
    for lConst in lConstraints:
        # print lConst.Name
        # armL_subjnt_Relation_cnst connection
        Connect_Boxes(lConst)


def Add_Constraints():
    u'''
    マージして実行
    '''
    HelperFbxPath = "//cgs-str-fas05/100_projects/051_world/production/team/rig/add_helperbone/data/male00_def_al_nrm-Setup-lite_constraints.fbx"
    MergeFile(HelperFbxPath)
    Connect_Boxes_In_RelationConstraints()
