import maya.cmds as cmds

'''
Tool Created by Ignacio Zorrilla

Copy this python file to you maya scipts folder, usually located under user/documents/maya/version/scripts

Run this in Maya's python script editor to run the tool

import IKSpline
import imp
imp.reload(IKSpline)
IKSpline.UI()
'''

bindJoints = []
FKJoints = []
IKJoints = []
DriverIKJoints = []
FKCC= []
IKCC = []
HybridIKCC = []
FKLocatorList = []
IKLocatorList = []
HybridIKLocatorList = []


def UI():
    windowID = "IKSpline_UI"
    if(cmds.window(windowID,q = True, exists = True)):
        cmds.deleteUI(windowID)

    window = cmds.window(windowID, title = "IK Spline Window", rtf = True, s = True)
    windowLayout = cmds.columnLayout(co = ("both", 10))

    #create IKFK Chain section UI
    cmds.setParent(windowID)
    IKFKLayout = cmds.frameLayout(l = "Naming Convenction", cll = True, w = 320)
    cmds.text(h = 5, l = "")
    cmds.text(l = "  Determine the naming for all alements", al = "left")
    cmds.separator(h = 5)

    cmds.setParent(IKFKLayout)
    cmds.rowColumnLayout(nc = 2)
    cmds.text(l = "  Joint name:  ", al = "left")
    JointNameField = cmds.textField(vis = True, ed = True, w = 120, tx = "bn")
    cmds.text(l = "  Controller name:  ", al = "left")
    CCNameField = cmds.textField(vis = True, ed = True, w = 120, tx = "cc")
    cmds.text(l = "  Locator name:  ", al = "left")
    LocatorNameField = cmds.textField(vis = True, ed = True, w = 120, tx = "locAlign")
    cmds.text(l = "  Group name:  ", al = "left")
    GroupNameField = cmds.textField(vis = True, ed = True, w = 120, tx = "grp")
    cmds.text(h = 10, l = "")
    cmds.text(h = 10, l = "")

    #Create IK Spline Rig Section UI
    cmds.setParent(windowID)
    IKLayout = cmds.frameLayout(l = "Create IK Spline Rig", cll = True, collapse = False, w = 320)
    cmds.text(h = 5, l = "")
    cmds.text(l = "  Create the Rig chain", al = "left")

    cmds.separator(h = 5)

    cmds.setParent(windowID)
    cmds.setParent(IKLayout)
    cmds.rowColumnLayout(nc = 2)
    cmds.text(l = "  Name:       ", al = "left")
    NameField = cmds.textField(vis = True, ed = True, w = 200, tx = "Tail")
    cmds.setParent(IKLayout)
    #Bones and Controller Number Section

    BonesNumberSlider = cmds.intSliderGrp(l = "  Number of Bones:", min = 0, max = 50, field = True, ad3 = True, cw3 = [50, 30, 200], cl3 = ["left","left","left"], v = 5)
    ControllerNumberSlider = cmds.intSliderGrp(l = "  Number of Controllers:", min = 0, max = 50, field = True, ad3 = True, cw3 = [50, 30, 200], cl3 = ["left","left","left"], v = 3)
    cmds.setParent(IKLayout)

    cmds.rowColumnLayout(nc = 2)
    cmds.text(l = "  Controller Scale:    ", al = "left")
    CCScaleField = cmds.textField(vis = True, ed = True, w = 50, tx = "1")
    cmds.setParent(IKLayout)

    cmds.separator(h = 10)

    cmds.rowColumnLayout(nc = 5)
    RigType = cmds.radioCollection()
    cmds.text(h = 5, l = "          ")
    FKRig = cmds.radioButton("FK       ", al = "center")
    IKRig = cmds.radioButton("IK       ", al = "center")
    IKFKRig = cmds.radioButton("IKFK     ", al = "center")
    IKFKHybridRig = cmds.radioButton("Hybrid IKFK", al = "center", sl = True)

    cmds.setParent(IKLayout)

    cmds.separator(h = 10)

    StretchyLayout = cmds.rowColumnLayout(nc = 2)
    stretchyBtn = cmds.checkBox( l = " Stretchy IK", v = True, onc = lambda *x: Show(StretchyScale, StretchyTranslate), ofc = lambda *x: Hide(StretchyScale, StretchyTranslate))
    cmds.text(h = 5, l = "")
    cmds.rowColumnLayout(nc = 2, columnWidth =[(1, 120)])
    StretchyMode = cmds.radioCollection()
    StretchyTranslate = cmds.radioButton("Translate", sl = True)
    StretchyScale = cmds.radioButton("Scale")
    cmds.setParent(IKLayout)

    bnName = JointNameField
    CCName = CCNameField
    LocatorName = LocatorNameField
    grpName = GroupNameField
    jointsNumVar = BonesNumberSlider
    CCNumVar = ControllerNumberSlider
    nameVar = NameField
    rigType = RigType
    CCScale = CCScaleField
    SquashStretch = stretchyBtn
    stretchyType = StretchyMode

    cmds.separator(h = 10)

    cmds.text(l = "  Select a NURBS Curve or nothing and create guides", al = "left")
    cmds.button(l = "GUIDES", w = 300, h = 50, c = lambda *x: IKFKSplineGuides())

    cmds.text(l = "  Create Rig", al = "left")
    cmds.button(l = "CREATE", w = 300, h = 50, c = lambda *x: IKFKSplineRig(bnName, CCName, LocatorName, grpName, jointsNumVar, CCNumVar, nameVar, rigType, CCScale,  SquashStretch, stretchyType, IKCCSHape, FKCCSHape, IKColor, FKColor))

    cmds.text(h = 12, l = "")

    #Change Controllers section UI
    cmds.setParent(windowID)
    CClayout = cmds.frameLayout(l = "Change Controllers (Optional)", cll = True, collapse = True, w = 320)
    cmds.text(h = 5, l = "")
    cmds.text(l = "  Change the shape and collor of IK and FK Controllers", al = "left")
    cmds.text(h = 5, l = "")
    cmds.text(l = "  Shape:", al = "left")
    cmds.rowColumnLayout(nc = 2)
    cmds.text(l = "  IK Controller:         ")
    IKCCSHape = cmds.optionMenu(w = 150)
    cmds.menuItem( label='Cube')
    cmds.menuItem( label='Circle')
    cmds.menuItem( label='Star')
    cmds.menuItem( label='Square')
    cmds.menuItem( label='Diamond')
    cmds.menuItem( label='Plus')
    cmds.text(l = "  FK Controller:         ")
    FKCCSHape = cmds.optionMenu(w = 150)
    cmds.menuItem( label='Circle')
    cmds.menuItem( label='Cube')
    cmds.menuItem( label='Star')
    cmds.menuItem( label='Square')
    cmds.menuItem( label='Diamond')
    cmds.menuItem( label='Plus')
    cmds.text(h = 20, l = "")
    cmds.text(h = 20, l = "")

    cmds.text(l = " IK Color:", al = "left")
    IKColor = cmds.optionMenu(w = 150)
    cmds.menuItem( label='Yellow')
    cmds.menuItem( label='Red')
    cmds.menuItem( label='Blue')
    cmds.menuItem( label='Green')
    cmds.menuItem( label='LightBlue')
    cmds.menuItem( label='Pink')

    cmds.text(l = " FK Color:", al = "left")
    FKColor = cmds.optionMenu(w = 150)
    cmds.menuItem( label='Red')
    cmds.menuItem( label='Blue')
    cmds.menuItem( label='Yellow')
    cmds.menuItem( label='Green')
    cmds.menuItem( label='LightBlue')
    cmds.menuItem( label='Pink')

    cmds.text(h = 10, l = "")
    cmds.setParent(windowID)

    #SHOW WINDOW
    cmds.showWindow(windowID)

def Show(StretchyScale, StretchyTranslate):
    cmds.radioButton(StretchyScale, e = True, vis = True )
    cmds.radioButton(StretchyTranslate,  e = True, vis = True)

def Hide(StretchyScale, StretchyTranslate):
    cmds.radioButton(StretchyScale, e = True, vis = False)
    cmds.radioButton(StretchyTranslate, e = True, vis = False)

def createController(CCSHape, Color, Scale):

    #Define Color variables
    if Color == "Red":
        colorCode = 13
    if Color == "Pink":
        colorCode = 9
    if Color == "Green":
        colorCode = 14
    elif Color == "Blue":
        colorCode = 6
    elif Color == "Yellow":
        colorCode = 17
    elif Color == "LightBlue":
        colorCode = 18

    #Create Controllers
    if CCSHape == "Cube":
        Controller = cmds.curve(p=[(-1.0, 1.0, 1.0), (-1.0, 1.0, -1.0), (1.0, 1.0, -1.0),
                         (1.0, 1.0, 1.0), (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0),
                         (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, -1.0, -1.0),
                         (-1.0, -1.0, 1.0), (-1.0, -1.0, -1.0), (-1.0, 1.0, -1.0),
                         (1.0, 1.0, -1.0), (1.0, -1.0, -1.0), (1.0, -1.0, 1.0), (1.0, 1.0, 1.0)],
                         k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], d=1, n= "temp_cc_name")

    if CCSHape == "Circle":
        Controller = cmds.circle(d = 3, n= "temp_cc_name")
        cmds.select(Controller[0] + ".cv[0:7]")
        cmds.rotate(0, 90, 0)

    if CCSHape == "Star":
        Controller = cmds.circle(d = 3, n= "temp_cc_name")
        cmds.select(Controller[0] + ".cv[2]", Controller[0] + ".cv[0]", Controller[0] + ".cv[4]", Controller[0] + ".cv[6]")
        cmds.scale(0, 0, 0, r = True)
        cmds.select(Controller[0] + ".cv[0:7]")
        cmds.rotate(0, 90, 0)
        cmds.scale(2, 2, 2, r = True)
        cmds.select(cl = True)

    if CCSHape == "Square":
        Controller = cmds.curve(d=1, p=[(-1,0,-1),(1,0,-1),(1,0,1),(-1,0,1), (-1,0,-1)], k=[0,1,2,3,4], n= "temp_cc_name")
        cmds.select(Controller + ".cv[0:4]")
        cmds.rotate(0, 0, 90)
        cmds.move(-1, 0, 0, r = True, os = True, wd = True)

    if CCSHape == "Diamond":
        Controller = cmds.curve(d=1, p=[(0, 1, 0),(-1, 0.00278996, 6.18172e-08),(0, 0, 1),(0, 1, 0),(1, 0.00278996, 0),
            (0, 0, 1),(1, 0.00278996, 0),(0, 0, -1),(0, 1, 0),(0, 0, -1),
            (-1, 0.00278996, 6.18172e-08),(0, -1, 0),(0, 0 ,-1),(1, 0.00278996, 0),
            (0, -1, 0),(0, 0, 1)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], n = "temp_cc_name")

    if CCSHape == "Plus":
        Controller = cmds.curve(d=1, p=[(-1,0,-3),(1,0,-3),(1,0,-1),(3,0,-1),(3,0,1),(1,0,1),(1,0,3),(-1,0,3),(-1,0,1),(-3,0,1),(-3,0,-1),(-1,0,-1),(-1,0,-3)], k=[0,1,2,3,4,5,6,7,8,9,10,11,12], n = "temp_cc_name")

    ControllerList = cmds.ls(Controller)
    shapes = cmds.listRelatives(ControllerList, s = True)


    #Change Controller Scale
    cmds.setAttr(ControllerList[0] + ".scaleX", float(Scale))
    cmds.setAttr(ControllerList[0] + ".scaleY", float(Scale))
    cmds.setAttr(ControllerList[0] + ".scaleZ", float(Scale))

    cmds.makeIdentity(ControllerList[0], a = True)

    #Change Controller Color
    for item in shapes:
        cmds.setAttr(item + ".overrideEnabled", 1)
        cmds.setAttr(item + ".overrideColor", colorCode)

def orientJoints(obj):
    cmds.joint(obj, e = True, oj = "xyz", sao = "yup", ch = True, zso = True)

def clearTransformInputs(obj):
    cmds.delete(obj + ".tx", icn = True)
    cmds.delete(obj + ".ty", icn = True)
    cmds.delete(obj + ".tz", icn = True)
    cmds.delete(obj + ".rx", icn = True)
    cmds.delete(obj + ".ry", icn = True)
    cmds.delete(obj + ".rz", icn = True)
    cmds.delete(obj + ".sx", icn = True)
    cmds.delete(obj + ".sy", icn = True)
    cmds.delete(obj + ".sz", icn = True)

def clearScale(obj):
    cmds.delete(obj + ".sx", icn = True)
    cmds.delete(obj + ".sy", icn = True)
    cmds.delete(obj + ".sz", icn = True)

def clearVis(obj):
    cmds.delete(obj + ".visibility", icn = True)

def clearJointOrientation(obj):
    cmds.setAttr(obj + ".jointOrientX", 0)
    cmds.setAttr(obj + ".jointOrientY", 0)
    cmds.setAttr(obj + ".jointOrientZ", 0)

def constraintToCurve(obj, crv, uValue = 0.5, freeChannel = False):
    motionPath = cmds.pathAnimation(obj, crv, f = True, fm = True)
    MotionPathAnimationInput = motionPath + "_uValue.output"
    cmds.disconnectAttr(MotionPathAnimationInput, motionPath + ".uValue")
    cmds.setAttr(motionPath + ".uValue", uValue)
    if freeChannel:

        clearTransformInputs(obj)
        cmds.delete(motionPath)

def createJointsAlongCurve(jointsNumVar, nameVar, bnName):
    curveSelected = cmds.ls(sl = True)[0]
    jntAmount = jointsNumVar
    name = nameVar
    tempGrpConst = []
    jointsinCrv = []
    #Constraint Joints to Curve:
    for iter in range(0, jntAmount):
        jointName = bnName + "_" + name + "_" + str(iter + 1).zfill(2)
        if jntAmount == 1:
            uValue = 0.5
        else:
            uValue = 1.0/(jntAmount-1.0) * iter

        cmds.select(cl = True)
        bn = cmds.joint( n = jointName)
        jntGrp = cmds.group(bn, n = "grp_" + jointName)
        constraintToCurve(jntGrp, curveSelected, uValue)
        jointsinCrv.append(bn)
        tempGrpConst.append(jntGrp)

        if "Driver" in bnName:
            DriverIKJoints.append(bn)
        else:
            bindJoints.append(bn)

    #Parent under previous Joint
    for joint in range(1, len(jointsinCrv)):
        cmds.parent(jointsinCrv[joint], jointsinCrv[joint - 1])

    #Parent first Joint under World
    cmds.parent(jointsinCrv[0], w = True)

    #Orient Joints and delete Groups
    orientJoints(obj = jointsinCrv[0])
    clearJointOrientation(obj = jointsinCrv[-1])

    for grp in tempGrpConst:
        cmds.delete(grp)

def cleanLocators(obj):
    #Hide Locator Visibility
    for item in obj:
        cmds.select(item + "Shape")
        cmds.setAttr(item + "Shape" + ".lodVisibility", 0)

def createConnections(CCName, LocatorName, grpName, nameVar, rigType, CCScale):

    if rigType == "FK":
        for j in range(0, len(bindJoints)):
            PConstraint = cmds.parentConstraint(FKJoints[j], bindJoints[j], mo = True)
            Sconstraint = cmds.scaleConstraint(FKCC[j], bindJoints[j], mo = True)

    elif rigType == "IK":
        for j in range(0, len(bindJoints)):
            PConstraint = cmds.parentConstraint(IKJoints[j], bindJoints[j], mo = True)

    elif rigType == "IKFK" or rigType == "Hybrid_IKFK":
        #Create IKFK Switch Controller
        IKFKSwitch = cmds.curve(p=[(0, 0, -1), (1, 0, 0), (0, 0, 1),
                             (-1, 0, 0), (0, 0, -1)], d = 1, n = CCName + "_IKFKSwitch_" + nameVar + "01")

        #Change Scale
        cmds.setAttr(IKFKSwitch + ".sx", float(CCScale))
        cmds.setAttr(IKFKSwitch + ".sy", float(CCScale))
        cmds.setAttr(IKFKSwitch + ".sz", float(CCScale))
        cmds.makeIdentity(IKFKSwitch, a = True)

        IKFKSwitchLoc = cmds.spaceLocator(n = LocatorName + "_" + IKFKSwitch)
        cmds.parent(IKFKSwitch, IKFKSwitchLoc)
        cmds.matchTransform(IKFKSwitchLoc, bindJoints[0])
        cmds.parentConstraint(CCName + "_Main_" + nameVar + "01", IKFKSwitchLoc, mo = True)
        cmds.scaleConstraint(CCName + "_Main_" + nameVar + "01", IKFKSwitchLoc, mo = True)

        #Change IKFKSwitch CC Shape and add custom attribute
        cmds.select(IKFKSwitch + ".cv[0:4]")
        cmds.rotate(0, 0, 90, r = True)
        cmds.move(0, float(CCScale)*3.5, 0, r = True, os = True, wd = True)
        cmds.setAttr(IKFKSwitch + ".overrideEnabled", 1)
        cmds.setAttr(IKFKSwitch + ".overrideColor", 14)
        cmds.setAttr(IKFKSwitch + ".tx", k=False, l=True, channelBox=False)
        cmds.setAttr(IKFKSwitch + ".ty", k=False, l=True, channelBox=False)
        cmds.setAttr(IKFKSwitch + ".tz", k=False, l=True, channelBox=False)
        cmds.setAttr(IKFKSwitch + ".rx", k=False, l=True, channelBox=False)
        cmds.setAttr(IKFKSwitch + ".ry", k=False, l=True, channelBox=False)
        cmds.setAttr(IKFKSwitch + ".rz", k=False, l=True, channelBox=False)
        cmds.setAttr(IKFKSwitch + ".sx", k=False, l=True, channelBox=False)
        cmds.setAttr(IKFKSwitch + ".sy", k=False, l=True, channelBox=False)
        cmds.setAttr(IKFKSwitch + ".sz", k=False, l=True, channelBox=False)
        cmds.setAttr(IKFKSwitch + ".v", k=False, l=True, channelBox=False)
        cmds.addAttr(IKFKSwitch, ln='IKFKSwitch',at='float',min=0,max=1,dv=1, k=True)

        if cmds.objExists(grpName + "_" + CCName + "_" + nameVar + "01") == True:
            cmds.parent(IKFKSwitchLoc, grpName + "_" + CCName + "_" + nameVar + "01")

        IKRevNode01 = cmds.shadingNode('reverse', asUtility=True, n="reverse_" + IKFKSwitch)
        cmds.connectAttr(IKFKSwitch + ".IKFKSwitch", IKRevNode01 + ".inputX" )

        for j in range(0, len(bindJoints)):
            PConstraint = cmds.parentConstraint(FKJoints[j], IKJoints[j], bindJoints[j], mo = True)
            cmds.connectAttr(IKFKSwitch + ".IKFKSwitch", PConstraint[0] + "." + IKJoints[j] + "W1")
            cmds.connectAttr(IKRevNode01 + ".output.outputX", PConstraint[0] + "." + FKJoints[j] + "W0")

        #Control CC Visibility
        cmds.connectAttr(IKFKSwitch + ".IKFKSwitch", grpName + "_IK_" + CCName + "_" + nameVar + ".visibility")
        cmds.connectAttr(IKRevNode01 + ".output.outputX", grpName + "_FK_" + CCName + "_" + nameVar + ".visibility")
        cleanLocators(obj = IKFKSwitchLoc)

def RenameChain(Chain, JointName, newName):

    cmds.select(Chain[0], hi = True)
    selection = cmds.ls(sl = True, dag=True, l=True)
    children = cmds.listRelatives(selection, children=True, ad=True, f=True)
    for item in children:
        root,_,  tail =  item.rpartition("|")
        FinalName = tail.replace(JointName, newName)
        cmds.rename(item, FinalName)

def TwistIK(obj):
    #Create Nodes
    InvTwist = cmds.shadingNode('multiplyDivide', asUtility=True, n="mult_Inv_Twist_" + obj)
    sumValues = cmds.shadingNode('plusMinusAverage', asUtility=True, n="plus_Twist_" + obj)

    #Make Connections
    #Connect to roll
    cmds.connectAttr(DriverIKJoints[0] + ".rx", obj + ".roll")
    #Connect and inverse value to twist
    cmds.connectAttr(DriverIKJoints[0] + ".rx", InvTwist + ".input1X")
    cmds.setAttr(InvTwist + ".input2X", -1)

    cmds.connectAttr(DriverIKJoints[-1] + ".rx", sumValues + ".input1D[0]")
    cmds.connectAttr(InvTwist + ".outputX", sumValues + ".input1D[1]")

    #Final connection to twist
    cmds.connectAttr(sumValues + ".output1D", obj + ".twist")

def createFKRig(bnName, CCName, LocatorName, grpName, nameVar, CCScale, Color, CCSHape ):
    FKJoint = cmds.duplicate(bindJoints[0], n=bindJoints[0].replace(bnName, "FK_" + bnName))
    RenameChain(Chain= FKJoint, JointName = bnName, newName = "FK_" + bnName)
    #Store Joints in a variable
    cmds.select(FKJoint[0], hi= True)
    FKSelection = cmds.ls(sl = True)
    for item in FKSelection:
        FKJoints.append(item)

    #Create FK Controllers
    for joint in FKJoints:
        createController(CCSHape, Color = Color, Scale = CCScale)
        FKCCName = cmds.rename("temp_cc_name", joint.replace("FK_" + bnName, CCName + "_FK"))
        FKCC.append(FKCCName)
        FKLocator = cmds.spaceLocator(n = LocatorName + FKCCName)
        FKLocatorList.append(FKLocator[0])
        cmds.parent(FKCCName, FKLocator)
        cmds.matchTransform(FKLocator, joint)

        #Constraint to Joint
        cmds.parentConstraint(FKCCName, joint, mo = True)
        cmds.scaleConstraint(FKCCName, joint, mo = True)


    #Parent controller under previous FK Controller
    for i in range(1, len(FKLocatorList)):
        cmds.parent(FKLocatorList[i], FKCC[i-1])

    #Clean up scene
    cmds.group(FKJoints[0], n = grpName + "_FK_" + nameVar)
    cmds.group(FKLocatorList[0], n = grpName + "_FK_" + CCName + "_" + nameVar)
    cleanLocators(obj = FKLocatorList)

def createIKRig(bnName, CCName, LocatorName, CCNumVar, grpName, nameVar, CCScale, Color, CCSHape):
    IKJoint = cmds.duplicate(bindJoints[0], n=bindJoints[0].replace(bnName, "IK_" + bnName))
    RenameChain(Chain= IKJoint, JointName = bnName, newName = "IK_" + bnName)
    #Store Joints in a variable
    cmds.select(IKJoint[0], hi= True)
    IKSelection = cmds.ls(sl = True)
    for item in IKSelection:
        IKJoints.append(item)

    cmds.delete("IKSplineCrv", ch = True)

    #Create IK Spline Handle
    IKSplineHandle = cmds.ikHandle(n = "IKHandle_" + nameVar, sol='ikSplineSolver', ccv=False, pcv=False, sj=IKJoints[0], ee= IKJoints[-1], c= "IKSplineCrv")
    cmds.setAttr("IKHandle_" + nameVar + ".visibility", 0)
    IKSplineCrv = cmds.rename("IKSplineCrv", "crv_IK_" + nameVar)

    #Create Driver bones
    cmds.select(IKSplineCrv)
    createJointsAlongCurve(jointsNumVar = CCNumVar, nameVar = nameVar, bnName = "Driver_IK_" + bnName)

    IKDriverGrp = cmds.group(DriverIKJoints[0], n = grpName + "_Driver_IK_" + nameVar)

    for Driver in DriverIKJoints:
        cmds.parent(Driver, w = True)

    for Driver in DriverIKJoints:
        cmds.parent(Driver,IKDriverGrp)

    #bind Driver jnts with ribbon:
    cmds.select(cl=True)
    cmds.select(DriverIKJoints)
    cmds.select(IKSplineCrv, add = True)
    cmds.skinCluster()

    #Create IK Controllers
    for joint in DriverIKJoints:
        createController(CCSHape, Color, Scale = CCScale)
        IKCCName = cmds.rename("temp_cc_name", joint.replace("Driver_IK_" + bnName, CCName + "_IK"))
        IKCC.append(IKCCName)
        IKLocator = cmds.spaceLocator(n = LocatorName + "_" + IKCCName)
        IKLocatorList.append(IKLocator[0])
        cmds.parent(IKCCName, IKLocator)
        cmds.matchTransform(IKLocator, joint)

        #Constraint to Joint
        cmds.parentConstraint(IKCCName, joint, mo = True)

    TwistIK(obj = IKSplineHandle[0])

    #Clean up scene
    cmds.group(IKJoints[0], n = grpName + "_IK_" + nameVar)
    grpCCIK = cmds.group( n = grpName + "_IK_" + CCName + "_" + nameVar, em = True)
    for item in IKLocatorList:
        cmds.parent(item, grpCCIK)
    cleanLocators(obj = IKLocatorList)

    return grpCCIK

def createHybridRig(CCName, LocatorName, CCScale, FKCCSHape, FKColor):
    #Create FK Controllers
    for controller in IKCC:
        createController(CCSHape = FKCCSHape, Color = FKColor, Scale = float(CCScale)*2)
        HybridIKCCName = cmds.rename("temp_cc_name", controller.replace(CCName + "_IK", CCName + "_FKHybrid"))
        HybridIKCC.append(HybridIKCCName)
        HybridFKLocator = cmds.spaceLocator(n = LocatorName + "_" + HybridIKCCName)
        HybridIKLocatorList.append(HybridFKLocator[0])
        cmds.parent(HybridIKCCName, HybridFKLocator)
        cmds.matchTransform(HybridFKLocator, controller)

    #Hide Locator visibility
    cleanLocators(obj = HybridIKLocatorList)

    #Parent controller under previous FK Controller
    for i in range(1, len(HybridIKCC)):
        cmds.parent(HybridIKLocatorList[i], HybridIKCC[i-1])

    for i in range (0, len(HybridIKLocatorList)):
        cmds.parentConstraint(HybridIKCC[i], IKLocatorList[i])

def stretchySpline(CCName, nameVar, stretchyType, SquashStretch, rigType):
    #Create Curve Info Node
    CrvInfo = cmds.shadingNode('curveInfo', asUtility=True, n="crvInfo_" + "crv_IK_" + nameVar)

    #Store crv Shape in variable
    Crv = "crv_IK_" + nameVar
    cmds.select(Crv)
    cmds.pickWalk(d = "down")
    crvShape = cmds.ls(sl = True)

    #Connect arc length to curve info node
    cmds.connectAttr(crvShape[0] + ".local", CrvInfo + ".inputCurve")
    defaultLength = cmds.getAttr(CrvInfo + ".arcLength")

    #Scale Ratio
    CrvMult = cmds.shadingNode('multiplyDivide', asUtility=True, n="div_" + "crv_length_" + nameVar)
    cmds.setAttr(CrvMult + ".input2X", float(defaultLength))
    cmds.setAttr(CrvMult + ".operation", 2)
    cmds.connectAttr(CrvInfo + ".arcLength",CrvMult + ".input1X")

    if SquashStretch == True:
        if cmds.objExists(CCName + "_IKFKSwitch_" + nameVar + "01"):
            StretchyAttr = cmds.addAttr(CCName + "_IKFKSwitch_" + nameVar + "01", ln='Stretchy_IK',at='float',min=0,max=1,dv=1, k=True)
            VolumeAttr = cmds.addAttr(CCName + "_IKFKSwitch_" + nameVar + "01", ln='Squash_Stretch',at='float',min=0,max=5,dv=1, k=True)
        else:
            StretchyAttr = cmds.addAttr(CCName + "_Main_" + nameVar + "01", ln='Stretchy_IK',at='float',min=0,max=1,dv=1, k=True)
            StretchyAttr = cmds.addAttr(CCName + "_Main_" + nameVar + "01", ln='Squash_Stretch',at='float',min=0,max=5,dv=1, k=True)


        if stretchyType == "Scale":
            #Create node storing default Scale value
            ConstantScale = cmds.shadingNode('multiplyDivide', asUtility=True, n="constScale_" + nameVar + "01")
            blendAttr = cmds.shadingNode('blendTwoAttr', asUtility=True, n="blendAttr_Stretch" + nameVar + "01")

            cmds.setAttr(ConstantScale + ".input2X", 1)
            cmds.connectAttr(CCName + "_Main_" + nameVar + "01" + ".sx", ConstantScale + ".input1X")

            cmds.connectAttr(ConstantScale + ".outputX", blendAttr + ".input[0]")
            cmds.connectAttr(CrvMult + ".outputX", blendAttr + ".input[1]")

            if cmds.objExists(CCName + "_IKFKSwitch_" + nameVar + "01"):
                cmds.connectAttr(CCName + "_IKFKSwitch_" + nameVar + "01" + ".Stretchy_IK", blendAttr + ".attributesBlender")
            else:
                cmds.connectAttr(CCName + "_Main_" + nameVar + "01" + ".Stretchy_IK", blendAttr + ".attributesBlender")

            for i in range(0, len(IKJoints) - 1):
                #Final connection to Joint
                cmds.connectAttr(blendAttr + ".output", IKJoints[i] + ".sx")

        elif stretchyType == "Translate":
            # Scale ratio applied to translation and volume squash and stretch
            for i in range(1, len(IKJoints)):
                defaultTranslation = cmds.getAttr(IKJoints[i] + ".translateX")
                MultTrans = cmds.shadingNode('multiplyDivide', asUtility=True, n="mult_" + "crv_Translation_ratio" + nameVar + "01")
                cmds.setAttr(MultTrans + ".input2X", defaultTranslation)
                cmds.connectAttr(CrvMult + ".outputX", MultTrans + ".input1X")

                #Create node storing default translation value
                ConstantTranslation = cmds.shadingNode('multiplyDivide', asUtility=True, n="constTrans_" + IKJoints[i])
                blendAttr = cmds.shadingNode('blendTwoAttr', asUtility=True, n="blendAttr_Stretch" + IKJoints[i])

                cmds.connectAttr(CCName + "_Main_" + nameVar + "01" + ".sx", ConstantTranslation + ".input1X")
                cmds.setAttr(ConstantTranslation + ".input2X", defaultTranslation)

                cmds.connectAttr(ConstantTranslation + ".outputX", blendAttr + ".input[0]")
                cmds.connectAttr(MultTrans + ".outputX", blendAttr + ".input[1]")


                if cmds.objExists(CCName + "_IKFKSwitch_" + nameVar + "01"):
                    cmds.connectAttr(CCName + "_IKFKSwitch_" + nameVar + "01" + ".Stretchy_IK", blendAttr + ".attributesBlender")
                else:
                    cmds.connectAttr(CCName + "_Main_" + nameVar + "01" + ".Stretchy_IK", blendAttr + ".attributesBlender")

                #Final connection to Joint
                cmds.connectAttr(blendAttr + ".output", IKJoints[i] + ".tx")


        #SQUASH AND STRETCH
        #Create Nodes
        squashStretchRatio = cmds.shadingNode('multiplyDivide', asUtility=True, n="Volume_STretch_Pow" + nameVar + "01")
        cmds.setAttr(squashStretchRatio + ".operation", 3)

        #cmds.connectAttr(CrvMult + ".outputX", squashStretchRatio + ".input1X")
        cmds.setAttr(squashStretchRatio + ".input2X", 0.5)

        InvSquashStretchRatio = cmds.shadingNode('multiplyDivide', asUtility=True, n="Volume_STretch_Invert_Div" + nameVar + "01")
        cmds.setAttr(InvSquashStretchRatio + ".operation", 2)
        cmds.setAttr(InvSquashStretchRatio + ".input1X", 1)
        cmds.connectAttr(squashStretchRatio + ".outputX",InvSquashStretchRatio + ".input2X")

        #Create attribute switch node
        ConstScaleFinal = cmds.shadingNode('floatConstant', asUtility=True, n="ConstScaleFinal" + nameVar + "01")
        blendAttrScale = cmds.shadingNode('blendTwoAttr', asUtility=True, n="blendAttr_Volume" + nameVar + "01")

        #Scale preservation through scale main cc
        MultMainScale = cmds.shadingNode('multiplyDivide', asUtility=True, n="Mult_MainScale" + nameVar + "01")
        DivMainScale = cmds.shadingNode('multiplyDivide', asUtility=True, n="Div_MainScale" + nameVar + "01")

        cmds.setAttr(MultMainScale + ".input1X",defaultLength)
        cmds.connectAttr(CCName + "_Main_" + nameVar + "01" + ".sx", MultMainScale + ".input2X")

        cmds.setAttr(DivMainScale + ".operation", 2)
        cmds.connectAttr(MultMainScale + ".outputX", DivMainScale + ".input2X")
        cmds.connectAttr(CrvInfo + ".arcLength", DivMainScale + ".input1X")
        cmds.connectAttr(DivMainScale + ".outputX", squashStretchRatio + ".input1X")

        if cmds.objExists(CCName + "_IKFKSwitch_" + nameVar + "01"):
            cmds.connectAttr(CCName + "_IKFKSwitch_" + nameVar + "01" + ".Squash_Stretch", blendAttrScale + ".attributesBlender")
        else:
            cmds.connectAttr(CCName + "_Main_" + nameVar + "01" + ".Squash_Stretch", blendAttrScale + ".attributesBlender")

        cmds.connectAttr(ConstScaleFinal + ".outFloat", blendAttrScale + ".input[0]")
        cmds.connectAttr(InvSquashStretchRatio + ".outputX", blendAttrScale + ".input[1]")

        #Create nodes to maintain Main Control Scale
        AverageMainScale = cmds.shadingNode('plusMinusAverage', asUtility=True, n="AverageMainScale_" + nameVar + "01")
        SumAverageTotalScale = cmds.shadingNode('plusMinusAverage', asUtility=True, n="SumTotalScale" + nameVar + "01")

        #Connect to Average Scale between scale Y and Z
        cmds.setAttr(AverageMainScale + ".operation", 3)
        cmds.connectAttr(CCName + "_Main_" + nameVar + "01" +".sy", AverageMainScale + ".input1D[1]")
        cmds.connectAttr(CCName + "_Main_" + nameVar + "01" +".sz", AverageMainScale + ".input1D[2]")

        #Connect to the final Scale node
        cmds.setAttr(SumAverageTotalScale + ".input1D[0]", -1)
        cmds.connectAttr(blendAttrScale + ".output", SumAverageTotalScale + ".input1D[1]")
        cmds.connectAttr(AverageMainScale + ".output1D", SumAverageTotalScale + ".input1D[2]")

        #Connect scale ratio to IK Joint
        for i in range(0, len(IKJoints)):
            cmds.connectAttr(SumAverageTotalScale + ".output1D", IKJoints[i] + ".sy")
            cmds.connectAttr(SumAverageTotalScale + ".output1D", IKJoints[i] + ".sz")

        #Final Connection to Joint
        if rigType != "IK":
            for i in range(0, len(bindJoints)):
                AverageScale = cmds.shadingNode('blendColors', asUtility=True, n="Blend_Scale" + bindJoints[i] + "_01")

                cmds.connectAttr(CCName + "_IKFKSwitch_" + nameVar + "01" + ".IKFKSwitch", AverageScale + ".blender")
                cmds.connectAttr(IKJoints[i] + ".scale", AverageScale + ".color1")
                cmds.connectAttr(FKJoints[i] + ".scale", AverageScale + ".color2")
                cmds.connectAttr(AverageScale + ".output", bindJoints[i] + ".scale")
        if rigType == "IK":
            for i in range(0, len(bindJoints)):
                cmds.connectAttr(IKJoints[i] + ".scale", bindJoints[i] + ".scale")

    else:
        for i in range(0, len(IKJoints)):

            cmds.connectAttr(CCName + "_Main_" + nameVar + "01" + ".scaleX", IKJoints[i] + ".sx")
            cmds.connectAttr(CCName + "_Main_" + nameVar + "01" + ".scaleX", IKJoints[i] + ".sy")
            cmds.connectAttr(CCName + "_Main_" + nameVar + "01" + ".scaleX", IKJoints[i] + ".sz")

def IKFKSplineGuides():
    if cmds.objExists("IKSplineCrv") == True:
        cmds.warning( "Don't click me twice")

    else:
        selection = cmds.ls(sl = True) or []
        selectionType = cmds.listRelatives(selection, shapes=True)
        nodeType = cmds.nodeType(selectionType)
        if len(selection) and nodeType == 'nurbsCurve':
            cmds.rename(selection, "IKSplineCrv")
            cmds.makeIdentity("IKSplineCrv", apply = True)
            cmds.delete("IKSplineCrv", ch = True)

        else:
            PlaceCrv = cmds.curve(n="IKSplineCrv", d=3, p=[(0, 0, 20),(0, 0, 18), (0, 0, 0), (0, 0, -18),(0, 0, -20)])

            # Get all cvs from curve
            curveCVs = cmds.ls('{0}.cv[:]'.format(PlaceCrv), fl = True)

            #Create Clusters
            cmds.select(curveCVs[0], curveCVs[1])
            clusterA = cmds.cluster(n ="clstrStart")
            cmds.select(curveCVs[2])
            clusterB = cmds.cluster(n = "clstrMid")
            cmds.select(curveCVs[3], curveCVs[4])
            clusterC = cmds.cluster(n = "clstrEnd")
            clstrGrp = cmds.group(clusterA, clusterB, clusterC, n = "temp_Clusters")
            cmds.setAttr(clstrGrp + ".visibility", 0)

            #Create Locators
            PTStartLoc = cmds.spaceLocator(n = "locAlign_PTStart")
            cmds.matchTransform(PTStartLoc, clusterA)
            cmds.makeIdentity(PTStartLoc, apply = True)
            cmds.parentConstraint(PTStartLoc, clusterA, mo=True)
            cmds.setAttr(PTStartLoc[0] + ".localScaleX", 5)
            cmds.setAttr(PTStartLoc[0] + ".localScaleY", 5)
            cmds.setAttr(PTStartLoc[0] + ".localScaleZ", 5)

            PTMidLoc = cmds.spaceLocator(n = "locAlign_PTMid")
            cmds.matchTransform(PTMidLoc, clusterB)
            cmds.makeIdentity(PTMidLoc, apply = True)
            cmds.parentConstraint(PTMidLoc, clusterB, mo=True)
            cmds.setAttr(PTMidLoc[0] + ".localScaleX", 5)
            cmds.setAttr(PTMidLoc[0] + ".localScaleY", 5)
            cmds.setAttr(PTMidLoc[0] + ".localScaleZ", 5)

            PTEndLoc = cmds.spaceLocator(n = "locAlign_PTEnd")
            cmds.matchTransform(PTEndLoc, clusterC)
            cmds.makeIdentity(PTEndLoc, apply = True)
            cmds.parentConstraint(PTEndLoc, clusterC, mo=True)
            cmds.setAttr(PTEndLoc[0] + ".localScaleX", 5)
            cmds.setAttr(PTEndLoc[0] + ".localScaleY", 5)
            cmds.setAttr(PTEndLoc[0] + ".localScaleZ", 5)

            #Group Locators
            tempLocGrp = cmds.group(PTStartLoc, PTMidLoc, PTEndLoc, n="Temp_PTLocators")

def IKFKSplineRig(bnName, CCName, LocatorName, grpName, jointsNumVar, CCNumVar, nameVar, rigType, CCScale,  SquashStretch, stretchyType, IKCCSHape, FKCCSHape, IKColor, FKColor):

    bnName = cmds.textField(bnName, q = True, tx = True)
    CCName = cmds.textField(CCName, q = True, tx = True)
    LocatorName = cmds.textField(LocatorName, q = True, tx = True)
    grpName = cmds.textField(grpName, q = True, tx = True)
    jointsNumVar = cmds.intSliderGrp(jointsNumVar, q = True, value = True)
    CCNumVar = cmds.intSliderGrp(CCNumVar, q = True, value = True)
    nameVar = cmds.textField(nameVar, q = True, tx = True)
    rigType = cmds.radioCollection(rigType, q = True, sl = True)
    CCScale = cmds.textField(CCScale, q = True, tx = True)
    SquashStretch = cmds.checkBox(SquashStretch, q = True, v = True)
    stretchyType = cmds.radioCollection(stretchyType, q = True, sl = True)
    IKCCSHape = cmds.optionMenu(IKCCSHape, q = True, value = True)
    FKCCSHape = cmds.optionMenu(FKCCSHape, q = True, value = True)
    IKColor = cmds.optionMenu(IKColor, q = True, value = True)
    FKColor = cmds.optionMenu(FKColor, q = True, value = True)

    #Clean sefault selection and symetry attr
    cmds.softSelect(sse=0)
    cmds.symmetricModelling(s = 0)


    if cmds.objExists("IKSplineCrv") == False:
        cmds.confirmDialog( icn = "warning", title='ERROR!', message='Please Create Guides first', button=['OK'], ma='center')
    if cmds.objExists("IKSplineCrv") == True:
        if cmds.objExists(bnName + "_" + nameVar + "_01"):
            cmds.confirmDialog( icn = "warning", title='ERROR!', message='The name you used already exists, please change the name', button=['OK'], ma='center')
        else:
            #Create top group nodes
            TopCCGrp = cmds.group(n = grpName + "_" + CCName + "_" + nameVar + "01", em = True)
            TopRigGrp = cmds.group(n = grpName + "_Rig_" + nameVar + "01", em = True)
            TopIKRigGrp = cmds.group(n = grpName + "_IKRig_" + nameVar + "01", em = True)
            TopFKRigGrp = cmds.group(n = grpName + "_FKRig_" + nameVar + "01",em = True)

            #Control Visibility of rig grp
            cmds.setAttr(TopRigGrp + ".visibility", 0)

            cmds.parent(TopFKRigGrp, TopIKRigGrp, TopRigGrp)

            cmds.select("IKSplineCrv")
            #Create Joints Under Curve and delete constraints
            createJointsAlongCurve(jointsNumVar, nameVar, bnName)
            cmds.rebuildCurve("IKSplineCrv", ch = False, s = CCNumVar-1, d = 3)
            cmds.delete("IKSplineCrv", ch = True)
            cmds.select(cl=True)

            #Create Master Controller
            createController(CCSHape = "Square", Color = "Yellow", Scale = float(CCScale)*1.5)
            MasterCC = cmds.rename("temp_cc_name", CCName + "_Main_" + nameVar + "01")
            MasterLocator = cmds.spaceLocator(n = LocatorName + "_" + MasterCC)
            cleanLocators(obj = MasterLocator)
            cmds.parent(MasterCC, MasterLocator)

            cmds.matchTransform(MasterLocator, bindJoints[0])
            cmds.parent(MasterLocator, TopCCGrp)

            if rigType == "FK":
                createFKRig(bnName, CCName, LocatorName, grpName, nameVar, CCScale, Color = FKColor, CCSHape = FKCCSHape)
                #Clean scene and organize under groups
                cmds.parent( grpName + "_FK_" + nameVar, TopFKRigGrp)
                cmds.parent(grpName + "_FK_" + CCName + "_" + nameVar, MasterCC)
                cmds.delete("IKSplineCrv")
                cmds.delete(TopIKRigGrp)

            if rigType == "IK":
                createIKRig(bnName, CCName, LocatorName, CCNumVar, grpName, nameVar, CCScale, Color = IKColor, CCSHape = IKCCSHape)

                #Clean scene and organize under groups
                cmds.parent(grpName + "_IK_" + nameVar, TopIKRigGrp)
                cmds.parent(grpName + "_Driver_IK_" + nameVar, TopIKRigGrp)
                cmds.parent("IKHandle_" + nameVar, TopIKRigGrp)
                cmds.parent("crv_IK_" + nameVar, TopIKRigGrp)
                cmds.parent(grpName + "_IK_" + CCName + "_" + nameVar, MasterCC)
                cmds.delete(TopFKRigGrp)

            if rigType == "IKFK" or rigType == "Hybrid_IKFK":
                createFKRig(bnName, CCName, LocatorName, grpName, nameVar, CCScale, Color = FKColor, CCSHape = FKCCSHape)
                createIKRig(bnName, CCName, LocatorName, CCNumVar, grpName, nameVar, CCScale, Color = IKColor, CCSHape = IKCCSHape)

                #Clean scene and organize under groups
                cmds.parent(grpName + "_FK_" + nameVar, TopFKRigGrp)
                cmds.parent(grpName + "_FK_" + CCName + "_" + nameVar, MasterCC)
                cmds.parent(grpName + "_IK_" + nameVar, TopIKRigGrp)
                cmds.parent(grpName + "_Driver_IK_" + nameVar, TopIKRigGrp)
                cmds.parent("IKHandle_" + nameVar, TopIKRigGrp)
                cmds.parent("crv_IK_" + nameVar, TopIKRigGrp)
                cmds.parent(grpName + "_IK_" + CCName + "_" + nameVar, MasterCC)

            if rigType == "Hybrid_IKFK":
                createHybridRig(CCName, LocatorName, CCScale, FKCCSHape, FKColor)
                cmds.parent(HybridIKLocatorList[0], TopIKRigGrp)

                if cmds.objExists(grpName + "_IK_" + CCName + "_" + nameVar):
                    cmds.parent(LocatorName + "_" + CCName + "_FKHybrid_" + nameVar + "_01", grpName + "_IK_" + CCName + "_" + nameVar)
                else:
                    cmds.parent(LocatorName + "_" + CCName + "_FKHybrid_" + nameVar + "_01", MasterCC)

            createConnections(CCName, LocatorName, grpName, nameVar, rigType, CCScale)

            if rigType != "FK":
                stretchySpline(CCName, nameVar, stretchyType, SquashStretch, rigType)

            bindJoints[:]=[]
            FKJoints[:]=[]
            IKJoints[:]=[]
            DriverIKJoints[:]=[]
            FKCC[:]=[]
            IKCC[:]=[]
            HybridIKCC[:]=[]
            FKLocatorList[:]=[]
            IKLocatorList[:]=[]
            HybridIKLocatorList[:]=[]

            #CLEAN SCENE
            if cmds.objExists("temp_Clusters"):
                cmds.delete("temp_Clusters")
            if cmds.objExists("Temp_PTLocators"):
                cmds.delete("Temp_PTLocators")

            cmds.select(cl=True)
                
            #Empty Lists
            bindJoints[:]=[]
            FKJoints[:]=[]
            IKJoints[:]=[]
            DriverIKJoints[:]=[]
            FKCC[:]=[]
            IKCC[:]=[]
            HybridIKCC[:]=[]
            FKLocatorList[:]=[]
            IKLocatorList[:]=[]
            HybridIKLocatorList[:]=[]

            print("Rig created Succesfully")
    else:
        cmds.confirmDialog( icn = "warning", title='ERROR!', message='Please create Guides first', button=['OK'], ma='center')

