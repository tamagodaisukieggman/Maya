# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import os
import functools

class Main():
    def __init__(self):
        # self.modulename = os.path.basename(__file__).replace('.py', '')
        pass

    def function(self, byTool=None, bool=1):
        move = cmds.ls('*move*ctrl', recursive=1, type='transform')
        main = cmds.ls('*main*ctrl', recursive=1, type='transform')
        pelvis = cmds.ls('*pelvis*_fk_*ctrl', recursive=1, type='transform')

        ctrls = [move[0], main[0], pelvis[0]]
        follows = []
        consts = []
        for ctrl in ctrls:
            tfn = cmds.createNode('transform', n='{}_followTfn'.format(ctrl))
            follows.append(tfn)
            wt = cmds.xform(ctrl, q=1, t=1, ws=1)
            wr = cmds.xform(ctrl, q=1, ro=1, ws=1)
            cmds.xform(tfn, t=wt, ro=wr, ws=1, a=1)
            pa = cmds.parentConstraint(ctrl, tfn, w=1, mo=1)
            consts.append(pa[0])

        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        cmds.refresh(su=1)
        cmds.bakeResults(follows, sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
        cmds.refresh(su=0)

        cmds.delete(consts)

        moveFollow = cmds.ls('*move*ctrl*_followTfn', recursive=1, type='transform')
        mainFollow = cmds.ls('*main*ctrl*_followTfn', recursive=1, type='transform')
        pelvisFollow = cmds.ls('*pelvis*_fk_*ctrl*_followTfn', recursive=1, type='transform')

        constDict = {}
        constDict['w'] = 1
        constDict['mo'] = 1

        # cmds.orientConstraint(moveFollow[0], mainFollow[0], skip=('x', 'z'), **constDict)
        # cmds.parentConstraint(pelvisFollow[0], pelvisFollow[0].split('_followTfn')[0], w=1, mo=1)
        # cmds.pointConstraint(pelvisFollow[0], mainFollow[0].split('_followTfn')[0], skip=('y'), mo=0)
        # cmds.orientConstraint(moveFollow[0], mainFollow[0].split('_followTfn')[0], skip=('x', 'z'), **constDict)

        self.rotOrdPel = cmds.getAttr('{}.rotateOrder'.format(pelvisFollow[0].split('_followTfn')[0]))

        if byTool == None:
            cmds.orientConstraint(moveFollow[0], mainFollow[0], skip=('x', 'z'), **constDict)
            cmds.parentConstraint(pelvisFollow[0], pelvisFollow[0].split('_followTfn')[0], w=1, mo=1)
            cmds.pointConstraint(pelvisFollow[0], mainFollow[0].split('_followTfn')[0], skip=('y'), mo=0)
            cmds.orientConstraint(moveFollow[0], mainFollow[0].split('_followTfn')[0], skip=('x', 'z'), **constDict)

            cmds.refresh(su=1)
            cmds.bakeResults(ctrls, sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
            cmds.refresh(su=0)

        elif byTool == 1:
            rotOrdMov = cmds.getAttr('{}.rotateOrder'.format(moveFollow[0].split('_followTfn')[0]))
            cmds.setAttr('{}.rotateOrder'.format(moveFollow[0].split('_followTfn')[0]), self.rotOrdPel)

            ori = cmds.orientConstraint(pelvisFollow[0], moveFollow[0].split('_followTfn')[0], skip=('x', 'z'), mo=1)
            po = cmds.pointConstraint(pelvisFollow[0], moveFollow[0].split('_followTfn')[0], skip=('y'), mo=1)

            cmds.refresh(su=1)
            cmds.bakeResults(ctrls, sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
            cmds.refresh(su=0)

            cmds.setAttr('{}.rotateOrder'.format(moveFollow[0].split('_followTfn')[0]), rotOrdMov)

        elif byTool == 2:
            cmds.parentConstraint(pelvisFollow[0], pelvisFollow[0].split('_followTfn')[0], w=1, mo=1)

            rotOrdMan = cmds.getAttr('{}.rotateOrder'.format(moveFollow[0].split('_followTfn')[0]))
            cmds.setAttr('{}.rotateOrder'.format(mainFollow[0].split('_followTfn')[0]), self.rotOrdPel)

            ori = cmds.orientConstraint(pelvisFollow[0], mainFollow[0].split('_followTfn')[0], skip=('x', 'z'), mo=1)
            po = cmds.pointConstraint(pelvisFollow[0], mainFollow[0].split('_followTfn')[0], skip=('y'), mo=1)

            cmds.refresh(su=1)
            cmds.bakeResults(ctrls, sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
            cmds.refresh(su=0)

            cmds.setAttr('{}.rotateOrder'.format(mainFollow[0].split('_followTfn')[0]), rotOrdMan)

        cmds.delete(follows)

    def UI(self):
        self.window = 'Anim_FollowMove&Main'
        if cmds.window(self.window, q=True, ex=True):
            cmds.deleteUI(self.window)
        cmds.window(self.window, title=self.window, mb=True)
        self.widgets()
        cmds.showWindow(self.window)

    def widgets(self):
        move_label = 'FollowMove'
        root_label = 'FollowMain'
        cmdA = functools.partial(self.function, 1)
        cmdB = functools.partial(self.function, 2)

        cmds.columnLayout(adj=1)
        cmds.button(l=move_label, c=cmdA)
        cmds.button(l=root_label, c=cmdB)
"""
folloeMove = Main()
folloeMove.UI()
# bat
"""
# folloeMove = Main()
# folloeMove.function(byTool=1)
# folloeMove.function(byTool=2)
