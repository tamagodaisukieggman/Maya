import maya.cmds as cmds
#-------------------------------------------------------------------------------------------
#   Author: Hideyo Isayama
#   Copyright (c) 2009 Hideyo Isayama
#-------------------------------------------------------------------------------------------

import math

scriptPrifix="TkgSimplifyCurve."
infoSuffix="Information"
saveSuffix="_IsSaveCurve"

#-------------------------------------------------------------------------------------------
#   Disuplay User Interface
#-------------------------------------------------------------------------------------------
def UI():
    
    global scriptPrifix
    windowName=scriptPrifix.replace(".","")

    width=250+7
    height=597
    
    if cmds.window( windowName+"Win", exists=True ):
        cmds.deleteUI( windowName+"Win", window=True )
    if cmds.windowPref( windowName+"Win", exists=True ):
        cmds.windowPref( windowName+"Win", remove=True )

    cmds.window( windowName+"Win", title=windowName, widthHeight=(width, height),s=False)

    cmds.columnLayout()

    cmds.button(label="GraphEditor",w=250,command=scriptPrifix+"ViewGraphEditor()")
    cmds.button(label="Select Original Curve",w=250,command=scriptPrifix+"SelectOriginalKey()")

    cmds.separator( style='in',h=10,w=250)

    cmds.text(label=" Time Range Setting",al="left",fn="boldLabelFont",w=250)

    cmds.rowColumnLayout( numberOfColumns=4, columnWidth=[(1, 55), (2,65),(3, 65),(4, 65)])

    cmds.radioCollection()
    cmds.text(label="Range",al="center")
    cmds.radioButton("RangeSelect",label="Select",al="left",select=True,cc=scriptPrifix+"ChangeRange()")
    cmds.radioButton("RangeAll",label="All",al="left",cc=scriptPrifix+"ChangeRange()")
    cmds.radioButton("RangeTime",label="Time",al="left",cc=scriptPrifix+"ChangeRange()")    

    cmds.setParent( ".." )

    cmds.separator( style='in',h=10,w=250) 

    cmds.rowColumnLayout("TimeColumnLayout",numberOfColumns=3, columnWidth=[(1, 100), (2,100),(3, 50)],visible=False)

    cmds.text(label="StartFrame",al="center")
    cmds.text(label="EndFrame",al="center")
    cmds.text(label="",al="center")

    cmds.floatField("StartFrame",v=0)
    cmds.floatField("EndFrame",v=0)
    cmds.button(label="Get",command=scriptPrifix+"GetFrame()")

    cmds.setParent( ".." )
    
    cmds.separator( style='in',h=10,w=250)    

    cmds.text(label=" Check Tangent Setting",al="left",fn="boldLabelFont",w=250)
    cmds.floatSliderGrp("TangentLength" ,l="Length",min=0, max=2, value=0.5, step=0.1,w=250,field=True,cw3=[50,40,1] )
    cmds.floatSliderGrp("TangentAngle",l="Angle" ,min=0, max=180, value=45, step=0.1,w=250,field=True,cw3=[50,40,1] )

    cmds.separator( style='in',h=10,w=250)

    cmds.text(label=" Same Key Setting",al="left",fn="boldLabelFont",w=250)

    cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 50), (2,100), (3,90), (4,10)])
    
    cmds.radioCollection()
    cmds.text(l="Same",al="center")
    cmds.radioButton("SameKeyOn",al="left",label="All",cc=scriptPrifix+"ChangeSameKey()")
    cmds.radioButton("SameKeyOff",al="left",label="Individual",select=True,cc=scriptPrifix+"ChangeSameKey()")
    cmds.text(l="")

    cmds.setParent( ".." )

    cmds.separator( style='in',h=10,w=250)

    cmds.text(label=" Round Range Setting",al="left",fn="boldLabelFont",w=250)
    cmds.intSliderGrp("CurveRoundRange",l="Curve" ,min=0, max=20, value=1, step=1,w=250,field=True,cw3=[50,40,1] )
    cmds.intSliderGrp("AllRoundRange",l="All" ,min=0, max=20, value=3, step=1,w=250,field=True,cw3=[50,40,1],enable=False)

    cmds.text(label=" Round Important Key",al="center")
    cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 50), (2,100), (3,90), (4,10)])
    
    cmds.radioCollection()
    cmds.text(l="")
    cmds.radioButton("RoundImportantOn",al="left",label="Yes",enable=False)
    cmds.radioButton("RoundImportantOff",al="left",label="No",select=True,enable=False)
    cmds.text(l="")

    cmds.setParent( ".." )

    cmds.separator( style='in',h=10,w=250)

    cmds.text(label=" Additional Key Setting",al="left",fn="boldLabelFont",w=250)

    cmds.intSliderGrp("AddKeyCheckNum",l="Check" ,min=0, max=10, value=3, step=1,w=250,field=True,cw3=[50,40,1])
    cmds.floatSliderGrp("AddKeyPercent" ,l="Percent",min=0.00, max=1.00, value=0.90, step=0.01,w=250,field=True,cw3=[50,40,1])
    cmds.floatSliderGrp("AddKeyRange",l="Range" ,min=0.01, max=5.00, value=0.10, step=0.01,w=250,field=True,cw3=[50,40,1] )

    cmds.separator( style='in',h=10,w=250)

    cmds.text(label=" Original Key Setting",al="left",fn="boldLabelFont",w=250)

    cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 50), (2,100), (3,90), (4,10)])
    
    cmds.radioCollection()
    cmds.text(l="Save",al="center")
    cmds.radioButton("OriginalSaveOn",al="left",label="Yes")
    cmds.radioButton("OriginalSaveOff",al="left",label="No",select=True)
    cmds.text(l="")

    cmds.setParent( ".." )    
    
    cmds.separator( style='in',h=10,w=250)

    cmds.button(label="Reset",w=250,command=scriptPrifix+"Reset()")
    cmds.button(label="Make Simple Curve",w=250,h=30,bgc=(1,0.8,0.8),command=scriptPrifix+"MakeCurve()")

    cmds.progressBar("ProgressBarS",maxValue=100, width=250,h=7,step=0)
    cmds.progressBar("ProgressBarL",maxValue=100, width=250,h=10,step=0)

    cmds.showWindow(windowName+"Win")

    GetFrame()


#-------------------------------------------------------------------------------------------
#   Make Curve
#-------------------------------------------------------------------------------------------
def MakeCurve():

    rangeSelect=cmds.radioButton("RangeSelect",query=True,select=True)
    rangeAll=cmds.radioButton("RangeAll",query=True,select=True)
    rangeTime=cmds.radioButton("RangeTime",query=True,select=True)

    sameKey=cmds.radioButton("SameKeyOn",query=True,select=True)

    startFrame=cmds.floatField("StartFrame",query=True,v=True)
    endFrame=cmds.floatField("EndFrame",query=True,v=True)

    tangentLength=cmds.floatSliderGrp("TangentLength" ,query=True,value=True)
    tangentAngle=cmds.floatSliderGrp("TangentAngle",query=True,value=True)

    curveRoundRange=cmds.intSliderGrp("CurveRoundRange",query=True, value=True)
    allRoundRange=cmds.intSliderGrp("AllRoundRange",query=True,value=True)
    roundImportantKey=cmds.radioButton("RoundImportantOn",query=True,select=True)

    addKeyCheckNum=cmds.intSliderGrp("AddKeyCheckNum",query=True,value=True)
    addKeyPercent=cmds.floatSliderGrp("AddKeyPercent",query=True,value=True)
    addKeyRange=cmds.floatSliderGrp("AddKeyRange",query=True,value=True)

    originalSave=cmds.radioButton("OriginalSaveOn",query=True,select=True)
    
    selectList=cmds.ls(sl=True,l=True)
    curveList=cmds.keyframe(query=True,selected=True,name=True)
    timeList=cmds.keyframe(query=True,selected=True,tc=True,a=True)
    
    if curveList==None:
        return "Select Animation Curves !"

    if timeList==None:
        return "Select Key Frames !"

    timeList.sort()

    newCurveList=[]
    for cnt in range(0,len(curveList)):

        if curveList[cnt].find(saveSuffix)>=0:
            continue

        newCurveList.append(curveList[cnt])

    curveList=newCurveList


    if originalSave==True:
        SaveOriginalKey(curveList)  

    
    keyValueList=[]
    if sameKey==True:        
        keyValueList=MakeKeyValueList(curveList,tangentLength,tangentAngle,curveRoundRange,allRoundRange,roundImportantKey,addKeyCheckNum,addKeyPercent,addKeyRange)

    cmds.progressBar("ProgressBarL",edit=True,max=len(curveList))
    for cnt in range(0,len(curveList)):

        if sameKey==False:
            keyValueList=MakeKeyValueList([curveList[cnt]],tangentLength,tangentAngle,curveRoundRange,0,roundImportantKey,addKeyCheckNum,addKeyPercent,addKeyRange)
        
        thisKeyValueList=GetValueFromCurve(keyValueList,curveList[cnt])

        if rangeAll==True:
            curveList[cnt]=KeyFromKeyList(thisKeyValueList,curveList[cnt],None)
        elif rangeSelect==True:
            curveList[cnt]=KeyFromKeyList(thisKeyValueList,curveList[cnt],[timeList[0],timeList[len(timeList)-1]])
        elif rangeTime==True:
            curveList[cnt]=KeyFromKeyList(thisKeyValueList,curveList[cnt],[startFrame,endFrame])

        cmds.progressBar("ProgressBarL",edit=True,progress=cnt+1)

    cmds.progressBar("ProgressBarL",edit=True,progress=0)

    cmds.select(cl=True)
    cmds.select(selectList,r=True)
    for cnt in range(0,len(curveList)):        
        cmds.selectKey(curveList[cnt],add=True)
        



#-------------------------------------------------------------------------------------------
#   Get value from time slider and applay the value to the form
#-------------------------------------------------------------------------------------------
def GetFrame():
    
    minTimeValue=float(cmds.playbackOptions(query=True,minTime=True))
    maxTimeValue=float(cmds.playbackOptions(query=True,maxTime=True))

    cmds.floatField("StartFrame",edit=True,v=float(minTimeValue))
    cmds.floatField("EndFrame",edit=True,v=float(maxTimeValue))



#-------------------------------------------------------------------------------------------
#   Display grapheditor
#-------------------------------------------------------------------------------------------
def ViewGraphEditor():
    cmds.GraphEditor()



#-------------------------------------------------------------------------------------------
#   Get time range from time slider
#-------------------------------------------------------------------------------------------
def ChangeRange():

    select=cmds.radioButton("RangeTime",query=True,select=True)
    cmds.rowColumnLayout("TimeColumnLayout",edit=True,visible=select)

#-------------------------------------------------------------------------------------------
#   Get time range from time slider
#-------------------------------------------------------------------------------------------
def ChangeSameKey():

    select=cmds.radioButton("SameKeyOn",query=True,select=True)
    cmds.intSliderGrp("AllRoundRange",edit=True,enable=select)
    cmds.radioButton("RoundImportantOn",edit=True,enable=select)
    cmds.radioButton("RoundImportantOff",edit=True,enable=select)


#-------------------------------------------------------------------------------------------
#   reset
#-------------------------------------------------------------------------------------------
def Reset():
    cmds.radioButton("RangeSelect",edit=True,select=True)

    cmds.radioButton("SameKeyOff",edit=True,select=True)

    cmds.floatSliderGrp("TangentLength",edit=True,value=0.5)
    cmds.floatSliderGrp("TangentAngle",edit=True,value=45)

    cmds.intSliderGrp("CurveRoundRange",edit=True, value=1)
    cmds.intSliderGrp("AllRoundRange",edit=True,value=3)

    cmds.radioButton("RoundImportantOff",edit=True,select=True)

    cmds.intSliderGrp("AddKeyCheckNum",edit=True,value=3)
    cmds.floatSliderGrp("AddKeyPercent",edit=True,value=0.9)
    cmds.floatSliderGrp("AddKeyRange",edit=True,value=0.10)

    cmds.radioButton("OriginalSaveOff",edit=True,select=True)

    GetFrame()
    ChangeRange()
    ChangeSameKey()


#-------------------------------------------------------------------------------------------
#   Set key from keyValueList
#-------------------------------------------------------------------------------------------
def KeyFromKeyList(keyValueList,targetCurve,timeRange):

    thisCurveKeyList=cmds.keyframe(targetCurve,query=True,a=True,tc=True)
    
    nodeList=cmds.listConnections(targetCurve,p=True)

    if nodeList==None:
        return "Curve do not have any node !"

    cmds.selectKey(targetCurve,r=True,k=True)

    if timeRange==None:
        cmds.cutKey(targetCurve,cl=True)
    else:        
        cmds.cutKey(targetCurve,time=(timeRange[0],timeRange[1]))


    keyList=[]
    valueList=[]    
    inAngleList=[]
    outAngleList=[]
    for cnt in range(0,len(keyValueList)):

        if len(thisCurveKeyList)>1:
            if keyValueList[cnt][0]<thisCurveKeyList[0] or keyValueList[cnt][0]>thisCurveKeyList[len(thisCurveKeyList)-1]:
                continue

        if timeRange==None:            
            keyList.append(keyValueList[cnt][0])
            valueList.append(keyValueList[cnt][1])
            inAngleList.append(keyValueList[cnt][2])
            outAngleList.append(keyValueList[cnt][3])
        else:
            if keyValueList[cnt][0]>=timeRange[0] and keyValueList[cnt][0]<=timeRange[1]:
                keyList.append(keyValueList[cnt][0])
                valueList.append(keyValueList[cnt][1])
                inAngleList.append(keyValueList[cnt][2])
                outAngleList.append(keyValueList[cnt][3])    

    cmds.setKeyframe(nodeList[0],time=keyList,value=0)
    
    thisNewCurve=None
    thisNewCurve=cmds.listConnections(nodeList[0],d=True,t="animCurve")

    cmds.setKeyframe(nodeList[0],time=keyList,value=0)

    for cnt in range(0,len(keyList)):
        cmds.keyframe(thisNewCurve[0],edit=True,a=True,t=(keyList[cnt],keyList[cnt]),vc=valueList[cnt])
        cmds.keyTangent(thisNewCurve[0],edit=True,a=True,t=(keyList[cnt],keyList[cnt]),itt="spline",ia=inAngleList[cnt],lock=False)
        cmds.keyTangent(thisNewCurve[0],edit=True,a=True,t=(keyList[cnt],keyList[cnt]),ott="spline",oa=outAngleList[cnt],lock=False)

    return thisNewCurve



#-------------------------------------------------------------------------------------------
#   Caluculate inangle and outangle from key
#-------------------------------------------------------------------------------------------
def SearchKeySlope(key,slopeRange,targetCurve):

    nodeList=cmds.listConnections(targetCurve,p=True)

    if nodeList==None:
        return "Curve do not have any node !"
    

    resultSlope=[0,0]

    sourceValue=cmds.getAttr(nodeList[0],time=key)
    sourceValueIn=cmds.getAttr(nodeList[0],time=key-slopeRange)
    sourceValueOut=cmds.getAttr(nodeList[0],time=key+slopeRange)    

    slopeIn=(sourceValue-sourceValueIn)/(slopeRange)   
    slopeOut=(sourceValueOut-sourceValue)/(slopeRange)

    angleIn=math.degrees(math.atan(slopeIn))
    angleOut=math.degrees(math.atan(slopeOut))

    resultSlope[0]=angleIn
    resultSlope[1]=angleOut

    return resultSlope



#-------------------------------------------------------------------------------------------
#   Get important key from animation curve
#-------------------------------------------------------------------------------------------
def SearchImportantKey(targetCurve,slopeRange,angleRange):
    
    nodeList=cmds.listConnections(targetCurve,p=True)

    if nodeList==None:
        return "Curve do not have any node !"

    keyframeList=cmds.keyframe(targetCurve,query=True,tc=True)

    if keyframeList==None:
        return "Cannot find any key !"


    keyValueList=[]
    for key in range(int(keyframeList[0]),int(keyframeList[len(keyframeList)-1]+1)):

        sourceValue=cmds.getAttr(nodeList[0],time=key)
        slopeValue=SearchKeySlope(key,slopeRange,nodeList[0])        
        keyValueList.append([key,sourceValue,slopeValue[0],slopeValue[1],True])
        


    importantKeyValueList=[]
    previousSlope=[0,0]
    for cnt in range(0,len(keyValueList)):

        if cnt==0 or cnt==len(keyValueList)-1:
            importantKeyValueList.append(keyValueList[cnt])

        if math.fabs(keyValueList[cnt][3]-keyValueList[cnt][2])>angleRange:
            importantKeyValueList.append(keyValueList[cnt])      
        elif keyValueList[cnt][2]*previousSlope[0]<0 or keyValueList[cnt][3]*previousSlope[1]<0:
            importantKeyValueList.append(keyValueList[cnt])
        
        previousSlope=[keyValueList[cnt][2],keyValueList[cnt][3]]
        

    return importantKeyValueList




#-------------------------------------------------------------------------------------------
#   Update similarities
#-------------------------------------------------------------------------------------------
def AddKeyToKeyValueList(keyValueList,targetCurve,minPercent,distanceRange):

    global scriptPrifix
    
    dummyGroup=cmds.group(name="DummyObjectForCurveCoxpy",em=True)
    dummyGroupAttr=dummyGroup+".translateX"    
    cmds.setKeyframe(dummyGroup)
    dummyGroupCurve=cmds.listConnections(dummyGroupAttr,type="animCurve")[0]
    dummyGroupCurve=KeyFromKeyList(keyValueList,dummyGroupCurve,None)    

    sourceNodeList=cmds.listConnections(targetCurve,p=True)

    if sourceNodeList==None:
        return "SourceCurve do not have any node !"

    resultKeyValueList=keyValueList
    totalPercent=0.0
    totalNum=0.0
    for cnt in range(0,len(keyValueList)-1):

        if keyValueList[cnt][0]==keyValueList[cnt+1][0]:
            continue
        
        compare=CompareCurveValue(targetCurve,dummyGroupCurve,(keyValueList[cnt][0],keyValueList[cnt+1][0]),distanceRange)

        totalPercent+=float(compare)
        totalNum+=1
        
        if compare<minPercent:
            newKey=(keyValueList[cnt][0]+keyValueList[cnt+1][0])/2
            newKey=int(newKey)            
            resultKeyValueList.append([newKey,0,0,0,False])

    cmds.delete(dummyGroup)

    resultKeyValueList.sort()
    resultKeyValueList=GetValueFromCurve(resultKeyValueList,targetCurve)

    return resultKeyValueList
            
        
#-------------------------------------------------------------------------------------------
#   Caluculate keyValueList again from previous keyValueList
#-------------------------------------------------------------------------------------------
def GetValueFromCurve(keyValueList,targetCurve):
    
    nodeList=cmds.listConnections(targetCurve,p=True)

    if nodeList==None:
        return "Curve do not have any node !"

    keyframeList=cmds.keyframe(targetCurve,query=True,tc=True)

    if keyframeList==None:
        return "Cannot find any key !"


    resultKeyValueList=[]
    for cnt in range(0,len(keyValueList)):
        
        sourceValue=cmds.getAttr(nodeList[0],time=keyValueList[cnt][0])
        slopeValue=SearchKeySlope(keyValueList[cnt][0],0.1,nodeList[0])        
        resultKeyValueList.append([keyValueList[cnt][0],sourceValue,slopeValue[0],slopeValue[1],keyValueList[cnt][4]])

    return resultKeyValueList        
        

#-------------------------------------------------------------------------------------------
#   Caluculate similarities between sourceCurve and destCurve
#-------------------------------------------------------------------------------------------
def CompareCurveValue(sourceCurve,destCurve,timeRange,distanceRange):

    sourceNodeList=cmds.listConnections(sourceCurve,p=True)

    if sourceNodeList==None:
        return "SourceCurve do not have any node !"

    destNodeList=cmds.listConnections(destCurve,p=True)

    if destNodeList==None:
        return "DestCurve do not have any node !"

    resultPercent=0.00

    totalNum=0.00
    equalNum=0.00
    for key in range(timeRange[0],timeRange[1]):
        
        floatKey=float(key)
        sourceValue=cmds.getAttr(sourceNodeList[0],time=key)
        destValue=cmds.getAttr(destNodeList[0],time=key)
        difference=math.fabs(sourceValue-destValue)

        totalNum+=1
        
        if difference<distanceRange:
            equalNum+=1

    resultPercent=0
    if totalNum!=0:
        resultPercent=equalNum/totalNum
    
    return resultPercent


#-------------------------------------------------------------------------------------------
#   Round keyValueList
#-------------------------------------------------------------------------------------------
def RoundKeyValueList(keyValueList,sameValueRange,roundImportantKey):
    roundKeyList=[]
    previousKey=[-9999999,0,0,0]
    for cnt in range(0,len(keyValueList)):

        if keyValueList[cnt][0]>previousKey[0]+sameValueRange:
            roundKeyList.append(keyValueList[cnt])
            previousKey=keyValueList[cnt]

        if roundImportantKey==False:        
            if keyValueList[cnt][4]==True:
                roundKeyList.append(keyValueList[cnt])

    roundKeyList.append(keyValueList[0])
    roundKeyList.append(keyValueList[len(keyValueList)-1])

    roundKeyList.sort()
            
    return roundKeyList



#-------------------------------------------------------------------------------------------
#   Make KeyValueList
#-------------------------------------------------------------------------------------------
def MakeKeyValueList(curveList,tangentLength,tangentAngle,curveRoundRange,allRoundRange,roundImportantKey,addKeyCheckNum,addKeyPercent,addKeyRange):

    cmds.progressBar("ProgressBarS",edit=True,max=len(curveList))
    
    allKeyValueList=[]
    for cnt in range(0,len(curveList)):
        thisKeyValueList=SearchImportantKey(curveList[cnt],tangentLength,tangentAngle)
        thisKeyValueList=RoundKeyValueList(thisKeyValueList,curveRoundRange,True)
        thisKeyValueList=GetValueFromCurve(thisKeyValueList,curveList[cnt])

        for cnt2 in range(0,addKeyCheckNum):
            thisKeyValueList=AddKeyToKeyValueList(thisKeyValueList,curveList[cnt],addKeyPercent,addKeyRange)

        allKeyValueList.extend(thisKeyValueList)

        cmds.progressBar("ProgressBarS",edit=True,progress=cnt+1)

    allKeyValueList.sort()

    allKeyValueList=RoundKeyValueList(allKeyValueList,allRoundRange,roundImportantKey)

    cmds.progressBar("ProgressBarS",edit=True,progress=0)
            
    return allKeyValueList

#-------------------------------------------------------------------------------------------
#   Save original key
#-------------------------------------------------------------------------------------------
def SaveOriginalKey(curveList):

    global scriptPrifix
    global infoSuffix
    global saveSuffix

    rootName=scriptPrifix.replace(".","")+infoSuffix
    
    if cmds.objExists(rootName)==False:
        cmds.group(name=scriptPrifix.replace(".","")+infoSuffix,em=True)

    if curveList==None:
        return "Select Animation Curves ! !"

    for cnt in range(0,len(curveList)):

        nodeList=cmds.listConnections(curveList[cnt],p=True)
        nodeName=cmds.ls(nodeList[0],l=True)

        if nodeName[0].find(saveSuffix)>=0:
            continue            
        
        thisName=nodeName[0].replace("|","_l_").replace(".","_o_")+saveSuffix
        globalName="|"+rootName+"|"+thisName

        if cmds.objExists(globalName)==False:
            cmds.group(em=True,name=thisName)
            cmds.parent(thisName,rootName)

        cmds.cutKey(thisName+".translateX")
        cmds.copyKey(curveList[cnt])        
        cmds.pasteKey(thisName+".translateX")

    
#-------------------------------------------------------------------------------------------
#   Select original key
#-------------------------------------------------------------------------------------------
def SelectOriginalKey():
    
    global scriptPrifix
    global infoSuffix
    global saveSuffix

    selectList=cmds.ls(sl=True,l=True)
    curveList=cmds.keyframe(query=True,sl=True,name=True)

    rootName=scriptPrifix.replace(".","")+infoSuffix

    if cmds.objExists(rootName)==False:
        return "Save Infomation !"

    if curveList==None:
        return "Select Animation Curves ! !"

    cmds.selectKey(cl=True)
    cmds.select(cl=True)

    cmds.select(selectList,r=True)
    for cnt in range(0,len(curveList)):

        nodeList=cmds.listConnections(curveList[cnt],p=True)
        nodeName=cmds.ls(nodeList[0],l=True)

        if nodeName[0].find(saveSuffix)>=0:
            continue  
        
        thisName=nodeName[0].replace("|","_l_").replace(".","_o_")+saveSuffix
        globalName="|"+rootName+"|"+thisName

        if cmds.objExists(globalName)==True:
            dummyCurveList=cmds.listConnections(globalName,d=True,t="animCurve")
            
            cmds.select(globalName,add=True)
            
            cmds.selectKey(dummyCurveList[0],add=True)
            cmds.selectKey(curveList[cnt],add=True)
