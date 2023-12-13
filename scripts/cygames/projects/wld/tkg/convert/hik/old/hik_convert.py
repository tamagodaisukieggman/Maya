from maya import cmds, mel
import xml.etree.ElementTree as ET

if cmds.pluginInfo('mayaHIK', q=True, l=True) == False:
    cmds.loadPlugin("mayaHIK")
if cmds.pluginInfo('mayaCharacterization', q=True, l=True) == False:
    cmds.loadPlugin("mayaCharacterization")
if cmds.pluginInfo('OneClick', q=True, l=True) == False:
    cmds.loadPlugin("OneClick")
if cmds.pluginInfo('fbxmaya', q=True, l=True) == False:
    cmds.loadPlugin("fbxmaya")


def fileDialog_import(cap=u'File'):
    filename = cmds.fileDialog2(ds=2, cap=cap, okc='Done', ff='All Files (*.*)', fm=1)
    if filename is None:
        return
    return filename[0]

# import:cog_jnt
def bake(sel, attrs=['tx', 'ty', 'tz']):
    try:
        cmds.refresh(su=1)
        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        cmds.bakeResults(sel, sm=1, t=(playmin, playmax), at=attrs, sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)

        cmds.filterCurve(sel, f='euler')
        cmds.refresh(su=0)
    except:
        cmds.refresh(su=0)

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


# sourceの切替
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

# --------------
# worldのリグに対しての処理
# --------------
namespace = 'male00_all1000_mdl_def:'
anim_jnt_sets = 'anim_jnt_sets'
root_jnt = 'root_jnt'
# anim_jnts = cmds.select(namespace + anim_jnt_sets, r=1, ne=1);cmds.pickWalk(d='down')

anim_jnts = cmds.ls(namespace + root_jnt, type='joint', dag=1)

# bake
to_hik_jt_array = []
to_hik_jt_cnst_array = []
for ch_jt in anim_jnts:
    to_hik_jt = ch_jt.replace(namespace, '')
    try:
        to_hik_jt_pa_cnst = cmds.parentConstraint(ch_jt, to_hik_jt, w=1)
        to_hik_jt_sc_cnst = cmds.scaleConstraint(ch_jt, to_hik_jt, w=1)
        to_hik_jt_array.append(to_hik_jt)
        to_hik_jt_cnst_array.append(to_hik_jt_pa_cnst[0])
        to_hik_jt_cnst_array.append(to_hik_jt_sc_cnst[0])
    except:
        pass


bake(to_hik_jt_array, attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])

for del_node in to_hik_jt_cnst_array:
    cmds.delete(del_node)
