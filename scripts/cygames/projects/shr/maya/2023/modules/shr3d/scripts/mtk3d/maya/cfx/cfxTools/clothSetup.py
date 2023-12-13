# -*- coding: utf-8 -*-

# ---------------------------------------------
# ======= author : yoshida_yutaka
# ======= Feb.2019
# ---------------------------------------------

import maya.api.OpenMaya as om2
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
        self.proj = []


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


    def _cleanupMeshes(self, cln, bor = 0):   # cleanup
        ### delete History ###
        tgt = pm.ls(cln)
        attrs = ['t', 'r', 's']
        axis = ['x', 'y', 'z']

        for src in tgt:
            pm.delete(src, ch=1)
            orig = self._getUnconnectedShapeOrigins(clnSrc = pm.listRelatives(src, s=1))
            pm.delete(orig)

            clnShape = pm.listRelatives(src, s=1)

            pm.polyNormalPerVertex(src, ufn=1)
            pm.polySoftEdge(src, a=180, ch=0)
            if not ('_INIT' in str(src) or '_REST' in str(src)):
                try:
                    for attr in attrs:
                        for ax in axis:
                            pm.setAttr(src+ '.'+attr+ax, l=0)
                    pm.makeIdentity(src, apply=1, t=1, r=1, s=1, n=0)
                except:
                    for i in pm.listAttr(src, l=1):
                        src.attr(i).unlock()
                    pm.makeIdentity(src, apply=1, t=1, r=1, s=1, n=0)
            pm.setAttr(src+ '.visibility', l=0)
            if bor == 1:
                pm.setAttr(clnShape[0]+ '.displayBorders', 1)
                pm.setAttr(clnShape[0]+ '.borderWidth', 4.7)
            pm.delete(src, ch=1)


    def _createSets(self, cr):    # create sets
        ### create or get 'sets' ###
        if not (pm.objExists('nClothCacheSet')):
            self.set = pm.sets(em=1, n='nClothCacheSet')
        else:
            self.set = pm.PyNode('nClothCacheSet')

        if cr:
            cr = cr.replace("_clothRigGP", "")
            if not (pm.objExists('{}_nClothCacheSet'.format(cr))):
                self.crSet = pm.sets(em=1, n='{}_nClothCacheSet'.format(cr))
            else:
                self.crSet = pm.PyNode('{}_nClothCacheSet'.format(cr))


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
            print('**** nucleus "NEW" ****')
            mm.eval('$gActiveNucleusNode = "";')
        ### exist nucleus ###
        elif nucRe:
            print('**** nucleus "exists" ****')
            mm.eval('$gActiveNucleusNode = "{}";'.format(self.solver[0]))
        ### new nucleus ###
        else:
            print('**** nucleus "NEW" **** # {}'.format(solver))
            mm.eval('$gActiveNucleusNode = "";')


    def _prepObj(self, mesh, cr):   # prepare objects
        ### create groups for clothObj ###
        self.tempGP = pm.group(em=1, n='_____tempGP')

        for obj in mesh:
            ### cleanup Object ###
            clnTgt = obj
            self._cleanupMeshes(cln = clnTgt, bor = 1)

            ### get Shape ###
            objShape = pm.listRelatives(obj, s=1, ni=1)
            ### rename originalObj ###
            if not("_CLOTH" in str(obj)):
                pm.rename(obj, '{}_CLOTH'.format(obj))
            pm.rename(objShape[0], '{}Shape'.format(obj))

            ### create INIT & REST ###
            initObj = pm.duplicate(obj, n='{}_INIT'.format(obj))
            initObjShape = pm.listRelatives(initObj, s=1, ni=1)
            pm.rename(initObjShape[0], '{}Shape'.format(initObj[0]))
            restObj = pm.duplicate(obj, n='{}_REST'.format(obj))
            restObjShape = pm.listRelatives(restObj, s=1, ni=1)
            pm.rename(restObjShape[0], '{}Shape'.format(restObj[0]))

            ### cleanup Object ###
            clnTgt = [obj, initObj, restObj]
            self._cleanupMeshes(cln = clnTgt, bor = 1)

            ### create blendShape ###
            bs = pm.blendShape(initObj, obj, o='local', n='{}_blendShape'.format(initObj[0]))[0]
            pm.setAttr(bs+ '.{}'.format(initObj[0]), 1, l=1)

            ### create skinCluster ###    clA=INIT, clB=cloth
            # clA
            clA = pm.cluster(initObj)[0]
            clAHandle = pm.PyNode(clA + 'Handle')
            clANode = pm.PyNode(clA)
            pm.rename(clAHandle, '{}_cluster'.format(initObj[0]))
            pm.rename(clANode, '{}_clusterNode'.format(initObj[0]))
            pm.setAttr(clANode+ '.envelope', l=1)
            # clB
            clB = pm.cluster(obj)[0]
            clBHandle = pm.PyNode(clB + 'Handle')
            clBNode = pm.PyNode(clB)
            pm.rename(clBHandle, '{}_cluster'.format(obj))
            pm.rename(clBNode, '{}_clusterNode'.format(obj))
            pm.hide(initObj, restObj, clBHandle)
            pm.parent(clBHandle, clAHandle)
            clAGP = pm.group(clAHandle, n='{}_cluster_space'.format(initObj[0]))

            ### parentConstraint clAGP ###
            self._parentConstCluster(clAGP=clAGP)

            self.src = pm.ls(obj)
            self.init = initObj
            self.rest = restObj

            ### create clothNode ###
            cltNode = self._createNClothNode()

            ### obj into the set ###
            mm.eval('sets -edit -forceElement  {} {} ;'.format(self.set, cltNode))
            if self.crSet:
                mm.eval('sets -edit -forceElement  {} {} ;'.format(self.crSet, cltNode))
            ### parent objects ###
            pm.parent(obj, cltNode, initObj, restObj, self.tempGP)
            ### append selectObj ###
            self.sel.append(self.src)


    def _parentConstCluster(self, clAGP):
        tgt = []
        if self.proj == 'mutsunokami':
            tgt = pm.ls('pelvis_C_001_body_jnt', r=1)

        if tgt:
            pm.parentConstraint(tgt, clAGP, mo=1)


    def _createNClothNode(self):    # apply nCloth
        cltNode = []
        cltObj = pm.ls(self.src)[0]
        initObj = pm.ls(self.init)[0]
        restObj = pm.ls(self.rest)[0]

        ### convert to nCloth ###
        pm.select(self.src)
        mm.eval('createNCloth 0;')

        ### rename clothNode ###
        cltNodeShape = pm.listHistory(cltObj, type='nCloth')
        cltShape = pm.listRelatives(cltObj, s=1, ni=1)
        cltNode = cltNodeShape[0].getParent()
        pm.rename(cltNode, "{}_node".format(cltObj))
        pm.rename(cltShape[0], "{}_outputCloth".format(cltObj))

        ### lockAttr clothOrig ###
        pm.setAttr(cltObj+ '.translate', l=1)
        pm.setAttr(cltObj+ '.rotate', l=1)
        pm.setAttr(cltObj+ '.scale', l=1)
        ### lockAttr clothINIT ###
        pm.setAttr(initObj+ '.translate', l=1)
        pm.setAttr(initObj+ '.rotate', l=1)
        pm.setAttr(initObj+ '.scale', l=1)
        ### lockAttr clothREST ###
        pm.setAttr(restObj+ '.translate', l=1)
        pm.setAttr(restObj+ '.rotate', l=1)
        pm.setAttr(restObj+ '.scale', l=1)

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

        print('------------------------------------------------------')
        print('==== added clothNode ==== # {}'.format(cltNode))
        return cltNode


    def _editClothAndNucleus(self):    # assign&rename nucleus
        nuc = pm.ls(typ='nucleus')
        tgtName = []
        print('------------------------------------------------------')
        print('******\n')

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
                            mm.eval('assignNSolver "{}";'.format(self.selSolver))
                            self.tgtNuc = pm.listHistory(clt, type='nucleus')[0]
                            self._editClothAndNucleusElse(loop, cltNode)
                            delTgt = pm.listConnections(delNuc, type='nCloth')
                            if (delTgt == []):
                                pm.delete(delNuc)

                    if not (pm.objExists(self.selSolver)):
                        ### rename nucleus ###
                        self.tgtNuc.rename('{}'.format(self.selSolver))
                        print('--------------------------------------------------')
                        print("---- assign NewSolver ---- # '{}' >> '{}'".format(self.tgtNuc, cltNode))
                        print('--------------------------------------------------')
                        self._nucleusSetAttributes(loop)
                ### newSolver rename by default ###
                else:
                    if not (tgtName == self.tgtNuc):
                        count = self._countUp(src = '__nucleus', type='nucleus')
                        self.tgtNuc.rename('__nucleus' + count)
                        tgtName = self.tgtNuc
                        print('--------------------------------------------------')
                        print("---- assign NewSolver ---- # '{}' >> '{}'".format(self.tgtNuc, cltNode))
                        print('--------------------------------------------------')
                        self._nucleusSetAttributes(loop)
                    else:
                        self._editClothAndNucleusElse(loop, cltNode)
            else:
                self._editClothAndNucleusElse(loop, cltNode)

            print('\n== Done == {}\n\n'.format(loop[0]))


    def _editClothAndNucleusElse(self, loop, cltNode):    # assign&rename nucleus else
        print('--------------------------------------------------')
        print("---- assign ExistSolver ---- # '{}' >> '{}'".format(self.tgtNuc, cltNode))
        print('--------------------------------------------------')
        initCl = pm.PyNode('{}_INIT_cluster_space'.format(loop[0]))
        initGP = pm.PyNode('{}_INIT_clusterGP'.format(self.tgtNuc))
        self.nucGP = pm.PyNode('{}_GP'.format(self.tgtNuc))
        defGP = pm.PyNode('{}_deformerGP'.format(self.tgtNuc))
        fieldGP = pm.PyNode('{}_fieldGP'.format(self.tgtNuc))
        clothObj = self.tempGP.getChildren()
        pm.parent(defGP, fieldGP, w=1)
        pm.parent(clothObj, defGP, fieldGP, self.nucGP)
        pm.parent(initCl, initGP)
        print("**** parent object **** # '{}' >> '{}_GP'".format(loop[0], self.tgtNuc))
        print('--------------------------------------------------')


    def _nucleusSetAttributes(self, loop):    # setAttr nucleus
        ### setAttr nucleus ###
        pm.expression(s='{}.startFrame = `playbackOptions -q -min`'.format(self.tgtNuc))
        pm.setAttr(self.tgtNuc+ '.airDensity', 1)
        pm.setAttr(self.tgtNuc+ '.subSteps', 15)
        pm.setAttr(self.tgtNuc+ '.spaceScale', 0.01)
        ### create groups ###
        self._makeHierarchy(loop)


    def _makeHierarchy(self, loop):   # create groups
        initCl = pm.PyNode('{}_INIT_cluster_space'.format(loop[0]))
        initGP = pm.group(initCl, n='{}_INIT_clusterGP'.format(self.tgtNuc))
        colGP = pm.group(em=1, n='{}_collisionGP'.format(self.tgtNuc))
        constPSGP = pm.group(em=1, n='{}_PS_GP'.format(self.tgtNuc))
        constCCGP = pm.group(em=1, n='{}_CC_GP'.format(self.tgtNuc))
        constOtherGP = pm.group(em=1, n='{}_Other_GP'.format(self.tgtNuc))
        constGP = pm.group(constPSGP, constCCGP, constOtherGP, n='{}_constraintGP'.format(self.tgtNuc))
        clothObj = self.tempGP.getChildren()
        defGP = pm.group(em=1, n='{}_deformerGP'.format(self.tgtNuc))
        fieldGP = pm.group(em=1, n='{}_fieldGP'.format(self.tgtNuc))
        self.nucGP = pm.group(self.tgtNuc, initGP, colGP, constGP, clothObj, defGP, fieldGP,  n='{}_GP' .format(self.tgtNuc))
        pm.hide(initGP)
        print('++++ created groups ++++ # {}_GP'.format(self.tgtNuc))
        print('--------------------------------------------------')
        print("**** parent object **** # '{}' >> '{}_GP'".format(loop[0], self.tgtNuc))
        print('--------------------------------------------------')


    def _addConnectAttribute(self):    # add&connect Attributes
        for obj in self.sel:
            if not (pm.attributeQuery('enableINIT', n=obj[0], ex=1)):
                pm.addAttr(obj, ln='clothLocalSetting', at='enum', en='=======', k=1)
                pm.addAttr(obj, ln='enableINIT', at='bool', k=1)
            else:
                pm.setAttr(obj[0]+ '.enableINIT', 0)
            pm.setAttr(obj[0]+ '.clothLocalSetting', l=1)
            rev = pm.createNode('reverse', n='{}_cluster_reverse'.format(obj[0]))
            pm.setAttr(rev+ '.inputY', l=1)
            pm.setAttr(rev+ '.inputZ', l=1)
            pm.PyNode(obj[0]).enableINIT >> pm.PyNode(rev).inputX
            pm.PyNode(rev).outputX >> pm.PyNode('{}_clusterNode'.format(obj[0])).envelope
            pm.PyNode(obj[0]).enableINIT >> pm.PyNode('{}_INIT_blendShape'.format(obj[0])).envelope


    def _getClothRig(self, cr):
        if cr:
            crClt = cr.replace("_clothRigGP", "_clothGP")
            pm.parent(self.nucGP, crClt)


    def _clothSetup(self, cr = "", solver = "", proj = ""):   # main
        warn = self._warning()
        mesh = []
        if not (warn == None):
            mesh = self._checkObj()
            if mesh:
                print('\n\n######################################################\n')
                self.proj = proj
                self._createSets(cr)
                self._assignSolver(solver)
                self._prepObj(mesh, cr)
                self._editClothAndNucleus()
                self._addConnectAttribute()
                self._getClothRig(cr)
                pm.delete(self.tempGP)
                pm.select(self.sel)
                print('################### created nCloth ###################\n\n')

        return self.tgtNuc


# ---------------------------------------------------------------------------------


    def _makeClothRig(self, name = ""):    # create rootGP
        crCam = pm.group(em=1, n='{}_cameraGP'.format(name))
        crIn = pm.group(em=1, n='{}_inputGP'.format(name))
        crClt = pm.group(em=1, n='{}_clothGP'.format(name))
        crOut = pm.group(em=1, n='{}_outputGP'.format(name))
        crname = pm.group(crCam, crIn, crClt, crOut, n='{}_clothRigGP'.format(name))
        pm.select(cl=1)
        return crname


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
            cltShape = []
            nucTgt = []

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

            count = self._countUp(src = '{}__{}'.format(typ, allObj), type='dynamicConstraint')
            pm.rename(const, "{}__{}_{}".format(typ, allObj, count))

            ### parent nConstraint into the group ###
            clt = pm.listRelatives(list[0], s=1, ni=1)
            cltShape = pm.listConnections(clt, type='nCloth')
            if not cltShape:
                cltShape = pm.listConnections(clt, type='nRigid')
            nucTgt = pm.listHistory(cltShape, type='nucleus')
            nuc = nucTgt[0].name()

            if (typ == 'PS' or typ == 'CC'):
                if pm.objExists('{}_{}_GP'.format(nuc, typ)):
                    constGP = pm.PyNode('{}_{}_GP'.format(nuc, typ))
            else:
                if pm.objExists('{}_Other_GP'.format(nuc)):
                    constGP = pm.PyNode('{}_Other_GP'.format(nuc))

            if constGP:
                pm.parent(const, constGP)

            print('\n==== created nConstraint ==== # {}\n'.format(const))


    def _makeCollide(self, solver = ""):    # make collision
        warn = self._warning()
        mesh = []
        if not (warn == None):
            mesh = self._checkObj()
            if mesh:
                selCol = []
                name = solver.replace("__", "_")
                mm.eval('$gActiveNucleusNode = "{}";'.format(solver))

                for tgt in mesh:
                    ### cleanup ###
                    clnTgt = tgt
                    self._cleanupMeshes(cln = clnTgt, bor = 0)

                    pm.rename(tgt, '{}{}_col'.format(tgt, name))
                    tgtShape = pm.listRelatives(tgt, s=1, ni=1)
                    pm.rename(tgtShape[0], '{}Shape'.format(tgt))

                    pm.select(tgt)
                    colShape = mm.eval('makeCollideNCloth;')

                    col = pm.PyNode(colShape[0]).getParent()
                    pm.rename(col, '{}_nRigid'.format(tgt))
                    colShape = pm.listRelatives(col, s=1, ni=1)
                    pm.setAttr(colShape[0] + '.thickness', 0.01)
                    pm.setAttr(colShape[0]+ '.displayColor', 0, 0.735, 0.035, type='double3')
                    if (pm.objExists('{}_collisionGP'.format(solver))):
                        colGP = pm.PyNode('{}_collisionGP'.format(solver))
                        pm.parent(tgt, col, colGP)
                    selCol.append(col)

                    print('\n**** made collide **** # {}\n'.format(col))

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
        count = self._countUp(src = '{}__{}'.format(typ, name), type='field')
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
            pm.rename(fld[0], '{}Field__{}_{}'.format(typName, name, count))
        else:
            pm.rename(fld, '{}Field__{}_{}'.format(typName, name, count))
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
        if (pm.objExists('{}_fieldGP'.format(solver))):
            pm.parent(fld, '{}_fieldGP'.format(solver))

        if (typ == 'Radial'):
            print('\n==== created field ==== # {}\n'.format(fld[0]))
        else:
            print('\n==== created field ==== # {}\n'.format(fld))


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


    def _countUp(self, src, type):    # countUp
        tgt = []
        count = []
        for list in pm.ls(typ=type):
            if (src in str(list)):
                tgt.append(list)
        if type == 'nucleus':
            count = str(len(tgt) + 1)
        else:
            count = str(len(tgt) + 1).zfill(2)
        return count


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

    # before run script

    def _warning(self):
        sel = pm.selected()
        warn = []
        if not sel:
            warn = pm.warning("You must've selected the object(s)")
        return warn


    def _checkObj(self):
        sel = pm.selected()
        mesh = []
        for obj in sel:
            if pm.objectType(obj, i='transform'):
                src = pm.listRelatives(obj, s=1, ni=1) or []
                if src and pm.objectType(src, i='mesh'):
                    mesh.append(obj)
                    
            elif pm.objectType(obj, i='mesh'):
                trans = obj.getParent()
                mesh.append(trans)

        if not mesh:
            pm.warning("You must've selected the 'Polygon Object(s)'")
        return mesh


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

#cn = CreateNCloth()
#cn._clothSetup(solver = "nucleus2")
#cn._makeCollide(solver = "__nucleus1")
#cn._nConstraint(typ = 'TF')
#cn._makeClothRig(name = "")
#cn._createField(typ = "Turbulence", solver = "__nucleus1")
