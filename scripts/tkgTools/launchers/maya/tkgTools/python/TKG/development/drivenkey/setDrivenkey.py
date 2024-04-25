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

sel = cmds.ls(os=True)

driver = sel[0]
driverAttr = 'rotateX'
driverValues = [0, 30]

driven = sel[1]
drivenAttrs = ['tx', 'ty', 'rx']
drivenValues = [[0, 10], [0, 40], [0, 60]]

preInf = 4
postInf = 4

setDrivenKey(driver, driverAttr, driverValues,
              driven, drivenAttrs, drivenValues)

animCurves = cmds.listConnections(driver, d=True, scn=True, type='animCurve')

for ac in animCurves:
    cmds.setAttr(ac+'.preInfinity', preInf)
    cmds.setAttr(ac+'.postInfinity', postInf)


# graph editor
# cmds.animCurveEditor('graphEditor1GraphEd', edit=1, displayInfinities=True)
# cmds.optionVar(intValue=('graphEditorDisplayInfinities', True))
# cmds.GraphEditor()

node = cmds.ls(os=True)[0]

animCurvesList = []
animCurves = cmds.listConnections(node, scn=True, type='animCurve')
if not animCurves:
    blendWeighteds = cmds.listConnections(node, scn=True, type='blendWeighted')

    for bwd in blendWeighteds:
        animCurves = cmds.listConnections(bwd, scn=True, type='animCurve')
        [animCurvesList.append(ac) for ac in animCurves if not ac in animCurvesList]
else:
    [animCurvesList.append(ac) for ac in animCurves if not ac in animCurvesList]

cmds.listAttr(animCurvesList[2])
cmds.getAttr(animCurvesList[2]+'.keyTanInX')