from maya import cmds
import pymel.core as pm
import re

def get_tmp_namespace():
    nsbase = 'custom_locator_%d'
    i = 1
    while True:
        ns = nsbase % i
        if cmds.namespace(ex=ns):
            i += 1
        else:
            return ns
            
def create_locator(filepath):
    ns = get_tmp_namespace()

    refs = pm.ls(type='reference')
    cmds.file(filepath, ns=ns, r=True, f=True)
    newrefs = pm.ls(type='reference')
    newref = list(set(refs).symmetric_difference(set(newrefs)))[0]

    cmds.file(ir=True, rfn=newref.name())

    res = []
    for n in pm.ls(ns+':*'):
        base = re.sub('.*[:]', '', n.name())
        _res = cmds.rename(n.name(), base)
        if pm.objectType(n) == 'curveLocator':
            res.append(_res)

    cmds.namespace(rm=ns)

    return res