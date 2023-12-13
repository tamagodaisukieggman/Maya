import maya.cmds as cmds
# import maya.mel as mel
import os


def importFBX_main(fbxPath):
    if not os.path.exists(fbxPath):
        return False
    
    print fbxPath
    cmds.file(fbxPath, i=True, type="FBX")
    cmds.file(selectAll=True)
    
    impotObjShape = cmds.ls(selection=True, type="mesh")[0]
    # --------------------------------------
    texfilePath = fbxPath.replace(".fbx", "_u1_v1.png")
    if not os.path.exists(texfilePath):
        return False
    # --------------------------------------
    texNode = cmds.shadingNode("file", asTexture=True, isColorManaged=True)
    p2dTex = cmds.shadingNode("place2dTexture", asUtility=True)
    # --------------------------------------
    cmds.connectAttr(p2dTex + ".coverage", texNode + ".coverage", f=True)
    cmds.connectAttr(p2dTex + ".translateFrame", texNode + ".translateFrame", f=True)
    cmds.connectAttr(p2dTex + ".rotateFrame", texNode + ".rotateFrame", f=True)
    cmds.connectAttr(p2dTex + ".mirrorU", texNode + ".mirrorU", f=True)
    cmds.connectAttr(p2dTex + ".mirrorV", texNode + ".mirrorV", f=True)
    cmds.connectAttr(p2dTex + ".stagger", texNode + ".stagger", f=True)
    cmds.connectAttr(p2dTex + ".wrapU", texNode + ".wrapU", f=True)
    cmds.connectAttr(p2dTex + ".wrapV", texNode + ".wrapV", f=True)
    cmds.connectAttr(p2dTex + ".repeatUV", texNode + ".repeatUV", f=True)
    cmds.connectAttr(p2dTex + ".offset", texNode + ".offset", f=True)
    cmds.connectAttr(p2dTex + ".rotateUV", texNode + ".rotateUV", f=True)
    cmds.connectAttr(p2dTex + ".noiseUV", texNode + ".noiseUV", f=True)
    cmds.connectAttr(p2dTex + ".vertexUvOne", texNode + ".vertexUvOne", f=True)
    cmds.connectAttr(p2dTex + ".vertexUvTwo", texNode + ".vertexUvTwo", f=True)
    cmds.connectAttr(p2dTex + ".vertexUvThree", texNode + ".vertexUvThree", f=True)
    cmds.connectAttr(p2dTex + ".vertexCameraOne", texNode + ".vertexCameraOne", f=True)
    cmds.connectAttr(p2dTex + ".outUV", texNode + ".uv", f=True)
    cmds.connectAttr(p2dTex + ".outUvFilterSize", texNode + ".uvFilterSize", f=True)
    # --------------------------------------
    cmds.setAttr(texNode + ".fileTextureName", texfilePath, type="string")
    matLambert = "lambert1"
    cmds.connectAttr(texNode + ".outColor", matLambert + ".color", force=True, f=True)
    # --------------------------------------
    cmds.sets(impotObjShape, forceElement="initialShadingGroup", edit=True)
    retImportObj = cmds.listRelatives(impotObjShape, parent=True)[0]
    cmds.setAttr(retImportObj + ".rotateY", 0.0)
    return retImportObj


def createSshot(strFile, thumb_mode):
    fileExt = os.path.exists(strFile)
    thumbprefix = "_thumb"
    if not fileExt:
        return False
    dirName = os.path.dirname(strFile)
    jpgBaseName = os.path.basename(strFile)
    jpgPath = dirName + "\\" + jpgBaseName.split(".")[0] + thumbprefix + ".jpg"
    jpgPathExt = os.path.exists(jpgPath)
    if thumb_mode:
        if jpgPathExt:
            return False
    
    if not jpgPathExt:
        print jpgPath, jpgPathExt
    # -------------------------
    cmds.file(f=True, new=True)
    importFBX_main(strFile)
    cmds.select(cl=True)
    cmds.viewFit()
    # -------------------------
    for i in cmds.getPanel(allPanels=True):
        if i == "modelPanel4":
            tergetPannel = i

    cmds.setFocus(tergetPannel)
    cmds.modelEditor(tergetPannel, edit=True, displayAppearance='flatShaded', displayTextures=True, displayLights="flat")
    cmds.select(cl=True)
    cmds.viewFit('perspShape', all=True)
    cmds.setAttr("perspShape.nearClipPlane", 1)
    cmds.setAttr("perspShape.farClipPlane", 10000000)
    cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
    cmds.playblast(completeFilename=jpgPath, frame=[1], format="image", viewer=False, widthHeight=[1024, 1024], orn=False)

    return jpgPath


def createSS_main(serchDir):
    strFileArry = []

    for root, dirs, files in os.walk(serchDir):
        for f in files:
            jpgBaseName = os.path.basename(f)
            ext = jpgBaseName.split(".")
            extLen = len(ext)
            if extLen == 2:
                if ext[1] == "fbx":
                    strFileArry.append(root + f)

    for filePathStr in strFileArry:
        createSshot(filePathStr, True)


def createSS(mode):
    dirNameArry = [
        "\\\\CGS-STR-PRI01-M\\mutsunokami_storage\\30_design\\environment\\Photogrammetry\\3d\\cambodia_201712\\180111\\180111\\",
        "\\\\CGS-STR-PRI01-M\\mutsunokami_storage\\30_design\\environment\\Photogrammetry\\3d\\cambodia_201712\\",
        "\\\\CGS-STR-PRI01-M\\mutsunokami_storage\\30_design\\environment\\Photogrammetry\\3d\\cambodia_201712\\180110\\CG6358_work_exp\\",
        "\\\\CGS-STR-PRI01-M\\mutsunokami_storage\\30_design\\environment\\Photogrammetry\\3d\\cambodia_201712\\180109\\CG3575_work_exp\\",
        "\\\\CGS-STR-PRI01-M\\mutsunokami_storage\\30_design\\environment\\Photogrammetry\\3d\\cambodia_201712\\180109\\CG3652_work_exp\\"
    ]

    if mode:
        dialogObj = cmds.confirmDialog(title='Confirm', message='Are you sure?', button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if dialogObj != "Yes":
            return False

    for dirName in dirNameArry:
        createSS_main(dirName)


def createSS_test():
    print("mokemoke")

