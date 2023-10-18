from maya import cmds, mel
import traceback

default_fbx_settings = {'Export': {'FBXExportAnimationOnly': 0,
            'FBXExportApplyConstantKeyReducer': 0,
            'FBXExportAudio': 1,
            'FBXExportAxisConversionMethod': 'convertAnimation',
            'FBXExportBakeComplexAnimation': 'false',
            'FBXExportBakeComplexEnd': 48,
            'FBXExportBakeComplexStart': 1,
            'FBXExportBakeComplexStep': 1,
            'FBXExportBakeResampleAnimation': 0,
            'FBXExportCacheFile': 0,
            'FBXExportCameras': 1,
            'FBXExportColladaFrameRate': 24.0,
            'FBXExportColladaSingleMatrix': 1,
            'FBXExportColladaTriangulate': 1,
            'FBXExportConstraints': 1,
            'FBXExportConvert2Tif': 0,
            'FBXExportConvertUnitString': 1.0,
            'FBXExportDeleteOriginalTakeOnSplitAnimation': 0,
            'FBXExportEmbeddedTextures': 0,
            'FBXExportFileVersion': 'FBX202000',
            'FBXExportFinestSubdivLevel': 0,
            'FBXExportGenerateLog': 1,
            'FBXExportHardEdges': 0,
            'FBXExportInAscii': 0,
            'FBXExportIncludeChildren': 1,
            'FBXExportInputConnections': 1,
            'FBXExportInstances': 0,
            'FBXExportLights': 1,
            'FBXExportQuaternion': 'resample',
            'FBXExportQuickSelectSetAsCache': ' ',
            'FBXExportReferencedAssetsContent': 1,
            'FBXExportScaleFactor': 1.0,
            'FBXExportShapeAttributeValues': 'Relative',
            'FBXExportShapeAttributes': 0,
            'FBXExportShapes': 1,
            'FBXExportShowUI': 'FBXExportShowUI is no longer supported via MEL '
                               'script.',
            'FBXExportSkeletonDefinitions': 1,
            'FBXExportSkins': 1,
            'FBXExportSmoothMesh': 1,
            'FBXExportSmoothingGroups': 0,
            'FBXExportSplitAnimationIntoTakes': 0,
            'FBXExportTangents': 0,
            'FBXExportTriangulate': 0,
            'FBXExportUpAxis': 'y',
            'FBXExportUseSceneName': 0,
            'FBXExportUseTmpFilePeripheral': 'Success',
            'FBXLoadMBExportPresetFile': None},
 'Import': {'FBXImportAudio': 1,
            'FBXImportAutoAxisEnable': 1,
            'FBXImportAxisConversionEnable': 0,
            'FBXImportCacheFile': 1,
            'FBXImportCameras': 1,
            'FBXImportConstraints': 1,
            'FBXImportConvertDeformingNullsToJoint': 1,
            'FBXImportConvertUnitString': None,
            'FBXImportFillTimeline': 0,
            'FBXImportForcedFileAxis': 'disabled',
            'FBXImportGenerateLog': 1,
            'FBXImportHardEdges': 0,
            'FBXImportLights': 1,
            'FBXImportMergeAnimationLayers': 0,
            'FBXImportMergeBackNullPivots': 1,
            'FBXImportMode': 'merge',
            'FBXImportProtectDrivenKeys': 0,
            'FBXImportQuaternion': 'resample',
            'FBXImportResamplingRateSource': 'File',
            'FBXImportScaleFactor': 1.0,
            'FBXImportSetLockedAttribute': 0,
            'FBXImportSetMayaFrameRate': 1,
            'FBXImportShapes': 1,
            'FBXImportShowUI': 'FBXImportShowUI is no longer supported via MEL '
                               'script.',
            'FBXImportSkeletonDefinitionsAs': 'humanik',
            'FBXImportSkins': 1,
            'FBXImportUnlockNormals': 0,
            'FBXImportUpAxis': 'y',
            'FBXLoadMBImportPresetFile': None},
 'Other': {'FBXPopSettings': 'Success',
           'FBXProperties': {'Export|AdvOptGrp|AxisConvGrp|UpAxis': 'Y',
                             'Export|AdvOptGrp|Collada|FrameRate': 24.0,
                             'Export|AdvOptGrp|Collada|SingleMatrix': 1,
                             'Export|AdvOptGrp|Collada|Triangulate': 1,
                             'Export|AdvOptGrp|Dxf|Deformation': 1,
                             'Export|AdvOptGrp|Dxf|Triangulate': 1,
                             'Export|AdvOptGrp|Fbx|AsciiFbx': 'Binary',
                             'Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionFrameRange': 1,
                             'Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionFrameRateUsed': 1,
                             'Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionTranslation': 1,
                             'Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionWriteDefaultAsBaseTR': 0,
                             'Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionFrameRange': 1,
                             'Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionFrameRateUsed': 1,
                             'Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionTranslation': 1,
                             'Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionWriteDefaultAsBaseTR': 0,
                             'Export|AdvOptGrp|FileFormat|Biovision_BVH|MotionTranslation': 1,
                             'Export|AdvOptGrp|FileFormat|Motion_Base|MotionASFSceneOwned': 1,
                             'Export|AdvOptGrp|FileFormat|Motion_Base|MotionC3DRealFormat': 0,
                             'Export|AdvOptGrp|FileFormat|Motion_Base|MotionFrameCount': 0,
                             'Export|AdvOptGrp|FileFormat|Motion_Base|MotionFrameRate': 30.0,
                             'Export|AdvOptGrp|FileFormat|Motion_Base|MotionFromGlobalPosition': 1,
                             'Export|AdvOptGrp|FileFormat|Motion_Base|MotionGapsAsValidData': 0,
                             'Export|AdvOptGrp|FileFormat|Obj|Deformation': 1,
                             'Export|AdvOptGrp|FileFormat|Obj|Triangulate': 1,
                             'Export|AdvOptGrp|UI|GenerateLogData': 1,
                             'Export|AdvOptGrp|UI|ShowWarningsManager': 1,
                             'Export|AdvOptGrp|UnitsGrp|DynamicScaleConversion': 1,
                             'Export|AdvOptGrp|UnitsGrp|UnitsSelector': 'Centimeters',
                             'Export|IncludeGrp|Animation': 1,
                             'Export|IncludeGrp|Animation|BakeComplexAnimation': 0,
                             'Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameEnd': 48,
                             'Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStart': 1,
                             'Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStep': 1,
                             'Export|IncludeGrp|Animation|BakeComplexAnimation|HideComplexAnimationBakedWarning': 0,
                             'Export|IncludeGrp|Animation|BakeComplexAnimation|ResampleAnimationCurves': 0,
                             'Export|IncludeGrp|Animation|ConstraintsGrp|Character': 1,
                             'Export|IncludeGrp|Animation|ConstraintsGrp|Constraint': 1,
                             'Export|IncludeGrp|Animation|CurveFilter': 0,
                             'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed': 0,
                             'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|AutoTangentsOnly': 1,
                             'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedOPrec': 0.009,
                             'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedRPrec': 0.009,
                             'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedSPrec': 0.004,
                             'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedTPrec': 0.0001,
                             'Export|IncludeGrp|Animation|Deformation': 1,
                             'Export|IncludeGrp|Animation|Deformation|Shape': 1,
                             'Export|IncludeGrp|Animation|Deformation|ShapeAttributes': 0,
                             'Export|IncludeGrp|Animation|Deformation|ShapeAttributes|ShapeAttributesValues': 'Relative',
                             'Export|IncludeGrp|Animation|Deformation|Skins': 1,
                             'Export|IncludeGrp|Animation|ExtraGrp|Quaternion': 'Resample '
                                                                                'As '
                                                                                'Euler '
                                                                                'Interpolation',
                             'Export|IncludeGrp|Animation|ExtraGrp|RemoveSingleKey': 0,
                             'Export|IncludeGrp|Animation|ExtraGrp|UseSceneName': 0,
                             'Export|IncludeGrp|Animation|PointCache': 0,
                             'Export|IncludeGrp|Animation|PointCache|SelectionSetNameAsPointCache': ' ',
                             'Export|IncludeGrp|Audio': 1,
                             'Export|IncludeGrp|BindPose': 1,
                             'Export|IncludeGrp|BypassRrsInheritance': 0,
                             'Export|IncludeGrp|CameraGrp|Camera': 1,
                             'Export|IncludeGrp|EmbedTextureGrp|EmbedTexture': 0,
                             'Export|IncludeGrp|Geometry|AnimationOnly': 0,
                             'Export|IncludeGrp|Geometry|BlindData': 1,
                             'Export|IncludeGrp|Geometry|ContainerObjects': 1,
                             'Export|IncludeGrp|Geometry|GeometryNurbsSurfaceAs': 'NURBS',
                             'Export|IncludeGrp|Geometry|Instances': 0,
                             'Export|IncludeGrp|Geometry|SelectionSet': 0,
                             'Export|IncludeGrp|Geometry|SmoothMesh': 1,
                             'Export|IncludeGrp|Geometry|SmoothingGroups': 0,
                             'Export|IncludeGrp|Geometry|TangentsandBinormals': 0,
                             'Export|IncludeGrp|Geometry|Triangulate': 0,
                             'Export|IncludeGrp|Geometry|expHardEdges': 0,
                             'Export|IncludeGrp|InputConnectionsGrp|IncludeChildren': 1,
                             'Export|IncludeGrp|InputConnectionsGrp|InputConnections': 1,
                             'Export|IncludeGrp|LightGrp|Light': 1,
                             'Export|IncludeGrp|PivotToNulls': 0,
                             'Export|PlugInGrp|PlugInUIHeight': 500,
                             'Export|PlugInGrp|PlugInUIWidth': 500,
                             'Export|PlugInGrp|PlugInUIXpos': 100,
                             'Export|PlugInGrp|PlugInUIYpos': 100,
                             'Export|PlugInGrp|UILIndex': 'ENU',
                             'Import|AdvOptGrp|AxisConvGrp|AxisConversion': 0,
                             'Import|AdvOptGrp|AxisConvGrp|UpAxis': 'Y',
                             'Import|AdvOptGrp|Dxf|ObjectDerivation': 'By '
                                                                      'layer',
                             'Import|AdvOptGrp|Dxf|ReferenceNode': 1,
                             'Import|AdvOptGrp|Dxf|WeldVertices': 1,
                             'Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionBaseRInPrerotation': 1,
                             'Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionBaseTInOffset': 1,
                             'Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionCreateReferenceNode': 1,
                             'Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionDummyNodes': 1,
                             'Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionLimits': 1,
                             'Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionBaseRInPrerotation': 1,
                             'Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionBaseTInOffset': 1,
                             'Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionCreateReferenceNode': 1,
                             'Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionDummyNodes': 1,
                             'Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionLimits': 1,
                             'Import|AdvOptGrp|FileFormat|Biovision_BVH|MotionCreateReferenceNode': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|AmbientLight': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|Animation': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|Camera': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|Filter': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|Light': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|Material': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|Mesh': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|ReferenceNode': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|Rescaling': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|Smoothgroup': 1,
                             'Import|AdvOptGrp|FileFormat|Max_3ds|Texture': 1,
                             'Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionBaseRInPrerotation': 1,
                             'Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionBaseTInOffset': 1,
                             'Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionCreateReferenceNode': 1,
                             'Import|AdvOptGrp|FileFormat|Motion_Base|MotionASFSceneOwned': 1,
                             'Import|AdvOptGrp|FileFormat|Motion_Base|MotionActorPrefix': 1,
                             'Import|AdvOptGrp|FileFormat|Motion_Base|MotionAsOpticalSegments': 1,
                             'Import|AdvOptGrp|FileFormat|Motion_Base|MotionExactZeroAsOccluded': 1,
                             'Import|AdvOptGrp|FileFormat|Motion_Base|MotionFrameCount': 0,
                             'Import|AdvOptGrp|FileFormat|Motion_Base|MotionFrameRate': 0.0,
                             'Import|AdvOptGrp|FileFormat|Motion_Base|MotionRenameDuplicateNames': 1,
                             'Import|AdvOptGrp|FileFormat|Motion_Base|MotionSetOccludedToLastValidPos': 1,
                             'Import|AdvOptGrp|FileFormat|Motion_Base|MotionUpAxisUsedInFile': 3,
                             'Import|AdvOptGrp|FileFormat|Obj|ReferenceNode': 1,
                             'Import|AdvOptGrp|Performance|RemoveBadPolysFromMesh': 1,
                             'Import|AdvOptGrp|UI|GenerateLogData': 1,
                             'Import|AdvOptGrp|UI|ShowWarningsManager': 1,
                             'Import|AdvOptGrp|UnitsGrp|DynamicScaleConversion': 0,
                             'Import|AdvOptGrp|UnitsGrp|UnitsSelector': 'Centimeters',
                             'Import|IncludeGrp|Animation': 1,
                             'Import|IncludeGrp|Animation|ConstraintsGrp|CharacterType': 'HumanIK',
                             'Import|IncludeGrp|Animation|ConstraintsGrp|Constraint': 1,
                             'Import|IncludeGrp|Animation|CurveFilter': 0,
                             'Import|IncludeGrp|Animation|Deformation': 1,
                             'Import|IncludeGrp|Animation|Deformation|ForceWeightNormalize': 0,
                             'Import|IncludeGrp|Animation|Deformation|Shape': 1,
                             'Import|IncludeGrp|Animation|Deformation|Skins': 1,
                             'Import|IncludeGrp|Animation|ExtraGrp|BakeAnimationLayers': 0,
                             'Import|IncludeGrp|Animation|ExtraGrp|DeformNullsAsJoints': 1,
                             'Import|IncludeGrp|Animation|ExtraGrp|Markers': 0,
                             'Import|IncludeGrp|Animation|ExtraGrp|NullsToPivot': 1,
                             'Import|IncludeGrp|Animation|ExtraGrp|PointCache': 1,
                             'Import|IncludeGrp|Animation|ExtraGrp|ProtectDrivenKeys': 0,
                             'Import|IncludeGrp|Animation|ExtraGrp|Quaternion': 'Resample '
                                                                                'As '
                                                                                'Euler '
                                                                                'Interpolation',
                             'Import|IncludeGrp|Animation|ExtraGrp|Take': 'No '
                                                                          'Animation',
                             'Import|IncludeGrp|Animation|ExtraGrp|TimeLine': 0,
                             'Import|IncludeGrp|Animation|SamplingPanel|CurveFilterSamplingRate': 30.0,
                             'Import|IncludeGrp|Animation|SamplingPanel|SamplingRateSelector': 'File',
                             'Import|IncludeGrp|Audio': 1,
                             'Import|IncludeGrp|CameraGrp|Camera': 1,
                             'Import|IncludeGrp|Geometry|BlindData': 1,
                             'Import|IncludeGrp|Geometry|HardEdges': 0,
                             'Import|IncludeGrp|Geometry|UnlockNormals': 0,
                             'Import|IncludeGrp|LightGrp|Light': 1,
                             'Import|IncludeGrp|MergeMode': 'Add and update '
                                                            'animation',
                             'Import|PlugInGrp|PlugInUIHeight': 500,
                             'Import|PlugInGrp|PlugInUIWidth': 500,
                             'Import|PlugInGrp|PlugInUIXpos': 100,
                             'Import|PlugInGrp|PlugInUIYpos': 100,
                             'Import|PlugInGrp|UILIndex': 'ENU'},
           'FBXPushSettings': 'Success',
           'FBXResamplingRate': 30.0,
           'FBXUICallBack': None,
           'FBXUIShowOptions': None}}


def get_current_fbx_settings():
    fbx_properties = {
        'Import|PlugInGrp|PlugInUIWidth':500, #   ( TYPE: Integer ) ( VALUE: 500 ) #
        'Import|PlugInGrp|PlugInUIHeight':500, #    ( TYPE: Integer ) ( VALUE: 500 ) #
        'Import|PlugInGrp|PlugInUIXpos':100, #    ( TYPE: Integer ) ( VALUE: 100 ) #
        'Import|PlugInGrp|PlugInUIYpos':100, #    ( TYPE: Integer ) ( VALUE: 100 ) #
        'Import|PlugInGrp|UILIndex':'ENU', #    ( TYPE: Enum )  ( VALUE: "ENU" )  (POSSIBLE VALUES: "ENU" "DEU" "FRA" "JPN" "KOR" "CHS" "PTB"  ) #
        'Import|IncludeGrp|MergeMode':'Add and update animation', #    ( TYPE: Enum )  ( VALUE: "Add and update animation" )  (POSSIBLE VALUES: "Add" "Add and update animation" "Update animation" "Update animation (keyed transforms)"  ) #
        'Import|IncludeGrp|Geometry|UnlockNormals':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Import|IncludeGrp|Geometry|HardEdges':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Import|IncludeGrp|Geometry|BlindData':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Animation':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Animation|ExtraGrp|Take':'No Animation', #    ( TYPE: Enum )  ( VALUE: "No Animation" )  (POSSIBLE VALUES: "No Animation"  ) #
        'Import|IncludeGrp|Animation|ExtraGrp|TimeLine':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Import|IncludeGrp|Animation|ExtraGrp|BakeAnimationLayers':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Animation|ExtraGrp|Markers':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Import|IncludeGrp|Animation|ExtraGrp|Quaternion':'Resample As Euler Interpolation', #    ( TYPE: Enum )  ( VALUE: "Resample As Euler Interpolation" )  (POSSIBLE VALUES: "Retain Quaternion Interpolation" "Set As Euler Interpolation" "Resample As Euler Interpolation"  ) #
        'Import|IncludeGrp|Animation|ExtraGrp|ProtectDrivenKeys':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Import|IncludeGrp|Animation|ExtraGrp|DeformNullsAsJoints':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Animation|ExtraGrp|NullsToPivot':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Animation|ExtraGrp|PointCache':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Animation|Deformation':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Animation|Deformation|Skins':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Animation|Deformation|Shape':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Animation|Deformation|ForceWeightNormalize':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Import|IncludeGrp|Animation|SamplingPanel|SamplingRateSelector':'File', #   ( TYPE: Enum )  ( VALUE: "File" )  (POSSIBLE VALUES: "Scene" "File" "Custom"  ) #
        'Import|IncludeGrp|Animation|SamplingPanel|CurveFilterSamplingRate':30.000000, #    ( TYPE: Number ) ( VALUE: 30.000000 ) #
        'Import|IncludeGrp|Animation|CurveFilter':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Import|IncludeGrp|Animation|ConstraintsGrp|Constraint':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Animation|ConstraintsGrp|CharacterType':'HumanIK', #    ( TYPE: Enum )  ( VALUE: "HumanIK" )  (POSSIBLE VALUES: "None" "HumanIK"  ) #
        'Import|IncludeGrp|CameraGrp|Camera':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|LightGrp|Light':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|IncludeGrp|Audio':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|UnitsGrp|DynamicScaleConversion':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|UnitsGrp|UnitsSelector':'Centimeters', #    ( TYPE: Enum )  ( VALUE: "Centimeters" )  (POSSIBLE VALUES: "Millimeters" "Centimeters" "Decimeters" "Meters" "Kilometers" "Inches" "Feet" "Yards" "Miles"  ) #
        'Import|AdvOptGrp|AxisConvGrp|AxisConversion':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Import|AdvOptGrp|AxisConvGrp|UpAxis':'Y', #    ( TYPE: Enum )  ( VALUE: "Y" )  (POSSIBLE VALUES: "Y" "Z"  ) #
        'Import|AdvOptGrp|UI|ShowWarningsManager':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|UI|GenerateLogData':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Obj|ReferenceNode':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|ReferenceNode':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|Texture':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|Material':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|Animation':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|Mesh':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|Light':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|Camera':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|AmbientLight':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|Rescaling':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|Filter':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Max_3ds|Smoothgroup':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Motion_Base|MotionFrameCount':0, #    ( TYPE: Integer ) ( VALUE: 0 ) #
        'Import|AdvOptGrp|FileFormat|Motion_Base|MotionFrameRate':0.000000, #    ( TYPE: Number ) ( VALUE: 0.000000 ) #
        'Import|AdvOptGrp|FileFormat|Motion_Base|MotionActorPrefix':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Motion_Base|MotionRenameDuplicateNames':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Motion_Base|MotionExactZeroAsOccluded':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Motion_Base|MotionSetOccludedToLastValidPos':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Motion_Base|MotionAsOpticalSegments':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Motion_Base|MotionASFSceneOwned':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Motion_Base|MotionUpAxisUsedInFile':3, #    ( TYPE: Integer ) ( VALUE: 3 ) #
        'Import|AdvOptGrp|FileFormat|Biovision_BVH|MotionCreateReferenceNode':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionCreateReferenceNode':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionBaseTInOffset':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|MotionAnalysis_HTR|MotionBaseRInPrerotation':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionCreateReferenceNode':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionDummyNodes':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionLimits':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionBaseTInOffset':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Acclaim_ASF|MotionBaseRInPrerotation':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionCreateReferenceNode':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionDummyNodes':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionLimits':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionBaseTInOffset':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|FileFormat|Acclaim_AMC|MotionBaseRInPrerotation':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|Dxf|WeldVertices':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|Dxf|ObjectDerivation':'By layer', #    ( TYPE: Enum )  ( VALUE: "By layer" )  (POSSIBLE VALUES: "By layer" "By entity" "By block"  ) #
        'Import|AdvOptGrp|Dxf|ReferenceNode':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Import|AdvOptGrp|Performance|RemoveBadPolysFromMesh':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|PlugInGrp|PlugInUIWidth':500, #    ( TYPE: Integer ) ( VALUE: 500 ) #
        'Export|PlugInGrp|PlugInUIHeight':500, #    ( TYPE: Integer ) ( VALUE: 500 ) #
        'Export|PlugInGrp|PlugInUIXpos':100, #    ( TYPE: Integer ) ( VALUE: 100 ) #
        'Export|PlugInGrp|PlugInUIYpos':100, #    ( TYPE: Integer ) ( VALUE: 100 ) #
        'Export|PlugInGrp|UILIndex':'ENU', #    ( TYPE: Enum )  ( VALUE: "ENU" )  (POSSIBLE VALUES: "ENU" "DEU" "FRA" "JPN" "KOR" "CHS" "PTB"  ) #
        'Export|IncludeGrp|Geometry|SmoothingGroups':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Geometry|expHardEdges':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Geometry|TangentsandBinormals':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Geometry|SmoothMesh':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|Geometry|SelectionSet':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Geometry|BlindData':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|Geometry|AnimationOnly':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Geometry|Instances':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Geometry|ContainerObjects':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|Geometry|Triangulate':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Geometry|GeometryNurbsSurfaceAs':'NURBS', #    ( TYPE: Enum )  ( VALUE: "NURBS" )  (POSSIBLE VALUES: "NURBS" "Interactive Display Mesh" "Software Render Mesh"  ) #
        'Export|IncludeGrp|Animation':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|Animation|ExtraGrp|UseSceneName':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Animation|ExtraGrp|RemoveSingleKey':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Animation|ExtraGrp|Quaternion':'Resample As Euler Interpolation', #    ( TYPE: Enum )  ( VALUE: "Resample As Euler Interpolation" )  (POSSIBLE VALUES: "Retain Quaternion Interpolation" "Set As Euler Interpolation" "Resample As Euler Interpolation"  ) #
        'Export|IncludeGrp|Animation|BakeComplexAnimation':'false',  #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStart':1,  #    ( TYPE: Integer ) ( VALUE: 1 ) #
        'Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameEnd':48,  #    ( TYPE: Integer ) ( VALUE: 48 ) #
        'Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStep':1,  #    ( TYPE: Integer ) ( VALUE: 1 ) #
        'Export|IncludeGrp|Animation|BakeComplexAnimation|ResampleAnimationCurves':'false',  #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Animation|BakeComplexAnimation|HideComplexAnimationBakedWarning':'false',  #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Animation|Deformation':'true',  #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|Animation|Deformation|Skins':'true',  #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|Animation|Deformation|Shape':'true',  #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|Animation|Deformation|ShapeAttributes':'false',  #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Animation|Deformation|ShapeAttributes|ShapeAttributesValues':'Relative',  #    ( TYPE: Enum )  ( VALUE: "Relative" )  (POSSIBLE VALUES: "Relative" "Absolute"  ) #
        'Export|IncludeGrp|Animation|CurveFilter':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedTPrec':0.000100, #    ( TYPE: Number ) ( VALUE: 0.000100 ) #
        'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedRPrec':0.009000, #    ( TYPE: Number ) ( VALUE: 0.009000 ) #
        'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedSPrec':0.004000, #    ( TYPE: Number ) ( VALUE: 0.004000 ) #
        'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedOPrec':0.009000, #    ( TYPE: Number ) ( VALUE: 0.009000 ) #
        'Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|AutoTangentsOnly':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|Animation|PointCache':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|Animation|PointCache|SelectionSetNameAsPointCache':' ', #    ( TYPE: Enum )  ( VALUE: " " )  (POSSIBLE VALUES: " " "defaultLightSet" "defaultObjectSet"  ) #
        'Export|IncludeGrp|Animation|ConstraintsGrp|Constraint':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|Animation|ConstraintsGrp|Character':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|CameraGrp|Camera':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|LightGrp|Light':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|Audio':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|EmbedTextureGrp|EmbedTexture':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|BindPose':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|PivotToNulls':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|BypassRrsInheritance':'false', #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|IncludeGrp|InputConnectionsGrp|IncludeChildren':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|IncludeGrp|InputConnectionsGrp|InputConnections':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|UnitsGrp|DynamicScaleConversion':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|UnitsGrp|UnitsSelector':'Centimeters', #    ( TYPE: Enum )  ( VALUE: "Centimeters" )  (POSSIBLE VALUES: "Millimeters" "Centimeters" "Decimeters" "Meters" "Kilometers" "Inches" "Feet" "Yards" "Miles"  ) #
        'Export|AdvOptGrp|AxisConvGrp|UpAxis':'Y', #    ( TYPE: Enum )  ( VALUE: "Y" )  (POSSIBLE VALUES: "Y" "Z"  ) #
        'Export|AdvOptGrp|UI|ShowWarningsManager':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|UI|GenerateLogData':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Obj|Triangulate':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Obj|Deformation':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Motion_Base|MotionFrameCount':0, #    ( TYPE: Integer ) ( VALUE: 0 ) #
        'Export|AdvOptGrp|FileFormat|Motion_Base|MotionFromGlobalPosition':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Motion_Base|MotionFrameRate':30.000000, #    ( TYPE: Number ) ( VALUE: 30.000000 ) #
        'Export|AdvOptGrp|FileFormat|Motion_Base|MotionGapsAsValidData':'false',  #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|AdvOptGrp|FileFormat|Motion_Base|MotionC3DRealFormat':'false',  #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|AdvOptGrp|FileFormat|Motion_Base|MotionASFSceneOwned':'true',  #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Biovision_BVH|MotionTranslation':'true',  #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionTranslation':'true',  #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionFrameRateUsed':'true',  #   ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionFrameRange':'true',  #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Acclaim_ASF|MotionWriteDefaultAsBaseTR':'false',  #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionTranslation':'true',  #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionFrameRateUsed':'true',  #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionFrameRange':'true',  #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|FileFormat|Acclaim_AMC|MotionWriteDefaultAsBaseTR':'false',  #    ( TYPE: Bool ) ( VALUE: "false" ) #
        'Export|AdvOptGrp|Fbx|AsciiFbx':'Binary',  #    ( TYPE: Enum )  ( VALUE: "Binary" )  (POSSIBLE VALUES: "Binary" "ASCII"  ) #
        'Export|AdvOptGrp|Fbx|ExportFileVersion':'FBX202000', #    ( TYPE: Alias )  ( VALUE: "FBX202000" )  (POSSIBLE VALUES: "FBX202000" "FBX201900" "FBX201800" "FBX201600" "FBX201400" "FBX201300" "FBX201200" "FBX201100" "FBX201000" "FBX200900" "FBX200611"  ) #
        'Export|AdvOptGrp|Dxf|Deformation':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|Dxf|Triangulate':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|Collada|Triangulate':'true', #    ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|Collada|SingleMatrix':'true', #     ( TYPE: Bool ) ( VALUE: "true" ) #
        'Export|AdvOptGrp|Collada|FrameRate':24.000000 #    ( TYPE: Number ) ( VALUE: 24.000000 ) #
    }

    fbx_cmds = [cmd for cmd in cmds.__dict__.keys() if 'FBX' in cmd]
    fbx_exclude = [
        'OpenFBXReview',
        'FBXImport',
        'FBXExport',
        'FBXResetImport',
        'FBXResetExport',
        'FBXExtPlugin',
        'FBXImportOCMerge',
        'FBXLoadImportPresetFile',
        'FBXLoadExportPresetFile',
        'FBXImportSetTake',
        'FBXExportReferencedContainersContent',
        'FBXRead',
        'FBXClose',
        'FBXGetTakeCount',
        'FBXGetTakeIndex',
        'FBXGetTakeName',
        'FBXGetTakeComment',
        'FBXGetTakeLocalTimeSpan',
        'FBXGetTakeReferenceTimeSpan',
        'FBXProperty',
    ]
    fbx_true_settings = {}

    fbx_properties_errors = list()
    for fbx_cmd in fbx_cmds:
        if not fbx_cmd in fbx_exclude:
            if 'Import' in fbx_cmd:
                if not 'Import' in fbx_true_settings.keys():
                    fbx_true_settings['Import'] = {}
                fbx_true_settings['Import'][fbx_cmd] = mel.eval('{} -q;'.format(fbx_cmd))

            elif 'Export' in fbx_cmd:
                if not 'Export' in fbx_true_settings.keys():
                    fbx_true_settings['Export'] = {}
                fbx_true_settings['Export'][fbx_cmd] = mel.eval('{} -q;'.format(fbx_cmd))

            else:
                if not 'Other' in fbx_true_settings.keys():
                    fbx_true_settings['Other'] = {}
                fbx_true_settings['Other'][fbx_cmd] = mel.eval('{} -q;'.format(fbx_cmd))

                if 'FBXProperties' == fbx_cmd:
                    fbx_true_settings['Other'][fbx_cmd] = {}
                    for prk, prv in fbx_properties.items():
                        try:
                            fbx_true_settings['Other'][fbx_cmd][prk] = mel.eval('FBXProperty {} -q;'.format(prk))
                        except:
                            fbx_properties_errors.append(prk)

    fbx_true_settings = dict(sorted(fbx_true_settings.items()))
    return fbx_true_settings

# fbx_true_settings['Other']['FBXProperties']
# このアトリビュートが
# mel.eval('FBXProperty Import|AdvOptGrp|UnitsGrp|DynamicScaleConversion -v 0;')
# mel.eval('FBXProperty Import|IncludeGrp|Animation|ExtraGrp|BakeAnimationLayers -v 0;')

fbx_true_settings = get_current_fbx_settings()

fbx_true_settings = default_fbx_settings

fbx_cmd_type = 'Import'
for fbx_cmd_type_key, fbx_cmd_val in fbx_true_settings.items():
    # Import FBX
    if fbx_cmd_type_key == fbx_cmd_type:
        for fbx_im_cmd, fbx_im_cmd_val in fbx_cmd_val.items():
            if fbx_im_cmd_val:
                if ('FBXImportShowUI' != fbx_im_cmd):
                    if ('FBXImportScaleFactor' == fbx_im_cmd
                        or 'FBXImportUpAxis' == fbx_im_cmd
                        or 'FBXImportAutoAxisEnable' == fbx_im_cmd):
                        mel.eval('{} {};'.format(fbx_im_cmd, fbx_im_cmd_val))
                    else:
                        mel.eval('{} -v {};'.format(fbx_im_cmd, fbx_im_cmd_val))

    elif fbx_cmd_type_key == 'Other':
        for fbx_im_cmd, fbx_im_cmd_val in fbx_cmd_val.items():
            if fbx_im_cmd == 'FBXProperties':
                for fbx_cmd_prp, fbx_cmd_prp_val in fbx_im_cmd_val.items():
                    if ('Import|IncludeGrp|MergeMode' == fbx_cmd_prp
                        or 'Import|IncludeGrp|Animation|ExtraGrp|Take' == fbx_cmd_prp
                        or 'Import|IncludeGrp|Animation|ExtraGrp|Quaternion' == fbx_cmd_prp
                        or 'Import|AdvOptGrp|Dxf|ObjectDerivation' == fbx_cmd_prp
                        or 'Export|IncludeGrp|Animation|ExtraGrp|Quaternion' == fbx_cmd_prp
                        or 'Export|IncludeGrp|Animation|PointCache|SelectionSetNameAsPointCache' == fbx_cmd_prp):
                        mel.eval('FBXProperty {} -v "{}";'.format(fbx_cmd_prp, fbx_cmd_prp_val))
                    else:
                        mel.eval('FBXProperty {} -v {};'.format(fbx_cmd_prp, fbx_cmd_prp_val))
            else:
                mel.eval('{} -v {};'.format(fbx_im_cmd, fbx_im_cmd_val))
