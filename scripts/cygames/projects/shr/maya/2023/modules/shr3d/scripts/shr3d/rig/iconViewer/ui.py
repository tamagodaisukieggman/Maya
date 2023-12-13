# -*- coding: utf-8 -*-
from __future__ import absolute_import

# -- import modules
import pymel.core as pm
import maya.cmds as mc
from functools import partial
import subprocess
import webbrowser


def show_mayaHelp(self, *args):
    mayaHelp_url = r'https://help.autodesk.com/view/MAYAUL/2019/JPN/'
    webbrowser.open_new_tab(mayaHelp_url)


def show_toolHelp(self, *args):
    toolHelp_url = r'https://wisdom.cygames.jp/display/tsubasa/%5BMaya%5D+Icon+Viewer'
    webbrowser.open_new_tab(toolHelp_url)


def copy2clip(*args, **argvs):
    txt = mc.textField('txF2', tx=True, q=True)
    cmd = 'echo ' + txt.strip()+'|clip'
    print ('"{0}" was copied to clipboard.\n'.format(txt),)
    return subprocess.check_call(cmd, shell=True)


def copy2clip_addPrefix(*args, **argvs):
    pre = args[0]
    txt = '{0}{1}'.format(pre, mc.textField('txF2', tx=True, q=True))
    cmd = 'echo ' + txt.strip()+'|clip'
    print ('"{0}" was copied to clipboard.\n'.format(txt))
    return subprocess.check_call(cmd, shell=True)


# -- icon Change
def iconChange(*args, **argvs):
    mc.nodeIconButton('nib1', i=args[0], e=True)
    mc.textField('txF2', tx=args[0], e=True)
    print ('{0}\n'.format(args[0]))

# -- resize UI
def resizeUI(*args, **argvs):
    iconSize = mc.gridLayout('grL', cw=True, q=True)
    row    = mc.scrollLayout('scL_base', w=True, q=True) / iconSize
    offset = mc.scrollLayout('scL_base', w=True, q=True) % iconSize
    if offset > 15:
        mc.gridLayout('grL', nc=row, e=True)
    else:
        mc.gridLayout('grL', nc=row-1, e=True)

# -- resize Thumbnail
def resizeThumbnail(*args, **argvs):
    val = args[0]
    mc.gridLayout('grL', cwh=(val, val), e=True)
    for icon in mc.gridLayout('grL', ca=True, q=True):
        if icon:
            mc.nodeIconButton(icon, w=val, h=val, e=True)
    # -- resize
    row = mc.scrollLayout('scL_base', w=True, q=True) / val
    mc.gridLayout('grL', nc=row, e=True)

# -- get Icons
def getIcons(*args, **argvs):
    # -- progress bar visible
    mc.progressBar('pgb1', vis=True, e=True)
    # -- get UI info
    text = mc.textField('txF1', tx=True, q=True)
    size = mc.gridLayout('grL', cw=True, q=True)
    # -- edit UI
    mc.deleteUI(mc.gridLayout('grL', ca=True, q=True), ctl=True)
    iconList = [target for target in mc.resourceManager(nf='*{0}*'.format(text))]
    # -- progress bar max value
    mc.progressBar('pgb1', max=len(iconList), e=True)
    # -- loop of icon creation
    for icon in iconList:
        mc.nodeIconButton(icon.split('.')[0],
                          i=icon,
                          w=size,
                          h=size,
                          st='iconOnly',
                          p='grL',
                          c=partial(iconChange, icon))
        mc.progressBar('pgb1', s=1, e=True)
    mc.progressBar('pgb1', vis=False, e=True)
    mc.text('txt1', l='{0} icons'.format(len(iconList)), e=True)

def iV_resetUI(*args, **argvs): 
    mc.textField('txF1', tx='', e=True)
    getIcons()
    resizeThumbnail(32)

def iV_deleteUI(*args, **argvs):  
    mc.deleteUI('iconViewerUI', wnd=True)

# ----------------------------------------------------------------------
# -- icon viewer main ui
# ----------------------------------------------------------------------
def iconViewerUI():
    # -- log
    ver = '0.7.0'
    log = ''
    iconList = mc.resourceManager(nf='*')
    row = 40
    # -- ui

    windowName = mc.window('iconViewerUI',
                           t='Icon Viewer {0}'.format(ver),
                           mb=True)
    mc.menu(l='UI', to=False )
    mc.menuItem(l='Reset UI', c=partial(iV_resetUI))
    mc.menuItem(d=True)
    #mc.menuItem(l='Hide UI', c='mc.window("iconViewerUI", vis=False, e=True)')
    mc.menuItem(l='Quit UI', c=partial(iV_deleteUI))
    mc.menu(l='Edit', to=False )
    mc.menuItem(sm=True, l='icon size')
    mc.radioMenuItemCollection('rdC')
    mc.menuItem(l='Small', rb=False, c=partial(resizeThumbnail, 16))
    mc.menuItem(l='Medium', rb=False, c=partial(resizeThumbnail, 24))
    mc.menuItem(l='Large', rb=True,  c=partial(resizeThumbnail, 32))
    mc.menuItem(l='Extra Large', rb=False, c=partial(resizeThumbnail, 48))
    # -- menu
    pm.menu(l='Help', hm=True)
    pm.menuItem(l='Maya 2019 HELP', c=partial(show_mayaHelp))
    pm.menuItem(d=True)
    pm.menuItem(l='Tool HELP', c=partial(show_toolHelp))
    mc.setParent('..', m=True )

    # -- layout
    mc.formLayout('fmL_init')
    mc.separator('sep1')
    mc.nodeIconButton('nib1', i='commandButton.png')
    mc.textField('txF1', tx='', ec=partial(getIcons))
    mc.button('btn1', l='Search', c=partial(getIcons))
    mc.textField('txF2', tx='commandButton.png', ed=False)
    mc.button('btn2', l='Copy', c=partial(copy2clip))
    mc.button('btn3', l='+:/', c=partial(copy2clip_addPrefix, ':/'))
    mc.text('txt1', l='{0} icons'.format(len(iconList)))
    mc.progressBar('pgb1')
    mc.separator('sep2')
    mc.scrollLayout('scL_base', pe=True, rc=partial(resizeUI))
    mc.gridLayout('grL', nc=10, cwh=(32, 32), ag=True)
    for icon in iconList:
        if len(icon.split('.')) >= 2:
            mc.nodeIconButton(icon.split('.')[0], i=icon, w=32, h=32, st='iconOnly', c=partial(iconChange, icon))

    # -- style
    mc.formLayout('fmL_init', w=208, e=True)
    mc.nodeIconButton('nib1', w=64, h=64, bgc=[0.15, 0.15, 0.15], e=True)
    mc.textField('txF1', bgc=[0.15, 0.15, 0.15], h=22, e=True)
    mc.button('btn1', w=80, h=20, e=True)
    mc.textField('txF2', ed=False, bgc=[0.15, 0.15, 0.15], e=True)
    mc.button('btn2', w=50, h=20, e=True)
    mc.button('btn3', w=28, h=20, e=True)
    mc.text('txt1', al='left', e=True)
    mc.progressBar('pgb1', w=80, h=16, vis=False, e=True)
    mc.scrollLayout('scL_base', bgc=[0.15, 0.15, 0.15], e=True)

    # -- edit UI
    mc.formLayout('fmL_init', e=True,
        af = [('sep1', 'top', 0), ('sep1', 'right', 0), ('sep1', 'left', 0),
              ('nib1', 'top', 10), ('nib1', 'left', 6),
              ('txF1', 'top', 10), ('txF1', 'right', 93),
              ('btn1', 'top', 11), ('btn1', 'right', 7),
              ('txF2', 'top', 35), ('txF2', 'right', 93),
              ('btn2', 'top', 35), ('btn2', 'right', 37),
              ('btn3', 'top', 35), ('btn3', 'right', 7),
              ('txt1', 'top', 60), ('txt1', 'right', 93),
              ('pgb1', 'top', 60), ('pgb1', 'right', 7),
              ('sep2', 'top', 79), ('sep2', 'right', 0), ('sep2', 'left', 0),
              ('scL_base', 'top', 80),  ('scL_base', 'right', 0), ('scL_base', 'left', 0), ('scL_base', 'bottom', 0),
              ],
        ac = [('txF1', 'left',  5, 'nib1'),
              ('txF2', 'left',  5, 'nib1'),
              ('txt1', 'left', 10, 'nib1')],
        )
    mc.showWindow()


# -- run
def showUI():
    if mc.window('iconViewerUI', ex=True) == False:
        iconViewerUI()
    else:
        mc.showWindow('iconViewerUI')
