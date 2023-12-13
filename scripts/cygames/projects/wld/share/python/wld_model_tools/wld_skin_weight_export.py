import pymel.core as pm
import re
import os
import maya.cmds as cmds
import maya.mel as mel
import xml.etree.ElementTree as ET

def setTarget(target, type):
    return pm.listRelatives(target, ni=True, ad=True, type=type) + pm.ls(target, type=type)
        

def getTargetMeshes():
    sel = pm.selected()
    
    #print 'jnts', jnts
    targets = list()
    jnts = setTarget(sel, 'joint')
    if len(jnts) > 0:
        pm.select(jnts)
        scs = pm.listConnections('.worldMatrix', type='skinCluster', s=False, d=True)
        #print 'skinClusters', scs
        pm.select(scs)
        targets = pm.listConnections('.outputGeometry', sh=True, type='mesh', s=False, d=True)
    
    meshes = setTarget(sel, 'mesh')
    if len(meshes) > 0:
        targets += meshes

    targets = list(set(targets))


    buf = []
    verts = [x for x in sel if x.__class__.__name__ == 'MeshVertex']
    if len(verts) > 0:
        nodes = list()
        for n in verts:
            if n.node() not in nodes:
                nodes.append(n.node())
        for n in nodes:
            buf2 = [x for x in verts if x.node() == n]
            if len(buf2) > 0:
                buf.append(buf2)
    
    targets += buf
    
    return targets

def exportWeight(path, name):
    targets = getTargetMeshes()
    
    if len(targets) == 0:
        raise Exception('No meshes selected.')
    listtest = [x for x in targets if x.__class__.__name__ == 'list']
    if len(listtest) > 0:
        raise Exception('Select meshes or(and) joints.')

    nodes = dict()
    dup = False
    for n in targets:
        nodeName = n.nodeName()
        if nodeName in list(nodes.keys()):
            nodes[nodeName].append(n.shortName())
            dup = True
        else:
            nodes[nodeName] = [n.shortName()]
    if dup:
        for k in list(nodes.keys()):
            if len(nodes[k]) > 0:
                print(k)
                for n in nodes[k]:
                    print('\t', n)
        pm.error('Some node names above not unique.')
        return
    
    mes = 'These meshes will be processed.\n\n'
    for t in targets:
        mes += t + '\n'
    mes += '\nAre you OK?\n'
    res = pm.confirmDialog(title='Confirm', message=mes, button='OK', defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')

    if res == 'OK':
        outfiles = list()
        for target in targets:        
            print(target)
            buf = pm.listConnections(target, s=True, d=False, type='skinCluster')
            if len(buf) == 0:
                raise Exception('skinCluster not found.')
            sc = buf[0]
            print(sc)
            fullname = name + '_' + re.sub('[|]', '_', target.nodeName())

            pm.deformerWeights(fullname + '.xml', export=True, deformer=sc, path=path)
            outfiles.append(path + '/' + fullname + '.xml')

            mel.eval('source exportSkinMap')
            pm.select(target)
            cmd = 'exportSkinWeightMap "' + path+'/'+fullname + '" "iff"'
            print(cmd)
            mel.eval(cmd)

            outfiles.append(path + '/' + fullname + '.weightMap')

            # export mesh
            pm.select(target)
            objfilename = path + '/' + fullname + '.obj'
            cmds.file(objfilename, force=True, options='groups=0;ptgroups=0;materials=0;smoothing=1;normals=1', typ='OBJexport', pr=True, es=True)

            outfiles.append(objfilename)
            


        outfile = file(path + '/' + name + '.wdata', 'w')
        outfile.write('\n'.join(outfiles))
        outfile.close()
            
def getMeshObject(target):
    cname = target.__class__.__name__ 
    if cname == 'Mesh':
        return target
    elif cname == 'list':
        return target[0].node()
    else:
        raise Exception('')

def importWeight(path, name, method, target=None):
    targets = getTargetMeshes()

    if len(targets) == 0:
        raise Exception('No meshes selected.')
    mes = 'These meshes will be processed.\n\n'
    for t in targets:
        mes += getMeshObject(t).nodeName() + '\n'

    mes += '\nAre you OK?\n'
    res = pm.confirmDialog(title='Confirm', message=mes, button='OK', defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')


    if res == 'OK':
        for mesh in targets:
            #if method == 'closestPoint' or 'closestComponent':
            #    importWeightFromXML(path, name, mesh, method)
            #elif method == 'uv':
            #    importWeightFromMap(jnt)
            #else:
            #    raise Exception('Invalid method option.')
            importWeightFromXML(path, name, mesh, method)


def getRootJoint(mesh):
    sc = pm.listConnections(mesh + '.inMesh', s=True, d=False, type='skinCluster')[0]
    jnts = pm.listConnections(sc + '.matrix', s=True, d=False, type='joint')
    sh = -1
    root = ''
    for jnt in jnts:
        v = len(jnt.longName().split('|'))
        if sh < 0 or v < sh:
            sh = v
            root = jnt
    return root

def importWeightFromXML(path, name, target, method):
    targetMesh = getMeshObject(target)

    print('importWeightFromXML:', targetMesh)

    joint = getRootJoint(targetMesh)

    fullname = name + '_' + re.sub('[|]', '_', targetMesh.nodeName())
    print('fullname:', fullname)
    filename = path + '/' + fullname + '.xml'

    #remove existing namespace.
    ns = 'cyWldSkinWeightExport'
    if pm.namespace(ex=ns):
        try:
            if len(pm.ls(ns + ':*')) > 0:
                pm.delete(ns + ':*')
            pm.namespace(rm=ns)
        except:
            raise Exception('Cannot remove namespace: ' + ns)

    objfilename = path + '/' + fullname + '.obj'
    print('objfilename:', objfilename)
    if not os.path.exists(objfilename):
        raise Exception('File not exists: ' + objfilename)

    cmds.file(objfilename, force=True, i=True, typ='OBJ', ignoreVersion=True, ra=True, namespace=ns, options='mo=1', pr=1)

    mesh = pm.ls('cyWldSkinWeightExport:*', type='mesh', ni=True)[0]
    meshTr = mesh.firstParent()

    try:
        pm.select(meshTr, joint)
        res = mel.eval('SmoothBindSkin')
        buf = pm.listConnections(mesh, s=True, d=False, type='skinCluster')
        sc = buf[-1]
        print('skinCluster:', sc)
        pm.select(meshTr)
        #return
        #mel.eval('newCluster "-envelope 1"')
        #pm.delete()
        #pm.select(meshTr)
        print('fullname:', fullname)
        print('path:', path)
        pm.deformerWeights(fullname + '.xml', im=True, method='index', deformer=sc, path=path)
        pm.skinCluster(sc, e=True, fnw=True)

        pm.select(meshTr)
        #pm.select(targetMesh, add=True)
        pm.select(target, add=True)

        if method  == 'uv':
            pm.copySkinWeights(noMirror=True, surfaceAssociation='closestPoint', influenceAssociation='closestJoint', uv=('map1', 'map1') )
        else:
            pm.copySkinWeights(noMirror=True, surfaceAssociation=method, influenceAssociation='closestJoint')
        print('method:', method)
        
    except:
        print('Failed in ', target)
        pass

    finally:
        pm.delete(meshTr)



def importWeightFromMap(target):
    pass

def buildDmyMesh(filename):
    print('buildDmy')
    tree = ET.parse(filename)
    root = tree.getroot()
    shape = root[1]
    buf = []
    for pnt in shape:
        st = pnt.get('value')
        tok = st.split()

        buf.append((float(tok[0]), float(tok[1]), float(tok[2])))
    print(buf)        
    res = pm.polyCreateFacet(p=buf, ch=False)
    return res[0]





