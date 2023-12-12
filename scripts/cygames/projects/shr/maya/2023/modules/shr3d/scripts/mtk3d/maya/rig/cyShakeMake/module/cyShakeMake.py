# -*- coding:utf-8 -*-
import maya.cmds as cmds, maya.OpenMaya as om , maya.cmds as mc
import random
from functools import partial

def setInterpolation(ui,*args):
    curveVal = cmds.gradientControlNoAttr( 'falloffCurve',q=True, civ=True)
    if curveVal == 0:
        mc.optionMenu("Menu_01",e=True,value="None")
    elif curveVal == 1 :
        mc.optionMenu("Menu_01",e=True,value="Linear")
    elif curveVal == 2:
        mc.optionMenu("Menu_01",e=True,value="Smooth")
    else:
        mc.optionMenu("Menu_01",e=True,value="Spline")

# callbacks for editing check boxes
def translateOnCallBack(ui, *args):
    ui.tX.setChecked(False)
    ui.tY.setChecked(False)
    ui.tZ.setChecked(False)

def translateOffCallBack(ui , *args):
    ui.translateShake.setChecked(False)

def rotateOnCallBack(ui , *args):
    ui.rX.setChecked(False)
    ui.rY.setChecked(False)
    ui.rZ.setChecked(False)

def rotateOffCallBack(ui,*args):
    ui.rotateShake.setChecked(False)
    

def Charactor_Set(ui,*args):
    selProject = cmds.optionMenu( "Menu_01" , q=True , v=True ) 
    if selProject == "None":
        cmds.gradientControlNoAttr( 'falloffCurve',e=True ,currentKeyInterpValue= 0)
        
    elif selProject == "Linear":
        cmds.gradientControlNoAttr( 'falloffCurve',e=True ,currentKeyInterpValue= 1)
        
    elif selProject == "Smooth":
        cmds.gradientControlNoAttr( 'falloffCurve',e=True ,currentKeyInterpValue= 2)
    else:
        cmds.gradientControlNoAttr( 'falloffCurve',e=True ,currentKeyInterpValue= 3)
        
def runShake(ui,  *args):
    
    #スタートフレームとエンドフレームを取得
    sliderStart = cmds.playbackOptions( query = True, min = True )
    sliderEnd = cmds.playbackOptions( query = True, max = True )
    
    #カレントタイムをシーンのスタート位置へ設定する
    cmds.currentTime( int(sliderStart) )
    
    #text fieldに入力した何フレームごとに揺れを適用するかの値を取得
    everyFrame = float(ui.PerFrameValue.text())
    
    if (float(everyFrame) < 1):
        return om.MGlobal.displayWarning( u'1フレーム以上の値を入力してください' )
    
    # creat seelction variable of object to have shake applied to
    selection = cmds.ls(sl=True)
    if len( selection ) == 0:
        return om.MGlobal.displayWarning( u'揺れを追加する対象を選択してください' )
    
    # start the main for loop for shake
    for i in selection:
        cmds.select( i )
        trg = i
        # query global keyframe interpolation settings and set them to linear
        # this is to optemise the results produced by arShake
        currentInKey = cmds.keyTangent( query = True, g=True )
        currentOutKey = cmds.keyTangent( query = True, g=True )
        cmds.keyTangent( g=True, inTangentType = 'linear' )
        cmds.keyTangent( g=True, outTangentType = 'linear' )
        time = cmds.currentTime(query = True)
        
        #アニメーションレイヤーがあるかを判定、なければ新たに作成
        animLayerExists = cmds.animLayer( i + '_ShakeLayer', query = True, exists = True )
        if animLayerExists:
            om.MGlobal.displayInfo( 'shake layer already exists, running now' )
        else:
            cmds.animLayer( i + '_ShakeLayer', attribute = ( i + '.translate', i + '.rotate', i + '.scale' )  )
            
        #適用する総フレーム数を算出
        totalSliderTime = int(sliderEnd) - time
        
        # make the available time a factor of 1
        divTime = 1 / totalSliderTime
        newDivTime = 0
        
        #translate shake のcheck boxの状態を取得
        translateShake = (ui.translateShake.isChecked())
                
        if translateShake == False:
            # query individual chack boxes for translate shake
            tX= (ui.tX.isChecked())      

            tY= (ui.tY.isChecked())

            tZ= (ui.tZ.isChecked())
           
        
        else:
            tX = False
            tY = False
            tZ = False
            
        #stF=int(ui.strFTxt.text())
        translateShakeAmount = int(ui.translateAmount.text())
                
        # query main chack box for rotate shake
        rotateShake = (ui.rotateShake.isChecked())
        if rotateShake == False:
            # query individual chack boxes for translate shake
            rX = (ui.rX.isChecked()) 
            rY = (ui.rY.isChecked())
            rZ = (ui.rZ.isChecked())       
        
        else:
            rX = False
            rY = False
            rZ = False
            
        #rotateShiveAmount = cmds.textField( 'rotateShiveAmount', query = True, text = True )
        rotateShiveAmount =  int(ui.rotateAmount.text())
        
        
        # This for loop calcuates the shake amount to be applied based on current time and the value of the falloff curve used.
        for i in range(int(time),int(sliderEnd) + 1):
            newDivTime+= divTime
            gradiantValue = cmds.gradientControlNoAttr( 'falloffCurve', query = True, valueAtPoint = newDivTime )
            
            
            useCurveTick = (ui.useCurve.isChecked())
            
            if useCurveTick:
                gradiantMultipler = gradiantValue
            else:
                gradiantMultipler = 1
            timePlus = cmds.currentTime(query = True)
            if timePlus <= int(sliderEnd):
                cmds.animLayer( trg + '_ShakeLayer', edit = True, mute = True )
                # translate shake starts here
                # make some nice random variables for the shaking!
                translateXRandom = (random.random() - 0.5 )
                translateYRandom = (random.random() - 0.5 )
                translateZRandom = (random.random() - 0.5 )
                # query the current translate values of the object
                currentTranslateX = cmds.getAttr( trg + '.translateX' )
                currentTranslateY = cmds.getAttr( trg + '.translateY' )
                currentTranslateZ = cmds.getAttr( trg + '.translateZ' )
                cmds.animLayer( trg + '_ShakeLayer', edit = True, mute = False )
                
                # based on the state of the check boxes, apply translate shake
                if tX or translateShake:
                    TraX = cmds.setKeyframe( animLayer = trg + '_ShakeLayer', 
                    value = currentTranslateX + ((translateXRandom * float(translateShakeAmount)) * gradiantMultipler), 
                    attribute = 'translateX' )
                 
                    
                else:
                    tXdone = False
                    
                if tY or translateShake:
                    cmds.setKeyframe( animLayer = trg + '_ShakeLayer', 
                    value = currentTranslateY + ((translateYRandom * float(translateShakeAmount)) * gradiantMultipler), 
                    attribute = 'translateY' )
                else:
                    tYdone = False
                if tZ or translateShake:
                    cmds.setKeyframe( animLayer = trg + '_ShakeLayer', 
                    value = currentTranslateZ + ((translateZRandom * float(translateShakeAmount)) * gradiantMultipler), 
                    attribute = 'translateZ' )
                else:
                    tZdone = False
                cmds.animLayer( trg + '_ShakeLayer', edit = True, mute = True )
                # rotate shake starts here
                # make some more random variables for the shaking!
                rotateRandomX = (random.random() -.5 )
                rotateRandomY = (random.random() -.5 )
                rotateRandomZ = (random.random() -.5 )
                currentRotateX = cmds.getAttr( trg + '.rotateX' )
                currentRotateY = cmds.getAttr( trg + '.rotateY' )
                currentRotateZ = cmds.getAttr( trg + '.rotateZ' )
                cmds.animLayer( trg + '_ShakeLayer', edit = True, mute = False )
                # based on the state of the check boxes, apply rotate shake
                # I found that if the current rotate value of the object were 0, it threw out he script
                if currentRotateX > 0.000001:
                    if rX or rotateShake:
                        cmds.setKeyframe( animLayer = trg + '_ShakeLayer', 
                        value = currentRotateX + ((rotateRandomX * float(rotateShiveAmount)) * gradiantMultipler ), 
                        attribute = 'rotateX' )
                    else:
                        rXdone = False
                if currentRotateX < 0.000001:
                    if rX or rotateShake:
                        cmds.setKeyframe( animLayer = trg + '_ShakeLayer', 
                        value = currentRotateX - ((rotateRandomX * float(rotateShiveAmount)) * gradiantMultipler ), 
                        attribute = 'rotateX' )
                    else:
                        rXdone = False
                if currentRotateY > 0.000001:
                    if rY or rotateShake:
                        cmds.setKeyframe( animLayer = trg + '_ShakeLayer', 
                        value = currentRotateY + ((rotateRandomY * float(rotateShiveAmount)) * gradiantMultipler ), 
                        attribute = 'rotateY' )
                    else:
                        rYdone = False
                if currentRotateY < 0.000001:
                    if rY or rotateShake:
                        cmds.setKeyframe( animLayer = trg + '_ShakeLayer', 
                        value = currentRotateY - ((rotateRandomY * float(rotateShiveAmount)) * gradiantMultipler ), 
                        attribute = 'rotateY' )
                    else:
                        rYdone = False
                if currentRotateZ > 0.000001:
                    if rZ or rotateShake:
                        cmds.setKeyframe( animLayer = trg + '_ShakeLayer', 
                        value = currentRotateZ + ((rotateRandomZ * float(rotateShiveAmount)) * gradiantMultipler ), 
                        attribute = 'rotateZ' )
                    else:
                        rZdone = False
                if currentRotateZ < 0.000001:
                    if rZ or rotateShake:
                        cmds.setKeyframe( animLayer = trg + '_ShakeLayer', 
                        value = currentRotateZ + ((rotateRandomZ * float(rotateShiveAmount)) * gradiantMultipler ), 
                        attribute = 'rotateZ' )
                    else:
                        rZdone = False
            else:
                om.MGlobal.displayInfo( 'reached end of loop' )
            #advance current time by amount specified in by frame text field
            cmds.currentTime( timePlus + int(everyFrame) )
        # once the loop has finished, reset the global keyframe interpolation to its original setting.
        cmds.keyTangent( g=True, inTangentType = currentInKey[0] )
        cmds.keyTangent( g=True, outTangentType = currentOutKey[1] )
        # set the current time back to the start time.
        cmds.currentTime( time )
        