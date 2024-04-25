import maya.cmds as cmds

# set
def setDrivenKey(driver=None, driverAttr=None, driverValues=None,
                  driven=None, drivenAttrs=None, drivenValues=None,
                  itt='clamped', ott='clamped'):
    for i, drv in enumerate(driverValues):
        for j, dnat in enumerate(drivenAttrs):
            dnv = drivenValues[j]
            drivenAnimCrv = cmds.setDrivenKeyframe('{}.{}'.format(driven, dnat),
                                   currentDriver='{}.{}'.format(driver, driverAttr),
                                   driverValue=driverValues[i], value=dnv[i],
                                   itt=itt, ott=ott,
                                   ib=True)

def setDrivenKeys(driver=None, driverAttr=None, driverValues=None,
                  driven=None, drivenAttrs=None, drivenValues=None,
                  preInf='CycleWithOffset', postInf='CycleWithOffset'):

    prePostInfDict = {
        'Constant':0,
        'Linear':1,
        'Cycle':3,
        'CycleWithOffset':4,
        'Oscillate':5
    }

    setDrivenKey(driver, driverAttr, driverValues,
                  driven, drivenAttrs, drivenValues)

    animCurves = cmds.listConnections(driver, d=True, scn=True, type='animCurve')

    for ac in animCurves:
        cmds.setAttr(ac+'.preInfinity', prePostInfDict[preInf])
        cmds.setAttr(ac+'.postInfinity', prePostInfDict[postInf])


def getDriverAnimCrvs(node=None):
    animCurvesList = []
    animCurves = cmds.listConnections(node, s=True, d=False, scn=True, type='animCurve')
    if not animCurves:
        blendWeighteds = cmds.listConnections(node, scn=True, type='blendWeighted')

        for bwd in blendWeighteds:
            animCurves = cmds.listConnections(bwd, scn=True, type='animCurve')
            [animCurvesList.append(ac) for ac in animCurves if not ac in animCurvesList]
    else:
        [animCurvesList.append(ac) for ac in animCurves if not ac in animCurvesList]

    animCrvDrivers = {}
    for ac in animCurvesList:
        acPlugs = cmds.listConnections(ac, s=True, d=False, p=True, scn=True)
        if acPlugs:
            animCrvDrivers[ac] = acPlugs

    return animCrvDrivers


def getAnimCrvValues(animCrvs=None):
    prePostInfDict = {
        0:'Constant',
        1:'Linear',
        3:'Cycle',
        4:'CycleWithOffset',
        5:'Oscillate'
    }

    animCrvValues = {}
    for animCrv in animCrvs:
        animCrvValues[animCrv] = {}
        # get keyframe attrs
        keyTimes = cmds.keyframe(animCrv, floatChange=True, q=True)
        keyValues = cmds.keyframe(animCrv, valueChange=True, q=True)

        animCrvValues[animCrv]['keyTimes'] = keyTimes
        animCrvValues[animCrv]['keyValues'] = keyValues

        # get keyTangent attrs
        keyItts = cmds.keyTangent(animCrv, inTangentType=True, q=True)
        keyOtts = cmds.keyTangent(animCrv, outTangentType=True, q=True)
        keyInAngles = cmds.keyTangent(animCrv, inAngle=True, q=True)
        keyInWeights = cmds.keyTangent(animCrv, inWeight=True, q=True)
        keyOutAngles = cmds.keyTangent(animCrv, outAngle=True, q=True)
        keyOutWeights = cmds.keyTangent(animCrv, outWeight=True, q=True)

        animCrvValues[animCrv]['keyItts'] = keyItts
        animCrvValues[animCrv]['keyOtts'] = keyOtts
        animCrvValues[animCrv]['keyInAngles'] = keyInAngles
        animCrvValues[animCrv]['keyInWeights'] = keyInWeights
        animCrvValues[animCrv]['keyOutAngles'] = keyOutAngles
        animCrvValues[animCrv]['keyOutWeights'] = keyOutWeights

        # get inf attrs
        animCrvValues[animCrv]['preInfinity'] = prePostInfDict[cmds.getAttr(animCrv+'.preInfinity')]
        animCrvValues[animCrv]['postInfinity'] = prePostInfDict[cmds.getAttr(animCrv+'.postInfinity')]

    return animCrvValues


sel = cmds.ls(os=True)

driver = sel[0]
driverAttr = 'tx'
driverValues = [0, 30]

driven = sel[1]
drivenAttrs = ['rz', 'rx']
drivenValues = [[0, 10], [0, 40]]

preInf = 'CycleWithOffset'
postInf = 'CycleWithOffset'

setDrivenKeys(driver, driverAttr, driverValues,
                  driven, drivenAttrs, drivenValues,
                  preInf, postInf)

# graph editor
# cmds.animCurveEditor('graphEditor1GraphEd', edit=1, displayInfinities=True)
# cmds.optionVar(intValue=('graphEditorDisplayInfinities', True))
# cmds.GraphEditor()


# get drivenkeys
node = cmds.ls(os=True)[0]
animCrvDrivers = getDriverAnimCrvs(node=node)

for animCrv in animCrvDrivers:
    


animCrvValues = getAnimCrvValues(animCrvs=animCrvDrivers)

# set keyframe attrs
t = 10.0
if t in keyTimes:
    i = keyTimes.index(t)
cmds.setKeyframe(animCrv, f=t, insert=True)
cmds.keyframe(animCrv, e=True, absolute=True, index=(i,i), vc=0.5)
