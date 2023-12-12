# -*- coding: cp932 -*-
#===============================================
#
# �\���֘A
#
# Fujita Yukihiro
#
#===============================================
import maya.OpenMaya as OM
import maya.OpenMayaUI as OMUI

#-----------------------------------------------
#
# �r���[�|�[�g���L���v�`��
#
# @param      mPanel : �L���v�`�����郂�f���p�l��
# @param      filename : �L���v�`���摜��ۑ�����t�@�C����
# @param      extension : �摜�t�H�[�}�b�g
#
#-----------------------------------------------
def captureViewport(mPanel, filename, extension):

    img = OM.MImage()

    view = OMUI.M3dView()

    OMUI.M3dView.getM3dViewFromModelPanel(mPanel, view)

    view.beginGL()

    view.readColorBuffer(img, 1)

    view.endGL()

    #img.resize(w, h, aspect)

    img.writeToFile(filename, extension)
