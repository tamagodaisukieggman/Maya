from maya import cmds
import apiutils

def convert():
    toolopt = apiutils.ToolOpt('Create_CurveLocator')
    div = toolopt.getvalue('division', 24)
    kcp = toolopt.getvalue('keepControlPoints', False)

    crvs = cmds.ls(sl=True, type='nurbsCurve')
    dsc = cmds.listRelatives(ad=True, type='nurbsCurve')
    if type(dsc) is list:
        crvs += dsc

    if len(crvs) == 0:
        cmds.error('Select at least a nurbscurve.')

    if not cmds.pluginInfo('curveLocator', q=True, l=True):
        cmds.loadPlugin('curveLocator')

    lct = cmds.createNode('curveLocator', n='curveLocatorShape1')
    rbs = []
    for i, crv in enumerate(crvs):
        rb = cmds.createNode('rebuildCurve')
        cmds.setAttr(rb+'.keepControlPoints', kcp)
        rbs.append(rb)
        cmds.setAttr(rb+'.degree', 1)
        cmds.setAttr(rb+'.rebuildType', 0)
        cmds.setAttr(rb+'.spans', div)

        cmds.connectAttr(crv+'.worldSpace', rb+'.inputCurve')
        cmds.connectAttr(rb+'.outputCurve', lct+'.inputCurves[%d]' % i)

        cmds.disconnectAttr(rb+'.outputCurve', lct+'.inputCurves[%d]' % i)

    cmds.delete(rbs)

    cmds.select(cmds.listRelatives(lct, p=True, pa=True))