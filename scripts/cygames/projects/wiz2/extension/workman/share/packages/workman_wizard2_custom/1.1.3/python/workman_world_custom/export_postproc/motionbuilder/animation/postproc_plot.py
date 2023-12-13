# -*- coding: utf-8 -*-
from __future__ import print_function
try:
    import pyfbsdk as fb
    from workfile_manager_mbuilder import assetutils_motionbuilder
    dccutils = assetutils_motionbuilder.MotionBuilderUtils.get_instance()
except:
    pass

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

class Plugin(PostProcBase):
    def application(self):
        return Application.MotionBuilder

    def apps_executable_on(self):
        return (
            Application.MotionBuilder,
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False

    def order(self):
        return 10
        
    def execute(self, args):
        import cymobuapiutils
        #print 'args: ', args
        print('frame_range:', args['frame_range'])
        print('frame_rate: ', args['frame_rate'])

        try:
            start_frame, end_frame = args['frame_range']
        except:
            print('>>>>>>>>>>>> frame_range not set. use current range.')
            start_frame, end_frame = dccutils.get_framerange()

        if 'plot_all' in args['global_args'] and args['global_args']['plot_all']:
            #cymobuapiutils.select_all()  # To avoid crashing during the file open iteration of the PublisFiles tool, do not use this.
            cymobuapiutils.select_children(fb.FBSystem().Scene.RootModel.Children)
            comps = [fb.FBSystem().Scene.ControlSets, fb.FBSystem().Scene.Characters, 
                fb.FBSystem().Scene.Cameras, fb.FBSystem().Scene.Constraints,
                fb.FBSystem().Scene.Sets, fb.FBSystem().Scene.Groups,
                fb.FBSystem().Scene.Namespaces,
                fb.FBSystem().Scene.Lights,fb.FBSystem().Scene.Materials,
                fb.FBSystem().Scene.Shaders,
                fb.FBSystem().Scene.Takes,fb.FBSystem().Scene.Textures,
                ]
            for comp in comps:
                for n in comp:
                    n.Selected = True
                
        else:
            cymobuapiutils.select_children()


        for n in cymobuapiutils.get_selection():
            for p in n.PropertyList:
                try:
                    p.SetAnimated(True)
                except:
                    pass
        
        if 'frame_rate' not in args or args['frame_rate'] is None:
            args['frame_rate'] = dccutils.get_framerate()
        
        fb.FBPlayerControl().SetTransportFps(fb.FBTimeMode.kFBTimeModeCustom, args['frame_rate'])

        fps = fb.FBTime(0,0,0,1,0, fb.FBTimeMode.kFBTimeModeCustom)
        opt = fb.FBPlotOptions()
        opt.RotationFilterToApply = fb.FBRotationFilter.kFBRotationFilterNone
        opt.UseConstantKeyReducer = False
        opt.PlotPeriod = fps
        opt.PlotAllTakes = False
        opt.PlotOnFrame = True
        opt.PlotLockedProperties = True

        start = fb.FBSystem().CurrentTake.LocalTimeSpan.GetStart()
        end = fb.FBSystem().CurrentTake.LocalTimeSpan.GetStop()
        try:
            start.SetFrame(int(start_frame))
            end.SetFrame(int(end_frame))
        except:
            print('Could not start/end frame.')
        
        timespan = fb.FBTimeSpan(start, end)

        fb.FBSystem().CurrentTake.LocalTimeSpan = timespan
        
        fb.FBSystem().CurrentTake.PlotTakeOnSelected(opt)

        for ch in fb.FBSystem().Scene.Characters:
            ch.ActiveInput = False

        
    def getlabel(self):
        return 'Plot Animation'

    def get_args(self):
        args = {}
        try:
            start = fb.FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
            end = fb.FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()
            args['frame_range'] = (start, end)
            args['frame_rate'] = fb.FBPlayerControl().GetTransportFpsValue()
        except:
            pass
        return args

    def default_checked(self):
        return True