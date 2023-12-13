import re
import os
import tempfile

import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

import xml.etree.ElementTree as ET


def set_target(target, type):
    return pm.listRelatives(target, ni=True, ad=True, type=type) + pm.ls(target, type=type)
        

def get_target_meshes():
    sel = pm.selected()
    
    #print 'jnts', jnts
    targets = list()
    jnts = set_target(sel, 'joint')
    if len(jnts) > 0:
        pm.select(jnts)
        scs = pm.listConnections('.worldMatrix', type='skinCluster', s=False, d=True)
        pm.select(scs)
        #targets = pm.listConnections('.outputGeometry', sh=True, type='mesh', s=False, d=True)
        targets = pm.ls(pm.listHistory(future=True), type='mesh')
    
    meshes = set_target(sel, 'mesh')
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

def copy_weight():
    sel = pm.selected()

    if len(sel) != 2:
        pm.error('Select a source mesh (or joint), then a target mesh (or joint).')
        return
    pm.select(sel[0])

    dirname = tempfile.gettempdir()
    filename = os.path.join(dirname, 'copy_weight_temp.wdata')
    #print 'filename:', filename
    export_weight_cmd(filename, force=True)
    

    pm.select(sel[1])

    optname = 'Copy_Skin_Weight__matchMode'
    if cmds.optionVar(ex=optname):
        method = cmds.optionVar(q=optname)
    else:
        method = 'Closest Point'

    delhis = False
    optname = 'Copy_Skin_Weight__deleteHistory'
    if cmds.optionVar(ex=optname):
        delhis = True if cmds.optionVar(q=optname) == 'True' else False

    import_weight_cmd(filename, method=method, force=True, delete_history=delhis)
    

def export_weight():
    result = pm.fileDialog2(fileFilter='wdata Files (*.wdata)', dialogStyle=2)
    if not result:
        return
    export_weight_cmd(result[0])

def export_weight_cmd(filename, force=False):
    name = re.sub('[.][^.]*$', '', os.path.basename(filename))
    path = os.path.join(os.path.dirname(filename), name)
    if not os.path.exists(path):
        os.makedirs(path)

    targets = get_target_meshes()
    
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
    
    if not force:
        mes = 'These meshes will be processed.\n\n'
        for t in targets:
            mes += t + '\n'
        mes += '\nAre you OK?\n'
        res = pm.confirmDialog(title='Confirm', message=mes, button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
        if res != 'OK':
            return

    outfiles = list()
    for target in targets:        
        buf = pm.ls(pm.listHistory(target), type='skinCluster')

        if len(buf) == 0:
            print('Warning: skinCluster not found:%s. Skipped. ' % target)
            continue

        sc = buf[0]
        fullname = name + '_' + re.sub('[|]', '_', target.nodeName())

        pm.deformerWeights(fullname + '.xml', export=True, deformer=sc, path=path)
        outfiles.append(path + '/' + fullname + '.xml')
        '''
        mel.eval('source exportSkinMap')
        pm.select(target)
        cmd = 'exportSkinWeightMap "' + path+'/'+fullname + '" "iff"'
        print cmd
        mel.eval(cmd)
        '''
        outfiles.append(path + '/' + fullname + '.weightMap')

        # export mesh
        if not cmds.pluginInfo('objExport', q=True, l=True):
            cmds.loadPlugin('objExport')
        pm.select(target)
        objfilename = path + '/' + fullname + '.obj'
        cmds.file(objfilename, force=True, options='groups=0;ptgroups=0;materials=0;smoothing=1;normals=1', typ='OBJexport', pr=True, es=True)

        outfiles.append(objfilename)
        


    outfile = file(filename, 'w')
    outfile.write('\n'.join(outfiles))
    outfile.close()
            
def get_mesh_object(target):
    cname = target.__class__.__name__ 
    if cname == 'Mesh':
        return target
    elif cname == 'list':
        return target[0].node()
    else:
        raise Exception('')



def import_weight():
    optname = 'Import_Skin_Weight__matchMode'
    if cmds.optionVar(ex=optname):
        method = cmds.optionVar(q=optname)
    else:
        method = 'Closest Point'

    optname = 'Import_Skin_Weight__deleteHistory'
    delhis = False
    if cmds.optionVar(ex=optname):
        delhis = True if cmds.optionVar(q=optname) == 'True' else False

    res = pm.fileDialog2(fileFilter='wdata Files (*.wdata)', dialogStyle=2, fileMode=1)
    if not res:
        return

    import_weight_cmd(res[0], method=method, delete_history=delhis)


def import_weight_cmd(filename, method, delete_history=True, force=False):
    sel = pm.selected()
    targets = get_target_meshes()

    if delete_history:
        try:
            hi = pm.ls(hilite=True)
            for t in targets:
                m = get_mesh_object(t)
                tr = m.firstParent()
                for io in pm.ls(pm.listRelatives(tr, s=True, type='mesh'), io=True):
                    if pm.objExists(io):
                        io.setAttr('io', 0)
                        pm.delete(io, ch=True)
                        io.setAttr('io', 1)
            pm.select(sel)
            pm.hilite(hi)
        except:
            pm.error('Failed in deleting history:')

    name = re.sub('[.][^.]*$', '', os.path.basename(filename))
    path = os.path.join(os.path.dirname(filename), name)

    
    if len(targets) == 0:
        raise Exception('No meshes selected.')

    if not force:
        mes = 'These meshes will be processed.\n\n'
        for t in targets:
            mes += get_mesh_object(t).nodeName() + '\n'

        mes += '\nAre you OK?\n'
        res = pm.confirmDialog(title='Confirm', message=mes, button=['OK', 'Cancel'], 
                defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
        if res != 'OK':
            return
    for mesh in targets:
        import_weight_from_xml(path, name, mesh, method)


def get_root_joint(mesh):
    buf = pm.ls(pm.listHistory(mesh), type='skinCluster')
    #buf = pm.listConnections(mesh + '.inMesh', s=True, d=False, type='skinCluster')
    if len(buf) == 0:
        pm.warning('Cannot find skinCluster for %s' % mesh)
        return None

    sc = buf[0]
    jnts = pm.listConnections(sc + '.matrix', s=True, d=False, type='joint')
    sh = -1
    root = ''
    for jnt in jnts:
        v = len(jnt.longName().split('|'))
        if sh < 0 or v < sh:
            sh = v
            root = jnt
    return root

def import_weight_from_xml(path, name, target, method):
    targetMesh = get_mesh_object(target)
    joint = get_root_joint(targetMesh)
    
    if joint is None:
        return

    fullname = name + '_' + re.sub('[|]', '_', targetMesh.nodeName())

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
    if not os.path.exists(objfilename):
        pm.warning('File not exists: '+ objfilename)
        return
    xmlfilename = path + '/' + fullname + '.xml'
    if not os.path.exists(xmlfilename):
        pm.warning('File not exists: ' + xmlfilename)
        return

    cmds.file(objfilename, force=True, i=True, typ='OBJ', ignoreVersion=True, ra=True, namespace=ns, options='mo=1', pr=1)

    try:
        mesh = pm.ls('cyWldSkinWeightExport:*', type='mesh', ni=True)[0]
        meshTr = mesh.firstParent()

        pm.select(meshTr, joint)
        res = mel.eval('SmoothBindSkin')
        buf = pm.listConnections(mesh, s=True, d=False, type='skinCluster')
        sc = buf[-1]
        pm.select(meshTr)
        pm.setAttr(sc+'.normalizeWeights', 0)
        pm.skinPercent(sc, mesh, pruneWeights=100, normalize=False)

        pm.deformerWeights(os.path.basename(xmlfilename), im=True, method='index', deformer=sc, path=path)
        pm.skinCluster(sc, e=True, fnw=True)

        pm.select(meshTr)
        pm.select(target, add=True)

        if method  == 'UV':
            pm.copySkinWeights(noMirror=True, surfaceAssociation='closestPoint', influenceAssociation='closestJoint', uv=('map1', 'map1') )
        else:
            _method = 'closestPoint' if method == 'Closest Point' else  'closestComponent' if method == 'Closest Component' else None
            if not _method:
                pm.error('Invalid surface association:', method)
            else:
                pm.copySkinWeights(noMirror=True, surfaceAssociation=_method, influenceAssociation='closestJoint')
        
    except:
        print('Failed in ', target)
        pass

    finally:
        pm.delete(meshTr)
        #pass



def build_dmymesh(filename):
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




def import_weight_manual():
    mesh = pm.listRelatives(ad=True, type='mesh')[0]
    tree = ET.parse('W:/production/work/asset/character/all/default/animation/default/data/test/test_mesh_bodyShape.xml')
    root = tree.getroot()
    for ws in root.findall('weights'):
        dfm = ws.get('deformer')
        src = ws.get('source')
        #print 'deformer:', dfm
        #print 'src:', src
        pnts = ws.findall('point')
        for pnt in pnts:
            index = int(pnt.get('index'))
            value = float(pnt.get('value'))
            #print 'index:%d value=%f' % (index, value)
            pm.select('%s.vtx[%d]' % (mesh, index))
            pm.skinPercent('skinCluster11', tv=[(src, value)])
