# -*- coding: utf-8 -*-
from __future__ import absolute_import

#-- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser


def getRefNameSpaceList():
    '''
get reference namespace list

Parameters:
  - : 

Returns:
  - : 

Error:
  - :
    '''
    refList = mc.ls(type='reference')
    returnValue = []
    if not refList == None:
        for ref in refList:
            refLoad = False
            try:
                refLoad = mc.referenceQuery(ref, il=True)
            except:
                pass
            if not ref == 'sharedReferenceNode' and not ref == '_UNKNOWN_REF_NODE_' and refLoad:
                nameSpace = mc.referenceQuery(ref, ns=True)
                returnValue.append(nameSpace.lstrip(':'))
    return returnValue



def getNameSpace():
    '''
get namespace list

Parameters:
  - : 

Returns:
  - : 

Error:
  - :
    '''
    nsList = mc.namespaceInfo(r=True, lon=True)
    nsList.remove(u'UI')
    nsList.remove(u'shared')

    newNS = []
    for i in nsList:
        if i[0:1] == 'f' and len(i) == 9:
            newNS.append(i)
    return newNS


def getCamList():
    '''
get camera list in the scene without default cameras

Parameters:
  - : 

Returns:
  - : 

Error:
  - :
    '''
    defaultCamList = [u'backShape', u'bottomShape', u'frontShape', u'leftShape', u'perspShape', u'sideShape', u'topShape']
    camList = [cam for cam in mc.ls(typ='camera') if not cam in defaultCamList]
    return camList


def createCamForCtrl(ns='', tgt=''):
    '''
create camera for fc ctrl

Parameters:
  - : 

Returns:
  - : 

Error:
  - :
    '''
    ns   = getNamespaceStr(ns)
    src  = pm.PyNode('{0}{1}'.format(ns, tgt))
    cam  = pm.camera(coi = 5,
                     fl  = 35,
                     lsr = 1,
                     cs  = 1,
                     hfa = 1.41732,
                     hfo = 0,
                     vfa = 0.94488,
                     vfo = 0,
                     ff  = 'Fill',
                     ovr = 1,
                     mb  = 0,
                     sa  = 144,
                     ncp = 0.1,
                     fcp = 10000,
                     o   = 0,
                     ow  = 30,
                     pze = 0,
                     hpn = 0,
                     vpn = 0,
                     zom = 1)
    cam[0].rename('{0}_cam'.format(src.name()))
    ctrl = pm.spaceLocator(n='{0}_cam_ctrl'.format(src.name())) 
    cnst = pm.createNode('transform', n='{0}_cam_cnst'.format(src.name()))
    cam[0].setParent(ctrl)
    ctrl.setParent(cnst)
    
    # -- parent constraint
    pConst = pm.parentConstraint(src, cnst, w=1)
    if tgt == 'facial_ctrl_vis':
        mc.setAttr('{0}.focalLength'.format(cam[1]), 35)
        mc.setAttr('{0}.target[0].targetOffsetTranslateX'.format(pConst.name()), 6.5)
        mc.setAttr('{0}.target[0].targetOffsetTranslateY'.format(pConst.name()), -8.5)
        mc.setAttr('{0}.target[0].targetOffsetTranslateZ'.format(pConst.name()), 30)
    elif tgt == '_005':
        mc.setAttr('{0}.focalLength'.format(cam[1]), 200)
        mc.setAttr('{0}.target[0].targetOffsetTranslateX'.format(pConst.name()), 0.0)
        mc.setAttr('{0}.target[0].targetOffsetTranslateY'.format(pConst.name()), 2.0)
        mc.setAttr('{0}.target[0].targetOffsetTranslateZ'.format(pConst.name()), 200)
    else:
        mc.setAttr('{0}.focalLength'.format(cam[1]), 35)
        mc.setAttr('{0}.target[0].targetOffsetTranslateX'.format(pConst.name()), 0.0)
        mc.setAttr('{0}.target[0].targetOffsetTranslateY'.format(pConst.name()), 0.0)
        mc.setAttr('{0}.target[0].targetOffsetTranslateZ'.format(pConst.name()), 0.0)
    return cam[1]


def createPinLocator(tgt='', key=False):
    '''
create pin locator with keyframe

Parameters:
  - tgt str: target to create pin locator
  - key bool: set current key frame

Returns:
  - : 

Error:
  - :
    '''
    eac = pm.PyNode(tgt)
    crf = int(pm.currentTime(q=True))
    pos = pm.xform(eac, ws=True, t=True, q=True)
    lgp = pm.createNode('transform', n='{0}_{1}_pos'.format(eac.name(), crf))
    loc = pm.spaceLocator(n='{0}_{1}_offset'.format(eac.name(), crf))
    loc.setParent(lgp)
    pm.move(pos[0], pos[1], pos[2], lgp, a=True)
    pcn = pm.parentConstraint(loc, eac, mo = False, 
                                        sr = ['x', 'y', 'z'], 
                                        n  = '{0}_{1}_parentConstraint'.format(eac.name(), crf))

    if key:
        eac.t.setKey()
        loc.t.setKey()


def bakeSelected(st=0, ed=100):
    '''
plot selected object and selected attribute

Parameters:
  - st float: start frame
  - ed float: end frame

Returns:
  - : 

Error:
  - :
    '''
    tgtList = pm.selected()
    atList  = mc.channelBox('mainChannelBox', sma=True, q=True)
    if atList:
        pm.bakeResults(tgtList,
                       sm  = True, 
                       t   = '{0}:{1}'.format(st, ed),
                       sb  = 1,
                       osr = 1,
                       dic = True,
                       pok = True,
                       sac = False,
                       ral = False,
                       rba = False,
                       bol = False,
                       mr  = True, 
                       at  = atList)
    else:
        pm.bakeResults(tgtList,
                       sm  = True, 
                       t   = '{0}:{1}'.format(st, ed),
                       sb  = 1,
                       osr = 1,
                       dic = True,
                       pok = True,
                       sac = False,
                       ral = False,
                       rba = False,
                       bol = False,
                       mr  = True)


def getNamespaceStr(ns=''):
    '''
get namespace string include :

Parameters:
  - ns str: namespace
  - setName str: ctrl set name 

Returns:
  - : 

Error:
  - :
    '''
    resStr = ''
    if ns:
        if not ':' in ns:
            resStr = '{0}:'.format(ns)
        else:
            resStr = ns
    return resStr


def resetSelectedCtrl(ns='', setName=''):
    '''
reset selected control

Parameters:
  - ns str: namespace
  - setName str: ctrl set name 

Returns:
  - : 

Error:
  - :
    '''
    ns    = getNamespaceStr(ns)
    nodes = mc.ls(sl=True)
    attrs = mc.channelBox('mainChannelBox', sma=True, q=True)
    log   = ''

    if not nodes:
        nodes = mc.ls(mc.select('{0}{1}'.format(ns, setName), r=True))

    if not attrs:
        attrs = mc.listAttr(k=True, u=True, sn=True)

    for node in nodes:
        for attr in set(attrs):
            defaultAttr = '{0}_default'.format(attr)
            if not mc.attributeQuery(defaultAttr, n=node, ex=True):
                continue

            targetNodeAttr = '{0}.{1}'.format(node, attr)
            cachedNodeAttr = '{0}.{1}'.format(node, defaultAttr)

            # -- set default value
            val = mc.getAttr(cachedNodeAttr)
            mc.setAttr(targetNodeAttr, val)
            log += 'setAttr {0} : {1}\n'.format(targetNodeAttr, val)
    print(log)


class fcSupportToolsUI(object):
    def __init__(self):
        self.__ver__          = '0.0.7'
        self.windowManageName = 'fcSupportTools'
        self.windowTitle      = 'FC Support v{0}'.format(self.__ver__)
        self.windowSize       = [800, 600]
        self._mayaHelp_url    = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._toolHelp_url    = r'https://wisdom.cygames.jp/display/tsubasa/%5BMaya%5D+FC+Support+Tools'
        self._slHelp_url      = r'https://wisdom.cygames.jp/display/tsubasa/%5BMaya%5DStudio+Library'
        self._fcReference_url = r'https://wisdom.cygames.jp/pages/viewpage.action?pageId=79020104'
        
    def checkWindowOverlap(self):
        if pm.window(self.windowManageName, ex=True):
            pm.deleteUI(self.windowManageName)

    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)

    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)

    def show_fcReference(self, *args):
        webbrowser.open_new_tab(self._fcReference_url)

    def show_slHelp(self, *args):
        webbrowser.open_new_tab(self._slHelp_url)

    def launchStudioLibrary(self):
        import studiolibrary
        studiolibrary.main()

    def launchAnimCopyAndPaste(self):
        import tsubasa.maya.tools.animcopypaste.gui as animcopypaste
        animcopypaste.main()

    def launchFCTargetAnim(self):
        import tsubasa.maya.tools.copyfacialtargetanim.gui as copyfacialtargetanim
        copyfacialtargetanim.main()

    def launchLiveLink(self):
        pm.mel.eval('LiveLink_Joint;')

    def launchSetEditor(self):
        import setEditor.ui
        setEditor.ui.showUI()

    # ---- namespace -------------------------------------------------
    def setNamespace(self, ns):
        if ns == 'null':
            ns = ''
        else:
            ns = mc.menuItem('_ns_mi_{0}'.format(ns), l=True, q=True)
        self._ns_txf.setText(ns)
        # -- reload camera
        self.reloadCam()
        self.reloadList()

    def setInitNamespace(self):
        nsList = getNameSpace()
        if nsList:
            self._ns_txf.setText(nsList[0])
        else:
            self._ns_txf.setText('')

    def reloadNamespace(self):
        self._ns_txf.setText('')
        # -- delete UI
        pm.popupMenu(self._ns_pum, dai=True, e=True)

        # -- create null text
        pm.menuItem('_ns_mi_null', l = 'none', 
                                   c = pm.Callback(self.setNamespace, 'null'),
                                   p = self._ns_pum)
        # -- reload
        for ns in getNameSpace():
            pm.menuItem('_ns_mi_{0}'.format(ns), l = ns, 
                                                 c = pm.Callback(self.setNamespace, ns), 
                                                 p = self._ns_pum)
        
        pm.menuItem('_ns_mi_div', d=True, p=self._ns_pum)
        pm.menuItem('_ns_mi_reload', l = 'reload', 
                                     i = 'redrawPaintEffects.png',
                                     c = pm.Callback(self.reloadNamespace), 
                                     p = self._ns_pum)
        # -- reload camera
        self.reloadCam()
        self.reloadList()


    # ---- camera ------------------------------------------------------
    def createCamToSelected(self):
        if mc.ls(sl=True)[0]:
            if ':' in mc.ls(sl=True)[0]:
                ns, tgt = mc.ls(sl=True)[0].split(':') # -- split selected object by namespace
                ns  = getNamespaceStr(ns)
            else:
                ns  = ''
                tgt = mc.ls(sl=True)[0]
            camName = '{0}{1}_cam'.format(ns, tgt)
            if not pm.objExists(camName):
                cam = createCamForCtrl(ns, tgt)
                self.reloadCam()
                pm.modelEditor(self._cam_mde, cam=cam, e=True)
                # -- set current
                self.setCurrentCam()
            else:
                pm.warning('{0} already exisits in this scene.'.format(camName))
        else:
            pm.warning('Please select something to target.')

    def createCam(self, tgt=''):
        ns      = getNamespaceStr(self._ns_txf.getText())
        camName = '{0}{1}_cam'.format(ns, tgt)
        if not pm.objExists(camName):
            if pm.objExists('{0}{1}'.format(ns, tgt)):
                cam = createCamForCtrl(ns, tgt)
                self.reloadCam()
                pm.modelEditor(self._cam_mde, cam=cam, e=True)
                # -- set current
                self.setCurrentCam()
            else:
                pm.warning('{0}{1} doesn\'t exisit in this scene.'.format(ns, tgt))
        else:
            pm.warning('{0} already exisits in this scene.'.format(camName))

    def setCam(self):
        cam = self._cam_opm.getValue()
        if cam == 'choice camera...':
            pm.modelEditor(self._cam_mde, cam='persp', e=True) 
        else:
            pm.modelEditor(self._cam_mde, cam=cam, e=True) 

    def resetCam(self):
        cam = pm.modelEditor(self._cam_mde, cam=True, q=True) 
        cam.t.set(0,0,0)
        cam.r.set(0,0,0)
        cam.s.set(1,1,1)

    def reloadCam(self):
        # -- delete UI
        miList = pm.optionMenu(self._cam_opm, ill=True, q=True)
        for mi in miList:
            pm.deleteUI(mi, mi=True)

        # -- create default text
        pm.menuItem('_cam_mi_default', l='choice camera...', p=self._cam_opm)

        # -- reload
        ns  = self._ns_txf.getText()
        for cam in pm.ls(typ='camera'):
            cam = cam.getTransform().name()
            if ns in cam:
                pm.menuItem('_cam_mi_{0}'.format(cam), l=cam, p=self._cam_opm)
        
        # -- set current
        self.setCurrentCam()


    def setCurrentCam(self):
        cam = pm.modelEditor(self._cam_mde, cam=True, q=True)
        for i in pm.optionMenu(self._cam_opm, ill=True, q=True):
            if pm.menuItem(i, l=True, q=True) == cam:
                pm.optionMenu(self._cam_opm, v=cam, e=True)
        

    # -- sets and ctrl
    def resetCtrl(self, setName=''):
        ns = self._ns_txf.getText()
        resetSelectedCtrl(ns, setName)


    def selectSet(self, setName=''):
        ns      = getNamespaceStr(self._ns_txf.getText())
        setName = '{0}{1}'.format(ns, setName)
        pm.select(mc.sets(setName, q=True), r=True)


    def selectAllCtrl(self):
        ns      = getNamespaceStr(self._ns_txf.getText())
        setName = '{0}fc_set'.format(ns)
        pm.select(mc.sets(setName, q=True), r=True)


    def toggleCtrlVis(self, attr=''):
        ns  = getNamespaceStr(self._ns_txf.getText())
        val = pm.getAttr('{0}facial_ctrl_vis.{1}'.format(ns, attr))
        pm.setAttr('{0}facial_ctrl_vis.{1}'.format(ns, attr), (1-val))


    def deleteCurrentCam(self):
        cam = pm.modelEditor(self._cam_mde, cam=True, q=True)
        res = mc.confirmDialog(t  = 'Confirm delete current cam',
                               m  = 'Are you sure to delete \n\n{0}'.format(cam), 
                               b  = ['Yes', 'No'],
                               db = 'No', 
                               cb = 'No',
                               ds = 'No')
        if res == 'Yes':
            paPath = mc.listRelatives(cam.name(), p=True, f=True)[0]
            paList = paPath.split('|')
            rootPa = paList[1]
            mc.delete(rootPa)
            self.reloadCam()
        else:
            return

    def deleteAllCam(self):
        ns = getNamespaceStr(self._ns_txf.getText())
        if ns:
            camList = [i for i in mc.ls(typ='camera') if ns in i]
        else:
            camList = mc.ls(typ='camera')
        # -- get parent list
        paList = []
        for cam in camList:
            paList.append(mc.listRelatives(cam, p=True, f=True)[0].split('|')[1])
        paList = list(set(paList))
        
        # -- camera name list
        camStr = ''
        for i in camList:
            camShape = pm.PyNode(i)
            camTrans = camShape.getTransform()
            camStr += '{0}\n'.format(camTrans.name())

        res = mc.confirmDialog(t  = 'Confirm delete current cam',
                               m  = 'Are you sure to delete \n\n{0}'.format(camStr), 
                               b  = ['Yes', 'No'],
                               db = 'No', 
                               cb = 'No',
                               ds = 'No')
        if res == 'Yes':
            mc.delete(paList)
            self.reloadCam()
        else:
            return        


    # ---- node list -----------------------------------------------
    def setNodeList(self, nsf=True):
        typ = self._nfl_txf.getText()
        
        # -- get list
        if typ:
            nodeList = [i for i in mc.ls(typ=typ)]
        else:
            pm.warning('Please fill in a node type.')
            return
        # -- namespace
        if nsf:
            ns = getNamespaceStr(self._ns_txf.getText())
            nodeList = [i for i in nodeList if ns in i]

        # -- remove all and add items
        mc.textScrollList(self._lst_tsl, ra=True, e=True)
        mc.textScrollList(self._lst_tsl, a=nodeList, e=True)


    def setNodeFilter(self, nf=''):
        # -- check namespace filter
        cb = pm.menuItem('_nfl_mi_nsf', cb=True, q=True)   

        if nf == '_null_':
            nf = ''
        elif nf == '_selected_':
            objList = pm.selected()
            if objList:
                nf = objList[0].nodeType()   
            else:
                nf = ''
                pm.warning('Please select a node what you want to get node type.')

        # -- set to text field
        self._nfl_txf.setText(nf)
        self.setNodeList(nsf=cb)


    def toggleNSFilter(self):
        # -- check namespace filter
        cb = pm.menuItem('_nfl_mi_nsf', cb=True, q=True)
        self.setNodeList(nsf=cb)


    def setObjList(self):
        typ = self._nfl_txf.getText()
        nsf = pm.menuItem('_nfl_mi_nsf', cb=True, q=True) 

        # -- remove all
        mc.textScrollList(self._lst_tsl, ra=True, e=True)
        # -- add items
        if typ:
            objList = mc.ls(typ=typ)
            if nsf:
                ns = getNamespaceStr(self._ns_txf.getText())
                objList = [i for i in objList if ns in i]   
            mc.textScrollList(self._lst_tsl, a=objList, e=True)


    def setBSList(self):
        nsf    = pm.menuItem('_nfl_mi_nbf', cb=True, q=True)
        bsList = mc.ls(typ='blendShape')
        # -- namespace filter
        if nsf:
            ns = getNamespaceStr(self._ns_txf.getText())
            bsList = [i for i in bsList if ns in i]

        # -- remove all
        mc.textScrollList(self._bsl_tsl, ra=True, e=True)
        mc.textScrollList(self._bsl_tsl, a=bsList, e=True)


    def setALList(self):
        nsf    = pm.menuItem('_nfl_mi_naf', cb=True, q=True)
        alList = mc.ls(typ='animLayer')
        if nsf:
            ns = getNamespaceStr(self._ns_txf.getText())
            alList = [i for i in alList if ns in i]

        # -- remove all
        mc.textScrollList(self._all_tsl, ra=True, e=True)
        mc.textScrollList(self._all_tsl, a=alList, e=True)


    def reloadList(self):
        self.setObjList()
        self.setBSList()
        self.setALList()


    # ---- selection ------------------------------------------------
    def selectListedObject(self):
        targetNodeType = mc.textScrollList(self._lst_tsl, si=True, q=True)
        mc.select(targetNodeType, r=True)


    def selectListedBS(self):
        bs = mc.textScrollList(self._bsl_tsl, si=True, q=True)
        mc.select(bs, r=True)


    def selectListedAL(self):
        al = mc.textScrollList(self._all_tsl, si=True, q=True)
        mc.select(al, r=True)


    # ---- add pin locator -------------------------------------------
    def pinLocator(self):
        kv = self._apl_ckb.getValue()
        for i in mc.ls(sl=True):
            createPinLocator(i, kv)

    # ---- plot ------------------------------------------------------
    def setSelectedRange(self):
        val = pm.mel.eval('timeControl -q -range $gPlayBackSlider;').replace('"', '').split(':')
        st  = self._str_flf.setValue(float(val[0]))
        ed  = self._end_flf.setValue(float(val[1]))


    def plotSelected(self):
        st = self._str_flf.getValue()
        ed = self._end_flf.getValue()
        bakeSelected(st, ed)


    # ---- edit UI size ----------------------------------------------
    def editListSize(self, val=(4,3,3)):
        a = val[0] * 10
        b = a + (val[1] * 10)
        pm.formLayout(self.fmL4, e=True,
               ap = [(self._lst_tsl, 'bottom', 24, a), 
                     (self._bsl_tsl, 'bottom', 24, b)],
                    )

    def resetUI(self):
        self._ns_txf.setText('')
        self.reloadNamespace()
        self.reloadCam()
        
        # -- list of namespace filter option
        pm.menuItem('_nfl_mi_nsf', cb = True, e=True)
        pm.menuItem('_nfl_mi_nbf', cb = True, e=True)
        pm.menuItem('_nfl_mi_naf', cb = True,e=True)

        # -- list edit
        self._nfl_txf.setText('')
        self.setObjList()  
        self.setBSList()
        self.setALList() 


    # -- UI
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
        pm.menuItem(l = 'Studio Library',
                    i = 'studiolibrary_icon.png', 
                    c = pm.Callback(self.launchStudioLibrary)) 
        pm.menuItem(d = True)
        pm.menuItem(l = 'Anim Copy Paste ...',
                    c = pm.Callback(self.launchAnimCopyAndPaste)) 
        pm.menuItem(l = 'Copy Facial Target Anim ...',
                    c = pm.Callback(self.launchFCTargetAnim)) 
        pm.menuItem(d = True)
        pm.menuItem(l = 'LiveLink Open GUI ...',
                    c = pm.Callback(self.launchLiveLink)) 
        pm.menuItem(d = True)
        pm.menuItem(l = 'Set Editor',
                    i = 'objectSet.svg', 
                    c = pm.Callback(self.launchSetEditor)) 
        pm.menuItem(d = True)
        pm.menuItem(l = 'Reset UI',
                    i = 'redrawPaintEffects.png', 
                    c = pm.Callback(self.resetUI))
        pm.menu(l  ='Help', 
                to = False, 
                hm = True)
        pm.menuItem(l = 'Facial Reference',
                    c = self.show_fcReference)
        pm.menuItem(d = True)
        pm.menuItem(l = 'Maya 2019 HELP',
                    c = self.show_mayaHelp)
        pm.menuItem(d = True)
        pm.menuItem(l = 'Tool HELP',
                    c = self.show_toolHelp)
        pm.menuItem(l = 'StudioLibrary HELP',
                    i = 'studiolibrary_icon.png', 
                    c = self.show_slHelp)

        # -- base form layout
        self.fmL0 = pm.formLayout(nd=100)
        with self.fmL0:
            self.sep0 = pm.separator()
            
            # -- main form layout
            self.fmL1 = pm.formLayout(nd=100)
            with self.fmL1:
                # -- button form layout
                self.fmL2 = pm.formLayout(nd=100, w=245)
                with self.fmL2:
                    self._ns_txt = pm.text(l  = 'Namespace',
                                           al = 'left', 
                                           h  = 28)
                    self._ns_txf = pm.textField(h = 28)
                    self._ns_btn = pm.iconTextButton(st = 'iconOnly',
                                                     i  = 'arrowDown.png',
                                                     w  = 28,
                                                     h  = 28,
                                                     )
                    self._ns_pum = pm.popupMenu(b=1)
                    pm.menuItem('_ns_mi_null', l='none', c=pm.Callback(self.setNamespace, 'null'))
                    for ns in getNameSpace():
                        pm.menuItem('_ns_mi_{0}'.format(ns), l=ns, c=pm.Callback(self.setNamespace, ns))
                    pm.menuItem('_ns_mi_div', d=True, p=self._ns_pum)
                    pm.menuItem('_ns_mi_reload', l = 'Reload', 
                                                 i = 'redrawPaintEffects.png',
                                                 c = pm.Callback(self.reloadNamespace), 
                                                 p = self._ns_pum)
                    
                    # -- cam menu
                    self._cam_opm = pm.optionMenu(cc = pm.Callback(self.setCam),
                                                  h  = 28,
                                                  w  = 100)
                    pm.menuItem('_cam_mi_default', l='choice camera...')
                    for cam in pm.ls(typ='camera'):
                        cam = cam.getTransform().name()
                        pm.menuItem('_cam_mi_{0}'.format(cam), l=cam)
                    self._rec_btn = pm.iconTextButton(st = 'iconOnly', 
                                                      i  = 'menuIconReset.png',
                                                      c  = pm.Callback(self.reloadCam), 
                                                      h  = 28,
                                                      w  = 28
                                                      )


                    self._sep0    = pm.separator(st='in')
                    
                    self._ach_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                      i1  = 'Camera.png', 
                                                      bgc = (0.4, 0.4, 0.4),
                                                      l   = 'Add to Head', 
                                                      c   = pm.Callback(self.createCam, '_005'), 
                                                      h   = 25,
                                                      mw  = 4
                                                      )
                    self._acc_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                      i1  = 'Camera.png', 
                                                      bgc = (0.4, 0.4, 0.4),
                                                      l   = 'Add to Ctrl', 
                                                      c   = pm.Callback(self.createCam, 'facial_ctrl_vis'), 
                                                      h   = 25,
                                                      mw  = 4
                                                      )
                                                     
                    self._ac_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                     i1  = 'Camera.png', 
                                                     bgc = (0.4, 0.4, 0.4),
                                                     l   = 'Add to Select', 
                                                     c   = pm.Callback(self.createCamToSelected), 
                                                     h   = 25,
                                                     mw  = 4
                                                     )
                    self._rc_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                     i   = 'hyperShadeResetCameraView.png',
                                                     bgc = (0.4, 0.4, 0.4),
                                                     l   = 'Reset', 
                                                     c   = pm.Callback(self.resetCam), 
                                                     h   = 25,
                                                     mw  = 4
                                                     )

                    self._dcc_btn = pm.iconTextButton(st = 'iconAndTextHorizontal', 
                                                     i1  = 'QR_delete.png', 
                                                     bgc = (0.4, 0.4, 0.4),
                                                     l   = 'Delete Current', 
                                                     c   = pm.Callback(self.deleteCurrentCam), 
                                                     h   = 25,
                                                     mw  = 2
                                                     )
                    self._dac_btn = pm.iconTextButton(st = 'iconAndTextHorizontal', 
                                                     i   = 'QR_delete.png', 
                                                     bgc = (0.4, 0.4, 0.4),
                                                     l   = 'Delete All', 
                                                     c   = pm.Callback(self.deleteAllCam), 
                                                     h   = 25,
                                                     mw  = 2
                                                     )

                    self._sep1    = pm.separator(st='in')

                    self._scs_btn = pm.button(l = 'shape_ctrl select', 
                                              c = pm.Callback(self.selectSet, 'shape_ctrl_set'), 
                                              h = 25,
                                              )
                    self._scr_btn = pm.button(l = 'shape_ctrl reset', 
                                              c = pm.Callback(self.resetCtrl, 'shape_ctrl_set'), 
                                              h = 25,
                                              )
                    self._pcs_btn = pm.button(l = 'parts_ctrl select', 
                                              c = pm.Callback(self.selectSet, 'parts_ctrl_set'), 
                                              h = 25,
                                              )
                    self._pcr_btn = pm.button(l = 'parts_ctrl reset', 
                                              c = pm.Callback(self.resetCtrl, 'parts_ctrl_set'), 
                                              h = 25,
                                              )
                    self._gcs_btn = pm.button(l = 'grp_ctrl select', 
                                              c = pm.Callback(self.selectSet, 'grp_ctrl_set'), 
                                              h = 25,
                                              )
                    self._gcr_btn = pm.button(l = 'grp_ctrl reset', 
                                              c = pm.Callback(self.resetCtrl, 'grp_ctrl_set'), 
                                              h = 25,
                                              )
                    self._p2s_btn = pm.button(l = 'ps2_ctrl select', 
                                              c = pm.Callback(self.selectSet, 'ps2_ctrl_set'), 
                                              h = 25,
                                              )
                    self._p2r_btn = pm.button(l = 'ps2_ctrl reset', 
                                              c = pm.Callback(self.resetCtrl, 'ps2_ctrl_set'), 
                                              h = 25,
                                              )           
                    self._ecs_btn = pm.button(l = 'ed4_ctrl select', 
                                              c = pm.Callback(self.selectSet, 'ed4_ctrl_set'), 
                                              h = 25,
                                              )
                    self._ecr_btn = pm.button(l = 'ed4_ctrl reset', 
                                              c = pm.Callback(self.resetCtrl, 'ed4_ctrl_set'), 
                                              h = 25,
                                              )
                    self._als_btn = pm.button(l = 'select all ctrl', 
                                              c = pm.Callback(self.selectAllCtrl), 
                                              h = 25,
                                              )
                    self._slr_btn = pm.button(l = 'select reset', 
                                              c = pm.Callback(self.resetCtrl, ''), 
                                              h = 25,
                                              )

                    self._sep2    = pm.separator(st='in')

                    self._scv_btn = pm.button(l = 'Shape Ctrl Vis', 
                                              c = pm.Callback(self.toggleCtrlVis, 'shape_ctrl_vis'), 
                                              h = 25,
                                              )
                    self._pcv_btn = pm.button(l = 'Parts Ctrl Vis', 
                                              c = pm.Callback(self.toggleCtrlVis, 'Parts_ctrl_vis'), 
                                              h = 25,
                                              )
                    self._psv_btn = pm.button(l = 'ps2 Ctrl Vis', 
                                              c = pm.Callback(self.toggleCtrlVis, 'ps2_ctrl_vis'), 
                                              h = 25,
                                              )
                    self._gcv_btn = pm.button(l = 'Grp Ctrl Vis', 
                                              c = pm.Callback(self.toggleCtrlVis, 'grp_ctrl_vis'), 
                                              h = 25,
                                              )
                    self._cmv_btn = pm.button(l = 'Cm3 Ctrl Vis', 
                                              c = pm.Callback(self.toggleCtrlVis, 'cm3_ctrl_vis'), 
                                              h = 25,
                                              )
                    self._ecv_btn = pm.button(l = 'Eye Ctrl Vis', 
                                              c = pm.Callback(self.toggleCtrlVis, 'eye_ctrl_vis'), 
                                              h = 25,
                                              )
                    self._edv_btn = pm.button(l = 'Ed4 Ctrl Vis', 
                                              c = pm.Callback(self.toggleCtrlVis, 'ed4_ctrl_vis'), 
                                              h = 25,
                                              )
                    self._ctv_btn = pm.button(l = 'Custom Target Vis', 
                                              c = pm.Callback(self.toggleCtrlVis, 'custom_tgt_vis'), 
                                              h = 25,
                                              )


                    self._sep3    = pm.separator(st='in')
                    self._apl_ckb = pm.checkBox(l='Key', v=True)
                    self._apl_btn = pm.iconTextButton(st = 'iconAndTextHorizontal', 
                                                     i   = 'out_locator.png', 
                                                     bgc = (0.4, 0.4, 0.4),
                                                     l   = 'Add Pin Locator', 
                                                     c   = pm.Callback(self.pinLocator), 
                                                     h   = 25,
                                                     mw  = 2
                                                     )
                    self._str_flf = pm.floatField(v   = pm.playbackOptions(min=True, q=True), 
                                                  pre = 2, 
                                                  tze = False, 
                                                  w   = 70,
                                                  h   = 25,
                                                  )
                    self._end_flf = pm.floatField(v   = pm.playbackOptions(max=True, q=True), 
                                                  pre = 2, 
                                                  tze = False, 
                                                  w   = 70,
                                                  h   = 25,
                                                  )
                    self._gan_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                      i   = 'teSetKeyframe.png', 
                                                      bgc = (0.4, 0.4, 0.4),
                                                      l   = 'Get', 
                                                      c   = pm.Callback(self.setSelectedRange), 
                                                      h   = 25,
                                                      mw  = 2
                                                      )        
                    self._ban_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                      i   = 'out_animCurveTA.png', 
                                                      bgc = (0.4, 0.4, 0.4),
                                                      l   = 'Bake Selected', 
                                                      c   = pm.Callback(self.plotSelected), 
                                                      h   = 25,
                                                      mw  = 2
                                                      )        




                self.pnL1 = pm.paneLayout(cn = 'vertical2', 
                                          ps = ([1,60,100], [2,40,100]))
                with self.pnL1:
                    # -- model panel
                    self.fmL3 = pm.formLayout(nd=100)
                    with self.fmL3:
                        self._cam_mde = pm.modelPanel()

                    self.fmL4 = pm.formLayout(nd=100)
                    with self.fmL4:
                        self._nfl_txf = pm.textField(ec  = pm.Callback(self.setNodeList),
                                                     pht = 'node type...',
                                                     h   = 28)
                        self._nfl_btn = pm.iconTextButton(st = 'iconOnly',
                                                          i  = 'arrowDown.png',
                                                          w  = 28,
                                                          h  = 28,
                                                          )
                        self._nfl_pum = pm.popupMenu(b=1)
                        pm.menuItem('_nfl_mi_sch',  l = 'Search...', 
                                                    i = 'search.png',
                                                    c = pm.Callback(self.setNodeList))
                        pm.menuItem('_nfl_mi_get',  l = 'Get node type from selection.', 
                                                    i = 'newPreset.png',
                                                    c = pm.Callback(self.setNodeFilter, '_selected_'))
                        pm.menuItem('_nfl_mi_div1', d = True)
                        pm.menuItem('_nfl_mi_nsf',  l = 'Namespace filter', 
                                                   cb = True,
                                                    c = pm.Callback(self.toggleNSFilter))
                        pm.menuItem('_nfl_mi_nbf',  l = 'Namespace filter : Blendshape', 
                                                   cb = True,
                                                    c = pm.Callback(self.setBSList))
                        pm.menuItem('_nfl_mi_naf',  l = 'Namespace filter : AnimLayer', 
                                                   cb = True,
                                                    c = pm.Callback(self.setALList))
                        pm.menuItem('_nfl_mi_div2', d = True)
                        pm.menuItem('_nfl_mi_els1', l = 'Resize 4:3:3 (default)', 
                                                    i = 'menuIconLeftSideFilters.png',
                                                    c = pm.Callback(self.editListSize, (4,3,3)))
                        pm.menuItem('_nfl_mi_els2', l = 'Resize 6:2:2', 
                                                    i = 'menuIconLeftSideFilters.png',
                                                    c = pm.Callback(self.editListSize, (6,2,2)))
                        pm.menuItem('_nfl_mi_els3', l = 'Resize 2:4:4', 
                                                    i = 'menuIconLeftSideFilters.png',
                                                    c = pm.Callback(self.editListSize, (2,4,4)))
                        pm.menuItem('_nfl_mi_els4', l = 'Resize 2:6:2', 
                                                    i = 'menuIconLeftSideFilters.png',
                                                    c = pm.Callback(self.editListSize, (2,6,2)))
                        pm.menuItem('_nfl_mi_els5', l = 'Resize 2:2:6', 
                                                    i = 'menuIconLeftSideFilters.png',
                                                    c = pm.Callback(self.editListSize, (2,2,6)))
                        pm.menuItem('_nfl_mi_div3', d =True)
                        pm.menuItem('_nfl_mi_null', l = 'Clear', c=pm.Callback(self.setNodeFilter, '_null_'))
                        pm.menuItem('_nfl_mi_re',   l = 'Reload', 
                                                    i = 'menuIconReset.png',
                                                    c = pm.Callback(self.reloadList))
                                                    
                        self._lst_tsl = pm.textScrollList(ams = True, 
                                                          sc  = pm.Callback(self.selectListedObject))
                        self._bsl_txt = pm.text(l  = 'BlendShape',
                                               al = 'left', 
                                               h  = 28)                                 
                        self._bsl_tsl = pm.textScrollList(ams = True, 
                                                          sc  = pm.Callback(self.selectListedBS))
                        self._all_txt = pm.text(l  = 'AnimaLayer',
                                               al = 'left', 
                                               h  = 28)
                        self._all_tsl = pm.textScrollList(ams = True, 
                                                          sc  = pm.Callback(self.selectListedAL))                                  

        # -- Edit UI Layout
        pm.formLayout(self.fmL0, e=True,
               af = [(self.sep0, 'top', 0), (self.sep0, 'left', 0), (self.sep0, 'right', 0), 
                     (self.fmL1, 'top', 0), (self.fmL1, 'left', 0), (self.fmL1, 'right', 0), (self.fmL1, 'bottom', 0),
                    ])
                    
        pm.formLayout(self.fmL1, e=True,
               af = [(self.fmL2, 'top', 0), (self.fmL2, 'left', 0), (self.fmL2, 'bottom', 5),
                     (self.pnL1, 'top', 0), (self.pnL1, 'left', 245), (self.pnL1, 'right', 5), (self.pnL1, 'bottom', 0),
                    ],
               ac = [(self.fmL2, 'right', 0, self.pnL1)], 
                    )
        pm.formLayout(self.fmL2, e=True,
               af = [(self._ns_txt, 'top',  10), (self._ns_txt, 'left', 10), (self._ns_txt, 'right', 120),
                     (self._ns_txf, 'top',  10), (self._ns_txf, 'left', 76), (self._ns_txf, 'right',  24),
                     (self._ns_btn, 'top',  10),                             (self._ns_btn, 'right',   0),
                     (self._cam_opm, 'top', 45), (self._cam_opm, 'left', 5), (self._cam_opm, 'right', 26),
                     (self._rec_btn, 'top', 49),                             (self._rec_btn, 'right',  0),

                     (self._sep0,    'top', 90), (self._sep0, 'left', 5), (self._sep0, 'right',  5),

                     (self._ach_btn, 'top', 100), (self._ach_btn, 'left',   5), (self._ach_btn, 'right', 125),
                     (self._acc_btn, 'top', 100), (self._acc_btn, 'left', 125), (self._acc_btn, 'right',   5),
                     (self._ac_btn,  'top', 130), (self._ac_btn,  'left',   5), (self._ac_btn,  'right', 125),
                     (self._rc_btn,  'top', 130), (self._rc_btn,  'left', 125), (self._rc_btn,  'right',   5),
                     (self._dcc_btn, 'top', 160), (self._dcc_btn,  'left',   5), (self._dcc_btn,  'right', 125),
                     (self._dac_btn, 'top', 160), (self._dac_btn,  'left', 125), (self._dac_btn,  'right',   5),


                     (self._sep1,   'top', 200), (self._sep1, 'left', 5), (self._sep1, 'right',  5),

                     (self._scs_btn, 'top', 210), (self._scs_btn, 'left',  5),  (self._scs_btn, 'right', 125),
                     (self._scr_btn, 'top', 210), (self._scr_btn, 'left', 125), (self._scr_btn, 'right',   5),
                     (self._pcs_btn, 'top', 240), (self._pcs_btn, 'left',  5),  (self._pcs_btn, 'right', 125),
                     (self._pcr_btn, 'top', 240), (self._pcr_btn, 'left', 125), (self._pcr_btn, 'right',   5),
                     (self._gcs_btn, 'top', 270), (self._gcs_btn, 'left',  5),  (self._gcs_btn, 'right', 125),
                     (self._gcr_btn, 'top', 270), (self._gcr_btn, 'left', 125), (self._gcr_btn, 'right',   5),
                     (self._p2s_btn, 'top', 300), (self._p2s_btn, 'left',  5),  (self._p2s_btn, 'right', 125), 
                     (self._p2r_btn, 'top', 300), (self._p2r_btn, 'left', 125), (self._p2r_btn, 'right',   5),
                     (self._ecs_btn, 'top', 330), (self._ecs_btn, 'left',   5), (self._ecs_btn, 'right', 125),
                     (self._ecr_btn, 'top', 330), (self._ecr_btn, 'left', 125), (self._ecr_btn, 'right',   5),
                     (self._als_btn, 'top', 360), (self._als_btn, 'left',   5), (self._als_btn, 'right', 125),
                     (self._slr_btn, 'top', 360), (self._slr_btn, 'left', 125), (self._slr_btn, 'right',   5),


                     (self._sep2,   'top', 400), (self._sep2, 'left', 5), (self._sep2, 'right',  5),

                     (self._scv_btn, 'top', 410), (self._scv_btn, 'left',  5),  (self._scv_btn, 'right', 125),
                     (self._pcv_btn, 'top', 440), (self._pcv_btn, 'left',  5),  (self._pcv_btn, 'right', 125),
                     (self._psv_btn, 'top', 440), (self._psv_btn, 'left', 125), (self._psv_btn, 'right',  5),
                     (self._gcv_btn, 'top', 470), (self._gcv_btn, 'left',  5),  (self._gcv_btn, 'right', 125),
                     (self._cmv_btn, 'top', 470), (self._cmv_btn, 'left', 125), (self._cmv_btn, 'right',  5),
                     (self._ecv_btn, 'top', 500), (self._ecv_btn, 'left',   5), (self._ecv_btn, 'right', 125),
                     (self._edv_btn, 'top', 500), (self._edv_btn, 'left', 125), (self._edv_btn, 'right',  5),
                     (self._ctv_btn, 'top', 530), (self._ctv_btn, 'left',   5), (self._ctv_btn, 'right',  5),


                     (self._sep3,    'top', 570), (self._sep3,    'left',   5), (self._sep3, 'right',  5),
                     (self._apl_ckb, 'top', 585), (self._apl_ckb, 'left',  15), 
                     (self._apl_btn, 'top', 580), (self._apl_btn, 'left',  80), (self._apl_btn, 'right',  5),
                     (self._str_flf, 'top', 610), (self._str_flf, 'left',   5), 
                     (self._end_flf, 'top', 610), (self._end_flf, 'left',  80), 
                     (self._gan_btn, 'top', 610), (self._gan_btn, 'left', 155), (self._gan_btn, 'right',  5),
                     (self._ban_btn, 'top', 640), (self._ban_btn, 'left',   5), (self._ban_btn, 'right',  5),
                    ])

        pm.formLayout(self.fmL3, e=True,
               af = [(self._cam_mde, 'top', 0), (self._cam_mde, 'left', 0), (self._cam_mde, 'right', 0), (self._cam_mde, 'bottom', 0),
                    ])

        pm.formLayout(self.fmL4, e=True,
               af = [(self._nfl_txf, 'top', 10), (self._nfl_txf, 'left', 0), (self._nfl_txf, 'right', 24),
                     (self._nfl_btn, 'top', 10),                             (self._nfl_btn, 'right',  0),
                     (self._lst_tsl, 'top', 45), (self._lst_tsl, 'left', 0), (self._lst_tsl, 'right',  0), 
                     (self._bsl_txt, 'top', 10), (self._bsl_txt, 'left', 10), (self._bsl_txt, 'right', 120),
                                                 (self._bsl_tsl, 'left',  0), (self._bsl_tsl, 'right',  0), 
                     (self._all_txt, 'top', 10), (self._all_txt, 'left', 10), (self._all_txt, 'right', 120),
                                                 (self._all_tsl, 'left',  0), (self._all_tsl, 'right',  0), (self._all_tsl, 'bottom', 0),
                    ],
               ac = [                                          (self._lst_tsl, 'bottom', 24, self._bsl_tsl), 
                    (self._bsl_tsl, 'top', 24, self._lst_tsl), (self._bsl_tsl, 'bottom', 24, self._all_tsl),
                    (self._all_tsl, 'top', 24, self._bsl_tsl), 
                    (self._bsl_txt, 'top',  0, self._lst_tsl), 
                    (self._all_txt, 'top',  0, self._bsl_tsl), ], 
               ap = [(self._lst_tsl, 'bottom', 24, 40), 
                     (self._bsl_tsl, 'bottom', 24, 70)],
                    )
        
        # -- Edit model editor
        pm.modelEditor(self._cam_mde, e=True,
                       cam = 'persp',
                       hud = False,
                       alo = False,
                       nc  = True,
                       pm  = True,
                       da  = 'smoothShaded',
                       dtx = True
                       )

        # -- set init namespace
        self.setInitNamespace()
        self.reloadCam()
        self.setBSList()
        self.setALList()

        window.show()


def showUI():
    testIns = fcSupportToolsUI()
    testIns.main()
