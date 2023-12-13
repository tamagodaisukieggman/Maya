from __future__ import print_function
try:
    import maya.cmds as cmds

except:
    pass

from workman_world_custom.export_postproc.maya.all import postproc_publish_parts_base_maya

class Plugin(postproc_publish_parts_base_maya.BasePlugin):
    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False

    def getlabel(self):
        return 'Publish split animation'

    def get_additional_args(self, args):
        from workfile_manager import postproc_utils
        from workfile_manager.plugin_utils import PluginType

        res = {}

        if args['publish_op_included']:
            res['is_custom_task'] =True

        
        res['child_postprocs'] = args['child_postprocs']
        if 'publish_parts_operators' in args:
            res['publish_parts_operators'] = args['publish_parts_operators']

        proc2 = postproc_utils.find_proc_by_name('maya.all.import_postproc_set', plugin_type=PluginType.PublishPostProcess)
        #
        if 'publish_op_included' in args and args['publish_op_included']:
            proc = postproc_utils.find_proc_by_name('postproc_edit_set', plugin_type=PluginType.PublishPostProcess)
            res['postproc'] = [proc2, proc] # order matters

            print('postproc_publish_split_motion_maya: get_additional_args: ', args['publish_op_included'])
            # split motion.
            dags = cmds.ls(dag=True)
            if len(dags) > 0:
                cmds.select(dags, add=True)
            
        else:
            print('postproc_publish_split_motion_maya: get_additional_args: publish op not included.')

            # publish motion.
            from workfile_manager_maya import assetutils_maya
            dccutils = assetutils_maya.MayaUtils.get_instance()
            res['postproc'] = [proc2] + args['child_postprocs']
            res['export_all'] = False
            res['frame_range'] = dccutils.get_framerange()
            res['frame_rate'] = dccutils.get_framerate()
            print('postproc_publish_split_motion_maya: get_additional_args: res: ', res)

            if 'selection' in args:
                if type(args['selection']) is list and len(args['selection']) > 0:
                    res['selection'] = args['selection']

        return res
            