from __future__ import print_function
try:
    import maya.cmds as cmds
    from workfile_manager_maya import assetutils_maya
    dccutils = assetutils_maya.MayaUtils.get_instance()
except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def apps_executable_on(self):
        return [Application.Maya, 
                Application.Standalone,
            ]

    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False
            
    def order(self):
        return 8
        
    def execute(self, args):
        selection = cmds.ls(sl=True)

        try:
            _start_frame, _end_frame = args['frame_range']
            start_frame = int(_start_frame)
            end_frame = int(_end_frame)
        except:
            start_frame, end_frame = dccutils.get_framerange()

        if end_frame <= start_frame:
            end_frame = start_frame + 1

        cmds.bakeResults(cmds.ls(dag=True), simulation=False, time=(start_frame, end_frame), hierarchy='below', 
            sampleBy=1, oversamplingRate=1, disableImplicitControl=True, preserveOutsideKeys=True, 
            sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False,
            bakeOnOverrideLayer=False, minimizeRotation=True, controlPoints=False, shape=True)
        print ('baking done.')

        print('selection:', selection)
        if selection == []:
            cnst = cmds.ls(type='constraint')
        else:
            cnst = cmds.listRelatives(selection, f=True, ad=True, type='constraint')
        #print('constraints to delete:', cnst) # Too much information.
        if cnst is not None and len(cnst) > 0:
            cmds.delete(cnst)
            print('constraints deleted.')
        
        selection = [x for x in selection if cmds.objExists(x)]
        cmds.select(selection, hi=True)
        cmds.filterCurve()

        al = cmds.ls(type='animLayer')
        if len(al) > 0:
            try:
                cmds.delete(al)
            except:
                pass

        cmds.select(selection)
        
        return True

    def getlabel(self):
        return 'Bake Animation'

    def get_args(self):
        args = {}
        try:
            start = cmds.playbackOptions(q=True, min=True)
            end = cmds.playbackOptions(q=True, max=True)
            args['frame_range'] = (start, end)
        except:
            pass
        return args