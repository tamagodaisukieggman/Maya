from __future__ import print_function
from workfile_manager import cmds as wcmds, postproc_utils
from workfile_manager.plugin_utils import PostProcBase, PluginType, Application
from postproc_set_editor import operator
import postproc_set_editor

import copy

class BasePlugin(PostProcBase):
    def apps_executable_on(self):
        return (
            Application.Maya, Application.MotionBuilder, Application.Standalone
        )

    def is_asset_eligible(self, asset):
        raise Exception('Override in derived class: is_asset_eligible')
            
    def order(self):
        return 0
        
    def tweak_asset(self, set_, asset, tags):
        pass
        
    def dcccmds(self):
        pass

    def execute(self, args):
        parts = args['publish_parts_parts']

        #inputfile = args['inputfile']
        print('parts: ', parts)
        #print 'inputfile: ', inputfile
        #self.dcccmds().open(inputfile)
        asset = args['child_asset']

        sets = self.dcccmds().list_node_names(type='objectSet')
        print('sets: ', sets)
        for _, set_ in enumerate(sets):
            print('set_:', set_)
            try:
                basename = self.dcccmds().get_attr(set_+'.postproc_edit_set__name')
            except Exception as e:
                continue
            print('basename: ', basename)
            
            if basename not in parts:
                continue
            
            childs = [self.dcccmds().get_name(x) for x in self.dcccmds().sets(set_, q=True)]
            print('childs: ', childs)
            try:
                tgt_set = [x for x in childs if x.endswith('_target')][0]
            except:
                print('ERROR: Cannot find target set: ', set_)
                continue
            
            descs = self.dcccmds().sets(tgt_set, q=True)
            descs = descs if descs is not None else []

            
            self.dcccmds().select(set_, ne=True)
            self.dcccmds().select('persp', add=True)
            for n in descs:
                self.dcccmds().select(n, ne=True, add=True)
            
            tags = copy.deepcopy(args['child_tags'])
            asset_ = copy.deepcopy(asset)

            self.tweak_asset(set_, asset_, tags)
            args['tags'] = tags

            self._publish(args, asset_, set_)
            #break

        return True

    def _publish(self, args, asset, set_):
        wfile = {'local_master_path':args['source_file'], 'version':args['source_version']}
        
        print('preproc: ', args['preproc'])
        wcmds.preproc(args, silent=True)

        publish_op_included = False

        #
        if 'export_postproc_sets' in args:
            # check if publish operator included.
            for main_set in args['export_postproc_sets']:
                setobj = postproc_set_editor.Set(set_name=main_set, dcccmds=self.dcccmds())
                ops = setobj.get_operators()
                for op_name in ops:
                    op = operator.get_operator_from_set(op_name, self.dcccmds())
                    if op is not None and op.is_publish_operator():
                        publish_op_included = True
                        break
                else:
                    continue
                
                break

            #
            if set_ in args['export_postproc_sets']:
                args['export_postproc_sets'].remove(set_)

        print('publish_op_included: ', publish_op_included)

        comment = args['comment'] if 'comment' in args else 'Published with publish parts.'

        from workfile_manager import p4utils
        p4u = p4utils.P4Utils.get_instance()
        
        _args = {
            'export_all': False, 
            'export_only': False,
            'submit_server': args['submit_server'] if 'submit_server' in args else False,
            'postproc': args['postproc'],
            'preproc': [],
            'procs': args['procs'], 
            'user': args['user'] if 'user' in args else p4u.p4.user,
            'commit_to_engine': args['commit_to_engine'],
            'keep_intermediate': args['keep_intermediate'],
            'textures': args['textures'], 
            'export_postproc_sets': args['export_postproc_sets'] if 'export_postproc_sets' in args else [],
            'comment': comment,
        }
        _arg_names = ['thumbnail_source', 'dont_delete_tmp_thumbnail', 'deadline_batchname',
                        'lazy_submit', 'lazy_submit_session', 'lazy_publish_cnts',]
        
        from postproc_set_editor import operator as opmod
        opmod.copy_args(args, _args, _arg_names)

        args['publish_op_included'] = publish_op_included
        args['specified'] = [set_]
        add = self.get_additional_args(args)
        
        if add is not None:
            for k in add:
                _args[k] = add[k]
        
        task = wcmds.PublishTask(asset, args['tags'], wfile, comment, _args)
        
        res = task.execute(silent=True)
        
        
    def get_additional_args(self, args):
        res = {}
        if args['publish_op_included']:
            proc = postproc_utils.find_proc_by_name('postproc_edit_set', plugin_type=PluginType.PublishPostProcess)
            res['is_custom_task'] =True
            res['postproc'] = [proc]
            res['child_postprocs'] = args['child_postprocs']
            if 'publish_parts_operators' in args:
                res['publish_parts_operators'] = args['publish_parts_operators']

        return res

        

    def getlabel(self):
        raise Exception('Override in derived class: getlabel')

    def default_checked(self):
        return False

    def is_editable(self):
        return False