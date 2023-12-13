# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pymel.core as pm
import maya.cmds as mc


def ishex(v):
    try:
        int(v, 16)
        return True
    except ValueError:
        return False


#-------------------------------------------------------------------------------
#-- Name -----------------------------------------------------------------------
def SearchAndReplace(src='', tgt=''):
    log = '------------------- Search & Replace ----------------------------\n'
    for i in pm.selected():
        try:
            old = i.name()
            new = i.name().replace(src, tgt)
            i.rename(new)
            log += 'Search & Replace    : {0} -> {1}\n'.format(old, new)
        except:
            log += '{0} can\'t rename.\n'.format(i.name())
    print(log)
    return log


def addPrefix(pre=''):
    log = '------------------- Add Prefix -----------------------------------\n'
    for i in pm.selected():
        nam = i.name()
        org = i.longName().split('|')[-1]
        print(org)
        i.rename('{0}{1}'.format(pre, org))
        log += 'Add Prefix          : {0} -> {1}\n'.format(nam, i.name())
    print(log)
    return log


def addSuffix(suf=''):
    log = '------------------- Add Suffix -----------------------------------\n'
    for i in pm.selected():
        nam = i.name()
        org = i.longName().split('|')[-1]
        print(org)
        i.rename('{0}{1}'.format(org, suf))
        log += 'Add Suffix          : {0} -> {1}\n'.format(nam, i.name())
    print(log)
    return log


def countAndRename(nn='', st=0, sp=1):
    log = '------------------- Count & Rename : Base 10 ---------------------\n'
    selObj = pm.selected()
    #-- step
    if sp == 0:
        sp = 1

    #-- Rename
    if not nn == '':
        #-- digit
        if '#' in nn:
            digit = nn.rfind('#') - nn.find('#') + 1
        else:
            digit = 1

        for i, num in zip(selObj, range(st, len(selObj)*sp+st, sp)):
            org = i.name()
            i.rename(nn.replace('#'*digit, '{0:0>{1}}'.format(num, digit)))
            log += 'Rename              : {0} -> {1}\n'.format(org, i.name())
    else:
        mc.warning('please fill in new name in the Rename field.')
    print(log)
    return log


def countAndRenameHex(nn='', st='0', sp=1):
    log = '------------------- Count & Rename : Base 16 ---------------------\n'
    selObj = pm.selected()
    #-- step
    if sp == 0:
        sp = 1
    #-- Start
    if not st:
        stv = int('0', 16)
    else:
        stv = int(st, 16)
    print(st, stv)

    #-- Rename
    if not nn == '':
        #-- digit
        if '#' in nn:
            digit = nn.rfind('#') - nn.find('#') + 1
        else:
            digit = 1

        for i, num in zip(selObj, range(stv, len(selObj)*sp+stv, sp)):
            org = i.name()
            i.rename(nn.replace('#'*digit, '{0:0>{1}x}'.format(num, digit)))
            log += 'Rename              : {0} -> {1}\n'.format(org, i.name())
    else:
        mc.warning('please fill in new name in the Rename field.')
    print(log)
    return log


#-------------------------------------------------------------------------------
#-- Joint ----------------------------------------------------------------------
def checkJointName(j='_000'):
    if len(j) == 4 and j[0] == '_':
        if ishex(j[1:4]):
            return True
        else:
            return False
    else:
        return False


def jointCount():
    log = '------------------- Joint Count ---------------------------------\n'
    jt = pm.ls('null', dag=True, typ='joint')
    al = [i for i in jt if not 'del' in i.name() and not 'null' == i.name()]
    nl = [i for i in jt if 'null' == i.name()]
    dl = [i for i in jt if 'del' == i.name()[:3]]
    iv = [i for i in al if not checkJointName(i.name())]
    print(iv)

    j0 = [i for i in al if '_0' == i.name()[:2]]
    j1 = [i for i in al if '_1' == i.name()[:2]]
    j2 = [i for i in al if '_2' == i.name()[:2]]
    j3 = [i for i in al if '_3' == i.name()[:2]]
    j4 = [i for i in al if '_4' == i.name()[:2]]
    j5 = [i for i in al if '_5' == i.name()[:2]]
    j6 = [i for i in al if '_6' == i.name()[:2]]
    j7 = [i for i in al if '_7' == i.name()[:2]]
    j8 = [i for i in al if '_8' == i.name()[:2]]
    j9 = [i for i in al if '_9' == i.name()[:2]]
    ja = [i for i in al if '_a' == i.name()[:2]]
    jb = [i for i in al if '_b' == i.name()[:2]]
    jc = [i for i in al if '_c' == i.name()[:2]]
    jd = [i for i in al if '_d' == i.name()[:2]]
    je = [i for i in al if '_e' == i.name()[:2]]
    jf = [i for i in al if '_f' == i.name()[:2]]

    log += 'Primary Body Joint         _0**  :  {:3d}\n'.format(len(j0))
    log += 'Primary Right Joint        _1**  :  {:3d}\n'.format(len(j1))
    log += 'Primary Left Joint         _2**  :  {:3d}\n'.format(len(j2))
    log += 'Animation Contol Joint     _3**  :  {:3d}\n'.format(len(j3))
    log += 'Hand Joint                 _4**  :  {:3d}\n'.format(len(j4))
    log += '                           _5**  :  {:3d}\n'.format(len(j5))
    log += 'Effect Joint               _6**  :  {:3d}\n'.format(len(j6))
    log += '                           _7**  :  {:3d}\n'.format(len(j7))
    log += 'Facial Joint               _8**  :  {:3d}\n'.format(len(j8))
    log += 'Weapon Joint               _9**  :  {:3d}\n'.format(len(j9))
    log += 'Assist Drive Joint         _a**  :  {:3d}\n'.format(len(ja))
    log += '                           _b**  :  {:3d}\n'.format(len(jb))
    log += 'Simulation Joint1          _c**  :  {:3d}\n'.format(len(jc))
    log += 'Simulation Joint2          _d**  :  {:3d}\n'.format(len(jd))
    log += 'Simulation Joint3          _e**  :  {:3d}\n'.format(len(je))
    log += 'Syatem Joint               _f**  :  {:3d}\n'.format(len(jf))
    log += '-----------------------------------------------------------------\n'
    log += '*All Valid Joint                 :  {:3d}*\n'.format(len(al))
    log += '-----------------------------------------------------------------\n'
    log += 'null Joint                 null  :  {:3d}\n'.format(len(nl))
    log += 'Delete Joint               del_  :  {:3d}\n'.format(len(dl))
    log += '*Invalid Joint             ????  :  {:3d}*\n'.format(len(iv))
    log += '-----------------------------------------------------------------\n'
    log += 'All Joint Node                   :  {:3d}\n'.format(len(jt))

    #-- delete invalid set
    if pm.objExists('invalid_joint_set'):
        pm.delete('invalid_joint_set')

    if iv:
        log += '------------------- *Invalid Joint ------------------------------\n'
        #-- create set
        pm.select(iv, r=True)
        pm.sets(n='invalid_joint_set')
        #-- log
        for i in iv:
            log += 'Invalid Joint                    :  {0}\n'.format(i.name())

    print(log)
    return log


def getJointList(v='_0', typ=False):
    log = '------------------- Joint Name {0}** -----------------------------\n'.format(v)
    jt = pm.ls('null', dag=True, typ='joint')
    al = [i for i in jt if not 'del' in i.name() and not 'null' == i.name()]

    hv  = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    tgt = ['{0}{1}{2}'.format(v, i, j) for i in hv for j in hv]
    jList = [i for i in al if v in i.name()]
    tl = []
    jl = []

    if typ == 0: #-- Unused
        for i in tgt:
            if i in jList:
                v = '    '
            else:
                v = i
            tl.append(v)
    elif typ == 1: #-- Used
        for i in tgt:
            if not i in jList:
                v = '    '
            else:
                v = i
            tl.append(v)
    elif typ == 2: #-- Select
        for i in tgt:
            if not i in jList:
                v = '    '
            else:
                v = i
                jl.append(i)
            tl.append(v)
            
    #-- select
    if typ == 2:
        pm.select(jl, r=True)

    #-- log
    for i in range(16):
        log += '{0}\n'.format(', '.join(tl[i*16:(i+1)*16]))
    print(log)
    return log




#-- Renamer    
# ---- declare variables
AR_prefixList = ['L_', 'R_', 'SU_']
AR_suffixList = ['_ax', '_old', '_GP', '_JT', '_pos', '_cnst', '_ctrl']


def AR_SearchAndReplacePreview(*args, **kwargs):
    if mc.menuItem('AR_mb_cbx1', cb=True, q=True):
        AR_preview()
    else:
        pass


# -- Rename and numbering
def AR_renameAndNumber(*args, **kwargs):
    # -- declare object valuables
    selObj = pm.selected()
    # -- get information from main UI
    newName = mc.textField('AR_txf30', tx=True, q=True)
    start   = mc.intField('AR_inf30', v=True, q=True)
    step    = mc.intField('AR_inf31', v=True, q=True)
    
    if not newName == '':
        # -- loop of renaming
        if '#' in newName:
            digit = newName.rfind('#') - newName.find('#') + 1
            for obj, num in zip(selObj, range(start, len(selObj)*step+start, step)):
                obj.rename(newName.replace('#'*digit, '{0:0>{1}}'.format(num, digit)))
        else:
            for obj, num in zip(selObj, range(start, len(selObj)*step+start, step)):
                obj.rename('{0}{1}'.format(newName, num))
    else:
        mc.warning('please fill in new name in the Rename field.')


# -- hide UI
def AR_hideMainUI(*args, **kwargs):
    mc.window('airRenamerUI', vis=False)


# -- quit UI
def AR_deleteMainUI(*args, **kwargs):
    mc.deleteUI('airRenamerUI', wnd=True)


# -- clear field
def AR_clearTextField(*args, **kwargs):
    mc.textField('AR_txf{0}'.format(str(args[0])), tx='', e=True)


def AR_clearAllField(*args, **kwargs):   
    mc.textField('AR_txf10', tx='', e=True)
    mc.textField('AR_txf11', tx='', e=True)
    mc.textField('AR_txf20', tx='', e=True)
    mc.textField('AR_txf21', tx='', e=True)
    mc.intField('AR_inf30', v=0, e=True)
    mc.intField('AR_inf31', v=1, e=True)
    mc.textField('AR_txf30', tx='', e=True)


# -- get last Selected
def AR_getLastSelected(*args, **kwargs):
    name = mc.ls(sl=True)[args[1]]
    mc.textField('AR_txf{0}'.format(str(args[0])), tx=name, e=True)


# -- seach from UI
def AR_searchObject(*args, **kwargs):
    search = mc.textField('AR_txf10', tx=True, q=True)
    if not mc.ls(search):
        mc.warning('\'{0}\' in not exists.'.format(search))
    else:
        mc.select(search, r=True)

def AR_addPrefixText(*args, **kwargs):
    mc.textField('AR_txf20', tx=AR_prefixList[args[0]], e=True)


def AR_addSuffixText(*args, **kwargs):
    mc.textField('AR_txf21', tx=AR_suffixList[args[0]], e=True)


def AR_previewWindow(*args, **kwargs):
    windowName = mc.window('airPreviewUI', t='air preview', ret=False, mb=False, w=240)
    PR_fmL00 = mc.formLayout('PR_fmL00')
    PR_spa00 = mc.separator('PR_spa00', st='in', h=6)
    PR_pnL00 = mc.paneLayout(cn='vertical2')
    PR_txL00 = mc.textScrollList('PR_txL00')
    PR_txL01 = mc.textScrollList('PR_txL01', ams=True)
    mc.setParent('..')
    PR_btn00 = mc.button('PR_btn00', l='Run', w=120)
    PR_btn01 = mc.button('PR_btn01', l='Cancel', w=60)
    
    
    mc.formLayout(PR_fmL00, e=True,
           af = [(PR_spa00, 'top',  0),  (PR_spa00, 'left', 2), (PR_spa00, 'right', 2),
                 (PR_pnL00, 'top',  6),  (PR_pnL00, 'left', 0), (PR_pnL00, 'right', 0),
                 (PR_btn00, 'bottom', 10), (PR_btn00, 'left', 20), 
                 (PR_btn01, 'bottom', 10), (PR_btn01, 'right', 20),
                 ], 
           ac = [(PR_btn00, 'right', 5, PR_btn01),
                 (PR_pnL00, 'bottom',  5, PR_btn00)]
           )
    mc.textScrollList(PR_txL00, a=['test', 'ddd', 'eee', 'dsaf', 'setraf', 'sdfadsfa', 'sss', 'ghhhg'], e=True)
    mc.textScrollList(PR_txL01, a=['test', 'ddd', 'eee', 'dsaf', 'setraf', 'sdfadsfa', 'sss', 'ghhhg'], e=True)
    mc.showWindow()


# -- preview window exe
def AR_preview():
    if mc.window('airPreviewUI', ex=True) == False :
        AR_previewWindow()
    else:
        mc.deleteUI('airPreviewUI', wnd=True)
        AR_previewWindow()

