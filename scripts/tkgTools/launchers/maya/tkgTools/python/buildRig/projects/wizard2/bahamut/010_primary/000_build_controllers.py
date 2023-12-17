# -*- coding: utf-8 -*-
from imp import reload
import os
import traceback

import maya.cmds as cmds
import maya.mel as mel

import buildRig.root as brRoot
import buildRig.fk as brFk
reload(brRoot)
reload(brFk)

##############
# chr reference
namespace = 'chr'
rig_chara_ref_dict = {
    'bahamut':"F:/myTechData/Maya/sandbox/cygames/wizard2/chr/bahamut/maya/Bahamut.ma"
}
if rig_setup_id in rig_chara_ref_dict.keys():
    ref_path = rig_chara_ref_dict[rig_setup_id]

cmds.file(ref_path, ignoreVersion=True, namespace=namespace, r=True, gl=True, mergeNamespacesOnClash=True, options="v=0;")

##############
# root setup
# roots
root_joints = ['Global', 'Local', 'Root']

try:
    root = brRoot.Root(module='root',
                 side='Cn',
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 joints=root_joints,
                 namespace=namespace,
                 shapes=['gnomon', 'pacman', 'arrow_one_way_z'],
                 axis=[0,0,0],
                 scale=3000,
                 scale_step=-500,
                 prefix=None)
except:
    print(traceback.format_exc())

root.base_connection()

##############
# FK setup
# tails
tail_joints = ['Tail_01',
 'Tail_02',
 'Tail_03',
 'Tail_04',
 'Tail_05',
 'Tail_06',
 'Tail_07',
 'Tail_08']
tail_fk = brFk.Fk(module='tail',
             side='Cn',
             rig_joints_parent=None,
             rig_ctrls_parent=None,
             joints=tail_joints,
             namespace=namespace,
             shape='cube_pointer',
             axis=[0,90,0],
             scale=1000,
             scale_step=-90,
             prefix='FK_')

tail_fk.connect_children()
tail_fk.base_connection()



##############
# chr parent MODEL
ref_top_nodes = cmds.ls(rn=True, assemblies=True)
[cmds.parent(rfn, 'MODEL') for rfn in ref_top_nodes]