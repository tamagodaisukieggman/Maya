# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as mc
import tsubasa.maya.tools.convertfbxtexture.gui


def ishex(v):
    try:
        int(v, 16)
        return True
    except ValueError:
        return False

def getIDFromRoot():
    ID = ''
    for i in pm.ls(typ='transform'):
        if not i.getParent() and len(i.name()) == 6:
            if i[:2].isalpha() and ishex(i[-4:]):
                ID = i.name()
                print('Asset ID : {0}'.format(i))
                print('Type     : {0}'.format(i[:2]))
                print('Number   : {0}'.format(i[-4:]))
    if ID:
        return ID
    else:
        return None


def main():

    # ----------------------------------------------------------------------
    # ---- low material
    # ----------------------------------------------------------------------
    def attributeExists(node, attr):
        if node == '' or attr == '':
            return False
        if mc.objExists(node) == False:
            return False
        attrList = mc.listAttr(node, sn=True)
        for i in range(len(attrList)):
            if attr == attrList[i]:
                return True
        attrList = mc.listAttr(node)
        for i in range(len(attrList)):
            if attr == attrList[i]:
                return True
        return False

    def replaceLowMT(tgt=''):
        #-- create shader for MB
        sd = pm.shadingNode('lambert', asShader=True, n='{0}_lowMT'.format(tgt))
        se = pm.sets(nss=True, r=True, em=True)
        sd.outColor >> se.surfaceShader
        #-- get target
        pm.select(tgt, r=True)
        pm.hyperShade(objects='')
        pm.sets(se, fe=pm.ls(sl=True))
        #-- orverride
        atex = attributeExists(tgt, 'g_IsOverrideAlbedo')
        #-- get file color texture
        fList = []
        val   = False
        if not atex or not pm.getAttr('{0}.g_IsOverrideAlbedo'.format(tgt)):
            if not val:
                try:
                    fList = pm.listConnections('{0}.g_AlbedoMap'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                    val   = True
                except:
                    pass
            if not val:
                try:
                    fList = pm.listConnections('{0}.g_AlbedoMap0'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                    val   = True
                except:
                    pass
            if not val:
                try:
                    fList = pm.listConnections('{0}.g_AlbedoMap1'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                    val   = True
                except:
                    pass
            if not val:
                try:
                    fList = pm.listConnections('{0}.g_EyeIrisTexture'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                    val   = True
                except:
                    pass
            if not val:
                try:
                    fList = pm.listConnections('{0}.g_AlbedoTex0'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                    val   = True
                except:
                    pass
            if not val:
                try:
                    fList = pm.listConnections('{0}.g_AlbedoTex1'.format(tgt), s=True, c=False, p=False, d=False, t='file')
                    val   = True
                except:
                    pass
            #-- connection
            if fList:
                for i in fList:
                    path = i.fileTextureName.get()
                    i.outColor >> sd.color
        #-- simple color
        elif atex and pm.getAttr('{0}.g_IsOverrideAlbedo'.format(tgt)):
            col = pm.getAttr('{0}.g_OverrideAlbedoColor'.format(tgt))
            pm.setAttr('{0}.color'.format(sd.name()), col, typ='double3')
        #-- deselect
        pm.select(cl=True)

    mtList = pm.ls(typ='dx11Shader')
    if mtList:
        for i in mtList:
            replaceLowMT(i.name())
    pm.mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    # ----------------------------------------------------------------------
    # ---- delete vertex color
    # ----------------------------------------------------------------------
    for mesh in pm.ls(typ='mesh'):
        # ---- delete vertex color
        csList = pm.polyColorSet(mesh, acs=True, q=True)
        if csList:
            for cs in csList:
                pm.polyColorSet(mesh, cs=cs, d=True)
    # ----------------------------------------------------------------------
    # ---- Normal lock
    # ----------------------------------------------------------------------
    meshList = list(set([i.getParent() for i in pm.ls('LOD0', dag=True, typ='mesh')]))
    log = ''
    for i in meshList:
        if any(pm.polyNormalPerVertex('{0}.vtx[*]'.format(i), fn=True, q=True)):
            log += 'unlock normal : {0}'.format(i.name())
            pm.polyNormalPerVertex(i, ufn=True)
    print(log)


def convertTexPath2Hd():	
    assetID = getIDFromRoot()
    astType = assetID[:2]
    pfPath  = r'D:\cygames\tsubasa\work\chara\{0}\{1}\rig'.format(astType, assetID)
    maPath  = r'{0}\motionbuilder'.format(pfPath)
    mbPath  = r'{0}\maya'.format(pfPath)
    daPath  = r'{0}\_data'.format(pfPath)
    siPath  = r'{0}\sourceimages\hd'.format(daPath).replace('\\', '/')
    fList   = [i for i in pm.ls(typ='file')]
    for i in fList:
        tx     = i.fileTextureName.get().split('/')[-1].replace('.tga', '.jpg')
        txPath = r'{0}/{1}'.format(siPath, tx)
        try:
            i.fileTextureName.set(txPath)
        except:
            pass


def convertfbxtexture():
    tsubasa.maya.tools.convertfbxtexture.gui.main()


def ui():
    winname = 'winf_ct2co'
    if pm.window(winname, ex=True):
        pm.deleteUI(winname)
    win = pm.window(winname, t='convertTex2ColorOnly', w=400)
    cl = pm.columnLayout(adj=True)

    pm.frameLayout(l=u'fbxシーン用にテクスチャをjpg変換', bgc=(0.32, 0.22, 0.32))
    with pm.verticalLayout() as hl:
        pm.button(
            l=u'１．ColorだけにしたLambertに変換',
            ann=u'ゲームマテリアル(dx11Shader) のデータをテクスチャをColorだけにしたLambertに変換Script',
            c=pm.Callback(main))
        pm.button(
            l=u'２．1で変換したシーンを普通にfbx出力し　→　「Convert Fbx」でjpg化',
            ann=u'jpg化ツール（指定したfolderへ吐き出す）',
            c=pm.Callback(convertfbxtexture))
        pm.text(l=u'３．２で生成されたjpgをhdフォルダへ移動させる')
        pm.button(
            l=u'４．２で生成されたjpgへのパス変更', ann=u'１．で開いていたシーン上で実行',
            c=pm.Callback(convertTexPath2Hd))

    win.show()







