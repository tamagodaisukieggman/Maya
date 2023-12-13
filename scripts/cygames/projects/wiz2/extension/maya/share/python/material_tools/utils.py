from maya import cmds
import os

def create_glslshader(ogsfx):
    if not cmds.pluginInfo('glslShader.mll', q=True, l=True):
        try:
            cmds.loadPlugin('glslShader.mll')
        except:
            cmds.error('Failed in loading glslShader plugin.')

    basename = os.path.basename(ogsfx)
    if '.' in basename:
        basename = basename[:basename.index('.')]

    glsl_shader = cmds.shadingNode('GLSLShader', asShader=True, name=basename)
    set_ = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=glsl_shader+'_se')
    cmds.setAttr(glsl_shader+'.shader', ogsfx, type='string')
    cmds.connectAttr(glsl_shader+'.outColor', set_+'.surfaceShader', f=True)

    return (glsl_shader, set_)

def assign_new_glslshader(ogsfx):
    sel = cmds.ls(sl=True)
    _, set_ = create_glslshader(ogsfx)
    cmds.select(sel, ne=True)
    cmds.sets(e=True, fe=set_)

