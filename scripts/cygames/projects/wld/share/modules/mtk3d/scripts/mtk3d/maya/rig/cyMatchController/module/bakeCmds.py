# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mm
import os
import mtk3d.maya.rig.cyMatchController.module.matchFuncs as match

# reload(exe)
reload(match)

def envs(*args):
    lang = ["rm"]
    append = lang.append

    for k, v in os.environ.items():
        if k == "MAYA_UI_LANGUAGE":
            append(v)
    lang.pop(0)        
    return lang 
    
def viewChange(*args):
    env = envs()
    if env:
        if env[0] == 'en_US':
            mm.eval('setNamedPanelLayout("Single Perspective View")')
            mc.modelPanel( "modelPanel4", edit=True, up=True )
        elif  env[0] == 'ja_JP':
            mm.eval(u'setNamedPanelLayout ("単一のパース ビュー")')
            mc.modelPanel( "modelPanel4", edit=True, up=True )
    else:
        mm.eval(u'setNamedPanelLayout ("単一のパース ビュー")')
        mc.modelPanel( "modelPanel4", edit=True, up=True )

        
def viewChangeEnd(*args):
    env = envs()
    if env:
        if env[0] == 'en_US':
            mm.eval('setNamedPanelLayout("Single Perspective View")')
        elif  env[0] == 'ja_JP':
            mm.eval(u'setNamedPanelLayout ("単一のパース ビュー")')

    else:
        mm.eval(u'setNamedPanelLayout ("単一のパース ビュー")')

def bakeCmds(*args):
    viewChange()

    Prts = mc.radioButtonGrp( 'partsChk',q=True,select=True )
    
    #LRチェックボックスの正誤
    boolLR = mc.checkBox('boxLR',q=True,v=True)
    #ArmLegチェックボックスの正誤
    boolArmLeg = mc.checkBox('boxArmLeg',q=True,v=True)
     
    if boolArmLeg == False and boolLR == False:#

        #　左右判定
        sideSts = mc.radioButtonGrp( 'sideChk',q=True,select=True )
        if sideSts == 1:
            LR = 'L'
        else:
            LR = 'R'
        # Ikbake かFkbakeかの判定  パーツ判定と実行コマンド
        bakeType = mc.radioButtonGrp( 'bakeType',q=True,select=True )
        partSts = mc.radioButtonGrp( 'partsChk',q=True,select=True )
        if bakeType == 1:
            # print 'FK bake'
            if partSts == 1:
                ctrls = ['upArm_ _fkCtrl', 'arm_ _fkCtrl']
            else:
                ctrls = ['upLeg_ _fkCtrl', 'leg_ _fkCtrl', 'foot_ _fkCtrl', 'toe_ _fkCtrl']
        elif bakeType == 2:
            # print 'IK bake'     
            if partSts == 1:
                ctrls = ['hand_ _Ctrl', 'arm_ _PVCtrl']
            else:
                ctrls = ['leg_ _Ctrl', 'leg_ _PVCtrl', 'toe_ _Ctrl']
        # セレクト用手足コントローラ群
        n=len(ctrls)
        Ctrl=[]
        for i in xrange(0,n,1):
            nmspSts = mc.checkBox('useNMspsChk',q=True,v=True)
            if nmspSts == True:
                nmsp = mc.textScrollList('nmspList',q=True,si=True)
                NNsp = nmsp[0] + ':'
                prxCtrl = ctrls[i].split(' ')
                prxCtrl=NNsp + prxCtrl[0] + LR + prxCtrl[1]
                Ctrl.append(prxCtrl)
                #print prxCtrl
                
            else:
                prxCtrl = ctrls[i].split(' ')
                prxCtrl= prxCtrl[0] + LR + prxCtrl[1]
                Ctrl.append(prxCtrl)
                #print prxCtrl        
        
        #　ベイク処理
        sF=mc.playbackOptions(q=True, minTime=True)
        eF=mc.playbackOptions(q=True, maxTime=True)
        allF = eF + 1
        for j in range(int(sF),int(allF),1):
            mc.currentTime( int(j),e=True )
            if bakeType == 1:
                if partSts == 1:
                    match.armFkToIk()
                    # mc.select(Ctrl,r=True)
                    mc.setKeyframe(Ctrl)
                else:
                    match.legFkToIk()
                    # mc.select(Ctrl,r=True)
                    mc.setKeyframe(Ctrl)
            elif bakeType == 2:
                if partSts == 1:
                    match.armIkToFk()
                    # mc.select(Ctrl,r=True)
                    mc.setKeyframe(Ctrl)
                else:
                    match.legIkToFk()
                    # mc.select(Ctrl,r=True)
                    mc.setKeyframe(Ctrl)

                    
    #LRチェックボックスがOn,ArmLegチェックボックスがOff,Armを選択しているとき
    elif boolLR == True and boolArmLeg == False and Prts == 1:#
        bakeType = mc.radioButtonGrp( 'bakeType',q=True,select=True )
        
        lr = ['L','R']
        Ctrl=[]
        for LR in lr:
            bakeType = mc.radioButtonGrp( 'bakeType',q=True,select=True )
            if bakeType == 1:
                # print 'FK bake'
                ctrls = ['upArm_ _fkCtrl', 'arm_ _fkCtrl']
            elif bakeType == 2:
                # print 'IK bake'     
                ctrls = ['hand_ _Ctrl', 'arm_ _PVCtrl']
                    
            # セレクト用手足コントローラ群
            n=len(ctrls)
            for i in xrange(0,n,1):
                nmspSts = mc.checkBox('useNMspsChk',q=True,v=True)
                if nmspSts == True:
                    nmsp = mc.textScrollList('nmspList',q=True,si=True)
                    NNsp = nmsp[0] + ':'
                    prxCtrl = ctrls[i].split(' ')
                    prxCtrl=NNsp + prxCtrl[0] + LR + prxCtrl[1]
                    Ctrl.append(prxCtrl)
                    #print prxCtrl
                    
                else:
                    prxCtrl = ctrls[i].split(' ')
                    prxCtrl= prxCtrl[0] + LR + prxCtrl[1]
                    Ctrl.append(prxCtrl)
                    #print prxCtrl        
            
        #　ベイク処理
        sF=mc.playbackOptions(q=True, minTime=True)
        eF=mc.playbackOptions(q=True, maxTime=True)
        allF = eF + 1
        for j in range(int(sF),int(allF),1):
            mc.currentTime( int(j),e=True )
            if bakeType == 1:
                match.armFkToIkLR()
                # mc.select(Ctrl,r=True)
                mc.setKeyframe(Ctrl)
            elif bakeType == 2:
                match.armIkToFkLR()
                # mc.select(Ctrl,r=True)
                mc.setKeyframe(Ctrl)
                
    
    #LRチェックボックスがOn,ArmLegチェックボックスがOff,Legを選択しているとき
    elif boolLR == True and boolArmLeg == False and Prts == 2:#
        bakeType = mc.radioButtonGrp( 'bakeType',q=True,select=True )
        
        lr = ['L','R']
        Ctrl=[]
        for LR in lr:
            bakeType = mc.radioButtonGrp( 'bakeType',q=True,select=True )
            if bakeType == 1:
                # print 'FK bake'
                ctrls = ['upLeg_ _fkCtrl', 'leg_ _fkCtrl', 'foot_ _fkCtrl', 'toe_ _fkCtrl']
            elif bakeType == 2:
                # print 'IK bake'     
                ctrls = ['leg_ _Ctrl', 'leg_ _PVCtrl', 'toe_ _Ctrl']
                    
            # セレクト用手足コントローラ群
            n=len(ctrls)
            for i in xrange(0,n,1):
                nmspSts = mc.checkBox('useNMspsChk',q=True,v=True)
                if nmspSts == True:
                    nmsp = mc.textScrollList('nmspList',q=True,si=True)
                    NNsp = nmsp[0] + ':'
                    prxCtrl = ctrls[i].split(' ')
                    prxCtrl=NNsp + prxCtrl[0] + LR + prxCtrl[1]
                    Ctrl.append(prxCtrl)
                    #print prxCtrl
                    
                else:
                    prxCtrl = ctrls[i].split(' ')
                    prxCtrl= prxCtrl[0] + LR + prxCtrl[1]
                    Ctrl.append(prxCtrl)
                    #print prxCtrl        
            
        #　ベイク処理
        sF=mc.playbackOptions(q=True, minTime=True)
        eF=mc.playbackOptions(q=True, maxTime=True)
        allF = eF + 1
        for j in range(int(sF),int(allF),1):
            mc.currentTime( int(j),e=True )
            if bakeType == 1:
                match.legFkToIkLR()
                # mc.select(Ctrl,r=True)
                mc.setKeyframe(Ctrl)
            elif bakeType == 2:
                match.legIkToFkLR()
                # mc.select(Ctrl,r=True)
                mc.setKeyframe(Ctrl)
    
    #LRチェックボックスがOff,ArmLegチェックボックスがOnのとき
    elif boolLR == False and boolArmLeg == True:#
        sideSts = mc.radioButtonGrp( 'sideChk',q=True,select=True )
        if sideSts == 1:
            LR = 'L'
        else:
            LR = 'R'
        
        # Ikbake かFkbakeかの判定  パーツ判定と実行コマンド
        bakeType = mc.radioButtonGrp( 'bakeType',q=True,select=True )
        partSts = mc.radioButtonGrp( 'partsChk',q=True,select=True )

        
        if bakeType == 1:
            ctrls = ['upArm_ _fkCtrl', 'arm_ _fkCtrl','upLeg_ _fkCtrl', 'leg_ _fkCtrl', 'foot_ _fkCtrl', 'toe_ _fkCtrl']
        elif bakeType == 2:
            ctrls = ['hand_ _Ctrl', 'arm_ _PVCtrl','leg_ _Ctrl', 'leg_ _PVCtrl', 'toe_ _Ctrl']
            
        # セレクト用手足コントローラ群
        n=len(ctrls)
        Ctrl=[]
        for i in xrange(0,n,1):
            nmspSts = mc.checkBox('useNMspsChk',q=True,v=True)
            if nmspSts == True:
                nmsp = mc.textScrollList('nmspList',q=True,si=True)
                NNsp = nmsp[0] + ':'
                prxCtrl = ctrls[i].split(' ')
                prxCtrl=NNsp + prxCtrl[0] + LR + prxCtrl[1]
                Ctrl.append(prxCtrl)
                #print prxCtrl
                
            else:
                prxCtrl = ctrls[i].split(' ')
                prxCtrl= prxCtrl[0] + LR + prxCtrl[1]
                Ctrl.append(prxCtrl)
                #print prxCtrl        
        
        #　ベイク処理
        sF=mc.playbackOptions(q=True, minTime=True)
        eF=mc.playbackOptions(q=True, maxTime=True)
        allF = eF + 1
        for j in range(int(sF),int(allF),1):
            mc.currentTime( int(j),e=True )
            if bakeType == 1:
                match.armFkToIk()
                match.legFkToIk()
                # mc.select(Ctrl,r=True)
                mc.setKeyframe(Ctrl)
            elif bakeType == 2:
                match.armIkToFk()
                match.legIkToFk()
                # mc.select(Ctrl,r=True)
                mc.setKeyframe(Ctrl)

    
    #LRチェックボックスがOn,ArmLegチェックボックスがOnのとき
    elif boolLR == True and boolArmLeg == True:#
        bakeType = mc.radioButtonGrp( 'bakeType',q=True,select=True )
        
        lr = ['L','R']
        Ctrl=[]
        for LR in lr:
            bakeType = mc.radioButtonGrp( 'bakeType',q=True,select=True )
            if bakeType == 1:
                ctrls = ['upArm_ _fkCtrl', 'arm_ _fkCtrl','upLeg_ _fkCtrl', 'leg_ _fkCtrl', 'foot_ _fkCtrl', 'toe_ _fkCtrl']
            elif bakeType == 2:
                ctrls = ['hand_ _Ctrl', 'arm_ _PVCtrl','leg_ _Ctrl', 'leg_ _PVCtrl', 'toe_ _Ctrl']
                    
            # セレクト用手足コントローラ群
            n=len(ctrls)
            for i in xrange(0,n,1):
                nmspSts = mc.checkBox('useNMspsChk',q=True,v=True)
                if nmspSts == True:
                    nmsp = mc.textScrollList('nmspList',q=True,si=True)
                    NNsp = nmsp[0] + ':'
                    prxCtrl = ctrls[i].split(' ')
                    prxCtrl=NNsp + prxCtrl[0] + LR + prxCtrl[1]
                    Ctrl.append(prxCtrl)
                    #print prxCtrl
                    
                else:
                    prxCtrl = ctrls[i].split(' ')
                    prxCtrl= prxCtrl[0] + LR + prxCtrl[1]
                    Ctrl.append(prxCtrl)
                    #print prxCtrl        
            
        #　ベイク処理
        sF=mc.playbackOptions(q=True, minTime=True)
        eF=mc.playbackOptions(q=True, maxTime=True)
        allF = eF + 1
        for j in range(int(sF),int(allF),1):
            mc.currentTime( int(j),e=True )
            if bakeType == 1:
                match.legFkToIkLR()
                match.armFkToIkLR()
                # mc.select(Ctrl,r=True)
                mc.setKeyframe(Ctrl)
            elif bakeType == 2:
                match.legIkToFkLR()
                match.armIkToFkLR()
                # mc.select(Ctrl,r=True)
                mc.setKeyframe(Ctrl)
                
    viewChangeEnd()

