# -*- coding: utf-8 -*-
from maya import cmds, mel

from mtk3d.maya.rig.convert.hik import converter as converter
reload(converter)

class MVNConvertToPly(object):
    def __init__(self):
        self.playmin = None
        self.playmax = None

    def main(self, current_scene=None, save_path=None):
        try:
            self.convert_mvn(current_scene)
            fbxspl = current_scene.split('/')
            fname = fbxspl[-1].split('.')[0]

            cmds.file(rn='{0}/{1}.ma'.format(save_path, fname))
            cmds.file(f=1, save=1)

            print('Saved:{0}/{1}.ma'.format(save_path, fname))

        except Exception as e:
            print('-------------\nCONVERT MVN ERROR:{0}'.format(e))

    def file_import(self, file_path):
        if file_path.endswith('.ma'):
            scene_type = 'mayaAscii'
            scene_options = 'v=0;p=17;f=0'
        elif file_path.endswith('.mb'):
            scene_type = 'mayaBinary'
            scene_options = 'v=0;'
        elif file_path.endswith('.fbx'):
            scene_type = 'FBX'
            scene_options = 'fbx'

            mel.eval('FBXRead -f "' + file_path + '";')
            result=mel.eval("FBXGetTakeLocalTimeSpan 1;")
            mel.eval("FBXClose;")
            self.playmin = round(result[0])
            self.playmax = round(result[1])


        cmds.file(file_path,
                  pr=1,
                  ignoreVersion=1,
                  i=1,
                  type=scene_type,
                  importFrameRate=True,
                  importTimeRange="override",
                  mergeNamespacesOnClash=False,
                  options=scene_options)


    def convert_mvn(self, current_scene=None):
        cmds.file('z:/mtk/work/resources/animations/clips/mob/workscenes/anm_mob00_m_000_anim.ma', f=1, o=1)
        print('OPEN BASE SCENE')
        destinationFilePath = 'Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/convert/hik/data/characters/mob00_m_000/mob00_m_000_ctrls.json'
        connectFilePath = 'Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/convert/hik/data/characters/mob00_m_000/mob00_m_000_connect_ctrls.json'
        c_mvn = converter.ConvertMVN(destinationChara='mob00_m_000', ctrlsSets=['mob00_m_000_000:ctrls_sets'], destinationFilePath=destinationFilePath, connectFilePath=connectFilePath)
        c_mvn.convert()

        consts = [u'upperarm_L_ik_pv_ctrl_pointConstraint1',
         u'upperarm_R_ik_pv_ctrl_pointConstraint1',
         u'calf_L_ik_pv_ctrl_pointConstraint1',
         u'calf_R_ik_pv_ctrl_pointConstraint1']

        cmds.delete(consts)

        pv_ctrls = {
                    'HIK_mob00_m_000:lowerarm_L_body_jnt':'mob00_m_000_000:upperarm_L_ik_pv_ctrl',
                    'HIK_mob00_m_000:lowerarm_R_body_jnt':'mob00_m_000_000:upperarm_R_ik_pv_ctrl',
                    'HIK_mob00_m_000:calf_L_body_jnt':'mob00_m_000_000:calf_L_ik_pv_ctrl',
                    'HIK_mob00_m_000:calf_R_body_jnt':'mob00_m_000_000:calf_R_ik_pv_ctrl',
                    }

        locs = []
        for body_jnt, ctrl in pv_ctrls.items():
            loc = cmds.spaceLocator()
            cmds.matchTransform(loc[0], ctrl)
            cmds.parentConstraint(body_jnt, loc[0], w=1, mo=1)
            cmds.pointConstraint(loc[0], ctrl, w=1, mo=1)
            locs.append(loc[0])

        self.file_import(current_scene)
        # select sets
        cmds.currentUnit(time='{}fps'.format(59.94))
        cmds.playbackOptions(min=self.playmin, max=self.playmax, ast=self.playmin, aet=self.playmax)

        cmds.select(['mob00_m_000_000:CtrlSet', 'mob00_m_000_000:ctrls_sets'], r=1, ne=1)
        ctrls = cmds.pickWalk(d='down')
        cmds.bakeResults(ctrls,
                         sparseAnimCurveBake=False,
                         minimizeRotation=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         oversamplingRate=1,
                         bakeOnOverrideLayer=False,
                         preserveOutsideKeys=True,
                         simulation=True,
                         sampleBy=1,
                         shape=False,
                         t=(self.playmin, self.playmax), disableImplicitControl=True, controlPoints=False)

        cmds.delete('HIK_mob00_m_000:root_jnt', 'Reference')
        cmds.delete('HIK*')
        cmds.delete(locs)

        print('CONVERTED')
