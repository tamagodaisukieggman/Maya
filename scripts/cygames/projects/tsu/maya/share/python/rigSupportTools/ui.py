# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : rig support tools
# Author  : rkanda
# Version : 0.0.1
# Updata  : 2019/10/07 18:38:26
# ----------------------------------
# ---- import modules
import pymel.core as pm
import maya.cmds as mc
import webbrowser
import json

# ---- json
def exportJson(path=r'', dict={}):
    f = open(path, 'w')
    json.dump(dict, f, indent=4)
    f.close()


def importJson(path=r''):
    f = open(path, 'r')
    tmp = f.read()
    res = json.loads(tmp)
    f.close()
    return res


def turtleKiller():
    if mc.pluginInfo('Turtle.mll', loaded=True, q=True):
        mc.unloadPlugin('Turtle.mll', f=True)
    for unk in mc.ls('Turtle*'):
        mc.lockNode(unk, l=False)
        mc.delete(unk)
    print 'unloaded turtle plugin and deleted related nodes successfully.'


def setEdit(typ=0, tgtSet=[]):
    '''
maya object set edit

Parameters:
  - int typ: type of set edit 

Returns:
  - : 

Error:
  - :
    '''
    if typ == 0: # -- add to target set
        if tgtSet:
            for tgt in tgtSet:
                mc.sets(mc.ls(sl=True), add=tgt)
        else:
            mc.warning('Please fill in new set name.')

    elif typ == 1: # -- remove from target set
        if tgtSet:
            for tgt in tgtSet:
                mc.sets(mc.ls(sl=True), rm=tgt)
        else:
            mc.warning('Please fill in new set name.')

    elif typ == 2: # -- simple parent set
        selectObj = mc.ls(sl=True)
        if mc.nodeType(selectObj[-1]) == 'objectSet':
            selectObj = mc.ls(sl=True)
            mc.sets(selectObj[:-1], add=selectObj[-1])
        else :
            mc.warning('Please select objectSet node at the end.')

    elif typ == 3: # -- simple unparent set
        selectObj = mc.ls(sl=True)
        if mc.nodeType(selectObj[-1]) == 'objectSet':
            mc.sets(selectObj[:-1], rm=selectObj[-1])
        else :
            mc.warning('Please select objectSet node at the end.')

    elif typ == 4: # -- add attribute
        atList  = mc.channelBox('mainChannelBox', sma=True, q=True)
        objList = mc.ls(sl=True)
        if tgtSet:
            for tgt in tgtSet:
                if objList:
                    chList = ['{0}.{1}'.format(obj, at) for obj in objList for at in atList]
                    mc.sets(chList, add=tgt)

    mc.select(d=True)


def replaceMaterialForMB(tgt=''):
    # -- create shader for MB
    sd = pm.shadingNode('lambert', asShader=True, n='{0}_lowMT'.format(tgt))
    se = pm.sets(nss=True, r=True, em=True)
    sd.outColor >> se.surfaceShader

    # -- get target objects
    sgList = pm.listConnections(tgt, s=False, c=False, p=False, d=True, t='shadingEngine')
    for sg in sgList:
        objList = [i for i in pm.listConnections(sg, s=True, c=False, p=False, d=False, t='mesh')]
        for obj in objList:
            pm.sets(se, fe=obj)

    # -- get file color texture
    fList = []
    try:
        fList = pm.listConnections('{0}.g_AlbedoMap'.format(tgt), s=True, c=False, p=False, d=False, t='file')
    except:
        pass
    if fList:
        for i in fList:
            path = i.fileTextureName.get()
            i.outColor >> sd.color

    # -- mesh display
    for obj in objList:
        sh = obj.getShape()
        sh.displayEdges.set(0)
        sh.displayColors.set(0)


def createEndJoint(jtDict={}):
    jtList = [u'_202', u'_213', u'_223', u'_233', u'_243', u'_102', u'_113', u'_123', u'_133', u'_143', u'_015', u'_011']

    for i, jt in enumerate(jtList):
        jt = pm.PyNode(jt)
        pos = jt.t.get()
        end = pm.duplicate(jt)[0]
        end.rename('{0}_end'.format(jtList[i]))
        end.setParent(jt)
        end.t.set(pos)

    idList = ['53', '57', '61', '65', '69', '77', '81', '85', '89', '93', '118', '142']
    for id in idList:
        jtInfo = jtDict[id]
        jt     = jtInfo[0]
        if pm.objExists(jt):
            pm.setAttr('{0}.side'.format(jt), jtInfo[1])
            pm.setAttr('{0}.type'.format(jt), jtInfo[2])   
            pm.setAttr('{0}.otherType'.format(jt), jtInfo[3])


def setTimeSlider(jtDict={}):
    pm.playbackOptions(ast=0, aet=10, min=0, max=10, e=True)

    # ---- set Keyframe
    pm.currentTime(0)

    for jtInfo in jtDict.values():
        if jtInfo[0]:
            jt = pm.PyNode(jtInfo[0])
            pm.setKeyframe(jt.rx)
            pm.setKeyframe(jt.ry)
            pm.setKeyframe(jt.rz)
        
    pm.currentTime(10)
    jtList = ['_00a', '_00b', '_00c', '_00d',
              '_201', '_211', '_221', '_231', '_241',
              '_006', '_007', '_008', '_009',
              '_101', '_111', '_121', '_131', '_141',
              '_012', '_013', '_014',
              '_00e', '_00f', '_010'] 
    for jt in jtList:
        pm.setAttr('{0}.rx'.format(jt), 0)
        pm.setAttr('{0}.ry'.format(jt), 0)
        pm.setAttr('{0}.rz'.format(jt), 0)
    for jtInfo in jtDict.values():
        if jtInfo[0]:
            jt = pm.PyNode(jtInfo[0])
            pm.setKeyframe(jt.rx)
            pm.setKeyframe(jt.ry)
            pm.setKeyframe(jt.rz)


def createCharacterDefinition(jtDict={}, prefix=''):
    # ---- create character definition
    pm.mel.eval('hikCreateDefinition;')

    # ---- set Definition : setCharacterObject("_000","Character1",1,0);
    chNode = pm.PyNode('Character1')
    chNode.rename(prefix)
    for k, v in jtDict.items():
        if pm.objExists(v[0]):
            pm.mel.eval('setCharacterObject("{0}", "{1}", {2}, 0);'.format(v[0], chNode.name(), k))


# -- create wld matrix
def createWldMatrix(tgt=''):
    tgtNode = pm.PyNode(tgt)
    wldList = []
    # -- wld_GP
    if not pm.objExists('wld_GP'):
        wldGP = pm.createNode('transform', n='wld_GP')
    else:
        wldGp = pm.PyNode('wld_GP')
    # -- world matrix
    if not mc.objExists('{0}_wld'.format(tgt)):
        wld = pm.createNode('transform', n='{0}_wld'.format(tgt))
        pos = pm.createNode('transform', n='{0}_wld_pos'.format(tgt))
        pos.setParent(wld)
        wld.setParent(wldGp)
        # -- connection
        dmat = pm.createNode('decomposeMatrix', n='{0}_dmat'.format(tgt))
        tgtNode.worldMatrix  >> dmat.inputMatrix
        dmat.outputShear     >> wld.shear
        dmat.outputTranslate >> wld.translate
        dmat.outputRotate    >> wld.rotate
        dmat.outputScale     >> wld.scale
    else:
        mc.warning('{0}_wld already exists in the scene.'.format(tgt))

    return wldList


def duplicateToWldMatrix(jtDict={}, tgt=''):
    log      = ''
    wldPos   = pm.PyNode('{0}_wld_pos'.format(tgt))
    chList   = pm.listRelatives(tgt)
    mcjtList = [jt[0] for jt in jtDict.values() if jt[0]]
    
    for ch in chList:
        if not ch in mcjtList and not '_a' in ch.name():
            rigCh = pm.duplicate(ch, rc=True)[0]
            rigCh.setParent(wldPos)
            
            # -- rename
            rigCh.rename('rig{0}'.format(ch.name()))
            for rch in pm.listRelatives(rigCh, ad=True):
                rch.rename('rig{0}'.format(rch.name()))
            
            log += '{0} ---- duplicate to wld ----> {1} : {2}\n'.format(ch.name(), wldPos.name(), rigCh.name())
    print log


def autoParentToWldMatrix(jtDict={}, tgt=''):
    log      = ''
    wld      = pm.PyNode('{0}_wld_pos'.format(tgt))
    chList   = pm.listRelatives(tgt)
    mcjtList = [jt[0] for jt in jtDict.values()]
    
    for ch in chList:
        if not ch in mcjtList:
            ch.setParent(wld)
            log += '{0} -- parent --> {1}\n'.format(ch.name(), wld.name())
    print log


def returnParentToMcjt(jtDict={}, tgt=''):
    log    = ''
    chList = pm.listRelatives(tgt)
    mcjt   = pm.PyNode(tgt.replace('_wld_pos', ''))
    for ch in chList:
        ch.setParent(mcjt)
        log += '{0} -- parent --> {1}\n'.format(ch.name(), mcjt.name())


def createbaseSet():
    allSet  = mc.sets(n='all_set')

    # -- geo set
    geoSet  = mc.sets(n='geo_set')
    objList = list(set([i.getParent() for i in pm.listRelatives('LOD0', typ='mesh', ad=True)]))
    if objList:
        pm.select(objList, r=True)
        setEdit(0, [geoSet])

    # -- plot set
    plotSet = mc.sets(n='plot_set')
    jtList  = [jt for jt in mc.listRelatives('null', ad=True, typ='joint') if not '_end' in jt]
    if jtList:
        pm.select(jtList, r=True)
        setEdit(0, [plotSet])

    # -- delete set
    delSet  = mc.sets(n='delete_set')
    endList = [jt for jt in mc.listRelatives('null', ad=True, typ='joint') if '_end' in jt]
    pm.select(endList, r=True)
    setEdit(0, [delSet])
    if pm.objExists('workbench'):
        pm.select('workbench', r=True)
        setEdit(0, [delSet])

    # -- save set
    saveSet  = mc.sets(n='save_set')
    plotList = mc.sets('plot_set', q=True)
    resList  = []
    if plotList:
        for i in plotList:
            resList += mc.listRelatives(i, f=True, ap=True)[0].split('|')[1:]
        pm.select(list(set(resList)), r=True)
        setEdit(0, [saveSet])     

    # -- ctrl set
    ctrlSet  = mc.sets(n='ctrl_set')
    ctrlList = mc.ls('*_ctrl', typ='transform')
    if ctrlList:
        pm.select(ctrlList, r=True)
        setEdit(0, [ctrlSet])  

    # -- rig set
    rigSet  = mc.sets(n='rig_set')

    # -- rig extension set
    extSet  = mc.sets(n='rig_extSet')

    # -- all set
    setList = [geoSet, plotSet, delSet, saveSet, ctrlSet, rigSet, extSet]
    for i in setList:
        mc.sets(i, add='all_set')


def exportFbx(path=r''):
    mc.file(path, f   = True, 
                  op  = 'v=0;',
                  typ = 'FBX export',
                  pr  = True,
                  ea  = True)


class rigSupportToolsUI(object):
    def __init__(self):
        self.__ver__          = '0.0.1'
        self.windowManageName = 'rigSupportTools'
        self.windowTitle      = 'Rig support v{0}'.format(self.__ver__)
        self.windowSize       = [400, 600]
        self._mayaHelp_url    = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
        self._toolHelp_url    = r'https://wisdom.cygames.jp/display/tsubasa/%5BMaya%5D+FC+Support+Tools'
        self._jsonPath_       = r'//cgs-str-fas05/100_projects/115_tsubasa/30_design/07_CutScene/98_member/RyoKanda/rig/primary/definition/pl_base.json'
        self._scenePath_      = pm.Env().sceneName()


    def checkWindowOverlap(self):
        if pm.window(self.windowManageName, ex=True):
            pm.deleteUI(self.windowManageName)


    def show_mayaHelp(self, *args):
        webbrowser.open_new_tab(self._mayaHelp_url)


    def show_toolHelp(self, *args):
        webbrowser.open_new_tab(self._toolHelp_url)

    # -- check ---------------------------------------------------------------
    def check(self):
        print 'OK'

    # -- function ------------------------------------------------------------
    def getRootStr(self):
        aRoot = ''
        if pm.objExists('null'):
            aRoot = mc.listRelatives('null', p=True)[0]
            if not '_00' in aRoot:
                aRoot = '{0}_00'.format(aRoot)
            return aRoot
        else:
            return aRoot


    def renameRoot(self):
        aName = self._an_txg.getText()
        aRoot = pm.listRelatives('null', p=True)[0]
        aRoot.rename(aName)
        print 'Root node name : {0}'.format(aRoot)


    def createWorkbench(self):
        prefix = self.getRootStr()
        # -- create workbench
        wb  = pm.createNode('transform', n='workbench')
        print 'create workbench node : workbench'

        # -- parent unused nodes to workbench 
        defaultList = ['front', 'side', 'top', 'persp', 'workbench', prefix]
        for i in pm.ls('|*', typ='transform'):
            if not i in defaultList:
                i.setParent(wb)
                print '{0} ---- parent ----> {1}'.format(i.name(), wb)


    def arrangeJointDisplay(self):
        uocLog = ''
        dlaLog = ''
        for jt in pm.ls(typ='joint'):
            uocVal = jt.uoc.get()
            if uocVal: 
                jt.uoc.set(0)
                uocLog += 'use object color off : {0} \n'.format(jt.name())
            
            dlaVal = jt.dla.get()
            if dlaVal:
                jt.dla.set(0)
                dlaLog += 'display local lotation axis off : {0} \n'.format(jt.name())
        
        # -- hide null 
        pm.setAttr('null.drawStyle', 2)
        
        # -- log
        print 'null drawStype : none'
        print uocLog
        print dlaLog


    def arrageMeshDisplay(self):
        csLog = ''
        deLog = ''
        for mesh in pm.ls(typ='mesh'):
            # ---- delete vertex color
            csList = pm.polyColorSet(mesh, acs=True, q=True)
            if csList:
                for cs in csList:
                    pm.polyColorSet(mesh, cs=cs, d=True)
                    csLog += 'delete color set : {0} \n'.format(cs)

            # ---- edge display standard
            deVal = mesh.displayEdges.get()
            if not deVal == 0:
                mesh.displayEdges.set(0)
                deLog += 'mesh display edge standard : {0} \n'.format(mesh.name())


    def launchHypershade(self):
        pm.mel.eval('HypershadeWindow;')


    def materialReplacement(self):
        pm.select(pm.ls(typ='dx11Shader'))
        for i in mc.ls(sl=True):
            replaceMaterialForMB(i)
        pm.modelEditor('modelPanel4', tsl=True, e=True)


    def deleteUnusedNode(self):
        pm.mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')


    def getJsonDialog(self):
        jsonFilter = 'Json Files (*.json)'
        stPath     = self._cdp_txf.getText()
        if not stPath:
            stPath = self._jsonPath_
        filePath   = pm.fileDialog2(ff  = jsonFilter, 
                                    ds  = 2, 
                                    spe = False, 
                                    dir = stPath, 
                                    fm  = 1)[0]
        self._cdp_txf.setText(filePath)


    def deleteAnimKey(self):
        log = ''
        animList = pm.ls(typ=['animCurveTA', 'animCurveTL', 'animCurveTU'])
        pm.delete(animList)
        for i in animList:
            log += 'delete animation key : {0} \n'.format(i.name())
        print log


    def run_createEndJoint(self):
        jtDict = importJson(self._cdp_txf.getText())
        createEndJoint(jtDict)


    def run_setTimeSlider(self):
        jtDict = importJson(self._cdp_txf.getText())
        setTimeSlider(jtDict)


    def run_createCharacterDefinition(self):
        prefix = self.getRootStr().split('_')[0]
        jtDict = importJson(self._cdp_txf.getText())
        createCharacterDefinition(jtDict, prefix)


    def createRigHierarchy(self):
        aRoot = self.getRootStr()
        rigGP = pm.createNode('transform', n='rig_GP')
        mtxGP = pm.createNode('transform', n='matrix_GP')
        wldGP = pm.createNode('transform', n='wld_GP')
        lclGP = pm.createNode('transform', n='lcl_GP')
        wldGP.setParent(mtxGP)
        lclGP.setParent(mtxGP)
        mtxGP.setParent(rigGP)
        rigGP.setParent(aRoot) 


    def createPrimaryWorldMatrix(self):
        jtDict = importJson(self._cdp_txf.getText())
        # -- create mcjt matrix
        mcjtList = [jt[0] for jt in jtDict.values() if jt[0]]
        mc.select(mcjtList, r=True)
        for i in mc.ls(sl=True):
            if i in mcjtList and not '_end' in i:
                createWldMatrix(i)


    def createSelectedWorldMatrix(self):
        jtDict = importJson(self._cdp_txf.getText())
        # -- create mcjt matrix
        mcjtList = [jt[0] for jt in jtDict.values() if jt[0]]
        for i in mc.ls(sl=True):
            createWldMatrix(i)


    def duplicatePrimaryWorldMatrix(self):
        jtDict = importJson(self._cdp_txf.getText())
        # -- create mcjt matrix
        mcjtList = [jt[0] for jt in jtDict.values() if jt[0]]
        mc.select(mcjtList, r=True)
        for i in mc.ls(sl=True):
            if i in mcjtList and not '_end' in i:
                duplicateToWldMatrix(jtDict, i)


    def duplicateSelectedWorldMatrix(self):
        jtDict = importJson(self._cdp_txf.getText())
        for i in mc.ls(sl=True):
            duplicateToWldMatrix(jtDict, i)


    def extendEndJoint(self):
        for i in pm.selected():
            pos = i.t.get()
            end = pm.duplicate(i)[0]
            end.rename('{0}_end'.format(i.name()))
            end.setParent(i)
            end.t.set(pos)


    def autoParentToMatrix(self):
        jtDict = importJson(self._cdp_txf.getText())
        mcjtList = [jt[0] for jt in jtDict.values() if jt[0]]
        mc.select(mcjtList, r=True)
        for i in mc.ls(sl=True):
            if i in mcjtList and not '_end' in i:
                autoParentToWldMatrix(jtDict, i)


    def returnParentToMatrix(self):
        jtDict = importJson(self._cdp_txf.getText())
        mcjtList = [jt[0] for jt in jtDict.values() if jt[0]]
        mc.select(mcjtList, r=True)
        for i in mc.ls(sl=True):
            returnParentToMcjt(jtDict, '{0}_wld_pos'.format(i))


    def deleteUnusedMatrix(self):
        for i in mc.ls('_*_wld_pos'):
            if not mc.listRelatives(i, c=True):
                mc.delete(i.replace('_pos', '')) 


    def createSet(self):
        createbaseSet()


    def launchSetEditor(self):
        import setEditor.ui
        setEditor.ui.showUI()


    def setFbxPath(self):
        fbxFilter = 'fbx Files (*.fbx)'
        stPath    = self._fbx_txf.getText()
        if not stPath:
            stPath = self._jsonPath_
        filePath   = pm.fileDialog2(ff  = fbxFilter, 
                                    ds  = 2, 
                                    spe = True, 
                                    dir = stPath, 
                                    fm  = 0)[0]
        self._fbx_txf.setText(filePath)


    def launchDiagnosis(self):
        import diagnosis.ui
        reload(diagnosis.ui)
        diagnosis.ui.showUI()


    def run_exportFbx(self):
        path = self._fbx_txf.getText()
        exportFbx(path)
 

    # -- edit UI -------------------------------------------------------------
    def resetUI(self):
        self._an_txg.setText('')


    # -- UI ------------------------------------------------------------------------- 
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
        pm.menuItem(l = 'Reset UI',
                    i = 'redrawPaintEffects.png',
                    c = pm.Callback(self.resetUI))
        pm.menu(l  ='Help', 
                to = False, 
                hm = True)
        pm.menuItem(l = 'Maya 2019 HELP',
                    c = self.show_mayaHelp)
        pm.menuItem(d = True)
        pm.menuItem(l = 'Tool HELP',
                    c = self.show_toolHelp)

        # -- base form layout
        self.fmL0 = pm.formLayout(nd  = 100)
        with self.fmL0:
            self.sep0 = pm.separator()
            self.tbL0 = pm.tabLayout(bs = 'none', 
                                     cr = True, 
                                     tp = 'west')
            with self.tbL0:
                self._tb0_cmL = pm.columnLayout(adj=True)
                with self._tb0_cmL:
                    self._ns_sep0 = pm.separator(h=7, st='none')
                    self._an_txg  = pm.textFieldGrp(l  = ' Asset name : ', 
                                                   pht = 'pl0000',
                                                   tx  = self.getRootStr(),
                                                   adj = 2, 
                                                   cw  = [(1, 80), (2, 80)],
                                                   h   = 24)
                    self._ns_sep1 = pm.separator(h=7, st='none')
                    self._chk_frL1 = pm.frameLayout(l = 'Data Arrangement', 
                                                  cll = True,
                                                  bgc = (0.0, 0.3, 0.7))
                    with self._chk_frL1:
                        self._chk_fmL = pm.formLayout(nd=100)
                        with self._chk_fmL:
                            self._ren_btn = pm.button(l = 'rename root', 
                                                      c = pm.Callback(self.renameRoot),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._cwb_btn = pm.button(l = 'create workbench', 
                                                      c = pm.Callback(self.createWorkbench),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._dtp_btn = pm.button(l = 'delete turtle plugin', 
                                                      c = pm.Callback(turtleKiller),
                                                    bgc = (0.4, 0.4, 0.4))

                            self._arg_txt = pm.text(l = ' Arrangement: ',
                                                   al = 'left',
                                                    h = 24)
                            self._ajd_btn = pm.button(l = 'joint display', 
                                                      c = pm.Callback(self.arrangeJointDisplay),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._aja_btn = pm.button(l = 'joint attribute', 
                                                      c = pm.Callback(self.arrangeJointDisplay),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._amd_btn = pm.button(l = 'mesh display', 
                                                      c = pm.Callback(self.arrageMeshDisplay),
                                                    bgc = (0.4, 0.4, 0.4))

                            self._mat_txt = pm.text(l = ' Materials: ',
                                                   al = 'left',
                                                    h = 24)
                            self._lhs_btn = pm.button(l = 'launch Hypershade', 
                                                      c = pm.Callback(self.launchHypershade),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._rmf_btn = pm.button(l = 'replace materials for MB', 
                                                      c = pm.Callback(self.materialReplacement),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._dun_btn = pm.button(l = 'delete unused node', 
                                                      c = pm.Callback(self.deleteUnusedNode),
                                                    bgc = (0.4, 0.4, 0.4))


                    self._chk_frL2 = pm.frameLayout(l = 'Character Definition', 
                                                  cll = True,
                                                  bgc = (0.0, 0.25, 0.6))
                    with self._chk_frL2:
                        self._cdf_fmL = pm.formLayout(nd=100)
                        with self._cdf_fmL:
                            self._cdp_txt = pm.text(l = ' Json file: ',
                                                   al = 'left',
                                                    h = 24)
                            self._cdp_txf = pm.textField(tx = self._jsonPath_,
                                                         h  = 24)
                            self._cdb_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                              i   = 'browseFolder.png', 
                                                              bgc = (0.4, 0.4, 0.4),
                                                              l   = 'browse', 
                                                              c   = pm.Callback(self.getJsonDialog), 
                                                              h   = 24,
                                                              w   = 75,
                                                              mw  = 2
                                                              )
                            self._dak_btn = pm.button(l = 'delete animation keys', 
                                                      c = pm.Callback(self.deleteAnimKey),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._cej_btn = pm.button(l = 'create end joints', 
                                                      c = pm.Callback(self.run_createEndJoint),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._sts_btn = pm.button(l = 'T-pose & set time slider', 
                                                      c = pm.Callback(self.run_setTimeSlider),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._ccd_btn = pm.button(l = 'create character definition', 
                                                      c = pm.Callback(self.run_createCharacterDefinition),
                                                    bgc = (0.4, 0.4, 0.4))


                    self._chk_frL3 = pm.frameLayout(l = 'Matrix Hierarachy', 
                                                  cll = True,
                                                  bgc = (0.0, 0.2, 0.5))
                    with self._chk_frL3:
                        self._rig_fmL = pm.formLayout(nd=100)
                        with self._rig_fmL:
                            self._crh_btn = pm.button(l = 'create hierarchy', 
                                                      c = pm.Callback(self.createRigHierarchy),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._cpm_btn = pm.button(l = 'create primary world matrix', 
                                                      c = pm.Callback(self.createPrimaryWorldMatrix),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._csm_btn = pm.button(l = 'create selected world matrix', 
                                                      c = pm.Callback(self.createSelectedWorldMatrix),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._dph_btn = pm.button(l = 'duplicate primary hierarchy', 
                                                      c = pm.Callback(self.duplicatePrimaryWorldMatrix),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._dsh_btn = pm.button(l = 'duplicate selected hierarchy', 
                                                      c = pm.Callback(self.duplicateSelectedWorldMatrix),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._eej_btn = pm.button(l = 'extend end joint', 
                                                      c = pm.Callback(self.extendEndJoint),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._apm_btn = pm.button(l = 'parent joint -> matrix', 
                                                      c = pm.Callback(self.autoParentToMatrix),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._rpm_btn = pm.button(l = 'parent matrix -> joint', 
                                                      c = pm.Callback(self.returnParentToMatrix),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._dum_btn = pm.button(l = 'delete unused matrix', 
                                                      c = pm.Callback(self.deleteUnusedMatrix),
                                                    bgc = (0.4, 0.4, 0.4))


                    self._chk_frL4 = pm.frameLayout(l = 'Sets', 
                                                  cll = True,
                                                  bgc = (0.0, 0.15, 0.4))
                    with self._chk_frL4:
                        self._set_fmL = pm.formLayout(nd=100)
                        with self._set_fmL:
                            self._lse_btn = pm.button(l = 'launch set editor', 
                                                      c = pm.Callback(self.launchSetEditor),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._cbs_btn = pm.button(l = 'create base sets', 
                                                      c = pm.Callback(self.createSet),
                                                    bgc = (0.4, 0.4, 0.4))


                    self._chk_frL5 = pm.frameLayout(l = 'Export FBX', 
                                                  cll = True,
                                                  bgc = (0.0, 0.1, 0.3))
                    with self._chk_frL5:
                        self._fbx_fmL = pm.formLayout(nd=100)
                        with self._fbx_fmL:
                            self._fbx_txt = pm.text(l = ' FBX Export: ',
                                                   al = 'left',
                                                    h = 24)
                            self._fbx_txf = pm.textField(tx = self._scenePath_.replace('.mb', '.fbx'),
                                                         h  = 24)
                            self._fbx_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                              i   = 'browseFolder.png', 
                                                              bgc = (0.4, 0.4, 0.4),
                                                              l   = 'browse', 
                                                              c   = pm.Callback(self.setFbxPath), 
                                                              h   = 24,
                                                              w   = 75,
                                                              mw  = 2
                                                              )
                            self._ldg_btn = pm.button(l = 'launch diagnosis', 
                                                      c = pm.Callback(self.launchDiagnosis),
                                                    bgc = (0.4, 0.4, 0.4))
                            self._exf_btn = pm.button(l = 'Export FBX', 
                                                      c = pm.Callback(self.run_exportFbx),
                                                    bgc = (0.4, 0.4, 0.4))


        # -- Edit UI Layout
        pm.formLayout(self.fmL0, e=True,
               af = [(self.sep0, 'top', 0), (self.sep0, 'left', 0), (self.sep0, 'right', 0), 
                     (self.tbL0, 'top', 0), (self.tbL0, 'left', 0), (self.tbL0, 'right', 0),  (self.tbL0, 'bottom', 0),
                    ])
        pm.formLayout(self._chk_fmL, e=True,
               af = [(self._ren_btn, 'top',   0), (self._ren_btn, 'left', 0), (self._ren_btn, 'right', 0), 
                     (self._cwb_btn, 'top',  25), (self._cwb_btn, 'left', 0), (self._cwb_btn, 'right', 0), 
                     (self._dtp_btn, 'top',  50), (self._dtp_btn, 'left', 0), (self._dtp_btn, 'right', 0),
                     (self._arg_txt, 'top',  75), (self._arg_txt, 'left', 0), (self._arg_txt, 'right', 0), 
                     (self._ajd_btn, 'top', 100), (self._ajd_btn, 'left', 0), (self._ajd_btn, 'right', 0),  
                     (self._aja_btn, 'top', 125), (self._aja_btn, 'left', 0), (self._aja_btn, 'right', 0),  
                     (self._amd_btn, 'top', 150), (self._amd_btn, 'left', 0), (self._amd_btn, 'right', 0), 
                     (self._mat_txt, 'top', 175), (self._mat_txt, 'left', 0), (self._mat_txt, 'right', 0), 
                     (self._lhs_btn, 'top', 200), (self._lhs_btn, 'left', 0), (self._lhs_btn, 'right', 0),  
                     (self._rmf_btn, 'top', 225), (self._rmf_btn, 'left', 0), (self._rmf_btn, 'right', 0),
                     (self._dun_btn, 'top', 250), (self._dun_btn, 'left', 0), (self._dun_btn, 'right', 0),
                    ])
        pm.formLayout(self._cdf_fmL, e=True,
               af = [(self._cdp_txt, 'top',   0), (self._cdp_txt, 'left', 0), (self._cdp_txt, 'right', 0),
                     (self._cdp_txf, 'top',  25), (self._cdp_txf, 'left', 0), (self._cdp_txf, 'right', 0),
                     (self._cdb_btn, 'top',  50),                             (self._cdb_btn, 'right', 0),
                     (self._dak_btn, 'top',  75), (self._dak_btn, 'left', 0), (self._dak_btn, 'right', 0), 
                     (self._cej_btn, 'top', 100), (self._cej_btn, 'left', 0), (self._cej_btn, 'right', 0), 
                     (self._sts_btn, 'top', 125), (self._sts_btn, 'left', 0), (self._sts_btn, 'right', 0), 
                     (self._ccd_btn, 'top', 150), (self._ccd_btn, 'left', 0), (self._ccd_btn, 'right', 0), 
                    ])
        pm.formLayout(self._rig_fmL, e=True,
               af = [(self._crh_btn, 'top',   0), (self._crh_btn, 'left', 0), (self._crh_btn, 'right', 0), 
                     (self._cpm_btn, 'top',  25), (self._cpm_btn, 'left', 0), (self._cpm_btn, 'right', 0), 
                     (self._csm_btn, 'top',  50), (self._csm_btn, 'left', 0), (self._csm_btn, 'right', 0), 
                     (self._dph_btn, 'top',  75), (self._dph_btn, 'left', 0), (self._dph_btn, 'right', 0), 
                     (self._dsh_btn, 'top', 100), (self._dsh_btn, 'left', 0), (self._dsh_btn, 'right', 0), 
                     (self._eej_btn, 'top', 125), (self._eej_btn, 'left', 0), (self._eej_btn, 'right', 0), 
                     (self._apm_btn, 'top', 150), (self._apm_btn, 'left', 0), (self._apm_btn, 'right', 0),
                     (self._rpm_btn, 'top', 175), (self._rpm_btn, 'left', 0), (self._rpm_btn, 'right', 0),
                     (self._dum_btn, 'top', 200), (self._dum_btn, 'left', 0), (self._dum_btn, 'right', 0), 
                    ])
        pm.formLayout(self._set_fmL, e=True,
               af = [(self._lse_btn, 'top',   0), (self._lse_btn, 'left', 0), (self._lse_btn, 'right', 0), 
                     (self._cbs_btn, 'top',  25), (self._cbs_btn, 'left', 0), (self._cbs_btn, 'right', 0), 
                    ])
        pm.formLayout(self._fbx_fmL, e=True,
               af = [(self._fbx_txt, 'top',   0), (self._fbx_txt, 'left', 0), (self._fbx_txt, 'right', 0),
                     (self._fbx_txf, 'top',  25), (self._fbx_txf, 'left', 0), (self._fbx_txf, 'right', 0),
                     (self._fbx_btn, 'top',  50),                             (self._fbx_btn, 'right', 0),
                     (self._ldg_btn, 'top',  75), (self._ldg_btn, 'left', 0), (self._ldg_btn, 'right', 0), 
                     (self._exf_btn, 'top', 100), (self._exf_btn, 'left', 0), (self._exf_btn, 'right', 0),
                    ])
        # -- Tab label edit
        pm.tabLayout(self.tbL0, tl = [(self._tb0_cmL, 'Rig')], e=True)

        window.show()

def showUI():
    testIns = rigSupportToolsUI()
    testIns.main()
