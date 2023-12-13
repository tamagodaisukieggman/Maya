# -*- coding: utf-8 -*-
import copy
import os
from pyfbsdk import *

"""
camera property
MultiTake
DefaultKeyingGroup
DefaultKeyingGroupEnum
ManipulationMode
QuaternionInterpolate
Visibility
Visibility Inheritance
Lcl Translation
Lcl Rotation
Lcl Scaling
Primary Visibility
Casts Shadows
Receive Shadows
RotationOffset
RotationPivot
ScalingOffset
ScalingPivot
RotationPivotUpdateOffset
ScalingPivotUpdateOffset
TranslationActive
TranslationMin
TranslationMax
TranslationMinX
TranslationMinY
TranslationMinZ
TranslationMaxX
TranslationMaxY
TranslationMaxZ
RotationOrder
RotationSpaceForLimitOnly
AxisLen
PreRotation
PostRotation
RotationActive
RotationMin
RotationMax
RotationMinX
RotationMinY
RotationMinZ
RotationMaxX
RotationMaxY
RotationMaxZ
RotationStiffnessX
RotationStiffnessY
RotationStiffnessZ
MinDampRangeX
MinDampRangeY
MinDampRangeZ
MaxDampRangeX
MaxDampRangeY
MaxDampRangeZ
MinDampStrengthX
MinDampStrengthY
MinDampStrengthZ
MaxDampStrengthX
MaxDampStrengthY
MaxDampStrengthZ
PreferedAngleX
PreferedAngleY
PreferedAngleZ
SetPreferedAngle
InheritType
ScalingActive
ScalingMin
ScalingMax
ScalingMinX
ScalingMinY
ScalingMinZ
ScalingMaxX
ScalingMaxY
ScalingMaxZ
GeometricTranslation
GeometricRotation
GeometricScaling
PivotsVisibility
RotationLimitsVisibility
LocalTranslationRefVisibility
RotationRefVisibility
RotationAxisVisibility
ScalingRefVisibility
HierarchicalCenterVisibility
GeometricCenterVisibility
ReferentialSize
LookAtProperty
UpVectorProperty
Show
Pickable
Transformable
CullingMode
ShowTrajectories
NegativePercentShapeSupport
Roll
FieldOfView
FieldOfViewX
FieldOfViewY
OpticalCenterX
OpticalCenterY
BackgroundColor
TurnTable
DisplayTurnTableIcon
Motion Blur Intensity
UseMotionBlur
UseRealTimeMotionBlur
ResolutionMode
ApertureMode
GateFit
FocalLength
mAlsoKeyOnFOVProperty
CameraFormat
AspectW
AspectH
PixelAspectRatio
UseFrameColor
FrameColor
ShowName
ShowGrid
ShowOpticalCenter
ShowAzimut
ShowTimeCode
ShowBackplate
ShowFrontplate
NearPlane
FarPlane
FilmWidth
FilmHeight
FilmAspectRatio
FilmSqueezeRatio
FilmFormatIndex
ViewFrustumNearFarPlane
ViewFrustumBackPlaneMode
BackPlaneDistance
BackPlaneDistanceMode
ViewCameraToLookAt
LockMode
LockInterestNavigation
BackPlateFitImage
BackPlateCrop
BackPlateCenter
BackPlateKeepRatio
Background Texture
FrontPlateFitImage
FrontPlateCrop
FrontPlateCenter
FrontPlateKeepRatio
Foreground Opacity
BackgroundAlphaTreshold
ForegroundTransparent
Foreground Texture
ViewFrustumFrontPlaneMode
FrontPlaneDistance
FrontPlaneDistanceMode
DisplaySafeArea
SafeAreaDisplayStyle
SafeAreaAspectRatio
Use2DMagnifierZoom
Display2DMagnifierFrame
2D Magnifier Zoom
2D Magnifier X
2D Magnifier Y
CameraProjectionType
UseRealTimeDOFAndAA
UseDepthOfField
FocusSource
FocusAngle
FocusDistance
Focus Model
UseAntialiasing
AntialiasingIntensity
UseAccumulationBuffer
FrameSamplingCount
OrthoZoom
ResetCamera
AlsoKeyOnFOVProperty
UpVector
InterestPosition
AspectRatioMode
AspectWidth
AspectHeight
FilmOffsetX
FilmOffsetY
PreScale
FilmTranslateX
FilmTranslateY
FilmRollPivotX
FilmRollPivotY
FilmRollValue
FilmRollOrder
ShowInfoOnMoving
ShowAudio
AudioColor
AutoComputeClipPanes
BackPlaneOffsetX
BackPlaneOffsetY
BackPlaneRotation
BackPlaneScaleX
BackPlaneScaleY
FrontPlaneOffsetX
FrontPlaneOffsetY
FrontPlaneRotation
FrontPlaneScaleX
FrontPlaneScaleY
DisplaySafeAreaOnRender
AntialiasingMethod
FrameSamplingType
"""

def GetObj(name = None):
    u'''
    シーン内のコンポーネントを探索
    '''
    lComps = FBSystem().Scene.Components
    lGetObjects = [lCm for lCm in lComps if lCm.LongName == name]
    return lGetObjects


def Find_AnimationNode( pParent, pName ):
    u'''
    # Boxが指定された名前のノードを持っているかを調べる。
    '''
    lResult = None
    for lNode in pParent.Nodes:
        if lNode.Name == pName:
            lResult = lNode
            break
    return lResult


def BoxExists_In_RelationCnst(lConst = None, lExBox = None):
    u'''
    Relation Constraint 内にlExBoxが存在するかどうか
    '''
    for lBox in lConst.Boxes:
        if lBox.LongName == lExBox:
            return True
            break

    return False

fModels = []
lComps = FBSystem().Scene.Components
for lComp in lComps:
    if lComp.LongName == 'Camera':
        lComp_Camera = lComp

# Camera
print(lComp_Camera.LongName)

for camComp in lComp_Camera.PropertyList:
    if camComp.Name == 'ResolutionMode':
        camComp.Data = 2

    elif camComp.Name == 'ApertureMode':
        camComp.Data = 2


for camComp in lComp_Camera.PropertyList:
    if camComp.Name == 'FilmWidth':
        camComp.Data = 1.417

    elif camComp.Name == 'FilmHeight':
        camComp.Data = 0.945

    elif camComp.Name == 'FocalLength':
        camComp.Data = 28.971

    elif camComp.Name == 'Pickable':
        camComp.Data = 0


for camComp in lComp_Camera.PropertyList:
    if camComp.Name == 'CameraFormat':
        camComp.Data = 0

    elif camComp.Name == 'FilmFormatIndex':
        camComp.Data = 0

    elif camComp.Name == 'NearPlane':
        camComp.Data = 14

    elif camComp.Name == 'FarPlane':
        camComp.Data = 4000

# なぜか効かない場合がある
for camComp in lComp_Camera.PropertyList:
    if camComp.Name == 'AspectWidth':
        camComp.Data = 960

    elif camComp.Name == 'AspectHeight':
        camComp.Data = 540

# なぜかFocalLengthは2回やらないといけない
for camComp in lComp_Camera.PropertyList:
    if camComp.Name == 'FocalLength':
        camComp.Data = 28.971


for camComp in lComp_Camera.PropertyList:
    try:
        camComp.SetLocked(True)
    except RuntimeError:
        pass
