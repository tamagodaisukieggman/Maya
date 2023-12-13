from maya import cmds, mel
import xml.etree.ElementTree as ET

hik_load_plugins = ['mayaHIK', 'mayaCharacterization', 'OneClick', 'fbxmaya']
for plugin in hik_load_plugins:
    if cmds.pluginInfo(plugin, q=True, l=True) == False:
        cmds.loadPlugin(plugin)

"""
予備のスクリプト
def fileDialog_import(cap=u'File'):
    filename = cmds.fileDialog2(ds=2, cap=cap, okc='Done', ff='All Files (*.*)', fm=1)
    if filename is None:
        return
    return filename[0]


# Affect on Joints
import_joints_filePath = fileDialog_import(u'Select Import Joints')
if import_joints_filePath.endswith('ma'):
    import_xml_filePath = import_joints_filePath.replace('.ma', '.xml')
elif import_joints_filePath.endswith('mb'):
    import_xml_filePath = import_joints_filePath.replace('.mb', '.xml')

# Animation Joints
anim_joints_filePath = fileDialog_import(u'Select Mocap Joints')
if anim_joints_filePath.endswith('ma'):
    anim_xml_filePath = anim_joints_filePath.replace('.ma', '.xml')
elif anim_joints_filePath.endswith('mb'):
    anim_xml_filePath = anim_joints_filePath.replace('.mb', '.xml')
"""

def convert(namespace='male00_all1000_mdl_def:', gender='male', import_joints_filePath=None, import_xml_filePath=None, anim_joints_filePath=None, anim_xml_filePath=None):
    if cmds.namespace(ex='import'):
        cmds.namespace(rm='import', dnc=1, f=1)


    cmds.file("{0}".format(import_joints_filePath), pr=1, ignoreVersion=1, i=1, type="mayaAscii", importTimeRange="combine", mergeNamespacesOnClash=False, options="v=0;", namespace='import')
    cmds.file("{0}".format(anim_joints_filePath), pr=1, ignoreVersion=1, i=1, type="mayaAscii", importTimeRange="combine", mergeNamespacesOnClash=False, options="v=0;")

    defaultHikJoints = {u'Reference': 0,
                         u'Head': 15,
                         u'Hips': 1,
                         u'HipsTranslation': 49,
                         u'LeafLeftArmRoll1': 176,
                         u'LeafLeftArmRoll2': 184,
                         u'LeafLeftArmRoll3': 192,
                         u'LeafLeftArmRoll4': 200,
                         u'LeafLeftArmRoll5': 208,
                         u'LeafLeftForeArmRoll1': 177,
                         u'LeafLeftForeArmRoll2': 185,
                         u'LeafLeftForeArmRoll3': 193,
                         u'LeafLeftForeArmRoll4': 201,
                         u'LeafLeftForeArmRoll5': 209,
                         u'LeafLeftLegRoll1': 173,
                         u'LeafLeftLegRoll2': 181,
                         u'LeafLeftLegRoll3': 189,
                         u'LeafLeftLegRoll4': 197,
                         u'LeafLeftLegRoll5': 205,
                         u'LeafLeftUpLegRoll1': 172,
                         u'LeafLeftUpLegRoll2': 180,
                         u'LeafLeftUpLegRoll3': 188,
                         u'LeafLeftUpLegRoll4': 196,
                         u'LeafLeftUpLegRoll5': 204,
                         u'LeafRightArmRoll1': 178,
                         u'LeafRightArmRoll2': 186,
                         u'LeafRightArmRoll3': 194,
                         u'LeafRightArmRoll4': 202,
                         u'LeafRightArmRoll5': 210,
                         u'LeafRightForeArmRoll1': 179,
                         u'LeafRightForeArmRoll2': 187,
                         u'LeafRightForeArmRoll3': 195,
                         u'LeafRightForeArmRoll4': 203,
                         u'LeafRightForeArmRoll5': 211,
                         u'LeafRightLegRoll1': 175,
                         u'LeafRightLegRoll2': 183,
                         u'LeafRightLegRoll3': 191,
                         u'LeafRightLegRoll4': 199,
                         u'LeafRightLegRoll5': 207,
                         u'LeafRightUpLegRoll1': 174,
                         u'LeafRightUpLegRoll2': 182,
                         u'LeafRightUpLegRoll3': 190,
                         u'LeafRightUpLegRoll4': 198,
                         u'LeafRightUpLegRoll5': 206,
                         u'LeftArm': 9,
                         u'LeftFingerBase': 21,
                         u'LeftFoot': 4,
                         u'LeftFootExtraFinger1': 118,
                         u'LeftFootExtraFinger2': 119,
                         u'LeftFootExtraFinger3': 120,
                         u'LeftFootExtraFinger4': 121,
                         u'LeftFootIndex1': 102,
                         u'LeftFootIndex2': 103,
                         u'LeftFootIndex3': 104,
                         u'LeftFootIndex4': 105,
                         u'LeftFootMiddle1': 106,
                         u'LeftFootMiddle2': 107,
                         u'LeftFootMiddle3': 108,
                         u'LeftFootMiddle4': 109,
                         u'LeftFootPinky1': 114,
                         u'LeftFootPinky2': 115,
                         u'LeftFootPinky3': 116,
                         u'LeftFootPinky4': 117,
                         u'LeftFootRing1': 110,
                         u'LeftFootRing2': 111,
                         u'LeftFootRing3': 112,
                         u'LeftFootRing4': 113,
                         u'LeftFootThumb1': 98,
                         u'LeftFootThumb2': 99,
                         u'LeftFootThumb3': 100,
                         u'LeftFootThumb4': 101,
                         u'LeftForeArm': 10,
                         u'LeftHand': 11,
                         u'LeftHandExtraFinger1': 70,
                         u'LeftHandExtraFinger2': 71,
                         u'LeftHandExtraFinger3': 72,
                         u'LeftHandExtraFinger4': 73,
                         u'LeftHandIndex1': 54,
                         u'LeftHandIndex2': 55,
                         u'LeftHandIndex3': 56,
                         u'LeftHandIndex4': 57,
                         u'LeftHandMiddle1': 58,
                         u'LeftHandMiddle2': 59,
                         u'LeftHandMiddle3': 60,
                         u'LeftHandMiddle4': 61,
                         u'LeftHandPinky1': 66,
                         u'LeftHandPinky2': 67,
                         u'LeftHandPinky3': 68,
                         u'LeftHandPinky4': 69,
                         u'LeftHandRing1': 62,
                         u'LeftHandRing2': 63,
                         u'LeftHandRing3': 64,
                         u'LeftHandRing4': 65,
                         u'LeftHandThumb1': 50,
                         u'LeftHandThumb2': 51,
                         u'LeftHandThumb3': 52,
                         u'LeftHandThumb4': 53,
                         u'LeftInFootExtraFinger': 163,
                         u'LeftInFootIndex': 159,
                         u'LeftInFootMiddle': 160,
                         u'LeftInFootPinky': 162,
                         u'LeftInFootRing': 161,
                         u'LeftInFootThumb': 158,
                         u'LeftInHandExtraFinger': 151,
                         u'LeftInHandIndex': 147,
                         u'LeftInHandMiddle': 148,
                         u'LeftInHandPinky': 150,
                         u'LeftInHandRing': 149,
                         u'LeftInHandThumb': 146,
                         u'LeftLeg': 3,
                         u'LeftShoulder': 18,
                         u'LeftShoulderExtra': 170,
                         u'LeftToeBase': 16,
                         u'LeftUpLeg': 2,
                         u'Neck': 20,
                         u'Neck1': 32,
                         u'Neck2': 33,
                         u'Neck3': 34,
                         u'Neck4': 35,
                         u'Neck5': 36,
                         u'Neck6': 37,
                         u'Neck7': 38,
                         u'Neck8': 39,
                         u'Neck9': 40,
                         u'RightArm': 12,
                         u'RightFingerBase': 22,
                         u'RightFoot': 7,
                         u'RightFootExtraFinger1': 142,
                         u'RightFootExtraFinger2': 143,
                         u'RightFootExtraFinger3': 144,
                         u'RightFootExtraFinger4': 145,
                         u'RightFootIndex1': 126,
                         u'RightFootIndex2': 127,
                         u'RightFootIndex3': 128,
                         u'RightFootIndex4': 129,
                         u'RightFootMiddle1': 130,
                         u'RightFootMiddle2': 131,
                         u'RightFootMiddle3': 132,
                         u'RightFootMiddle4': 133,
                         u'RightFootPinky1': 138,
                         u'RightFootPinky2': 139,
                         u'RightFootPinky3': 140,
                         u'RightFootPinky4': 141,
                         u'RightFootRing1': 134,
                         u'RightFootRing2': 135,
                         u'RightFootRing3': 136,
                         u'RightFootRing4': 137,
                         u'RightFootThumb1': 122,
                         u'RightFootThumb2': 123,
                         u'RightFootThumb3': 124,
                         u'RightFootThumb4': 125,
                         u'RightForeArm': 13,
                         u'RightHand': 14,
                         u'RightHandExtraFinger1': 94,
                         u'RightHandExtraFinger2': 95,
                         u'RightHandExtraFinger3': 96,
                         u'RightHandExtraFinger4': 97,
                         u'RightHandIndex1': 78,
                         u'RightHandIndex2': 79,
                         u'RightHandIndex3': 80,
                         u'RightHandIndex4': 81,
                         u'RightHandMiddle1': 82,
                         u'RightHandMiddle2': 83,
                         u'RightHandMiddle3': 84,
                         u'RightHandMiddle4': 85,
                         u'RightHandPinky1': 90,
                         u'RightHandPinky2': 91,
                         u'RightHandPinky3': 92,
                         u'RightHandPinky4': 93,
                         u'RightHandRing1': 86,
                         u'RightHandRing2': 87,
                         u'RightHandRing3': 88,
                         u'RightHandRing4': 89,
                         u'RightHandThumb1': 74,
                         u'RightHandThumb2': 75,
                         u'RightHandThumb3': 76,
                         u'RightHandThumb4': 77,
                         u'RightInFootExtraFinger': 169,
                         u'RightInFootIndex': 165,
                         u'RightInFootMiddle': 166,
                         u'RightInFootPinky': 168,
                         u'RightInFootRing': 167,
                         u'RightInFootThumb': 164,
                         u'RightInHandExtraFinger': 157,
                         u'RightInHandIndex': 153,
                         u'RightInHandMiddle': 154,
                         u'RightInHandPinky': 156,
                         u'RightInHandRing': 155,
                         u'RightInHandThumb': 152,
                         u'RightLeg': 6,
                         u'RightShoulder': 19,
                         u'RightShoulderExtra': 171,
                         u'RightToeBase': 17,
                         u'RightUpLeg': 5,
                         u'Spine': 8,
                         u'Spine1': 23,
                         u'Spine2': 24,
                         u'Spine3': 25,
                         u'Spine4': 26,
                         u'Spine5': 27,
                         u'Spine6': 28,
                         u'Spine7': 29,
                         u'Spine8': 30,
                         u'Spine9': 31}


    hiks = cmds.ls('*HIK*')
    for obj in hiks:
        if cmds.objExists(obj):
            cmds.delete(obj)

    # アニメーションをimportする骨への割り当て
    dst_tree = ET.parse("{0}".format(import_xml_filePath))
    dst_root = dst_tree.getroot()

    mel.eval('HIKCharacterControlsTool;')

    mel.eval('hikCreateCharacter( "import_character" )')
    for i in range(len(dst_root[0])):
        try:
            if dst_root[0][i].get('value') != '':
                try:
                    print(dst_root[0][i].get('value'), defaultHikJoints[dst_root[0][i].get('key')])
                    mel.eval('setCharacterObject("import:{0}","import_character",{1},0);'.format(dst_root[0][i].get('value'), defaultHikJoints[dst_root[0][i].get('key')]))
                except KeyError:
                    pass
        except RuntimeError:
            pass
    mel.eval('$gCurrentCharacter = "import_character";refreshAllCharacterLists();hikToggleLockDefinition();')


    # アニメーションされている骨への割り当て
    dst_tree = ET.parse("{0}".format(anim_xml_filePath))
    dst_root = dst_tree.getroot()

    mel.eval('HIKCharacterControlsTool;')

    mel.eval('hikCreateCharacter( "anim_character" )')
    for i in range(len(dst_root[0])):
        try:
            if dst_root[0][i].get('value') != '':
                try:
                    print(dst_root[0][i].get('value'), defaultHikJoints[dst_root[0][i].get('key')])
                    mel.eval('setCharacterObject("{0}","anim_character",{1},0);'.format(dst_root[0][i].get('value'), defaultHikJoints[dst_root[0][i].get('key')]))
                except KeyError:
                    pass
        except RuntimeError:
            pass
    mel.eval('$gCurrentCharacter = "anim_character";refreshAllCharacterLists();hikToggleLockDefinition();')


    def matchConstraint(currentNamespace='', jointNamepace='', gender='male'):
        def constraint_convert(src, dst, pos, rot, scl, mo):
            print(src, dst)
            cnsts = []
            if pos:
                cnst = cmds.pointConstraint(src, dst, w=1, mo=mo)
                cnsts.append(cnst)
            if rot:
                if ('fk_forearmL_ctl' in dst
                    or 'fk_forearmR_ctl' in dst
                    or 'fk_legL_ctl' in dst
                    or 'fk_legR_ctl' in dst):
                    cnst = cmds.orientConstraint(src, dst, w=1, mo=mo, sk=['x', 'z'])
                    cnsts.append(cnst)
                else:
                    cnst = cmds.orientConstraint(src, dst, w=1, mo=mo)
                    cnsts.append(cnst)
            if scl:
                cnst = cmds.scaleConstraint(src, dst, w=1, mo=mo)
                cnsts.append(cnst)

            return cnsts

        def constraint_convert_ik_pv(dst, pos, rot, scl, mo, start, mid, end, move):
            print(dst)
            cnsts = []

            # start, mid, end = 'uplegL_jnt', 'legL_jnt', 'footL_jnt'

            loc1 = cmds.spaceLocator()
            loc2 = cmds.duplicate(loc1)
            loc3 = cmds.duplicate(loc1)
            cmds.parent(loc3, loc2)
            cmds.parent(loc2, loc1)

            cmds.pointConstraint(start, loc1, w=1)
            cmds.pointConstraint(end, loc1, w=1)

            if ('forearmL_ctl' in dst
                or 'forearmR_ctl' in dst):
                cmds.move(0, 0, 5, r=1, os=1, wd=1)
                cmds.aimConstraint(mid, loc2, w=1, aim=(0,0,-1), u=(0,1,0), wut='vector', wu=(0,1,0))
                cmds.move(0, 0, move*-1, loc3, r=1, os=1, wd=1)


            elif ('legL_ctl' in dst
                or 'legR_ctl' in dst):
                cmds.move(0, 0, -15, loc2, r=1, os=1, wd=1)
                cmds.aimConstraint(mid, loc2, w=1, aim=(0,0,1), u=(0,1,0), wut='vector', wu=(0,1,0))
                cmds.move(0, 0, move, loc3, r=1, os=1, wd=1)

            cnsts.append(loc1)

            src = loc3[0]

            if pos:
                cnst = cmds.pointConstraint(src, dst, w=1, mo=mo)
                cnsts.append(cnst)
            if rot:
                cnst = cmds.orientConstraint(src, dst, w=1, mo=mo)
                cnsts.append(cnst)
            if scl:
                cnst = cmds.scaleConstraint(src, dst, w=1, mo=mo)
                cnsts.append(cnst)

            return cnsts

        source_joints = [u'root_jnt',
         u'cog_jnt',
         u'spine_01_jnt',
         u'spine_02_jnt',
         u'spine_03_jnt',
         u'neck_jnt',
         u'head_jnt',
         u'shoulderL_jnt',
         u'armL_jnt',
         u'forearmL_jnt',
         u'handL_jnt',
         u'handWeaponL_offset_jnt',
         u'handWeaponL_bind_jnt',
         u'shoulderR_jnt',
         u'armR_jnt',
         u'forearmR_jnt',
         u'handR_jnt',
         u'handWeaponR_offset_jnt',
         u'handWeaponR_bind_jnt',
         u'hip_jnt',
         u'uplegL_jnt',
         u'legL_jnt',
         u'footL_jnt',
         u'toebaseL_jnt',
         u'uplegR_jnt',
         u'legR_jnt',
         u'footR_jnt',
         u'toebaseR_jnt']


        match_ctrls = OrderedDict()
        match_ctrls[currentNamespace+'root_ctl'] = [jointNamepace+'root_jnt', 1, 1, 0, 1]
        match_ctrls[currentNamespace+'cog_ctl'] = [jointNamepace+'cog_jnt', 1, 1, 0, 1]
        match_ctrls[currentNamespace+'hip_ctl'] = [jointNamepace+'hip_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'spine_01_ctl'] = [jointNamepace+'spine_01_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'spine_02_ctl'] = [jointNamepace+'spine_02_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'spine_03_ctl'] = [jointNamepace+'spine_03_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'neck_ctl'] = [jointNamepace+'neck_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'head_ctl'] = [jointNamepace+'head_jnt', 0, 1, 0, 1]

        # IK arm
        match_ctrls[currentNamespace+'shoulderL_ctl'] = [jointNamepace+'shoulderL_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'handL_ctl'] = [jointNamepace+'handL_jnt', 1, 0, 0, 1]
        match_ctrls[currentNamespace+'handL_rot_ctl'] = [jointNamepace+'handL_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_con_armL_loc'] = [jointNamepace+'armL_jnt', 1, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_con_forearmL_loc'] = [jointNamepace+'forearmL_jnt', 1, 1, 0, 1]

        match_ctrls[currentNamespace+'shoulderR_ctl'] = [jointNamepace+'shoulderR_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'handR_ctl'] = [jointNamepace+'handR_jnt', 1, 0, 0, 1]
        match_ctrls[currentNamespace+'handR_rot_ctl'] = [jointNamepace+'handR_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_con_armR_loc'] = [jointNamepace+'armR_jnt', 1, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_con_forearmR_loc'] = [jointNamepace+'forearmR_jnt', 1, 1, 0, 1]

        # IK arm pv
        match_ctrls[currentNamespace+'forearmL_ctl'] = [1, 0, 0, 0, jointNamepace+'armL_jnt', jointNamepace+'forearmL_jnt', jointNamepace+'handL_jnt', 60]
        match_ctrls[currentNamespace+'forearmR_ctl'] = [1, 0, 0, 0, jointNamepace+'armR_jnt', jointNamepace+'forearmR_jnt', jointNamepace+'handR_jnt', 60]


        # FK arm
        match_ctrls[currentNamespace+'fk_armL_ctl'] = [jointNamepace+'armL_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_forearmL_ctl'] = [jointNamepace+'forearmL_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_handL_ctl'] = [jointNamepace+'handL_jnt', 0, 1, 0, 1]

        match_ctrls[currentNamespace+'fk_armR_ctl'] = [jointNamepace+'armR_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_forearmR_ctl'] = [jointNamepace+'forearmR_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_handR_ctl'] = [jointNamepace+'handR_jnt', 0, 1, 0, 1]


        # IK leg
        match_ctrls[currentNamespace+'footL_ctl'] = [jointNamepace+'footL_jnt', 1, 1, 0, 1]
        match_ctrls[currentNamespace+'toebaseL_ctl'] = [jointNamepace+'toebaseL_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_con_uplegL_loc'] = [jointNamepace+'uplegL_jnt', 1, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_con_legL_loc'] = [jointNamepace+'legL_jnt', 1, 1, 0, 1]

        match_ctrls[currentNamespace+'footR_ctl'] = [jointNamepace+'footR_jnt', 1, 1, 0, 1]
        match_ctrls[currentNamespace+'toebaseR_ctl'] = [jointNamepace+'toebaseR_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_con_uplegR_loc'] = [jointNamepace+'uplegR_jnt', 1, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_con_legR_loc'] = [jointNamepace+'legR_jnt', 1, 1, 0, 1]

        # IK leg pv
        match_ctrls[currentNamespace+'legL_ctl'] = [1, 0, 0, 0, jointNamepace+'uplegL_jnt', jointNamepace+'legL_jnt', jointNamepace+'footL_jnt', 60]
        match_ctrls[currentNamespace+'legR_ctl'] = [1, 0, 0, 0, jointNamepace+'uplegR_jnt', jointNamepace+'legR_jnt', jointNamepace+'footR_jnt', 60]


        # FK leg
        match_ctrls[currentNamespace+'fk_uplegL_ctl'] = [jointNamepace+'uplegL_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_legL_ctl'] = [jointNamepace+'legL_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_footL_ctl'] = [jointNamepace+'footL_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_toebaseL_ctl'] = [jointNamepace+'toebaseL_jnt', 0, 1, 0, 1]

        match_ctrls[currentNamespace+'fk_uplegR_ctl'] = [jointNamepace+'uplegR_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_legR_ctl'] = [jointNamepace+'legR_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_footR_ctl'] = [jointNamepace+'footR_jnt', 0, 1, 0, 1]
        match_ctrls[currentNamespace+'fk_toebaseR_ctl'] = [jointNamepace+'toebaseR_jnt', 0, 1, 0, 1]

        # Weapons
        match_ctrls[currentNamespace+'handWeaponL_offset_ctl'] = [jointNamepace+'handWeaponL_offset_jnt', 1, 1, 1, 0]
        match_ctrls[currentNamespace+'handWeaponR_offset_ctl'] = [jointNamepace+'handWeaponR_offset_jnt', 1, 1, 1, 0]

        match_ctrls[currentNamespace+'handWeaponL_ctl'] = [jointNamepace+'handWeaponL_bind_jnt', 1, 1, 1, 0]
        match_ctrls[currentNamespace+'handWeaponR_ctl'] = [jointNamepace+'handWeaponR_bind_jnt', 1, 1, 1, 0]



        for jnt in source_joints:
            cmds.xform(jointNamepace+jnt, ro=[0, 0, 0], a=1)

        # root cog zero out
        cmds.xform(jointNamepace+'root_jnt', t=[0, 0, 0], a=1)

        if 'male' in gender:
            cmds.xform(jointNamepace+'cog_jnt', t=[0, 103.400, 0], a=1)

            # weapon
            if cmds.objExists(jointNamepace+'handWeaponL_offset_jnt'):
                cmds.xform(jointNamepace+'handWeaponL_offset_jnt', t=[7.300, -2.400, 0.0], a=1)
            if cmds.objExists(jointNamepace+'handWeaponR_offset_jnt'):
                cmds.xform(jointNamepace+'handWeaponR_offset_jnt', t=[7.300, 2.400, 0.0], a=1)

            if cmds.objExists(jointNamepace+'handWeaponL_bind_jnt'):
                cmds.xform(jointNamepace+'handWeaponL_bind_jnt', t=[0, 0, 0], a=1)
            if cmds.objExists(jointNamepace+'handWeaponR_bind_jnt'):
                cmds.xform(jointNamepace+'handWeaponR_bind_jnt', t=[0, 0, 0], a=1)

        if 'female' in gender:
            cmds.xform(jointNamepace+'cog_jnt', t=[0, 101.147, 1.688], a=1)

            # weapon
            if cmds.objExists(jointNamepace+'handWeaponL_offset_jnt'):
                cmds.xform(jointNamepace+'handWeaponL_offset_jnt', t=[7.456, 0.0, 0.0], a=1)
            if cmds.objExists(jointNamepace+'handWeaponR_offset_jnt'):
                cmds.xform(jointNamepace+'handWeaponR_offset_jnt', t=[-7.456, 0.0, 0.0], a=1)

            if cmds.objExists(jointNamepace+'handWeaponL_bind_jnt'):
                cmds.xform(jointNamepace+'handWeaponL_bind_jnt', t=[0, 0, 0], a=1)
            if cmds.objExists(jointNamepace+'handWeaponR_bind_jnt'):
                cmds.xform(jointNamepace+'handWeaponR_bind_jnt', t=[0, 0, 0], a=1)

        # const sets
        if not cmds.objExists('bake_cnst_sets'):
            cmds.sets(em=1, n='bake_cnst_sets')


        ik_pv_ctrls = [currentNamespace+'forearmL_ctl',
                       currentNamespace+'forearmR_ctl',
                       currentNamespace+'legL_ctl',
                       currentNamespace+'legR_ctl']

        bake_ctrls = []
        for ctrl, jnt_value in match_ctrls.items():
            bake_ctrls.append(ctrl)
            if ('fk_con_armL_loc' in ctrl
                or 'fk_con_forearmL_loc' in ctrl
                or 'fk_con_armR_loc' in ctrl
                or 'fk_con_forearmR_loc' in ctrl
                or 'fk_con_uplegL_loc' in ctrl
                or 'fk_con_legL_loc' in ctrl
                or 'fk_con_uplegR_loc' in ctrl
                or 'fk_con_legR_loc' in ctrl):
                    cmds.xform(ctrl, t=[0, 0, 0], ro=[0, 0, 0], a=1)

            try:
                if ctrl in ik_pv_ctrls:
                    cnsts = constraint_convert_ik_pv(ctrl,
                                                     jnt_value[0],
                                                     jnt_value[1],
                                                     jnt_value[2],
                                                     jnt_value[3],
                                                     jnt_value[4],
                                                     jnt_value[5],
                                                     jnt_value[6],
                                                     jnt_value[7])
                else:
                    cnsts = constraint_convert(jnt_value[0], ctrl, jnt_value[1], jnt_value[2], jnt_value[3], jnt_value[4])
                for ccnn in cnsts:
                    cmds.sets(ccnn, add='bake_cnst_sets')
            except Exception as e:
                print(e)


    # --------------
    # worldのリグに対しての処理
    # --------------
    matchConstraint(currentNamespace=namespace, jointNamepace='import:', gender=gender)

    # sourceの切替 anim_characterからimport_characterへの割り当て
    mel.eval("""
    $gCurrentCharacter = "import_character";
    refreshAllCharacterLists();
    //optionMenuGrp -e -v "import_character" hikCharacterList;
    //hikUpdateCurrentCharacterFromUI();
    //hikUpdateContextualUI();
    $gCurrentCharacter = "anim_character";
    refreshAllCharacterLists();
    mayaHIKsetCharacterInput( "import_character","anim_character" );
    //refreshAllSourceLists();
    //optionMenuGrp -e -v " anim_character" hikSourceList;
    //hikUpdateCurrentSourceFromUI;
    //hikUpdateContextualUI;
    refreshAllCharacterLists();""")
