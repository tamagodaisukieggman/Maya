# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as mc

def setDrawingOverride(obj='', oe=1, dt=0, lod=0, sd=1, tx=1, pb=1, vis=1, cot=0, cid=0, rgb=(0.0, 0.0, 0.0)):
    '''
set Drawing Override attributes

Parameters:
  - obj str: object
  - oe bool: override enabled
  - dt int: display type
  - lod int: Level of detail
  - sd bool: shading
  - tx bool: texturing
  - pb bool: playback
  - vis bool: visibility
  - cot int: color type
  - cid int: index color id
  - rgb float list: rgb color values

Returns:
  - : 

Error:
  - :
    '''
    obj = pm.PyNode(obj)
    obj.overrideEnabled.set(oe)
    obj.overrideDisplayType.set(dt)
    obj.overrideLevelOfDetail.set(lod)
    obj.overrideShading.set(sd)
    obj.overrideTexturing.set(tx)
    obj.overridePlayback.set(pb)
    obj.overrideVisibility.set(vis)
    obj.overrideRGBColors.set(cot)
    obj.overrideColor.set(cid)
    obj.overrideColorRGB.set(rgb[0],rgb[1],rgb[2])


def resetDrawingOverrirde():
    pm.checkBox('rsdo_OverrideEnabled', v=0, e=True)
    pm.optionMenu('rsdo_DisplayType', sl=1, e=True)
    pm.optionMenu('rsdo_LOD', sl=1, e=True)
    pm.checkBox('rsdo_Shading', v=1, e=True)
    pm.checkBox('rsdo_Texturing', v=1, e=True)
    pm.checkBox('rsdo_Playback', v=1, e=True)
    pm.checkBox('rsdo_Visibility', v=1, e=True)
    pm.palettePort('rsdo_Color', scc=0, e=True)


class DrawingOverrideEditorUI(object):
    def __init__(self):
        self.windowManageName = 'DrawingOverrideEditor'
        self.windowTitle      = 'Drawing Override Editor'
        self.windowSize       = [600, 200]

    def checkWindowOverlap(self):
        if pm.window(self.windowManageName, ex=True):
            pm.deleteUI(self.windowManageName)

    def run_drawingOverride(self):
        oe  = self._oe_ckb.getValue()
        dt  = self._dt_opm.getSelect() - 1
        lod = self._lod_opm.getSelect() - 1
        sd  = self._sd_ckb.getValue()
        tx  = self._tx_ckb.getValue()
        pb  = self._pb_ckb.getValue()
        vis = self._vis_ckb.getValue()
        cot = self._cot_opm.getSelect() - 1
        cid = self._cid_ppt.getSetCurCell()
        rgb = self._rgb_csg.getRgbValue()

        for i in mc.ls(sl=True):
            setDrawingOverride(i, oe, dt, lod, sd, tx, pb, vis, cot, cid, rgb)

    def reset_drawingOverride(self):
        self._oe_ckb.setValue(0)
        self._dt_opm.setSelect(1)
        self._lod_opm.setSelect(1)
        self._sd_ckb.setValue(1)
        self._tx_ckb.setValue(1)
        self._pb_ckb.setValue(1)
        self._vis_ckb.setValue(1)
        self._cot_opm.setSelect(1)
        self._cid_ppt.setSetCurCell(0)
        self._rgb_csg.setRgbValue([0.0,0.0,0.0])

    def main(self):               
        self.checkWindowOverlap()
        window = pm.window(self.windowManageName,
                           t  = self.windowTitle,
                           w  = self.windowSize[0],
                           h  = self.windowSize[1],
                           mb = True)

        # -- menu
        pm.menu(l='Help', hm=True)
        pm.menuItem(l='Maya 2019 HELP',
                    c='mc.showHelp("https://help.autodesk.com/view/MAYAUL/2019/JPN/", a=True, docs=True)')

        # -- base form layout
        self.fmL0 = pm.formLayout(nd=100)
        with self.fmL0:
            self.sep0 = pm.separator()
            
            # -- main form layout
            self.fmL1 = pm.formLayout(nd=100)
            with self.fmL1:
                self._oe_ckb  = pm.checkBox(v=0, l='Override Enabled')
                self._dt_opm  = pm.optionMenu(l='DisplayType :')
                pm.menuItem(l='Normal')
                pm.menuItem(l='Template')
                pm.menuItem(l='Reference')
                self._lod_opm = pm.optionMenu(l='LOD :')
                pm.menuItem(l='All')
                pm.menuItem(l='Bounding Box')
                self._sd_ckb  = pm.checkBox(v=1, en=1, l='Shading')
                self._tx_ckb  = pm.checkBox(v=1, en=1, l='Texturing')
                self._pb_ckb  = pm.checkBox(v=1, en=1, l='Playback')
                self._vis_ckb = pm.checkBox(v=1, en=1, l='Visibility')
                self._cot_opm = pm.optionMenu(l='Color Type :')
                pm.menuItem(l='Index')
                pm.menuItem(l='RGB')

                # -- color index
                self._cid_ppt = pm.palettePort(dim = (16, 2),
                                               w   = 16*20,
                                               h   = 2*20,
                                               t   = 0,
                                               td  = True,
                                               ced = False,
                                               en  = True)
                
                for i in range(1, 32):
                    col = pm.colorIndex(i, q=True)
                    pm.palettePort(self._cid_ppt, rgb=(i, col[0], col[1], col[2]), e=True)  


                # -- rgb color
                self._rgb_csg = pm.colorSliderGrp(l   = 'RGB color :', 
                                                  rgb = (0.0, 0.0, 0.0),
                                                  adj = False,
                                                  ad2 = False,
                                                  ad3 = True,
                                                  cw  = (1, 70),
                                                  en  = True)
                self.sep12 = pm.separator(st='none')
                
                # -- button
                self._run_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                  i1  = 'pencilCursor.png',
                                                  al  = 'center', 
                                                  bgc = (0.4, 0.4, 0.4),
                                                  l   = 'Set Override', 
                                                  c   = pm.Callback(self.run_drawingOverride), 
                                                  h   = 30)
                self._res_btn = pm.iconTextButton(st  = 'iconAndTextHorizontal', 
                                                  i1  = 'redrawPaintEffects.png', 
                                                  al  = 'center', 
                                                  bgc = (0.4, 0.4, 0.4),
                                                  l   = 'Reset', 
                                                  c   = pm.Callback(self.reset_drawingOverride), 
                                                  h   = 30)

                self.sep13 = pm.separator(st='none')
                
        # -- Edit UI Layout
        pm.formLayout(self.fmL0, e=True,
               af = [(self.sep0, 'top', 0), (self.sep0, 'left', 0), (self.sep0, 'right', 0), 
                     (self.fmL1, 'top', 0), (self.fmL1, 'left', 0), (self.fmL1, 'right', 0), (self.fmL1, 'bottom', 0),
                    ])
                    
        pm.formLayout(self.fmL1, e=True,
               af = [(self._oe_ckb, 'top',  20), (self._oe_ckb, 'left', 10), (self._oe_ckb, 'right', 10),
                     (self._dt_opm, 'top',  50), (self._dt_opm, 'left', 10), (self._dt_opm, 'right', 10),
                     (self._lod_opm, 'top', 80), (self._lod_opm, 'left', 10), (self._lod_opm, 'right', 10),
                     (self._sd_ckb, 'top', 120), (self._sd_ckb, 'left', 10), (self._sd_ckb, 'right', 10),
                     (self._tx_ckb, 'top', 150), (self._tx_ckb, 'left', 10), (self._tx_ckb, 'right', 10),
                     (self._pb_ckb, 'top', 180), (self._pb_ckb, 'left', 10), (self._pb_ckb, 'right', 10),
                     (self._vis_ckb, 'top', 210), (self._vis_ckb, 'left', 10), (self._vis_ckb, 'right', 10),
                     (self._cot_opm, 'top', 240), (self._cot_opm, 'left', 10), (self._cot_opm, 'right', 10),
                     (self._cid_ppt, 'top', 270), (self._cid_ppt, 'left', 10), (self._cid_ppt, 'right', 10),
                     (self._rgb_csg, 'top', 330), (self._rgb_csg, 'left', 10), (self._rgb_csg, 'right', 10),
                     (self.sep12, 'top', 370),
                     (self._run_btn, 'bottom', 10), (self._run_btn, 'left', 10), 
                     (self._res_btn, 'bottom', 10),  (self._res_btn, 'right', 10),
                     (self.sep13, 'bottom', 10),
                    ],
               ap = [(self._run_btn, 'right', 2, 70), 
                     (self._res_btn, 'left', 2, 70), 
                    ])
                    
        window.show()
        

def showUI():
    testIns = DrawingOverrideEditorUI()
    testIns.main()
    

