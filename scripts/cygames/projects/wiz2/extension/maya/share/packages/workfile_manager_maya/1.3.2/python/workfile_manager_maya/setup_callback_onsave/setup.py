import maya.api.OpenMaya as om
from maya import cmds

def embed_scene_desc(client_data):
    from workman_world_custom.export_postproc.maya.animation import postproc_update_plot_rig_anim_work
    presets = eval(postproc_update_plot_rig_anim_work.export_presets(None))
    print('presets: ', presets)

    object_sets = []
    for set_ in cmds.ls(type='objectSet'):
        if cmds.objectType(set_) == 'shadingEngine':
            continue
        if not cmds.attributeQuery('postproc_edit_set__name', n=set_, ex=True) and not cmds.attributeQuery('postproc_edit_set__operator_name', n=set_, ex=True):
            continue
            
        members = cmds.sets(set_, q=True)
        if members is None:
            members = []
        params = []
        for attr in cmds.listAttr(set_):
            if attr.startswith('postproc_edit_set__'):
                v = cmds.getAttr(set_+'.'+attr)
                params.append((attr, v))
        d = {'name':set_, 'members':members, 'params':params}
        object_sets.append(d)

    refs = {}
    for ref in cmds.ls(type='reference'):
        try:
            filename = cmds.reference(rfn=ref, f=True, q=True)
        except:
            filename = None
        refs[ref] = filename

    desc = {'sets':presets, 'object_sets':object_sets, 'textures':[], 'references':refs}
    print('desc: ', desc)

    cmds.fileInfo('workman_scene_desc', str(desc))



om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeSave, embed_scene_desc)
print('Callback setup !!!!!!!!!!!!!!!!!!!')

