mp = 'C:/Users/tkgill/Documents/maya/projects/ASSETS/ninja/model/ninja_model.mb'
gp = 'C:/Users/tkgill/Documents/maya/projects/ASSETS/ninja/guides/ninja_guides.mb'

import tkgRigBuild.build.buildPart as tkgPart
reload(tkgPart)
cmds.file(new=True, f=True)
root = tkgPart.build_module(module_type='root', side='Cn', part='root', 
                           model_path=mp, guide_path=gp)
cmds.viewFit('perspShape', fitFactor=1, all=True, animate=True)

hip = tkgPart.build_module(module_type='hip', side='Cn', part='hip',
                          guide_list=['Hips'], offset_hip=-0.5,
                          ctrl_scale=55)
                          
chest = tkgPart.build_module(module_type='chest', side='Cn', part='chest',
                            guide_list=['Spine2'], ctrl_scale=55)
                            
spine = tkgPart.build_module(module_type='spine', side='Cn', part='spine', 
                            guide_list=['Hips', 'Spine', 'Spine1', 'Spine2'], ctrl_scale=1)

neck = tkgPart.build_module(module_type='neck', side='Cn', part='neck',
                           guide_list=['Neck', 'Neck1', 'Head'], ctrl_scale=1)
                           
head = tkgPart.build_module(module_type='head', side='Cn', part='head',
                           guide_list=['Head'], ctrl_scale=5)
                            
for s in ['Lf', 'Rt']:
    if s == 'Lf':
        fs = 'Left'
    else:
        fs = 'Right'
    arm = tkgPart.build_module(module_type='bipedLimb',
                              side=s,
                              part='arm',
                              guide_list=[fs + 'Arm', fs + 'ForeArm', fs + 'Hand'],
                              offset_pv=30,
                              ctrl_scale=15)
    clav = tkgPart.build_module(module_type='clavicle',
                               side=s,
                               part='clavicle',
                               guide_list=[fs + 'Shoulder', fs + 'Arm'],
                               local_orient=True,
                               ctrl_scale=9)
    leg = tkgPart.build_module(module_type='bipedLimb',
                              side=s,
                              part='leg',
                              guide_list=[fs + 'UpLeg', fs + 'Leg', fs + 'Foot'],
                              offset_pv=60,
                              ctrl_scale=10)
    hand = tkgPart.build_module(module_type='hand',
                               side=s,
                               part='hand',
                               guide_list=[fs + 'Hand'],
                               ctrl_scale=8)
    foot = tkgPart.build_module(module_type='foot',
                               side=s,
                               part='foot',
                               guide_list=[fs + 'Foot', fs + 'ToeBase', fs + 'Toe_End'],
                               ctrl_scale=10,
                               toe_piv=fs + 'ToePiv',
                               heel_piv=fs + 'HeelPiv',
                               in_piv=fs + 'In',
                               out_piv=fs + 'Out')
    pinky = tkgPart.build_module(module_type='finger',
                                side=s,
                                part='pinky',
                                guide_list=[fs + 'HandPinky1', fs + 'HandPinky2', fs + 'HandPinky3', fs + 'HandPinky4'],
                                ctrl_scale=2)
    ring = tkgPart.build_module(module_type='finger',
                                side=s,
                                part='ring',
                                guide_list=[fs + 'HandRing1', fs + 'HandRing2', fs + 'HandRing3', fs + 'HandRing4'],
                                ctrl_scale=2)
    middle = tkgPart.build_module(module_type='finger',
                                side=s,
                                part='middle',
                                guide_list=[fs + 'HandMiddle1', fs + 'HandMiddle2', fs + 'HandMiddle3', fs + 'HandMiddle4'],
                                ctrl_scale=2)
    index = tkgPart.build_module(module_type='finger',
                                side=s,
                                part='index',
                                guide_list=[fs + 'HandIndex1', fs + 'HandIndex2', fs + 'HandIndex3', fs + 'HandIndex4'],
                                ctrl_scale=2)
    thumb = tkgPart.build_module(module_type='finger',
                                side=s,
                                part='thumb',
                                guide_list=[fs + 'HandThumb1', fs + 'HandThumb2', fs + 'HandThumb3', fs + 'HandThumb4'],
                                ctrl_scale=2)



import tkgRigBuild.post.finalize as tkgFinalize
import tkgRigBuild.post.dataIO.controls as tkgCtrlIO
import tkgRigBuild.post.dataIO.weights as tkgWeights
reload(tkgFinalize)
reload(tkgWeights)
reload(tkgCtrlIO)
tkgFinalize.finalize_rig()

'''
# write data
tkgCtrlIO.write_controls('C:/Users/tkgill/Documents/maya/projects/ASSETS/ninja/control_data/', force=True)
tkgWeights.write_skin('C:/Users/tkgill/Documents/maya/projects/ASSETS/ninja/weight_data/', force=True)
'''

# read data
tkgCtrlIO.read_controls('C:/Users/tkgill/Documents/maya/projects/ASSETS/ninja/control_data/control_curves.json')
tkgWeights.read_skin('C:/Users/tkgill/Documents/maya/projects/ASSETS/ninja/weight_data/')


# initial bind
'''
# get bind joints
bind_joints = [bj.split('.')[0] for bj in cmds.ls('*.bindJoint')]
# cmds.select(bind_joints, r=True)

geo = cmds.ls('*GEO')
for g in geo:
    cmds.skinCluster(bind_joints, g, tsb=True)
'''


cmds.file('C:/Users/tkgill/Documents/maya/projects/ASSETS/ninja/anim/breakdance.fbx', i=True, type='FBX')

import tkgRigBuild.post.mocap as tkgMocap
reload(tkgMocap)

tkgMocap.build_mocap_rig()

tkgMocap.connect_to_mocap()

# tkgMocap.align_skeletons()

# tkgMocap.bake_to_controls()



