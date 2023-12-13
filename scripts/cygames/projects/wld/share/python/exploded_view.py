import pymel.core as pm





def create_node_list(node_set, node=None):

    if node == None:

        nodes = pm.ls(selection=True)

    else:

        nodes = node.getChildren()

    

    for node in nodes:      

        if node.nodeType() == 'transform' and node.getShape():

            node_set.add(node)

        create_node_list(node_set, node)





def create_obj_dict(obj_list):

    '''

    node name is something like 'export_nomove|low|mdl_gld_bld_corner01_lo|door_nob01_low'

    this function get the last part "door_nob01_low",

    then remove sufiix and get base obj name "door_nob01".

    this base name will be key of the dictionary and contain a list of high and poly models.

    [nt.Transform(u'export_nomove|low|mdl_gld_bld_corner01_lo|door_nob01_low'), nt.Transform(u'export_nomove|high|mdl_gld_bld_corner01_hi|door_nob01_high')]

    

    '''

    obj_dict = dict()

    for i, obj in enumerate(obj_list):

        obj_name = obj.name().split('|')[-1]

        base_obj_name = obj_name.split('_') # exhaust_port01_high

        base_obj_name = '_'.join(base_obj_name[:-1]) # exhaust_port01

        if base_obj_name in obj_dict:

            obj_dict[base_obj_name].append(obj)

        else:

            obj_dict[base_obj_name] = [obj]

    

    return obj_dict



        

def calculate_centroid(node_list=None):

    if node_list == None:

        nodes = pm.ls(selection=True)

    else:

        nodes = node_list



    min = [0,0,0]

    max = [0,0,0]

    for node in nodes:

        for i in range(3):

            if node.boundingBox().min()[i] < min[i]:

                min[i] = node.boundingBox().min()[i]

            if node.boundingBox().max()[i] > max[i]:

                max[i] = node.boundingBox().max()[i]

          

    centroid = pm.datatypes.Vector((min[0]+max[0])/2, (min[0]+max[1])/2, (min[0]+max[2])/2)  

    return centroid    





def set_keyframe(nodes, frame):

    pm.select(nodes)

    pm.setKeyframe(attribute='translate', t=frame)





def remove_keyframe(nodes):

    pm.select(nodes)

    pm.cutKey()





def move_obj(node_dict, centroid_all):

    pm.currentTime(2)

    for key in node_dict.keys():

        #print node_dict[key]

        nodes = node_dict[key]



        centroid = calculate_centroid(nodes) 

        #print centroid



        for node in nodes:

            pos = node.getTranslation()

            new_pos = pos + 10 * (centroid - centroid_all)

            node.setTranslation(new_pos)



        

def run():

    # create node list first   

    nodes = pm.ls(selection=True)

    object_set = set()

    create_node_list(object_set)



    # key default location

    pm.currentTime(1)

    remove_keyframe(object_set)

    set_keyframe(object_set, 1)



    # calculate centroid for entire selection

    centroid_all = calculate_centroid() 



    # create object dictionary for high and low

    objlist = list(object_set)

    obj_dict = create_obj_dict(objlist)



    # move the obj and set keyframe

    move_obj(obj_dict, centroid_all)

    set_keyframe(object_set, 2)

    

    pm.select(nodes)

   

   



   

   

   

   

  

