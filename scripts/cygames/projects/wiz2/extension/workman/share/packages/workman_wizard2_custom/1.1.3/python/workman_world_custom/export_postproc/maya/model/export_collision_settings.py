from __future__ import print_function
try:
    import maya.cmds as cmds
except:
    pass

import json
import os
import re

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

def get_json_path_from_masterfile(masterfile):
    dirname = os.path.dirname(masterfile)
    outdir = re.sub('[/][^/]+$', '/json', dirname)
    basename = os.path.basename(masterfile)
    basename0 = basename[:basename.rindex('.')]
    m = re.search('(.*)_(v\d{3})$', basename0)
    if m:
        outname = '%s_physics_data_%s.json' % (m.group(1), m.group(2))
    else:
        outname = basename0 + '_physics_data.json'

    return outdir + '/' + outname


class Plugin(PostProcBase):
    def application(self):
        return Application.Maya

    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        if asset.assetgroup == 'environment' and asset.task == 'model':
            return True
        else:
            return False

    def order(self):
        return 20000

    def execute(self, args):
        def separate_enumlist(enumlist):
            return enumlist[0].split(":")
        
        #order
        all = cmds.ls(dag = True)
        def getOrder(findItem):
            return all.index(findItem)

        outfile = args['outfile']
        
        #get selection
        selection = args['global_args']['selection']
        gargs = args['global_args']
        if 'additional_select' in gargs:
            selection.extend(gargs['additional_select'])

        selectionTransforms = []
        #collision
        children = []
        for lp in selection:
            try:
                if "transform" == cmds.objectType(lp):
                    selectionTransforms.append(lp)
            except:
                continue
    
        children = cmds.listRelatives(selectionTransforms,ad=True,type="transform",pa=True)
        
        if children == None:
            children = selectionTransforms
        else:
            children.extend(selectionTransforms)
        
        selectionAndChildren = children
        if selectionAndChildren == None:
            return 0

        geoTransforms = []
        for selectChild in selectionAndChildren:
            if not cmds.objExists(selectChild):
                continue
            children = cmds.listRelatives(selectChild,c=True,pa=True)
            if children != None:
                for lp in children:
                    if cmds.objectType(lp) == "mesh" and cmds.objectType(selectChild) != "objectSet":
                        if cmds.getAttr('%s.intermediateObject' % lp) != 1:
                            geoTransforms.append(selectChild)
                            break
        colsets = cmds.ls("col_*",type ="objectSet")
        #topIndex = -1
        mesh_dict = {}
        render_meshes = []
        exist_all_node = False
        for geoTransform in geoTransforms:
            nodeName = geoTransform
            visibility = True
            parent     = False
            collision_presets = "BlockAll"
            is_collision = False

            is_skip = 0

            if cmds.objExists("UBX_*{}_*".format(geoTransform)) or cmds.objExists("UCX_*{}_*".format(geoTransform)):
                collisions = cmds.ls("UBX_*{}_*".format(geoTransform))
                collisions.extend(cmds.ls("UCX_*{}_*".format(geoTransform)))
                if collisions != []:
                    for colset in colsets:
                        if cmds.sets(collisions[0],isMember = colset):
                            collision_presets = cmds.attributeQuery( 'collisionNames', node=colset, listEnum=True )
                            collision_presets = separate_enumlist(collision_presets)[cmds.getAttr("{}.collisionNames".format(colset))]

            pattern = re.compile("(UCX|UBX)_(.*?)_(\d{1,5})")
                #Check collision assets. 
            if re.search(pattern,str(geoTransform)):
                is_skip = 1
                is_collision = True
                
            if is_skip:
                continue

            shapes = cmds.listRelatives(geoTransform,c=True,type="mesh",pa=True)
            SG = cmds.listConnections(shapes, s=False, d=True, t='shadingEngine')
            materials = set(cmds.ls(cmds.listConnections(SG, s=True, d=False), mat=True))
            nodetype = "mesh"
            collision_type = "simple"
            simple_phys_material = tuple(materials)[0]
            
            if "COMPLEX_" in nodeName:
                simple_phys_material = None
                collision_type = "complex"

            #dummyMesh
            if is_collision == False:
                if tuple(materials)[0].startswith("phx_"):
                    visibility = False
                
                #RenderMesh
                else:
                   simple_phys_material = None
                   render_meshes.append(nodeName)

            if nodeName == "all":
                parent = True
                exist_all_node = True

            mesh_dict[nodeName] = {
                            "node_type" : nodetype,
                            "visibility" : visibility,
                            "parent": parent,
                            "collision_presets": collision_presets,
                            "materials":tuple(materials),
                            "collision_type" : collision_type,
                            "simple_phys_material":simple_phys_material
                            }
            
        else:
            print("exist_all_node>>"+str(exist_all_node))
            print("render_meshes>>"+str(render_meshes))
            if exist_all_node == False and len(render_meshes) >= 1:
                mesh_dict[render_meshes[0]]["parent"] = True
                cmds.warning(u"Does not exist node name 'all'.Substitute the '{}'".format(render_meshes[0]))

        #materials
        mats = cmds.ls(type = "lambert")
        material_dict = {}
        for lp in mats:
            try:
                attributeFlags = cmds.getAttr(lp+'.attributeFlags').split(",")
                materialName = cmds.attributeQuery( 'materialNames', node=lp, listEnum=True )
                materialName = separate_enumlist(materialName)[cmds.getAttr("{}.materialNames".format(lp))]
                material_dict[lp] = {
                    "node_type" : "material",
                    "attributeFlags": attributeFlags,
                    "materialName": materialName,
                    }                
            except (RuntimeError,ValueError) :
                material_dict[lp] = {
                    "node_type" : "material",
                    "attributeFlags": None,
                    "materialName": None,
                    }    
                continue

        json_file_path = get_json_path_from_masterfile(outfile)

        export_dict = {}
        export_dict["mesh_datas"] = {
            "node_type" : "group",
            "datas" : mesh_dict 
            }
        
        export_dict["materials"]  = {
            "node_type" : "group",
            "datas" : material_dict
            }

        output_path = os.path.dirname(json_file_path)
        if os.path.isdir(output_path) == False:
            os.makedirs(output_path)
        with open(json_file_path, 'w') as f:
            json.dump(export_dict, f, indent=4)

        #delete colsets 
        cmds.delete(colsets)
        for colset in colsets:
            if colset in args['global_args']['selection']:
                args['global_args']['selection'].remove(str(colset))

        #export json file path.
        self.set_outputs([json_file_path])

    def getlabel(self):
        return 'Export collision settings'

    def default_checked(self):
        return True

    def is_editable(self):
        return False