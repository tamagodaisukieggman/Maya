# -*- coding: utf-8 -*-

import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mm

class CreateNCloth():
    def __init__(self):
        self.src = []
        self.init = []
        self.rest = []
        self.sel = []
        self.tgtNuc = []
        self.solver = []
        self.selSolver = []
        self.set = []
        self.crSet = []
        self.nucGP = []


    def _getUnconnectedShapeOrigins(self, clnSrc):   # cleanup
        ### get unConnectedShapeOrigins ###
        pm.select(cl=1)
        garb = []

        for tgt in clnSrc:
            list = pm.listConnections(tgt, d=1, s=0)
            scn = pm.connectionInfo(tgt + '.instObjGroups', isSource=1)
            if (len(list) < 1):
                if (scn == 0):
                    if tgt.isIntermediate():
                        garb.append(tgt)
        return garb


    def _cleanupMeshes(self, cln):   # cleanup
        ### delete History ###
        tgt = pm.ls(cln)
        attrs = ['t', 'r', 's']
        axis = ['x', 'y', 'z']

        for src in tgt:
            clnShape = pm.listRelatives(src, s=1)
            pm.delete(src, ch=1)
            orig = self._getUnconnectedShapeOrigins(clnSrc = pm.listRelatives(src, s=1))
            pm.delete(orig)
            pm.polyNormalPerVertex(src, ufn=1)
            pm.polySoftEdge(src, a=180, ch=0)
            if not ('_INIT' in str(src) or '_REST' in str(src)):
                try:
                    for attr in attrs:
                        for ax in axis:
                            pm.setAttr(src+ '.'+attr+ax, l=0)
                    pm.makeIdentity(src, apply=1, t=1, r=1, s=1, n=0)
                except:
                    for i in pm.listAttr(src):
                        src.attr(i).unlock()
                    pm.makeIdentity(src, apply=1, t=1, r=1, s=1, n=0)
            pm.setAttr(src+ '.visibility', l=0)
            pm.setAttr(clnShape[0]+ '.displayBorders', 1)
            pm.setAttr(clnShape[0]+ '.borderWidth', 4.7)
            pm.delete(src, ch=1)


    def _assignSolver(self, solver = ""):    # assign nSolver
        nuc = pm.ls(typ='nucleus')
        self.solver = pm.ls(solver, typ='nucleus')
        self.selSolver = solver
        nucRe = []

        for tgtNuc in nuc:
            if (tgtNuc == self.selSolver):
                nucRe = tgtNuc

        ### new nucleus ###
        if (self.solver == []):
            print ('**** nucleus "NEW" ****')
            mm.eval('$gActiveNucleusNode = "";')
        ### exist nucleus ###
        elif nucRe:
            print ('**** nucleus "exist" ****')
            mm.eval('$gActiveNucleusNode = "%s";' % self.solver[0])
        ### new nucleus ###
        else:
            print ('**** nucleus "NEW" **** # %s' % solver)
            mm.eval('$gActiveNucleusNode = "";')


    def _prepObj(self, mesh, cr):   # prepare objects
        ### create groups for clothObj ###
        self.tempGP = pm.group(em=1, name='_____tempGP')

        for obj in mesh:
            ### cleanup Object ###
            clnTgt = obj
            self._cleanupMeshes(cln = clnTgt)

            ### get Shape ###
            objShape = pm.listRelatives(obj, s=1, ni=1)
            ### rename originalObj ###
            if not("_CLOTH" in str(obj)):
                obj.rename('%s_CLOTH' % obj)
            objShape[0].rename('%sShape' % obj)

            ### create INIT & REST ###
            initObj = pm.duplicate(obj, n='%s_INIT' % obj)
            initObjShape = pm.listRelatives(initObj, s=1, ni=1)
            initObjShape[0].rename('%sShape' % initObj[0])
            restObj = pm.duplicate(obj, n='%s_REST' % obj)
            restObjShape = pm.listRelatives(restObj, s=1, ni=1)
            restObjShape[0].rename('%sShape' % restObj[0])

            ### cleanup Object ###
            clnTgt = [obj, initObj, restObj]
            self._cleanupMeshes(cln = clnTgt)

            ### create blendShape ###
            bs = pm.blendShape(initObj, obj, o='local', n='%s_blendShape' % initObj[0])[0]
            bs.weight[0].set(1)
            pm.setAttr(bs+ '.%s' % initObj[0], l=1)
            ### create skinCluster ###    clA=INIT, clB=cloth
            clA = pm.cluster(initObj)[0]
            clAHandle = pm.PyNode(clA + 'Handle')
            clANode = pm.PyNode(clA)
            clAHandle.rename('%s_cluster' % initObj[0])
            clANode.rename('%s_clusterNode' % initObj[0])
            clB = pm.cluster(obj)[0]
            clBHandle = pm.PyNode(clB + 'Handle')
            clBNode = pm.PyNode(clB)
            clBHandle.rename('%s_cluster' % obj)
            clBNode.rename('%s_clusterNode' % obj)
            pm.hide(initObj, restObj, clBHandle)
            pm.parent(clBHandle, clAHandle)
            clAGP = pm.group(clAHandle, n='%s_cluster_space' % initObj[0])

            self.src = pm.ls(obj)
            self.init = initObj
            self.rest = restObj

            ### create clothNode ###
            cltNode = self._createNClothNode()

            ### obj into the set ###
            mm.eval('sets -edit -forceElement  %s %s ;' % (self.set, cltNode))
            if self.crSet:
                mm.eval('sets -edit -forceElement  %s %s ;' % (self.crSet, cltNode))
            ### parent objects ###
            pm.parent(obj, cltNode, initObj, restObj, self.tempGP)
            ### append selectObj ###
            self.sel.append(self.src)


    def _createNClothNode(self):    # apply nCloth
        cltNode = []
        cltObj = pm.ls(self.src)[0]

        ### convert to nCloth ###
        pm.select(self.src)
        mm.eval('createNCloth 0;')

        ### rename clothNode ###
        cltNodeShape = pm.listHistory(cltObj, type='nCloth')
        cltShape = pm.listRelatives(cltObj, s=1, ni=1)
        cltNode = cltNodeShape[0].getParent()
        cltNode.rename("%s_node" % cltObj)
        cltShape[0].rename("%s_outputCloth" % cltObj)
        ### setAttr clothOrig ###
        pm.setAttr(cltObj+ '.translate', l=1)
        pm.setAttr(cltObj+ '.rotate', l=1)
        pm.setAttr(cltObj+ '.scale', l=1)
        ### setAttr clothNode ###
        pm.setAttr(cltNodeShape[0]+ '.selfCollisionFlag', 1)
        pm.setAttr(cltNodeShape[0]+ '.thickness', 0.35)
        pm.setAttr(cltNodeShape[0]+ '.displayColor', 0.918, 0.57, 0, type='double3')
        pm.setAttr(cltNodeShape[0]+ '.friction', 0.01)
        pm.setAttr(cltNodeShape[0]+ '.stretchResistance', 100)
        pm.setAttr(cltNodeShape[0]+ '.pointMass', 0.1)
        pm.setAttr(cltNodeShape[0]+ '.lift', 0.015)
        pm.setAttr(cltNodeShape[0]+ '.drag', 0.05)
        pm.setAttr(cltNodeShape[0]+ '.tangentialDrag', 0.05)
        pm.setAttr(cltNodeShape[0]+ '.damp', 0.1)
        pm.setAttr(cltNodeShape[0]+ '.stretchDamp', 0.5)
        pm.setAttr(cltNodeShape[0]+ '.scalingRelation', 1)
        ### display borderEdges ###
        pm.setAttr(cltShape[0]+ '.displayBorders', 1)
        pm.setAttr(cltShape[0]+ '.borderWidth', 4.7)

        ### connect REST to CLOTH ###
        restShape = pm.listRelatives(self.rest, s=1)
        pm.PyNode(restShape[0]).worldMesh[0] >> pm.PyNode(cltNodeShape[0]).restShapeMesh

        print ('------------------------------------------------------')
        print ('==== added clothNode ==== # %s' % cltNode)
        return cltNode


    def _editClothAndNucleus(self):    # assign&rename nucleus main
        nuc = pm.ls(typ='nucleus')
        tgtName = []
        print ('------------------------------------------------------')
        print ('******\n')

        for loop in self.sel:
            clt = pm.listHistory(loop, type='nCloth')
            cltNode = clt[0].getParent()
            self.tgtNuc = pm.listHistory(clt, type='nucleus')[0]

            if (self.solver == []):
                ### newSolver rename as inputName ###
                if not (self.selSolver == ""):
                    if not ('__' in self.selSolver):
                        if not ('nucleus' in self.selSolver):
                            if ('Nucleus' in self.selSolver):
                                self.selSolver = self.selSolver.replace('Nucleus','')
                                self.selSolver = '__' + self.selSolver + '_nucleus'
                            else:
                                self.selSolver = '__' + self.selSolver + '_nucleus'
                        else:
                            self.selSolver = '__' + self.selSolver
                    elif not ('nucleus' in self.selSolver):
                        if ('Nucleus' in self.selSolver):
                            self.selSolver = self.selSolver.replace('Nucleus','')
                            self.selSolver = self.selSolver + '_nucleus'
                        else:
                            self.selSolver = self.selSolver + '_nucleus'
                    elif ('Nucleus' in self.selSolver):
                        self.selSolver = self.selSolver.replace('Nucleus','')

                    ### look into self.selSolver ###
                    for exNuc in nuc:
                        ### if the name already exists ###
                        if (str(exNuc) == self.selSolver):
                            print '**** the solver already exists ****'
                            delNuc = pm.listHistory(clt, type='nucleus')[0]
                            pm.select(clt)
                            mm.eval('assignNSolver "%s";' % self.selSolver)
                            self.tgtNuc = pm.listHistory(clt, type='nucleus')[0]
                            self._editClothAndNucleusElse(loop, cltNode)
                            delTgt = pm.listConnections(delNuc, type='nCloth')
                            if (delTgt == []):
                                pm.delete(delNuc)

                    if not (pm.objExists(self.selSolver)):
                        ### rename nucleus ###
                        self.tgtNuc.rename('%s' % self.selSolver)
                        print ('--------------------------------------------------')
                        print ("---- assign NewSolver ---- # '%s' >> '%s'" % (self.tgtNuc, cltNode))
                        print ('--------------------------------------------------')
                        self._nucleusSetAttributes(loop)
                ### newSolver rename by default ###
                else:
                    if not (tgtName == self.tgtNuc):
                        name = self._countUpNucleus()
                        self.tgtNuc.rename(name)
                        tgtName = self.tgtNuc
                        print ('--------------------------------------------------')
                        print ("---- assign NewSolver ---- # '%s' >> '%s'" % (self.tgtNuc, cltNode))
                        print ('--------------------------------------------------')
                        self._nucleusSetAttributes(loop)
                    else:
                        self._editClothAndNucleusElse(loop, cltNode)
            else:
                self._editClothAndNucleusElse(loop, cltNode)
            print ('\n== Done == %s\n\n' % loop[0])


    def _editClothAndNucleusElse(self, loop, cltNode):    # assign&rename nucleus else
        print ('--------------------------------------------------')
        print ("---- assign ExistSolver ---- # '%s' >> '%s'" % (self.tgtNuc, cltNode))
        print ('--------------------------------------------------')
        initCl = pm.PyNode('%s_INIT_cluster_space' % loop[0])
        initGP = pm.PyNode('%s_INIT_clusterGP' % self.tgtNuc)
        self.nucGP = pm.PyNode('%s_GP' % self.tgtNuc)
        defGP = pm.PyNode('%s_deformerGP' % self.tgtNuc)
        fieldGP = pm.PyNode('%s_fieldGP' % self.tgtNuc)
        clothObj = self.tempGP.getChildren()
        pm.parent(defGP, fieldGP, w=1)
        pm.parent(clothObj, defGP, fieldGP, self.nucGP)
        pm.parent(initCl, initGP)
        print ("**** parent object **** # '%s' >> '%s_GP'" % (loop[0], self.tgtNuc))
        print ('--------------------------------------------------')


    def _nucleusSetAttributes(self, loop):    # setAttr nucleus
        ### setAttr nucleus ###
        pm.expression(s='%s.startFrame = `playbackOptions -q -min`' % self.tgtNuc)
        pm.setAttr(self.tgtNuc+ '.airDensity', 1)
        pm.setAttr(self.tgtNuc+ '.subSteps', 15)
        pm.setAttr(self.tgtNuc+ '.spaceScale', 0.01)
        ### create groups ###
        self._makeHierarchy(loop)


    def _makeHierarchy(self, loop):   # create groups
        initCl = pm.PyNode('%s_INIT_cluster_space' % loop[0])
        initGP = pm.group(initCl, name='%s_INIT_clusterGP' % self.tgtNuc)
        colGP = pm.group(em=1, name='%s_collisionGP' % self.tgtNuc)
        constPSGP = pm.group(em=1, name='%s_PS_GP' % self.tgtNuc)
        constCCGP = pm.group(em=1, name='%s_CC_GP' % self.tgtNuc)
        constOtherGP = pm.group(em=1, name='%s_Other_GP' % self.tgtNuc)
        constGP = pm.group(constPSGP, constCCGP, constOtherGP, name='%s_constraintGP' % self.tgtNuc)
        clothObj = self.tempGP.getChildren()
        defGP = pm.group(em=1, name='%s_deformerGP' % self.tgtNuc)
        fieldGP = pm.group(em=1, name='%s_fieldGP' % self.tgtNuc)
        self.nucGP = pm.group(self.tgtNuc, initGP, colGP, constGP, clothObj, defGP, fieldGP,  n='%s_GP'  % self.tgtNuc)
        pm.hide(initGP)
        print ('++++ created groups ++++ # %s_GP' % self.tgtNuc)
        print ('--------------------------------------------------')
        print ("**** parent object **** # '%s' >> '%s_GP'" % (loop[0], self.tgtNuc))
        print ('--------------------------------------------------')


    def _addConnectAttribute(self):    # add&connect Attributes
        for obj in self.sel:
            if not (pm.attributeQuery('enableINIT', n=obj[0], ex=1)):
                pm.addAttr(obj, ln='clothLocalSetting', at='enum', en='=======', k=1)
                pm.addAttr(obj, ln='enableINIT', at='bool', k=1)
            else:
                pm.setAttr(obj[0]+ '.enableINIT', 0)
            pm.setAttr(obj[0]+ '.clothLocalSetting', l=1)
            rev = pm.createNode('reverse', n='%s_cluster_reverse' % obj[0])
            pm.setAttr(rev+ '.inputY', l=1)
            pm.setAttr(rev+ '.inputZ', l=1)
            pm.PyNode(obj[0]).enableINIT >> pm.PyNode(rev).inputX
            pm.PyNode(rev).outputX >> pm.PyNode('%s_clusterNode' % obj[0]).envelope
            pm.PyNode(obj[0]).enableINIT >> pm.PyNode('%s_INIT_blendShape' % obj[0]).envelope


    def _countUpNucleus(self):    # countUp nucleusNumber
        tgt = []
        for nuc in pm.ls(typ='nucleus'):
            if ('__nucleus' in str(nuc)):
                tgt.append(nuc)
        sp = self.tgtNuc.split('nucleus')
        name = '__nucleus{}'.format(int(sp[1]) + len(tgt))
        return name


    def _getClothRig(self, cr):
        if cr:
            pm.parent(self.nucGP, cr)



    def _clothSetup(self, cr = "", solver = ""):   # main
        warn = self._warning()
        mesh = []
        if not (warn == None):
            mesh = self._checkObj()
            if mesh:
                print ('\n\n######################################################\n')
                self._createSets(cr)
                self._assignSolver(solver)
                self._prepObj(mesh, cr)
                self._editClothAndNucleus()
                self._addConnectAttribute()
                self._getClothRig(cr)
                pm.delete(self.tempGP)
                pm.select(self.sel)
                print ('################### created nCloth ###################\n\n')

        return self.tgtNuc


# ---------------------------------------------------------------------------------


    def _makeClothRig(self, name = ""):    # create rootGP
        crname = pm.group(em=1, name='%s_clothRig' % name)
        return crname


    def _createSets(self, cr):    # create sets
        ### create or get 'sets' ###
        if not (pm.objExists('nClothCacheSet')):
            self.set = pm.sets(n='nClothCacheSet', em=1)
        else:
            self.set = pm.PyNode('nClothCacheSet')

        if cr:
            cr = cr.replace("_clothRig", "")
            if not (pm.objExists('%s_nClothCacheSet' % cr)):
                self.crSet = pm.sets(n='%s_nClothCacheSet' % cr, em=1)
            else:
                self.crSet = pm.PyNode('%s_nClothCacheSet' % cr)


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

    def _nConstraint(self, typ = ""):    # create nConstraint
        warn = self._warning()
        if not (warn == None):
            sel = cmds.ls(sl=True)
            list = []
            namelist = []
            constGP = []

            for loop in sel:
                obj = loop.split('.')[0]
                if obj in list:
                    continue
                else:
                    list.append(obj)

            allObj = '__'.join(list)

            if (typ == 'PS'):
                const_shape = mm.eval("createNConstraint pointToSurface 0;")[0]
            elif (typ == 'CC'):
                const_shape = mm.eval("createNConstraint pointToPoint 0;")[0]
            elif (typ == 'TF'):
                const_shape = mm.eval("createNConstraint transform 0;")[0]
            elif (typ == 'SS'):
                const_shape = mm.eval("createNConstraint slideOnSurface 0;")[0]
            elif (typ == 'WB'):
                const_shape = mm.eval("createNConstraint weldBorders 0;")[0]
            elif (typ == 'EC'):
                const_shape = mm.eval("createNConstraint collisionExclusion 0;")[0]
            elif (typ == 'FF'):
                const_shape = mm.eval("createNConstraint force 0;")[0]
            elif (typ == 'TS'):
                const_shape = mm.eval("createNConstraint tearableSurface 0;")[0]
            elif (typ == 'BC'):
                const_shape = mm.eval("createComponentNConstraint 1 0 0 1;")
            elif (typ == 'SC'):
                const_shape = mm.eval("createComponentNConstraint 1 0 0 0;")

            if (typ == 'BC' or typ == 'SC'):
                const = pm.PyNode('dynamicConstraint1'.decode('utf-8'))
            else:
                const = pm.PyNode(const_shape).getParent()

            count = self._countUp(src = '%s__%s' % (typ, allObj), type='dynamicConstraint')
            const.rename("%s__%s_%s" % (typ, allObj, count))

            ### parent const ###
            clt = pm.listHistory(list[0], type='nCloth')
            nucTgt = pm.listHistory(clt, type='nucleus')
            nuc = nucTgt[0].name()

            if (typ == 'PS'):
                if pm.objExists('%s_PS_GP' % nuc):
                    constGP = pm.PyNode('%s_PS_GP' % nuc)
            elif (typ == 'CC'):
                if pm.objExists('%s_CC_GP' % nuc):
                    constGP = pm.PyNode('%s_CC_GP' % nuc)
            else:
                if pm.objExists('%s_Other_GP' % nuc):
                    constGP = pm.PyNode('%s_Other_GP' % nuc)

            if constGP:
                pm.parent(const, constGP)
            print ('\n==== created nConstraint ==== # %s\n' % const)


    def _makeCollide(self, solver = ""):    # make collision
        warn = self._warning()
        mesh = []
        if not (warn == None):
            mesh = self._checkObj()
            if mesh:
                selCol = []
                name = solver.replace("__", "_")
                mm.eval('$gActiveNucleusNode = "%s";' % solver)

                for tgt in mesh:
                    pm.select(tgt)
                    tgtShape = pm.listRelatives(tgt, s=1, ni=1)
                    tgt.rename('%s%s_col' % (tgt, name))
                    tgtShape[0].rename('%sShape' % tgt)
                    colShape = mm.eval('makeCollideNCloth;')
                    col = pm.PyNode(colShape[0]).getParent()
                    col.rename('%s_nRigid' % tgt)
                    colShape = pm.listRelatives(col, s=1, ni=1)
                    pm.setAttr(colShape[0] + '.thickness', 0.01)
                    pm.setAttr(colShape[0]+ '.displayColor', 0, 0.735, 0.035, type='double3')
                    if (pm.objExists('%s_collisionGP' % solver)):
                        colGP = pm.PyNode('%s_collisionGP' % solver)
                        pm.parent(tgt, col, colGP)
                    selCol.append(col)
                    print ''
                    print '**** made collide **** # %s' % col
                    print ''
                pm.select(selCol)
                return selCol


    def _createField(self, typ, solver, sel):    # create field
        if not sel:
            sel = pm.selected()
        else:
            sel = pm.ls(sel)
        pm.select(cl=1)
        exType = ["airField", "dragField", "gravityField", "newtonField", "radialField",
                     "turbulenceField", "uniformField", "vortexField", "volumeAxisField", "nucleus"]
        fld = []
        name = []
        obj = []
        list = []
        typName = []
        clt = []
        cltList = []
        if sel:
            for obj in sel:
                if not (pm.objectType(obj) in exType):
                    list.append(obj.name())
                else:
                    name = solver.replace("__", "")
            if list:
                if not (len(list) > 2):
                    name = "__".join(list)
                else:
                    name = solver.replace("__", "")
        else:
            name = solver.replace("__", "")
        ### countUp ###
        count = self._countUp(src = '%s__%s' % (typ, name), type='field')
        ### select type ###
        if (typ == 'Air'):
            fld = pm.air()
            typName = 'air'
        elif (typ == 'Turbulence'):
            fld = pm.turbulence()
            typName = 'turb'
        elif (typ == 'Vortex'):
            fld = pm.vortex()
            typName = 'vortex'
        elif (typ == 'Volume Axis'):
            fld = pm.volumeAxis()
            typName = 'volAxis'
        elif (typ == 'Gravity'):
            fld = pm.gravity()
            typName = 'gravity'
        elif (typ == 'Radial'):
            fld = pm.radial()
            fld = pm.ls(fld)
            typName = 'radial'
        ### rename field ###
        if (typ == 'Radial'):
            fld[0].rename('%sField__%s_%s' % (typName, name, count))
        else:
            fld.rename('%sField__%s_%s' % (typName, name, count))
        ### assign field ###
        if sel:
            for tgt in sel:
                if not (pm.objectType(tgt) in exType):
                    clt = pm.listHistory(tgt, type='nCloth')
                    cltList.append(clt)
            if not cltList:
                clt = pm.listConnections(solver, type='nCloth')
            pm.connectDynamic(clt, f=fld)
        ### parent field ###
        if (pm.objExists('%s_fieldGP' % solver)):
            pm.parent(fld, '%s_fieldGP' % solver)

        if (typ == 'Radial'):
            print ('\n==== created field ==== # %s\n' % fld[0])
        else:
            print ('\n==== created field ==== # %s\n' % fld)


    def _countUp(self, src, type):    # countUp
        tgt = []
        for list in pm.ls(typ=type):
            if (src in str(list)):
                tgt.append(list)
        count = len(tgt) + 1
        return count


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


    def _warning(self):    # before run script
        sel = pm.selected()
        warn = []
        if not sel:
            warn = pm.warning("You must've selected the object")
        return warn


    def _checkObj(self):
        sel = pm.selected()
        mesh = []
        src = []
        for obj in sel:
            if pm.objectType(obj, i='transform'):
                try:
                    src = pm.listRelatives(obj, s=1, ni=1)
                    if pm.objectType(src, i='mesh'):
                        mesh.append(obj)
                    src = []
                except:
                    pass
        if not mesh:
            pm.warning("You must've selected the 'Polygon Mesh'")
        return mesh


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

#cn = CreateNCloth()
#cn._clothSetup(solver = "nucleus2")
#cn._makeCollide(solver = "__nucleus1")
#cn._nConstraint(typ = 'TF')
#cn._makeClothRig(name = "")
#cn._createField(typ = "Turbulence", solver = "__nucleus1")
