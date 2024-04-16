# -*- coding: utf-8 -*-
u"""
UI込みのスクリプトになります
"""
import maya.cmds as cmds
import maya.mel as mel

def get_mid_point(pos1, pos2, percentage=0.5):
    mid_point = [pos1[0] + (pos2[0] - pos1[0]) * percentage,
                 pos1[1] + (pos2[1] - pos1[1]) * percentage,
                 pos1[2] + (pos2[2] - pos1[2]) * percentage]
    return mid_point

def mid_obj_point(objA=None, objB=None, percentage=0.5):
    pos1 = cmds.xform(objA, q=True, t=True, ws=True)
    pos2 = cmds.xform(objB, q=True, t=True, ws=True)
    return get_mid_point(pos1, pos2, percentage)

def create_end_joint(node=None, end_parent=None):
    # parent = cmds.listRelatives(node, p=True) or None
    # if not parent:
    #     return
    # else:
    #     end_parent = parent[0]
    mid_point = mid_obj_point(node, end_parent, percentage=-0.1)
    end_jnt = node+'_end'
    cmds.createNode('joint', n=end_jnt, ss=True)
    cmds.xform(end_jnt, t=mid_point, ws=True, a=True)
    cmds.parent(end_jnt, node)
    return end_jnt

class AutoOverlap(object):
    def __init__(self):
        self.MAIN_WINDOW = 'attachOverlap'

    def ui(self):
        if cmds.workspaceControl(self.MAIN_WINDOW, q=True, ex=True):
            cmds.deleteUI(self.MAIN_WINDOW)

        win = cmds.workspaceControl(self.MAIN_WINDOW, l=self.MAIN_WINDOW)

        self.layout()

        cmds.showWindow(win)
        cmds.scriptJob(e=['SelectionChanged', self.select_nucleus_object], p=win, rp=True)

    def layout(self):
        cmds.columnLayout(adj=True, rs=3)
        self.cten_cb = cmds.checkBox(l='Connect to exist nucleus')
        cmds.rowLayout(nc=2, adj=True)
        self.ncls_tfbg = cmds.textFieldButtonGrp(l='Base Ctrl:', tx='', cw3=[50, 150, 50], ad3=2, bl='Set', bc=self.set_base_ctrl)
        cmds.button(l='Clear', c='cmds.textFieldButtonGrp("{0}", e=True, tx="")'.format(self.ncls_tfbg))
        cmds.setParent('..')

        self.ncls_tfg = cmds.textFieldGrp(l='Nucleus:', tx='', cw2=[50, 150], ad2=2)
        cmds.button(l='Create Dynamics', c=self.create_dynamics)
        cmds.button(l='Create RigidBody', c=self.do_create_rigidBody)
        self.ctrl_size_fsg = cmds.floatSliderGrp(l='Controll Size', f=True, v=1, cw3=[70, 30, 60])
        cmds.rowLayout(nc=4)
        cmds.text(l='InteractivePlayback:')
        cmds.iconTextButton(l='InteractivePlayback', c="mel.eval('InteractivePlayback;')", i='interactivePlayback.png')

    def set_base_ctrl(self, *args, **kwargs):
        sel = cmds.ls(os=True)
        if 1 < len(sel):
            cmds.textFieldButtonGrp(self.ncls_tfbg, e=True, tx='{0}'.format(','.join(sel)))
        else:
            cmds.textFieldButtonGrp(self.ncls_tfbg, e=True, tx='{0}'.format(''.join(sel[0])))

    def select_nucleus_object(self, *args, **kwargs):
        u"""
        ui()のscriptJobのSelectionChangedのイベント
        """
        sel = cmds.ls(os=True, type='nucleus')
        if sel:
            cmds.textFieldGrp(self.ncls_tfg, e=True, tx='{0}'.format(sel[0]))

    def createCurveFromJoints(self, jointChain):
        u"""ジョイントに合わせてカーブが作成されます

        params
        ----------------
        jointChain: list
            ['joint1', 'joint2', 'joint3' ...]
        ----------------

        return
        ----------------
        driverCurve: string
        ----------------

        """
        jointPositions = []

        for joints in jointChain:
            if cmds.objectType( joints, isType='joint' ):
                pos = cmds.xform(joints, q=True, ws=True, t=True)
                jointPositions.append(tuple(pos))
            else:
                raise RuntimeError("Method 'createCurveFromJoints()' expects a joint chain.")

        crv = cmds.curve(ep=jointPositions)
        driverCurve = '{0}_aol_driver_crv'.format(jointChain[0])
        cmds.rename(crv, driverCurve)
        return driverCurve

    def makeCurveDynamic(self, driverCurve, nucleus):
        u"""カーブにnHairを割り当てます

        params
        ----------------
        driverCurve: string
            'driverCurve'
        nucleus: string
            'nucleus1'
        ----------------

        return
        ----------------
        createAutoOverlapChain()に必要な値を返します
        return outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput
        ----------------

        """

        driverCurveShape = cmds.listRelatives(driverCurve, shapes=True)[0]

        if cmds.objectType( driverCurveShape, isType='nurbsCurve' ):
            outputCurve = '{0}_{1}'.format(driverCurve, 'output')
            baseCurve = cmds.createNode('nurbsCurve')
            cmds.rename(cmds.listRelatives(baseCurve, p=True)[0], outputCurve)
            hairSystem = cmds.createNode( 'hairSystem', n='{0}_{1}'.format(driverCurve, 'hairSystemShape') )
            follicle = cmds.createNode( 'follicle', n='{0}_{1}'.format(driverCurve, 'follicleShape') )
            cmds.setAttr('{0}.restPose'.format(follicle), 1)
            cmds.setAttr('{0}.active'.format(hairSystem), 1)

            # Connect nodes to set up simulation

            # Rebuild driverCurve
            rebuildCurve1 = cmds.createNode('rebuildCurve', n='rebuildCurve1')
            rebuiltCurveOutput = cmds.createNode( 'nurbsCurve', n=( driverCurve + 'rebuiltCurveShape1') )


            # Generate curve output
            cmds.connectAttr((driverCurveShape + '.worldSpace[0]'), (rebuildCurve1 + '.inputCurve'))
            cmds.connectAttr((rebuildCurve1 + '.outputCurve'), (rebuiltCurveOutput + '.create'))

            # Connect curves to follicle
            cmds.connectAttr((driverCurve + '.worldMatrix[0]'), (follicle + '.startPositionMatrix'))
            cmds.connectAttr((rebuiltCurveOutput + '.local'), (follicle + '.startPosition'))

            # Connect follicle to output curve
            cmds.connectAttr((follicle + '.outCurve'), (outputCurve + '.create'))

            # Connect time to hair system and nucleus
            if not nucleus:
                nucleus = cmds.createNode( 'nucleus', n='{0}_{1}'.format(driverCurve, 'nucleus'))
                cmds.connectAttr('time1.outTime', (nucleus + '.currentTime'))
            cmds.connectAttr('time1.outTime', (hairSystem + '.currentTime'))

            # Connect hair system and nucleus together
            nucleus_connections_ia = cmds.listConnections('{0}.inputActive'.format(nucleus))
            nucleus_connections_ias = cmds.listConnections('{0}.inputActiveStart'.format(nucleus))
            if nucleus_connections_ia == None:
                con = 0
            else:
                con = len(nucleus_connections_ia)
            cmds.connectAttr((hairSystem + '.currentState'), (nucleus + '.inputActive[{0}]'.format(str(con))))
            cmds.connectAttr((hairSystem + '.startState'), (nucleus + '.inputActiveStart[{0}]'.format(str(con))))
            cmds.connectAttr((nucleus + '.outputObjects[0]'), (hairSystem + '.nextState'))
            cmds.connectAttr((nucleus + '.startFrame'), (hairSystem + '.startFrame'))

            # Connect hair system to follicle
            cmds.connectAttr((hairSystem + '.outputHair[0]'), (follicle + '.currentPosition'))
            cmds.connectAttr((follicle + '.outHair'), (hairSystem + '.inputHair[0]'))

            # rename outputCurve
            # Return all created objects from simulation.
            # return [outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput]
            return outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput

        else:
            raise RuntimeError("Method 'makeCurveDynamic()' expects a curve.")

    def createControlCurve(self, jointChain):
        u"""シミュレーション用のコントローラを作成します

        params
        ----------------
        jointChain: list
        ----------------
        """
        if cmds.objectType( jointChain[0], isType='joint' ):
            baseCtrlName = '{0}_aol_ctrl'.format(jointChain[0])

            # Create control curve
            baseControl = cmds.curve(d=1,n='BASE_CTL',p=[(0,0,0),(0.75,0,0),(1,0.25,0),(1.25,0,0),(1,-0.25,0),(0.75,0,0),(1,0,0.25),(1.25,0,0),(1,0,-0.25),(1,0.25,0),(1,0,0.25),(1,-0.25,0),(1,0,-0.25),(0.75,0,0),(0,0,0),(-0.75,0,0),(-1,0.25,0),(-1.25,0,0),(-1,-0.25,0),(-0.75,0,0),(-1,0,0.25),(-1.25,0,0),(-1,0,-0.25),(-1,0.25,0),(-1,0,0.25),(-1,-0.25,0),(-1,0,-0.25),(-0.75,0,0),(0,0,0),(0,0.75,0),(0,1,-0.25),(0,1.25,0),(0,1,0.25),(0,0.75,0),(-0.25,1,0),(0,1.25,0),(0.25,1,0),(0,1,0.25),(-0.25,1,0),(0,1,-0.25),(0.25,1,0),(0,0.75,0),(0,0,0),(0,-0.75,0),(0,-1,-0.25),(0,-1.25,0),(0,-1,0.25),(0,-0.75,0),(-0.25,-1,0),(0,-1.25,0),(0.25,-1,0),(0,-1,-0.25),(-0.25,-1,0),(0,-1,0.25),(0.25,-1,0),(0,-0.75,0),(0,0,0),(0,0,-0.75),(0,0.25,-1),(0,0,-1.25),(0,-0.25,-1),(0,0,-0.75),(-0.25,0,-1),(0,0,-1.25),(0.25,0,-1),(0,0.25,-1),(-0.25,0,-1),(0,-0.25,-1),(0.25,0,-1),(0,0,-0.75),(0,0,0),(0,0,0.75),(0,0.25,1),(0,0,1.25),(0,-0.25,1),(0,0,0.75),(-0.25,0,1),(0,0,1.25),(0.25,0,1),(0,0.25,1),(-0.25,0,1),(0,-0.25,1),(0.25,0,1),(0,0,0.75)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83])
            # baseControl = cmds.circle( n=baseCtrlName, nr=(1, 0, 0) )
            cmds.rename(baseControl, baseCtrlName)
            cmds.rename(cmds.listRelatives(baseCtrlName, s=True)[0], '{0}Shape'.format(baseCtrlName))

            # Set attributes on control curve
            # dynamicOptions
            cmds.addAttr(baseCtrlName, ln='dynamicJoints', keyable=True, at='enum', en='____________')
            cmds.setAttr('{0}.dynamicJoints'.format(baseCtrlName), l=True)
            cmds.addAttr(ln='autoOverlap', sn='autoOverlap', at='bool', k=True, h=False)
            cmds.addAttr(ln='stopFollicle', sn='stopFollicle', at='float', k=True)
            cmds.setAttr('{0}.stopFollicle'.format(baseCtrlName), l=True)

            # Snap control curve to base joint and clean up control curve
            ctrlOffset = cmds.createNode('transform', n='{0}_offset'.format(baseCtrlName), ss=True)
            cmds.parent(baseCtrlName, ctrlOffset)
            baseJointConstraint = cmds.parentConstraint(jointChain[0], ctrlOffset, mo=False)
            cmds.delete(baseJointConstraint)
            # cmds.makeIdentity( baseCtrlName, apply=True, t=True, r=True, s=True, n=2 )

            return baseCtrlName, ctrlOffset

        else:
            raise RuntimeError("Method 'createControlCurve()' expects a joint as the first index.")

    def createAutoOverlapExpression(self, baseCtrl, hairSystem, nucleus):
        u"""インタラクティブにシミュレーションさせるエクスプレッションを設定します
        シミュレーション用のコントローラのautoOverlapアトリビュートでON, OFFを切り替えます

        params
        ----------------
        baseCtrl: string
        hairSystem: string
        nucleus: string
        ----------------
        """

        # set nucleusShare
        base = cmds.textFieldButtonGrp(self.ncls_tfbg, q=True, tx=True)
        exp_name = '{0}_autoOverlap_exp'.format(base)
        if base == '':
            base = baseCtrl
            exp_name = '{0}_autoOverlap_exp'.format(base)
        elif base != '':
            exp_name = '{0}_autoOverlap_exp'.format(base)
            cmds.checkBox(self.cten_cb, e=True, v=True)
        if not cmds.objExists(base):
            print('{0} is not exists.'.format(base))
            return

        listAttr = cmds.listAttr(base, ud=True)
        if not 'nucleusShare' in listAttr:
            cmds.addAttr(base, ln='nucleusShare', dt='string', multi=True)

        multi_indices = cmds.getAttr('{0}.nucleusShare'.format(base), mi=True)
        if not multi_indices:
            cmds.setAttr('{0}.nucleusShare[0]'.format(base), baseCtrl, type='string')
        else:
            cmds.setAttr('{0}.nucleusShare[{1}]'.format(base, str(len(multi_indices))), baseCtrl, type='string')

        # Break time connections from hair system and nucleus
        nucCurrTime = '%s.currentTime' % nucleus
        hairCurrTime = '%s.currentTime' % hairSystem
        try:
            cmds.disconnectAttr('time1.outTime', hairCurrTime)
            cmds.disconnectAttr('time1.outTime', nucCurrTime)
        except Exception as e:
            print(e)

        if cmds.objExists(exp_name):
            cmds.delete(exp_name)

        multi_indices = cmds.getAttr('{0}.nucleusShare'.format(base), mi=True)

        # refresh string
        refresh_string_buf = []
        for i in range(len(multi_indices)):
            baseCtrl = cmds.getAttr('{0}.nucleusShare[{1}]'.format(base, str(i)))
            if not base == baseCtrl:
                listAttr = cmds.listAttr(baseCtrl, ud=True)
                if not 'nucleusShareParent' in listAttr:
                    cmds.addAttr(baseCtrl, ln='nucleusShareParent', dt='string')
                cmds.setAttr('{0}.nucleusShareParent'.format(baseCtrl), base, type='string')
            if ':' in baseCtrl:
                set_refresh = baseCtrl.split(':')[-1]
            else:
                set_refresh = baseCtrl
            refresh_string = ('\tfloat $'+set_refresh+'refresh_tx = ' + baseCtrl + '.translateX; \n'
                              '\tfloat $'+set_refresh+'refresh_ty = ' + baseCtrl + '.translateY; \n'
                              '\tfloat $'+set_refresh+'refresh_tz = ' + baseCtrl + '.translateZ; \n'
                              '\tfloat $'+set_refresh+'refresh_rx = ' + baseCtrl + '.rotateX; \n'
                              '\tfloat $'+set_refresh+'refresh_ry = ' + baseCtrl + '.rotateY; \n'
                              '\tfloat $'+set_refresh+'refresh_rz = ' + baseCtrl + '.rotateZ; \n\n')

            refresh_string_buf.append(refresh_string)

        # playbackDynamic
        cmds.addAttr(baseCtrl, ln="playbackDynamic", keyable=True, at='bool')
        cmds.addAttr(baseCtrl, ln="startFrame", keyable=True, at='float', k=True)
        cmds.connectAttr('{0}.startFrame'.format(baseCtrl), '{0}.startFrame'.format(nucleus), f=True)
        cmds.setAttr('{0}.startFrame'.format(baseCtrl), cmds.currentTime(q=True))

        listAttr = cmds.listConnections('{0}.currentTime'.format(nucleus), s=True)
        aoExpression = ('if (' + base + '.autoOverlap == 1 && ' + base + '.playbackDynamic == 0) { \n'
                        '\t' + nucleus + '.currentTime += 1; \n'
                        '' + ''.join(refresh_string_buf) + ''
                        '} else if (' + base + '.autoOverlap == 0 && ' + base + '.playbackDynamic == 0) { \n'
                        '\t' + nucleus + '.currentTime = ' + base + '.stopFollicle; \n'
                        '} else if (' + base + '.autoOverlap == 0 && ' + base + '.playbackDynamic == 1) { \n'
                        '\t' + nucleus + '.currentTime = frame; \n}'
                        )
        # Set up auto overlap expression
        cmds.expression(n =exp_name, string=aoExpression, ae=False)

        # Connect current time of nucleus to current time of hair system
        cmds.connectAttr(nucCurrTime, hairCurrTime)

    def createAutoOverlapChain(self, jointHierarchy, nucleus=None):
        u"""コア関数になります
        jointHierarchy引数に渡されたFKジョイント、またはFKコントローラに対してシミュレーションを設定します

        以下の順に実行されます
        createCurveFromJoints()
        makeCurveDynamic()
        createControlCurve()
        createAutoOverlapExpression()

        params
        ----------------
        jointHierarchy: list
            2つ以上指定しなければエラーが返されます
        nucleus: string
            既存のnucleusに適用させたい場合に設定します
        ----------------
        """

        # Create auto overlap chain from joint hierarchy. If one joint or no joints are selected, stop the script and prompt the user.
        if jointHierarchy and cmds.objectType( jointHierarchy[0], isType='joint' ) and len(jointHierarchy) > 1:
            # ao = AutoOverlap()

            # We can now call our createCurve method to generate our curve.
            driverCurve = self.createCurveFromJoints(jointHierarchy)
            print('createCurveFromJoints:{0}'.format(driverCurve))


            # Make our generated curve dynamic.
            # dynamicCurveObjects = ao.makeCurveDynamic(driverCurve, nucleus)
            outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput = self.makeCurveDynamic(driverCurve, nucleus)
            print(outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput)
            # print('makeCurveDynamic:{0}'.format(dynamicCurveObjects))

            # Create spline IK handle from a base joint, an end joint, and a curve.
            splineIK = cmds.ikHandle(sj=jointHierarchy[0], ee=jointHierarchy[-1], sol='ikSplineSolver', c=outputCurve, ccv=False, p=2, w=.5, n='{0}_aol_ikHandle'.format(jointHierarchy[0]))

            # Create control curve.
            controlCurve, ctrlOffset = self.createControlCurve(jointHierarchy)
            print('createControlCurve:{0}'.format(controlCurve))


            # Parent constrain control curve to follicle curve.
            cmds.parentConstraint(controlCurve, driverCurve, mo=True)

            # Create auto overlap expression.
            self.createAutoOverlapExpression(controlCurve, hairSystem, nucleus)
            print('createAutoOverlapExpression:{0}, {1}, {2}'.format(controlCurve, hairSystem, nucleus))


            # Group all objects created by makeCurvesDynamic command.
            dynamicCurveObjects = [outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput]
            dynamicGrp = cmds.group(dynamicCurveObjects, n='dynamicCurve_' + controlCurve + '_grp' )
            cmds.parent(driverCurve, dynamicGrp)
            cmds.parent(splineIK[0], dynamicGrp)

            """
            CreateCollisions
            """
            # collision = cmds.polySphere(cuv=2, sy=20, sx=20, r=10, ax=(0, 1, 0), n='collision_{0}'.format(jointHierarchy[0]))
            # rigidBody = 'collide_{0}'.format(collision[0])
            # cmds.delete(ch=True)
            # rigidBodies = cmds.ls(type='nRigid')
            # if rigidBodies == []:
                # collide = mel.eval('makeCollideNCloth;')
            # elif len(rigidBodies) > 0:
                # mel.eval('string $nucleus = "{0}";'.format(nucleus))
                # mel.eval('setActiveNucleusNode( $nucleus );')
                # collide = mel.eval('makeCollideNCloth;')
            # cmds.setAttr('{0}.thickness'.format(collide[0]), 1)
            # cmds.rename(cmds.listRelatives(collide[0], p=True)[0], rigidBody)
            # cmds.parent(rigidBody, dynamicGrp)
            # cmds.parent(collision[0], dynamicGrp)
            cmds.parent(ctrlOffset, dynamicGrp)

            # Hide any unused nodes from view port.
            unusedObjects = cmds.listRelatives( dynamicGrp, allDescendents=True )
            for objects in unusedObjects:
                cmds.setAttr((objects + '.visibility'), 0)

            # collision vis
            # cmds.setAttr("{0}.visibility".format(collision[0]), 1)
            # cmds.setAttr("{0}Shape.visibility".format(collision[0]), 1)
            # ctrl vis
            cmds.setAttr("{0}.visibility".format(ctrlOffset), 1)
            cmds.setAttr("{0}.visibility".format(controlCurve), 1)
            cmds.setAttr("{0}Shape.visibility".format(controlCurve), 1)

            """
            Add attributes and connections
            """
            # cmds.setAttr("{0}.active".format(hairSystem), 1)
            cmds.setAttr("{0}.startDirection".format(follicle), 1)

            # ikOptions
            cmds.addAttr(controlCurve, ln='ikOptions', keyable=True, at='enum', en='____________')
            cmds.setAttr('{0}.ikOptions'.format(controlCurve), l=True)
            cmds.addAttr(controlCurve, ln='roll', keyable=True, at='float', dv=0.0)
            cmds.addAttr(controlCurve, ln='twist',  keyable=True, at='float', dv=0.0)
            # dynamicOptions
            cmds.addAttr(controlCurve, ln='dynamicOptions', keyable=True, at='enum', en='____________')
            cmds.setAttr('{0}.dynamicOptions'.format(controlCurve), l=True)
            # Add attributes to controller for the dynamics
            cmds.addAttr(controlCurve, min=0, ln='stiffness', max=1, keyable=True, at='double', dv=0.15)
            cmds.addAttr(controlCurve, min=0, ln='lengthFlex', max=1, keyable=True, at='double', dv=0)
            cmds.addAttr(controlCurve, ln="pointLock", en="No Attach:Base:Tip:BothEnds:", at="enum", k=True)
            cmds.setAttr('{0}.pointLock'.format(controlCurve), 1)
            cmds.addAttr(controlCurve, min=0, ln="drag", max=1, keyable=True, at='double', dv=.05)
            cmds.addAttr(controlCurve, min=0, ln='friction', max=1, keyable=True, at='double', dv=0.5)
            cmds.addAttr(controlCurve, min=0, ln="gravity", max=10, keyable=True, at='double', dv=1)
            cmds.addAttr(controlCurve, min=0, ln="turbulenceStrength", max=1, keyable=True, at='double', dv=0)
            cmds.addAttr(controlCurve, min=0, ln="turbulenceFrequency", max=2, keyable=True, at='double', dv=0.2)
            cmds.addAttr(controlCurve, min=0, ln="turbulenceSpeed", max=2, keyable=True, at='double', dv=0.2)
            cmds.addAttr(controlCurve, min=0, ln="damp", max=10, keyable=True, at='double', dv=0, k=True)
            cmds.addAttr(controlCurve, min=0, ln="mass", max=10, keyable=True, at='double', dv=1.0, k=True)
            cmds.addAttr(controlCurve, min=0, ln="attractionDamp", max=1, keyable=True, at='double', dv=0, k=True)
            cmds.addAttr(controlCurve, min=0, ln="startCurveAttract", max=1, keyable=True, at='double', dv=0, k=True)
            cmds.addAttr(controlCurve, min=0, ln="motionDrag", max=1, keyable=True, at='double', dv=0, k=True)
            # collisions
            cmds.addAttr(controlCurve, ln='collisionOptions', keyable=True, at='enum', en='____________')
            cmds.setAttr('{0}.collisionOptions'.format(controlCurve), l=True)
            cmds.addAttr(controlCurve, ln="useNucleusSolver", keyable=True, at='bool')
            cmds.addAttr(controlCurve, min=0, ln="stickiness", keyable=True, at='double', dv=0.0, k=True)

            cmds.connectAttr(controlCurve + ".roll", splineIK[0] + ".roll", f=True)
            cmds.connectAttr(controlCurve + ".twist", splineIK[0] + ".twist", f=True)
            #Connect attributes on the controller sphere to the follicle node
            cmds.connectAttr(controlCurve + ".pointLock", follicle + ".pointLock", f=True)
            #Connect attribute on the controller sphere to the hair system node
            cmds.connectAttr(controlCurve + ".stiffness", hairSystem + ".stiffness", f=True)
            cmds.connectAttr(controlCurve + ".lengthFlex", hairSystem + ".lengthFlex", f=True)
            cmds.connectAttr(controlCurve + ".damp", hairSystem + ".damp", f=True)
            cmds.connectAttr(controlCurve + ".drag", hairSystem + ".drag", f=True)
            cmds.connectAttr(controlCurve + ".friction", hairSystem + ".friction", f=True)
            cmds.connectAttr(controlCurve + ".mass", hairSystem + ".mass", f=True)
            cmds.connectAttr(controlCurve + ".gravity", hairSystem + ".gravity", f=True)
            cmds.connectAttr(controlCurve + ".turbulenceStrength", hairSystem + ".turbulenceStrength", f=True)
            cmds.connectAttr(controlCurve + ".turbulenceFrequency", hairSystem + ".turbulenceFrequency", f=True)
            cmds.connectAttr(controlCurve + ".turbulenceSpeed", hairSystem + ".turbulenceSpeed", f=True)
            cmds.connectAttr(controlCurve + ".attractionDamp", hairSystem + ".attractionDamp", f=True)
            cmds.connectAttr(controlCurve + ".startCurveAttract", hairSystem + ".startCurveAttract", f=True)
            cmds.connectAttr(controlCurve + ".motionDrag", hairSystem + ".motionDrag", f=True)
            # collisions
            cmds.connectAttr(controlCurve + ".useNucleusSolver", hairSystem + ".active", f=True)
            cmds.connectAttr(controlCurve + ".stickiness", hairSystem + ".stickiness", f=True)

            # scale lock
            cmds.setAttr(controlCurve + '.sx', l=True, cb=False, k=False)
            cmds.setAttr(controlCurve + '.sy', l=True, cb=False, k=False)
            cmds.setAttr(controlCurve + '.sz', l=True, cb=False, k=False)

            # Return group containing all needed objects to make curve dynamic.

            """
            Advanced Twist
            """
            cmds.setAttr(splineIK[0]+'.dTwistControlEnable', True)
            controlCurve_dup = cmds.duplicate(controlCurve, n=controlCurve+'_up', po=True)[0]
            cmds.parent(controlCurve_dup, controlCurve)
            cmds.xform(controlCurve_dup, t=[0, 10, 0], os=True)

            return dynamicGrp, controlCurve
        else:
            cmds.confirmDialog( title='Please select joint.', message='Please make sure to select a joint with at least one child joint.' )
            raise RuntimeError("Selection was not a joint with at least one child joint.")


    def create_dynamics(self, *args, **kwargs):
        u"""UIから実行するための関数になります
        createAutoOverlapChain()を実行します
        """
        sel = cmds.ls(os=True, r=True)
        if not sel or not 1 < len(sel):
            cmds.warning('Please select FK ctrls.')
            return

        end = create_end_joint(node=sel[-1], end_parent=sel[-2])
        sel.append(end)

        bake_sets = '{0}_aol_bake_sets'.format(sel[0])
        if not cmds.objExists(bake_sets):
            cmds.sets(em=True, n=bake_sets)

        aol_joints = []
        for i, obj in enumerate(sel):
            aol_jnt = cmds.createNode('joint', n='{0}_aol_dynamic_jnt'.format(obj), ss=True)
            cmds.matchTransform(aol_jnt, obj)
            cmds.makeIdentity(aol_jnt, n=False, s=False, r=True, t=False, apply=True, pn=True)
            if i == 0:
                pass
            else:
                cmds.parent(aol_jnt, aol_joints[-1])

            aol_joints.append(aol_jnt)
            cmds.sets(obj, add=bake_sets)

        for i, (aol_jnt, obj) in enumerate(zip(aol_joints, sel)):
            cmds.orientConstraint(aol_jnt, obj, w=True, mo=True)

        for j in aol_joints[0]:
            if j == '|':
                cmds.confirmDialog( title='Please rename joint.', message=('Joint "' + aol_joints[0] + '" has | characters dividing the name. Please rename the joint.') )
                raise RuntimeError("Joint cannot have dividers in name.")

        cten_cb = cmds.checkBox(self.cten_cb, q=True, v=True)
        if cten_cb:
            ncls_tfg = cmds.textFieldGrp(self.ncls_tfg, q=True, tx=True)
            if cmds.objExists(ncls_tfg):
                nucleus_name = ncls_tfg
            else:
                nucleus_name = None

        else:
            nucleus_name = None

        dynamicGrp, ctrl = self.createAutoOverlapChain(aol_joints, nucleus=nucleus_name)
        cmds.parent(aol_joints[0], dynamicGrp)

        ctrl_sets = '{0}_aol_ctrl_sets'.format(sel[0])
        if not cmds.objExists(ctrl_sets):
            cmds.sets(em=True, n=ctrl_sets)

        cmds.sets(ctrl, add=ctrl_sets)
        cmds.sets(bake_sets, add=ctrl_sets)

        ctrl_size = cmds.floatSliderGrp(self.ctrl_size_fsg, q=True, v=1)
        cmds.select('{0}.cv[*]'.format(ctrl), r=True)
        cmds.scale(ctrl_size, ctrl_size, ctrl_size)

        cmds.select(ctrl, r=True)

    def create_rigidBody(self, selection=None, nucleus=None):
        u"""nucleusとオブジェクトを選択してリジッドボディを設定します
        """
        if selection and nucleus:
            if 'nucleus' == cmds.objectType(nucleus) and cmds.objExists(nucleus):
                for obj in selection:
                    if cmds.objExists(obj):
                        rigidBody = 'rigidBody_{0}'.format(obj)
                        if not cmds.objExists(rigidBody):
                            cmds.select(obj, r=True)
                            rigidBodies = cmds.ls(type='nRigid')
                            if rigidBodies == []:
                                collide = mel.eval('makeCollideNCloth;')
                            else:
                                sh = cmds.listRelatives(obj, s=True)
                                if sh:
                                    mesh_shape = sh[0]
                                    listConnections = cmds.listConnections('{0}.worldMesh[0]'.format(mesh_shape), d=True)

                                collide = cmds.ls(cmds.listRelatives(listConnections, s=True), type='nRigid')

                                if collide:
                                    cmds.connectAttr('{0}.currentState'.format(collide[0]), '{0}.inputPassive[0]'.format(nucleus), f=True)
                                    cmds.connectAttr('{0}.startState'.format(collide[0]), '{0}.inputPassiveStart[0]'.format(nucleus), f=True)
                                else:
                                    mel.eval('string $nucleus = "{0}";'.format(nucleus))
                                    mel.eval('setActiveNucleusNode( $nucleus );')
                                    collide = mel.eval('makeCollideNCloth;')

                            if collide == []:
                                continue
                            else:
                                cmds.setAttr('{0}.thickness'.format(collide[0]), 1)
                                cmds.rename(cmds.listRelatives(collide[0], p=True)[0], rigidBody)
                        else:
                            cmds.warning('"{0}" is already exists.'.format(rigidBody))
        else:
            cmds.warning('Set "selection" and "nucleus".')

    def do_create_rigidBody(self, *args, **kwargs):
        u"""UIから実行するための関数になります
        create_rigidBody()を実行します
        """
        sel = cmds.ls(os=True)
        nucleus = sel[0]
        selection = sel[1::]

        self.create_rigidBody(selection=selection, nucleus=nucleus)

if __name__ == '__main__':
    aol = AutoOverlap()
    aol.ui()
