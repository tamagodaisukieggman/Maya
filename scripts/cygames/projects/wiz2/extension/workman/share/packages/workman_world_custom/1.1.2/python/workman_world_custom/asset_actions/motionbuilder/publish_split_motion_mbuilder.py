# -*- coding: utf-8 -*-

from workfile_manager.plugin_utils import Application

try:
    from workman_world_custom.asset_actions.motionbuilder import publish_parts_base_mbuilder
except:
    pass

from Qt import QtWidgets, QtCore, QtGui

class Plugin(publish_parts_base_mbuilder.BasePlugin):
    def apps_executable_on(self):
        return [
            Application.MotionBuilder,
            Application.Standalone,]

    def is_asset_eligible(self, asset):
        if asset.area() != 'work':
            return False
        if asset.task != 'animation':
            return False

        return True

    def getlabel(self):
        return 'Publish animations'

    
    def is_valid_part(self, part, asset, tags):
        return True

    def postproc_name(self):
        return 'postproc_publish_split_motion_mbuilder'

    def allow_multi_items(self):
        return True

    def additional_args(self, args):
        args['plot_all'] = True
        args['frame_range'] = None
        args['frame_rate'] = None

        if 'inputfile_source' in args:
            filename = args['inputfile_source']
            
            try:
                import publish_files.ui
                from workman_world_custom.asset_actions.motionbuilder import publish_parts_base_mbuilder
                args['frame_range'] = publish_files.ui.get_maximum_framerange(filename, publish_parts_base_mbuilder.FBXReader)
            except:
                import traceback
                print((traceback.format_exc()))
                pass
            