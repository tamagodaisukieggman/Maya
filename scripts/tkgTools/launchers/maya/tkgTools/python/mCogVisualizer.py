# mCogVisualizer
# v.0.1
# to do:
# - smarter cleanup
# - constraint weights exposed on main group
#

#installation:

#    1) open script using script editor
#    2) Go to File -> Save Script to Shelf and label it mCog

#Usage:

#    For regular bipeds:

#        1) find the skin bones and make sure you can select them
#        2) select the following joints by holding shift:
#            - closet joint at the base of the neck (usually first neck bone)
#            - the knee joint on each leg
#        3) press the script button to create the mCog_Grp, mCogVizSet and mCogViz_Layer. You should see
#        a green sphere with an attached cone pointing to the ground
#        4) find the mCogConstraint and set the offset weight of the neck joint to 2


import maya.cmds as cmds
import maya.mel as mel



def makeMCogViz(*args):

    deleteOldMcog()

    #collect selection
    mAnchors=cmds.ls(selection=True)

    if len(mAnchors) < 2:
        cmds.warning('youm must select more than 1 object')
    else:

        #create offset nodes for anchors
        for i in range (len(mAnchors)):
            cmds.createNode('transform', n=mAnchors[i]+'AnchorOffset', p=mAnchors[i])

        try:
            cmds.select('*AnchorOffset')
        except:
            print('*AnchorOffset doesnt exist. trying referenced version')

        try:
            cmds.select('*:*AnchorOffset')
        except:
            print('*:*AnchorOffset doesnt exist')

        mAnchorsOffset = cmds.ls(selection=True)

        for i in range (len(mAnchorsOffset)):
            cmds.setAttr(mAnchorsOffset[i]+'.rx', keyable=False, channelBox=False, lock=True)
            cmds.setAttr(mAnchorsOffset[i]+'.ry', keyable=False, channelBox=False, lock=True)
            cmds.setAttr(mAnchorsOffset[i]+'.rz', keyable=False, channelBox=False, lock=True)
            cmds.setAttr(mAnchorsOffset[i]+'.tx', keyable=False, channelBox=True)
            cmds.setAttr(mAnchorsOffset[i]+'.ty', keyable=False, channelBox=True)
            cmds.setAttr(mAnchorsOffset[i]+'.tz', keyable=False, channelBox=True)
            cmds.setAttr(mAnchorsOffset[i]+'.sx', keyable=False, channelBox=False, lock=True)
            cmds.setAttr(mAnchorsOffset[i]+'.sy', keyable=False, channelBox=False, lock=True)
            cmds.setAttr(mAnchorsOffset[i]+'.sz', keyable=False, channelBox=False, lock=True)

        # make connecting geo
        makeBasLine()

        makeCog()
        cmds.connectAttr('mCog.t', 'mBasLine.vtx[6]')
        cmds.connectAttr('mCog.t', 'mBasLine.vtx[7]')
        cmds.connectAttr('mCog.t', 'mBasLine.vtx[8]')
        cmds.connectAttr('mCog.t', 'mBasLine.vtx[9]')
        cmds.connectAttr('mCog.t', 'mBasLine.vtx[10]')
        cmds.connectAttr('mCog.t', 'mBasLine.vtx[11]')

        makeBas()
        cmds.connectAttr('mBas.t', 'mBasLine.vtx[0]')
        cmds.connectAttr('mBas.t', 'mBasLine.vtx[1]')
        cmds.connectAttr('mBas.t', 'mBasLine.vtx[2]')
        cmds.connectAttr('mBas.t', 'mBasLine.vtx[3]')
        cmds.connectAttr('mBas.t', 'mBasLine.vtx[4]')
        cmds.connectAttr('mBas.t', 'mBasLine.vtx[5]')


        # point constrain mBas to mCog
        #mBasConstraint = cmds.pointConstraint('mCog', 'mBas', mo=True, skip='y', weight=1, name='mBasConstraint')

        cmds.connectAttr('mCog.tx', 'mBas.tx')
        cmds.connectAttr('mCog.tz', 'mBas.tz')

        # point constraint mCog to offset nodes
        if cmds.objExists('mCogConstraint'):
            cmds.delete('mCogConstraint')
        mCogConstraint = cmds.pointConstraint(mAnchorsOffset , 'mCog', mo=False, name='mCogConstraint', wal=True)


        cmds.createNode('transform', name='mCog_Grp')

        #add scale control for cog
        cmds.addAttr(ln='mCogScale', nn='M Cog Scale', at='float', dv=1, keyable=False, hidden=False)
        cmds.setAttr('mCog_Grp.mCogScale', cb=True)
        cmds.connectAttr('mCog_Grp.mCogScale', 'mCog.sx')
        cmds.connectAttr('mCog_Grp.mCogScale', 'mCog.sy')
        cmds.connectAttr('mCog_Grp.mCogScale', 'mCog.sz')


        #add scale control for mBas
        cmds.addAttr(ln='mBasScale', nn='M Bas Scale', at='float', dv=1, keyable=False, hidden=False)
        cmds.setAttr('mCog_Grp.mBasScale', cb=True)
        cmds.connectAttr('mCog_Grp.mBasScale', 'mBas.sx')
        cmds.connectAttr('mCog_Grp.mBasScale', 'mBas.sy')
        cmds.connectAttr('mCog_Grp.mBasScale', 'mBas.sz')

        cmds.setAttr('mCog_Grp.rx', keyable=False, channelBox=False, lock=True)
        cmds.setAttr('mCog_Grp.ry', keyable=False, channelBox=False, lock=True)
        cmds.setAttr('mCog_Grp.rz', keyable=False, channelBox=False, lock=True)
        cmds.setAttr('mCog_Grp.tx', keyable=False, channelBox=False, lock=True)
        cmds.setAttr('mCog_Grp.ty', keyable=False, channelBox=False, lock=True)
        cmds.setAttr('mCog_Grp.tz', keyable=False, channelBox=False, lock=True)
        cmds.setAttr('mCog_Grp.sx', keyable=False, channelBox=False, lock=True)
        cmds.setAttr('mCog_Grp.sy', keyable=False, channelBox=False, lock=True)
        cmds.setAttr('mCog_Grp.sz', keyable=False, channelBox=False, lock=True)


        cmds.select(mAnchorsOffset,'mCog','mBas','mBasLine','mCog_Grp')
        cmds.sets(n='mCogVizSet')

        try:
            cmds.delete('mCogViz_Layer')
        except:
            print('layer doesnt exist')
        cmds.createDisplayLayer(name='mCogViz_Layer')
        cmds.setAttr("{}.displayType".format('mCogViz_Layer'), 2) # Change layer to reference.


        cmds.parent('mCog','mBas','mBasLine', 'mCog_Grp')









def deleteOldMcog(*args):
    #clean up old mCogViz if exists
    try:
        cmds.select('mCogVizSet')
        cmds.delete()
    except:
        print ('no previous mcog exists')

#color material for objects.
def assignMat(obj,R,G,B):

    #delete old material if it exists

    try:
        cmds.delete(obj+'Color')
    except:
        print('materialDoesntExsit')

    cmds.shadingNode('lambert', name=obj+"Color", asShader=True)
    cmds.select(obj)
    cmds.hyperShade(assign=obj+"Color")
    cmds.setAttr(obj+'Color.transparency', .65, .65, .65, type='double3')
    cmds.setAttr(obj+'Color.color', R, G, B, type='double3')
    cmds.setAttr(obj+'Color.ambientColor', .5, .5, .5, type='double3')
    cmds.setAttr(obj+'Color.diffuse', 4)

#base of support object
def makeBas(*args):

    mBas = cmds.polyCone(n="mBas")
    cmds.xform('mBas', r=True, translation=[0,1,0], rotation=[180,0,0])
    cmds.move(0, 0, 0, 'mBas.rotatePivot', 'mBas.scalePivot')
    cmds.makeIdentity(apply=True)
    cmds.setAttr('mBasShape.castsShadows', 0)
    cmds.setAttr('mBasShape.receiveShadows', 0)
    cmds.setAttr('mBas.alwaysDrawOnTop',1)

    #lock and hide attributes
    cmds.setAttr('mBas.rx', keyable=False, channelBox=False, lock=True)
    cmds.setAttr('mBas.ry', keyable=False, channelBox=False, lock=True)
    cmds.setAttr('mBas.rz', keyable=False, channelBox=False, lock=True)
    cmds.setAttr('mBas.tx', keyable=False, channelBox=False)
    cmds.setAttr('mBas.ty', keyable=False, channelBox=False, lock=True)
    cmds.setAttr('mBas.tz', keyable=False, channelBox=False)
    cmds.setAttr('mBas.sx', keyable=False, channelBox=False)
    cmds.setAttr('mBas.sy', keyable=False, channelBox=False)
    cmds.setAttr('mBas.sz', keyable=False, channelBox=False)

    assignMat('mBas',1,0,0)


def makeBasLine(*args):

    mBasLine = cmds.polyCylinder(n="mBasLine", radius=.1, height=.05, sx=6)
    cmds.setAttr('mBasLineShape.castsShadows', 0)
    cmds.setAttr('mBasLineShape.receiveShadows', 0)
    cmds.setAttr('mBasLine.alwaysDrawOnTop',1)
    cmds.move( 0, .5, 0, 'mBasLine')
    # cmds.makeIdentity(apply=True)
    assignMat('mBasLine',1,0,0)

#center of gravity object
def makeCog(*args):


    mCog = cmds.polyPlatonicSolid(name='mCog', ch=False, st=1)
    cmds.displaySmoothness('mCog', du=3, dv=3, pw=16, ps=4, po=3)
    cmds.setAttr('mCogShape.castsShadows', 0)
    cmds.setAttr('mCogShape.receiveShadows', 0)
    cmds.setAttr('mCog.alwaysDrawOnTop',1)

    cmds.setAttr('mCog.rx', keyable=False, channelBox=False, lock=True)
    cmds.setAttr('mCog.ry', keyable=False, channelBox=False, lock=True)
    cmds.setAttr('mCog.rz', keyable=False, channelBox=False, lock=True)
    cmds.setAttr('mCog.tx', keyable=False, channelBox=False)
    cmds.setAttr('mCog.ty', keyable=False, channelBox=False)
    cmds.setAttr('mCog.tz', keyable=False, channelBox=False)
    cmds.setAttr('mCog.sx', keyable=False, channelBox=False)
    cmds.setAttr('mCog.sy', keyable=False, channelBox=False)
    cmds.setAttr('mCog.sz', keyable=False, channelBox=False)



    assignMat('mCog',0,1,0)



# makeMCogViz()
