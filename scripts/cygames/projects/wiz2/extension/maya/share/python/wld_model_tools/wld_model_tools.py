import pymel.core as pm
from . import wld_skin_weight_export as we
import re

def ui():
	wname = 'wld_model_tools'
	if pm.window(wname, q=True, ex=True):
		pm.deleteUI(wname, window=True)
	win = pm.window(wname)
	pm.columnLayout(adj=True, rs=10)
	pm.menuBarLayout()
	pm.menu(l='Help')
	pm.menuItem(l='')
	pm.setParent()

	pm.button(l='Export Skin Weight', c=pm.Callback(exportWeight), ann='Select meshes or(and) joints.')
	pm.separator(h=10)

	pm.rowLayout(nc=2, cw2=(150, 200), cat=(1, 'both',10), cl2=('right', 'left'), rat=(1, 'top', 3))
	pm.text(l='Surface Association:', al='right')	
	pm.columnLayout()
	rc = pm.radioCollection()	
	rb1 = pm.radioButton(l='Closest Point')
	rb2 = pm.radioButton(l='Closest Component')
	rb3 = pm.radioButton(l='UV')
	pm.setParent('..')
	pm.setParent('..')
	pm.radioCollection(rc, e=True, select=rb1)

	pm.button(l='Import Skin Weight', c=pm.Callback(importWeight, rc, rb1, rb2, rb3), ann='Select meshes or(and) vertices or(and) joints.')

	pm.separator(h=10)

	pm.showWindow(win)



def exportWeight():
	result = pm.fileDialog2(fileFilter='wdata Files (*.wdata)', dialogStyle=2)[0]
	print(result)
	base = re.sub('[.]wdata$', '', result)
	path = re.sub('[/][^/]*$', '', base)
	name = re.sub('.*[/]', '', base)
	print('base', base)
	print('path', path)
	print('name', name)
	if path == '' or name == '':
		raise Exception('Invalid path specified.')

	we.exportWeight(path, name)


def importWeight(rc, rb1, rb2, rb3):
	bname = pm.radioCollection(rc, q=True, select=True)
	
	rb1 = re.sub('.*[|]', '', rb1)
	rb2 = re.sub('.*[|]', '', rb2)
	rb3 = re.sub('.*[|]', '', rb3)
	
	result = pm.fileDialog2(fileFilter='wdata Files (*.wdata)', dialogStyle=2, fileMode=1)[0]
	base = re.sub('[.]wdata$', '', result)
	path = re.sub('[/][^/]*$', '', base)
	name = re.sub('.*[/]', '', base)
	if path == '' or name == '':
		raise Exception('Invalid path specified.')

	we.importWeight(path, name, method='closestPoint' if bname == rb1 else 'closestComponent' if bname == rb2 else 'uv')

