from workman_world_custom.export_postproc.motionbuilder.all import postproc_publish_parts_base_mbuilder

class Plugin(postproc_publish_parts_base_mbuilder.BasePlugin):
    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False

    def getlabel(self):
        return 'Publish split animation'

    def get_additional_args(self, args):
        #
        from workfile_manager_mbuilder.export.preproc.all import export_postproc_sets
        from cylibassetdbutils import assetutils

        from workfile_manager import postproc_utils
        from workfile_manager.plugin_utils import PluginType

        res = {}

        if args['publish_op_included']:
            res['is_custom_task'] =True

        proc = postproc_utils.find_proc_by_name('postproc_edit_set', plugin_type=PluginType.PublishPostProcess)
        proc2 = postproc_utils.find_proc_by_name('maya.all.import_postproc_set', plugin_type=PluginType.PublishPostProcess)

        res['postproc'] = [proc2, proc] # order matters
        res['child_postprocs'] = args['child_postprocs']
        if 'publish_parts_operators' in args:
            res['publish_parts_operators'] = args['publish_parts_operators']

        #
        pp = export_postproc_sets.Plugin()

        # Get selected set objs.
        from postproc_set_editor_mbuilder import ui_mbuilder
        dcccmds = ui_mbuilder.DccCmds()

        tmpfile = assetutils.get_publish_tempfilename('postproc_set.yaml')

        
        _args = {
                #'specified': target_sets,
                'specified': args['specified'],
                'preset_file': tmpfile,
                'dryrun': True, 
            }
        print(('postproc_publish_split_motion_mbuilder: _args:', _args))    
        print(('postproc_publish_split_motion_mbuilder: tmp_preset:', tmpfile.replace('/', '\\')))
        
        pp.execute(_args)

        print(('tmp set file: ', tmpfile))
        res['postproc_set_file'] = tmpfile

        try:
            print(('>>>>> publish_op_included: ', args['publish_op_included']))
        except:
            print('>>>>>> publish_op_included not included.')

        if 'publish_op_included' in args and args['publish_op_included']:
            pass
        else:
            from workfile_manager_mbuilder import assetutils_motionbuilder
            dccutils = assetutils_motionbuilder.MotionBuilderUtils.get_instance()
            res['frame_range'] = dccutils.get_framerange()
            res['frame_rate'] = dccutils.get_framerate()
            print(('frame_range: ', res['frame_range']))

        return res
        

    def order(self):
        return 99999