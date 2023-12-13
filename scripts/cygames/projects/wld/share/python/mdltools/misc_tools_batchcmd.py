import pymel.core as pm
import apiutils


def combinePart():
	part = pm.selected()[0]
	targets = getTypeNodes(pm.selected()[1], 'mesh')
	for t in targets:
		lct = pm.spaceLocator(name='PlaceHolder')
		tr = t.firstParent()
		buf = tr.listRelatives(p=True)
		if len(buf) > 0:
			pm.parent(lct, buf[0])

		_part = pm.duplicate(part)[0]
		_t = pm.duplicate(t)[0]

		pm.select(_part)
		pm.select(_t, add=True)
		pm.polyUnite(ch=False, mergeUVSets=True, centerPivot=True)
		cpTop = pm.selected()[0]
		newsh = pm.listRelatives(cpTop, c=True, s=True)[0]
		#pm.parent(pm.selected(), pr)
		pm.parent(newsh, tr, add=True, s=True)
		orgname = t.nodeName()
		pm.rename(t, t.nodeName() + '_')
		pm.rename(newsh, orgname)
		pm.delete(lct)
		pm.parent(t, rm=True, s=True)
		pm.delete(cpTop)

def getpos(node, idx):
	return pm.xform(node+ '.vtx[%d]' % idx, q=True, t=True)

def applyTargetDif(copy=False):
	sel = pm.selected()
	base = apiutils.get_typenodes(types='mesh', target=sel[0])[0]
	tgt = apiutils.get_typenodes(types='mesh', target=sel[2])[0]
	if copy:
		copy_t = pm.duplicate(base, n='%s_%s' % (base.firstParent().nodeName(), tgt.firstParent().nodeName()))
		base = pm.listRelatives(copy_t, c=True, s=True, ni=True)[0]
	intm = apiutils.get_typenodes(types='mesh', target=sel[1])[0]
	

	for idx in range(pm.polyEvaluate(base, v=True)):
		pt = getpos(tgt, idx)
		pi = getpos(intm, idx)
		dif = [x[0]-x[1] for x in zip(pt, pi)]
		pb = getpos(base, idx)
		res = [x[0]+x[1] for x in zip(pb, dif)]
		pm.xform(base+'.vtx[%d]' % idx, t=res) 

def getTypeNodes(nodes, nodeType):
	res = pm.listRelatives(nodes, ad=True, ni=True, s=True, type=nodeType) + pm.ls(nodes, type=nodeType)
	return res

def transferPos():
	src = pm.selected()[0]
	d = pm.selected()[1]

	cpTr = pm.duplicate(src)
	cp = pm.listRelatives(cpTr, c=True, s=True, ni=True)[0]
	tr = d.firstParent()
	pm.parent(cp, tr, s=True, add=True)
	name = d.nodeName()
	pm.rename(d, 'tmp')
	pm.rename(cp, name)
	pm.delete(cpTr)

	pm.select(d)
	pm.select(cp, add=True)
	pm.transferAttributes(transferPositions=True, transferNormals=False, 
		transferUVs=False, transferColors=False,
		sampleSpace=3, searchMethod=3, flipUVs=False)
	pm.delete(cp, ch=True)
	pm.delete(d)


