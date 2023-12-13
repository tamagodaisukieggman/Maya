#test
import pymel.core as pm

def ui():
	wname = 'wld_chr_misc_tools'
	if pm.window(wname, q=True, ex=True):
		pm.deleteUI(wname, window=True)
	pm.window(wname)
	pm.columnLayout(adj=True, rs=5)
	pm.button(l='Apply Target Dif', ann='Apply target differences to a base model.', c=pm.Callback(applyTargetDif))
	pm.button(l='Combine Parts', ann='Combine a part with every targets.', c=pm.Callback(combinePart))
	pm.button(l='Transfer Positions', 
		ann='Transfer positions of a new topology to every targets.', c=pm.Callback(transferPos))
	pm.showWindow()


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

def applyTargetDif():
	base = pm.listRelatives(ad=True, type='mesh', ni=True)[0]
	intm = pm.listRelatives(ad=True, type='mesh', ni=True)[1]
	tgt = pm.listRelatives(ad=True, type='mesh', ni=True)[2]

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
	srcs = getTypeNodes(pm.selected()[0], 'mesh')
	dsts = getTypeNodes(pm.selected()[1], 'mesh')
	for d in dsts:
		cpTr = pm.duplicate(srcs[0])
		cp = pm.listRelatives(cpTr, c=True, s=True, ni=True)[0]
		tr = d.firstParent()
		#buf = pm.listRelatives(tr, p=True)
		#gp = None
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


