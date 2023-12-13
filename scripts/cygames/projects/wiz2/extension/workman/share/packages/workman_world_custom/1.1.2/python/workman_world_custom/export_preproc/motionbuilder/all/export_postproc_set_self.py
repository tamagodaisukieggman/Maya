# -*- coding: utf-8 -*-
from workfile_manager.plugin_utils import PreprocBase, Application

try:
    from postproc_set_editor_mbuilder import ui_mbuilder 
except:
    pass

class Plugin(PreprocBase):
    def application(self):
        return Application.MotionBuilder

    def apps_executable_on(self):
        return (
            Application.MotionBuilder,
        )

    def is_asset_eligible(self, asset):
        return True

    def execute(self, args):
        global_args = args['global_args']
        dcccmds = ui_mbuilder.DccCmds()
        buf = dcccmds.list_node_names(sl=True, type='objectSet')
        print(('export_postproc_set_self: selected sets: ', buf))

        export_sets = [x for x in buf if dcccmds.attribute_query('postproc_edit_set', n=x, ex=True) and dcccmds.get_attr(x+'.postproc_edit_set')]
        global_args['export_postproc_sets'] = export_sets
        print(('export_postproc_set_self: set export_postproc_sets var: ', export_sets))


        return True, None
        

    def getlabel(self):
        return 'Export post-proc set self'

    def order(self):
        return 100000

    def is_editable(self):
        return False

    def default_checked(self):
        return True

    
