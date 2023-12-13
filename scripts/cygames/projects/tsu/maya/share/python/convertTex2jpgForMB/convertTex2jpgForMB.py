# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as mc
from dccUserMayaSharePythonLib import ui
from dccUserMayaSharePythonLib import file_dumspl as f
import os
import stat
import shutil
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
#from shiboken2 import wrapInstance
#import maya.OpenMaya as om
#import maya.OpenMayaUI as OpenMayaUI


# UI_def
winname = 'convertTex2jpgForMB'
bt_1 = 'bt_toLambert'
bt_2 = 'bt_startConvJpg'
bt_3 = 'bt_moveJpg2Hd'
bt_4 = 'bt_replace_path'
bt_5 = 'bt_exportFbx'

grey = [0.32, 0.32, 0.32]
green = [0.32, 0.4, 0.32]


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
                print( 'Type     : {0}'.format(i[:2]))
                print( 'Number   : {0}'.format(i[-4:]))
    if ID:
        return ID
    else:
        return None


def toLambert():

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

    def replaceLowMT(tgt_mt=''):
        # -- create shader for MB （新しいマテリアルを作成して繋ぎなおす）
        low_mt = pm.shadingNode('lambert', asShader=True, n='{0}_lowMT'.format(tgt_mt))
        se = pm.sets(nss=True, r=True, em=True)
        low_mt.outColor >> se.surfaceShader

        # -- get target
        pm.select(tgt_mt, r=True)
        pm.hyperShade(objects='')
        pm.sets(se, fe=pm.ls(sl=True))

        # -- orverride
        atex = attributeExists(tgt_mt, 'g_IsOverrideAlbedo')

        # -- get file color texture
        ALBEDO_NAMES = (
            'g_AlbedoMap', 'g_AlbedoMap0', 'g_AlbedoMap1', 'g_EyeIrisTexture', 'g_AlbedoTex',
            'g_AlbedoTex0', 'g_AlbedoTex1'

        )

        fList = []
        print('atex: ', atex)
        val = False
        if not atex or not pm.getAttr('{0}.g_IsOverrideAlbedo'.format(tgt_mt)):
            print('tgt_mt: ', tgt_mt)
            for albedo in ALBEDO_NAMES:
                try:
                    fList = pm.listConnections(
                        '{}.{}'.format(tgt_mt, albedo),
                        s=True, c=False, p=False, d=False, t='file')
                    val = True
                    print(albedo)
                except:
                    pass
            print('val: ', val)

            # -- connection
            print('fList', fList)
            if fList:
                for f in fList:
                    # path = f.fileTextureName.get()
                    f.outColor >> low_mt.color

        # -- simple color
        elif atex and pm.getAttr('{0}.g_IsOverrideAlbedo'.format(tgt_mt)):
            col = pm.getAttr('{0}.g_OverrideAlbedoColor'.format(tgt_mt))
            pm.setAttr('{0}.color'.format(low_mt.name()), col, typ='double3')
        # -- deselect
        pm.select(cl=True)
        print('')

    mtList = pm.ls(typ='dx11Shader')
    if mtList:
        for i in mtList:
            replaceLowMT(i.name())

    # 未使用ノード削除
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
    pm.button(bt_1, e=True, bgc=green)


def exportFbxModelOnly(exportPath):
    pm.mel.eval('FBXExportAnimationOnly -v false;')
    pm.mel.eval('FBXExportShapes -v true;')
    pm.mel.eval('FBXExportSkins -v true;')
    pm.mel.eval('FBXExportCameras -v false;')
    pm.mel.eval('FBXExportLights -v false;')
    pm.mel.eval('FBXExportApplyConstantKeyReducer -v false;')
    pm.mel.eval('FBXExportBakeComplexAnimation -v false;')
    pm.mel.eval('FBXExportInAscii -v false;')
    pm.mel.eval('FBXExportInputConnections -v false;')
    pm.mel.eval('FBXExportConstraints -v false;')
    exportPath = exportPath.replace('\\', '/')
    pm.mel.eval('FBXExport -f (\"' + exportPath + '\");')


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


def _getConvertfbxtextureWindow():
    return ui.getMainWindowAsQMainWindow().findChildren(QMainWindow)


def _getConvFoldPath():
    scene_name = mc.file(q=True, sn=True)
    scene_fld = os.path.dirname(scene_name)
    conv_fold = os.path.join(scene_fld, 'convertTexture')
    if not os.path.isdir(conv_fold):
        os.makedirs(conv_fold)
    return conv_fold


def _getTmpFbxPath():
    id_ = getIDFromRoot()
    return os.path.join(_getConvFoldPath(), id_ + '_tmp.fbx')


def startConvJpg():
    id_ = getIDFromRoot()
    if id_ is None:
        pm.warning('モデルからidが取得できません')
        return

    conv_fold = _getConvFoldPath()
    tmp_fbx_name = _getTmpFbxPath()

    # 変換元としてfbx出力
    exportFbxModelOnly(tmp_fbx_name)

    # sourceimagesの中身を念の為消す
    tgt_si_fld = os.path.join(conv_fold, 'sourceimages')
    if os.path.isdir(tgt_si_fld):
        tgt_files = f.getAllFiles(tgt_si_fld)
        for tgt_f in tgt_files:
            os.remove(tgt_f)

    # convertfbxtextureで変換
    import tsubasa.maya.tools.convertfbxtexture.gui
    tsubasa.maya.tools.convertfbxtexture.gui.main()
    wins = _getConvertfbxtextureWindow()
    cftw = None
    for w in wins:
        try:
            if w.windowTitle() == 'Convert Fbx (Texture & Material)':
                les = w.findChildren(QLineEdit)
                les[0].setText(tmp_fbx_name)
                les[1].setText(conv_fold)
                pbs = w.findChildren(QPushButton)[2]
                cftw = w
        except:
            pass
    # 無理やりクリックして実行
    pbs.click()

    if w is not None:
        w.close()

    pm.button(bt_2, e=True, bgc=green)


def moveJpg2Hd():
    conv_fold = _getConvFoldPath()
    tgt_si_fld = os.path.join(conv_fold, 'sourceimages')
    tgt_files = f.getAllFiles(tgt_si_fld)
    id = getIDFromRoot()
    dst_fld = 'D:/cygames/tsubasa/work/chara/{0}/{1}/rig/_data/sourceimages/hd'.format(id[:2], id)
    if not os.path.isdir(dst_fld):
        os.makedirs(dst_fld)

    for tgt_f in tgt_files:
        dst_file_path = os.path.join(dst_fld, os.path.basename(tgt_f))
        do_copy = True
        if os.path.isfile(dst_file_path):
            response = pm.confirmDialog(
                title='question', message='既に同名のファイルが存在します\n\n' + dst_file_path,
                button=['overwrite', 'cancel'], dismissString='cancel')

            if response == 'cancel':
                do_copy = False

        if do_copy:
            if os.path.isfile(dst_file_path):
                os.chmod(dst_file_path, stat.S_IWRITE)
            shutil.copy2(tgt_f, dst_file_path)

            print('copied : {0}'.format(dst_file_path))

    pm.button(bt_3, e=True, bgc=green)


def replacePath():
    convertTexPath2Hd()
    try:
        # tmpFbxは消しておく
        os.remove(_getTmpFbxPath())
    except:
        pass
    pm.button(bt_4, e=True, bgc=green)


def exportFbx():
    conv_fold = _getConvFoldPath()
    id_ = getIDFromRoot()
    save_fbx_name = os.path.join(conv_fold, id_ + '_tex_converted.fbx')
    exportFbxModelOnly(save_fbx_name)
    pm.button(bt_5, e=True, bgc=green)


# ----------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------
def main():
    def update():
        id = getIDFromRoot()
        if id is not None:
            pm.text(tx, e=True, l=u'対象id : <big><b>{0}'.format(id))
        else:
            pm.text(tx, e=True, l=u'id不明')

        pm.button(bt_1, e=True, bgc=grey)
        pm.button(bt_2, e=True, bgc=grey)
        pm.button(bt_3, e=True, bgc=grey)
        pm.button(bt_4, e=True, bgc=grey)
        pm.button(bt_5, e=True, bgc=grey)

    if pm.window(winname, ex=True):
        pm.deleteUI(winname)
    win = pm.window(winname, t='ConvertTextureForMB', w=450, mb=True)
    pm.menu(l='Help')
    pm.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/EscgFw'))
    pm.columnLayout(adj=True)

    with pm.verticalLayout() as hl:
        with pm.rowLayout(nc=3, adj=True):
            tx = pm.text()
            pm.button(l='update', c=pm.Callback(update))
        pm.separator(h=3)
        pm.button(
            bt_1,
            l=u'[ 1 ] Color だけにした Lambert に変換',
            c=pm.Callback(toLambert))
        pm.button(
            bt_2,
            l=u'[ 2 ] .jpg に変換 （ プロンプト画面が閉じるまで待ちます ）',
            c=pm.Callback(startConvJpg))
        pm.separator(h=3)
        pm.button(
            bt_3,
            l=u'[ 3 ] 2で変換した .jpg を hdフォルダへコピー',
            c=pm.Callback(moveJpg2Hd))
        pm.button(
            bt_4,
            l=u'[ 4 ] テクスチャパスを hdフォルダの .jpg に置き換える',
            c=pm.Callback(replacePath))
        pm.separator(h=3)
        pm.button(
            bt_5,
            l=u'[ 5 ] このシーンをfbx出力(モデル、テクスチャのみ)',
            c=pm.Callback(exportFbx))
        pm.separator(h=3)
        with pm.rowLayout(nc=2, adj=True):
            pm.button(l='File Path Editor', c=pm.mel.FilePathEditor)
            pm.button(l=u'変換先のフォルダを開く', c=pm.Callback(os.startfile, _getConvFoldPath()))
    win.show()
    update()








