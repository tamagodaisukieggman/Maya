# -- import modules
import pymel.core as pm
import maya.cmds as mc


# -- multi string replace
def multiReplace(str='', **kwargs):
    for k, v in kwargs.items():
        str = str.replace(k, v)
    return str


# -- skinCls -> joint
def getJointFromSkinCls(skn=''):
    skn = pm.PyNode(skn)
    return mc.listConnections('{0}.matrix'.format(skn.name()), s=1, d=0, t='joint', sh=1)


# -- weight copy
def skinWeightTransfer(src='', tgt=''):
    src = pm.PyNode(src)
    tgt = pm.PyNode(tgt)
    # -- bind
    skn = pm.mel.eval('findRelatedSkinCluster {0};'.format(src.name()))
    jtList = getJointFromSkinCls(skn)
    pm.skinCluster(jtList, tgt, tsb=True, bm=0, sm=0, nw=1, wd=0)
    # -- weight copy
    pm.copySkinWeights(src, tgt, ia='closestJoint', sa='closestPoint', nm=True)


# -- add pc rivet attr
def addRivetConstAttr(loc, comp, lock=False):
    loc = pm.PyNode(loc)
    if not pm.objExists('{0}.RivetConst_compornent'.format(loc.name())):
        pm.addAttr(loc, ln='RivetConst_compornent', dt='string')
        loc.RivetConst_compornent.set(comp)
    else:
        loc.RivetConst_compornent.set(comp)
    # -- lock
    if lock:
        loc.RivetConst_compornent.lock(True)


# -- pcRive to vertex
def rivetConstToVertex(vtx='', loc=''):
    # -- declare variables
    vtx = pm.Component(vtx)
    pos = pm.xform(vtx, ws=True, t=True, q=True)
    skn = pm.mel.eval('findRelatedSkinCluster {0};'.format(vtx.node().name()))
    rep = {'.':'_', '[':'_', ']':'_'}
    
    if skn:
        jtList = pm.skinCluster(skn, inf=True, q=True)
        wtList = pm.skinPercent(skn, vtx, v=True, q=True)

        # -- create dictionary joint and skin weight
        wtInfo = {}
        for i in range(len(jtList)):
            wtInfo.update({jtList[i]:wtList[i]})

        useInf = [inf for inf in wtInfo if wtInfo[inf] > 0.000]

        # -- create locator and set parent constrant
        if loc:
            loc = pm.PyNode(loc)
        else:
            loc = pm.spaceLocator(n='{0}rivetConst'.format(multiReplace(vtx.name(), **rep)))
        loc.t.set(pos)
        
        for inf in useInf:
            pm.parentConstraint(inf, loc, w=wtInfo[inf], mo=True)
        pc = pm.listRelatives(loc, typ='parentConstraint', c=True)[0]
        pc.rename('{0}parentConstraint'.format(multiReplace(vtx.name(), **rep)))
        
        # -- add pc rivet attr
        addRivetConstAttr(loc, vtx.name(), False)
        
        # -- return
        return loc.name()

    else:
        pm.warning('Please select vertex which is a skin binded mesh.')
        return None


# ---- rivet constraint to face
def rivetConstToFace(face='', loc=''):
    # -- declare variables
    face = pm.PyNode(face)
    loc  = pm.PyNode(loc)
    skn  = pm.mel.eval('findRelatedSkinCluster {0};'.format(face.name()))
    rep  = {'.':'_', '[':'_', ']':'_'}
    
    if skn:
        cpom = pm.createNode('closestPointOnMesh', n='_cpom')
        wtcv = pm.curve(d=1, p=[(0,0,0),(0,0,0)], k=(0,1), n='_wtCv')
        # -- get closest position
        cpom.inPosition.set(pm.xform(loc, ws=True, t=True, q=True))
        face.outMesh >> cpom.inMesh
        wtcv.t.set(cpom.result.position.get())

        pm.delete(pm.parentConstraint(wtcv, loc, w=1, mo=False))       
        skinWeightTransfer(face, wtcv)
        wtcvSkn = pm.mel.eval('findRelatedSkinCluster {0};'.format(wtcv.name()))

        # -- set weight
        jtList = pm.skinCluster(skn, inf=True, q=True)
        wtList = pm.skinPercent(wtcvSkn, wtcv.cv[0], v=True, q=True)

        # -- create dictionary joint and skin weight
        wtInfo = {}
        for i in range(len(jtList)):
            wtInfo.update({jtList[i]:wtList[i]})

        useInf = [inf for inf in wtInfo if wtInfo[inf] > 0.000]
      
        for inf in useInf:
            pm.parentConstraint(inf, loc, w=wtInfo[inf], mo=True)
        pc = pm.listRelatives(loc, typ='parentConstraint', c=True)[0]
        pc.rename('{0}parentConstraint'.format(multiReplace(face, **rep)))
             
        # -- add pc rivet attr
        addRivetConstAttr(loc, face, False)
        
        # -- delete 
        pm.delete(wtcv, cpom)
        
        # -- reselect and return
        pm.select(loc, r=True)
        return loc.name()

    else:
        pm.warning('Please select face which is a skin binded mesh and transform node like locator.')
        return None


def reConstraint(loc):
    # -- declare variables
    loc  = pm.PyNode(loc)
    comp = loc.rivetConst_compornent.get()
    
    # -- delete parentConstraint
    pc = pm.listRelatives(loc, typ='parentConstraint')
    if pc:
        pm.delete(pc[0])
    
    if '.vtx' in comp:
        rivetConstToVertex(comp, loc)
    else:
        rivetConstToFace(comp, loc)
 

class rivetConstraintUI(object):
    def __init__(self):
        self.__ver__          = '0.0.2'
        self.windowManageName = 'rivetConstraint'
        self.windowTitle      = 'Rivet Constraint v{0}'.format(self.__ver__)
        self.windowSize       = [240, 200]
        self._mayaHelp_url    = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._toolHelp_url    = r'https://wisdom.cygames.jp/display/tsubasa/%5BMaya%5D+Rivet+Constraint'

    def checkWindowOverlap(self):
        if pm.window(self.windowManageName, ex=True):
            pm.deleteUI(self.windowManageName)

    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)

    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)

    def createLocator(self):
        loc = pm.spaceLocator()
        return loc

    def getObjName(self):
        if pm.selected():
            obj = pm.selected()[-1]
            skn = pm.mel.eval('findRelatedSkinCluster {0};'.format(obj.name()))
            if skn:
                self.txf10.setText(obj.name())
            
            else:
                pm.warning('Please select skin object.')
        else:
            pm.warning('Please select skin object.')  

    def clearObjName(self):
        self.txf10.setText('')

    def rivetConstToVertex_run(self):
        vtxList = pm.selected()
        pm.select(d=True)
        for vtx in vtxList:
            rivetConstToVertex(vtx.name())
    
    def rivetConstToFace_run(self):
        obj = self.txf10.getText()
        for loc in pm.selected():
            if loc.getShape().type() == 'locator':
                rivetConstToFace(obj, loc)    

    def reConstraint_run(self):
        locList = pm.selected()
        pm.select(d=True)
        for loc in locList:
            reConstraint(loc)   

    def main(self):
        self.checkWindowOverlap()
        window = pm.window(self.windowManageName,
                           t  = self.windowTitle,
                           w  = self.windowSize[0],
                           h  = self.windowSize[1],
                           mb = True)
        # -- menu
        pm.menu(l  = 'Tools', 
                to = False)
        pm.menuItem(l = 'Create Locator',
                    i = 'out_locator.png',
                    c = pm.Callback(self.createLocator))
        pm.menu(l  ='Help', 
                to = False, 
                hm = True)
        pm.menuItem(l = 'Maya 2019 HELP',
                    c = self.show_mayaHelp)
        pm.menuItem(d = True)
        pm.menuItem(l = 'Tool HELP',
                    c = self.show_toolHelp)

        # -- base form layout
        self.fmL0 = pm.formLayout(nd=100)
        with self.fmL0:
            self.sep0 = pm.separator()

            # -- main form layout
            self.fmL1 = pm.formLayout(nd=100)
            with self.fmL1:
                self.itb10 = pm.iconTextButton(st = 'iconAndTextHorizontal', 
                                               i1 = 'out_locator.png', 
                                              bgc = (0.35, 0.35, 0.35),
                                                l = 'Create to Vertex', 
                                                c = pm.Callback(self.rivetConstToVertex_run), 
                                              ann = 'Select vertex of skin object.',
                                                h = 28,
                                               mh = 5,
                                               mw = 5)
                self.sep10 = pm.separator()
                self.txf10 = pm.textField(pht='skin object', h=24)
                self.itb11 = pm.iconTextButton(st = 'iconOnly', 
                                               i1 = 'arrowDown.png', 
                                               w  = 20, 
                                               h  = 20,)
                self.opm10 = pm.popupMenu(b=1) 
                pm.menuItem(l = 'get', 
                            i = 'transformPlus.png', 
                            c = pm.Callback(self.getObjName))
                pm.menuItem(l = 'clear', 
                            i = 'hsClearView.png', 
                            c = pm.Callback(self.clearObjName))
                pm.menuItem(d = True)
                pm.menuItem(l = 'Create Locator',
                            i = 'out_locator.png',
                            c = pm.Callback(self.createLocator))
                self.itb12 = mc.iconTextButton(st = 'iconAndTextHorizontal', 
                                               i1 = 'out_locator.png', 
                                              bgc = (0.35, 0.35, 0.35),
                                                l = 'Create to Face', 
                                                c = pm.Callback(self.rivetConstToFace_run), 
                                              ann = 'Set skin object and select locator.',
                                                h = 28,
                                               mh = 5,
                                               mw = 5)
                self.sep11 = pm.separator()
                self.itb13 = mc.iconTextButton(st ='iconAndTextHorizontal', 
                                               i1 ='redrawPaintEffects.png', 
                                              bgc = (0.35, 0.35, 0.35),
                                                l = 'Reconstraint', 
                                                c = pm.Callback(self.reConstraint_run), 
                                              ann = 'Recreate rivet locator after skin edit.',
                                                h = 28,
                                               mh = 5,
                                               mw = 5)
                self.sep12 = pm.separator(h=20)
                self.helpL = pm.helpLine(bgc = (0.25, 0.25, 0.25), 
                                           w = 200)

        # -- Edit UI Layout
        pm.formLayout(self.fmL0, e=True,
               af = [(self.sep0,  'top', 0), (self.sep0, 'right', 0), (self.sep0, 'left', 0),
                     (self.fmL1,  'top', 0), (self.fmL1, 'left', 0), (self.fmL1, 'right', 0),
                    ])

        pm.formLayout(self.fmL1, e=True,
               af = [(self.itb10, 'top',  10), (self.itb10, 'left', 10), (self.itb10, 'right', 10),
                     (self.sep10, 'top',  50), (self.sep10, 'left',  2), (self.sep10, 'right',  2),
                     (self.txf10, 'top',  60), (self.txf10, 'left', 10), (self.txf10, 'right', 40),
                     (self.itb11, 'top',  62), (self.itb11, 'right', 15),
                     (self.itb12, 'top',  90), (self.itb12, 'left', 10), (self.itb12, 'right', 10),
                     (self.sep11, 'top', 130), (self.sep11, 'left',  2), (self.sep11, 'right',  2),
                     (self.itb13, 'top', 145), (self.itb13, 'left', 10), (self.itb13, 'right', 10),
                     (self.sep12, 'top', 180), (self.sep12, 'left',  2), (self.sep12, 'right',  2),
                     (self.helpL, 'bottom', 0), (self.helpL, 'left', 0), (self.helpL, 'right',  0),
                    ])

        window.show()


def showUI():
    testIns = rivetConstraintUI()
    testIns.main()
