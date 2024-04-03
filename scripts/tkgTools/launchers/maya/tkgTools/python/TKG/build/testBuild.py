# -*- coding: utf-8 -*-
from imp import reload
import TKG.library.rigJoints as tkgRigJoints
import TKG.library.ik as tkgIk
reload(tkgRigJoints)
reload(tkgIk)

limb_joints = tkgRigJoints.create_limb_joints(nodes=None,
                       blend_prefix='',
                       blend_suffix='',
                       blend_replace=['BIND_', 'BLEND_'],
                       first_segments_num=8,
                       second_segments_num=8,
                       fk_prefix='',
                       fk_suffix='',
                       fk_replace=['BIND_', 'FK_'],
                       ik_prefix='',
                       ik_suffix='',
                       ik_replace=['BIND_', 'IK_'])


tkgIk.create_RP_ikHandle(limb_joints[2][0], limb_joints[2][-1])