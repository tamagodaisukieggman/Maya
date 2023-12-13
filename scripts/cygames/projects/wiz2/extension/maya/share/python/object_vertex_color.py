import random

import pymel.core as pm





def create_mesh_list(mesh_set, node=None):

    if node == None:

        nodes = pm.ls(selection=True)

    else:

        nodes = node.getChildren()

    

    for node in nodes:      

        if node.nodeType() == 'mesh':

            mesh_set.add(node)

        create_mesh_list(mesh_set, node)





def apply_color(mesh_set):    

    for i, mesh in enumerate(mesh_set):    

        #random.seed(i)    

        color = [random.random(), random.random(), random.random()]

        pm.select(mesh)

        pm.polyColorPerVertex( rgb=color )





def run():

    nodes = pm.ls(selection=True)

    object_list = set()

    create_mesh_list(object_list)

    apply_color(object_list)

    pm.select(nodes)



