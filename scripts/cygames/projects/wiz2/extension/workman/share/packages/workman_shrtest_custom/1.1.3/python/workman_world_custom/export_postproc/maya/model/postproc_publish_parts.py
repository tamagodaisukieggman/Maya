from __future__ import print_function
try:
    import maya.cmds as cmds
except:
    pass

from workman_world_custom.export_postproc.maya.all import postproc_publish_parts_base_maya

class Plugin(postproc_publish_parts_base_maya.BasePlugin):
    def is_asset_eligible(self, asset):
        if asset.task == 'model':
            return True
        else:
            return False

    def tweak_asset(self, set_, asset, tags):
        import re
        basename = cmds.getAttr(set_+'.postproc_edit_set__name')
        m = re.search('(^|.*[^_])__($|[^_])', basename)
        if m:
            part = m.group(1)
        else:
            part = basename

        buf = [x[0] for x in tags]

        if 'char-part' in buf:
            idx = buf.index('char-part')
            tags[idx] = ('char-part', part)
        else:
            tags.append(('char-part', part))

        output_rule = asset.check_output_config(tags=tags)
        asset.path_template = asset.evaluate_output(output_rule, proc_non_tag=False, proc_tag=True, tags=tags)


    def getlabel(self):
        return 'Publish parts'
